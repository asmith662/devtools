# ADR-0004 — Context disclosure planning and model-input assembly semantics

- Status: Accepted
- Date: 2026-09-16
- Scope: semantic architecture after ranking: Context/disclosure planning,
  representation, coverage, prior information, sufficiency, budgeting,
  ContextDisclosure, model-input assembly, and optional InformationNeed
  decomposition. This decision authorizes no compiler, disclosure model,
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

Selection and representation are coupled. One ContextCandidate can have
different useful representations—identity/name, signature, documentation,
source region, complete definition, relationship view, or future forms—with
different fidelity and cost. `DisclosureOption` is accepted only as conceptual
terminology for a subject together with a potential representation; no concrete
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
it remains separate from mutable InformationNeed state. It may eventually weigh
coverage, fidelity, authority, uncertainty, consumer requirements, and other
evidence. No satisfaction enum or assessor is selected.

Additional acquisition or disclosure is justified by expected marginal
information value relative to expected cost and current sufficiency evidence,
not merely because capacity remains. The mechanism can later be deterministic,
learned, model-assisted, hybrid, or policy-driven; no value-of-information
formula is selected.

### Constraints, budgets, and ContextDisclosure

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

A **ContextDisclosure** is an identifiable, provenance-bearing account of
information selected for disclosure to a consumer for a purpose. It must retain
semantic room for associated InformationNeed/purpose, selected represented
information, compilation/selection derivation or policy identity, provenance,
dependencies/applicability, and relevant prior-disclosure relation. Its concrete
model and identity remain open. It is distinct from repository state and
Conversation history so disclosure can be reproducible, inspectable, and
evaluable.

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

InformationNeed decomposition is optional. A broad/multifaceted need may derive
smaller purpose-relative needs when that improves acquisition, precision,
concurrency, coverage reasoning, or efficiency; focused needs can proceed
directly to retrieval. The parent remains meaningful, and child relationships
must retain parent provenance rather than replace/discard it. Decomposition may
be progressive as acquired knowledge reveals dimensions, and should itself be
an identifiable derivation with replay/evaluation provenance.

Independent child needs can enable concurrent planning/retrieval where no
dependency requires ordering. Decomposition can omit a material parent
dimension: coverage or satisfaction of all children therefore does not prove
parent satisfaction. Parent-level sufficiency remains independently assessable,
and decomposition failure is a future distinguishable evaluation category.
Deterministic, structural/repository-aware, model-assisted, learned, and hybrid
decomposition remain replaceable future mechanisms.

### Open semantic pressure

Semantic repository-subject decomposition remains future pressure. Subjects may
eventually yield coherent disclosure units—public contract, lifecycle, failure
behavior, evidence behavior, or coherent source region—rather than arbitrary
line/token slices. This ADR does not select its name, derivation method,
summary policy, persistence, identity, or representation policy.

Coherence, authority, and derived/synthesized representations remain open.
Dense fragments need not be better than contiguous/coherent material. Future
authority-aware selection may distinguish implementation, tests, accepted
architecture, ADR rationale, package documentation, comments, generated
artifacts, historical documentation, and experiments without imposing a
universal ordering. Generated summaries, relationship explanations, compressed
representations, and model-produced summaries require provenance/dependencies
sufficient to distinguish them from source-preserving material and assess
correctness/applicability.

## Status and implementation boundary

This decision accepts Context/disclosure semantics only. It does not implement
a compiler, DisclosureOption, ContextDisclosure, representation/coverage/
satisfaction model, decomposition mechanism, utility/stopping/budget policy,
availability/history store, applicability cache, capability/behavior profile,
assembly layer, tokenizer integration, derived representation, persistence, or
evaluation infrastructure. B-0002 retains this unimplemented design pressure.
ADR-0001 remains the model-native Tool boundary; ADR-0002 remains repository
identity/derivation/graph architecture; ADR-0003 remains InformationNeed,
retrieval, evidence, and ranking architecture.
