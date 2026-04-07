"""
Main entry point for the FastAPI application.
"""

import uvicorn

from app.api import create_app
from app.config import settings

app = create_app()


def main():
    """Run the FastAPI application."""
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
    )


if __name__ == "__main__":
    main()
