# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- exact retained public refusal diagnostics
"""Exact anchored replacement admission; source identity/permission stay explicit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from devtools.context import RepositoryResourceAddress
from devtools.context.repository.resource import ContentIdentity

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from devtools.context.planning.source import SourceRangeDisclosureOption
    from devtools.context.repository.snapshot import RepositorySnapshot


class CodingEditError(ValueError):
    """A proposal was refused before source mutation, with bounded diagnostics."""

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, object] | None = None,
    ) -> None:
        """Retain independently meaningful refusal facts without changing source."""
        super().__init__(message)
        self.details = details or {}


def replace_exact_text(  # noqa: PLR0913 -- explicit independent host limits/deletion policy
    source: str,
    old_text: object,
    new_text: object,
    *,
    region_bytes: int,
    source_bytes: int,
    allow_empty_new: bool = False,
) -> tuple[str, int, int]:
    """Admit one exact unique anchor using caller limits and original line endings."""
    if not isinstance(old_text, str) or not isinstance(new_text, str):
        raise CodingEditError(
            "Structured edit text values must be strings",
            details={"code": "INVALID_TEXT_TYPE"},
        )
    if (
        not old_text
        or (not new_text and (not allow_empty_new))
        or "\x00" in old_text
        or ("\x00" in new_text)
        or (len(old_text.encode()) > region_bytes)
        or (len(new_text.encode()) > region_bytes)
        or (old_text == new_text)
    ):
        raise CodingEditError(
            "Structured edit text is empty, unchanged or oversized",
            details={
                "code": "EMPTY_TEXT"
                if not old_text or (not new_text and (not allow_empty_new))
                else "NUL_TEXT"
                if "\x00" in old_text or "\x00" in new_text
                else "REGION_BYTE_LIMIT"
                if max(len(old_text.encode()), len(new_text.encode())) > region_bytes
                else "NO_OP",
                "old_bytes": len(old_text.encode()),
                "new_bytes": len(new_text.encode()),
                "region_limit_bytes": region_bytes,
            },
        )
    for text in (source, old_text, new_text):
        without_crlf = text.replace("\r\n", "")
        if (
            "\r" in without_crlf
            or ("\r\n" in text and "\n" in without_crlf)
            or any(
                marker in text
                for marker in (
                    "\x0b",
                    "\x0c",
                    "\x1c",
                    "\x1d",
                    "\x1e",
                    "\x85",
                    "\u2028",
                    "\u2029",
                )
            )
        ):
            raise CodingEditError(
                "Mixed or unsupported structured edit line endings",
                details={"code": "UNSUPPORTED_LINE_ENDINGS"},
            )
    newline = "\r\n" if "\r\n" in source else "\n"
    old_text = old_text.replace("\r\n", "\n").replace("\n", newline)
    new_text = new_text.replace("\r\n", "\n").replace("\n", newline)
    if (
        old_text == new_text
        or max(len(old_text.encode()), len(new_text.encode())) > region_bytes
    ):
        raise CodingEditError(
            "Adapted structured edit is unchanged or oversized",
            details={
                "code": "NO_OP" if old_text == new_text else "REGION_BYTE_LIMIT",
                "adapted_old_bytes": len(old_text.encode()),
                "adapted_new_bytes": len(new_text.encode()),
                "region_limit_bytes": region_bytes,
            },
        )
    matches = 0
    offset = 0
    while (found := source.find(old_text, offset)) >= 0:
        matches += 1
        offset = found + 1
        if matches > 1:
            break
    if matches != 1:
        raise CodingEditError(
            "Old text must match exactly one source region",
            details={"code": "OLD_TEXT_NOT_UNIQUE"},
        )
    updated = source.replace(old_text, new_text, 1)
    if len(updated.encode()) > source_bytes:
        raise CodingEditError(
            "Structured edit exceeds the bounded source size",
            details={
                "code": "SOURCE_BYTE_LIMIT",
                "source_bytes": len(updated.encode()),
                "source_limit_bytes": source_bytes,
            },
        )
    return (updated, source.index(old_text), source.index(old_text) + len(old_text))


@dataclass(frozen=True, slots=True)
class EditLimits:
    """Host-selected region/source/transaction ceilings, without Qwen defaults."""

    region_bytes: int
    source_bytes: int
    aggregate_bytes: int
    operations: int

    def __post_init__(self) -> None:
        """Refuse unbounded admission before effects."""
        if (
            min(
                self.region_bytes,
                self.source_bytes,
                self.aggregate_bytes,
                self.operations,
            )
            <= 0
        ):
            msg = "Edit limits must be positive."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class SourceChange:
    """Admitted whole after-image with its original addressed source and span."""

    address: RepositoryResourceAddress
    before: str
    after: str
    start: int
    end: int


def admit_source_batch(
    arguments: Iterable[Mapping[str, object]],
    *,
    snapshot: RepositorySnapshot,
    editable: tuple[RepositoryResourceAddress, ...],
    available: tuple[SourceRangeDisclosureOption, ...],
    limits: EditLimits,
) -> tuple[SourceChange, ...]:
    """Plan exact current, bounded, nonoverlapping replacements without effects.

    The host checks source currentness, readiness and the native operation count
    before entering. Arguments are decoded lazily so a later malformed operation
    cannot hide an earlier admission refusal. No partial plan escapes on error.
    Scope membership and exact disclosed witnesses are checked here; model/Tool
    correlation, authorization, effect entry and custody remain host-owned.
    """
    changes: list[SourceChange] = []
    total = 0
    for values in arguments:
        address = RepositoryResourceAddress(cast("str", values["path"]))
        if address not in editable:
            msg = "Edit path is outside the admitted editing surface."
            raise CodingEditError(msg)
        before = snapshot.resource_at(address).content
        after, start, end = replace_exact_text(
            before,
            values["old_text"],
            values["new_text"],
            region_bytes=limits.region_bytes,
            source_bytes=limits.source_bytes,
            allow_empty_new=True,
        )
        if not any(
            o.unit.resource.address == address
            and o.snapshot_id == snapshot.id
            and o.repository_id == snapshot.repository_id
            and o.unit.resource.content_identity == ContentIdentity.from_text(before)
            and o.span[0] <= start
            and end <= o.span[1]
            for o in available
        ):
            msg = "Exact current edit source was not acquired."
            raise CodingEditError(msg)
        if any(
            c.address == address and start < c.end and c.start < end for c in changes
        ):
            msg = "Edit anchors overlap."
            raise CodingEditError(msg)
        total += len(before[start:end].encode()) + len(
            cast("str", values["new_text"]).encode(),
        )
        if total > limits.aggregate_bytes:
            msg = "Aggregate edit byte limit exceeded."
            raise CodingEditError(msg)
        changes.append(SourceChange(address, before, after, start, end))
    # Combine admitted same-file anchors against the one original version.
    combined = []
    for address in dict.fromkeys(c.address for c in changes):
        original = snapshot.resource_at(address).content
        after = original
        for c in sorted(
            (c for c in changes if c.address == address),
            key=lambda c: c.start,
            reverse=True,
        ):
            inserted = c.after[c.start : len(c.after) - (len(c.before) - c.end)]
            after = after[: c.start] + inserted + after[c.end :]
        if len(after.encode()) > limits.source_bytes:
            msg = "Combined source byte limit exceeded."
            raise CodingEditError(msg)
        combined.append(
            SourceChange(address, original, after, 0, len(original)),
        )
    return tuple(combined)
