"""
FastAPI application factory with security hardening and optional rate limiting.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable

from app.config import settings
from app.routes import router
from app.auth_routes import router as auth_router
from app.database import init_db
from app.loader import load_sgi_data

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add common security headers to all responses."""

    async def dispatch(self, request, call_next: Callable):
        response: Response = await call_next(request)
        # Prevent clickjacking
        response.headers.setdefault("X-Frame-Options", "DENY")
        # Prevent MIME sniffing
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        # XSS protection
        response.headers.setdefault("X-XSS-Protection", "1; mode=block")
        # Referrer policy
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        # Content-Security-Policy could be added here per app requirements
        return response


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    - Applies secure defaults
    - Configures CORS from settings (no wildcard in production)
    - Adds TrustedHost and optional HTTPS redirect
    - Registers routers
    - Initializes DB and schedules data loading on startup
    """
    # Basic logging configuration
    logging.basicConfig(level=logging.INFO)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    # Trusted hosts
    try:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts)
    except Exception:
        logger.exception("Failed to configure TrustedHostMiddleware")

    # HTTPS redirect in production if enabled
    if settings.enforce_https:
        app.add_middleware(HTTPSRedirectMiddleware)

    # Add security headers
    app.add_middleware(SecurityHeadersMiddleware)

    # CORS configuration: prefer explicit list from environment
    cors_origins = settings.cors_origins or []

    if not cors_origins:
        # No origins configured: be conservative and disable wide-open CORS
        logger.info("No CORS origins configured. Restricting cross-origin requests by default.")
    else:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=settings.allow_credentials,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include routers
    app.include_router(auth_router)
    app.include_router(router)

    # Initialize database and schedule data loading at startup
    @app.on_event("startup")
    async def startup_event():
        logger.info("Initializing database and loading static data (if any)")
        try:
            init_db()
        except Exception:
            logger.exception("Database initialization failed")
            raise

        try:
            # loader is synchronous; call directly (fast) or run in threadpool if heavy
            load_sgi_data()
        except Exception:
            logger.exception("Failed to load CSV data")

    return app
