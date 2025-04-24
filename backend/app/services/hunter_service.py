import requests
from app.config import settings

def find_email(first_name: str, last_name: str, domain: str) -> dict:
    url = "https://api.hunter.io/v2/email-finder"
    params = {
        "first_name": first_name,
        "last_name": last_name,
        "domain": domain,
        "api_key": settings.HUNTER_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return {"email": data.get("data", {}).get("email")}
    else:
        return {"email": None}
