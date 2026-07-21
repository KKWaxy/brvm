"""
Main entry point for the FastAPI application.
"""

import uvicorn
import logging
from app.api import create_app
from app.config import settings

logger = logging.getLogger(__name__)

app = create_app()


def main():
    """Run the FastAPI application."""
    log_level = "debug" if settings.debug else "info"
    logger.info("Starting application: %s", settings.app_name)
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        log_level=log_level,
    )


if __name__ == "__main__":
    main()
