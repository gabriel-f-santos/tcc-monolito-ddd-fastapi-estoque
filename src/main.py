# src/main.py
"""Main application module."""

import time
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from src.api.middleware import LoggingMiddleware, PrometheusMiddleware
from src.api.routers import auth, usuarios, produtos, estoque, movimentacoes, relatorios, health
from src.config import get_settings
from src.shared.infrastructure.database.connection import init_db, close_db
from src.shared.infrastructure.logging.setup import setup_logging

# # Metrics
# REQUEST_COUNT = Counter(
#     'http_requests_total',
#     'Total HTTP requests',
#     ['method', 'endpoint', 'status']
# )
# REQUEST_DURATION = Histogram(
#     'http_request_duration_seconds',
#     'HTTP request duration',
#     ['method', 'endpoint']
# )

settings = get_settings()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging(settings.log_level, settings.log_format)
    logger.info("Starting application", project=settings.project_name)
    
    # Initialize database
    await init_db(settings.database_url)
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    await close_db()
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    """Create FastAPI application instance."""
    
    app = FastAPI(
        title=settings.project_name,
        description="Sistema de Gerenciamento de Estoque - TCC",
        version="1.0.0",
        debug=settings.debug,
        lifespan=lifespan,
        docs_url=f"{settings.api_v1_str}/docs",
        redoc_url=f"{settings.api_v1_str}/redoc",
        openapi_url=f"{settings.api_v1_str}/openapi.json"
    )
    
    # Middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts + ["*"]  # Allow all in dev
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Custom middleware
    app.add_middleware(LoggingMiddleware)
    
    # if settings.prometheus_enabled:
    #     app.add_middleware(PrometheusMiddleware)
    
    # Routers
    app.include_router(
        health.router,
        prefix=f"{settings.api_v1_str}/health",
        tags=["Health"]
    )
    
    app.include_router(
        auth.router,
        prefix=f"{settings.api_v1_str}/auth",
        tags=["Authentication"]
    )
    
    app.include_router(
        usuarios.router,
        prefix=f"{settings.api_v1_str}/usuarios",
        tags=["Usuários"]
    )
    
    app.include_router(
        produtos.router,
        prefix=f"{settings.api_v1_str}/produtos",
        tags=["Produtos"]
    )
    
    app.include_router(
        estoque.router,
        prefix=f"{settings.api_v1_str}/estoque",
        tags=["Estoque"]
    )
    
    app.include_router(
        movimentacoes.router,
        prefix=f"{settings.api_v1_str}/movimentacoes",
        tags=["Movimentações"]
    )
    
    app.include_router(
        relatorios.router,
        prefix=f"{settings.api_v1_str}/relatorios",
        tags=["Relatórios"]
    )
    
    # Prometheus metrics endpoint
    if settings.prometheus_enabled:
        @app.get("/metrics")
        async def metrics():
            """Prometheus metrics endpoint."""
            return Response(
                generate_latest(),
                media_type=CONTENT_TYPE_LATEST
            )
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Inventory Management System API",
            "version": "1.0.0",
            "docs": f"{settings.api_v1_str}/docs"
        }
    
    return app


# Create application instance
app = create_app()