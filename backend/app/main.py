from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="MissionScout",
        version="0.1.0",
        description="Satellite servicing opportunity intelligence platform",
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
