#---General configs
API_TIMEOUT = 10

# --- OpenAlex

OPENALEX_BASE_URL = "https://api.openalex.org/works"
OPENALEX_PARAMS = {"filter": "authorships.institutions.country_code:DK,from_publication_date:2014-01-01",
          "per-page": 200
        }

LOG_PATH_EXTRACT_OPENALEX = "logs/extract_openalex.log"


#--- DB
LOG_PATH_DB = "logs/db_setup.log"
DB_NAME = "openalex_db"




