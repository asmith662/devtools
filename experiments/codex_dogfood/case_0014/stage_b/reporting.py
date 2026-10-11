# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812, E501, C901, PLR0912, PLR0915, PLR2004 -- complete mechanical validation/report boundary
"""Complete mechanical diagnostics over captured evidence; no gold or gates."""

from __future__ import annotations

import gzip
import json
from fractions import Fraction
from typing import TYPE_CHECKING, Any

from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b.graph import describe
from experiments.codex_dogfood.case_0014 import freeze, protocol
from experiments.codex_dogfood.case_0014.stage_b.execute import (
    EXECUTION,
    SCHEDULE,
    source_hashes,
)
from experiments.query_term_weighting.classification import Arm
from experiments.query_term_weighting.scoring import score
from experiments.query_term_weighting.serialization import trace

if TYPE_CHECKING:
    from experiments.codex_dogfood.case_0012.stage_b.durability import Journal


def exact(value: Fraction) -> str:
    """Retain exact binary-rational diagnostics without altering treatment scores."""
    return str(value.numerator) + "/" + str(value.denominator)


def role_sums(row: dict[str, Any]) -> dict[str, Fraction]:
    """Sum mathematical channel-adjusted weighted contributions exactly."""
    totals = {
        r: Fraction(0) for r in ("EXPLICIT_ANCHOR", "SEMANTIC", "GENERIC_OPERATION")
    }
    for c in row["contributions"]:
        totals[c["role"]] += Fraction(c["weighted"]) * Fraction(c["channel_weight"])
    return totals


def attribution(
    a: dict[str, Any], b: dict[str, Any], c: dict[str, Any]
) -> dict[str, Any]:
    """Verify role-only changes plus the frozen ordered float summation exactly."""
    rows = []
    for left, middle, right in zip(
        sorted(a["matches"], key=lambda r: r["collection_position"]),
        sorted(b["matches"], key=lambda r: r["collection_position"]),
        sorted(c["matches"], key=lambda r: r["collection_position"]),
        strict=True,
    ):
        identities = tuple(
            (
                r["document_id"],
                r["address"],
                r["content_identity"],
                r["collection_position"],
            )
            for r in (left, middle, right)
        )
        if len(set(identities)) != 1:
            raise ValueError("EXPERIMENTAL_CONTRACT_DEFECT: candidate identity")
        for x, y, z in zip(
            left["contributions"],
            middle["contributions"],
            right["contributions"],
            strict=True,
        ):
            if any(
                x[k] != y[k] or x[k] != z[k]
                for k in (
                    "term",
                    "role",
                    "channel",
                    "native",
                    "native_hex",
                    "channel_weight",
                )
            ):
                raise ValueError("Native contribution/provenance changed")
            expected = (
                (1, 2, 2)
                if x["role"] == "EXPLICIT_ANCHOR"
                else (1, 1, 0.5)
                if x["role"] == "GENERIC_OPERATION"
                else (1, 1, 1)
            )
            if tuple(v["multiplier"] for v in (x, y, z)) != expected or any(
                v["weighted"] != v["native"] * v["multiplier"]
                or v["weighted_hex"] != float(v["weighted"]).hex()
                for v in (x, y, z)
            ):
                raise ValueError("QUERY_WEIGHT_APPLICATION_DEFECT")
        sums = [role_sums(r) for r in (left, middle, right)]
        anchor = sums[0]["EXPLICIT_ANCHOR"]
        attenuation = -sums[0]["GENERIC_OPERATION"] / 2
        mathematical = [sum(s.values(), Fraction(0)) for s in sums]
        rounding = [
            Fraction(r["weighted_score"]) - total
            for r, total in zip((left, middle, right), mathematical, strict=True)
        ]
        if (
            sums[0]["SEMANTIC"] != sums[1]["SEMANTIC"]
            or sums[0]["SEMANTIC"] != sums[2]["SEMANTIC"]
            or mathematical[1] - mathematical[0] != anchor
            or mathematical[2] - mathematical[1] != attenuation
            or mathematical[2] - mathematical[0] != anchor + attenuation
        ):
            raise ValueError("Role-only attribution failed")
        # Binary floating point need not distribute over subtraction. Expose
        # its exact residual; reconstruct using the sealed channel/order contract.
        differences = {}
        for name, i, j, delta in (
            ("B-A", 0, 1, anchor),
            ("C-B", 1, 2, attenuation),
            ("C-A", 0, 2, anchor + attenuation),
        ):
            actual = Fraction((left, middle, right)[j]["weighted_score"]) - Fraction(
                (left, middle, right)[i]["weighted_score"]
            )
            residual = rounding[j] - rounding[i]
            if actual != delta + residual:
                raise ValueError("Ordered float attribution mismatch")
            differences[name] = {
                "role_delta_exact": exact(delta),
                "float_score_difference_exact": exact(actual),
                "ordered_sum_rounding_difference_exact": exact(residual),
            }
        rows.append(
            {
                "address": left["address"],
                "document_id": left["document_id"],
                "anchor_emphasis_delta_exact": exact(anchor),
                "generic_attenuation_delta_exact": exact(attenuation),
                "rank_A": left["rank"],
                "rank_B": middle["rank"],
                "rank_C": right["rank"],
                "decomposition": differences,
            }
        )
    return {
        "status": "PASS",
        "arithmetic": "Exact role multiplication and unchanged ordered float channel reconstruction; binary-rational diagnostics disclose floating subtraction residuals, never normalize scores",
        "documents": rows,
    }


def pairwise(baseline: dict[str, Any], treatment: dict[str, Any]) -> dict[str, Any]:
    """Publish full movements, top-K crossings and pair-order inversion sets."""
    before = {r["document_id"]: r for r in baseline["matches"]}
    after = {r["document_id"]: r for r in treatment["matches"]}
    if before.keys() != after.keys():
        raise ValueError("EXPERIMENTAL_CONTRACT_DEFECT: candidate difference")
    movements = [
        {
            "document_id": key,
            "address": row["address"],
            "before": row["rank"],
            "after": after[key]["rank"],
            "upward_positions": row["rank"] - after[key]["rank"],
            "score_delta": after[key]["weighted_score"] - row["weighted_score"],
        }
        for key, row in before.items()
    ]
    top = {}
    for k in (10, 20, 50):
        first = {r["document_id"] for r in baseline["matches"][:k]}
        second = {r["document_id"] for r in treatment["matches"][:k]}
        union = sorted(first | second, key=lambda key: before[key]["rank"])
        inversions = [
            [a, b]
            for i, a in enumerate(union)
            for b in union[i + 1 :]
            if after[a]["rank"] > after[b]["rank"]
        ]
        entered = sorted(second - first, key=lambda key: after[key]["rank"])
        exited = sorted(first - second, key=lambda key: before[key]["rank"])
        top[str(k)] = {
            "definition": "Pair-order reversals within union of both top-K sets; crossings are separate",
            "pair_inversions": inversions,
            "inversion_count": len(inversions),
            "entered": entered,
            "exited": exited,
            "crossing_count_each_direction": len(entered),
        }
    return {
        "top_k": top,
        "movements": movements,
        "largest_upward": sorted(
            movements, key=lambda r: (-r["upward_positions"], r["before"])
        )[:5],
        "largest_downward": sorted(
            movements, key=lambda r: (r["upward_positions"], r["before"])
        )[:5],
    }


def totals(arm: dict[str, Any]) -> dict[str, Any]:
    """Aggregate complete contribution channels/roles without relevance labels."""
    by_role = {
        r: Fraction(0) for r in ("EXPLICIT_ANCHOR", "SEMANTIC", "GENERIC_OPERATION")
    }
    by_channel = {
        "content": Fraction(0),
        "filename_before_0_25": Fraction(0),
        "filename_after_0_25": Fraction(0),
    }
    terms: dict[str, dict[str, Any]] = {}
    for row in arm["matches"]:
        for term in row["contributions"]:
            weighted = Fraction(term["weighted"])
            by_role[term["role"]] += weighted * Fraction(term["channel_weight"])
            if term["channel"] == "content":
                by_channel["content"] += weighted
            else:
                by_channel["filename_before_0_25"] += weighted
                by_channel["filename_after_0_25"] += weighted / 4
            item = terms.setdefault(
                term["term"],
                {
                    "role": term["role"],
                    "documents": set(),
                    "native_channel_adjusted": Fraction(0),
                    "weighted_channel_adjusted": Fraction(0),
                },
            )
            item["documents"].add(row["document_id"])
            item["native_channel_adjusted"] += Fraction(term["native"]) * Fraction(
                term["channel_weight"]
            )
            item["weighted_channel_adjusted"] += weighted * Fraction(
                term["channel_weight"]
            )

    def project(values: dict[str, Fraction]) -> dict[str, Any]:
        return {
            k: {"exact": exact(v), "float_display": float(v)} for k, v in values.items()
        }

    return {
        "roles": project(by_role),
        "channels": project(by_channel),
        "terms": {
            k: {
                "role": v["role"],
                "documents": sorted(v["documents"]),
                "matching_documents": len(v["documents"]),
                "native_total_exact": exact(v["native_channel_adjusted"]),
                "weighted_total_exact": exact(v["weighted_channel_adjusted"]),
                "delta_exact": exact(
                    v["weighted_channel_adjusted"] - v["native_channel_adjusted"]
                ),
            }
            for k, v in terms.items()
        },
    }


def outputs(journal: Journal) -> dict[str, bytes]:
    """Validate and render all captured mechanical facts deterministically."""
    journal.ready()
    marker = journal.state["marker"]
    operations = journal.state["operations"]
    if (
        tuple(o["identity"] for o in operations) != SCHEDULE
        or any(o["invocations"] != 1 or o["status"] != "RETURNED" for o in operations)
        or marker["implementation_sha256"] != source_hashes()
    ):
        raise ValueError("Exactly-once schedule or implementation mismatch")
    captured = journal.state["values"]
    index = captured["index-build"]
    documents = captured["frame:prepare"]
    if (
        index.corpus_statistics.collection_analysis.document_collection is not documents
        or len(documents.documents) != 515
    ):
        raise ValueError("Shared native index/frame identity mismatch")
    frozen_rows = json.loads(gzip.decompress(binary(freeze.CASE / "resources.json.gz")))
    for d, row in zip(documents.documents, frozen_rows, strict=True):
        if (
            str(d.id) != row["document_identity"]
            or str(d.resource.address) != row["address"]
            or str(d.resource.content_identity) != row["content_identity"]
            or d.resource.content != row["content"]
        ):
            raise ValueError("Frozen frame identity/content differs")
    arms: dict[str, dict[str, Any]] = {a.name: {} for a in Arm}
    queries: dict[str, Any] = {}
    native_surfaces = {}
    for p in protocol.policies(protocol.authored()["task_text"]):
        key = p.identity.value
        native = captured["query:" + key]
        if (
            native.index is not index
            or native.maximum_results != 515
            or native.query != p.native_query
        ):
            raise ValueError("Native query/index/analysis mismatch")
        for arm in Arm:
            result = trace(score(native, p, arm))
            if result != captured[f"construct:{arm.name}:{key}"]:
                raise ValueError("Captured arm reconstruction mismatch")
            arms[arm.name][key] = result
        a, b, c = (arms[n][key] for n in ("A", "B", "C"))
        if tuple(
            (r["document_id"], r["weighted_score"]) for r in a["matches"]
        ) != tuple(
            (str(m.document_statistics.analysis.document.id), m.score)
            for m in native.matches
        ):
            raise ValueError("QUERY_WEIGHT_APPLICATION_DEFECT: A/native mismatch")
        queries[key] = {
            "obligation": p.obligation.value,
            "candidate_count": len(native.matches),
            "candidate_safety": "PASS",
            "arm_a_native_equality": "PASS",
            "score_ranges": {
                n: {
                    "maximum": value[key]["matches"][0]["weighted_score"]
                    if native.matches
                    else None,
                    "minimum": value[key]["matches"][-1]["weighted_score"]
                    if native.matches
                    else None,
                }
                for n, value in arms.items()
            },
            "comparisons": {
                "B-A": pairwise(a, b),
                "C-A": pairwise(a, c),
                "C-B": pairwise(b, c),
            },
            "attribution": attribution(a, b, c),
            "contribution_totals": {n: totals(value[key]) for n, value in arms.items()},
            "native_filename_statistics_identity": digest(
                json_bytes(describe(native.filename_index))
            ),
        }
        native_surfaces[key] = a
    reference = captured["query:reference"]
    if (
        reference.index is not index
        or reference.query.text != protocol.authored()["task_text"]
        or reference.maximum_results != 515
    ):
        raise ValueError("Reference lane changed")
    filename_identity = digest(json_bytes(describe(reference.filename_index)))
    if any(
        q["native_filename_statistics_identity"] != filename_identity
        for q in queries.values()
    ):
        raise ValueError("Native filename statistics changed across queries")
    native_times = {o["identity"]: o["runtime_ns"] for o in operations}
    shared = {
        "frame_preparation_ns": native_times["frame:prepare"],
        "canonical_index_ns": native_times["index-build"],
        "obligation_native_acquisition_ns": sum(
            native_times["query:Q" + str(i)] for i in range(1, 7)
        ),
        "reference_native_acquisition_ns": native_times["query:reference"],
    }
    shared_charge = (
        shared["frame_preparation_ns"]
        + shared["canonical_index_ns"]
        + shared["obligation_native_acquisition_ns"]
    )
    specific = {
        a.name: {
            "queries": {
                "Q" + str(i): native_times[f"construct:{a.name}:Q{i}"]
                for i in range(1, 7)
            },
            "construction_ns": sum(
                native_times[f"construct:{a.name}:Q{i}"] for i in range(1, 7)
            ),
        }
        for a in Arm
    }
    for value in specific.values():
        value["charged_ns"] = shared_charge + value["construction_ns"]
    costs = {
        "shared": shared,
        "shared_charged_equally_ns": shared_charge,
        "arms": specific,
        "publication_durability": read_json(journal.root / "publication_cost.json"),
        "classification": "Frozen in Stage A; restoration verification separately reported, not mechanism charged",
        "reference": "Separate unchanged lane; not mechanism charged",
        "accounting": "All top-level native times single-run; no child, wall, publication or durability double counting; no timing reruns",
    }
    summary = {
        "execution": EXECUTION,
        "stage_b": "CAPTURED",
        "journal_pairs": len(operations),
        "index_builds": 1,
        "obligation_query_executions": {"Q" + str(i): 1 for i in range(1, 7)},
        "reference_query_executions": 1,
        "arm_construction_records": 18,
        "candidate_counts": {k: q["candidate_count"] for k, q in queries.items()},
        "total_candidate_occurrences": sum(
            q["candidate_count"] for q in queries.values()
        ),
        "reference_candidate_count": len(reference.matches),
        "candidate_identity": "A=B=C; PASS",
        "native_statistics": "UNCHANGED",
        "role_attribution": "PASS",
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
    }
    frozen_design = read_json(freeze.CASE / "protocol.json")
    protocol_surface = {
        k: frozen_design[k]
        for k in (
            "case",
            "task_identity",
            "task_text",
            "requirement_matrix",
            "queries",
            "taxonomy",
            "weights",
            "arms",
            "scorer_semantics",
        )
    }
    mechanical_trace = {
        "summary": summary,
        "stage_a_protocol": protocol_surface,
        "queries": queries,
        "costs": costs,
        "journal_operations": operations,
        "reference_identity": digest(json_bytes(describe(reference))),
        "native_index_identity": digest(json_bytes(describe(index))),
        "native_filename_statistics_identity": filename_identity,
        "complete_surface_artifacts": [
            "native_capture.json.gz",
            "native_contributions.json.gz",
            "arm_a.json.gz",
            "arm_b.json.gz",
            "arm_c.json.gz",
            "reference.json.gz",
        ],
    }
    review = (
        "# Case 0014 Stage B mechanical review\n\nGOLD = ABSENT\n\nEFFECTIVENESS = UNKNOWN\n\nR1.7 OUTCOME = NOT_SELECTED\n\nRANK MOVEMENT IS NOT EFFECTIVENESS EVIDENCE WITHOUT GOLD\n\nSEARCH_POLICY_FAILURE = NOT_ASSESSED\n\n## Exact task\n\n"
        + protocol.authored()["task_text"]
        + "\n## Complete frozen obligations, queries, classifications and multipliers\n\nSee unchanged [Stage A](../../../STAGE_A_REVIEW.md) and trace.json's stage_a_protocol.\n\n## Exactly-once summary\n\n```json\n"
        + json_bytes(summary).decode()
        + "```\n\n## Candidate counts and top-K pair inversions\n\n| Query | Candidates | B-A K10/20/50 | C-A K10/20/50 | C-B K10/20/50 |\n|---|---:|---|---|---|\n"
    )
    for key, q in queries.items():
        counts = [
            "/".join(
                str(q["comparisons"][pair]["top_k"][str(k)]["inversion_count"])
                for k in (10, 20, 50)
            )
            for pair in ("B-A", "C-A", "C-B")
        ]
        review += f"| {key} | {q['candidate_count']} | {' | '.join(counts)} |\n"
    review += (
        "\nPair inversions count order reversals inside the union of both top-K sets; entered/exited crossings are separately retained. Every full arm ranking/contribution is in the compressed arm artifacts; trace.json retains every movement, inversion set, role/channel aggregate and per-document attribution. Native contributions, IDF/statistics and reference are captured separately. Binary-rational attribution discloses frozen floating summation residuals without changing scores.\n\n## Captured cost accounting\n\n```json\n"
        + json_bytes(costs).decode()
        + "```\n\nNo gold-dependent analysis, witness calculation, decision-rule evaluation or outcome selection has occurred.\n"
    )
    validation = {
        "mechanical_capture": "PASS",
        "checks": [
            "committed Stage A authenticated",
            "zero initial prospective counts",
            "immutable exactly-once journal with complete schedule",
            "one index and seven queries",
            "complete positive candidate capture",
            "A native equality",
            "A/B/C candidate and statistics identity",
            "frozen role/multiplier identity",
            "weighted contribution and score reconstruction",
            "anchor-only B-A attribution",
            "generic-only C-B attribution",
            "combined C-A attribution",
            "semantic contributions unchanged",
            "native collection-order ties",
            "reference unchanged",
            "deterministic pure replay",
        ],
        **summary,
    }
    return {
        "summary.json": json_bytes(summary),
        "costs.json": json_bytes(costs),
        "operations.json": json_bytes(operations),
        "native_capture.json.gz": gzip.compress(
            json_bytes(
                describe(
                    {
                        k: v
                        for k, v in captured.items()
                        if not k.startswith("construct:")
                    }
                )
            ),
            mtime=0,
        ),
        "native_contributions.json.gz": gzip.compress(
            json_bytes(native_surfaces), mtime=0
        ),
        **{
            "arm_" + n.lower() + ".json.gz": gzip.compress(json_bytes(value), mtime=0)
            for n, value in arms.items()
        },
        "reference.json.gz": gzip.compress(json_bytes(describe(reference)), mtime=0),
        "trace.json": json_bytes(mechanical_trace),
        "TRACE.md": review.replace(
            "Stage B mechanical review", "Stage B mechanical trace"
        ).encode(),
        "STAGE_B_REVIEW.md": review.encode(),
        "validation.json": json_bytes(validation),
    }
