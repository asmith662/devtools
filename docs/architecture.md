# Architecture

`devtools` is organized by responsibility. This document is the canonical
overview of current and accepted system architecture: it records domains,
cross-package ownership, dependency direction, and cross-domain composition.
[The taxonomy](architecture/taxonomy.md) defines semantic terms; package-local
documentation defines exact implemented APIs; and
[architecture decisions](architecture/decisions/) preserve rationale and
historical evolution. Accepted architecture is summarized here as well as in
its ADR, while accepted-but-unimplemented semantics never claim a current API.

A first-class semantic distinction does not by itself require a separately
identified, persistent production artifact. Concrete artifacts remain permitted
when independent lifecycle, replay, persistence, reuse, authority, or other
evidence establishes their value.

## Reading architectural and implementation status

An architectural domain can be recognized while its reusable implementation is
sparse; accepted ADR semantics can exist before a production API. Conversely,
implemented package behavior can remain experimental or unfrozen without making
the domain boundary unsettled. ADR acceptance is not implementation completion.
For exact current APIs and their maturity, follow package documentation and
source/tests; use the taxonomy's status labels for semantic vocabulary rather
than as a single implementation-lifecycle scale.

## Domains

```text
core/           foundational values and transformations
resources/      reusable filesystem and process access
models/         model interaction, serving, and benchmarks
agents/         durable conversation and external agent integrations
context/        bounded repository observation and future repository intelligence/Context
tools/          typed controlled capability boundaries
execution/      narrow Runtime and specialized InteractionAttempt lifecycle
orchestration/  reserved workflow coordination
governance/     reserved authority and policy responsibility
observability/  Evidence and diagnostic observation
persistence/    durable representation storage and restoration
evaluation/     reserved reusable evaluation responsibility
```

Sparse domains are intentional. Their presence does not authorize speculative
APIs.

## Current boundaries

```text
ConversationMessage
    -> Prompt
        -> ModelInteraction
            -> ModelResponse
                -> materialized ConversationMessage
```

`Runtime` coordinates that one-model exchange for one `Conversation`. It owns
neither agent loops nor orchestration. With an execution observer configured,
it creates and terminalizes a specialized `InteractionAttempt`. Execution does
not depend on observability. `ExecutionInspector` in observability observes
attempt facts, constructs immutable terminal Evidence, and optionally forwards
it to an EvidenceSink.

`CodexAgent` is an external Agent integration under `agents.integrations`; it
does not implement `ModelInteraction`. `LlamaCppInteraction` is a configurable
model provider under `models.interaction.providers`. Model serving makes an
endpoint available; model interaction communicates with it.

Resources are not Tools. Resources provide reusable lower-level access;
Tools adapt bounded typed capabilities for controlled invocation. Tool
validation is not authorization.

Persistence stores and restores Conversation representations. It keeps the
established durable JSON and SQLite wire/schema names where compatibility
requires them; storage does not own conversation semantics.

## Dependency direction

```text
core <- resources <- models
core <- resources <- tools
models, tools, resources <- agents
models, agents <- execution
execution <- observability
agents <- persistence
experiments -> devtools
devtools -/> experiments
```

The diagram permits only dependencies justified by a concrete package API.
Notably, core does not depend upward, model interaction does not depend on
Codex, execution does not depend on observability, and Runtime does not own
orchestration.

## Principles

- Model is not Agent; ModelResponse is not AgentResult.
- Conversation is not Run; generic Run, Step, and Attempt remain future work.
- Context is not Memory or Persistence.
- Evidence is not Trace, Telemetry, or present authority.
- Provenance explains origin/support; it does not itself establish authority,
  certainty, correctness, or truth.
- Model proposal, Tool visibility, and Tool validation are not authorization.
- Cancellation is not rollback, and communication failure does not prove an
  external effect did not occur.

## Accepted ModelInteraction boundary

[ADR-0001](architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
approves a cohesive ModelInteraction boundary: immutable semantic
requests and settings, typed provider-only request extensions, normalized
model-native Tool calls, capture-controlled model interaction Evidence, and
serving-profile provenance. Its phased implementation preserves that models
never execute Tools, Tools do not depend on model providers, Runtime remains
narrow, and raw provider exchange data stays outside `ModelResponse`.

All three ADR-0001 phases are implemented; package documentation and source
remain authoritative for exact current APIs.

## Accepted repository-intelligence semantics

[ADR-0002](architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
accepts future semantic architecture for Repository identity, content-derived
RepositorySnapshots, derivation-aware DerivedKnowledge, and distinct derivation
and repository-relationship graph families. RepositorySubject is the
snapshot-local identifiable repository thing about which intelligence may make
assertions; SourceOccurrence is a snapshot-local source anchor within a
ResourceOccurrence and is not automatically a subject. Subjecthood and
DerivedKnowledge are orthogonal: analysis may establish a subject, while
Derivations establish knowledge about subjects, source occurrences, resources,
and other dependencies. Subject identity is not a path/range, name, qualified
name, AST node, or cross-snapshot continuity claim.

Typed containment, declaration, reference, call, import, inheritance, and
other relationships remain DerivedKnowledge. Their semantics do not select a
physical graph representation. The preferred current posture is canonical
typed relationship knowledge, relation-specific indexes/traversal support when
justified, and ephemeral typed structural projections for particular consumers.
A future unified typed substrate or independently materialized view remains
possible only with concrete consumer and measurement evidence. Views choose
suitable node domains: they may reuse subjects and source occurrences, or use
local derived nodes without making every graph node a RepositorySubject. Shared
mechanics may compose compatible typed views, but do not define relationship
semantics or create universal node identity. There is no universal repository
hierarchy, semantic graph, graph store, graph database, or foundational Chunk.
This also preserves Context as purpose-relative selection and disclosure rather
than repository truth.

Relationship labels are illustrative, not universally unqualified Booleans;
their knowledge-family semantics determine qualification. Repository-relative
conflict/divergence knowledge can itself be DerivedKnowledge when a derivation
defines semantic comparability and incompatibility under compatible
assumptions/scope. Source/resource roles and governance or temporal status can
likewise be derived knowledge useful to downstream authority assessment. No
universal conflict engine, mandatory source-role field/taxonomy, or source
precedence is accepted; purpose-relative trust remains an ADR-0004 concern.

A RepositorySnapshot is an immutable, logically complete successfully observed
state under explicit snapshot/observation semantics. Completeness is relative
to declared inclusion and consistency guarantees, not physical copying, a full
rescan, or repository-intelligence completeness. Observation must not claim a
stronger simultaneous-state guarantee than its mechanism establishes; watcher
events are only future triggers/hints. Snapshot identity is deterministic and
content-derived, but digest construction, policy-to-state-identity treatment,
and observation mechanisms remain open. ContentIdentity is address-independent
and reusable; ResourceOccurrences remain snapshot-local.

SnapshotDelta is a difference relationship between states, and
IncrementalMaintenance is the process of efficiently establishing applicable
knowledge. Neither defines repository state or identity. Immutable logical
snapshots and reuse are complementary: applicable DerivedKnowledge can serve
multiple snapshots without copying or rebinding, while missing/inapplicable
knowledge is rederived as required. Applicability follows actual semantic
dependencies, which may include content, occurrences, subjects, source anchors,
other knowledge, snapshot facts, or derivation semanticsâ€”not a fixed
path/content pair or local-versus-relational category. Applicability,
invalidation discovery, rederivation, and cache lookup remain separate.

Repository intelligence distinguishes an identified **DerivationDefinition**
(reusable semantic computation), a **Derivation** (that definition applied to
explicit direct semantic dependencies), a particular execution/Attempt that may
realize it, and the zero-or-more immutable **DerivedKnowledge** artifacts it
may establish. Definitions are not necessarily executable bindings; executions
and their Evidence are not repository truth. Dependencies are role-bearing
semantic inputs rather than incidental execution settings, and direct
dependencies need not flatten transitive closure. Dependencies differ from
provenance: shared derivation provenance and result-specific support may both
matter.

These are distinct semantic roles, not a requirement for four heavyweight
subsystems or one production class per role. DerivedKnowledge does not include
every temporary/intermediate computation value, and dependency/provenance
records need not capture every implementation access or duplicate shared support
per result. Granularity must preserve correct applicability; finer tracking is
an optimization justified by reuse gained versus bookkeeping, maintenance, and
provenance cost.

DerivedKnowledge is repository-relative semantic intelligence established by an
identified Derivation; it is not a universal container for every semantic
assertion or provenance-bearing item in the system. Its meaning can include
explicit assumptions, approximation, uncertainty, scope, and completeness.
Deterministic computation does not imply semantic certainty. Representational
transformation of already available information is distinct from epistemic
derivation that establishes a materially new assertion, and not every epistemic
derivation belongs to repository intelligence. These are semantic distinctions,
not requirements for new production classes or artifacts.

DerivedKnowledge does not mean hard or infallible fact. The identified
DerivationDefinition/result vocabulary determines whether a result means
definite, possible, necessary, conservative, ambiguous, unresolved, bounded,
exhaustive, partial, or another explicitly qualified relationship,
classification, semantic property, or result.
Conceptual `MAY_CALL`, `MUST_CALL`, and `CANNOT_CALL` results would therefore be
different propositions, not confidence levels on one generic `CALLS` fact; no
universal predicates or qualifier encoding are selected. Nor is there a
foundational Claim/Assertion/Proposition layer spanning repository intelligence,
retrieval evidence, Context synthesis, and authority judgments.

DerivedKnowledge is not snapshot-owned and has heterogeneous value shape.
Applicability is an external assessment, not mutable knowledge state. Zero
results do not prove absence, positive results do not prove exhaustive coverage,
and failed or partial execution does not automatically negate independently
established knowledge. Definition, derivation, execution, and knowledge
identities remain distinct; concrete models, compatibility/versioning,
provenance, execution integration, and coverage mechanisms remain open.

Semantic-result coverage describes which result space a derivation/result set
accounted for under its scope, assumptions, and semantics; it is not ADR-0004
purpose-relative disclosure coverage. Execution success is not completeness,
partial analysis is not failure, unsupported territory is not negative
knowledge, and absent knowledge normally means unknown/not established. Absence
has negative force only when derivation semantics and sufficient coverage
justify it. Assertion/result, dependencies, assumptions/scope, provenance,
coverage, applicability, and execution Evidence remain distinct without
requiring one production object per distinction.

Repository-intelligence capability is semantic-capability-first: it is the
currently available ability to realize compatible DerivationDefinition
semantics, distinct from that definition and from a particular implementation
binding. Registration/discovery exposes available realizations; it does not
create semantic definitions or alter historical knowledge. Maintenance planning
determines required semantic work, capabilities realize admitted bounded work,
and execution performs the chosen realization. This does not assign cache/reuse,
prerequisite planning, global scheduling, or caller information needs to an
individual capability.

Capabilities receive bounded repository-state and dependency access capable of
accounting for semantically consumed inputs. Dynamic discovery is permitted,
but finalized dependencies must make consumed semantic state explicit for replay
and applicability. “Consumed” denotes semantic support rather than an
instrumentation trace of every operational access. Foundational repository
intelligence is deterministic,
LLM-independent, and observational with respect to the analyzed repository;
it is not Tool, Agent, retrieval, Context compiler, or generic Runtime
semantics. Internal admission for bounded deterministic work differs from
ADR-0001 model Tool authorization. Concrete bindings, registries, selection,
admission, evidence, scheduling, and package APIs remain open.

This deterministic foundational preference concerns realization behavior, not
semantic certainty. A future explicitly accepted learned/probabilistic analyzer
could establish only the qualified prediction, classification, heuristic, or
approximation its DerivationDefinition defines; it could not silently strengthen
that output into an unqualified fact. No such analyzer or infrastructure is
selected.

Analyzer-established structural decomposition may establish subjects. Further
repository-semantic decomposition (for example a failure path or responsibility)
is DerivedKnowledge by default. Purpose-relative information-purpose
decomposition and purpose-relative composite disclosure are downstream concerns
under ADR-0003/ADR-0004; neither makes resulting demands or disclosure units
into RepositorySubjects.

Current `context` implementation includes bounded recursive discovery of regular
file addresses beneath an explicit resolved root. The operation is correlated
to a logical Repository, requires positive maximum counts for both examined
filesystem entries and discovered regular resources, skips symbolic links and
Windows junctions, and returns canonical repository-relative addresses in
lexical order. It uses filesystem metadata without reading file contents.
Discovery does not create resource occurrences, content identities, or a
RepositorySnapshot, and it assigns no language or relevance semantics.
Successful empty discovery applies only to that root and local mechanism; a
required traversal failure or exceeded bound publishes no partial result. These
recursion, link, and bound choices are local implementation semantics, and the
sequential metadata traversal makes no atomic or race-free filesystem claim.
They are not universal Repository architecture.

Current `context` implementation also has an immutable
`RepositoryTextCorpusDefinition`: it retains one completed discovery and the
exact caller-selected subset of its addresses, projected into discovery order.
It can expose only the complementary meaning “discovered but not selected.”
This is explicit future-textual-corpus membership intent, not a corpus,
observation, content claim, classification, or relevance claim; in particular,
construction does not read resources. Bounded UTF-8 observation can then supply
the selected occurrences to an identified `RepositoryTextCorpus`. The corpus
retains that definition and exactly its selected observed occurrences, ordered
by the definition. Its local identity is scoped to the logical Repository and
selected address/content identities, rather than all snapshot state; unrelated
observed resources do not become corpus members or identity inputs. A
RepositorySnapshot is therefore not a RepositoryTextCorpus. Neither value
classifies resources or implements indexing, BM25, or retrieval.

Current `context` implementation can deterministically represent each
RepositoryTextCorpus member as one whole-resource `RepositoryTextDocument`.
The document retains its exact observed occurrence and text, including its
repository-relative address and content identity through that correlation. Its
identity is scoped to the logical Repository, that address, that content
identity, and the explicit whole-resource representation semantics -- not the
whole corpus or unrelated members. `RepositoryTextDocumentCollection` retains
the corpus and documents in corpus order. This is one faithful representation
strategy, not a universal one-resource-one-document rule: future structural,
section, symbol, or bounded-chunk strategies remain open. It performs no
tokenization, indexing, ranking, or BM25 retrieval, while preserving paths for
future structural/path signals.

Current `context.retrieval` implementation provides one baseline heterogeneous
lexical analysis over RepositoryTextDocuments. It observes ordered Python
Unicode-regex `\w+` spans (Unicode letters/numbers and underscore), retaining
each exact span, string offsets, encounter ordinal, and `casefold()`-normalized
term. Punctuation and whitespace separate spans; repeated spans remain repeated;
camelCase/PascalCase and snake_case spans are not decomposed. This is lexical
document observation, not parsing, language classification, repository
knowledge, retrieval evidence, ranking, or Context selection. Address/path
evidence remains separate from document-content lexical observations. Collection
analysis simply composes independent document analyses in document order.

Current retrieval implementation can also derive lexical corpus statistics and
a content-only inverted index from one exact collection analysis. Document length
is its number of lexical observations; term frequency is the number of one
normalized term's observations in one document; document frequency is the count
of distinct documents containing that term; and average document length is the
arithmetic mean across all documents, including zero-observation documents
(`0.0` for an empty collection). Vocabulary follows first lexical encounter in
document order, and postings follow document order while retaining direct
document-analysis and observation correlation.

Current retrieval implementation can analyze a query with those same Unicode
span and `casefold()` semantics, retaining repeated query observations but scoring
only its distinct normalized terms in first encounter order. It performs bounded
Okapi BM25 retrieval with defaults `k1 = 1.2` and `b = 0.75`, using
`ln(1 + (N - df + 0.5) / (df + 0.5))` for IDF and the standard saturated,
length-normalized contribution
`IDF * tf * (k1 + 1) / (tf + k1 * (1 - b + b * length / average_length))`.
OOV terms remain query evidence with no
posting or score contribution. Positive matches retain term-level TF, DF, IDF,
document length, average length, and contribution evidence; they rank by
descending score, with existing document order breaking ties, and require a
positive maximum-result bound. Production additionally scores the final filename
stem as an independent field with the same spans and `casefold()` semantics,
excluding extensions and all directory/path components. Its independent TF, DF,
length, average-length, postings, and term evidence produce a second BM25 score;
matches rank by `content_score + 0.25 * filename_score` with retained field-level
evidence and the same document-order tie break. Filename state never changes
content statistics. Empty, OOV-only, and empty-index retrievals succeed with
zero matches. This does not implement identifier decomposition, full-path or
package proximity, structural/language signals, Context selection, retrieval
quality, or general repository retrieval sufficiency.

Current retrieval implementation can deterministically evaluate one retained
bounded BM25 result against fixture-designated relevant
`RepositoryResourceAddress` values. Relevance is binary, case-local ground truth
for that evaluation—not repository truth, score-derived inference, or model
judgment. Evaluation retains the exact result, recovered relevant resources and
ranks, and designated resources missed within an explicit positive `K`; `K`
cannot exceed the result's retained bound. It reports Hit@K, Recall@K
(`recovered relevant / designated relevant`), and reciprocal rank
(`1 / first relevant rank`, or `0.0`), while same-K summaries report hit rate, mean
Recall@K, and MRR. Cases require at least one distinct address belonging to the
indexed collection. Controlled heterogeneous fixtures confirm clear content
matches, Markdown, configuration, and casefolded queries; they also expose
fixture-local gaps for identifier decomposition, path-only signals, package
proximity, and lexical distractors. These are controlled findings, not a claim
about real-repository retrieval quality or BM25 sufficiency.

A repository-owned operational benchmark can now run that unchanged pipeline
against a bounded, explicitly selected corpus from the checked-out `devtools`
repository. It uses manually designated native resource addresses as case-local
ground truth, retains each ranked result and recovered/missed resources, and
reports same-`K` Hit@K, mean Recall@K, and MRR in a caller-selected JSON report.
Its `.py`, `.md`, `.toml`, `.yaml`, and `.yml` eligibility and exclusions for
Git internals, virtual environments, caches, generated output, historical
dossiers, and benchmark self-input are operational benchmark policy—not
repository classification or relevance semantics. It measures this baseline's
real-repository behavior without rescoring it or adding identifier, path,
package, structural, semantic, hybrid, Context, or model behavior. Its findings
are a small inspectable checkpoint for choosing a later signal, not a broad
retrieval-quality conclusion.

For the bounded Python-function path, a separate purpose-sensitive projection
can nominate discovered addresses ending in the exact, case-sensitive `.py`
suffix for source observation. It consumes only the completed discovery value,
preserves discovery order and original address values, and performs no
filesystem or content access. This address convention is evidence of candidacy,
not proof of Python contents, successful UTF-8 observation, task relevance, or
declaration knowledge. Repository discovery itself remains language-neutral.

Current `context` implementation includes bounded observation of a finite,
explicitly addressed collection of UTF-8 text resources, including an explicit
empty collection. Each required resource is subject to a caller-supplied
positive per-resource byte bound. It establishes nominal
Repository identity, repository-relative resource occurrences,
address-independent decoded-text content identities, and deterministic
identified snapshot state under versioned local semantics. Caller order is
canonicalized by repository-relative address, and duplicate addresses are
rejected. Resources are read sequentially; success claims completeness only for
the exact requested collection and makes no repository-wide or atomic-filesystem
claim. Its local digest and representation choices do not select universal
snapshot or ContentIdentity architecture.

For the exact Python function-name purpose, a bounded pre-analysis selector can
filter a caller-ordered, nonempty set of eligible observed resources by exact
stdlib-tokenizer `NAME` equality over their retained decoded text. It preserves
eligible order and all matching-token observations while selecting each
resource once. A positive candidate is only a purpose-relative prediction that
the resource may deserve declaration analysis; calls, references, and methods
are expected false positives relative to the later direct-declaration scope.
Candidate zero is bounded to the explicitly eligible resources, and tokenizer
failure publishes no successful candidate result. The selector performs no
filesystem acquisition or AST analysis and establishes no declaration
knowledge.

The first bounded derivation consumes one caller-selected resource occurrence
from that observed state and uses stdlib `ast` with explicit Python 3.12
grammar-feature semantics to establish source-grounded knowledge for direct
module-body synchronous and asynchronous function declarations. Other snapshot
resources are not direct semantic dependencies of that derivation. Its
identified definition also records the ambient parser
implementation and runtime version. Successful analysis publishes separately
referable declaration knowledge plus exhaustive coverage of exactly that scope;
syntax failure publishes neither successful coverage nor declaration knowledge.
Subjects are snapshot-local and distinct from their AST nodes, declared names,
and UTF-8-byte-column source occurrences. This local representation does not
select universal subject, source, derivation, coverage, or failure architecture.
A bounded aggregate can apply that existing derivation independently to a
caller-ordered, nonempty set of distinct selected resource addresses. It retains
each per-resource analysis and flattens their existing knowledge in selection
and source order for downstream retrieval. It is not a synthetic derivation or
aggregate coverage claim; selection or parse failure returns no aggregate.
Direct resource containment was already intrinsic to each function declaration:
its occurrence gives the resource and exact span, and its subject binds to the
derivation's observed resource dependency. A production
`PythonFunctionDeclarationContainmentView` now validates an aggregate against
one retained snapshot and navigates resource to direct declarations and
declaration to containing resource. It derives no duplicate ownership fact,
aggregate derivation, relevance judgment, or Context disclosure. The
[function package overview](../src/devtools/context/python/function/docs/overview.md)
defines its bounded contract. Classes, methods, and nested declarations remain
outside this direct module-body function analysis. A separate production
[`context.python.classes` package](../src/devtools/context/python/classes/docs/overview.md)
now establishes direct `Module.body` class declarations and synchronous/async
methods directly in each supported class body. It reuses the existing Python
source occurrence/range and observed-resource dependency values without
changing function declaration identity or exact-name/Reference consumers.
Class and method subjects have distinct structural identities: class ordinal
within the exact resource, and method ordinal within the exact class subject.
Each occurrence belongs to its observed resource; a method's direct lexical
parent is its class declaration. These are different relationships. A class
retains exact direct base-expression syntax and spans. A separate bounded
direct-base derivation assesses every expression and establishes a class-to-class
repository relation only through an unambiguous earlier local class binding,
direct imported member, or explicitly imported module attribute. It reuses
production module/import resolution, retains both class declarations and exact
resource/content dependencies, and leaves unsupported or ambiguous expressions
visible. This is a static repository relation, not runtime inheritance, Method
Resolution Order, subtype closure, or retrieval relevance. Decorators do not
imply descriptor semantics. Bounded coverage
separates supported results from encountered excluded nested syntax and from
module-body functions owned by the existing analyzer. Validated navigation
supports both directions without duplicate containment facts, ranking, or
Context disclosure. A later declaration model may add deeper lexical parents
without treating every declaration as directly resource-contained.

`context.python.imports` separately derives ordered, direct module-body Python
import aliases from one exact observed resource, retaining their source spans,
module text, relative level, imported name, and local alias. Those values are
syntactic declarations only: they do not assert existence, repository membership,
runtime importability, resolution, or a dependency relationship. The adjacent
`context.python.modules` capability interprets an explicit caller-selected set
of observed `.py` resources under one explicit repository-relative module root.
It maps ordinary modules and `__init__.py` package modules to dotted names while
retaining the exact resource, root, role, and snapshot correlation. A repository
address is not Python module identity: content, root, and role matter, duplicate
names remain distinct interpretations, and root precedence is absent. It performs
no root inference, acquisition, namespace-package interpretation, import
resolution, relationship construction, retrieval, or Context work.

`context.python.modules.membership` now derives qualified immediate membership
from existing module interpretations. One child module `P.C` is a member of
exactly one observed package module `P` under the same explicit root and
snapshot. The fact retains both interpreted resources and its derivation;
per-child assessments distinguish missing, non-package, and ambiguous parents
within the supplied selected set. Both directions query this one fact. It
implies no Imports relation, runtime importability, transitive containment, or
relevance. The [package contract](../src/devtools/context/python/modules/docs/overview.md)
defines the bounded API.

`context.python.imports` can additionally resolve a declaration's eligible
module portion only within an explicit `PythonModuleInterpretationUniverse`.
It reports resolved, unresolved-in-universe, ambiguous, or qualified unsupported
outcomes; ambiguity preserves every match and unresolved retains the exact
universe that supports its bounded absence claim. Relative imports consume an
explicit source interpretation, while absolute imports do not. This is neither
runtime import resolution nor generic dependency semantics.

`context.python.project_configuration` separately owns six bounded retained-TOML
selectors: project README, Hatch wheel packages, pytest testpaths, Coverage
source, mypy files and mypy search paths. Declaration analysis uses `tomllib`
and semantic key/item anchors with the exact configuration resource, not
fabricated character spans.
Declaration analysis also retains bounded build/project metadata, named script
and entry-point strings, pytest naming/recursion settings and recognized
tool-table presence. These are static declarations, not effective configuration,
full test discovery or runtime registration. Existing README/testpaths selectors
remain their sole declaration owners. Intrinsic basename, suffix, parent and
prefix membership derive from canonical addresses without parallel RI facts.
Resolution uses canonical repository addresses,
explicit command-cwd/pytest-root assumptions and native module interpretations.
README/Hatch configuration-parent routes remain distinct. Shared exact dotted
name lookup now belongs to `context.python.modules.lookup`; imports migrate to
it without changed behavior. Configuration does not manufacture import syntax.

Positive configuration facts assert only observed exact-resource correlation,
directory-prefix membership or an exact native module target. Many directory
members are multiple facts under one reading, not ambiguity. Competing observed
Coverage path/module readings and module roots remain ambiguous; missing means
only no match in the retained frame. Unsupported forms and invalid/duplicate-key
TOML establish no targets. Source and target occurrence/content, snapshot,
repository, universe and assumptions are validated dependencies. No tool
execution, directory existence, packaging outcome, runtime binding or general
entrypoint machinery is established. See the
[package contract and ownership diagram](../src/devtools/context/python/project_configuration/docs/overview.md).
Future Retrieval consumption needs a separate explicit selector/relation,
direction, applicability and aggregation decision retaining native fact support;
current ranking, projections and Context policy are unchanged. This static RI
does not promote B-0019 framework runtime configuration ownership.

The adjacent `context.python.imports.relations` operation derives one directed
`PythonResolvedModuleImportRelation` for each supplied `RESOLVED` declaration
resolution when exactly one matching source module interpretation is available.
Each relation connects that exact source interpretation to the exact resolved
target interpretation and retains its declaration/resolution evidence. The
explicit interpretation universe bounds resolution; unresolved-in-universe,
ambiguous, unsupported, or source-unavailable outcomes do not produce a
relation, while repeated declarations remain distinct evidence. These are
deterministic, source- and declaration-grounded Repository Intelligence
relations; they do not establish runtime import execution, runtime dependency,
undirected adjacency, retrieval relevance, or ranking. No retrieval integration
or Context behavior is implemented.

`context.python.imports.members` provides a separate bounded imported-member
binding resolution capability. For one direct module-body `ImportFrom` member
occurrence, it accepts exactly one eligible direct facade binding, resolves that
facade's target module uniquely within the explicit interpretation universe,
and accepts exactly one existing direct module-body `FunctionDef` or
`AsyncFunctionDef` declaration. It retains resolved,
unresolved-in-universe, ambiguous, and unsupported outcomes with provenance
through the source occurrence, facade binding, target-module resolution, and
target declaration; where projected as resources, the result is source
resource to defining resource. This remains distinct from the module-only
import relation above and establishes only qualified static Repository
Intelligence: not runtime import behavior, public/exported API or `__all__`
semantics, general Python reference resolution, later local-name use,
recursive facade traversal, other target kinds, or retrieval relevance.

`context.python.references` derives bounded source-grounded References to
supported direct module functions, classes, and direct class methods from
same-module, named-import, module-qualified, and statically class-qualified
expressions. A positive result retains the exact source occurrence, structural
target declaration and resource, resolution route, import/module support where
applicable, snapshot, and derivation identity. A direct Call is the same
Reference when the resolved expression occupies `ast.Call.func`; it does not
establish runtime invocation or dispatch. Ambiguous, shadowed, dynamic, and
unsupported bindings produce inspectable assessments without positive facts;
coverage is non-exhaustive. Direct module declaration lookup is owned by module
interpretation and shared with class-base resolution. The
[package contract](../src/devtools/context/python/references/docs/overview.md)
defines the bounded API. Retrieval graph ranking and Context disclosure remain
independent consumer decisions.

The first bounded retrieval operation consumes supplied declaration knowledge
and filters it by exact declared-name equality. Its nonempty name query is the
purpose representation, and each match carries purpose-relative exact-match
RelevanceEvidence referencing the original knowledge. Input order is preserved;
zero matches succeed only over the supplied knowledge. The operation performs no
repository access or parsing and introduces no score, ranking, or Context
selection semantics.

A bounded resource-selection projection can consume that retrieval result and
identify the distinct snapshot-relative resource addresses supporting its
matches. It preserves first-match order and every original declaration-level
match as support when several matches occur in one resource. This projection
performs no retrieval, analysis, or source access and makes no claim that an
unselected resource is irrelevant or that a selected resource is useful beyond
the exact-name purpose.

The first bounded Context operation consumes that successful retrieval result,
selects every exact-name match in retrieval order, and realizes a structured
knowledge projection for each selection. Each item retains its retrieval
evidence and exposes only the established declared name, declaration kind,
proposition, and snapshot-local source occurrence. The retrieval result does not
carry resource content, so the structured disclosure itself does not include
source text or reacquire it. A bounded materializer can separately accept the
identified RepositorySnapshot, validate each occurrence's snapshot identity,
resolve its exact observed resource by repository-relative address, and extract
its exact source segment using the established one-based line and UTF-8-byte-column
coordinates. It preserves observed newline
bytes after UTF-8 decoding and performs no filesystem access or parsing.
A bounded renderer then produces deterministic human-readable Context text from
the materialized values, preserving selection order, duplicates, source
metadata, and each unchanged exact source segment. It retains correlation to
the materialized Context and performs no upstream work or model-specific request
construction. Successful retrieval zero becomes a successful zero-item
disclosure, materialization, and rendering. These local Context artifacts are
not a generic DisclosurePlan/compiler, ranking result, or prompt protocol. A
bounded assembly operation can accept an existing caller-owned `ModelRequest`
whose `Prompt` contains the primary task, preserve its role and all other request
semantics, and construct a new `ModelRequest` whose prompt visibly places the
unchanged rendered Context after the unchanged task. It does not mutate
Conversation, invoke ModelInteraction, or retain Context provenance in the
request. General model-input assembly remains unimplemented.

A sibling bounded Context path accepts an explicit purpose and one
caller-chosen qualified Python Reference/direct Call fact from its production
analysis. It validates fact membership, source and target dependencies, and
qualified resolution support against an identified RepositorySnapshot. It
extracts the exact Reference Name occurrence and resolved direct function
declaration span from retained snapshot content, renders the relationship
separately from both source segments with locations and navigation pointers,
and can place the result beside an unchanged task in a copied ModelRequest.
The Call tag describes syntax at ast.Call.func, not execution; Reference
coverage remains non-exhaustive. No fact is chosen automatically, and invalid
dependencies fail without whole-file fallback or filesystem reacquisition.

The first common Context Planning foundation now records a caller-directed,
immutable DisclosurePlan under one purpose and RepositorySnapshot identity.
It can hold multiple ordered concrete disclosure choices. One adapter
realizes the existing qualified Reference path; another explicitly discloses
one whole retained resource. Materialization rechecks applicability, retains
native provenance and content identities in ContextDisclosure items, and
fails on missing or stale state. Rendering and ModelRequest assembly happen
after realization. This is a production plan/materialization boundary, not
an automatic planner, resource Selector, sufficiency judgment, or retrieval
operation. A later plan may identify a preceding plan, without claiming
agent recovery or prior model comprehension. The
[Context Planning package](../src/devtools/context/planning/docs/overview.md)
describes the implemented API and limits.

Filesystem Resources remain access mechanisms, not Repository identity. Python
analysis beyond the bounded implemented scopes, automatic Context planning,
progressive disclosure, and durable Context storage remain future
responsibilities; Runtime remains narrow and model requests remain
non-authoritative.

These concepts describe reusable semantic relationships, not a mandatory
runtime pipeline. ResourceOccurrence, SourceOccurrence, and RepositorySubject
are distinct referential domains; graph views are first-class reusable typed
projections over relationship knowledge rather than a mandatory stage; and
directly addressed information can be
acquired without relevance discovery. Retrieval strategies may independently
query different intelligence views. Repository-relative derivation can establish
new DerivedKnowledge, while purpose-relative Context synthesis can establish
provenance-bearing information without automatically becoming repository
intelligence. Progressive disclosure can justify another information purpose/
acquisition episode. A request need not traverse every concept or view.

## Accepted retrieval and ranking semantics

### Current retrieval-foundation checkpoint

The [retrieval foundation](architecture/retrieval.md) owns the detailed current
inventory, empirical evidence, demonstrated limitations and open retrieval
hypotheses. Production is more than BM25 plus graph: whole-resource content
BM25 plus independent filename-stem BM25, exact symbolic acquisition/grounding,
direct typed structural candidates, PPR, repository-map ranking, optional RRF,
and Localization task/obligation lexical lanes, role routing and bounded
structural witness generation all exist. They are separate callable surfaces,
not one automatic pipeline or a default fusion policy. Production has no dense,
learned sparse, learned ranking/reranking or BM25F implementation.

Canonical Unicode-word/casefold terms do not split code identifiers. Independent
`content BM25 + 0.25 × filename-stem BM25` is **not BM25F**. Lower-level
representation, fielding, query formulation, semantic mismatch handling,
ranking/discrimination and candidate selection remain materially underexplored.
Fixed-window and CodeRankEmbed results did not settle semantic granularity or
disprove embeddings. Negative graph evidence does not negate direct structural
value. The [failure taxonomy](architecture/taxonomy.md#retrieval-and-localization-failure-classes)
separates these surfaces from obligation formulation and Context disclosure.

The [coordinated roadmap](roadmap.md#current-sequencing) mandates R1 additive
identifier/subtoken representation, diagnostic/sensitivity checkpoints R1.5–R1.7,
then **R2 true BM25F regardless of R1's
outcome**, with representation and fielding separately attributable. No production
algorithm or accepted Localization semantics change in this checkpoint.

[Case 0009 Stage D](../experiments/codex_dogfood/case_0009/analysis.md) now
prospectively evaluates R1 against clean independent gold and selects **RETAIN
AS SEPARATE RETRIEVAL VIEW**. REQUIRED positive reach is unchanged; mixed ranking
gains/regressions fail the frozen promotion gates. Canonical production BM25
remains unchanged. [R1.5 experimental diagnostics](../experiments/retrieval_diagnostics/README.md)
now validates mechanical score/failure evidence with optional independent gold,
without a production dependency. R1.6's
[Case 0010 Stage D](../experiments/codex_dogfood/case_0010/analysis.md) is complete:
**MIXED / NO SAFE REPLACEMENT**. Required reach is complete, but no selected
parameter configuration passes the frozen improvement and obligation-safety gates.
Production remains (1.2, 0.75, 0.25). U1 manual information-need decomposition
is now the next upstream experiment under the [roadmap](roadmap.md): task,
obligation, information need, query/acquisition intent and retrieval action are
distinct. U2 exact-hint routing and U3 need/mechanism routing remain future.
R1.7 is retained after upstream evidence; R2 BM25F remains mandatory
after R1.7. Localization's reasoning continuation is unchanged.

### Accepted boundaries and implemented composition

[ADR-0003](architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
accepts InformationNeed as purpose-relative desired-information semantics,
bounded retrieval planning/applications,
ContextCandidate, provenance-bearing RelevanceEvidence, and ranking semantics.
ContextCandidate addresses a repository-intelligence referent—such as a
RepositorySubject, ResourceOccurrence, SourceOccurrence, DerivedKnowledge, or
relationship knowledge—not RepositorySubject alone; representation remains a
later disclosure concern.
RelevanceEvidence preserves typed, provenance-bearing purpose-relative
retrieval observations and retriever-native measurements without requiring a
standalone artifact or repository DerivedKnowledge status. It preserves
retrieval as multi-strategy evidence discovery; ranking as evidence
interpretation; and Context selection/compilation as a later, distinct concern.
When scarce capacity requires an admission decision, the purpose represented by
or referenced from InformationNeed must be available to that decision; query
text alone is insufficient. Admission may explicitly abstain and need not be a
score or total ordering. It remains a purpose-relative decision over surfaced
evidence, not proof of usefulness, and can stay operation-local or within
Context planning. This accepted distinction does not create a universal
Candidate/CandidateEvidence, first-class Selector, Selection domain, or
production relationship-expansion policy.
It also preserves concurrent dependency-aware retrieval, staged expansion,
progressive disclosure, and future evaluation pressure without assigning them
to Runtime, Tool execution, authorization, or an Agent loop.

The current direct Python structural retrieval operation consumes established
Imports, bounded References with direct Call tags, and qualified immediate
package membership from Repository Intelligence. It projects one relation from
explicit snapshot resource seeds under a purpose-bearing request and retains
each native fact, seed, and direction as support for the surfaced resource.
It does not parse source, create repository relationship truth, traverse further,
score candidates, or disclose Context. Repository Intelligence owns deterministic
facts; Retrieval owns purpose-relative candidate evidence; Context decides
which supported facts, occurrences, spans, pointers, or whole resources to
disclose for a purpose. Resource admission may later be a bounded
purpose-specific decision, but no universal resource-Selection stage is
mandatory between Retrieval and Context. A candidate or resource orientation
does not require disclosure, whole-resource presentation, closed-set membership,
or a sufficiency claim. The
[retrieval package overview](../src/devtools/context/retrieval/docs/overview.md)
defines the implemented API and bounds. A separate snapshot-bound composition
operation now correlates native lexical and direct structural evidence for the
same observed resource under a caller-supplied purpose. It validates the entire
lexical corpus against that snapshot, including content identity for unreturned
documents that can affect BM25 statistics; it requires the structural result's
snapshot and purpose to match. The lexical query remains mechanism input, not
an InformationNeed identity. The result retains both original mechanism results
and iterates candidate resources by canonical address, with no cross-mechanism
rank or budgeted file selection. Purpose-relative resource assessment and
sufficiency remain distinct possible decisions; their owners and concrete
policies are unresolved. An explicit caller-chosen RI fact can enter bounded
Context disclosure without either decision.

The first controlled Codex dogfood uses these production results from a
research-owned capture, with the full task prompt and a separately frozen short
InformationNeed as comparable lexical arms. It hands over a complete, neutral
address-oriented evidence list as advisory orientation. Codex retains normal
repository search, open, edit, and validation access; no production Selection
policy or Context disclosure compiler is introduced. Agent actions are recorded
separately from later required-resource adjudication. The current read-only
`CodexAgent` adapter returns final text and continuation but does not retain
exhaustive tool activity, so dogfood observations require an explicit external
recording source. The [roadmap](roadmap.md) defines the controlled protocol.

Increment 23 independently validates this boundary but does not promote its
directional-reservation-v1 realization. Canonical and practical top five each
recover 10/18 known-useful resources; the rule exchanges one useful rank-five
resource for one useful relationship resource and also makes one not-useful
admission. Lexical top fifteen contains all 18 known-useful material resources,
while relationships contribute only one useful resource beyond top five. The
rule is not ready for shadow or production. At that checkpoint, this evidence
preserved purpose-relative decision semantics and the heterogeneous portfolio
while directing subsequent experiments toward bounded candidate generation and
ranking. Production remains content BM25 plus `0.25 *` filename-stem BM25 and
retains up to the caller-supplied positive `maximum_results`. The `K=5` results
above use the experiment's fixed evaluation bound.

Increment 24's offline comparison over the same retained six-case surface did
not improve this result: its purpose-relative deterministic ordering recovered
9 known-useful resources versus 10 for the lexical/native baseline. This is
repository-local evidence only; it does not promote a ranker, alter production,
or close the cross-repository evaluation requirement.

The accepted long-term direction is a heterogeneous, non-mandatory portfolio:
Repository Intelligence can supply lexical, typed structural/relational,
semantic/representation-based, change/history, and other future evidence;
bounded discovery can then be interpreted for an InformationNeed under scarce
capacity before Context disclosure. Exact addressed resolution remains a
separate path when discovery is unnecessary. Native evidence retains its own
meaning: a future pretrained semantic representation is not a trained ranking
model, and either differs from repository truth and from later disclosure.
No evidence family, physical graph representation, ranker, learned capability,
or shadow execution is selected by this statement. Devtools-only observations
cannot establish lexical sufficiency, relationship failure, or a general
ranking policy; independent-repository evidence remains required.

Increment 25 subsequently found bounded imported-member structural
candidate-generation complementarity on `devtools`. Increment 26 development
found useful semantic-only top-five resources, but each had a deeper positive
lexical rank; its sealed confirmation is suspended. These observations do not
change the accepted repository-truth, evidence, ranking, and disclosure
boundaries. The [roadmap](roadmap.md) records the current retrieval-foundations
sequence as it stood at that checkpoint. No graph, vector, ranking, or shadow
infrastructure was selected by those results.

The subsequent Tier-1 breadth sprint is complete. Its
[development evidence and production gate](research/repository-retrieval-breadth-production-gate.md)
show useful resource reach from direct Imports and bounded References/direct
Calls, while greater graph depth has large fan-out and only sparse sampled
usefulness. The heterogeneous pool contains more known-useful resources than
the executable K=5 rankings select. This supports qualified direct structural
facts and keeps structural admission under a fixed budget an open retrieval
question. Canonical BM25 remains the implemented production retrieval baseline;
the stronger development lexical RRF control, dense comparison, unions, and
simple fusion are not production defaults. No universal graph or graph store is
selected.

Graph-1/Graph-2 tested unranked structural neighborhood traversal for resource
candidate generation. Sparse useful novelty in judged samples and sharp fan-out
reject that mechanism as a strong default. Task-conditioned graph ranking and
graph-assisted Context compilation were not tested by those traversals.

Production Retrieval now has a separate, query-conditioned structural-ranking
baseline. It projects qualified forward Imports and References/direct Calls
from production RI onto snapshot resource nodes, retaining fact and occurrence
provenance. Package membership and reverse edges do not propagate by default.
Each distinct fact has equal initial edge weight; outgoing transitions are
normalized. Positive BM25 ranks seed a personalized PageRank walk with 0.85
damping, personalized dangling redistribution, deterministic convergence, and
native ranked structural evidence. Optional equal-channel RRF fuses BM25 and
PPR ranks without combining their raw scores or erasing either native result.
The view belongs to Retrieval, not a universal repository graph or durable RI
fact store. The [graph package documentation](../src/devtools/context/retrieval/graph/docs/overview.md)
defines the exact contract. It does not choose Context disclosure.

The [development replay](../experiments/graph_ranking_baseline/README.md) on
one frozen production-RI dogfood snapshot found that PPR and equal RRF worsened
complete required-resource depth relative to BM25. Seven of ten required
resources were isolated in the forward projection. This keeps the graph as
optional retrieval evidence and withholds any automatic ranking/disclosure
policy. The result is case-local and does not close the broader graph-ranking
hypothesis or authorize tuning on the same labels.

The subsequent typed Retrieval graph view projects production Repository
Intelligence onto observed resources and supported function, class, and method
declarations. Containment in both navigational directions, forward Imports
and References, and resolved direct bases form its core; an optional navigation
view also projects qualified immediate package membership and weak mirrored
source/test path correspondence. Retrieval owns these transition directions
and balanced outgoing-family normalization. RI still owns the exact underlying
facts. The same Personalized PageRank kernel ranks every view, lexical mass
enters only resource nodes, and the maximum node mass in a resource becomes
its structural resource score. This neither selects nor discloses Context.
The [typed-view development replay](../experiments/typed_graph_baseline/README.md)
restored same-resource declaration topology but worsened complete required
depth against BM25 on the retained development case. This does not establish a
default graph ranking policy. Documentation/governance and configuration
resources remain without supported structural relations in this graph.

The bounded source-grounded Python function Reference occurrence
with direct Call specialization is now production RI with explicit uncertainty
and coverage; no runtime dispatch or generic call graph is implied. Immediate
qualified package membership is another production typed fact. Exact observed
Python mirrored source/test path correspondence is now a separate production RI
fact with source and test-side roles, snapshot-bound resource/content support,
and bounded coverage. It asserts path convention, not TESTS, COVERS, VALIDATES,
EXERCISES, execution, or behavioral dependency. Its weak historical incremental
retrieval reach is independent of whether the path fact is deterministic. The
direct structural retriever and Context Planning do not consume this fact
automatically. The optional typed navigation graph projects it as a weak,
explicitly labeled path correspondence; the typed core view omits it. The
[Python RI overview](../src/devtools/context/python/docs/overview.md) defines its
contract.

## Accepted repository Localization semantics

The [Localization continuity view](architecture/localization.md) owns the single
current capability-status matrix, Cases 0004–0008 history, structural-breadth
closure and downstream resumption point. Package contracts retain API detail;
the roadmap retains sequencing. Accepted future frontier, acquisition and
Context handoff concepts must not be read as implemented behavior.

[ADR-0005](architecture/decisions/ADR-0005-obligation-driven-repository-localization.md)
accepts **Localization** between native Retrieval evidence and Context Planning.
The semantic kernel is implemented in
[`devtools.context.localization`](../src/devtools/context/localization/docs/overview.md):
it represents caller-authored obligations and shared task anchors, alternative
conjunctive witness sets, snapshot-qualified assessments, and deterministic
frame readiness. A bounded one-way lexical adapter also executes the full-task
BM25 safety lane and caller-authored obligation queries while retaining native
ranked results. Automatic task interpretation, autonomous acquisition planning/execution,
and Context integration remain unimplemented; bounded nonlexical candidate
generation is implemented as described below. Localization readiness is scoped to
the supplied obligation frame; it does not establish that the frame is exhaustive
or that the task will succeed.

The [Localization role-evidence package](../src/devtools/context/localization/roles/docs/overview.md)
now derives query-independent, multi-label positive supports from canonical
resource addresses and explicitly supplied native RI analyses. It retains
convention, structural, declaration/table and bounded target-match bases via
distinct support kinds and native references. The immutable view retains the
whole observed frame; missing support is not negative evidence. Configuration
matching is bounded and does not emulate tool execution or pytest collection.
RI and core Retrieval do not depend on this package. The optional Localization
router takes caller-authored per-query preferred roles and projects existing
obligation BM25 lanes into positive-support and complete escape tiers. It retains
the native full-task lane, every candidate, native rank and support explanation.
Routing changes attention order only; no score, filtering, elimination or
obligation judgment is produced. The Localization association package additionally
validates caller-supplied, unresolved candidate witness hypotheses against the
task and snapshot. Each member retains an observed resource, explicit reason and
native lexical, role or routing support. Several members may complement one
another and hypotheses may compete, without becoming accepted witness sets or
changing readiness. This slice supplies no automatic generation or resolution
policy.
Localization also accepts caller-authored exact anchor-grounding requests.
Its bounded resolvers consume snapshot resource and Python RI identities,
retaining ambiguous, unresolved and unsupported outcomes. Grounding does not
infer an obligation witness or produce repository truth.
The bounded Localization generator consumes explicit caller recipes and exact
owner, observed mirror, Reference or direct import dependency RI relations. It
retains native structural provenance, attaches matching lexical/role/routing evidence, and
constructs unresolved candidate hypotheses through the association validator.
Ambiguous or missing projection members abstain without partial acceptance.
No graph expansion, score, witness resolution or candidate elimination occurs
inside generation. The stable relation set also includes bounded exact Reference
and one-hop direct import dependency projections; neither establishes satisfaction.

The language-neutral [resolution kernel](../src/devtools/context/localization/docs/overview.md#explicit-evidence-to-witness-resolution)
now records explicit caller decisions over validated associated candidates from
any acquisition channel. Native support lineage and the obligation criterion
remain exact. Partial immutable views distinguish missing records, unresolved
judgments, abstention and explicit contradiction. Contradiction retains candidates;
all complementary members must be supported before explicit promotion produces
existing WitnessSet/SupportedWitness values. Assessment and readiness remain
downstream caller operations. No automatic policy, elimination, frontier requests
or Context Planning integration is implemented.

```text
task interpretation: shared anchors + obligations + constraints
                        |
RI + full-task/scoped Retrieval evidence
                        |
                        v
Localization: witnesses, alternatives, applicability, readiness
                        |
                        v
FUTURE obligation handoff -> Context Planning: representation + capacity
                        |
                        v
materialization / assembly -> Agent
```

The implemented Context plans/materializers are caller-directed. A reusable
unresolved frontier, bounded acquisition requests, iterative reacquisition and
the automatic obligation-to-Context handoff are future work; generation-local
incomplete-enumeration diagnostics are not that frontier. Localization may
describe missing evidence under the accepted direction; Agent/orchestration
owns whether/how/when to acquire, retry or stop. No end-to-end sufficiency or
autonomous coding-agent effectiveness is established.

InformationNeed remains purpose-relative desired-information semantics; queries
remain acquisition inputs. Localization does not require a generic TaskModel,
parallel evidence ontology, universal FileRole or scalar confidence. Obligations
have task-local identity, source provenance, subject anchors, required/helpful
status, applicability conditions and bounded satisfaction criteria. Assessments
record resolution states. Candidates compete within a unique-owner criterion
and complement across obligations; acceptable alternatives can contain several
native referents. Validation-location obligations do not execute validation.

Full-task BM25 remains a global safety lane alongside obligation-scoped queries
and soft role routing. Repository Intelligence (RI) owns facts and bounded
coverage; path conventions are hints, not exclusions. Low score, absent support
and graph disconnection never justify elimination. Hard elimination requires an
obligation-scoped proof with exact referent, rule, snapshot/frame and adequate
coverage. Existing Personalized PageRank (PPR), repository-map ranking and
Reciprocal Rank Fusion (RRF) remain available; targeted relationship navigation
remains available as bounded candidate evidence. Aggregate prospective evidence
has closed the current relation-breadth phase, without establishing retrieval
adequacy. Structural acquisition alone is insufficient. Retrieval/Search acquires
candidate evidence; Localization defines obligation-relative needs and candidate
witness semantics; semantic resolution judges task-relative member/witness claims.
Semantic resolution must not compensate for avoidable representation, fielding
or query defects; stronger retrieval cannot establish semantic witness sufficiency.
The experimental external decision adapter retains the resolution direction.
Prospective semantic-resolution effectiveness evaluation is paused until R1 and
R2 progress, unless a concrete reason justifies an earlier parallel experiment
under the roadmap. No automatic production resolution policy is added.

A complete handoff requires supported satisfaction of every applicable mandatory
obligation within the stated frame. Named inherent discovery allows an explicitly
conditional handoff; abstention or budget exhaustion leaves coverage incomplete.
The current adapter executes only the bounded BM25 lanes and retains native
results; it does not assess satisfaction. An authorized Agent/caller owns any
further acquisition, retries, and escalation. Context chooses faithful
representations and will preserve obligation provenance without redefining
satisfaction or repository truth. Localization is not an autonomous subsystem.

## Accepted Context and disclosure semantics

The [heterogeneous evidence admission and recovery investigation](research/heterogeneous-context-admission-and-recovery.md)
and ADR-0004's 2026-10-02 refinement selected an **unimplemented** direction:
evidence-guided option admission inside Context Planning, with a
separate observable decision/coverage account alongside the selected plan.
Native resource, declaration, occurrence and relationship identities remain
referents; concrete representations consume disclosure capacity. There is no
mandatory intermediate file-admission service or universal evidence score.

ADR-0005 now separates obligation resolution from representation admission. The
earlier question-lane score floors/capacity weights remain historical development
research, not the next implementation policy. Context retains concrete option
choice, exact materialization, representation-relative coverage and capacity;
Localization supplies obligation witnesses and unresolved requirements.

Bounded planning assessments distinguish integrity, applicability, cost,
currently available requested representations and open questions. They do not
establish general Context sufficiency. Requests may acquire information for a
question or expand an exact target; obligation acquisition is interpreted by
Localization and exact representation expansion by Context. Context
plans/materializes, while
Agent/orchestration decides successive attempts, validation, recovery limits
and escalation. Previous plan lineage does not establish current availability.
This accepts request semantics, not a transport, Tool registry or recovery loop.

[ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
accepts the post-ranking Context layer. Context compilation is conditional
information composition, not top-K retrieval or automatic budget filling.
Disclosure planning couples candidate and representation choice and reasons
about coverage, marginal contribution, complementarity, representation-relative
overlap, prior currently available information, applicability, sufficiency,
authority, and multidimensional cost. It selects information rather than prompt
strings. A DisclosureOption is a future purpose-relative possibility for
exposing information through a selected representation or transformation, with
origin, form, fidelity, cost, and provenance kept semantically distinct.
Source-preserving material, existing knowledge projections, and synthesized
semantic assertions are distinct origins. A new
repository-relative assertion can be ADR-0002 DerivedKnowledge; a purpose-
relative Context synthesis remains explicit and provenance-bearing without
automatic promotion to repository intelligence. Composite provenance-preserving
representations are permitted.

DisclosurePlan, ContextDisclosure, and ModelRequest remain distinct:

```text
InformationNeed -> DisclosurePlan -> materialization -> ContextDisclosure
    -> model-input assembly -> ModelRequest
```

The Plan is an immutable selected-information decision; the Disclosure is an
immutable realized information artifact under/reference to that plan; the
ModelRequest is a consumer-specific presentation. Materialization faithfully
realizes the selected representation and may perform an explicitly planned
semantic transformation or lossy synthesis. It cannot silently re-plan, invent
a materially different synthesis, or present inapplicable information as
current. Assembly arranges already-realized disclosure and must not introduce
new semantic assertions through formatting, placement, or budget handling.
Planning and possession of a disclosure are not disclosure/presentation
authority.

The implemented DisclosurePlan is intentionally narrower than this accepted
general concept: a caller chooses its purpose and concrete options. Supported
forms are a qualified Python Reference fact with exact source and target
declaration, and an explicit whole observed resource. The plan is bound to
one snapshot, preserves ordered choices and optional preceding-plan lineage,
and materializes to a ContextDisclosure with native provenance. Retrieval
rank may inform a caller but does not automatically choose a representation,
disclosure quantity, or claim of sufficiency. ADR-0004 continues to govern
future planning, cost, and disclosure semantics. The
[Context Planning and graph-assisted retrieval research](research/repository-context-planning-and-graph-assisted-retrieval.md)
motivates this boundary and a separate query-conditioned structural-ranking
baseline; its automatic planner, graph weighting, and fusion recommendations
are not implemented here.

Every disclosure stage preserves semantic strength: representation selection,
projection, synthesis, compression, materialization, disclosure realization,
and assembly must not turn a possible result into a definite one, a partial set
into an exhaustive set, an approximation into an exact assertion, or a
preserved disagreement into one truth unless an identified semantically capable
process establishes the stronger conclusion. Source semantics, support,
assumptions/scope, conflict state, and semantic-result coverage bound what may
be represented.

This architecture distinguishes repository history, disclosure history, and
Conversation history. Current Conversation ownership remains
`agents.conversation`; the sparse `context` namespace does not own a current
compiler or former Session semantics. Model-input assembly is a separate future
concern: it determines how a selected disclosure is realized for a model, while
disclosure planning determines what information should be available. Context
budgets are ceilings rather than targets, and repeated acquisition remains above
deterministic retrieval/compilation rather than inside Runtime.

Coherence concerns intelligible meaningful units and consumer reconstruction
burden, not source contiguity. Authority is claim-/purpose-relative evidence,
not a universal source hierarchy; relevant applicable conflicts remain
preservable rather than being silently arbitrated. Concrete coverage, fidelity,
authority, uncertainty, completeness, conflict, coherence, semantic-
transformation/synthesis validation, materialization, cache, assembly, and
evaluation mechanisms remain unimplemented.

The breadth gate makes the broader Context problem concrete: use established
facts and source spans to choose supported representations for a purpose.
The first cross-resource slice accepts a caller-chosen qualified Reference fact
and faithfully discloses its exact occurrence and target declaration. Future
planning may choose among facts, spans, pointers, and whole resources under
applicable constraints. Later or refined InformationNeeds may cause further
retrieval and disclosure, but this slice does not establish a recovery
guarantee or progressive controller. Lexical windows and structural supports are
possible localization inputs, not demonstrated disclosure policies or
permission to synthesize stronger claims than their provenance supports.

## Accepted Evaluation responsibility

Evaluation is a distinct semantic responsibility for assessment and controlled
comparison. It correlates layer-owned artifacts and factual Evidence without
owning RepositorySnapshot, DerivedKnowledge, retrieval observations, Context
artifacts, ModelRequest/ModelResponse, Tool execution, Runtime lifecycle, or
generic Trace. Distributed ownership plus explicit correlation is preferred to
one cross-domain experiment object.

At the granularity required by a particular evaluation, the evaluation meaning
must make referenceable the assessment/comparison basis, intended condition or
intervention and relevant fixed factors, realized execution, applied evaluator/
oracle/criterion, heterogeneous observations or outcomes, and any later
comparison or inference. These are semantic distinctions, not mandatory
classes, globally identified artifacts, persistent lifecycles, or a universal
runtime pipeline. A fixture or scoped configuration can be sufficient for a
bounded evaluation. Repeated realizations remain distinguishable when the
claim depends on them, but an execution Attempt does not automatically become
an evaluation realization.

Evaluation outcomes retain their native meanings: correctness judgments,
coverage, sets, categorical results, durations, token or call counts, costs,
human assessments, and other observations do not collapse into a foundational
scalar score. Policy-specific aggregation, Pareto comparison, or cost-
effectiveness analysis may be layered later. Trace/observability can explain
what occurred and its execution order; it does not establish intended
intervention, controlled factors, oracle meaning, or comparison validity.

Historical evaluation evidence remains truth about an assessment performed
under identified conditions. Whether it predicts or transfers to current
conditions is a later evaluation inference, not ADR-0002 DerivedKnowledge
applicability. An evaluator can judge DerivedKnowledge without that judgment
becoming repository intelligence. Evaluator-private answers, tests, labels,
solutions, or treatment assignments must not become model-visible unless
disclosure is deliberate and authorized; host-side oracle use that changes an
adaptive interaction remains intervention/provenance even when the oracle is
not directly disclosed.

No universal `EvaluationCase`, `Treatment`, `EvaluationRun`,
`EvaluationEpisode`, scalar quality model, causal DAG, trajectory ontology,
oracle abstraction, metric system, trace platform, statistics subsystem, or
evaluation store is accepted. RepositorySnapshot also does not identify the
whole evaluated intelligence condition: knowledge/view availability,
derivation or analyzer semantics, coverage, external semantic state, and reuse
state can differ. Experiments retain the actual relevant basis without creating
a universal `RepositoryIntelligenceSnapshot`, `KnowledgeClosure`, or
`IntelligenceClosure`.

Experimental causation is study-relative and is not either ADR-0002 graph
family. Derivation dependencies explain semantic support/applicability, and
repository graph views express repository relationships; neither makes a claim
such as “graph retrieval improved task outcome” repository graph knowledge.
Such a claim remains an evaluation hypothesis or inference supported by the
particular design, correlations, observations, and analysis.

Counterfactual claims remain bounded. A fixed candidate/evidence set can support
a local ranker comparison, a fixed disclosure can support an assembly
comparison, and an exact request can support repeated model realizations. When
an earlier adaptive decision changes, recorded downstream purposes, retrieval,
or model actions are not automatically a valid counterfactual continuation;
the affected continuation may require a rerun. Progressive evaluation can
retain experiment-local decision correlation without a foundational Episode or
Trajectory model.

The completed retrieval breadth work justifies a small production Evaluation
kernel for expected-versus-observed identity coverage. It reports duplicate
identities on each side, missing expected identities, and unexpected observed
identities while preserving input order. Evaluation owns comparison and
assessment validity at this boundary; callers own identity meaning and decide
whether a non-exact report is fatal. Coverage concerns identity presence only:
an observed `UNJUDGED` outcome is observed, while an identity left unsampled is
missing if it remains in the expected frame. Evaluation does not own outcome,
relevance/usefulness, rationale, or sampling semantics, metrics, artifact
freezing, or experiment protocols. The primitive is designed to support future
assessment domains without interpreting their outcomes. No generic Population,
metric interface, universal experiment object, or Learning package is
established. See the [Evaluation package documentation](../src/devtools/evaluation/docs/overview.md)
and [breadth gate](research/repository-retrieval-breadth-production-gate.md).

## Implementation-start and remaining evidence constraints

The focused external-semantic-state investigation has been reconciled within
ADR-0002. Repository derivations may consume an open set of external semantic
inputs, including configuration, language/toolchain semantics, dependency or
resolution state, generated inputs, platform semantics, environment values, and
external resources. If such state can change derivation meaning or results, it
must not remain an invisible ambient dependency: definition, dependency,
assumption/scope, observation, applicability, and provenance semantics account
for it according to its role. A value, reference, constraint, existing identity,
inline observation, or other adequate representation may suffice; semantic
importance does not automatically require independent identity or persistence.

The semantic thing, its state/value, and its observation are distinct.
Observation must not claim stronger identity, consistency, completeness,
equivalence, or other guarantees than its mechanism establishes. Identity,
value equality, semantic equivalence, compatibility, and applicability likewise
remain distinct, and dependency satisfaction uses the domain- and derivation-
appropriate relation rather than universal identity equality. No foundational
universal `WorkspaceSnapshot`, `EnvironmentSnapshot`, external-state ontology,
observation artifact, equivalence framework, or applicability algorithm is
accepted. One RepositorySnapshot can support multiple configuration/toolchain/
platform interpretations. Committed generated files can be snapshot resources,
while other generated material can be derivation-produced or use a future
analysis-resource model without expanding repository-state identity.

Provenance inspection, semantic replay/reconstruction, and operational replay
have different retention requirements. Semantic identity neither requires a
retained executable artifact nor proves that a historical environment can be
recreated. External dependencies and their observations also bound negative or
exhaustive knowledge; coverage cannot exceed the closure actually established
by dependencies, scope, assumptions, and observation semantics. Concrete
external-state representation, observation, equivalence/compatibility,
generated-resource, enforcement, retention, and replay mechanisms remain
implementation design.

The focused evaluation-architecture and causal-attribution investigation has
completed its substantive analysis, and its accepted findings are reconciled
above. The research dossier's producing process did not complete its final
mechanical artifact-integrity verification; the later architectural review and
this reconciliation therefore treat it as research evidence rather than as a
verified decision artifact.

Existing boundaries require future evaluation to distinguish, where meaningful,
repository observation correctness;
repository-intelligence semantic correctness and derivation-family-specific
soundness, precision, or coverage; incremental-maintenance correctness and
dependency-granularity economics; graph, retrieval, RelevanceEvidence, and
ranking contribution; disclosure selection, representation, coherence,
redundancy, complementarity, synthesis fidelity, and semantic-strength
preservation; model-input presentation effects; resource efficiency; and
end-to-end coding-agent outcomes. Layer-local correctness or quality is not
equivalent to task success, and task success alone does not identify which
layer caused success or failure. Controlled comparison and causal or marginal
contribution assessment should remain possible where practical without
requiring a universal score or a score from every component. Metrics, datasets,
benchmarks, formulas, storage, and APIs remain open. Relevant attribution can
include the marginal or unique contribution of retrievers, graph views, ranking
mechanisms, Context representations, synthesis, and finer incremental-
maintenance precision.

Replay, debugging, and evaluation may therefore need sufficient correlation
among relevant RepositorySnapshot, derivation semantics, semantic dependencies,
DerivedKnowledge, retrieval purpose/planning/applications, candidates and
RelevanceEvidence, ranking, DisclosurePlan, ContextDisclosure, model-input
assembly, ModelInteraction Evidence, and downstream outcome/evaluation identity.
This is a correlation and evidence requirement for the purpose being supported,
not a requirement that every concept have standalone identity, persistence, an
independent lifecycle, or universal storage. It creates no universal
`ReplayRecord`, `Episode`, or Trace and does not collapse repository state,
derivation, retrieval, disclosure, model interaction, and evaluation into one
ownership domain.

The implementation-start assessment is **SAFE WITH PRESERVED SEAMS**. A bounded
repository-intelligence slice can enter concrete design without a generic
Evaluation framework, provided it does not foreclose retention or correlation
of the semantic basis its claims require. Depending on the slice, that includes
deterministic fixture/state reference, RepositorySnapshot identity and
observation semantics, consumed external semantic inputs, DerivationDefinition
meaning and compatibility basis, direct dependencies, produced
DerivedKnowledge and result-specific support, relevant qualification and
semantic-result coverage, distinct success/zero/partial/exhaustive/failure
semantics, analyzer/binding provenance, and correlation among requested work,
realization, dependencies, results, diagnostics, and terminal outcome. This is
neither implementation authorization nor a claim that Evaluation infrastructure
exists.

The external adversarial confirmation remains a confirmation/reopen gate, not
an implementation-start gate. It can reopen architecture if it exposes a
material defect. Initial design remains governed by B-0002 promotion and must
preserve local semantic correctness separately from downstream/task utility,
typed resource observations, and the intended factor/fixed-condition seams
needed to assess marginal contribution or interaction effects later.

Supporting historical investigations are indexed in [research evidence](research/README.md).
They preserve rationale and alternatives; ADRs and this document remain the
authoritative accepted architecture.

Remaining choices such as snapshot digest/Merkle construction, observation
mechanics, parser/analyzer technology, graph storage/indexes/algorithms,
cache/persistence backend, concrete dependency representation and per-family
granularity, capability APIs/scheduling, InformationNeed and RelevanceEvidence
representations, retrieval/ranking implementations, DisclosurePlan/
ContextDisclosure models, materializer and synthesis mechanisms, and exact
evaluation metrics/benchmarks are normally implementation-design and empirical-
evidence questions under the accepted constraints, not reasons to continue
general abstract architecture research.

Settled foundational semantics should be reopened only when concrete research
or implementation evidence contradicts an accepted invariant or shows that
required semantics cannot be represented correctly. Representative triggers
include external state that cannot be represented reproducibly, no viable
dependency granularity preserving correct applicability, required graph
composition needing a missing common semantic abstraction, bounded realization
preventing correct dependency discovery, a knowledge family unable to express
its qualification, Context realization unable to preserve semantic strength,
or accepted layer boundaries preventing meaningful causal evaluation.

See [documentation_map.md](documentation_map.md) for current package
documentation, [taxonomy.md](architecture/taxonomy.md) for definitions, and
[ADR-0001](architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
for the approved future boundary.


### Repository-map structural retrieval

Production Retrieval now also exposes a separate repository-map channel over
Repository Intelligence (RI): query-independent dependency PageRank importance,
compact symbol/path BM25 relevance, symbol rank combination, and maximum-symbol
resource projection. It retains exact declaration identity, source support and
native incoming fact flow. Uniform resource restart and exclusion of outward
containment avoid creating importance merely through declaration count.
This is distinct from lexical-resource-seeded Personalized PageRank (PPR).
Optional Reciprocal Rank Fusion (RRF) combines resource ranks while retaining
native evidence. Neither channel chooses Context, budget or sufficiency.
Selection remains an operation within Context Planning; map rendering and
materialization remain after explicit representation choice. See the
[repository-map package contract](../src/devtools/context/retrieval/repository_map/docs/overview.md)
for algorithms, provenance, supported scope and diagram, and the
[frozen development diagnosis](../experiments/repository_map_baseline/README.md).
No new domain, dependency direction, durable schema or ADR is introduced.
The [first prospective multi-channel case](../experiments/codex_dogfood/case_0003/README.md)
is now complete on the independently justified configuration RI task. It
preserves ranking parameters and evaluates the pre-implementation structural
coverage: map promotes several repository primitives but omits fourteen of
nineteen required resources; lexical/map fusion worsens complete coverage.
Typed PPR improves full-prompt complete depth while hurting early recall.
These are local development observations, not a universal ranking/Selection
policy. Case 0002 remains strictly diagnostic. New configuration RI facts are
not projected into any ranking channel without a separate Retrieval decision.
