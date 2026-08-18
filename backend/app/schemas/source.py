from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SourceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    adapter_type: str = Field(min_length=1, max_length=100)
    description: str | None = None
    enabled: bool = True


class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    adapter_type: str
    description: str | None
    enabled: bool
