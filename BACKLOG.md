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
