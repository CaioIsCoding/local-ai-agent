from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/local_ai_db"
    
    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI & Media Services
    OPENAI_API_KEY: Optional[str] = None
    PHOTOROOM_API_KEY: Optional[str] = None
    
    # Evolution API (WhatsApp)
    EVOLUTION_API_URL: Optional[str] = None
    EVOLUTION_API_KEY: Optional[str] = None
    EVOLUTION_INSTANCE_NAME: Optional[str] = "local-ai"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
