import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class InstagramService:
    @staticmethod
    async def publish_photo(image_url: str, caption: str, access_token: str) -> Dict[str, Any]:
        """
        Mock implementation of Instagram Graph API 'Image Container' and 'Media Publish' endpoints.
        """
        logger.info(f"[MOCK] Publishing to Instagram: URL={image_url}, Caption={caption[:30]}...")
        # Simulate API response
        return {
            "status": "success",
            "media_id": "mock_ig_media_12345",
            "platform": "instagram"
        }
