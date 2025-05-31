# src/api/middleware.py
"""Custom middleware for the application."""

import time
from typing import Callable

import structlog
from fastapi import Request, Response
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

REQUEST_SIZE = Histogram(
    'http_request_size_bytes',
    'HTTP request size in bytes',
    ['method', 'endpoint']
)

RESPONSE_SIZE = Histogram(
    'http_response_size_bytes',
    'HTTP response size in bytes',
    ['method', 'endpoint']
)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for structured request logging."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with logging."""
        start_time = time.time()
        
        # Extract request info
        method = request.method
        url = str(request.url)
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Log request
        logger.info(
            "Request started",
            method=method,
            path=path,
            client_ip=client_ip,
            user_agent=user_agent
        )
        
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                "Request completed",
                method=method,
                path=path,
                status_code=response.status_code,
                duration=duration,
                client_ip=client_ip
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            logger.error(
                "Request failed",
                method=method,
                path=path,
                duration=duration,
                error=str(e),
                client_ip=client_ip
            )
            raise


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware for Prometheus metrics collection."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with metrics collection."""
        start_time = time.time()
        
        method = request.method
        path = request.url.path
        
        # Skip metrics endpoint
        if path == "/metrics":
            return await call_next(request)
        
        # Request size
        request_size = int(request.headers.get("content-length", 0))
        REQUEST_SIZE.labels(method=method, endpoint=path).observe(request_size)
        
        try:
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            status = str(response.status_code)
            
            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status=status
            ).inc()
            
            REQUEST_DURATION.labels(
                method=method,
                endpoint=path
            ).observe(duration)
            
            # Response size
            response_size = 0
            if hasattr(response, "body"):
                response_size = len(response.body)
            
            RESPONSE_SIZE.labels(
                method=method,
                endpoint=path
            ).observe(response_size)
            
            return response
            
        except Exception as e:
            # Record error metrics
            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status="500"
            ).inc()
            
            duration = time.time() - start_time
            REQUEST_DURATION.labels(
                method=method,
                endpoint=path
            ).observe(duration)
            
            raise
