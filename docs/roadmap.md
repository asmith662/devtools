# Roadmap

## Purpose

This document records deliberately selected current sequencing. It is not an
API reference, a replacement for the canonical backlog, or authorization to
implement a future domain. The [architecture taxonomy](architecture/taxonomy.md)
defines terms; [architecture](architecture.md) defines current ownership; the
[backlog](backlog/overview.md) preserves unresolved pressure.

## Established architecture

The twelve-domain framework architecture is established:

```text
core/ resources/ models/ agents/ context/ tools/
execution/ orchestration/ governance/ observability/ persistence/ evaluation/
```

Current implemented seams include the core and resource substrates,
`Prompt -> ModelInteraction -> ModelResponse`, durable `Conversation` and
`ConversationMessage` state, narrow execution `Runtime` with specialized
`InteractionAttempt`, terminal Evidence in observability, Conversation
persistence, Tools, model serving and benchmarks, and the external Codex Agent
integration. Sparse domains are intentionally not implementation commitments.

Historical pre-migration milestones, including former Session, Interaction,
and Evidence ownership terminology, remain in the
[implementation ledger](implementation_ledger.md) as history only.

## Current sequencing

### Current — production consolidation after retrieval breadth

The Tier-1 breadth sprint through Increment 36 is complete. The
[breadth evidence and production gate](research/repository-retrieval-breadth-production-gate.md)
records its empirical limits and dispositions; the prospective Increment 27
sequence and earlier retrieval checkpoint below remain historical. Direct
Imports and bounded References/direct Calls supplied useful complementary
resource reach. Graph depth caused large fan-out, and structural selection at
K=5 is unresolved. Canonical lexical retrieval remains the production baseline;
no union, graph expansion, dense model, or fusion policy is promoted.

Proceed in dependency order: (1) bounded source-grounded Python function
Reference/direct Call Repository Intelligence; (2) qualified immediate package
membership; (3) a narrow cross-domain Evaluation assessment/coverage kernel;
(4) direct retrieval candidate generation consuming production typed facts;
(5) one fine-grained Context disclosure slice using exact spans, qualified
relations and progressive pointers; (6) bounded structural selection research
and later Learning convergence only after their prerequisites. Item 1 is the
first completed production implementation increment. Qualified immediate
package membership is next. Preserve frozen experiments
as evidence and remove duplicate derivation from future consumers only after
production parity is established. Confirmation remains sealed until a specific
executable selection policy exists; no shadow or independent-repository claim
follows from these development results.

### Ongoing — documentation integrity and backlog rebase

- [B-0001](backlog/epics/B-0001-architecture-documentation-integrity.md) and
  [B-0006](backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md)
  keep current documentation, roadmap sequencing, and backlog pressure aligned
  with the established architecture.

### Historical starting point — bounded Repository Intelligence and retrieval evidence

- [ADR-0002](architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
  establishes semantic architecture for Repository identity, snapshots,
  RepositorySubjects/SourceOccurrences, Derivations, DerivedKnowledge, graph
  semantics, snapshot observation/delta/incremental-maintenance, minimum
  derivation/knowledge semantics, repository DerivedKnowledge jurisdiction,
  qualified epistemic semantics, semantic-result coverage/absence,
  repository conflict/source-role knowledge, epistemic-derivation/
  representational-transformation distinction, capability-realization boundary,
  and Context boundaries.
  [ADR-0003](architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
  establishes InformationNeed, retrieval evidence/planning, and ranking
  semantics. [ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
  establishes Context/disclosure planning, materialization, provenance-bearing
  disclosure artifacts, representation origins, purpose-relative synthesis,
  explicitly planned semantic transformation and semantic-strength preservation
  during materialization/assembly, and model-input assembly semantics.
  [B-0002](backlog/epics/B-0002-coding-context-substrate.md)
  retains the unimplemented design pressure. These decisions are not authorization
  for a general Context compiler, disclosure model, parser, graph store, retrieval
  system, Memory, Agent loop, or orchestration system; the current bounded lexical
  index, bounded filename-field BM25 baseline, deterministic fixture evaluation, and small real-repository
  benchmark do not settle those broader responsibilities.
  [B-0008](backlog/items/B-0008-investigate-repository-context-discovery.md)
  remains superseded historical navigation evidence.

- The selected starting hypothesis began with direct module-body Python function
  declaration knowledge. The bounded implementation tests the proposition in
  which direct module-body `ast.FunctionDef` and `ast.AsyncFunctionDef` source
  occurrences in an identified RepositorySnapshot syntactically declare
  distinct snapshot-local function RepositorySubjects. Subsequent bounded
  production slices establish direct module-body import-declaration syntax and
  explicit-root Python module interpretation for selected observed `.py`
  resources. The first slices did not implement import resolution, repository
  dependency relationships, graphs, retrieval integration, or runtime import
  semantics.
  A subsequent bounded resolver now resolves eligible import module portions only
  within an explicit module-interpretation universe. A bounded relation
  derivation now retains directed declaration-grounded source-to-target module
  relations only for qualified resolved outcomes; it does not establish runtime
  imports or retrieval relevance, and is not integrated into production
  retrieval. The resolver and relation derivation remain distinct from runtime
  import semantics.
  These are design targets, not fixed production representations or a universal
  declaration ontology. [B-0002](backlog/epics/B-0002-coding-context-substrate.md)
  preserves the exact scope, design pressure, and deliberate deferrals.

- Increment 23 completes the independent blinded validation of Increment 22's
  rule. Its repaired pipeline freezes 96 judgments and preserves disagreement
  among control expectation, blinded usefulness, and post-unblinding review.
  The rule has zero net known-useful gain, one not-useful admission, and one
  useful rank-five loss; it is `NOT_READY_FOR_SHADOW` and not production-ready.
  Lexical top fifteen contains all known-useful material resources, so this
  checkpoint points toward measuring candidate coverage and ranking depth
  separately, not further tuning of the single reservation slot. Production
  retrieval/disclosure remains unchanged; no generic experiment platform,
  Selector, or production Context influence is authorized.

### Architecture review gate — crossed with preserved seams

The broad repository-intelligence architecture investigation has occurred. The
work included architecture reconstruction/archaeology, rationale steelmanning,
external adversarial/Deep Research review, finding-by-finding reconciliation
across multiple focused passes, and a preservation audit. Repository identity,
subjects/source occurrences, snapshots/maintenance, derivation/knowledge,
capability realization, graph views, retrieval/ranking, Context disclosure,
synthesis, authority/conflict boundaries, and semantic-strength preservation
are considered sufficiently settled at the foundational semantic level. The
focused external-semantic-state/dependency-identity/applicability/replay Deep
Research investigation has also completed and its accepted findings have been
reconciled into ADR-0002 without selecting concrete mechanisms.

The focused integrated-evaluation/causal-attribution investigation has now
completed its substantive analysis and its accepted findings have been
reconciled into the canonical architecture. Evaluation is a distinct semantic
responsibility, but no universal Evaluation framework, Episode, score, causal
graph, trajectory, store, or lifecycle is accepted. The producing research
process did not complete its dossier's final mechanical artifact-integrity
verification; subsequent review and reconciliation treated the dossier as
research evidence rather than an accepted or mechanically verified decision.

The implementation-start assessment is **SAFE WITH PRESERVED SEAMS**. The core
semantic architecture is sufficiently settled, and B-0002's bounded-slice
promotion trigger is now met at the design level by the selected starting
hypothesis. This sequencing decision does not itself authorize production
implementation. Initial design must retain the semantic basis and correlation
needed for later local-correctness, downstream-utility, resource, and marginal-
contribution evaluation without first building generic Evaluation
infrastructure.

The recovered [research evidence](research/README.md) has been reconciled into
canonical research records and linked ADR dispositions. It preserves historical
alternatives and deferrals; it neither authorizes implementation nor converts
research recommendations into roadmap commitments.

Later external adversarial/Deep Research confirmation remains a confirmation/
reopen gate, not an implementation-start gate. It can reopen foundational
architecture if it discovers a material contradiction or missing semantic
capability. This roadmap state does not authorize implementation, mark B-0002
complete, claim Evaluation infrastructure exists, or settle implementation-
shaped choices.

### Later — promotion only when evidence is sufficient

The canonical backlog contains deferred pressure for generic execution
lifecycle promotion, model-facing Tool and Action boundaries, Agent semantics,
orchestration, governance, durable observability, and advanced model
interaction. Each remains subject to its own dependencies and promotion
conditions. The Qwen probes are experimental evidence, not reusable framework
promotion.

## Validation cadence

Use deterministic validation for implemented changes. Add task-specific live
acceptance only when a meaningful specialized path exists; live evidence tests
framework enforcement and causal boundaries, not voluntary model obedience.

See [documentation_map.md](documentation_map.md) for authority and navigation.

## Historical retrieval evidence checkpoint

Increment 24's offline comparison over Increment 23's retained six-case surface
does not promote a ranker: its frozen purpose-relative deterministic arm recovers
9 known-useful resources versus 10 for lexical/native ranking. The reconciled
[structural-retrieval research](research/structural-repository-retrieval.md)
changed the Increment 25 question from how relationship evidence should occupy
K=5 to which evidence families expose complementary useful resources. The
[repository-retrieval landscape](research/repository-retrieval-algorithm-landscape.md)
now directs the next experiment toward foundational retrieval variables.

- **Increment 25 (complete):** the frozen `devtools` confirmation compared
  one-hop outgoing imported-member function-binding expansion from lexical
  top-five seeds with candidate-volume-matched lexical widening. Structural
  expansion fired in 12/16 cases and produced 31 additions: 17 useful and 14
  not useful. Of the useful additions, seven overlapped matched lexical
  widening, ten were structural-only, and five had no positive lexical rank.
  Matched lexical widening produced 15 useful and 16 not-useful additions,
  including eight useful lexical-only resources. This repository-local result
  retains the imported-member family as validated structural evidence without
  authorizing production retrieval, common graph infrastructure, or ranking
  changes.
- **Increment 26 (development complete):** the frozen CodeRankEmbed comparison
  found eight useful semantic-only top-five resources. All eight had a deeper
  positive lexical rank, so this is top-K/ranking complementarity, not evidence
  of useful lexical-unreachable resources. Preserve its valid development
  evidence and sealed confirmation population. Confirmation is suspended
  pending a decision-worthy future comparison; it is neither completed nor
  rejected. No trained ranker or vector database follows from this result.
- **Increment 27 — Repository Retrieval Foundations: unit, representation,
  fielding, fusion, and ranking-depth falsification:** test the ceiling and
  failure modes of inexpensive code-aware retrieval. Measure Recall@K over
  depth; exact symbol/path/error resolution or routing where applicable;
  resource, declaration/AST-aware, and useful fixed-window retrieval units;
  exact identifiers plus
  subtokens, code-aware lexical text, and path/module/symbol/content fields;
  deterministic query-clue extraction while preserving the InformationNeed;
  a small BM25 sensitivity check; character n-gram auxiliary retrieval; cheap
  union/interleaving/Reciprocal Rank Fusion; already validated structural
  evidence; and compact repository/symbol-map disclosure where appropriate.
  Keep retrieval unit distinct from disclosure unit. This is a bounded
  falsification program, not a generic retrieval framework.
- **Later, conditional evidence:** test additional typed relations, lightweight
  learned ranking only after a high-recall pool exists, and persistent-index
  neural retrieval with a competitive model only if cheaper baselines leave a
  decision-worthy gap. Any broader evidence-family comparison depends on the
  foundations results; no later increment is selected yet. Falsify surviving
  claims on independently selected repositories before broader generalization
  or production promotion. Consider non-controlling shadow comparison only
  under separate governance and later supporting evidence.

Evaluate stages separately: poor broad Recall@K points to candidate generation;
good broad recall but poor small-K ordering points to ranking; good ordering
but poor useful information per disclosure budget points to representation and
Context disclosure. Cheap follow-up inspection/search can also change the
value of one-shot ranking. These are diagnostic guides for experiments, not
fixed architecture or a universal score.

The broader portfolio remains heterogeneous: typed structural/relational views,
semantic/pretrained-representation evidence, and later learned decision models
are separate hypotheses with native evidence semantics. Repository Intelligence
owns qualified typed facts; whether future structural navigation uses independent
views, a unified typed substrate, or relation/index projections remains an
operational question. Shadow execution, if later justified, follows offline and
independent validation and remains non-controlling until separately promoted.
