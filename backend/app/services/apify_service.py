import requests
from apify_client import ApifyClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class ApifyService:
    def __init__(self):
        self.client = ApifyClient(settings.APIFY_API_KEY)
        self.linkedin_feed_url = "https://www.linkedin.com/sales/home"
        self.jsession_cookie = ""
        self.bcookie_ = ""

    def check_session_valid(self, session_cookie: str) -> bool:
        """Validate the LinkedIn session cookie before starting the scrape."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Cookie": f"li_at={session_cookie}"
            }
            response = requests.get(self.linkedin_feed_url, headers=headers, timeout=10)
            if "login" in response.url.lower() or response.status_code != 200:
                logger.warning(f"⚠️ LinkedIn session invalid. Response URL: {response.url}")
                return False
            logger.info("✅ LinkedIn session is valid.")
            return True
        except Exception as e:
            logger.error(f"❌ Error validating LinkedIn session: {e}")
            return False

    def start_scrape(self, linkedin_url: str,bcookie_: str ,jsession_cookie: str, session_cookie: str, lead_count: int):
        run_input = {
            "searchUrl": linkedin_url,
            "cookie": [
                {"name": "li_at",
            "value": session_cookie,
            "domain": "www.linkedin.com",
            "path": "/",
            "httpOnly": True,
            "secure": True,},
                {
            "name": "JSESSIONID",
            "value": jsession_cookie,
            "domain": ".linkedin.com",
            "path": "/",
            "httpOnly": True,
            "secure": True
        },
        {
            "name": "bcookie",
            "value": bcookie_,
            "domain": ".linkedin.com",
            "path": "/",
            "httpOnly": False,
            "secure": True
        },
            
            ],
            "count": lead_count,
            "deepScrape": True,
            "startPage": 1,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyCountry": "IN",
                "apifyProxyGroups": ["RESIDENTIAL"],
            },
            "minDelay": 5,
            "maxDelay": 30,
        }

        logger.info(f"🚀 Starting Apify run with URL: {linkedin_url}")
        run = self.client.actor("put your actor id").call(run_input=run_input)
        logger.info(f"data = \n\n {run}\n\n")
        logger.info(f"Run ID = \n\n {run["id"]}\n\n")
        logger.info(f"Run Database ID = \n\n {run["defaultDatasetId"]}\n\n")
        return run["id"], run["defaultDatasetId"]

    def get_scrape_results(self, dataset_id: str):
        dataset = self.client.dataset(dataset_id).iterate_items()
        return list(dataset)

apify_service = ApifyService()
