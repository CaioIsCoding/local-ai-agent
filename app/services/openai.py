import os
import base64
from typing import Optional
import httpx

class OpenAIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1/chat/completions"

    async def analyze_image(self, image_path: str) -> dict:
        """
        Analyze an image using GPT-4o Vision to generate branding suggestions, 
        context, Social Caption, and SEO Caption.
        """
        if not self.api_key:
            raise ValueError("OpenAI API key is not set. Please set OPENAI_API_KEY environment variable.")

        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Analyze this image and provide:\n"
                                "1. branding_suggestion: Short branding advice.\n"
                                "2. context_description: Brief description of the image content.\n"
                                "3. social_caption: Engaging caption for social media (Instagram/WhatsApp).\n"
                                "4. seo_caption: Optimized description for SEO/Alt-text.\n"
                                "Return as a JSON object with these 4 keys."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "response_format": { "type": "json_object" },
            "max_tokens": 1000
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=payload, timeout=60.0)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                import json
                return json.loads(content)
            else:
                raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
