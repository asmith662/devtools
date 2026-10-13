# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, PLR2004, S101, D103, COM812 -- bounded proof fixtures
"""Sealed downstream rejection and small deep fixtures; no full native replay."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import binary, digest, json_bytes
from experiments.codex_dogfood.case_0016 import freeze
from experiments.codex_dogfood.case_0016.adjudication.reviewed import (
    materialize as gold,
)
from experiments.codex_dogfood.case_0016.stage_b import authenticate as a
from experiments.codex_dogfood.case_0016.stage_d import analysis, authentication

from . import case_0016, completion
from .bindings import bind
from .case_0016 import AuthenticatedInputs, Invocation
from .proof import CHECKS, CompletionBindings, authenticate_proof, publish_proof


def bindings() -> CompletionBindings:
    value: dict[str, Any] = {
        "case": "fixture",
        "execution": "fixture-1",
        "frame": {"repository_id": "r", "snapshot_id": "s", "corpus_id": "c"},
    }
    for name in ("protocol", "schedule", "journal_chain", "completion"):
        value[name + "_sha256"] = digest(name.encode())
    for name in ("native", "canonical", "implementation", "verifier"):
        value[name + "_sha256"] = {name: digest(name.encode())}
    return CompletionBindings.create(value)


def test_future_proof_executes_once_and_authenticates_exact_result(
    tmp_path: Path,
) -> None:
    count = 0

    def prove() -> bytes:
        nonlocal count
        count += 1
        return json_bytes({"status": "PASS", "checks": dict.fromkeys(CHECKS, "PASS")})

    path = tmp_path / "proof.json"
    inputs = bindings()
    sha = publish_proof(path, inputs, prove)
    result = authenticate_proof(path.read_bytes(), sha, inputs)
    assert json.loads(result)["status"] == "PASS"
    assert count == 1
    assert authenticate_proof(path.read_bytes(), sha, inputs) == result
    assert count == 1
    with pytest.raises(FileExistsError):
        publish_proof(path, inputs, prove)
    assert count == 1
    for field in ("inputs_sha256", "deep_result_sha256", "schema", "deep_result_b64"):
        mutated = json.loads(path.read_bytes())
        mutated[field] = "changed"
        with pytest.raises(ValueError, match=r".+"):
            authenticate_proof(json_bytes(mutated), sha, inputs)
    for field in json.loads(inputs.raw):
        altered = json.loads(inputs.raw)
        if isinstance(altered[field], dict):
            first = next(iter(altered[field]))
            altered[field][first] = digest(b"foreign")
        else:
            altered[field] = (
                digest(b"foreign") if field.endswith("sha256") else "foreign"
            )
        with pytest.raises(ValueError, match=r".+"):
            authenticate_proof(
                path.read_bytes(), sha, CompletionBindings.create(altered)
            )


def test_failed_deep_proof_cannot_publish(tmp_path: Path) -> None:
    path = tmp_path / "proof.json"
    with pytest.raises(ValueError, match="every required check"):
        publish_proof(path, bindings(), lambda: json_bytes({"status": "PASS"}))
    assert not path.exists()


def test_normal_rejects_gold_mutation(monkeypatch: pytest.MonkeyPatch) -> None:
    target = gold.ROOT / "reviewed_gold.json"
    original = Path.read_bytes

    def read(path: Path) -> bytes:
        raw = original(path)
        if path == target:
            value = json.loads(raw)
            value["primary"]["cells"][0]["label"] = "foreign"
            return json_bytes(value)
        return raw

    monkeypatch.setattr(Path, "read_bytes", read)
    with pytest.raises(ValueError, match="Reviewed reconstruction"):
        Invocation().reviewed()


@pytest.mark.parametrize(
    "name",
    [
        "integrity.json",
        "execution_completed.json",
        "execution_started.json",
        "native_context.json",
        "validation.json",
        "arm_a.json.gz",
        "arm_c.json.gz",
        "ppr_states.json.gz",
        "pair_flows.json.gz",
        "operations/000001.returned.json",
    ],
)
def test_normal_rejects_capture_mutation(
    name: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = a.CAPTURE / name
    original = Path.read_bytes

    def read(path: Path) -> bytes:
        raw = original(path)
        return raw + b"changed" if path == target else raw

    monkeypatch.setattr(Path, "read_bytes", read)
    with pytest.raises(ValueError, match="explicit deep/proof migration required"):
        completion.authenticate(a.CAPTURE)


def test_normal_rejects_frame_and_implementation_binding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = binary

    def read(path: Path) -> bytes:
        raw = original(path)
        if path == freeze.CASE / "frame.json":
            value = json.loads(raw)
            value["snapshot_id"] = "foreign"
            return json_bytes(value)
        return raw

    monkeypatch.setattr(completion, "binary", read)
    with pytest.raises(ValueError, match="frame/protocol/source"):
        completion.authenticate(a.CAPTURE)
    monkeypatch.setattr(completion, "binary", original)
    hashes = a.source_hashes()
    changed = copy.deepcopy(hashes)
    changed[next(iter(changed))] = digest(b"changed")
    monkeypatch.setattr(a, "source_hashes", lambda: changed)
    with pytest.raises(ValueError, match="producer implementation"):
        completion.authenticate(a.CAPTURE)


def test_normal_never_decodes_native_and_reauthenticates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: Any) -> Any:
        raise AssertionError("Normal verification entered deep replay")

    count = 0
    original = completion.authenticate

    def authenticate(root: Path) -> completion.AuthenticatedCompletion:
        nonlocal count
        count += 1
        return original(root)

    monkeypatch.setattr(case_0016, "authenticate_completion", authenticate)
    monkeypatch.setattr(Invocation, "native", forbidden)
    monkeypatch.setattr(Invocation, "replay", forbidden)
    provenance = json.loads((analysis.PACKAGE / "trace.json").read_bytes())[
        "provenance"
    ]

    def checkpoints(_invocation: Invocation, facade: Any) -> Any:
        # Actual checkpoint authentication belongs to the one separate-process
        # proving run. This focused fixture exercises the real normal input path.
        return bind(authentication.read_inputs, {"m": facade}), provenance

    def wrapped(invocation: Invocation, facade: Any) -> Any:
        read, retained = checkpoints(invocation, facade)
        return SimpleNamespace(read_inputs=read), retained

    monkeypatch.setattr(Invocation, "checkpoints", wrapped)
    for _ in range(2):
        invocation = Invocation()
        inputs = invocation.authenticate()
        assert isinstance(inputs, AuthenticatedInputs)
        assert inputs.journal is None
        assert inputs.completion is not None
        assert inputs.completion.envelopes == 465
        assert invocation.authenticate() is inputs
        assert invocation.counts["primary_authentication"] == 1
        assert invocation.counts["primary_adversarial_bundle"] == 1
        assert invocation.counts["native_archives_decoded"] == 0
        assert invocation.counts["deep_correspondence_executions"] == 0
        expected = invocation.expected(inputs)
        assert all(
            (analysis.PACKAGE / n).read_bytes() == raw for n, raw in expected.items()
        )
    assert count == 2
