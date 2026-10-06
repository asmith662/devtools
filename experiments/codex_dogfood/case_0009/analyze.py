# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, EM102, PLR0912, PLR0915, PLR2004, T201, TRY003 -- bounded scientific artifact analysis
"""Join frozen R1 captures with clean gold; never execute another treatment."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import itertools
import json
import math
import statistics
from collections import Counter
from pathlib import PurePosixPath
from typing import Any

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans
from devtools.context.retrieval.lexical.scoring import (
    calculate_bm25_inverse_document_frequency,
    calculate_bm25_term_contribution,
)
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from experiments.codex_dogfood.case_0009.adjudication.stage_c import (
    statistics as gold_statistics,
)
from experiments.codex_dogfood.case_0009.adjudication.stage_c import (
    validate as validate_gold,
)
from experiments.codex_dogfood.case_0009.artifacts import (
    CASE,
    binary,
    digest,
    git,
    json_bytes,
    read_json,
)
from experiments.codex_dogfood.case_0009.freeze import load_inputs
from experiments.codex_dogfood.case_0009.protocol import TASK, treatment
from experiments.identifier_sparse.analysis import ANALYZER_SEMANTICS, query_terms
from experiments.identifier_sparse.index import build_field
from experiments.identifier_sparse.retrieval import SETTINGS
from experiments.retrieval_identifier import expand_identifier_terms

CHAIN = (
    (
        "eb4060ff8ffd1ff0bf18e11c47d162a6c02bd0f2",
        "Add identifier-aware sparse retrieval experiment",
    ),
    (
        "44638db3980e63416094e91cbf901abb08777d24",
        "Capture R1 treatments and blind adjudication packet",
    ),
    (
        "c2d6f3224bbb7c3c4535c8deaefe0c003f94a563",
        "Repair Case 0009 blind packet integrity",
    ),
    (
        "092f9a760c1ec1ec29db5986a97b702ba5e1eff2",
        "Freeze Case 0009 blind obligation judgments",
    ),
)
GOLD_HASHES = {
    "judgments.json": "81161a361216a8c24d68688de90e134982ffe29c159e30a7d85eea169166d257",
    "gold_statistics.json": "c8098071f531ebf2f65b7a3929f1ad88005f7d5d91ca10be05e6ff8f8bc0522a",
    "judgments.sha256": "2e55e8629e3447a186feb78cf53b96a225171dc8e48079260a733ed7c47fb46c",
    "METHOD.md": "d0c5a4322b4a8f5b549a6984152f0a2a5b2a8325aa7d6ef3ad70a3cb02686e10",
    "build_judgments.py": "eaaf536b51d01d3dbb806604f731abb30a4a64afb9025911dd9c3f3b69aa651c",
    "stage_c.py": "cdc6edea6a17d6776e6ab31b6d19cba1e92964823a6cf078bf8c7b0e34747d09",
    "test_stage_c.py": "422e8b77b30b8ce99a7f8bf31b4ff3c192231dedc0aee2fb9f83ad79e1e77be8",
    "stage_c_pytest.ini": "149ea333c05ca2075d2872171beeb273994a352293358a74a14f4f50f08af550",
}
PACKET_HASHES = {
    "resources.json.gz": "c23e0908d664e9c81149dec54a81aeeff3ef25fa9624c342cfac9bda44be5b37",
    "manifest.json": "a68bf46bec7e7875e9321986864bbe3cb12cec80ecc167992d770610f48ae932",
    "integrity.json": "edce2e60cea2e5dee279ad60aa9d97b9ac3fd95514167f242a8f87d78e8e9849",
}
PAYLOAD_HASH = "29e09439ad7812b96f7a10ccb40e34548e842a56ab9e90306fcac8a299349c99"
LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "UNRESOLVED")


async def verify_commits() -> dict[str, Any]:
    """Read only named frozen Git blobs and verify their ordered ancestry."""
    for index, (commit, subject) in enumerate(CHAIN):
        if (await git("show", "-s", "--format=%s", commit)).decode().strip() != subject:
            raise ValueError("Frozen checkpoint subject differs.")
        if index:
            await git("merge-base", "--is-ancestor", CHAIN[index - 1][0], commit)
    await git("merge-base", "--is-ancestor", CHAIN[-1][0], "HEAD")
    for name, expected in {**GOLD_HASHES, **PACKET_HASHES}.items():
        path = "experiments/codex_dogfood/case_0009/adjudication/" + name
        committed = await git("show", CHAIN[-1][0] + ":" + path)
        if (
            digest(committed) != expected
            or digest(binary(CASE / "adjudication" / name)) != expected
        ):
            raise ValueError(f"Frozen adjudication bytes differ: {name}")
    for commit, names in (
        (
            CHAIN[0][0],
            ("treatment.json", "inputs.pkl.gz", "pre_execution.json", "integrity.json"),
        ),
        (
            CHAIN[1][0],
            (
                "results.json.gz",
                "costs.json",
                "execution_started.json",
                "stage_b_integrity.json",
            ),
        ),
    ):
        for name in names:
            path = "experiments/codex_dogfood/case_0009/" + name
            if digest(await git("show", commit + ":" + path)) != digest(
                binary(CASE / name)
            ):
                raise ValueError(f"Frozen treatment checkpoint differs: {name}")
    return {
        "checkpoints": [{"commit": c, "subject": s} for c, s in CHAIN],
        "ordered_ancestry": True,
        "gold_sha256": GOLD_HASHES,
        "packet_sha256": PACKET_HASHES,
    }


def partition(a: set[Any], b: set[Any], universe: set[Any]) -> dict[str, Any]:
    """Preserve every member of a disjoint paired reach partition."""
    return {
        "both": sorted(a & b),
        "A_only": sorted(a - b),
        "B_only": sorted(b - a),
        "neither": sorted(universe - (a | b)),
    }


def best_completion(
    alternatives: list[dict[str, Any]], ranks: dict[str, int]
) -> dict[str, Any]:
    """Require ALL members of one accepted alternative, never mix witnesses."""
    choices = []
    for alt in alternatives:
        addresses = [w["resource"]["address"] for w in alt["witnesses"]]
        missing = sorted(set(addresses) - ranks.keys())
        choices.append(
            {
                "alternative": alt["identity"],
                "resources": sorted(addresses),
                "missing": missing,
                "depth": None if missing else max(ranks[p] for p in addresses),
            }
        )
    valid = [item for item in choices if item["depth"] is not None]
    best = (
        min(valid, key=lambda item: (item["depth"], item["alternative"]))
        if valid
        else None
    )
    return {
        "depth": best["depth"] if best else None,
        "best_alternative": best["alternative"] if best else None,
        "alternatives": choices,
    }


def validate_join(
    results: dict[str, Any],
    gold: dict[str, Any],
    manifest: dict[str, Any],
    packet: dict[str, Any],
    resources: list[dict[str, Any]],
) -> None:
    """Validate both result universes and the complete gold frame before metrics."""
    if results["schema"] != "case-0009-r1-results-v1" or results["analyzers"] != {
        "A": "unicode-word-span-casefold-v1",
        "B": ANALYZER_SEMANTICS,
    }:
        raise ValueError("Treatment analyzer identity differs.")
    frame = gold["frame"]
    for key in ("repository_id", "snapshot_id", "corpus_id"):
        if frame[key] != manifest[key] or frame[key] != packet[key]:
            raise ValueError(f"Join frame mismatch: {key}")
    if (
        results["snapshot_id"] != frame["snapshot_id"]
        or results["corpus_id"] != frame["corpus_id"]
    ):
        raise ValueError("Treatment result frame differs.")
    if (
        frame["task_identity"] != "case-0009-explicit-assessment-bridge"
        or gold["task"] != TASK
        or packet["task"] != TASK
    ):
        raise ValueError("Task identity/text mismatch.")
    identity = {r["address"]: r["content_identity"] for r in manifest["resources"]}
    if (
        len(identity) != 531
        or len(resources) != 531
        or {r["address"]: r["content_identity"] for r in resources} != identity
    ):
        raise ValueError("Resource frame mismatch.")
    if (
        len(gold["resources"]) != 531
        or {r["address"]: r["content_identity"] for r in gold["resources"]} != identity
    ):
        raise ValueError("Gold resource identity mismatch.")
    validate_gold(gold, packet, resources)
    expected_obligations = {o["id"] for o in treatment()["obligations"]}
    if (
        len(gold["obligations"]) != 9
        or {o["identity"] for o in gold["obligations"]} != expected_obligations
    ):
        raise ValueError("Gold obligation identities differ.")
    queries = {
        "global": (None, TASK),
        **{
            o["id"] + "-query": (o["id"], o["query"])
            for o in treatment()["obligations"]
        },
    }
    if set(results["arms"]) != {"A", "B"}:
        raise ValueError("Arm identities differ.")
    order = {r["address"]: i for i, r in enumerate(manifest["resources"])}
    for arm, lanes in results["arms"].items():
        if set(lanes) != set(queries):
            raise ValueError("Query lane identities differ.")
        for key, lane in lanes.items():
            if (lane["obligation"], lane["query_text"]) != queries[key]:
                raise ValueError("Query/obligation text differs.")
            terms = (
                list(query_terms(lane["query_text"]))
                if arm == "B"
                else list(
                    dict.fromkeys(
                        span[1] for span in iter_lexical_spans(text=lane["query_text"])
                    )
                )
            )
            if lane["query_terms"] != terms:
                raise ValueError("Captured query analyzer differs.")
            seen = set()
            previous = (float("-inf"), -1)
            for rank, row in enumerate(lane["rows"], 1):
                address = row["address"]
                sorting = (-row["score"], order[address])
                if (
                    address in seen
                    or identity.get(address) != row["content_identity"]
                    or row["rank"] != rank
                    or row["score"] <= 0
                    or sorting < previous
                ):
                    raise ValueError("Invalid positive result identity/order.")
                seen.add(address)
                previous = sorting
                for field in ("content", "filename"):
                    contributions = row[field + "_terms"]
                    if len({t["term"] for t in contributions}) != len(
                        contributions
                    ) or not {t["term"] for t in contributions} <= set(terms):
                        raise ValueError("Invalid field terms.")
                    if not math.isclose(
                        sum(t["contribution"] for t in contributions),
                        row[field + "_score"],
                        abs_tol=1e-10,
                    ):
                        raise ValueError("Field contribution sum differs.")
                if not math.isclose(
                    row["content_score"] + 0.25 * row["filename_score"],
                    row["score"],
                    abs_tol=1e-10,
                ):
                    raise ValueError("Combined score differs.")


def validate_statistics(
    results: dict[str, Any], resources: list[dict[str, Any]]
) -> dict[str, Any]:
    """Reconstruct field statistics only, never rerank or collect new costs."""
    for arm in ("A", "B"):
        fields = {
            "content": build_field(
                (r["content"] for r in resources), identifier=arm == "B"
            ),
            "filename": build_field(
                (PurePosixPath(r["address"]).stem for r in resources),
                identifier=arm == "B",
            ),
        }
        postings = {
            field: {term: dict(items) for term, items in index.postings}
            for field, index in fields.items()
        }
        for lane in results["arms"][arm].values():
            expected_positions = {
                pos
                for field in postings.values()
                for term in lane["query_terms"]
                for pos in field.get(term, {})
            }
            expected_addresses = {
                resources[pos]["address"] for pos in expected_positions
            }
            if {r["address"] for r in lane["rows"]} != expected_addresses:
                raise ValueError("Incomplete positive retrieval universe.")
            positions = {r["address"]: i for i, r in enumerate(resources)}
            for row in lane["rows"]:
                pos = positions[row["address"]]
                for field, index in fields.items():
                    expected_terms = {
                        t
                        for t in lane["query_terms"]
                        if pos in postings[field].get(t, {})
                    }
                    if {t["term"] for t in row[field + "_terms"]} != expected_terms:
                        raise ValueError("Incomplete field evidence.")
                    for t in row[field + "_terms"]:
                        term_postings = postings[field][t["term"]]
                        if (t["tf"], t["df"], t["length"], t["average_length"]) != (
                            term_postings[pos],
                            len(term_postings),
                            index.lengths[pos],
                            index.average_length,
                        ):
                            raise ValueError("Captured analyzer statistics differ.")
                        expected_idf = calculate_bm25_inverse_document_frequency(
                            document_count=len(resources),
                            document_frequency=len(term_postings),
                        )
                        expected_contribution = contribution(
                            t["tf"], expected_idf, t["length"], t["average_length"]
                        )
                        if not math.isclose(
                            t["idf"], expected_idf, abs_tol=1e-10
                        ) or not math.isclose(
                            t["contribution"], expected_contribution, abs_tol=1e-10
                        ):
                            raise ValueError(
                                "Captured IDF or BM25 contribution differs."
                            )
    return {
        "complete_positive_universes": True,
        "all_captured_tf_df_length_average_verified": True,
        "query_analysis_verified": True,
        "all_captured_idf_contributions_verified": True,
        "new_treatment_rankings_executed": False,
    }


def arm_metrics(lanes: dict[str, Any], gold: dict[str, Any]) -> dict[str, Any]:
    """Compute positive reach separately from sufficient completion prefixes."""
    cells = {(c["obligation"], c["resource"]["address"]): c for c in gold["cells"]}
    required_resources = {p for (_, p), c in cells.items() if c["label"] == "REQUIRED"}
    global_ranks = {r["address"]: r["rank"] for r in lanes["global"]["rows"]}
    global_reach = set(global_ranks) & required_resources
    lane_union = set()
    reached_cells = set()
    reached_units = set()
    obligation_results = {}
    prefixes = []
    topk = {str(k): Counter() for k in (1, 3, 5, 10, 20, 50)}
    for o in gold["obligations"]:
        key = o["identity"]
        lane = lanes[key + "-query"]
        ranks = {r["address"]: r["rank"] for r in lane["rows"]}
        lane_union.update(ranks)
        for p in ranks:
            c = cells[key, p]
            if c["label"] == "REQUIRED":
                reached_cells.add((key, p))
                reached_units.update((key, u) for u in c["required_units"])
        completion = best_completion(o["acceptable_alternatives"], ranks)
        depth = completion["depth"]
        prefix = lane["rows"][:depth] if depth is not None else []
        prefixes.extend((key, r["address"]) for r in prefix)
        obligation_results[key] = {
            "positive_resources": len(ranks),
            "completion": completion,
            "prefix_resources": [r["address"] for r in prefix],
        }
        for k, counter in topk.items():
            counter.update(
                cells[key, r["address"]]["label"] for r in lane["rows"][: int(k)]
            )
    combinations = []
    for selected in itertools.product(
        *(o["acceptable_alternatives"] for o in gold["obligations"])
    ):
        union = sorted(
            {w["resource"]["address"] for a in selected for w in a["witnesses"]}
        )
        missing = sorted(set(union) - global_ranks.keys())
        combinations.append(
            {
                "alternatives": [a["identity"] for a in selected],
                "resources": union,
                "missing": missing,
                "depth": None if missing else max(global_ranks[p] for p in union),
            }
        )
    valid_depths = [c["depth"] for c in combinations if c["depth"] is not None]
    depths = [r["completion"]["depth"] for r in obligation_results.values()]
    prefix_labels = Counter(cells[c]["label"] for c in prefixes)
    prefix_union = {p for _, p in prefixes}
    # Global top-K counts membership in the union of REQUIRED resources and the
    # union of HELPFUL resources, with REQUIRED taking precedence. Own top-K is
    # strictly obligation relative and remains the primary supporting table.
    helpful_resources = {
        p for (_, p), c in cells.items() if c["label"] == "HELPFUL_ONLY"
    } - required_resources
    global_top = {}
    for k in topk:
        c = Counter(
            "REQUIRED"
            if r["address"] in required_resources
            else "HELPFUL_ONLY"
            if r["address"] in helpful_resources
            else "UNNECESSARY"
            for r in lanes["global"]["rows"][: int(k)]
        )
        global_top[k] = {label: c[label] for label in LABELS}
    return {
        "positive_global_count": len(global_ranks),
        "global_positive_resources": sorted(global_ranks),
        "obligation_positive_union": sorted(lane_union),
        "obligation_positive_cells": sum(
            r["positive_resources"] for r in obligation_results.values()
        ),
        "all_lanes_positive_union": sorted(lane_union | global_ranks.keys()),
        "required_global_resources": sorted(global_reach),
        "required_any_lane_resources": sorted(
            (lane_union | global_ranks.keys()) & required_resources
        ),
        "required_cells": sorted(reached_cells),
        "required_unit_judgments": sorted(reached_units),
        "distinct_required_units": sorted({u for _, u in reached_units}),
        "global_completion_combinations": combinations,
        "global_completion_depth": min(valid_depths) if valid_depths else None,
        "obligations": obligation_results,
        "maximum_own_completion_depth": max(depths) if None not in depths else None,
        "completion_prefix": {
            "complete": None not in depths,
            "occurrences": len(prefixes),
            "unique_union": sorted(prefix_union),
            "union_count": len(prefix_union),
            "labels": {label: prefix_labels[label] for label in LABELS},
            "lower_bound": 22,
            "excess": len(prefix_union) - 22,
            "multiple": len(prefix_union) / 22,
        },
        "own_topk": {k: {label: c[label] for label in LABELS} for k, c in topk.items()},
        "global_topk": global_top,
    }


def span_evidence(text: str, term: str, *, expanded: bool) -> list[dict[str, Any]]:
    """Find exact source spans exposing a term, without inferring semantics."""
    output = []
    for observed, whole, start, end in iter_lexical_spans(text=text):
        terms = expand_identifier_terms(observed_text=observed)
        if term in terms and ((whole != term) if expanded else (whole == term)):
            output.append(
                {
                    "observed": observed,
                    "canonical": whole,
                    "expanded_terms": terms,
                    "start": start,
                    "end": end,
                    "line": text.count("\n", 0, start) + 1,
                }
            )
    return output


def contribution(tf: int, idf: float, length: int, average: float) -> float:
    """Reuse production arithmetic for captured-statistic attribution only."""
    return calculate_bm25_term_contribution(
        term_frequency=tf,
        inverse_document_frequency=idf,
        document_length=length,
        average_document_length=average,
        settings=SETTINGS,
    )


def attribution(
    a: dict[str, Any] | None,
    b: dict[str, Any] | None,
    lane_a: dict[str, Any],
    lane_b: dict[str, Any],
    resource: dict[str, Any],
) -> dict[str, Any]:
    """Explain score changes from frozen field statistics, not new ranked arms."""
    fields = {}
    query_added = sorted(set(lane_b["query_terms"]) - set(lane_a["query_terms"]))
    for field in ("content", "filename"):
        text = (
            resource["content"]
            if field == "content"
            else PurePosixPath(resource["address"]).stem
        )
        ae = {t["term"]: t for t in a[field + "_terms"]} if a else {}
        be = {t["term"]: t for t in b[field + "_terms"]} if b else {}
        added = []
        shared = []
        for term in sorted(be.keys() - ae.keys()):
            extra = term in query_added
            doc_spans = span_evidence(text, term, expanded=True)
            whole_spans = span_evidence(text, term, expanded=False)
            if extra:
                side = (
                    "BOTH_SIDES"
                    if doc_spans and not whole_spans
                    else "QUERY_SIDE"
                    if whole_spans and not doc_spans
                    else "QUERY_AND_MIXED_DOCUMENT_OCCURRENCES"
                )
            else:
                side = "DOCUMENT_SIDE"
            if not doc_spans and not whole_spans:
                raise ValueError("Captured match has no source evidence.")
            added.append(
                {
                    "term": term,
                    "side": side,
                    "query_added": extra,
                    "query_identifier_spans": span_evidence(
                        lane_a["query_text"], term, expanded=True
                    )
                    if extra
                    else [],
                    "source_identifier_occurrences": len(doc_spans),
                    "source_identifier_spans": doc_spans[:3],
                    "source_whole_occurrences": len(whole_spans),
                    "source_whole_spans": whole_spans[:3],
                    "evidence": be[term],
                }
            )
        for term in sorted(ae.keys() & be.keys()):
            old, new = ae[term], be[term]
            tf_step = contribution(
                new["tf"], old["idf"], old["length"], old["average_length"]
            )
            df_step = contribution(
                new["tf"], new["idf"], old["length"], old["average_length"]
            )
            final = contribution(
                new["tf"], new["idf"], new["length"], new["average_length"]
            )
            if not math.isclose(final, new["contribution"], abs_tol=1e-10):
                raise ValueError("Captured BM25 arithmetic mismatch.")
            identifiers = span_evidence(text, term, expanded=True)
            if new["tf"] - old["tf"] != len(identifiers):
                raise ValueError("Identifier TF expansion attribution differs.")
            shared.append(
                {
                    "term": term,
                    "A": old,
                    "B": new,
                    "source_identifier_occurrences": len(identifiers),
                    "source_identifier_spans": identifiers[:3],
                    "tf_effect": tf_step - old["contribution"],
                    "df_effect": df_step - tf_step,
                    "length_normalization_effect": final - df_step,
                }
            )
        weight = 1.0 if field == "content" else 0.25
        fields[field] = {
            "A_score": a[field + "_score"] if a else 0.0,
            "B_score": b[field + "_score"] if b else 0.0,
            "weight": weight,
            "added_matches": added,
            "lost_terms": sorted(ae.keys() - be.keys()),
            "shared_terms": shared,
            "weighted_score_delta": weight
            * ((b[field + "_score"] if b else 0) - (a[field + "_score"] if a else 0)),
            "weighted_added_match_score": weight
            * sum(be[t]["contribution"] for t in be.keys() - ae.keys()),
        }
    added_fields = [
        f
        for f, evidence in fields.items()
        if evidence["added_matches"]
        or any(t["B"]["tf"] != t["A"]["tf"] for t in evidence["shared_terms"])
    ]
    field_class = (
        "MIXED"
        if len(added_fields) == 2
        else "CONTENT_IDENTIFIER_GAIN"
        if added_fields == ["content"]
        else "FILENAME_IDENTIFIER_GAIN"
        if added_fields == ["filename"]
        else "STATISTICS_ONLY"
    )
    a_rank = a["rank"] if a else None
    b_rank = b["rank"] if b else None
    recovery = (
        a is None and b is not None and any(e["added_matches"] for e in fields.values())
    )
    status = (
        "VERIFIED_IDENTIFIER_REPRESENTATION_RECOVERY"
        if recovery
        else "IDENTIFIER_AWARE_RANKING_GAIN"
        if a and b and b_rank < a_rank
        else "PAIRED_REGRESSION"
        if a and b and b_rank > a_rank
        else "UNCHANGED"
        if a and b
        else "REQUIRED_LOSS"
        if a
        else "UNREACHED"
    )
    a_ahead = {r["address"] for r in lane_a["rows"] if a and r["rank"] < a_rank}
    b_ahead = {r["address"] for r in lane_b["rows"] if b and r["rank"] < b_rank}
    a_positive = {r["address"] for r in lane_a["rows"]}
    mechanisms = {
        "added_term_score": sum(
            e["weighted_added_match_score"] for e in fields.values()
        ),
        **{
            effect: sum(
                e["weight"] * sum(t[effect] for t in e["shared_terms"])
                for e in fields.values()
            )
            for effect in ("tf_effect", "df_effect", "length_normalization_effect")
        },
    }
    score_delta = sum(e["weighted_score_delta"] for e in fields.values())
    if (
        a
        and b
        and not math.isclose(sum(mechanisms.values()), score_delta, abs_tol=1e-9)
    ):
        raise ValueError("Attribution score-delta partition differs.")
    if a and b and len(b_ahead - a_ahead) - len(a_ahead - b_ahead) != b_rank - a_rank:
        raise ValueError("Rank overtaker partition differs.")
    return {
        "classification": status,
        "field_class": field_class,
        "A_rank": a_rank,
        "B_rank": b_rank,
        "delta": b_rank - a_rank if a and b else None,
        "query_text": lane_a["query_text"],
        "A_query_terms": lane_a["query_terms"],
        "B_query_terms": lane_b["query_terms"],
        "query_added_terms": query_added,
        "fields": fields,
        "score_delta": score_delta,
        "mechanisms": mechanisms,
        "new_overtakers": sorted(b_ahead - a_ahead),
        "new_overtakers_A_zero": sorted((b_ahead - a_ahead) - a_positive),
        "removed_overtakers": sorted(a_ahead - b_ahead),
        "stats_decomposition": "Exact sequential tf -> df/IDF -> length/average changes for shared terms; path-dependent allocation of interactions, not independently executed counterfactual treatments.",
    }


def decision(
    metrics: dict[str, Any],
    reach: dict[str, Any],
    attribution_rows: list[dict[str, Any]],
    costs: dict[str, Any],
) -> dict[str, Any]:
    """Apply the exact prospective promotion and separate-view conditions."""
    a, b = metrics["A"], metrics["B"]
    reduction = (
        a["completion_prefix"]["union_count"] - b["completion_prefix"]["union_count"]
    ) / a["completion_prefix"]["union_count"]
    rescued = [
        r
        for r in attribution_rows
        if r["lane"] != "global"
        and r["classification"] == "VERIFIED_IDENTIFIER_REPRESENTATION_RECOVERY"
    ]
    top20 = [
        r
        for r in attribution_rows
        if r["lane"] != "global"
        and r["B_rank"] is not None
        and r["B_rank"] <= 20
        and (r["A_rank"] is None or r["A_rank"] > 20)
    ]
    fields = (
        "median_query_seconds",
        "index_plus_query_seconds",
        "serialized_index_bytes",
        "traced_peak_bytes",
    )
    ratios = {f: costs["B"][f] / costs["A"][f] for f in fields}
    depths = [
        (
            a["obligations"][k]["completion"]["depth"],
            b["obligations"][k]["completion"]["depth"],
        )
        for k in a["obligations"]
    ]
    depths.append((a["global_completion_depth"], b["global_completion_depth"]))
    no_worse = all(y is not None and (x is None or y <= x) for x, y in depths)
    improved_own = sum(y is not None and (x is None or y < x) for x, y in depths[:-1])
    conditions = {
        "valid_complete_gold_and_join": True,
        "no_A_positive_required_cells_lost": not reach["cells"]["A_only"],
        "no_worse_every_own_and_global_completion": no_worse,
        "twenty_percent_burden_or_verified_required_rescue": reduction >= 0.2
        or bool(rescued),
        "all_frozen_cost_limits": all(v <= 3 for v in ratios.values()),
    }
    promotion = all(conditions.values())
    separate = not promotion and bool(rescued or top20) and improved_own > 0
    return {
        "outcome": "PROMOTE / PRODUCTIONIZE REPRESENTATION CANDIDATE"
        if promotion
        else "RETAIN AS SEPARATE RETRIEVAL VIEW"
        if separate
        else "PARK",
        "promotion_conditions": conditions,
        "concrete_analyzer_defect": False,
        "cost_B_over_A": ratios,
        "cost_limit": 3,
        "burden_reduction": reduction,
        "burden_reduction_percent": reduction * 100,
        "verified_required_cell_rescues": len(rescued),
        "required_top20_entries": [
            {
                "obligation": r["lane"],
                "resource": r["resource"],
                "A": r["A_rank"],
                "B": r["B_rank"],
            }
            for r in top20
        ],
        "improved_own_completions": improved_own,
        "R2": "MANDATORY REGARDLESS OF R1 OUTCOME",
        "production_adoption": "NOT AUTHORIZED",
    }


def build() -> dict[str, Any]:
    """Verify exact frozen inputs, then deterministically join and attribute."""
    chain = asyncio.run(verify_commits())
    native = load_inputs()
    manifest = read_json(CASE / "pre_execution.json")
    frozen_treatment = read_json(CASE / "treatment.json")
    if frozen_treatment != treatment():
        raise ValueError("Frozen treatment definition differs.")
    seal = read_json(CASE / "stage_b_integrity.json")
    if seal["stage_a_integrity_sha256"] != digest(binary(CASE / "integrity.json")):
        raise ValueError("Stage B lineage mismatch.")
    for name, expected in seal["sha256"].items():
        if digest(binary(CASE / name)) != expected:
            raise ValueError("Stage B artifact hash mismatch.")
    results = json.loads(gzip.decompress(binary(CASE / "results.json.gz")))
    if digest(json_bytes(results)) != seal["deterministic_rankings_sha256"]:
        raise ValueError("Rankings payload mismatch.")
    packet = read_json(CASE / "adjudication/manifest.json")
    payload = gzip.decompress(binary(CASE / "adjudication/resources.json.gz"))
    if digest(payload) != PAYLOAD_HASH:
        raise ValueError("Blind payload hash differs.")
    resources = json.loads(payload)["resources"]
    if [(r["address"], r["content_identity"], r["content"]) for r in resources] != [
        (d.resource.address.value, d.resource.content_identity.value, d.text)
        for d in native["documents"].documents
    ]:
        raise ValueError("Native/packet resource bytes differ.")
    if (
        native["task"].identity.value != packet["task_identity"]
        or str(native["snapshot"].repository_id) != packet["repository_id"]
    ):
        raise ValueError("Native task/repository frame differs.")
    gold = read_json(CASE / "adjudication/judgments.json")
    validate_join(results, gold, manifest, packet, resources)
    analyzer_verification = validate_statistics(results, resources)
    if {q.identity.value: (q.obligation.value, q.text) for q in native["queries"]} != {
        o["id"] + "-query": (o["id"], o["query"])
        for o in frozen_treatment["obligations"]
    }:
        raise ValueError("Native query lane identities differ.")
    summary = gold_statistics(gold)
    if summary != read_json(CASE / "adjudication/gold_statistics.json"):
        raise ValueError("Gold statistics differ.")
    expected = {
        "resource_count": 531,
        "obligation_count": 9,
        "qualified_cell_count": 4779,
        "applicable_obligations": 9,
        "distinct_required_information_units": 40,
        "unique_required_resources": 23,
        "acceptable_alternative_count": 10,
        "minimum_sufficient_unique_resource_union": 22,
        "maximum_sufficient_unique_resource_union": 23,
        "inferable_units": 40,
        "inherent_discovery_units": 0,
    }
    if any(summary[k] != v for k, v in expected.items()) or summary["label_counts"] != {
        "REQUIRED": 37,
        "HELPFUL_ONLY": 78,
        "UNNECESSARY": 4664,
        "UNRESOLVED": 0,
    }:
        raise ValueError("Expected clean gold summary differs.")
    if (
        gold["task_gap"]["status"] != "NONE"
        or gold["repository_gap"]["status"] != "NONE"
        or len(gold["blindness_attestation"]) != 10
        or set(gold["blindness_attestation"].values()) != {"NO"}
    ):
        raise ValueError("Gold gaps or blindness differ.")
    metrics = {arm: arm_metrics(results["arms"][arm], gold) for arm in ("A", "B")}
    positive_partitions = {}
    labels_by_cell = {
        (c["obligation"], c["resource"]["address"]): c["label"] for c in gold["cells"]
    }
    for key, lane_a in results["arms"]["A"].items():
        pa = {r["address"] for r in lane_a["rows"]}
        pb = {r["address"] for r in results["arms"]["B"][key]["rows"]}
        extra_labels = (
            Counter(labels_by_cell[lane_a["obligation"], p] for p in pb - pa)
            if key != "global"
            else Counter()
        )
        positive_partitions[key] = {
            "both": len(pa & pb),
            "A_only": len(pa - pb),
            "B_only": len(pb - pa),
            "union": len(pa | pb),
            "B_added_labels": {label: extra_labels[label] for label in LABELS},
        }
    cells = {
        (c["obligation"], c["resource"]["address"])
        for c in gold["cells"]
        if c["label"] == "REQUIRED"
    }
    required_resources = {p for _, p in cells}
    units = {
        (o["identity"], u) for o in gold["obligations"] for u in o["required_units"]
    }
    reach = {
        "global_resources": partition(
            set(metrics["A"]["required_global_resources"]),
            set(metrics["B"]["required_global_resources"]),
            required_resources,
        ),
        "any_lane_resources": partition(
            set(metrics["A"]["required_any_lane_resources"]),
            set(metrics["B"]["required_any_lane_resources"]),
            required_resources,
        ),
        "cells": partition(
            set(metrics["A"]["required_cells"]),
            set(metrics["B"]["required_cells"]),
            cells,
        ),
        "unit_judgments": partition(
            set(metrics["A"]["required_unit_judgments"]),
            set(metrics["B"]["required_unit_judgments"]),
            units,
        ),
        "distinct_units": partition(
            set(metrics["A"]["distinct_required_units"]),
            set(metrics["B"]["distinct_required_units"]),
            {u for _, u in units},
        ),
    }
    resource_map = {r["address"]: r for r in resources}
    attribution_rows = []
    for lane, address in sorted(cells | {("global", p) for p in required_resources}):
        key = lane if lane == "global" else lane + "-query"
        la, lb = (results["arms"][a][key] for a in ("A", "B"))
        a = next((r for r in la["rows"] if r["address"] == address), None)
        b = next((r for r in lb["rows"] if r["address"] == address), None)
        info = attribution(a, b, la, lb, resource_map[address])
        if lane != "global":
            label_map = {
                c["resource"]["address"]: c["label"]
                for c in gold["cells"]
                if c["obligation"] == lane
            }
            info["new_overtaker_labels"] = dict(
                sorted(Counter(label_map[p] for p in info["new_overtakers"]).items())
            )
        required_units = sorted(
            {
                u
                for c in gold["cells"]
                if c["resource"]["address"] == address
                and c["label"] == "REQUIRED"
                and (lane == "global" or c["obligation"] == lane)
                for u in c["required_units"]
            }
        )
        attribution_rows.append(
            {
                "lane": lane,
                "resource": address,
                "required_units": required_units,
                **info,
            }
        )
    paired = [
        r for r in attribution_rows if r["lane"] != "global" and r["delta"] is not None
    ]
    deltas = [r["delta"] for r in paired]
    counts = Counter(
        "IMPROVED" if d < 0 else "WORSENED" if d > 0 else "UNCHANGED" for d in deltas
    )
    whole = []
    for r in attribution_rows:
        for field, evidence in r["fields"].items():
            for item in evidence["shared_terms"]:
                if any(
                    len(expand_identifier_terms(observed_text=s[0])) > 1
                    and s[1] == item["term"]
                    for s in iter_lexical_spans(text=r["query_text"])
                ):
                    whole.append(  # noqa: PERF401 -- nested evidence filter is clearer explicitly
                        {
                            "lane": r["lane"],
                            "resource": r["resource"],
                            "field": field,
                            "whole_term": item["term"],
                            "A_tf": item["A"]["tf"],
                            "B_tf": item["B"]["tf"],
                            "A_rank": r["A_rank"],
                            "B_rank": r["B_rank"],
                            "only_A_field_term": len(evidence["shared_terms"]) == 1,
                            "statistics": item,
                        }
                    )
    costs = read_json(CASE / "costs.json")
    return {
        "schema": "case-0009-r1-stage-d-v1",
        "frozen_chain": chain,
        "input_sha256": {
            name: digest(binary(CASE / name))
            for name in (
                "treatment.json",
                "inputs.pkl.gz",
                "pre_execution.json",
                "integrity.json",
                "stage_b_integrity.json",
                "results.json.gz",
                "costs.json",
            )
        },
        "join_integrity": {
            "status": "EXACT",
            "frame": gold["frame"],
            "treatment_resources": 531,
            "gold_resources": 531,
            "obligations": 9,
            "lanes": 10,
            "duplicate_missing_unexpected": 0,
            "native_packet_bytes_equal": True,
            "analyzer_verification": analyzer_verification,
            "gold_blindness_attestations": gold["blindness_attestation"],
        },
        "gold_summary": summary,
        "gold_gaps": {
            "task": gold["task_gap"],
            "repository_information": gold["repository_gap"],
        },
        "arms": metrics,
        "positive_universe_partitions": positive_partitions,
        "reach_partitions": reach,
        "required_attribution": attribution_rows,
        "paired_own_required_ranks": {
            "counts": {k: counts[k] for k in ("IMPROVED", "UNCHANGED", "WORSENED")},
            "median_delta": statistics.median(deltas) if deltas else None,
            "mean_delta": statistics.mean(deltas) if deltas else None,
            "largest_improvements": [
                {k: r[k] for k in ("lane", "resource", "A_rank", "B_rank", "delta")}
                for r in sorted(paired, key=lambda r: r["delta"])[:5]
            ],
            "largest_regressions": [
                {k: r[k] for k in ("lane", "resource", "A_rank", "B_rank", "delta")}
                for r in sorted(paired, key=lambda r: -r["delta"])[:5]
            ],
        },
        "whole_form_preservation": whole,
        "costs": costs,
        "decision": decision(metrics, reach, attribution_rows, costs),
        "access": {
            "blind_intentionally_lifted": True,
            "confirmation_accessed": False,
            "quarantined_invalid_gold_accessed": False,
            "treatment_executed_again": False,
            "production_changed": False,
            "R2_implemented": False,
        },
    }


def render(data: dict[str, Any]) -> str:
    """Render the complete primary report before contextual historical comparison."""
    a, b = data["arms"]["A"], data["arms"]["B"]
    rule = data["decision"]
    rows = [
        "# Case 0009 Stage D: joined R1 effectiveness",
        "",
        "**R1 = prospectively evaluated against clean independent Stage C gold.**",
        "**R2 TRUE BM25F / FIELD-AWARE SPARSE RETRIEVAL REMAINS MANDATORY REGARDLESS OF R1 OUTCOME.**",
        "",
        "Canonical production BM25 is unchanged. One prospective task cannot establish universal dominance or solve code-aware representation. The primary questions below precede the architectural recommendation.",
        "",
        "## Integrity and procedural provenance",
        "",
        "Ordered ancestry and exact committed bytes were verified for Stage A `eb4060ff`, Stage B `44638db3`, packet repair `c2d6f322`, and clean Stage C `092f9a76`. The join has 531 treatment and gold resources, 9 obligations and exactly 10 frozen query lanes; duplicate/missing/unexpected identities = 0. Repository, snapshot, corpus, task, resource/content and query identities agree. Native frozen input content equals the packet. All eight clean gold hashes and repaired packet digests match committed Git bytes. Captured query terms, complete positive universes, all field TF/DF/length/average statistics, field sums and score arithmetic were mechanically verified without executing new ranked treatments or collecting costs.",
        "",
        "The initial Stage C stopped before decompression over ambiguous digest scopes. Repair changed digest scopes, not packet semantics. A later broad pytest run crossed the blind boundary and invalidated its provisional gold. That quarantined attempt is never used here. Fresh Stage C ran in a sterile external workspace; clean outputs were imported byte-for-byte and committed. The supplied procedural history records material differences from invalid provisional gold; no comparison or access to that invalid gold was made during this analysis. Only Stage D now intentionally lifts the blind. The ten original Stage C NO attestations remain frozen historical assertions, not a claim that Stage D is blind.",
        "",
        "Frame: `" + json.dumps(data["join_integrity"]["frame"], sort_keys=True) + "`.",
        "",
        "Gold: 4,779 cells (37 REQUIRED, 78 HELPFUL_ONLY, 4,664 UNNECESSARY, 0 UNRESOLVED); 9 applicable obligations; 40 distinct required units, 42 obligation-relative unit judgments, 23 unique required resources and 10 alternatives. Minimum/maximum sufficient resource union = 22/23. All 40 units are INFERABLE_AT_START; inherent discovery = 0. Task gap and repository-information gap = NONE.",
        "",
        "Arm A is exact canonical whole-resource content BM25 + 0.25 filename-stem BM25. Arm B changes only lexical analysis of content, filename stems and queries to whole identifiers plus unique subtokens. Both use k1=1.2, b=0.75, identical corpus/query text, independent field arithmetic and native corpus tie order. No structural retrieval, fusion, reranking, stemming, synonyms, semantic expansion, reformulation or BM25F. Primary intended class = REPRESENTATION_FAILURE; secondary = RANKING_DISCRIMINATION_FAILURE.",
        "",
        "## Primary questions before recommendation",
        "",
        "| Question | Joined answer |",
        "|---|---|",
        "| 1. Any A-positive REQUIRED resource lost by B? | NO, either globally or in own lanes. |",
        "| 2. Any REQUIRED zero-A-positive resource rescued? | NO; both reach all 23 resources and 37 own cells. |",
        "| 3. Better global completion? | YES: 342 to 331 (-11). |",
        "| 4. Better own-obligation completion? | Three improve, five worsen, one ties; maximum worsens 185 to 231. |",
        "| 5. Lower prefix burden? | YES but small: union 257 to 252 (1.9455%); occurrences 454 to 423. |",
        "| 6. Better REQUIRED ranks without harming others? | NO: 13 improve, 9 tie, 15 worsen. |",
        "| 7. Identifier-attributable gains? | Source component exposure in explicit_package_bases and test names; query-side LocalizationAssessment; shared-term TF expansion. No positive-reach rescue. |",
        "| 8. Expansion regressions? | Captured TF/DF/length changes and new overtakers explain score/rank partitions; isolated rank-causal field allocation is unknown. |",
        "| 9. Net gain/loss? | Required reach gains 0, losses 0, net 0; mixed ranking changes and one top-20 entry versus two exits. |",
        "| 10. Frozen rule satisfied? | Promotion NO (two gates fail); separate-view condition YES (one required top-20 entry and three improved completions). |",
        "",
        "## Primary paired metrics",
        "",
        "| Metric | Arm A | Arm B | B minus A |",
        "|---|---:|---:|---:|",
    ]
    metrics = [
        (
            "REQUIRED unique resources reached / 23",
            len(a["required_global_resources"]),
            len(b["required_global_resources"]),
        ),
        (
            "REQUIRED own cells reached / 37",
            len(a["required_cells"]),
            len(b["required_cells"]),
        ),
        (
            "REQUIRED unit judgments reached / 42",
            len(a["required_unit_judgments"]),
            len(b["required_unit_judgments"]),
        ),
        (
            "Distinct REQUIRED units reached / 40",
            len(a["distinct_required_units"]),
            len(b["distinct_required_units"]),
        ),
        (
            "Global sufficient completion depth",
            a["global_completion_depth"],
            b["global_completion_depth"],
        ),
        (
            "Maximum own-obligation completion",
            a["maximum_own_completion_depth"],
            b["maximum_own_completion_depth"],
        ),
        (
            "Completion-prefix unique union",
            a["completion_prefix"]["union_count"],
            b["completion_prefix"]["union_count"],
        ),
        (
            "Completion-prefix occurrences",
            a["completion_prefix"]["occurrences"],
            b["completion_prefix"]["occurrences"],
        ),
        *[
            (
                f"Own top-{k} REQUIRED (nine lanes)",
                a["own_topk"][str(k)]["REQUIRED"],
                b["own_topk"][str(k)]["REQUIRED"],
            )
            for k in (5, 10, 20)
        ],
    ]
    rows.extend(f"| {name} | {x} | {y} | {y - x:+} |" for name, x, y in metrics)
    rows += [
        "",
        "Both arms positively retrieve the same 23 REQUIRED resources, all 37 REQUIRED own cells, all 42 obligation-relative unit judgments and all 40 distinct units. Both global and any-lane required-resource partitions are identical. A-only = B-only = neither = 0 in all required reach partitions. B required gains = 0, required losses = 0, net positive-reach change = 0. There are no verified positive-reach representation recoveries. The complete lists are in analysis.json; positive reach is not completion prefix size.",
        "",
        "Required resources reached by both:",
        "",
    ]
    rows.extend(
        "- `" + p + "`" for p in data["reach_partitions"]["global_resources"]["both"]
    )
    rows += [
        "",
        "## Complete positive universes and own completion",
        "",
        "| Lane/obligation | A positives | B positives | A completion | B completion | Delta | Winner |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    rows.append(
        f"| global | {a['positive_global_count']} | {b['positive_global_count']} | {a['global_completion_depth']} | {b['global_completion_depth']} | {b['global_completion_depth'] - a['global_completion_depth']:+} | B |"
    )
    for name in a["obligations"]:
        ar, br = a["obligations"][name], b["obligations"][name]
        x, y = ar["completion"]["depth"], br["completion"]["depth"]
        rows.append(
            f"| {name} | {ar['positive_resources']} | {br['positive_resources']} | {x if x is not None else 'MISS'} | {y if y is not None else 'MISS'} | {y - x if x is not None and y is not None else 'N/A'} | {'Tie' if x == y else 'B' if y is not None and (x is None or y < x) else 'A'} |"
        )
    rows += [
        "",
        f"Own positive-resource unions: A {len(a['obligation_positive_union'])}, B {len(b['obligation_positive_union'])}; own positive cells: A {a['obligation_positive_cells']}, B {b['obligation_positive_cells']}. Across global and own lanes, unique positive resources: A {len(a['all_lanes_positive_union'])}, B {len(b['all_lanes_positive_union'])}. The two global positive sets are equal. A/B global completeness is evaluated over each valid combination, not all 23 possible resources by assumption.",
        "",
        "| Arm | Combination | Unique required resources | Global completion |",
        "|---|---|---:|---:|",
    ]
    for arm in ("A", "B"):
        for combo in data["arms"][arm]["global_completion_combinations"]:
            rows.append(
                f"| {arm} | {', '.join(combo['alternatives'])} | {len(combo['resources'])} | {combo['depth']} |"
            )
    rows += [
        "",
        "Both global combinations have the same depth within each arm, with pyproject.toml the global bottleneck at A342/B331. For the alternatives obligation, both arms choose the documentation alternative; incompatible alternatives are never mixed. B improves documentation, package and tests completion, ties validation, and worsens alternatives, applicability, bridge, frame and readiness. Maximum own depth worsens 185 to 231 (+46).",
        "",
        "## Completion-prefix burden and top-K",
        "",
        "| Prefix metric | Arm A | Arm B |",
        "|---|---:|---:|",
    ]
    for key in ("occurrences", "union_count", "excess", "multiple"):
        rows.append(
            f"| {key} | {a['completion_prefix'][key]} | {b['completion_prefix'][key]} |"
        )
    for label in LABELS:
        rows.append(
            f"| {label} cells in own prefixes | {a['completion_prefix']['labels'][label]} | {b['completion_prefix']['labels'][label]} |"
        )
    rows += [
        "",
        f"The exact unique-union reduction is (257 - 252) / 257 = 5/257 = **{rule['burden_reduction_percent']:.10f}%**, below the frozen 20% threshold. The 22-resource lower bound leaves A 235 excess candidates (11.681818x gold), B 230 excess candidates (11.454545x gold). Prefixes include 36 of the 37 REQUIRED cells: the unchosen alternative's source-only member is not needed by the selected sufficient combination. Own occurrences fall by 31; unnecessary own-prefix cells fall by 30. Severe discrimination weakness remains.",
        "",
        "Own top-K sums nine obligation-relative prefixes (45/90/180 candidate cells). Global top-K uses union relevance: REQUIRED precedence, then HELPFUL in any obligation, then UNNECESSARY; it is not an obligation-relative judgment or the historical Increment 27 metric.",
        "",
        "| Scope | K | A REQUIRED | B REQUIRED | A useful (R+H) | B useful | A UNNECESSARY | B UNNECESSARY |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for scope in ("own_topk", "global_topk"):
        for k in (5, 10, 20):
            x, y = a[scope][str(k)], b[scope][str(k)]
            rows.append(
                f"| {scope} | {k} | {x['REQUIRED']} | {y['REQUIRED']} | {x['REQUIRED'] + x['HELPFUL_ONLY']} | {y['REQUIRED'] + y['HELPFUL_ONLY']} | {x['UNNECESSARY']} | {y['UNNECESSARY']} |"
            )
    paired = data["paired_own_required_ranks"]
    rows += [
        "",
        "## All paired REQUIRED own-cell ranks",
        "",
        f"Counts: {paired['counts']['IMPROVED']} improved, {paired['counts']['UNCHANGED']} unchanged, {paired['counts']['WORSENED']} worsened. Median delta = {paired['median_delta']}; mean delta = {paired['mean_delta']:.6f} (supporting only; does not cancel regressions). Delta = B - A.",
        "",
        "| Obligation | Resource | A | B | Delta | Status | Field mechanism |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    own = [r for r in data["required_attribution"] if r["lane"] != "global"]
    for r in own:
        delta = r["delta"]
        label = "IMPROVED" if delta < 0 else "WORSENED" if delta > 0 else "UNCHANGED"
        rows.append(
            f"| {r['lane']} | `{r['resource']}` | {r['A_rank']} | {r['B_rank']} | {delta:+} | {label} | {r['field_class']} |"
        )
    rows += [
        "",
        "## Representation, field and query attribution",
        "",
        "No B-only REQUIRED resource/cell exists, so **VERIFIED_IDENTIFIER_REPRESENTATION_RECOVERY = 0**. Paired rank wins are IDENTIFIER_AWARE_RANKING_GAIN, not rescues. Whole-form plus components changes TF, DF and document length even when both arms already match. Field classes below identify local added-match/TF mechanisms; they do not independently prove that field alone caused a rank movement. The only query with added identifier terms is the global task and readiness lane: `LocalizationAssessment` retains `localizationassessment` and adds `localization`, `assessment`. Other own queries are ordinary separated words and have no query-side additions.",
        "",
        "For every REQUIRED cell and global REQUIRED resource, analysis.json records exact A/B terms and ranks, required units, field contribution evidence, source identifier/text samples with line/character offsets, occurrence counts, query identifier spans, and sequential TF/DF/length score decomposition. These records distinguish document-only matches, query-only matches and both-side compound exposure. Each field's total delta equals added matches plus shared-term statistic deltas. Source samples are capped at three occurrences per term; full occurrence counts are verified.",
        "",
        "Meaningful own-cell gains and their exact lexical evidence:",
        "",
    ]
    for r in own:
        if r["delta"] >= 0:
            continue
        snippets = []
        for field, evidence in r["fields"].items():
            for t in evidence["added_matches"]:
                sample = (t["source_identifier_spans"] or t["source_whole_spans"])[0]
                snippets.append(
                    f"{field}: `{sample['observed']}` -> `{t['term']}` ({t['side']}, line {sample['line']})"
                )
            for t in evidence["shared_terms"]:
                if t["source_identifier_spans"]:
                    sample = t["source_identifier_spans"][0]
                    snippets.append(
                        f"{field}: `{sample['observed']}` -> `{t['term']}` (TF {t['A']['tf']}->{t['B']['tf']}, line {sample['line']})"
                    )
        rows.append(
            f"- **{r['lane']}** `{r['resource']}` {r['A_rank']}->{r['B_rank']}: {r['field_class']}; "
            + (
                "; ".join(snippets[:5])
                if snippets
                else "no local matching-term/TF expansion; captured DF and length statistics change"
            )
            + "."
        )
    rows += [
        "",
        "The readiness promotion resource improves 33->11, entering top-20; its required unit is `promotion-no-mutation`. Query-side `LocalizationAssessment` expansion is material: B matches `localization`/`assessment` that A's whole query term did not supply to this resource. It is an identifier-aware ranking gain, not a zero-score rescue. It does not complete readiness earlier because `resolution/view.py` moves 34->35. Required top-20 exits are bridge assessment.py (16->23) and frame task.py (20->22), so own top-20 REQUIRED net change is -1 despite the one entry.",
        "",
        "## Regression attribution",
        "",
        "Known: the frozen statistics show additional identifier matches, changed term frequencies and document frequencies, and changed relative document lengths. Added query terms have nonnegative additive scores; there is no query-score dilution normalization in this BM25 implementation. Rank moves are exactly partitioned into new overtakers minus removed overtakers. The following score decomposition is sequential TF -> DF/IDF -> length/average; interaction attribution is path-dependent, not a new ranked ablation.",
        "",
        "| Regressed cell | Rank delta | Score delta | Added matches | TF effect | DF effect | Length effect | New/removed overtakers | Newly ahead labels |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for r in own:
        if r["delta"] <= 0:
            continue
        m = r["mechanisms"]
        rows.append(
            f"| {r['lane']}: `{r['resource']}` | +{r['delta']} | {r['score_delta']:.6f} | {m['added_term_score']:.6f} | {m['tf_effect']:.6f} | {m['df_effect']:.6f} | {m['length_normalization_effect']:.6f} | {len(r['new_overtakers'])}/{len(r['removed_overtakers'])} | {r.get('new_overtaker_labels', {})} |"
        )
    rows += [
        "",
        "Known local arithmetic effects and overtaker identities are recorded exactly. New own positive cells total 346: 345 UNNECESSARY, 1 HELPFUL_ONLY and 0 REQUIRED; per-lane counts are in positive_universe_partitions. Likely: common component exposure increases competition from weakly relevant/unnecessary resources, consistent with expanded positive cells and the overtaker label counts. Unknown: unique causal allocation of final rank changes among interacting TF, DF, length, content and filename changes without separately frozen ablation arms. No such arms were executed. Native tie ordering is preserved; no analyzer-contract defect was demonstrated. Whole-form preservation guarantees lexical reach, not ranking preservation.",
        "",
        "## Whole forms, complementarity and remaining failures",
        "",
        f"All canonical positive REQUIRED field terms are retained in B (lost terms = 0). {len(data['whole_form_preservation'])} required lane/resource/field observations retain the compound whole query term `localizationassessment`. No REQUIRED observed row depends exclusively on that compound whole form as its only canonical matching term. Both arms have other canonical evidence for those rows; there is no isolated whole-form-only REQUIRED reach case. Captured whole-term statistics/ranks still change with corpus length normalization and competition.",
        "",
        "A union B reaches the same 23 REQUIRED resources, 37 own cells and 40 units as either arm alone: no added REQUIRED positive reach. Complementarity here is ranking: readiness's required top-20 entry and three improved obligation completions coexist with five worsened completions and 15 worsened required-cell ranks. The frozen separate-view rule explicitly permits that top-20 entry plus improved completion; no fusion is implemented.",
        "",
        "Remaining positive-reach misses = 0, so no residual zero-score miss can be assigned to REPRESENTATION_FAILURE or VOCABULARY_SEMANTIC_MISMATCH. Required evidence outside shallow prefixes/top-20 and the 252-resource union demonstrate RANKING_DISCRIMINATION_FAILURE. Query/field representation effects are observed, but not all semantic insufficiency is representation failure. RELATIONAL_RELEVANCE may motivate future hypotheses but is not established as the cause of a positive miss here. CONTEXT_DISCLOSURE_FAILURE is unmeasured (no downstream Context output). INFORMATION_NEED_OBLIGATION_FAILURE is not established: task gap NONE and nine applicable obligations cover the task. No semantic-resolution effectiveness or execution claim follows.",
        "",
        "## Costs and exact frozen decision",
        "",
        "| Captured cost | Arm A | Arm B | B/A | Frozen <=3x |",
        "|---|---:|---:|---:|---|",
    ]
    for field in (
        "index_build_seconds",
        "median_query_seconds",
        "index_plus_query_seconds",
        "content_vocabulary_size",
        "content_posting_count",
        "serialized_index_bytes",
        "traced_peak_bytes",
    ):
        x, y = data["costs"]["A"][field], data["costs"]["B"][field]
        limit = (
            "PASS" if field in rule["cost_B_over_A"] else "not a separate frozen gate"
        )
        rows.append(f"| {field} | {x} | {y} | {y / x:.9f} | {limit} |")
    rows += [
        "",
        "All four frozen gates (median query, index+queries, serialized index, traced peak) pass <=3x. Single traced execution, not a latency benchmark. Native A serializes richer provenance/span objects than B and allocation includes projection; lower B index bytes/peak are not evidence that lexical expansion saves memory. Filename indexes rebuild per query in both arms. No RSS conclusion.",
        "",
        "| Promotion condition | Result |",
        "|---|---|",
    ]
    rows.extend(
        f"| {k} | {'PASS' if v else 'FAIL'} |"
        for k, v in rule["promotion_conditions"].items()
    )
    rows += [
        "",
        "Promotion fails both no-worse-completion and 20%-burden-or-rescue gates. Separate-view criteria pass: one verified identifier-attributable required top-20 entry, three improved own completions, and failed promotion. Primary outcome: **RETAIN AS SEPARATE RETRIEVAL VIEW**. No production consideration checkpoint is earned by this exact prospective case, no concrete representation defect is demonstrated, and the PARK condition is not selected. Canonical production retrieval remains unchanged.",
        "",
        "## Historical context after the primary metric freeze",
        "",
        "Primary Case 0009 metrics were computed and written before contextual historical comparison. Retained Increment 27 aggregates: canonical useful@5=63; identifier=68; lexical RRF=74. Increment 27 also preserved whole forms plus subtokens but used different scoring infrastructure. Case 0009 remains **mixed** relative to that evidence: it prospectively reinforces specific unused identifier signal and paired ranking gains, while weakening any replacement inference through regressions, unchanged REQUIRED positive reach and only 1.9455% burden reduction. Case 0009 own useful@5 falls 36->35; it is a different nine-obligation aggregation and cannot be pooled numerically with Increment 27. Historical RRF is a comparator, not a default or a new Case 0009 fusion result.",
        "",
        "## R2 design inputs and limits",
        "",
        "R1 asks which lexical terms should be exposed; R2 asks how evidence from distinct code/document fields should contribute. R2 must prospectively retain separate canonical and identifier-aware representations so fielding and representation effects can be attributed independently. Include whole+subtoken terms in an R2 comparison arm, preserve whole identifiers, and explicitly distinguish filename/name evidence from body/content. Filename expansion demonstrably supplies `resolution` from `test_resolution`; content expansion and query-side `LocalizationAssessment` provide different ranking effects. Expanded common components also grow positive candidate competition. These observations inform hypotheses and field schemas, not Case 0009 post-hoc BM25F weight tuning. No R2 weights, BM25F implementation or semantic-resolution experiment is introduced here.",
        "",
        "## Validation and access",
        "",
        "15 focused Stage D tests passed, checking joins, golden metric totals, gain/loss partitions, alternative ALL/ANY completion, source/term attribution, score decomposition, costs and frozen decision precedence. CLI verify rebuilds analysis.json and analysis.md exactly from frozen inputs. Scoped Ruff and formatter checks apply only to new Stage D Python; frozen Stage C remains byte-identical. Diff checks pass. Confirmation/reserve and quarantined invalid gold were not accessed. Stage B treatments were not reexecuted.",
        "",
        "Next step:",
        "",
        "> R2 — design, implement, freeze and prospectively evaluate true BM25F / field-aware sparse retrieval. R2 occurs regardless of R1 outcome.",
        "",
        "STOP. Do not implement R2 in this task.",
    ]
    return "\n".join(rows) + "\n"


def main() -> None:
    """Publish once or verify exact deterministic regeneration in memory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("build", "verify"))
    args = parser.parse_args()
    result = build()
    rendered = render(result)
    if args.operation == "build":
        # Only derived Stage D outputs may be regenerated; sealed inputs never
        # reach this write boundary. Original primary metrics remain unchanged.
        write(
            TextFile(resolve_path(CASE / "analysis.json"), json_bytes(result).decode()),
            overwrite=True,
        )
        write(TextFile(resolve_path(CASE / "analysis.md"), rendered), overwrite=True)
    elif (
        binary(CASE / "analysis.json") != json_bytes(result)
        or binary(CASE / "analysis.md") != rendered.encode()
    ):
        raise ValueError("Stage D deterministic replay mismatch.")
    print(
        json.dumps(
            {
                "decision": result["decision"],
                "positive_global": {
                    a: result["arms"][a]["positive_global_count"] for a in ("A", "B")
                },
                "own_required_reach": {
                    a: len(result["arms"][a]["required_cells"]) for a in ("A", "B")
                },
            }
        )
    )


if __name__ == "__main__":
    main()
