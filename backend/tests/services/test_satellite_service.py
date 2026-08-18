from uuid import UUID, uuid4

import pytest

from backend.app.domain.satellite import Satellite
from backend.app.models.operator import OperatorModel
from backend.app.services.satellite import SatelliteService


@pytest.mark.asyncio
async def test_create_satellite_for_existing_operator(
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

        service = SatelliteService(session)

        satellite = await service.create(
            operator_id=operator.id,
            name="  IS-901  ",
            orbit_type="GEO",
            status="operational",
        )

        assert isinstance(satellite, Satellite)
        assert isinstance(satellite.id, UUID)
        assert satellite.name == "IS-901"
        assert satellite.normalized_name == "is-901"
        assert satellite.orbit_type == "GEO"
        assert satellite.status == "operational"


@pytest.mark.asyncio
async def test_create_satellite_requires_existing_operator(
    session_factory,
) -> None:
    async with session_factory() as session:
        service = SatelliteService(session)

        with pytest.raises(ValueError, match="operator"):
            await service.create(
                operator_id=uuid4(),
                name="IS-901",
                orbit_type="GEO",
                status="operational",
            )


@pytest.mark.asyncio
async def test_create_satellite_rejects_duplicate_for_operator(
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

        service = SatelliteService(session)

        await service.create(
            operator_id=operator.id,
            name="IS-901",
            orbit_type="GEO",
            status="operational",
        )

        with pytest.raises(ValueError, match="already exists"):
            await service.create(
                operator_id=operator.id,
                name=" is-901 ",
                orbit_type="GEO",
                status="operational",
            )


@pytest.mark.asyncio
async def test_get_satellite_by_id_returns_domain_object(
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

        service = SatelliteService(session)

        created = await service.create(
            operator_id=operator.id,
            name="IS-901",
            orbit_type="GEO",
            status="operational",
        )

        result = await service.get_by_id(created.id)

        assert isinstance(result, Satellite)
        assert result.id == created.id
        assert result.name == "IS-901"
