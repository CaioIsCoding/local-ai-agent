# Research & Deep Dive Documentation

## Adversarial Round Findings

### Human-in-the-Loop (HITL) vs. Auto-post Trade-offs
- **HITL:** Increases safety and compliance but slows down throughput. Crucial for medical/sensitive content.
- **Auto-post:** Higher scalability and speed, but requires robust automated guardrails and forensic AI to prevent compliance violations.

### Multi-tenant Isolation Strategies
- Logical isolation via schema-based or row-level security (RLS) in databases.
- Containerization or separate worker queues for high-risk tenants.
- Token-level rate limiting and resource quotas per tenant.

### Compliance Challenges (CFM/CRM/LGPD)
- **CFM/CRM:** Strict regulations on medical advertising and patient privacy. Requires "soft" AI filters and mandatory human review for diagnostic-adjacent content.
- **LGPD:** Brazilian data protection law requiring explicit consent, data minimization, and right to erasure. Multi-tenant systems must ensure data never leaks between instances.

## Next Steps for Deep Dives

### Deep Dive A: Image Forensic & Compliance AI
Researching models specific to medical skin analysis/safety. Focus on identifying non-compliant visual elements (e.g., "before and after" photos prohibited in some regions) and ensuring privacy through PII masking in images.

### Deep Dive B: WhatsApp Native Engagement Patterns
Researching how to maximize response rates for "Approve" commands. Testing button-based templates vs. natural language confirmation to reduce friction for the "Human-in-the-loop" step.

### Deep Dive C: Distributed Task Priority
Researching Redis/Celery strategies for 10,000+ concurrent jobs across different subscription plans. Implementing tiered priority queues (e.g., 'platinum' vs 'standard') and fair-use scheduling.
