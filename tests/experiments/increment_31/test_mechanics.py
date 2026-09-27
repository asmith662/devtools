# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Exact mirrored paths and outcome-blind one-edge projections."""

from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath
from experiments.increment_31.mechanics import derive_mirrors, project_case, summarize

if TYPE_CHECKING:
    from pathlib import Path

    from experiments.increment_25.development import SnapshotCorpus


def _corpus(tmp_path: Path, paths: list[str]) -> SnapshotCorpus:
    for address in paths:
        target = tmp_path / address
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# observed\n", encoding="utf-8")
    addresses = tuple(RepositoryResourceAddress(address) for address in paths)
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000031")
        ),
        root=ResolvedPath(tmp_path),
        addresses=addresses,
        maximum_resource_bytes=1024,
    )
    return cast(
        "SnapshotCorpus", SimpleNamespace(snapshot=snapshot, addresses=addresses)
    )


def _case(seeds: list[str]) -> dict[str, Any]:
    return {
        "case_id": "case-1",
        "parent_snapshot_sha": "parent",
        "snapshot_id": "snapshot",
        "corpus_id": "corpus",
        "information_need": {"purpose": "task", "lexical_query": "query"},
        "seeds": [
            {"address": address, "canonical_rank": index}
            for index, address in enumerate(seeds, 1)
        ],
        "arms": {"incoming": {"candidates": []}, "outgoing": {"candidates": []}},
        "evaluator_only_changed_paths": ["tests/pkg/test_unrelated.py"],
    }


def _lexical() -> dict[str, Any]:
    return {
        "rankings": {
            method: []
            for method in ("canonical", "bm25_plus", "identifier", "path", "rrf")
        }
    }


def _project(
    case: dict[str, Any],
    relations: list[dict[str, str]],
    lexical: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return project_case(
        original=case,
        relations=relations,
        lexical=lexical or _lexical(),
        references={"candidates": []},
        containment={"candidates": []},
        diagnostics={
            "source_resources_examined": 0,
            "test_resources_examined": 0,
            "unmatched_source_resources": 0,
            "unmatched_named_test_resources": 0,
            "excluded_initializers": 0,
        },
    )


def test_exact_paths_and_initializer_exclusions(tmp_path: Path) -> None:
    corpus = _corpus(
        tmp_path,
        [
            "src/devtools/pkg/thing.py",
            "tests/pkg/test_thing.py",
            "src/devtools/pkg/other.py",
            "tests/other/test_other.py",
            "src/devtools/pkg/__init__.py",
            "tests/pkg/test___init__.py",
            "tests/pkg/test_orphan.py",
            "src/elsewhere/pkg/thing.py",
        ],
    )
    relations, diagnostic = derive_mirrors(corpus)
    assert [(r["source_address"], r["test_address"]) for r in relations] == [
        ("src/devtools/pkg/thing.py", "tests/pkg/test_thing.py")
    ]
    assert diagnostic["excluded_initializers"] == 1
    assert diagnostic["unmatched_source_resources"] == 1
    assert diagnostic["unmatched_named_test_resources"] == 2
    assert relations[0]["snapshot_id"] == str(corpus.snapshot.id)
    assert relations[0]["source_content_identity"]
    assert relations[0]["test_content_identity"]


def test_both_directions_seed_exclusion_and_support_retention(tmp_path: Path) -> None:
    relations, _ = derive_mirrors(
        _corpus(tmp_path, ["src/devtools/pkg/a.py", "tests/pkg/test_a.py"])
    )
    source = "src/devtools/pkg/a.py"
    test = "tests/pkg/test_a.py"
    forward = _project(
        _case([source, "s2", "s3", "s4", "s5"]), [*relations, *relations]
    )
    assert [row["address"] for row in forward["candidates"]] == [test]
    assert forward["candidates"][0]["directions"] == ["source_to_test"]
    assert forward["candidates"][0]["support_count"] == 2
    assert summarize([forward])["max_seed_fanout"] == 1
    reverse = _project(_case([test, "s2", "s3", "s4", "s5"]), relations)
    assert [row["address"] for row in reverse["candidates"]] == [source]
    assert reverse["candidates"][0]["directions"] == ["test_to_source"]
    both = _project(_case([source, test, "s3", "s4", "s5"]), relations)
    assert both["candidates"] == []


def test_saved_reach_and_changed_paths_cannot_select_candidates(tmp_path: Path) -> None:
    relations, _ = derive_mirrors(
        _corpus(tmp_path, ["src/devtools/pkg/a.py", "tests/pkg/test_a.py"])
    )
    case = _case(["src/devtools/pkg/a.py", "s2", "s3", "s4", "s5"])
    first = _project(case, relations)
    case["evaluator_only_changed_paths"] = ["tests/pkg/test_a.py"]
    assert _project(case, relations) == first
    test = "tests/pkg/test_a.py"
    lexical = _lexical()
    lexical["rankings"]["canonical"] = [{"address": test, "rank": 8}]
    candidate = _project(case, relations, lexical)["candidates"][0]
    assert candidate["saved_positive_method_ranks"]["canonical"] == 8
    assert not candidate["absent_all_saved_positive_lexical"]
    assert not candidate["existing_import_candidate"]
    assert not candidate["existing_references_calls_candidate"]
    assert not candidate["existing_containment_candidate"]
