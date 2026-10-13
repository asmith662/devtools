# Retrieval performance characterization

**RETRIEVAL_PERFORMANCE_BASELINE = COMPLETE. Complete warm computation: VIABLE**; pooled median 66.7613 ms, p95 87.2052 ms.
Engineering baseline only. GRAPH-3 remains COMPLETE / GRAPH_HARMFUL. No gold join, relevance re-evaluation, scientific Stage B schedule, Astra call, confirmation/reserve access, production change or optimization.

## Cold, warm and ownership

| Primary category | Work | Ownership/amortization |
|---|---|---|
| OFFLINE_SNAPSHOT_BUILD | Frame, lexical fields/statistics/index, RI, native fact/definition keys, graph pairs/weights/normalized rows | Once per snapshot, outside requests |
| INCREMENTAL_UPDATE | Existing one-resource RI operation (candidate) | Changed source plus affected dependents; invalidation not implemented |
| ONLINE_QUERY | BM25, exact lookup, seed/personalization, PPR, propagated B, RRF | Every request on retained state |
| CONTEXT_MATERIALIZATION | Definition flow aggregation/order; 8192-byte diagnostic map | After acquisition; separate representation choice |
| EXPERIMENT_ONLY | Native reauthentication, callback profiling, journal serialization/durability, canonicalization, hashing, validation/publication, Markdown, Git | Never a per-query agent cost |

Cold starts with archive bytes and reconstructs snapshot/index/RI/graph. Warm already retains snapshot, index, References, normalized graph rows and query-independent provenance/definition metadata. The current canonical BM25 API still rebuilds its filename index internally; actual BM25 and complete-query timing includes this work. No cached production replacement was substituted.
Complete warm computation includes canonical BM25 + actual resource_at lookup + lexical top-ten/exact seed union + uniform personalization + production PPR + propagated-flow B + production RRF C. It excludes RI/graph construction, scientific authentication, definition/map representation and artifact publication.

## Reproduction and measurement

~~~text
uv run python -X utf8 -m experiments.performance.retrieval.benchmark
uv run python -X utf8 -m experiments.performance.retrieval.profiler
uv run python -X utf8 -m experiments.performance.retrieval.reporting
uv run pytest --no-cov experiments/performance/retrieval/test_benchmark.py -q
~~~

The benchmark repeats computational algorithms intentionally, without invoking the original scientific execution schedule. The profiler uses isolated managed child processes with a 120-second hard limit; a timed-out path is stopped and not repeated. Do not run Case 0016 Stage D full verify for ordinary benchmark validation.
Wall latency uses perf_counter_ns(), GC enabled, no tracemalloc or profiler inside warm samples, and no concurrent diagnostic process. Cheap online surfaces have 10 warmups/50 samples. Offline reconstruction has three samples and no expensive extra warmup. Full RI totals sum 415 individually timed native calls; equality checks, progress, counters and loop orchestration are outside those times. The representative per-resource candidate has five warmups/30 samples. Memory runs are separate.
p95 is nearest rank, sorted samples at ceil(0.95*n)-1; SD is population SD. Aggregates pool equal-count samples across six queries. All raw repetitions are retained; these are descriptive single-host measurements, not confidence intervals or production service guarantees.
Exact A/B/C order, seeds, iterations, vector numerical convention, graph occurrence membership/weights/transitions and definition/map outputs are checked against the immutable capture. No gold labels are read for benchmark correctness.

## Environment and workload

~~~json
{
  "environment": {
    "architecture": "64bit",
    "gc_enabled": true,
    "logical_cpus": 32,
    "os": "Windows-11-10.0.26200-SP0",
    "processor": "Intel64 Family 6 Model 183 Stepping 1, GenuineIntel",
    "python": "3.14.0 (tags/v3.14.0:ebf955d, Oct  7 2025, 10:15:03) [MSC v.1944 64 bit (AMD64)]",
    "repository_head": "ba1c51037d7d0a255e4e2c3c2476a3a37470d6cf",
    "tracemalloc_during_latency": false
  },
  "timestamp": "2026-10-12T19:39:29.049413+00:00",
  "workload": {
    "case": "0016",
    "dangling_nodes": 305,
    "directed_pairs": 561,
    "execution": "case-0016-stage-b-2",
    "frame": {
      "corpus_id": "1e0df552f370938fcbbbf489a4bf433a25b4a218b1f624b72a21e463bcbdc7b0",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "636f86afb0fef7b8ccdd9adfd1c9f64dea76139b90d3d098f8f2b811bd90dfca"
    },
    "native_references": 3954,
    "nodes": 514,
    "python_resources": 415,
    "resources": 514,
    "use": "INPUT_DATA_AND_SEMANTIC_OUTPUT_REFERENCE_ONLY"
  }
}
~~~

results.json retains physical implementation/input hashes. Trusted native returns use their original shared pickle memo after immutable manifest/segment authentication, omitting scientific canonical re-encoding. That adapter is engineering input preparation, not a replacement scientific verifier.

## Warm online queries

| Query | BM25 median/p95 ms | PPR median/p95 ms | Iterations | ns/iteration | B projection median/p95 ms | RRF median/p95 ms | Complete median/p95 ms | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Q1 | 38.7265/48.2575 | 25.8184/28.5056 | 47 | 549327.7 | 1.5954/2.0481 | 1.2531/1.5250 | 73.9207/96.2293 | VIABLE |
| Q2 | 29.9215/33.9601 | 29.6422/31.7656 | 54 | 548929.6 | 1.5587/1.8124 | 0.5812/0.6811 | 65.3433/87.2052 | VIABLE |
| Q3 | 32.2264/43.1071 | 26.3339/31.0736 | 49 | 537425.5 | 1.6641/1.9450 | 0.6633/0.8391 | 64.8253/78.0270 | VIABLE |
| Q4 | 37.9938/54.9295 | 27.1775/28.7648 | 50 | 543549.0 | 1.5610/2.5075 | 1.1214/1.3171 | 71.7263/93.2499 | VIABLE |
| Q5 | 29.0129/34.3966 | 25.3068/29.3152 | 46 | 550146.7 | 1.5536/1.9871 | 0.4247/0.4478 | 59.7794/76.4561 | VIABLE |
| Q6 | 32.0874/35.4521 | 29.5882/39.8399 | 54 | 547930.6 | 1.3064/2.1403 | 0.7826/0.9493 | 66.1107/80.3229 | VIABLE |

| Aggregate | Median ms | p95 ms | Engineering status |
|---|---:|---:|---|
| bm25 | 32.2803 | 45.3682 | VIABLE |
| seed_construction | 1.2848 | 1.5625 | VIABLE |
| ppr | 27.1726 | 31.0794 | VIABLE |
| B_projection | 1.5900 | 1.9686 | VIABLE |
| rrf | 0.7757 | 1.2897 | VIABLE |
| warm_graph_query | 66.7613 | 87.2052 | VIABLE |

New engineering targets, independent of scientific gates: BM25 <=50 ms median; complete warm <=250 ms median and <=1 second p95. Exact lookup, seed construction, scoring, flow, accumulation and sort appear in the exhaustive surface table.

## Cold/offline and incremental work

| Operation | n | Median seconds | p95 seconds |
|---|---:|---:|---:|
| frame_archive_decode | 3 | 0.008723 | 0.008763 |
| frame_adaptation | 3 | 5.746723 | 7.864328 |
| lexical_fields | 3 | 1.143174 | 1.151708 |
| lexical_index | 3 | 0.597487 | 0.609214 |
| full_ri_derivation | 3 | 288.759644 | 294.221487 |
| one_resource_ri | 30 | 0.170641 | 0.189979 |
| graph_computation | 3 | 1.747082 | 1.766978 |
| native_graph_build_with_checks | 3 | 16.903903 | 16.908456 |

RI per-source pooled p50/p95/max 171.3484/3206.5933/9535.8172 ms across 3 x 415 samples; 175.7 assessments/s and 13.7 positive References/s. Representative one-resource path is recorded in its measurement note.
Full RI cannot be paid per query or per edit. Existing per-resource derivation validates the entire module universe with linear resource_at lookups and reparses/resolves declarations/imports. Required production maintenance: changed lexical documents/statistics, changed source/declaration/module interpretation, affected referencers and outgoing graph pairs/rows. An altered outgoing row renormalizes all its probabilities. Cross-snapshot identities/provenance must remain correct. No invalidation implementation was added.
Graph row totals sort/scan the full pair table for every node: O(V * E log E), on 514 nodes and 561 pairs. Endpoint validation adds repeated linear snapshot lookups and native identity derivation. This is offline build cost, not a stationary-kernel bottleneck.

## Why Stage B reported B 15-18 seconds and C ~3 seconds

Journal.call starts runtime_ns immediately before invoke() and stops it immediately after return. describe/JSON, pickle, gzip/b85, hashing and fsynced returned-event publication happen afterward. Progress boundary records are outside it. Journal durability contributes to capture wall time, but does not explain B/C runtime_ns.
B invokes observed_ppr(lambda: rank(...)); sys.setprofile wraps the entire rank function, including require_view() native reconstruction and seed_union() lexical authentication. It then computes PPR and full incoming provenance states. The universal callback observes Python events throughout expensive validation. C invokes fuse(), which calls require_ranking() (including require_view()/seed_union()) before _fused_resource_order().

| Query | Captured B s | Pure B ms | B ratio | Captured C s | Pure RRF ms | C ratio |
|---|---:|---:|---:|---:|---:|---:|
| Q1 | 15.532187 | 27.4138 | 566.6x | 3.149360 | 1.2531 | 2513.2x |
| Q2 | 15.211994 | 31.2009 | 487.5x | 3.228600 | 0.5812 | 5555.1x |
| Q3 | 17.163724 | 27.9979 | 613.0x | 3.379570 | 0.6633 | 5095.5x |
| Q4 | 17.878819 | 28.7384 | 622.1x | 3.629899 | 1.1214 | 3236.9x |
| Q5 | 15.574588 | 26.8604 | 579.8x | 3.057803 | 0.4247 | 7199.9x |
| Q6 | 15.436819 | 30.8946 | 499.7x | 3.170875 | 0.7826 | 4051.5x |

Pure B here is median kernel + median B projection on retained seeds/rows, excluding A/exact/seed costs just as captured B receives those inputs. A sum of medians is a descriptive comparison, not a recovered historical subphase split. Direct Q1 require_view/require_ranking/unprofiled rank/profiled rank measurements appear below.
Captured wall 335.817 s; journal durability 115.564 s. Original construction/validation/publication costs are retained verbatim in results.json. Historical timing boundaries do not permit an exact finer nanosecond decomposition; later component samples are not retroactive measurements.

## Context materialization and memory

Definition timing starts with query-independent native definition identities/metadata retained. It splits actual pair flow by occurrence count, aggregates with math.fsum and applies exact definition/parent-rank tie rules. Ordered identity/owner/flow matches captured native outputs. Map timing invokes the frozen 8192-byte whole-line renderer and matches capture exactly. These are CONTEXT_MATERIALIZATION; diagnostic validation/provenance wrappers are separate.
Memory is measured outside latency loops. Tracemalloc warm peaks exclude retained snapshot/index/RI/graph. All-return decode is a conservative upper bound for RI alone. Retained sys.getsizeof object-graph sizes count shared objects once and are not RSS. Interpreter state, allocator arenas, OS cache and external allocations are excluded.

~~~json
{
  "Q1.ppr": {
    "peak_bytes": 34536,
    "retained_bytes": 19912
  },
  "Q1.warm_graph_query": {
    "peak_bytes": 970466,
    "retained_bytes": 929546
  },
  "Q2.ppr": {
    "peak_bytes": 34408,
    "retained_bytes": 19784
  },
  "Q2.warm_graph_query": {
    "peak_bytes": 705545,
    "retained_bytes": 685873
  },
  "Q3.ppr": {
    "peak_bytes": 34408,
    "retained_bytes": 19784
  },
  "Q3.warm_graph_query": {
    "peak_bytes": 778528,
    "retained_bytes": 753248
  },
  "Q4.ppr": {
    "peak_bytes": 34408,
    "retained_bytes": 19784
  },
  "Q4.warm_graph_query": {
    "peak_bytes": 925962,
    "retained_bytes": 888570
  },
  "Q5.ppr": {
    "peak_bytes": 34408,
    "retained_bytes": 19784
  },
  "Q5.warm_graph_query": {
    "peak_bytes": 649928,
    "retained_bytes": 634008
  },
  "Q6.ppr": {
    "peak_bytes": 34408,
    "retained_bytes": 19784
  },
  "Q6.warm_graph_query": {
    "peak_bytes": 742972,
    "retained_bytes": 718628
  },
  "graph_computation": {
    "peak_bytes": 888872,
    "retained_bytes": 289984
  },
  "lexical_fields": {
    "peak_bytes": 62656301,
    "retained_bytes": 62595837
  },
  "lexical_index": {
    "peak_bytes": 17023632,
    "retained_bytes": 15460912
  },
  "limitations": "tracemalloc incremental Python allocations; existing frame/graph/index excluded from warm peaks. Native-return decode includes all retained returns, a conservative upper bound for RI alone. No process RSS, allocator arenas, OS cache or external allocations measured. Memory runs are excluded from latency samples.",
  "native_return_decode": {
    "peak_bytes": 552442252,
    "retained_bytes": 118315140
  }
}
~~~

## Bounded Stage D verifier diagnosis

| Mechanical phase | Status | Median ms or elapsed lower bound | n |
|---|---|---:|---:|
| artifact_hashing | COMPLETE | 249.2774 | 3 |
| native_return_authentication | TIME_LIMIT_STOPPED_NOT_REPEATED | >=100716.3 | 0 |
| stage_d_deepcopy | COMPLETE | 13.8149 | 3 |
| stage_d_json_encoding | COMPLETE | 15.9787 | 3 |
| stage_d_json_parse | COMPLETE | 10.5401 | 3 |
| stage_d_markdown_json_sections | COMPLETE | 16.3642 | 3 |

source_audit records exact hashes/call/loop sites for analysis, metrics, reporting, authentication, validation, reviewed materialize, Stage B reporting and Journal.load. No metric/gate/effectiveness function was invoked; existing Stage D JSON is opaque published output for mechanical parsing/copying/encoding.
Confirmed static amplification: checkpoints() calls reviewed outputs(); read_inputs() calls reviewed verify()->outputs(). Each outputs() invokes primary authentication three times (construct_gold; validate; nested construct_gold), giving six primary authentications per full Stage D verify. Each authentication runs validate_review plus bundle; bundle performs validation and 22 adversarial checks, several rebuilding witnesses/cells/864 combinations/90 unions. This is a call-count audit, not a new semantic replay.
Stage B verify()->derived()->reconstruct() calls Journal.load(), validates all RI returns, the view, six rankings and definition projections, then reserializes derived artifacts. Journal.load parses/decompresses all native returns and describes/canonical-encodes every complete returned object. Alias tracking is per return, repeatedly traversing shared snapshot/index/universe state across 464 results: O(sum of reachable return graph sizes), much larger than O(unique retained state).
metrics.flow scans 514 states and 561 pairs repeatedly for targets: O(targets*(V+E)); indexing can remove repeated scans. analysis.expected makes five full deep copies for adversarial validation and renders identical large Markdown outputs. Mechanical parsing/copying/encoding/hashing timings distinguish these costs. Complete Markdown construction and semantic constructors were intentionally not rerun.
The historical ~55-minute run has no retained phase trace. Bounded timings confirm costly mechanical paths and static amplification, but cannot attribute every historical second or prove the full-run dominant phase. Native-authentication counters are inclusive and overlap; they are not an additive historical breakdown. A timed-out phase is stopped once and not repeated.
Recommended separate verifier repair: authenticate blobs once per invocation; pass an explicit authenticated-input/result bundle; eliminate repeated primary bundle/adversarial replay while preserving every rejection/equivalence check; memoize immutable graph encodings/identity projections where exact-byte equivalence is proven; preindex state/pair/cell maps; render identical Markdown once. Measure repaired phases before any bounded full equivalence replay. No verifier repair occurred here.

## Fifteen performance decisions

1. **YES — Is canonical BM25 fast enough for the online agent loop?** Median/p95 32.2803/45.3682 ms; VIABLE; target 50 ms median.

2. **YES — Is exact resource lookup fast enough?** Hit median/p95 0.0604/0.0711 ms; current tuple scan.

3. **YES — Is pure current PPR fast enough?** Median/p95 27.1726/31.0794 ms; VIABLE; target 250 ms budget.

4. **YES — Is propagated-flow projection fast enough?** Median/p95 1.5900/1.9686 ms; VIABLE; target 250 ms budget.

5. **YES — Is production RRF fast enough?** Median/p95 0.7757/1.2897 ms; VIABLE; target 250 ms budget.

6. **YES — Is COMPLETE warm graph-assisted retrieval fast enough?** Median/p95 66.7613/87.2052 ms; VIABLE; target 250 ms median / 1 s p95.

7. **NO — Are prior 15-18 second B timings representative of retrieval computation?** They include native view/lexical authentication and a Python callback around the entire rank wrapper. Journal publication happens after this timer.

8. **NO — Are prior ~3 second C timings representative of actual RRF?** fuse() calls require_ranking(), reconstructing/validating the view and lexical frame before the tiny RRF primitive.

9. **NO — Can full RI derivation happen synchronously for every query?** Median pure full pass 288.760 seconds across three samples.

10. **NO — Can full RI derivation reasonably happen after every edit?** Median 288.760 seconds; incremental maintenance is required.

11. **CONDITIONAL — Can graph reconstruction happen after every edit?** Pure graph median 1.747 seconds, excluding RI/provenance. Coalesced background rebuilding is feasible; synchronous per-edit rebuilding is unsuitable.

12. **YES — Is incremental RI/graph maintenance required for production?** One-resource RI exists but no complete invalidation system. Changed sources/declarations, affected referencers, outgoing graph rows and lexical statistics must be maintained.

13. **CONDITIONAL — Is definition/map materialization a meaningful online bottleneck?** Cached projection/render medians 0.5668/0.5592 ms are small. Current diagnostic wrappers add audit/identity work; this is separate from required query arithmetic.

14. **CONDITIONAL — Why did Stage D verification take approximately 55 minutes?** Confirmed repeated native replay and reviewed-primary/adversarial reconstruction amplify experiment-only work. The historical run has no retained phase trace; exact attribution of every second is unavailable. Bounded mechanical diagnostics and static call counts are retained; no complete verifier or gold join was rerun.

15. **YES — What single performance bottleneck should be fixed FIRST?** retain the canonical filename index as snapshot state instead of rebuilding it per query. Follow measured online targets, then offline ownership/incremental work, then verifier amplification.

Priority order: core online >1 second; complete warm >250 ms; offline/audit work incorrectly repeated online; missing incremental maintenance; pathological verifier infrastructure. Fast kernels must not be redesigned to compensate for harness overhead. BASELINE only: no production retrieval or verifier optimization.

## Exhaustive surface summaries

Raw samples and n/min/median/mean/p95/max/population SD are in results.json.

| Surface | Primary category | n | Median ms | p95 ms | Status |
|---|---|---:|---:|---:|---|
| B_wrapper_with_capture_profiler | EXPERIMENT_ONLY | 3 | 77306.8328 | 77632.6398 | descriptive |
| B_wrapper_without_profiler | EXPERIMENT_ONLY | 3 | 16930.8032 | 16947.7691 | descriptive |
| Q1.B_projection | ONLINE_QUERY | 50 | 1.5954 | 2.0481 | VIABLE |
| Q1.B_sort | ONLINE_QUERY | 50 | 0.2546 | 0.2687 | VIABLE |
| Q1.bm25 | ONLINE_QUERY | 50 | 38.7265 | 48.2575 | VIABLE |
| Q1.content_scoring_and_ranking | ONLINE_QUERY | 50 | 14.8328 | 24.9653 | VIABLE |
| Q1.definition_projection | CONTEXT_MATERIALIZATION | 50 | 0.7571 | 0.8156 | descriptive |
| Q1.filename_scoring | ONLINE_QUERY | 50 | 0.1840 | 0.1975 | VIABLE |
| Q1.final_lexical_ranking | ONLINE_QUERY | 50 | 2.9729 | 3.4489 | VIABLE |
| Q1.incoming_accumulation | ONLINE_QUERY | 50 | 0.8287 | 0.8470 | VIABLE |
| Q1.map_rendering | CONTEXT_MATERIALIZATION | 50 | 0.7046 | 0.8253 | descriptive |
| Q1.pair_flow | ONLINE_QUERY | 50 | 0.4451 | 0.4612 | VIABLE |
| Q1.ppr | ONLINE_QUERY | 50 | 25.8184 | 28.5056 | VIABLE |
| Q1.query_analysis | ONLINE_QUERY | 50 | 0.0411 | 0.0423 | VIABLE |
| Q1.rrf | ONLINE_QUERY | 50 | 1.2531 | 1.5250 | VIABLE |
| Q1.seed_construction | ONLINE_QUERY | 50 | 1.3450 | 1.5180 | VIABLE |
| Q1.warm_graph_query | ONLINE_QUERY | 50 | 73.9207 | 96.2293 | VIABLE |
| Q2.B_projection | ONLINE_QUERY | 50 | 1.5587 | 1.8124 | VIABLE |
| Q2.B_sort | ONLINE_QUERY | 50 | 0.1913 | 0.2273 | VIABLE |
| Q2.bm25 | ONLINE_QUERY | 50 | 29.9215 | 33.9601 | VIABLE |
| Q2.content_scoring_and_ranking | ONLINE_QUERY | 50 | 7.2176 | 8.0945 | VIABLE |
| Q2.definition_projection | CONTEXT_MATERIALIZATION | 50 | 0.4497 | 0.4832 | descriptive |
| Q2.filename_scoring | ONLINE_QUERY | 50 | 0.1401 | 0.1534 | VIABLE |
| Q2.final_lexical_ranking | ONLINE_QUERY | 50 | 1.8677 | 2.3085 | VIABLE |
| Q2.incoming_accumulation | ONLINE_QUERY | 50 | 0.8402 | 1.1308 | VIABLE |
| Q2.map_rendering | CONTEXT_MATERIALIZATION | 50 | 0.5071 | 0.5988 | descriptive |
| Q2.pair_flow | ONLINE_QUERY | 50 | 0.4578 | 0.4707 | VIABLE |
| Q2.ppr | ONLINE_QUERY | 50 | 29.6422 | 31.7656 | VIABLE |
| Q2.query_analysis | ONLINE_QUERY | 50 | 0.0144 | 0.0150 | VIABLE |
| Q2.rrf | ONLINE_QUERY | 50 | 0.5812 | 0.6811 | VIABLE |
| Q2.seed_construction | ONLINE_QUERY | 50 | 1.2612 | 1.4614 | VIABLE |
| Q2.warm_graph_query | ONLINE_QUERY | 50 | 65.3433 | 87.2052 | VIABLE |
| Q3.B_projection | ONLINE_QUERY | 50 | 1.6641 | 1.9450 | VIABLE |
| Q3.B_sort | ONLINE_QUERY | 50 | 0.2813 | 0.3170 | VIABLE |
| Q3.bm25 | ONLINE_QUERY | 50 | 32.2264 | 43.1071 | VIABLE |
| Q3.content_scoring_and_ranking | ONLINE_QUERY | 50 | 8.9553 | 11.8194 | VIABLE |
| Q3.definition_projection | CONTEXT_MATERIALIZATION | 50 | 1.0691 | 1.1940 | descriptive |
| Q3.filename_scoring | ONLINE_QUERY | 50 | 0.1115 | 0.1130 | VIABLE |
| Q3.final_lexical_ranking | ONLINE_QUERY | 50 | 2.1217 | 2.5365 | VIABLE |
| Q3.incoming_accumulation | ONLINE_QUERY | 50 | 0.8319 | 0.9746 | VIABLE |
| Q3.map_rendering | CONTEXT_MATERIALIZATION | 50 | 0.7429 | 0.8133 | descriptive |
| Q3.pair_flow | ONLINE_QUERY | 50 | 0.4494 | 0.4616 | VIABLE |
| Q3.ppr | ONLINE_QUERY | 50 | 26.3339 | 31.0736 | VIABLE |
| Q3.query_analysis | ONLINE_QUERY | 50 | 0.0340 | 0.0359 | VIABLE |
| Q3.rrf | ONLINE_QUERY | 50 | 0.6633 | 0.8391 | VIABLE |
| Q3.seed_construction | ONLINE_QUERY | 50 | 1.2606 | 1.4235 | VIABLE |
| Q3.warm_graph_query | ONLINE_QUERY | 50 | 64.8253 | 78.0270 | VIABLE |
| Q4.B_projection | ONLINE_QUERY | 50 | 1.5610 | 2.5075 | VIABLE |
| Q4.B_sort | ONLINE_QUERY | 50 | 0.1904 | 0.2203 | VIABLE |
| Q4.bm25 | ONLINE_QUERY | 50 | 37.9938 | 54.9295 | VIABLE |
| Q4.content_scoring_and_ranking | ONLINE_QUERY | 50 | 14.2799 | 18.5451 | VIABLE |
| Q4.definition_projection | CONTEXT_MATERIALIZATION | 50 | 0.4806 | 0.5076 | descriptive |
| Q4.filename_scoring | ONLINE_QUERY | 50 | 0.1567 | 0.1720 | VIABLE |
| Q4.final_lexical_ranking | ONLINE_QUERY | 50 | 2.7153 | 3.1200 | VIABLE |
| Q4.incoming_accumulation | ONLINE_QUERY | 50 | 0.6801 | 0.7211 | VIABLE |
| Q4.map_rendering | CONTEXT_MATERIALIZATION | 50 | 0.5372 | 0.6652 | descriptive |
| Q4.pair_flow | ONLINE_QUERY | 50 | 0.4455 | 0.4570 | VIABLE |
| Q4.ppr | ONLINE_QUERY | 50 | 27.1775 | 28.7648 | VIABLE |
| Q4.query_analysis | ONLINE_QUERY | 50 | 0.0537 | 0.0563 | VIABLE |
| Q4.rrf | ONLINE_QUERY | 50 | 1.1214 | 1.3171 | VIABLE |
| Q4.seed_construction | ONLINE_QUERY | 50 | 1.2993 | 2.3356 | VIABLE |
| Q4.warm_graph_query | ONLINE_QUERY | 50 | 71.7263 | 93.2499 | VIABLE |
| Q5.B_projection | ONLINE_QUERY | 50 | 1.5536 | 1.9871 | VIABLE |
| Q5.B_sort | ONLINE_QUERY | 50 | 0.2404 | 0.2527 | VIABLE |
| Q5.bm25 | ONLINE_QUERY | 50 | 29.0129 | 34.3966 | VIABLE |
| Q5.content_scoring_and_ranking | ONLINE_QUERY | 50 | 6.2327 | 7.7926 | VIABLE |
| Q5.definition_projection | CONTEXT_MATERIALIZATION | 50 | 0.4318 | 0.6206 | descriptive |
| Q5.filename_scoring | ONLINE_QUERY | 50 | 0.1303 | 0.1439 | VIABLE |
| Q5.final_lexical_ranking | ONLINE_QUERY | 50 | 1.3074 | 1.4499 | VIABLE |
| Q5.incoming_accumulation | ONLINE_QUERY | 50 | 0.8405 | 1.1334 | VIABLE |
| Q5.map_rendering | CONTEXT_MATERIALIZATION | 50 | 0.3961 | 0.4417 | descriptive |
| Q5.pair_flow | ONLINE_QUERY | 50 | 0.3553 | 0.3832 | VIABLE |
| Q5.ppr | ONLINE_QUERY | 50 | 25.3068 | 29.3152 | VIABLE |
| Q5.query_analysis | ONLINE_QUERY | 50 | 0.0375 | 0.0486 | VIABLE |
| Q5.rrf | ONLINE_QUERY | 50 | 0.4247 | 0.4478 | VIABLE |
| Q5.seed_construction | ONLINE_QUERY | 50 | 1.2374 | 1.3785 | VIABLE |
| Q5.warm_graph_query | ONLINE_QUERY | 50 | 59.7794 | 76.4561 | VIABLE |
| Q6.B_projection | ONLINE_QUERY | 50 | 1.3064 | 2.1403 | VIABLE |
| Q6.B_sort | ONLINE_QUERY | 50 | 0.1958 | 0.2169 | VIABLE |
| Q6.bm25 | ONLINE_QUERY | 50 | 32.0874 | 35.4521 | VIABLE |
| Q6.content_scoring_and_ranking | ONLINE_QUERY | 50 | 7.8871 | 9.0965 | VIABLE |
| Q6.definition_projection | CONTEXT_MATERIALIZATION | 50 | 0.5695 | 0.6106 | descriptive |
| Q6.filename_scoring | ONLINE_QUERY | 50 | 0.1396 | 0.1651 | VIABLE |
| Q6.final_lexical_ranking | ONLINE_QUERY | 50 | 1.8527 | 2.1889 | VIABLE |
| Q6.incoming_accumulation | ONLINE_QUERY | 50 | 0.8314 | 0.9483 | VIABLE |
| Q6.map_rendering | CONTEXT_MATERIALIZATION | 50 | 0.7314 | 0.8906 | descriptive |
| Q6.pair_flow | ONLINE_QUERY | 50 | 0.4546 | 0.5041 | VIABLE |
| Q6.ppr | ONLINE_QUERY | 50 | 29.5882 | 39.8399 | VIABLE |
| Q6.query_analysis | ONLINE_QUERY | 50 | 0.0305 | 0.0318 | VIABLE |
| Q6.rrf | ONLINE_QUERY | 50 | 0.7826 | 0.9493 | VIABLE |
| Q6.seed_construction | ONLINE_QUERY | 50 | 1.4219 | 1.5945 | VIABLE |
| Q6.warm_graph_query | ONLINE_QUERY | 50 | 66.1107 | 80.3229 | VIABLE |
| canonical_filename_index_rebuild | OFFLINE_SNAPSHOT_BUILD | 50 | 19.6043 | 22.7616 | descriptive |
| exact_lookup_hit | ONLINE_QUERY | 50 | 0.0604 | 0.0711 | VIABLE |
| exact_lookup_miss | ONLINE_QUERY | 50 | 0.1101 | 0.1330 | VIABLE |
| frame_adaptation | OFFLINE_SNAPSHOT_BUILD | 3 | 5746.7232 | 7864.3279 | descriptive |
| frame_archive_decode | OFFLINE_SNAPSHOT_BUILD | 3 | 8.7227 | 8.7626 | descriptive |
| full_ri_derivation | OFFLINE_SNAPSHOT_BUILD | 3 | 288759.6439 | 294221.4873 | descriptive |
| graph_computation | OFFLINE_SNAPSHOT_BUILD | 3 | 1747.0819 | 1766.9777 | descriptive |
| lexical_fields | OFFLINE_SNAPSHOT_BUILD | 3 | 1143.1741 | 1151.7084 | descriptive |
| lexical_index | OFFLINE_SNAPSHOT_BUILD | 3 | 597.4874 | 609.2142 | descriptive |
| native_graph_build_with_checks | OFFLINE_SNAPSHOT_BUILD | 3 | 16903.9031 | 16908.4561 | descriptive |
| one_resource_ri | INCREMENTAL_UPDATE | 30 | 170.6413 | 189.9795 | descriptive |
| require_ranking | EXPERIMENT_ONLY | 3 | 16840.3871 | 17003.1861 | descriptive |
| require_view | EXPERIMENT_ONLY | 3 | 18296.2900 | 18451.8687 | descriptive |

## Durable state and next step

U1 = COMPLETE / INFORMATION_NEED_AUTHORING_DEFECT; U2 = COMPLETE / EXACT_HINT_ROUTING_SUPPORTED; U3 = COMPLETE / SELECTIVE_MECHANISM_ROUTING_SUPPORTED; R1.7 = COMPLETE / QUERY_TERM_WEIGHTING_HARMFUL; R2 = COMPLETE / BM25F_HARMFUL; GRAPH-3 = COMPLETE / GRAPH_HARMFUL. SEARCH_POLICY_FAILURE = NOT_ASSESSED; production behavior = UNCHANGED; confirmation/reserve = NOT_ACCESSED.
Maintainer reviews the measured retrieval-performance baseline. Then optimize the highest-priority measured bottleneck before authorizing any further retrieval-effectiveness experiment. No Graph-4 or other effectiveness increment is selected.

## Supplemental ownership and retained memory

These samples were taken after the primary run and remain separately retained in supplement.json.

| Surface | Category | n | Median ms | p95 ms |
|---|---|---:|---:|---:|
| Q1.frozen_exact_lookup_hit | ONLINE_QUERY | 50 | 0.0313 | 0.0325 |
| Q6.frozen_exact_lookup_hit | ONLINE_QUERY | 50 | 0.0155 | 0.0161 |
| diagnostic_definition_wrapper_Q1 | CONTEXT_MATERIALIZATION | 3 | 20777.6803 | 20808.7648 |
| module_interpretation_universe | OFFLINE_SNAPSHOT_BUILD | 3 | 43.5865 | 43.6095 |
| native_lexical_authentication_Q1 | EXPERIMENT_ONLY | 3 | 38.1975 | 41.5744 |
| native_reference_key_preparation | OFFLINE_SNAPSHOT_BUILD | 3 | 13693.7869 | 14471.4324 |

~~~json
{
  "lexical_index_statistics": {
    "bytes": 78121782,
    "distinct_objects": 1567434
  },
  "limitation": "Shared objects counted once per surface; overlapping surfaces cannot be summed. sys.getsizeof container/dataclass traversal excludes interpreter/global state and unvisited non-dataclass native internals; not RSS.",
  "native_reference_analyses": {
    "bytes": 28948990,
    "distinct_objects": 402589
  },
  "native_resource_graph": {
    "bytes": 16565797,
    "distinct_objects": 177751
  },
  "normalized_graph_rows": {
    "bytes": 96472,
    "distinct_objects": 1839
  },
  "positive_native_references": {
    "bytes": 15802752,
    "distinct_objects": 174810
  }
}
~~~

## Run provenance and validation

The primary latency run had no concurrent diagnostic process. An initial supplemental offline run overlapped the bounded profiler and was stopped; its progress is retained in supplement_interruption.json. The final supplement was rerun after the profiler exited. The early native-authentication diagnostic interval therefore had concurrent offline key preparation; its wall timing is descriptive, and no historical additive phase split is claimed. The diagnostic was stopped once at the hard 120-second worker limit and not repeated. See run_notes.json for the complete scope and byte-authentication record.

Focused tests: 8 passed. Protected development validation: 1,588 passed, two live tests skipped, 100% configured production branch coverage. Scoped Ruff, formatting, strict mypy, diff checks and performance-artifact validation passed. Full Stage D deterministic verification was not run. The committed Stage D analysis bytes were authenticated before using them as opaque profiling data.

## Bounded verifier repair: acceptance failed

The invocation-local [repair candidate](../../codex_dogfood/verification/README.md)
is **INCOMPLETE / HARD_WALL_EXCEEDED**. It is not a completed performance repair.
No repair checkpoint was committed or pushed. Scientific Case 0016 sources,
gold, gates, artifacts and `GRAPH_HARMFUL` remain unchanged.

One separate-process optimized full verification reached its 180-second hard wall
and was terminated without repetition. Parent wall including termination was
180.264 seconds. The last saved progress at 176.886 seconds showed 438/465
native/canonical envelope comparisons started, 4,118,429 checked node bindings and
20,339 shared-block authentications. The last logged operation was
`query:Q3:exact`. Full native authentication and Stage D construction did not finish.

Primary authentication, its primary bundle and its 22-check adversarial bundle
each ran once, replacing approximately six nested primary authentications in the
historical top-level call structure. Primary authentication took 828.724 ms;
reviewed-gold authentication took 29.467 ms. Checkpoint authentication took
11.855 seconds and exact capture-byte authentication took 1.602 seconds. No
new invocation can inherit trusted state from a previous invocation.

The adapter uses an explicit read-only authenticated input bundle, private sealed
function bindings, identity/resource/state/pair indices, exact row totals from one
canonical pair ordering, UTF-8 source indices and invocation-local native graph
blocks. It leaves all sealed implementations untouched. It keeps journal envelope
checks and requires exact capture seals before native deserialization/comparison.

Isolated Stage B algebra/artifact reconstruction passed exact derived-byte
comparison in 60.561 seconds, excluding journal authentication. Focused Stage D
construction reproduced all seven artifacts exactly, including all 36 REQUIRED
cells, 22 witnesses and gates. Its rounded diagnostic metrics/Markdown times were
28/8 ms; those observations overlapped protected tests and are not full verifier
timings. Validation/encoding timings for the full verifier are NOT_ASSESSED because
construction was not reached.

The remaining blocker is native/canonical correspondence over repeatedly captured
reachable graphs and archive decoding. A bounded profile of an earlier candidate
recorded 13.85 million calls in 21.301 seconds for Q1 A, including 257,331 per-node
JSON decodes (5.846 inclusive seconds). Smaller lexical-state blocks reduced a
subsequent Q1 A correspondence probe from 27.791 to 4.554 seconds, but the complete
input-authentication path still exceeded the required wall. This does not implicate
retrieval kernels or reopen the Graph-3 verdict. A complete alias-aware unique-state
authentication strategy remains necessary before this candidate can be accepted.

The previous native-authentication diagnostic remains >100.7 seconds observed with
a 120-second stop; the historical full verifier remains approximately 55+ minutes
without exact phase attribution. No completed full-runtime speedup is claimed.
All prior benchmark samples and implementation bindings are unchanged. The original
engineering manifest is retained in `verifier_repair/baseline_integrity.json`; the
current engineering manifest only refreshes this README hash. Raw attempts,
progress, profiles, sealed-file audit and summary are in
[`verifier_repair/`](verifier_repair/).

Validation: final repair tests 13 passed; existing Stage D/gold/gate/performance and
early repair selection 55 passed; protected development 1,588 passed, 2 skipped,
100% production branch coverage. Scoped Ruff/format, strict mypy and diff checks
pass. The hard-wall failure blocks a completed repair checkpoint. Filename-index
optimization and incremental RI remain separate pending work. No next retrieval
experiment was designed or executed.
## Verifier continuation — qualification remains incomplete

The previous incomplete candidate was preserved and authenticated: all 33 recorded
candidate hashes and 26 sealed scientific hashes matched at entry. No scientific
source, gold, gate, treatment or Stage D artifact changed. No commit or push occurred.
The previous 180-second failure and all baseline performance samples remain intact.

The continuation removes per-binding canonical JSON decoding through exact-content
fragment caching, one-array RI/new-tail parsing, and immutable closure byte programs.
The original journal loader retains the claim, ordering, chain, native archive,
shared pickle memo and completion checks. Optional existing NumPy operations
accelerate exact base85 decoding and dense ordinal binding; no dependency was added.
Cache trust remains invocation-local and follows physical capture authentication.

The final bounded representative run took 48.695 seconds, including its initialization
and final cyclic collection. Q1 A correspondence is **1.144 seconds**, B **1.584
seconds**, and C **39.006 ms**. A uses **22 JSON decodes**, versus 257,331 in the
retained earlier profile; the separate entry diagnostic found 26,931 decodes across
25,128 exact payloads in the starting candidate. These measurements describe
different candidate revisions and are retained separately.

A fails the required <=500 ms qualification. The complete native projection has
not qualified <=60 seconds, so **no new full verifier was launched**. Repair status
is **INCOMPLETE / MICROBENCHMARK_GATE_FAILED**. The 90-second proving run remains
unused. This is not a completed verifier checkpoint and has no repair commit.

The archive inventory covers 465 envelopes and 930 native/canonical bindings:
927 distinct encoded blocks, one repeated block, three duplicate decompressions.
Thus repeated identical archives have limited yield; large shared canonical
closures and their ordinal layouts dominate. The representative counters are
626,781 unique nodes, 641,306 recursive visits, 128 closure hits, and 70,604 total
JSON decodes. Current remaining work is exact shared-block relocation/rendering
and unique-state validation, before an eligible full proving run.

Focused validation passes 85 tests, including all seven retained Stage D bytes,
the 3,084 gold cells, 36 REQUIRED cells, 22 witnesses and unchanged gates/outcome.
Protected development validation passes 1,588 tests with two skips and 100%
production branch coverage. Ruff, formatting and strict typing pass. Focused
equivalence is not complete authentication of all 465 envelopes.

Raw runs, the decoder frequency table, archive inventory, projection limitations
and machine-readable status are retained under
[verifier_repair/continuation](verifier_repair/continuation/results.json).
Production Retrieval remains unchanged; GRAPH-3 remains COMPLETE / GRAPH_HARMFUL;
the performance baseline remains COMPLETE. Incremental RI and filename-index work
remain separate and pending; confirmation/reserve were not accessed.

## Layered verification repair (completed)

This checkpoint separates proof execution from authentication of a completed proof.
Normal verification is now the standard downstream integrity path; explicit deep
forensic replay remains available. No historical scientific artifact or retrieval
behavior changes. The preceding failed candidate and all baseline samples remain
unchanged as historical engineering evidence.

The [verification contract](../../codex_dogfood/verification/README.md) documents
the acyclic trust chain and future content-addressed completion proof. Case 0016
uses a read-only audited compatibility rule: its accepted integrity seal binds
1,888 files, 40 capture implementations, the successful validation/publication and
the deep-proof producer control flow. The execution marker binds another 172
scientific implementations through Stage A. Completion alone is insufficient;
the accepted outer publication occurs only after native/canonical proof succeeds.
The rule accepts this exact committed seal, not arbitrary legacy PASS summaries.

| Surface | Ownership | Measured result |
| --- | --- | --- |
| Warm online retrieval (unchanged baseline) | ONLINE_QUERY | 66.76 ms median; 87.21 ms p95; VIABLE |
| Capture-time deep validation | EXPERIMENT_ONLY | Expensive, sealed once; not online cost |
| Normal completed-experiment verification | EXPERIMENT_ONLY | 22.446 s child; 23.122 s managed wall; PASS <=30 s |
| Explicit deep forensic replay | EXPERIMENT_ONLY | Full Case 0016 runtime not remeasured here |

The one clean child ran under a 60-second wall and reproduced all seven committed
Stage D artifacts exactly, including 3,084 gold cells, 36 REQUIRED results, 22
witnesses, gates and GRAPH_HARMFUL. Native archives decoded = 0; deep correspondence
executions = 0. Capture-time deep proof = AUTHENTICATED, not REEXECUTED.

| Normal phase | Time (seconds) |
| --- | ---: |
| Historical sealed-byte audit | 0.021 |
| Primary authentication / one 22-check adversarial bundle | 0.900 |
| Reviewed-gold authentication | 0.028 |
| Checkpoint/ancestry/committed-blob authentication | 15.110 |
| Capture/completion proof authentication total | 3.783 |
| Canonical artifact hashing (within capture total) | 0.097 |
| Journal/archive byte hashing (within capture total; no decode) | 1.304 |
| Completion chain/source checks (within capture total) | 2.163 |
| Seal/file-set identity (within capture total) | 0.194 |
| Canonical loading and input indexing | 1.779 |
| Metrics | 0.138 |
| Enrichment | 0.003 |
| Semantic validation plus five adversarial mutations | 0.073 |
| Markdown | 0.053 |
| Artifact encoding/hashing | 0.457 |
| Committed-byte comparison | 0.016 |

Nested phase times are not additive with their owning total. The 10-second desired
target was not met; the 30-second acceptance target passed. Checkpoint authentication
is the remaining largest measured phase, not retrieval or native graph traversal.
Versus the approximate historical 55-minute observation, ordinary verification is
about 147 times shorter; this is a changed proof-reexecution boundary, not an
equal-work speedup of forensic replay. The prior 180-second failure did not complete
and is not a valid exact speedup denominator.

Primary authentication fell from approximately six recursive executions to one;
the primary adversarial bundle executes once. Normal journal/native reconstruction
count is zero; journal envelopes and the completed chain are authenticated once.
Each fresh invocation reauthenticates authoritative bytes independently. No trusted
filesystem or global cache is introduced. Deep parse/block/alias optimizations and
all earlier diagnostics are retained for forensic use.

Repair commit: the owning Git checkpoint, **Separate sealed and deep experiment
verification**. [Raw bounded run](verifier_repair/layered/normal_verify.json),
[parsed result](verifier_repair/layered/normal_verification.json) and
[repair record](verifier_repair/layered/results.json) preserve timings and evidence.
Full RI (~289 s), incremental maintenance requirement and the ~19.6 ms filename
index optimization remain unchanged and separate. No next retrieval experiment
is designed or executed in this checkpoint.
