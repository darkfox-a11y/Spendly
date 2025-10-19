# app/core/rate_limiter.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Global limiter instance
limiter = Limiter(key_func=get_remote_address)

# Exception handler to attach in main.py
rate_limit_handler = _rate_limit_exceeded_handler
RateLimitExceeded = RateLimitExceeded
