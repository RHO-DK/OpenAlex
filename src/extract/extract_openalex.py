# --- API hentning openalex --- #

import os
import json
import requests
import logging
import traceback
from logging.handlers import RotatingFileHandler

try:
    from config import OPENALEX_BASE_URL, OPENALEX_PARAMS, LOG_PATH_EXTRACT_OPENALEX
    if not isinstance(OPENALEX_BASE_URL, str) or not OPENALEX_BASE_URL.strip():
        raise ValueError("OPENALEX_BASE_URL er ikke defineret korrekt i config.py")
    if not isinstance(OPENALEX_PARAMS, dict) or not OPENALEX_PARAMS:
        raise ValueError("OPENALEX_PARAMS er ikke defineret korrekt i config.py")
    if not isinstance(LOG_PATH_EXTRACT_OPENALEX, str) or not LOG_PATH_EXTRACT_OPENALEX.strip():
        raise ValueError("LOG_PATH_EXTRACT_OPENALEX er ikke defineret korrekt i config.py")
except ImportError as e:
    raise ImportError("config.py kunne ikke importeres -  mangler filen?") from e


# --- Logging
log_handler = RotatingFileHandler(LOG_PATH_EXTRACT_OPENALEX, maxBytes=10**6, backupCount=3)
logging.basicConfig(
    handlers=[log_handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s" #
)

# --- gemmer på sidebasis (se også openalex dokumentation - for cursor-baserede sider) - en jsonfil pr side
def save_page(data, page_number):
    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/works_page_{page_number:03}.json"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info("Gemte side %03d med %d værker til %s", page_number, len(data.get("results", [])), filename)
    except Exception as e:
        logging.error("Fejl ved lagring af side %d: %s", page_number, str(e))
        logging.debug(traceback.format_exc())

# --- datahentning - også sidebaseret
def fetch_openalex_works():
    url = OPENALEX_BASE_URL
    cursor = "*"
    page = 1
    total_works = 0

    while cursor:
        params = OPENALEX_PARAMS.copy()
        params["cursor"] = cursor

        
        try:
            logging.info("Henter side %03d (cursor: %s)", page, cursor)
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])
            if not results:
                logging.warning("Tom side %03d -  ingen værker returneret", page)
                break

            save_page(data, page)
            total_works += len(results)

            #sidebaseret cursor: "next_cursor" - se openalex dok.
            cursor = data.get("meta", {}).get("next_cursor")
            if not cursor:
                logging.info("Sidste side - ingen cursor")
                break

            page += 1

        except requests.exceptions.Timeout:
            logging.error("Timeout ved hentning af side %03d", page)
            break
        except requests.exceptions.HTTPError as e:
            logging.error("HTTP-fejl på side %03d: %s", page, str(e))
            logging.debug(traceback.format_exc())
            break
        except Exception as e:
            logging.error("Ukendt fejl på side %03d: %s", page, str(e))
            logging.debug(traceback.format_exc())
            break

    logging.info("Hentning afsluttet. %d sider, %d værker i alt.", page, total_works)



if __name__ == "__main__":
    fetch_openalex_works()
