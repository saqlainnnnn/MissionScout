import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.app.models.base import Base

# Import models so they are registered with Base.metadata.
from backend.app.models.intelligence_event import IntelligenceEvent  # noqa: F401
from backend.app.models.operator import OperatorModel  # noqa: F401
from backend.app.models.outbox_event import OutboxEvent  # noqa: F401
from backend.app.models.source import Source  # noqa: F401


TEST_DATABASE_URL = (
    "postgresql+asyncpg://"
    "missionscout:missionscout@localhost:5434/"
    "missionscout_test"
)


@pytest_asyncio.fixture
async def session_factory():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    try:
        yield session_factory
    finally:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

        await engine.dispose()
