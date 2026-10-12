# Copyright (c) 2026
# ruff: noqa: ANN401, T201, E501, COM812
"""Deterministic engineering conclusions from retained timings; no gold join."""

from __future__ import annotations

import json
from typing import Any

from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from experiments.performance.retrieval.benchmark import PACKAGE, publish
from experiments.performance.retrieval.workload import read_json, sha


def ms(stats: Any, field: str = "median_ns") -> str:
    """Render milliseconds while preserving the raw nanosecond samples."""
    return f"{stats[field] / 1e6:.4f}"


def decisions(result: Any) -> list[dict[str, str]]:
    """Answer engineering questions without reading gold or scientific gates."""
    aggregates = result["aggregates"]
    items = []
    for question, surface, target in (
        (
            "Is canonical BM25 fast enough for the online agent loop?",
            "bm25",
            "50 ms median",
        ),
        ("Is pure current PPR fast enough?", "ppr", "250 ms budget"),
        ("Is propagated-flow projection fast enough?", "B_projection", "250 ms budget"),
        ("Is production RRF fast enough?", "rrf", "250 ms budget"),
        (
            "Is COMPLETE warm graph-assisted retrieval fast enough?",
            "warm_graph_query",
            "250 ms median / 1 s p95",
        ),
    ):
        row = aggregates[surface]
        items.append(
            {
                "question": question,
                "answer": "YES" if row["viability"] == "VIABLE" else "NO",
                "evidence": f"Median/p95 {ms(row['summary'])}/{ms(row['summary'], 'p95_ns')} ms; {row['viability']}; target {target}.",
            },
        )
    lookup = result["measurements"]["exact_lookup_hit"]["summary"]
    items.insert(
        1,
        {
            "question": "Is exact resource lookup fast enough?",
            "answer": "YES",
            "evidence": f"Hit median/p95 {ms(lookup)}/{ms(lookup, 'p95_ns')} ms; current tuple scan.",
        },
    )
    ri = result["measurements"]["full_ri_derivation"]["summary"]
    graph = result["measurements"]["graph_computation"]["summary"]
    slow = [
        name
        for name, row in result["measurements"].items()
        if row["category"] == "ONLINE_QUERY" and row["viability"] == "TOO_SLOW"
    ]
    first = (
        slow[0]
        if slow
        else "complete warm retrieval"
        if aggregates["warm_graph_query"]["viability"] != "VIABLE"
        else "retain the canonical filename index as snapshot state instead of rebuilding it per query"
    )
    remaining = [
        (
            "Are prior 15-18 second B timings representative of retrieval computation?",
            "NO",
            "They include native view/lexical authentication and a Python callback around the entire rank wrapper. Journal publication happens after this timer.",
        ),
        (
            "Are prior ~3 second C timings representative of actual RRF?",
            "NO",
            "fuse() calls require_ranking(), reconstructing/validating the view and lexical frame before the tiny RRF primitive.",
        ),
        (
            "Can full RI derivation happen synchronously for every query?",
            "NO",
            f"Median pure full pass {ri['median_ns'] / 1e9:.3f} seconds across three samples.",
        ),
        (
            "Can full RI derivation reasonably happen after every edit?",
            "NO",
            f"Median {ri['median_ns'] / 1e9:.3f} seconds; incremental maintenance is required.",
        ),
        (
            "Can graph reconstruction happen after every edit?",
            "CONDITIONAL",
            f"Pure graph median {graph['median_ns'] / 1e9:.3f} seconds, excluding RI/provenance. Coalesced background rebuilding is feasible; synchronous per-edit rebuilding is unsuitable.",
        ),
        (
            "Is incremental RI/graph maintenance required for production?",
            "YES",
            "One-resource RI exists but no complete invalidation system. Changed sources/declarations, affected referencers, outgoing graph rows and lexical statistics must be maintained.",
        ),
        (
            "Is definition/map materialization a meaningful online bottleneck?",
            "CONDITIONAL",
            f"Cached projection/render medians {ms(aggregates['definition_projection']['summary'])}/{ms(aggregates['map_rendering']['summary'])} ms are small. Current diagnostic wrappers add audit/identity work; this is separate from required query arithmetic.",
        ),
        (
            "Why did Stage D verification take approximately 55 minutes?",
            "CONDITIONAL",
            "Confirmed repeated native replay and reviewed-primary/adversarial reconstruction amplify experiment-only work. The historical run has no retained phase trace; exact attribution of every second is unavailable. Bounded mechanical diagnostics and static call counts are retained; no complete verifier or gold join was rerun.",
        ),
        (
            "What single performance bottleneck should be fixed FIRST?",
            "YES",
            first
            + ". Follow measured online targets, then offline ownership/incremental work, then verifier amplification.",
        ),
    ]
    items.extend({"question": q, "answer": a, "evidence": e} for q, a, e in remaining)
    return [{"number": str(i), **item} for i, item in enumerate(items, 1)]


def render(result: Any, profile: Any, conclusions: Any) -> str:
    """Generate stable human-readable ownership, measurement and diagnosis tables."""
    aggregates = result["aggregates"]
    warm = aggregates["warm_graph_query"]
    lines = [
        "# Retrieval performance characterization",
        "",
        f"**RETRIEVAL_PERFORMANCE_BASELINE = COMPLETE. Complete warm computation: {warm['viability']}**; pooled median {ms(warm['summary'])} ms, p95 {ms(warm['summary'], 'p95_ns')} ms.",
        "Engineering baseline only. GRAPH-3 remains COMPLETE / GRAPH_HARMFUL. No gold join, relevance re-evaluation, scientific Stage B schedule, Astra call, confirmation/reserve access, production change or optimization.",
        "",
        "## Cold, warm and ownership",
        "",
        "| Primary category | Work | Ownership/amortization |",
        "|---|---|---|",
        "| OFFLINE_SNAPSHOT_BUILD | Frame, lexical fields/statistics/index, RI, native fact/definition keys, graph pairs/weights/normalized rows | Once per snapshot, outside requests |",
        "| INCREMENTAL_UPDATE | Existing one-resource RI operation (candidate) | Changed source plus affected dependents; invalidation not implemented |",
        "| ONLINE_QUERY | BM25, exact lookup, seed/personalization, PPR, propagated B, RRF | Every request on retained state |",
        "| CONTEXT_MATERIALIZATION | Definition flow aggregation/order; 8192-byte diagnostic map | After acquisition; separate representation choice |",
        "| EXPERIMENT_ONLY | Native reauthentication, callback profiling, journal serialization/durability, canonicalization, hashing, validation/publication, Markdown, Git | Never a per-query agent cost |",
        "",
        "Cold starts with archive bytes and reconstructs snapshot/index/RI/graph. Warm already retains snapshot, index, References, normalized graph rows and query-independent provenance/definition metadata. The current canonical BM25 API still rebuilds its filename index internally; actual BM25 and complete-query timing includes this work. No cached production replacement was substituted.",
        "Complete warm computation includes canonical BM25 + actual resource_at lookup + lexical top-ten/exact seed union + uniform personalization + production PPR + propagated-flow B + production RRF C. It excludes RI/graph construction, scientific authentication, definition/map representation and artifact publication.",
        "",
        "## Reproduction and measurement",
        "",
        "~~~text",
        "uv run python -X utf8 -m experiments.performance.retrieval.benchmark",
        "uv run python -X utf8 -m experiments.performance.retrieval.profiler",
        "uv run python -X utf8 -m experiments.performance.retrieval.reporting",
        "uv run pytest --no-cov experiments/performance/retrieval/test_benchmark.py -q",
        "~~~",
        "",
        "The benchmark repeats computational algorithms intentionally, without invoking the original scientific execution schedule. The profiler uses isolated managed child processes with a 120-second hard limit; a timed-out path is stopped and not repeated. Do not run Case 0016 Stage D full verify for ordinary benchmark validation.",
        "Wall latency uses perf_counter_ns(), GC enabled, no tracemalloc or profiler inside warm samples, and no concurrent diagnostic process. Cheap online surfaces have 10 warmups/50 samples. Offline reconstruction has three samples and no expensive extra warmup. Full RI totals sum 415 individually timed native calls; equality checks, progress, counters and loop orchestration are outside those times. The representative per-resource candidate has five warmups/30 samples. Memory runs are separate.",
        "p95 is nearest rank, sorted samples at ceil(0.95*n)-1; SD is population SD. Aggregates pool equal-count samples across six queries. All raw repetitions are retained; these are descriptive single-host measurements, not confidence intervals or production service guarantees.",
        "Exact A/B/C order, seeds, iterations, vector numerical convention, graph occurrence membership/weights/transitions and definition/map outputs are checked against the immutable capture. No gold labels are read for benchmark correctness.",
        "",
        "## Environment and workload",
        "",
        "~~~json",
        json.dumps(
            {
                "timestamp": result["timestamp"],
                "environment": result["environment"],
                "workload": result["workload"],
            },
            sort_keys=True,
            indent=2,
        ),
        "~~~",
        "",
        "results.json retains physical implementation/input hashes. Trusted native returns use their original shared pickle memo after immutable manifest/segment authentication, omitting scientific canonical re-encoding. That adapter is engineering input preparation, not a replacement scientific verifier.",
        "",
        "## Warm online queries",
        "",
        "| Query | BM25 median/p95 ms | PPR median/p95 ms | Iterations | ns/iteration | B projection median/p95 ms | RRF median/p95 ms | Complete median/p95 ms | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for i in range(1, 7):
        q = f"Q{i}"
        row = []
        for surface in ("bm25", "ppr", "B_projection", "rrf", "warm_graph_query"):
            stats = result["measurements"][q + "." + surface]["summary"]
            row.append(ms(stats) + "/" + ms(stats, "p95_ns"))
        observed = result["ppr_observations"][q]
        lines.append(
            f"| {q} | {row[0]} | {row[1]} | {observed['iterations']} | {observed['median_ns_per_iteration']:.1f} | {row[2]} | {row[3]} | {row[4]} | {result['measurements'][q + '.warm_graph_query']['viability']} |",
        )
    lines += [
        "",
        "| Aggregate | Median ms | p95 ms | Engineering status |",
        "|---|---:|---:|---|",
    ]
    for name in (
        "bm25",
        "seed_construction",
        "ppr",
        "B_projection",
        "rrf",
        "warm_graph_query",
    ):
        row = aggregates[name]
        lines.append(
            f"| {name} | {ms(row['summary'])} | {ms(row['summary'], 'p95_ns')} | {row['viability']} |",
        )
    lines += [
        "",
        "New engineering targets, independent of scientific gates: BM25 <=50 ms median; complete warm <=250 ms median and <=1 second p95. Exact lookup, seed construction, scoring, flow, accumulation and sort appear in the exhaustive surface table.",
        "",
        "## Cold/offline and incremental work",
        "",
        "| Operation | n | Median seconds | p95 seconds |",
        "|---|---:|---:|---:|",
    ]
    for name in (
        "frame_archive_decode",
        "frame_adaptation",
        "lexical_fields",
        "lexical_index",
        "full_ri_derivation",
        "one_resource_ri",
        "graph_computation",
        "native_graph_build_with_checks",
    ):
        stats = result["measurements"][name]["summary"]
        lines.append(
            f"| {name} | {stats['n']} | {stats['median_ns'] / 1e9:.6f} | {stats['p95_ns'] / 1e9:.6f} |",
        )
    ri = result["measurements"]["full_ri_derivation"]
    stats = ri["per_source_summary"]
    lines += [
        "",
        f"RI per-source pooled p50/p95/max {ms(stats)}/{ms(stats, 'p95_ns')}/{ms(stats, 'maximum_ns')} ms across 3 x 415 samples; {ri['assessments_per_second']:.1f} assessments/s and {ri['references_per_second']:.1f} positive References/s. Representative one-resource path is recorded in its measurement note.",
        "Full RI cannot be paid per query or per edit. Existing per-resource derivation validates the entire module universe with linear resource_at lookups and reparses/resolves declarations/imports. Required production maintenance: changed lexical documents/statistics, changed source/declaration/module interpretation, affected referencers and outgoing graph pairs/rows. An altered outgoing row renormalizes all its probabilities. Cross-snapshot identities/provenance must remain correct. No invalidation implementation was added.",
        "Graph row totals sort/scan the full pair table for every node: O(V * E log E), on 514 nodes and 561 pairs. Endpoint validation adds repeated linear snapshot lookups and native identity derivation. This is offline build cost, not a stationary-kernel bottleneck.",
        "",
        "## Why Stage B reported B 15-18 seconds and C ~3 seconds",
        "",
        "Journal.call starts runtime_ns immediately before invoke() and stops it immediately after return. describe/JSON, pickle, gzip/b85, hashing and fsynced returned-event publication happen afterward. Progress boundary records are outside it. Journal durability contributes to capture wall time, but does not explain B/C runtime_ns.",
        "B invokes observed_ppr(lambda: rank(...)); sys.setprofile wraps the entire rank function, including require_view() native reconstruction and seed_union() lexical authentication. It then computes PPR and full incoming provenance states. The universal callback observes Python events throughout expensive validation. C invokes fuse(), which calls require_ranking() (including require_view()/seed_union()) before _fused_resource_order().",
        "",
        "| Query | Captured B s | Pure B ms | B ratio | Captured C s | Pure RRF ms | C ratio |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for q, row in result["harness_ratios"].items():
        lines.append(
            f"| {q} | {row['captured_B_ns'] / 1e9:.6f} | {row['pure_B_ns'] / 1e6:.4f} | {row['B_ratio']:.1f}x | {row['captured_C_ns'] / 1e9:.6f} | {row['pure_RRF_ns'] / 1e6:.4f} | {row['C_ratio']:.1f}x |",
        )
    lines += [
        "",
        "Pure B here is median kernel + median B projection on retained seeds/rows, excluding A/exact/seed costs just as captured B receives those inputs. A sum of medians is a descriptive comparison, not a recovered historical subphase split. Direct Q1 require_view/require_ranking/unprofiled rank/profiled rank measurements appear below.",
        f"Captured wall {result['captured_costs']['capture_wall_ns'] / 1e9:.3f} s; journal durability {result['captured_costs']['journal_publication_durability_ns'] / 1e9:.3f} s. Original construction/validation/publication costs are retained verbatim in results.json. Historical timing boundaries do not permit an exact finer nanosecond decomposition; later component samples are not retroactive measurements.",
        "",
        "## Context materialization and memory",
        "",
        "Definition timing starts with query-independent native definition identities/metadata retained. It splits actual pair flow by occurrence count, aggregates with math.fsum and applies exact definition/parent-rank tie rules. Ordered identity/owner/flow matches captured native outputs. Map timing invokes the frozen 8192-byte whole-line renderer and matches capture exactly. These are CONTEXT_MATERIALIZATION; diagnostic validation/provenance wrappers are separate.",
        "Memory is measured outside latency loops. Tracemalloc warm peaks exclude retained snapshot/index/RI/graph. All-return decode is a conservative upper bound for RI alone. Retained sys.getsizeof object-graph sizes count shared objects once and are not RSS. Interpreter state, allocator arenas, OS cache and external allocations are excluded.",
        "",
        "~~~json",
        json.dumps(result["memory"], sort_keys=True, indent=2),
        "~~~",
        "",
        "## Bounded Stage D verifier diagnosis",
        "",
        "| Mechanical phase | Status | Median ms or elapsed lower bound | n |",
        "|---|---|---:|---:|",
    ]
    for name, row in profile["phases"].items():
        timing = (
            ms(row["summary"])
            if "summary" in row
            else f">={row.get('phase_elapsed_lower_bound_ns', 0) / 1e6:.1f}"
        )
        lines.append(
            f"| {name} | {row['status']} | {timing} | {len(row.get('samples_ns', []))} |",
        )
    lines += [
        "",
        "source_audit records exact hashes/call/loop sites for analysis, metrics, reporting, authentication, validation, reviewed materialize, Stage B reporting and Journal.load. No metric/gate/effectiveness function was invoked; existing Stage D JSON is opaque published output for mechanical parsing/copying/encoding.",
        "Confirmed static amplification: checkpoints() calls reviewed outputs(); read_inputs() calls reviewed verify()->outputs(). Each outputs() invokes primary authentication three times (construct_gold; validate; nested construct_gold), giving six primary authentications per full Stage D verify. Each authentication runs validate_review plus bundle; bundle performs validation and 22 adversarial checks, several rebuilding witnesses/cells/864 combinations/90 unions. This is a call-count audit, not a new semantic replay.",
        "Stage B verify()->derived()->reconstruct() calls Journal.load(), validates all RI returns, the view, six rankings and definition projections, then reserializes derived artifacts. Journal.load parses/decompresses all native returns and describes/canonical-encodes every complete returned object. Alias tracking is per return, repeatedly traversing shared snapshot/index/universe state across 464 results: O(sum of reachable return graph sizes), much larger than O(unique retained state).",
        "metrics.flow scans 514 states and 561 pairs repeatedly for targets: O(targets*(V+E)); indexing can remove repeated scans. analysis.expected makes five full deep copies for adversarial validation and renders identical large Markdown outputs. Mechanical parsing/copying/encoding/hashing timings distinguish these costs. Complete Markdown construction and semantic constructors were intentionally not rerun.",
        "The historical ~55-minute run has no retained phase trace. Bounded timings confirm costly mechanical paths and static amplification, but cannot attribute every historical second or prove the full-run dominant phase. Native-authentication counters are inclusive and overlap; they are not an additive historical breakdown. A timed-out phase is stopped once and not repeated.",
        "Recommended separate verifier repair: authenticate blobs once per invocation; pass an explicit authenticated-input/result bundle; eliminate repeated primary bundle/adversarial replay while preserving every rejection/equivalence check; memoize immutable graph encodings/identity projections where exact-byte equivalence is proven; preindex state/pair/cell maps; render identical Markdown once. Measure repaired phases before any bounded full equivalence replay. No verifier repair occurred here.",
        "",
        "## Fifteen performance decisions",
        "",
    ]
    for item in conclusions:
        lines += [
            f"{item['number']}. **{item['answer']} — {item['question']}** {item['evidence']}",
            "",
        ]
    lines += [
        "Priority order: core online >1 second; complete warm >250 ms; offline/audit work incorrectly repeated online; missing incremental maintenance; pathological verifier infrastructure. Fast kernels must not be redesigned to compensate for harness overhead. BASELINE only: no production retrieval or verifier optimization.",
        "",
        "## Exhaustive surface summaries",
        "",
        "Raw samples and n/min/median/mean/p95/max/population SD are in results.json.",
        "",
        "| Surface | Primary category | n | Median ms | p95 ms | Status |",
        "|---|---|---:|---:|---:|---|",
    ]
    for name, row in result["measurements"].items():
        stats = row["summary"]
        lines.append(
            f"| {name} | {row['category']} | {stats['n']} | {ms(stats)} | {ms(stats, 'p95_ns')} | {row.get('viability', 'descriptive')} |",
        )
    lines += [
        "",
        "## Durable state and next step",
        "",
        "U1 = COMPLETE / INFORMATION_NEED_AUTHORING_DEFECT; U2 = COMPLETE / EXACT_HINT_ROUTING_SUPPORTED; U3 = COMPLETE / SELECTIVE_MECHANISM_ROUTING_SUPPORTED; R1.7 = COMPLETE / QUERY_TERM_WEIGHTING_HARMFUL; R2 = COMPLETE / BM25F_HARMFUL; GRAPH-3 = COMPLETE / GRAPH_HARMFUL. SEARCH_POLICY_FAILURE = NOT_ASSESSED; production behavior = UNCHANGED; confirmation/reserve = NOT_ACCESSED.",
        "Maintainer reviews the measured retrieval-performance baseline. Then optimize the highest-priority measured bottleneck before authorizing any further retrieval-effectiveness experiment. No Graph-4 or other effectiveness increment is selected.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    """Publish deterministic report/conclusions and physical engineering hashes."""
    result = read_json(PACKAGE / "results.json")
    profile = read_json(PACKAGE / "stage_d_profile.json")
    conclusions = decisions(result)
    publish(
        PACKAGE / "decisions.json",
        {
            "status": "RETRIEVAL_PERFORMANCE_BASELINE = COMPLETE",
            "decisions": conclusions,
        },
    )
    write(
        TextFile(
            resolve_path(PACKAGE / "README.md"),
            render(result, profile, conclusions),
        ),
        overwrite=True,
    )
    supplement = read_json(PACKAGE / "supplement.json")
    extra = [
        "",
        "## Supplemental ownership and retained memory",
        "",
        "These samples were taken after the primary run and remain separately retained in supplement.json.",
        "",
        "| Surface | Category | n | Median ms | p95 ms |",
        "|---|---|---:|---:|---:|",
    ]
    for name, row in supplement["measurements"].items():
        stats = row["summary"]
        extra.append(
            f"| {name} | {row['category']} | {stats['n']} | {ms(stats)} | {ms(stats, 'p95_ns')} |"
        )
    extra += [
        "",
        "~~~json",
        json.dumps(
            supplement["retained_python_object_graph"], sort_keys=True, indent=2
        ),
        "~~~",
        "",
    ]
    # Stable regeneration from retained samples; no measurements are rewritten.
    write(
        TextFile(
            resolve_path(PACKAGE / "README.md"),
            render(result, profile, conclusions) + "\n".join(extra),
        ),
        overwrite=True,
    )
    paths = sorted(
        path
        for path in PACKAGE.rglob("*")
        if path.is_file()
        and "__pycache__" not in str(path)
        and path.name != "integrity.json"
    )
    publish(
        PACKAGE / "integrity.json",
        {
            "schema": "retrieval-performance-integrity-v1",
            "sha256": {
                path.relative_to(PACKAGE).as_posix(): sha(path.read_bytes())
                for path in paths
            },
            "excluded": [".local", "__pycache__", "self hash"],
        },
    )
    print("Performance report and hashes published")


if __name__ == "__main__":
    main()
