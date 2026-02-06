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
        Analyze an image using GPT-4o Vision.
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
                            "text": "Analyze this image and provide branding suggestions and context. Return a JSON with 'branding_suggestion' and 'context_description'."
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
            "max_tokens": 500
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
