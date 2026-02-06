import httpx
from app.config import settings
import base64
import os
from app.core.exceptions import RateLimitError, ServiceUnavailableError, AuthError, ExternalAPIError

class EvolutionService:
    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL
        self.api_key = settings.EVOLUTION_API_KEY

    def _get_headers(self):
        return {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }

    async def _handle_response(self, response: httpx.Response, service_name: str):
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        elif response.status_code == 429:
            raise RateLimitError(service_name, response.status_code, response.text)
        elif response.status_code in [401, 403]:
            raise AuthError(service_name, response.status_code, response.text)
        elif response.status_code >= 500:
            raise ServiceUnavailableError(service_name, response.status_code, response.text)
        else:
            raise ExternalAPIError(service_name, response.status_code, response.text)

    async def send_text(self, remote_jid: str, text: str):
        """
        Send a text message via Evolution API.
        """
        url = f"{self.base_url}/message/sendText/{settings.EVOLUTION_INSTANCE_NAME}"
        payload = {
            "number": remote_jid,
            "options": {
                "delay": 1200,
                "presence": "composing"
            },
            "textMessage": {
                "text": text
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self._get_headers(), json=payload)
                return await self._handle_response(response, "Evolution")
            except httpx.HTTPError as e:
                raise ServiceUnavailableError("Evolution", 503, str(e))

    async def send_image(self, remote_jid: str, image_path: str, caption: str = ""):
        """
        Send an image via Evolution API.
        """
        url = f"{self.base_url}/message/sendMedia/{settings.EVOLUTION_INSTANCE_NAME}"
        
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        payload = {
            "number": remote_jid,
            "mediaMessage": {
                "mediatype": "image",
                "caption": caption,
                "media": base64_image
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self._get_headers(), json=payload)
                return await self._handle_response(response, "Evolution")
            except httpx.HTTPError as e:
                raise ServiceUnavailableError("Evolution", 503, str(e))
