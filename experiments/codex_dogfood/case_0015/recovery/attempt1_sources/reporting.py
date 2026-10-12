# Copyright (c) 2026
# ruff: noqa: PERF401, PLR2004, COM812, E501, EM101, TRY003 -- complete deterministic mechanical publication
"""Publish complete lossless surfaces and diagnostics solely from durable returns."""

from __future__ import annotations

import gzip
import json
import time
from fractions import Fraction
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

from experiments.bm25f.trace import serialize
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    put_binary,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal, exclusive
from experiments.codex_dogfood.case_0015 import freeze, protocol
from experiments.codex_dogfood.case_0015.stage_b import validation
from experiments.codex_dogfood.case_0015.stage_b.execute import (
    EXECUTION,
    SCHEDULE,
    source_hashes,
)

SURFACES = (
    "fields.json.gz",
    "native_statistics.json.gz",
    "union_statistics.json.gz",
    "arm_a.json.gz",
    "arm_b.json.gz",
    "contributions.json.gz",
    "decomposition.json.gz",
    "reference.json.gz",
    "top_k.json.gz",
)
METADATA = (
    "summary.json",
    "costs.json",
    "trace.json",
    "TRACE.md",
    "STAGE_B_REVIEW.md",
    "validation.json",
)


def exact(value: Fraction) -> dict[str, int]:
    """Represent exact binary-rational totals independently of float rounding."""
    return {"numerator": value.numerator, "denominator": value.denominator}


def pairwise(a: list[dict[str, Any]], b: list[dict[str, Any]]) -> dict[str, Any]:
    """Retain both top-K unions, crossings, all inversions and complete movements."""
    before = {r["document_identity"]: r for r in a}
    after = {r["document_identity"]: r for r in b}
    if before.keys() != after.keys() or len(before) != len(a) or len(after) != len(b):
        raise ValueError("EXPERIMENTAL_CONTRACT_DEFECT: candidate identity")
    movements = [
        {
            "document_identity": key,
            "content_identity": row["content_identity"],
            "address": row["address"],
            "A_rank": row["rank"],
            "B_rank": after[key]["rank"],
            "upward_positions": row["rank"] - after[key]["rank"],
            "A_score": row["score"],
            "B_score": after[key]["score"],
            "score_delta": after[key]["score"] - row["score"],
        }
        for key, row in before.items()
    ]
    top = {}
    for k in (10, 20, 50):
        first = {r["document_identity"] for r in a[:k]}
        second = {r["document_identity"] for r in b[:k]}
        union = sorted(first | second, key=lambda key: before[key]["rank"])
        pairs = [
            [x, y]
            for i, x in enumerate(union)
            for y in union[i + 1 :]
            if after[x]["rank"] > after[y]["rank"]
        ]
        top[str(k)] = {
            "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
            "union": union,
            "entered": sorted(second - first, key=lambda key: after[key]["rank"]),
            "exited": sorted(first - second, key=lambda key: before[key]["rank"]),
            "pair_inversions": pairs,
            "inversion_count": len(pairs),
            "movements": [
                m for m in movements if m["document_identity"] in first | second
            ],
        }
    return {
        "top_k": top,
        "movements": movements,
        "largest_upward": sorted(
            movements, key=lambda r: (-r["upward_positions"], r["A_rank"])
        )[:5],
        "largest_downward": sorted(
            movements, key=lambda r: (r["upward_positions"], r["A_rank"])
        )[:5],
    }


def decomposition(
    comparison: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Prove exact telescoping with disclosed term and document grouping residuals."""
    rows = validation.diagnostic(comparison)
    a = {r["document_identity"]: r for r in comparison["A"]}
    b = {r["document_identity"]: r for r in comparison["B"]["matches"]}
    keys = (
        "union_idf_delta",
        "pre_saturation_weight_delta",
        "cross_field_single_saturation_delta",
    )
    sums = dict.fromkeys(keys, Fraction(0))
    for row in rows:
        key = row["document_identity"]
        ta = {t["term"]: t for t in row["terms"]}
        bterms = b[key]["terms"]
        deltas = Fraction(0)
        for bt in bterms:
            t = ta[bt["term"]]
            subtotal = sum((Fraction(t[k]) for k in keys), Fraction(0))
            residual = (
                Fraction(bt["term_score"])
                - Fraction(t["native_additive_term"])
                - subtotal
            )
            t["exact_stage_subtraction_residual"] = exact(residual)
            deltas += subtotal + residual
            for component in keys:
                sums[component] += Fraction(t[component])
        ag = Fraction(a[key]["score"]) - sum(
            (Fraction(t["native_additive_term"]) for t in row["terms"]), Fraction(0)
        )
        bg = Fraction(b[key]["score"]) - sum(
            (Fraction(t["term_score"]) for t in bterms), Fraction(0)
        )
        expected = Fraction(b[key]["score"]) - Fraction(a[key]["score"])
        if deltas + bg - ag != expected:
            raise ValueError("Explanatory decomposition does not reconstruct")
        row["exact_native_grouping_residual"] = exact(ag)
        row["exact_b_grouping_residual"] = exact(bg)
        row["exact_document_score_delta"] = exact(expected)
        row["reconstruction"] = "PASS"
    return rows, {
        k: {"exact": exact(v), "float_display": float(v)} for k, v in sums.items()
    }


def joined(comparison: dict[str, Any], union: dict[str, Any]) -> list[dict[str, Any]]:
    """Own every candidate/term's native and BM25F evidence together, without labels."""
    native = {r["document_identity"]: r for r in comparison["A"]}
    rows = []
    for b in comparison["B"]["matches"]:
        a = native[b["document_identity"]]
        channels = {
            "CONTENT": {t["normalized_term"]: t for t in a["content_terms"]},
            "FILENAME": {t["normalized_term"]: t for t in a["filename_terms"]},
        }
        terms = []
        for t in b["terms"]:
            term = t["term"]
            membership = union["terms"].get(
                term, {"CONTENT": [], "FILENAME": [], "union": [], "df_union": 0}
            )
            fields = {}
            for f in ("CONTENT", "FILENAME"):
                fields[f] = {
                    **t[f],
                    "native_df": len(membership[f]),
                    "native_idf": validation.idf(union["N"], len(membership[f])),
                    "native_arm_a_contribution": channels[f]
                    .get(term, {})
                    .get("contribution", 0.0),
                    "native_positive_contribution_present": term in channels[f],
                }
            terms.append(
                {
                    **t,
                    **fields,
                    "union_membership_owner": "union_statistics.json.gz:terms/" + term,
                }
            )
        rows.append(
            {
                "address": b["address"],
                "document_identity": b["document_identity"],
                "content_identity": b["content_identity"],
                "collection_position": b["collection_position"],
                "A_rank": a["rank"],
                "B_rank": b["rank"],
                "A_score": a["score"],
                "B_score": b["score"],
                "terms": terms,
            }
        )
    return rows


def data(root: Path) -> dict[str, Any]:
    """Authenticate the journal and reconstruct mechanical facts from returned values."""
    if (root / "capture_failure.json").exists() or not (
        root / "execution_completed.json"
    ).exists():
        raise ValueError("Only complete successful capture may publish")
    j = Journal.load(root)
    j.ready()
    operations = j.state["operations"]
    if tuple(o["identity"] for o in operations) != SCHEDULE or any(
        o["invocations"] != 1 or o["status"] != "RETURNED" for o in operations
    ):
        raise ValueError("Exactly-once schedule differs")
    marker = j.state["marker"]
    if (
        marker["implementation_sha256"] != source_hashes()
        or marker["initial_counts"] != protocol.COUNTS
        or marker["execution"] != EXECUTION
    ):
        raise ValueError("Capture source/initial-count/identity mismatch")
    values = j.state["values"]
    state = values["index:native-prepare"]
    union = values["statistics:union-prepare"]
    surface = validation.validate_fields(state, union)
    frozen_resources = json.loads(
        gzip.decompress(binary(freeze.CASE / "resources.json.gz"))
    )
    if len(surface["documents"]) != 515:
        raise ValueError("Frozen 515-resource universe differs")
    for d, r in zip(state.collection.documents, frozen_resources, strict=True):
        if (
            str(d.id),
            str(d.resource.content_identity),
            str(d.resource.address),
            d.text,
        ) != (
            r["document_identity"],
            r["content_identity"],
            r["address"],
            r["content"],
        ):
            raise ValueError("Frozen exact frame resource join differs")
    design = read_json(freeze.CASE / "protocol.json")
    arms_a, arms_b, pairs, diagnostics, contributions, aggregate = (
        {},
        {},
        {},
        {},
        {},
        {},
    )
    for i, q in enumerate(design["queries"], 1):
        key = "Q" + str(i)
        comparison = validation.validate_pair(
            state, values[f"query:{key}:A"], values[f"query:{key}:B"], surface, union, q
        )
        binding = {
            "case": "0015",
            "task_identity": design["task_identity"],
            "query_identity": q["identity"],
            "obligation_identity": q["obligation"],
            "frame": marker["frame"],
        }
        arms_a[key] = {**binding, **validation.native_surface(values[f"query:{key}:A"])}
        arms_b[key] = {**binding, **comparison["B"]}
        pairs[key] = pairwise(comparison["A"], comparison["B"]["matches"])
        diagnostics[key], aggregate[key] = decomposition(comparison)
        contributions[key] = {**binding, "candidates": joined(comparison, union)}
    reference = values["query:reference"]
    ref_query = {
        "analysis": design["global_reference_lane"]["analysis"],
        "normalized_terms": reference.query.normalized_terms,
    }
    ref_surface = validation.validate_native(
        reference, state, surface, union, ref_query
    )
    durations = {o["identity"]: o["runtime_ns"] for o in operations}
    shared = sum(durations[k] for k in SCHEDULE[:4])
    a_cost = sum(durations[f"query:Q{i}:A"] for i in range(1, 7))
    b_cost = sum(durations[f"query:Q{i}:B"] for i in range(1, 7))
    costs = {
        "shared_operations_ns": {k: durations[k] for k in SCHEDULE[:4]},
        "shared_charged_equally_ns": shared,
        "arm_a_native_retrieval_ns": a_cost,
        "arm_b_bm25f_scoring_ns": b_cost,
        "charged_A_ns": shared + a_cost,
        "charged_B_ns": shared + b_cost,
        "reference_ns": durations["query:reference"],
        "query_operations_ns": {
            k: v for k, v in durations.items() if k.startswith("query:")
        },
        **read_json(root / "capture_costs.json"),
        "counting": "Top-level scientific intervals only. Shared charged once to each arm. Native filename construction inside A/reference included in native timing. Durability, mechanical checks, wall and publication are descriptive; no double counting or outcome selection.",
    }
    candidate_counts = {q: len(a["matches"]) for q, a in arms_a.items()}
    summary = {
        "case": "0015",
        "execution": EXECUTION,
        "stage_b": "CAPTURED",
        "stage_a": marker["stage_a"],
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "journal_pairs": len(operations),
        "journal_events": j.events,
        "native_retries": 0,
        "failures": 0,
        "operation_counts": {o["identity"]: o["invocations"] for o in operations},
        "shared_field_preparations": 1,
        "native_content_index_builds": 1,
        "bm25f_union_statistics_preparations": 1,
        "native_intrinsic_filename_builds": 7,
        "candidate_counts": candidate_counts,
        "total_candidate_occurrences": sum(candidate_counts.values()),
        "candidate_identity": "PASS",
        "native_arm_a_authenticity": "PASS",
        "formula_reconstruction": "PASS",
        "decomposition_reconstruction": "PASS",
        "reference_safety": "PASS",
        "frame": marker["frame"],
        "field_statistics": {
            "N": surface["N"],
            "content_average_length": surface["content_average_length"],
            "filename_average_length": surface["filename_average_length"],
            "distinct_union_terms": len(union["terms"]),
        },
        "diagnostic_aggregates": aggregate,
        "top_k_inversions": {
            q: {k: v["inversion_count"] for k, v in p["top_k"].items()}
            for q, p in pairs.items()
        },
        "largest_movements": {
            q: {"upward": p["largest_upward"], "downward": p["largest_downward"]}
            for q, p in pairs.items()
        },
    }
    statistics = {
        "N": union["N"],
        "content_average_length": surface["content_average_length"],
        "filename_average_length": surface["filename_average_length"],
        "terms": {
            t: {
                **m,
                "content_df": len(m["CONTENT"]),
                "filename_df": len(m["FILENAME"]),
                "content_idf": validation.idf(union["N"], len(m["CONTENT"])),
                "filename_idf": validation.idf(union["N"], len(m["FILENAME"])),
                "idf_union": validation.idf(union["N"], m["df_union"]),
            }
            for t, m in union["terms"].items()
        },
    }
    return {
        "design": design,
        "fields": surface,
        "statistics": statistics,
        "union": union,
        "arm_a": arms_a,
        "arm_b": arms_b,
        "contributions": contributions,
        "diagnostics": diagnostics,
        "pairs": pairs,
        "reference": {
            "case": "0015",
            "task_identity": design["task_identity"],
            "frame": marker["frame"],
            **ref_surface,
        },
        "summary": summary,
        "costs": costs,
    }


def surfaces(d: dict[str, Any]) -> dict[str, bytes]:
    """Deterministic gzip of complete lossless JSON, without native operations."""
    names = (
        "fields",
        "statistics",
        "union",
        "arm_a",
        "arm_b",
        "contributions",
        "diagnostics",
        "reference",
        "pairs",
    )
    return {
        name: gzip.compress(serialize(d[key]), mtime=0)
        for name, key in zip(SURFACES, names, strict=True)
    }


def render(title: str, d: dict[str, Any], costs: dict[str, Any]) -> str:
    """Expose all candidate ranks/scores, inputs and diagnostics without relevance labels."""
    parts = [
        f"# {title}\n\nGOLD = ABSENT\n\nEFFECTIVENESS = UNKNOWN\n\nR2 OUTCOME = NOT_SELECTED\n\nRANK MOVEMENT IS NOT EFFECTIVENESS EVIDENCE WITHOUT GOLD.\n\nSEARCH_POLICY_FAILURE = NOT_ASSESSED.\n\n",
        "## Exact task\n\n" + d["design"]["task_text"] + "\n",
    ]
    for key in (
        "requirement_matrix",
        "queries",
        "scorer_semantics",
        "bm25f_formula",
        "parameters",
    ):
        parts.append(
            f"## Frozen {key}\n\n```json\n"
            + serialize(d["design"][key]).decode()
            + "```\n\n"
        )
    parts.append(
        "## Execution, journal, statistics and mechanical checks\n\n```json\n"
        + serialize(d["summary"]).decode()
        + "```\n\n"
    )
    parts.append(
        "## Captured cost\n\n```json\n" + serialize(costs).decode() + "```\n\n"
    )
    parts.append(
        "## Complete field-length inventory\n\n| Resource | CONTENT length | FILENAME length | Stem |\n|---|---:|---:|---|\n"
    )
    for row in d["fields"]["documents"]:
        parts.append(
            f"| {row['address']} | {row['CONTENT']['length']} | {row['FILENAME']['length']} | {row['FILENAME']['stem']} |\n"
        )
    for q, a in d["arm_a"].items():
        b = {r["document_identity"]: r for r in d["arm_b"][q]["matches"]}
        parts.append(
            f"\n## {q}: every candidate, exact native A and true BM25F B\n\n| Resource | A rank | B rank | A score hex | B score hex | Upward positions |\n|---|---:|---:|---|---|---:|\n"
        )
        for row in a["matches"]:
            t = b[row["document_identity"]]
            parts.append(
                f"| {row['address']} | {row['rank']} | {t['rank']} | {row['score'].hex()} | {t['score'].hex()} | {row['rank'] - t['rank']} |\n"
            )
        parts.append(
            "\n### Per-term df and IDF\n\n| Term | Content df | Filename df | Union df | Content IDF hex | Filename IDF hex | Union IDF hex |\n|---|---:|---:|---:|---|---|---|\n"
        )
        for t in d["arm_b"][q]["field_statistics"]["query_terms"]:
            term = t["term"]
            n = d["fields"]["N"]
            parts.append(
                f"| {term} | {t['content_df']} | {t['filename_df']} | {t['df_union']} | {validation.idf(n, t['content_df']).hex()} | {validation.idf(n, t['filename_df']).hex()} | {validation.idf(n, t['df_union']).hex()} |\n"
            )
        parts.append(
            "\n### Complete top-K crossings and inversion identities\n\n```json\n"
            + serialize(d["pairs"][q]["top_k"]).decode()
            + "```\n\n"
        )
    parts.append(
        "## Full provenance ownership\n\nfields.json.gz retains every canonical observation/token and tf/length; native_statistics.json.gz and union_statistics.json.gz retain every term's membership, field df/IDF and union df/IDF. arm_a.json.gz and arm_b.json.gz retain all six exact query-bound candidate results. contributions.json.gz joins both field channels and every distinct term's normalized/weighted/combined tf, IDFs, saturation and scores. decomposition.json.gz retains the frozen diagnostic and exact rational residuals. top_k.json.gz owns full movements/inversions/crossings; reference.json.gz owns the unchanged separate canonical whole-task lane. All are pretty lossless JSON under deterministic gzip. Immutable operations/ owns complete native object graphs and recoverable pickle segments; projections never replace authoritative native A.\n\n"
    )
    parts.append(
        "Frozen decomposition order is union-IDF replacement, moving filename weight inside saturation, then cross-field single saturation. Normalization inputs are unchanged; exact field denominators and native channel/grouping/subtraction residuals remain explicit. No intermediate stages are ranked and no relevance conclusion is drawn.\n"
    )
    return "".join(parts)


def metadata(d: dict[str, Any], receipt: dict[str, Any]) -> dict[str, bytes]:
    """Replay metadata and Markdown from captured scientific and descriptive values."""
    costs = {**d["costs"], "derived_publication": receipt}
    owners = dict(
        zip(
            (
                "field_observations",
                "native_statistics",
                "union_statistics",
                "arm_a",
                "arm_b",
                "complete_contributions",
                "decomposition",
                "reference",
                "top_k",
            ),
            SURFACES,
            strict=True,
        )
    )
    trace = {
        "schema": "case-0015-stage-b-trace-v1",
        "summary": d["summary"],
        "costs": costs,
        "complete_surfaces": owners,
        "claims": "Mechanical capture only; no gold, witness analysis or outcome selection",
    }
    result = {
        "mechanical_capture": "PASS",
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
        "checks": [
            "Stage A sealed bindings",
            "exclusive claim and exact 17-operation schedule",
            "zero initial counts and no retries",
            "complete immutable native returns",
            "exact frozen frame/content/document identities",
            "exact canonical content and filename-stem observations",
            "per-field length/average/tf/df",
            "union membership/cardinality/document once",
            "native Arm A scores/ranks/contributions/ties",
            "identical positive A/B candidates without repair",
            "frozen B parameters and query analyses",
            "pre-saturation aggregation, one IDF, one saturation",
            "exact every-term/document reconstruction",
            "frozen diagnostic and exact rational residual reconstruction",
            "unchanged separate reference",
            "deterministic float.hex JSON/gzip/Markdown replay",
        ],
        "operation_counts": d["summary"]["operation_counts"],
    }
    return {
        "summary.json": serialize(d["summary"]),
        "costs.json": serialize(costs),
        "trace.json": serialize(trace),
        "TRACE.md": render("Case 0015 Stage B trace", d, costs).encode(),
        "STAGE_B_REVIEW.md": render(
            "Case 0015 Stage B mechanical human review", d, costs
        ).encode(),
        "validation.json": json_bytes(result),
    }


def publish(root: Path) -> None:
    """Exclusively derive outputs; refusal never reruns a scientific operation."""
    if any(
        (root / name).exists()
        for name in (*SURFACES, *METADATA, "publication_costs.json", "integrity.json")
    ):
        raise FileExistsError("Stage B publication overwrite refused")
    started = time.perf_counter_ns()
    d = data(root)
    raw = surfaces(d)
    construction = time.perf_counter_ns() - started
    writing_started = time.perf_counter_ns()
    for name, value in raw.items():
        put_binary(root / name, value)
    receipt = {
        "derived_artifact_construction_ns": construction,
        "large_surface_publication_ns": time.perf_counter_ns() - writing_started,
        "scope": "Descriptive, excluded from mechanism cost; metadata/receipt/integrity publication itself is outside these measured intervals.",
    }
    exclusive(root / "publication_costs.json", receipt)
    for name, value in metadata(d, receipt).items():
        put_text(root / name, value.decode())
    integrity = {
        "schema": "case-0015-stage-b-integrity-v1",
        "execution": EXECUTION,
        "implementation_sha256": source_hashes(),
        "stage_a_integrity_sha256": digest(binary(freeze.CASE / "integrity.json")),
        "sha256": {
            p.relative_to(root).as_posix(): digest(binary(p))
            for p in sorted(root.rglob("*"))
            if p.is_file()
        },
        "hash_scopes": "Exact gzip and canonical UTF-8 LF journal/projection/Markdown bytes; floating projections use float.hex; .local excluded",
    }
    put_text(root / "integrity.json", json_bytes(integrity).decode())


def verify(root: Path) -> None:
    """Authenticate every artifact and byte-replay derived surfaces without native calls."""
    seal = read_json(root / "integrity.json")
    actual = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and p.name != "integrity.json"
    }
    if (
        actual != set(seal["sha256"])
        or any(digest(binary(root / p)) != h for p, h in seal["sha256"].items())
        or seal["implementation_sha256"] != source_hashes()
    ):
        raise ValueError("Stage B integrity/tamper mismatch")
    d = data(root)
    values = {**surfaces(d), **metadata(d, read_json(root / "publication_costs.json"))}
    for name, raw in values.items():
        if binary(root / name) != raw:
            raise ValueError("Stage B deterministic replay/tamper mismatch: " + name)
