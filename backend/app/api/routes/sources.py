from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.dependencies import get_db
from backend.app.schemas.source import SourceCreate, SourceResponse
from backend.app.services.source import (
    SourceAlreadyExistsError,
    SourceService,
)

router = APIRouter(
    prefix="/sources",
    tags=["sources"],
)


@router.get(
    "",
    response_model=list[SourceResponse],
)
async def list_sources(
    session: AsyncSession = Depends(get_db),
) -> list[SourceResponse]:
    service = SourceService(session)
    sources = await service.list()

    return [
        SourceResponse.model_validate(source)
        for source in sources
    ]


@router.post(
    "",
    response_model=SourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_source(
    data: SourceCreate,
    session: AsyncSession = Depends(get_db),
) -> SourceResponse:
    service = SourceService(session)

    try:
        source = await service.create(data)
    except SourceAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return SourceResponse.model_validate(source)
