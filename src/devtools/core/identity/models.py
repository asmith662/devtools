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
        return cls(UUID(value))

    def __str__(self) -> str:
        """Return the canonical UUID representation.

        :returns: Canonical UUID string.
        """
        return str(self.value)
