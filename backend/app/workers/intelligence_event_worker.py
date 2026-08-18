import asyncio
import logging
from uuid import UUID

from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.redis import get_redis
from backend.app.db.session import AsyncSessionLocal
from backend.app.handlers.intelligence import handle_intelligence_event
from backend.app.repositories.intelligence_event import (
    IntelligenceEventRepository,
)
from backend.app.services.queue import IntelligenceEventQueue

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BASE_BACKOFF_SECONDS = 2


async def handle_event(
    session: AsyncSession,
    event_id: UUID,
    queue: IntelligenceEventQueue,
) -> None:
    repository = IntelligenceEventRepository(session)

    event = await repository.get_by_id(event_id)

    if event is None:
        logger.error("Event %s not found", event_id)
        return

    if event.status == "processed":
        logger.info("Event %s already processed", event_id)
        return

    await repository.update_status(
        event,
        status="processing",
    )
    await session.commit()

    try:
        await handle_intelligence_event(event)

        await repository.update_status(
            event,
            status="processed",
            last_error=None,
        )
        await session.commit()

        logger.info("Event %s processed successfully", event_id)

    except Exception as exc:
        await session.rollback()

        async with AsyncSessionLocal() as retry_session:
            retry_repository = IntelligenceEventRepository(retry_session)

            retry_event = await retry_repository.get_by_id(event_id)

            if retry_event is None:
                return

            retry_count = retry_event.retry_count + 1

            if retry_count >= MAX_RETRIES:
                await retry_repository.update_status(
                    retry_event,
                    status="dead_letter",
                    retry_count=retry_count,
                    last_error=str(exc),
                )
                await retry_session.commit()

                await queue.enqueue_dlq(
                    event_id=event_id,
                    reason=str(exc),
                )

                logger.error(
                    "Event %s moved to DLQ after %s attempts: %s",
                    event_id,
                    retry_count,
                    exc,
                )
                return

            await retry_repository.update_status(
                retry_event,
                status="retrying",
                retry_count=retry_count,
                last_error=str(exc),
            )
            await retry_session.commit()

        backoff = BASE_BACKOFF_SECONDS**retry_count

        logger.warning(
            "Event %s failed on attempt %s. Retrying in %ss: %s",
            event_id,
            retry_count,
            backoff,
            exc,
        )

        await asyncio.sleep(backoff)

        await queue.enqueue_retry(
            event_id=event_id,
            retry_count=retry_count,
        )


async def worker_loop() -> None:
    logger.info("MissionScout intelligence event worker started")

    while True:
        redis = get_redis()
        queue = IntelligenceEventQueue(redis)

        try:
            event_id = await queue.dequeue()

            async with AsyncSessionLocal() as session:
                await handle_event(
                    session=session,
                    event_id=event_id,
                    queue=queue,
                )

        except RedisError:
            logger.exception("Redis failure. Reconnecting in 2 seconds")
            await asyncio.sleep(2)

        except Exception:
            logger.exception("Worker failure. Continuing in 2 seconds")
            await asyncio.sleep(2)

        finally:
            await redis.aclose()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(worker_loop())
