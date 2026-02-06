# SMM Best Practices for Automated Management

This document outlines industry standards and technical constraints for social media management (SMM) within the Local AI Agent ecosystem.

## 1. Visual Content Standards

### Image Aspect Ratios (2026 Standards)
| Platform | Recommended Ratio | Ideal Resolution | Usage |
| :--- | :--- | :--- | :--- |
| **Instagram/FB** | 1:1 (Square) | 1080 x 1080 px | Standard Feed |
| **Instagram/FB** | 4:5 (Portrait) | 1080 x 1350 px | Optimized Feed (Max Screen) |
| **Stories/Reels** | 9:16 (Vertical) | 1080 x 1920 px | Full Screen |
| **LinkedIn** | 1.91:1 or 1:1 | 1200 x 627 px | Professional Feed |
| **Google BP** | 4:3 or 1:1 | 720 x 720 px (min) | Local Search Results |

### Technical Checks
- **File Format:** Prefer JPEG for feed posts (smaller size) and PNG for branded content with overlays.
- **File Size:** Keep under 8MB for Instagram; under 5MB for Google Business Profile.
- **Safety Zones:** Ensure text and logos are centered; avoid placing critical information in the top/bottom 15% to prevent UI overlap in Stories.

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
