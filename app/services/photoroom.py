import httpx
import os
from typing import Optional

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
            response = await client.post(self.base_url, headers=headers, files=files, timeout=30.0)
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                return output_path
            else:
                raise Exception(f"PhotoRoom API error: {response.status_code} - {response.text}")

    async def remove_background_from_url(self, image_url: str, output_path: str):
        """
        Remove background from an image URL.
        
        :param image_url: URL of the image.
        :param output_path: Path where the result will be saved.
        """
        async with httpx.AsyncClient() as client:
            resp = await client.get(image_url)
            if resp.status_code != 200:
                raise Exception(f"Failed to fetch image from URL: {image_url}")
            image_data = resp.content
            
        return await self.remove_background(image_data, output_path)
