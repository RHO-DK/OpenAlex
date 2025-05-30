import requests

BASE_URL = "https://api.openalex.org/works"
PARAMS = {"filter": "authorships.institutions.country_code:DK,from_publication_date:2022-01-01",
    "per-page": 5

}



def fetch_works():
    response = requests.get(BASE_URL, params=PARAMS)
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])
    
    for work in results:
        print(f"\nTitle: {work.get('title')}")
        print(f"Year: {work.get('publication_year')}")
        print(f"Citations: {work.get('cited_by_count')}")
        print("Topics:")
        for topic in work.get("topics", []):
            print(f"  - {topic['display_name']} ({topic['score']})")

if __name__ == "__main__":
    fetch_works()
    
    
