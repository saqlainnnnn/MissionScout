from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


def build_intelligence_event_payload(
    *,
    event_id: UUID,
    event_type: str,
    entity_type: str,
    entity_id: UUID,
    source: str,
    source_event_id: str | None = None,
    occurred_at: datetime | None = None,
    correlation_id: UUID | None = None,
    payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "event_id": str(event_id),
        "event_type": event_type,
        "entity_type": entity_type,
        "entity_id": str(entity_id),
        "source": source,
        "source_event_id": source_event_id or str(uuid4()),
        "occurred_at": (
            occurred_at or datetime.now(UTC)
        ).isoformat(),
        "correlation_id": str(correlation_id or entity_id),
        "payload": payload,
    }
