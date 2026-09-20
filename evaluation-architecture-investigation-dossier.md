# Evaluation architecture investigation dossier

## A. Baseline

Investigation date: 2026-09-18. This is a repository-grounded, read-only architectural investigation, with this dossier as its sole authorized filesystem output. It is research, not an accepted decision, implementation authorization, or amendment of the roadmap.

| Baseline fact | Observed value |
|---|---|
| Branch | main |
| HEAD | b6561ca2672822ceaed3f70edc82d3187e5d8e3a |
| Tracked working tree | Clean; no unstaged tracked diff |
| Index | No staged changes; cached diff empty |
| Initial diff checks | git diff --check and git diff --cached --check both clean |
| Existing dossier at this investigation's target | Absent |
| Files captured in the initial integrity manifest | 339 tracked files and five non-ignored untracked files |
| Initial index SHA-256 | 50BB1E5AF54AED7BA85C2BB3690D1C2426182300BA8CCA11E70BC388F3220223 |

The complete original porcelain status was:

    ?? .qwen-selection-stress-bounded-live-report.json
    ?? .qwen-selection-stress-live-report.json
    ?? .qwen-selection-stress-termination-live-report.json
    ?? .qwen-selection-stress-thinking-disabled-live-report.json
    ?? architecture-archaeology-dossier.md

These artifacts belonged to the pre-existing workspace. Their content hashes and lengths were recorded before investigation:

| Path | Bytes | SHA-256 |
|---|---:|---|
| .qwen-selection-stress-bounded-live-report.json | 5721 | 35251ED0546424ACF7D7F93C48C0A84B8D3E8804AE044A0595C6B507D26A407B |
| .qwen-selection-stress-live-report.json | 5699 | 7BA8C6A14A69F67652AB9F4728FAA1D45D25DF6726E4483563F12DE90BEF5743 |
| .qwen-selection-stress-termination-live-report.json | 5806 | 8F2CD99BA5DC09C76D5095DDA468B74F14B992E0B095007743B3B37BF25F2287 |
| .qwen-selection-stress-thinking-disabled-live-report.json | 7361 | B13C02A6F8E5C83AD1C2052699B8441B11FDE43E9999B54E09DE543FCA2F11C0 |
| architecture-archaeology-dossier.md | 108411 | C963E79E1F762C854176B7CB12E021F6AAA240814B543770742B7366CE2FA9B9 |

The accepted ADR set consists of exactly the four decision files present in docs/architecture/decisions:

| Decision | Status/date | Implementation status established by current documentation and inspection |
|---|---|---|
| ADR-0001 — Cohesive ModelInteraction boundary | Accepted; 2026-09-15 | All three scoped phases are reported implemented. Request, observation, serving-provenance, and native Tool values exist. The breadth of that completion claim exceeds some actual Evidence fields and failure observation; see AM-I1 and AM-I2. |
| ADR-0002 — Repository intelligence identity and derivation semantics | Accepted; 2026-09-16 | Semantic architecture only; no production repository-intelligence substrate |
| ADR-0003 — InformationNeed, retrieval evidence, and ranking semantics | Accepted; 2026-09-16 | Semantic architecture only; no production retriever/ranker |
| ADR-0004 — Context disclosure planning and model-input assembly semantics | Accepted; 2026-09-16 | Semantic architecture only; no production disclosure compiler/materializer/assembler |

B-0002 is BACKLOG, decision_maturity READY_FOR_DESIGN, necessity REQUIRED, architectural_significance STRUCTURAL, urgency SOON, validation_level NONE. Its primary domain is context. It has no hard or pressure dependencies; operational dependencies are resources filesystem, core paths, and core regex. Its promotion trigger is an independently useful bounded semantic slice ready for design without collapsing domain ownership.

The roadmap still records an unclosed architecture-review gate: completion of integrated evaluation research and reconciliation of accepted findings precede implementation design becoming the primary activity. This dossier does not close that gate or change B-0002. The user's request explicitly asks about starting slices before later external confirmation; the assessment in AP/AU concerns architectural safety, separately from project sequencing and authorization.

## B. Evidence inspected

### Method and evidence categories

Repository evidence was reconstructed in authority order: AGENTS.md; taxonomy and documentation map; current architecture and accepted ADRs; relevant package documentation, source, and tests; backlog and roadmap; experimental and historical material. Broad rg searches covered all terms requested in the investigation across docs, src, tests, experiments, and scripts. Searches for concrete definitions then checked whether named architectural concepts actually have implementations.

The following labels distinguish claims throughout:

- **Evidence:** directly inspected repository text, code, test assertions, or Git/file facts.
- **Interpretation:** architectural meaning reconstructed from those facts.
- **Inference:** a consequence or failure possibility not demonstrated by a live experiment here.
- **Recommendation:** proposed future preservation or correction, not accepted architecture.
- **Uncertainty:** what the evidence cannot establish.

Recommendations also identify their level: semantic architecture, experimental design, observability, statistics, or implementation infrastructure. A necessary distinction is not automatically a Python class, independently identified artifact, service, store, or universal framework.

No test suite, model request, service command, Docker operation, acceptance runner, benchmark, formatter, or code import was executed. Existing tests were read. This avoids test caches, coverage files, disposable fixtures, and live artifacts under the single-output restriction. Historical passing-test claims are not reported as fresh validation.

### Evidence register

The short evidence identifiers below refer to these repository-relative paths and precise anchors. Primary architecture documents and the ledger were read; source/test entries identify the relevant complete modules or selected bodies inspected, rather than claiming an exhaustive audit of unrelated modules.

| ID | Evidence inspected and anchor | Evidentiary role |
|---|---|---|
| E01 | [AGENTS.md](AGENTS.md); [docs/documentation_map.md](docs/documentation_map.md) | Operating rules, authority, sparse domains, historical versus current claims |
| E02 | [docs/architecture/taxonomy.md](docs/architecture/taxonomy.md), especially Repository intelligence, InformationNeed/retrieval/ranking, Context disclosure and assembly, InteractionAttempt, Evidence, Evaluation, Trace | Semantic distinctions and maturity |
| E03 | [docs/architecture.md](docs/architecture.md), Accepted repository-intelligence semantics through Remaining preimplementation research and evidence constraints | Integrated current/accepted system architecture and evaluation correlation requirement |
| E04 | [docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md](docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md), Semantic request and response; Interaction occurrence and Evidence; Serving provenance; migration phases | Accepted model boundary, observation, and dependency direction |
| E05 | [docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md](docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md), all decision sections including external semantic dependencies, capability boundary, and graph families | Accepted repository-intelligence foundation |
| E06 | [docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md](docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md), especially Evaluation, progressive disclosure, and authority | Accepted retrieval/ranking and explicit evaluation-case latitude |
| E07 | [docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md](docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md), Constraints, budgets, and disclosure artifacts; Planning versus model-input assembly; semantic-strength invariant | Accepted selection, realization, and presentation separation |
| E08 | [docs/backlog/epics/B-0002-coding-context-substrate.md](docs/backlog/epics/B-0002-coding-context-substrate.md); [docs/roadmap.md](docs/roadmap.md) | Unimplemented pressure, promotion, remaining review gate |
| E09 | [docs/backlog/metadata.md](docs/backlog/metadata.md); [docs/backlog/overview.md](docs/backlog/overview.md) | Dependency and maturity meanings, record navigation |
| E10 | [docs/implementation_ledger.md](docs/implementation_ledger.md), historical milestones and Architecture decision checkpoints | Superseded terminology and sequence of architecture refinements |
| E11 | [src/devtools/models/interaction/docs/overview.md](src/devtools/models/interaction/docs/overview.md); models.py, prompt.py, response.py, observation.py in that package | Actual ModelRequest/ModelSettings/Prompt/ModelResponse/ModelInteractionObservation values |
| E12 | [src/devtools/models/interaction/providers/llama_cpp.py](src/devtools/models/interaction/providers/llama_cpp.py), LlamaCppInteraction.__init__/send; [tests/models/interaction/providers/test_llama_cpp.py](tests/models/interaction/providers/test_llama_cpp.py), observation, settings, continuation, failure, native Tool tests | Implemented adapter path and tests; source of occurrence IDs |
| E13 | [src/devtools/observability/evidence/docs/overview.md](src/devtools/observability/evidence/docs/overview.md); [model_interaction.py](src/devtools/observability/evidence/model_interaction.py), all capture/Evidence/inspector definitions; [tests/observability/evidence/test_model_interaction.py](tests/observability/evidence/test_model_interaction.py), capture, omission, immutability, repeated occurrence assertions | Exact capture and replay limits |
| E14 | [src/devtools/execution/docs/overview.md](src/devtools/execution/docs/overview.md); runtime.py and interaction_attempt.py; [src/devtools/observability/evidence/terminal.py](src/devtools/observability/evidence/terminal.py) and inspection.py; [tests/execution/test_runtime.py](tests/execution/test_runtime.py), failure, cancellation, observer, and serialization tests; [tests/observability/evidence/test_inspection.py](tests/observability/evidence/test_inspection.py) | Narrow lifecycle, stage meaning, current correlation |
| E15 | [src/devtools/tools/docs/overview.md](src/devtools/tools/docs/overview.md); [execution.py](src/devtools/tools/execution.py); [tests/tools/test_runtime_integration.py](tests/tools/test_runtime_integration.py), nested Tool failure and source-validation tests | Tool ownership and limits of outer Runtime stage attribution |
| E16 | [src/devtools/models/serving/docs/overview.md](src/devtools/models/serving/docs/overview.md); [identity.py](src/devtools/models/serving/identity.py); [scripts/qwen/llama_cpp_profile.py](scripts/qwen/llama_cpp_profile.py); [docs/experiments/qwen38_llama_cpp.md](docs/experiments/qwen38_llama_cpp.md) | Serving identity fields, pinned experimental settings, unresolved defaults and unverified expected digest |
| E17 | [src/devtools/models/benchmarks/docs/overview.md](src/devtools/models/benchmarks/docs/overview.md); models.py, runner.py, storage.py; [tests/models/benchmarks/test_runner.py](tests/models/benchmarks/test_runner.py), TTFT/usage/throughput assertions; [test_storage.py](tests/models/benchmarks/test_storage.py), schema and round-trip assertions | Concrete bounded model benchmark, typed measurements, separate provider path |
| E18 | [experiments/qwen/docs/overview.md](experiments/qwen/docs/overview.md); [two_action_read_only_experiment.py](experiments/qwen/two_action_read_only_experiment.py), run and _follow_up_message; [patch_proposal_worker.py](experiments/qwen/patch_proposal_worker.py), fixtures, measurements, worker, grounding, patch and behavioral validation | Experimental adaptive acquisition, host evaluation, oracle intervention |
| E19 | [scripts/qwen/patch_proposal_worker_acceptance.py](scripts/qwen/patch_proposal_worker_acceptance.py), B0009LiveReport, run_acceptance, run, _report_payload, _cumulative_usage_payload, failure classification | Existing experiment-local correlation, partial failures, timing scope, serialization |
| E20 | [tests/experiments/qwen/test_patch_proposal_worker.py](tests/experiments/qwen/test_patch_proposal_worker.py), optimal acquisition, nonrequired reads, zero reads; [tests/scripts/qwen/test_patch_proposal_worker_acceptance.py](tests/scripts/qwen/test_patch_proposal_worker_acceptance.py), stress measurements and incomplete usage | Tested measurement semantics and secrecy assertions, not evidence of live model success |
| E21 | [experiments/worker_story/result.py](experiments/worker_story/result.py); test symbol inventory in [tests/experiments/test_worker_story.py](tests/experiments/test_worker_story.py) | Typed experimental human-review/resource outcomes, no reusable evaluation API |
| E22 | [src/devtools/context/__init__.py](src/devtools/context/__init__.py); [src/devtools/evaluation/__init__.py](src/devtools/evaluation/__init__.py); source-wide concept-definition searches | Sparse namespaces; no implemented EvaluationCase/Task/Derivation/retrieval/disclosure models |
| E23 | [docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md](docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md); items B-0016, B-0017, B-0018, B-0023, B-0031, B-0008; relevant B-0046 request/diagnostic pressure | Evaluation already has ownership; tracing, generic lifecycle, minimization and provider growth are deferred |
| E24 | [src/devtools/persistence/docs/overview.md](src/devtools/persistence/docs/overview.md); [src/devtools/agents/conversation/docs/overview.md](src/devtools/agents/conversation/docs/overview.md); [src/devtools/agents/integrations/codex/docs/overview.md](src/devtools/agents/integrations/codex/docs/overview.md) | Conversation persistence, external Agent distinction; no general evaluation persistence |
| E25 | [src/devtools/resources/filesystem/docs/io.md](src/devtools/resources/filesystem/docs/io.md); [src/devtools/resources/commands/docs/events.md](src/devtools/resources/commands/docs/events.md); pyproject.toml pytest/coverage configuration | Observation limitations and best-effort events; reason not to execute tests here |
| E26 | The four pre-existing untracked Qwen JSON reports listed in A; selected schema, fixture, task, verdict, failure, usage, termination, timing fields | Historical local observations, not controlled comparative evidence |
| E27 | Opening reconstruction and baseline of the pre-existing architecture-archaeology-dossier.md | Prior research at another HEAD, inspected only for context and supersession risk |

For E23, the full record filenames are discoverable in E09's canonical index. The relevant exact records include docs/backlog/items/B-0016-define-framework-live-harness-acceptance.md, B-0017-investigate-runtime-occurrence-observability-boundaries.md, B-0018-investigate-operational-data-minimization-disclosure.md, B-0023-investigate-observability-architecture.md, B-0031-investigate-generic-execution-lifecycle-promotion.md, B-0008-investigate-repository-context-discovery.md, and B-0046-investigate-advanced-model-interaction-provider-pressure.md.

### Limits and historical corrections

The old archaeology dossier identifies HEAD 7ff69df7196fe2c3bf67fa894c492b45583e5cfd. Its opening says synthesis introducing new assertions returns to repository derivation and describes graph views as DerivedKnowledge. Current E03/E05/E07 distinguish purpose-relative synthesis from repository intelligence and graph projections from the relationship knowledge they expose. The old dossier is not substituted for current architecture.

The ledger's former Session/Interaction/Attempt ownership, immutable InformationNeed assumption, and universal synthesis-promotion wording are historical. Later checkpoints and current E02/E06/E07 supersede them. Current persistence retaining session-named wire fields does not restore a Session runtime API.

The review found a scoped ADR-0001 completion/conformance discrepancy, detailed later. It does not resolve the discrepancy by inventing architecture or modifying code. Other naming/status residue, such as serving documentation initially describing only its first vLLM slice before documenting the second llama.cpp slice, is not evidence of a foundational evaluation defect.

No external research result, statistical performance claim, or current hosted-provider behavior was independently verified. Causal-design analysis below specifies information requirements and logical limits; it neither selects an estimator nor claims empirical effectiveness.

## C. Current architecture reconstructed

This reconstruction precedes recommendations. It separates accepted semantics from implemented mechanisms.

### Repository state

**Evidence, E02/E03/E05:** Repository has nominal logical identity across states and checkouts. A checkout path, Git HEAD, and current content do not identify that logical repository. RepositorySnapshot identifies immutable, logically complete successfully observed included state under explicit observation and inclusion semantics. Completeness is relative to that contract; it is not all filesystem objects, intelligence completeness, a physical copy, or a full recomputation.

Snapshot observation must expose the strength it actually establishes. Sequential file reads cannot silently claim an atomic whole-workspace instant. Inclusion/exclusion, generated and vendored material, links, submodules, address interpretation, and identity-relevant attributes matter. Exact policy identity and digest construction remain open. Git can supply provenance or an observation mechanism; dirty state can differ at the same HEAD.

A ResourceOccurrence is contextual to a snapshot and repository-relative address; it refers independently to ContentIdentity. ContentIdentity is address-independent and reusable under its content semantics. A move can preserve content and change occurrence; copies share content without being one occurrence. Rename/continuity is derived knowledge.

External semantic inputs include consumed configuration, language/toolchain semantics, dependency resolution, platform, environment values, generators, and external resources. One repository snapshot can support different interpretations. The external thing, its relevant state, and the observation establishing it differ. Representation may be a value, constraint, reference, inline observation, or independently identified object. Identity equality, value equality, semantic equivalence, compatibility, and applicability are not interchangeable.

**Implementation, E22/E25:** Filesystem Resources provide bounded access, decoding, and atomic writes, not repository snapshots. Current read semantics explicitly have stat/read races. No production RepositorySnapshot or external-state observation substrate exists. A file path and current Git HEAD cannot substitute for it in an experiment.

### Repository intelligence

**Evidence, E05:** RepositorySubject is a snapshot-local identifiable structural or semantic thing about which knowledge can be asserted. Analysis can establish subjecthood. A SourceOccurrence instead addresses a span or anchor within a ResourceOccurrence. Names, ranges, parser nodes, and global entity continuity are not foundational subject identity. Source anchors and subjects may participate independently in relationships and provenance.

DerivationDefinition identifies reusable semantic computation and its result meaning. It is not an executable binding. Derivation identifies application of those semantics to actual role-bearing direct semantic dependencies. DerivationExecution is a particular realization attempt. Zero or more immutable DerivedKnowledge artifacts may result. Definition, derivation, execution, and result identity serve distinct purposes; this is not a mandate for four services or classes.

Definition compatibility concerns semantic behavior, including relevant configuration/revision. Build identity helps explain a realization but does not alone define semantic compatibility. Equal derivation identities imply equivalent semantics for identical relevant inputs. An implementation believed compatible can still be buggy; deterministic output is not proof of correctness.

Dependencies govern state-relative applicability. Provenance explains production and support. Shared derivation support and result-specific source support may coexist without duplication. Direct dependencies need not flatten transitive closure, and semantic consumption is not every operational memory/file access.

DerivedKnowledge owns repository-relative intelligence only. It can express possible, necessary, conservative, ambiguous, partial, exhaustive, unresolved, approximate, and scoped propositions. It is neither infallible fact nor a universal assertion container. RelevanceEvidence, purpose-relative Context synthesis, execution failures, and evaluation judgments do not become DerivedKnowledge merely by being reproducible.

Applicability is an external assessment of whether relevant semantic dependencies remain satisfied under compatible definition semantics. It is not a mutable validity bit or snapshot ownership. Historical knowledge can remain applicable to multiple snapshots. Cache lookup, invalidation discovery, rederivation, and applicability differ.

Semantic-result coverage states the result space accounted for under assumptions and scope. Successful execution does not imply exhaustiveness; zero results do not imply absence; unsupported territory is not a negative finding. Partial execution can leave independently established results meaningful.

Two graph families are distinct. Derivation dependencies support applicability/reuse. Typed repository relationship views project semantic relationships such as calls/imports/references. A graph view can be an index, on-demand projection, or persisted representation; relationships derive meaning from knowledge families, not storage. Views need not use one node universe, and graph-local nodes need not be RepositorySubjects. A graph index is rebuildable, not an independent authority.

SnapshotDelta compares states. IncrementalMaintenance establishes applicable knowledge efficiently. Capabilities realize compatible semantic definitions with bounded access and finalized dynamic dependency accounting; they do not own global scheduling, callers' information needs, retrieval, model calls, or analyzed-repository mutation. Coarse dependencies are valid if correct; finer tracking is an optimization with explicit bookkeeping and maintenance economics.

**Implementation, E22:** These concepts have no production implementation. The current absence of a graph store, analyzer protocol, execution schema, or dependency index is planned openness, not an observed defective mechanism.

### Retrieval and ranking

**Evidence, E06:** InformationNeed is desired information relative to a purpose, distinct from Task, query, strategy, budget, Prompt, Context, and satisfaction. A Task may generate many evolving purposes. Purpose, typed anchors, constraints on acceptable information, and causal provenance can live in acquisition/planning structures without a global runtime InformationNeed identity.

Retrieval planning selects bounded applications of capabilities with purpose-derived inputs. Planning hypotheses are not repository truth. Exact addressed acquisition can bypass relevance discovery. Independent applications may run concurrently; dependencies and conditional waves impose partial order. Discovery bounds differ from disclosure budgets.

A ContextCandidate addresses a repository-intelligence referent: subject, resource occurrence, source occurrence, knowledge, relationship, or another justified referent. Candidate equivalence follows that referent, not an arbitrary hit UUID. File, symbol, and overlapping region candidates remain distinct; Context handles overlap later.

RelevanceEvidence preserves typed purpose-relative observations, originating application, provenance, native measurement semantics, and qualifiers. A lexical score, distance, reference count, and exact-match predicate have different meanings. Missing discovery is not negative evidence of usefulness. Evidence need not have standalone identity or persistence if a containing record preserves its meaning.

Ranking interprets purpose, candidates, preserved evidence, and identified ranking semantics. It does not overwrite evidence and must permit different rankers over the same observations. Ranking is separate from Context selection, diversity, representation, deduplication, budgeting, and final presentation order.

**Implementation, E18/E22:** Listing and reading fixtures is bounded fact acquisition; scripted/model-directed navigation does not implement accepted retrieval/planning/ranking semantics.

### Context and disclosure

**Evidence, E07:** DisclosureOption is a conceptual possibility for exposing identified information through a representation or characterized transformation. Origin, form, fidelity, support, applicability, and cost differ. Selection and representation are deliberately coupled in normal planning. Context is conditional composition, with non-additive coverage, overlap, complementarity, prior availability, sufficiency, authority, and multidimensional constraints.

DisclosurePlan is an immutable identified selected-information decision, including selected representations or transformations. ContextDisclosure is the immutable realized, provenance-bearing information artifact under/reference to that plan. Materialization realizes that decision and can perform an explicitly planned lossy synthesis. It cannot silently re-plan or present stale information as current. Planning cost estimates and actual realization cost differ.

Source-preserving representations and existing-knowledge projections need not establish new assertions. Synthesis can introduce purpose-relative assertions with explicit support without becoming repository DerivedKnowledge. If work independently establishes reusable repository-relative semantics, it crosses the explicit ADR-0002 derivation boundary.

Semantic-strength preservation applies through selection, projection, synthesis, compression, materialization, disclosure, and assembly. Possible cannot silently become definite; partial cannot become exhaustive; conflict cannot disappear into an unsupported single truth. Authority is purpose/claim-relative, not a universal source score.

Assembly arranges already-realized disclosure for a consumer, alongside instructions, Tools, and conversation. Order, separators, framing, serialization, and placement can vary under identifiable policies. Assembly cannot silently perform semantic compression to fit a budget; that requires planning/materialization. Provider wire translation remains at ModelInteraction even when assembly accounts for provider-facing constraints.

Disclosure history, currently available information, repository history, and Conversation history differ. Availability does not prove model comprehension. Budget is a ceiling, not a fill target.

**Implementation, E22:** There is no reusable compiler, DisclosurePlan, ContextDisclosure, materializer, synthesis system, or assembler. Experiment-authored SYSTEM follow-ups are concrete local presentation choices, not these implemented abstractions.

### ModelInteraction, Runtime, Tools, Evidence, and evaluation today

**Evidence, E11–E15:** ModelRequest is a frozen value with Prompt, ModelSettings, optional ConversationRef/provider settings, and ordered normalized Tool definitions. It has no identity. Prompt currently contains only content and role. ModelSettings currently exposes maximum_output_tokens and thinking_enabled; omission preserves provider defaults. ModelResponse retains visible content, source, continuation, optional usage/termination/reasoning, and descriptive Tool calls.

LlamaCppInteraction holds endpoint, model alias, source, and optional observer. It rejects continuation, serializes one message and established controls, calls the endpoint, normalizes output, and publishes a completed observation. ModelInteractionId identifies an invocation occurrence; EvidenceId identifies an observation record. Neither is a case, treatment, or evaluation realization.

Runtime retains the input message, constructs the request, invokes one selected interaction, validates source, retains output, and optionally replaces continuation under Conversation coordination. An optional specialized InteractionAttempt spans those boundaries. Runtime does not perform retrieval, disclosure compilation, Agent loops, Tool dispatch, retries, orchestration, or evaluation. Conversation history is not necessarily the exact model input.

ToolRunner validates and executes one typed Tool. Validation is not authority, Tool visibility is not permission, and model Tool calls do not execute. Tools do not own the outcome of a whole task. The test-only _CommandToolInteraction nests a Tool to test outer failure behavior; that does not promote Tool execution into the production ModelInteraction responsibility.

ExecutionInspector retains live attempt attribution and constructs immutable terminal Evidence. ModelInteractionInspector separately constructs capture-controlled completed-interaction Evidence. There is no automatic attempt-to-model-occurrence foreign key and no generic Trace implementation. Persistence currently stores Conversation, not arbitrary Evidence or evaluations.

ModelServing manages endpoint lifecycle. ServingProfileIdentity carries optional model revision/artifact/quantization/server/template facts, supplied by composition, not verified merely by constructing the value. ModelBenchmark is a separate bounded serving/model experiment, not Agent evaluation.

**Evidence, E02/E03/E21–E23:** Evaluation already has an EMERGING taxonomy responsibility, a reserved namespace, and B-0015/B-0016 ownership. There is no reusable EvaluationCase/Treatment/EvaluationRun API. No current reusable Task type was found; experimental tasks are ConversationMessage values. WorkerStoryResult and benchmark results provide bounded experimental measurements, not a general evaluation ontology.

## D. Existing experimental seams

The tests below judge semantic factorization separately from present executability. In each case, a clean accepted seam means the architecture permits the intervention; it does not mean a runnable harness exists.

### D1. Fixed repository state/intelligence; compare retrieval strategies

**Fixed:** included snapshot and observation contract; consumed external semantic state; available applicable knowledge and its definition semantics/coverage; graph/index view semantics and visible corpus; purpose, anchors, prior information, discovery constraints; ranker and downstream policies if measuring task effects.

**Treatment:** identified retrieval strategy/portfolio and its planning/query rules. If only acquisition mechanisms are compared, purpose-to-query planning must also be held fixed where possible; otherwise the treatment is the planner-plus-retriever bundle.

**Realization:** bounded applications, dependency waves, concurrency, caches, timing, and any permitted strategy stochasticity. A fixed snapshot alone does not freeze these.

**Retained evidence:** case/assignment, actual application inputs/bounds, available knowledge/view basis, candidates, native observations, origin and search coverage, failures, requested extra derivation, costs, and later ranking/disclosure/outcomes.

**Outcomes:** candidate recall/precision against an identified relevance judgment, unique useful discovery, cost, and separately task success.

**Seam:** semantically clean in E05/E06. Additional intelligence acquisition must cross explicit maintenance rather than silently enrich one retriever's corpus.

**Missing today:** all retrieval implementations and replayable input/result capture. A harness must freeze or record the evaluated knowledge availability, not merely snapshot identity. This is preservation/implementation work, not a required new intelligence-set ontology.

### D2. Fixed candidates and evidence; compare rankers

**Fixed:** purpose; exact referent multiset/set semantics, duplicate treatment and initial order where meaningful; complete retained RelevanceEvidence including measurement meaning and provenance; feature availability; downstream compiler and budgets for downstream comparison.

**Treatment:** ranking semantics, implementation/model/configuration, tie handling.

**Realization:** ranker application and any stochasticity. A ranker that makes new live retrieval or feature queries is a broader treatment unless those inputs are fixed.

**Retained evidence:** original candidate/evidence collection, policy version, produced ordering/ties/native rank values, evaluated cutoff, failures, latency, later selection.

**Outcomes:** rank-sensitive local measures and downstream coverage, tokens, task results.

**Seam:** explicitly required by E06, Ranking and Context boundary. Ranking need not use universal normalized scores.

**Missing today:** concrete ranker and an artifact/reference closure sufficient to replay the exact candidate/evidence input.

### D3. Fixed selected information; compare Context representations

**Fixed:** identified support/referents, propositions and required qualifications, purpose, required coverage, prior availability, consumer and declared resource comparison policy.

**Treatment:** representation/transform, fidelity or synthesis policy, with an explicit declaration whether information loss is itself intended.

**Realization:** materializer or synthesis execution; resulting disclosure and actual size/cost.

**Retained evidence:** shared selected-support basis, distinct plans/options, source/knowledge versions, actual disclosures, transformation versions, qualifications/conflicts/omissions, actual cost and downstream requests.

**Outcomes:** fidelity, semantic-strength violations, coverage, reconstruction burden, token/cost savings, and consuming-model/task utility.

**Seam:** conditional. E07 deliberately couples selection and representation. Changing a selected representation normally creates another plan. Holding a whole plan fixed is valid only for alternative conforming realizations of the representation already selected.

**Missing today:** concrete selected-support correspondence and transformation evaluators. Same candidate identity is too weak to mean same selected information: signature versus body, or partial versus exhaustive claim, changes what is available.

### D4. Fixed ContextDisclosure; compare assembly policies

**Fixed:** exact realized information and qualifications, purpose, consumer configuration, other conversation/instructions/Tool definitions, capacity and policy constraints, unless one of these is the intended treatment.

**Treatment:** ordering, framing, separators, placement, or prompt-instruction policy, explicitly defining what changes.

**Realization:** assembler output followed by separately identified model trial(s).

**Retained evidence:** disclosure/plan references, assembly policy/configuration, exact ModelRequest, material-to-presentation correspondence, effective model/serving facts, outcomes.

**Outcomes:** faithful presentation, truncation or strengthening violations, input tokens, model utilization indicators and task success.

**Seam:** explicitly clean in E07. A policy that drops or summarizes information to fit creates a selection/materialization change, not a pure assembly variant.

**Missing today:** production disclosure/assembly and exact request retention suitable for the promised replay strength.

### D5. Fixed exact ModelRequest; repeated model realizations

**Fixed:** full immutable semantic request, adapter semantics, intended model/serving profile, known external/continuation state, and explicit inference controls. With the current stateless adapter, continuation is rejected.

**Treatment:** for repeatability measurement there is no A/B treatment change; these are repeated realizations of one condition. Comparing models or seeds can make those explicit treatments or designed nuisance variations.

**Realization:** each invocation occurrence, sampling, runtime nondeterminism, provider service state, and response.

**Retained evidence:** distinct occurrence and trial references, exact request or authorized reconstructable representation, response/failure, capture availability, requested versus reported identity/configuration, time window, resource observations.

**Outcomes:** response variability, semantic/task correctness, termination, usage, latency.

**Seam:** directly executable through ModelInteraction, but request equality does not fix the model: the alias is adapter construction state, and defaults/environment are outside ModelRequest.

**Missing today:** portable sampling/seed/reasoning-effort semantics, guaranteed exact reconstruction from Evidence, and completed-failure observation. Repeated current requests support a claim about the observed route under known settings, not necessarily an exact immutable model distribution.

### D6. Fixed repository; enable/disable a graph view

**Fixed:** snapshot/external interpretation, relevant relationship knowledge and qualification if evaluating access to a view, task set, non-graph retrieval, downstream policies, and declared budget policy.

**Treatment:** availability/use of one identified typed graph view. Alternatively, construction and use of graph intelligence together form a broader treatment with indexing/maintenance cost.

**Realization:** view construction/materialization if in scope, retrieval/traversal, ranking, disclosure, model/Agent execution.

**Retained evidence:** what view and backing facts were available/used; bounded traversal and paths; candidates and evidence attributable to it; ranker/consumer compatibility; setup and ongoing cost; downstream results.

**Outcomes:** relation correctness/coverage, traversal latency, candidate contribution, disclosure efficiency, task-class-specific success.

**Seam:** clean as a semantic capability/view intervention, but graph-aware retrieval/ranking are interacting factors. A consumer that cannot use the view does not test the view's potential usefulness.

**Missing today:** all concrete views and consumers. A graph toggle must distinguish precomputed availability from graph production cost, and must not quietly change total budget.

### D7. Coarse versus fine dependency tracking

**Fixed:** initial snapshot, ordered edit/external-state sequence, requested knowledge workload, analyzer result semantics, correctness oracle, comparable resource limits and cache warmness policy.

**Treatment:** dependency granularity and/or maintenance strategy; changing both is an explicit bundle or factorial comparison.

**Realization:** dependency discovery, applicability assessments, reuse/invalidation/recomputation, reverse-index operations, publication and projection maintenance.

**Retained evidence:** state transition, actual dependencies/roles, applicability basis, reused versus recomputed products, full-recomputation or independent reference results, partial/unsupported states, operation counts, latency, storage/bookkeeping scope.

**Outcomes:** stale/wrong reuse and missed invalidation separately from recomputation avoided, unnecessary invalidation, maintenance cost, and storage.

**Seam:** clean in E05 because applicability is independent of the optimization. Equal semantic results need not have identical knowledge IDs across different derivation/dependency representations.

**Missing today:** maintenance implementations and comparable observation boundaries. Granularity may change semantic derivation keys while result meaning stays equivalent; byte/identity inequality must not automatically be scored incorrect.

## E. Experimental factorization failures

The following are failed naive experimental interpretations, not proof that accepted architecture is intrinsically invalid.

| Apparently fixed boundary | Why the proposed control can fail | Adequate control or honest claim |
|---|---|---|
| Same Git HEAD | Dirty files, inclusion policy, generated inputs, external semantics may differ | Identified observed snapshot plus relevant external observations |
| Same RepositorySnapshot | Available knowledge, semantic interpretation, index coverage, materialization and caches can differ | Freeze/record evaluated knowledge closure, capability/view availability and operational conditions |
| Same DerivationDefinition | Bindings can differ in bugs, resource use, supported territory | Record realization identity and coverage; compare under the semantic contract |
| Same DerivedKnowledge IDs | References may be retained while support or executable environment is unavailable | State intended replay strength and retain its required closure |
| Same candidates | Observations/features, duplicate handling, tie order, and purpose can differ | Fix candidate/evidence input and feature basis, not candidate names alone |
| Same DisclosurePlan, new representation | The plan already selected representation/transformation | New paired plans sharing selected-support constraints, or vary only conforming realization |
| Same ContextDisclosure | Other instructions/Tools/prior availability or model capabilities can differ | Fix these or declare them treatment dimensions |
| Same ModelRequest | Adapter alias, defaults, provider revision and continuation backing state may vary | Record external invocation facts; limit claim to identifiable conditions |
| Same recorded later retrieval after earlier Context changes | Later purpose was caused by the original model response | Conditional local replay only, or regenerate the affected continuation |
| Same terminal success/failure | Different stages, missing observations, oracle strength and costs can yield the same verdict | Preserve typed evidence and evaluator-specific observations |

**Interpretation:** The accepted boundaries are substantially well-factored. Their experimental strength comes from invariants and referential/support semantics, not from the presence of names. E05–E07 mostly anticipate the controls above. Freezing every possible input would be wasteful and sometimes impossible; the experiment must identify what its causal claim depends on and record uncertainty where control fails.

**Recommendation — experimental design/observability:** distinguish intended fixed factors, intended treatment changes, observed conditions, and deviations. A configuration diff only proves that two configurations differ; it does not identify the intended contrast or prove all relevant external state was fixed.

**Uncertainty:** Actual snapshot consistency, knowledge publication, index freezing, reference retention, and dynamic-dependency behavior cannot be pressure-tested until implementations exist. This is not converted into a FATAL or MATERIAL finding.

## F. Layer-local correctness versus downstream utility

**Evidence:** E03 explicitly separates local correctness/quality from task success. E05 defines deterministic but possibly incorrect/qualified knowledge; E06 separates native retrieval evidence, ranking, and selection; E07 separates fidelity, coverage, cost, and consumer utilization.

| Mechanism | Local question | Different downstream question |
|---|---|---|
| Call graph | Does each relation and coverage claim satisfy the family's semantics? | Does using this view help this task class under the resource policy? |
| Retriever | Which judged-useful referents were discovered under stated bounds? | Did later selection and the model turn that discovery into success? |
| Ranker | Does ordering improve the chosen rank-sensitive criterion on fixed observations? | Does the compiler select complementary information, or now overselect redundant high-ranked items? |
| Synthesis | Is the assertion faithful, supported, qualified, and conflict-preserving? | Is synthesis useful compared with source, existing projections, or no additional information? |
| Compression | Which details/qualifications survive and at what cost? | Does the consuming model succeed with the remaining information? |
| Fine dependency tracking | Is reuse/applicability correct under the changed state? | Does saved work exceed bookkeeping, storage, and maintenance cost for the workload? |

**Interpretation:** No architecture change is required to admit both judgments. An evaluator needs a typed target and criterion with scope, rather than a universal quality value. One layer may be correct and unhelpful; one successful task can conceal an incorrect layer because another source compensated. Downstream success cannot retroactively validate a graph proposition, and a local metric cannot substitute for coding success.

**Recommendation — evaluation semantics:** preserve each judgment's target, evaluator/oracle, scope, missingness and supporting evidence. Connect downstream observations by explicit realization references. Do not award all upstream mechanisms equal credit for one terminal success.

## G. Failure-attribution analysis

This matrix describes what would distinguish explanations and what is available now. Accepted semantic artifacts permit most distinctions; source implementation does not yet supply the repository-intelligence/Context records. A plausible diagnostic category is not automatically a demonstrated cause.

| Failure hypothesis | Evidence needed to distinguish it | Boundary and present limitation |
|---|---|---|
| Observation incomplete | Inclusion/consistency contract, observed resource set and failures, independent fixture/observation basis | E05 forbids incomplete observation masquerading as complete; current filesystem reads are not snapshots |
| Intelligence wrong | Definition/result proposition, actual inputs, result/support, compatible oracle counterexample | E05 supports semantic checking; no analyzer exists |
| Intelligence correct but incomplete | Accounted-for result space, unsupported/partial regions, requested analysis, oracle scope | Must not infer coverage from successful execution or result count |
| Applicable knowledge incorrectly reused | Reused knowledge, target state/external interpretation, dependencies, satisfaction relation and assessment, reference recomputation | Applicability is distinct in E05; no assessment/maintenance records yet |
| Graph relation missing | Backing relationship results versus view content versus traversal limits | Separate analyzer omission, stale/broken projection, and query exclusion; “no edge” alone cannot distinguish them |
| Retriever missed useful information | Available/indexed corpus, purpose and query/application, complete candidate output, relevance judgments and search bounds | Absence can arise from corpus incompleteness or discovery; current list/read probes cannot diagnose reusable retrieval |
| Ranking buried discovered information | Fixed candidates and native evidence, exact output order/ties, ranker/features, selection cutoff | E06 explicitly preserves this seam; no ranker output artifact yet |
| Disclosure omitted surfaced information | Ranked inputs, candidate/options, selected plan, prior availability, budget/policy and omission rationale where needed | High rank alone does not prove selection was wrong; competing coverage may justify omission |
| Representation lost semantic detail | Selected source/propositions, planned representation, realized information, fidelity/coverage contract | Distinguish intentional tested loss from accidental materialization loss |
| Synthesis strengthened a weak claim | Source qualification, assumptions/conflicts/coverage, selected transformation, output and any stronger derivation | E07 prohibits silent strengthening; local semantic tests possible, arbitrary prose remains difficult |
| Materialization wrong | Immutable plan, source state/applicability at realization, transformation identity, actual disclosure/failure | Separates planning intent from realization; no implementation today |
| Assembly buried critical information | Exact disclosure and request, ordering/framing policy, other prompt components, capacity/omission mapping | Presentation can be varied cleanly; “buried” as cause requires comparison, not just position |
| Model ignored correct Context | Proof material reached the invocation, compatible task oracle, response/behavior, repeated or paired presentation tests | No artifact proves internal comprehension or ignoring; supported category is failure despite available adequate information |
| Model hallucinated despite correct Context | Same delivery basis, identifiable unsupported response proposition, oracle and qualifications | Can establish unsupported/incorrect output, not its unique internal cognitive cause |
| Tool/runtime failed afterward | Model output/proposal, admission/authorization, actual Tool invocation/result/error, Runtime stage, state effects | Current ToolRunner has no generic lifecycle; Runtime stage is location, not cause |

Additional ambiguity: a model interaction can finish successfully and Runtime later fail source validation or continuation commit. Interaction success is not task success. Conversely, E15's test-only nested Tool failure appears as INTERACTION_INVOCATION at the outer boundary; that stage does not mean the provider or model caused it.

**Recommendation — observability:** correlate selected, realized, presented, invoked, and evaluated artifacts at the boundary where each fact is known. Preserve execution absence, capture omission, timeout, cancellation, unsupported analysis, and oracle abstention as distinct from semantic negative results.

**Inference:** Complete records make alternative explanations testable and can localize the earliest observable contract violation. They do not guarantee a unique causal explanation: redundant information, multiple simultaneous defects, and compensating mechanisms can make attribution set-valued or unresolved. Model-reported reasoning is another observation, not privileged proof of why the result occurred.

## H. Evaluation responsibility verdict

**Position A, strongest version:** Small experiment-local harnesses can use existing identities, immutable artifacts, source fixtures, configuration, Evidence, and ordinary references. The vLLM benchmark and Qwen reports demonstrate that meaningful bounded measurements do not require a generic EvaluationRun class, Trace backend, or universal evaluator. An experiment-local structure can express the whole experimental contract adequately.

**Challenge to A:** Task, request, execution, and repository provenance do not by themselves say what is being judged, which variation was intended, what comparison population was selected, which oracle was applied, or whether two judgments concern the same realization. Source-wide inspection found no current Task primitive that supplies these semantics. A record can faithfully say what happened while leaving a comparison invalid. If the harness stores those distinctions, it has implemented evaluation semantics locally; their ownership has not disappeared.

**Position B, strongest version:** Evaluation owns assessment and comparison meaning that observability, repository intelligence, Context, execution, and model serving do not. It correlates their facts without taking their lifecycles. A benchmark outcome, human judgment, or treatment assignment is neither repository knowledge nor a Runtime attempt.

**Challenge to B:** Most suggested nouns do not justify universal classes or independent persistence. A fixed fixture identifier, experiment-scoped variant key, realization ordinal, and structured evaluator output can suffice. A universal system that forces every analyzer/retriever/Tool to expose a score would damage existing boundaries.

**Verdict — interpretation grounded in E02/E03/E06/E23:** A distinct Evaluation responsibility is justified and already recognized. Evaluation cannot remain semantically ownerless “just infrastructure,” but its first implementations can remain experiment-local infrastructure. This is a refinement of an existing reserved responsibility, not discovery of a missing thirteenth domain.

**Minimum ownership — recommendation, semantic architecture:**

- Define the subject and conditions of assessment, and the comparison basis when comparison is intended.
- Distinguish intended intervention/fixed factors from observed execution conditions.
- Associate realizations with cases/conditions and with existing layer-local evidence, including failed or incomplete realizations.
- Preserve criterion/evaluator/oracle/rubric meaning and version, heterogeneous observations/judgments, and their targets.
- Keep later comparison/inference separate from raw observations and declare its population, assumptions, exclusions, and uncertainty.

It does not own repository snapshots, DerivedKnowledge, retrieval, materialization, model invocation, Tool authority, execution scheduling, generic traces, storage technology, or statistical algorithms. A future Evaluation ADR is justified only to accept this distinct comparison/assessment contract, if formalization is needed for reusable consumers; it need not precede the first deterministic repository-intelligence slice.

## I. EvaluationCase analysis

**Evidence:** E06 expressly permits fixed evaluation cases and evaluation-case identity without runtime InformationNeed identity. E08 preserves concrete evaluation-case identity as unresolved implementation pressure. E17's BenchmarkCase is a narrow workload value with name, prompt, maximum tokens, temperature, and optional expected text; it is not the general case semantics requested here.

**Interpretation:** EvaluationCase is a useful and, for repeatable comparisons, necessary semantic distinction: the versioned problem or assessment opportunity to which treatments are applied. “Necessary” here means an unambiguous comparison basis, not an independently persisted framework object.

A repository/coding case can refer to Task specification, observed repository state, relevant external-state assumptions, purpose/anchors, expected behavior, admissible resources, and acceptance constraints. A local analyzer case may have no Agent Task, Prompt, or model. A ranker case may begin at frozen candidates/evidence. Forcing all of these into one mandatory case shape would erase useful local experiments.

**Identity:** Repeated comparisons need stable reference to case content/version. An experiment-scoped key plus immutable fixture revision or content-derived basis is sufficient initially. Nominal case-family identity can survive revisions; each materially different comparison basis must remain distinguishable. A filename or “selection-stress” label alone does not prove stable content. No global UUID or standalone runtime lifecycle is required.

**Invariants across treatments:** State what the comparison promises to preserve: task meaning, repository/external interpretation, purpose/anchors, success criterion, permitted information, and resource constraints when these are controls. Inputs designated as treatments are not silently baked into shared case identity. A study explicitly varying repository states can have a case family with state as a factor; that is a different comparison from the seven fixed-state examples.

**What should not determine problem-case identity:** invocation timestamp, attempt ID, response, observed outcome, random draw, execution machine, treatment label, optional capture setting, or model alias when model is a factor. Incidental path changes should not create a different semantic fixture. Conversely, changed test/oracle assumptions that change “success” must be versioned somewhere in the assessment contract.

| Factor | Case/control role | Treatment role | Execution/environment role |
|---|---|---|---|
| Model configuration | Fixed consumer requirement for a declared model-specific case, or experiment control | Vary model/reasoning/sampling to compare it | Effective/provider-reported settings and drift observations |
| Context budget | Fixed admissibility/resource ceiling when comparing quality at a budget | Budget sweep or disclosure-policy treatment | Actual remaining capacity after instructions/Tools/history; realized token consumption |
| Available Tools | Task's permissible environment/capability contract | Deliberate capability ablation or exposure-policy comparison | Actual versions, availability, admission, results and failures |
| Oracle/expected behavior | Problem success meaning and protected expected constraints | Usually held fixed; changing evaluator is a separate assessment study | Which oracle/rubric actually ran, version, failure/abstention |
| Repository/external state | Fixed problem basis in matched comparisons | Deliberate state/configuration factor in a different study | Observation guarantees and deviations |

**Recommendation:** Separate case content from treatment assignment, evaluator application, and observed realization. Regrading a retained patch with a repaired oracle creates a new judgment, not a retroactively different execution. If an oracle change changes the problem's success definition, name that changed definition in the comparison rather than merging grades.

The ADR-0003 sentence permitting a case identity to hold “treatment identity stable” is compatible with a repeatable case-treatment association. It should not be read as requiring a different base problem identity for each treatment. AM-R2 records this clarification.

## J. Treatment analysis

Explicit treatment **semantics** are required for an intended causal comparison. A universal Treatment **class** is not.

**Interpretation:** A treatment identifies the intervention being assigned within an experiment: retriever/portfolio, graph availability, ranker, disclosure policy/budget, representation, synthesis, model, reasoning configuration, Tool access, dependency granularity, maintenance policy, or a declared bundle. “Differ in exactly one intended dimension” means the experiment identifies that dimension and keeps other pre-intervention conditions controlled or accounted for. It does not mean all downstream artifacts remain equal.

For example, changing retrieval should change candidates; those candidate differences are part of the treatment's pathway. If a graph treatment also changes ranker semantics and budget without declaration, “graph alone” is not the contrast actually tested. If changing model necessarily changes tokenizer, fixed token count and fixed information cannot both be assumed without defining the comparison.

| Identity distinction | Meaning | Why conflation fails |
|---|---|---|
| Configuration identity | Exact/versioned specification of parameter values and component bindings | Does not say which values are experimental factors, controls, defaults, or nuisance conditions |
| Treatment identity | Experiment-relative intended intervention/condition | Same config can be a control in one study and a treatment in another |
| Execution identity | One actual realization under assigned/observed conditions | Same treatment can produce many stochastic or deterministic runs |
| Outcome/judgment reference | One observed result or assessment tied to a realization and criterion | One run can have multiple outcomes and later re-evaluations |

**When ordinary configuration suffices:** A small harness explicitly records two named variants, a shared immutable basis, the intended difference, and effective observations. That configuration-plus-design is already enough treatment representation.

**When stable treatment reference matters:** repeated trials; factorial cells; external joins; distributed/partial execution; reused result sets; later comparison. A scoped tuple such as experiment-version plus variant key can supply identity; no standalone lifecycle or arbitrary UUID follows.

**Recommendation — experimental design:** Preserve assigned condition, realized condition, and deviations separately. A requested graph view that is unavailable is not the same observation as successfully running the no-graph control. A setting omitted to provider defaults is not equivalent to an explicit setting without supporting evidence.

Treatment identity must not become a mandatory semantic dependency of repository knowledge. Record it in evaluation provenance unless the changed factor actually changes the derivation's meaning or inputs.

## K. Evaluation-run / realization analysis

A realization is one application of the case/condition protocol, including its execution and terminal or incomplete state. It is not necessarily an Agent Run. An analyzer-only evaluation may use one derivation execution; a coding realization may involve dozens of interactions, Tool calls, and multiple state transitions.

**Evidence, E04/E14:** ModelInteractionId identifies one invocation. InteractionAttempt identifies Runtime's retention/invocation/validation/continuation effort for one input. Neither identifies a whole comparison trial; EvidenceId identifies a historical observation. Reusing one of these as a generic evaluation-run identity would falsely collapse independent meanings.

**Required distinction:** same case + same treatment + repetition 1/2/3 must remain separately referenceable. An experiment-local realization key/ordinal is enough. A deterministic execution also benefits from occurrence distinction when measuring cost, diagnosing failures, comparing implementations, or detecting nondeterminism. A semantic derivation key identifies intended computation, not the execution's duration or failure.

An evaluation realization can correlate an existing Agent Run when one exists, but evaluation does not implement its lifecycle. It can correlate zero, one, or many ModelInteractionIds, InteractionAttemptIds, derivation executions, Tool/command results, and state references. A pure offline re-evaluation can consume existing artifacts without rerunning the task.

**Recommendation — evaluation semantics:** Distinguish execution realization from evaluator application. Repeated human/model grading of one patch gives multiple judgments about one patch realization, not extra independent coding successes. A failed provider call remains an assigned trial with a failure/missing-outcome status; dropping it because no ModelInteractionEvidence was produced biases the retained population.

**Persistence:** Required when the claimed comparison depends on retaining or joining trials later; not universally required for a transient deterministic assertion. Correlation scope must be explicit under concurrency. Timestamps and matching prompt text are insufficient as primary joins.

## L. Outcome / measurement / judgment semantics

**Interpretation:** Outcome is what resulted at a stated boundary; measurement is an observation under a defined procedure/unit; judgment interprets an artifact or behavior against a criterion/rubric. A constraint states admissibility. Resource consumption is an observed quantity. These roles can coexist in one small record without being one score.

Examples:

- A patch is an output artifact; test executions are observations; “correct for the specified task” is an evaluator judgment.
- A timeout is an execution outcome; its duration is a measurement; the maximum allowed duration is a constraint.
- A conservative call relation is a semantic result; compatibility with a soundness oracle is a local judgment.
- Provider-reported token use is a measurement with provenance and missingness, not a reconstructed truth about every internal token.
- Authorization compliance is a judgment over declared policy and observed admissions/effects; lack of a forbidden proposal alone does not demonstrate enforcement.

**Evidence:** E17 keeps TTFT, total duration, usage, throughput, expectation_met and finish_reason distinct. E19/E20 leave incomplete cumulative usage unknown. E21 distinguishes gate summary, review outcome, corrections, escalation, architecture violations, and human intervention.

**Recommendation — minimum semantic requirements:** an observation/judgment must be attributable to its target realization/artifact, criterion and relevant version, evaluator/procedure, scope and units where meaningful, evidence basis, and availability/completion state. Keep false, zero, not measured, unavailable, not applicable, censored, evaluator failure, and abstention distinguishable where the evaluation depends on them. No universal metadata schema is proposed.

Collections, sets, distributions, categorical verdicts, counts, elapsed durations, and typed relations are legitimate outcomes. Exhaustive correctness requires an explicit universe and coverage obligation; it cannot be inferred from a pass count. Human disagreements and model-judge uncertainty remain observations, not silently resolved truth.

## M. Universal-score verdict

A foundational score: float is harmful because it discards what was measured, what the scale means, the evidence/oracle, scope, tradeoffs, and missingness. It can equate “no result,” “zero correctness,” “zero latency,” and “not applicable,” or let performance compensate for a correctness/authority violation.

E05 rejects universal confidence/truth scalars; E06 rejects universal native-relevance normalization; E07 separates constraints, utility considerations, and costs. Evaluation should preserve the same discipline without banning useful numeric measurements.

**Recommendation:** A policy-specific score or aggregate is legitimate as a derived evaluation conclusion, with declared criterion, inputs, weighting/normalization, population, exclusions, budget, and version. Raw typed outcomes remain accessible. A leaderboard value, quality-at-budget measure, or cost-effectiveness policy is not foundational universal quality. No formula is selected here.

## N. Universal EvaluationEpisode verdict

A universal EvaluationEpisode containing snapshot, intelligence, retrieval, ranking, disclosure, model request/response, Agent execution, outcomes, and metrics is not justified.

It would help navigation if it were merely a bounded report or reference manifest. As an owner, however, it would impose a fictitious mandatory pipeline, optional-field inflation, shared lifetime/retention, and duplicated truth across domains. It would fit neither analyzer-only evaluation nor multiple adaptive retrieval/model episodes cleanly. It would also make privacy and partial failure harder by bundling protected oracle information with model-visible material.

**Counterattack against fragmentation:** Separate records without navigable joins are equally inadequate. Hundreds of content hashes do not make a comprehensible experiment if the case assignment, realized condition, missing pieces, and input/output correspondences are lost. The minimum architecture requires resolvable correlation for the claim made.

**Recommendation:** small experiment/case/condition/realization references, layer-owned artifacts, and evaluator-owned outputs; optional bounded experiment-local manifest/report. A single local JSON record is acceptable if its semantics and ownership remain explicit. E19's B0009LiveReport is useful precisely because it is a bounded fixture report, not a universal framework episode.

## O. Trace architecture verdict

**Evidence:** E02 defines Trace as future causal/temporal execution structure, distinct from Evidence and Telemetry. E23 defers generic tracing until consumers establish shared pressure. E25 command events have bounded queues and best-effort loss; even terminal events may be dropped.

Generic traces can show order, duration, parent operations, retries, and resource spans. They cannot infer the treatment contrast, the intended fixed basis, the meaning of a rubric, hidden oracle privileges, or the denominator of a comparison. An execution dependency is not proof of a treatment effect.

Explicit evaluation records can capture those meanings but need factual execution observations. Copying complete spans into every evaluation record is unnecessary.

**Verdict:** a hybrid is appropriate: evaluation-owned design/assessment references, existing layer-local artifacts and immutable Evidence, optional traces for execution detail. Trace must not become the authoritative owner of case/treatment/outcome semantics. Sampling, dropped events, incomplete collection, capture policy, and instrumentation version must remain visible whenever conclusions depend on trace coverage.

No tracing technology, event bus, propagation framework, or backend is recommended now.

## P. Causal-DAG verdict

Neither of the accepted graph families is an experimental causal model. A derivation dependency can explain applicability, and a call graph can describe repository relationships; neither by itself identifies causes of a coding-success difference.

A universal third causal DAG is not justified. Relevant causal structure depends on the experiment and question: graph availability may affect candidate acquisition, which affects disclosure, which affects task success; concurrent cache state or model drift may confound the comparison. Another experiment might treat the ranker or token budget as the intervention and the graph as a fixed condition.

**Recommendation — experimental design:** preserve intervention targets, assignments, decision dependencies, observed factor values, and episode references sufficient to express an experiment-relative causal hypothesis later. Ordinary records/links can do this; optional diagrams or analytical DAGs belong to that study.

Even adaptive policy analysis or mediation does not show a need for a foundational DAG service. It may require a study-specific causal model and stronger logged decision information. Such a model encodes assumptions, including unobserved causes; a trace of observed execution is not a substitute.

**Reopen condition:** multiple real consumers require the same stable causal semantics that cannot be expressed honestly through design records and local references. No such scenario was found in current source, tests, or the seven requested interventions.

## Q. Causal-attribution requirements

A rise in coding success supports a causal contribution claim only to the extent that the intended contrast, comparable units, realized conditions, measurement, and alternative explanations are adequately controlled or accounted for. Correlation alone remains descriptive.

The architecture must preserve the information needed for later methods; it does not implement or select the methods.

| Design concern | Semantic information that must survive | Invalid shortcut |
|---|---|---|
| Paired evaluation | Same case/version, snapshot and relevant external interpretation, pairing reference, both assignments and results | Matching task names or Git HEADs |
| Repeated trials | Case/condition/realization distinction, sampling/seed if exposed, shared environment blocks, all assigned attempts | Treating repeated grading or correlated invocations as independent tasks |
| Ablation | Precisely removed capability/use, fallback behavior, resulting candidate/disclosure changes, budget and cost scope | Calling a bundle change “graph off” |
| Factorial comparison | Joint factor values and cell assignment, compatible consumer versions, full outcomes by case | Averaging away graph-by-ranker or representation-by-model effects |
| Interaction effects | Task class, joint conditions, model/consumer, intermediate outputs and resource changes | Assuming component benefits are additive |
| Randomization | Unit of assignment, assigned condition/order, assignment procedure/version and realization, relevant seed if used | Inferring randomized assignment from shuffled-looking timestamps |
| Blocking/stratification | Repository/task family, size/difficulty or other declared pre-treatment attributes, provider/time/hardware block | Inventing strata after looking at success without recording that choice |
| Matched repository/task/external basis | Immutable/referenceable case contents and observations, interpretation semantics, deviations | One repository snapshot used as shorthand for all environment state |
| Model/provider drift | Requested identity, observed revision/profile or known alias, defaults/settings, adapter version, time window and unknowns | Claiming exact model equality from a served name |
| Resource budgets | Assigned ceiling, effective remaining capacity, actual consumption, timeouts, setup/amortization policy | Calling higher success an improvement without reporting doubled tokens or indexing cost |
| Missing/failing trials | Intended trial roster, starts, aborts, exclusions, timeout/cancellation, oracle/capture failures | Keeping successful response records as the full denominator |
| Cross-trial interference | Shared caches/indexes/service load, resets or reuse policy, scheduling/order and warm-up | Treating a warm second treatment as exchangeable with a cold first |

**Recommendation — evaluation semantics:** distinguish intended assignment from realized exposure. Preserve failures/deviations for later declared handling; do not automatically turn infrastructure failure into either task failure or deletion from the sample.

**Recommendation — experimental design:** decide whether the question is total system contribution or a controlled local effect. If graph retrieval changes candidates and tokens, those are potential mechanisms of its total effect. Holding them fixed can answer a narrower direct-effect question but can remove the pathway under investigation. Record both the intended comparison and observed mediators rather than “controlling” them silently after seeing results.

**Recommendation — statistics:** retain per-case/per-realization data, grouping, assignments, evaluator versions and exclusions so later uncertainty estimates and comparisons can respect dependence and heterogeneity. No sample size, estimator, significance threshold, or statistical algorithm is selected.

**Limit:** Even excellent records cannot prove the absence of unobserved confounding, provider drift, benchmark contamination, or oracle error. A defensible conclusion states the tested cases/conditions, comparison design, uncertainty, costs, and plausible limitations. “Contributed under these conditions” is narrower than “this architecture is better.”

## R. Counterfactual replay analysis

Replay has three strengths already distinguished by E05: provenance inspection, semantic reconstruction, and operational rerun. A stable identity alone guarantees none of the latter two.

| Replay | Valid when | What must be retained |
|---|---|---|
| Same candidate/evidence input to two rankers | Purposes, candidate equivalence, evidence/features and availability are fixed; no hidden live acquisition | Input closure, native semantics, order/ties where relevant, ranker versions/configuration |
| Same selected support to representations A/B | Support and intended information constraints are identified; different representation decisions are explicit | Paired plans, source/knowledge references plus retrievable values, transformations, qualifications, actual disclosures |
| Same plan to materializers A/B | Both realize the representation/transformation authorized by that plan | Plan, dependency state, materializer bindings, output/cost/failure |
| Same disclosure to assemblers A/B | Disclosure and other fixed prompt inputs are unchanged; no silent semantic compression | Exact disclosure, assembly policies, other prompt components, exact requests |
| Same request to repeated model trials | Requested input and known provider/model conditions are fixed or deviations declared | Full request, route/profile/settings, occurrence IDs, responses/failures, unknown defaults |
| Same edit sequence to maintenance policies | Initial state, workload, edit/external transitions, reference semantics and cache policy are matched | Ordered states/transitions, dependency/reuse decisions, output equivalence basis, cost boundaries |

A hash can support equality checking if its construction and domain are known. It cannot reconstruct missing content. Redacted or omitted payloads limit replay; operational reproducibility may require retained binaries, templates, dependency artifacts, or service behavior that is unavailable. Report “not replayable at this strength” instead of silently substituting current state.

**Adaptive boundary:** If earlier Context changes a model response, that response may change the next information purpose, retrieval query, Tool action, edited repository, and later available information. The recorded later episode belongs to the original trajectory. Replaying rankers against its fixed candidates is valid as a conditional local evaluation of that episode; it is not automatically the continuation the alternative earlier policy would have produced.

For an end-to-end alternative, regenerate downstream decisions from the divergence point under the alternative policy and declared environment. If instead a recorded continuation is forced, label the study as conditional/teacher-forced rather than natural policy performance. No generic off-policy estimator is selected or assumed valid.

Do not replay side-effecting Tools solely because historical Evidence exists. Replay requires an appropriate isolated environment and authority; cancellation is not rollback, and ambiguous remote effects require authorized reconciliation.

## S. Progressive-disclosure / trajectory analysis

Progressive disclosure requires enough episode/decision correlation to distinguish initial information from acquired follow-up information and to measure the acquisition policy. It does not require a foundational Agent trajectory ontology.

**Evidence, E06/E07:** changed uncertainty or prior disclosure can justify later purposes; prior disclosure differs from current availability and comprehension; decomposition need not create a persistent need tree. E18 actually reconstructs stateless follow-up prompts from ordered accepted Tool cycles. That local sequence is useful evidence but not an implementation of generic Context history.

**Minimum information — recommendation:** realization reference; ordered or partially ordered decision occurrences; policy/configuration version; information and resources available at each decision; purpose/anchors; acquisition/application selected; resulting evidence/disclosure; actual model-visible request; source of feedback; remaining budget; stopping/continuation decision; state changes and causal predecessor references where needed.

An experiment-local episode ordinal or parent reference is sufficient for many probes. Concurrency may require dependency order rather than a single sequence. A trace can carry execution links, but the evaluation still needs policy assignment and the information visible when the decision was made.

Initial and eventual recall/coverage remain distinct. More follow-up calls may repair weak initial acquisition while increasing cost. Count repeated disclosures, stale reuse, compaction, and policy stopping conditions where relevant. “The model saw it earlier” is not proof it remained available later.

**Uncertainty:** Future off-policy comparison may need action probabilities or a justified policy reconstruction, and some counterfactuals may not be identifiable from logs. That is study-specific pressure, not a reason to require probability fields or causal edges in every Context artifact now.

## T. Nondeterminism and model/provider drift

**Evidence:** E05's foundational intelligence is deterministic under identified semantics, not certain or necessarily correct. E11's portable settings expose output limit and thinking enablement only. E12 leaves sampling defaults at the server. E16 supplies optional reproducibility facts and a pinned experimental profile. E17's separate benchmark route has an explicit temperature field; this does not mean portable ModelSettings already supports temperature.

| Source of variation | Control where practical | Record/identify | Repeat or stratify when needed |
|---|---|---|---|
| Model inference | Explicit supported sampling/reasoning settings; fixed input | Requested controls, omissions, response usage/termination, occurrence | Repeated trials by case/condition |
| Provider/service drift | Pinned artifact/build for local routes | Requested alias; observed model/revision/profile; time window; unavailable facts | Provider/build/time blocks; do not claim hidden revision equality |
| Hardware/runtime/concurrency | Comparable hardware/load and execution policy | Runtime, relevant placement/precision/cache settings, concurrency, warmness, clock scope | Performance repetitions and environment blocks |
| External semantic state | Bound and observe consumed inputs | Actual values/constraints/observations and semantic compatibility | Reobserve after change; separate interpretations |
| Retrieval/ranking order | Stable semantics for ties or declared randomization | Ordering, scheduling, conditional-wave inputs and limits | Repeats for nondeterministic policies |
| Tool timing/services | Isolated fixtures/stubs when matching real scope | Tool/environment versions, returned facts/errors, effect ambiguity | Timing/service blocks or repeated isolated execution |
| Tests/oracles | Fixed test/evaluator versions and environment | Flakes, retries, failing/unknown status, exact outputs and evaluator procedure | Re-evaluation with provenance; no silent replacement of failed grades |
| Adaptive Agents | Fixed initial conditions and policy | Decision history, observed information, actions, budgets and feedback | Whole-policy trials; dependent episodes are not independent cases |

Deterministic intelligence is a valuable stable substrate: freeze its identified results and coverage, then vary downstream retrieval/ranking/disclosure/model mechanisms. Determinism permits reproducible local oracles and helps expose stale reuse. It does not remove observation races, external dependencies, implementation bugs, or runtime cost variance.

### Exact current model/provenance limits

Model family/name, provider, exact revision, request configuration, local quantization, and serving runtime are different dimensions. ServingProfileIdentity has provider, served_model_alias, context_capacity, optional model_repository/model_revision, artifact_filename/hash, quantization, server_build, and template_reasoning_defaults. Its fingerprint is supplied text; construction does not attest that the endpoint ran those bits. The Qwen profile carries additional placement/cache/parallelism choices, while docs state that expected artifact SHA-256 is visible provenance rather than acquisition-time verification.

InteractionSource is a source/continuation discriminator, not an immutable model revision. The llama.cpp requested model alias is adapter state, outside ModelRequest. Provider-reported model identity is optional and capture-controlled. ModelSettings.thinking_enabled is not a reasoning-effort level or a reasoning-token budget. Portable temperature, top-p, seed, and such effort controls remain deferred.

Current ModelInteractionEvidence captures successful completed observations, not all failures, and duration is derived from wall-clock Timestamp subtraction. Benchmark elapsed measures use Stopwatch. A cost comparison should state timing boundaries and clock properties; these current measures are not automatically interchangeable.

**Legitimate claim when exact provider revision is unknowable:** outcomes were observed for the named route/alias under recorded requested settings and conditions during the stated interval, with revision/default uncertainty disclosed. Repeated trials can describe that observed service distribution; they cannot establish exact immutable model reproducibility or disentangle unobserved drift by naming a model family.

**Recommendation — ADR-0001 pressure, not serving redesign:** preserve requested, configured, reported, independently verified, and unknown facts distinctly at composition/observation boundaries. Promote new setting or provenance semantics only when a concrete consumer requires them; do not add universal model identity or capability negotiation here.

## U. Repository-intelligence evaluation

Repository intelligence can and should be evaluated independently of Agent success. E05 makes it LLM-independent and gives assertions identified semantics, dependencies, support, and coverage. An Agent's success is a separate usefulness test.

| Oracle/technique | What it can support | Limits that must remain explicit |
|---|---|---|
| Compiler/analyzer oracle | Declaration, resolution, import, typing or target facts under identified semantics | Toolchain/version/configuration and oracle bugs; semantic compatibility is required |
| Curated fixture | Precisely labeled relationships, ambiguity, unsupported features and expected coverage | Labels are partial unless their universe is explicitly exhaustive; curator errors possible |
| Synthetic repository | Controlled structures and combinations with known construction | Artificial distribution may not represent real repositories |
| Generated repository | Larger structured variations with generator-defined expected properties | Generator version/seed and its assumptions; generation does not guarantee independent truth |
| Differential analyzers | Disagreement localization and potential defects | Agreement is not proof when implementations share assumptions or bugs |
| Property-based generation | General invariants over many generated cases | Distribution and generator limits, not universal proof |
| Mutation testing | Sensitivity to meaningful changes and detection of stale/incorrect reuse | Surviving mutations can be equivalent or outside the contract |
| Metamorphic tests | Predictable relationships across transformed inputs | Transformation must preserve the relevant semantics; rename/import changes may not be neutral |

Declaration/reference, calls, imports, dependency, containment, failure-path, responsibility, possible-target, and exhaustive-implementation results have different propositions and oracle obligations. A syntactic reference oracle cannot automatically judge a responsibility claim. A runtime trace showing one call is evidence of a possible target; failure to observe a call does not refute a conservative possibility.

**Minimum DerivationDefinition requirement — interpretation of E05:** expose enough result vocabulary/semantics for an evaluator to know the proposition, relation direction, relevant assumptions/scope, and coverage obligations. Evaluation must know what counts as semantic equivalence between results from different implementations. A name such as “call graph v1” without defined may/must behavior is not sufficient.

**Recommendation — refinement, not a new oracle architecture:** make each implemented family's semantic contract evaluator-visible through authoritative documentation, test fixtures, and inspectable outputs/references. This extends no responsibility beyond E05; a machine-readable universal truth contract is unnecessary. Evaluator-specific oracles can consume those meanings and record their own limits.

The deterministically correct but useless analyzer must be discoverable: local evaluation may pass while task utility, maintenance economics, or available-consumer value remains negligible. That result should argue against eager construction or even continued support without invalidating the correctness result.

## V. Semantic qualification / coverage evaluation

Qualified knowledge is evaluated against what it claims, not against an imagined unqualified fact. Possible, necessary, conservative, approximate, ambiguous, unresolved, partial, and exhaustive do not form one ordered confidence scale.

Examples of different obligations:

- A possible-target set intended as a sound over-approximation must include all targets within its supported semantic universe; extra targets affect precision, not necessarily soundness.
- An explicitly partial discovered-target set cannot be judged incomplete as a contract violation unless the promised coverage is missing. Its usefulness may still be poor.
- A “no implementations” result requires the relevant closure/configuration to have been examined sufficiently under the definition. An empty result after timeout has no such force.
- An unresolved reference is a legitimate analysis result if unresolvedness is what was established, not a failed attempt to produce a falsely definite binding.
- Contradictory assertions under mutually exclusive configurations may not conflict under compatible scope; conflict evaluation must know those scopes.

**Evidence:** E05 explicitly assigns meaning to DerivationDefinition/result vocabulary and distinguishes semantic-result coverage from execution and disclosure coverage. The architecture already contains the required distinctions.

**Recommendation:** evaluators need inspectable qualifier/scope/coverage semantics and references to supporting observations. A global complete: bool or confidence score would lose distinctions within one execution. No additional foundational contract concept is needed; concrete result families must make the accepted contract usable.

**Uncertainty:** Some families may not be exhaustively testable against a complete oracle. Their evaluation should report bounded checks, counterexamples, and unsupported regions. Inability to prove arbitrary program properties is not evidence that the architecture must collapse qualified meanings into a scalar.

## W. Incremental-maintenance evaluation

The key experiment compares identical requested semantics over the same state-transition workload using different correct dependency/maintenance policies. It needs both correctness and economics.

**Correctness observations:** target snapshot/external state; knowledge selected for reuse; actual finalized dependencies and their roles; definition compatibility and applicability assessment basis; invalidations/rederivations; produced result semantics/coverage; graph-view state; independent/reference result and mismatch characterization. Distinguish missed invalidation, incorrect reuse, missing recomputation, stale projection, unsupported analysis, and failure to produce required knowledge.

**Efficiency observations:** semantic work requested versus executed; applicable results reused; recomputation avoided; unnecessary invalidation; dependency-record creation/comparison; reverse-index update/query work; persistence reads/writes; storage footprint; cache warmness; wall/CPU time when measurable; scheduling overhead and memory if relevant. Instrumentation overhead itself matters when fine tracking is being evaluated.

**Comparison rule — recommendation:** compare semantically equivalent result propositions and coverage, not necessarily identical artifact IDs or physical graph layout. A finer dependency representation can change derivation/knowledge identity. Full recomputation is a useful reference for maintenance correctness, but shared analyzer bugs mean agreement with it is not complete semantic correctness.

An edit sequence is part of the workload, not just its final snapshot. Two histories can yield the same final state but different cache reuse costs. Keep transitions and requested workloads referenceable; watcher events alone cannot establish the states. External configuration changes are also transitions even when repository bytes do not change.

**Economics:** include initial indexing and amortized repeated-maintenance costs under a declared horizon. Report the workload distribution: many tiny edits, broad configuration changes, cold starts, large graph-impact changes, and no-op observations can favor different strategies. A policy that only wins after unrealistic reuse does not “earn its complexity” universally.

**Architectural verdict:** E05 already separates correctness-bearing applicability from maintenance optimizations and explicitly calls for granularity economics. No universal incremental benchmark or cost API is required before implementation. The first slices must expose enough facts to tell reused, recomputed, failed, and unsupported work apart.

## X. Graph evaluation

Evaluate a graph view at three independent levels:

1. Relationship knowledge: proposition correctness, qualification and coverage under derivation semantics.
2. View mechanics: projection completeness relative to applicable backing facts; typed traversal correctness; stale-index detection; query latency; construction/maintenance/storage costs.
3. Consumer contribution: useful discovery, Context coverage/efficiency, task-class success and total system cost.

**Evidence:** E05 makes typed views first-class but rejects a universal repository graph and independent view authority. This lets a view be judged and replaced without redefining relationship truth.

To isolate one view, record which relationship families and compatible node domains it exposed, backing knowledge/coverage, traversal constraints, materialization state, and consumer use. A missing candidate may be caused by absent knowledge, an incomplete projection, an overly narrow traversal, or a consumer that ignored the view.

**Interaction example:** a call view may have no effect with a lexical-only retriever, help with graph-aware acquisition, and hurt under a ranker that overweights distant call neighbors. Preserve graph availability × retriever × ranker conditions and task strata. Removing a view can change both candidates and native evidence for already-discovered candidates; “unique candidates” alone understates its contribution.

**Recommendation:** separate the value of graph access from the cost of constructing/maintaining it. An ablation over a prebuilt view answers an access question; an end-to-end experiment including startup and maintenance answers a broader economic question. Neither should silently stand for the other.

## Y. Retrieval / RelevanceEvidence evaluation

E06's separation is experimentally valuable because original native observations survive interpretation. A lexical match score, graph path/distance, reference count, exact match, and semantic similarity remain available for alternate rankers, error analysis, and evidence contribution.

Independent retrieval evaluation can measure candidate recall/precision, discovery of judged-useful information, application cost, and marginal candidate/evidence contribution under fixed purpose and knowledge basis. It must define the relevance unit: file, occurrence, subject, assertion, or another referent. Overlapping candidate granularities cannot be counted interchangeably without declared evaluation mapping.

Gold relevant files are not universal truth about all useful information. Labels may be incomplete, task-relative, or based on one successful solution. Preserve unjudged candidates, oracle coverage, and alternative valid solutions. “Retriever did not return it” and “judged irrelevant” remain different.

**Cross-retriever comparison:** native scores need not be normalized. Compare outputs against a shared, appropriately scoped relevance criterion and common budgets, or feed preserved native evidence into the same ranker and compare downstream outcomes. Different discovery cost or candidate-count limits are experimental factors, not automatically fairness.

Native heterogeneity makes naive averaging harder, which is a strength: it prevents false commensurability. It creates practical work for evaluator mappings and ranker features; it does not require a universal relevance scale. Measurement direction, domain, mechanism version, query/application provenance, and qualifiers must be interpretable.

**Unique contribution:** retain candidate origins and observations from each application, including corroborating evidence on shared candidates. Leave-one-retriever-out comparisons should recompute ranking/selection under the declared protocol. Removing duplicate candidates alone cannot measure a retriever whose main value is corroboration or useful ranking evidence.

**Current limitation:** E20's acquisition_precision counts fixture-required successful read events divided by successful file reads; repeated required reads can contribute repeatedly. It is not generic candidate precision, information novelty, or rank-sensitive retrieval quality. Directory listings are a different operation. Keep its local meaning rather than promoting the field name.

## Z. Ranking evaluation

Candidate acquisition can be held fixed while rankers vary; E06 requires that possibility. Evidence must also be fixed, including provenance, qualifiers, query/application semantics, and all features actually consumed. If a ranker calls a live repository query or learned model, capture that dependency/realization rather than pretending only arithmetic changed.

**Exact retained comparison points:** information purpose and prior-information assumptions; candidate referents and equivalence/grouping; original evidence per candidate/application; ranker definition/model/configuration and tie rules; output order/ties/scores with their own meaning; evaluation cutoff/criterion; latency and other cost; resulting DisclosurePlan and downstream outcome for utility tests.

A ranking improvement does not imply better selection. Top-ranked candidates can be redundant; a lower-ranked test or governing document can be complementary. Compare local rank measures and actual selected coverage/cost separately. The compiler may ignore rank differences if hard constraints dominate.

**Recommendation:** do not replace native evidence with ranked scores, and do not freeze candidate acquisition implicitly inside a ranker API. Concrete ranking artifacts and persistence remain implementation-shaped. Learned-ranker training/evaluation splits and contamination controls are evaluator-specific requirements, not a new repository-intelligence responsibility.

## AA. Context / disclosure evaluation

E07 provides semantically distinct targets for selection, coverage, redundancy, representation, ordering, fidelity, compression, budgets, progression, synthesis, and strength preservation. Their tradeoffs are conditional on purpose, consumer, prior information, and resource policy.

| Evaluation target | Needed comparison basis | Independent utility/cost question |
|---|---|---|
| Selection | Fixed candidates/evidence/ranking/options and constraints | Which complementary information was chosen, and why did it improve task behavior? |
| Coverage | Explicit purpose/aspects, actual represented propositions and known limits | Is adequate coverage worth the tokens/latency? |
| Redundancy | Representation-relative overlap and current availability | Does repetition help this consumer or waste capacity? |
| Fidelity | Identified source/support and transformation promise | Does the model need the preserved detail for this task? |
| Compression | Matched support and declared loss; qualifiers/conflicts | Quality at stated cost, including reconstruction burden |
| Coherence | Relations and purpose made intelligible | Can this model use fragmented versus composite information effectively? |
| Budgeting | Hard capacity, policy ceiling, reserved/remaining capacity and actual cost | Is added Context worth its marginal cost? |
| Progressive disclosure | Initial/updated purpose, decision history and current availability | Does additional acquisition improve eventual success enough to justify calls/time? |

A more complete disclosure can be slower and less usable; a smaller one can omit a crucial exception; a faithful summary can add nothing beyond a signature; redundancy can aid one model and burden another. These are observations for specific comparisons, not violations of one universal Context utility function.

**Minimum semantics — recommendation:** target/referenceable support and plan/disclosure; transformation origin; preserved versus intentionally omitted information; purpose and consumer; prior availability; constraints versus preferences; estimated versus realized cost; criterion/evaluator and downstream correlation. Representation fidelity is not token count. Disclosure coverage is not repository semantic-result coverage.

### DisclosurePlan versus ContextDisclosure interventions

Holding DisclosurePlan fixed and varying materialization tests conforming implementations of its selected representation/transformation. If the plan allows a bounded task-focused summary, alternative summary realizations may be compared for faithfulness and cost under that same decision. Selecting a signature instead of a full definition changes the plan's representation choice.

Holding selected information fixed while varying final presentation ordering normally belongs to assembly and can preserve both plan and disclosure. If ordering encodes semantic relationships, precedence, temporal meaning, or qualification attachment, it is not merely movable decoration; the alternative must preserve that meaning or become a different transformation.

Holding exact ContextDisclosure fixed while varying assembly is expressly permitted. If capacity forces dropping a constituent, the experiment no longer holds exact disclosed information fixed unless it records a new plan/disclosure or fails the assembly. The current distinctions are sufficiently precise semantically; a future API that exposes only rendered strings would foreclose them.

## AB. Synthesis / semantic-strength evaluation

Synthesis can be evaluated locally against identified support for source fidelity, provenance, preservation of material assumptions/conflicts, and claims no stronger than justified. Compression benefit includes token/cost change and information lost; downstream usefulness requires the consuming model/task.

**Local test examples — recommendation:**

- Invariant tests: source tagged possible never renders as definite without an identified strengthening derivation; a partial result never becomes an “only/all” claim.
- Metamorphic tests: introducing a conflicting applicable source must not silently leave an unqualified one-sided summary; weakening coverage must not retain an exhaustive conclusion.
- Semantic-contract tests: a family-specific structured projection preserves relation direction, scope, and may/must distinctions; a lossy transformation preserves mandatory qualifications.
- Provenance checks: every asserted claim maps to identified support or an explicit synthesis process; removed or changed support triggers the appropriate realization/reassessment behavior.

These can be exercised with deterministic fixtures and constrained transformations. Source-link presence alone does not prove entailment, and string searches for words such as “possible” cannot validate arbitrary language. Negative wording, scope shifts, implicit exhaustiveness, and conflict suppression need semantic judgments appropriate to the representation.

**Verdict:** the architectural invariant is practically testable in bounded families and falsifiable by counterexamples. General natural-language faithfulness is not completely decidable through one generic checker. That limit does not make the invariant meaningless or require a universal Claim object. If a specific transformation cannot expose what it promises to preserve, that implementation's contract is underspecified and should not claim validated fidelity.

Purpose-relative synthesis stays in Context. A synthesis evaluator's judgment stays evaluation. Neither is promoted to repository DerivedKnowledge by determinism, model agreement, or human approval. Reusable repository assertions, when independently established under E05, have their own derivation contract.

No generic synthesis-evaluation framework is required now. A concrete synthesizer needs explicit transformation intent, support, qualifications, observed output, and bounded tests/judgments before strong fidelity claims.

## AC. Model-input assembly evaluation

The accepted architecture separates selected information from presentation strongly enough to compare order, framing, formatting, prompt instructions, placement, and allocation. It deliberately permits different identified policies to assemble the same disclosure.

**Experimental controls:** exact disclosure; fixed task and consumer; other instructions, Tools, conversation state and capacity, except deliberately varied dimensions; adapter/model settings and relevant defaults; representation-to-request correspondence. Instruction changes can be an assembly treatment but are not purely placement effects.

**Retain:** exact ModelRequest value or adequate authorized reconstruction; assembly policy/version; relevant tokenizer and model capacity where used; omitted/unavailable components and failures; provider translation/version/profile; response and evaluation realization. Assembly policy need not own provider transport serialization to record the request it handed to that boundary.

**Current implementation:** Prompt has a single content string and role. There is no Context compiler or generic assembler. Direct invocation can retain an exact ModelRequest in a local harness, but ModelInteractionEvidence is not a lossless request store: prompt/schema capture is optional; continuation is a presence flag; provider extension values are replaced by a type name. Even fully captured present fields do not establish the provider's effective defaults.

**Recommendation:** preserve the assembly boundary and explicit exact-input retention only at the replay strength and disclosure authority required. Do not add a request ID merely to correlate a value; a containing realization reference or content identity with defined semantics can suffice. Do not bypass capture policy by placing sensitive payloads in ungoverned evaluation metadata.

## AD. End-to-end outcome evaluation

Eventual coding evaluation must correlate a task/case, initial state and environment, policy/treatment, actual execution, patch/result artifacts, validation/evaluator applications, resource observations, and relevant authority/admission/effect evidence. It need not redesign Agent architecture.

| Role | Examples | Required distinction |
|---|---|---|
| Output/outcome | Patch, completion status, escalation, final artifact | Model text is not necessarily an applied patch or AgentResult |
| Behavioral measurement | Visible/hidden test results, regression count, observed failures | A pass count describes a test scope, not all correctness |
| Evaluator judgment | Patch correctness, minimality, maintainability, security correctness | Rubric/oracle and uncertainty are explicit |
| Constraint | Time/token ceiling, authorized effect scope, required behavior | A constraint violation cannot silently be offset by speed or another score |
| Consumption | Runtime, tokens, model/Tool calls, storage/indexing cost | Boundary, units, missingness and amortization are explicit |
| Authority assessment | Proposed actions, actual admissions, prevented/observed effects | Voluntary model compliance differs from framework enforcement |

E18's _validate_fixture_behavior executes the known fixture function and checks non-target file contents; it is not a hidden-test suite or general patch evaluator. The allowed patch grammar is deliberately narrow. E19 distinguishes patch conformance, application, behavioral validation, provider failure, and ungrounded final response, but its categories are local.

**Recommendation:** keep raw output, canonicalization, applied artifact/state, test/evaluator evidence, and judgment separate enough to re-evaluate. Preserve human assistance, repair/correction turns, and oracle feedback as parts of the evaluated policy. “Autonomous task completion” is invalid if an undisclosed host oracle steered the run.

## AE. Marginal contribution and interaction effects

“Graph retrieval improved performance by 5%, so it is worth it” omits the denominator, cases, comparison design, uncertainty, changed costs, and interacting mechanisms. The same average can hide gains on graph-heavy tasks and regressions on localization tasks.

**Conceptual comparisons — recommendation, experimental design:**

- Ablation or leave-one-component-out evaluates removal under a stated fallback and remaining policy. It can expose unique usefulness but is conditional on those other components.
- Matched comparisons hold cases, repository/external state and declared budgets comparable; realization variation is retained.
- Factorial conditions preserve combinations such as graph × retriever × ranker, or representation × model, so complementary effects remain discoverable.
- Local fixed-input replay identifies contribution at one boundary; end-to-end trials assess the full pathway, including altered candidates, disclosure and costs.

Retain task-class membership, joint factor assignments, candidate/evidence contributions, selection/disclosure changes, realized resources, and per-case/per-run outcomes. A retriever may add no unique candidates but supply evidence that enables ranking; a graph may help only when the ranker can interpret path semantics; synthesis may help a small model but harm a stronger one.

Do not assign a universal additive “credit” to every component. Architectural interfaces should expose replaceable mechanisms and relevant input/output evidence, not prescribe an attribution algorithm. Report negative and null contributions as legitimate results; a correct expensive mechanism may be disabled, made lazy, or abandoned if its measured role does not justify its cost.

## AF. Multi-objective efficiency

Preserve typed outcomes for semantic correctness, task success, latency, input/output tokens, indexing and maintenance cost, storage, model calls, Tool calls, and semantic fidelity. Additional resource measures are justified by the question, not mandatory on every object.

Later policies can compare Pareto alternatives, quality at a budget, cost-effectiveness, or task-specific aggregates if underlying measurements and constraints survive. Dominance itself depends on comparable units/scope and uncertainty; missing cost must not be interpreted as zero.

Separate cold construction, warm incremental maintenance, per-query retrieval, per-disclosure synthesis/assembly, and end-to-end cost. Shared indexing can be amortized under a declared workload horizon; it should not vanish from a graph-economics claim. Monetary estimates need their own pricing assumptions/version rather than replacing physical resource counts.

**Verdict:** aggregation belongs to comparison/decision policy outside foundational outcome semantics. This matches E05/E06's rejection of universal truth/relevance scores and E07's multidimensional cost and constraint distinctions.

## AG. Leakage / governance

Evaluation-only information can invalidate a comparison if it enters consumer-visible repository intelligence, Context, prompts, Tool results, or persistent state.

Protected examples include expected answers, benchmark solutions, hidden tests, gold relevant files, evaluator labels/rationale, and blinded treatment labels. Ordinary task requirements and deliberately disclosed tests are not automatically protected. The distinction is experiment-specific and must be declared.

**Evidence:** E04 separates capture and model Tool disclosure from authority. E07 says planning/possession does not authorize disclosure. E20 asserts initial task strings omit target paths/filenames. E18's host grounding rule nevertheless consumes fixture-known required paths to decide whether to admit a final patch or send a correction.

**Interpretation:** Existing boundaries allow evaluation-private information to remain outside the consumer path. They do not implement a general information-flow guarantee. Initial-prompt secrecy tests alone cannot establish absence of leakage through indexes, errors, Tools, later prompts, continuation, caches, logs, or oracle-driven control flow.

The fixture grounding correction is intentional host assistance. Even without revealing paths, feedback that a final answer is premature depends on gold required reads. That is a form of oracle-informed intervention that must be part of the evaluated controller/policy, not described as wholly unassisted acquisition. It is not evidence of a current unauthorized disclosure defect.

**Recommendation — evaluation semantics/design:** identify evaluator-only inputs and permitted consumer inputs; separate their roots/views/projections in a concrete harness; retain provenance of any authorized feedback or assistance. Excluding hidden tests from model-facing source reads is insufficient if their facts have already entered shared DerivedKnowledge or a retriever index.

**Recommendation — implementation:** use bounded explicit projections and tests of model-facing inputs/Tool results for the concrete experiment. No new authority framework is required merely to protect fixture labels. If evaluator-only data must cross reusable shared storage/Tools with different authority, existing governance pressure should be promoted deliberately.

Treatment metadata used for blinded human/model review must stay out of the review input when the design requires blinding. The model inevitably sees the actual representation or Tools being tested; blinding metadata does not make its treatment experience invisible. Pretraining contamination cannot be excluded by repository boundaries alone and remains an external validity uncertainty.

## AH. Human / model judgment

Subjective outcomes require identifiable assessment procedure and role, not a universal human-rating type. Retain target artifact/realization, rubric/version, information disclosed to the evaluator, evaluator role and suitably protected identity/reference, blinding condition, judgment, rationale if appropriate, abstention, and adjudication lineage.

Multiple raters' judgments must remain separately attributable. Disagreement is evidence, not noise to erase. A later adjudication should reference the earlier judgments without overwriting them. Repeated ratings of one artifact are not repeated task executions.

An LLM-as-judge is an evaluator whose own model/request/response/configuration and uncertainty may matter. Its output is a judgment, not truth; shared model biases, answer-position effects, rubric sensitivity, and leakage can affect it. When model interaction is used to judge, reuse ModelInteraction Evidence and attach the evaluator meaning outside that boundary.

**Evidence:** E21's closed supervisor-review outcomes show a local typed judgment need, but no rater/rubric/blinding semantics are implemented there. E16 mentions future blind supervisor review as experiment sequencing, not a framework capability.

**Verdict:** generic ownership of “judgment against identified criterion” belongs to Evaluation. Specific rubric formats, rater management, adjudication methods, blinding mechanics, and judge calibration remain evaluator-specific infrastructure until shared concrete pressure earns promotion.

## AI. Evidence / Attempt reuse analysis

| Existing concept | Appropriate evaluation reuse | Inappropriate reuse |
|---|---|---|
| InteractionAttempt | Reference one Runtime-managed lifecycle and input/Conversation attribution | Treat as analyzer execution, Tool attempt, whole Agent Run, or evaluation trial |
| InteractionAttemptTerminalEvidence | Reuse immutable terminal fact and stage | Treat stage as root cause, or success as semantic/task correctness |
| ModelInteractionId | Reference one invocation occurrence, including repeated same-request calls when observed | Identify a case/treatment or a multi-call realization |
| ModelInteractionEvidence | Consume captured request/response facts, usage/termination/profile and manifest | Assume lossless replay, complete failure population, or current authority |
| EvidenceId | Identify an immutable observation | Use as universal outcome identity or erase evaluator meaning |
| ExecutionInspector / ModelInteractionInspector | Collect bounded process-local observations | Treat retention as durable storage or an automatic cross-inspector join |
| Command events/results | Consume bounded output, duration, exit facts and loss/truncation indicators | Treat best-effort events as a complete trace or proof an external effect did not happen |
| Conversation / Message identity | Reference communication and its source | Use conversation history as all actual model inputs or as a generic execution lifecycle |

**Exact implementation gaps, E11–E14:** CapturedModelRequest retains role, captured prompt, portable settings, continuation presence, provider-settings type, and captured Tools. CapturedModelResponse retains normalized output and continuation presence. ProviderExchange contains provider, captured response ID, and captured model string. It does not contain a complete effective request/response, failure stage, timings/cache diagnostics, or original continuation value.

LlamaCppInteraction creates an interaction ID before validation, but sends its observation only after response parsing succeeds. Validation, transport, malformed-response, cancellation, or earlier failure paths do not publish that ID through a failure observation. Runtime can separately report an invocation-stage failure when observed, but it does not hold the model occurrence ID.

The completed-observer callback is synchronous and unguarded in LlamaCppInteraction.send. **Inference from source:** if that callback raises, a provider response may have been received while the caller sees an exception; Runtime would classify the boundary as invocation failure. This was not executed here. Any evaluation depending on that path must distinguish observation failure from model/provider failure.

**ADR discrepancy:** E04 describes structural failure facts and broader controlled provider/settings/exchange capture while also declaring its three scoped phases implemented. E13's package documentation and source describe the narrower completed-response implementation. The safe reconstruction is that the current observation subset is implemented; the broader accepted capture language is not fully represented. No compatibility or architectural change is made by this dossier.

**Recommendation:** reuse existing factual observations and canonical core identity/time values. Keep experiment correlation/assignment and evaluator semantics above them. Supply concrete missing adapters/records only when a harness requires them; never force new meanings into InteractionAttempt merely because it has IDs and timestamps.

## AJ. DerivedKnowledge boundary

Correctness judgments, metrics, comparison results, statistical estimates, benchmark outcomes, human ratings, and resource measurements are generally about an evaluation, execution, evaluator, or population. They are not repository-relative semantic intelligence under E05.

An analyzer can establish repository-relative knowledge that a function has a property under explicit semantics. An evaluator can judge whether that analyzer's result meets its contract. These are different targets and epistemic roles even when both refer to the same source.

A narrow exception is possible: a repository Derivation might consume repository test artifacts to establish a precisely defined repository fact, such as a declared test relationship or a property under stated assumptions. That work must independently satisfy ADR-0002 jurisdiction and semantics. It is not permission to relabel arbitrary benchmark scores as DerivedKnowledge.

**Verdict:** Evaluation ownership helps prevent DerivedKnowledge from becoming a universal evidence/claim container. It also prevents all purpose-relative synthesis from being promoted merely because it was judged faithful. No foundational Claim/Belief/TruthRecord layer is needed.

## AK. Historical evaluation versus applicability

An observation that a treatment achieved a particular outcome on benchmark version Y, model route X, and repository/architecture revision Z remains an observation of that historical experiment when any component changes. Its relevance to predicting current performance may decline. That is external validity, transportability, or scope of inference, not automatically ADR-0002 knowledge applicability.

DerivedKnowledge applicability asks whether dependencies of an immutable repository assertion are satisfied under compatible semantics in another state. Evaluation generalization asks whether evidence from a population and conditions supports a new prediction or decision. Similar attention to provenance does not make them the same predicate.

Raw measurements may later be found faulty or an oracle may be corrected. Preserve the original observation with its limitations and issue a new evaluation/correction referencing it; “historically recorded” does not mean the judgment was true. New rubrics or statistical methods can yield new comparisons over unchanged raw outcomes.

**Recommendation:** separate experiment/design, realization observations, evaluator applications, and later comparison/inference. A later comparison can select a different population or method, but must identify its selection, assumptions and exclusions. Neither comparison nor experiment needs a universal lifecycle object for this distinction to hold.

The analogy to repository state versus DerivedKnowledge, or evidence versus ranking, is limited: it illustrates observation versus interpretation. It does not justify importing repository identity/applicability or ranking scores into evaluation conclusions.

## AL. Architecture-family comparison

These are qualitative comparisons of ownership choices, not numeric scores. “Infrastructure only” has two readings: legitimately local harness implementation, or absence of evaluation-owned semantics. The former can realize the recommended hybrid; the latter cannot support reliable reusable comparisons.

| Family | Causal attribution and isolation | Reproducibility and adaptive work | Ownership/semantic clarity | Complexity, storage, ontology risk |
|---|---|---|---|---|
| A. Existing artifacts + ad hoc harnesses | Good for a bounded explicitly designed experiment; fragile when assignment/controls are implicit | Can retain exact fixtures; cross-harness joins and adaptive continuation often become accidental | Preserves layers if evaluation meaning stays explicit locally; fails if “infrastructure” denies ownership | Lowest initial cost; duplication and incompatible meanings grow with reuse |
| B. Minimal Evaluation responsibility | Makes case/condition/realization/criterion meaning explicit; does not itself prove causality | Stable comparison references and typed results can support later reanalysis | Strong if it correlates rather than owns layer artifacts | Moderate conceptual cost; concrete models can remain small and local |
| C. Universal EvaluationEpisode | Convenient single-record navigation, but one pipeline shape hides optional/parallel/adaptive structure | Retains much data if filled; encourages duplication, overcapture and fictitious completeness | Cross-domain ownership and lifecycle coupling are poor | High storage/retention pressure; high god-object risk |
| D. Trace-centered | Strong observed execution ordering; weak intended contrast, oracle and comparison meaning | Helps replay diagnostics, but sampled/dropped spans and missing semantics limit inference | Tends to overload observability with experimental design | Instrumentation/backend cost can precede need; encourages event ontology growth |
| E. Explicit universal causal DAG | Can encode hypotheses, but risks mistaking execution/reference edges for causal assumptions | Flexible on paper; adaptive counterfactual validity still needs real design and observations | A universal edge meaning would erase experiment-relative semantics | Highest foundational complexity and speculative ontology growth |
| F. Minimal semantics + layer evidence + optional traces + local causal structure | Best fit for intended contrasts, observed mediators and honest uncertainty | Supports local replay and adaptive trials without claiming unavailable counterfactuals | Preserves existing ownership; evaluation owns assessment/comparison meaning only | Can start as a small harness; storage bounded by purpose/replay/capture requirements |

| Family | Multi-objective outcomes | Likely failure under this repository's pressure |
|---|---|---|
| A | Possible with typed local records, as E17/E21 show | Later comparisons silently mix fixture versions, budgets or evaluator meanings |
| B | Naturally preserves heterogeneous criterion-specific results | Overformalization into mandatory classes despite a simple consumer |
| C | Can carry many measures but encourages a giant metrics bag | Payload growth and an overall episode score conceal distinctions |
| D | Operational metrics easy; correctness/judgment semantics remain external | Latency spans mistaken for evaluation coverage or causal contribution |
| E | Can attach outcomes but does not define their validity | A graph offers apparent rigor without controlled assignments or usable oracles |
| F | Preserves typed local measurements and later policy-specific comparison | Requires discipline to keep correlation resolvable and semantic records small |

**Recommendation:** F, implemented initially through bounded experiment-local structures. This is B's minimal semantic responsibility with optional supporting mechanisms, not six new subsystems. A is sufficient operationally when it implements those semantics honestly; C/D/E are not justified as foundations.

## AM. Adversarial findings

Finding counts: FATAL 0; MATERIAL 0; REFINEMENT 7; IMPLEMENTATION-SHAPED 4.

No accepted boundary was found to prevent rigorous controlled evaluation. No open implementation mechanism was promoted into an architectural defect. The ADR-0001 conformance discrepancy is real, but its smallest correction is implementation/claim alignment within an already sound boundary, not a new architecture. Thus it is IMPLEMENTATION-SHAPED under the requested classification definitions.

The strengths established in C/D/F are not counted as defects. The following findings are the complete counted set; related discussion elsewhere expands these findings rather than adding uncounted findings.

### AM-R1 — Intended comparison must remain distinct from observed execution

- **Classification:** REFINEMENT.
- **Evidence:** E03, Remaining preimplementation research and evidence constraints, requires controlled comparison and cross-layer correlation but leaves integrated evaluation architecture open. E02 already recognizes Evaluation; E06 recognizes fixed cases/treatments; E23 B-0015/B-0016 distinguish judgment from observation.
- **Failure scenario:** Two reports have identical task labels and different graph settings, but one uses a larger Context budget and a different ranker. A later analyst calls the success difference a graph effect.
- **Why existing semantics are insufficient alone:** Artifact identity/provenance records what existed or occurred, not which differences were intended, which factors were controls, how assignments occurred, or what population was compared. Existing Evaluation ownership permits the missing semantics; it does not yet specify them.
- **Smallest correction:** make a future experiment's target, intended contrast, fixed basis, assignment/realized-condition distinction, criterion and result population explicit. A local design record is enough.
- **Ownership:** already recognized Evaluation responsibility; a genuinely evaluation-owned future ADR is justified only for reusable comparison/assessment semantics. Experimental-design details remain local.
- **Implementation-blocking?** no. Required before claiming a controlled integrated comparison, not before deterministic repository intelligence.

### AM-R2 — Case, condition, realization and evaluator application need distinct reference scopes

- **Classification:** REFINEMENT.
- **Evidence:** E06, Evaluation, progressive disclosure, and authority, permits evaluation-case identity without runtime need identity and mentions stable treatment identity. E14 InteractionAttempt has Conversation/message attribution. E17 BenchmarkCase combines workload and settings for its narrow purpose; E22 has no general models.
- **Failure scenario:** Changing model creates a new “case,” preventing paired analysis; or three ratings of one patch are counted as three independent coding trials.
- **Why existing semantics are insufficient alone:** A Task/message is not the comparison basis; ModelInteractionId and InteractionAttemptId have narrower occurrence meanings; EvidenceId identifies an observation, not its experimental assignment.
- **Smallest correction:** define scoped, versioned comparison references and distinct realization/evaluator-application associations. Do not require global IDs or new lifecycle classes.
- **Ownership:** Evaluation responsibility and ADR-0003 refinement of the case-identity wording.
- **Implementation-blocking?** no. Preserve ordinary references now; settle concrete models with a real harness.

### AM-R3 — Snapshot equality is not a complete fixed-intelligence/replay claim

- **Classification:** REFINEMENT.
- **Evidence:** E05, External semantic dependencies and observation; Repository-intelligence capability boundary; Two graph families; E06 retrieval planning. E03 explicitly separates observation, interpretation, retention and replay strength.
- **Failure scenario:** Retriever B lazily derives additional relationships over the same snapshot and appears to beat A; or a retained knowledge hash cannot reconstruct evicted support.
- **Why existing semantics are insufficient alone:** Snapshot identity fixes included repository state, not available intelligence/coverage, external interpretation, view materialization, caches, or retained executable/input closure.
- **Smallest correction:** record/fix the evaluated knowledge and observation basis plus relevant availability and cost conditions; state replay strength and retention limits. Reuse existing identities/values rather than inventing a universal intelligence/environment snapshot.
- **Ownership:** ADR-0002/ADR-0003 preservation and B-0002 pressure; experimental capture is implementation infrastructure.
- **Implementation-blocking?** no. The first substrate must retain the accepted dependency/observation distinctions.

### AM-R4 — Representation comparisons cannot generally reuse one unchanged DisclosurePlan

- **Classification:** REFINEMENT.
- **Evidence:** E07, Disclosure planning is conditional composition, explicitly couples selection and representation; Constraints, budgets, and disclosure artifacts makes the plan select representations/transforms; Planning versus model-input assembly permits same-disclosure presentation variants.
- **Failure scenario:** A “fixed plan” selects a full definition, but treatment B substitutes a summary and calls it only a materializer change. An apparent representation gain includes unrecorded information loss.
- **Why existing semantics are insufficient alone:** “Selected information” has no automatic independent artifact boundary, and candidate equality does not establish equivalent represented information. The accepted plan is intentionally more specific.
- **Smallest correction:** pair distinct representation plans against an explicit shared support/information constraint, or compare only conforming realizations of one selected transformation. Keep exact-disclosure ordering in assembly.
- **Ownership:** ADR-0004 interpretive refinement; experiment-local pairing is implementation-shaped.
- **Implementation-blocking?** no. No change to the accepted coupling is required.

### AM-R5 — Adaptive replay and model-utilization attribution need bounded claims

- **Classification:** REFINEMENT.
- **Evidence:** E06 changed-purpose/progressive acquisition semantics; E07 prior availability is not comprehension; E18 model-dependent cycles and stateless follow-up reconstruction.
- **Failure scenario:** An earlier disclosure is replaced, but the old model-generated later purpose and retrieval are replayed as though they would still occur. A failure is then confidently attributed to the model “ignoring” correct Context.
- **Why existing semantics are insufficient alone:** References and observed order do not establish counterfactual continuation or internal model causation. Model self-reports and identical later artifacts cannot repair this.
- **Smallest correction:** distinguish conditional local replay from regenerated policy trajectories; retain decision inputs/policy and causal predecessors where needed; report utilization failure as an observation with unresolved cognitive cause.
- **Ownership:** ADR-0003/ADR-0004 preserved seams plus Evaluation experimental-design/inference responsibility.
- **Implementation-blocking?** no. No foundational trajectory or causal-DAG ontology follows.

### AM-R6 — Qualified result contracts must be usable by evaluators

- **Classification:** REFINEMENT.
- **Evidence:** E05, DerivationDefinition/result vocabulary and Semantic-result coverage, completeness, and absence; E07 semantic-strength invariant.
- **Failure scenario:** A conservative possible-call relation is scored false because one execution trace did not call it; a partial analyzer passes tests then is treated as exhaustive.
- **Why existing semantics are insufficient alone:** The accepted architecture names the required meanings, but a concrete family with only opaque “CALLS” outputs would not expose enough interpretation. That is a preservation obligation for design, not a demonstrated present model defect.
- **Smallest correction:** expose/document the implemented family's propositions, assumptions, supported universe, and coverage obligations; preserve them through projection/synthesis and test with compatible oracles.
- **Ownership:** ADR-0002 and ADR-0004 refinement; concrete oracle/test design is implementation-shaped.
- **Implementation-blocking?** no at the architectural level; a slice cannot honestly publish a result before defining that result's meaning.

### AM-R7 — Evaluator-private data and oracle assistance must remain explicit

- **Classification:** REFINEMENT.
- **Evidence:** E04/E07 disclosure does not confer authority; E18 _ground_final_response uses required_evidence_paths; E20 tests initial task secrecy; E23 B-0018 preserves disclosure/minimization pressure.
- **Failure scenario:** Hidden tests or gold relevant files enter a shared index/Tool view; alternatively, gold-driven corrective feedback improves a run that is reported as unassisted.
- **Why existing semantics are insufficient alone:** Capture controls and initial-prompt checks do not prove end-to-end information-flow separation, and experiment labels do not describe feedback policy.
- **Smallest correction:** declare evaluator-only inputs and allowed feedback, bound consumer projections, preserve assistance as policy/treatment evidence, and test leakage at the concrete harness boundaries.
- **Ownership:** Evaluation responsibility with ADR-0004 disclosure refinement; governance remains existing pressure, not a newly designed framework.
- **Implementation-blocking?** no. Required when protected oracle data and consumer execution first coexist.

### AM-I1 — Current model observation omits failed realizations and can conflate observer failure

- **Classification:** IMPLEMENTATION-SHAPED.
- **Evidence:** E04, Interaction occurrence and Evidence, describes failure-stage/category facts and reports scoped phases implemented. E11 ModelInteractionObservation requires a response. E12 LlamaCppInteraction.send invokes its observer only after successful normalization and does not catch callback exceptions. E14 Runtime reports an outer invocation stage.
- **Failure scenario:** A model comparison retains only completed Evidence, losing timeouts and malformed responses; a capture callback failure is scored as a model failure despite a received response.
- **Why existing semantics are insufficient alone:** There is no provider-failure observation carrying the locally created occurrence ID; a Runtime stage does not identify the nested cause. The broad ADR completion wording cannot be used as evidence that these fields exist.
- **Smallest correction:** for a concrete evaluation, retain all assigned realizations and boundary-specific failure facts through an explicit harness/observation seam; reconcile ADR implementation-status claims in separately authorized work. A future provider observation extension should remain within ADR-0001 and preserve execution/observability ownership.
- **Ownership:** ADR-0001 conformance/implementation; local failure accounting in Evaluation infrastructure.
- **Implementation-blocking?** no for initial repository intelligence. Blocks claims that current completed Evidence alone represents a complete model-trial population.

### AM-I2 — Current Evidence is neither exact-request storage nor an automatic cross-layer join

- **Classification:** IMPLEMENTATION-SHAPED.
- **Evidence:** E13 CapturedModelRequest stores conversation_present and provider_settings_type; ProviderExchange has only provider/response_id/provider_model; E14 attempt attribution has no ModelInteractionId; inspectors are separate process-local collections.
- **Failure scenario:** Two concurrent identical requests are matched to attempts by time or content; later replay assumes the retained request includes continuation or provider extension values that were discarded.
- **Why existing semantics are insufficient alone:** Omitted/redacted information is unreconstructable, and separate identities lack an explicit association. Future provider extension values cannot be recovered from a type name.
- **Smallest correction:** composition-owned correlation and authorized exact-input/reference retention for the promised replay strength; preserve capture manifests and unavailable facts. Do not add arbitrary evaluation metadata to ModelResponse or broaden InteractionAttempt.
- **Ownership:** ADR-0001 capture/correlation pressure plus implementation-shaped evaluation adapters.
- **Implementation-blocking?** no. Required before the affected replay/concurrency claim.

### AM-I3 — Model/profile equality and cost measurements are weaker than their labels can suggest

- **Classification:** IMPLEMENTATION-SHAPED.
- **Evidence:** E11 ModelSettings fields; E12 adapter-owned model alias; E16 optional caller-supplied ServingProfileIdentity, profile defaults and unverified expected SHA-256; E13 wall-clock-derived duration; E17 Stopwatch and benchmark total-duration semantics.
- **Failure scenario:** Same request/profile label is treated as the same inference configuration despite changed defaults or endpoint artifacts; total request throughput is compared with decode speed; setup-inclusive duration is called model latency.
- **Why existing semantics are insufficient alone:** Configured/reported/verified identity are not automatically equivalent; absent sampling controls are unknown; different clock and boundary scopes measure different quantities.
- **Smallest correction:** retain explicit known settings, provenance source/strength, drift unknowns, clock/measurement boundary and environment. Add controls only when supported and required by a concrete experiment.
- **Ownership:** ADR-0001 refinement pressure and implementation-shaped ModelBenchmark/evaluation composition; no serving redesign.
- **Implementation-blocking?** no. Limits current reproducibility and economic claims.

### AM-I4 — Existing acceptance artifacts are useful local observations, not a general comparative substrate

- **Classification:** IMPLEMENTATION-SHAPED.
- **Evidence:** E18 fixture constants and selection_stress_measurements; E19 run_acceptance temporarily replaces Tool class execute methods, report fixture ID is a label, _message_payload omits IDs, run timing includes setup/status/cleanup; E20 repeated-read precision; E26 historical reports.
- **Failure scenario:** Two different fixture revisions named selection-stress are paired; repeated required reads appear precise despite no new information; concurrent harness calls cross-contaminate monkeypatched counters; local duration or success is generalized to repository retrieval quality.
- **Why existing semantics are insufficient alone:** The schema is intentionally fixture-specific, not versioned comparison semantics or concurrency-safe reusable instrumentation. Stored path structure does not identify exact fixture bytes/analyzer/model state.
- **Smallest correction:** retain fixture/procedure revision, scoped realization references, declared measurement meanings/cost scope and isolated collection in a future comparative harness. Preserve these reports as historical evidence rather than migrating them into universal records.
- **Ownership:** implementation-shaped experiments/Evaluation infrastructure; B-0002 pressure only for future integration.
- **Implementation-blocking?** no. Blocks broad causal claims based solely on these artifacts.

## AN. Minimum strong evaluation architecture

The minimum is a responsibility contract, not a package/API design:

    experiment intent and comparison basis
        -> case + assigned condition + realization reference
        -> references to layer-owned artifacts and execution observations
        -> evaluator applications and typed outcomes/judgments
        -> later, separately identified comparison/inference

The arrows describe associations, not a mandatory runtime pipeline. An analyzer-only fixture may omit most layers; a model trial may have one request; an adaptive coding trial may have many branches and changing state.

### Minimality test: semantic necessity and correct reuse

| Candidate concept | Distinction it represents | What becomes invalid without the distinction | Can existing concepts represent it correctly, and would reuse overload them? |
|---|---|---|---|
| EvaluationCase | Stable/versioned assessment opportunity or problem basis | Pairing and regression comparison can mix changed problems | Existing fixture/task values plus scoped key can represent it; a ConversationMessage or InformationNeed alone cannot own the full basis |
| Treatment | Intended experiment-relative variation | A configuration difference is mistaken for an isolated cause | Local configuration plus explicit design can represent it; adding treatment ownership to repository/provenance values would overload them |
| EvaluationRun/realization | One application of case/condition protocol | Repetitions, failures, repeated grading and denominators become confused | Scoped execution correlation can represent it; InteractionAttempt/Agent Run alone has different or narrower meaning |
| Outcome | What resulted at a stated evaluated boundary | Response, patch, terminal status and correctness become conflated | Reuse existing outputs/results as targets; add evaluation associations without redefining ModelResponse or DerivedKnowledge |
| Measurement | Observation with defined quantity/procedure/scope | Units, missingness, denominators and costs become incomparable | Reuse typed usage/duration/test facts; no universal metrics dictionary required |
| Judgment | Assessment under an identified criterion | A grader's opinion becomes unqualified truth | Local typed evaluator result suffices; execution Evidence cannot acquire criterion semantics automatically |
| Evaluator | Procedure/role producing an assessment | Different graders/rubrics are silently pooled | Existing callable/tool/human role can implement it; evaluation retains its meaning/version without a universal protocol now |
| Oracle | Reference or rule supporting assessment | Partial, incompatible or leaky ground truth is treated as universal | Family-specific fixtures/analyzers/rubrics suffice; no universal repository truth object |
| Experiment | Intended design, units, controls, assignments and protocol | Observational records are mistaken for a controlled study | A local manifest/document plus references suffices; Trace cannot infer intent |
| Comparison | Later interpretation across selected results | New methods overwrite raw observations or silently change populations | A report/analysis artifact suffices; ranking and DerivedKnowledge do not own this meaning |
| Trajectory | Related adaptive decisions/observations within a realization | Natural continuation is confused with forced replay | Existing future execution references or experiment-local sequence/partial order suffice; no foundational Agent ontology |
| Intervention | The targeted change in a treatment assignment | “One factor” loses a defined target and pathway | Treatment/design semantics suffice; no separate universal Intervention object needed |
| Causal edge | A study-relative dependence or causal hypothesis | Counterfactual assumptions remain hidden when that study needs them | Ordinary design/reference/trace links plus explicit assumptions suffice; execution dependency must not be relabeled as causal proof |

### Minimality test: identity, persistence, universality, and timing

| Concept | Independent identity needed? | Persistence needed? | Universal or evaluator-specific? | Architecture versus infrastructure; must exist before initial implementation? |
|---|---|---|---|---|
| EvaluationCase | Stable scoped reference/version; no mandatory nominal entity | When reusing/comparing later; immutable fixture reference may suffice | Common distinction, heterogeneous content | Semantic basis recognized; concrete class/store not needed now |
| Treatment | Scoped variant/condition reference when joining runs; no global identity | Retain design/config for later comparisons | Experiment-relative factors | Semantic distinction required for comparisons; no initial framework type |
| EvaluationRun/realization | Distinct occurrence key for repetitions/joins | When evidence/outcomes outlive execution | Common occurrence distinction, protocol-specific shape | Preserve execution correlation; no generic lifecycle promotion prerequisite |
| Outcome | Referenceable under target/realization; separate ID only for independent use | For regrading/comparison as required | Heterogeneous layer/evaluator values | Do not erase types; no universal outcome class now |
| Measurement | Usually nested scope/key enough | Retain when conclusions depend on it | Typed quantity/procedure-specific | Semantic meaning/units required when measuring; instrumentation can defer |
| Judgment | Separate reference when multiple/revised judgments exist | Needed for review/adjudication lineage when retained | Evaluator/rubric-specific | Evaluation owns assessment meaning; concrete workflow can defer |
| Evaluator | Identifiable version/role; independent ID only when necessary | Retain definition/reference sufficient for interpretation | Specific evaluators, common provenance need | No universal evaluator API before real consumers |
| Oracle | Version/scope/reference as relevant; not necessarily standalone | Retain support needed for intended re-evaluation | Family/task-specific | First slice needs a suitable oracle/test basis, not a framework Oracle |
| Experiment | Stable design/version reference for multiple realizations | Needed for a durable comparative claim | Experiment-specific design | Minimal contract before that study; no substrate blocker |
| Comparison | Reference/version if conclusions are retained/revised | Retain claim, input population and method when publishing | Question/policy-specific | Separate inference from observations; no statistics engine now |
| Trajectory | Realization plus local decision references often enough | Only to support claimed adaptive replay/analysis | Policy/experiment-specific | Can defer reusable semantics; preserve local causal/availability facts |
| Intervention | Usually identified by treatment and target | Within retained design | Experiment-relative | No independent foundational object now |
| Causal edge | Ordinary endpoints/type or local hypothesis sufficient | Only if the study depends on retaining it | Experiment-relative, not universally empirical | No foundational DAG or edge identity now |

**Minimality result:** case basis, intended condition, realization, assessment target/criterion, and observation-versus-inference distinctions survive because concrete comparisons are invalid without them. They can be represented simply and reused correctly without independent classes. Universal Treatment, EvaluationEpisode, causal DAG, ground-truth abstraction, trajectory ontology, and scalar quality fail the necessity test as foundations.

This minimum does not demand all state be retained forever. It demands that claims match the identity, capture, observation, and retention strength actually provided.

## AO. ADR impact

No ADR, architecture document, backlog, roadmap, or ledger was changed.

| Recommendation area | Ownership classification | Smallest architectural impact |
|---|---|---|
| Complete failure accounting, explicit capture/replay limits, interaction/attempt association, known model/provenance strength | ADR-0001 refinement/conformance; implementation-shaped adapters | Preserve current boundary; reconcile completion scope and extend only concrete missing observation semantics in authorized work |
| Fixed repository/external interpretation, knowledge availability, semantic/result/coverage contract, dependency/reuse evidence | ADR-0002 refinement | Make accepted meaning usable by first implementations; no new state/claim ontology |
| Case versus need identity, candidate/evidence input retention, explicit retriever/ranker factorization | ADR-0003 refinement | Clarify comparison references without imposing runtime InformationNeed/Evidence IDs |
| Paired representation decisions, faithful materialization, assembly controls, availability and protected-evaluator inputs | ADR-0004 refinement | Preserve existing selection/representation coupling and realization/presentation separation |
| Experiment intent, case/condition/realization association, criterion/judgment meaning, later comparison | Genuinely Evaluation-owned responsibility; possible future Evaluation ADR | Formalizes already recognized Evaluation ownership, not a new domain or runtime dependency |
| Exact APIs, storage, fixture/version mechanisms, retention, traces, instrumentation, rankers/metrics/oracles | Implementation-shaped and B-0002 pressure only | Resolve with concrete slices and bounded harnesses |

A future Evaluation ADR is justified by distinct assessment/comparison semantics, not by a desire for a convenient common record. This dossier recommends that minimum ownership, but does not require a new ADR before deterministic substrate implementation or select its schema/package.

## AP. Implementation-start implications

### BLOCKING

No FATAL finding and no foundational semantic blocker was identified for a bounded repository-intelligence implementation slice under ADR-0002.

There are claim-specific prerequisites: an analyzer result needs defined proposition/coverage semantics; a controlled comparison needs a declared fixed basis/treatment; exact replay needs retained inputs at its promised strength. These are conditions of doing that work honestly, not reasons to halt unrelated initial implementation.

The roadmap's review/reconciliation gate remains administratively open. This artifact neither revises it nor authorizes implementation. The distinction matters: technical safety is not a claim that existing project sequencing has already been changed.

### MUST-PRESERVE SEAMS

- Repository state versus observed external semantic interpretation, and honest observation guarantees.
- Definition semantics versus binding/build, derivation versus execution, produced knowledge versus coverage/absence.
- Direct semantic dependencies and support sufficient for applicability/replay; reuse versus recomputation and failure.
- Applicable relationship knowledge versus rebuildable graph projection and its availability/cost.
- Purpose/planning/application versus candidate discovery, preserved native evidence, ranking, and selection.
- Selected information/representation decision versus realized disclosure versus assembled model request.
- Local correctness/fidelity versus downstream usefulness; typed outcomes and explicit constraints/cost scope.
- Case/condition/realization/evaluator referenceability at the experiment boundary without requiring universal IDs.
- Capture absence and failed/incomplete executions versus successful results.
- Evaluator-private information and declared feedback versus consumer-visible information.

### SAFE TO DEFER

Reusable Evaluation APIs/classes/store; global case/treatment IDs; generic Run/Step/Attempt promotion; tracing backend; universal metrics/rubrics/oracles; statistical methods; dataset selection; adaptive policy ontology; causal graph infrastructure; production replay engine; all-layer durable capture; exhaustive performance telemetry.

Likewise, existing ADR-0002 choices such as digest layout, parser technology, reverse indexes, graph storage, cache policy, and precise dependency granularity remain implementation-design questions. Choose a correct bounded slice and test its stated contract; do not pre-build every future evaluation mechanism.

**Architectural start verdict:** SAFE WITH PRESERVED SEAMS.

## AQ. First implementation slice requirements

These requirements describe evidence to retain, not a proposed data model or API. Their extent is proportional to the slice's semantic claims.

| Preserve from the first relevant slice | Why required | Minimum acceptable form |
|---|---|---|
| Exact deterministic fixture state and its version/reference | Repeated tests must concern the same input | Immutable fixture data plus source revision/content basis; generated fixtures also identify generator/seed when relevant |
| RepositorySnapshot/state identity and declared observation/inclusion semantics when the slice introduces snapshots | Same HEAD/path must not masquerade as same state | Correct bounded state identity with its explicit contract; no mandated Merkle implementation |
| Relevant external semantic inputs/assumptions and observation strength | Prevent hidden configuration/toolchain dependence | Values/references/constraints appropriate to the actual derivation |
| DerivationDefinition meaning and relevant compatibility/revision | Evaluators must know the asserted proposition | Family documentation/test contract plus inspectable semantic reference |
| Actual direct role-bearing semantic dependencies | Applicability and replay require consumed support | Correct coarse scope is acceptable; no obligation to maximal fine tracking |
| Produced knowledge and result-specific support where necessary | Local correctness and later attribution require a target | Immutable semantic values/references; avoid treating temporary internals as knowledge |
| Qualification, scope and semantic-result coverage when the family makes such claims | Partial/unsupported/empty results must not become exhaustive negatives | Explicit vocabulary/representation sufficient for the family, not a universal boolean |
| Distinction between semantic computation and its realization/failure | Cost/failure/repeated-execution comparisons require occurrence attribution | Local execution reference and terminal/partial facts; no forced reuse of InteractionAttempt |
| Analyzer/binding implementation provenance for evaluated executions | Compatible semantics do not identify the code that produced a bug/performance result | Version/build/source revision reference appropriate to the experiment |
| Inputs and outputs accessible at the tested boundary | Future consumers must be replaceable without hidden ambient state | Bounded explicit composition; optional capture/reconstruction sufficient for the selected tests |

**Required when the slice actually claims efficiency/reuse:** distinguish work reused, recomputed, invalidated, unavailable, and failed; identify the before/after states and workload; retain relevant cost boundaries. A count of avoided derivations can be more useful initially than a comprehensive profiler.

**Nice to have initially, required only for corresponding quantitative claims:** monotonic timings, memory/CPU/storage observations, detailed dependency bookkeeping counts, reverse-index cost, cache warmness, granular provenance storage cost. Do not require every tiny analyzer to emit Telemetry or every semantic result to own timing fields. Resource observations belong with executions/experiments, not as knowledge validity.

**Concrete validation direction without implementation design:** compare a bounded analyzer against known fixtures; test qualification/coverage/absence; run the same semantic input through independent realizations; exercise a small changed-state case showing correct reuse or invalidation. If a slice introduces incremental reuse, compare semantic results with a reference recomputation and preserve the disagreement rather than only reporting pass/fail.

No source, test, schema, or code implementing these suggestions was created.

## AR. Remaining foundational questions

The remaining questions are bounded ownership or meaning questions, not an invitation to reopen settled architecture wholesale:

1. Should the recognized Evaluation responsibility be formally accepted with the minimum contract in AN before its first reusable consumer, or remain articulated through local experiments until evidence converges? Either approach permits initial deterministic intelligence.
2. For future reusable consumers, what is the exact scope of case version, assigned condition, realization, evaluator application, and comparison identity? Their distinction is necessary; independent global IDs are not settled.
3. When a future protected evaluator and an Agent share information stores or Tools, which existing governance/disclosure owner enforces the concrete visibility contract? Current fixture-local isolation need not answer the universal case.
4. How should a particular future learned/probabilistic repository analyzer declare its semantics? E05 deliberately requires explicit acceptance; this investigation does not promote one.

No evidence presently requires a universal score, Episode, Claim layer, causal graph, ModelKnowledgeState, or trajectory ontology. Questions about exact provider revision that an external service does not expose may remain irreducible uncertainty rather than solvable architecture.

## AS. Remaining implementation-shaped questions

Concrete case/fixture serialization and version references; knowledge/input closure retention; graph-view freezing and cache isolation; applicability assessment records; partial-result publication; candidate/evidence grouping and replay; per-family semantic equivalence/oracles; ranker features and tie handling; representation-support correspondence; semantic-strength tests for chosen forms; exact request retention under capture policy; concurrent correlation; failed/cancelled model observation; observer-failure policy; profile observation/verification; monotonic timing scopes; protected label projection; experiment-local storage and regrading; human/LLM judge rubrics; datasets and sample sizes; budget protocols and statistics.

These questions should be answered by the first consumer that needs them. Their presence is not evidence that ADR-0002–0004 lack a usable architecture.

## AT. Reopen triggers

Reopen a foundational decision only on evidence such as:

- A real semantic input cannot be represented/observed sufficiently through the accepted dependency/assumption/scope boundary to support honest applicability.
- A result family cannot express its proposition or coverage without silently strengthening meaning.
- A concrete API forces selection/representation/materialization/assembly together so an intended controlled intervention cannot be represented.
- Actual dynamic acquisition cannot expose the consumed input basis needed for correct replay or reuse.
- A meaningful graph composition requires shared semantics that compatible typed views cannot represent.
- Repeated consumers cannot correlate case/condition/realization/criterion without overloading unrelated execution or knowledge identities.
- A capture/privacy requirement and promised replay strength conflict in a way that cannot be addressed by limiting the claim or authorized retention.
- Adaptive evaluation requires decision semantics that local records or existing execution references cannot preserve.
- Empirical results show finer dependencies, graph infrastructure, synthesis, retrieval portfolios, or another costly mechanism consistently fails to justify its complexity for the intended workload.

The last trigger may call for simplification, lazy use, or removal of a mechanism rather than expansion of architecture. Negative evidence is a successful output of evaluation.

Not reopen triggers by themselves: no graph database selected; no universal metric; no global treatment ID; no generic Trace implementation; no completed external review yet; a local report lacks durable storage; one model trial fails; or one mechanism needs a more concrete test fixture.

## AU. Final verdict

The architecture is experimentally well-factored at the semantic level and only partially equipped operationally. The recommended minimum is explicit experiment/assessment meaning correlated with layer-local artifacts and Evidence, with optional traces and study-relative causal reasoning. The first deterministic repository-intelligence slices can begin safely when separately authorized, preserving the seams listed in AP/AQ. No foundational reason was found to wait for later external Deep Research confirmation; the recorded roadmap gate still requires its own reconciliation and has not been silently closed.

The following explicitly answers all 38 mandatory questions.

1. **Is the architecture experimentally well-factored?** Yes, substantially at the accepted semantic level. Most upstream-to-downstream interventions can be expressed with identified state and preserved outputs; present implementation does not yet execute most of them.

2. **Which existing boundaries are strong experimental intervention seams?** Snapshot/external interpretation versus derivation; semantic derivation versus realization; relationship knowledge versus graph projection; candidate/evidence discovery versus ranking; plan versus faithful realization; disclosure versus assembly; request value versus invocation occurrence.

3. **Which boundaries are insufficient?** Naively fixing snapshot, candidates, plan, or request is insufficient without their relevant input closure and external conditions. Current capture/correlation/failure observation is operationally incomplete; same-plan representation changes and adaptive continuation replay require narrower claims.

4. **Can evaluation remain entirely implementation infrastructure?** Its mechanisms can remain local infrastructure initially. Its assessment/comparison semantics cannot be erased into configuration or generic observation without losing intended contrast and criterion meaning.

5. **Is a distinct Evaluation architectural responsibility justified?** Yes, and the taxonomy, architecture, namespace and backlog already recognize it. This investigation refines that responsibility rather than introducing a new domain.

6. **What is its minimum responsibility?** Assessment target/basis, intended conditions and assignment, realization correlation, evaluator/criterion meaning, typed observations/judgments, and separation of raw evidence from later comparison/inference.

7. **Is EvaluationCase a necessary semantic concept?** A stable comparison/assessment basis is necessary for repeatable case-based evaluation. A universal EvaluationCase class is not.

8. **Does EvaluationCase require identity?** It needs an unambiguous scoped/versioned reference when reused or paired. Independent global nominal identity and standalone persistence are optional.

9. **Is explicit treatment semantics required?** Yes for an intended controlled contrast. Configuration can carry it only if intended differences, fixed factors and realized deviations remain explicit.

10. **Does Treatment require independent identity?** No universal independent entity is required. A scoped variant/configuration reference is enough unless reuse, joining or lifecycle needs justify more.

11. **Is evaluation-run identity required?** Distinct realization referenceability is required for repeated trials, failure accounting and joins. An experiment-scoped ordinal/key can suffice without a new generic lifecycle.

12. **Can existing Attempt/Evidence semantics provide it?** They provide reusable component occurrence/evidence references, not the whole evaluation realization's meaning. InteractionAttempt remains specialized; an evaluation association can reference it without redefining it.

13. **Should outcomes/measurements remain heterogeneous and typed?** Yes. Preserve criterion, units/scope, provenance and missingness rather than normalizing all outcomes into numbers.

14. **Is a universal scalar score harmful or useful?** Harmful as foundational semantics; useful only as a declared policy-specific derived aggregate with raw outcomes retained.

15. **Is a universal EvaluationEpisode justified?** No. A bounded experiment-local report/reference manifest can aid navigation without owning all layer lifecycles.

16. **Is a universal causal DAG justified?** No. Experiment-relative causal hypotheses and ordinary references suffice for the demonstrated requirements.

17. **Is generic tracing sufficient?** No. It explains observed execution structure, not intended controls, assignment, or evaluator meaning; optional traces can support explicit evaluation records.

18. **Can repository-intelligence correctness be evaluated independently of agent success?** Yes, against definition-specific fixtures, analyzers, properties and other compatible oracles. Downstream usefulness is a separate judgment.

19. **Can retrieval be isolated from ranking?** Yes, by fixing purpose, repository/external/intelligence basis and ranker while retaining candidate/evidence outputs. Any extra intelligence acquisition must be explicit.

20. **Can ranking be isolated from candidate acquisition?** Yes, over fixed candidates, native evidence and consumed features with identified ranking policies.

21. **Can information selection be isolated from representation?** Conditionally, by fixing identified support/information obligations and pairing explicit representation decisions. An unchanged whole DisclosurePlan generally cannot choose a different representation.

22. **Can ContextDisclosure be isolated from ModelRequest assembly?** Yes, explicitly in ADR-0004. Other prompt components and consumer conditions must be fixed or declared treatments, and assembly cannot silently drop or synthesize information.

23. **Can synthesis be evaluated independently?** Faithfulness, support, qualification/conflict preservation and some compression properties can be evaluated locally. Utility requires consumer/task evaluation.

24. **Can semantic-strength preservation be tested?** Yes with bounded invariant, metamorphic, semantic-contract and provenance tests. Arbitrary prose still needs appropriately limited semantic judgments; no universal proof is claimed.

25. **Does progressive disclosure require foundational trajectory semantics?** No. Realization-scoped decision/episode references, policy, available information, outcomes and dependency order suffice initially.

26. **What nondeterminism must be recorded?** Relevant sampling/defaults, provider drift, runtime/hardware/concurrency/cache state, external observations, Tool/service timing, test/oracle flakes, and adaptive decisions, with unknowns retained.

27. **What model/provider identity is necessary?** Requested model/route and settings, provider/adapter, known revision/artifact/quantization/server/template facts, observed identity and time window, and provenance strength. Unknown exact revision limits claims to the observed service conditions.

28. **How should historical evaluation evidence differ from DerivedKnowledge applicability?** Historical observations remain records of their experiment; predictive relevance under changed conditions is a separate inference. Repository knowledge applicability is dependency satisfaction under derivation semantics, not a universal evaluation-validity predicate.

29. **What is required for counterfactual replay?** Identified and retained fixed input closure at the promised replay strength, compatible alternate mechanism, explicit external conditions, authorized effects, and regeneration after adaptive divergence unless the replay is deliberately conditional.

30. **What is required for causal claims?** A defined contrast/population, comparable units, assignment and actual-condition records, controlled/accounted-for relevant state, complete trial accounting, credible evaluator, resource scope, and uncertainty/confounding limits.

31. **How should marginal contribution be evaluated conceptually?** Through declared ablations, matched or factorial comparisons and local replay, retaining downstream pathway changes and total costs. No universal additive credit formula follows.

32. **How should interaction effects be preserved?** Retain joint factor assignments, task/model/consumer strata, intermediate candidate/disclosure evidence and per-realization outcomes/costs instead of collapsing them into one mean.

33. **Should efficiency remain multi-objective?** Yes. Correctness, success, latency, tokens, calls, indexing/maintenance/storage and fidelity should remain distinguishable; later policy may aggregate.

34. **What evaluation information must never become model-visible?** Information designated evaluator-only by the experiment, including hidden tests/solutions, gold labels/relevant files, private oracle rationale and blinded metadata. Deliberate feedback must be authorized and recorded as assistance; naturally visible treatment behavior is not the same as leaked labels.

35. **Which findings block implementation?** None blocks the initial deterministic repository-intelligence substrate architecturally. Current model-evaluation completeness/replay claims have concrete prerequisites, and project authorization/review sequencing is separate.

36. **Which findings merely require implementation seams?** AM-R1–R7 require preserved distinctions and bounded claims; AM-I1–I4 require concrete observation/capture/provenance/harness work before their corresponding evaluation claims.

37. **What should the first implementation preserve now so future evaluation remains possible?** Exact fixture/state references, observation and external-input semantics, derivation definition/compatibility, actual dependencies/support, produced knowledge/coverage, implementation/execution correlation, and cost facts when efficiency is claimed.

38. **Is there any architectural reason implementation should not begin before later external Deep Research confirmation?** None was demonstrated for a bounded slice that preserves these seams. This is a safety assessment, not implementation authorization or an assertion that the roadmap's review gate has already been reconciled.

### Verification record

The completed artifact is to be checked against all 47 required section labels A–AU, the 38 numbered answers above, the complete counted finding set, and the initial repository integrity manifest. Final verification results are recorded below after the full reread and Git/hash comparison.
