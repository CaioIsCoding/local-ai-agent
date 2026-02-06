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

## 8. Scaling & Production
### Asset Isolation Strategy
To prevent cross-tenant branding leaks (e.g., Clinic A's logo appearing on Clinic B's posts), the storage layer implements a multi-tenant pathing structure.
- **Pattern:** `/{tenant_id}/assets/{asset_type}/{filename}`
- **Example:** `/tenant_123/assets/logos/main_logo.png`
- **Enforcement:** The `StorageService` prepends the `tenant_id` to all read/write operations.

### Post Quota System
Limits are enforced at the service layer before task dispatch:
- **Daily/Monthly Quotas:** Each tenant has a defined limit for "Social Media Management" posts.
- **Logic:** `QuotaService` checks current usage in Postgres/Redis before allowing `Task` creation.
- **Exhaustion:** Returns a `429 Too Many Requests` or sends a WhatsApp notification if the limit is reached.

### Priority Queuing
Celery is configured with multiple queues to ensure high-value tenants or urgent tasks are processed first:
- **`high_priority`:** For "Premium" plan tenants or manual "Urgent" triggers.
- **`default`:** Standard processing for regular accounts.
- **`low_priority`:** Background tasks like periodic cleanup or historical data syncing.
- **Routing Logic:** The worker determines the queue at runtime based on the user's `plan_level`.

## 10. Multi-Admin Approval & Legal Guardrails
To ensure security and compliance, especially in sensitive niches like healthcare, the system implements a "Multi-Eye" approval flow.

### Multi-Admin Approval Flow
1. **Trigger:** An admin (Admin A) sends an image or triggers a publishing request.
2. **Notification:** The agent notifies all registered admins (`admin_jids`) for that tenant.
3. **Consensus:** The post remains in `PENDING_APPROVAL` until a second admin (Admin B or C) confirms, or until a designated "Super Admin" overrides.
4. **Execution:** Once approved by the required number of admins, the publishing pipeline proceeds.

### Legal Compliance Check
Before any AI-generated caption or processed image is finalized, it passes through a **Legal Guardrail Layer**:
- **Vision Compliance:** OpenAI Vision checks for forbidden content (e.g., "Before & After" medical photos, explicit pricing in images).
- **Text Compliance:** NLP check for "guaranteed results" or missing professional registration (CRM/RQE).
- **Result:** If a violation is detected, the job is flagged for manual review and the admins are notified of the specific legal risk.

## 9. Post Verification (The "Verification-First" Flow)
To ensure high reliability and data integrity in automated publishing, we implement a **two-step verification flow**:

1.  **Request Post:** The system initiates the publishing request to the target platform (Instagram, Facebook, Google).
2.  **Verify Live Status:** Instead of assuming success upon a 200 OK from the API, the system enters a verification loop:
    - **API Check:** Polling `GET /media_id` to confirm the post reached a `PUBLISHED` state.
    - **Scraping/Public Check:** If the API is unreliable or limited, the system performs a lightweight public URL check (if available) to verify the content is live and visible.
    - **Confirmation:** Only after successful verification is the user notified that the post is "Live". If verification fails after max retries, the system triggers a `PUBLICATION_FAILED` alert.
