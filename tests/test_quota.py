import pytest
from unittest.mock import MagicMock
from app.services.quota import QuotaService
from app.core.constants import PlanConfig

@pytest.fixture
def quota_service():
    return QuotaService()

@pytest.fixture
def mock_r():
    from app.services.quota import r
    return r

def test_check_quota_free_below_limit(quota_service, mock_r):
    mock_r.get.return_value = "5"
    assert quota_service.check_quota(1, PlanConfig.FREE) is True

def test_check_quota_free_at_limit(quota_service, mock_r):
    # Limit is 10. If current is 10, it should return False
    mock_r.get.return_value = "10"
    assert quota_service.check_quota(1, PlanConfig.FREE) is False

def test_check_quota_free_above_limit(quota_service, mock_r):
    mock_r.get.return_value = "11"
    assert quota_service.check_quota(1, PlanConfig.FREE) is False

def test_check_quota_premium_unlimited(quota_service, mock_r):
    mock_r.get.return_value = "100"
    assert quota_service.check_quota(1, PlanConfig.PREMIUM) is True

def test_check_quota_enterprise_unlimited(quota_service, mock_r):
    mock_r.get.return_value = "100"
    assert quota_service.check_quota(1, PlanConfig.ENTERPRISE) is True

def test_check_quota_new_user(quota_service, mock_r):
    mock_r.get.return_value = None
    assert quota_service.check_quota(1, PlanConfig.FREE) is True
    mock_r.set.assert_called_with("quota:1", 0)

def test_increment_usage(quota_service, mock_r):
    quota_service.increment_usage(1)
    mock_r.incr.assert_called_with("quota:1")
