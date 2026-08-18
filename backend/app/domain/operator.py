from uuid import UUID, uuid4


class Operator:
    def __init__(
        self,
        name: str,
        country: str | None = None,
    ) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("name cannot be empty")

        self.id: UUID = uuid4()
        self.name = normalized_name
        self.normalized_name = normalized_name.lower()
        self.country = country

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Operator):
            return NotImplemented

        return self.normalized_name == other.normalized_name
