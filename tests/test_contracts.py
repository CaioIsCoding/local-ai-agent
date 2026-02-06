import pytest
import respx
import json
import os
from httpx import Response
from app.services.openai import OpenAIService
from app.services.photoroom import PhotoRoomService
from app.services.evolution import EvolutionService

# --- Mocks for OpenAI ---

@pytest.mark.asyncio
@respx.mock
async def test_openai_service_contract():
    service = OpenAIService(api_key="fake-key")
    
    # Mocking a fake image file
    with open("test_image.jpg", "wb") as f:
        f.write(b"fake image data")
    
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "branding_suggestion": "Use gold accents",
                        "context_description": "A luxury watch",
                        "social_caption": "Check out this timepiece!",
                        "seo_caption": "Luxury watch product photo"
                    })
                }
            }
        ]
    }
    
    respx.post("https://api.openai.com/v1/chat/completions").mock(return_value=Response(200, json=mock_response))
    
    result = await service.analyze_image("test_image.jpg")
    
    assert result["branding_suggestion"] == "Use gold accents"
    assert result["social_caption"] == "Check out this timepiece!"
    
    os.remove("test_image.jpg")

# --- Mocks for PhotoRoom ---

@pytest.mark.asyncio
@respx.mock
async def test_photoroom_service_contract():
    service = PhotoRoomService(api_key="fake-key")
    
    # Mock response with binary data (representing a transparent PNG)
    respx.post("https://sdk.photoroom.com/v1/segment").mock(return_value=Response(200, content=b"fake-transparent-png-data"))
    
    output_path = "result.png"
    await service.remove_background(b"original-data", output_path)
    
    assert os.path.exists(output_path)
    with open(output_path, "rb") as f:
        assert f.read() == b"fake-transparent-png-data"
    
    os.remove(output_path)

# --- Mocks for Evolution API ---

@pytest.mark.asyncio
@respx.mock
async def test_evolution_service_contract(monkeypatch):
    # Mock settings
    monkeypatch.setattr("app.config.settings.EVOLUTION_API_URL", "https://api.evolution.com")
    monkeypatch.setattr("app.config.settings.EVOLUTION_API_KEY", "fake-key")
    monkeypatch.setattr("app.config.settings.EVOLUTION_INSTANCE_NAME", "test-instance")

    service = EvolutionService()
    
    mock_response = {"status": "SUCCESS", "message": "sent"}
    respx.post("https://api.evolution.com/message/sendText/test-instance").mock(return_value=Response(200, json=mock_response))
    
    result = await service.send_text("123456789@s.whatsapp.net", "Hello World")
    assert result["status"] == "SUCCESS"

# --- Webhook Ingestion Contract ---

from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock

def test_evolution_webhook_ingestion(monkeypatch):
    # Mocking Database and Task
    mock_db = MagicMock()
    mock_task = MagicMock()
    
    # We mock the dependency injection
    from app.database import get_db
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Mock the Celery task delay
    monkeypatch.setattr("app.api.v1.webhooks.process_image_task.delay", mock_task)
    
    # Mock DB Query for Tenant
    mock_tenant = MagicMock()
    mock_tenant.id = 1
    mock_db.query().first.return_value = mock_tenant

    client = TestClient(app)
    
    webhook_payload = {
        "event": "messages.upsert",
        "data": {
            "key": {
                "remoteJid": "123456789@s.whatsapp.net",
                "fromMe": False,
                "id": "ABC123"
            },
            "message": {
                "imageMessage": {
                    "url": "https://mmg.whatsapp.net/v/...",
                    "mimetype": "image/jpeg",
                    "caption": "Process this"
                }
            },
            "mediaUrl": "https://example.com/image.jpg"
        }
    }

    response = client.post("/api/v1/webhooks/evolution", json=webhook_payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert mock_task.called
    
    # Cleanup
    app.dependency_overrides.clear()

# --- Mocks for Instagram ---
from app.services.instagram import InstagramService

@pytest.mark.asyncio
@respx.mock
async def test_instagram_service_contract(monkeypatch):
    monkeypatch.setattr("app.config.settings.INSTAGRAM_ACCESS_TOKEN", "fake-token")
    monkeypatch.setattr("app.config.settings.INSTAGRAM_BUSINESS_ACCOUNT_ID", "fake-id")

    # 1. Mock Container Creation
    respx.post("https://graph.facebook.com/v19.0/fake-id/media").mock(
        return_value=Response(200, json={"id": "container_123"})
    )
    
    # 2. Mock Status Polling (ready)
    respx.get("https://graph.facebook.com/v19.0/container_123").mock(
        return_value=Response(200, json={"status_code": "FINISHED", "id": "container_123"})
    )
    
    # 3. Mock Publish
    respx.post("https://graph.facebook.com/v19.0/fake-id/media_publish").mock(
        return_value=Response(200, json={"id": "media_999"})
    )

    result = await InstagramService.publish_photo("http://example.com/img.jpg", "Test caption")
    
    assert result["status"] == "success"
    assert result["id"] == "media_999"

@pytest.mark.asyncio
@respx.mock
async def test_instagram_status_contract(monkeypatch):
    monkeypatch.setattr("app.config.settings.INSTAGRAM_ACCESS_TOKEN", "fake-token")
    
    respx.get("https://graph.facebook.com/v19.0/media_999").mock(
        return_value=Response(200, json={"id": "media_999", "status_code": "FINISHED"})
    )
    
    result = await InstagramService.get_media_status("media_999")
    assert result["id"] == "media_999"
