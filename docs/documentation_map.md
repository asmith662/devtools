# Documentation Map

## Authority and ownership

- [Central architecture](architecture.md) is the canonical current and accepted
  system-architecture overview: domains, boundaries, dependency direction,
  cross-domain composition, and whether architecture is implemented/current or
  accepted but not implemented. It must be understandable without replaying all
  ADRs.
- [Architecture taxonomy](architecture/taxonomy.md) defines semantic vocabulary
  and non-equivalence. It does not replace the architecture overview.
- [Accepted architecture decisions](architecture/decisions/) preserve decision
  rationale, alternatives, consequences, and historical evolution. They explain
  why architecture was chosen; they are not the sole current-state specification.
  ADR-0001 defines ModelInteraction/Tool semantics; ADR-0002 repository identity,
  snapshot observation/delta/maintenance, subjects/source occurrences,
  repository DerivedKnowledge jurisdiction, epistemic-derivation/
  representational-transformation boundary, semantic-result coverage/absence,
  repository conflict/source-role knowledge, external-semantic-dependency and
  observation boundaries, capability-realization contract, and graph semantics;
  ADR-0003
  InformationNeed/retrieval/ranking; and
  [ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
  Context/disclosure planning, purpose-relative synthesis, materialization of
  explicitly planned transformations, semantic-strength preservation,
  representation-origin, and model-input assembly semantics.
- [AGENTS.md](../AGENTS.md) defines repository-operating rules.
- Package-local documentation defines detailed implemented public APIs, package
  design, lifecycle/operational behavior, and usage. Central architecture
  summarizes system-level ownership and links outward; it does not duplicate
  every package contract.
- Source and tests define the final implemented behavior where documentation is
  incomplete.
- Backlog records unresolved/future pressure; [roadmap](roadmap.md) records
  sequencing; the implementation ledger records implementation/history; and
  experiments are evidence. None is canonical current architecture or
  independently authorizes implementation. Historical terminology remains
  historical unless a clarification is needed to prevent a current-state error.

## Package documentation

- Core: [identity](../src/devtools/core/identity/docs/overview.md),
  [paths](../src/devtools/core/paths/docs/overview.md),
  [time](../src/devtools/core/time/docs/overview.md),
  [regex](../src/devtools/core/regex/docs/overview.md), and
  [conversion](../src/devtools/core/conversion/docs/overview.md).
- Resources: [commands](../src/devtools/resources/commands/docs/overview.md)
  and [filesystem](../src/devtools/resources/filesystem/docs/overview.md).
- Models: [interaction](../src/devtools/models/interaction/docs/overview.md),
  [serving](../src/devtools/models/serving/docs/overview.md), and
  [benchmarks](../src/devtools/models/benchmarks/docs/overview.md).
- Agents: [conversation](../src/devtools/agents/conversation/docs/overview.md)
  and [Codex integration](../src/devtools/agents/integrations/codex/docs/overview.md).
- Execution: [Runtime](../src/devtools/execution/docs/overview.md).
- Observability: [Evidence](../src/devtools/observability/evidence/docs/overview.md).
- Persistence: [overview](../src/devtools/persistence/docs/overview.md),
  [JSON](../src/devtools/persistence/docs/json.md), and
  [SQLite](../src/devtools/persistence/docs/sqlite.md).
- Tools: [overview](../src/devtools/tools/docs/overview.md).

The `context` domain exposes narrow Repository Intelligence APIs. Its current
implementation can recursively discover regular-file addresses beneath an
explicit root using metadata only, caller-supplied maximum counts for examined
filesystem entries and discovered resources, lexical ordering, and conservative
link skipping. Discovery produces addresses, not contents, occurrences,
language classification, relevance, or snapshot state. A separate bounded
`RepositoryTextCorpusDefinition` retains a completed discovery and the exact
caller-selected subset of its discovered addresses in discovery order. It records
only future textual-corpus membership intent: it performs no observation and
makes no content, text-validity, classification, or relevance claim. Bounded
observation can subsequently acquire the selected collection, and an identified
`RepositoryTextCorpus` can retain exactly those selected observed occurrences.
Its identity is dependency-scoped to the logical Repository and selected
address/content identities, not all observed snapshot state. It is not an index
or retrieval mechanism; BM25 is not implemented. A separate bounded
whole-resource representation can turn every `RepositoryTextCorpus` member into
one `RepositoryTextDocument`, retaining exact observed text and resource
correlation in corpus order. This is a current representation strategy rather
than a universal one-resource-one-document rule; it does not tokenize, index,
rank, or retrieve. Resource addresses remain available for later structural or
path-sensitive retrieval evidence. A separate bounded
`context.retrieval` baseline lexical mechanism observes each document's ordered
Unicode-regex `\w+` spans, retaining exact text, offsets, encounter order, and
casefolded terms. It is heterogeneous rather than Python-specific: punctuation
and whitespace separate spans, repeated spans remain repeated, and camelCase,
PascalCase, and snake_case are not decomposed. Corpus-level statistics now retain
observation-count document lengths, document-local term frequencies,
distinct-document frequencies, and average document length (`0.0` for an empty
collection); a content-only inverted index retains direct observation/document
correlation in first-encounter vocabulary and document posting order. It has no
parser or path scoring. The current bounded BM25 operation analyzes query text
with the same spans and `casefold()` rule, retains repeated query evidence while
scoring distinct terms, and uses `k1 = 1.2`, `b = 0.75`, and
`ln(1 + (N - df + 0.5) / (df + 0.5))` IDF. It retains local score-contribution
evidence, ranks positive content matches by descending score with document-order
tie breaking, and requires a positive maximum-result bound. Empty/OOV cases are
successful zero matches; it has no structural, path, Context-selection, or
quality claim. A separate bounded
Python-function-path projection nominates exact, case-sensitive `.py` addresses
for observation without inspecting content; this is candidacy evidence rather
than proof of Python source. The observation operation then reads a finite
caller-declared collection of UTF-8 text resources into identified snapshot
state. For an exact Python function-name
purpose, a bounded pre-analysis selector filters an explicit caller-ordered set
of those resources by exact stdlib `NAME` token presence. Its candidates are
purpose-relative predictions with expected false positives, not declaration
knowledge, and zero applies only to the eligible set. The domain derives
source-grounded knowledge from one explicitly selected occurrence for direct
module-body Python function declarations with exhaustive bounded coverage. A
bounded composition operation retains independent analyses for an explicit
caller-ordered resource selection
and exposes their existing knowledge as one sequence for retrieval. It
also provides exact declared-name retrieval over supplied declaration knowledge,
with purpose-relative match evidence and no ranking. A bounded projection of
that evidence identifies distinct matching resources in first-match order while
retaining every supporting declaration match; it does not choose resources to
analyze or drive Context disclosure. The domain also provides a bounded all-match
Context disclosure that projects established declaration and source-location
information. A separate bounded materializer validates explicitly supplied
identified snapshot state and adds exact UTF-8 source segments without
filesystem reacquisition or parsing. A purpose-specific renderer transforms
that materialized Context into deterministic human-readable text while
preserving exact source, order, duplicates, and correlation; it does not create
a model message or request. A bounded composition operation separately accepts
an existing caller-owned `ModelRequest`, preserves its request semantics, and
places that rendered Context after its distinct primary task in a new request
without execution or Conversation mutation. The domain does not provide
Git-aware or language-classifying discovery, capability/execution
infrastructure, broader retrieval, a generic Context compiler, or general
ModelRequest assembly. Current durable
conversation semantics remain in `agents.conversation`, and `context` does not
own former Message/History/Session semantics.

The `orchestration`, `governance`, and `evaluation` domains remain recognized
sparse namespaces without reusable implementation APIs. Current accepted
Evaluation responsibility and boundaries are summarized in the central
architecture and taxonomy; no Evaluation ADR or reusable framework API is
currently established.

## Experiments and scripts

`experiments/` is non-installable composition and may depend on `devtools`;
reusable source must not import it. [Qwen experiment documentation](../experiments/qwen/docs/overview.md)
describes the bounded read-only experiments. Operational entry points remain
under `scripts/`.

## Backlog navigation

[Backlog overview](backlog/overview.md) is the canonical record index, grouped
by stable ID, lifecycle status, and primary domain. [Backlog metadata](backlog/metadata.md)
defines ownership, split-lineage, dependency, and promotion terminology.

## Update workflow

For an implemented behavior change, update package documentation first, then
this map and architecture documentation when navigation or cross-package
ownership changes. Update an accepted ADR when an approved cross-package
decision changes. Preserve historical records as history rather than rewriting
them to conceal a former architecture.
