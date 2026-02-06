import httpx
import asyncio
import logging
from typing import Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class InstagramService:
    API_VERSION = "v19.0"
    BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

    @classmethod
    async def publish_photo(cls, image_url: str, caption: str, access_token: str = None, ig_user_id: str = None) -> Dict[str, Any]:
        """
        Real implementation of Instagram Graph API 'Image Container' and 'Media Publish' endpoints.
        """
        access_token = access_token or settings.INSTAGRAM_ACCESS_TOKEN
        ig_user_id = ig_user_id or settings.INSTAGRAM_BUSINESS_ACCOUNT_ID

        if not access_token or not ig_user_id:
            logger.error("Instagram access token or business account ID not configured")
            return {"status": "error", "error": "Credentials not configured"}

        # 1. Create Media Container
        container_url = f"{cls.BASE_URL}/{ig_user_id}/media"
        params = {
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token
        }
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(container_url, params=params, timeout=30.0)
                resp_data = resp.json()
                
                if resp.status_code != 200:
                    logger.error(f"Error creating Instagram media container: {resp_data}")
                    return {"status": "error", "error": resp_data}
                
                creation_id = resp_data.get("id")
                logger.info(f"Created Instagram media container: {creation_id}")
                
                # 2. Poll for container readiness
                ready = False
                for i in range(12): # Try 12 times (60 seconds total)
                    status_url = f"{cls.BASE_URL}/{creation_id}"
                    status_params = {
                        "fields": "status_code",
                        "access_token": access_token
                    }
                    status_resp = await client.get(status_url, params=status_params)
                    status_data = status_resp.json()
                    
                    status_code = status_data.get("status_code")
                    if status_code == "FINISHED":
                        ready = True
                        break
                    
                    if status_code == "ERROR":
                        logger.error(f"Instagram container creation error: {status_data}")
                        return {"status": "error", "error": status_data}
                    
                    logger.info(f"Instagram container {creation_id} status: {status_code}. Polling...")
                    await asyncio.sleep(5)
                
                if not ready:
                    return {"status": "error", "error": "Container readiness timeout"}

                # 3. Publish container
                publish_url = f"{cls.BASE_URL}/{ig_user_id}/media_publish"
                publish_params = {
                    "creation_id": creation_id,
                    "access_token": access_token
                }
                publish_resp = await client.post(publish_url, params=publish_params, timeout=30.0)
                publish_data = publish_resp.json()
                
                if publish_resp.status_code != 200:
                    logger.error(f"Error publishing Instagram container: {publish_data}")
                    return {"status": "error", "error": publish_data}
                
                media_id = publish_data.get("id")
                logger.info(f"Successfully published to Instagram. Media ID: {media_id}")
                
                return {
                    "status": "success",
                    "id": media_id,
                    "platform": "instagram"
                }
            except Exception as e:
                logger.error(f"Exception during Instagram publishing: {str(e)}")
                return {"status": "error", "error": str(e)}

    @classmethod
    async def get_media_status(cls, media_id: str, access_token: str = None) -> Dict[str, Any]:
        """
        Check if a media object is published and accessible.
        """
        access_token = access_token or settings.INSTAGRAM_ACCESS_TOKEN
        url = f"{cls.BASE_URL}/{media_id}"
        params = {
            "fields": "id,ig_id,media_type,shortcode,status_code",
            "access_token": access_token
        }
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, params=params, timeout=10.0)
                return resp.json()
            except Exception as e:
                logger.error(f"Error checking Instagram media status: {str(e)}")
                return {"status": "error", "error": str(e)}
