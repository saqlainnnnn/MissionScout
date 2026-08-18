from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class OperatorModel(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "operators"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    normalized_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
