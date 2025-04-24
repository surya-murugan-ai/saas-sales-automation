import time
import logging
from app.core.celery_app import celery_app
from app.services.apify_service import apify_service
from app.services.llm_service import llm_service
from app.services.hunter_service import find_email
from app.db.airtable import AirtableClient
from app.utils.email import send_email
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

airtable_client = AirtableClient()

def clean_lead_data(raw_lead: dict) -> dict:
    exclude_fields = {
        "educations",
        "positions",
        "skills",
        "numOfConnections",
        "unlocked",
        "profileBackgroundPictureUrl",
        "viewed",
        "saved",
        "pendingInvitation",
        "openLink",
        "salesNavigatorUrl",
        "profileId",
        "connectionType",
    }

    cleaned_lead = {k: v for k, v in raw_lead.items() if k not in exclude_fields}

    # Keep enriched fields explicitly
    if "email" in raw_lead:
        cleaned_lead["email"] = raw_lead["email"]
    if "phone" in raw_lead:
        cleaned_lead["phone"] = raw_lead["phone"]
    if "personalized_profile" in raw_lead:
        cleaned_lead["personalized_profile"] = raw_lead["personalized_profile"]
    if "outreach_message" in raw_lead:
        cleaned_lead["outreach_message"] = raw_lead["outreach_message"]

    return cleaned_lead

@celery_app.task
def scrape_leads(linkedin_url: str, session_cookie: str, lead_count: int, notification_email: str):
    try:
        logger.info(f"Validating LinkedIn session cookie before scraping.")
        if not apify_service.check_session_valid(session_cookie):
            raise Exception("LinkedIn session cookie is invalid or expired. Please update it and try again.")

        logger.info(f"Starting scrape for {lead_count} leads from {linkedin_url}")
        run_id, dataset_id = apify_service.start_scrape(linkedin_url,apify_service.bcookie_,apify_service.jsession_cookie, session_cookie, lead_count)
        leads = apify_service.get_scrape_results(dataset_id)
        logger.info(f"Scraped {len(leads)} leads")

        if not leads:
            logger.warning("No leads scraped. Possibly invalid LinkedIn cookie or wrong URL.")
            send_email(
                to_email=notification_email,
                subject="No Leads Scraped",
                body="No leads were scraped. This may mean your LinkedIn session cookie is invalid/expired or the search URL is incorrect."
            )
            return {"status": "failed", "leads": 0, "reason": "no leads scraped"}

        enriched_leads = []
        hunter_used_counter = 0
        counter = 0
        lead_id = 1

        for lead in leads:
            logger.info(f"Processing lead: {lead.get('firstName')} {lead.get('lastName')}")
            email = None
            phone = lead.get("phone")
            company_data = lead.get("companyWebsite", "")

            if hunter_used_counter < 3:
                logger.info("Using Hunter.io for this lead.")
                hunter_result = find_email(
                    first_name=lead.get("firstName"),
                    last_name=lead.get("lastName"),
                    domain=company_data
                )
                email = hunter_result.get("email")
                hunter_used_counter += 1
            else:
                logger.info("Skipping Hunter.io for this lead due to monthly limit.")

            if counter < 3:
                profile = ""
                outreach = ""
                profile = llm_service.generate_profile(lead, company_data)
                outreach = llm_service.generate_outreach(profile)
                counter += 1
            else:
                profile = ""
                outreach = ""
                logger.info("Skipping personalised AI lead generation, as local model will take time.")

            enriched_lead = {
                "id":lead_id
                **lead,
                "email": email,
                "phone": phone,
                "company_data": company_data,
                "personalized_profile": profile,
                "outreach_message": outreach
            }

            cleaned_lead = clean_lead_data(enriched_lead)
            enriched_leads.append(cleaned_lead)
            lead_id +=1

        logger.info(f"Enriched {len(enriched_leads)} leads")
        print(f"printing one data\n: {enriched_leads[0]}")
        

        # Save enriched leads to Airtable
        airtable_client.save_leads(enriched_leads)
        logger.info("Saved leads to Airtable")

        airtable_link = f"https://airtable.com/{settings.AIRTABLE_BASE_ID}/{settings.AIRTABLE_LEADS_TABLE_ID}"
        send_email(
            to_email=notification_email,
            subject="Leads Scraped and Uploaded",
            body=f"Successfully scraped and enriched {len(enriched_leads)} leads. View them here: {airtable_link}"
        )
        logger.info(f"Sent email to {notification_email}")

        return {"status": "completed", "leads": len(enriched_leads)}
    except Exception as e:
        logger.error(f"Scrape task failed: {str(e)}")
        send_email(
            to_email=notification_email,
            subject="Lead Scraping Failed",
            body=f"Scraping process failed.\n\nError: {str(e)}"
        )
        raise
