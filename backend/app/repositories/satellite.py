from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.satellite import SatelliteModel


class SatelliteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        satellite: SatelliteModel,
    ) -> SatelliteModel:
        self.session.add(satellite)
        await self.session.flush()
        await self.session.refresh(satellite)
        return satellite

    async def get_by_id(
        self,
        satellite_id: UUID,
    ) -> SatelliteModel | None:
        result = await self.session.execute(
            select(SatelliteModel).where(
                SatelliteModel.id == satellite_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_operator_id(
        self,
        operator_id: UUID,
    ) -> list[SatelliteModel]:
        result = await self.session.execute(
            select(SatelliteModel)
            .where(
                SatelliteModel.operator_id == operator_id,
            )
            .order_by(SatelliteModel.name)
        )

        return list(result.scalars().all())

    async def get_by_normalized_name(
        self,
        normalized_name: str,
    ) -> SatelliteModel | None:
        result = await self.session.execute(
            select(SatelliteModel).where(
                SatelliteModel.normalized_name == normalized_name,
            )
        )

        return result.scalar_one_or_none()
