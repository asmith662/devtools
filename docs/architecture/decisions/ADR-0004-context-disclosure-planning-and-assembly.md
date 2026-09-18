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
intelligence subjects available through a particular representation or
explicitly characterized transformation. It is not rendered prompt content,
need not map one-to-one to a file/symbol/candidate, and may have origin, form,
fidelity, provenance/dependencies, applicability, expected cost, and
information-contribution characteristics. These are semantic dimensions, not
required fields or a type hierarchy.

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

This disclosure coverage is distinct from ADR-0002 semantic-result coverage.
Disclosure coverage asks what represented information contributes toward a
purpose; semantic-result coverage asks what result space a repository derivation
accounted for sufficiently to support completeness or absence reasoning. Neither
substitutes for the other.

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
made available, through selected disclosure possibilities, representations, or
transformations under its purpose, evidence, constraints, and planning
semantics. A **ContextDisclosure** is the identifiable, provenance-bearing
information artifact actually realized with reference to a DisclosurePlan.
Neither is a ModelRequest. Concrete models, identities, and cardinality are
open: a plan can fail to produce a disclosure, revision creates a new plan, and
future semantics may permit more than one realized disclosure from a plan. Once
established as identified planning/evidence artifacts, plans and disclosures
are immutable.

The materialization boundary is:

```text
DisclosurePlan -> materialization -> ContextDisclosure -> model-input assembly -> ModelRequest
```

Materialization faithfully realizes the disclosure decision selected by the
DisclosurePlan. It can resolve applicable source, extract source-preserving
material, project existing DerivedKnowledge, format or structurally transform
information, and perform a semantic transformation or lossy synthesis when that
transformation was explicitly selected by the plan. For example, a plan may
select a bounded task-focused summary of identified supporting information.
Materialization does not thereby promote that purpose-relative synthesis to
repository DerivedKnowledge.

Materialization must not silently invent a materially different synthesis or
substitute a materially different disclosure decision under the guise of
formatting or faithful realization. When material to correct interpretation,
the realized information preserves its origin, support, assumptions,
uncertainty, conflicts, and purpose-relative nature. Changed dependencies,
inapplicable knowledge, unresolved source, unavailable knowledge, failed
transformation, cost violation, or disclosure policy can make faithful
realization impossible and require an observable failure or later re-planning/
acquisition. No mandatory independent global identity, persistent synthesis
artifact, or synthesis store follows from performing the selected work.

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

Assembly arranges and serializes already-realized disclosure. It must not
silently introduce a new semantic assertion through placement, formatting,
truncation, or token-budget handling. If a semantic compression or synthesis is
needed to fit a consumer constraint, disclosure planning must select it and
materialization must realize it before assembly presents it.

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

A **representational transformation** changes how already available information
is exposed without intentionally establishing a materially new semantic
assertion. It can include source-preserving extraction, selecting a method
signature, formatting, lossless structural representation, or a deterministic
projection whose stated meaning remains the projected information. Computation,
omission, or reorganization alone does not make the result DerivedKnowledge or
synthesis.

An **epistemic derivation** establishes a materially new semantic assertion,
for example explaining why behavior occurs, deriving a call relationship or
transitive reachability, inferring responsibility, or composing a multi-source
narrative. Lossy semantic compression can be epistemic because a summary can
implicitly assert an interpretation. This is a semantic rather than
LLM-versus-deterministic classification: determinism provides reproducibility,
not semantic certainty. The distinction is conceptual and does not authorize a
class, protocol, enum, mandatory artifact, or complete representation taxonomy.

Some epistemic derivations establish reusable repository-relative semantic
intelligence under ADR-0002:

```text
repository support -> identified repository Derivation -> DerivedKnowledge
    -> knowledge projection/materialization
```

Other epistemic work establishes purpose-relative synthesized information for
Context disclosure:

```text
supporting information -> explicitly selected Context synthesis
    -> purpose-relative represented information -> ContextDisclosure
```

The second flow is not automatically repository DerivedKnowledge. It must not
silently present synthesis as source truth or reusable repository intelligence.
Its origin and support remain explicit, and assumptions, uncertainty,
conflicts, completeness limitations, and purpose-relative nature remain
preservable where material. Such information may remain ephemeral or be retained
within future execution/evaluation records; independent identity, persistence,
querying, caching, reuse, and validation mechanisms remain unresolved.

When Context synthesis establishes a genuinely reusable repository-relative
semantic assertion, the work may cross the explicit ADR-0002 derivation boundary
and establish DerivedKnowledge under those semantics. That does not make every
textual summary a Derivation, every representation transformation knowledge, or
every Context-specific judgment persistent repository intelligence.

The semantic-strength invariant across disclosure is:

> Representation selection, projection, synthesis, compression,
> materialization, ContextDisclosure realization, and model-input assembly must
> not silently strengthen an assertion beyond what its source semantics,
> support, assumptions/scope, conflict state, and semantic-result coverage
> justify.

Thus a possible relationship must not become a definite one; a partial result
that found B and C must not become a claim that B and C are the only results;
an approximation must not become exact merely because shorter natural language
is convenient; observed examples must not become an exhaustive set without
coverage support; and source disagreement must not become one synthesized truth
without an identified semantically capable resolution process. Preservation can
require retaining qualification, scope, uncertainty, coverage limitations,
conflict, and source role. This selects no prompt template, serialization, or
phrasing mechanism.

Composite representations may combine multiple provenance-preserving forms,
such as a structural orientation, purpose-relative synthesis, and exact
supporting source, without flattening their constituent origins. Provenance
explains origin and support; it does not by itself establish authority,
certainty, correctness, or truth.

Model-generated synthesis does not become DerivedKnowledge merely because
temperature is zero, its output is reproducible, provenance is recorded,
multiple models agree, a human agrees, or the model expresses confidence. A
later repository Derivation can independently establish relevant repository
semantics. This ADR selects no generic promotion workflow and neither prohibits
nor accepts future learned analyzers under ADR-0002's separately governed
repository-intelligence boundary.

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

ADR-0002 repository intelligence may establish source/resource roles and
related governance or temporal status as reusable repository-relative knowledge.
Such roles are inputs to possible authority assessment, not authority by
themselves. A source can have multiple roles at different granularities; roles
can be ecosystem-specific, derived, or absent. This ADR selects neither a
mandatory `source_role` field nor a closed role taxonomy, `source_priority`,
`authority_score`, or universal precedence such as implementation over tests or
documentation.

Material disagreement among relevant applicable sources is itself preservable
information. Disclosure planning does not generally arbitrate truth or silently
choose a winner: disagreement can reveal defects, stale documentation/tests,
undocumented change, incomplete analysis, or other inconsistency. Synthesis
must not collapse material conflict into an unqualified assertion unless an
identified derivation is authorized and semantically capable of resolving it.
Likewise, absence of found evidence is not evidence of absence unless
acquisition semantics justify that conclusion; this preserves ADR-0003 absence
discipline for authority, synthesis, conflict, coverage, and sufficiency.

Repository-relative semantic conflict follows ADR-0002 vocabulary semantics:
comparability and incompatibility under compatible assumptions/scope matter,
not identical labels, arguments, or differing source strings alone. An ADR-0002
Derivation may establish reusable conflict/divergence knowledge. Disclosure
planning instead decides how purpose-relevant disagreement should be preserved
or represented; it does not become a universal conflict detector or truth-
arbitration engine.

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

Concrete representation-form/taxonomy, fidelity, source-role, authority-
evidence, uncertainty, confidence, completeness, conflict, coherence,
reconstruction-burden, semantic-transformation and synthesis representation,
synthesis validation/fidelity and semantic-strength evaluation,
provenance/support, model-generated information treatment, derivation-
orchestration, materializer,
materialization-evidence, applicability-race/cost-estimator, cache/reuse,
disclosure-authorization, assembly, package/API ownership, and evaluation
mechanisms remain open. So do synthesis identity, persistence, querying,
caching, reuse, conflict-preserving mechanisms, and any promotion of
interpretive knowledge. Derived and synthesized representations retain the
origin/support discipline above without selecting when or how they are produced.

## Status and implementation boundary

This decision accepts Context/disclosure semantics only. It does not implement
a compiler, DisclosureOption, DisclosurePlan, ContextDisclosure,
representation/coverage/satisfaction model, decomposition mechanism,
utility/stopping/budget policy, availability/history store, applicability cache,
capability/behavior profile, assembly layer, tokenizer integration, derived
representation, semantic-transformation or synthesis mechanism, synthesis
store, persistence, or evaluation infrastructure. B-0002 retains this
unimplemented design pressure.
ADR-0001 remains the model-native Tool boundary; ADR-0002 remains repository
identity/derivation/graph architecture; ADR-0003 remains InformationNeed,
retrieval, evidence, and ranking architecture.
