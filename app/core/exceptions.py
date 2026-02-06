class LocalAIError(Exception):
    """Base exception for Local AI Agent"""
    pass

class ExternalAPIError(LocalAIError):
    """Raised when an external API call fails"""
    def __init__(self, service_name, status_code, message):
        self.service_name = service_name
        self.status_code = status_code
        self.message = message
        super().__init__(f"Error from {service_name} (Status: {status_code}): {message}")

class RateLimitError(ExternalAPIError):
    """Raised when we hit an API rate limit (429)"""
    pass

class ServiceUnavailableError(ExternalAPIError):
    """Raised when an external service is down (500, 503, etc)"""
    pass

class AuthError(ExternalAPIError):
    """Raised when there's an authentication error (401, 403)"""
    pass
