# SMM Best Practices for Automated Management

This document outlines industry standards and technical constraints for social media management (SMM) within the Local AI Agent ecosystem.

## 1. Visual Content Standards

### Image Aspect Ratios (2026 Standards)
| Platform | Recommended Ratio | Ideal Resolution | Usage |
| :--- | :--- | :--- | :--- |
| **Instagram/FB** | 4:5 (Portrait) | 1080 x 1350 px | **PREMIUM STANDARD (Default)** |
| **Instagram/FB** | 1:1 (Square) | 1080 x 1080 px | Legacy Standard Feed |
| **Stories/Reels** | 9:16 (Vertical) | 1080 x 1920 px | Full Screen |
| **LinkedIn** | 1.91:1 or 1:1 | 1200 x 627 px | Professional Feed |
| **Google BP** | 4:3 or 1:1 | 720 x 720 px (min) | Local Search Results |

### Automated Professional Production (The "Luxury Standard")
To differentiate from basic automated tools, the agent applies an automated retouching and lighting pipeline:
- **High-End Retouching:** Integrated with Claid.ai for smart-enhancement, noise reduction, and "polishing."
- **Professional Polish:**
    - **Color Grading:** Applied to achieve a "clinical/luxury" white balance (slight brightness boost, cooling color temperature).
    - **Depth of Field (Bokeh):** Subtle Gaussian blur applied to backgrounds to create subject-background separation.
- **Aspect Ratio Enforcement:** All output defaults to 4:5 (Portrait) unless otherwise specified, ensuring maximum screen real estate and a "premium" editorial feel.

## 2. Copywriting & SEO (The "Caption Engine")

### Platform Caption Limits
- **Instagram:** 2,200 characters (optimal: 125-150 for engagement).
- **LinkedIn:** 3,000 characters (optimal: 200-400 with a clear "hook").
- **Google BP:** 1,500 characters (optimal: 150-300 with local keywords).

### SEO & Hashtag Density
- **Hashtag Density:** Use 3-5 highly relevant hashtags. Avoid "hashtag stuffing" (30+), as modern algorithms prioritize context over volume.
- **Keyword Placement:** Include primary keywords (e.g., "Aesthetic Clinic Sao Paulo") in the first two lines of the caption.
- **Call to Action (CTA):** Every post must include a CTA (e.g., "Link in Bio", "DM for details").

## 3. Scheduling & Intelligence

### Peak-Hour Strategy (Industry Averages)
*Note: The agent should eventually adapt these based on tenant-specific engagement data.*
- **B2B (LinkedIn):** Tuesday - Thursday, 09:00 - 12:00.
- **B2C (Instagram):** Monday - Friday, 11:00 - 13:00 and 19:00 - 21:00.
- **Local Services (Google):** Thursday - Saturday, 10:00 - 14:00.

### Automated Queueing
- **Staggered Posting:** Avoid publishing to multiple platforms at the exact same second to mimic human behavior.
- **Retry Logic:** Use exponential backoff for API failures, especially during global platform outages.
