from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import ContentJob, Tenant
from app.services.evolution import EvolutionService
from app.tasks.image_processing import publish_content_task
import logging

logger = logging.getLogger(__name__)

class InteractionService:
    def __init__(self, db: Session):
        self.db = db
        self.evolution_service = EvolutionService()

    async def handle_message(self, remote_jid: str, text: str):
        cmd = text.strip().lower()
        
        # Find the most recent job for this sender or related tenant
        # In a real multi-tenant app, we'd filter by sender's association to a tenant
        job = self.db.query(ContentJob).order_by(desc(ContentJob.created_at)).first()

        if not job:
            return {"status": "error", "message": "No job found"}

        tenant = job.tenant
        if remote_jid not in tenant.admin_jids:
            logger.warning(f"Unauthorized access attempt by {remote_jid}")
            return {"status": "error", "message": "Unauthorized"}

        if cmd == "approve":
            return await self.process_approval(job, remote_jid)
        elif cmd == "reject":
            return await self.process_rejection(job, remote_jid)
        
        return {"status": "ignored"}

    async def process_approval(self, job: ContentJob, admin_jid: str):
        if admin_jid in job.approvals:
             await self.evolution_service.send_text(admin_jid, "⚠️ You have already approved this content.")
             return {"status": "already_approved"}

        # Use a list to store approvals
        current_approvals = list(job.approvals) if job.approvals else []
        current_approvals.append(admin_jid)
        job.approvals = current_approvals
        
        tenant = job.tenant
        required = tenant.required_approvals or 2

        if len(job.approvals) < required:
            job.status = "first_approved"
            self.db.commit()
            
            # Notify other admins
            others = [jid for jid in tenant.admin_jids if jid != admin_jid]
            for other in others:
                await self.evolution_service.send_text(
                    other, 
                    f"🔔 Content approved by {admin_jid}. Need {required - len(job.approvals)} more approval(s) to publish.\nReply 'Approve' to confirm or 'Reject' to kill."
                )
            
            await self.evolution_service.send_text(admin_jid, f"✅ Approval recorded ({len(job.approvals)}/{required}). Waiting for consensus...")
            
        else:
            job.status = "completed" # Transitioning to publish
            self.db.commit()
            
            # Final Publish
            publish_content_task.delay(job.id, "instagram")
            publish_content_task.delay(job.id, "google_business")
            
            for jid in tenant.admin_jids:
                await self.evolution_service.send_text(jid, "🚀 Consensus reached! Publishing to Instagram and Google...")

        return {"status": "success"}

    async def process_rejection(self, job: ContentJob, admin_jid: str):
        job.status = "rejected"
        self.db.commit()
        
        tenant = job.tenant
        for jid in tenant.admin_jids:
            await self.evolution_service.send_text(jid, f"❌ Content REJECTED by {admin_jid}. Job killed.")
        
        return {"status": "success", "action": "rejected"}
