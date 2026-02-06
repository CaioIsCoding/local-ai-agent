from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    platform = Column(String, nullable=False)  # e.g., 'instagram', 'whatsapp', 'google_business'
    tokens = Column(JSON)  # Stores access/refresh tokens
    expiry = Column(DateTime)
    external_id = Column(String, index=True)
    
    tenant = relationship("Tenant", back_populates="social_accounts")
