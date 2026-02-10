# Centralized Business & Plan Constants
# All "Big Numbers" and Strategy definitions should live here.
# Do not hardcode limits in logic; import from here.

class PlanConfig:
    """
    Defines the tiers and limits for our SaaS offering.
    """
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

    # Quotas (posts per month)
    QUOTA_FREE = 10
    QUOTA_PREMIUM = -1  # -1 implies unlimited
    QUOTA_ENTERPRISE = -1

    # Feature Flags
    FEATURES_PREMIUM = ["auto_resize", "video_processing", "advanced_analytics"]
    FEATURES_ENTERPRISE = FEATURES_PREMIUM + ["dedicated_support", "custom_branding"]

class ProcessingLimits:
    """
    Technical constraints for image/video processing.
    """
    MAX_IMAGE_SIZE_MB = 8
    MAX_VIDEO_SIZE_MB = 50
    SUPPORTED_IMAGE_FORMATS = ["image/jpeg", "image/png", "image/webp"]
    SUPPORTED_VIDEO_FORMATS = ["video/mp4", "video/quicktime"]

    # Aspect Ratios (Enforced for SMM Standards)
    RATIO_FEED = (4, 5)  # 1080x1350
    RATIO_STORY = (9, 16) # 1080x1920
    RATIO_SQUARE = (1, 1) # 1080x1080

    # Standard Dimensions for Image Processing
    WIDTH_STANDARD = 1080
    HEIGHT_FEED = 1350
    HEIGHT_SQUARE = 1080

class Compliance:
    """
    Legal and Safety Guardrails.
    """
    MIN_APPROVERS_ENTERPRISE = 2
    MIN_APPROVERS_SMB = 1

class FeatureFlags:
    """
    Feature toggles for Beta/Alpha testing.
    """
    FEATURE_VIDEO_CUTTING = True
