# Copyright (c) 2026
# ruff: noqa: D103, E501
# mypy: disable-error-code=index
"""Integrity tests for Increment-26's outcome-free protocol freeze."""

from __future__ import annotations

import json
from pathlib import Path

from experiments.increment_26 import configuration

_I25_FREEZE = Path("experiments/increment_25/task_population_freeze.json")
_I26_FREEZE = Path("experiments/increment_26/experiment_freeze.json")


def test_increment_25_population_and_partitions_are_reused_exactly() -> None:
    increment_25 = json.loads(_I25_FREEZE.read_text(encoding="utf-8"))
    increment_26 = configuration.build_freeze(increment_25_freeze_path=_I25_FREEZE)
    expected = increment_25["payload"]["split"]
    actual = increment_26["payload"]["population"]
    assert actual["increment_25_freeze_identity"] == increment_25["content_identity"]
    assert actual["development_case_ids"] == expected["development_case_ids"]
    assert actual["confirmation_case_ids"] == expected["confirmation_case_ids"]
    assert actual["reserve_case_ids"] == expected["reserve_case_ids"]


def test_query_and_representation_boundaries_are_frozen() -> None:
    freeze = configuration.build_freeze(increment_25_freeze_path=_I25_FREEZE)
    representation = freeze["payload"]["representation"]
    query = representation["query"]
    document = representation["document"]
    assert query["source"] == "task-card.lexical_query exactly"
    assert "information_need_purpose" not in query["serialization"]
    assert "no filename" in document["serialization"]
    assert "changed-path metadata" in document["serialization"]
    assert representation["unit_boundary"].startswith("Chunks are experiment-local")


def test_capacity_is_independent_matched_and_nonstructural() -> None:
    freeze = configuration.build_freeze(increment_25_freeze_path=_I25_FREEZE)
    arms = freeze["payload"]["arms"]
    assert arms["capacity"]["n"] == "min(5, available semantic resources, available positive lexical resources)"
    assert arms["capacity"]["shared_lexical_seed"] is False
    assert arms["structural"].startswith("not an Increment-26 candidate input")


def test_judgment_reuse_requires_need_snapshot_resource_and_semantics() -> None:
    freeze = configuration.build_freeze(increment_25_freeze_path=_I25_FREEZE)
    rule = freeze["payload"]["judgment_reuse"]["rule"]
    assert "InformationNeed identity" in rule
    assert "parent snapshot identity" in rule
    assert "repository resource address" in rule
    assert "usefulness semantics" in rule


def test_serialization_is_deterministic_and_contains_no_outcomes() -> None:
    first = configuration.build_freeze(increment_25_freeze_path=_I25_FREEZE)
    second = configuration.build_freeze(increment_25_freeze_path=_I25_FREEZE)
    assert first == second
    assert configuration.validate_freeze(first)
    assert first["payload"]["protocol"]["outcomes_generated"] is False
    assert first["payload"]["protocol"]["usefulness_adjudication_started"] is False


def test_committed_freeze_is_valid_and_contains_no_semantic_results() -> None:
    freeze = json.loads(_I26_FREEZE.read_text(encoding="utf-8"))
    assert configuration.validate_freeze(freeze)
    rendered = json.dumps(freeze, sort_keys=True)
    assert '"embeddings"' not in rendered
    assert '"semantic_candidates"' not in rendered
    assert '"semantic_results"' not in rendered


def test_configuration_never_imports_or_executes_an_encoder() -> None:
    source = Path("experiments/increment_26/configuration.py").read_text(encoding="utf-8")
    assert "import transformers" not in source
    assert "import torch" not in source
    assert "AutoModel" not in source
    assert "SentenceTransformer" not in source
