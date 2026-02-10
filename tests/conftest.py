import sys
from unittest.mock import MagicMock

# NOTE: The following mocks are necessary because the current testing environment
# does not have the required production dependencies (redis, sqlalchemy, etc.) installed.
# Mocking these in sys.modules allows pytest to collect and run tests that import
# modules dependent on these packages.

# Mock redis
mock_redis = MagicMock()
sys.modules["redis"] = mock_redis

# Mock sqlalchemy
mock_sqlalchemy = MagicMock()
sys.modules["sqlalchemy"] = mock_sqlalchemy
sys.modules["sqlalchemy.orm"] = MagicMock()
sys.modules["sqlalchemy.exc"] = MagicMock()

# Mock pydantic-settings
mock_pydantic_settings = MagicMock()
sys.modules["pydantic_settings"] = mock_pydantic_settings
sys.modules["pydantic"] = MagicMock()

# Mock app.core.config (original import path in quota.py)
mock_settings = MagicMock()
mock_settings.REDIS_URL = "redis://localhost:6379/0"
sys.modules["app.core.config"] = MagicMock(settings=mock_settings)

# Mock app.database
sys.modules["app.database"] = MagicMock()
