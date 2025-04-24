import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "Sales Automation"
    APIFY_API_KEY = os.getenv("APIFY_API_KEY")
    HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
    PHANTOM_BUSTER_API_KEY = os.getenv("PHANTOM_API_KEY")
    HEYREACH_API_KEY = os.getenv("HEYREACH_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sales.db")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

settings = Settings()