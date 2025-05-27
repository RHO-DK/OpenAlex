import requests
import logging
from logging.handlers import RotatingFileHandler

# --- Opsæt af logning
log_handler = RotatingFileHandler(
    "logs/test.log", maxBytes=10**6, backupCount=3
)
logging.basicConfig(
    handlers=[log_handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_works():
    url = "https://api.openalex.org/works" # tester med "wrongURL" fremfor works
    params = {
        "filter": "authorships.institutions.country_code:DK,from_publication_date:2022-01-01",
        "per-page": 5
    }

    try:
        logging.info("Starter API-kald til OpenAlex (filter: DK, from 2022)")
        response = requests.get(url, params=params, timeout=10) #tester med timeout 0.000001 fremfor 10
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])
        logging.info("Hentede %d værker uden fejl", len(results))
        
        #henter år og titel
        for work in results:
            title = work.get("title", "Uden titel")
            year = work.get("publication_year", "Ukendt")
            print(f"{year}: {title}")
            
        raise ValueError("Manuel testfejl") #tester fejllogging

    except requests.exceptions.Timeout:
        logging.error("Timeout ved hentning fra OpenAlex (url: %s)", url)
    except requests.exceptions.HTTPError as e:
        logging.error("HTTP-fejl %s: %s", e.response.status_code, e.response.reason)
    except Exception as e:
        logging.error("Ukendt fejl i fetch_works: %s", str(e))


if __name__ == "__main__":
    fetch_works()
