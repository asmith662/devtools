# Case 0016 Graph-3 Stage A review

Stage B NOT EXECUTED; gold ABSENT; effectiveness NOT_EVALUATED.

# Graph-3 ownership and gap audit

## Historical experiments: exact scope and results

Graph-1 (Increment 32) added exactly one typed edge from the saved direct
frontier, usually two edges from the original canonical lexical top-five seeds.
Its four families were Imports, bounded References/direct Call tags, immediate
package membership and exact mirrored source/test correspondence, in supported
forward/inverse directions. It had no scoring, normalization, pruning, top-N or
task-conditioned ranking. Novelty excluded all five positive lexical universes
and all prior direct candidate populations. The frozen development result records
24 cases, 22 with novelty, 225 frontier pairs/957 first supports, 704 novel pairs
(183 distinct addresses), 10,550 novel-support paths, maximum 80 candidates per
case/75 per seed, 969 direct-union overlaps and 6,561 originating-seed returns
rejected. Second-edge Imports had 65,576 paths, including 46,883 inverse versus
18,693 forward; package 4,356, References 1,489, mirrors 105. Its prospective
sample found 2 USEFUL/126 NOT_USEFUL out of 128; 574 pairs were unsampled. The
original breadth verdict established sampled complementary reach, with low
sampled useful density; it did not claim full-population precision or total
failure of structural retrieval.

Graph-2 (Increment 33) expanded all 704 Graph-1 candidates by exactly one further
edge, normally three edges from original seeds. Frontier choice was independent
of judgments. The same four relation families/directions remained unweighted and
unranked. It recorded 11,208 third-edge supports, 2,084 projected pairs, 987 novel
pairs (232 addresses; 82 globally new), 598 direct overlaps and 499 Graph-1
overlaps. There were 294,154 COMPLETE three-edge paths, of which 85,015 supported
novel pairs; these scopes must not be conflated. Immediate reversals numbered
93,248 and direct-frontier returns 132,594. Maximum novelty was 87 per case/70
per seed. Forward/inverse Imports contributed 120,350/120,811 complete paths.
The prospective sample found 0 USEFUL/128 NOT_USEFUL; 857 unresolved pairs were
unsampled, with 2 separately reused NOT_USEFUL judgments. No complete-population
absence claim is supported. The verdict did not establish useful complementary
Graph-2 reach and parked further blind depth expansion.

Authority: retained increment_32/33 README.md and development_results.json,
docs/architecture/retrieval.md and the retained breadth/repository-context
research synthesis. No prior treatment was rerun. Reverse Imports, degree-driven
fan-out, rediscovery and reversal traffic are demonstrated failure patterns;
sampled low yield concerns breadth, not every possible ranked structural view.
Historical path volumes describe mechanism/cost, never Graph-3 effectiveness.

Existing ranked graph/map baselines (Case 0002) and prospective Case 0003 also
exist. Graph-3 is a new references-only, uniformly task-seeded hypothesis, not
the repository's first PPR implementation. Current graph docs distinguish those
retained tests from Graph-3; no parameters are selected from their gold.

## Current inventory

RI currently lives in context.repository and context.python, not a universal
graph domain. Native resources have RepositoryId/SnapshotId/address/content
identity; functions, classes and direct methods have structural subject,
definition/derivation identity and exact UTF-8 spans. Active bounded declaration
References assess Name/outermost Attribute loads and resolve same-module,
imported-member, one-facade, module-qualified and class-qualified-method routes.
Calls are syntactic tags on References, not runtime call knowledge. Unresolved,
ambiguous, shadowed, unsupported/dynamic receiver and decorated-binding cases
assert no positive edge. Imports/module/member resolution and explicit-root
interpretations retain native dependencies and routes. Legacy function-only
Reference values exist only for historical replay.

graph.view supplies resource-forward, typed-core and typed-navigation views.
Resource-forward has resource nodes and Imports/References; typed variants add
function/class/method nodes, containment/direct bases, and optionally immediate
membership/mirrors. Resource-forward normalizes distinct facts; typed views
balance relation families, then contributions. Resource self-transitions are
omitted by the current builder. graph.pagerank is query-relative PPR, seeded by
all supplied positive lexical ranks with normalized 1/(60+rank), no exact seed
union. Damping .85, L1 tolerance 1e-10, 200 iterations, personalized dangling
return and deterministic stationary_distribution already exist. Resource score
is max resource/declaration mass; ties use lexical rank then address.

repository_map supplies query-independent global dependency importance with
resource-uniform restart, compact symbol/name/path BM25, symbol-level RRF and
best-symbol resource projection. It is not task-personalized references-only
PPR and does not render a map. Native RepositoryMapSymbol preserves definition
identity/name/span/owner. structural.py offers one supplied direct relationship
in either direction; composition preserves native evidence without fused rank.
fusion.py owns optional resource-level equal-channel RRF constant 60, absent
view contribution zero, union membership, score descending then lexical rank
then address. These are callable capabilities, not a default pipeline.

Exact acquisition already owns snapshot.resource_at, module lookup, declared
name/source declaration and direct-method grounding. Graph-3 freezes caller
resource-address locators copied literally from obligation queries; native
snapshot.resource_at resolves them in Stage B, retaining absent outcomes. No
automatic identifier extractor, fuzzy heuristic or future requested file seed.

Context Planning owns explicit DisclosurePlan choices, retained-state
materialization and rendering/ModelRequest assembly. It has whole-resource and
qualified-reference choices, no repository-map renderer or automatic token
planner. Native function.materialization extracts exact UTF-8 source spans.
Token/representation budgeting belongs in Context Planning, not RI or graph
truth. This experiment's map uses an exact 8192-byte diagnostic ceiling only.
Localization owns obligations, accepted witnesses/readiness, not PPR semantics.

## Required capability / existing owner / gap matrix

| REQUIRED CAPABILITY | EXISTING OWNER | EXISTING IMPLEMENTATION | SEMANTICS MATCH? | REUSE / ADAPT / ADD | RATIONALE |
| --- | --- | --- | --- | --- | --- |
| Snapshot-qualified resources/content/documents | RI context.repository | observation, snapshot, corpus, document | Yes | REUSE | Native identities and retained text; Git commit is not snapshot identity |
| Definitions and references | RI context.python | function/classes declarations; references.declarations | Yes, bounded | REUSE | Positive native facts only, explicit non-exhaustive resolution |
| Import/call knowledge | RI context.python | imports/modules; direct_call tag | Yes as provenance, not separate relations | REUSE | Preserve resolution support; no additional treatment edge families |
| Reference-only resource nodes/edges | Retrieval | graph.view resource-forward | Partial | ADAPT | Existing builder mixes optional Imports, omits self edges and uses linear counts |
| sqrt distinct-reference weights | Retrieval experiment | view.py | Missing | ADD | Count positive occurrences once, sqrt damping, normalize each source row |
| Exact existing target seeds | RI exact lookup, Retrieval seed policy | snapshot.resource_at and grounding mechanisms | Partial | ADAPT | Frozen caller literals; native result validation, no new resolution heuristic |
| Top-10 lexical and uniform seed union | Retrieval experiment | canonical BM25, ranking.seed_union | Partial | ADD | Production wrapper uses all reciprocal-rank seeds; policy is different |
| Restart/degree-normalized PPR | Retrieval graph.walk | stationary_distribution | Yes | REUSE | Accepted .85/1e-10/200 arithmetic, dangling personalization |
| Resource ranking and contribution trace | Retrieval experiment | native view/facts plus ranking.py | Partial | ADAPT | Resource-only score, address ties; restart/dangling/edge-flow separation |
| Definition projection | RI declarations, Retrieval diagnostic | RepositoryMapSymbol/native declarations | Partial | ADAPT | Reuse native identities/source extraction; parent PPR and reference flow, no global-map rank |
| Lexical/graph RRF | Retrieval fusion | _fused_resource_order | Yes | REUSE | Exact production arithmetic and ties; adapter avoids falsely naming native reciprocal-seed mechanism |
| Map textual representation | Context Planning | explicit plans/rendering; no map renderer | Missing | ADD experiment diagnostic | Exact native header excerpts; no production representation promotion |
| Diagnostic size budget | Context Planning boundary | no universal token cost policy | Missing | ADD experiment diagnostic | Exact UTF-8 byte ceiling; no tokenizer or scoring influence |
| Sufficiency/witness interpretation | Localization and future blind gold | localization semantic kernel | Separate owner | REUSE boundary | No rank-derived relevance or semantic adjudication at Stage A |

## Boundary and implementation disposition

RI facts/provenance remain native truth, Retrieval owns the reference projection,
task seeds, PPR and RRF evidence; Context owns later production representation
choices, and Localization owns obligation-relative witnesses/readiness. New code
is non-installable experiments/task_conditioned_graph composition only. No
universal graph, Selection domain, registry, production graph semantics, RI
budget or Localization satisfaction engine is introduced. Private canonical
validation/source-extraction/RRF helpers are deliberately reused and sealed,
rather than copied into a second scientific arithmetic implementation.

No paths or BFS frontiers generate candidates. Ranking iterates a compact graph;
optional shortest distance from seeds can be computed only AFTER ranking as a
diagnostic and never determines scores. Every positive node is retained, bounded
by the finite observed frame; display diagnostics use top 10/20/50 and the map
byte ceiling. No unbounded path-family publication is planned.


## Prospective amendment

# Prospective propagated-reference-flow amendment

Prior Stage A: e2cc61600705eb5faccb814cb19f81aac5645a73.
Prior integrity SHA-256: 84529a786ada2d814a56039328f902fa6e28ddb93e7488d41b83282b2ee67009.
Status: PROSPECTIVE; no Case 0016 execution or gold before amendment.

The original stationary-mass B ranking could give lexical seeds a second RRF
vote from restart/dangling personalization without structural evidence. PPR now
remains internal source importance; TASK_CONDITIONED_REFERENCE_PPR_FLOW ranks
only positive incoming flow, d * sum(pi(source) * P(source,target)). No additional
arm or stationary-mass fusion is introduced. Seed-only state is retained as
diagnostic evidence and excluded from B. Genuine incoming flow can qualify seeds.

Every node retains stationary, direct restart, dangling return and incoming
structural flow. The existing algebraic convention remains 2*tolerance for
stationary accounting, with frozen kernel/convergence unchanged. Definition
diagnostics aggregate equal-per-occurrence pair flow and order primarily by that
definition flow, then existing parent-resource rank and definition identity ties.
Map byte/header bounds remain 8192/240. Production RRF uses corrected B ranks.

Task identity/text, obligations/queries, frame/content, RI derivation, graph/view
policy, reference identities, counts/sqrt/rows/self edges, exact locators, K=10,
uniform seeds, no-seed behavior, damping/tolerance/iterations/dangling behavior,
Arm A, RRF arithmetic/weights/ties, gold policy, metrics/burden, failure classes,
gate thresholds/precedence and historical Graph-1/2 evidence remain unchanged.
Original checkpoint remains immutable historical evidence in Git. The amended
publication authenticates its original seal, checks a restricted protocol diff,
preserves frame/resources bytes and refuses a second amendment overwrite.

No prospective retrieval, exact resolution, RI References, graph, PPR, fusion,
rankings, map or gold is produced. Controlled fixtures remain segregated.


## Selection

# Case 0016 selection

SELECTION_CRITERIA.json was written before final task authoring. Inputs were
current architecture/package contracts, B-0002 future disclosure pressure, source
interfaces and the exact task texts of Cases 0011–0015. No prior gold was used.
No prospective lexical, exact-route, graph/connectivity, rank, score or candidate
surface was inspected. No claim about actual required resources is made here.

| Candidate considered | Disposition and reason |
| --- | --- |
| Caller-selected resource-pointer disclosure | Selected: bounded Context representation already motivated by B-0002 and ADR-0004; existing whole-resource/plan/materialization/assembly interfaces provide a realistic multi-package task, while policy/validation evidence remains partly lexical |
| Direct Python source-declaration disclosure | Rejected: same immediate feature as Case 0012 |
| Context disclosure manifest | Rejected: same immediate feature as Case 0013 |
| General incremental RI invalidation/cache | Rejected: broad unresolved persistence/scheduling design, unsuitable for a bounded feature task |
| New graph or configuration relationship family | Rejected: would entangle the requested feature with the treatment architecture and invite graph-oriented selection |

Selected task contains six mandatory obligations. Definition/reference structure
plausibly relates existing plan, resource, materialization and ModelRequest
interfaces; documentation, export policy and validation obligations may remain
primarily lexical. This is a hypothesis, not inspected prospective connectivity.
The feature itself remains unimplemented.


## Frozen selection criteria

```json
{
  "case": "0016",
  "frozen_before_final_task_authoring": true,
  "criteria": [
    "New bounded realistic devtools development capability, different immediate feature from Cases 0011-0015",
    "At least five mandatory obligations with explicit satisfaction criteria",
    "Evidence distributed across multiple resources and packages",
    "Native definition/reference relationships plausibly useful alongside primarily lexical policy/documentation evidence",
    "Natural task identifiers and domain language, not manufactured from inspected edges",
    "Prefer existing backlog/future-capability pressure with a supported architectural owner"
  ],
  "selection_inputs": "Current architecture, backlog, source/package contracts, and prior task text only",
  "excluded_selection_inputs": ["Prior-case gold", "Prospective retrieval", "Lexical ranks", "Exact-route results", "Graph facts/connectivity", "Graph ranks", "Fusion ranks", "Candidate counts"],
  "production_implementation_authorized": false
}
```

## Exact task

Add an explicit caller-selected resource-pointer disclosure choice to common Context Planning, alongside existing whole-resource and qualified-reference choices.

O1. A pointer identifies an already observed repository resource without including its source body. Reuse the existing snapshot/resource identity and lookup contracts, and inspect the whole-resource choice in src/devtools/context/planning/resource.py. Preserve repository identity, snapshot identity, canonical resource address and content identity; a pointer is orientation evidence, not proof of relevance, adequacy or task completion.

O2. Integrate the new immutable choice with PlannedDisclosure, DisclosurePlan and materialize_disclosure_plan. Its deterministic option identity must bind representation, purpose and exact resource applicability. Mixed plans preserve caller order and the one-item-per-choice contract; reject duplicate identical choices and incompatible purpose or frames using existing conventions.

O3. Materialization uses only retained RepositorySnapshot state. Authenticate the supplied observed occurrence through RepositorySnapshot.resource_at, reject foreign/stale snapshots, missing resources and changed content before publishing a MaterializedDisclosureItem, and preserve exact native resource provenance. Do not reacquire files or silently expand a pointer to whole source.

O4. Define a deterministic human-readable pointer representation containing purpose, repository/snapshot identities, resource address, content identity and the observed source UTF-8 byte count, with an explicit statement that source is not disclosed. Keep support address/content pairs aligned even though the represented text omits source. Non-ASCII addresses and source text must be handled faithfully; the byte count is observed source size, not represented Context size.

O5. Preserve render_context_disclosure and assemble_context_disclosure_model_request behavior for mixed pointer/whole-resource/qualified-reference plans: task precedes supporting Context, item order is unchanged, and copied ModelRequest preserves prompt role and all other fields. Export the new choice through the common planning and outer Context facades, without Retrieval dependencies or Python-specific logic in common assembly.

O6. Add focused tests under tests/context/planning/ and update src/devtools/context/planning/docs/overview.md and governing architecture documentation for explicit choice, applicability, native provenance, mixed ordering, deterministic identity/rendering, non-ASCII byte accounting, rejection cases and unchanged existing choices. Follow docs/development/validation.md and scripts/validate_development.py, retaining configured production coverage and strict typing. Do not implement automatic selection, budgeting, truncation, semantic resolution, persistence, authorization or agent execution.

Operational boundary: this is a future development specification for a prospective acquisition experiment. Freeze Stage A only; do not implement this feature or execute prospective retrieval or adjudication.


## case

```json
"0016"
```


## increment

```json
"GRAPH-3 / TASK-CONDITIONED REPOSITORY-MAP RETRIEVAL"
```


## source head

```json
"941678aab144b274216ab1482843ab194a1f5e88"
```


## task identity

```json
"case-0016-resource-pointer-disclosure-v1"
```


## requirement matrix

```json
[
  {
    "mandatory": true,
    "obligation": "O1",
    "query": "repository resource pointer observed snapshot content identity src/devtools/context/planning/resource.py",
    "query_id": "Q1",
    "satisfaction_criteria": "Pointer identifies existing observed resource with exact repository/snapshot/address/content identity and no source body; no relevance/sufficiency claim.",
    "task_clause": "A pointer identifies an already observed repository resource without including its source body. Reuse the existing snapshot/resource identity and lookup contracts, and inspect the whole-resource choice in src/devtools/context/planning/resource.py. Preserve repository identity, snapshot identity, canonical resource address and content identity; a pointer is orientation evidence, not proof of relevance, adequacy or task completion."
  },
  {
    "mandatory": true,
    "obligation": "O2",
    "query": "PlannedDisclosure DisclosurePlan materialize_disclosure_plan purpose identity ordered choices duplicate frame",
    "query_id": "Q2",
    "satisfaction_criteria": "Immutable choice conforms to existing PlannedDisclosure/DisclosurePlan/materialization, deterministic identity, mixed caller order and duplicate/frame rejection.",
    "task_clause": "Integrate the new immutable choice with PlannedDisclosure, DisclosurePlan and materialize_disclosure_plan. Its deterministic option identity must bind representation, purpose and exact resource applicability. Mixed plans preserve caller order and the one-item-per-choice contract; reject duplicate identical choices and incompatible purpose or frames using existing conventions."
  },
  {
    "mandatory": true,
    "obligation": "O3",
    "query": "RepositorySnapshot resource_at MaterializedDisclosureItem retained native provenance stale missing changed content",
    "query_id": "Q3",
    "satisfaction_criteria": "Retained-state resource lookup authenticates native provenance and rejects foreign/stale/missing/changed resources, with no reacquisition or source expansion.",
    "task_clause": "Materialization uses only retained RepositorySnapshot state. Authenticate the supplied observed occurrence through RepositorySnapshot.resource_at, reject foreign/stale snapshots, missing resources and changed content before publishing a MaterializedDisclosureItem, and preserve exact native resource provenance. Do not reacquire files or silently expand a pointer to whole source."
  },
  {
    "mandatory": true,
    "obligation": "O4",
    "query": "resource pointer representation source not disclosed UTF-8 byte count content identity non-ASCII",
    "query_id": "Q4",
    "satisfaction_criteria": "Exact deterministic pointer text exposes prescribed identity/purpose/observed source bytes, explicit source omission and aligned supports including non-ASCII.",
    "task_clause": "Define a deterministic human-readable pointer representation containing purpose, repository/snapshot identities, resource address, content identity and the observed source UTF-8 byte count, with an explicit statement that source is not disclosed. Keep support address/content pairs aligned even though the represented text omits source. Non-ASCII addresses and source text must be handled faithfully; the byte count is observed source size, not represented Context size."
  },
  {
    "mandatory": true,
    "obligation": "O5",
    "query": "render_context_disclosure assemble_context_disclosure_model_request ModelRequest prompt role mixed plan public exports",
    "query_id": "Q5",
    "satisfaction_criteria": "Existing common rendering/copied ModelRequest and choices remain compatible; exports and dependency direction preserved.",
    "task_clause": "Preserve render_context_disclosure and assemble_context_disclosure_model_request behavior for mixed pointer/whole-resource/qualified-reference plans: task precedes supporting Context, item order is unchanged, and copied ModelRequest preserves prompt role and all other fields. Export the new choice through the common planning and outer Context facades, without Retrieval dependencies or Python-specific logic in common assembly."
  },
  {
    "mandatory": true,
    "obligation": "O6",
    "query": "pointer disclosure tests documentation architecture validation scripts/validate_development.py",
    "query_id": "Q6",
    "satisfaction_criteria": "Focused tests, authoritative/package docs and protected validation cover exact fidelity/rejections/nonclaims without changing production test policy.",
    "task_clause": "Add focused tests under tests/context/planning/ and update src/devtools/context/planning/docs/overview.md and governing architecture documentation for explicit choice, applicability, native provenance, mixed ordering, deterministic identity/rendering, non-ASCII byte accounting, rejection cases and unchanged existing choices. Follow docs/development/validation.md and scripts/validate_development.py, retaining configured production coverage and strict typing. Do not implement automatic selection, budgeting, truncation, semantic resolution, persistence, authorization or agent execution."
  }
]
```


## arms

```json
{
  "A": "CANONICAL_BM25",
  "B": "TASK_CONDITIONED_REFERENCE_PPR_FLOW",
  "C": "BM25_GRAPH_RRF"
}
```


## comparisons

```json
{
  "diagnostic": "B versus A",
  "primary": "C versus A",
  "reference": "Whole exact task canonical BM25, unchanged separate lane; never treatment/rescue"
}
```


## canonical bm25

```json
{
  "analyzer": "Native Unicode word spans/casefold, distinct query terms",
  "b": 0.75,
  "filename_weight": 0.25,
  "k1": 1.2,
  "maximum_results": "All positive matches, bound = frame resource count",
  "score": "Native content BM25 + .25 independent filename-stem BM25",
  "ties": "Native collection order"
}
```


## ri fact contract

```json
{
  "coverage": "Native bounded non-exhaustive assessment outcomes retained; unsupported/ambiguous/unresolved creates no edge; parse/derivation error is contract/ranking defect, no scientific retry",
  "derivation": "derive_python_declaration_references",
  "input": "Frozen retained snapshot only",
  "module_addresses": "All frame .py resources interpreted under src for src/ paths, under . otherwise; no automatic root guesses",
  "module_roots": [
    "src",
    "."
  ],
  "native_support": "Definition/reference subjects, occurrences, derivations, source/target resources, spans, import/member/module route provenance; no guessed truth",
  "reference_sources": "Each frame .py resource once, address order, supplied native universe/source interpretations"
}
```


## graph projection

```json
{
  "call_import_tags": "Native reference qualification/Call tags only; no separate edge or weight",
  "edges": "REFERENCER_RESOURCE -> DEFINER_RESOURCE for each positive resolved declaration Reference; retain self references",
  "excluded_families": [
    "Imports as separate edge",
    "Calls as separate edge",
    "tests",
    "inheritance",
    "containment",
    "configuration",
    "directory adjacency",
    "reverse edges"
  ],
  "families": [
    "REFERENCE"
  ],
  "no_paths": "No BFS/frontier/path enumeration generates or scores candidates; optional distance only after ranking, not effectiveness metric",
  "nodes": "Every eligible observed repository resource occurrence, address order, bound N",
  "normalization": "weight / fsum(outgoing pair weights), canonical source/target order",
  "provenance": "Retain native fact objects unmodified; compact serialization retains fact/derivation/occurrence/subject/definition/route/content identities, spans, identifier expression and full native route support. Derived identity is not a replacement for support.",
  "raw_count": "Distinct native resolved reference occurrences per directed resource pair; duplicate identical fact counts once, conflicting same-occurrence facts rejected",
  "weight": "sqrt(raw_reference_count)"
}
```


## seed policy

```json
{
  "K": 10,
  "exact": "Caller-frozen literal resource-address locators in owning query; existing RepositorySnapshot.resource_at only; retain native resolved/absent result. No prospective resolution at Stage A.",
  "exact_locators": {
    "Q1": [
      "src/devtools/context/planning/resource.py"
    ],
    "Q2": [],
    "Q3": [],
    "Q4": [],
    "Q5": [],
    "Q6": [
      "scripts/validate_development.py"
    ]
  },
  "fallback": "Exact seeds suffice when no lexical positives. If neither signal resolves a seed, NO_SEEDS/empty B, iterations=0; C=A; never global PageRank",
  "future_resource": "A requested future pointer implementation file is not an existing seed; no new hint/extraction/fuzzy heuristic",
  "lexical": "First K unique positive native Arm A resources for same obligation query",
  "personalization": "Uniform 1 / number of unique seeds; normalized",
  "union": "Exact existing resources UNION lexical top K; canonical address deduplication"
}
```


## pagerank

```json
{
  "convergence": "L1 delta <= tolerance, deterministic supplied node/row order; normalize returned mass. Nonconvergence is PAGERANK_APPLICATION_DEFECT; no silent fallback or parameter change.",
  "damping": 0.85,
  "dangling": "personalization",
  "initial": "personalization",
  "kernel": "devtools.context.retrieval.graph.walk.stationary_distribution",
  "maximum_iterations": 200,
  "restart": 0.15,
  "result": "Arm B score is propagated_reference_score(v) = d * fsum(pi(u) * P(u,v)), exactly incoming_structural_flow(v). Only positive structural flow enters B; descending propagated score then canonical address. Stationary mass/restart/dangling do not rank or fuse.",
  "tolerance": 1e-10,
  "trace": "Every node retains stationary_mass, direct_restart_mass, dangling_return_mass, incoming_structural_flow and native incoming pair flows. Retain each seed and whether it appears in B. Stationary = restart + dangling + incoming within unchanged 2*tolerance accounting convention; full mass normalization unchanged. Seeds with zero flow are excluded from B. Edge flow divided equally among native occurrences; no flow-score renormalization."
}
```


## definition projection

```json
"Positive pair flow = d*pi(source)*P(source,target); divide equally among distinct native reference occurrences, aggregate by resolved definition identity. Retain source/target resources, native reference occurrence/span/expression, resolved definition/owner/span, pair/per-occurrence/aggregated definition flow and parent propagated resource rank/score. Validate sums against resource pair flow. Diagnostic only; no symbol aggregation changes resource ranks."
```


## map diagnostic

```json
{
  "budget": "Whole lines in descending propagated definition-flow / parent propagated-resource-rank / definition-identity order, stop at first blocked line; omissions metadata; no token estimator",
  "effectiveness_arm": false,
  "header_characters": 240,
  "maximum_utf8_bytes": 8192,
  "owner_boundary": "Experiment rendering only; production Context representation remains a later decision",
  "representation": "Exact first native declaration line excerpt plus explicit excerpt marker, name/address/location; not complete signature/body/decorators",
  "score_effect": "NONE"
}
```


## fusion

```json
{
  "dependence": "B seeded by A; agreement is not independent corroboration",
  "graph_weight": 1,
  "implementation": "devtools.context.retrieval.fusion._fused_resource_order",
  "lexical_weight": 1,
  "limit": "Entire union bounded by N",
  "missing_view": "Zero contribution; union membership",
  "rank_constant": 60,
  "score": "1/(60+A_rank) + 1/(60+B_rank)",
  "ties": "Descending score, lexical rank (missing infinity), canonical address"
}
```


## metrics

```json
[
  "REQUIRED resource/cell reach",
  "Required repository-supported and all semantic-unit reach (task-backed units unranked)",
  "Every reviewed witness completion depth and stable minimum complete selected witness per obligation",
  "Obligation completeness",
  "Obligation/task-indispensable ranks",
  "Every REQUIRED-cell rank, gain, regression and reach rescue",
  "Graph-novel REQUIRED / HELPFUL_ONLY / UNNECESSARY resources after gold",
  "A-only, B-only, A intersection B, C union and graph-novel resources before labels",
  "Selected completion-prefix union unique resources, repeated occurrences, duplicate occurrences",
  "Obligation-relative REQUIRED / HELPFUL_ONLY / UNNECESSARY occurrences",
  "Distinct UTF-8 resource bytes in selected prefix union",
  "Captured single-run execution/preparation/publication cost without outcome threshold"
]
```


## measurement semantics

```json
{
  "burden": "Only selected mandatory owning-query prefixes. Count repeated resources per query separately; distinct resource/UTF-8 byte union counts each exact content occurrence once. Label occurrences against their own obligation; all candidate/gold joins must validate.",
  "candidate_safety": "A/B membership may differ; C=union(A,B) with full frame-size result bound. No retrospective pruning or candidate removal. Compare reach, noise and concentration only after blind gold.",
  "incomplete_burden": "Report incomplete obligations separately; strong burden comparison not eligible if either arm has an incomplete selected mandatory obligation. A-incomplete/C-complete may still support through safe material reach rescue or complementary value, never fictional baseline completion burden.",
  "indispensability": "Obligation intersection of reviewed minimal witnesses; task intersection of reviewed complete task combinations; task-backed units have no rank",
  "joins": "Exact case/task/obligation/query/repository/snapshot/corpus/address/document/content identity; no filename-only mapping; Q1-Q6 own O1-O6 respectively",
  "resource_reach": "Distinct REQUIRED union resources reached in owning REQUIRED cells; cell reach is owning-query membership, never rank under another obligation",
  "unit_reach": "A repository-supported unit is reached when one complete reviewed support alternative is reached under its owning obligation query; never mix members from different alternatives. Task-backed units are available from task, have no retrieval rank; report repository-supported and all units separately.",
  "witnesses": "For each reviewed witness independently, all repository members must be reached; depth=max owning-query ranks, empty witness=0; incomplete=None. Prefix occurrences are owning-query ranks 1..depth. Select minimum complete depth then reviewed stable identity; no complete witness means incomplete, no fabricated prefix/depth."
}
```


## diagnostics

```json
[
  "Top-K overlap/entered/exited/inversions at 10/20/50, labels only after blind gold",
  "Seed versus propagated mass/rank share, top incoming contributors and responsible reference identifiers",
  "Structural distance from seeds after ranking only",
  "A/B native rank contributions to C; removing B from frozen RRF (A order) explains hybrid movement without a new treatment"
]
```


## historical comparison

```json
"Later compare retained Graph-1/2 expansion size, ranked concentration, novel evidence yield, path explosion, reverse/fan-out noise and discovered required evidence; nonmatched cases prohibit a controlled causal superiority claim. No historical rerun or raw path-count effectiveness metric."
```


## failure taxonomy

```json
[
  "GRAPH_VIEW_CONSTRUCTION_DEFECT",
  "REFERENCE_RESOLUTION_DEFECT",
  "GRAPH_EDGE_PROVENANCE_DEFECT",
  "PERSONALIZATION_DEFECT",
  "PAGERANK_APPLICATION_DEFECT",
  "FUSION_APPLICATION_DEFECT",
  "SEED_CARRYOVER_WITHOUT_PROPAGATED_VALUE",
  "DEGREE_DILUTION",
  "HUB_DOMINANCE",
  "AMBIGUOUS_IDENTIFIER_FANOUT",
  "REVERSE_DEPENDENCY_NOISE",
  "GRAPH_PROPAGATION_NOISE",
  "GRAPH_MISSES_DISCONNECTED_REQUIRED_EVIDENCE",
  "LEXICAL_ONLY_REQUIRED_EVIDENCE",
  "EXPERIMENTAL_CONTRACT_DEFECT"
]
```


## attribution policy

```json
"Graph-contributed gain requires positive Arm-B propagated structural flow, relevant captured native reference provenance, hybrid RRF movement and deterministic graph-channel ablation showing the gain disappears without B. Restart, dangling return and seed identity alone cannot contribute a B rank/vote. SEED_CARRYOVER_WITHOUT_PROPAGATED_VALUE identifies forbidden positive seed-only ranking or diagnostic internal state, never valid graph-channel credit. Noise/hub/dilution classifications require demonstrated necessary-evidence/overtaker consequence, not raw degree/score. B-only poor ordering does not itself select hybrid failure."
```


## decision rule

```json
{
  "bounds": "Baseline-complete selected depths remain complete; 5*C_depth <= 6*A_depth AND C-A <= 5; baseline-reached REQUIRED ranks retained, 5*C_rank <= 6*A_rank AND C-A <= 10; every regression independently bounded",
  "burden_scope": "Selected mandatory witness prefixes only; union resources/bytes across obligations, retain repeated occurrences and obligation-relative labels; no fictional global task ranking",
  "cost_and_map": "Descriptive only; no outcome threshold",
  "implementation": "experiments/task_conditioned_graph/gates.py",
  "implementation_checks": "Native RI frame/content/support, unchanged reference projection/count/sqrt/rows/seeds/PPR; full stationary accounting and pair flow sums; B membership/score/order exactly positive incoming flow, reject seed-only/total-stationary ranking; definition occurrence/aggregate sums equal pair/resource flows; production RRF consumes corrected flow ranks only; exact native joins, unchanged reference lane, once-only execution and valid blind gold",
  "meaningful_required_rank": "Both reached, A_rank-C_rank >= 2 AND 5*C_rank <= 4*A_rank",
  "meaningful_witness": "A incomplete and C complete OR A_depth > 0 AND 5*C_depth <= 4*A_depth",
  "precedence": [
    "Contract defect => EXPERIMENTAL_CONTRACT_DEFECT",
    "RI/view/provenance/personalization/PPR/fusion implementation defect => GRAPH_RANKING_DEFECT",
    "REQUIRED resource/cell/unit reach loss OR baseline completion loss OR any unbounded required rank/selected depth regression => GRAPH_HARMFUL",
    "Valid and no loss/unbounded regression, graph-contributed meaningful witness gain or REQUIRED reach rescue AND (strong burden improvement OR safe material reach gain) => GRAPH_HYBRID_SUPPORTED",
    "No loss/unbounded regression, graph-contributed meaningful rank/witness gain or novel REQUIRED reach rescue => COMPLEMENTARY_GRAPH_VALUE",
    "Otherwise => NO_MATERIAL_VALUE"
  ],
  "primary": "C versus A only",
  "reach_rescue": "A REQUIRED cell unreached and C reached, minimum one cell; no fabricated A rank; resource/unit reach also retained",
  "safe_material_gain": "At least one graph-contributed REQUIRED-cell reach rescue, no baseline-complete depth or baseline-reached REQUIRED-rank worsening, no required-unit reach loss",
  "selected_witness": "Minimum complete depth, then stable reviewed witness identity; never mix members from alternative witnesses",
  "strong_burden": "Positive baseline unique and occurrence counts; (10*C_unique <= 9*A_unique OR 10*C_occurrences <= 9*A_occurrences) AND all unique/occurrence/distinct-byte dimensions nonincreasing",
  "zero_resource_witness": "Complete at depth 0, zero prefix/burden, task-backed units unranked; 0-to-0 not meaningful, no division"
}
```


## gold policy

```json
{
  "MODEL": "GPT-6 Astra",
  "REASONING": "High",
  "allowed": [
    "case/task identity",
    "exact task",
    "obligations/satisfaction criteria without queries",
    "eligible resource identities/content"
  ],
  "automatic_second_reviewer": false,
  "excluded": [
    "queries",
    "seed identities",
    "lexical ranks",
    "exact-route results",
    "graph nodes/edges/reference graph",
    "PPR parameters/scores",
    "graph/fusion ranks",
    "repository-map diagnostic",
    "candidate results",
    "metrics",
    "costs",
    "gates",
    "outcomes"
  ],
  "natural_text": "Unchanged; no treatment-origin metadata or text rewriting",
  "reviewers": "One clean primary; no automatic second reviewer/reconciliation",
  "treatment_blind": true
}
```


## durable state

```json
{
  "R1": "Separate identifier-aware view",
  "R1.7": "COMPLETE / QUERY_TERM_WEIGHTING_HARMFUL",
  "R1.7_scope": "Query-side evidence",
  "R2": "COMPLETE / BM25F_HARMFUL",
  "R2_scope": "Document-field-combination evidence",
  "U1": "COMPLETE / INFORMATION_NEED_AUTHORING_DEFECT",
  "U2": "COMPLETE / EXACT_HINT_ROUTING_SUPPORTED",
  "U3": "COMPLETE / SELECTIVE_MECHANISM_ROUTING_SUPPORTED",
  "next_direction": "GRAPH / REPOSITORY-MAP RETRIEVAL"
}
```


## exclusions

```json
{
  "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
  "confirmation_reserve": "NOT_ACCESSED",
  "feature_implementation": "NOT_AUTHORIZED",
  "no_tuning": true,
  "production_behavior": "UNCHANGED",
  "prospective_execution": "NOT_EXECUTED"
}
```


## no execution

```json
{
  "exact_seed_resolutions": 0,
  "fusion_executions": 0,
  "gold": "ABSENT",
  "graph_construction_executions": 0,
  "lexical_query_executions": 0,
  "pagerank_executions": 0,
  "reference_query_executions": 0,
  "repository_map_diagnostics": 0,
  "ri_reference_derivations": 0,
  "treatment_rankings": 0
}
```


## prospective amendment

```json
{
  "prior_integrity_sha256": "84529a786ada2d814a56039328f902fa6e28ddb93e7488d41b83282b2ee67009",
  "prior_stage_a_checkpoint": "e2cc61600705eb5faccb814cb19f81aac5645a73",
  "reason": "Remove seed restart/dangling carryover from Arm-B structural ranking; stationary PageRank is source importance, propagated reference flow is retrieval evidence",
  "scientific_status": "PROSPECTIVE / no Case 0016 execution before amendment",
  "unchanged": "Task/obligations/queries/frame/RI/view/edge/seeds/PPR/A/RRF/gold/metrics/burden/failure classes/gate thresholds and precedence remain frozen"
}
```


## frame policy

```json
{
  "eligibility": "Broad committed source/test/docs/config; exclude experiments, tests/experiments, research/reports/ledger, held-out/operational paths before content reads",
  "excluded_prior_case_resources": [
    "docs/architecture.md",
    "docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md",
    "docs/architecture/localization.md",
    "docs/architecture/retrieval.md",
    "docs/architecture/taxonomy.md",
    "docs/backlog/epics/B-0002-coding-context-substrate.md",
    "docs/backlog/items/B-0047-protected-development-validation-profile.md",
    "docs/development/validation.md",
    "docs/documentation_map.md",
    "docs/roadmap.md",
    "src/devtools/context/localization/docs/overview.md",
    "src/devtools/context/localization/roles/docs/overview.md",
    "src/devtools/context/python/project_configuration/docs/overview.md",
    "src/devtools/context/python/references/analysis.py",
    "src/devtools/context/retrieval/docs/overview.md",
    "src/devtools/context/retrieval/graph/docs/overview.md",
    "src/devtools/context/retrieval/repository_map/docs/overview.md"
  ],
  "prior_case_text": "Exclude whole resource containing case[_ -]?00\\d\\d marker; never strip natural content",
  "task_query_independent": true
}
```

## Frozen native frame

```json
{
  "corpus_id": "1e0df552f370938fcbbbf489a4bf433a25b4a218b1f624b72a21e463bcbdc7b0",
  "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
  "representation": "native exact decoded whole UTF-8 text; no windows/subtokens/fields changed",
  "resource_count": 514,
  "resource_order": "canonical resource address ascending",
  "snapshot_id": "636f86afb0fef7b8ccdd9adfd1c9f64dea76139b90d3d098f8f2b811bd90dfca",
  "source_head": "941678aab144b274216ab1482843ab194a1f5e88"
}
```

All resource identities: frame.json; exact retained contents: resources.json.gz. No prospective RI reference derivation, graph, exact resolution, lexical retrieval, rank, candidate result, map or gold was produced. Synthetic fixtures are separate and contain no Case 0016 resources.

Maintainer reviews frozen Case 0016 Graph-3 Stage A. Then separately execute canonical BM25, task-conditioned reference PPR and frozen RRF prospectively exactly once. STOP before Stage B now.
