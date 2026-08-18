from uuid import UUID, uuid4


SUPPORTED_ORBIT_TYPES = {
    "LEO",
    "MEO",
    "GEO",
    "HEO",
}

SUPPORTED_STATUSES = {
    "planned",
    "operational",
    "degraded",
    "retired",
    "lost",
}


class Satellite:
    def __init__(
        self,
        name: str,
        orbit_type: str | None = None,
        status: str | None = None,
    ) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("name cannot be empty")

        if orbit_type is not None and orbit_type not in SUPPORTED_ORBIT_TYPES:
            raise ValueError(
                f"invalid orbit_type: {orbit_type}"
            )

        if status is not None and status not in SUPPORTED_STATUSES:
            raise ValueError(
                f"invalid status: {status}"
            )

        self.id: UUID = uuid4()
        self.name = normalized_name
        self.normalized_name = normalized_name.lower()
        self.orbit_type = orbit_type
        self.status = status


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Satellite):
            return NotImplemented

        return self.normalized_name == other.normalized_name
