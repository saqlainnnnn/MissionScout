from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.domain.operator import Operator
from backend.app.mappers.operator import OperatorMapper
from backend.app.models.operator import OperatorModel
from backend.app.repositories.operator import OperatorRepository


class OperatorService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = OperatorRepository(session)

    async def create(
        self,
        *,
        name: str,
        country: str | None = None,
    ) -> Operator:
        operator = Operator(
            name=name,
            country=country,
        )

        existing = await self.repository.get_by_normalized_name(
            operator.normalized_name,
        )

        if existing is not None:
            raise ValueError(
                f"operator '{name}' already exists"
            )

        model = OperatorMapper.to_model(operator)

        await self.repository.create(model)
        await self.session.commit()

        return operator

    async def get_by_name(
        self,
        name: str,
    ) -> Operator | None:
        normalized_name = name.strip().lower()

        if not normalized_name:
            return None

        model = await self.repository.get_by_normalized_name(
            normalized_name,
        )

        if model is None:
            return None

        return OperatorMapper.to_domain(model)
