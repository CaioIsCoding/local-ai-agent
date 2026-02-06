from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import ContentJob, Tenant, SocialAccount
from app.tasks.image_processing import process_image_task, publish_content_task
from app.services.evolution import EvolutionService
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
    remote_jid = data.get("key", {}).get("remoteJid")
    
    # Identify message type
    image_msg = message.get("imageMessage")
    text_msg = message.get("conversation") or (message.get("extendedTextMessage", {}).get("text"))

    # 1. HANDLE IMAGE (New Content Job)
    if image_msg:
        # Mocking the URL extraction for this exercise:
        media_url = data.get("mediaUrl") # Some versions of Evolution API provide this
        if not media_url:
            media_url = "https://images.unsplash.com/photo-1523275335684-37898b6baf30" 

        tenant = db.query(Tenant).first()
        if not tenant:
            tenant = Tenant(business_name="Default Business", niche="E-commerce")
            db.add(tenant)
            db.commit()
            db.refresh(tenant)

        job = ContentJob(
            tenant_id=tenant.id,
            status="pending",
            media_urls=[media_url],
            input_data={"remote_jid": remote_jid}
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        process_image_task.delay(job.id)
        return {"status": "success", "job_id": job.id}

    # 2. HANDLE COMMANDS (Interaction Logic)
    if text_msg:
        cmd = text_msg.strip().lower()
        platforms = {
            "approve": "all",
            "post ig": "instagram",
            "post google": "google_business",
            "reject": "rejected"
        }

        matched_platform = None
        for key, val in platforms.items():
            if cmd == key:
                matched_platform = val
                break
        
        if matched_platform:
            # Find the most recent job for this sender
            job = db.query(ContentJob).filter(
                ContentJob.input_data["remote_jid"].astext == remote_jid
            ).order_by(desc(ContentJob.created_at)).first()

            if not job:
                return {"status": "error", "message": "No job found for this sender"}

            evolution_service = EvolutionService()
            
            if matched_platform == "rejected":
                job.status = "rejected"
                db.commit()
                await evolution_service.send_text(remote_jid, "❌ Content rejected.")
                return {"status": "success", "action": "rejected"}
            
            if matched_platform == "all":
                publish_content_task.delay(job.id, "instagram")
                publish_content_task.delay(job.id, "google_business")
                await evolution_service.send_text(remote_jid, "🚀 Publishing to Instagram and Google...")
            else:
                publish_content_task.delay(job.id, matched_platform)
                await evolution_service.send_text(remote_jid, f"🚀 Publishing to {matched_platform.replace('_', ' ').title()}...")
            
            return {"status": "success", "action": f"publishing_{matched_platform}"}

    return {"status": "ignored", "reason": "no_actionable_content"}
