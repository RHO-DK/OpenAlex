import psycopg2

try:
    from config import OA_DB_NAME, OA_LOG_PATH_DB, OA_DB_USER, OA_DB_HOST, OA_DB_PORT
    if not isinstance(OA_DB_NAME, str) or not OA_DB_NAME.strip():
        raise ValueError("OA_DB_NAME er ikke defineret korrekt i config.py")
    if not isinstance(OA_LOG_PATH_DB, str) or not OA_LOG_PATH_DB.strip():
        raise ValueError("OA_LOG_PATH_DB er ikke defineret korrekt i config.py")
    if not isinstance(OA_DB_USER, str) or not OA_DB_USER.strip():
        raise ValueError("OA_DB_USER er ikke defineret korrekt i config.py")
    if not isinstance(OA_DB_HOST, str) or not OA_DB_HOST.strip():
        raise ValueError("OA_DB_HOST er ikke defineret korrekt i config.py")
    if not isinstance(OA_DB_PORT, int) or not OA_DB_PORT:
        raise ValueError("OA_DB_PORT er ikke defineret korrekt i config.py")
except ImportError as e:
    raise ImportError("config.py kunne ikke importeres -  mangler filen?") from e


import logging
import traceback

#---Logging - both by log and print

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



#--- connect and alte tables

def connect_db():
    return psycopg2.connect(
        dbname=OA_DB_NAME, 
        user=OA_DB_USER,
        host=OA_DB_HOST,
        port=OA_DB_PORT
        )

def alter_tables():
    try:
        conn = connect_db()
        cur = conn.cursor()
        
        
        #Authorships
        
        try:
            logging.info("Tilføjer fremmednøgler til authorships")
            cur.execute("""
                ALTER TABLE authorships
                ADD CONSTRAINT fk_authorships_work FOREIGN KEY (work_id) REFERENCES works(work_id),
                ADD CONSTRAINT fk_authorships_author FOREIGN KEY (author_id) REFERENCES authors(author_id),
                ADD CONSTRAINT fk_authorships_institution FOREIGN KEY (institution_id) REFERENCES institutions(institution_id);
            """)
            
            conn.commit()
            
            logging.info("Fremmednøgler tilføjet til authorships")
            
        except Exception as e:
            logging.error("Fejl ved tilføjelse af fremmednøgl(er) til authorships: " + str(e))
            logging.debug(traceback.format_exc())
            conn.rollback()
        

        # work_topics
        try:
            logging.info("Tilføjer fremmednøgler til work_topics")
            cur.execute("""
                ALTER TABLE work_topics
                ADD CONSTRAINT fk_work_topics_work FOREIGN KEY (work_id) REFERENCES works(work_id),
                ADD CONSTRAINT fk_work_topics_topic FOREIGN KEY (topic_id) REFERENCES topics(topic_id);
            """)
            
            conn.commit()
            
            logging.info("Fremmednøgler tilføjet til work_topics")
            
        except Exception as e:
            logging.error("Fejl ved tilføjelse af fremmednøgl(er) til work_topics: " + str(e))
            logging.debug(traceback.format_exc())
            conn.rollback()

        
        # work_concepts
        try:
            logging.info("tilføje fremmenøgle(r) til work_concepts")
            cur.execute("""
                ALTER TABLE work_concepts
                ADD CONSTRAINT fk_work_concepts_work FOREIGN KEY (work_id) REFERENCES works(work_id),
                ADD CONSTRAINT fk_work_concepts_concept FOREIGN KEY (concept_id) REFERENCES concepts(concept_id);
            """)
            
            conn.commit()
            
            logging.info("Fremmednøgler tilføjet til work_concepts")
            
        except Exception as e:
            logging.error("Fejl ved tilføjelse af fremmednøgl(er) til work_concepts: " + str(e))
            logging.debug(traceback.format_exc())
            conn.rollback()
    

        # topics
        try:
            logging.info("fremmednøgle tilføjes topics tabel")

            cur.execute("""  
                ALTER TABLE topics
                ADD CONSTRAINT fk_topics_subfield FOREIGN KEY (subfield_id) REFERENCES subfields(subfield_id),
                ADD CONSTRAINT fk_topics_field FOREIGN KEY (field_id) REFERENCES fields(field_id),
                ADD CONSTRAINT fk_topics_domain FOREIGN KEY (domain_id) REFERENCES domains(domain_id);
                """)
            conn.commit()
            
            logging.info("fremmednøgle tilføjet topics tabel")
            
        except Exception as e:
            logging.error("Fejl ved tilføjelse af fremmednøgl(er) til topics tabel: " + str(e))
            logging.debug(traceback.format_exc())
            conn.rollback()
            

        # fields
        try:
            logging.info("Fremmednøgle tilføjes fields tabel")
            
            cur.execute("""
                ALTER TABLE fields
                ADD CONSTRAINT fk_fields_domain FOREIGN KEY (domain_id) REFERENCES domains(domain_id);
                """)
            conn.commit()
            
            logging.info("fremmednøgle tilføjet tields tabel")
        
        except Exception as e:
            logging.error("Fejl ved tilføjelse af fremmednøgl(er) til fields tabel: " + str(e))
            logging.debug(traceback.format_exc())
            conn.rollback()
            

        # subfields
        try:
            logging.info("fremmednøgle tilføjes subfields tabel")
            
            cur.execute("""
                ALTER TABLE subfields
                ADD CONSTRAINT fk_subfields_field FOREIGN KEY (field_id) REFERENCES fields(field_id);
                """)
            
            logging.info("fremmednøgle tilføjet subfields tabel")
        
        except Exception as e:
            logging.error("Fejl ved tilføjelse af fremmednøgl(er) til subfields tabel: " + str(e))
            logging.debug(traceback.format_exc())
            conn.rollback()
            
        
        # citations
        try:
            logging.info("fremmednøgle tiføjes citations tabel")
            
            cur.execute("""
                ALTER TABLE citations
                ADD CONSTRAINT fk_citations_citing FOREIGN KEY (citing_work_id) REFERENCES works(work_id),
                ADD CONSTRAINT fk_citations_cited FOREIGN KEY (cited_work_id) REFERENCES works(work_id);
                """)
            
            logging.info("fremmednøgle tilføjet citations tabel")
        
        except Exception as e:
            logging.error("Fejl ved tilføjelse af fremmednøgl(er) til citations tabel: " + str(e))
            logging.debug(traceback.format_exc())
            conn.rollback()
            
            
        # works → institutions
        try:
            logging.info("fremmednøgle tilføjet works tabel")
            cur.execute("""
                ALTER TABLE works
                ADD CONSTRAINT fk_works_host_venue FOREIGN KEY (host_venue_ror) REFERENCES institutions(ror);
                """)
            logging.info("fremmednøgle tilføjet works tabel")
        
        except Exception as e:
            logging.error("Fejl ved tilføjelse af fremmednøgl(er) til works tabel: " + str(e))
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
        
    

