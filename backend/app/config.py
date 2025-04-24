import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API keys for third-party services
    APIFY_API_KEY = os.getenv("APIFY_API_KEY")
    PHANTOM_BUSTER_API_KEY = os.getenv("PHANTOM_BUSTER_API_KEY")
    HEYREACH_API_KEY = os.getenv("HEYREACH_API_KEY")
    HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
    AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
    AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
    AIRTABLE_LEADS_TABLE_ID=os.getenv("AIRTABLE_LEADS_TABLE_ID")
    
    # SMTP settings for email notifications
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = os.getenv("SMTP_PORT", 587)
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    
    # Redis for Celery task queue
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Local LLaMA 3.2 endpoint
    LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://localhost:11434")
    LLM_MODEL="llama3.2"
        
settings = Settings()