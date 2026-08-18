import logging

from backend.app.models.intelligence_event import IntelligenceEvent

logger = logging.getLogger(__name__)


SUPPORTED_EVENT_TYPES = {
    "satellite.launched",
    "satellite.lifecycle_update",
    "satellite.eol_signal",
    "satellite.replacement_announced",
    "satellite.retirement_announced",
    "satellite.relocation",
    "satellite.anomaly",
    "operator.funding",
    "operator.acquisition",
    "operator.partnership",
    "operator.fleet_expansion",
    "operator.revenue_decline",
}


async def handle_intelligence_event(
    event: IntelligenceEvent,
) -> None:
    if event.event_type not in SUPPORTED_EVENT_TYPES:
        raise ValueError(
            f"Unsupported intelligence event type: {event.event_type}"
        )

    logger.info(
        "Received intelligence event: type=%s entity=%s/%s source=%s",
        event.event_type,
        event.entity_type,
        event.entity_id,
        event.source,
    )

    # Phase 4 will attach real signal detectors here.
    # For Phase 1, successful dispatch is enough.
