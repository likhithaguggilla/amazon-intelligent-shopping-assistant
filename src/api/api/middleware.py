import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware that adds a unique request ID to each request."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        
        # Add request_id to request state
        request.state.request_id = request_id
        
        # Log request start
        logger.info(f"Request started: {request.method} {request.url.path} (request_id: {request_id})")
        
        # Process the request
        response = await call_next(request)
        
        # Add request_id to response headers
        response.headers["X-Request-ID"] = request_id
        
        # Log request completion
        logger.info(f"Request completed: {request.method} {request.url.path} (request_id: {request_id})")
        
        return response