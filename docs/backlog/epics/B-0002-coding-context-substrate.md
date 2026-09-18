# B-0002 — Coding Context Substrate

- type: EPIC
- status: BACKLOG
- decision_maturity: READY_FOR_DESIGN
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: unimplemented repository intelligence and coding-Context capabilities
- primary_domain: context
- supporting_domains: resources, tools, agents, models, experiments

## Problem / value

[ADR-0002](../../architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
now settles the semantic foundation that this epic originally investigated:
Repository identity is distinct from location and Git identity; snapshots are
content-derived under explicit policy; deterministic knowledge is produced by
identified Derivations over explicit dependencies; and repository semantic
relationships are distinct from derivation dependencies. It also settles
snapshot-local RepositorySubjects, distinct SourceOccurrences, and their
orthogonality to DerivedKnowledge: analysis may establish subjects, while
subject continuity, hierarchy, and relationships remain derived knowledge.
RepositorySnapshots are logically complete successfully observed states under
explicit semantics; SnapshotDelta and IncrementalMaintenance remain separate;
and dependency-scoped applicability permits reuse without making state change
or cache/invalidation mechanisms into repository truth.
ADR-0002 further distinguishes DerivationDefinition, Derivation, execution,
and immutable DerivedKnowledge; role-bearing direct semantic dependencies from
incidental execution inputs; and dependencies from shared/result-specific
provenance. Execution failure and incomplete coverage remain separate from
repository semantics. DerivedKnowledge is not restricted to infallible facts:
its DerivationDefinition/result vocabulary defines definite, possible,
necessary, approximate, ambiguous, unresolved, exhaustive, partial, or other
qualified propositions. Semantic-result coverage, assumptions/scope,
provenance, applicability, and execution evidence remain distinct, and absence
has negative force only where derivation semantics and sufficient coverage
justify it.
ADR-0002 now also settles the repository-intelligence capability boundary:
available semantic realization is distinct from DerivationDefinition and
implementation binding; bounded dependency access and finalized dynamic
dependency accounting preserve replay/applicability; and internal admission,
execution evidence, scheduling, retrieval, Tool authorization, Context, Agent,
and Runtime ownership remain separate.
Context remains
purpose-relative selection and disclosure, not Conversation state, repository
storage, Memory, or repository truth.

[ADR-0003](../../architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
now settles the next semantic layer: InformationNeed as purpose-relative
desired-information semantics, without requiring a durable independently
identified runtime artifact; bounded retrieval planning/applications;
ContextCandidates; provenance-bearing purpose-relative RelevanceEvidence
without requiring standalone identity, persistence, or repository
DerivedKnowledge status; and ranking distinct from final Context selection. It
does not implement a retrieval system or Context compiler.

[ADR-0004](../../architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
now settles post-ranking Context/disclosure semantics: conditional composition,
representation-coupled selection, coverage, applicability, prior availability,
sufficiency, budgeting, ContextDisclosure, and separation from model-input
assembly. Its refinement further settles information-not-string disclosure,
DisclosureOption/DisclosurePlan/ContextDisclosure distinctions, representation
origin/form/fidelity/cost, repository-relative DerivedKnowledge distinct from
purpose-relative synthesis, representational transformation distinct from
epistemic derivation, coherence, authority, conflict preservation, and faithful
materialization of explicitly planned semantic transformation without silent
semantic strengthening. It leaves
compiler, concrete artifacts, representation/coverage/authority/conflict/
coherence mechanisms, derivation orchestration, materialization, assembly,
caching, authorization integration, and evaluation implementations unresolved.

The focused external-semantic-state research has been reconciled into ADR-0002.
External semantic inputs already fit through the open heterogeneous dependency,
definition, assumptions/scope, observation, provenance, and applicability
semantics; relevant ambient state must not remain hidden. The research did not
justify a universal external-state ontology, independent identity for every
input, foundational `WorkspaceSnapshot`/`EnvironmentSnapshot`, identity-based
applicability, hermetic execution, or mandatory operational replay. The focused
evaluation-architecture/causal-attribution investigation has now completed and
its accepted semantic findings are reconciled. Evaluation remains a distinct
assessment/comparison responsibility correlating layer-local artifacts and
Evidence; it is not a universal framework or owner of those artifacts. Metrics,
benchmarks, datasets, storage, APIs, and scoring formulas remain open.

This epic preserves the unimplemented pressure enabled by that decision:
snapshot policy and acquisition, deterministic repository knowledge,
analyzer-established subjects/source occurrences, relationship views, graph
views, incremental observation/consistency, SnapshotDelta, appropriate
dependency granularity, applicability/reuse, invalidation discovery,
rederivation, caching, historical/replay support, retrieval/relevance evidence,
ranking distinct from final selection, representation and compilation,
provenance/disclosure, budgeting, progressive acquisition, and evaluation.
Resources provide access and
Tools may adapt bounded access, but neither constitutes repository intelligence
or Context compilation.

Replay, debugging, and evaluation may require sufficient correlation among the
relevant snapshot, derivation semantics and dependencies, knowledge, retrieval
purpose/planning/applications, candidates/evidence, ranking, disclosure plan and
realization, assembly, model-interaction Evidence, and downstream evaluation
outcome. This does not require every concept to have standalone identity,
persistence, or lifecycle and does not accept a universal replay/episode/Trace
artifact or merge their existing ownership domains.

Integrated evaluation pressure includes, where meaningful, repository
observation and semantic correctness; derivation-family soundness, precision,
or coverage; incremental correctness and dependency-granularity economics;
graph/retrieval/evidence/ranking contribution; disclosure, representation,
coherence, redundancy, complementarity, synthesis fidelity, and semantic-
strength preservation; model-input presentation effects; resource efficiency;
and end-to-end coding-agent outcomes. Layer-local quality is not task success,
and task success alone does not identify the causal layer. Controlled comparison
and marginal or unique contribution of costly mechanisms should remain possible
where practical without imposing a universal utility score or requiring every
component to expose a score.

Evaluation semantics preserve a referenceable assessment/comparison basis,
intended condition and relevant fixed factors, distinguishable realizations,
evaluator/oracle/criterion meaning, heterogeneous observations/outcomes, and
later comparison/inference where the claim requires them. This does not require
universal `EvaluationCase`, `Treatment`, `EvaluationRun`, `EvaluationEpisode`,
Trace, causal-DAG, trajectory, oracle, metric, or scalar-quality abstractions.
Historical evaluation truth, current predictive relevance/transferability, and
ADR-0002 knowledge applicability remain distinct. Evaluator judgments and
resource observations do not become repository DerivedKnowledge.

The first bounded repository-intelligence design must preserve the semantic
basis needed to evaluate its claims without implementing generic Evaluation:
fixture/state and RepositorySnapshot observation basis; consumed external
semantic inputs; DerivationDefinition meaning/compatibility; direct semantic
dependencies; produced knowledge and result-specific support; applicable
qualification and semantic-result coverage; success/zero/partial/exhaustive/
failure distinctions; analyzer/binding provenance; and correlation among
requested work, realization, dependencies, results, diagnostics, and terminal
outcome. RepositorySnapshot alone is not the whole evaluated intelligence
condition, but no universal `RepositoryIntelligenceSnapshot`,
`KnowledgeClosure`, or `IntelligenceClosure` is accepted.

## Selected first design target

The selected starting hypothesis for concrete design is **direct module-body
Python function declaration knowledge**. The design should test a bounded
proposition approximately equivalent to: for a Python module resource in an
identified RepositorySnapshot, each direct module-body `ast.FunctionDef` or
`ast.AsyncFunctionDef` SourceOccurrence syntactically declares a distinct
snapshot-local function RepositorySubject.

This is an implementation-design target, not an implemented feature, a frozen
production representation, or a universal declaration ontology. It does not
claim runtime binding, importability, callability, reference resolution,
qualified-name semantics, cross-snapshot continuity, class-method or nested-
function declarations, lambda declarations, conditional runtime availability,
or import resolution. Exact proposition vocabulary and production models remain
open under ADR-0002.

The target was selected for architectural information value per unit of
implementation complexity. It pressures RepositorySnapshot,
ResourceOccurrence, ContentIdentity where appropriate, SourceOccurrence,
RepositorySubject, DerivationDefinition, Derivation, capability realization
and binding, DerivationExecution, direct semantic dependencies,
provenance/support, DerivedKnowledge, semantic-result coverage, and
deterministic evaluation without first requiring external-state-sensitive
semantic resolution.

Initial deterministic acceptance pressure includes distinguishing same-named
direct synchronous and asynchronous declarations as separate subjects and
source occurrences, excluding a same-named class method from the bounded scope,
and representing exhaustive coverage of that declared syntactic scope.
Successful zero results, partial results, exhaustive results, and parse or
execution failure remain distinct. This is acceptance pressure, not a
normative fixture or API.

Concrete snapshot observation and identity, occurrence/content roles, source
and subject identity, derivation proposition and compatibility, parser/analyzer
identity, capability/binding representation, dependency accounting,
provenance/support, result publication/grouping, coverage, and execution/
evidence correlation remain design questions. Classes, methods, nested
functions, lambdas, imports and semantic resolution, calls, inheritance,
qualified names, cross-snapshot continuity, generic graph infrastructure,
retrieval/ranking/Context integration, persistence/caching, generic registries
or schedulers, external-environment ontology, LLMs, Agent orchestration, and
governed self-modification remain outside this first slice unless concrete
design evidence proves a prerequisite unavoidable. They are deferred, not
permanently excluded from Repository Intelligence.

Concrete external-state dependency representations, optional domain/composite
identities, observation structures and guarantees, equality/equivalence/
compatibility relations, applicability algorithms, dynamic dependency
discovery/enforcement, sandboxing or hermetic mechanisms, generated-resource
models, retention/artifact storage, environment reconstruction, and semantic or
operational replay mechanisms remain implementation/design pressure. An
external input may be represented by a value, reference, constraint, existing
identity, inline observation, or another adequate form; no representation is
mandatory. Coverage/exhaustiveness remains derivation-specific and cannot
claim closure beyond external dependencies, observations, scope, and assumptions.

Concrete graph-view representation/identity, typed node and relationship
references, compatible cross-view composition and bounded traversal, projection
and adjacency/index structures, eager/lazy materialization, incremental graph
maintenance, cache/persistence/storage, graph-database evaluation, specialized
CFG/DFG and historical/change views, retrieval integration/evidence, initial
high-value views, and graph quality/performance/cost evaluation remain
unresolved implementation/evaluation pressure.

Concrete DerivationDefinition/Derivation/DerivedKnowledge models and identities,
semantic vocabulary/qualification representation, assumptions/scope,
dependency-role and provenance schemas, compatibility/versioning, applicability
assessment, semantic-result coverage/result grouping, partial-result and
absence publication, execution/Evidence integration, capability bindings,
dependency indexes, schedulers, and evaluation infrastructure remain unresolved
implementation/design pressure.

Concrete semantic dependency granularity, dynamic dependency accounting,
provenance schema and structural sharing/compact representation, result grouping
and referential granularity, reverse dependency indexes, invalidation discovery,
cache/persistence strategy, incremental scheduling, eager/lazy maintenance,
parser/analyzer incremental capability, and evaluation of reuse gained versus
dependency/provenance bookkeeping and recomputation cost remain unresolved
implementation/evaluation pressure.

Concrete information-purpose/InformationNeed representation, whether explicit
need identity proves useful, anchors and constraints, decomposition/refinement
and causal provenance, satisfaction/sufficiency assessment, progressive
acquisition, planning/application models, assessment-basis/condition/
realization correlation, persistence/replay, and controlled metrics/experiments
remain unresolved
implementation/evaluation pressure.

Concrete relevance-observation/evidence representation, candidate/evidence
association, measurement taxonomy, provenance, polarity and confidence
semantics, cross-retriever composition, persistence/replay and execution-record
design, marginal-contribution measurement, ranking features/policies,
learned/task-conditioned ranking, evidence caching if justified, and interaction
with repository DerivedKnowledge remain unresolved implementation/evaluation
pressure.

Concrete representation taxonomy, semantic-transformation and purpose-relative
synthesis representation, synthesis validation and fidelity evaluation,
uncertainty and completeness semantics, claim-/purpose-relative authority,
source roles, conflict preservation, provenance/support representation,
model-generated information treatment, explicitly planned materialization,
synthesis identity/persistence/querying/caching/reuse if justified, and package/
API ownership remain unresolved implementation/design/evaluation pressure. No
generic promotion of interpretive or model-generated information to repository
DerivedKnowledge is selected.

Learned/probabilistic analyzer policy if ever justified, conflict/divergence
detection mechanisms, source-role analyzers or ecosystem-specific taxonomies,
semantic-strength-preserving materialization, and evaluation of qualification,
coverage, absence, conflict, and synthesis fidelity remain unresolved. No
universal confidence model, Claim layer, conflict engine, authority hierarchy,
or mandatory source-role representation is selected.

Concrete capability/binding representations, catalogs/registration/discovery,
selection/lifecycle, bounded dependency-acquisition and execution-context APIs,
dynamic tracking algorithms, admission/governance integration, execution
evidence schema, scheduler/concurrency, analyzer/parser interfaces, result
publication, persistence/caching, replay/evaluation, and package/API design
remain unresolved implementation/design pressure.

These concrete choices, together with snapshot digest/observation mechanics,
parser technology, graph storage/indexes/algorithms, per-derivation dependency
granularity, InformationNeed/RelevanceEvidence representation, retrieval and
ranking algorithms, DisclosurePlan/ContextDisclosure models, materialization/
synthesis mechanisms, and exact evaluation metrics/benchmarks, are normally
implementation-design and empirical-evidence work under the accepted semantics.
Their openness is not by itself a reason to repeat general foundational
architecture research. Foundational semantics should be reconsidered only when
research or implementation evidence contradicts an accepted invariant or shows
that required semantics cannot be represented correctly.

- hard_dependencies: none
- pressure_dependencies: none
- operational_dependencies: resources filesystem, core paths, core regex
- related: ADR-0002; ADR-0003; ADR-0004; B-0008 (superseded historical investigation)
- promotion_trigger: an independently useful, bounded semantic slice is ready
  for design without collapsing Repository intelligence, Context, Tool,
  Runtime, Agent, or orchestration ownership
- validation_level: NONE
