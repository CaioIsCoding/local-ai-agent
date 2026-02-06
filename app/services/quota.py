import redis
from app.core.config import settings
from app.core.constants import PlanConfig
from app.database import SessionLocal

r = redis.from_url(settings.REDIS_URL)

class QuotaService:
    """
    Manages tenant quotas using Redis for high-performance counting.
    """
    def check_quota(self, tenant_id: int, plan_tier: str) -> bool:
        """
        Returns True if the tenant can post, False if limit reached.
        """
        key = f"quota:{tenant_id}"
        
        if plan_tier == PlanConfig.PREMIUM or plan_tier == PlanConfig.ENTERPRISE:
            return True # Unlimited

        current = r.get(key)
        if current is None:
            r.set(key, 0)
            return True
        
        if int(current) >= PlanConfig.QUOTA_FREE:
            return False
        
        return True

    def increment_usage(self, tenant_id: int):
        key = f"quota:{tenant_id}"
        r.incr(key)
        # Optional: Set expiry to reset monthly (requires cron/celery beat)

quota_service = QuotaService()
