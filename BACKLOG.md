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
- [ ] **Ticket 011: Instagram Graph API Integration**
  - Implement `app/services/instagram.py`.
  - Handle image upload, container creation, and final publishing.
- [ ] **Ticket 012: Google Business Profile Integration**
  - Implement `app/services/google_business.py`.
  - Handle local post creation for aesthetics/healthcare clinics.
