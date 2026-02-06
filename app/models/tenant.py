from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False)
    niche = Column(String)
    location_city = Column(String)
    admin_jids = Column(JSON, default=[])  # List of WhatsApp JIDs allowed to manage this tenant
    required_approvals = Column(Integer, default=2) # Ticket 027: Multi-Admin Approval Implementation
    
    # SaaS & Quota Logic (Ticket 018)
    plan_tier = Column(String, default="free") # free, premium, enterprise
    current_post_count = Column(Integer, default=0)
    
    branding_config = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    social_accounts = relationship("SocialAccount", back_populates="tenant")
    content_jobs = relationship("ContentJob", back_populates="tenant")
