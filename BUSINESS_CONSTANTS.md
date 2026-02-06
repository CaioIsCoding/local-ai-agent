# Business Constants & Strategy Definition

This document outlines the "Big Numbers" and business rules that drive the LocalAI Agent. All configuration related to SaaS tiers, quotas, and limits should be managed here or in `app/core/constants.py`.

## 1. SaaS Tiers (Subscription Model)

| Tier | Name | Monthly Cost (Hypothetical) | Post Limit | Key Features |
| :--- | :--- | :--- | :--- | :--- |
| **FREE** | Starter | $0 | **10 Posts/mo** | Basic Watermarking, Instagram Only |
| **PREMIUM** | Agency | $49 | **Unlimited** | Pro Retouching, Google Business, Video (Reels/Stories) |
| **ENTERPRISE** | Franchise | $199 | **Unlimited + Whitelabel** | Multi-Admin Approval, Dedicated Support |

## 2. Technical Quotas (Processing Limits)

- **Image Size:** Max 8MB (Instagram limit)
- **Video Size:** Max 50MB (Reels limit)
- **Processing Timeout:** 300 seconds (5 mins) per image to prevent hanging.

## 3. Compliance & Governance

- **Multi-Admin Quorum:** 
  - **Standard (Free/Premium):** 1 Admin approval required.
  - **Enterprise:** 2 Admin approvals required (Consensus).
- **Legal Guardrails:** 
  - No "Before/After" guarantees.
  - No price advertising for medical procedures.
