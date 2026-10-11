# Copyright (c) 2026
# ruff: noqa: COM812, S101, D103, PLR2004, EM101, TRY003, PT011, E501 -- controlled native fixtures
"""Test full synthetic capture, durable failures, blind allowlists and no-rerun replay."""

from __future__ import annotations

import asyncio
import copy
import gzip
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    put_text,
)
from experiments.codex_dogfood.case_0012.freeze import frame_resources
from experiments.codex_dogfood.case_0012.stage_b import durability
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal
from experiments.codex_dogfood.case_0013 import freeze, protocol
from experiments.codex_dogfood.case_0013.stage_b import execute, reporting
from experiments.codex_dogfood.case_0013.stage_b.authenticate import (
    STAGE_A,
    authenticate,
)
from experiments.codex_dogfood.case_0013.stage_c import packet, validate_packet
from experiments.exact_hint_routing.models import ResolutionDisposition

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(scope="module")
def captured(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    # Artificial content only. No prospective Case 0013 native input is executed.
    blobs = {
        "src/devtools/context/planning/materialization.py": b"class ContextDisclosure: pass\ndef materialize_disclosure_plan(): pass\n# Context planning source structure\n",
        "src/devtools/context/repository/snapshot.py": b"class RepositorySnapshot:\n    def resource_at(self): pass\n# integrity resource content\n",
        "src/devtools/context/planning/rendering.py": b"def render(): pass\n# Context planning ModelRequest render\n",
        "src/devtools/context/planning/docs/overview.md": b"Context planning documentation manifest provenance\n",
        "pyproject.toml": b"# protected development validation coverage mypy\n",
    }
    frame, m = freeze.prepare_frame(blobs)
    image = {"metadata": m, "resources": frame_resources(frame)}
    t = protocol.definition()
    j = Journal.start(
        tmp_path_factory.mktemp("synthetic-stage-b"),
        {
            "execution": "CONTROLLED_FIXTURE_ONLY",
            "stage_a_trace_sha256": "f" * 64,
            "frame": {
                k: m[k]
                for k in ("repository_id", "snapshot_id", "corpus_id", "frame_identity")
            },
            "runtime": "fixture",
        },
    )
    j.context({"metadata": m, "treatment": t, "image": image})
    execute.run_schedule(j, image, t)
    loaded = Journal.load(j.root)
    assert loaded.state["state"] == "NATIVE_CAPTURE_COMPLETE"
    return loaded.state


def test_complete_synthetic_schedule_and_deterministic_mechanics(
    captured: dict[str, Any],
) -> None:
    result = reporting.artifacts(captured)
    assert result == reporting.artifacts(captured)
    s = json.loads(result["summary.json"])
    assert s["counts"]["index_builds"] == 1
    assert s["counts"]["obligation_queries"] == 9
    assert s["counts"]["global_queries"] == 1
    assert s["counts"]["A_exact_requests"] == 0
    assert s["counts"]["B_exact_requests"] == 10
    assert s["counts"]["C_exact_requests"] == 6
    assert {r["hint"] for r in s["C_skipped"]} == {"H04", "H05", "H06", "H08"}
    assert all(
        r["C_native_outcome"] is None and r["C_invocations"] == 0
        for r in s["C_skipped"]
    )
    assert s["lexical_fallback"] == s["global_safety"] == "PRESERVED"
    assert s["gold"] == "ABSENT"
    assert s["effectiveness"] == "UNKNOWN"
    assert s["u3_outcome"] == "NOT_SELECTED"
    assert all(set(s["families"][a]) == set(reporting.FAMILIES) for a in ("B", "C"))
    assert sum(f["admitted_requests"] for f in s["families"]["B"].values()) == 10
    assert sum(f["admitted_requests"] for f in s["families"]["C"].values()) == 6
    assert result["TRACE.md"] == result["STAGE_B_REVIEW.md"]
    for arm in ("A", "B", "C"):
        costs = s["costs"]["arms"][arm]
        assert costs["charged_ns"] == s["costs"]["native_index_ns"] + s["costs"][
            "shared_queries_ns"
        ] + costs["policy_ns"] + costs["route_ns"] + costs["presentation_ns"] + (
            0 if arm == "A" else s["costs"]["shared_purposes_hint_extraction_ns"]
        )


def test_native_arm_aliases_and_no_cross_arm_reuse(captured: dict[str, Any]) -> None:
    v = captured["values"]
    for c in v["arm:C"]["resolutions"]:
        b = next(
            r
            for r in v["arm:B"]["resolutions"]
            if r.request.identity == c.request.identity
        )
        assert b is not c
        assert all(
            x is not y
            for x, y in zip(b.native_provenance, c.native_provenance, strict=True)
        )
    changed = copy.deepcopy(captured)
    c_arm = changed["values"]["arm:C"]
    r = changed["values"]["arm:B"]["resolutions"][0]
    c_arm["resolutions"] = (r, *c_arm["resolutions"][1:])
    with pytest.raises(ValueError):
        reporting.artifacts(changed)


@pytest.mark.parametrize(
    "mutation", ["policy", "route", "order", "score", "global", "duplicate", "frame"]
)
def test_captured_tamper_rejected(captured: dict[str, Any], mutation: str) -> None:
    s = copy.deepcopy(captured)
    v = s["values"]
    if mutation == "policy":
        v["treatment"]["route_decisions"]["C"][0]["disposition"] = "LEXICAL_ONLY"
    elif mutation == "route":
        r = v["arm:C"]["resolutions"][0]
        v["arm:C"]["resolutions"] = (
            replace(r, reason="tampered"),
            *v["arm:C"]["resolutions"][1:],
        )
    elif mutation == "frame":
        v["frame:assembly"] = replace(v["frame:assembly"], declaration_addresses=())
    elif mutation == "duplicate":
        s["operations"].append(s["operations"][0])
    else:
        view = v["arm:C"]["views"]["structure"]
        if mutation == "global":
            changed = replace(
                view,
                global_lexical_safety_lane=replace(
                    view.global_lexical_safety_lane, matches=()
                ),
            )
        elif mutation == "order":
            changed = replace(view, exact_first=view.exact_first[::-1])
        else:
            e = next(
                e for e in view.exact_first if e.lexical_result_reference is not None
            )
            changed_entry = replace(
                e,
                lexical_result_reference=replace(e.lexical_result_reference, score=999),
            )
            changed = replace(
                view,
                exact_first=tuple(
                    changed_entry if x is e else x for x in view.exact_first
                ),
            )
        v["arm:C"]["views"]["structure"] = changed
    with pytest.raises(ValueError):
        reporting.artifacts(s)


def test_nonresolved_scope_promotes_nothing(captured: dict[str, Any]) -> None:
    s = json.loads(reporting.artifacts(captured)["summary.json"])
    new = [
        r
        for r in s["hint_rows"]
        if r["arm"] == "B" and r["hint"] in {"H04", "H05", "H06", "H08"}
    ]
    assert all(r["disposition"] == "UNRESOLVED" and not r["targets"] for r in new)
    # All enum scope outcomes remain supported; native ambiguous/unsupported
    # fixture coverage is also inherited from the exact-hint contract tests.
    assert {s.value for s in ResolutionDisposition} == {
        "RESOLVED",
        "AMBIGUOUS",
        "UNRESOLVED",
        "UNSUPPORTED",
    }


def test_journal_exclusive_no_duplicate_and_summary_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    j = Journal.start(tmp_path, {"execution": "durability-fixture"})
    j.context({})

    def fail(*_args: object) -> None:
        raise PermissionError("derived summary blocked")

    monkeypatch.setattr(durability, "atomic", fail)
    calls = []

    def returned() -> int:
        calls.append(1)
        return 42

    assert j.call("once", {}, returned) == 42
    loaded = Journal.load(tmp_path)
    assert loaded.state["values"]["once"] == 42
    assert len(calls) == 1
    with pytest.raises(ValueError):
        j.call("once", {}, lambda: calls.append(2))
    with pytest.raises(FileExistsError):
        Journal.start(tmp_path, {"execution": "second"})
    with pytest.raises(ValueError, match="cannot invoke"):
        loaded.call("new", {}, lambda: None)
    with pytest.raises(FileExistsError):
        durability.exclusive(tmp_path / "operations/000001.entered.json", {})


def test_return_publication_loss_blocks_inference_and_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    j = Journal.start(tmp_path, {"execution": "return-loss-fixture"})
    j.context({})
    original = j.event

    def event(sequence: int, status: str, payload: dict[str, Any]) -> None:
        if status == "RETURNED":
            raise OSError("durable return publication failure")
        original(sequence, status, payload)

    monkeypatch.setattr(j, "event", event)
    calls = []

    def returned() -> int:
        calls.append(1)
        return 42

    with pytest.raises(OSError):
        j.call("one", {}, returned)
    assert len(calls) == 1
    with pytest.raises(ValueError, match="Unrecoverable"):
        Journal.load(tmp_path).ready()
    with pytest.raises(ValueError, match="already entered"):
        j.call("one", {}, lambda: calls.append(2))


def test_native_exception_fails_without_return(tmp_path: Path) -> None:
    j = Journal.start(tmp_path, {"execution": "exception-fixture"})

    def error() -> None:
        raise RuntimeError("native fixture failure")

    with pytest.raises(RuntimeError):
        j.call("fail", {}, error)
    with pytest.raises(ValueError, match="Unrecoverable"):
        Journal.load(tmp_path).ready()


def test_producer_records_return_loss_and_refuses_second_attempt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "controlled-attempt"
    monkeypatch.setattr(execute, "CAPTURE", target)

    async def auth() -> dict[str, Any]:
        return {"frame": json.loads(binary(freeze.CASE / "frame.json"))}

    async def git(*args: str) -> bytes:
        if args[0] == "rev-parse":
            return STAGE_A.encode()
        return b"main" if args[0] == "branch" else b""

    monkeypatch.setattr(execute, "authenticate", auth)
    monkeypatch.setattr(execute, "git", git)
    original = Journal.event

    def event(
        self: Journal, sequence: int, status: str, payload: dict[str, Any]
    ) -> None:
        if status == "RETURNED":
            raise OSError("controlled return persistence failure")
        original(self, sequence, status, payload)

    monkeypatch.setattr(Journal, "event", event)
    calls: list[int] = []

    def native_return() -> str:
        calls.append(1)
        return "controlled native return"

    def schedule(j: Journal, *_args: object) -> None:
        j.call("CONTROLLED_FIXTURE_ONLY", {}, native_return)

    monkeypatch.setattr(execute, "run_schedule", schedule)
    with pytest.raises(OSError):
        asyncio.run(execute.execute())
    assert len(calls) == 1
    assert (target / "capture_failure.json").is_file()
    assert not (target / "execution_completed.json").exists()
    with pytest.raises(FileExistsError, match="retry refused"):
        asyncio.run(execute.execute())


def test_stage_a_authentication_after_implementation_without_execution() -> None:
    assert asyncio.run(authenticate())["authentication"] == "PASS"


def test_authentication_rejects_gold_and_authority_tamper_before_execution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(freeze, "CASE", tmp_path)
    put_text(tmp_path / "gold.json", "forbidden")
    with pytest.raises(ValueError, match="gold artifact"):
        asyncio.run(authenticate())
    # Use a separate fresh fixture; no deletion or replacement of frozen inputs.
    fresh = tmp_path / "authority-tamper"
    put_text(fresh / "integrity.json", json.dumps({"sha256": {}}))
    monkeypatch.setattr(freeze, "CASE", fresh)
    with pytest.raises(ValueError, match="integrity differs"):
        asyncio.run(authenticate())


@pytest.mark.parametrize(
    "field",
    [
        "query",
        "analyzed_terms",
        "roles",
        "hint_metadata",
        "locator",
        "arm",
        "rank",
        "score",
        "cost",
        "result",
        "mechanism",
    ],
)
def test_blind_metadata_leakage_rejection(field: str) -> None:
    p = packet.payload()
    p["resources"][0][field] = "forbidden metadata"
    with pytest.raises(ValueError, match="leakage"):
        validate_packet.validate_payload(p)


def test_packet_exact_allowlist_content_and_tamper(tmp_path: Path) -> None:
    p = packet.payload()
    assert set(p) == validate_packet.PAYLOAD
    assert all(set(r) == validate_packet.RESOURCE for r in p["resources"])
    output = packet.render(p)
    assert output == packet.render(p)
    root = tmp_path / "fresh"
    packet.publish(root, output)
    assert {x.name for x in root.iterdir()} == validate_packet.FILES
    assert validate_packet.validate(root)["status"].startswith("PASS")
    with pytest.raises(FileExistsError):
        packet.publish(root, output)
    put_text(root / ".local", "forbidden")
    with pytest.raises(ValueError, match="whitelist"):
        validate_packet.validate(root)
    changed = copy.deepcopy(p)
    changed["resources"][0]["text"] += "tamper"
    with pytest.raises(ValueError, match="content"):
        validate_packet.validate_payload(changed)
    seal = json.loads(output["integrity.json"])
    assert seal["canonical_payload_sha256"] == digest(
        gzip.decompress(output["resources.json.gz"])
    )


def test_complete_capture_replay_without_native_calls_if_present(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if not (execute.CAPTURE / "integrity.json").exists():
        return

    def forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("native rerun prohibited")

    monkeypatch.setattr(execute, "run_schedule", forbidden)
    monkeypatch.setattr(
        execute, "retrieve_repository_text_documents_by_bm25", forbidden
    )
    assert execute.verify()["stage_b"] == "CAPTURED"
