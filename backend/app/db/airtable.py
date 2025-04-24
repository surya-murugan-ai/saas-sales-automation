
from pyairtable import Table
from typing import List, Dict, Any
from app.config import settings
import logging

class AirtableClient:
    def __init__(self):
        self.base_id = settings.AIRTABLE_BASE_ID
        self.table_name = settings.AIRTABLE_LEADS_TABLE_ID
        self.api_key = settings.AIRTABLE_API_KEY
        self.table = Table(self.api_key, self.base_id, self.table_name)
        self.logger = logging.getLogger(__name__)

    def save_leads(self, leads: List[Dict[str, Any]]):
        try:
            # Normalize leads in case they're wrapped in "fields"
            # records = [{"fields": lead.get("fields", lead)} for lead in leads]
            print(f"records being sent to Airtable:\n{leads}")
            response = self.table.batch_create(leads)
            self.logger.info(f"Successfully saved {len(leads)} leads to Airtable")
            return response
        except Exception as e:
            self.logger.error(f"Error saving leads to Airtable: {str(e)}")
            raise Exception(f"Error saving leads to Airtable: {str(e)}")


    # def save_leads(self, leads: List[Dict[str, Any]]):
    #     try:
    #         # Create records in batch for Airtable
    #         records = [{"fields": lead} for lead in leads]
    #         print(f"records:{records}")
    #         response = self.table.batch_create(records)
    #         self.logger.info(f"Successfully saved {len(records)} leads to Airtable")
    #         return response
    #     except Exception as e:
    #         self.logger.error(f"Error saving leads to Airtable: {str(e)}")
    #         raise Exception(f"Error saving leads to Airtable: {str(e)}")












# _______________________________________________________________




# import pyairtable
# from app.config import settings
# from typing import List, Dict, Any

# class AirtableClient:
#     def __init__(self):
#         # Initialize Airtable client with API key and base ID
#         self.client = pyairtable.Api(settings.AIRTABLE_API_KEY)
#         self.base = self.client.base(settings.AIRTABLE_BASE_ID)
#         self.leads_table = self.base.table("Table 1")
#         # self.enriched_table = self.base.table("EnrichedLeads")

#     def save_leads(self, leads: List[Dict[str, Any]]):
#         # Batch save leads to Airtable
#         return self.leads_table.batch_create([{"fields": lead} for lead in leads])

#     def get_leads(self, max_records: int = 100):
#         # Retrieve leads from Airtable
#         return [record["fields"] for record in self.leads_table.all(max_records=max_records)]

#     # def save_enriched_lead(self, lead: Dict[str, Any]):
#     #     # Save a single enriched lead
#     #     return self.enriched_table.create({"fields": lead})

# # Singleton instance
# airtable_client = AirtableClient()