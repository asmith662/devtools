# Copyright (c) 2026
# Case-specific deterministic freeze validation; no checkout package imports.
# ruff: noqa: ANN001, ANN201, D103, INP001, PLR2004, S101
"""Focused tests of the blind packet and judgment artifact mechanics."""

import hashlib
import json
from copy import deepcopy

import inspect_blind
import pytest
from freeze_judgments import build, coverage_primitive, serialize
from inspect_blind import BASE, BY_PATH, MANIFEST, RESOURCES, validate_packet


def test_packet_contract_and_content_digests():
    validate_packet()


def test_packet_rejects_treatment_field(monkeypatch):
    changed = deepcopy(MANIFEST)
    changed["anchors"][0]["bm25_score"] = 1
    monkeypatch.setattr(inspect_blind, "MANIFEST", changed)
    with pytest.raises(AssertionError):
        validate_packet()


def test_exact_coverage_and_independent_cell_accounting():
    artifact = build()
    expected = {
        (o["identity"], json.dumps(r["resource_identity"], sort_keys=True))
        for o in MANIFEST["obligations"]
        for r in RESOURCES
    }
    observed = [
        (c["obligation_identity"], json.dumps(c["resource_identity"], sort_keys=True))
        for c in artifact["resource_obligation_judgments"]
    ]
    assert len(observed) == 4635
    assert len(set(observed)) == len(observed)
    assert set(observed) == expected
    assert artifact["summary"]["identity_coverage"] == {
        "duplicate_expected": (),
        "duplicate_observed": (),
        "missing": (),
        "unexpected": (),
    }


def test_frozen_evaluation_primitive_reports_all_diagnostics():
    result = coverage_primitive()(expected=("a", "a", "b"), observed=("a", "a", "c"))
    assert result.duplicate_expected == ("a",)
    assert result.duplicate_observed == ("a",)
    assert result.missing == ("b",)
    assert result.unexpected == ("c",)
    assert not result.is_exact


def test_witness_targets_reviews_and_applicability():
    artifact = build()
    units = {u["identity"]: u for u in artifact["information_units"]}
    assert len(units) == len(artifact["information_units"])
    for unit in units.values():
        resource = BY_PATH[unit["resource_identity"]["address"]]
        assert unit["resource_identity"] == resource["resource_identity"]
        lines = resource["content"].splitlines()
        selected = "\n".join(
            "\n".join(lines[start - 1 : end])
            for start, end in unit["line_spans_inclusive"]
        )
        assert (
            hashlib.sha256(selected.encode()).hexdigest()
            == (unit["selected_text_sha256"])
        )
    for obligation in artifact["obligations"]:
        assert obligation["applicability"] == "APPLICABLE"
        assert obligation["applicability_rationale"].strip()
        judgments = obligation["information_unit_judgments"]
        required = {j["unit_identity"] for j in judgments}
        alternatives = obligation["acceptable_witness_alternatives"]
        assert set().union(*(set(a["all_members"]) for a in alternatives)) == required
        assert required <= set(units)
        for judgment in judgments:
            assert judgment["judgment"] == "REQUIRED"
            assert judgment["inferability"] == "INFERABLE_AT_START"
            assert judgment["inherent_discovery"] is None
            assert all(judgment["required_review"].values())
    assert artifact["task_interpretation_gaps"]["findings"] == []
    assert artifact["summary"]["inherent_discovery_count"] == 0


def test_serialization_replay_and_frozen_digest():
    expected = serialize(build())
    assert serialize(build()) == expected
    assert serialize(json.loads(expected)) == expected
    assert (BASE / "judgments.json").read_bytes() == expected
    digest = hashlib.sha256(expected).hexdigest()
    assert (BASE / "judgments.sha256").read_text().strip() == (
        digest + "  judgments.json"
    )


def test_artifact_contains_no_treatment_fields():
    forbidden = {
        "lexical_queries",
        "query_identity",
        "query_text",
        "preferred_roles",
        "caller_role_preferences",
        "role_assignments",
        "role_support_records",
        "routing_tier",
        "routed_position",
        "native_rank",
        "bm25_rank",
        "score",
        "bm25_score",
        "retrieved",
        "candidate_count",
        "acquisition_runtime",
        "routing_runtime",
        "retrieval_results",
        "routing_results",
    }
    pending = [build()]
    while pending:
        value = pending.pop()
        if isinstance(value, dict):
            assert not forbidden.intersection(value)
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)
