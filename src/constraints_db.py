import psycopg2

try:
    from config import DB_NAME
    if not DB_NAME or not isinstance(DB_NAME, str):
        raise ValueError("DB_NAME er ikke defineret korrekt i config.py")
except ImportError as e:
    raise ImportError("config.py kunne ikke importeres -  mangler filen?") from e


import logging
import traceback

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


def apply_foreign_keys():
    conn = psycopg2.connect(dbname=DB_NAME, user="postgres")
    cur = conn.cursor()

    foreign_key_commands = [
        # authorships
        """
        ALTER TABLE authorships
        ADD CONSTRAINT fk_authorships_work FOREIGN KEY (work_id) REFERENCES works(work_id),
        ADD CONSTRAINT fk_authorships_author FOREIGN KEY (author_id) REFERENCES authors(author_id),
        ADD CONSTRAINT fk_authorships_institution FOREIGN KEY (institution_id) REFERENCES institutions(institution_id);
        """,

        # work_topics
        """
        ALTER TABLE work_topics
        ADD CONSTRAINT fk_work_topics_work FOREIGN KEY (work_id) REFERENCES works(work_id),
        ADD CONSTRAINT fk_work_topics_topic FOREIGN KEY (topic_id) REFERENCES topics(topic_id);
        """,

        # work_concepts
        """
        ALTER TABLE work_concepts
        ADD CONSTRAINT fk_work_concepts_work FOREIGN KEY (work_id) REFERENCES works(work_id),
        ADD CONSTRAINT fk_work_concepts_concept FOREIGN KEY (concept_id) REFERENCES concepts(concept_id);
        """,

        # topics
        """
        ALTER TABLE topics
        ADD CONSTRAINT fk_topics_subfield FOREIGN KEY (subfield_id) REFERENCES subfields(subfield_id),
        ADD CONSTRAINT fk_topics_field FOREIGN KEY (field_id) REFERENCES fields(field_id),
        ADD CONSTRAINT fk_topics_domain FOREIGN KEY (domain_id) REFERENCES domains(domain_id);
        """,

        # fields
        """
        ALTER TABLE fields
        ADD CONSTRAINT fk_fields_domain FOREIGN KEY (domain_id) REFERENCES domains(domain_id);
        """,

        # subfields
        """
        ALTER TABLE subfields
        ADD CONSTRAINT fk_subfields_field FOREIGN KEY (field_id) REFERENCES fields(field_id);
        """,

        # citations
        """
        ALTER TABLE citations
        ADD CONSTRAINT fk_citations_citing FOREIGN KEY (citing_work_id) REFERENCES works(work_id),
        ADD CONSTRAINT fk_citations_cited FOREIGN KEY (cited_work_id) REFERENCES works(work_id);
        """,

        # works → institutions
        """
        ALTER TABLE works
        ADD CONSTRAINT fk_works_host_venue FOREIGN KEY (host_venue_ror) REFERENCES institutions(ror);
        """
       
    ]

    for cmd in foreign_key_commands:
        try:
            cur.execute(cmd)
            conn.commit()
            print("OK:", cmd.strip().split('\n')[0])  # Print første linje af kommandoen
        except Exception as e:
            print("FEJL:", e)
            conn.rollback()

    cur.close()
    conn.close()

if __name__ == "__main__":
    apply_foreign_keys()
