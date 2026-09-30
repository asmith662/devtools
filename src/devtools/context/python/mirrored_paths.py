# Copyright (c) 2026
"""Exact observed Python source/test path correspondence.

This is a repository path-convention fact, not a claim that a test executes,
covers, exercises, validates, or otherwise depends on the source resource.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )

_SEMANTICS = "exact-observed-python-mirrored-path-v1"


@dataclass(frozen=True, slots=True)
class PythonMirroredPathDerivation:
    """Identify this rule and its complete explicit observed resource input."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    resource_dependencies: tuple[tuple[str, str], ...]

    DEFINITION_SEMANTICS: ClassVar[str] = _SEMANTICS

    @property
    def identity(self) -> str:
        """Change when the rule, repository, snapshot, or input changes."""
        return _digest(
            self.DEFINITION_SEMANTICS,
            str(self.repository_id),
            str(self.snapshot_id),
            *(
                value
                for dependency in self.resource_dependencies
                for value in dependency
            ),
        )


@dataclass(frozen=True, slots=True)
class PythonMirroredPathCorrespondence:
    """Two observed resources satisfy the exact source/test path convention."""

    derivation_identity: str
    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    source: RepositoryResourceOccurrence
    test: RepositoryResourceOccurrence

    PROPOSITION: ClassVar[str] = "observed-python-source-test-path-correspondence"

    @property
    def identity(self) -> str:
        """Identify the supported pair and both observed contents."""
        return _digest(
            self.PROPOSITION,
            self.derivation_identity,
            str(self.source.address),
            str(self.source.content_identity),
            str(self.test.address),
            str(self.test.content_identity),
        )


@dataclass(frozen=True, slots=True)
class PythonMirroredPathCoverage:
    """Account for eligible and unmatched paths in the supplied snapshot."""

    derivation_identity: str
    source_resources_examined: int
    test_resources_examined: int
    excluded_initializers: int
    eligible_source_resources: int
    eligible_named_test_resources: int
    unmatched_source_resources: int
    unmatched_named_test_resources: int
    correspondence_count: int

    SCOPE: ClassVar[str] = "explicit-observed-snapshot-resource-set"
    IS_EXHAUSTIVE_FOR_SELECTION: ClassVar[bool] = True


@dataclass(frozen=True, slots=True)
class PythonMirroredPathAnalysis:
    """Retain the exact rule application, positive facts, and bounded coverage."""

    derivation: PythonMirroredPathDerivation
    correspondences: tuple[PythonMirroredPathCorrespondence, ...]
    coverage: PythonMirroredPathCoverage


def derive_python_mirrored_path_correspondences(
    snapshot: RepositorySnapshot,
) -> PythonMirroredPathAnalysis:
    """Match only observed paths; never read the working tree or infer absence.

    The exact Increment 31 rule is ``src/devtools/<directory>/<stem>.py`` to
    ``tests/<directory>/test_<stem>.py``. Empty directories are supported.
    Source initializers and test-side initializer counterparts are excluded.
    """
    resources = tuple(sorted(snapshot.resources, key=lambda item: str(item.address)))
    if len({item.address for item in resources}) != len(resources):
        msg = "A repository snapshot repeats a resource address."
        raise ValueError(msg)
    by_address = {str(item.address): item for item in resources}
    derivation = PythonMirroredPathDerivation(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        resource_dependencies=tuple(
            (str(item.address), str(item.content_identity)) for item in resources
        ),
    )
    source = tuple(
        item
        for item in resources
        if item.address.parts[:2] == ("src", "devtools")
        and str(item.address).endswith(".py")
    )
    tests = tuple(
        item
        for item in resources
        if item.address.parts[0] == "tests" and str(item.address).endswith(".py")
    )
    eligible_source = tuple(
        item for item in source if item.address.parts[-1] != "__init__.py"
    )
    eligible_tests = tuple(
        item
        for item in tests
        if item.address.parts[-1].startswith("test_")
        and item.address.parts[-1] != "test___init__.py"
    )
    correspondences: list[PythonMirroredPathCorrespondence] = []
    matched_tests: set[str] = set()
    for item in eligible_source:
        test_address = "/".join(
            ("tests", *item.address.parts[2:-1], f"test_{item.address.parts[-1]}"),
        )
        test = by_address.get(test_address)
        if test is None:
            continue
        correspondences.append(
            PythonMirroredPathCorrespondence(
                derivation_identity=derivation.identity,
                repository_id=snapshot.repository_id,
                snapshot_id=snapshot.id,
                source=item,
                test=test,
            ),
        )
        matched_tests.add(test_address)
    return PythonMirroredPathAnalysis(
        derivation=derivation,
        correspondences=tuple(correspondences),
        coverage=PythonMirroredPathCoverage(
            derivation_identity=derivation.identity,
            source_resources_examined=len(source),
            test_resources_examined=len(tests),
            excluded_initializers=sum(
                item.address.parts[-1] == "__init__.py" for item in (*source, *tests)
            ),
            eligible_source_resources=len(eligible_source),
            eligible_named_test_resources=len(eligible_tests),
            unmatched_source_resources=len(eligible_source) - len(correspondences),
            unmatched_named_test_resources=len(eligible_tests) - len(matched_tests),
            correspondence_count=len(correspondences),
        ),
    )


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
