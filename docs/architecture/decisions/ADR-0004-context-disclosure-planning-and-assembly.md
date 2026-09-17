# ADR-0004 — Context disclosure planning and model-input assembly semantics

- Status: Accepted
- Date: 2026-09-16
- Scope: semantic architecture after ranking: Context/disclosure planning,
  representation, coverage, prior information, sufficiency, budgeting,
  DisclosurePlan, ContextDisclosure, materialization, model-input assembly, and
  optional InformationNeed decomposition. This decision authorizes no compiler, disclosure model,
  decomposer, retriever, ranker, assembler, persistence, or test.

## Context

ADR-0002 establishes repository identity, DerivedKnowledge, applicability, and
relationship semantics. ADR-0003 establishes InformationNeed, candidate and
evidence semantics, bounded retrieval, and ranking. Those decisions deliberately
leave open how ranked candidates become useful information available to a
consumer. Treating that step as top-K candidates until a token ceiling is full
would lose representation choice, overlap, prior disclosure, authority,
sufficiency, and efficiency semantics.

Current conversation behavior belongs to `agents.conversation`; the sparse
`context/` namespace does not own historical Message, History, or Session
semantics and this ADR does not select a future package location.

## Decision

### Disclosure planning is conditional composition

Context compilation is a conditional information-composition problem, not
top-K retrieval. RelevanceEvidence explains why a repository subject might
matter to an InformationNeed. Ranking interprets candidate relevance. Disclosure
utility is the marginal value of represented information given proposed and
currently available disclosure state. Selecting one disclosure changes remaining
marginal utility without changing underlying RelevanceEvidence or making prior
coverage observations false.

Disclosure planning selects information to make available to a consumer, not
arbitrary strings or prompt chunks. Model-visible text/serialization is a later
realization and assembly concern. A DisclosureOption is a purpose-relative
possibility for making identified information about one or more repository-
intelligence subjects available through a particular representation. It is not
rendered prompt content, need not map one-to-one to a file/symbol/candidate, and
may have origin, form, fidelity, provenance/dependencies, applicability,
expected cost, and information-contribution characteristics. These are semantic
dimensions, not required fields or a type hierarchy.

Selection and representation are coupled. One ContextCandidate can have
different useful representations—identity/name, signature, documentation,
source region, complete definition, relationship view, or future forms—with
different fidelity and cost. A DisclosureOption remains conceptual; no concrete
model, API, hierarchy, or exhaustive representation taxonomy is selected.

Coverage is distinct from relevance. Relevance concerns why a candidate may
help; coverage concerns which aspects/information requirements a proposed
disclosure contributes toward satisfying a need. A need may expose identifiable
sub-needs/aspects incrementally, but complete decomposition is not required
before retrieval or compilation. Coverage is purpose-relative and should obey
ADR-0002 derivation, dependency, provenance, identity/versioning where
appropriate, and reproducibility principles. Literal inheritance from
DerivedKnowledge is not required.

Disclosure utility is non-additive. Highly relevant options can overlap so a
second contributes little after the first; a lower-ranked option can add more
coverage. Options can also be complementary: implementation plus test,
implementation plus governing architecture, interface plus implementation, or
relationship evidence plus source can jointly establish information that neither
does sufficiently alone. Complementarity must be grounded in information and
repository/DerivedKnowledge relationships, not generic file-type bonuses.

Redundancy/overlap is representation- and purpose-relative, not inferable only
from path, file, subject, or physical source overlap. A signature and full
definition can overlap strongly, while implementation and architectural
rationale can be complementary. No utility, complementarity, coverage,
redundancy, deduplication, or coherence algorithm is selected.

Repository semantic relationships remain intelligence substrate, not disposable
retrieval artifacts. They may later support discovery, coverage, complementarity,
redundancy/overlap, change impact, and other selection reasoning. ADR-0002
remains authoritative for relationship and graph semantics.

### Prior information, applicability, and sufficiency

Disclosure history (what was previously disclosed) differs from currently
available information (what the present interaction can rely on). Prior material
may become unavailable through truncation, compaction/summarization, provider
behavior, a new interaction, provider transition, or other lifecycle effects.
Previously disclosed does not mean available forever.

Reuse is dependency-based, not `previously disclosed => omit`. A prior
disclosure may remain applicable across snapshots under ADR-0002 dependency
semantics, or may be invalidated by changed dependencies. This is stronger than
snapshot-ID equality and blind prompt caching. The architecture may track what
was disclosed, currently available, and applicable; it must not claim that a
model understood, remembered, or correctly reasoned from it. Model utilization
remains evaluation evidence, not an authoritative ModelKnowledgeState.

Coverage says which information/aspects are represented. Satisfaction/sufficiency
assesses whether available information is adequate for the purpose and consumer;
it is not state intrinsic to an InformationNeed representation. It may eventually weigh
coverage, fidelity, authority, uncertainty, consumer requirements, and other
evidence. No satisfaction enum or assessor is selected.

Additional acquisition or disclosure is justified by expected marginal
information value relative to expected cost and current sufficiency evidence,
not merely because capacity remains. The mechanism can later be deterministic,
learned, model-assisted, hybrid, or policy-driven; no value-of-information
formula is selected.

### Constraints, budgets, and disclosure artifacts

A disclosure budget is a ceiling, not a fill target. Context quality and
efficiency are both objectives, and optimal disclosure can be materially smaller
than model capacity. Future costs can include input tokens, latency, retrieval
compute, representation/compilation compute, monetary cost, and other bounded
resources. Architecture distinguishes hard consumer/model capacity, policy
budget, resources already consumed by instructions/tools/conversation/current
interaction, and derived remaining capacity. It selects no universal cost
function or `token_budget` field.

Disclosure planning distinguishes hard constraints from optimization preferences.
Potential hard constraints include capacity, authorization/disclosure policy,
applicability, and mandatory authority/governance requirements. Potential
preferences include useful coverage, low redundancy, complementarity, coherence,
fidelity, authority, token efficiency, latency, and cost. They must not be
collapsed into one undifferentiated score.

A **DisclosurePlan** is the identified decision about what information should be
made available, through selected disclosure possibilities/representations under
its purpose, evidence, constraints, and planning semantics. A
**ContextDisclosure** is the identifiable, provenance-bearing information
artifact actually realized with reference to a DisclosurePlan. Neither is a
ModelRequest. Concrete models, identities, and cardinality are open: a plan can
fail to produce a disclosure, revision creates a new plan, and future semantics
may permit more than one realized disclosure from a plan. Once established as
identified planning/evidence artifacts, plans and disclosures are immutable.

The materialization boundary is:

```text
DisclosurePlan -> materialization -> ContextDisclosure -> model-input assembly -> ModelRequest
```

Materialization resolves applicable source, extracts source-preserving material,
projects existing DerivedKnowledge, realizes already-derived synthesis, and
formats/structures information without new semantic assertions. It must not
silently substitute a materially different decision when faithful realization is
impossible. Changed dependencies, inapplicable knowledge, unresolved source,
unavailable knowledge, failed derivation, cost violation, or disclosure policy
may make that discrepancy observable and require later re-planning/acquisition.
If a selected representation requires new semantic knowledge, that derivation
remains explicit rather than hidden in materialization.

Planning-time applicability does not guarantee applicability when realization
occurs: repository dependencies may change. Materialization must not silently
present selected information as current when it is no longer applicable; future
handling may re-plan, re-derive, or re-acquire without selecting race/atomicity
mechanics here. Planning may use estimated cost, while materialization and
assembly expose actual realized cost. Those remain distinct so future evaluation
can assess representation, derivation-latency, token, and other predictions.

A ContextDisclosure may be reusable independently of one ModelRequest or one
assembly policy when its information remains applicable and appropriate to a
later purpose/consumer. Applicability alone does not establish relevance.
Possible future reuse levels include DerivedKnowledge, materialized
representation, and ContextDisclosure; cache keys, storage, and granularity are
open. Provenance must eventually distinguish planning failure, materialization
failure, assembly failure, and model-utilization failure rather than collapse
differences between selected, realized, and presented information.

Repository history (snapshots and knowledge applicability), disclosure history
(selected/disclosed purpose-relative information and policy), and Conversation
history (retained messages/interactions under `agents.conversation`) are distinct
histories. They may reference each other but do not share one identity or
lifecycle.

### Planning versus model-input assembly

Disclosure planning determines **what** information should be available:
candidate/representation choices, coverage, marginal contribution, overlap,
complementarity, prior availability, applicability, authority, coherence, and
cost/budget. Model-input assembly determines **how** selected information is
realized and positioned for a particular model interaction: provider
serialization, prompt structure, order, separators, tokenizer/model constraints,
and coexistence with tools, instructions, and conversation.

Presentation order may affect utilization, but does not contaminate repository
relevance or coverage semantics. Selection decides what to disclose;
presentation policy arranges selected material. Positional effects are empirical,
model-specific evidence, not universal rules. Future assembly policy can depend
on identified hard capabilities and versioned empirical behavior profiles without
changing repository relevance evidence. Neither `ModelCapabilities` nor
`ModelBehaviorProfile` is selected as a model.

The same ContextDisclosure may be assembled by different identified policies
into different ModelRequests. This permits presentation/input experiments while
holding retrieval, ranking, and disclosure selection fixed. No assembly
abstraction or policy is implemented.

### InformationNeed decomposition

Information-purpose decomposition is optional. A broad/multifaceted purpose may
lead to subordinate purpose/acquisition work when that improves acquisition,
precision, concurrency, coverage reasoning, or efficiency; focused purposes can
proceed directly to retrieval. The broader purpose remains meaningful, and
causal/provenance relationships should remain available where needed rather
than replacing or discarding it. Decomposition may be progressive as acquired
knowledge reveals dimensions, without requiring a persistent tree of
independently identified InformationNeed artifacts.

Independent subordinate work can enable concurrent planning/retrieval where no
dependency requires ordering. Decomposition can omit a material broader-purpose
dimension: coverage or satisfaction of all subordinate work therefore does not
prove broader-purpose sufficiency. Decomposition failure is a future
distinguishable evaluation category; its concrete representation and replay
mechanism remain open.
Deterministic, structural/repository-aware, model-assisted, learned, and hybrid
decomposition remain replaceable future mechanisms.

### Representation origin, coherence, authority, and conflict refinement

Origin, form, fidelity, and cost are distinct representation concerns. Origin
asks how represented information came into existence; form asks how it is
exposed/organized; fidelity asks how completely and precisely it preserves what
it purports to represent for the purpose; cost asks what realization/presentation
resources it requires. Fidelity is not information volume, source length, or
token cost: a signature can have complete relevant fidelity for a parameter
question despite a full body containing more total information.

Source-preserving representations select or transform identified source without
new semantic assertions, such as a complete definition, signature, docstring,
contiguous region, test body, or architecture section. Extraction, formatting,
or omission alone does not make a representation synthesized. Knowledge
projections expose existing structured/DerivedKnowledge in usable form, such as
symbol facts, relationship lists, dependency neighborhoods, test-to-code facts,
or structural views. Synthesized representations contain new semantic assertions
or explanations derived from supporting information, such as an implementation
summary, lifecycle explanation, behavioral synopsis, or change-impact narrative.

Transformative realization changes extraction, formatting, organization, or
serialization without materially new semantic claims. Interpretive work adds
semantic assertions, for example explaining why behavior occurs, inferring
responsibility, or composing a multi-source narrative. This is semantic rather
than LLM-versus-deterministic classification: determinism provides
reproducibility, not semantic certainty.

When preparation requires new semantic assertions, those assertions should be
explicit provenance-bearing DerivedKnowledge under ADR-0002 rather than opaque
ephemeral compiler text:

```text
supporting information -> identified derivation -> DerivedKnowledge -> disclosure possibility/materialization
```

This does not require every formatting operation to derive knowledge. It keeps
existing knowledge distinct from a selected representation requiring new
derivation work, whose cost, latency, failure modes, provenance,
reproducibility, uncertainty, and authority implications can differ. Composite
representations may combine multiple provenance-preserving forms, such as a
structural orientation plus exact supporting source, without flattening their
constituent origins.

Coherence concerns whether information presented together forms an intelligible
meaningful unit whose relationships and purpose can be understood without
unnecessary consumer reconstruction. It is not physical contiguity.
Source, structural, and semantic coherence are possible forms, not an enum.
Precise fragments can be coherent when purpose and relationships are clear; one
large contiguous block can impose needless reconstruction burden. Coherence
measurement or optimization remains open. Progressive disclosure may vary form,
fidelity, directness/source preservation, and derivation/synthesis level; no
universal summary-first or source-first progression is selected.

Authority is claim- and purpose-relative. No universal ordering exists among
implementation, tests, accepted architecture, ADRs, documentation, comments,
history, experiments, and generated artifacts. Current implementation can
establish executable behavior, tests expected/verified behavior, accepted
architecture constraints, ADRs rationale/history, and ledger/history prior
state; these examples do not form a fixed hierarchy. Repository intelligence
should preserve source role where known. Authority is future purpose-/claim-
relative evidence, potentially derived with source role, applicability,
provenance, agreement/conflict, and identified assessment semantics—not an
intrinsic scalar attached permanently to a source. Relevance, authority,
confidence, coverage, and ranking influence remain distinct.

Material disagreement among relevant applicable sources is itself preservable
information. Disclosure planning does not generally arbitrate truth or silently
choose a winner: disagreement can reveal defects, stale documentation/tests,
undocumented change, incomplete analysis, or other inconsistency. Synthesis
must not collapse material conflict into an unqualified assertion unless an
identified derivation is authorized and semantically capable of resolving it.
Likewise, absence of found evidence is not evidence of absence unless
acquisition semantics justify that conclusion; this preserves ADR-0003 absence
discipline for authority, synthesis, conflict, coverage, and sufficiency.

Planning selects informationally desirable disclosure but is not authority to
disclose it. Nor does possession of a ContextDisclosure authorize every item in
every ModelRequest. Materialization/assembly can remain subject to consumer-
specific disclosure policy, provider constraints, governance/authorization,
applicability, and interaction limits. This preserves the repository principle
that planning/proposal does not confer authority.

### Remaining open pressure

Semantic repository-subject decomposition remains future pressure. Subjects may
eventually yield coherent disclosure units—public contract, lifecycle, failure
behavior, evidence behavior, or coherent source region—rather than arbitrary
line/token slices. This ADR does not select its name, derivation method,
summary policy, persistence, identity, or representation policy.

Concrete representation-form, fidelity, source-role, authority-evidence,
conflict, coherence, reconstruction-burden, synthesis/validation, derivation-
orchestration, materializer, materialization-evidence, applicability-race/cost-
estimator, cache/reuse, disclosure-authorization, assembly, package, and
evaluation mechanisms remain open. Derived/synthesized representations retain
the provenance/dependency requirement above without selecting when or how they
are produced.

## Status and implementation boundary

This decision accepts Context/disclosure semantics only. It does not implement
a compiler, DisclosureOption, DisclosurePlan, ContextDisclosure,
representation/coverage/satisfaction model, decomposition mechanism,
utility/stopping/budget policy, availability/history store, applicability cache,
capability/behavior profile, assembly layer, tokenizer integration, derived
representation, persistence, or evaluation infrastructure. B-0002 retains this
unimplemented design pressure.
ADR-0001 remains the model-native Tool boundary; ADR-0002 remains repository
identity/derivation/graph architecture; ADR-0003 remains InformationNeed,
retrieval, evidence, and ranking architecture.
