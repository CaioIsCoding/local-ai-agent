from fastapi import FastAPI

app = FastAPI(title="Local AI Agent API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
