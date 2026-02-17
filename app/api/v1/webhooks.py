from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import ContentJob, Tenant, SocialAccount
from app.tasks.image_processing import process_image_task, publish_content_task
from app.services.evolution import EvolutionService
import logging

from app.services.interaction import InteractionService

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
    remote_jid = data.get("key", {}).get("remoteJid")
    
    # Identify message type
    image_msg = message.get("imageMessage")
    text_msg = message.get("conversation") or (message.get("extendedTextMessage", {}).get("text"))

    # 1. HANDLE IMAGE (New Content Job)
    if image_msg:
        # Mocking the URL extraction for this exercise:
        media_url = data.get("mediaUrl") # Some versions of Evolution API provide this
        if not media_url:
            logger.warning(f"Image message received from {remote_jid} but mediaUrl is missing.")
            return {"status": "ignored", "reason": "missing_media_url"}

        tenant = db.query(Tenant).first()
        if not tenant:
            tenant = Tenant(
                business_name="Default Business", 
                niche="E-commerce",
                admin_jids=[remote_jid], # Add the sender as admin for testing
                required_approvals=2
            )
            db.add(tenant)
            db.commit()
            db.refresh(tenant)

        job = ContentJob(
            tenant_id=tenant.id,
            status="pending_approval", # Ticket 027: Multi-Admin Approval Implementation
            media_urls=[media_url],
            input_data={"remote_jid": remote_jid}
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        process_image_task.delay(job.id)
        
        # Notify admins about the new job
        evolution_service = EvolutionService()
        for admin_jid in tenant.admin_jids:
            await evolution_service.send_text(
                admin_jid, 
                "📸 New content received and processed. Reply 'Approve' to start the approval workflow."
            )
            
        return {"status": "success", "job_id": job.id}

    # 2. HANDLE COMMANDS (Interaction Logic)
    if text_msg:
        interaction_service = InteractionService(db)
        result = await interaction_service.handle_message(remote_jid, text_msg)
        return result

    return {"status": "ignored", "reason": "no_actionable_content"}
