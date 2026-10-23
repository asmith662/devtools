# Copyright (c) 2026
# ruff: noqa: D103 -- independent synthetic binding counterexamples
"""No original ranking, adjudication or repository acquisition runs here."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from typing import Any

import pytest

from devtools.context.repository.resource import RepositoryResourceAddress as Address
from experiments.purpose_relative_admission.validation_adjudication import (
    freeze_adjudication_set,
    unblind_records,
)
from experiments.purpose_relative_admission.validation_execution import (
    _digest,
    artifact_envelope,
    frozen_adjudication_artifact,
    validate_artifact_correspondence,
)
from experiments.purpose_relative_admission.verification_v1 import (
    verified_unblind_records,
    verify_artifact_bindings,
)
from experiments.purpose_relative_import.cases import UsefulnessJudgment as J
from tests.experiments.purpose_relative_admission.test_validation_mechanics import (
    _capture,
    _frozen,
)


def _inputs() -> dict[str, dict[str, Any]]:
    """Use the original producer on an explicitly synthetic six-resource frame."""
    c = _capture()
    p, bindings, f = _frozen(
        c,
        {Address("l1.py"): J.USEFUL, Address("l2.py"): J.NOT_USEFUL},
    )
    cp = {
        "design_fingerprint": c.design_fingerprint,
        "rule_fingerprint": "synthetic-rule",
        "repository_checkpoint": {"checkpoint": c.checkpoint},
        "case_capture_identities": [c.identity()],
        "cases": [c],
        "direct_resolution_controls": [],
    }
    cid = _digest(
        {
            "design_fingerprint": c.design_fingerprint,
            "rule_fingerprint": "synthetic-rule",
            "checkpoint": c.checkpoint,
            "case_capture_identities": [c.identity()],
            "direct_controls": [],
        },
    )
    cp["capture_set_identity"] = cid
    pid = _digest({"capture_set_identity": cid, "packages": [p]})
    package = artifact_envelope(
        schema="devtools-b0002-increment-23-blinded-adjudication-package-v2",
        payload={
            "capture_set_identity": cid,
            "design_fingerprint": c.design_fingerprint,
            "package_set_identity": pid,
            "packages": [p],
        },
    )
    frozen = frozen_adjudication_artifact(
        freeze_adjudication_set(
            packages=(p,),
            records_by_case={p.case_name: f.records},
            package_set_identity=pid,
        ),
    )
    return {
        "capture": artifact_envelope(
            schema="devtools-b0002-increment-23-hidden-surface-capture-v1",
            payload=cp,
        ),
        "package": package,
        "mapping": artifact_envelope(
            schema="devtools-b0002-increment-23-neutral-resource-mapping-v1",
            payload={
                "capture_set_identity": cid,
                "design_fingerprint": c.design_fingerprint,
                "case_capture_identities": [c.identity()],
                "mappings": [bindings],
                "mapping_set_identity": _digest(
                    {"capture_set_identity": cid, "mappings": [bindings]},
                ),
            },
        ),
        "frozen": frozen,
    }


def _reseal(value: dict[str, Any]) -> None:
    value["content_identity"] = _digest(value["payload"])


def test_original_weakness_is_rejected_without_rewriting_frozen_owner() -> None:
    c = _capture()
    p, bindings, f = _frozen(
        c,
        {Address("l1.py"): J.USEFUL, Address("l2.py"): J.NOT_USEFUL},
    )
    swapped = (
        replace(bindings[0], address=bindings[1].address),
        replace(bindings[1], address=bindings[0].address),
        *bindings[2:],
    )
    old = unblind_records(package=p, capture=c, frozen=f, mappings=swapped)
    assert old.by_address()[Address("l2.py")].judgment is J.USEFUL
    assert old.frozen_fingerprint == f.fingerprint
    with pytest.raises(ValueError, match="Canonical"):
        verified_unblind_records(package=p, capture=c, frozen=f, mappings=swapped)
    correct = verified_unblind_records(
        package=p,
        capture=c,
        frozen=f,
        mappings=bindings,
    )
    assert correct.by_address()[Address("l1.py")].judgment is J.USEFUL
    assert correct.by_address()[Address("l2.py")].judgment is J.NOT_USEFUL


@pytest.mark.parametrize(
    "change",
    [
        "duplicate",
        "missing",
        "unknown",
        "neutral",
        "reorder",
        "protocol",
        "question",
        "visibility",
    ],
)
def test_typed_adapter_negative_boundaries(change: str) -> None:
    c = _capture()
    p, b, f = _frozen(c, {})
    if change == "duplicate":
        b = (b[0], b[0], *b[2:])
    elif change == "missing":
        b = b[:-1]
    elif change == "unknown":
        b = (replace(b[0], address=Address("foreign.py")), *b[1:])
    elif change == "neutral":
        b = (replace(b[0], neutral_id="unknown"), *b[1:])
    elif change == "reorder":
        b = tuple(reversed(b))
    elif change == "protocol":
        p = replace(p, protocol_version="v1-unsupported")
    elif change == "question":
        p = replace(p, information_need="foreign question")
    elif change == "visibility":
        b = (replace(b[0], address_visible_to_adjudicator=True), *b[1:])
    with pytest.raises(
        ValueError,
        match=r"Canonical|Unsupported|differs|differ|Incomplete|zip",
    ):
        verified_unblind_records(package=p, capture=c, frozen=f, mappings=b)


def test_saved_json_returns_only_checked_labels_and_does_not_mutate() -> None:
    inputs = _inputs()
    before = deepcopy(inputs)
    records = verify_artifact_bindings(**inputs)["synthetic-case"].by_address()
    assert records[Address("l1.py")].judgment is J.USEFUL
    assert records[Address("l2.py")].judgment is J.NOT_USEFUL
    assert records[Address("l3.py")].judgment is J.UNJUDGED
    assert inputs == before


@pytest.mark.parametrize(
    "change",
    ["swap", "duplicate", "missing", "unknown", "neutral", "reorder", "visibility"],
)
def test_resealed_mapping_cannot_change_canonical_pairs_or_positional_join(
    change: str,
) -> None:
    inputs = _inputs()
    payload = inputs["mapping"]["payload"]
    bindings = payload["mappings"][0]
    if change == "swap":
        bindings[0]["address"], bindings[1]["address"] = (
            bindings[1]["address"],
            bindings[0]["address"],
        )
    elif change == "duplicate":
        bindings[1] = deepcopy(bindings[0])
    elif change == "missing":
        bindings.pop()
    elif change == "unknown":
        bindings[0]["address"] = "foreign.py"
    elif change == "neutral":
        bindings[0]["neutral_id"] = "foreign-neutral"
    elif change == "reorder":
        bindings.reverse()
    elif change == "visibility":
        bindings[0]["address_visible_to_adjudicator"] = True
    payload["mapping_set_identity"] = _digest(
        {
            "capture_set_identity": payload["capture_set_identity"],
            "mappings": payload["mappings"],
        },
    )
    _reseal(inputs["mapping"])
    assert validate_artifact_correspondence(
        **{key: inputs[key] for key in ("capture", "package", "mapping")},
    )
    with pytest.raises(ValueError, match=r"Canonical|visibility"):
        verify_artifact_bindings(**inputs)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ("schema", "Unsupported"),
        ("incomplete", "Incomplete"),
        ("case_order", "mapping set identity"),
        ("case_identity", "Case capture identities"),
        ("capture_set", "capture links"),
        ("mapping_set", "mapping set identity"),
        ("freeze", "fingerprint"),
        ("package", "package-set identity"),
        ("question", "question/frame"),
    ],
)
def test_incomplete_foreign_or_unsupported_artifacts_fail_closed(  # noqa: C901 -- independent artifact mutations
    change: str,
    message: str,
) -> None:
    inputs = _inputs()
    if change == "schema":
        inputs["package"]["schema"] = "package-v1"
    elif change == "incomplete":
        del inputs["capture"]["payload"]["cases"][0]["retained_targets"]
    elif change == "case_order":
        inputs["mapping"]["payload"]["mappings"] = []
    elif change == "case_identity":
        inputs["capture"]["payload"]["case_capture_identities"] = ["foreign"]
    elif change == "capture_set":
        inputs["capture"]["payload"]["capture_set_identity"] = "foreign"
    elif change == "mapping_set":
        inputs["mapping"]["payload"]["mapping_set_identity"] = "foreign"
    elif change == "freeze":
        inputs["frozen"]["payload"]["cases"][0]["records"].reverse()
    elif change == "package":
        inputs["package"]["payload"]["packages"][0]["items"].reverse()
    elif change == "question":
        inputs["capture"]["payload"]["cases"][0]["information_need"] = (
            "foreign question"
        )
    for value in inputs.values():
        _reseal(value)
    with pytest.raises(ValueError, match=message):
        verify_artifact_bindings(**inputs)
