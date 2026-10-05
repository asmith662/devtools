# Copyright (c) 2026
# ruff: noqa: COM812
"""Explicit frozen excerpts: code-point offsets and UTF-8 disclosure accounting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from experiments.codex_dogfood.semantic_resolution._identity import digest, text_digest

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceOccurrence


@dataclass(frozen=True, slots=True)
class ContentBounds:
    """Bound resource count, excerpt count and total disclosed UTF-8 bytes."""

    max_resources: int
    max_excerpts: int
    max_utf8_bytes: int

    def __post_init__(self) -> None:
        """Require explicit nonnegative integer limits, including valid zero limits."""
        if any(
            type(value) is not int or value < 0
            for value in (
                self.max_resources,
                self.max_excerpts,
                self.max_utf8_bytes,
            )
        ):
            msg = "Disclosure bounds must be nonnegative integers."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class FrozenContentSlice:
    """Validate one nonempty half-open Unicode code-point slice of native text."""

    resource: RepositoryResourceOccurrence
    start: int
    end: int
    excerpt_digest: str

    def __post_init__(self) -> None:
        """Validate spans; request admission verifies native occurrence identity."""
        if (
            type(self.start) is not int
            or type(self.end) is not int
            or not 0 <= self.start < self.end <= len(self.resource.content)
        ):
            msg = "Invalid content slice offsets."
            raise ValueError(msg)
        if text_digest(self.text) != self.excerpt_digest:
            msg = "Content excerpt digest mismatch."
            raise ValueError(msg)

    @classmethod
    def select(
        cls, resource: RepositoryResourceOccurrence, start: int, end: int
    ) -> FrozenContentSlice:
        """Describe caller-selected content; perform no selection or truncation."""
        return cls(resource, start, end, text_digest(resource.content[start:end]))

    @property
    def text(self) -> str:
        """Return exactly the retained content disclosed to the reasoner."""
        return self.resource.content[self.start : self.end]

    @property
    def utf8_bytes(self) -> int:
        """Count disclosed text bytes, including repeated overlapping disclosures."""
        return len(self.text.encode("utf-8"))

    @property
    def identity(self) -> str:
        """Bind span to address, content identity and exact excerpt."""
        return digest(
            (
                self.resource.address,
                self.resource.content_identity,
                self.start,
                self.end,
                self.excerpt_digest,
            )
        )


@dataclass(frozen=True, slots=True)
class ContentCitation:
    """Tie one exact disclosed excerpt to one decision request."""

    request_id: str
    content: FrozenContentSlice

    @property
    def identity(self) -> str:
        """Keep identical spans in different requests distinct."""
        return digest((self.request_id, self.content.identity))
