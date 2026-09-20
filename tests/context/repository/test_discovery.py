# Copyright (c) 2026
"""Tests for bounded repository regular-file address discovery."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from devtools.context import (
    PythonFunctionExactNameQuery,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    RepositoryResourceDiscovery,
    RepositoryResourceDiscoveryError,
    analyze_python_function_declaration_resources,
    assemble_python_function_context_model_request,
    disclose_python_function_exact_name_retrieval,
    discover_repository_resource_addresses,
    materialize_python_function_disclosure_source,
    observe_repository_resources,
    render_materialized_python_function_context,
    retrieve_python_functions_by_exact_name,
    select_python_function_analysis_candidates,
    select_python_function_resources_from_exact_name_retrieval,
)
from devtools.core.paths import ResolvedPath
from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from types import TracebackType

_REPOSITORY_ID = "00000000-0000-4000-8000-000000000001"
_DISCOVERY_LIMIT = 20
_TRAVERSAL_LIMIT = 100
_EXPECTED_COMPOSITION_ENTRY_COUNT = 6
_EXPECTED_DISCOVERED_COUNT = 5
_EXPECTED_ELIGIBLE_COUNT = 4
_EXPECTED_CANDIDATE_COUNT = 3
_MAXIMUM_RESOURCE_BYTES = 16 * 1024 * 1024


def _repository() -> Repository:
    """Return one stable logical repository for discovery tests."""
    return Repository(RepositoryId.parse(_REPOSITORY_ID))


def test_recursive_discovery_composes_with_explicit_observation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Discovery returns only canonical addresses; observation acquires content."""
    root = tmp_path / "repository"
    nested = root / "nested"
    empty = root / "empty"
    nested.mkdir(parents=True)
    empty.mkdir()
    (root / "a.py").write_text("A = 1\n", encoding="utf-8", newline="")
    (nested / "b.py").write_text("B = 2\n", encoding="utf-8", newline="")
    (nested / "notes.txt").write_text(
        "notes\n",
        encoding="utf-8",
        newline="",
    )
    (root / "README.md").write_text("readme\n", encoding="utf-8", newline="")

    def forbidden_read(*_args: object, **_kwargs: object) -> None:
        msg = "discovery attempted file-content acquisition"
        raise AssertionError(msg)

    with monkeypatch.context() as discovery_guard:
        discovery_guard.setattr(Path, "read_bytes", forbidden_read)
        discovery_guard.setattr(
            "devtools.context.repository.observation.read", forbidden_read,
        )
        discovery = discover_repository_resource_addresses(
            repository=_repository(),
            root=ResolvedPath(root),
            maximum_resource_count=_DISCOVERY_LIMIT,
            maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
        )

    expected_addresses = tuple(
        RepositoryResourceAddress(value)
        for value in ("README.md", "a.py", "nested/b.py", "nested/notes.txt")
    )
    assert isinstance(discovery, RepositoryResourceDiscovery)
    assert discovery.repository_id == _repository().id
    assert discovery.root == ResolvedPath(root.resolve())
    assert discovery.maximum_resource_count == _DISCOVERY_LIMIT
    assert discovery.maximum_traversal_entry_count == _TRAVERSAL_LIMIT
    assert discovery.examined_entry_count == _EXPECTED_COMPOSITION_ENTRY_COUNT
    assert discovery.addresses == expected_addresses
    assert discovery.DISCOVERY_SEMANTICS == (
        "recursive-entry-bounded-regular-files-skip-links-lexical-address-order-v2"
    )
    assert not hasattr(discovery, "snapshot_id")
    assert not hasattr(discovery, "content_identity")
    assert not hasattr(discovery, "resources")

    snapshot = observe_repository_resources(
        repository=_repository(),
        root=ResolvedPath(root),
        addresses=discovery.addresses,
        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,
    )

    assert tuple(resource.address for resource in snapshot.resources) == (
        discovery.addresses
    )
    assert [resource.content for resource in snapshot.resources] == [
        "readme\n",
        "A = 1\n",
        "B = 2\n",
        "notes\n",
    ]


def test_discovery_feeds_the_existing_python_function_pipeline(
    tmp_path: Path,
) -> None:
    """Caller eligibility narrows discovery before lexical and AST verification."""
    root = tmp_path / "repository"
    root.mkdir()
    sources = {
        "declaration.py": "def selected_function():\n    return 'TARGET'\n",
        "call.py": "value = selected_function()\n",
        "method.py": (
            "class Holder:\n    def selected_function(self):\n        return 'METHOD'\n"
        ),
        "unrelated.py": "def helper():\n    return 'OTHER'\n",
        "notes.txt": "selected_function\n",
    }
    for address, content in sources.items():
        (root / address).write_text(content, encoding="utf-8", newline="")

    discovery = discover_repository_resource_addresses(
        repository=_repository(),
        root=ResolvedPath(root),
        maximum_resource_count=_DISCOVERY_LIMIT,
        maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
    )
    snapshot = observe_repository_resources(
        repository=_repository(),
        root=ResolvedPath(root),
        addresses=discovery.addresses,
        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,
    )
    eligible_addresses = tuple(
        address for address in discovery.addresses if address.value.endswith(".py")
    )
    query = PythonFunctionExactNameQuery("selected_function")
    candidates = select_python_function_analysis_candidates(
        snapshot,
        query=query,
        resource_addresses=eligible_addresses,
    )
    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=candidates.candidate_resource_addresses,
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=query,
    )
    verified = select_python_function_resources_from_exact_name_retrieval(retrieval)
    disclosure = disclose_python_function_exact_name_retrieval(retrieval)
    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    rendered = render_materialized_python_function_context(materialized)
    request = assemble_python_function_context_model_request(
        task_request=ModelRequest(Prompt("Inspect selected_function.", "user")),
        context=rendered,
    )

    assert len(discovery.addresses) == _EXPECTED_DISCOVERED_COUNT
    assert len(snapshot.resources) == _EXPECTED_DISCOVERED_COUNT
    assert len(eligible_addresses) == _EXPECTED_ELIGIBLE_COUNT
    assert len(candidates.candidates) == _EXPECTED_CANDIDATE_COUNT
    assert len(aggregate.analyses) == _EXPECTED_CANDIDATE_COUNT
    assert len(retrieval.matches) == 1
    assert verified.resource_addresses == (RepositoryResourceAddress("declaration.py"),)
    assert len(disclosure.items) == 1
    assert len(materialized.items) == 1
    assert "Repository-relative resource: declaration.py" in rendered.text
    assert "Repository-relative resource: call.py" not in rendered.text
    assert "Repository-relative resource: method.py" not in rendered.text
    assert rendered.text in request.prompt.content


def test_discovery_skips_symbolic_links_and_directories(
    tmp_path: Path,
) -> None:
    """Link-like entries are not followed into external filesystem trees."""
    root = tmp_path / "repository"
    external = tmp_path / "external"
    root.mkdir()
    external.mkdir()
    (root / "regular.txt").write_text("regular\n", encoding="utf-8")
    (external / "outside.txt").write_text("outside\n", encoding="utf-8")
    (root / "linked-directory").symlink_to(external, target_is_directory=True)
    (root / "linked-file.txt").symlink_to(external / "outside.txt")

    discovery = discover_repository_resource_addresses(
        repository=_repository(),
        root=ResolvedPath(root),
        maximum_resource_count=_DISCOVERY_LIMIT,
        maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
    )

    assert discovery.addresses == (RepositoryResourceAddress("regular.txt"),)


def test_empty_discovery_is_successful_and_resource_bound_is_strict(
    tmp_path: Path,
) -> None:
    """Empty is successful, while exceeding the explicit bound publishes nothing."""
    empty = tmp_path / "empty"
    empty.mkdir()
    empty_result = discover_repository_resource_addresses(
        repository=_repository(),
        root=ResolvedPath(empty),
        maximum_resource_count=1,
        maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
    )
    assert empty_result.addresses == ()
    assert not hasattr(empty_result, "repository_is_empty")

    bounded = tmp_path / "bounded"
    bounded.mkdir()
    (bounded / "a.txt").write_text("a\n", encoding="utf-8")
    (bounded / "b.txt").write_text("b\n", encoding="utf-8")
    with pytest.raises(RepositoryResourceDiscoveryError, match="exceeds maximum"):
        discover_repository_resource_addresses(
            repository=_repository(),
            root=ResolvedPath(bounded),
            maximum_resource_count=1,
            maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
        )


@pytest.mark.parametrize("maximum_resource_count", [0, -1])
def test_discovery_requires_a_positive_resource_bound(
    tmp_path: Path,
    maximum_resource_count: int,
) -> None:
    """An unbounded or nonsensical discovery request is rejected."""
    with pytest.raises(ValueError, match="must be positive"):
        discover_repository_resource_addresses(
            repository=_repository(),
            root=ResolvedPath(tmp_path),
            maximum_resource_count=maximum_resource_count,
            maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
        )


@pytest.mark.parametrize("maximum_traversal_entry_count", [0, -1])
def test_discovery_requires_a_positive_traversal_bound(
    tmp_path: Path,
    maximum_traversal_entry_count: int,
) -> None:
    """Traversal work cannot be requested without a positive finite bound."""
    with pytest.raises(ValueError, match="traversal entry count must be positive"):
        discover_repository_resource_addresses(
            repository=_repository(),
            root=ResolvedPath(tmp_path),
            maximum_resource_count=_DISCOVERY_LIMIT,
            maximum_traversal_entry_count=maximum_traversal_entry_count,
        )


def test_empty_directories_can_exhaust_the_traversal_bound(
    tmp_path: Path,
) -> None:
    """Entry work is bounded even when recursive traversal finds no files."""
    root = tmp_path / "repository"
    current = root
    for ordinal in range(5):
        current = current / f"empty-{ordinal}"
        current.mkdir(parents=True)

    with pytest.raises(
        RepositoryResourceDiscoveryError,
        match="filesystem entry count exceeds maximum 3",
    ):
        discover_repository_resource_addresses(
            repository=_repository(),
            root=ResolvedPath(root),
            maximum_resource_count=1,
            maximum_traversal_entry_count=3,
        )


@pytest.mark.parametrize("root_kind", ["missing", "file"])
def test_invalid_discovery_root_fails_instead_of_returning_empty(
    tmp_path: Path,
    root_kind: str,
) -> None:
    """A missing or non-directory root is an operation failure, not empty success."""
    root = tmp_path / root_kind
    if root_kind == "file":
        root.write_text("content\n", encoding="utf-8")

    with pytest.raises(RepositoryResourceDiscoveryError) as captured:
        discover_repository_resource_addresses(
            repository=_repository(),
            root=ResolvedPath(root),
            maximum_resource_count=_DISCOVERY_LIMIT,
            maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
        )

    assert captured.value.root == ResolvedPath(root.resolve())
    assert captured.value.discovery_message


def test_traversal_and_classification_failures_publish_no_partial_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Directory access and entry classification failures remain explicit."""
    root = ResolvedPath(tmp_path)

    def denied_scandir(_path: Path) -> object:
        msg = "directory denied"
        raise PermissionError(msg)

    monkeypatch.setattr(
        "devtools.context.repository.discovery.os.scandir",
        denied_scandir,
    )
    with pytest.raises(RepositoryResourceDiscoveryError, match="directory denied"):
        discover_repository_resource_addresses(
            repository=_repository(),
            root=root,
            maximum_resource_count=_DISCOVERY_LIMIT,
            maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
        )

    class FailingEntry:
        name = "blocked"

        def is_symlink(self) -> bool:
            msg = "classification denied"
            raise PermissionError(msg)

    class FailingScandir:
        def __enter__(self) -> tuple[FailingEntry, ...]:
            return (FailingEntry(),)

        def __exit__(
            self,
            _exception_type: type[BaseException] | None,
            _exception: BaseException | None,
            _traceback: TracebackType | None,
        ) -> None:
            return None

    monkeypatch.setattr(
        "devtools.context.repository.discovery.os.scandir",
        lambda _path: FailingScandir(),
    )
    with pytest.raises(RepositoryResourceDiscoveryError, match="classification denied"):
        discover_repository_resource_addresses(
            repository=_repository(),
            root=root,
            maximum_resource_count=_DISCOVERY_LIMIT,
            maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
        )


def test_resolved_child_escape_is_rejected_before_traversal(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Resolved descendant directories cannot redirect discovery outside its root."""
    root = tmp_path / "repository"
    child = root / "child"
    outside = tmp_path / "outside"
    child.mkdir(parents=True)
    outside.mkdir()
    calls = 0

    def escape_resolution(value: str | Path) -> ResolvedPath:
        nonlocal calls
        del value
        calls += 1
        return ResolvedPath(root) if calls == 1 else ResolvedPath(outside)

    monkeypatch.setattr(
        "devtools.context.repository.discovery.resolve_path",
        escape_resolution,
    )

    with pytest.raises(RepositoryResourceDiscoveryError, match="escapes"):
        discover_repository_resource_addresses(
            repository=_repository(),
            root=ResolvedPath(root),
            maximum_resource_count=_DISCOVERY_LIMIT,
            maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
        )


def test_discovery_invokes_no_observation_or_downstream_pipeline_work(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Discovery performs metadata traversal without content or semantic work."""
    (tmp_path / "module.py").write_text(
        "def selected_function():\n    pass\n",
        encoding="utf-8",
    )

    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "discovery attempted observation or downstream work"
        raise AssertionError(msg)

    monkeypatch.setattr("devtools.context.repository.observation.read", forbidden)
    monkeypatch.setattr(
        "devtools.context.repository.observation.observe_repository_resources",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.candidates.tokenize.generate_tokens",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.declarations.ast.parse", forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.declarations.derive_python_function_declarations",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.retrieval.retrieve_python_functions_by_exact_name",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.disclosure.disclose_python_function_exact_name_retrieval",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.materialization.materialize_python_function_disclosure_source",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.rendering.render_materialized_python_function_context",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.function.request_assembly.assemble_python_function_context_model_request",
        forbidden,
    )

    discovery = discover_repository_resource_addresses(
        repository=_repository(),
        root=ResolvedPath(tmp_path),
        maximum_resource_count=_DISCOVERY_LIMIT,
        maximum_traversal_entry_count=_TRAVERSAL_LIMIT,
    )

    assert discovery.addresses == (RepositoryResourceAddress("module.py"),)
