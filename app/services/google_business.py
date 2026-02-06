import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GoogleBusinessService:
    @staticmethod
    async def create_local_post(image_url: str, text: str, location_id: str) -> Dict[str, Any]:
        """
        Mock implementation of Google Business Profile API 'accounts.locations.localPosts' endpoint.
        """
        logger.info(f"[MOCK] Publishing to Google Business: URL={image_url}, Text={text[:30]}..., Location={location_id}")
        # Simulate API response
        return {
            "status": "success",
            "post_name": "mock_gbp_post_67890",
            "platform": "google_business"
        }
