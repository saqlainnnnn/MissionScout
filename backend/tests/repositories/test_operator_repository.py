from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.app.models.operator import OperatorModel
from backend.app.repositories.operator import OperatorRepository


@pytest.mark.asyncio
async def test_create_and_get_operator(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with session_factory() as session:
        repository = OperatorRepository(session)

        operator = OperatorModel(
            name="Example Space Systems",
            normalized_name="example space systems",
            country="India",
        )

        created = await repository.create(operator)
        await session.commit()

        result = await repository.get_by_id(created.id)

        assert result is not None
        assert result.id == created.id
        assert result.name == "Example Space Systems"
        assert result.country == "India"


@pytest.mark.asyncio
async def test_get_by_normalized_name(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with session_factory() as session:
        repository = OperatorRepository(session)

        operator = OperatorModel(
            name="Example Space Systems",
            normalized_name="example space systems",
        )

        await repository.create(operator)
        await session.commit()

        result = await repository.get_by_normalized_name(
            "example space systems",
        )

        assert result is not None
        assert result.name == "Example Space Systems"


@pytest.mark.asyncio
async def test_get_by_unknown_id_returns_none(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with session_factory() as session:
        repository = OperatorRepository(session)

        result = await repository.get_by_id(uuid4())

        assert result is None
