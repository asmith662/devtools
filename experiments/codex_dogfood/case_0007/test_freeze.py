# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, PLC0415, S101
"""Stage A integrity and malformed-input checks, with treatment tripwires."""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

from experiments.codex_dogfood.case_0007 import freeze, treatment


def forbidden(*_args: object, **_kwargs: object) -> None:
    pytest.fail("Stage A attempted a forbidden treatment operation")


def test_stage_a_validation_never_executes_treatment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from devtools.context.localization import lexical
    from devtools.context.localization.generation import generate
    from devtools.context.localization.grounding import resolve
    from devtools.context.localization.routing import derive
    from devtools.context.retrieval.lexical import bm25

    monkeypatch.setattr(lexical, "acquire_localization_lexical_evidence", forbidden)
    monkeypatch.setattr(bm25, "retrieve_repository_text_documents_by_bm25", forbidden)
    monkeypatch.setattr(resolve, "ground_task_anchor", forbidden)
    monkeypatch.setattr(generate, "generate_witness_hypotheses", forbidden)
    monkeypatch.setattr(derive, "route_localization_lexical_evidence", forbidden)
    assert freeze.validate()["treatment_operations_executed"] is False


@pytest.mark.parametrize(
    "address",
    [
        "experiments/codex_dogfood/case_0006/inputs.pkl.gz",
        "tests/experiments/test_probe.py",
        "confirmation/outcomes.json",
        ".local/task.py",
        "docs/research/historical.md",
        "src/binary.png",
    ],
)
def test_ineligible_addresses(address: str) -> None:
    assert not freeze.eligible(address)


@pytest.mark.parametrize(
    "address",
    [
        "src/pkg/module.py",
        "tests/context/test_contract.py",
        "docs/architecture.md",
        "README.md",
        "pyproject.toml",
        "scripts/validate_development.py",
    ],
)
def test_eligible_addresses(address: str) -> None:
    assert freeze.eligible(address)


def test_invalid_recipe_multiplicity_rejected() -> None:
    spec = copy.deepcopy(
        next(
            item
            for item in treatment.recipe_specs()
            if item["identity_kind"] == "family"
        ),
    )
    extra = copy.deepcopy(spec["members"][-1])
    extra["key"] = "second-branch"
    spec["members"].append(extra)
    with pytest.raises(ValueError, match="multiplicity"):
        freeze.validate_specs([spec], treatment.GROUNDINGS)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("max_results", 0),
        ("work_limit", -1),
        ("grounding_request", "absent"),
        ("operator", "OWNER_RESOURCE"),
    ],
)
def test_invalid_branch_spec_rejected(field: str, value: object) -> None:
    spec = copy.deepcopy(
        next(
            item
            for item in treatment.recipe_specs()
            if item["identity_kind"] == "family"
        ),
    )
    spec["members"][-1][field] = value
    with pytest.raises(ValueError, match="invalid"):
        freeze.validate_specs([spec], treatment.GROUNDINGS)


def test_exact_task_and_unaccepted_witnesses() -> None:
    assert len(treatment.TASK) == 1243
    task = treatment.interpretation()
    assert all(not item.witness_alternatives for item in task.obligations)
    queries, preferences = treatment.lexical_inputs()
    assert len(queries) == len(preferences) == 11
    assert treatment.PURPOSE != treatment.TASK


def test_identity_collision_rejected() -> None:
    spec = treatment.recipe_specs()[0]
    with pytest.raises(ValueError, match="identity"):
        freeze.validate_specs([spec, spec], treatment.GROUNDINGS)


def test_reference_module_seed_rejected() -> None:
    spec = copy.deepcopy(
        next(
            item
            for item in treatment.recipe_specs()
            if item["identity_kind"] == "family"
        ),
    )
    spec["members"][-1]["grounding_request"] = "g-python-api"
    with pytest.raises(ValueError, match="declaration locator"):
        freeze.validate_specs([spec], treatment.GROUNDINGS)


def test_integrity_tampering_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in (*freeze.ARTIFACTS, "integrity.json"):
        (tmp_path / name).write_bytes((freeze.CASE / name).read_bytes())
    (tmp_path / "treatment.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(freeze, "CASE", tmp_path)
    with pytest.raises(ValueError, match="integrity mismatch"):
        freeze.validate()
