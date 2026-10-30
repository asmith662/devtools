# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, ANN202, D103, INP001, S101, C408
# Dynamic experimental assertions; not an installable or maintained API.
"""Supervisor-only empirical oracle cross-checks, never disclosed to the worker."""

import json

import pytest

from devtools.agents.coding import navigation
from experiments.delegated_b0035 import focused, heldout


def reference(scope, editable, maximum_bytes):
    """Independent acceptance control, not a proposed production implementation."""
    if type(maximum_bytes) is not int or maximum_bytes < 1:
        message = "invalid bound"
        raise ValueError(message)
    scope.check_current()
    records = {str(r.address): r for r in scope.snapshot.resources}
    if {str(a) for a in editable} - records.keys():
        message = "foreign editability"
        raise ValueError(message)
    rows = []
    for name in sorted(records):
        occurrence = records[name]
        # Cross-check the independently observed byte count against encoded text.
        assert occurrence.byte_size == len(occurrence.content.encode("utf-8"))
        rows.append(
            dict(
                address=name,
                content_identity=str(occurrence.content_identity),
                byte_size=occurrence.byte_size,
                editable=occurrence.address in editable,
            ),
        )
    value = dict(
        repository_id=str(scope.snapshot.repository_id),
        snapshot_id=str(scope.snapshot.id),
        source_acquired=False,
        complete_inventory=True,
        resources=rows,
    )
    if len(json.dumps(value, ensure_ascii=False).encode("utf-8")) > maximum_bytes:
        message = "complete inventory exceeds budget"
        raise ValueError(message)
    return value


@pytest.mark.parametrize(
    "case",
    [
        focused.test_complete_metadata,
        focused.test_empty_scope,
        focused.test_budget_and_foreign_editability,
        focused.test_stale_scope_refused,
        heldout.test_many_complete_resources_and_utf8,
        heldout.test_updated_observation_changes_identity,
        heldout.test_canonical_order_not_input_order,
    ],
)
def test_positive_controls(monkeypatch, tmp_path, case):
    monkeypatch.setattr(navigation, "complete_inventory", reference, raising=False)
    case(tmp_path)


@pytest.mark.parametrize("fault", ["subset", "characters", "permission", "source"])
def test_public_oracle_rejects_wrong_payload(monkeypatch, tmp_path, fault):
    def corrupted(scope, editable, maximum_bytes):
        value = reference(scope, editable, maximum_bytes)
        if fault == "subset":
            value["resources"].pop()
        elif fault == "characters":
            value["resources"][0]["byte_size"] = 2
        elif fault == "permission":
            value["resources"][0]["editable"] = True
        else:
            value["leaked"] = "secret-source"
        return value

    monkeypatch.setattr(navigation, "complete_inventory", corrupted, raising=False)
    with pytest.raises(AssertionError):
        focused.test_complete_metadata(tmp_path)
