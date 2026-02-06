from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False)
    niche = Column(String)
    location_city = Column(String)
    branding_config = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    social_accounts = relationship("SocialAccount", back_populates="tenant")
    content_jobs = relationship("ContentJob", back_populates="tenant")

class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    platform = Column(String, nullable=False)  # e.g., 'instagram', 'whatsapp', 'google_business'
    tokens = Column(JSON)  # Stores access/refresh tokens
    expiry = Column(DateTime)
    external_id = Column(String, index=True)
    
    tenant = relationship("Tenant", back_populates="social_accounts")

class ContentJob(Base):
    __tablename__ = "content_jobs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    media_urls = Column(JSON, default=[])  # List of media URLs (original/processed)
    generated_copies = Column(JSON, default=[])  # Captions/descriptions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    tenant = relationship("Tenant", back_populates="content_jobs")
