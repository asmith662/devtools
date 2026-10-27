# Copyright (c) 2026
"""Host-scoped live source admission over canonical repository observations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context import Repository, observe_repository_resources
from devtools.context.planning import source
from devtools.core.paths import resolve_path
from devtools.tools.errors import ToolInputError

if TYPE_CHECKING:
    from devtools.context import RepositoryResourceAddress, RepositorySnapshot
    from devtools.context.planning.materialization import ContextDisclosure
    from devtools.core.paths import ResolvedPath


@dataclass(frozen=True, slots=True)
class SourceScope:
    """Explicit host permission for exactly one bounded observed collection.

    Constructing this value is a host decision, not model authority. Live
    correspondence is rechecked separately; observations are sequential, not
    an atomic filesystem snapshot or a lock against external writers.
    """

    root: ResolvedPath
    snapshot: RepositorySnapshot
    maximum_resource_bytes: int = 131072

    @classmethod
    def observe(
        cls,
        *,
        root: ResolvedPath,
        repository: Repository,
        addresses: tuple[RepositoryResourceAddress, ...],
        maximum_resource_bytes: int = 131072,
    ) -> SourceScope:
        """Admit unaliased entries and reuse the existing RI observation owner."""
        if resolve_path(root.value) != root:
            msg = "Source root aliases are not admitted."
            raise ToolInputError(msg)
        for address in addresses:
            candidate = root.value / address.value
            for path in (candidate, *candidate.parents):
                if (
                    path != root.value
                    and path.is_relative_to(root.value)
                    and (path.is_symlink() or path.is_junction())
                ):
                    msg = "Source path aliases are not admitted."
                    raise ToolInputError(msg)
        return cls(
            root,
            observe_repository_resources(
                repository=repository,
                root=root,
                addresses=addresses,
                maximum_resource_bytes=maximum_resource_bytes,
            ),
            maximum_resource_bytes,
        )

    def check_current(self) -> None:
        """Refuse a stale or foreign snapshot without replacing its identity."""
        current = self.observe(
            root=self.root,
            repository=Repository(self.snapshot.repository_id),
            addresses=tuple(r.address for r in self.snapshot.resources),
            maximum_resource_bytes=self.maximum_resource_bytes,
        )
        if current.snapshot != self.snapshot:
            msg = "Source snapshot is no longer current."
            raise ToolInputError(msg)


class ScopedSourceTool:
    """Materialize a selected file/symbol/window range within host scope."""

    name = "acquire_source_range"
    description = "Acquire exact bounded source with retained Context provenance."

    def __init__(self, scope: SourceScope, *, maximum_bytes: int = 4096) -> None:
        """Bind host scope and a finite disclosure cap."""
        if maximum_bytes <= 0:
            msg = "Source disclosure byte bound must be positive."
            raise ValueError(msg)
        self.scope = scope
        self.maximum_bytes = maximum_bytes

    def validate(self, arguments: source.SourceRangeDisclosureOption) -> None:
        """Refuse foreign resources, excessive disclosure and stale inputs."""
        unit = arguments.unit
        if (
            unit.repository_id != self.scope.snapshot.repository_id
            or unit.snapshot_id != self.scope.snapshot.id
            or unit.resource not in self.scope.snapshot.resources
            or arguments.maximum_bytes > self.maximum_bytes
        ):
            msg = "Source request is outside the host-admitted scope."
            raise ToolInputError(msg)
        self.scope.check_current()

    async def execute(
        self,
        arguments: source.SourceRangeDisclosureOption,
    ) -> ContextDisclosure:
        """Use Context's existing plan/materialization operation, without ranking."""
        return source.materialize_source_range(self.scope.snapshot, arguments)
