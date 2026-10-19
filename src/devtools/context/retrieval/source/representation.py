# Copyright (c) 2026
"""Snapshot-bound searchable source views, distinct from RI semantic subjects."""

from __future__ import annotations

import ast
import tokenize
from dataclasses import dataclass
from io import StringIO
from typing import TYPE_CHECKING, ClassVar, Literal, cast

from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonMethodDeclarationKnowledge,
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
    PythonSourceOccurrence,
    PythonSourceRange,
    derive_python_function_declarations,
)
from devtools.context.python.function.materialization import _absolute_byte_offset
from devtools.context.repository.document import (
    RepositoryTextDocument,
    RepositoryTextDocumentCollection,
    RepositoryTextDocumentId,
    _semantic_digest,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )

type SourceSearchMode = Literal["file", "symbol", "window", "mixed"]
type SourceRepresentation = Literal["file", "symbol", "window"]
type SourceDeclaration = (
    PythonFunctionDeclarationKnowledge
    | PythonClassDeclarationKnowledge
    | PythonMethodDeclarationKnowledge
)


@dataclass(frozen=True, slots=True)
class RepositorySourceUnit(RepositoryTextDocument):
    """One exact character slice with its original observed parent resource.

    Offsets are half-open decoded-text character offsets, never AST byte columns.
    A Python syntax occurrence and existing RI declaration are retained separately.
    Nested syntax without a canonical RI subject does not acquire a new subject.
    """

    snapshot_id: RepositorySnapshotId
    kind: SourceRepresentation
    start: int
    end: int
    qualified_name: str | None = None
    symbol_kind: str | None = None
    occurrence: PythonSourceOccurrence | None = None
    declaration: SourceDeclaration | None = None
    parent_symbol_id: RepositoryTextDocumentId | None = None

    REPRESENTATION_SEMANTICS: ClassVar[str] = "snapshot-exact-source-slice-v1"

    def __post_init__(self) -> None:
        """Refuse out-of-bounds spans and empty non-file representations."""
        if not 0 <= self.start <= self.end <= len(self.resource.content) or (
            self.kind != "file" and self.start == self.end
        ):
            msg = "Source representation span is outside its parent content or empty."
            raise ValueError(msg)

    @property
    def text(self) -> str:
        """Return original source, including original whitespace and line endings."""
        return self.resource.content[self.start : self.end]

    @property
    def start_line(self) -> int:
        """Return the one-based logical line under text splitlines semantics."""
        prefix = self.resource.content[: self.start]
        return len(prefix.splitlines()) + int(
            not prefix
            or prefix.endswith(
                (
                    "\n",
                    "\r",
                    "\v",
                    "\f",
                    "\x1c",
                    "\x1d",
                    "\x1e",
                    "\x85",
                    "\u2028",
                    "\u2029",
                ),
            ),
        )

    @property
    def end_line(self) -> int:
        """Return the inclusive last source line (one for an empty file)."""
        return max(1, len(self.resource.content[: self.end].splitlines()))


class SourceDocumentCollection(RepositoryTextDocumentCollection):
    """Reuse lexical collection machinery for explicit source representations."""

    REPRESENTATION_SEMANTICS: ClassVar[str] = "snapshot-source-view-population-v1"


def file_unit(
    snapshot: RepositorySnapshot,
    document: RepositoryTextDocument,
) -> RepositorySourceUnit:
    """Preserve the existing whole-file document identity and exact text."""
    return RepositorySourceUnit(
        id=document.id,
        repository_id=document.repository_id,
        resource=document.resource,
        snapshot_id=snapshot.id,
        kind="file",
        start=0,
        end=len(document.text),
    )


def window_units(
    file: RepositorySourceUnit,
    size: int,
    overlap: int,
) -> tuple[RepositorySourceUnit, ...]:
    """Cover original lines with bounded overlap and no contained tail window."""
    lines = file.text.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))
    units = []
    for first in range(0, len(lines), size - overlap):
        last = min(first + size, len(lines))
        units.append(_unit(file, "window", starts[first], starts[last]))
        if last == len(lines):
            break
    return tuple(units)


def symbol_units(
    snapshot: RepositorySnapshot,
    file: RepositorySourceUnit,
) -> tuple[tuple[RepositorySourceUnit, ...], str | None]:
    """Project recursive Python syntax while retaining canonical bounded RI facts."""
    if not str(file.resource.address).endswith(".py"):
        return (), "unsupported-language"
    try:
        tree = ast.parse(file.text, feature_version=(3, 12))
    except SyntaxError:
        return (), "invalid-python"
    functions = derive_python_function_declarations(
        snapshot,
        resource_address=file.resource.address,
    )
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=file.resource.address,
    )
    declarations: tuple[SourceDeclaration, ...] = (
        *functions.declarations,
        *classes.classes,
        *classes.methods,
    )
    native = {
        declaration.support.source_range: declaration for declaration in declarations
    }
    encoded_lines = tuple(
        line.encode("utf-8") for line in file.text.splitlines(keepends=True)
    )
    # AST expression positions can omit the opening @(... line. Token positions
    # recover that prefix without changing the original source representation.
    leading_decorators = tuple(
        token.start
        for token in tokenize.generate_tokens(
            StringIO(file.text.replace("\r\n", "\n").replace("\r", "\n")).readline,
        )
        if token.string == "@" and not token.line[: token.start[1]].strip()
    )
    units: list[RepositorySourceUnit] = []

    def visit(nodes: Iterable[ast.AST], parent: RepositorySourceUnit | None) -> None:
        for node in nodes:
            owner = parent
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                end_line, end_column = (
                    cast("int", node.end_lineno),
                    cast("int", node.end_col_offset),
                )
                syntax_range = PythonSourceRange(
                    node.lineno,
                    node.col_offset,
                    end_line,
                    end_column,
                )
                first = min(
                    (item.lineno for item in node.decorator_list),
                    default=node.lineno,
                )
                if node.decorator_list:
                    first = max(
                        line
                        for line, column in leading_decorators
                        if column == node.col_offset and line <= first
                    )
                source_range = PythonSourceRange(
                    first,
                    node.col_offset,
                    end_line,
                    end_column,
                )
                start_byte = _absolute_byte_offset(
                    encoded_lines,
                    line_number=first,
                    column=node.col_offset,
                )
                end_byte = _absolute_byte_offset(
                    encoded_lines,
                    line_number=end_line,
                    column=end_column,
                )
                start = len(file.text.encode("utf-8")[:start_byte].decode("utf-8"))
                end = len(file.text.encode("utf-8")[:end_byte].decode("utf-8"))
                name = f"{parent.qualified_name}.{node.name}" if parent else node.name
                owner = _unit(
                    file,
                    "symbol",
                    start,
                    end,
                    qualified_name=name,
                    symbol_kind=_symbol_kind(node, parent),
                    occurrence=PythonSourceOccurrence(
                        snapshot.id,
                        file.resource.address,
                        source_range,
                    ),
                    declaration=native.get(syntax_range),
                    parent_symbol_id=parent.id if parent else None,
                )
                units.append(owner)
            visit(ast.iter_child_nodes(node), owner)

    visit(tree.body, None)
    return tuple(units), None if units else "no-python-declarations"


def _symbol_kind(
    node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
    parent: RepositorySourceUnit | None,
) -> str:
    if isinstance(node, ast.ClassDef):
        return "class"
    kind = (
        "method" if parent is not None and parent.symbol_kind == "class" else "function"
    )
    return f"async-{kind}" if isinstance(node, ast.AsyncFunctionDef) else kind


def _unit(  # noqa: PLR0913 -- explicit metadata for this concrete source representation
    file: RepositorySourceUnit,
    kind: SourceRepresentation,
    start: int,
    end: int,
    *,
    qualified_name: str | None = None,
    symbol_kind: str | None = None,
    occurrence: PythonSourceOccurrence | None = None,
    declaration: SourceDeclaration | None = None,
    parent_symbol_id: RepositoryTextDocumentId | None = None,
) -> RepositorySourceUnit:
    return RepositorySourceUnit(
        id=RepositoryTextDocumentId(
            _semantic_digest(
                "source-search-unit-v1",
                str(file.snapshot_id),
                str(file.id),
                kind,
                str(start),
                str(end),
            ),
        ),
        repository_id=file.repository_id,
        resource=file.resource,
        snapshot_id=file.snapshot_id,
        kind=kind,
        start=start,
        end=end,
        qualified_name=qualified_name,
        symbol_kind=symbol_kind,
        occurrence=occurrence,
        declaration=declaration,
        parent_symbol_id=parent_symbol_id,
    )
