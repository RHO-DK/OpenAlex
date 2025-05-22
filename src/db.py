import psycopg2
from config import DB_NAME

import logging


#---Logging - both by log and print

# logfil-handler
file_handler = logging.FileHandler("logs/db_setup.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# konsol-handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

# combo
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])


#---creating tables

def connect_db():
    return psycopg2.connect(dbname=DB_NAME, user="postgres")

def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    
    
  
    #---works
    
    logging.info("Opretter works")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS works (
        work_id TEXT PRIMARY KEY,
        doi TEXT,
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
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'works'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel works oprettet")
    else:
        logging.error("Tabel works ikke oprettet")
        
        
    cur.execute("CREATE INDEX IF NOT EXISTS idx_works_ror ON works (host_venue_ror);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_works_citations ON works (cited_by_count);")
    
    conn.commit()
        
        
    
    #--- authorships
    
    logging.info("Opretter authorships")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS authorships (
        work_id TEXT,
        author_id TEXT,
        institution_id TEXT,
        author_position TEXT, 
        is_corresponding BOOLEAN
        PRIMARY KEY (work_id, author_id),
        FOREIGN KEY (work_id) REFERENCES works(work_id),
        FOREIGN KEY (author_id) REFERENCES authors(author_id),
        FOREIGN KEY (institution_id) REFERENCES institutions(institution_id)
      
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'authorships'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel authorships oprettet")
    else:
        logging.error("Tabel authorships ikke oprettet")
        
       
    cur.execute("CREATE INDEX IF NOT EXISTS idx_authorships_work_id ON authorships (work_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_authorships_author_id ON authorships (author_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_authorships_institution_id ON authorships (institution_id);")
    
    conn.commit()
        
        
       
    #---authors
     
    logging.info("Opretter authors")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        author_id TEXT PRIMARY KEY,
        name TEXT,
        orcid TEXT
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'authors'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel authors oprettet")
    else:
        logging.error("Tabel authors ikke oprettet")
        
        
        
    #---topics
    
    logging.info("Opretter topics")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        topic_id TEXT PRIMARY KEY,
        display_name TEXT,
        subfield_id TEXT,
        subfield_name TEXT,
        field_id TEXT,
        field_name TEXT,
        domain_id TEXT,
        domain_name TEXT,
        FOREIGN KEY (subfield_id) REFERENCES subfields(subfield_id)
      
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'topics'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel topics oprettet")
    else:
        logging.error("Tabel topics ikke oprettet")
        
    cur.execute("CREATE INDEX IF NOT EXISTS idx_topics_subfield_id ON topics (subfield_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_topics_field_id ON topics (field_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_topics_domain_id ON topics (domain_id);")
    
    conn.commit()
        
    
    
     #---domains
    
    logging.info("Opretter domains")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS domains (
        domain_id TEXT PRIMARY KEY,
        domain_name TEXT
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'domains'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel domains oprettet")
    else:
        logging.error("Tabel domains ikke oprettet")
        
        
    

    #---fields
    
    logging.info("Opretter fields")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS fields (
        field_id TEXT PRIMARY KEY,
        field_name TEXT,
        domain_id TEXT FOREIGN KEY
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'fields'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel fields oprettet")
    else:
        logging.error("Tabel fields ikke oprettet")
        


  #---subfields
    
    logging.info("Opretter subfields")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subfields (
        subfield_id TEXT PRIMARY KEY,
        subfield_name TEXT,
        field_id TEXT FOREIGN KEY
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'subfields'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel subfields oprettet")
    else:
        logging.error("Tabel subfields ikke oprettet")
        

     
    #---work_topics
    
    logging.info("Opretter work_topics")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS work_topics (
        work_id TEXT FOREIGN KEY,
        topic_id TEXT FOREIGN KEY,
        score FLOAT,
        is_primary BOOLEAN
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'work_topics'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel work_topics oprettet")
    else:
        logging.error("Tabel work_topics ikke oprettet")
        
      
             
    #---concepts
    
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

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'concepts'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel concepts oprettet")
    else:
        logging.error("Tabel concepts ikke oprettet")
        



    #---work_concepts
    
    logging.info("Opretter work_concepts")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS work_concepts (
        work_id TEXT FOREIGN KEY,
        concept_id TEXT FOREIGN KEY,
        score FLOAT,
       
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'work_concepts'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel work_concepts oprettet")
    else:
        logging.error("Tabel work_concepts ikke oprettet")
        



    #---institutions
    
    logging.info("Opretter institutions")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS institutions (
        institution_id TEXT PRIMARY KEY,
        display_name TEXT,
        ror TEXT,
        type TEXT,
        country_code TEXT
       
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'institutions'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel institutions oprettet")
    else:
        logging.error("Tabel institutions ikke oprettet")
        



#---citations
    
    logging.info("Opretter citations")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS citations (
        citation_work_id TEXT,
        cited_work_id TEXT,
    );
    """)

    conn.commit()

    # log check
    cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'citations'
    );
    """)
    exists = cur.fetchone()[0]

    if exists:
        logging.info("Tabel citations oprettet")
    else:
        logging.error("Tabel citations ikke oprettet")
        



    cur.close()
    conn.close()


