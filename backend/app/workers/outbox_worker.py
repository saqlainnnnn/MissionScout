import asyncio
import logging

from backend.app.core.redis import get_redis
from backend.app.db.session import AsyncSessionLocal
from backend.app.repositories.outbox import OutboxRepository
from backend.app.services.queue import IntelligenceEventQueue

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 2
BATCH_SIZE = 25


async def process_outbox() -> int:
    redis = get_redis()
    queue = IntelligenceEventQueue(redis)

    try:
        async with AsyncSessionLocal() as session:
            repository = OutboxRepository(session)
            events = await repository.get_pending(limit=BATCH_SIZE)

            processed = 0

            for event in events:
                try:
                    await queue.enqueue(
                        event_id=event.payload["event_id"],
                    )

                    await repository.mark_processed(event)
                    processed += 1

                    logger.info(
                        "Published outbox event %s to intelligence queue",
                        event.id,
                    )

                except Exception as exc:
                    logger.exception(
                        "Failed to publish outbox event %s",
                        event.id,
                    )

                    await repository.mark_failed(
                        event,
                        error=str(exc),
                    )

            await session.commit()

            return processed

    finally:
        await redis.aclose()


async def worker_loop() -> None:
    logger.info("MissionScout outbox worker started")

    while True:
        try:
            processed = await process_outbox()

            if processed:
                logger.info(
                    "Processed %s outbox events",
                    processed,
                )

        except Exception:
            logger.exception("Outbox worker failure")

        await asyncio.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(worker_loop())
