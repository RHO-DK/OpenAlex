
import json
import logging
import traceback
import psycopg2
import os
import sys

# Tilføj src til importsti for config - password til db via venv før  kørsel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#print("Looking for config in path:", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


from config import (
    OA_DB_NAME,
    OA_DB_USER,
    OA_DB_PASSWORD,
    OA_DB_HOST,
    OA_DB_PORT,
    OA_LOG_PATH_PARSER
)

from utils.helpers import strip_id



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(OA_LOG_PATH_PARSER),
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
    


def parse_and_insert_works(filepath, failed_files):
    
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
                logging.info(f"Springer over work uden authorships: {strip_id(work.get('id'))}")
                skipped_ids.append(strip_id(work.get("id")))
                continue
            
            # fallback til kildeoplysninger (host_venue eller source via primary_location)
            venue = work.get("host_venue") or work.get("primary_location", {}).get("source") or {}

            doi = strip_id(work.get("doi"))
            host_venue_name = venue.get("display_name")
            host_venue_issn = venue.get("issn_l")
            host_venue_ror = strip_id(venue.get("host_organization"))
            
            
            try:
                cur.execute("""
                    INSERT INTO works (
                        work_id, doi, title, publication_date, publication_year, type,
                        language, cited_by_count, is_oa, oa_status,
                        host_venue_name, host_venue_issn, host_venue_ror, created_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (work_id) DO NOTHING;
                """, (
                    strip_id(work.get("id")),
                    doi,
                    work.get("title"),
                    work.get("publication_date"),
                    work.get("publication_year"),
                    work.get("type"),
                    work.get("language"),
                    work.get("cited_by_count"),
                    work.get("open_access", {}).get("is_oa"),
                    work.get("open_access", {}).get("oa_status"),
                    host_venue_name,
                    host_venue_issn,
                    host_venue_ror,
                    work.get("created_date")
                ))
                
                if cur.rowcount == 1:
                    conn.commit()
                    inserted += 1
                else:
                    conn.commit()
                    logging.info(f"Work {strip_id(work.get('id'))} blev ikke indsat (muligvis allerede eksisterende).")
                    
            except Exception as e:
                conn.rollback()
                logging.warning(f"Fejl ved parsing af work {work.get('id')}: {e}")
                logging.debug(traceback.format_exc())
                
                
        if skipped_ids:
            with open("logs/skipped_works_ids.txt", "w") as f:
                for wid in skipped_ids:
                    f.write(wid + "\n")

        
        logging.info(f"Indsatte {inserted} værker fra {os.path.basename(filepath)}")
        logging.info(f"Sprang {skipped} værker over (manglende authorships)")

        cur.close()
        conn.close()

    except Exception as e:
        logging.critical(f"Fejl i parsing af {os.path.basename(filepath)}: {e}")
        logging.debug(traceback.format_exc())
        failed_files.append(os.path.basename(filepath))
        conn.rollback()
        
        
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass
    

if __name__ == "__main__":
    failed_files = []
    raw_dir = os.path.abspath(os.path.join("data", "raw"))
    json_files = sorted([
        f for f in os.listdir(raw_dir) 
        if f.endswith(".json")
    ])

    for filename in json_files:
        filepath = os.path.join(raw_dir, filename)
        logging.info(f"Starter parsing af {filename}")
        parse_and_insert_works(filepath, failed_files)
        
try:
    if failed_files:
        logging.info(f"{len(failed_files)} kunne ikke parses - Se logs/failed_files.txt")
        with open("logs/failed_files.txt", "w") as f:
            for name in failed_files:
                f.write(name + "\n")
except NameError:
    pass
                


