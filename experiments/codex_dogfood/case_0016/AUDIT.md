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
