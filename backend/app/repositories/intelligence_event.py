from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.intelligence_event import IntelligenceEvent


class IntelligenceEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_source_event(
        self,
        source: str,
        source_event_id: str,
    ) -> IntelligenceEvent | None:
        result = await self.session.execute(
            select(IntelligenceEvent).where(
                IntelligenceEvent.source == source,
                IntelligenceEvent.source_event_id == source_event_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        event_id: UUID,
    ) -> IntelligenceEvent | None:
        result = await self.session.execute(
            select(IntelligenceEvent).where(
                IntelligenceEvent.id == event_id
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        event: IntelligenceEvent,
    ) -> IntelligenceEvent:
        self.session.add(event)
        await self.session.flush()
        await self.session.refresh(event)
        return event

    async def update_status(
        self,
        event: IntelligenceEvent,
        status: str,
        retry_count: int | None = None,
        last_error: str | None = None,
    ) -> IntelligenceEvent:
        event.status = status

        if retry_count is not None:
            event.retry_count = retry_count

        event.last_error = last_error

        await self.session.flush()
        return event
