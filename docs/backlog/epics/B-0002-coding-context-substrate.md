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
repository facts.
Context remains
purpose-relative selection and disclosure, not Conversation state, repository
storage, Memory, or repository truth.

[ADR-0003](../../architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
now settles the next semantic layer: InformationNeed; bounded retrieval
planning/applications; ContextCandidates; provenance-bearing RelevanceEvidence;
and ranking distinct from final Context selection. It does not implement a
retrieval system or Context compiler.

[ADR-0004](../../architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
now settles post-ranking Context/disclosure semantics: conditional composition,
representation-coupled selection, coverage, applicability, prior availability,
sufficiency, budgeting, ContextDisclosure, and separation from model-input
assembly. Its refinement further settles information-not-string disclosure,
DisclosureOption/DisclosurePlan/ContextDisclosure distinctions, representation
origin/form/fidelity/cost, explicit derived synthesis, coherence, authority,
conflict preservation, and no-silent-replanning materialization. It leaves
compiler, concrete artifacts, representation/coverage/authority/conflict/
coherence mechanisms, derivation orchestration, materialization, assembly,
caching, authorization integration, and evaluation implementations unresolved.

This epic preserves the unimplemented pressure enabled by that decision:
snapshot policy and acquisition, deterministic repository knowledge,
analyzer-established subjects/source occurrences, relationship views, graph
views, incremental observation/consistency, SnapshotDelta, increasingly fine-
grained dependency scopes, applicability/reuse, invalidation discovery,
rederivation, caching, historical/replay support, retrieval/relevance evidence,
ranking distinct from final selection, representation and compilation,
provenance/disclosure, budgeting, progressive acquisition, and evaluation.
Resources provide access and
Tools may adapt bounded access, but neither constitutes repository intelligence
or Context compilation.

Concrete DerivationDefinition/Derivation/DerivedKnowledge models and identities,
dependency-role and provenance schemas, compatibility/versioning, applicability
assessment, result grouping/coverage, partial-result publication, execution/
Evidence integration, capability bindings, dependency indexes, schedulers, and
evaluation infrastructure remain unresolved implementation/design pressure.

- hard_dependencies: none
- pressure_dependencies: none
- operational_dependencies: resources filesystem, core paths, core regex
- related: ADR-0002; ADR-0003; ADR-0004; B-0008 (superseded historical investigation)
- promotion_trigger: an independently useful, bounded semantic slice is ready
  for design without collapsing Repository intelligence, Context, Tool,
  Runtime, Agent, or orchestration ownership
- validation_level: NONE
