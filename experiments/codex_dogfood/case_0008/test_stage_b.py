# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, ANN202, ARG005, D103, EM101, INP001, PLR2004, S101, S301, TRY003
"""Focused durable execution-state tests without treatment operations."""

from __future__ import annotations

import copy
import gzip
import importlib.util
import json
import pickle
from pathlib import Path
from types import SimpleNamespace

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "case0008_stage_b",
    Path(__file__).with_name("stage_b.py"),
)
assert _SPEC is not None
assert _SPEC.loader is not None
stage_b = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(stage_b)


def state():
    names = ("lexical", "routing", "generation")
    return {
        "execution_id": "test-run",
        "stage": "NOT_STARTED",
        "operations": {
            name: {"state": "NOT_STARTED", "invocations": 0} for name in names
        },
        "results": {},
    }


def test_checkpoint_captures_return_and_refuses_second_invocation(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(stage_b, "RAW", tmp_path / "raw.pkl.gz")
    current = state()
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        return {"native": "result"}

    stage_b.run_operation(current, "lexical", operation)
    stage_b.run_operation(current, "lexical", operation)
    assert calls == 1
    assert current["operations"]["lexical"]["invocations"] == 1
    stored = pickle.loads(gzip.decompress(stage_b.freeze.binary(stage_b.RAW)))
    assert stored["results"]["lexical"] == {"native": "result"}


def test_ambiguous_in_progress_state_is_never_retried(tmp_path, monkeypatch):
    monkeypatch.setattr(stage_b, "RAW", tmp_path / "raw.pkl.gz")
    current = state()
    current["operations"]["routing"]["state"] = "IN_PROGRESS"
    with pytest.raises(RuntimeError, match="ambiguous"):
        stage_b.run_operation(
            current,
            "routing",
            lambda: pytest.fail("must not execute"),
        )


def test_alias_preflight_accepts_only_exact_shared_role_evidence():
    class Routing:
        pass

    class Acquisition:
        full_task_retrieval = object()

    routing = Routing()
    routing.acquisition = Acquisition()
    routing.role_evidence = object()
    routing.global_retrieval = routing.acquisition.full_task_retrieval

    plan = SimpleNamespace(
        acquisition=routing.acquisition,
        role_evidence=routing.role_evidence,
        routing=routing,
    )
    stage_b.validate_plan_aliases(plan, routing)
    forged = copy.copy(plan)
    forged.role_evidence = copy.deepcopy(routing.role_evidence)
    with pytest.raises(ValueError, match="aliases"):
        stage_b.validate_plan_aliases(forged, routing)


def test_recovery_result_is_persisted_before_validation_and_never_retried(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(stage_b, "RECOVERY_RAW", tmp_path / "recovery.pkl.gz")
    monkeypatch.setattr(stage_b, "validate_recovery_checkpoint", lambda state: None)
    current = {
        "generation_state": "NOT_STARTED",
        "generation_invocations": 0,
        "generation_result": None,
        "history": [],
        "plan": object(),
    }
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        return {"native": "view"}

    def validate(result):
        saved = pickle.loads(
            gzip.decompress(stage_b.RECOVERY_RAW.read_bytes()),
        )
        assert saved["generation_state"] == ("GENERATION_RETURN_CAPTURED_UNVALIDATED")
        assert saved["generation_result"] is not None
        assert result == saved["generation_result"]

    stage_b.record_recovery_generation(current, operation, validate)
    with pytest.raises(RuntimeError, match="allowance is exhausted"):
        stage_b.record_recovery_generation(current, operation, validate)
    assert calls == 1


def test_failed_recovery_call_is_recorded_and_cannot_be_reentered(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(stage_b, "RECOVERY_RAW", tmp_path / "failed.pkl.gz")
    monkeypatch.setattr(stage_b, "validate_recovery_checkpoint", lambda state: None)
    current = {
        "generation_state": "NOT_STARTED",
        "generation_invocations": 0,
        "generation_attempted_calls": 0,
        "history": [],
    }
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        raise ValueError("synthetic generation failure")

    with pytest.raises(ValueError, match="synthetic generation failure"):
        stage_b.record_recovery_generation(current, operation, lambda _: None)
    saved = pickle.loads(gzip.decompress(stage_b.RECOVERY_RAW.read_bytes()))
    assert saved["generation_state"] == "GENERATION_RECOVERY_FAILED"
    assert saved["stage"] == "CAPTURE_FAILED"
    assert saved["generation_attempted_calls"] == 1
    assert saved["generation_error"]["type"] == "ValueError"
    with pytest.raises(RuntimeError, match="allowance is exhausted"):
        stage_b.record_recovery_generation(current, operation, lambda _: None)
    assert calls == 1


def test_recovery_state_preserves_attempt_and_recovery_identity(tmp_path, monkeypatch):
    monkeypatch.setattr(stage_b, "RECOVERY_RAW", tmp_path / "recovery.pkl.gz")
    attempt = {"execution_id": stage_b.ORIGINAL_EXECUTION_ID}
    state = stage_b.initial_recovery_state(attempt, plan=object())
    assert state["history"][0]["state"] == (
        "GENERATION_ATTEMPT_1_FAILED_BEFORE_PROJECTION"
    )
    assert state["recovery_id"] == stage_b.RECOVERY_ID
    assert state["prior_generation_attempts"] == 1
    assert state["generation_invocations"] == 0


def test_captured_recovery_plan_preserves_required_aliases_and_frozen_recipe_shape():
    case = Path(__file__).parent
    raw, _ = stage_b.validate_partial_checkpoint(allow_canonical=True)
    native = pickle.loads(gzip.decompress((case / "inputs.pkl.gz").read_bytes()))
    treatment = json.loads((case / "treatment.json").read_bytes())
    plan = stage_b.make_recovery_plan(raw, native, treatment)
    assert plan.routing is raw["results"]["routing"]
    assert plan.role_evidence is plan.routing.role_evidence
    assert plan.acquisition is plan.routing.acquisition
    assert plan.routing.global_retrieval is plan.acquisition.full_task_retrieval
    assert len(plan.recipes) == 29
    assert sum(len(item.members) for item in plan.recipes) == 44
    assert (
        sum(
            item.projection.name == "OWNER_RESOURCE"
            for recipe in plan.recipes
            for item in recipe.members
        )
        == 23
    )
    assert (
        sum(
            item.projection.name == "MIRRORED_RESOURCE"
            for recipe in plan.recipes
            for item in recipe.members
        )
        == 7
    )
    assert (
        sum(
            item.projection.name == "REFERENCING_RESOURCE"
            for recipe in plan.recipes
            for item in recipe.members
        )
        == 8
    )
    assert (
        sum(
            item.projection.name == "DIRECT_IMPORT_DEPENDENCY_RESOURCE"
            for recipe in plan.recipes
            for item in recipe.members
        )
        == 6
    )


def test_frozen_attempt_and_recovery_authorization_are_consistent():
    case = Path(__file__).parent
    attempt = json.loads((case / "stage_b_attempt_1.json").read_text())
    authorization = json.loads((case / "recovery_authorization.json").read_text())
    assert attempt["generation_attempt"]["combined_api_attempted"] == 1
    assert not attempt["generation_attempt"]["returned_successfully"]
    assert authorization["recovery_id"] == stage_b.RECOVERY_ID
    assert authorization["allowance"] == {
        "additional_lexical_executions": 0,
        "additional_routing_executions": 0,
        "additional_grounding_executions": 0,
        "additional_combined_generation_api_executions": 1,
        "other_treatment_operations": 0,
    }
