from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.operator import OperatorModel


class OperatorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        operator: OperatorModel,
    ) -> OperatorModel:
        self.session.add(operator)
        await self.session.flush()
        await self.session.refresh(operator)
        return operator

    async def get_by_id(
        self,
        operator_id: UUID,
    ) -> OperatorModel | None:
        result = await self.session.execute(
            select(OperatorModel).where(
                OperatorModel.id == operator_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_normalized_name(
        self,
        normalized_name: str,
    ) -> OperatorModel | None:
        result = await self.session.execute(
            select(OperatorModel).where(
                OperatorModel.normalized_name == normalized_name,
            )
        )

        return result.scalar_one_or_none()
