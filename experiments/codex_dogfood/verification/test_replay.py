# Copyright (c) 2026
# ruff: noqa: S101, D103, PLR2004, COM812 -- formatter owns commas
"""Equivalence and rejection tests without the old unbounded verifier."""

from __future__ import annotations

import copy
import json
import math
from dataclasses import dataclass, replace
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any

import pytest

from devtools.context.python.function.declarations import PythonSourceRange
from devtools.context.python.function.materialization import (
    PythonFunctionSourceMaterializationError,
    _extract_source_segment,
)
from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal, pack, unpack
from experiments.codex_dogfood.case_0012.stage_b.graph import describe
from experiments.codex_dogfood.case_0016.adjudication.reviewed import (
    materialize as gold,
)
from experiments.codex_dogfood.case_0016.stage_b import authenticate as stage_a
from experiments.codex_dogfood.case_0016.stage_d import analysis, authentication

from .audit import sealed_files
from .bindings import bind
from .case_0016 import AuthenticatedInputs, Invocation
from .journal import journal_type
from .native import NativeMemo
from .rows import totals
from .spans import SourceSpans

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class PythonModuleInterpretationUniverse:
    """Small immutable fixture for the native shared-subgraph path."""

    values: tuple[Any, ...]


def test_canonical_correspondence_aliases_and_blocks() -> None:
    memo = NativeMemo()
    shared = PythonModuleInterpretationUniverse(tuple((n, str(n)) for n in range(100)))
    for value in ((shared, shared), ("offset", (1, 2), shared)):
        assert memo.corresponds(value, json_bytes(describe(value)))
    assert memo.blocks_checked > 0
    changed = describe((shared, shared))
    changed["nodes"][-1]["items"][0] = 999
    assert not memo.corresponds((shared, shared), json_bytes(changed))
    changed = describe((shared, shared))
    changed["nodes"][0]["items"][1] = {"ref": 2}
    assert not memo.corresponds((shared, shared), json_bytes(changed))
    assert not memo.corresponds(
        replace(shared, values=("bad",)),
        json_bytes(describe(shared)),
    )
    assert not memo.corresponds(-0.0, json_bytes(describe(0.0)))
    mutable = [1, 2]
    raw = json_bytes(describe(mutable))
    assert memo.corresponds(mutable, raw)
    mutable[0] = 9
    assert not memo.corresponds(mutable, raw)


@pytest.mark.parametrize("field", ["chain", "native", "canonical"])
def test_native_journal_checks(tmp_path: Path, field: str) -> None:
    root = tmp_path / "journal"
    journal = Journal.start(root, {"execution": "test", "frame": {}, "runtime": "test"})
    journal.context({"retained": (1, 2)})
    journal.call("return", {}, lambda: (3, 4))
    journal.complete()
    adapted = journal_type(NativeMemo()).load(root)
    assert adapted.state == Journal.load(root).state
    record = root / "operations/000001.returned.json"
    value = json.loads(record.read_bytes())
    if field == "chain":
        value["prior_chain_sha256"] = "bad"
    elif field == "native":
        value["native"]["sha256"] = "bad"
    else:
        value["canonical"] = pack(json_bytes(describe((999, 4))))
    record.write_bytes(json_bytes(value))
    with pytest.raises(ValueError, match=r".+"):
        journal_type(NativeMemo()).load(root)
    with pytest.raises(ValueError, match=r".+"):
        unpack({**pack(b"test"), "sha256": "bad"})


def test_span_index_exact() -> None:
    cache = SourceSpans()
    for content in ("abc\nxyz\n", "éλ\r\nhello\n", "", "last line"):
        for a, b, x, y in (
            (1, 1, 0, 1),
            (1, 2, 0, 2),
            (1, 1, 1, 2),
            (0, 1, 0, 2),
            (2, 1, 0, 0),
            (1, 1, 0, 99),
        ):
            span = PythonSourceRange(a, x, b, y)
            try:
                expected = _extract_source_segment(content, span)
            except PythonFunctionSourceMaterializationError as error:
                with pytest.raises(type(error), match=str(error).replace(".", r"\.")):
                    cache.extract(content, span)
            else:
                assert cache.extract(content, span) == expected


def test_gold_authentication_once_and_next_invocation() -> None:
    for _ in range(2):
        invocation = Invocation()
        facade = invocation.reviewed()
        assert facade.verify()["status"] == "PASS"
        facade.outputs()
        facade.construct_gold()
        assert invocation.counts["primary_authentication"] == 1
        assert invocation.counts["primary_bundle_executions"] == 1
        assert invocation.counts["primary_adversarial_bundle"] == 1
        changed = copy.deepcopy(facade.construct_gold())
        changed["primary"]["cells"][0]["label"] = "bad"
        with pytest.raises(ValueError, match=r".+"):
            facade.validate(changed)


def test_expected_bytes_and_all_semantics() -> None:
    invocation = Invocation()
    facade = invocation.reviewed()
    read = bind(authentication.read_inputs, {"m": facade})
    provenance = gold.load(analysis.PACKAGE / "trace.json")["provenance"]
    data = read(provenance)
    files = invocation.expected(AuthenticatedInputs(data, invocation.primary, None))
    assert all(
        (analysis.PACKAGE / name).read_bytes() == raw for name, raw in files.items()
    )
    result = json.loads(files["analysis.json"])
    retained = gold.load(analysis.PACKAGE / "analysis.json")
    assert result["outcome"] == retained["outcome"] == "GRAPH_HARMFUL"
    assert result["gates"] == retained["gates"]
    assert result["required_cells"] == retained["required_cells"]
    assert len(result["required_cells"]) == 36
    assert result["witnesses"] == retained["witnesses"]
    assert len(result["witnesses"]) == 22
    assert len(data["gold"]["primary"]["cells"]) == 3084
    assert invocation.counts["metrics_construction"] == 1
    assert invocation.counts["markdown_rendering"] == 1
    assert invocation.counts["stage_d_semantic_validation"] == 6


def test_resource_index_matches_scanning() -> None:
    resources = tuple(SimpleNamespace(address=s, content=s) for s in ("x", "y", "z"))
    snapshot = SimpleNamespace(resources=resources)
    memo = NativeMemo()
    assert [memo.resource(snapshot, r.address) for r in resources] == list(resources)


def test_sealed_historical_files() -> None:
    assert len(sealed_files()) == 26
    Invocation().captured_bytes()


def test_exact_row_order_and_floats() -> None:

    nodes = tuple(str(i) for i in range(514))
    weights = {(str(i % 514), str((i * 7) % 514)): math.sqrt(i + 1) for i in range(561)}
    historical = {
        n: math.fsum(
            w for (source, _), w in sorted(weights.items(), key=str) if source == n
        )
        for n in nodes
    }
    indexed = totals(weights, nodes)
    assert tuple(indexed) == tuple(historical)
    assert [v.hex() for v in indexed.values()] == [v.hex() for v in historical.values()]


def test_bulk_graph_and_new_process_state() -> None:
    shared = PythonModuleInterpretationUniverse(
        tuple((i, str(i)) for i in range(12000)),
    )
    first = NativeMemo()
    assert first.corresponds(shared, json_bytes(describe(shared)))
    assert first.corresponds(
        ("offset", shared),
        json_bytes(describe(("offset", shared))),
    )
    assert first.blocks_checked == 1
    second = NativeMemo()
    assert second.corresponds(shared, json_bytes(describe(shared)))
    assert second.blocks_checked == 0


def test_indexed_scans_exact() -> None:
    memo = NativeMemo()
    ranking = SimpleNamespace(
        states=(SimpleNamespace(address="r", stationary_mass=0.5),),
    )
    edge = SimpleNamespace(source="r", target="t")
    view = SimpleNamespace(edges=(edge,))
    assert memo.state(ranking, "r") == next(
        s.stationary_mass for s in ranking.states if s.address == "r"
    )
    assert memo.pair(view, "r", "t") is next(
        e for e in view.edges if str(e.source) == "r" and str(e.target) == "t"
    )
    assert memo.member({"r": 1, "t": 2}, "t") == "t"


def test_capture_integrity_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "integrity.json").write_bytes(b"{}")
    monkeypatch.setattr(stage_a, "CAPTURE", tmp_path)
    with pytest.raises(ValueError, match="Authoritative capture seal"):
        Invocation().captured_bytes()
