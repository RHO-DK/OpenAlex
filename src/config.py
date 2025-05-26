#---Base configs

BASE_URL = "https://api.openalex.org/works"
LOG_PATH = "logs/fetch.log"
DB_NAME = "openalex_db"
PARAMS = {"filter": "authorships.institutions.country_code:DK,from_publication_date:2014-01-01",
          "per-page": 200
        }
API_TIMEOUT = 10


