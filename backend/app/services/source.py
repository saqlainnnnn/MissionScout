from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.source import Source
from backend.app.repositories.source import SourceRepository
from backend.app.schemas.source import SourceCreate


class SourceAlreadyExistsError(Exception):
    pass


class SourceService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = SourceRepository(session)

    async def list(self) -> list[Source]:
        return await self.repository.list_all()

    async def create(self, data: SourceCreate) -> Source:
        existing = await self.repository.get_by_name(data.name)

        if existing is not None:
            raise SourceAlreadyExistsError(
                f"Source '{data.name}' already exists"
            )

        source = Source(
            name=data.name,
            adapter_type=data.adapter_type,
            description=data.description,
            enabled=data.enabled,
        )

        await self.repository.create(source)
        await self.session.commit()

        return source
