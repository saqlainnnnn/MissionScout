from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.intelligence_event import IntelligenceEvent
from backend.app.repositories.intelligence_event import IntelligenceEventRepository
from backend.app.schemas.intelligence_event import IntelligenceEventCreate


class EventNotFoundError(Exception):
    pass


class EventNotReplayableError(Exception):
    pass


class IntelligenceEventService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = IntelligenceEventRepository(session)

    async def ingest(
        self,
        data: IntelligenceEventCreate,
    ) -> tuple[IntelligenceEvent, bool]:
        existing = await self.repository.get_by_source_event(
            source=data.source,
            source_event_id=data.source_event_id,
        )

        if existing is not None:
            return existing, False

        event = IntelligenceEvent(
            event_type=data.event_type,
            entity_type=data.entity_type,
            entity_id=data.entity_id,
            source=data.source,
            source_event_id=data.source_event_id,
            occurred_at=data.occurred_at,
            correlation_id=data.correlation_id,
            payload=data.payload,
        )

        try:
            event = await self.repository.create(event)
        except IntegrityError:
            await self.session.rollback()

            existing = await self.repository.get_by_source_event(
                source=data.source,
                source_event_id=data.source_event_id,
            )

            if existing is not None:
                return existing, False

            raise

        return event, True

    async def replay(
        self,
        event_id: UUID,
    ) -> IntelligenceEvent:
        event = await self.repository.get_by_id(event_id)

        if event is None:
            raise EventNotFoundError(f"Event '{event_id}' not found")

        if event.status != "dead_letter":
            raise EventNotReplayableError(
                f"Event '{event_id}' is not dead_letter"
            )

        event.status = "received"
        event.retry_count = 0
        event.last_error = None

        await self.session.commit()
        await self.session.refresh(event)

        return event
