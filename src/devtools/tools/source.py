# Copyright (c) 2026
"""Host-scoped live source admission over canonical repository observations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, overload

from devtools.context import Repository, observe_repository_resources
from devtools.context.planning import source
from devtools.core.paths import resolve_path
from devtools.tools.errors import ToolInputError

if TYPE_CHECKING:
    from devtools.context import RepositoryResourceAddress, RepositorySnapshot
    from devtools.context.planning.materialization import ContextDisclosure
    from devtools.context.retrieval.source import RepositorySourceUnit
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


@dataclass(frozen=True, slots=True)
class SourceReadRequest:
    """Literal requested coordinates, not an admitted Context disclosure.

    Bounds are absolute decoded Unicode offsets. An omitted end requests the
    rest of the selected unit, still subject to the host's UTF-8 byte ceiling.
    Scope/currentness must be checked before exposing bounds or materializing.
    """

    purpose: str
    unit: RepositorySourceUnit
    start: int
    end: int | None
    maximum_bytes: int

    def __post_init__(self) -> None:
        """Reject malformed host configuration separately from literal ranges."""
        if (
            not self.purpose.strip()
            or type(self.maximum_bytes) is not int
            or self.maximum_bytes <= 0
        ):
            msg = "Source read requires a purpose and positive byte bound."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class SourceReadRefusal:
    """A recognized invalid range; source disclosure was never entered."""

    request: SourceReadRequest


def select_source_read(
    request: SourceReadRequest,
) -> source.SourceRangeDisclosureOption | SourceReadRefusal:
    """Validate literal coordinates using Context, without reading or effects.

    Only this effect-free construction is caught. Materialization, authorization
    and operational exceptions are deliberately outside this boundary.
    """
    try:
        return source.SourceRangeDisclosureOption(
            request.purpose,
            request.unit,
            request.start,
            request.unit.end if request.end is None else request.end,
            request.maximum_bytes,
        )
    except ValueError:
        return SourceReadRefusal(request)


def source_read_bounds(
    request: SourceReadRequest | source.SourceRangeDisclosureOption,
) -> dict[str, object]:
    """Project authorized observed bounds, not a durable freshness guarantee."""
    return {
        "source_length": len(request.unit.resource.content),
        "valid_range": [request.unit.start, request.unit.end],
        "coordinate_convention": "half-open Unicode character offsets",
        "maximum_bytes": request.maximum_bytes,
    }


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

    def validate(
        self,
        arguments: source.SourceRangeDisclosureOption | SourceReadRequest,
    ) -> None:
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

    @overload
    async def execute(
        self,
        arguments: source.SourceRangeDisclosureOption,
    ) -> ContextDisclosure: ...

    @overload
    async def execute(
        self,
        arguments: SourceReadRequest,
    ) -> ContextDisclosure | SourceReadRefusal: ...

    async def execute(
        self,
        arguments: source.SourceRangeDisclosureOption | SourceReadRequest,
    ) -> ContextDisclosure | SourceReadRefusal:
        """Use Context's existing plan/materialization operation, without ranking."""
        if isinstance(arguments, SourceReadRequest):
            selected = select_source_read(arguments)
            if isinstance(selected, SourceReadRefusal):
                return selected
            arguments = selected
        return source.materialize_source_range(self.scope.snapshot, arguments)
