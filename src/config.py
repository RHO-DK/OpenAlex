#---General configs
API_TIMEOUT = 10

# --- OpenAlexExtraction

OPENALEX_BASE_URL = "https://api.openalex.org/works"
OPENALEX_PARAMS = {"filter": "authorships.institutions.country_code:DK,from_publication_date:2014-01-01",
          "per-page": 200
        }

LOG_PATH_EXTRACT_OPENALEX = "logs/extract_openalex.log"


#--- OpenAlexDB
import os
#setup logging
OA_LOG_PATH_DB = "logs/db_setup.log"

#connection
OA_DB_NAME = "openalex_db"
OA_DB_USER = "postgres"
OA_DB_HOST = "localhost"
OA_DB_PORT = 5432 
OA_DB_PASSWORD = os.getenv("OA_DB_PASSWORD")


#--- OpenAlexTransformation

#logging:
OA_LOG_PATH_PARSER = "logs/OA_parser.log"








