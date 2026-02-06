from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ContentJob(Base):
    __tablename__ = "content_jobs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    status = Column(String, default="pending")  # pending, processing, pending_approval, first_approved, completed, failed, rejected
    media_urls = Column(JSON, default=[])  # List of media URLs (original/processed)
    input_data = Column(JSON, default={})  # Store original payload data
    generated_copies = Column(JSON, default=[])  # Captions/descriptions
    approvals = Column(JSON, default=[]) # Ticket 027: List of JIDs that approved this job
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    tenant = relationship("Tenant", back_populates="content_jobs")
