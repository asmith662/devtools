# Copyright (c) 2026
# ruff: noqa: D103, S101, EM101, TRY003, PLR2004, TC003, B023
"""Synthetic journal/capture fixtures; real integrity only after capture exists."""

from __future__ import annotations

import gzip
import math
from pathlib import Path

import pytest

from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.core.paths import resolve_path
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b import durability
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal, exclusive
from experiments.codex_dogfood.case_0015.freeze import REPOSITORY
from experiments.codex_dogfood.case_0015.stage_b.execute import (
    prepare_fields,
    prepare_index,
)
from experiments.codex_dogfood.case_0015.stage_b.records import PreparedFrame
from experiments.codex_dogfood.case_0016 import freeze, protocol
from experiments.codex_dogfood.case_0016.stage_b.authenticate import (
    CAPTURE,
    EXECUTION,
    STAGE_A,
    source_hashes,
)
from experiments.codex_dogfood.case_0016.stage_b.execute import (
    Progress,
    observed_ppr,
    schedule,
    universe,
)
from experiments.codex_dogfood.case_0016.stage_b.reporting import (
    publish,
    reconstruct,
    verify,
)
from experiments.task_conditioned_graph.diagnostic import definitions, render_map
from experiments.task_conditioned_graph.ranking import fuse, rank, seed_union
from experiments.task_conditioned_graph.seeds import resolve_exact_seeds
from experiments.task_conditioned_graph.view import build_reference_view, require_view


def test_journal_failure_no_retry_and_loaded_no_invocation(tmp_path: Path) -> None:
    j = Journal.start(tmp_path / "synthetic", {"execution": "synthetic-failure"})
    calls = []

    def fail() -> None:
        calls.append(1)
        raise ValueError("synthetic scientific failure")

    with pytest.raises(ValueError, match="synthetic scientific"):
        j.call("fail", {}, fail)
    with pytest.raises(ValueError, match="already entered"):
        j.call("fail", {}, fail)
    loaded = Journal.load(j.root)
    assert loaded.state["operations"][0]["status"] == "FAILED_NO_RETURN"
    assert calls == [1]
    with pytest.raises(ValueError, match="Loaded journal"):
        loaded.call("another", {}, fail)
    with pytest.raises(FileExistsError):
        Journal.start(j.root, {"execution": "synthetic-failure"})


def test_return_durable_before_summary_failure_stops(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    j = Journal.start(
        tmp_path / "synthetic",
        {"execution": "synthetic-publication", "operation_schedule": ["one"]},
    )
    j.context({})
    progress = Progress(j, 1)

    def broken() -> None:
        raise OSError("synthetic summary failure")

    monkeypatch.setattr(j, "save", broken)
    with pytest.raises(RuntimeError, match="return durable"):
        progress.call("one", {}, lambda: "native-return")
    loaded = Journal.load(j.root)
    assert loaded.state["values"]["one"] == "native-return"
    assert loaded.state["operations"][0]["status"] == "RETURNED"
    with pytest.raises(ValueError, match="already entered"):
        j.call("one", {}, lambda: "forbidden")


def test_return_record_publication_failure_never_reruns(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    j = Journal.start(
        tmp_path / "synthetic",
        {"execution": "synthetic-return-publication"},
    )
    original = durability.exclusive
    calls = []

    def refuse(path: Path, value: object) -> None:
        if "returned" in path.name:
            raise OSError("synthetic durable return failure")
        original(path, value)

    def invoke() -> int:
        calls.append(1)
        return 42

    monkeypatch.setattr(durability, "exclusive", refuse)
    with pytest.raises(OSError, match="synthetic durable return failure"):
        j.call("one", {}, invoke)
    with pytest.raises(ValueError, match="already entered"):
        j.call("one", {}, invoke)
    loaded = Journal.load(j.root)
    assert loaded.state["operations"][0]["status"] == "ENTERED"
    assert "one" not in loaded.state["values"]
    assert calls == [1]


def synthetic_capture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """514 tiny synthetic nodes, no Case 0016 text/query/content or outcomes."""
    source = tmp_path / "synthetic-inputs"
    source.mkdir()
    texts = {
        "source.py": "from target import f\nf()\nf()\n",
        "target.py": "def f():\n    pass\n",
        **{f"empty{i:03}.md": "" for i in range(512)},
    }
    for address, text in texts.items():
        (source / address).write_text(text, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=REPOSITORY,
        root=resolve_path(source),
        addresses=tuple(RepositoryResourceAddress(a) for a in sorted(texts)),
        maximum_resource_bytes=1024,
    )
    discovery = discover_repository_resource_addresses(
        repository=REPOSITORY,
        root=resolve_path(source),
        maximum_resource_count=1000,
        maximum_traversal_entry_count=2000,
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=tuple(r.address for r in snapshot.resources),
        ),
        snapshot=snapshot,
    )
    documents = represent_repository_text_corpus(corpus=corpus)
    rows = [
        {
            "address": str(d.resource.address),
            "document_identity": str(d.id),
            "content_identity": str(d.resource.content_identity),
            "content": d.text,
        }
        for d in documents.documents
    ]
    case = tmp_path / "synthetic-case"
    case.mkdir()
    monkeypatch.setattr(freeze, "CASE", case)
    (case / "resources.json.gz").write_bytes(gzip.compress(json_bytes(rows), mtime=0))
    metadata = {
        "repository_id": str(snapshot.repository_id),
        "snapshot_id": str(snapshot.id),
        "corpus_id": str(corpus.id),
    }
    (case / "frame.json").write_bytes(json_bytes(metadata))
    design = {
        "task_text": "from",
        "requirement_matrix": [
            {"obligation": f"O{i}", "query": "from"} for i in range(1, 7)
        ],
        "seed_policy": {"exact_locators": {f"Q{i}": [] for i in range(1, 7)}},
    }
    (case / "protocol.json").write_bytes(json_bytes(design))
    root = case / "stage_b" / "attempts" / EXECUTION
    root.parent.parent.mkdir(parents=True)
    schedule_path = root.parent.parent / "operation_schedule.json"
    exclusive(schedule_path, {"operations": schedule(rows)})
    marker = {
        "execution": EXECUTION,
        "stage_a": STAGE_A,
        "frame": metadata,
        "protocol_sha256": digest(binary(case / "protocol.json")),
        "initial_counts": protocol.COUNTS,
        "implementation_sha256": source_hashes(),
        "operation_schedule": schedule(rows),
        "schedule_sha256": digest(binary(schedule_path)),
        "authentication": {"fixture": "SYNTHETIC ONLY"},
    }
    j = Journal.start(root, marker)
    frame = j.call("frame:prepare", {}, lambda: PreparedFrame(documents, snapshot))
    fields = j.call("lexical:fields", {}, lambda: prepare_fields(frame))
    state = j.call("lexical:index", {}, lambda: prepare_index(frame, fields))
    modules = j.call("ri:module-universe", {}, lambda: universe(snapshot))
    refs = []
    for address in ("source.py", "target.py"):
        a = RepositoryResourceAddress(address)
        result = j.call(
            "ri:references:" + address,
            {},
            lambda: derive_python_declaration_references(
                snapshot,
                resource_address=a,
                module_universe=modules,
                source_interpretations=tuple(
                    i for i in modules.interpretations if i.resource.address == a
                ),
            ),
        )
        refs.extend(result.references)
    view = j.call(
        "graph:construct",
        {},
        lambda: build_reference_view(snapshot, tuple(refs)),
    )
    j.call("graph:validate", {}, lambda: require_view(snapshot, view))
    for i in range(1, 7):
        lexical = j.call(
            f"query:Q{i}:A",
            {},
            lambda: retrieve_repository_text_documents_by_bm25(
                query=analyze_repository_text_lexical_query(text="from"),
                index=state.content,
                maximum_results=514,
            ),
        )
        exact = j.call(
            f"query:Q{i}:exact",
            {},
            lambda: resolve_exact_seeds(snapshot, "from", ()),
        )
        j.call(
            f"query:Q{i}:seeds",
            {},
            lambda: seed_union(snapshot, lexical, exact.resources),
        )
        observed = j.call(
            f"query:Q{i}:B",
            {},
            lambda: observed_ppr(
                lambda: rank(snapshot, view, lexical, exact.resources),
            ),
        )
        ranked = observed["ranking"]
        assert (
            next(
                s for s in ranked.states if str(s.address) == "source.py"
            ).stationary_mass
            > 0
        )
        assert [str(r.address) for r in ranked.resources] == ["target.py"]
        assert len(observed["kernel_observations"]) == 1
        j.call(f"query:Q{i}:C", {}, lambda: fuse(ranked))
        projected = j.call(f"query:Q{i}:definitions", {}, lambda: definitions(ranked))
        j.call(f"query:Q{i}:map", {}, lambda: render_map(projected))
    j.call(
        "query:reference",
        {},
        lambda: retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text="from"),
            index=state.content,
            maximum_results=514,
        ),
    )
    j.complete()
    exclusive(
        root / "capture_costs.json",
        {
            "journal_publication_durability_ns": j.overhead_ns,
            "capture_wall_ns": 1,
            "progress_records": 0,
        },
    )
    return root


def test_complete_synthetic_reader_flow_rrf_maps_replay_tamper_overwrite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = synthetic_capture(tmp_path, monkeypatch)
    summary, _, _ = reconstruct(root)
    for row in summary["queries"]:
        assert row["seed_only_count"] == 1
        assert row["nonseed_B_members"] == 1
        assert row["B_candidates"] == 1
        assert math.isclose(row["stationary_mass"], 1)
        assert row["PPR_final_delta"] <= 1e-10
    publish(root)
    verify(root)
    with pytest.raises(FileExistsError, match="overwrite"):
        publish(root)
    review = root / "STAGE_B_REVIEW.md"
    review.write_bytes(review.read_bytes() + b"tamper")
    with pytest.raises(ValueError, match="integrity"):
        verify(root)
    entered = root / "operations" / "000001.entered.json"
    value = read_json(entered)
    value["frame"] = {"snapshot_id": "foreign"}
    entered.write_bytes(json_bytes(value))
    with pytest.raises(ValueError, match="chain/frame"):
        Journal.load(root)


def test_real_complete_integrity_reader() -> None:
    if not (CAPTURE / "integrity.json").exists():
        pytest.skip(
            "Authoritative capture has not run; synthetic tests are independent",
        )
    verify(CAPTURE)
