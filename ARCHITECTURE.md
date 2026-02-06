# ARCHITECTURE: Local AI Agent

## 1. Project Overview
A local AI-driven automation agent designed to handle image processing, branding, and multi-channel publishing.

## 2. Tech Stack
- **Framework:** FastAPI (Python 3.10+)
- **Task Queue:** Celery with Redis broker
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Image Processing:** Vision AI, PhotoRoom API, PIL (Python Imaging Library)
- **Integrations:** Evolution API (WhatsApp), OpenAI, Instagram Graph API, Google Business Profile API

## 3. Project Structure
```text
local-ai-agent/
├── app/
│   ├── api/              # FastAPI Routes
│   │   ├── v1/
│   │   └── deps.py       # Dependencies (DB, Auth)
│   ├── core/             # Configuration & Security
│   ├── crud/             # Database CRUD operations
│   ├── models/           # SQLAlchemy Models
│   ├── schemas/          # Pydantic Schemas
│   ├── services/         # Logic for External APIs
│   │   ├── evolution.py
│   │   ├── photoroom.py
│   │   └── openai.py
│   └── worker.py         # Celery Worker definition
├── tasks/                # Celery Task implementations
│   └── image_processing.py
├── migrations/           # Alembic migrations
├── tests/
├── .env.example
├── docker-compose.yml
└── main.py               # Application entry point
```

## 4. Image Processing Pipeline (Celery)
The pipeline is designed as a series of atomic tasks to ensure reliability and retries:
1.  **Vision Analysis:** Analyze incoming image using OpenAI Vision to determine content and context.
2.  **Background Removal:** Send image to PhotoRoom API to remove backgrounds or apply specific templates.
3.  **Branding (PIL):** Overlay local branding (logos, watermarks, text) using PIL.
4.  **Final Polish:** Optimization for target platforms.

## 5. Database Schema (Postgres)
- **Users:** System authentication and API keys.
- **Tasks:** Track processing status (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`).
- **Media:** Metadata for processed images (original URL, processed URL, tags).
- **Integrations:** Credentials and webhooks for Evolution API, Instagram, etc.

## 6. API Integration Points
- **Evolution API:** Inbound WhatsApp messages trigger the workflow.
- **OpenAI:** GPT-4o for vision analysis and caption generation.
- **PhotoRoom:** High-quality background removal and compositing.
- **Instagram/Google:** Final publishing destinations.

## 7. Testing Strategy (Contract-First)
We prioritize **Contract Testing** over unit testing to ensure the integrity of the asynchronous pipeline and its reliance on external APIs.

### The "Contracts"
1. **Inbound Webhook (Evolution API → LocalAI):**
    - **Trigger:** `messages.upsert`
    - **Expectation:** Valid JID, message type (image), and media key/URL.
2. **AI Analysis (LocalAI → OpenAI):**
    - **Request:** Image bytes + System Prompt.
    - **Response:** Strict JSON object containing `social_caption`, `seo_caption`, and `branding_suggestions`.
3. **Background Removal (LocalAI → PhotoRoom):**
    - **Request:** Multipart image file.
    - **Response:** Binary stream of a transparent PNG.
4. **Outbound Message (LocalAI → Evolution API):**
    - **Request:** Valid `remote_jid`, base64 image payload, and formatted caption text.
5. **Persistence (LocalAI → Database):**
    - **Expectation:** `ContentJob` reflects the correct state transition (`pending` → `processing` → `completed`).
