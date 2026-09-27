# Copyright (c) 2026
# ruff: noqa: COM812, D103, E501, PLR2004
"""Bounded source-grounded reference and direct-call breadth mechanics."""

from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from pathlib import Path

from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath
from experiments.increment_29.mechanics import _source_occurrences, project_case


def _facts(
    tmp_path: Path, resources: dict[str, str]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    for address, content in resources.items():
        path = tmp_path / address
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    addresses = tuple(RepositoryResourceAddress(item) for item in resources)
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000029")
        ),
        root=ResolvedPath(tmp_path),
        addresses=addresses,
        maximum_resource_bytes=1024 * 1024,
    )
    interpretation = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=addresses,
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpretation.interpretations,
    )
    by_address: dict[str, list[Any]] = {}
    for item in interpretation.interpretations:
        by_address.setdefault(str(item.resource.address), []).append(item)
    corpus = SimpleNamespace(snapshot=snapshot, addresses=addresses)
    return _source_occurrences(
        corpus=cast("Any", corpus), universe=universe, by_address=by_address
    )


def test_direct_alias_reference_and_direct_call(tmp_path: Path) -> None:
    occurrences, diagnostic = _facts(
        tmp_path,
        {
            "src/consumer.py": "from target import f as alias\nx = alias\ny = alias()\n",
            "src/target.py": "def f():\n    return 1\n",
        },
    )
    assert len(occurrences) == 2
    assert [row["direct_call"] for row in occurrences] == [False, True]
    assert {row["target_resource"] for row in occurrences} == {"src/target.py"}
    assert {row["resolution_path"] for row in occurrences} == {"direct-module"}
    assert diagnostic["counts"]["reference_occurrences"] == 2
    assert diagnostic["counts"]["direct_call_occurrences"] == 1


def test_single_facade_target_and_shadowing(tmp_path: Path) -> None:
    occurrences, _ = _facts(
        tmp_path,
        {
            "src/consumer.py": "from package import f\nx = f\n",
            "src/package/__init__.py": "from .impl import f\n",
            "src/package/impl.py": "def f():\n    return 1\n",
        },
    )
    assert len(occurrences) == 1
    assert occurrences[0]["target_resource"] == "src/package/impl.py"
    assert occurrences[0]["resolution_path"] == "single-facade"
    shadowed, diagnostics = _facts(
        tmp_path,
        {
            "src/consumer.py": "from target import f\ndef use():\n    f = lambda: 1\n    return f()\n",
            "src/target.py": "def f():\n    return 1\n",
        },
    )
    assert not shadowed
    assert (
        diagnostics["counts"]["binding_indeterminate_uncertain-relevant-occurrence"]
        == 1
    )


def test_bidirectional_projection_deduplicates_and_classifies() -> None:
    seeds = [
        {"address": address, "canonical_rank": rank}
        for rank, address in enumerate(
            (
                "src/seed.py",
                "src/other1.py",
                "src/other2.py",
                "src/other3.py",
                "src/other4.py",
            ),
            1,
        )
    ]
    case = {
        "case_id": "case",
        "parent_snapshot_sha": "sha",
        "information_need": {"purpose": "p", "lexical_query": "q"},
        "snapshot_id": "snapshot",
        "corpus_id": "corpus",
        "seeds": seeds,
        "arms": {"outgoing": {"candidates": []}, "incoming": {"candidates": []}},
    }
    occurrences = [
        {
            "source_resource": "src/seed.py",
            "target_resource": "src/novel.py",
            "direct_call": False,
        },
        {
            "source_resource": "src/seed.py",
            "target_resource": "src/novel.py",
            "direct_call": True,
        },
        {
            "source_resource": "src/novel.py",
            "target_resource": "src/seed.py",
            "direct_call": False,
        },
    ]
    lexical: dict[str, Any] = {
        "rankings": {
            method: []
            for method in ("canonical", "bm25_plus", "identifier", "path", "rrf")
        }
    }
    projected = project_case(
        case=case,
        occurrences=occurrences,
        lexical=lexical,
        import_case=case,
        diagnostics={},
    )
    assert projected["candidate_count"] == 1
    row = projected["candidates"][0]
    assert row["support_count"] == 3
    assert row["directions"] == ["forward", "reverse"]
    assert row["reference"]
    assert row["direct_call"]
    assert row["absent_all_saved_positive_lexical"]
    assert not row["existing_import_candidate"]
