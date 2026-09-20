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
    observe_repository_resources,
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


def _observe_many(
    repository: Repository,
    root: Path,
    *addresses: str,
) -> RepositorySnapshot:
    """Observe an explicit fixture resource collection through the public boundary."""
    return observe_repository_resources(
        repository=repository,
        root=ResolvedPath(root),
        addresses=tuple(RepositoryResourceAddress(value) for value in addresses),
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
        "explicit-required-text-resources-sha256-v1"
    )
    assert snapshot.resources == (snapshot.resource,)
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


def test_observes_multiple_explicit_resources_as_one_identified_snapshot(
    tmp_path: Path,
) -> None:
    """One snapshot retains every distinct required occurrence and its content."""
    (tmp_path / "zeta.py").write_bytes(b"ZETA = 1\n")
    nested = tmp_path / "src" / "alpha.py"
    nested.parent.mkdir()
    nested.write_bytes(b"ALPHA = 2\n")

    snapshot = _observe_many(_repository(), tmp_path, "zeta.py", "src/alpha.py")

    assert [str(resource.address) for resource in snapshot.resources] == [
        "src/alpha.py",
        "zeta.py",
    ]
    assert [resource.content for resource in snapshot.resources] == [
        "ALPHA = 2\n",
        "ZETA = 1\n",
    ]
    assert all(
        isinstance(resource.content_identity, ContentIdentity)
        for resource in snapshot.resources
    )
    with pytest.raises(ValueError, match="exactly one"):
        _ = snapshot.resource


def test_multi_resource_state_is_root_and_caller_order_independent(
    tmp_path: Path,
) -> None:
    """Canonical address order makes equivalent admitted collections equivalent."""
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    for root in (first_root, second_root):
        (root / "alpha.py").write_text("ALPHA = 1\n", encoding="utf-8")
        (root / "beta.py").write_text("BETA = 2\n", encoding="utf-8")

    first = _observe_many(_repository(), first_root, "beta.py", "alpha.py")
    second = _observe_many(_repository(), second_root, "alpha.py", "beta.py")

    assert first == second
    assert first.id == second.id
    assert first.resources == second.resources


def test_changing_one_resource_changes_multi_resource_snapshot_state(
    tmp_path: Path,
) -> None:
    """Every required occurrence contributes to identified snapshot state."""
    alpha = tmp_path / "alpha.py"
    beta = tmp_path / "beta.py"
    alpha.write_text("ALPHA = 1\n", encoding="utf-8")
    beta.write_text("BETA = 2\n", encoding="utf-8")
    first = _observe_many(_repository(), tmp_path, "alpha.py", "beta.py")

    beta.write_text("BETA = 3\n", encoding="utf-8")
    second = _observe_many(_repository(), tmp_path, "alpha.py", "beta.py")

    assert first.resources[0] == second.resources[0]
    assert first.resources[1].content_identity != second.resources[1].content_identity
    assert first.id != second.id


def test_equal_content_at_two_addresses_retains_distinct_multi_occurrences(
    tmp_path: Path,
) -> None:
    """Equal content identity does not collapse address-contextual occurrences."""
    content = "VALUE = 1\n"
    (tmp_path / "alpha.py").write_text(content, encoding="utf-8")
    (tmp_path / "beta.py").write_text(content, encoding="utf-8")

    snapshot = _observe_many(_repository(), tmp_path, "alpha.py", "beta.py")
    first, second = snapshot.resources

    assert first.address != second.address
    assert first != second
    assert first.content_identity == second.content_identity


def test_multi_resource_observation_rejects_empty_and_duplicate_requests(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Invalid requested collections fail before acquiring repository state."""
    address = RepositoryResourceAddress("module.py")

    def forbidden_read(*_args: object, **_kwargs: object) -> None:
        msg = "invalid collection attempted acquisition"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.read", forbidden_read)
    with pytest.raises(ValueError, match="at least one"):
        observe_repository_resources(
            repository=_repository(),
            root=ResolvedPath(tmp_path),
            addresses=(),
        )
    with pytest.raises(ValueError, match="distinct"):
        observe_repository_resources(
            repository=_repository(),
            root=ResolvedPath(tmp_path),
            addresses=(address, address),
        )


def test_required_multi_resource_failure_does_not_publish_a_snapshot(
    tmp_path: Path,
) -> None:
    """A missing required member fails the whole bounded observation operation."""
    (tmp_path / "available.py").write_text("VALUE = 1\n", encoding="utf-8")

    with pytest.raises(FilesystemNotFoundError):
        _observe_many(_repository(), tmp_path, "available.py", "missing.py")


def test_unsupported_and_undecodable_multi_resources_prevent_a_snapshot(
    tmp_path: Path,
) -> None:
    """Every requested member must be a decodable regular UTF-8 text file."""
    (tmp_path / "available.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "directory").mkdir()
    (tmp_path / "undecodable.py").write_bytes(b"\xff")

    with pytest.raises(NotAFileError):
        _observe_many(_repository(), tmp_path, "available.py", "directory")
    with pytest.raises(TextDecodingError):
        _observe_many(_repository(), tmp_path, "available.py", "undecodable.py")


def test_unreadable_multi_resource_prevents_a_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A read failure for one required member fails the complete operation."""
    available = tmp_path / "available.py"
    denied = tmp_path / "denied.py"
    available.write_text("VALUE = 1\n", encoding="utf-8")
    denied.write_text("VALUE = 2\n", encoding="utf-8")
    original_read_bytes = Path.read_bytes

    def deny_one(path: Path) -> bytes:
        if path == denied:
            msg = "denied"
            raise PermissionError(msg)
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", deny_one)

    with pytest.raises(FilesystemPermissionError):
        _observe_many(_repository(), tmp_path, "available.py", "denied.py")


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
