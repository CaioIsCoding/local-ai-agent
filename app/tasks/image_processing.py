import os
import asyncio
import httpx
import shutil
from app.celery_app import celery_app
from app.services.openai import OpenAIService
from app.services.photoroom import PhotoRoomService
from app.services.branding import BrandingService
from app.database import SessionLocal
from app.models import ContentJob, Tenant

def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@celery_app.task(name="app.tasks.image_processing.process_image_task")
def process_image_task(job_id: int):
    db = SessionLocal()
    job = None
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        if not job:
            return f"Job {job_id} not found"

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
        
        # 3. PhotoRoom Background Removal
        photoroom_service = PhotoRoomService()
        run_async(photoroom_service.remove_background(open(original_path, "rb").read(), no_bg_path))

        # 4. Branding (Apply logo)
        logo_path = tenant.branding_config.get("logo_path") if tenant.branding_config else None
        
        if logo_path and os.path.exists(logo_path):
            BrandingService.apply_watermark(no_bg_path, logo_path, final_path)
        else:
            # Fallback if no logo
            shutil.copy(no_bg_path, final_path)

        # 5. Update Job
        # Note: In production, upload to S3/Cloudinary and use those URLs
        job.media_urls = job.media_urls + [f"file://{final_path}"]
        job.generated_copies = [analysis.get("branding_suggestion", ""), analysis.get("context_description", "")]
        job.status = "completed"
        db.commit()
        
        return {"status": "success", "job_id": job_id}

    except Exception as e:
        if job:
            job.status = "failed"
            db.commit()
        print(f"Error processing job {job_id}: {str(e)}")
        raise e
    finally:
        db.close()
