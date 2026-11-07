# Copyright (c) 2026
"""Views of already disclosed source; source and acquisition owners stay separate."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)

if TYPE_CHECKING:
    from devtools.context.repository.snapshot import RepositorySnapshotId


def coverage(
    size: int,
    spans: tuple[tuple[int, int], ...],
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    """Merge disclosed Unicode ranges and identify gaps, without acquiring source."""
    if (
        type(size) is not int
        or size < 0
        or any(
            type(start) is not int
            or type(end) is not int
            or not 0 <= start <= end <= size
            for start, end in spans
        )
    ):
        msg = "Invalid disclosed source ranges."
        raise ValueError(msg)
    merged: list[tuple[int, int]] = []
    for start, end in sorted(spans):
        if start == end:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1] = merged[-1][0], max(end, merged[-1][1])
        else:
            merged.append((start, end))
    cursor = 0
    gaps = []
    for start, end in merged:
        if cursor < start:
            gaps.append((cursor, start))
        cursor = end
    if cursor < size:
        gaps.append((cursor, size))
    return tuple(merged), tuple(gaps)


@dataclass(frozen=True, slots=True)
class SourceAnchor:
    """An exact quoted interval, not verification of an interpretation of it."""

    reference: str
    resource: RepositoryResourceAddress
    version: ContentIdentity
    snapshot: RepositorySnapshotId | None
    start: int
    end: int
    quote: str


@dataclass(frozen=True, slots=True)
class SourceBinding:
    """Borrow canonical source with host-authenticated disclosure and receipt IDs.

    Archived candidates have a source/receipt identity, not the live baseline's
    snapshot. An empty span collection exposes metadata only, never source text.
    """

    reference: str
    resource: RepositoryResourceOccurrence
    receipt: str
    spans: tuple[tuple[int, int], ...]
    snapshot: RepositorySnapshotId | None = None
    live: bool = False

    def __post_init__(self) -> None:
        """Check supplied source identity and disclosure bounds, not its semantics."""
        if (
            not self.reference.strip()
            or not self.receipt.strip()
            or self.resource.content_identity
            != ContentIdentity.from_text(self.resource.content)
        ):
            msg = "Working source requires authenticated content and receipt."
            raise ValueError(msg)
        coverage(len(self.resource.content), self.spans)

    def anchor(self, start: int, end: int, quote: str) -> SourceAnchor:
        """Require an exact quote entirely inside already disclosed source."""
        merged, _ = coverage(len(self.resource.content), self.spans)
        if (
            type(start) is not int
            or type(end) is not int
            or not 0 <= start < end <= len(self.resource.content)
            or not any(a <= start < end <= b for a, b in merged)
            or quote != self.resource.content[start:end]
            or len(quote) > 512  # noqa: PLR2004 -- bounded quoted working support
        ):
            msg = "Working support is not an exact disclosed source interval."
            raise ValueError(msg)
        return SourceAnchor(
            self.reference,
            self.resource.address,
            self.resource.content_identity,
            self.snapshot,
            start,
            end,
            quote,
        )

    def current(self, anchor: SourceAnchor) -> bool:
        """Recheck source, snapshot and exact disclosure without reacquiring it."""
        try:
            return anchor == self.anchor(anchor.start, anchor.end, anchor.quote)
        except ValueError:
            return False

    def reopen(self, anchor: SourceAnchor) -> dict[str, object]:
        """Reproject retained exact evidence; only live source gets a Tool pointer."""
        if not self.current(anchor):
            msg = "Working evidence is stale or no longer disclosed."
            raise ValueError(msg)
        return {
            "reference": self.reference,
            "receipt": self.receipt,
            "quote": anchor.quote,
            "read_source": {
                "path": str(anchor.resource),
                "start": anchor.start,
                "end": anchor.end,
            }
            if self.live
            else None,
            "origin": "current-source" if self.live else "retained-subject",
        }
