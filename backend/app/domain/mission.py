from uuid import UUID, uuid4


SUPPORTED_MISSION_TYPES = {
    "communications",
    "earth_observation",
    "navigation",
    "science",
    "defense",
    "technology",
    "servicing",
    "other",
}

SUPPORTED_STATUSES = {
    "planned",
    "active",
    "completed",
    "cancelled",
}


class Mission:
    def __init__(
        self,
        name: str,
        mission_type: str | None = None,
        status: str | None = None,
    ) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("name cannot be empty")

        if (
            mission_type is not None
            and mission_type not in SUPPORTED_MISSION_TYPES
        ):
            raise ValueError(
                f"invalid mission_type: {mission_type}"
            )

        if (
            status is not None
            and status not in SUPPORTED_STATUSES
        ):
            raise ValueError(
                f"invalid status: {status}"
            )

        self.id: UUID = uuid4()
        self.name = normalized_name
        self.normalized_name = normalized_name.lower()
        self.mission_type = mission_type
        self.status = status

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mission):
            return NotImplemented

        return self.normalized_name == other.normalized_name
