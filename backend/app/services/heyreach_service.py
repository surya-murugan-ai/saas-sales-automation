import requests
from app.config import settings

class HeyReachService:
    def __init__(self):
        self.base_url = "https://api.heyreach.io/v1"
        self.headers = {"Authorization": f"Bearer {settings.HEYREACH_API_KEY}"}

    def create_campaign(self, leads: list, message: str):
        payload = {
            "campaignName": "outreach-campaign",
            "leads": leads,
            "message": message
        }
        response = requests.post(
            f"{self.base_url}/campaigns",
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["campaignId"]

heyreach_service = HeyReachService()