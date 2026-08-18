from uuid import UUID

import pytest

from backend.app.domain.operator import Operator
from backend.app.services.operator import OperatorService


@pytest.mark.asyncio
async def test_create_operator_returns_domain_operator(
    session_factory,
) -> None:
    async with session_factory() as session:
        service = OperatorService(session)

        operator = await service.create(
            name="  Example Space Systems  ",
            country="India",
        )

        assert isinstance(operator, Operator)
        assert isinstance(operator.id, UUID)
        assert operator.name == "Example Space Systems"
        assert operator.normalized_name == "example space systems"
        assert operator.country == "India"


@pytest.mark.asyncio
async def test_create_operator_rejects_duplicate_name(
    session_factory,
) -> None:
    async with session_factory() as session:
        service = OperatorService(session)

        await service.create(
            name="Example Space Systems",
            country="India",
        )

        with pytest.raises(ValueError, match="already exists"):
            await service.create(
                name=" example space systems ",
                country="India",
            )


@pytest.mark.asyncio
async def test_get_operator_by_name_returns_domain_operator(
    session_factory,
) -> None:
    async with session_factory() as session:
        service = OperatorService(session)

        created = await service.create(
            name="Example Space Systems",
        )

        result = await service.get_by_name(
            "  EXAMPLE SPACE SYSTEMS  ",
        )

        assert isinstance(result, Operator)
        assert result is not None
        assert result.id == created.id
