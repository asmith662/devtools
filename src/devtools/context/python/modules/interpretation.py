# Copyright (c) 2026
"""Interpret observed Python resources under explicit module roots."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, cast

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )

_INTERPRETATION_SEMANTICS = "explicit-root-python-module-interpretation-v1"


@dataclass(frozen=True, slots=True)
class PythonModuleRoot:
    """Represent one caller-supplied repository-relative module root."""

    value: str

    def __post_init__(self) -> None:
        """Reject noncanonical root spellings."""
        if self.value == ".":
            return
        parts = self.value.split("/")
        if (
            not self.value
            or "\\" in self.value
            or any(part in {"", ".", ".."} for part in parts)
        ):
            msg = "Python module root must be '.' or a canonical relative directory."
            raise ValueError(msg)

    @property
    def parts(self) -> tuple[str, ...]:
        """Return the root's repository-relative directory components."""
        return () if self.value == "." else tuple(self.value.split("/"))


class PythonModuleKind(Enum):
    """Distinguish an ordinary module resource from a package module."""

    ORDINARY = "ordinary-module"
    PACKAGE = "package-module"


class PythonModuleInterpretationExclusionReason(Enum):
    """Explain why an explicitly selected resource has no interpretation."""

    NON_PYTHON_RESOURCE = "non-python-resource"
    OUTSIDE_MODULE_ROOT = "outside-module-root"
    ROOT_LEVEL_INIT = "root-level-init"
    NON_IDENTIFIER_COMPONENT = "non-identifier-component"


@dataclass(frozen=True, slots=True)
class PythonModuleInterpretationExclusion:
    """Retain one selected resource excluded by the bounded policy."""

    resource: RepositoryResourceOccurrence
    module_root: PythonModuleRoot
    reason: PythonModuleInterpretationExclusionReason


@dataclass(frozen=True, slots=True)
class PythonModuleInterpretation:
    """One exact resource's module interpretation under an explicit root."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    resource: RepositoryResourceOccurrence
    module_root: PythonModuleRoot
    dotted_name: str
    kind: PythonModuleKind

    SEMANTICS: ClassVar[str] = _INTERPRETATION_SEMANTICS

    @property
    def identity(self) -> str:
        """Identify this interpretation from its actual semantic inputs."""
        return _digest(
            self.SEMANTICS,
            str(self.repository_id),
            str(self.resource.address),
            str(self.resource.content_identity),
            self.module_root.value,
            self.dotted_name,
            self.kind.value,
        )


@dataclass(frozen=True, slots=True)
class PythonModuleInterpretationAnalysis:
    """Exhaustively classify a selected resource collection for one root."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    module_root: PythonModuleRoot
    interpretations: tuple[PythonModuleInterpretation, ...]
    exclusions: tuple[PythonModuleInterpretationExclusion, ...]

    SCOPE: ClassVar[str] = "explicit-selected-observed-resources-under-one-root"
    IS_EXHAUSTIVE: ClassVar[bool] = True


def interpret_python_module_resources(
    snapshot: RepositorySnapshot,
    *,
    module_root: PythonModuleRoot,
    resource_addresses: Sequence[RepositoryResourceAddress],
) -> PythonModuleInterpretationAnalysis:
    """Interpret exactly the caller-selected observed resources for one root.

    This operation performs no acquisition, parsing, package discovery, import
    resolution, or root inference.  Every selected resource yields exactly one
    interpretation or one explicit exclusion in caller-supplied address order.
    """
    selected_addresses = tuple(resource_addresses)
    if len(set(selected_addresses)) != len(selected_addresses):
        msg = "Python module interpretation resource addresses must be distinct."
        raise ValueError(msg)

    interpretations: list[PythonModuleInterpretation] = []
    exclusions: list[PythonModuleInterpretationExclusion] = []
    for address in selected_addresses:
        resource = snapshot.resource_at(address)
        interpretation, reason = _interpret_resource(
            repository_id=snapshot.repository_id,
            snapshot_id=snapshot.id,
            resource=resource,
            module_root=module_root,
        )
        if interpretation is None:
            exclusions.append(PythonModuleInterpretationExclusion(
                resource=resource,
                module_root=module_root,
                reason=cast("PythonModuleInterpretationExclusionReason", reason),
            ))
        else:
            interpretations.append(interpretation)

    return PythonModuleInterpretationAnalysis(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        module_root=module_root,
        interpretations=tuple(interpretations),
        exclusions=tuple(exclusions),
    )


def _interpret_resource(
    *,
    repository_id: RepositoryId,
    snapshot_id: RepositorySnapshotId,
    resource: RepositoryResourceOccurrence,
    module_root: PythonModuleRoot,
) -> tuple[
    PythonModuleInterpretation | None,
    PythonModuleInterpretationExclusionReason | None,
]:
    address_parts = resource.address.parts
    root_parts = module_root.parts
    if address_parts[: len(root_parts)] != root_parts:
        return None, PythonModuleInterpretationExclusionReason.OUTSIDE_MODULE_ROOT

    relative_parts = address_parts[len(root_parts) :]
    filename = relative_parts[-1]
    if not filename.endswith(".py"):
        return None, PythonModuleInterpretationExclusionReason.NON_PYTHON_RESOURCE

    stem = filename.removesuffix(".py")
    if stem == "__init__":
        if len(relative_parts) == 1:
            return None, PythonModuleInterpretationExclusionReason.ROOT_LEVEL_INIT
        name_parts = relative_parts[:-1]
        kind = PythonModuleKind.PACKAGE
    else:
        name_parts = (*relative_parts[:-1], stem)
        kind = PythonModuleKind.ORDINARY

    if not all(part.isidentifier() for part in name_parts):
        return None, PythonModuleInterpretationExclusionReason.NON_IDENTIFIER_COMPONENT
    return (
        PythonModuleInterpretation(
            repository_id=repository_id,
            snapshot_id=snapshot_id,
            resource=resource,
            module_root=module_root,
            dotted_name=".".join(name_parts),
            kind=kind,
        ),
        None,
    )


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
