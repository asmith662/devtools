# Copyright (c) 2026
"""Tests for bounded Repository state observation."""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools.context import (
    ContentIdentity,
    Repository,
    RepositoryId,
    RepositoryObservationError,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
    RepositorySnapshot,
    RepositorySnapshotId,
    observe_repository_resource,
)
from devtools.core.paths import ResolvedPath
from devtools.resources.filesystem import (
    FilesystemNotFoundError,
    FilesystemPermissionError,
    NotAFileError,
    TextDecodingError,
)

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"


def _repository() -> Repository:
    """Return one deterministic logical Repository."""
    return Repository(RepositoryId.parse(_REPOSITORY_ID))


def _observe(
    repository: Repository,
    root: Path,
    address: str,
) -> RepositorySnapshot:
    """Observe one fixture resource through the public boundary."""
    return observe_repository_resource(
        repository=repository,
        root=ResolvedPath(root),
        address=RepositoryResourceAddress(address),
    )


def test_repository_nominal_identity_is_independent_of_observation_root(
    tmp_path: Path,
) -> None:
    """A logical Repository has nominal identity without a filesystem location."""
    repository = Repository.new()
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    for root in (first_root, second_root):
        (root / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    expected_uuid_version = len(("one", "two", "three", "four"))

    assert repository.id.value.value.version == expected_uuid_version
    assert RepositoryId.parse(str(repository.id)) == repository.id
    assert first_root != second_root
    assert not hasattr(repository, "root")
    assert _observe(repository, first_root, "module.py") == _observe(
        repository,
        second_root,
        "module.py",
    )


def test_snapshot_identity_is_scoped_to_the_logical_repository(tmp_path: Path) -> None:
    """Equivalent resource state in distinct logical Repositories stays distinct."""
    source = tmp_path / "module.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    first_repository = _repository()
    second_repository = Repository(
        RepositoryId.parse("00000000-0000-4000-8000-000000000002"),
    )

    first = _observe(first_repository, tmp_path, "module.py")
    second = _observe(second_repository, tmp_path, "module.py")

    assert first.resource == second.resource
    assert first.repository_id != second.repository_id
    assert first.id != second.id


def test_observes_one_required_resource_into_identified_snapshot_state(
    tmp_path: Path,
) -> None:
    """Successful observation retains repository, occurrence, and content facts."""
    source = tmp_path / "src" / "module.py"
    source.parent.mkdir()
    source.write_bytes(b"def function():\r\n    pass\r\n")

    snapshot = _observe(_repository(), tmp_path, "src/module.py")

    assert snapshot.repository_id == _repository().id
    assert snapshot.OBSERVATION_SEMANTICS == (
        "single-required-text-resource-sha256-v1"
    )
    assert isinstance(snapshot.id, RepositorySnapshotId)
    assert isinstance(snapshot.resource, RepositoryResourceOccurrence)
    assert snapshot.resource.address.parts == ("src", "module.py")
    assert str(snapshot.resource.address) == "src/module.py"
    assert isinstance(snapshot.resource.content_identity, ContentIdentity)
    assert snapshot.resource.content == "def function():\r\n    pass\r\n"
    assert snapshot.resource.encoding == "utf-8"
    assert snapshot.resource.byte_size == len(source.read_bytes())
    assert str(snapshot.id) == snapshot.id.value
    assert str(snapshot.resource.content_identity) == (
        snapshot.resource.content_identity.value
    )


def test_repeated_observation_of_unchanged_state_is_equivalent(
    tmp_path: Path,
) -> None:
    """Equivalent admitted state yields the same snapshot and content identities."""
    source = tmp_path / "module.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    repository = _repository()

    first = _observe(repository, tmp_path, "module.py")
    second = _observe(repository, tmp_path, "module.py")

    assert first == second
    assert hash(first) == hash(second)


def test_changed_content_changes_content_and_snapshot_identity(tmp_path: Path) -> None:
    """A content edit establishes different content and snapshot state."""
    source = tmp_path / "module.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    repository = _repository()
    first = _observe(repository, tmp_path, "module.py")

    source.write_text("VALUE = 2\n", encoding="utf-8")
    second = _observe(repository, tmp_path, "module.py")

    assert first.resource.content_identity != second.resource.content_identity
    assert first.id != second.id


def test_equal_content_at_distinct_addresses_preserves_distinct_occurrences(
    tmp_path: Path,
) -> None:
    """Address changes occurrence and snapshot while content identity stays equal."""
    content = "VALUE = 1\n"
    (tmp_path / "first.py").write_text(content, encoding="utf-8")
    (tmp_path / "second.py").write_text(content, encoding="utf-8")
    repository = _repository()

    first = _observe(repository, tmp_path, "first.py")
    second = _observe(repository, tmp_path, "second.py")

    assert first.resource.content_identity == second.resource.content_identity
    assert first.resource != second.resource
    assert first.resource.address != second.resource.address
    assert first.id != second.id


@pytest.mark.parametrize(
    ("value", "match"),
    [
        ("", "cannot be empty"),
        ("/absolute.py", "must be relative"),
        ("C:/absolute.py", "must be relative"),
        ("../escape.py", "canonical"),
        ("a/../escape.py", "canonical"),
    ],
)
def test_resource_address_rejects_empty_absolute_and_traversing_values(
    value: str,
    match: str,
) -> None:
    """Repository resource addresses are finite canonical relative paths."""
    with pytest.raises(ValueError, match=match):
        RepositoryResourceAddress(value)


def test_resource_address_rejects_platform_separator() -> None:
    """A Windows separator cannot bypass POSIX-style address semantics."""
    with pytest.raises(ValueError, match="forward slashes"):
        RepositoryResourceAddress(r"src\module.py")


def test_observation_rejects_a_resolved_escape(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Resolution outside the root cannot become a repository occurrence."""
    root = ResolvedPath(tmp_path / "root")
    outside = ResolvedPath(tmp_path / "outside.py")
    calls = 0

    def escape_resolution(
        value: str | Path,
        *,
        base_directory: str | Path | None = None,
    ) -> ResolvedPath:
        nonlocal calls
        del value, base_directory
        calls += 1
        return root if calls == 1 else outside

    monkeypatch.setattr(
        "devtools.context.repository.resolve_path",
        escape_resolution,
    )

    with pytest.raises(RepositoryObservationError, match="outside"):
        observe_repository_resource(
            repository=_repository(),
            root=root,
            address=RepositoryResourceAddress("module.py"),
        )


def test_missing_and_non_file_resources_do_not_produce_snapshots(
    tmp_path: Path,
) -> None:
    """Every required resource must exist and be a regular file."""
    directory = tmp_path / "directory"
    directory.mkdir()

    with pytest.raises(FilesystemNotFoundError):
        _observe(_repository(), tmp_path, "missing.py")
    with pytest.raises(NotAFileError):
        _observe(_repository(), tmp_path, "directory")


def test_unreadable_and_undecodable_resources_do_not_produce_snapshots(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Read and UTF-8 decoding failures remain unsuccessful observations."""
    source = tmp_path / "module.py"
    source.write_bytes(b"content")

    def deny_read(_path: Path) -> bytes:
        msg = "denied"
        raise PermissionError(msg)

    monkeypatch.setattr(Path, "read_bytes", deny_read)
    with pytest.raises(FilesystemPermissionError):
        _observe(_repository(), tmp_path, "module.py")

    monkeypatch.undo()
    source.write_bytes(b"\xff")
    with pytest.raises(TextDecodingError):
        _observe(_repository(), tmp_path, "module.py")


@pytest.mark.parametrize(
    ("identity_type", "value", "match"),
    [
        (ContentIdentity, "0" * 63, "64-character"),
        (ContentIdentity, "g" * 64, "64-character"),
        (RepositorySnapshotId, "A" * 64, "lowercase"),
    ],
)
def test_local_digest_identities_reject_noncanonical_values(
    identity_type: type[ContentIdentity | RepositorySnapshotId],
    value: str,
    match: str,
) -> None:
    """Local digest identities require complete lowercase SHA-256 text."""
    with pytest.raises(ValueError, match=match):
        identity_type(value)
