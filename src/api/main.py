"""FastAPI application factory."""


from fastapi import FastAPI

from src.api.dependencies import lifespan


def create_app() -> FastAPI:
    """Create FastAPI application instance.

    Returns:
        FastAPI: Configured application instance.
    """
    app = FastAPI(
        title="Telemetriya API",
        version="0.1.0",
        lifespan=lifespan,
    )

    return app


# Global app instance
app = create_app()
