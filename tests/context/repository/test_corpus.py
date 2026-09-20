# Copyright (c) 2026
"""Tests for explicit discovery-grounded corpus membership intent."""

from pathlib import Path

import pytest

from devtools.context import (
    ContentIdentity,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    RepositoryResourceDiscovery,
    RepositoryResourceOccurrence,
    RepositorySnapshot,
    RepositorySnapshotId,
    RepositoryTextCorpusId,
    define_repository_text_corpus,
    observe_repository_resources,
    realize_repository_text_corpus,
)
from devtools.core.paths import ResolvedPath


def _discovery() -> RepositoryResourceDiscovery:
    return RepositoryResourceDiscovery(
        repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000001"),
        root=ResolvedPath(Path.cwd()),
        maximum_resource_count=20,
        maximum_traversal_entry_count=20,
        examined_entry_count=8,
        addresses=tuple(
            RepositoryResourceAddress(value)
            for value in (
                ".gitignore", "README.md", "assets/image.bin", "config.json",
                "notes", "pyproject.toml", "src/example.py", "uv.lock",
            )
        ),
    )


def _empty_discovery() -> RepositoryResourceDiscovery:
    return RepositoryResourceDiscovery(
        repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000001"),
        root=ResolvedPath(Path.cwd()),
        maximum_resource_count=20,
        maximum_traversal_entry_count=20,
        examined_entry_count=0,
        addresses=(),
    )


def _repository(value: str = "00000000-0000-4000-8000-000000000001") -> Repository:
    return Repository(RepositoryId.parse(value))


def _observe(
    *,
    repository: Repository,
    root: Path,
    addresses: tuple[str, ...],
) -> RepositorySnapshot:
    return observe_repository_resources(
        repository=repository,
        root=ResolvedPath(root),
        addresses=tuple(RepositoryResourceAddress(address) for address in addresses),
        maximum_resource_bytes=1024,
    )


def test_membership_is_discovery_grounded_heterogeneous_and_canonical() -> None:
    """Membership preserves discovery correlation and heterogeneous addresses."""
    discovery = _discovery()
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(
            RepositoryResourceAddress("uv.lock"),
            RepositoryResourceAddress("assets/image.bin"),
            RepositoryResourceAddress("src/example.py"),
        ),
    )
    assert definition.discovery is discovery
    assert tuple(map(str, definition.selected_addresses)) == (
        "assets/image.bin", "src/example.py", "uv.lock",
    )
    assert tuple(map(str, definition.excluded_addresses)) == (
        ".gitignore",
        "README.md",
        "config.json",
        "notes",
        "pyproject.toml",
    )


def test_equivalent_selection_is_caller_order_independent() -> None:
    """Equivalent caller selections yield the same canonical immutable value."""
    discovery = _discovery()
    first = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(
            RepositoryResourceAddress("src/example.py"),
            RepositoryResourceAddress("README.md"),
        ),
    )
    second = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(
            RepositoryResourceAddress("README.md"),
            RepositoryResourceAddress("src/example.py"),
        ),
    )
    assert first == second
    assert tuple(map(str, first.selected_addresses)) == ("README.md", "src/example.py")


def test_empty_membership_retains_nonempty_discovery() -> None:
    """An empty selection means only that no discovered address was selected."""
    discovery = _discovery()
    empty = define_repository_text_corpus(discovery=discovery, selected_addresses=())
    assert empty.discovery is discovery
    assert empty.selected_addresses == ()
    assert empty.excluded_addresses == discovery.addresses


def test_empty_discovery_can_define_an_empty_membership() -> None:
    """An empty definition remains correlated with its completed empty discovery."""
    discovery = _empty_discovery()
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(),
    )
    assert definition.discovery is discovery
    assert definition.selected_addresses == ()
    assert definition.excluded_addresses == ()


def test_duplicate_or_undiscovered_selection_fails() -> None:
    """Membership accepts only distinct addresses from the supplied discovery."""
    discovery = _discovery()
    address = RepositoryResourceAddress("src/example.py")
    with pytest.raises(ValueError, match="distinct"):
        define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=(address, address),
        )
    with pytest.raises(ValueError, match="not discovered"):
        define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=(RepositoryResourceAddress("missing.py"),),
        )


def test_definition_construction_performs_no_acquisition_or_analysis(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Membership construction does not rediscover, observe, parse, or classify."""
    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Definition construction must not perform work."
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.context.repository.discovery.discover_repository_resource_addresses",
        fail,
    )
    monkeypatch.setattr(
        "devtools.context.repository.observation.observe_repository_resources",
        fail,
    )
    monkeypatch.setattr("devtools.context.repository.observation.read", fail)
    monkeypatch.setattr("devtools.context.python.function.declarations.ast.parse", fail)

    definition = define_repository_text_corpus(
        discovery=_discovery(),
        selected_addresses=(RepositoryResourceAddress("assets/image.bin"),),
    )

    assert tuple(map(str, definition.selected_addresses)) == ("assets/image.bin",)


def test_realization_retains_exact_selected_observed_occurrences_in_definition_order(
    tmp_path: Path,
) -> None:
    """A corpus realizes only its selected occurrences in canonical definition order."""
    (tmp_path / "README.md").write_text("readme\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "example.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    repository = _repository()
    discovery = RepositoryResourceDiscovery(
        repository_id=repository.id,
        root=ResolvedPath(tmp_path),
        maximum_resource_count=10,
        maximum_traversal_entry_count=10,
        examined_entry_count=3,
        addresses=(
            RepositoryResourceAddress("README.md"),
            RepositoryResourceAddress("pyproject.toml"),
            RepositoryResourceAddress("src/example.py"),
        ),
    )
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(
            RepositoryResourceAddress("src/example.py"),
            RepositoryResourceAddress("README.md"),
        ),
    )
    snapshot = _observe(
        repository=repository,
        root=tmp_path,
        addresses=("README.md", "pyproject.toml", "src/example.py"),
    )

    corpus = realize_repository_text_corpus(definition=definition, snapshot=snapshot)

    assert corpus.definition is definition
    assert [str(resource.address) for resource in corpus.resources] == [
        "README.md",
        "src/example.py",
    ]
    assert corpus.resources[0] is snapshot.resource_at(
        RepositoryResourceAddress("README.md"),
    )
    assert corpus.resources[1] is snapshot.resource_at(
        RepositoryResourceAddress("src/example.py"),
    )


def test_unselected_observed_state_does_not_become_a_member_or_identity_input(
    tmp_path: Path,
) -> None:
    """An extra observed resource cannot change the selected corpus identity."""
    selected = tmp_path / "selected.txt"
    extra = tmp_path / "extra.txt"
    selected.write_text("selected\n", encoding="utf-8")
    extra.write_text("first\n", encoding="utf-8")
    repository = _repository()
    discovery = RepositoryResourceDiscovery(
        repository_id=repository.id,
        root=ResolvedPath(tmp_path),
        maximum_resource_count=10,
        maximum_traversal_entry_count=10,
        examined_entry_count=2,
        addresses=(
            RepositoryResourceAddress("extra.txt"),
            RepositoryResourceAddress("selected.txt"),
        ),
    )
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(RepositoryResourceAddress("selected.txt"),),
    )
    first = realize_repository_text_corpus(
        definition=definition,
        snapshot=_observe(
            repository=repository,
            root=tmp_path,
            addresses=("extra.txt", "selected.txt"),
        ),
    )
    extra.write_text("second\n", encoding="utf-8")
    second = realize_repository_text_corpus(
        definition=definition,
        snapshot=_observe(
            repository=repository,
            root=tmp_path,
            addresses=("extra.txt", "selected.txt"),
        ),
    )

    assert first.id == second.id
    assert [str(resource.address) for resource in second.resources] == ["selected.txt"]


def test_selected_content_membership_and_repository_change_corpus_identity(
    tmp_path: Path,
) -> None:
    """Corpus identity is scoped to selected content, membership, and Repository."""
    (tmp_path / "alpha.txt").write_text("alpha\n", encoding="utf-8")
    (tmp_path / "beta.txt").write_text("alpha\n", encoding="utf-8")
    first_repository = _repository()
    second_repository = _repository("00000000-0000-4000-8000-000000000002")
    discovery = RepositoryResourceDiscovery(
        repository_id=first_repository.id,
        root=ResolvedPath(tmp_path),
        maximum_resource_count=10,
        maximum_traversal_entry_count=10,
        examined_entry_count=2,
        addresses=(
            RepositoryResourceAddress("alpha.txt"),
            RepositoryResourceAddress("beta.txt"),
        ),
    )
    alpha_definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(RepositoryResourceAddress("alpha.txt"),),
    )
    beta_definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=(RepositoryResourceAddress("beta.txt"),),
    )
    first_snapshot = _observe(
        repository=first_repository,
        root=tmp_path,
        addresses=("alpha.txt", "beta.txt"),
    )
    alpha = realize_repository_text_corpus(
        definition=alpha_definition,
        snapshot=first_snapshot,
    )
    beta = realize_repository_text_corpus(
        definition=beta_definition,
        snapshot=first_snapshot,
    )
    (tmp_path / "alpha.txt").write_text("changed\n", encoding="utf-8")
    changed = realize_repository_text_corpus(
        definition=alpha_definition,
        snapshot=_observe(
            repository=first_repository,
            root=tmp_path,
            addresses=("alpha.txt", "beta.txt"),
        ),
    )
    other_discovery = RepositoryResourceDiscovery(
        repository_id=second_repository.id,
        root=ResolvedPath(tmp_path),
        maximum_resource_count=10,
        maximum_traversal_entry_count=10,
        examined_entry_count=2,
        addresses=discovery.addresses,
    )
    other_definition = define_repository_text_corpus(
        discovery=other_discovery,
        selected_addresses=(RepositoryResourceAddress("alpha.txt"),),
    )
    other = realize_repository_text_corpus(
        definition=other_definition,
        snapshot=_observe(
            repository=second_repository,
            root=tmp_path,
            addresses=("alpha.txt", "beta.txt"),
        ),
    )

    assert alpha.id != beta.id
    assert alpha.id != changed.id
    assert changed.id != other.id


def test_realization_rejects_missing_mismatched_or_duplicate_observed_state(
    tmp_path: Path,
) -> None:
    """Nonempty realization validates the supplied observed state exactly."""
    (tmp_path / "selected.txt").write_text("selected\n", encoding="utf-8")
    repository = _repository()
    address = RepositoryResourceAddress("selected.txt")
    definition = define_repository_text_corpus(
        discovery=RepositoryResourceDiscovery(
            repository_id=repository.id,
            root=ResolvedPath(tmp_path),
            maximum_resource_count=10,
            maximum_traversal_entry_count=10,
            examined_entry_count=1,
            addresses=(address,),
        ),
        selected_addresses=(address,),
    )
    empty_snapshot = _observe(repository=repository, root=tmp_path, addresses=())
    with pytest.raises(ValueError, match="requires an observed snapshot"):
        realize_repository_text_corpus(definition=definition)
    with pytest.raises(ValueError, match="lacks selected"):
        realize_repository_text_corpus(definition=definition, snapshot=empty_snapshot)
    mismatched_snapshot = _observe(
        repository=_repository("00000000-0000-4000-8000-000000000002"),
        root=tmp_path,
        addresses=("selected.txt",),
    )
    with pytest.raises(ValueError, match="does not match"):
        realize_repository_text_corpus(
            definition=definition,
            snapshot=mismatched_snapshot,
        )
    occurrence = RepositoryResourceOccurrence(
        address=address,
        content_identity=ContentIdentity("0" * 64),
        content="selected\n",
        encoding="utf-8",
        byte_size=len("selected\n"),
    )
    duplicate_snapshot = RepositorySnapshot(
        id=RepositorySnapshotId("0" * 64),
        repository_id=repository.id,
        resources=(occurrence, occurrence),
    )
    with pytest.raises(ValueError, match="repeats"):
        realize_repository_text_corpus(
            definition=definition,
            snapshot=duplicate_snapshot,
        )


def test_empty_definition_realizes_without_observed_state_or_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty membership has no observed-resource dependency or acquisition work."""
    definition = define_repository_text_corpus(
        discovery=_empty_discovery(),
        selected_addresses=(),
    )

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Empty corpus realization must not perform work."
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.corpus._selected_resource", fail)
    monkeypatch.setattr("devtools.context.repository.observation.read", fail)
    monkeypatch.setattr(
        "devtools.context.repository.discovery.discover_repository_resource_addresses",
        fail,
    )
    monkeypatch.setattr("devtools.context.python.function.declarations.ast.parse", fail)

    first = realize_repository_text_corpus(definition=definition)
    second = realize_repository_text_corpus(
        definition=definition,
        snapshot=RepositorySnapshot(
            id=RepositorySnapshotId("0" * 64),
            repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000002"),
            resources=(),
        ),
    )

    assert first == second
    assert first.resources == ()
    assert str(first.id) == first.id.value


def test_nonempty_realization_performs_no_acquisition_or_analysis(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Nonempty realization projects supplied occurrences without further work."""
    repository = _repository()
    address = RepositoryResourceAddress("selected.txt")
    occurrence = RepositoryResourceOccurrence(
        address=address,
        content_identity=ContentIdentity("0" * 64),
        content="selected\n",
        encoding="utf-8",
        byte_size=len("selected\n"),
    )
    definition = define_repository_text_corpus(
        discovery=RepositoryResourceDiscovery(
            repository_id=repository.id,
            root=ResolvedPath(Path.cwd()),
            maximum_resource_count=10,
            maximum_traversal_entry_count=10,
            examined_entry_count=1,
            addresses=(address,),
        ),
        selected_addresses=(address,),
    )
    snapshot = RepositorySnapshot(
        id=RepositorySnapshotId("0" * 64),
        repository_id=repository.id,
        resources=(occurrence,),
    )

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "Corpus realization must not perform additional work."
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", fail)
    monkeypatch.setattr(
        "devtools.context.repository.discovery.discover_repository_resource_addresses",
        fail,
    )
    monkeypatch.setattr("devtools.context.python.function.declarations.ast.parse", fail)
    monkeypatch.setattr(
        "devtools.context.python.function.retrieval.retrieve_python_functions_by_exact_name",
        fail,
    )

    corpus = realize_repository_text_corpus(definition=definition, snapshot=snapshot)

    assert corpus.resources == (occurrence,)


def test_corpus_identity_rejects_noncanonical_value() -> None:
    """Corpus identities use the existing lowercase SHA-256 validation contract."""
    with pytest.raises(ValueError, match="64-character"):
        RepositoryTextCorpusId("not-a-digest")
