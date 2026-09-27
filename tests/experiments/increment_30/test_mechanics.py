# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""One-edge relation and outcome-blind candidate projection tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from devtools.context.python.modules import (
    PythonModuleRoot,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath
from experiments.increment_30.mechanics import (
    derive_immediate_relations,
    project_case,
    summarize,
)

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.python.modules import PythonModuleInterpretation


def _interpret(
    tmp_path: Path, resources: dict[str, str], root: str
) -> list[PythonModuleInterpretation]:
    for address, content in resources.items():
        path = tmp_path / address
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000030")
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in resources),
        maximum_resource_bytes=1024 * 1024,
    )
    return list(
        interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot(root),
            resource_addresses=tuple(
                RepositoryResourceAddress(address) for address in resources
            ),
        ).interpretations
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
        "arms": {"outgoing": {"candidates": []}, "incoming": {"candidates": []}},
    }


def _lexical() -> dict[str, Any]:
    return {
        "rankings": {
            name: [] for name in ("canonical", "bm25_plus", "identifier", "path", "rrf")
        }
    }


def test_immediate_membership_and_no_recursive_or_cross_root(tmp_path: Path) -> None:
    resources = {
        "src/pkg/__init__.py": "",
        "src/pkg/a.py": "",
        "src/pkg/b.py": "",
        "src/pkg/nested/__init__.py": "",
        "src/pkg/nested/deep.py": "",
        "src/no_parent/c.py": "",
        "tests/pkg/other.py": "",
    }
    src = _interpret(tmp_path, resources, "src")
    tests = _interpret(tmp_path, resources, "tests")
    relations, statuses = derive_immediate_relations([*src, *tests])
    edges = {(row["package_address"], row["child_address"]) for row in relations}
    assert edges == {
        ("src/pkg/__init__.py", "src/pkg/a.py"),
        ("src/pkg/__init__.py", "src/pkg/b.py"),
        ("src/pkg/__init__.py", "src/pkg/nested/__init__.py"),
        ("src/pkg/nested/__init__.py", "src/pkg/nested/deep.py"),
    }
    assert statuses["missing_observed_immediate_package"] >= 2
    assert all(row["module_root"] == "src" for row in relations)


def test_ambiguous_parent_does_not_assert_relation(tmp_path: Path) -> None:
    interpretations = _interpret(
        tmp_path, {"src/pkg/__init__.py": "", "src/pkg/a.py": ""}, "src"
    )
    package, child = interpretations
    relations, statuses = derive_immediate_relations([package, package, child])
    assert relations == []
    assert statuses["ambiguous_immediate_package"] == 1


def test_parent_from_another_snapshot_does_not_assert_relation(tmp_path: Path) -> None:
    package = _interpret(tmp_path, {"src/pkg/__init__.py": ""}, "src")[0]
    child = _interpret(tmp_path, {"src/pkg/a.py": "changed"}, "src")[0]
    assert package.snapshot_id != child.snapshot_id
    relations, statuses = derive_immediate_relations([package, child])
    assert relations == []
    assert statuses["missing_observed_immediate_package"] == 1


def test_forward_reverse_seed_exclusion_and_supports(tmp_path: Path) -> None:
    resources = {
        "src/pkg/__init__.py": "",
        "src/pkg/a.py": "",
        "src/pkg/b.py": "",
    }
    relations, _ = derive_immediate_relations(_interpret(tmp_path, resources, "src"))
    case = _case(["src/pkg/__init__.py", "other1", "other2", "other3", "other4"])
    projected = project_case(
        case=case,
        relations=relations,
        lexical=_lexical(),
        references={"candidates": []},
        diagnostics={
            "resources_examined": len(resources),
            "interpreted_resources": len(resources),
            "relation_statuses": {},
            "interpretation_exclusions": {},
        },
    )
    assert {row["address"] for row in projected["candidates"]} == {
        "src/pkg/a.py",
        "src/pkg/b.py",
    }
    assert all(
        row["directions"] == ["package_to_child"] for row in projected["candidates"]
    )
    assert all(row["absent_existing_evidence_union"] for row in projected["candidates"])
    assert summarize([projected])["candidate_pairs"] == 2

    child_seed = _case(["src/pkg/a.py", "other1", "other2", "other3", "other4"])
    forward = project_case(
        case=child_seed,
        relations=[*relations, relations[0]],
        lexical=_lexical(),
        references={"candidates": []},
        diagnostics={},
    )
    assert [row["address"] for row in forward["candidates"]] == ["src/pkg/__init__.py"]
    assert forward["candidates"][0]["directions"] == ["child_to_package"]
    assert forward["candidates"][0]["support_count"] == 2
    assert {row["seed_address"] for row in forward["candidates"][0]["supports"]} == {
        "src/pkg/a.py"
    }
    assert "src/pkg/b.py" not in {row["address"] for row in forward["candidates"]}

    both_seeds = _case(
        ["src/pkg/a.py", "src/pkg/__init__.py", "other2", "other3", "other4"]
    )
    excluded = project_case(
        case=both_seeds,
        relations=relations,
        lexical=_lexical(),
        references={"candidates": []},
        diagnostics={},
    )
    assert {row["address"] for row in excluded["candidates"]} == {"src/pkg/b.py"}


def test_saved_evidence_escape_classification(tmp_path: Path) -> None:
    relations, _ = derive_immediate_relations(
        _interpret(
            tmp_path,
            {"src/pkg/__init__.py": "", "src/pkg/a.py": ""},
            "src",
        )
    )
    case = _case(["src/pkg/__init__.py", "other1", "other2", "other3", "other4"])
    lexical = _lexical()
    lexical["rankings"]["canonical"] = [{"address": "src/pkg/a.py", "rank": 7}]
    case["arms"]["incoming"]["candidates"] = [{"address": "src/pkg/a.py"}]
    projected = project_case(
        case=case,
        relations=relations,
        lexical=lexical,
        references={"candidates": [{"address": "src/pkg/a.py"}]},
        diagnostics={},
    )
    candidate = projected["candidates"][0]
    assert candidate["canonical_positive_rank"] == 7
    assert not candidate["absent_all_saved_positive_lexical"]
    assert candidate["existing_import_candidate"]
    assert candidate["existing_references_calls_candidate"]
    assert not candidate["absent_existing_evidence_union"]
