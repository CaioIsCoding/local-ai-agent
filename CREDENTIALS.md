# 🗂️ Centralized Credentials & Secrets Guide

This document maps all external API keys and secrets required to run the LocalAI Agent. 

## ⚠️ Security Rules
- **DO NOT** commit real API keys to GitHub.
- **DO** use `.env` files for local development.
- **DO** use a secrets manager (e.g., AWS Secrets Manager, Doppler) for production.

---

## 1. Core Infrastructure
| Service | Key Name | Where to Get It | Purpose |
| :--- | :--- | :--- | :--- |
| **PostgreSQL** | `DATABASE_URL` | Docker Compose Default | Primary Data Store |
| **Redis** | `REDIS_URL` | Docker Compose Default | Celery Queue & Caching |

---

## 2. AI & Media Services
| Service | Key Name | Where to Get It | Purpose |
| :--- | :--- | :--- | :--- |
| **OpenAI** | `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/) | Vision Analysis (Image Understanding) & Caption Generation |
| **PhotoRoom** | `PHOTOROOM_API_KEY` | [PhotoRoom API](https://www.photoroom.com/api/) | Background Removal |
| **Claid.ai** | `CLAID_API_KEY` | [Claid.ai](https://claid.ai/) | High-End Retouching & Professional Polish |

---

## 3. WhatsApp (Evolution API)
| Service | Key Name | Where to Get It | Purpose |
| :--- | :--- | :--- | :--- |
| **Evolution API** | `EVOLUTION_API_URL` | Self-hosted Docker | WhatsApp Instance Management |
| | `EVOLUTION_API_KEY` | Evolution Dashboard | Authentication for WhatsApp |
| | `EVOLUTION_INSTANCE_NAME` | Evolution Dashboard | Name of the connected WhatsApp number |

---

## 4. Social Publishing
### Instagram (Meta Graph API)
| Key Name | Where to Get It | Purpose |
| :--- | :--- | :--- |
| `INSTAGRAM_ACCESS_TOKEN` | Meta Developer Portal | Posting images to Instagram Business Account |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Instagram App Settings | Identifying the target profile |

### Google Business Profile
| Key Name | Where to Get It | Purpose |
| :--- | :--- | :--- |
| `GOOGLE_CLIENT_ID` | Google Cloud Console | OAuth 2.0 Authentication |
| `GOOGLE_CLIENT_SECRET` | Google Cloud Console | OAuth 2.0 Authentication |
| `GOOGLE_REFRESH_TOKEN` | Google OAuth Playground | Long-lived access to GBP API |

---

## 5. Production Infrastructure
| Service | Key Name | Where to Get It | Purpose |
| :--- | :--- | :--- | :--- |
| **AWS S3** | `AWS_ACCESS_KEY_ID` | AWS IAM User | Storing processed images/video |
| | `AWS_SECRET_ACCESS_KEY` | AWS IAM User | Storing processed images/video |
| | `AWS_STORAGE_BUCKET_NAME` | AWS S3 Console | The bucket name |
| **Observability** | `SENTRY_DSN` | [Sentry.io](https://sentry.io/) | Error tracking and performance monitoring |

---

## 🚀 Setup Checklist
1. Copy `.env.example` to `.env`.
2. Fill in all keys listed above.
3. Run `docker-compose up --build`.
