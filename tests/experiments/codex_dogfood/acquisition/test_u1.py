# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- explicit frozen protocol and tiny mechanical fixtures
"""Test linkage, controlled execution and blind projections without adjudication."""

from __future__ import annotations

import asyncio
import json
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from typing import TYPE_CHECKING, Any, NoReturn

import pytest

if TYPE_CHECKING:
    from pathlib import Path

from devtools.context.localization import (
    LocalizationAnchorIdentity,
    LocalizationTaskIdentity,
    TaskProvenance,
)
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.retrieval.lexical.bm25 import (
    retrieve_repository_text_documents_by_bm25,
)
from devtools.core.paths import resolve_path
from experiments.codex_dogfood.acquisition.needs import InformationNeed
from experiments.codex_dogfood.acquisition.trace import layer, review, validate
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    read_json,
)
from experiments.codex_dogfood.case_0009.freeze import REPOSITORY
from experiments.codex_dogfood.case_0011 import execute, freeze, packet, protocol
from experiments.retrieval_diagnostics.models import Configuration


@pytest.fixture
def native(tmp_path: Path) -> dict[str, Any]:
    """Use a two-resource synthetic frame, never a historical gold fixture."""
    for name, text in (("one.py", "alpha beta\n"), ("two.py", "beta gamma\n")):
        (tmp_path / name).write_bytes(text.encode())
    root = resolve_path(tmp_path)
    discovery = discover_repository_resource_addresses(
        repository=REPOSITORY,
        root=root,
        maximum_resource_count=10,
        maximum_traversal_entry_count=30,
    )
    snapshot = observe_repository_resources(
        repository=REPOSITORY,
        root=root,
        addresses=discovery.addresses,
        maximum_resource_bytes=1000,
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery, selected_addresses=discovery.addresses
        ),
        snapshot=snapshot,
    )
    _, task, queries = protocol.definition()
    return {
        "snapshot": snapshot,
        "corpus": corpus,
        "documents": represent_repository_text_corpus(corpus=corpus),
        "task": task,
        "queries": queries,
    }


def test_frozen_authoring_and_native_contracts() -> None:
    """Literal authored inputs survive native identity projection and tokenization."""
    t, task, queries = protocol.definition()
    original, authored = protocol.source()
    assert t["task"] == original
    assert len(task.obligations) == 9
    assert len(t["information_needs"]) == 18
    assert Counter(q["arm"] for q in t["queries"]) == {"A": 1, "B": 9, "C": 18}
    assert [q.text for q in queries] == [o["query"] for o in authored["obligations"]]
    literal_c = [n["query"] for o in authored["obligations"] for n in o["needs"]]
    assert [q["text"] for q in t["queries"] if q["arm"] == "C"] == literal_c
    for name, expected in protocol.AUTHOR_HASHES.items():
        assert digest((protocol.CASE / name).read_bytes()) == expected
    assert {h["hint"] for h in t["hints"]} == {
        "ModelRequest",
        "ContextDisclosure",
        "DisclosurePlan",
    }
    assert all(not h["exact_hint_routed"] for h in t["hints"])
    assert all(
        o.satisfaction.statement == row["criterion"]["statement"]
        for o, row in zip(task.obligations, t["obligations"], strict=True)
    )
    assert original.removesuffix("\n") in review(t)
    trace = layer(t, "STAGE_A")
    assert not trace["RESULT"]
    assert not trace["JUDGMENT"]
    assert not trace["FAILURE"]
    assert json_bytes(layer(t, "STAGE_A")) == json_bytes(trace)


def test_need_is_purpose_not_query_and_retains_native_scope() -> None:
    """Validate the bounded experimental value and foreign-anchor rejection."""
    _, task, _ = protocol.definition()
    n = InformationNeed(
        "test",
        task.obligations[0].identity,
        "What contract?",
        "Caller must learn it",
        TaskProvenance("task.txt"),
    )
    assert n.identity == task.identity.value + "/ownership/test"
    assert not hasattr(n, "query")
    with pytest.raises(ValueError, match="key"):
        replace(n, key="")
    with pytest.raises(ValueError, match="owning task"):
        replace(
            n,
            anchors=(
                LocalizationAnchorIdentity(
                    LocalizationTaskIdentity("foreign"), "symbol"
                ),
            ),
        )


@pytest.mark.parametrize(
    "mutation",
    [
        "duplicate",
        "owner",
        "scope",
        "query",
        "terms",
        "route",
        "hint",
        "basis",
        "whole",
        "need-query",
    ],
)
def test_trace_tamper_rejection(mutation: str) -> None:
    """Reject duplicates, scope changes, hidden rewrites and unauthorized routes."""
    t = deepcopy(protocol.definition()[0])
    if mutation == "duplicate":
        t["information_needs"].append(deepcopy(t["information_needs"][0]))
    elif mutation == "owner":
        t["information_needs"][0]["obligation"] = "unknown"
    elif mutation == "scope":
        t["information_needs"][0]["identity"] = "foreign/task/need"
    elif mutation == "query":
        t["queries"][1]["text"] += " repository_answer_only"
    elif mutation == "terms":
        t["queries"][1]["analyzed_terms"].append("fake")
    elif mutation == "route":
        t["queries"][0]["route"]["mechanism"] = "EXACT"
    elif mutation == "hint":
        t["queries"][0]["route"]["exact_hint_routed"] = True
    elif mutation == "basis":
        t["obligations"][0]["task_basis"][0]["text"] = "changed"
    elif mutation == "whole":
        t["queries"][0]["text"] = "summary"
    else:
        t["queries"] = [q for q in t["queries"] if q["arm"] != "C"]
    with pytest.raises(
        ValueError,
        match=r"Duplicate|unknown|scope|transformation|route|span|changed|linkage",
    ):
        validate(t)


def test_each_query_executes_once_without_fusion(
    native: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Count native calls on tiny fixture lanes and verify exact score projection."""
    t = deepcopy(protocol.definition()[0])
    t["queries"] = [
        deepcopy(t["queries"][0]),
        deepcopy(t["queries"][1]),
        deepcopy(next(q for q in t["queries"] if q["arm"] == "C")),
    ]
    for q in t["queries"]:
        q["text"] = "alpha beta"
        q["analyzed_terms"] = ["alpha", "beta"]
    monkeypatch.setattr(
        execute, "definition", lambda: (t, native["task"], native["queries"])
    )
    monkeypatch.setattr(execute, "load_inputs", lambda: native)
    monkeypatch.setattr(
        execute,
        "configuration",
        lambda: Configuration("fixture", "fixture-index", "canonical", 1.2, 0.75, 0.25),
    )
    original = retrieve_repository_text_documents_by_bm25
    calls: list[str] = []

    def counted(**kwargs: Any) -> Any:  # noqa: ANN401 -- native retrieval keyword boundary
        calls.append(kwargs["query"].text)
        return original(**kwargs)

    monkeypatch.setattr(execute, "retrieve_repository_text_documents_by_bm25", counted)
    captures, cost = execute.captures()
    assert calls == ["alpha beta"] * 3
    assert len(captures) == cost["query_count"] == 3
    assert all(c["execution_count"] == 1 for c in captures.values())
    assert all(len(c["rows"]) == 2 for c in captures.values())


def test_uncommitted_execution_and_existing_marker_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Refuse scoring before committed inputs and after an exclusive marker."""

    async def absent(*_args: str) -> bytes:
        return b"\n"

    monkeypatch.setattr(execute, "git", absent)
    with pytest.raises(ValueError, match="committed Stage A"):
        asyncio.run(execute.committed_stage_a())
    monkeypatch.setattr(execute, "CASE", tmp_path)
    (tmp_path / "execution_started.json").write_bytes(b"{}")
    with pytest.raises(FileExistsError):
        execute.run()


def test_blind_double_build_no_needs_queries_or_results(native: dict[str, Any]) -> None:
    """Strict metadata projections preserve task/criteria/full frame only."""
    a, b = packet.render(native), packet.render(native)
    assert a == b
    manifest = json.loads(a["manifest.json"])
    assert manifest["expected_cell_count"] == 18
    assert "information_needs" not in manifest
    assert "queries" not in manifest
    assert "arms" not in manifest
    assert all("query" not in o and "needs" not in o for o in manifest["obligations"])
    damaged = dict(a)
    manifest["queries"] = ["leak"]
    damaged["manifest.json"] = json_bytes(manifest)
    with pytest.raises(ValueError, match="leakage"):
        packet.validate(damaged, native)
    damaged = dict(a)
    damaged["resources.json.gz"] = a["resources.json.gz"] + b"damage"
    with pytest.raises((ValueError, OSError, EOFError)):
        packet.validate(damaged, native)


def test_workspace_whitelist_and_packet_overwrite(
    native: dict[str, Any], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Accept only six regular files and refuse any preexisting packet directory."""
    target = tmp_path / "packet"
    target.mkdir()
    for name, data in packet.render(native).items():
        (target / name).write_bytes(data)
    packet.whitelist(target)
    (target / "trace.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="shape"):
        packet.whitelist(target)
    monkeypatch.setattr(packet, "CASE", tmp_path)
    (tmp_path / "adjudication").mkdir()
    with pytest.raises(FileExistsError):
        packet.build()


def test_retained_stage_a_replay_when_frozen() -> None:
    """Verify official input/trace/review and all source hashes after freezing."""
    if not (protocol.CASE / "integrity.json").exists():
        pytest.skip("Stage A not yet frozen")
    m = freeze.verify()
    t, _, _ = protocol.definition()
    assert m["queries"] == 28
    assert read_json(protocol.CASE / "stage_a_trace.json") == layer(t, "STAGE_A")
    assert binary(protocol.CASE / "STAGE_A_REVIEW.md") == review(t).encode()


def forbidden(*_args: object, **_kwargs: object) -> NoReturn:
    """Prohibit rescoring in retained capture verification."""
    message = "Official queries must not execute again"
    raise AssertionError(message)


def test_retained_stage_b_and_sterile_packet_without_scoring(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify unjudged full captures and copied packet; never perform C/C.5/D."""
    if not (protocol.CASE / "stage_b_integrity.json").exists():
        pytest.skip("Stage B not yet captured")
    monkeypatch.setattr(
        execute, "retrieve_repository_text_documents_by_bm25", forbidden
    )
    assert execute.verify() == {
        "status": "R1.5/trace replay PASSED",
        "queries": 28,
        "effectiveness": "UNKNOWN",
    }
    if (protocol.CASE / "sterile_workspace.json").exists():
        assert packet.verify()["schema"] == "case-0011-blind-integrity-v1"
