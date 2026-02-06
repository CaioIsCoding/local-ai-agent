import httpx
import os
from typing import Optional
from app.core.exceptions import RateLimitError, ServiceUnavailableError, AuthError, ExternalAPIError

class EnhancementService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CLAID_API_KEY")
        self.base_url = "https://api.claid.ai/v1/process"

    async def enhance_image(self, image_url: str, output_path: str):
        """
        Enhance image using Claid.ai API.
        
        :param image_url: Public URL of the image to enhance.
        :param output_path: Path where the result will be saved.
        """
        if not self.api_key:
             # If no API key, we skip enhancement or use a mock/noop
             # For this ticket, we'll assume it's required for "automated professional production"
             raise ValueError("CLAID_API_KEY is not set.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Professional retouching payload based on Claid documentation
        payload = {
            "input": image_url,
            "operations": {
                "restorations": {
                    "upscale": "smart_enhance",
                    "polish": True
                },
                "adjustments": {
                    "hdr": 50,
                    "clarity": 20
                }
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, headers=headers, json=payload, timeout=60.0)
                
                if response.status_code == 200:
                    data = response.json()
                    output_url = data.get("output", {}).get("tmp_url")
                    if not output_url:
                        raise ExternalAPIError("Claid.ai", response.status_code, "No output URL returned")
                    
                    # Download result
                    img_resp = await client.get(output_url)
                    if img_resp.status_code == 200:
                        with open(output_path, "wb") as f:
                            f.write(img_resp.content)
                        return output_path
                    else:
                        raise ExternalAPIError("Claid.ai(Download)", img_resp.status_code, img_resp.text)
                
                elif response.status_code == 429:
                    raise RateLimitError("Claid.ai", response.status_code, response.text)
                elif response.status_code in [401, 403]:
                    raise AuthError("Claid.ai", response.status_code, response.text)
                else:
                    raise ExternalAPIError("Claid.ai", response.status_code, response.text)
            except httpx.HTTPError as e:
                raise ServiceUnavailableError("Claid.ai", 503, str(e))
