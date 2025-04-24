from fastapi import FastAPI
from app.api import leads

app = FastAPI(title="Sales Automation SaaS")

# Include API routes for lead operations
app.include_router(leads.router, prefix="/api")