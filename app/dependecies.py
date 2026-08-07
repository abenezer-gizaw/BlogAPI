from fastapi import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address



limiter = Limiter(key_func= get_remote_address, default_limits= ["10 per minute"])


def rate_limit_dependency (request:Request):
    limiter._check_request_limit(request, endpoint_func= None)