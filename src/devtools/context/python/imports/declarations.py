# Copyright (c) 2026
"""Direct module-body Python import declarations without resolution."""

from __future__ import annotations

import ast
import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, cast

if TYPE_CHECKING:
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )


@dataclass(frozen=True, slots=True)
class PythonImportSourceOccurrence:
    """Anchor one direct import statement in an observed resource."""

    snapshot_id: RepositorySnapshotId
    resource_address: RepositoryResourceAddress
    start_line: int
    start_column_utf8: int
    end_line: int
    end_column_utf8: int


@dataclass(frozen=True, slots=True)
class PythonImportDeclarationKnowledge:
    """One syntactic import alias; no target is resolved or asserted to exist."""

    derivation_identity: str
    support: PythonImportSourceOccurrence
    declaration_ordinal: int
    module: str | None
    level: int
    imported_name: str | None
    local_alias: str | None
    PROPOSITION: ClassVar[str] = "direct-module-body-python-import-declaration"


@dataclass(frozen=True, slots=True)
class PythonImportDeclarationCoverage:
    """Exhaustive coverage of only direct ``Module.body`` import statements."""

    derivation_identity: str
    declaration_count: int
    SCOPE: ClassVar[str] = "direct-module-body-ast.Import-or-ast.ImportFrom"
    IS_EXHAUSTIVE: ClassVar[bool] = True


@dataclass(frozen=True, slots=True)
class PythonImportDeclarationAnalysis:
    """Successful local import derivation and its bounded coverage."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    resource: RepositoryResourceOccurrence
    derivation_identity: str
    declarations: tuple[PythonImportDeclarationKnowledge, ...]
    coverage: PythonImportDeclarationCoverage


class PythonImportParseError(Exception):
    """Syntax failure distinct from exhaustive zero declarations."""


def derive_python_import_declarations(
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress | None = None,
) -> PythonImportDeclarationAnalysis:
    """Derive ordered direct import aliases from one already observed resource."""
    if resource_address is None:
        if len(snapshot.resources) != 1:
            msg = "An import derivation needs exactly one resource or an address."
            raise ValueError(msg)
        resource = snapshot.resources[0]
    else:
        resource = snapshot.resource_at(resource_address)
    derivation_identity = _digest(
        "python-import-declaration-v1",
        str(snapshot.repository_id),
        str(resource.address),
        str(resource.content_identity),
    )
    try:
        tree = ast.parse(resource.content, filename=str(resource.address), mode="exec")
    except SyntaxError as error:
        raise PythonImportParseError(error.msg) from error
    declarations: list[PythonImportDeclarationKnowledge] = []
    for node in tree.body:
        if not isinstance(node, ast.Import | ast.ImportFrom):
            continue
        support = PythonImportSourceOccurrence(
            snapshot_id=snapshot.id,
            resource_address=resource.address,
            start_line=node.lineno,
            start_column_utf8=node.col_offset,
            end_line=cast("int", node.end_lineno),
            end_column_utf8=cast("int", node.end_col_offset),
        )
        for alias in node.names:
            declarations.append(PythonImportDeclarationKnowledge(
                derivation_identity=derivation_identity,
                support=support,
                declaration_ordinal=len(declarations),
                module=alias.name if isinstance(node, ast.Import) else node.module,
                level=0 if isinstance(node, ast.Import) else node.level,
                imported_name=None if isinstance(node, ast.Import) else alias.name,
                local_alias=alias.asname,
            ))
    values = tuple(declarations)
    return PythonImportDeclarationAnalysis(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        resource=resource,
        derivation_identity=derivation_identity,
        declarations=values,
        coverage=PythonImportDeclarationCoverage(
            derivation_identity=derivation_identity,
            declaration_count=len(values),
        ),
    )


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
