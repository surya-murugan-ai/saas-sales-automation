import requests
from app.config import settings


class PhantomBusterService:
    def __init__(self):
        self.base_url = "https://api.phantombuster.com/api/v2"
        self.headers = {"X-Phantombuster-Key-1": settings.PHANTOM_BUSTER_API_KEY}
        print("PhantomBuster API Key:", settings.PHANTOM_BUSTER_API_KEY)

    def enrich_lead(self, lead: dict):
        # Check for required key
        if "profileUrl" not in lead:
            raise KeyError(f"Missing 'profileUrl' in lead: {lead}")
        
        payload = {
            "phantomId": "put your phantomId",
            "argument": {
                "linkedinUrl": lead["profileUrl"],
                "companyUrl": lead.get("company_url")
            }
        }

        response = requests.post(
            f"{self.base_url}/phantoms/run",
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["containerId"]

    def get_enrichment_results(self, container_id: str):
        response = requests.get(
            f"{self.base_url}/containers/{container_id}/output",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Create a singleton instance
phantom_service = PhantomBusterService()




# __________________________________________________________________________________
# import requests
# from app.config import settings

# class PhantomBusterService:
#     def __init__(self):
#         self.base_url = "https://api.phantombuster.com/api/v2"
#         self.headers = {"X-Phantom-Key": settings.PHANTOM_BUSTER_API_KEY}

#     def enrich_lead(self, lead: dict):
#         payload = {
#             "phantomId": "lead-enrichment-phantom",
#             "argument": {
#                 "linkedinUrl": lead["linkedin_url"],
#                 "companyUrl": lead.get("company_url")
#             }
#         }
#         response = requests.post(
#             f"{self.base_url}/phantoms/run",
#             json=payload,
#             headers=self.headers
#         )
#         response.raise_for_status()
#         return response.json()["containerId"]

#     def get_enrichment_results(self, container_id: str):
#         response = requests.get(
#             f"{self.base_url}/containers/{container_id}/output",
#             headers=self.headers
#         )
#         response.raise_for_status()
#         return response.json()

# phantom_service = PhantomBusterService()