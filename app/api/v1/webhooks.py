from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ContentJob, Tenant, SocialAccount
from app.tasks.image_processing import process_image_task
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/evolution")
async def evolution_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    
    # Evolution API message structure
    event = payload.get("event")
    if event != "messages.upsert":
        return {"status": "ignored", "event": event}

    data = payload.get("data", {})
    message = data.get("message", {})
    
    # Identify if it's an image
    image_msg = message.get("imageMessage")
    if not image_msg:
        return {"status": "ignored", "reason": "no_image"}

    # In Evolution API, the media might be in 'base64' or we might have a 'url'
    # For this flow, we expect a URL or we assume the system handles media download
    # Evolution API usually sends media via a separate integration or we fetch it
    # Mocking the URL extraction for this exercise:
    media_url = data.get("mediaUrl") # Some versions of Evolution API provide this
    if not media_url:
        # Fallback/Mock for demonstration
        media_url = "https://images.unsplash.com/photo-1523275335684-37898b6baf30" 

    # Find Tenant by external_id (remoteJid or instance name)
    # For now, let's take the first tenant or create one if none exists
    tenant = db.query(Tenant).first()
    if not tenant:
        tenant = Tenant(business_name="Default Business", niche="E-commerce")
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

    # Create ContentJob
    job = ContentJob(
        tenant_id=tenant.id,
        status="pending",
        media_urls=[media_url]
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Trigger Task
    process_image_task.delay(job.id)

    return {"status": "success", "job_id": job.id}
