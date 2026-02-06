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

    # Social Publishing (Instagram)
    INSTAGRAM_APP_ID: Optional[str] = None
    INSTAGRAM_APP_SECRET: Optional[str] = None
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    INSTAGRAM_BUSINESS_ACCOUNT_ID: Optional[str] = None

    # Social Publishing (Google Business Profile)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_PROJECT_ID: Optional[str] = None
    GOOGLE_REFRESH_TOKEN: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
