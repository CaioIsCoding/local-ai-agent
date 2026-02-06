from fastapi import FastAPI
import sentry_sdk
from app.api.v1.webhooks import router as webhook_router
from app.config import settings

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

app = FastAPI(title="Local AI Agent API")


app.include_router(webhook_router, prefix="/api/v1/webhooks", tags=["webhooks"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
