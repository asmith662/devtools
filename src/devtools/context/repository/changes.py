# Copyright (c) 2026
"""Compare exact retained resource collections without acquisition or mutation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import RepositorySnapshot


@dataclass(frozen=True, slots=True)
class RepositorySnapshotDelta:
    """Retain a difference relationship and both exact snapshot dependencies.

    Absence means exclusion from a supplied resource collection, never physical
    deletion. Equal content at different addresses establishes no rename or copy.
    This result neither defines snapshot identity nor applies changes or decides
    whether derived knowledge remains applicable.
    """

    before: RepositorySnapshot
    after: RepositorySnapshot
    added: tuple[RepositoryResourceAddress, ...]
    removed: tuple[RepositoryResourceAddress, ...]
    modified: tuple[RepositoryResourceAddress, ...]
    unchanged: tuple[RepositoryResourceAddress, ...]


def compare_repository_snapshots(
    before: RepositorySnapshot,
    after: RepositorySnapshot,
) -> RepositorySnapshotDelta:
    """Partition addressed occurrences from two snapshots of the same repository.

    Compare complete retained occurrence values at common exact addresses. Output
    ordering is canonical address order, independent of resource input ordering.
    No filesystem, Git, acquisition, mutation history or rename inference occurs.

    :raises ValueError: If repositories differ or either input repeats an address.
    :returns: Immutable partitions retaining the original snapshots.
    """
    if before.repository_id != after.repository_id:
        msg = "Snapshot comparison requires the same repository identity."
        raise ValueError(msg)
    left = {resource.address: resource for resource in before.resources}
    right = {resource.address: resource for resource in after.resources}
    if len(left) != len(before.resources) or len(right) != len(after.resources):
        msg = "Snapshot comparison requires distinct addresses in each input."
        raise ValueError(msg)
    common = left.keys() & right.keys()
    return RepositorySnapshotDelta(
        before=before,
        after=after,
        added=tuple(sorted(right.keys() - left.keys(), key=lambda item: item.value)),
        removed=tuple(sorted(left.keys() - right.keys(), key=lambda item: item.value)),
        modified=tuple(
            sorted(
                (address for address in common if left[address] != right[address]),
                key=lambda item: item.value,
            ),
        ),
        unchanged=tuple(
            sorted(
                (address for address in common if left[address] == right[address]),
                key=lambda item: item.value,
            ),
        ),
    )
