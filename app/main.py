from fastapi import FastAPI
from app.api.v1.webhooks import router as webhook_router

app = FastAPI(title="Local AI Agent API")

app.include_router(webhook_router, prefix="/api/v1/webhooks", tags=["webhooks"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
