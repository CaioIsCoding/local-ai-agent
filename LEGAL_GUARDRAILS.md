# LEGAL_GUARDRAILS: Brazilian Medical & Aesthetic Advertising

This document outlines the legal constraints and compliance rules for the Local AI Agent, specifically tailored to the Brazilian market (CFM, CRM, and CONAR).

## 1. CFM Resolution 2.336/2023 (Medical Advertising)
The Federal Council of Medicine (CFM) updated its rules in 2023 (effective March 2024).

### Key Rules for Content Generation:
- **Identification:** Every post must include the doctor's Name, CRM number, and RQE (Specialist Registration) if a specialty is mentioned.
- **Before & After (Selfies and Results):**
    - Allowed ONLY for educational purposes.
    - Must NOT be sensationalist.
    - Must include the physician's identification in the image or caption.
    - Must have explicit patient consent (stored outside this agent).
    - Avoid using filters that distort the actual result.
- **No Promise of Results:** Captions must never guarantee a specific outcome (e.g., "Get the perfect body in 10 days"). Use "possibility," "individual results may vary," etc.
- **Pricing & Promotions:** Do not advertise prices, discounts, or payment methods in public posts (Instagram/Google). These must be handled via DM or private channels.
- **Equipment & Drugs:** Mentioning specific equipment (e.g., "Ultraformer") is allowed, but must not imply superiority over other treatments or focus on the commercial brand rather than the technique.

## 2. Aesthetic & Biomedical Rules (CRBM / COFEN)
Biomedics and Nurses also have specific boards (CRBM, COFEN). Generally, they follow similar patterns to CFM regarding sensationalism.

## 3. CONAR (Brazilian Advertising Self-Regulation)
- **Truthfulness:** No misleading claims.
- **Clear Identification:** If a post is an ad (paid), it must be clearly labeled (though this agent focuses on organic posting).

## 4. AI Compliance Check (Prompt Logic)
The OpenAI Vision and GPT prompts are configured to flag:
1.  **Sensationalist Language:** Words like "Miracle," "Guaranteed," "Zero Pain."
2.  **Missing Credentials:** Lack of CRM/RQE in medical niche posts.
3.  **Forbidden "Before & After":** If the niche is medical and the image shows a side-by-side without educational context.
4.  **Pricing Disclosure:** Any mention of "R$" or values in captions.

## 5. Enforcement Levels
- **Level 1 (Warning):** The agent notifies the admin that the content might violate CRM rules but allows proceeding with manual approval.
- **Level 2 (Block):** The agent refuses to post if a critical violation is found (e.g., explicit price in a medical post).
