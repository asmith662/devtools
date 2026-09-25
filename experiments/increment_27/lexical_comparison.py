# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, EM102, PLR2004, TRY003
"""Development-only lexical hypotheses over frozen historical snapshots."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, cast

import bm25s  # type: ignore[import-untyped]

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.increment_25.development import (
    _build_snapshot_corpus,
    _materialize_git_snapshot,
    _task_card,
    write_artifact,
)
from experiments.increment_27.depth_diagnostic import (
    EXPECTED_DEVELOPMENT_SIZE,
    build_freeze,
    canonical_json_bytes,
    sha256_file,
)
from experiments.retrieval_identifier import expand_identifier_terms

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from experiments.increment_25.development import SnapshotCorpus

METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")
K_CHECKPOINTS = (1, 3, 5, 10, 20, 50)
RRF_K = 60
BASELINE_FILENAME_WEIGHT = 0.25
BM25_K1 = 1.2
BM25_B = 0.75
BM25_PLUS_DELTA = 0.5


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _read(path: Path) -> dict[str, object]:
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise TypeError(f"Expected object: {path}")
    return cast("dict[str, object]", result)


def build_comparison_freeze(*, output_root: Path) -> dict[str, object]:
    """Specify every ranking choice without loading usefulness outcomes."""
    phase0 = _read(output_root / "experiment_freeze.json")
    if phase0 != build_freeze(experiment_root=output_root.parent):
        raise ValueError("Increment-27 Phase-0 population freeze changed.")
    baseline_path = output_root / "canonical_positive_lexical_rankings.json"
    baseline = _read(baseline_path)
    source = cast("dict[str, object]", phase0["payload"])["source_population"]
    source = cast("dict[str, object]", source)
    cases = cast("list[dict[str, object]]", source["development_cases"])
    heldout = cast(
        "dict[str, object]",
        cast("dict[str, object]", phase0["payload"])["increment_27_confirmation"],
    )
    development_ids = [str(case["case_id"]) for case in cases]
    heldout_ids = cast("list[str]", heldout["case_ids"])
    baseline_cases = cast("list[dict[str, object]]", baseline["cases"])
    if (
        len(development_ids) != EXPECTED_DEVELOPMENT_SIZE
        or len(set(development_ids)) != EXPECTED_DEVELOPMENT_SIZE
        or len(heldout_ids) != 14
        or set(development_ids) & set(heldout_ids)
        or [case["case_id"] for case in baseline_cases] != development_ids
        or baseline["freeze_identity"] != phase0["content_identity"]
    ):
        raise ValueError("Development/held-out or canonical baseline integrity failed.")
    payload: dict[str, object] = {
        "phase0_freeze_identity": phase0["content_identity"],
        "phase0_freeze_sha256": sha256_file(output_root / "experiment_freeze.json"),
        "canonical_baseline_sha256": sha256_file(baseline_path),
        "development_case_ids": development_ids,
        "heldout_case_ids_sealed": heldout_ids,
        "methods": [
            {
                "id": "canonical",
                "source": "saved Phase-0 canonical positive ranking",
                "formula": "content Lucene BM25 + 0.25 filename-stem Lucene BM25",
                "k1": BM25_K1,
                "b": BM25_B,
            },
            {
                "id": "bm25_plus",
                "engine": "bm25s==0.3.11",
                "formula": "BM25+",
                "k1": BM25_K1,
                "b": BM25_B,
                "delta": BM25_PLUS_DELTA,
                "fields": {"content": 1.0, "filename_stem": BASELINE_FILENAME_WEIGHT},
                "tokenization": "Unicode word spans casefold; distinct query terms",
            },
            {
                "id": "identifier",
                "engine": "bm25s==0.3.11",
                "formula": "Lucene",
                "k1": BM25_K1,
                "b": BM25_B,
                "fields": {"content": 1.0, "filename_stem": BASELINE_FILENAME_WEIGHT},
                "tokenization": "exact Unicode word span plus unique snake/camel/acronym/digit subtokens; distinct query terms",
            },
            {
                "id": "path",
                "engine": "bm25s==0.3.11",
                "formula": "Lucene",
                "k1": BM25_K1,
                "b": BM25_B,
                "fields": {"full_relative_path": 1.0},
                "tokenization": "Unicode word spans casefold on full slash-separated relative path; distinct query terms",
            },
            {
                "id": "rrf",
                "inputs": ["canonical", "identifier", "path"],
                "constant": RRF_K,
                "formula": "sum 1/(60+positive_rank) for available input ranks",
            },
        ],
        "common": {
            "unit": "whole resource",
            "query": "unchanged frozen lexical_query",
            "positive": "actual query-term overlap in at least one contributing field and positive final score",
            "ties": "canonical corpus address order",
            "score_dtype": "float64 for bm25s",
            "index_backend": "numpy",
            "stem_or_stopwords": False,
            "ranking_depth": "all positive resources",
            "k_checkpoints": list(K_CHECKPOINTS),
        },
        "outcome_blind": True,
    }
    return {
        "schema": "devtools-i27-lexical-comparison-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_comparison(*, output_root: Path) -> dict[str, object]:
    """Persist the configuration before any new retrieval or label join."""
    freeze = build_comparison_freeze(output_root=output_root)
    path = output_root / "lexical_comparison_freeze.json"
    if path.exists() and _read(path) != freeze:
        raise ValueError("Existing lexical comparison freeze differs.")
    write_artifact(path=path, payload=freeze)
    return freeze


def _tokens(text: str, *, identifier: bool = False) -> list[str]:
    words = [span[0] for span in iter_lexical_spans(text=text)]
    if identifier:
        return [
            term
            for word in words
            for term in expand_identifier_terms(observed_text=word)
        ]
    return [word.casefold() for word in words]


def _score_field(
    *,
    documents: Sequence[Sequence[str]],
    query: Sequence[str],
    method: str,
) -> list[float]:
    if not documents:
        return []
    engine = bm25s.BM25(
        k1=BM25_K1,
        b=BM25_B,
        delta=BM25_PLUS_DELTA,
        method=method,
        dtype="float64",
        backend="numpy",
    )
    engine.index([list(tokens) for tokens in documents], show_progress=False)
    # BM25+ gives even nonmatching documents a delta-based score. Exclude it.
    raw = engine.get_scores(list(query)) if query else [0.0] * len(documents)
    query_set = set(query)
    return [
        float(raw[index]) if query_set.intersection(tokens) else 0.0
        for index, tokens in enumerate(documents)
    ]


def _rank_scored(
    *,
    addresses: Sequence[str],
    components: Mapping[str, Sequence[float]],
    weights: Mapping[str, float],
    query: Sequence[str],
    field_tokens: Mapping[str, Sequence[Sequence[str]]],
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    query_set = set(query)
    for index, address in enumerate(addresses):
        scores = {field: float(values[index]) for field, values in components.items()}
        final = sum(scores[field] * weights[field] for field in components)
        if final <= 0:
            continue
        matches = {
            field: sorted(query_set.intersection(field_tokens[field][index]))
            for field in components
        }
        if not any(matches.values()):
            continue
        results.append(
            {
                "address": address,
                "score": final,
                "component_scores": scores,
                "matched_terms": matches,
                "corpus_position": index,
            }
        )
    results.sort(
        key=lambda item: (
            -cast("float", item["score"]),
            cast("int", item["corpus_position"]),
        )
    )
    for rank, item in enumerate(results, start=1):
        item.pop("corpus_position")
        item["rank"] = rank
    return results


def _field_rankings(
    *, corpus: SnapshotCorpus, query_text: str
) -> dict[str, list[dict[str, object]]]:
    documents = (
        corpus.index.corpus_statistics.collection_analysis.document_collection.documents
    )
    addresses = [str(document.resource.address) for document in documents]
    content = [document.text for document in documents]
    stems = [Path(address).stem for address in addresses]
    standard_query = list(dict.fromkeys(_tokens(query_text)))
    identifier_query = list(dict.fromkeys(_tokens(query_text, identifier=True)))
    raw_fields = {
        "content": [_tokens(text) for text in content],
        "filename_stem": [_tokens(stem) for stem in stems],
    }
    plus = {
        field: _score_field(documents=values, query=standard_query, method="bm25+")
        for field, values in raw_fields.items()
    }
    expanded_fields = {
        "content": [_tokens(text, identifier=True) for text in content],
        "filename_stem": [_tokens(stem, identifier=True) for stem in stems],
    }
    expanded = {
        field: _score_field(documents=values, query=identifier_query, method="lucene")
        for field, values in expanded_fields.items()
    }
    path_fields = {"path": [_tokens(address) for address in addresses]}
    path = {
        "path": _score_field(
            documents=path_fields["path"], query=standard_query, method="lucene"
        )
    }
    weights = {"content": 1.0, "filename_stem": BASELINE_FILENAME_WEIGHT}
    return {
        "bm25_plus": _rank_scored(
            addresses=addresses,
            components=plus,
            weights=weights,
            query=standard_query,
            field_tokens=raw_fields,
        ),
        "identifier": _rank_scored(
            addresses=addresses,
            components=expanded,
            weights=weights,
            query=identifier_query,
            field_tokens=expanded_fields,
        ),
        "path": _rank_scored(
            addresses=addresses,
            components=path,
            weights={"path": 1.0},
            query=standard_query,
            field_tokens=path_fields,
        ),
    }


def _canonical_with_components(
    *, corpus: SnapshotCorpus, query_text: str,
    baseline: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Enrich the saved baseline only after exact rank and score agreement."""
    query = analyze_repository_text_lexical_query(text=query_text)
    result = retrieve_repository_text_documents_by_bm25(
        query=query,
        index=corpus.index,
        maximum_results=max(1, len(corpus.addresses)),
    )
    if len(result.matches) != len(baseline):
        raise ValueError("Canonical baseline length changed.")
    records: list[dict[str, object]] = []
    for rank, (match, saved) in enumerate(zip(result.matches, baseline, strict=True), start=1):
        address = str(match.document_statistics.analysis.document.resource.address)
        if (
            saved["address"] != address
            or saved["rank"] != rank
            or saved["score"] != match.score
        ):
            raise ValueError("Canonical baseline score or ordering changed.")
        records.append(
            {
                "address": address,
                "rank": rank,
                "score": match.score,
                "component_scores": {
                    "content": match.content_score,
                    "filename_stem": match.filename_score,
                    "weighted_filename_stem": match.weighted_filename_score,
                },
            }
        )
    return records


def _rrf(
    *, rankings: Mapping[str, Sequence[Mapping[str, object]]], addresses: Sequence[str]
) -> list[dict[str, object]]:
    by_address: dict[str, dict[str, int]] = {}
    for method in ("canonical", "identifier", "path"):
        for item in rankings[method]:
            address = str(item["address"])
            by_address.setdefault(address, {})[method] = int(cast("int", item["rank"]))
    scores = {
        address: sum(1 / (RRF_K + rank) for rank in ranks.values())
        for address, ranks in by_address.items()
    }
    ordered = sorted(
        by_address, key=lambda address: (-scores[address], addresses.index(address))
    )
    return [
        {
            "rank": rank,
            "address": address,
            "score": scores[address],
            "source_ranks": by_address[address],
        }
        for rank, address in enumerate(ordered, start=1)
    ]


def run_comparison(*, repository_root: Path, output_root: Path) -> dict[str, object]:
    """Run exactly the frozen 24 cases; no judgment artifacts are read."""
    freeze = build_comparison_freeze(output_root=output_root)
    if _read(output_root / "lexical_comparison_freeze.json") != freeze:
        raise ValueError("Lexical configuration must be frozen before ranking.")
    baseline = _read(output_root / "canonical_positive_lexical_rankings.json")
    baseline_cases = cast("list[dict[str, object]]", baseline["cases"])
    task_freeze = _read(
        output_root.parent / "increment_25" / "task_population_freeze.json"
    )
    task_cards = cast(
        "list[dict[str, object]]",
        cast("dict[str, object]", task_freeze["payload"])["task_cards"],
    )
    cards = {str(item["case_id"]): _task_card(item) for item in task_cards}
    allowed = cast(
        "list[str]",
        cast("dict[str, object]", freeze["payload"])["development_case_ids"],
    )
    cases: list[dict[str, object]] = []
    for baseline_case in baseline_cases:
        case_id = str(baseline_case["case_id"])
        if case_id != allowed[len(cases)]:
            raise ValueError(
                "Attempted execution outside ordered development partition."
            )
        card = cards[case_id]
        if (
            card.parent_snapshot_sha != baseline_case["parent_snapshot_sha"]
            or card.lexical_query
            != cast("dict[str, object]", baseline_case["information_need"])[
                "lexical_query"
            ]
        ):
            raise ValueError("Baseline and frozen task identity differ.")
        with tempfile.TemporaryDirectory(
            prefix=f"devtools-i27-lexical-{case_id}-"
        ) as raw:
            root = Path(raw)
            _materialize_git_snapshot(
                repository_root=repository_root,
                snapshot_sha=card.parent_snapshot_sha,
                source_roots=card.corpus_source_roots,
                destination=root,
            )
            corpus = _build_snapshot_corpus(
                snapshot_root=root, source_roots=card.corpus_source_roots
            )
            addresses = [str(address) for address in corpus.addresses]
            if len(addresses) != baseline_case["corpus_resource_count"]:
                raise ValueError(
                    "Historical corpus size changed from canonical baseline."
                )
            rankings = {
                "canonical": _canonical_with_components(
                    corpus=corpus,
                    query_text=card.lexical_query,
                    baseline=cast(
                        "list[dict[str, object]]",
                        baseline_case["positive_lexical_ordering"],
                    ),
                ),
                **_field_rankings(corpus=corpus, query_text=card.lexical_query),
            }
            rankings["rrf"] = _rrf(rankings=rankings, addresses=addresses)
            if any(
                len({str(item["address"]) for item in items}) != len(items)
                for items in rankings.values()
            ):
                raise ValueError("Duplicate ranked resource address.")
            cases.append(
                {
                    "case_id": case_id,
                    "parent_snapshot_sha": card.parent_snapshot_sha,
                    "corpus_id": corpus.corpus_id,
                    "corpus_resource_count": len(addresses),
                    "query_text": card.lexical_query,
                    "rankings": rankings,
                }
            )
    if len(cases) != EXPECTED_DEVELOPMENT_SIZE:
        raise ValueError("Incomplete development partition.")
    artifact: dict[str, object] = {
        "schema": "devtools-i27-lexical-comparison-rankings-v1",
        "configuration_identity": freeze["content_identity"],
        "cases": cases,
    }
    artifact["content_identity"] = _digest(artifact)
    write_artifact(
        path=output_root / "lexical_comparison_rankings.json", payload=artifact
    )
    return artifact
