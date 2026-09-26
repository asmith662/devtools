# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, EM102, PLR2004, TRY003
"""Frozen development-only whole-resource versus lexical-window ablation."""

from __future__ import annotations

import hashlib
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Settings,
    analyze_repository_text_lexical_query,
)
from devtools.context.retrieval.lexical.filename import (
    build_repository_text_filename_lexical_index,
    score_repository_text_filename_lexical_bm25,
)
from devtools.context.retrieval.lexical.scoring import (
    calculate_bm25_inverse_document_frequency,
    calculate_bm25_term_contribution,
)
from experiments.increment_25.development import (
    _build_snapshot_corpus,
    _materialize_git_snapshot,
    _task_card,
    write_artifact,
)
from experiments.increment_27.depth_diagnostic import (
    _read_json,
    canonical_json_bytes,
    sha256_file,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from experiments.increment_25.development import SnapshotCorpus

WINDOW_TOKENS = 256
OVERLAP_TOKENS = 32
STRIDE_TOKENS = WINDOW_TOKENS - OVERLAP_TOKENS
FILENAME_WEIGHT = 0.25
SETTINGS = RepositoryTextLexicalBm25Settings(k1=1.2, b=0.75)
EXPECTED_PHASE0_SHA256 = (
    "846e88929234261ac8e0fc3c872b65c329bb571f129181597bae1be8a9a7b800"
)
EXPECTED_BASELINE_SHA256 = (
    "6072195afe50376722c06157ae04e8b33ed1346e4c75c763d83f22f30dd72657"
)
EXPECTED_COMPARISON_RANKINGS_SHA256 = (
    "7d566ba0e402d180b2ddfc0840f3002ec8c8337edbed0e3d14e391b717b5f46e"
)
EXPECTED_I25_FREEZE_SHA256 = (
    "23435d68aedff808084fe33c611140343870a1222bf1fcd3a8d47d175e41cfe3"
)


@dataclass(frozen=True, slots=True)
class SourceWindow:
    """One lexical-token slice and its stable parent-resource provenance."""

    identity: str
    address: str
    ordinal: int
    token_start: int
    token_end: int
    char_start: int
    char_end: int
    terms: tuple[str, ...]
    text: str


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def source_windows(
    *, content: str, address: str, parent_snapshot_sha: str
) -> tuple[SourceWindow, ...]:
    """Cover every source character and lexical token without padding or truncation."""
    spans = tuple(iter_lexical_spans(text=content))
    if not spans:
        return ()
    windows: list[SourceWindow] = []
    for ordinal, start in enumerate(range(0, len(spans), STRIDE_TOKENS)):
        end = min(start + WINDOW_TOKENS, len(spans))
        char_start = 0 if start == 0 else spans[start][2]
        char_end = len(content) if end == len(spans) else spans[end][2]
        identity = _digest(
            {
                "parent_snapshot_sha": parent_snapshot_sha,
                "address": address,
                "ordinal": ordinal,
                "token_start": start,
                "token_end": end,
                "char_start": char_start,
                "char_end": char_end,
            }
        )
        windows.append(
            SourceWindow(
                identity,
                address,
                ordinal,
                start,
                end,
                char_start,
                char_end,
                tuple(span[1] for span in spans[start:end]),
                content[char_start:char_end],
            )
        )
        if end == len(spans):
            break
    return tuple(windows)


def score_window_content(
    *, windows: Sequence[SourceWindow], query_terms: Sequence[str]
) -> dict[str, dict[str, Any]]:
    """Use canonical BM25 arithmetic with windows as the content document corpus."""
    if not windows or not query_terms:
        return {}
    frequencies = [Counter(window.terms) for window in windows]
    average_length = sum(len(window.terms) for window in windows) / len(windows)
    document_frequency = {
        term: sum(term in counts for counts in frequencies)
        for term in dict.fromkeys(query_terms)
    }
    scores: dict[str, dict[str, Any]] = {}
    for window, counts in zip(windows, frequencies, strict=True):
        contributions: list[dict[str, object]] = []
        for term in dict.fromkeys(query_terms):
            tf = counts[term]
            if tf == 0:
                continue
            df = document_frequency[term]
            idf = calculate_bm25_inverse_document_frequency(
                document_count=len(windows), document_frequency=df
            )
            score = calculate_bm25_term_contribution(
                term_frequency=tf,
                inverse_document_frequency=idf,
                document_length=len(window.terms),
                average_document_length=average_length,
                settings=SETTINGS,
            )
            contributions.append(
                {
                    "term": term,
                    "term_frequency": tf,
                    "document_frequency": df,
                    "inverse_document_frequency": idf,
                    "contribution": score,
                }
            )
        if contributions:
            scores[window.identity] = {
                "score": sum(
                    cast("float", item["contribution"]) for item in contributions
                ),
                "contributions": contributions,
            }
    return scores


def rank_window_resources(
    *, corpus: SnapshotCorpus, parent_snapshot_sha: str, query_text: str
) -> dict[str, object]:
    """Project max content-window score plus unchanged filename score to resources."""
    collection = corpus.index.corpus_statistics.collection_analysis.document_collection
    query = analyze_repository_text_lexical_query(text=query_text)
    filename_index = build_repository_text_filename_lexical_index(
        document_collection=collection
    )
    filename_contributions = score_repository_text_filename_lexical_bm25(
        query=query, index=filename_index, settings=SETTINGS
    )
    all_windows: list[SourceWindow] = []
    by_address: dict[str, tuple[SourceWindow, ...]] = {}
    for document in collection.documents:
        address = str(document.resource.address)
        windows = source_windows(
            content=document.text,
            address=address,
            parent_snapshot_sha=parent_snapshot_sha,
        )
        by_address[address] = windows
        all_windows.extend(windows)
    window_scores = score_window_content(
        windows=all_windows, query_terms=query.normalized_terms
    )
    ranked: list[tuple[int, dict[str, object]]] = []
    for position, document in enumerate(collection.documents):
        address = str(document.resource.address)
        windows = by_address[address]
        positive_windows = [
            window for window in windows if window.identity in window_scores
        ]
        winning = (
            min(
                positive_windows,
                key=lambda window: (
                    -cast("float", window_scores[window.identity]["score"]),
                    window.ordinal,
                ),
            )
            if positive_windows
            else None
        )
        content_score = (
            cast("float", window_scores[winning.identity]["score"]) if winning else 0.0
        )
        filename_terms = filename_contributions.get(id(document), ())
        filename_score = sum(item.contribution for item in filename_terms)
        score = content_score + FILENAME_WEIGHT * filename_score
        if score <= 0:
            continue
        winning_record: dict[str, object] | None = None
        if winning is not None:
            winning_record = {
                "identity": winning.identity,
                "ordinal": winning.ordinal,
                "token_start": winning.token_start,
                "token_end": winning.token_end,
                "char_start": winning.char_start,
                "char_end": winning.char_end,
                "text_sha256": hashlib.sha256(winning.text.encode("utf-8")).hexdigest(),
                "text": winning.text,
                "content_score": content_score,
                "query_term_contributions": window_scores[winning.identity][
                    "contributions"
                ],
            }
        ranked.append(
            (
                position,
                {
                    "address": address,
                    "score": score,
                    "content_score": content_score,
                    "filename_score": filename_score,
                    "weighted_filename_score": FILENAME_WEIGHT * filename_score,
                    "filename_term_contributions": [
                        {
                            "term": item.normalized_term,
                            "contribution": item.contribution,
                        }
                        for item in filename_terms
                    ],
                    "winning_window": winning_record,
                    "window_count": len(windows),
                },
            )
        )
    ranked.sort(key=lambda item: (-cast("float", item[1]["score"]), item[0]))
    return {
        "corpus_resource_count": len(collection.documents),
        "lexical_window_count": len(all_windows),
        "total_window_tokens": sum(len(window.terms) for window in all_windows),
        "positive_resource_count": len(ranked),
        "resource_window_counts": {
            address: len(windows) for address, windows in by_address.items()
        },
        "positive_resource_ordering": [
            {"rank": rank, **item}
            for rank, (_position, item) in enumerate(ranked, start=1)
        ],
    }


def audit_saved_baseline(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Require exact saved canonical scores/order without rerunning baseline."""
    for filename, expected in (
        ("experiment_freeze.json", EXPECTED_PHASE0_SHA256),
        ("canonical_positive_lexical_rankings.json", EXPECTED_BASELINE_SHA256),
        ("lexical_comparison_rankings.json", EXPECTED_COMPARISON_RANKINGS_SHA256),
    ):
        if sha256_file(root / filename) != expected:
            raise ValueError(f"Saved canonical input changed: {filename}.")
    population = _read_json(root / "experiment_freeze.json")
    baseline = _read_json(root / "canonical_positive_lexical_rankings.json")
    comparison = _read_json(root / "lexical_comparison_rankings.json")
    development = [
        str(row["case_id"])
        for row in cast(
            "list[dict[str, object]]",
            cast(
                "dict[str, object]",
                cast("dict[str, object]", population["payload"])["source_population"],
            )["development_cases"],
        )
    ]
    heldout = cast(
        "list[str]",
        cast(
            "dict[str, object]",
            cast("dict[str, object]", population["payload"])[
                "increment_27_confirmation"
            ],
        )["case_ids"],
    )
    cases = cast("list[dict[str, Any]]", baseline["cases"])
    comparison_cases = cast("list[dict[str, Any]]", comparison["cases"])
    if (
        len(development) != 24
        or len(heldout) != 14
        or set(development) & set(heldout)
        or [row["case_id"] for row in cases] != development
        or [row["case_id"] for row in comparison_cases] != development
    ):
        raise ValueError(
            "Saved baseline partition differs from the frozen 24/14 split."
        )
    for case, compared in zip(cases, comparison_cases, strict=True):
        if (
            case["parent_snapshot_sha"] != compared["parent_snapshot_sha"]
            or case["information_need"]["lexical_query"] != compared["query_text"]
            or case["corpus_resource_count"] != compared["corpus_resource_count"]
        ):
            raise ValueError("Saved canonical case identity differs.")
        raw = case["positive_lexical_ordering"]
        enriched = compared["rankings"]["canonical"]
        if len(raw) != len(enriched) or any(
            (a["address"], a["rank"], a["score"])
            != (b["address"], b["rank"], b["score"])
            for a, b in zip(raw, enriched, strict=True)
        ):
            raise ValueError("Saved canonical scores or ordering differ.")
    return cases, heldout


def build_window_freeze(root: Path) -> dict[str, object]:
    """Freeze representation choices before retrieval or new judgment reuse."""
    cases, heldout = audit_saved_baseline(root)
    i25_path = root.parent / "increment_25" / "task_population_freeze.json"
    if sha256_file(i25_path) != EXPECTED_I25_FREEZE_SHA256:
        raise ValueError("Source task-card population freeze changed.")
    payload: dict[str, object] = {
        "phase0_freeze_sha256": EXPECTED_PHASE0_SHA256,
        "canonical_baseline_sha256": EXPECTED_BASELINE_SHA256,
        "canonical_comparison_rankings_sha256": EXPECTED_COMPARISON_RANKINGS_SHA256,
        "increment_25_task_population_sha256": EXPECTED_I25_FREEZE_SHA256,
        "development_case_ids": [row["case_id"] for row in cases],
        "heldout_case_ids_sealed": heldout,
        "baseline": "saved canonical full positive resource ranking; no rerun",
        "query": "exact frozen lexical_query; canonical Unicode word-span casefold; distinct terms",
        "window_unit": "256 canonical lexical content tokens from raw parent-snapshot resource source",
        "window_tokens": WINDOW_TOKENS,
        "overlap_tokens": OVERLAP_TOKENS,
        "stride_tokens": STRIDE_TOKENS,
        "coverage": "ordered overlapping windows from token zero, final nonempty partial window retained, no padding; char span includes surrounding gaps to cover all source text when lexical tokens exist",
        "short_resource": "one window containing all lexical tokens and complete source text",
        "empty_or_no_lexical_token_resource": "zero windows; filename-stem evidence remains available",
        "identity": "SHA-256 of parent snapshot, resource address, ordinal, token and character half-open spans",
        "scoring": {
            "formula": "canonical Lucene-style BM25 arithmetic on window content corpus; k1=1.2, b=0.75, distinct query terms",
            "content_document_count": "all nonempty windows",
            "filename_field": "unchanged resource-level filename-stem BM25",
            "filename_weight": FILENAME_WEIGHT,
            "positive": "positive combined score from content-window or filename evidence",
        },
        "projection": "maximum positive content-window score per resource plus 0.25 resource-level filename score; earliest window ordinal wins exact content ties",
        "resource_ties": "canonical corpus resource order after descending combined score",
        "capacity": 5,
        "new_judgment_origin_blind": True,
        "heldout_execution": False,
    }
    return {
        "schema": "devtools-i27-window-unit-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_window_unit(root: Path) -> dict[str, object]:
    """Persist the immutable experimental contract before ranking."""
    value = build_window_freeze(root)
    path = root / "window_unit_freeze.json"
    if path.exists() and _read_json(path) != value:
        raise ValueError("Existing window-unit freeze differs.")
    write_artifact(path=path, payload=value)
    return value


def run_window_development(*, repository_root: Path, root: Path) -> dict[str, object]:
    """Run only the frozen development cases; never load usefulness labels."""
    freeze = build_window_freeze(root)
    if _read_json(root / "window_unit_freeze.json") != freeze:
        raise ValueError("Window-unit contract must be frozen before execution.")
    baseline_cases, _heldout = audit_saved_baseline(root)
    task_freeze = _read_json(
        root.parent / "increment_25" / "task_population_freeze.json"
    )
    task_cards = cast(
        "list[dict[str, object]]",
        cast("dict[str, object]", task_freeze["payload"])["task_cards"],
    )
    cards = {str(row["case_id"]): _task_card(row) for row in task_cards}
    cases: list[dict[str, object]] = []
    for baseline in baseline_cases:
        case_id = str(baseline["case_id"])
        card = cards[case_id]
        if (
            card.parent_snapshot_sha != baseline["parent_snapshot_sha"]
            or card.lexical_query != baseline["information_need"]["lexical_query"]
        ):
            raise ValueError("Development task identity differs from saved baseline.")
        with tempfile.TemporaryDirectory(
            prefix=f"devtools-i27-window-{case_id}-"
        ) as raw:
            snapshot_root = Path(raw)
            _materialize_git_snapshot(
                repository_root=repository_root,
                snapshot_sha=card.parent_snapshot_sha,
                source_roots=card.corpus_source_roots,
                destination=snapshot_root,
            )
            corpus = _build_snapshot_corpus(
                snapshot_root=snapshot_root, source_roots=card.corpus_source_roots
            )
            if len(corpus.addresses) != baseline["corpus_resource_count"]:
                raise ValueError("Historical corpus resource count changed.")
            ranking = rank_window_resources(
                corpus=corpus,
                parent_snapshot_sha=card.parent_snapshot_sha,
                query_text=card.lexical_query,
            )
            cases.append(
                {
                    "case_id": case_id,
                    "parent_snapshot_sha": card.parent_snapshot_sha,
                    "corpus_id": corpus.corpus_id,
                    "query_text": card.lexical_query,
                    **ranking,
                }
            )
    if [case["case_id"] for case in cases] != cast("dict[str, Any]", freeze["payload"])[
        "development_case_ids"
    ]:
        raise ValueError(
            "Window execution did not cover exactly the development partition."
        )
    artifact: dict[str, object] = {
        "schema": "devtools-i27-window-resource-rankings-v1",
        "freeze_identity": freeze["content_identity"],
        "cases": cases,
    }
    artifact["content_identity"] = _digest(artifact)
    path = root / "window_resource_rankings.json"
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing window rankings differ from this execution.")
    write_artifact(path=path, payload=artifact)
    return artifact
