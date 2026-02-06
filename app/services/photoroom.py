import httpx
import os
from typing import Optional
from app.core.exceptions import RateLimitError, ServiceUnavailableError, AuthError, ExternalAPIError

class PhotoRoomService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("PHOTOROOM_API_KEY")
        self.base_url = "https://sdk.photoroom.com/v1/segment"

    async def remove_background(self, image_data: bytes, output_path: str):
        """
        Remove background from an image using PhotoRoom API.
        
        :param image_data: Binary data of the image.
        :param output_path: Path where the result will be saved.
        """
        if not self.api_key:
            raise ValueError("PhotoRoom API key is not set. Please set PHOTOROOM_API_KEY environment variable.")

        headers = {
            "x-api-key": self.api_key
        }
        
        files = {
            "image_file": ("image.jpg", image_data, "image/jpeg")
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, headers=headers, files=files, timeout=30.0)
                
                if response.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    return output_path
                elif response.status_code == 429:
                    raise RateLimitError("PhotoRoom", response.status_code, response.text)
                elif response.status_code in [401, 403]:
                    raise AuthError("PhotoRoom", response.status_code, response.text)
                elif response.status_code >= 500:
                    raise ServiceUnavailableError("PhotoRoom", response.status_code, response.text)
                else:
                    raise ExternalAPIError("PhotoRoom", response.status_code, response.text)
            except httpx.HTTPError as e:
                raise ServiceUnavailableError("PhotoRoom", 503, str(e))

    async def remove_background_from_url(self, image_url: str, output_path: str):
        """
        Remove background from an image URL.
        
        :param image_url: URL of the image.
        :param output_path: Path where the result will be saved.
        """
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(image_url)
                if resp.status_code != 200:
                    raise ExternalAPIError("PhotoRoom(ImageFetch)", resp.status_code, f"Failed to fetch image from URL: {image_url}")
                image_data = resp.content
            except httpx.HTTPError as e:
                 raise ServiceUnavailableError("PhotoRoom(ImageFetch)", 503, str(e))
            
        return await self.remove_background(image_data, output_path)
