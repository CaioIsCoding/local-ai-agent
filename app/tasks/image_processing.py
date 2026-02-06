import os
import asyncio
import httpx
import shutil
from app.celery_app import celery_app
from app.services.openai import OpenAIService
from app.services.photoroom import PhotoRoomService
from app.services.enhancement import EnhancementService
from app.services.branding import BrandingService
from app.services.evolution import EvolutionService
from app.services.instagram import InstagramService
from app.services.google_business import GoogleBusinessService
from app.services.storage import storage_service
from app.database import SessionLocal
from app.models import ContentJob, Tenant
from app.config import settings

from app.core.exceptions import RateLimitError, ServiceUnavailableError, ExternalAPIError

def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

from app.services.video import VideoService
from app.services.carousel import CarouselService

@celery_app.task(
    name="app.tasks.image_processing.generate_format_variant",
)
def generate_format_variant(job_id: int, format_type: str = "9:16"):
    """
    Creates a variant of the processed image in a different format (e.g., Stories/Reels).
    """
    db = SessionLocal()
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        if not job or not job.media_urls:
            return "Job or media not found"

        base_image_url = job.media_urls[-1]
        temp_dir = "/tmp/local-ai-agent"
        os.makedirs(temp_dir, exist_ok=True)
        
        base_path = os.path.join(temp_dir, f"base_{job_id}.png")
        variant_path = os.path.join(temp_dir, f"variant_{job_id}_{format_type.replace(':', '_')}.png")

        # Download base image
        with open(base_path, "wb") as f:
            resp = httpx.get(base_image_url, timeout=30.0)
            resp.raise_for_status()
            f.write(resp.content)

        # Apply ratio enforcement
        BrandingService.enforce_ratio(base_path, variant_path, ratio=format_type)

        # Upload variant
        s3_url = storage_service.upload_file(variant_path, f"results/{job_id}_{format_type.replace(':', '_')}.png")
        
        # Update job
        job.media_urls = job.media_urls + [s3_url]
        db.commit()

        # Cleanup
        os.remove(base_path)
        os.remove(variant_path)

        return {"status": "success", "variant_url": s3_url}
    finally:
        db.close()

@celery_app.task(
    name="app.tasks.image_processing.process_image_task",
    autoretry_for=(RateLimitError, ServiceUnavailableError),
    retry_backoff=True,
    retry_backoff_max=600,
    max_retries=5
)
def process_image_task(job_id: int):
    db = SessionLocal()
    job = None
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        if not job:
            return f"Job {job_id} not found"

        if job.status != "processing":
            job.status = "processing"
            db.commit()

        tenant = db.query(Tenant).filter(Tenant.id == job.tenant_id).first()
        
        if not job.media_urls or len(job.media_urls) == 0:
            raise ValueError("No media URLs found in job")

        original_url = job.media_urls[0]
        
        temp_dir = "/tmp/local-ai-agent"
        os.makedirs(temp_dir, exist_ok=True)
        
        original_path = os.path.join(temp_dir, f"orig_{job_id}.jpg")
        no_bg_path = os.path.join(temp_dir, f"nobg_{job_id}.png")
        final_path = os.path.join(temp_dir, f"final_{job_id}.png")

        # 1. Download original image
        with open(original_path, "wb") as f:
            resp = httpx.get(original_url, timeout=30.0)
            resp.raise_for_status()
            f.write(resp.content)

        # 2. OpenAI Vision Analysis
        openai_service = OpenAIService()
        analysis = run_async(openai_service.analyze_image(original_path))

        # --- TICKET 029: The Professional Aesthetic Module ---
        
        # 3. PhotoRoom Background Removal
        photoroom_service = PhotoRoomService()
        run_async(photoroom_service.remove_background(open(original_path, "rb").read(), no_bg_path))

        # 4. Automated High-End Retouching (Claid.ai)
        # Note: Claid requires a public URL. We'll use the original_url provided in the job.
        # If the original_url is not public, this would fail in production.
        enhanced_path = os.path.join(temp_dir, f"enhanced_{job_id}.png")
        try:
            enhancement_service = EnhancementService()
            run_async(enhancement_service.enhance_image(original_url, enhanced_path))
            # If enhancement succeeds, we use the enhanced image for subsequent branding/polish
            # We'll re-run background removal on the enhanced version for best quality
            run_async(photoroom_service.remove_background(open(enhanced_path, "rb").read(), no_bg_path))
        except Exception as e:
            print(f"Claid enhancement failed, falling back to basic: {e}")
            # Fallback already happened (no_bg_path from original_path)

        # 5. Professional Polish & 4:5 Portrait Ratio
        # We'll apply the polish (color grading + bokeh) to the no-background subject
        polished_path = os.path.join(temp_dir, f"polished_{job_id}.png")
        BrandingService.professional_polish(no_bg_path, polished_path, has_transparency=True)

        # 6. Branding (Apply logo)
        logo_path = tenant.branding_config.get("logo_path") if tenant.branding_config else None
        
        if logo_path and os.path.exists(logo_path):
            BrandingService.apply_watermark(polished_path, logo_path, final_path)
        else:
            # Fallback if no logo
            shutil.copy(polished_path, final_path)

        # 7. Ensure 4:5 (Portrait) ratio for premium feel
        from PIL import Image
        final_img = Image.open(final_path)
        w, h = final_img.size
        target_ratio = 4/5
        current_ratio = w/h
        
        if current_ratio != target_ratio:
            if current_ratio > target_ratio:
                # Too wide, crop sides
                new_w = h * target_ratio
                left = (w - new_w) / 2
                final_img = final_img.crop((left, 0, left + new_w, h))
            else:
                # Too tall, crop top/bottom
                new_h = w / target_ratio
                top = (h - new_h) / 2
                final_img = final_img.crop((0, top, w, top + new_h))
            
            final_img.save(final_path)

        # 8. Upload to S3-compatible storage
        s3_url = storage_service.upload_file(final_path, f"results/{job_id}_final.png")

        # 6. Update Job and Send Result
        job.media_urls = job.media_urls + [s3_url]
        job.generated_copies = [
            analysis.get("social_caption", ""),
            analysis.get("seo_caption", ""),
            analysis.get("branding_suggestion", ""),
            analysis.get("context_description", "")
        ]
        job.status = "completed"
        db.commit()

        # 7. Send to WhatsApp via Evolution API
        evolution_service = EvolutionService()
        
        # Format the caption for WhatsApp
        wa_caption = (
            f"*Branded Image Ready!*\n\n"
            f"*Social Caption:*\n{analysis.get('social_caption', '')}\n\n"
            f"*SEO Caption:*\n{analysis.get('seo_caption', '')}\n\n"
            f"_Powered by Local AI Agent_"
        )
        
        # We assume the user's phone number/JID is stored in job metadata or tenant info
        # For MVP, we'll try to get it from the job's input_data if available
        remote_jid = job.input_data.get("remote_jid") if job.input_data else None
        
        if remote_jid:
            run_async(evolution_service.send_image(
                remote_jid=remote_jid,
                image_path=final_path,
                caption=wa_caption
            ))
        
        # Cleanup local files
        try:
            os.remove(original_path)
            os.remove(no_bg_path)
            os.remove(final_path)
        except Exception:
            pass

        return {"status": "success", "job_id": job_id, "s3_url": s3_url}

    except Exception as e:
        if job:
            job.status = "failed"
            db.commit()
        print(f"Error processing job {job_id}: {str(e)}")
        raise e
    finally:
        db.close()

def dispatch_image_process(job_id: int, tenant_plan: str = "free"):
    """
    Helper function to demonstrate how tasks can be routed to queues
    based on a (mocked) tenant plan.
    """
    queue_map = {
        "premium": "high_priority",
        "standard": "default",
        "free": "low_priority"
    }
    target_queue = queue_map.get(tenant_plan, "default")
    
    return process_image_task.apply_async(
        args=[job_id],
        queue=target_queue
    )

@celery_app.task(
    name="app.tasks.image_processing.verify_post_task",
    bind=True,
    max_retries=10,
    default_retry_delay=60  # Retry every 60 seconds
)
def verify_post_task(self, job_id: int, platform: str, media_id: str):
    """
    Sub-task that retries until a post is confirmed live on the target platform.
    """
    db = SessionLocal()
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        if not job:
            return f"Job {job_id} not found"

        is_live = False
        if platform == "instagram":
            # Call Instagram API to check status
            status_resp = run_async(InstagramService.get_media_status(media_id))
            # If the API returns the media object with the same ID, it's live
            if status_resp.get("id") == media_id:
                is_live = True
        elif platform == "google_business":
            # Call Google API to check status
            status_resp = run_async(GoogleBusinessService.get_post_status(media_id, "mock_location_abc"))
            if status_resp.get("state") == "LIVE":
                is_live = True
        
        if is_live:
            # Final success notification
            job.status = f"verified_live_{platform}"
            db.commit()

            evolution_service = EvolutionService()
            remote_jid = job.input_data.get("remote_jid") if job.input_data else None
            if remote_jid:
                msg = f"🚀 VERIFIED: Your post is now LIVE on {platform.replace('_', ' ').title()}!\n\nID: {media_id}"
                run_async(evolution_service.send_text(remote_jid, msg))
            return {"status": "verified", "media_id": media_id}
        else:
            # Not live yet, retry
            raise self.retry(exc=Exception(f"Post {media_id} not yet live on {platform}"))

    except Exception as e:
        if self.request.retries >= self.max_retries:
            # Hard failure after all retries
            if job:
                job.status = f"verification_failed_{platform}"
                db.commit()
            
            evolution_service = EvolutionService()
            remote_jid = job.input_data.get("remote_jid") if job.input_data else None
            if remote_jid:
                msg = f"⚠️ VERIFICATION ALERT: We couldn't confirm your post on {platform} is live after multiple attempts. Please check the platform manually.\n\nID: {media_id}"
                run_async(evolution_service.send_text(remote_jid, msg))
            return {"status": "failed", "reason": str(e)}
        raise e
    finally:
        db.close()

@celery_app.task(
    name="app.tasks.image_processing.publish_content_task",
    autoretry_for=(RateLimitError, ServiceUnavailableError),
    retry_backoff=True,
    retry_backoff_max=600,
    max_retries=3
)
def publish_content_task(job_id: int, platform: str):
    db = SessionLocal()
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        if not job:
            return f"Job {job_id} not found"

        # Get first generated copy as caption (Social Caption)
        caption = job.generated_copies[0] if job.generated_copies else "Default caption"
        
        # Get processed image URL (last in the list usually)
        image_url = job.media_urls[-1] if job.media_urls else ""
        
        media_id = None
        if platform == "instagram":
            result = run_async(InstagramService.publish_photo(
                image_url=image_url,
                caption=caption
            ))
            media_id = result.get("id")
        elif platform == "google_business":
            result = run_async(GoogleBusinessService.create_local_post(
                image_url=image_url,
                text=caption,
                location_id="mock_location_abc"
            ))
            media_id = result.get("name") # Google uses names as IDs
        else:
            return f"Unsupported platform: {platform}"

        if media_id:
            # Trigger the verification loop after 60s
            verify_post_task.apply_async(args=[job_id, platform, media_id], countdown=60)
            
            job.status = f"publishing_{platform}"
            db.commit()
            return {"status": "publishing_initiated", "media_id": media_id}
        else:
            raise ExternalAPIError(f"Failed to get media_id from {platform}")

    except Exception as e:
        print(f"Error publishing job {job_id} to {platform}: {str(e)}")
        raise e
    finally:
        db.close()
