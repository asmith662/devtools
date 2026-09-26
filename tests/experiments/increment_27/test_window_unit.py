# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004
"""Falsification checks for the frozen lexical-window retrieval unit."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

import pytest

import experiments.increment_27.window_unit as window_module
from experiments.increment_27.window_pool import candidate_surface
from experiments.increment_27.window_unit import (
    _digest,
    audit_saved_baseline,
    build_window_freeze,
    score_window_content,
    source_windows,
)

if TYPE_CHECKING:
    from experiments.increment_25.development import SnapshotCorpus

ROOT = Path(__file__).resolve().parents[3] / "experiments" / "increment_27"


def test_window_contract_and_saved_canonical_equivalence() -> None:
    """The control is exactly the saved canonical resource ranking."""
    cases, sealed = audit_saved_baseline(ROOT)
    freeze = build_window_freeze(ROOT)
    payload = cast("dict[str, Any]", freeze["payload"])
    assert len(cases) == 24
    assert len(sealed) == 14
    assert not set(sealed) & {row["case_id"] for row in cases}
    assert freeze["content_identity"] == _digest(freeze["payload"])
    assert payload["window_tokens"] == 256
    assert payload["overlap_tokens"] == 32
    assert payload["capacity"] == 5
    assert payload["heldout_execution"] is False


def test_complete_window_coverage_and_stable_identity() -> None:
    """Overlap and final partial windows retain every token and source gap."""
    content = "  " + " ".join(f"T{i}" for i in range(500)) + "!!!"
    windows = source_windows(
        content=content, address="src/a.py", parent_snapshot_sha="parent"
    )
    assert [(w.token_start, w.token_end) for w in windows] == [
        (0, 256),
        (224, 480),
        (448, 500),
    ]
    assert windows[0].char_start == 0
    assert windows[-1].char_end == len(content)
    assert [
        token
        for i in range(500)
        for token in [f"t{i}"]
        if token not in {term for w in windows for term in w.terms}
    ] == []
    assert all(
        windows[i].char_end >= windows[i + 1].char_start
        for i in range(len(windows) - 1)
    )
    assert windows == source_windows(
        content=content, address="src/a.py", parent_snapshot_sha="parent"
    )
    assert (
        windows[0].identity
        != source_windows(
            content=content, address="src/b.py", parent_snapshot_sha="parent"
        )[0].identity
    )
    assert (
        windows[0].identity
        != source_windows(
            content=content, address="src/a.py", parent_snapshot_sha="other"
        )[0].identity
    )


def test_empty_short_and_boundary_windows() -> None:
    """No-token resources have no content windows; short resources get one."""
    assert not source_windows(content="", address="a.py", parent_snapshot_sha="p")
    assert not source_windows(content="...", address="a.py", parent_snapshot_sha="p")
    short = source_windows(content="\nFoo.\n", address="a.py", parent_snapshot_sha="p")
    assert len(short) == 1
    assert short[0].text == "\nFoo.\n"
    assert short[0].terms == ("foo",)
    exact = source_windows(
        content=" ".join(["x"] * 256), address="a.py", parent_snapshot_sha="p"
    )
    assert len(exact) == 1
    one_more = source_windows(
        content=" ".join(["x"] * 257), address="a.py", parent_snapshot_sha="p"
    )
    assert [(w.token_start, w.token_end) for w in one_more] == [(0, 256), (224, 257)]


def test_canonical_query_scoring_and_no_unmatched_positive() -> None:
    """Window BM25 scores only query-bearing windows with canonical terms."""
    windows = source_windows(
        content="alpha beta gamma", address="a.py", parent_snapshot_sha="p"
    ) + source_windows(content="delta", address="b.py", parent_snapshot_sha="p")
    scores = score_window_content(windows=windows, query_terms=("alpha",))
    assert set(scores) == {windows[0].identity}
    assert scores[windows[0].identity]["score"] > 0
    assert scores[windows[0].identity]["contributions"][0]["term"] == "alpha"
    assert not score_window_content(windows=windows, query_terms=("absent",))


def test_resource_projection_and_corpus_order_ties(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The best content window selects each resource; corpus order breaks ties."""
    documents = tuple(
        SimpleNamespace(resource=SimpleNamespace(address=address), text=text)
        for address, text in (
            ("a.py", "target " * 300),
            ("b.py", "target " * 300),
            ("c.py", "absent"),
        )
    )
    collection = SimpleNamespace(documents=documents)
    corpus = cast(
        "SnapshotCorpus",
        SimpleNamespace(
            index=SimpleNamespace(
                corpus_statistics=SimpleNamespace(
                    collection_analysis=SimpleNamespace(document_collection=collection)
                )
            )
        ),
    )
    monkeypatch.setattr(
        window_module,
        "build_repository_text_filename_lexical_index",
        lambda **_kwargs: object(),
    )
    monkeypatch.setattr(
        window_module,
        "score_repository_text_filename_lexical_bm25",
        lambda **_kwargs: {},
    )
    result = window_module.rank_window_resources(
        corpus=corpus, parent_snapshot_sha="p", query_text="target"
    )
    ordering = cast("list[dict[str, Any]]", result["positive_resource_ordering"])
    assert [row["address"] for row in ordering] == ["a.py", "b.py"]
    assert [row["rank"] for row in ordering] == [1, 2]
    assert ordering[0]["winning_window"]["ordinal"] == 0
    assert ordering[0]["window_count"] == 2
    assert result["positive_resource_count"] == 2


def test_surface_keeps_sealed_partition() -> None:
    """The equal-capacity candidate union contains no sealed case."""
    if not (ROOT / "window_resource_rankings.json").exists():
        pytest.skip("Development rankings not yet generated.")
    pairs, freeze, window = candidate_surface(ROOT)
    assert len({(row["case_id"], row["address"]) for row in pairs}) == len(pairs)
    assert len({row["case_id"] for row in pairs}) == 24
    assert not {row["case_id"] for row in pairs} & set(
        freeze["payload"]["heldout_case_ids_sealed"]
    )
    assert all(
        row["whole_top5_rank"] is not None or row["window_top5_rank"] is not None
        for row in pairs
    )
    assert len(window["cases"]) == 24
