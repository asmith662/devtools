# Copyright (c) 2026
"""Nominal identity for one logical repository."""

from __future__ import annotations

from dataclasses import dataclass

from devtools.core.identity import Identity


@dataclass(frozen=True, slots=True)
class RepositoryId:
    """Identify one logical Repository independently of its location or state."""

    value: Identity

    @classmethod
    def new(cls) -> RepositoryId:
        """Generate a new nominal Repository identity."""
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> RepositoryId:
        """Parse a Repository identity from UUID text."""
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return canonical UUID text."""
        return str(self.value)


@dataclass(frozen=True, slots=True)
class Repository:
    """Represent a logical software repository across changing states."""

    id: RepositoryId

    @classmethod
    def new(cls) -> Repository:
        """Create a logical Repository with a new nominal identity."""
        return cls(RepositoryId.new())
