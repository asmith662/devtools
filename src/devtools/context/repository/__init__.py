# Copyright (c) 2026
"""Public repository identity, state, observation, and discovery API."""

from devtools.context.repository.discovery import (
    RepositoryResourceDiscovery,
    RepositoryResourceDiscoveryError,
    discover_repository_resource_addresses,
)
from devtools.context.repository.corpus import (
    RepositoryTextCorpusDefinition,
    define_repository_text_corpus,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import (
    RepositoryObservationError,
    observe_repository_resource,
    observe_repository_resources,
)
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)

__all__ = [
    "ContentIdentity",
    "Repository",
    "RepositoryId",
    "RepositoryObservationError",
    "RepositoryResourceAddress",
    "RepositoryResourceDiscovery",
    "RepositoryResourceDiscoveryError",
    "RepositoryResourceOccurrence",
    "RepositorySnapshot",
    "RepositorySnapshotId",
    "RepositoryTextCorpusDefinition",
    "define_repository_text_corpus",
    "discover_repository_resource_addresses",
    "observe_repository_resource",
    "observe_repository_resources",
]
