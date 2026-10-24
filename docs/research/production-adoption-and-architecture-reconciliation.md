# Production adoption and architecture reconciliation

## Disposition

Source/evidence audit at `8d70ba9fc4f0d9bb45c1f8528e212ecf9c601e6b`,
2026-10-23. This is a dated reconciliation checkpoint, not an architectural
decision, API registry, execution grant or automatic backlog promotion.
The [taxonomy](../architecture/taxonomy.md), [documentation map](../documentation_map.md),
accepted ADRs, current source/tests and canonical backlog retain authority.
Original experiment judgments and earlier audit bodies are unchanged.

## Executive production state

Remote feature and local HEAD were both `8d70ba9fc4f0d9bb45c1f8528e212ecf9c601e6b`;
remote main was `5d979920d0728775ed529457c88f5b68b440c64f`.
One registered checkout, no active Checkout owner, clean initial index/tracked
tree and the same 13 original untracked forensics were authenticated. No branch
switch, production change, model call, scientific replay or service mutation
occurred. Main was not modified.

Of 250 framework Python files, 218 have identical Git blobs on main; 28 differ
and four are new. This is byte-level adoption evidence, not proof of equivalent
behavior for different bytes or live deployment. The nine Commands source
modules already match main. Main additionally owns
`tests/resources/commands/test_composition.py` and
`docs/development/commands-integration.md`, absent on the feature tree: preserve
them in every main-derived integration; do not copy feature directories wholesale.

The [machine evidence](production-adoption-and-architecture-evidence-20261023.json)
records 48 capability slices, exact source/test Git blobs and physical SHA-256,
eight proposed integration groups with conservative import closure, all 35
collections and custody checks. It is an audit companion, not a second registry.
The AST inventory covers 658 tracked Python files with no parse failures.
Imports/calls are bounded source evidence, not an executed application trace.
Only direct imported-call candidates were mechanically collected; prose qualifies
actual owners, deferred imports and internal versus application consumers.

The main-adopted graph/map/RI substrates are useful. Later caller-scoped search,
map/source Planning, native navigation, source-bound checks and governed local
publication remain feature-only. SnapshotDelta is exported/tested but has no
maintained non-test caller found. Conversation persistence and optional Evidence
inspectors do not make native working state durable. No generic framework Agent
loop is implemented by the orchestration namespace marker.

## Classification and method

`MAIN_ADOPTED` means the inspected semantic slice has source at the pinned main
destination. `FEATURE_ONLY` means a required slice differs or is absent there.
`MAINTAINED_NOT_CONSUMED` names a particular missing consumer, not necessarily
an entirely unused package. `EXPERIMENT_ONLY` is research machinery/policy with
no demonstrated maintained promotion. `SUPERSEDED` applies to a representation
or mechanism with a documented replacement. `INCOMPLETE_OR_BLOCKED` preserves
unmet prerequisites/outcomes. `NEEDS_SEMANTIC_REVIEW` marks a decision boundary;
`UNKNOWN` means a relationship was not established. Axes can coexist.

Source/test fingerprints and exports were compared with the actual destination,
representative producers/consumers and permanent test bodies. Package presence,
static imports, tests and scientific acceptance are separate evidence strengths.
No historical feature gate is treated as a new destination validation. Physical
CRLF hashes are not silently equated with LF Git blob identities. The
[five-flow audit](development-lifecycle-observability-audit.md) owns those joins.

## Capability, consumer and adoption matrix

Each linked source/test scope has an exact path inventory in the companion.
The provenance column identifies original design/research or delivery records;
the companion's last-touch commit is not claimed to be the original accepted
candidate. Where a collection-to-source promotion join is missing it remains
explicitly UNKNOWN in the experiment table.

| Slice and maintained interface | Adoption / missing consumer | Design/delivery provenance | Actual use, tests and disposition |
|---|---|---|---|
| [Package navigation/exports](../../src/devtools/__init__.py); namespace marker | FEATURE_ONLY | Accepted domain/package ownership | Public initializers connect maintained APIs; the Context root Delta export differs from main. Namespace presence does not implement a capability. No dedicated test scope found; not evidence of use; SELECTIVE_REVIEW |
| [Python address candidacy](../../src/devtools/context/python/source_candidacy.py); `select_python_source_address_candidates` | MAIN_ADOPTED | Bounded repository discovery projection | Caller selects exact lowercase .py suffix addresses; native acquisition consumes the selector, not a content classifier. [tests](../../tests/context/python/test_source_candidacy.py); RETAIN |
| [Direct structural projection](../../src/devtools/context/retrieval/structural.py); `retrieve_python_direct_structural_resources` | MAIN_ADOPTED | Qualified RI import/reference/membership projection | Explicit one-hop caller seeds and positive facts; composition/experiments consume it. No automatic ranking or negative inference. [tests](../../tests/context/retrieval/test_structural.py); RETAIN |
| [Core UUID identity](../../src/devtools/core/identity/__init__.py); `Identity` | FEATURE_ONLY | Continuation09 UUID invariant; nominal domain wrappers | Framework wrappers and source/evidence identity consumers; constructor hardening is feature-only. [tests](../../tests/core/identity/test_models.py); SELECTIVE_REVIEW |
| [Resolved paths](../../src/devtools/core/paths/__init__.py); `resolve_path`, `ResolvedPath` | MAIN_ADOPTED | Established core path policy | Resources, models, applications and WorkCycle use canonical resolution. [tests](../../tests/core/paths/test_errors.py); RETAIN |
| [Time/duration/stopwatch](../../src/devtools/core/time/__init__.py); `Timestamp`, `Duration`, `Stopwatch` | MAIN_ADOPTED | Established core time values | Commands, Runtime, usage and receipts; unresolved duration-boundary proposal remains. [tests](../../tests/core/time/test_models.py); RETAIN |
| [Callable conversion](../../src/devtools/core/conversion/__init__.py); `convert`, `convert_all` | MAIN_ADOPTED | Core conversion substrate | CSV and JSON models call convert/convert_all; no competing converter needed. [tests](../../tests/core/conversion/test_conversion.py); RETAIN |
| [Regex base and split extension](../../src/devtools/core/regex/__init__.py); `split_regex`, `search_regex`, `compile_regex` | FEATURE_ONLY; MAINTAINED_NOT_CONSUMED; gap: split_regex extension only | Editing06/regex development plus existing regex owners | Split is exported/tested with no maintained non-test call found; optional adoption, not a foundation prerequisite. [tests](../../tests/core/regex/test_models.py); SELECTIVE_REVIEW |
| [OS/BSD classification](../../src/devtools/core/system/__init__.py); `get_operating_system`, `OperatingSystem` | FEATURE_ONLY | Continuation09 BSD publication | OS abstraction consumed by filesystem; BSD branch has focused tests, no live BSD validation claimed. [tests](../../tests/core/system/test_bsd.py); SELECTIVE_REVIEW |
| [Filesystem models/codec/I-O](../../src/devtools/resources/filesystem/__init__.py); `BinaryCodec`, `JsonCodec`, `read` | FEATURE_ONLY | Engineering08/Continuation09; existing filesystem foundation | Commands/Tools, package models, Qwen and WorkCycle consume it. Binary, finite-float and bounded-read deltas need selective adoption; B-0048 remains independent. [tests](../../tests/resources/filesystem/codecs/test_csv.py); SELECTIVE_REVIEW |
| [Subprocess/value capabilities](../../src/devtools/resources/commands/__init__.py); `Command`, `CommandExecutor` | MAIN_ADOPTED | stdin11/environment13/engineering14/output validation/decoded output; merged PR1 | All nine source modules match protected main. Keep destination-only composition regression and integration document. [tests](../../tests/resources/commands/test_decoded_output.py); RETAIN |
| [Serving/profiles/providers](../../src/devtools/models/serving/__init__.py); `ServingProfileIdentity`, `VLLMServer`, `LlamaCppServer` | MAIN_ADOPTED | Existing local serving experiments and maintained scripts | scripts/qwen service and model benchmark/operator entrypoints; availability is not model/agent correctness. [tests](../../tests/models/serving/test_huggingface.py); RETAIN |
| [ModelInteraction/native Prompt](../../src/devtools/models/interaction/__init__.py); `ModelRequest`, `PromptMessage`, `ModelToolCall` | FEATURE_ONLY | ADR0001/native coding evolution | Runtime and native loop consume values; structured Prompt/provider/capture guards must be adopted together. [tests](../../tests/models/interaction/providers/test_llama_cpp.py); SELECTIVE_REVIEW |
| [External Codex integration](../../src/devtools/agents/integrations/codex/__init__.py); `CodexAgent` | MAIN_ADOPTED | Maintained external Agent adapter | Experimental semantic worker and usage ingestion consume it; no reclassification as raw model provider. [tests](../../tests/agents/integrations/codex/test_agent.py); RETAIN |
| [Conversation/history](../../src/devtools/agents/conversation/__init__.py); `Conversation`, `ConversationMessage` | MAIN_ADOPTED | Established Conversation ownership | Runtime and persistence consume state; native loop history is task-local Prompt history, not durable Run state. [tests](../../tests/agents/conversation/history/test_history.py); RETAIN |
| [Narrow Runtime/attempt](../../src/devtools/execution/__init__.py); `Runtime`, `InteractionAttempt` | MAIN_ADOPTED | ADR0001 one-invocation lifecycle | Legacy read/acceptance compositions use Runtime; current native loop calls ModelInteraction directly. [tests](../../tests/execution/test_interaction_attempt.py); RETAIN |
| [ToolRunner/adapters](../../src/devtools/tools/__init__.py); `ToolRunner`, `CommandTool`, `ReadRepositoryFileTool` | MAIN_ADOPTED | Narrow validated Tool protocol | Native ContextTools/CodingCommands and existing applications use validation then execution; not authorization. [tests](../../tests/tools/test_command.py); RETAIN |
| [Terminal/model Evidence](../../src/devtools/observability/evidence/__init__.py); `ModelInteractionInspector`, `ExecutionInspector`, `InvocationMeasurement` | FEATURE_ONLY; MAINTAINED_NOT_CONSUMED; gap: optional terminal/model inspectors not composed into maintained native worker | ADR0001/evidence research and worker measurements | Inspectors are optional and no maintained native installation found. InvocationMeasurement has experimental-worker/usage consumers; structured-history capture is feature-only. [tests](../../tests/observability/evidence/test_inspection.py); SELECTIVE_REVIEW |
| [Observed usage/reconciliation](../../src/devtools/observability/usage/__init__.py); `UsageObservation`, `reconcile` | MAIN_ADOPTED | Worker economics/usage engineering | scripts/usage.py and experiment controller consume records; account billing, failed realizations and universal trace joins remain incomplete. [tests](../../tests/observability/usage/test_sources.py); RETAIN |
| [Numeric usage governance](../../src/devtools/governance/__init__.py); `UsageBudget` | MAIN_ADOPTED | Orchestration budget engineering | Real experiment controller consumer; no maintained app-enforced standing budget or execution authority inferred. No dedicated test scope found; not evidence of use; RETAIN |
| [Conversation JSON/SQLite](../../src/devtools/persistence/__init__.py); `encode_conversation_json`, `SqliteConversationStore` | MAIN_ADOPTED; MAINTAINED_NOT_CONSUMED; gap: native task working-state/Evidence consumer, not Conversation store API | Established Conversation persistence | Public stores/tests; no native worker working-state durability or Evidence journal consumer established. [tests](../../tests/persistence/test_json.py); RETAIN |
| [Repository/retained source/snapshots](../../src/devtools/context/repository/__init__.py); `Repository`, `RepositorySnapshot`, `observe_repository_resources` | FEATURE_ONLY | ADR0002 retained observation foundation | RI, retrieval, Planning and native worker use snapshots; discovery/Delta additions are separate deltas. [tests](../../tests/context/repository/test_changes.py); SELECTIVE_REVIEW |
| [RepositorySnapshotDelta](../../src/devtools/context/repository/changes.py); `compare_repository_snapshots` | FEATURE_ONLY; MAINTAINED_NOT_CONSUMED; gap: snapshot-comparison non-test consumer | New-module22 Codex delivery 3c624129 | Exported through repository/context and independently tested; no maintained non-test caller. No rename/incremental-maintenance authority. [tests](../../tests/context/repository/test_changes.py); SELECTIVE_REVIEW |
| [Bounded/explicit-path discovery](../../src/devtools/context/repository/discovery.py); `discover_repository_resource_addresses` | FEATURE_ONLY | Qwen source-admission evolution | Native task-scoped source acquisition uses it; preserve symlink/junction and path/version limits. [tests](../../tests/context/repository/test_discovery.py); SELECTIVE_REVIEW |
| [Python module/import declarations](../../src/devtools/context/python/imports/__init__.py); `interpret_python_module_resources`, `derive_python_import_declarations`, `resolve_python_imported_member` | MAIN_ADOPTED | Earlier RI and Increment25 imported-member evidence | Native source index/static relationships and other RI consumers; no runtime-import claim. [tests](../../tests/context/python/imports/test_declarations.py); RETAIN |
| [Python function facts/source Context](../../src/devtools/context/python/function/__init__.py); `derive_python_function_declarations`, `assemble_python_function_context_model_request` | FEATURE_ONLY | Existing RI/Context and qualified-reference experiments | Source search/Planning and acceptance compositions consume it; new native-message rejection guards depend on Prompt change. [tests](../../tests/context/python/function/test_candidates.py); SELECTIVE_REVIEW |
| [Typed declaration References/Calls](../../src/devtools/context/python/references/__init__.py); `derive_python_declaration_references` | MAIN_ADOPTED | Increment29 bounded references followed by clean production slices | Source index/native source_relationships/navigation and Localization evidence; static qualified facts, not runtime calls. [tests](../../tests/context/python/references/declarations/test_analysis.py); RETAIN |
| [Classes/methods/direct bases](../../src/devtools/context/python/classes/__init__.py); `derive_python_class_method_declarations`, `derive_python_direct_bases` | MAIN_ADOPTED | Later bounded RI after breadth investigation | Native source/map frames and structural consumers; no MRO/runtime dispatch inference. [tests](../../tests/context/python/classes/test_bases.py); RETAIN |
| [Package/mirrored-path relations](../../src/devtools/context/python/mirrored_paths.py); `derive_python_immediate_package_memberships`, `derive_python_mirrored_path_correspondences` | MAIN_ADOPTED | Increment30/31 observations followed by bounded RI | Localization generation/roles consume qualified relations. Mirrored names are not execution or coverage proof. [tests](../../tests/context/python/modules/test_membership.py); RETAIN |
| [Project configuration RI](../../src/devtools/context/python/project_configuration/__init__.py); `analyze_python_project_configuration`, `resolve_python_project_configuration` | FEATURE_ONLY | Codex dogfood configuration plus obstruction21/dependency24 | Role evidence consumes declarations; later obstruction/top-level static groups are feature-only. Raw strings are not installed requirements. [tests](../../tests/context/python/project_configuration/test_configuration.py); SELECTIVE_REVIEW |
| [Canonical lexical/BM25](../../src/devtools/context/retrieval/lexical/__init__.py); `retrieve_repository_text_documents_by_bm25`, `build_repository_text_lexical_inverted_index` | MAIN_ADOPTED | Lexical foundation; sensitivity/breadth diagnostics | Retrieval composition, Localization lexical lane and legacy worker acquisition. Identifier/BM25F experiments are not default production policy. [tests](../../tests/context/retrieval/lexical/_helpers.py); RETAIN |
| [Source indexing/search/scoped selection](../../src/devtools/context/retrieval/source/__init__.py); `build_source_search_index`, `search_repository_source` | FEATURE_ONLY | Source-search foundation; scoped source 28 | Native search/navigation consumes it; only caller-scoped search delta is feature-only, not a new ranker/index. [tests](../../tests/context/retrieval/source/test_scope.py); SELECTIVE_REVIEW |
| [Typed graph/PPR](../../src/devtools/context/retrieval/graph/__init__.py); `build_python_graph_view`, `rank_python_repository_resources` | MAIN_ADOPTED | Typed-view and graph ranking development | Map/native navigation and experimental graph consumers; completed harmful Graph3 does not retire bounded typed graph primitives. [tests](../../tests/context/retrieval/graph/test_ranking.py); RETAIN |
| [Repository-map ranking](../../src/devtools/context/retrieval/repository_map/__init__.py); `build_repository_map_view`, `rank_repository_map` | MAIN_ADOPTED | Diagnostic map baseline and bounded production ranking | Opt-in native navigation consumes canonical ranking; no native model map use demonstrated in 28. [tests](../../tests/context/retrieval/repository_map/test_ranking.py); RETAIN |
| [Retrieval composition/RRF](../../src/devtools/context/retrieval/composition.py); `compose_lexical_structural_resource_evidence` | MAIN_ADOPTED | Explicit rank composition, not heterogeneous ceiling policy | Caller composition joins lexical and structural evidence; no dense/vector production integration inferred. [tests](../../tests/context/retrieval/graph/test_ranking.py); RETAIN |
| [Planning/disclosure/materialization/assembly](../../src/devtools/context/planning/__init__.py); `plan_disclosures`, `materialize_disclosure_plan`, `render_context_disclosure` | FEATURE_ONLY | ADR0004 and concrete bounded adapters | Native worker, host progressive demonstration and RI source Context. Broader autonomous Context assessment/planner remains unimplemented. [tests](../../tests/context/planning/test_map_source.py); SELECTIVE_REVIEW |
| [Caller-selected map orientation/source](../../src/devtools/context/planning/repository_map.py); `choose_repository_map_disclosure`, `choose_repository_map_source_disclosure` | FEATURE_ONLY | Map-disclosure26 and map-source 27 Codex deliveries | apps/qwen/navigation.py calls existing factories; actual model selection is not inferred from adapter availability. [tests](../../tests/context/planning/test_map_source.py); SELECTIVE_REVIEW |
| [Obligation/readiness semantic kernel](../../src/devtools/context/localization/__init__.py); `assess_localization_readiness`, `generate_witness_hypotheses` | FEATURE_ONLY; MAINTAINED_NOT_CONSUMED; gap: complete maintained coding-agent witness/readiness loop | ADR0005 clean production slices and bounded case evidence | Internal RI/Localization chains and experimental callers; no complete maintained coding-agent witness-resolution loop. [tests](../../tests/context/localization/association/test_hypothesis.py); SELECTIVE_REVIEW |
| [Soft repository-role evidence](../../src/devtools/context/localization/roles/__init__.py); `derive_repository_role_evidence` | FEATURE_ONLY; MAINTAINED_NOT_CONSUMED; gap: complete native coding-agent role/readiness consumer, not internal role composition | Role/configuration integration; Qwen role-groups25 source | Dependency groups correctly classify project evidence. Consumer is existing role framework/tests, not automatic test planning or native witness acceptance. [tests](../../tests/context/localization/roles/helpers.py); SELECTIVE_REVIEW |
| [Task anchor grounding/generation](../../src/devtools/context/localization/generation/__init__.py); `ground_task_anchor`, `generate_witness_hypotheses` | MAIN_ADOPTED; MAINTAINED_NOT_CONSUMED; gap: complete native coding-agent obligation consumer; internal uses exist | Bounded Localization facts and experimental structural cases | Internal composition exists; native exact-edit grounding is a different application contract, not this obligation consumer. [tests](../../tests/context/localization/generation/test_branching.py); RETAIN |
| [Routing/association/resolution/promotion](../../src/devtools/context/localization/association/__init__.py); `route_localization_lexical_evidence`, `build_candidate_witness_view`, `promote_supported_hypothesis` | MAIN_ADOPTED; MAINTAINED_NOT_CONSUMED; gap: maintained automatic semantic decision adapter | Caller-directed Localization and semantic-resolution experiments | Explicit resolution recording/promotion, not an automatic model resolver. External decision adapter remains experiment-only. [tests](../../tests/context/localization/association/test_hypothesis.py); RETAIN |
| [Native bounded Qwen worker](../../apps/qwen/__init__.py); `run_coding_task`, `ContextTools` | FEATURE_ONLY | Historical qwen collection moved to maintained app; Engineering04-28 | Trusted local CLI/WorkCycle historical real runs; source admission and feedback tested. Recent full native map/check milestone remains unproven. [tests](../../tests/apps/qwen/conftest.py); SELECTIVE_REVIEW |
| [Shared all-checks/change freshness](../../apps/qwen/change_checks.py); `CodingCommands`, `check_changes`, `current_report` | FEATURE_ONLY | Codex check-bundle and change-check delivery | Real native25 BLOCKED and host27 PASS/currentness exist; no publishing authority. Not a framework-wide agent-independent installed service. [tests](../../tests/apps/qwen/test_change_checks.py); SELECTIVE_REVIEW |
| [Canonical Checkout/WorkCycle](../../scripts/backlog/__init__.py); `Checkout`, `WorkCycle` | FEATURE_ONLY | Single-checkout integration lifecycle; reviewed local publications | Native worker, trusted operator CLI and dashboard read consumer. Historical grants/refs do not transfer authority to main. [tests](../../tests/scripts/backlog/test_checkout.py); SELECTIVE_REVIEW |
| [Read-only operator console](../../apps/operator_dashboard/__init__.py); `main`, `DashboardServer` | FEATURE_ONLY | Operator-dashboard branch/adoption pilot and live console ledger | Loopback read-only CLI with explicit roots/raw-details flag; source consumes real receipts. Stale documented counts/coordinator cursor need qualification. [tests](../../tests/apps/operator_dashboard/test_native_history.py); SELECTIVE_REVIEW |
| [Identity coverage/evaluation utility](../../src/devtools/evaluation/__init__.py); `compare_identity_coverage` | MAIN_ADOPTED | Bounded expected/observed coverage primitive | Localization readiness calls it; not a general acceptance oracle or automatic sufficiency certification. [tests](../../tests/evaluation/test_coverage.py); RETAIN |
| [Model benchmark infrastructure](../../src/devtools/models/benchmarks/__init__.py); `run_vllm_benchmark` | MAIN_ADOPTED; NEEDS_SEMANTIC_REVIEW | Historical local serving benchmark | Experimental API with empty package exports; test/operator benchmark composition is not engineering-agent integration. [tests](../../tests/models/benchmarks/test_models.py); RETAIN |
| [Generic orchestration namespace](../../src/devtools/orchestration/__init__.py); namespace marker | INCOMPLETE_OR_BLOCKED; NEEDS_SEMANTIC_REVIEW | Taxonomy placeholder | Only namespace marker; experimental controller does not implement a reusable supported Agent/Run engine. No dedicated test scope found; not evidence of use; RETAIN_NAMESPACE_NO_FRAMEWORK_ENGINE |

The matrix overlaps package and narrow feature scopes intentionally (for example
repository/Delta and Localization/roles). Do not sum row counts. High-level
Localization readiness/witness generation/routing is maintained, but no complete
native coding-agent obligation-resolution consumer was found. Internal callers
are real consumers of its primitives, not evidence of an autonomous resolver.
UsageBudget has a real *experimental* orchestration consumer, not an established
app-wide standing policy. Regex splitting has no maintained direct non-test call
found. Model benchmarks have leaf experimental APIs with no broad package export;
that is not a model-neutral engineering runtime.

No supported integration with the separate Learned Intelligence repository was
established in this audit. Bounded Python search in src/apps/scripts found no
such imports/mentions. Its scientific catalogs were not traversed or conflated
with Devtools'35 collections.

## All historical collection dispositions

Reauthenticated 35 top-level `manifest.json` and `SUMMARY.md` pairs: 24 CLOSED,
nine INCOMPLETE, two BLOCKED. CLOSED is lifecycle termination, never a scientific
PASS or adoption grant. The companion binds every manifest/summary digest,
original source revisions where supplied, report fingerprints and packet checks.
The manifest closeout revision (`b0c88a9c` in many collections) is *not* an
accepted implementation identity. Individually frozen protocol/result/candidate
records retain authority; missing promotion links are not reconstructed.

For every row, original artifacts and reusable methods are KEEP. Their continued
custody does not authorize execution. Original source/analysis/README and
candidate files listed by the manifest are the identity-bearing authorities.
The scientific-outcome column is a qualified summary, not a replacement judgment.

| Collection / lifecycle | Scientific scope and outcome | Maintained relationship / adoption | Remaining obligation |
|---|---|---|---|
| [archive](../../experiments/archive/SUMMARY.md) / CLOSED | ADMINISTRATIVE: Twenty-two obsolete root reports were compacted; no new science. | SUPERSEDED: Original root representation superseded by exact Git/packet bytes; no runtime capability. | Retain root-to-packet mapping and originals in Git; no reopening or removal authority. |
| [bm25_sensitivity](../../experiments/bm25_sensitivity/SUMMARY.md) / CLOSED | MIXED: Case 0010: MIXED / NO SAFE REPLACEMENT. | EXPERIMENT_ONLY: Canonical lexical BM25 is main-adopted; this tuning policy was not promoted. | Preserve per-arm gains/losses; no default parameter change. |
| [bm25f](../../experiments/bm25f/SUMMARY.md) / CLOSED | NEGATIVE: Case 0015: R2 true BM25F COMPLETE / BM25F_HARMFUL under its frozen rule. | EXPERIMENT_ONLY: Experimental two-field scorer and controlled mechanics exist; no production BM25F promotion. | R2 is completed, not pending; preserve attribution and do not treat this outcome as veto of all fielding. |
| [codex_dogfood](../../experiments/codex_dogfood/SUMMARY.md) / INCOMPLETE | INCOMPLETE: Composite population with individual Stage D decisions and sealed/unfinished records; no collection-wide success. | INCOMPLETE_OR_BLOCKED: Many RI/Localization/model facts have separate maintained implementations; no blanket promotion from this collection. | Retain case-level candidate/result identities; consolidated per-case promotion joins remain UNKNOWN where not explicitly recorded. |
| [development_population](../../experiments/development_population/SUMMARY.md) / BLOCKED | BLOCKED: Shared population freeze/confirmation prerequisites remain blocked. | INCOMPLETE_OR_BLOCKED: Population custody supports research, not a maintained agent capability. | No confirmation entry, retry or grant inferred from stored code. |
| [exact_hint_routing](../../experiments/exact_hint_routing/SUMMARY.md) / CLOSED | BOUNDED_POSITIVE: Case 0012: EXACT_HINT_ROUTING_SUPPORTED within its declared surface. | EXPERIMENT_ONLY: Core grounding has related bounded facts; this experimental routing policy is not a native worker default. | Prospective generality and production policy remain separate. |
| [graph_ranking_baseline](../../experiments/graph_ranking_baseline/SUMMARY.md) / CLOSED | DIAGNOSTIC: Connectivity and ranking diagnostic; no complete-depth effectiveness claim. | EXPERIMENT_ONLY: Typed graph/PPR substrate exists on main; diagnostic ranking policy not automatically promoted. | Keep graph representation and ranking effectiveness separate. |
| [identifier_sparse](../../experiments/identifier_sparse/SUMMARY.md) / CLOSED | MIXED: Case 0009: RETAIN AS SEPARATE RETRIEVAL VIEW, unchanged required reach and mixed ranking effects. | EXPERIMENT_ONLY: Canonical main lexical analyzer still uses whole identifiers; experimental subtokens are not its default. | R1 and completed R2 remain separately attributable; no cross-repository generality established. |
| [import_relationship](../../experiments/import_relationship/SUMMARY.md) / INCOMPLETE | INCOMPLETE: No authenticated consolidated terminal outcome. | UNKNOWN: Main has bounded Python import relationships; a promotion link from this small comparison collection is not established. | Retain comparison substrate; do not infer accepted candidate from closeout revision. |
| [increment_25](../../experiments/increment_25/SUMMARY.md) / CLOSED | BOUNDED_POSITIVE: Imported-member development: 31 additions, 17 useful, five lexical escapes; original README also records completed 16-case frozen confirmation. | MAIN_ADOPTED: Bounded one-facade imported-member RI is maintained/main-adopted; original case judgments retain authority. | Generic closeout wording underspecifies the original confirmation: preserve both and use the specific original report, not a blanket all-confirmation-sealed claim. |
| [increment_26](../../experiments/increment_26/SUMMARY.md) / CLOSED | DIAGNOSTIC: CodeRankEmbed dense probe: 8 cases, 69 judged pairs, 40 dense-top5 pairs; bounded CPU replay. | EXPERIMENT_ONLY: Embedding adapter/attention-mask compatibility remains experimental; no production dense/vector retrieval. | Confirmation/generalization not established; do not infer dense retrieval disproved. |
| [increment_27](../../experiments/increment_27/SUMMARY.md) / CLOSED | MIXED: Lexical breadth/window/import probe: development useful totals 63 canonical, 68 identifier, 74 RRF; 31 path candidates. | EXPERIMENT_ONLY: Main retains canonical BM25 and explicit composition; tested alternative policies are not default selection. | Preserve dev/confirmation separation and candidate-volume controls. |
| [increment_28](../../experiments/increment_28/SUMMARY.md) / CLOSED | INCONCLUSIVE: Task-relative import-use annotation on fixed candidates; conditional incremental value not established. | EXPERIMENT_ONLY: Main static reference/import facts are related; this enrichment annotation is not automatic maintained selection. | No added candidate/coverage claim; keep fixed-surface limits. |
| [increment_29](../../experiments/increment_29/SUMMARY.md) / CLOSED | BOUNDED_POSITIVE: Direct References/Calls: 71 additions, 35 useful, four useful beyond lexical plus imports. | MAIN_ADOPTED: Clean typed References/Calls RI exists on main and feeds source index/relationships and Localization. | Qualified static evidence only; no runtime-call or universal retrieval guarantee. |
| [increment_30](../../experiments/increment_30/SUMMARY.md) / CLOSED | MIXED: Immediate package membership: 49 additions, 14 useful; no useful new item beyond preceding union. | MAIN_ADOPTED: Bounded package-membership facts exist on main; experimental selection policy not thereby accepted. | Retain useful structure without claiming independent fixed-K ranking benefit. |
| [increment_31](../../experiments/increment_31/SUMMARY.md) / CLOSED | MIXED: Mirrored paths: 34 additions, 21 useful; sole candidate outside earlier union not useful. | MAIN_ADOPTED: Bounded mirrored-path RI is on main and used internally by Localization roles/generation. | Path correspondence is not test execution, coverage or behavioral ownership. |
| [increment_32](../../experiments/increment_32/SUMMARY.md) / CLOSED | NEGATIVE: Graph1: 704 novel pairs; sampled128 contained two useful candidates. | EXPERIMENT_ONLY: Typed graph substrate is maintained/main-adopted; broad expansion policy is not. | Fanout and sample limits qualify the negative outcome. |
| [increment_33](../../experiments/increment_33/SUMMARY.md) / CLOSED | NEGATIVE: Graph2: 987 further novel pairs; zero useful in sampled128. | EXPERIMENT_ONLY: Second-depth expansion policy is not production; unsampled usefulness remains unknown. | Do not promote expansion or generalize sample labels to all pairs. |
| [increment_34](../../experiments/increment_34/SUMMARY.md) / CLOSED | DIAGNOSTIC: Structural union: 1916 pairs, 85 known useful, 1431 never adjudicated. | EXPERIMENT_ONLY: Consolidation/ceiling is a reproducible diagnostic, not executable selector. | Unjudged is not negative; no production union policy. |
| [increment_35](../../experiments/increment_35/SUMMARY.md) / CLOSED | DIAGNOSTIC: Heterogeneous union: 3922 pairs, 176 known useful, 3228 never adjudicated; 99 ceiling is nonexecutable. | EXPERIMENT_ONLY: Combines experimental evidence families, not a production ranker. | No automatic candidate-generation or sufficiency guarantee. |
| [increment_36](../../experiments/increment_36/SUMMARY.md) / CLOSED | MIXED: Simple lexical-RRF plus dense: 73 useful versus lexical74; no structural ranking contribution. | EXPERIMENT_ONLY: Main explicit RRF arithmetic is separate from this unpromoted fusion policy. | Retain control; do not claim evidence for heterogeneous structural score fusion. |
| [mechanism_routing](../../experiments/mechanism_routing/SUMMARY.md) / CLOSED | BOUNDED_POSITIVE: Case 0013: SELECTIVE_MECHANISM_ROUTING_SUPPORTED within the frozen surface. | EXPERIMENT_ONLY: No automatic native task/mechanism router adopted; caller-directed mechanisms exist. | Further production policy needs separate qualification. |
| [orchestration](../../experiments/orchestration/SUMMARY.md) / BLOCKED | BLOCKED: Historical checkout-bound execution contract conflicts with single-checkout operating policy. | INCOMPLETE_OR_BLOCKED: Startup/economics/worker measurement and usage constraints are reusable; controller stays experimental. | No generic framework Agent/Run engine or old-grant reuse; contract reconciliation required before execution. |
| [performance](../../experiments/performance/SUMMARY.md) / INCOMPLETE | INCOMPLETE: Profiling collection has no consolidated terminal scientific outcome. | EXPERIMENT_ONLY: Bounded benchmark/profiling helpers are reusable evidence infrastructure; not runtime retrieval policy. | Choose individual profiles by identity, not collection-wide PASS. |
| [purpose_relative_admission](../../experiments/purpose_relative_admission/SUMMARY.md) / INCOMPLETE | INCOMPLETE: No consolidated terminal outcome; retained reservation-v1 case has zero known-useful net gain. | EXPERIMENT_ONLY: Experimental admission policies are not universal Context/Selection authority. | Preserve useful loss/not-useful admission and original individual decisions. |
| [purpose_relative_import](../../experiments/purpose_relative_import/SUMMARY.md) / INCOMPLETE | INCOMPLETE: Bounded import-factor comparison lacks consolidated terminal judgment. | EXPERIMENT_ONLY: Production import facts do not imply adoption of task-relative import ranking. | No automatic retrieval claim. |
| [query_term_weighting](../../experiments/query_term_weighting/SUMMARY.md) / CLOSED | NEGATIVE: Case 0014: harmful tested term weighting. | EXPERIMENT_ONLY: No matching default production query weighting. | Keep negative result, not a universal prohibition on query representation work. |
| [qwen](../../experiments/qwen/SUMMARY.md) / CLOSED | MIXED: Original Markdown task accepted at `1122500`; Task02 repair budget failed; original checkpoint CLOSED. | FEATURE_ONLY: Reusable composition moved into apps/qwen; four legacy Python modules match main, 11 differ. Later application evaluations04-28 are not35 additional collections. | Native uninterrupted map/check engineering remains unproven; accepted source and failed live receipts remain distinct. |
| [repository_map_baseline](../../experiments/repository_map_baseline/SUMMARY.md) / CLOSED | DIAGNOSTIC: Original map diagnostic, not prospective general retrieval-effectiveness evidence. | MAIN_ADOPTED: Canonical typed map/ranking is on main; later map/source Planning and native adapter are feature-only. | Caller-directed use is supported; no automatic ranking-effectiveness claim. |
| [retrieval_diagnostics](../../experiments/retrieval_diagnostics/SUMMARY.md) / INCOMPLETE | INCOMPLETE: No authenticated consolidated terminal outcome. | EXPERIMENT_ONLY: Attribution/diagnostic adapters are reusable research code, not production selector. | Individual case evidence retains authority. |
| [source_grounding](../../experiments/source_grounding/SUMMARY.md) / INCOMPLETE | INCOMPLETE: Candidate08 C22 stopped before entry on CLI-preflight log collision; dead predecessors stay dead. | INCOMPLETE_OR_BLOCKED: Frozen grounding controller and 13 forensics retained; current native exact-edit observations are a different application contract. | No replay/redispatch or promotion from restored packets; historical grants stale. |
| [structural_discrimination](../../experiments/structural_discrimination/SUMMARY.md) / INCOMPLETE | INCOMPLETE: Cases17-19 and annotations retain individual stages, no whole-collection conclusion. | EXPERIMENT_ONLY: Uses maintained/main RI and Localization; no fitted discriminator/ranker promoted. | Unresolved label/confirmation/sufficiency questions remain. |
| [task_conditioned_graph](../../experiments/task_conditioned_graph/SUMMARY.md) / CLOSED | NEGATIVE: Case 0016 GRAPH_HARMFUL: Graph3 broad fusion regressed; all 37 B-only occurrences were unnecessary under their own obligations. | EXPERIMENT_ONLY: Graph facts/ranking primitives remain maintained/main; tested automatic expansion policy not adopted. | Negative policy result does not retire all bounded graph navigation. |
| [typed_graph_baseline](../../experiments/typed_graph_baseline/SUMMARY.md) / CLOSED | DIAGNOSTIC: Typed-view development diagnostic; not prospective task effectiveness. | MAIN_ADOPTED: Typed RI graph view is maintained/main-adopted and supports map/source consumers. | Retain qualification and no runtime-import inference. |
| [worker_story](../../experiments/worker_story/SUMMARY.md) / INCOMPLETE | INCOMPLETE: Only small result/probe inventory; no consolidated terminal outcome authenticated. | UNKNOWN: WorkCycle later exists, but this collection-to-production promotion relationship is not proved. | Keep source and result; do not label WorkCycle a successful promotion from matching topic names. |

Increment25's original README/confirmation files are more specific than the
generic closeout phrase about development-only checkpoints. This audit does
not rewrite either: it records the original 16-case frozen confirmation and
keeps its bounded conclusion. Later app evaluations04-28 are application
development receipts under the Qwen lineage, not additional top-level experiment
collections. Env13's accepted model implementation/publication, 25's correct
Qwen role source with a BLOCKED live check, 27's no-edit original run and 28's
failed implementation/Codex fallback remain separately classified. No recent
uninterrupted native map/check success is invented.

Useful but incompletely integrated machinery includes the orchestration startup/
economics/measurement controller, source-grounding capture/evaluation chain,
dense probe, retrieval diagnostics and semantic resolution adapter. These do
not become framework execution policy merely because their outputs are useful.
Bounded import/reference/membership/mirrored-path facts did become maintained
RI; their promotion does not adopt the experiments' broad expansion/ranking
policies. Negative Graph1/2/3 results qualify policies, not all graph navigation.

## Selective protected-main adoption plan

These are *proposed destination review packets*, not validated integrations.
No cherry-pick/merge is performed. The companion enumerates exact seed changes,
source/test scope, public initializer/deferred-import closure, differing existing
dependencies, destination-preserved dependencies, docs and configuration review.
The closure is deliberately conservative: importing a package initializer can
pull unrelated exports, so it is not a copy list or proof that every dependency
must change. In particular Context's feature initializer adds Delta exports;
map/source adoption can retain compatible main exports rather than importing
Delta incidentally. Fresh destination execution must resolve this upper bound.

| Group / status | Exact changed production seeds | Dependencies, compatibility and exclusion |
|---|---|---|
| G1 Identity/BSD/optional regex / READY_FOR_DESTINATION_REVIEW | [core/identity/models.py](../../src/devtools/core/identity/models.py)<br>[core/regex/__init__.py](../../src/devtools/core/regex/__init__.py)<br>[core/regex/splitting.py](../../src/devtools/core/regex/splitting.py)<br>[core/system/detection.py](../../src/devtools/core/system/detection.py)<br>[core/system/models.py](../../src/devtools/core/system/models.py) | Depends: existing main baseline. Three independent semantic slices; split commits; regex has no non-test consumer and is optional. |
| G2 Filesystem binary/bounded read/finite JSON / READY_FOR_DESTINATION_REVIEW | [resources/filesystem/__init__.py](../../src/devtools/resources/filesystem/__init__.py)<br>[resources/filesystem/codecs/__init__.py](../../src/devtools/resources/filesystem/codecs/__init__.py)<br>[resources/filesystem/codecs/binary.py](../../src/devtools/resources/filesystem/codecs/binary.py)<br>[resources/filesystem/codecs/json.py](../../src/devtools/resources/filesystem/codecs/json.py)<br>[resources/filesystem/reading.py](../../src/devtools/resources/filesystem/reading.py)<br>[resources/filesystem/resolution.py](../../src/devtools/resources/filesystem/resolution.py)<br>[resources/filesystem/writing.py](../../src/devtools/resources/filesystem/writing.py) | Depends: G1 optional hardening. Preserve atomic write/read/decoder errors; B-0048 Python3.12 constructor question is separate; qualify supported versions in destination. |
| G3 Native model messages/provider/capture / READY_FOR_DESTINATION_REVIEW | [context/planning/rendering.py](../../src/devtools/context/planning/rendering.py)<br>[context/python/function/qualified_reference.py](../../src/devtools/context/python/function/qualified_reference.py)<br>[context/python/function/request_assembly.py](../../src/devtools/context/python/function/request_assembly.py)<br>[models/interaction/__init__.py](../../src/devtools/models/interaction/__init__.py)<br>[models/interaction/prompt.py](../../src/devtools/models/interaction/prompt.py)<br>[models/interaction/providers/llama_cpp.py](../../src/devtools/models/interaction/providers/llama_cpp.py)<br>[models/interaction/providers/llama_cpp_request_settings.py](../../src/devtools/models/interaction/providers/llama_cpp_request_settings.py)<br>[observability/evidence/model_interaction.py](../../src/devtools/observability/evidence/model_interaction.py) | Depends: existing main baseline. Structured history serialization, Tool IDs, request validation, per-category argument capture and text-only assembly guards travel together. |
| G4 Configuration obstruction/static groups/role consumer / READY_FOR_DESTINATION_REVIEW | [context/localization/roles/configuration.py](../../src/devtools/context/localization/roles/configuration.py)<br>[context/localization/roles/models.py](../../src/devtools/context/localization/roles/models.py)<br>[context/python/project_configuration/declarations.py](../../src/devtools/context/python/project_configuration/declarations.py)<br>[context/python/project_configuration/models.py](../../src/devtools/context/python/project_configuration/models.py)<br>[context/python/project_configuration/settings.py](../../src/devtools/context/python/project_configuration/settings.py) | Depends: existing main baseline. Three configuration files and two role files differ; retain qualified unsupported/absence, identities/derivation and valid siblings. No native resolver implied. |
| G5 Caller-directed map/source and scoped discovery / READY_FOR_DESTINATION_REVIEW | [context/planning/__init__.py](../../src/devtools/context/planning/__init__.py)<br>[context/planning/rendering.py](../../src/devtools/context/planning/rendering.py)<br>[context/planning/repository_map.py](../../src/devtools/context/planning/repository_map.py)<br>[context/repository/discovery.py](../../src/devtools/context/repository/discovery.py)<br>[context/retrieval/source/search.py](../../src/devtools/context/retrieval/source/search.py) | Depends: G3 guards when native messages supported. Select map factory/export/render guard, search scope and explicit discovery only; Delta exports in context root are not needed by this behavior. |
| G6 SnapshotDelta export/value / BLOCKED_CONSUMER_DECISION | [context/__init__.py](../../src/devtools/context/__init__.py)<br>[context/repository/__init__.py](../../src/devtools/context/repository/__init__.py)<br>[context/repository/changes.py](../../src/devtools/context/repository/changes.py) | Depends: existing main baseline. No maintained non-test consumer found. Define one bounded consumer before treating this as integration/maintenance completion; no incremental cache engine. |
| G7 Native worker/shared checks/Checkout WorkCycle / BLOCKED_RELIABILITY_AND_AUTHORITY_REVIEW | [apps/qwen/api_contracts.py](../../apps/qwen/api_contracts.py)<br>[apps/qwen/change_checks.py](../../apps/qwen/change_checks.py)<br>[apps/qwen/coding_loop.py](../../apps/qwen/coding_loop.py)<br>[apps/qwen/commands.py](../../apps/qwen/commands.py)<br>[apps/qwen/context_tools.py](../../apps/qwen/context_tools.py)<br>[apps/qwen/continuation.py](../../apps/qwen/continuation.py)<br>[apps/qwen/development_task.py](../../apps/qwen/development_task.py)<br>[apps/qwen/edits.py](../../apps/qwen/edits.py)<br>[apps/qwen/navigation.py](../../apps/qwen/navigation.py)<br>[apps/qwen/patch_proposal_worker.py](../../apps/qwen/patch_proposal_worker.py)<br>[apps/qwen/tasks.py](../../apps/qwen/tasks.py)<br>[scripts/backlog/__init__.py](../../scripts/backlog/__init__.py)<br>[scripts/backlog/__main__.py](../../scripts/backlog/__main__.py)<br>[scripts/backlog/checkout.py](../../scripts/backlog/checkout.py)<br>[scripts/backlog/coordinator.py](../../scripts/backlog/coordinator.py)<br>[scripts/backlog/delegation.py](../../scripts/backlog/delegation.py)<br>[scripts/backlog/intake.py](../../scripts/backlog/intake.py)<br>[scripts/backlog/integration/__init__.py](../../scripts/backlog/integration/__init__.py)<br>[scripts/backlog/integration/authority.py](../../scripts/backlog/integration/authority.py)<br>[scripts/backlog/integration/cli.py](../../scripts/backlog/integration/cli.py)<br>[scripts/backlog/integration/git.py](../../scripts/backlog/integration/git.py)<br>[scripts/backlog/integration/lifecycle.py](../../scripts/backlog/integration/lifecycle.py)<br>[scripts/backlog/integration/local.py](../../scripts/backlog/integration/local.py)<br>[scripts/backlog/integration/validation.py](../../scripts/backlog/integration/validation.py)<br>[scripts/backlog/work.py](../../scripts/backlog/work.py)<br>[scripts/qwen/coding_worker.py](../../scripts/qwen/coding_worker.py)<br>[scripts/qwen/llama_cpp_profile.py](../../scripts/qwen/llama_cpp_profile.py)<br>[scripts/qwen/patch_proposal_worker_acceptance.py](../../scripts/qwen/patch_proposal_worker_acceptance.py) | Depends: G2, G3, G5. Coupled application/task/check/admin contracts; exact-tree reuse investigation first. New root config/coordinator/grants are not imported. No old plans, archives or research ancestry. |
| G8 Read-only dashboard / BLOCKED_G7_AND_DISCLOSURE_REVIEW | [apps/operator_dashboard/__init__.py](../../apps/operator_dashboard/__init__.py)<br>[apps/operator_dashboard/details.py](../../apps/operator_dashboard/details.py)<br>[apps/operator_dashboard/project.py](../../apps/operator_dashboard/project.py)<br>[apps/operator_dashboard/server.py](../../apps/operator_dashboard/server.py) | Depends: G7. Include web source/config/package-lock/UPSTREAM/license docs, exclude node_modules/dist/runtime data. Review explicit roots/raw-details and stale startup prose. |

G1's three changes are independently reviewable, not one mandatory bundle.
G2/G3/G4/G5 are ready to *prepare destination-specific reviews* because bounded
APIs and permanent regressions exist; this audit does not claim main compatibility
has been executed. G3/G5 share a rendering guard: adopt it once, review native
message semantics together. G6 is low priority until a real bounded consumer is
specified. G7/G8 remain blocked on the listed reliability/authority/privacy work.

For each packet:

1. Authenticate current main (which may advance), select an ordinary main-derived
   branch in this checkout and preserve the destination-only Commands regression/doc.
   Enumerate actual required hunks, exports, dependencies and tests again.
2. Review package docs plus `pyproject.toml`, `uv.lock`, `.gitattributes`, supported
   Python/tool versions and external dependencies; root files are review inputs,
   never permission to import all feature configuration. Current feature/main
   configuration identities are in the companion. Preserve error contracts,
   frozen values, source representations and capture policy.
3. G1/G2 need core/real filesystem boundary regressions (including binary bytes,
   hard read bounds, decoder/error behavior and finite JSON); B-0048 remains a
   separate Python3.12 issue. G3 needs real provider request/response fixtures,
   Tool correlation/capture and text-only rejection tests. No live inference is
   implied. G4 needs obstruction/unsupported/absence/static-group/role-provenance
   fixtures; no dependency installation or role inference from group names.
4. G5 needs retained snapshot/map membership/UTF-8/CRLF/no-final-newline,
   unauthorized/stale reference, exact source, mixed rendering and scoped-query
   compatibility tests. Keep existing main graph/map/source APIs. No automatic
   ranking, source parser or whole-repository prompt expansion.
5. G7 needs existing native-loop, exact byte application/refusal, source-bound
   checks, freshness, interrupted Checkout/recovery and commit/push uncertainty
   tests. Review application/admin import coupling and concrete authorization at
   the destination. Never copy `.local/backlog` grants, original coordinator paths,
   research receipts, frozen tasks or old refs into fresh authority. G8 additionally
   includes exact web source/config/lockfile/license inventory from the companion,
   read-only loopback routes, explicit roots/raw-detail disclosure and dependency
   supply-chain review. Exclude node_modules/dist/runtime data and stale counts.
6. Independently review the final diff; run focused executable regressions,
   scoped Ruff/formatting/strict typing/layout/whitespace and the protected gate
   at 100% required production branch coverage on that exact destination candidate.
   A feature gate is supporting history, not substitute evidence. Use current
   authorization/review/promotion; do not merge unrelated ancestry.

## Cohesion and representative control/data flows

| Flow / owners | Cohesive boundary already present | Actual pressure, not automatic redesign |
|---|---|---|
| Task to model: CodingTask → coding_loop → ModelInteraction/llama.cpp | Task scopes, fixed budgets/plan; native Prompt/provider normalization | Native loop owns orchestration; Runtime remains one invocation. No generic Agent base justified by parallel names |
| Response to Tool: normalized calls → descriptor/ToolRunner → ContextTools/CodingCommands | Call IDs, validation-before-execution and managed Commands; availability is not authority | Domain schemas/dispatch/presentation repeated in two app owners; existing normalize_tool_descriptor already shared |
| Discovery to Context: snapshot → RI/source index/graph/map → Planning → model Prompt | Retained identity and caller-selected disclosures; orientation distinct from exact source | Native navigation exists but28 did not use it; no measured retrieval-effectiveness improvement from API availability |
| Exact observation to edit: source disclosure/version → edit grounding/admission → Git patch/Checkout | Map alone never grants edit authority; exact atomic source/absence and byte bounds preserved | Admission/application/validation are separate outcomes. Narrow refused-component diagnostics already delivered; no fuzzy cross-file repair |
| Candidate to validation: CodingCommands → run_check(all) → check_changes → is_current | Single command execution path, source/plan/Git/report evidence and stale rejection | Host is_current output lacks durable input digest/time in selected 27 record; not a success cache or approval |
| Validation to publication: Checkout → WorkCycle local closeout → independent review → commit/push | Separate authority, sealed review subject, canonical source restoration | Protected-gate reuse/input closure and post-push observation need bounded investigation; no bypass asserted |
| Activity to observation: Model/terminal Evidence, InvocationMeasurement, Command events, native receipts | Evidence/events/usage/correlation/durability remain different responsibilities | Inspectors not composed into native worker; usage/failure population and joins lack one maintained consumer |
| Experiment to software: original protocol/candidate → reviewed source/tests → main-derived review | Bounded facts can promote separately from experimental policies | Closeout revision/status/topic similarity cannot establish accepted implementation or consumer lineage |

Current dependency direction is intact in the inspected Python sources: framework
does not import apps/scripts/experiments. Applications/admin do have coupling:
WorkCycle consumes CodingTask and application validation helpers; native loop
imports private development-task helpers; deferred imports avoid concrete cycles.
This is a real packaging/review cost, not permission to move application policy
into Runtime or ToolRunner. Snapshot identities describe observed repository
content, not execution occurrences or exactly-once effects.

### Large Qwen owners: responsibility audit

The companion fingerprints/locates all functions; line counts below are a source
snapshot, not a style threshold. Existing navigation and change-check helpers
have already been extracted; do not propose duplicate owners.

| Current owner | Distinct current responsibilities | Qualified regrouping investigation |
|---|---|---|
| context_tools.py, 913 lines | Source/read corpus and observations, Tool schemas/dispatch, Context navigation, exact edit admission; accept_transaction 104 lines | Keep observation/admission authority cohesive. Examine descriptor/presentation extraction shared with CodingCommands; navigation.py already owns map adapter |
| coding_loop.py, 1620 lines; _turns 922 | History/Context capacity, provider turns, Tool batches, proposal admission/application, validation/feedback and accepted completion; run_coding_task 315 | Test observable loop transitions and cancellation first; separate bounded presentation or candidate-check coordination only where semantics remain exact |
| development_task.py, 1439 lines | Legacy/structured task freeze and probes, check commands, hashes/evidence, patch generation; shared private helpers used by loop/admin | Distinguish supported fixed-check/patch substrate from historical task-driver composition. Existing consumers/durable schemas determine a cohesive package, not repeated filename prefixes |

These files exceed the current 32768-byte single candidate/closeout source limit;
their exact physical sizes are recorded. The existing module-feasibility proposal
owns that maintenance pressure. Splitting merely to evade limits or broadening
admission is not authorized. A future extraction needs import/API/schema tests,
unchanged refusal/restoration/cancellation, and two actual callers where shared.

## Developer experience and reusable-definition candidates

| Repeated responsibility / real consumers | Minimal interface direction | Semantic obligations and disposition |
|---|---|---|
| ContextTools and CodingCommands schema/descriptor/argument/presentation declarations | Investigate typed helper/composition over existing ToolDefinition/ToolRunner; reuse normalize_tool_descriptor | Preserve domain-specific validation, IDs, permission checks, output bounds and primary exceptions; no new registry/decorator or execution layer selected. B-0035/B-0003 |
| Native loop and WorkCycle check/status/evidence coordination | Reuse delivered run_check(all)/change checks; expose a bounded stable application module only if dependencies justify | Do not merge fixed task validation, protected gate and independent publication. Input-closure/reuse investigation comes first; B-0047/B-0028 |
| development_task._save, WorkCycle sealed save/progress, check bounded view, usage snapshot writer | Extract only proven identical low-level mechanics; retain separate representations | Stable seals vs mutable journals vs bounded views vs versioned usage differ. Repeated JSON/hash syntax is not a universal serializer; B-0027/module proposal |
| Native check report and host freshness, WorkCycle publication observation | Small explicit record adapters/consumers before a tracing API | Add task/call/candidate/report/review/remote links with capture policy and time; no logging base class or EventBus. B-0023/B-0011/B-0018/B-0034 |
| Qwen native tests and WorkCycle integration tests | Qualify tiny independently authored Git/task fixtures and reusable assertions | Never copy Devtools source trees, import sealed outcome tests, weaken exact Git/source IDs or hide platform failures. B-0003/B-0015 |
| ModelInteraction provider settings and native profile/descriptor setup | Preserve explicit capability/config values and validated requests | Provider semantics, external Codex Agent and fixed-policy execution are distinct; no universal ModelAdapter from similar syntax. B-0046/B-0029 |
| Native exact-edit proposals and structured diagnostics | Investigate smaller model-facing expression only over identical host admission | Keep exact observation/version/absence, 4096 region/8192 aggregate/16384 patch limits, all-or-nothing semantics; no Aider-style tolerant/cross-file/partial edits. Existing edit-ergonomics proposal |

No base class or decorator is justified by module length. Reuse canonical
Commands, filesystem, paths, time and identity substrates. Existing Tool schema
normalization and source identity owners should be extended rather than competed
with. Dashboard's historical counts/coordinator cursor need documentation
qualification, not a new dynamic authority service.

## Observability adoption and prioritized maintenance

The [executed five-flow audit](development-lifecycle-observability-audit.md)
remains authoritative for authenticated historical joins. Its297 fingerprints,
21 original inputs, selected validation logs and five timelines are preserved;
this checkpoint adds source/adoption/custody context, not reconstructed events.
Optional terminal/model inspectors, immutable Evidence, live lossy Command events,
measured usage and durable native/WorkCycle receipts serve different purposes.
Usage ingestion has real CLI/controller consumers; universal tracing/export and
durable Evidence consumers are not established by those exports.

**Priority1: bounded exact-tree validation reuse/input-closure investigation.**
`scripts/backlog/integration/local.py` derives review_subject from result/base/files
and reuses a prior passed protected result when the subject matches. Other
task/baseline/Checkout checks still apply. The reuse condition does not separately
name full plan/config/toolchain closure. Determine the actual validated inputs,
including relevant read/test/config/runner/environment identities, and test
changed-input negative cases before strengthening reuse claims. This is a
source-supported question, **not evidence of a historical validation bypass**.
No unsafe publication or coverage waiver was established. B-0047's implemented
profile remains valid; its broader reuse/evidence question is a separate pending
bounded investigation, related to B-0028/B-0011/B-0027.

| Priority / classification | Evidence and consequence | Existing owner / acceptance direction | Architecture / maintenance-agent fit |
|---|---|---|---|
| P1 RESEARCH / operational reliability | Reuse subject omits separately named plan/config/toolchain closure; stale evidence could be misinterpreted | New pending investigation linked to B-0047; inventory closure, mutate each relevant input, prove reject/revalidate, unchanged-tree reuse once | Decision only if closure ownership changes; deterministic follow-up suitable after qualification |
| P1 BUG investigation / failure accounting | Provider normalization precedes observer; failed realization and post-success observer error have different facts | B-0046/B-0023; preserve actual response/usage/unknown effects and primary exception, no blind retry | Contract decision possible; bounded tests then maintenance implementation |
| P1 INTEGRATION / occurrence joins | Native task/model/Tool/check/review/publication have local keys but no maintained end-to-end consumer | B-0023/B-0011/B-0018; join existing receipts with explicit unknown/inferred edges and capture policy | Reuse records first; no Trace/EventBus dependency decision now |
| P1 MAINTENANCE / freshness and push | Host freshness result lacks input/time binding; closeout lacks separately observed post-push ref/time | B-0011/B-0034 and checks/WorkCycle; bind report identity/time and remote observation without implying rollback | Bounded maintenance after uncertain-effect semantics agreed |
| P2 INTEGRATION / bounded libraries | G1-G5 useful reviewed feature deltas missing main | B-0006/B-0002 plus existing filesystem proposals; exact destination packets and gate | No blanket merge; destination-authorized work suitable for agent assistance |
| P2 MAINTENANCE / cohesion | Three app owners exceed candidate-size limits and cross-import private helpers | Existing module proposal/B-0003; responsibility boundaries, feasible exact edits and compatibility tests | Investigation first, no mechanical split or new framework layer |
| P2 DOCUMENTATION / custody | Dashboard stale counts; qwen overview evolved since archived snapshot; generic25 summary less specific | B-0006/custody; current-status navigation and versioned provenance, preserve frozen originals | Safe documentation task; never rewrite science |
| P2 CLEANUP / operational | Eight residuals verified against packet manifests but shared SSD and denied regions remain | Existing custody proposal; exact allowlist/dependency/process/off-volume decision before removal | Maintenance-agent dry-run only until separate authority |
| P3 ENHANCEMENT / ergonomics | Two real Tool declaration owners; serializer syntax with differing semantics | B-0035/B-0027, module and edit-ergonomics proposals; compare two callers before helper | Optional; composition/extraction before decorators/base classes |
| P3 FEATURE / consumer | Delta unconsumed; full Localization/semantic-resolution agent consumer not delivered | B-0002/B-0009, existing CodeGraph/Memory research; one bounded consumer with evidence | Requires defined objective; not generic incremental engine or more experiment recycling |

No statuses, B-numbers, parents, grants or approvals change. Classifications above
map to the existing intake schema (`bug`, `enhancement`, `refactor`,
`investigation`), not new enum values. Advisory reviews/evidence appendices keep
existing records authoritative. The companion records exact new/review IDs.

## Custody, hygiene and bounded cleanup result

The [extended custody inventory](../development/artifact-custody-inventory.md)
and companion record exact paths, measured bytes, member hashes and denied
regions. All 24 CLOSED collection packet hashes/members authenticate without
extraction. The general checkout packet's 1638 members match its preservation
manifest. Seven ordinary residuals match the general packet; the16 legacy
target members match their separate manifest/packet and surviving bytes.
These are same-SSD recovery copies, not off-volume backup or a fresh restore test.

Current collection-file rehashing was capped at 64MiB per collection: 1073 EXACT,
5697 NOT_REHASHED within that bound, 22 expected compacted root-report absences,
one current-byte difference. The latter is `experiments/qwen/docs/overview.md`:
later app documentation was appended after its frozen manifest; the archived
original is exact. Do not overwrite current history or alter the old hash to
erase that distinction. No claim that all current scientific payload bytes were
freshly rehashed is made. The companion retains individual exceptions.

Generated caches have measured byte totals, but active node/python processes
have unqualified ownership. Cache candidates are future exact-path review,
not proof of idleness. Denied preserved-root/quarantine regions remain HOLD;
no ACL/ownership change or junction traversal occurred. Former worktree/deployment
targets remain absent; nested authored Git fixtures remain evidence, not Devtools
clones. Zero paths/bytes were removed. No source copy, backup repository or new
preservation archive was created.

## Prioritized roadmap and successor-session boundary

1. **Next checkpoint: comprehensive successor-session handoff.** Summarize actual
   branch/main/source/evidence/backlog state, this report and the earlier four-
   project/five-flow findings, exact next authorization boundaries and unresolved
   questions. Do not launch another open-ended audit or implementation now.
2. After a separate assignment, qualify protected validation reuse closure and
   failure/uncertain-effect observation. Review G1-G5 on actual current main,
   independently, preserving Commands. Do not wait for a generic tracing design
   to adopt a small coherent library slice, or bypass G7 authority checks.
3. Resolve native app module feasibility, maintained receipt consumers and G7
   destination authority/recovery before broad worker/dashboard adoption.
4. Choose one real bounded RI/Context consumer only after those decisions. Delta,
   Localization sufficiency and model map use remain explicit missing consumers;
   completed R1/R2/GRAPH-3 verdicts and sealed obligations retain their own
   roadmap authority. The completed performance baseline's maintainer review and
   highest-priority measured bottleneck precede further effectiveness work;
   neither is executed here.
5. Perform future custody cleanup only on separately qualified exact paths with
   independent recovery requirements; retain evidence and uncertainty.

## Limitations and checkpoint validation

This is source-level reconciliation, not a new runtime trace, destination gate,
scientific adjudication or proof of every historical case's promotion. The 35
collections all have explicit dispositions, but some candidate-to-production
links remain UNKNOWN. Static closure is an upper bound; transitive signatures,
configuration and side effects require real destination review. Unreadable areas,
bounded large-payload rehashing and same-SSD archives limit custody conclusions.
No external Learned Intelligence catalog, model cache or live service was touched.

Documentation/link/JSON/layout and canonical intake/hash-chain validation are
recorded with exact changed paths in the companion and local completion record.
Production source/tests/apps/scripts/experiments are unchanged; no protected
production gate is required or claimed for this documentation checkpoint.

## Canonical backlog intake result

One [reuse/input-closure investigation](../backlog/proposals/d58697fd-bb03-4e98-bdac-fa29444fc6ff/proposal.json)
is PENDING_REVIEW under B-0047. The original 17 states/payloads/chains remain
unchanged; four existing pending proposals received ADVISORY evidence only:

- [39c6663a-bab7-43ed-8166-82e780a75d05](../backlog/proposals/39c6663a-bab7-43ed-8166-82e780a75d05/proposal.json).
- [0385a359-399f-40bb-aed4-caf5239c9fc8](../backlog/proposals/0385a359-399f-40bb-aed4-caf5239c9fc8/proposal.json).
- [88246171-d102-4b62-93d7-03c1e19f8a7b](../backlog/proposals/88246171-d102-4b62-93d7-03c1e19f8a7b/proposal.json).
- [ae03cda7-955e-40c6-a131-9e2ba209c9a6](../backlog/proposals/ae03cda7-955e-40c6-a131-9e2ba209c9a6/proposal.json).

Queue after capture: 18 total, 17 PENDING_REVIEW and one existing APPROVED.
No B-number, grant, approval or canonical item status changed.

## Executed checkpoint checks

The documentation checkpoint validated 215 new local links/anchors and seven
changed/new JSON documents. All 513 selected source/test physical identities,
35 manifest/summary pairs, 342 original report fingerprints, 343 CLOSED packet
members, 297 earlier lifecycle files and 13 original forensics authenticate.
The general checkout packet's 1638 members and separate legacy packet's 16
members match their manifests; seven ordinary residual directories match the
general preservation packet. Large current collections retain the explicit
64MiB rehash bound and unknown/changed distinctions described above.

`uv run python scripts/validate_layout.py` passed. The existing focused
`uv run pytest --no-cov tests/scripts/test_validate_layout.py tests/scripts/backlog/test_intake.py -q`
passed 36 tests in 2.00s. Canonical intake reports 18 valid chains, 17 pending and
one previously approved, with all original 17 states/payloads/reviews preserved.
Git whitespace validation passes. Exact modified/new paths are listed in the
companion's checkpoint_validation record. No production source/test, original
experiment or earlier research-evidence changes; no inference/replay/protected
gate, main mutation or deletion occurred. Publication identity is recorded in
the Git commit and ignored final handoffs rather than a self-referential hash.
