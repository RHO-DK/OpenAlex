#### obs - helperfunkiton mangles - til strip af præfixer - placeres i utils navngives "strip_prefix"

import json
import logging
import traceback
import psycopg2
import os
import sys

# Tilføj src til importsti for config - password til db via venv før  kørsel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from config import (
    OA_DB_NAME,
    OA_DB_USER,
    OA_DB_PASSWORD,
    OA_DB_HOST,
    OA_DB_PORT
)

from utils.helpers import strip_id

LOG_PATH_TEST_PARSE = "logs/test_parse_works_001.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH_TEST_PARSE),
        logging.StreamHandler()
    ]
)


def connect_db():
    return psycopg2.connect(
        dbname=OA_DB_NAME,
        user=OA_DB_USER,
        password=OA_DB_PASSWORD,
        host=OA_DB_HOST,
        port=OA_DB_PORT
    )

def parse_and_insert_works(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            works = data.get("results", [])

        conn = connect_db()
        cur = conn.cursor()

        inserted = 0
        skipped = 0
        skipped_ids = []

        for work in works:
            # Eksklusionskritere: skip work hvis authorships er tom eller mangler
            if not work.get("authorships"):
                skipped += 1
                logging.info(f"Springer over work uden authorships: {strip_prefix(work.get('id'))}")
                skipped_ids.append(strip_id(work.get("id")))
                continue
            
        
            try:
                cur.execute("""
                    INSERT INTO works (
                        work_id, doi, title, publication_date, publication_year, type,
                        language, cited_by_count, is_oa, license,
                        host_venue_name, host_venue_issn, host_venue_ror, created_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (work_id) DO NOTHING;
                """, (
                    strip_id(work.get("id")),
                    work.get("doi"),
                    work.get("title"),
                    work.get("publication_date"),
                    work.get("publication_year"),
                    work.get("type"),
                    work.get("language"),
                    work.get("cited_by_count"),
                    work.get("open_access", {}).get("is_oa"),
                    work.get("open_access", {}).get("license"),
                    work.get("host_venue", {}).get("display_name"),
                    work.get("host_venue", {}).get("issn_l"),
                    strip_id(work.get("host_venue", {}).get("institution", {}).get("ror")),
                    work.get("created_date")
                ))
                
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
        
                inserted += 1
            except Exception as e:
                logging.warning(f"Fejl ved parsing af work {work.get('id')}: {e}")
                logging.debug(traceback.format_exc())
                
        if skipped_ids:
            with open("logs/skipped_works_ids.txt", "w") as f:
                for wid in skipped_ids:
                    f.write(wid + "\n")

        conn.commit()
        logging.info(f"Indsatte {inserted} værker fra {os.path.basename(filepath)}")
        logging.info(f"Sprang {skipped} værker over (manglende authorships)")

        cur.close()
        conn.close()

    except Exception as e:
        logging.critical(f"Fejl ved parser-test: {e}")
        logging.debug(traceback.format_exc())
        con.rollback()

        
    finally:
    cur.close()
    conn.close()
    

if __name__ == "__main__":
    file_path = os.path.abspath(os.path.join("data", "raw", "works_page_001.json"))
    parse_and_insert_works(file_path)