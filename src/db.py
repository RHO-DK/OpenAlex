import psycopg2

try:
    from config import OA_DB_NAME, OA_LOG_PATH_DB
    if not isinstance(OA_DB_NAME, str) or not OA_DB_NAME.strip():
        raise ValueError("OA_DB_NAME er ikke defineret korrekt i config.py")
    if not isinstance(OA_LOG_PATH_DB, str) or not OA_LOG_PATH_DB.strip():
        raise ValueError("OA_LOG_PATH_DB er ikke defineret korrekt i config.py")
except ImportError as e:
    raise ImportError("config.py kunne ikke importeres -  mangler filen?") from e


import logging
import traceback


# ------------------------------------------------------------
# NOTE og TODO om fremmednøgler  og datavalidering
#
# I dette script er fremmednøgle-begrænsninger (constraints) udeladt til efter parsing, se hvilke og årsag nedenfor.:
#
# Tabeller med udskudte fremmednøgler:
# - authorships → works, authors, institutions
# - work_topics → works, topics
# - work_concepts → works, concepts
# - topics → subfields, fields, domains
# - fields → domains
# - subfields → fields
# - citations → works (citing/cited)
# - evt works → institutions via host_venue_ror
# - evt authors → orcid (validering mod ORCID)
#
#
# Fremmednøgler integreres fuld ud efter validering.
#
#
# Årsagen er praktisk: Ved parsing og import af data fra OpenAlex (og senere ROR/ORCID)
# kan der ske henvisninger til rækker (fx work_id, concept_id), som endnu ikke
# findes i databasen på tidspunktet for indsættelse, og dette kan betyde en unødvendig komplex og meget lidt automatiseret parsing
#
# Ved at udskyde tilføjelsen af FK-constraints undgås INSERT-fejl under opbygningen
# af databasen. Når datasættet er komplet og valideret, kan constraints tilføjes
# med ALTER TABLE-kommandoer.
#
# Datavalidering:  – Muliggør kontrolleret og struktureret
# opbygning med validering i parseren og mulighed for efterfølgende
# fremmednøgle indsættelse via alter table.
# Der er endvidere andre indbyggede constrataints i db strukturen - primærnøgler, enestående og kombinerede, anvendelse af unikke identitteter, 
# ------------------------------------------------------------


#---Logging - both by log and print - NB: logging.INFO - kan ændres til niveau DEBUG hvis mere detaljeret niveau relevant for simulering af fejl fx.

# logfil-handler
file_handler = logging.FileHandler(OA_LOG_PATH_DB)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# konsol-handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

# combo
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])


#---connect og creating tables

def connect_db():
    return psycopg2.connect(dbname=OA_DB_NAME, user="postgres")

def create_tables():
    try:
        conn = connect_db()
        cur = conn.cursor()
        
        #---works
        try:
            logging.info("Opretter works")
            
            cur.execute("""
            CREATE TABLE IF NOT EXISTS works (
                work_id TEXT PRIMARY KEY,
                doi TEXT UNIQUE,
                title TEXT,
                publication_date DATE,
                publication_year INTEGER,
                type TEXT,
                language TEXT,
                cited_by_count INTEGER,
                is_oa BOOLEAN,
                license TEXT,
                host_venue_name TEXT,
                host_venue_issn TEXT,
                host_venue_ror TEXT,
                created_date DATE
        
            );
            """)

            conn.commit()
            
            # log check
            logging.info("Tabel works oprettet")
            

        except Exception as e:
            logging.error(f"Fejl ved oprettelse af tabel works: {e}")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
        
        #indexering
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_works_ror ON works (host_venue_ror);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_works_citations ON works (cited_by_count);")
        
            conn.commit()
            
            logging.info("Indexering for works er oprettet")
        
        except Exception as e:
            logging.error(f"fejl ved oprettelse af indeksering for works: {e}")
            logging.debug(traceback.format_exc())
            conn.rollback 
            
            
        
        #--- authorships
        
        try:
            logging.info("Opretter authorships")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS authorships (
                work_id TEXT,
                author_id TEXT,
                institution_id TEXT,
                author_position TEXT, 
                is_corresponding BOOLEAN,
                PRIMARY KEY (work_id, author_id),

            );
            """)

            conn.commit()
        
            # log check
            logging.info("Tabel works oprettet")
            

        except Exception as e:
            logging.error(f"Fejl ved oprettelse af tabel authorships: {e}")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
            
        #indexering
        
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_authorships_work_id ON authorships (work_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_authorships_author_id ON authorships (author_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_authorships_institution_id ON authorships (institution_id);")
        
            conn.commit()
            
            logging.info("Indexering for authorships er oprettet")
        
        except Exception as e:
            logging.error(f"fejl ved oprettelse af indeksering for authorships: {e}")
            logging.debug(traceback.format_exc())
            conn.rollback 
            
            
        
        #---authors
        
        try:
            logging.info("Opretter authors")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                author_id TEXT PRIMARY KEY,
                name TEXT,
                orcid TEXT UNIQUE
            );
            """)

            conn.commit()

            # log check
            logging.info("Tabel authors oprettet")
                
        except Exception as e:
            logging.error(f"Fejl ved oprettelse af tabel authors: {e}")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
            
        #indexering  
        try:   
            cur.execute("CREATE INDEX IF NOT EXISTS idx_authors_name ON authors (name);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_authors_orcid ON authors(orcid);")
            
            conn.commit()
            
        except Exception as e:
            logging.error(f"fejl ved oprettelse af indeksering for authorshs: {e}")
            logging.debug(traceback.format_exc())
            conn.rollback 
            
    
            
        #---topics
        
        try:
            logging.info("Opretter topics")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                topic_id TEXT PRIMARY KEY,
                display_name TEXT,
                subfield_id TEXT,
                field_id TEXT,
                domain_id TEXT
            
            );
            """)

            conn.commit()
            
            # log check
            logging.info("Tabel topics oprettet")
        
        except Exception as e:
            logging.error(f"Fejl ved oprettelse af topics tabel: {e}")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
            
        #indexering:
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_topics_subfield_id ON topics (subfield_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_topics_field_id ON topics (field_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_topics_domain_id ON topics (domain_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_topics_display_name ON topics (display_name);")
            
            conn.commit()
        
        except Exception as e:
            logging.error(f"Fejl ved indeksering af topics tabel: {e}")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
        
        #---domains
        
        try:
            logging.info("Opretter domains")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS domains (
                domain_id TEXT PRIMARY KEY,
                domain_name TEXT
            );
            """)

            conn.commit()
            
            logging.info("oprettet domains table")
            
        except Exception as e:
            logging.error(f"Fej ved oprettelse af domains table: {e}")
            logging.debug(traceback.format_exc())
            conn.roolback()


        #---fields
        
        try:
            logging.info("Opretter fields")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS fields (
                field_id TEXT PRIMARY KEY,
                field_name TEXT,
                domain_id TEXT
            );
            """)

            conn.commit()
            
            logging.info("fields table oprettet")
            
        except Exception as e:
            logging.error(f"Fejl ved oprettelse af fields table")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
        

        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_fields_domain_id ON fields (domain_id);")
        
            conn.commit()
            
        except Exception as e:
            logging.error(f"fejl ved indeksering af fields table")
            logging.debug(traceback.format_exc())
            conn.rollback()
            

    #---subfields
        
        try:
            logging.info("Opretter subfields")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS subfields (
                subfield_id TEXT PRIMARY KEY,
                subfield_name TEXT,
                field_id TEXT
            );
            """)

            conn.commit()

            # log check
            logging.info("subfields tabel oprettet")
            
        except Exception as e:
            logging.error(f"fejl under oprettelse af subfields tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
                
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_subfields_field_id ON subfields (field_id);")
        
            conn.commit()
            
        except Exception as e:
            logging.error(f"fejl under indeksering af subfields tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
            
        
        #---work_topics
        
        try:
            logging.info("Opretter work_topics")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS work_topics (
                work_id TEXT,
                topic_id TEXT,
                score FLOAT,
                is_primary BOOLEAN,
                PRIMARY KEY (work_id, topic_id),

            );
            """)
            
            conn.commit()

            # log check
            logging.info("Tabel work_topics oprettet")
            
        except Exception as e:
            logging.error(f"fejl under oprettelse af work_topics tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
    
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_work_topics_work_id ON work_topics (work_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_work_topics_topic_id ON work_topics (topic_id);")

            conn.commit()
            
        except Exception as e:
            logging.error(f"fejl under indexering af work_topics tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            

                
        #---concepts
        
        try:
            logging.info("Opretter concepts")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                concept_id TEXT PRIMARY KEY,
                display_name TEXT,
                level INTEGER,
                wikidata_id TEXT
            );
            """)

            conn.commit()
            
            logging.info("Tabel concepts oprettet")
            
        except Exception as e:
            logging.error(f"fejl under oprettelse af concepts tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
            

        #---work_concepts
        
        try:
            logging.info("Opretter work_concepts")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS work_concepts (
                work_id TEXT,
                concept_id TEXT,
                score FLOAT,
                PRIMARY KEY (work_id, concept_id)
            );
            """)

            conn.commit()


            logging.info("Tabel work_concepts oprettet")
            
        except Exception as e:
            logging.error(f"fejl under oprettelse af work_concepts tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
        
        #indeksering:    
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_work_concepts_work_id ON work_concepts (work_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_work_concepts_concept_id ON work_concepts (concept_id);")

            conn.commit()
            
        except Exception as e:
            logging.error(f"fejl under indexering af work_concepts tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            

        #---institutions
        
        try:
            logging.info("Opretter institutions")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS institutions (
                institution_id TEXT PRIMARY KEY,
                display_name TEXT,
                ror TEXT UNIQUE,
                type TEXT,
                country_code TEXT
            
            );
            """)

            conn.commit()

            logging.info("Tabel institutions oprettet")
            
        except Exception as e:
            logging.error(f"fejl under oprettelse af institutions tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
    
            
        #indexering:  
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_institutions_ror ON institutions (ror);")

            conn.commit()
            
        except Exception as e:
            logging.error(f"fejl under indeksering af institutions tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
            

    #---citations
        
        try:
            logging.info("Opretter citations")

            cur.execute("""
            CREATE TABLE IF NOT EXISTS citations (
                citing_work_id TEXT,
                cited_work_id TEXT,
                PRIMARY KEY (citing_work_id, cited_work_id)
            );
            """)

            conn.commit()

            logging.info("Tabel citations oprettet")
            
        except Exception as e:
            logging.error(f"fejl under oprettelse af citations tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            
            
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_citations_citing_work_id ON citations (citing_work_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_citations_cited_work_id ON citations (cited_work_id);")

            conn.commit()
        
        except Exception as e:
            logging.error(f"fejl under indeksering af citations tabel")
            logging.debug(traceback.format_exc())
            conn.rollback()
            

    except Exception as e:
        logging.critical("Fejl i forbindelse til db: " + str(e))
        logging.debug(traceback.format_exc())

    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass
