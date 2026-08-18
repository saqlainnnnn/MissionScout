from fastapi import FastAPI

from backend.app.api.routes.events import router as events_router
from backend.app.api.routes.sources import router as sources_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="MissionScout",
        version="0.1.0",
        description="Satellite servicing opportunity intelligence platform",
    )

    app.include_router(
        events_router,
        prefix="/api/v1",
    )

    app.include_router(
        sources_router,
        prefix="/api/v1",
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
