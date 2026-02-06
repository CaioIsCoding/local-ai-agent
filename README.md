# LocalAI Agent: Product & Technical Specification

**Version:** 1.0 (Initial Draft)
**Date:** February 6, 2026
**Target Niche:** Healthcare, Aesthetics, and Local Services (High-Ticket SMBs).
**Core Concept:** A friction-free, push-based marketing agent that lives in WhatsApp, automates content creation via AI, and synchronizes presence across Instagram and Google Maps.

---

## 📂 Strategic Documentation

As part of the BMAD method, this repository serves as a strategic knowledge base. Explore the following documents for deep dives into specific domains:

- [🔑 Credentials & Secrets](CREDENTIALS.md) - Centralized guide for API keys and environment variables.
- [📜 Legal Guardrails & Compliance](LEGAL_GUARDRAILS.md) - Analysis of CFM, CRM, and LGPD for AI agents.
- [💼 Business Constants](BUSINESS_CONSTANTS.md) - SaaS tiers, quotas, and pricing logic.
- [🔬 Research & Deep Dives](RESEARCH.md) - Adversarial findings and future R&D roadmap.
- [📱 SMM Best Practices](SMM_BEST_PRACTICES.md) - Social Media Marketing strategies optimized for Local AI.

---

## 1. Executive Summary

**The Problem:** Small business owners (SMBs) fail at marketing because existing tools (Canva, mLabs) require *initiative* (Pull). Owners do not have the time or skill to login to dashboards, edit photos, and write SEO copy.

**The Solution:** A **Push-based** agent. The system actively solicits raw content via WhatsApp ("Send me a photo"), processes it using Vision AI and Computer Vision pipelines, and posts optimized content to Google Business Profile (for conversion) and Instagram (for brand awareness) after a one-click approval.

**Key Differentiator:** "Zero-Friction" operations combined with "Hyper-Local Authority" (using RAG to leverage local news).

---

## 2. Roadmap & Phasing

### Phase 1: The MVP (The "Frictionless" Bot)
* **Goal:** Validate retention and daily usage.
* **Features:**
    * WhatsApp Push Notifications ("Send photo").
    * Basic Image Processing (Background removal + Logo application).
    * Dual-Copy Generation (SEO for Google vs. Engagement for Insta).
    * One-click Approval flow.
    * Automated Posting via Official APIs.

### Phase 2: The Authority Engine (Differentiation)
* **Goal:** Increase LTV and perceived value for High-Ticket clients (Doctors/Clinics).
* **Features:**
    * **Local News RAG:** Ingesting local news (via Tavily/Search APIs) to suggest contextual posts.
    * **Static Asset Library:** Fallback mechanism using professional stock photos if the client fails to send media.
    * **Reputation Management:** AI drafting responses to Google Reviews.

### Phase 3: Scale & Multimedia (The Upsell)
* **Goal:** Vertical expansion and higher pricing tiers.
* **Features:**
    * **AI Video Cuts:** Automated clipping of user-submitted videos with captions.
    * **Geofenced Ads:** "Boost this post" button directly in WhatsApp.
    * **White-label API:** Selling the engine to larger ERPs/Agencies.

---

## 3. Technical Architecture

The system is designed as an **Event-Driven, Asynchronous Microservice**.

### 3.1 Tech Stack
* **Interface:** WhatsApp Business API (via **Evolution API** or Z-API wrapper).
* **Backend:** **Python (FastAPI)**. Chosen for speed, async support, and rich AI ecosystem.
* **Task Queue:** **Redis + Celery**. Essential for handling image processing and API uploads without timing out the WhatsApp bot.
* **Database:** **PostgreSQL**. Relational data for Tenants, Auth Tokens, and Job Logs.
* **Storage:** **AWS S3** (or Supabase Storage). For raw and processed media assets.

### 3.2 The AI & Data Pipeline
* **LLM (Orchestrator):** `GPT-4o` (for Vision/Image understanding) & `GPT-4o-mini` (for copywriting/JSON formatting).
* **Computer Vision (The "Composition Engine"):**
    * **Segmentation:** **PhotoRoom API** (Best-in-class background removal).
    * **Composition:** **Pillow (PIL)** or **OpenCV**. Programmatic application of templates, logos, and typography. *Avoid Generative AI for the image itself to maintain realism.*
* **Data Retrieval (RAG):** **Tavily API**. To fetch real-time local news without brittle web scrapers.

---

## 4. Core Feature Specifications

### 4.1 Automated Onboarding (The Webview)
* **Mechanism:** A React/HTML Webview link sent via WhatsApp.
* **Logic:**
    1.  User clicks link -> Redirects to `auth.localai.com`.
    2.  User logs in via **Facebook Login** (Scope: `instagram_content_publish`, `pages_manage_posts`).
    3.  User logs in via **Google OAuth** (Scope: `business.manage`).
    4.  System captures `access_token` and `refresh_token`, encrypts them, and stores in Postgres `social_accounts`.
    5.  **Validation:** System checks if the Instagram account is "Business". If not, displays a tutorial.

### 4.2 The "Push" Trigger & Ingestion
* **Scheduler:** Cron job triggers based on client's preferred time (e.g., 09:00 AM).
* **Bot Logic:**
    * Check `last_post_date`.
    * If > 24h, send template message: *"Doctor, the clinic is busy today! Send me a photo of a procedure or the reception to keep your Google ranking up."*
* **Handling Inputs:**
    * User sends image -> Webhook receives payload.
    * Download image to S3 (`/raw`).
    * Trigger Celery Task: `process_image_pipeline`.

### 4.3 Image Composition Engine (Canvas-as-Code)
* **Input:** Raw messy photo.
* **Step 1 (Analysis):** GPT-4o Vision analyzes the image quality and subject (e.g., "Person", "Object", "Room").
* **Step 2 (Cleanup):** If subject is "Object/Person", call PhotoRoom API to remove background. If "Room", perform histogram equalization (brighten).
* **Step 3 (Branding):**
    * Load Client Template (defined in Onboarding).
    * Overlay Cleaned Image + Client Logo + Semi-transparent Gradient + Call to Action.
* **Output:** Save to S3 (`/processed`).

### 4.4 The Content Brain (SEO vs. Social)
* **Prompt Engineering Strategy:**
    * **Google Business Profile:** Strict instruction to focus on **Local SEO keywords**, location (Neighborhood/City), and transactional intent ("Schedule now").
    * **Instagram:** Focus on **Storytelling**, emojis, aesthetics, and broad hashtags.
* **Review:** System sends the processed image + both captions to WhatsApp with interactive buttons: `[✅ Approve]`, `[🔄 Try Again]`.

### 4.5 The "Local Insight" RAG (Phase 2)
* **Trigger:** Daily background job.
* **Process:**
    1.  Call Tavily API: `query="health news São Luís Maranhão today"`.
    2.  Filter results for relevance to client niche (e.g., Dermatology).
    3.  **If Match:** Bot proactively messages client: *"Doctor, news just came out about a UV index spike in São Luís. Shall we post a tip about sunscreen?"*

---

## 5. Database Schema Overview (Simplified)

```sql
CREATE TABLE tenants (
    id UUID PRIMARY KEY,
    business_name VARCHAR,
    niche VARCHAR, -- e.g., 'dermatology', 'restaurant'
    location_city VARCHAR, -- e.g., 'São Luís'
    branding_config JSONB -- {primary_color, logo_url, tone_of_voice}
);

CREATE TABLE social_accounts (
    tenant_id UUID REFERENCES tenants,
    platform VARCHAR, -- 'instagram', 'google'
    access_token TEXT, -- Encrypted
    refresh_token TEXT, -- Encrypted
    token_expires_at TIMESTAMP,
    external_id VARCHAR -- Page ID / Location ID
);

CREATE TABLE content_jobs (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants,
    status VARCHAR, -- 'waiting_media', 'processing', 'waiting_approval', 'posted'
    raw_media_url TEXT,
    processed_media_url TEXT,
    generated_copy_google TEXT,
    generated_copy_insta TEXT,
    created_at TIMESTAMP
);
```

## 6. Business Logic & Monetization

### Pricing Strategy (Anchor & Upsell)
* **Essential (R$ 199/mo):** 3 posts/week. Instagram Only.
* **Professional (R$ 399/mo):** Daily posts. Instagram + Google Business Profile. Includes "Local News" insights.
* **Enterprise (R$ 699/mo):** Above + Video Cuts + Reputation Management.

### Cost Analysis (Per Active Client/Month)
* **Infrastructure:** R$ 15.00 (Shared VPS/DB)
* **WhatsApp API:** R$ 10.00 (Marketing conversations)
* **AI (OpenAI/Tavily):** R$ 25.00
* **Image API:** R$ 10.00
* **Total COGS:** ~R$ 60.00
* **Gross Margin:** ~85% on Professional Plan.

## 7. Critical Risk Analysis & Mitigation

| Risk | Impact | Mitigation Strategy |
|---|---|---|
| Token Expiration | Critical (Service stops) | Auto-refresh jobs + "Reconnect" Alert via WhatsApp bot. |
| "Bad Photo" Input | High (Client dissatisfaction) | Detect low res/dark photos via Vision AI and reject/ask for new one immediately. |
| API Bans (Meta) | High | Use official APIs only. Randomize posting times (humanize). |
| Google Verification | Medium (Onboarding friction) | Manual assistance for the first 10 clients to get GBP verified. |
| Compliance (Health) | High (Legal) | Strict prompts preventing medical advice. Mandatory user approval step (Human-in-the-loop). |

## 8. Rollout Plan
* **Weeks 1-4:** Build Image Pipeline & WhatsApp Integration (Localhost).
* **Weeks 5-8:** Implement Auth Flows (OAuth) & Deploy to Cloud.
* **Week 9:** Alpha Test in São Luís. 3 Friendly Clients (Free).
* **Week 12:** Beta Launch. Niche down to Medical Clinics only. Sales via Direct Outreach showing the "Alpha" results.
