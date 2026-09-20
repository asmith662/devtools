# Copyright (c) 2026
"""Exact source materialization for Python function Context disclosure."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.python.function.declarations import PythonSourceRange
    from devtools.context.python.function.disclosure import (
        PythonFunctionDeclarationDisclosureItem,
        PythonFunctionExactNameContextDisclosure,
    )
    from devtools.context.repository.resource import ContentIdentity
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )

_MATERIALIZATION_IDENTITY_SEMANTICS = "python-function-exact-source-materialization-v1"


class PythonFunctionSourceMaterializationError(Exception):
    """Reject source materialization against incompatible identified state."""


@dataclass(frozen=True, slots=True)
class MaterializedPythonFunctionDeclaration:
    """Add exact observed source to one structured disclosure item."""

    disclosure_item: PythonFunctionDeclarationDisclosureItem
    source_snapshot_id: RepositorySnapshotId
    source_content_identity: ContentIdentity
    source_text: str

    REPRESENTATION: ClassVar[str] = "exact-observed-utf8-source-segment-v1"


@dataclass(frozen=True, slots=True)
class MaterializedPythonFunctionContext:
    """Retain a disclosure and its ordered exact-source representations."""

    disclosure: PythonFunctionExactNameContextDisclosure
    items: tuple[MaterializedPythonFunctionDeclaration, ...]

    @property
    def identity(self) -> str:
        """Identify this local deterministic materialization."""
        values = tuple(
            value
            for item in self.items
            for value in (
                str(item.source_snapshot_id),
                str(item.source_content_identity),
                item.source_text,
            )
        )
        return _semantic_digest(
            _MATERIALIZATION_IDENTITY_SEMANTICS,
            MaterializedPythonFunctionDeclaration.REPRESENTATION,
            self.disclosure.identity,
            *values,
        )


def materialize_python_function_disclosure_source(
    *,
    disclosure: PythonFunctionExactNameContextDisclosure,
    snapshot: RepositorySnapshot,
) -> MaterializedPythonFunctionContext:
    """Resolve selected source occurrences against explicit observed state."""
    materialized_items: list[MaterializedPythonFunctionDeclaration] = []
    for disclosure_item in disclosure.items:
        occurrence = disclosure_item.source_occurrence
        if occurrence.snapshot_id != snapshot.id:
            msg = "Source occurrence does not belong to the supplied snapshot."
            raise PythonFunctionSourceMaterializationError(msg)
        try:
            resource = snapshot.resource_at(occurrence.resource_address)
        except ValueError as error:
            msg = "Source occurrence does not address a resource in the snapshot."
            raise PythonFunctionSourceMaterializationError(msg) from error

        materialized_items.append(
            MaterializedPythonFunctionDeclaration(
                disclosure_item=disclosure_item,
                source_snapshot_id=snapshot.id,
                source_content_identity=resource.content_identity,
                source_text=_extract_source_segment(
                    resource.content,
                    occurrence.source_range,
                ),
            ),
        )

    return MaterializedPythonFunctionContext(
        disclosure=disclosure,
        items=tuple(materialized_items),
    )


def _extract_source_segment(content: str, source_range: PythonSourceRange) -> str:
    """Extract one half-open range using UTF-8 byte-column coordinates."""
    if (
        source_range.start_line,
        source_range.start_column_utf8,
    ) > (
        source_range.end_line,
        source_range.end_column_utf8,
    ):
        msg = "Source occurrence range ends before it starts."
        raise PythonFunctionSourceMaterializationError(msg)

    encoded_lines = tuple(
        line.encode("utf-8") for line in content.splitlines(keepends=True)
    )
    start = _absolute_byte_offset(
        encoded_lines,
        line_number=source_range.start_line,
        column=source_range.start_column_utf8,
    )
    end = _absolute_byte_offset(
        encoded_lines,
        line_number=source_range.end_line,
        column=source_range.end_column_utf8,
    )
    try:
        return content.encode("utf-8")[start:end].decode("utf-8")
    except UnicodeDecodeError as error:
        msg = "Source occurrence columns do not fall on UTF-8 character boundaries."
        raise PythonFunctionSourceMaterializationError(msg) from error


def _absolute_byte_offset(
    encoded_lines: tuple[bytes, ...],
    *,
    line_number: int,
    column: int,
) -> int:
    """Translate one AST line/byte-column pair into an absolute byte offset."""
    if line_number < 1 or line_number > len(encoded_lines):
        msg = "Source occurrence line is outside the observed content."
        raise PythonFunctionSourceMaterializationError(msg)

    line = encoded_lines[line_number - 1]
    source_line = line.rstrip(b"\r\n")
    if column < 0 or column > len(source_line):
        msg = "Source occurrence column is outside the observed source line."
        raise PythonFunctionSourceMaterializationError(msg)
    return sum(len(previous) for previous in encoded_lines[: line_number - 1]) + column


def _semantic_digest(semantics: str, *values: str) -> str:
    """Hash length-framed values for this bounded materialization."""
    digest = hashlib.sha256()
    for value in (semantics, *values):
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, byteorder="big"))
        digest.update(encoded)
    return digest.hexdigest()
