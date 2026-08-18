from uuid import uuid4

import pytest

from backend.app.models.operator import OperatorModel
from backend.app.models.satellite import SatelliteModel
from backend.app.repositories.satellite import SatelliteRepository


@pytest.mark.asyncio
async def test_create_satellite_for_operator(
    session_factory,
) -> None:
    async with session_factory() as session:
        operator = OperatorModel(
            name="Example Space Systems",
            normalized_name="example space systems",
            country="India",
        )

        session.add(operator)
        await session.commit()
        await session.refresh(operator)

        repository = SatelliteRepository(session)

        satellite = SatelliteModel(
            name="IS-901",
            normalized_name="is-901",
            orbit_type="GEO",
            status="operational",
            operator_id=operator.id,
        )

        created = await repository.create(satellite)
        await session.commit()

        result = await repository.get_by_id(created.id)

        assert result is not None
        assert result.id == created.id
        assert result.operator_id == operator.id
        assert result.name == "IS-901"


@pytest.mark.asyncio
async def test_get_satellites_for_operator(
    session_factory,
) -> None:
    async with session_factory() as session:
        operator = OperatorModel(
            name="Example Space Systems",
            normalized_name="example space systems",
        )

        session.add(operator)
        await session.commit()
        await session.refresh(operator)

        repository = SatelliteRepository(session)

        first = SatelliteModel(
            name="IS-901",
            normalized_name="is-901",
            orbit_type="GEO",
            status="operational",
            operator_id=operator.id,
        )

        second = SatelliteModel(
            name="IS-902",
            normalized_name="is-902",
            orbit_type="GEO",
            status="operational",
            operator_id=operator.id,
        )

        await repository.create(first)
        await repository.create(second)
        await session.commit()

        result = await repository.get_by_operator_id(operator.id)

        assert len(result) == 2
        assert {item.name for item in result} == {"IS-901", "IS-902"}


@pytest.mark.asyncio
async def test_unknown_operator_has_no_satellites(
    session_factory,
) -> None:
    async with session_factory() as session:
        repository = SatelliteRepository(session)

        result = await repository.get_by_operator_id(uuid4())

        assert result == []
