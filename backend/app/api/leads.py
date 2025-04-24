from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.tasks import leads as lead_tasks

router = APIRouter()

class ScrapeRequest(BaseModel):
    linkedin_url: str
    session_cookie: str
    lead_count: int
    notification_email: str

class CampaignRequest(BaseModel):
    notification_email: str

@router.post("/scrape")
async def start_scrape(request: ScrapeRequest):
    try:
        task = lead_tasks.scrape_leads.delay(
            request.linkedin_url,
            request.session_cookie,
            request.lead_count,
            request.notification_email
        )
        return {"task_id": task.id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/campaign")
async def start_campaign(request: CampaignRequest):
    try:
        task = lead_tasks.start_campaign.delay(
            request.notification_email
        )
        return {"task_id": task.id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    from celery.result import AsyncResult
    task = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }