# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, D103, INP001, PLR2004, S101
"""Stage A schema, native-preparation firewall and immutable freeze checks."""

from __future__ import annotations

import asyncio
import copy
import importlib.util
import json
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "case0008_freeze",
    Path(__file__).with_name("freeze.py"),
)
assert _SPEC is not None
assert _SPEC.loader is not None
freeze = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(freeze)


def treatment():
    return json.loads(freeze.binary(Path(__file__).with_name("treatment.json")))


def test_exact_task_empty_gold_and_all_four_operator_shapes():
    data = treatment()
    task, queries, preferences, locators = freeze.contracts(data)
    assert data["task_full_prompt"] == freeze.TASK
    assert len(task.anchors) == 11
    assert len(task.obligations) == 13
    assert len(queries) == len(preferences) == 13
    assert len(locators) == 11
    assert all(not item.witness_alternatives for item in task.obligations)
    assert {
        member["projection"]
        for recipe in data["recipes"]
        for member in recipe["members"]
    } == set(data["operators"])
    assert sum(recipe["kind"] == "family" for recipe in data["recipes"]) == 14
    assert sum(recipe["kind"] == "fixed" for recipe in data["recipes"]) == 15


@pytest.mark.parametrize(
    "alteration",
    [
        "task",
        "gold",
        "double-branch",
        "fixed-reference",
        "unknown-operator",
        "unlinked-anchor",
        "bound",
        "unsupported-locator",
        "no-recipe",
        "roles",
        "preference",
        "query-duplicate",
        "resource-reference",
    ],
)
def test_rejects_invalid_treatment(alteration):  # noqa: C901, PLR0912
    data = copy.deepcopy(treatment())
    family = next(item for item in data["recipes"] if item["kind"] == "family")
    branch = next(
        item for item in family["members"] if item["multiplicity"] == "branching"
    )
    if alteration == "task":
        data["task_full_prompt"] += " rewritten"
    elif alteration == "gold":
        data["obligations"][0]["witness_alternatives"] = [["invented-gold"]]
    elif alteration == "double-branch":
        family["members"].append({**branch, "key": "second-branch"})
    elif alteration == "fixed-reference":
        branch["multiplicity"] = "fixed"
    elif alteration == "unknown-operator":
        branch["projection"] = "GRAPH_NEIGHBOR"
    elif alteration == "unlinked-anchor":
        branch["grounding"] = "g-package"
    elif alteration == "bound":
        branch["max_results"] = 0
    elif alteration == "unsupported-locator":
        data["grounding_specs"][0]["locator"]["kind"] = "text-search"
    elif alteration == "no-recipe":
        data["no_recipe_obligations"] = []
    elif alteration == "roles":
        data["role_preferences"][0]["roles"] = ["NEW_ROLE"]
    elif alteration == "preference":
        data["role_preferences"][0]["obligation"] = "tests"
    elif alteration == "query-duplicate":
        data["queries"].append(data["queries"][0])
    else:
        spec = next(
            item
            for item in data["grounding_specs"]
            if item["id"] == branch["grounding"]
        )
        spec["locator"] = {
            "kind": "module",
            "module": "devtools.context.localization",
            "module_kind": "PACKAGE",
        }
    with pytest.raises((ValueError, KeyError)):
        freeze.contracts(data)


@pytest.mark.parametrize(
    ("module", "operation"),
    [
        ("devtools.context.localization", "acquire_localization_lexical_evidence"),
        (
            "devtools.context.retrieval.lexical.bm25",
            "retrieve_repository_text_documents_by_content_bm25",
        ),
        (
            "devtools.context.localization.routing",
            "route_localization_lexical_evidence",
        ),
        ("devtools.context.localization.grounding", "ground_task_anchor"),
        ("devtools.context.localization.generation", "generate_witness_hypotheses"),
        ("devtools.context.localization.association.structural", "owner_resource"),
        ("devtools.context.localization.generation.generate", "_project"),
        (
            "devtools.context.localization.generation.references",
            "project_referencing_resources",
        ),
        (
            "devtools.context.localization.generation.imports",
            "project_direct_import_dependencies",
        ),
    ],
)
def test_forbidden_operation_tripwires(module, operation):
    api = importlib.import_module(module)
    original = getattr(api, operation)
    with freeze.stage_a_guard() as attempts:
        with pytest.raises(RuntimeError, match="Stage A forbids"):
            getattr(api, operation)()
        assert attempts[operation] == 1
    assert getattr(api, operation) is original


def test_generic_native_preparation_without_any_treatment(tmp_path):
    contents = {
        "src/sample/__init__.py": "from .model import Value\n",
        "src/sample/model.py": "class Value: pass\n",
        "pyproject.toml": '[project]\nname="synthetic"\nversion="0.1.0"\n',
    }
    for name, content in contents.items():
        freeze.put_text(tmp_path / name, content)
    discovery = freeze.discover_repository_resource_addresses(
        repository=freeze.REPOSITORY,
        root=freeze.resolve_path(tmp_path),
        maximum_resource_count=10,
        maximum_traversal_entry_count=20,
    )
    selected = tuple(
        freeze.RepositoryResourceAddress(name) for name in sorted(contents)
    )
    snapshot = freeze.observe_repository_resources(
        repository=freeze.REPOSITORY,
        root=freeze.resolve_path(tmp_path),
        addresses=selected,
        maximum_resource_bytes=4096,
    )
    corpus = freeze.realize_repository_text_corpus(
        definition=freeze.define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=selected,
        ),
        snapshot=snapshot,
    )
    with freeze.stage_a_guard() as attempts:
        native = freeze.prepare_native(snapshot, corpus, treatment())
        freeze.validate_reference_frame(native["python_references"], snapshot)
        freeze.validate_import_dependency_frame(
            native["python_import_dependencies"],
            snapshot,
        )
        assert not any(attempts.values())
    assert len(native["python_references"].sources) == 2
    assert len(native["python_import_dependencies"].sources) == 2
    assert len(native["grounding_requests"]) == 11
    assert native["request"].full_task_query == freeze.TASK
    assert native["request"].maximum_results == 3
    assert "grounding_outcomes" not in native
    assert "generated" not in native


@pytest.mark.parametrize(
    "path",
    [
        "experiments/codex_dogfood/case_0007/adjudication/judgments.json",
        "tests/experiments/outcome.py",
        "docs/research/historical.md",
        "docs/reports/report.md",
        "docs/implementation_ledger.md",
        "tests/confirmation/results.md",
        ".local/file.md",
        "assets/binary.png",
    ],
)
def test_excluded_frames_never_exported(path):
    assert not freeze.eligible(path)


@pytest.mark.parametrize(
    "path",
    [
        "AGENTS.md",
        "README.md",
        "pyproject.toml",
        "scripts/validate_development.py",
        "src/devtools/context/localization/task.py",
        "tests/context/localization/test_kernel.py",
        "docs/architecture/taxonomy.md",
    ],
)
def test_broad_frame_includes_code_tests_and_policy(path):
    assert freeze.eligible(path)


def test_freeze_refuses_overwrite_before_git_or_treatment(tmp_path, monkeypatch):
    freeze.put_text(tmp_path / "pre_execution.json", "{}")
    monkeypatch.setattr(freeze, "CASE", tmp_path)
    with pytest.raises(FileExistsError, match="already frozen"):
        asyncio.run(freeze.freeze())


def test_stage_b_marker_rejected_without_loading_native_archive(tmp_path, monkeypatch):
    freeze.put_text(tmp_path / "execution_started.json", "{}")
    monkeypatch.setattr(freeze, "CASE", tmp_path)
    with pytest.raises(ValueError, match="Stage B/later"):
        freeze.validate()


def test_atomic_text_write_refuses_overwrite(tmp_path):
    path = tmp_path / "artifact.json"
    freeze.put_text(path, "{}")
    with pytest.raises(FileExistsError):
        freeze.put_text(path, "changed")


def test_artifact_digest_drift_rejected_before_pickle(tmp_path, monkeypatch):
    monkeypatch.setattr(freeze, "CASE", tmp_path)
    hashes = dict.fromkeys(freeze.ARTIFACTS, "0" * 64)
    freeze.put_text(
        tmp_path / "integrity.json",
        freeze.json_bytes({"sha256": hashes}).decode(),
    )
    freeze.put_text(tmp_path / "treatment.json", "{}")
    freeze.put_text(tmp_path / "README.md", "digest drift")
    with pytest.raises(ValueError, match="Frozen artifact digest differs"):
        freeze.validate()


def test_readme_relative_links_exist():
    import re  # noqa: PLC0415

    readme = Path(__file__).with_name("README.md").read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)]+)\)", readme):
        assert (Path(__file__).parent / target.split("#", 1)[0]).exists()
