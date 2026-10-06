# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, T201, TRY003 -- bounded artifact CLI
"""Freeze analyzer bytes before an outcome-free retained-development token check."""

from __future__ import annotations

import json
import unicodedata

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    put_json,
    read_json,
)
from experiments.identifier_sparse.analysis import ANALYZER_SEMANTICS, iter_terms
from experiments.retrieval_identifier import analyze_identifier_query


def record() -> dict[str, object]:
    """Pin mechanism first; inspect only three saved development query strings."""
    root = ROOT / "experiments/identifier_sparse"
    if (root / "analyzer_definition.json").exists() or (
        root / "historical_diagnostic.json"
    ).exists():
        raise FileExistsError("Analyzer definition/diagnostic already frozen.")
    sources = [
        root / name
        for name in ("__init__.py", "analysis.py", "index.py", "retrieval.py")
    ]
    sources.append(ROOT / "experiments/retrieval_identifier.py")
    definition = {
        "schema": "r1-analyzer-definition-v1",
        "semantics": ANALYZER_SEMANTICS,
        "unicode_version": unicodedata.unidata_version,
        "source_sha256": {
            path.relative_to(ROOT).as_posix(): digest(binary(path)) for path in sources
        },
        "rules": "Canonical Unicode word spans; whole casefold first; underscore pieces; lower-to-upper, acronym-before-Capitalized and alpha/digit boundaries; unique casefold terms per span; independent occurrence frequency retained; distinct query terms; no semantic rewriting.",
        "parameters": {"k1": 1.2, "b": 0.75, "filename_weight": 0.25},
        "frozen_before": "historical diagnostic and prospective execution; no tuning from outcomes",
    }
    put_json(root / "analyzer_definition.json", definition)
    source = ROOT / "experiments/increment_27/lexical_comparison_rankings.json"
    saved = read_json(source)
    rows = []
    for case in saved["cases"][:3]:
        text = case["query_text"]
        old = tuple(
            item.normalized_term for item in analyze_identifier_query(text=text)
        )
        current = tuple(iter_terms(text))
        if old != current:
            raise ValueError("R1 diverges from the retained identifier analyzer.")
        rows.append(
            {
                "case_id": case["case_id"],
                "query": text,
                "canonical_terms": [item[1] for item in iter_lexical_spans(text=text)],
                "identifier_terms": current,
                "historical_term_stream_equal": True,
            }
        )
    result = {
        "schema": "r1-retrospective-mechanical-diagnostic-v1",
        "analyzer_definition_sha256": digest(binary(root / "analyzer_definition.json")),
        "source_sha256": digest(binary(source)),
        "rows": rows,
        "interpretation": "Exact query-term parity with retained Increment 27. No labels joined, no historical retrieval re-executed and no effectiveness claim. Increment 27 already used whole plus subtokens, not split-only. R1 replaces bm25s with canonical shared arithmetic; no numerical historical replay claimed.",
        "R2": "Mandatory regardless of R1 outcome.",
    }
    put_json(root / "historical_diagnostic.json", result)
    return {"queries_checked": len(rows), "status": "TERM PARITY; NOT EFFECTIVENESS"}


if __name__ == "__main__":
    print(json.dumps(record()))
