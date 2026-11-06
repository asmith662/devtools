# Copyright (c) 2026
"""Independent rejection of rehashed state and reordered recorder acknowledgments."""

from __future__ import annotations

import asyncio
import hashlib
import json
import sqlite3
from dataclasses import replace
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from devtools.learning.classification.linear import _hash
from devtools.learning.integrations.local.inspection import inspect_learning
from devtools.learning.integrations.local.regression.codec import state as decode_state
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.plans import LearningPlan, canonical
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.tools.learning import ManagedLearningWorker
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.learning.integrations.local.operations import LearningPublication


def fitted(
    tmp_path: Path,
) -> tuple[LearningPlan, ExecutionAuthorization, LearningPublication]:
    """Create and positively inspect one owned genuine Mean fitting control."""
    plan = authored_task("regression").plan("mean", "online", "corruption-control")
    grant = ExecutionAuthorization(
        plan.identity,
        (plan.method,),
        EvidenceReference(
            "learning_execution_grant-v1",
            "owned-test-grant",
            plan.identity,
        ),
    )
    reference = asyncio.run(
        ManagedLearningWorker.current().execute(plan, grant, tmp_path / "operation"),
    )
    inspect_learning(reference, plan, grant)
    return plan, grant, reference


def test_rehashed_false_mean_even_with_rewritten_ledger(tmp_path: Path) -> None:
    """A wrong mean cannot become evidence by rewriting hashes and ledger claims."""
    plan, grant, reference = fitted(tmp_path)
    root = reference.root.value
    generation = root / "publication/generations" / reference.generation_id
    member = generation / "result.json"
    saved = json.loads(member.read_bytes())
    old_root = _hash(saved["state"])
    old_state = decode_state(saved["state"]).content_identity
    saved["state"]["intercept"] += 1.0
    new_root = _hash(saved["state"])
    new_state = decode_state(saved["state"]).content_identity
    before = member.read_bytes()
    after = canonical(saved).encode()
    assert len(before) == len(after)
    member.write_bytes(after)
    manifest = generation / "manifest.json"
    metadata = json.loads(manifest.read_bytes())
    metadata["artifacts"][0]["sha256"] = hashlib.sha256(after).hexdigest()
    raw = canonical(metadata).encode()
    manifest.write_bytes(raw)
    new_manifest = hashlib.sha256(raw).hexdigest()
    current = root / "publication/current.json"
    pointer = json.loads(current.read_bytes())
    pointer["manifest_sha256"] = new_manifest
    current.write_bytes(canonical(pointer).encode())
    changes = {
        old_state: new_state,
        old_root: new_root,
        reference.manifest_sha256: new_manifest,
        hashlib.sha256(before).hexdigest(): hashlib.sha256(after).hexdigest(),
    }
    with sqlite3.connect(root / "science.sqlite") as conn:
        for identity, text in conn.execute("SELECT id,document FROM events").fetchall():
            for a, b in sorted(changes.items(), key=lambda p: -len(p[0])):
                text = text.replace(a, b)
            conn.execute("UPDATE events SET document=? WHERE id=?", (text, identity))
    with pytest.raises(ValueError, match="original training mean arithmetic"):
        inspect_learning(replace(reference, manifest_sha256=new_manifest), plan, grant)


def test_fit_ack_observed_after_prediction_refuses(tmp_path: Path) -> None:
    """An event occurrence does not prove that its recorder acknowledged it in time."""
    plan, grant, reference = fitted(tmp_path)
    root = reference.root.value
    member = next((root / "publication/generations").glob("*/result.json"))
    saved = json.loads(member.read_bytes())
    with sqlite3.connect(root / "science.sqlite") as conn:
        rows = [
            (identity, json.loads(text))
            for identity, text in conn.execute(
                "SELECT id,document FROM events",
            ).fetchall()
        ]
        predicting = next(
            d
            for _, d in rows
            if d["kind"] == "Admitted"
            and d["payload"]["operation"] == "learning.predict"
        )
        for identity, d in rows:
            if (
                d["execution_id"] == saved["fitting_execution_id"]
                and d["kind"] == "Terminal"
            ):
                d["observed_at"] = (
                    datetime.fromisoformat(predicting["occurred_at"])
                    + timedelta(microseconds=1)
                ).isoformat()
                conn.execute(
                    "UPDATE events SET document=? WHERE id=?",
                    (canonical(d), identity),
                )
    with pytest.raises(ValueError, match=r"fitting.*prediction"):
        inspect_learning(reference, plan, grant)
