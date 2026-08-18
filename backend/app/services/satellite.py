from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.domain.satellite import Satellite
from backend.app.mappers.satellite import SatelliteMapper
from backend.app.repositories.operator import OperatorRepository
from backend.app.repositories.satellite import SatelliteRepository


class SatelliteService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = SatelliteRepository(session)
        self.operator_repository = OperatorRepository(session)

    async def create(
        self,
        *,
        operator_id: UUID,
        name: str,
        orbit_type: str | None = None,
        status: str | None = None,
    ) -> Satellite:
        operator = await self.operator_repository.get_by_id(operator_id)

        if operator is None:
            raise ValueError(
                f"operator '{operator_id}' does not exist"
            )

        satellite = Satellite(
            name=name,
            orbit_type=orbit_type,
            status=status,
        )

        existing = await self.repository.get_by_normalized_name(
            satellite.normalized_name,
        )

        if existing is not None and existing.operator_id == operator_id:
            raise ValueError(
                f"satellite '{name}' already exists for operator"
            )

        model = SatelliteMapper.to_model(
            satellite,
            operator_id=operator_id,
        )

        await self.repository.create(model)
        await self.session.commit()

        return satellite

    async def get_by_id(
        self,
        satellite_id: UUID,
    ) -> Satellite | None:
        model = await self.repository.get_by_id(satellite_id)

        if model is None:
            return None

        return SatelliteMapper.to_domain(model)
