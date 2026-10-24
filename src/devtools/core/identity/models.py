# Copyright (c) 2026
"""Identity value objects."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Identity:
    """Represent an immutable globally unique identity.

    :ivar value: UUID backing the identity.
    """

    value: UUID

    def __init__(self, value: UUID) -> None:
        """Initialize the identity with a UUID value.

        :param value: UUID backing the identity.
        :raises TypeError: If the supplied value is not a UUID.
        """
        message = "Identity value must be a UUID"
        if not isinstance(value, UUID):
            raise TypeError(message)
        object.__setattr__(self, "value", value)

    @classmethod
    def new(cls) -> Identity:
        """Generate a new identity.

        :returns: Newly generated UUID4 identity.
        """
        return cls(uuid4())

    @classmethod
    def parse(cls, value: str) -> Identity:
        """Parse an identity from its UUID string representation.

        :param value: UUID string representation.
        :returns: Parsed identity.
        :raises ValueError: If the supplied value is not a valid UUID.
        """
        return cls(cls._parse_uuid(value))

    @staticmethod
    def _parse_uuid(value: str) -> UUID:
        """Parse a UUID string into a UUID instance.

        :param value: UUID string representation.
        :returns: Parsed UUID.
        :raises ValueError: If the supplied value is not a valid UUID.
        """
        return UUID(value)

    def __str__(self) -> str:
        """Return the canonical UUID representation.

        :returns: Canonical UUID string.
        """
        return str(self.value)
