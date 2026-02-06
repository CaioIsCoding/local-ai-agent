# BACKLOG: Phase 1 (The MVP)

## Goal
Build a functional pipeline that receives an image via WhatsApp (Evolution API), processes it with a brand watermark, and returns it to the user.

## Sprints & Tickets

### Priority 1: Infrastructure & Project Setup
- [ ] **Ticket 001: Initialize FastAPI & Celery Scaffold**
  - Set up the directory structure.
  - Configure `docker-compose` with Postgres, Redis, and Worker.
  - Implement base FastAPI app with health checks.
- [ ] **Ticket 002: Database & Model Definition**
  - Configure SQLAlchemy and Alembic.
  - Create `User`, `Task`, and `Media` models.
- [ ] **Ticket 003: Environment & Configuration Management**
  - Implement Pydantic `Settings` to manage API keys for PhotoRoom, OpenAI, and Evolution API.

### Priority 2: Core Processing Logic
- [ ] **Ticket 004: PIL Branding Service**
  - Create a service to overlay a PNG watermark onto a base image.
  - Handle resizing and positioning logic.
- [ ] **Ticket 005: PhotoRoom Integration**
  - Implement client for background removal.
- [ ] **Ticket 006: Celery Task Orchestration**
  - Create the multi-step task chain: Vision -> PhotoRoom -> PIL.

### Priority 3: Messaging & Webhooks
- [ ] **Ticket 007: Evolution API Webhook Receiver**
  - Create an endpoint to receive messages.
  - Filter for images and trigger the Celery worker.
- [ ] **Ticket 008: Outbound Message Service**
  - Send the final processed image back to the user via Evolution API.

## First 3 Priority Tasks
1. **Ticket 001:** Initialize FastAPI & Celery Scaffold.
2. **Ticket 002:** Database & Model Definition.
3. **Ticket 003:** Environment & Configuration Management.

---

# BACKLOG: Phase 2 (Multi-Channel & Interaction)

## Goal
Enable multi-platform publishing (Instagram, Google) with a human-in-the-loop approval system via WhatsApp.

## Sprints & Tickets

### Priority 4: Human-in-the-Loop & State Management
- [ ] **Ticket 009: Interaction Logic (Keyword Commands)**
  - Implement logic in the webhook to listen for "Approve", "Post IG", or "Post Google".
  - Update `ContentJob` model to track the "Processed Image URL" and "Generated Captions" for later publishing.
- [ ] **Ticket 010: Persistent State for ContentJobs**
  - Ensure the system can retrieve the last processed job for a specific user when they send an approval command.

### Priority 5: Social Integrations
- [x] **Ticket 011: Instagram Graph API Integration**
  - Implement `app/services/instagram.py`.
  - Handle image upload, container creation, and final publishing.
- [ ] **Ticket 012: Google Business Profile Integration**
  - Implement `app/services/google_business.py`.
  - Handle local post creation for aesthetics/healthcare clinics.

### Priority 6: Verification & SMM Optimization
- [x] **Ticket 027: The Verification Loop**
  - Implement polling logic to verify `media_id` is live before sending WA confirmation.
- [ ] **Ticket 028: Auto-Resizer Module**
  - Implement PIL-based resizing to 4:5 (IG) and 4:3 (Google) to match SMM best practices.

---

# BACKLOG: Phase 3 (Scaling & Production)

## Goal
Prepare the system for multi-tenant usage, high-availability, and reliable resource management.

## Sprints & Tickets

### Priority 6: Multi-Tenancy & Resource Control
- [ ] **Ticket 017: Multi-Tenant Asset Isolation**
  - Implement `TenantStorageService` using the `/{tenant_id}/assets/` path pattern.
  - Migrated existing flat storage to the new structure.
- [ ] **Ticket 018: Quota Enforcement Logic**
  - Create a `QuotaManager` service to track and limit posts per tenant.
  - Implement Redis-backed counters for real-time quota checking.
- [ ] **Ticket 019: Dynamic Task Routing**
  - Refactor `app/celery_app.py` to route tasks dynamically based on tenant plan levels.
  - Configure workers to listen to `high_priority`, `default`, and `low_priority` queues.

---

# BACKLOG: Phase 4 (Verification & SMM Intelligence)

## Goal
Implement a robust verification loop for all publishing actions and introduce platform-specific intelligence based on SMM best practices.

## Sprints & Tickets

### Priority 7: Verification Loop
- [ ] **Ticket 022: Implementation of `verify_post` Task**
    - Refactor `app/tasks/image_processing.py` to include a polling loop for `media_id` status.
    - Implement fallback to web-scraping/URL validation for platforms with weak API status reporting.
    - Integration with WhatsApp notification service to alert on "Live" vs "Failed" status.

### Priority 8: SMM Intelligence Module
- [ ] **Ticket 023: Aspect Ratio & File Validation Service**
    - Create a pre-flight check service to validate image dimensions against `SMM_BEST_PRACTICES.md` before sending to platform APIs.
    - Automatically resize or pad images to meet platform requirements.
- [ ] **Ticket 024: Dynamic Hashtag & Caption Optimizer**
    - Refactor OpenAI prompt to strictly enforce hashtag density (3-5) and platform-specific character limits.
    - Implement local keyword injection for Google Business Profile posts.
- [ ] **Ticket 025: Intelligent Scheduling Engine**
    - Implement a "Queue with Jitter" to stagger posts.
    - Allow tenants to select "Peak Hour" slots based on the researched industry standards.

---

# BACKLOG: Phase 5 (Proactive Engagement & Compliance)

## Goal
Transform the agent from a reactive tool into a proactive brand partner while ensuring total legal safety.

## Sprints & Tickets

### Priority 9: Proactive Nudging (Engagement)
- [ ] **Ticket 026: Proactive Nudging Module**
    - Implement a scheduler (Celery Beat) to send proactive suggestions to admins.
    - Examples: "It's Monday! How about a photo of the team for the weekly vibe?", "New treatment day? Show the setup!"
    - Logic: Use the tenant's niche and location to tailor suggestions (e.g., local holidays, industry trends).

### Priority 10: Advanced Compliance & Security
- [ ] **Ticket 027: Multi-Admin Approval Implementation**
    - Refactor the approval workflow to require consensus from multiple `admin_jids`.
    - Implement WhatsApp interactive buttons for "Approve/Reject" that track which admin responded.
### Priority 11: Professional Aesthetic Module
- [x] **Ticket 029: The Professional Aesthetic Module**
    - **Logic:** Shift from "basic branding" to "automated professional production."
    - **Implemented:** 
        - `app/services/branding.py`: Added `professional_polish` with color grading (clinical white balance) and bokeh.
        - `app/services/enhancement.py`: Integrated Claid.ai for high-end retouching.
        - `app/tasks/image_processing.py`: Integrated enhancement and polish steps; enforced 4:5 Portrait ratio.
    - **Status:** COMPLETED. The agent now acts as a digital "Lighting & Retouching Assistant" before acting as a "Social Media Manager."
