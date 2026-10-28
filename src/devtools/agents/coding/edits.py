# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- exact retained public refusal diagnostics
"""Exact anchored replacement admission; source identity/permission stay explicit."""

from __future__ import annotations


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
