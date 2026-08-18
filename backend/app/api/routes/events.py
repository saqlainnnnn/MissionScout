from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.dependencies import get_db
from backend.app.repositories.outbox import OutboxRepository
from backend.app.schemas.intelligence_event import (
    IntelligenceEventCreate,
    IntelligenceEventIngestResponse,
    IntelligenceEventResponse,
)
from backend.app.services.intelligence_event import IntelligenceEventService

router = APIRouter(
    prefix="/events",
    tags=["events"],
)


@router.post(
    "",
    response_model=IntelligenceEventIngestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest_event(
    data: IntelligenceEventCreate,
    session: AsyncSession = Depends(get_db),
) -> IntelligenceEventIngestResponse:
    service = IntelligenceEventService(session)

    event, created = await service.ingest(data)

    if created:
        outbox = OutboxRepository(session)

        await outbox.create(
            aggregate_type=data.entity_type,
            aggregate_id=data.entity_id,
            event_type=data.event_type,
            payload={
                "event_id": str(event.id),
            },
        )

        await session.commit()

    response = IntelligenceEventResponse.model_validate(event)

    return IntelligenceEventIngestResponse(
        event=response,
        created=created,
    )
