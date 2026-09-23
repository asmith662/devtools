# ADR-0002 — Repository intelligence identity and derivation semantics

- Status: Accepted
- Date: 2026-09-16
- Scope: semantic architecture for future repository intelligence and coding
  Context, including repository subject, source-occurrence, derivation, and
  graph semantics; snapshot observation, SnapshotDelta, and incremental-
  maintenance semantics. This decision authorizes no production implementation,
  storage, parser, graph, retrieval system, or Context compiler.

## Research reconciliation

This ADR is supported by the [snapshot identity](../../research/repository-snapshot-identity.md),
[subject identity](../../research/repository-subject-identity-and-decomposition.md),
[DerivedKnowledge boundary](../../research/repository-derived-knowledge-boundary.md),
[information-boundaries](../../research/repository-information-boundaries.md),
[comparative architecture](../../research/repository-intelligence-architecture-review.md),
and [adversarial review](../../research/architecture-adversarial-review.md) investigations.

They reinforce that nominal Repository identity differs from paths/checkouts/Git;
snapshots, occurrences, subjects, source anchors, derivation, knowledge, support,
coverage, and applicability remain distinct; determinism does not make every
proposition intrinsic repository truth; and model synthesis is not automatically
DerivedKnowledge. Qualified repository relationships do not imply runtime
dependency or retrieval relevance. Universal graph/store, confidence, authority,
and conflict machinery remain rejected for now. Snapshot consistency policy,
incremental reuse, external semantic state, and richer applicability remain
deferred pending concrete consumers.

Revisit these choices only when evidence shows the accepted qualification and
dependency semantics cannot represent an independently useful bounded slice.

## Context

Existing filesystem and Tool boundaries establish bounded file access, not
repository identity, repository knowledge, retrieval, or Context compilation.
Earlier bounded Qwen navigation evidence proved only root-origin fact
acquisition. It did not establish reusable inventory, ranking, symbol search,
retrieval, selection, budgeting, or compilation semantics.

Repository intelligence must be useful independently of a language model. It
also must make incremental reuse and invalidation explainable without mistaking
a checkout path, Git commit, or heuristic rename for foundational identity.
Coding Context is separately the purpose-relative selection and disclosure of
such information to a task or model.

## Decision

### Repository state and identity

A **Repository** is a logical software repository across changing states. It
has nominal logical identity. Its identity is not its filesystem path, current
contents, Git commit, or a particular checkout. A repository may be backed by
a Git checkout, temporary fixture, generated workspace, extracted archive, or
another supported resource arrangement. `ResolvedPath` and filesystem
Resources remain access and location mechanisms; they do not acquire
repository-identity meaning.

A **RepositorySnapshot** is an immutable, logically complete description of
successfully observed repository state under explicit snapshot and observation
semantics. Its identity is content-derived, not merely timestamp- or
Git-commit-derived. Logical completeness is relative to declared inclusion
semantics; it does not require every filesystem object below a root, physical
copying of all state, or rescanning/rebuilding all intelligence. A snapshot can
share unchanged physical representation with another snapshot while each still
describes a complete state. Git metadata may be provenance associated with a
snapshot, but does not define snapshot identity: dirty working-tree states can
share a Git HEAD while being different snapshots.

Snapshot semantics must be able to establish root, inclusion/exclusion and
ignore treatment, generated/vendor/binary treatment, symlink/nested-repository/
submodule behavior, identity-relevant resource attributes, and necessary path
interpretation. The exact SnapshotPolicy API and universal default remain open.
Policy/observation semantics and resulting repository-state identity are not
casually identical: distinct policies can potentially observe equivalent state,
while some policy differences can be identity-relevant. The exact relationship
is deliberately unresolved.

Observation succeeds only under an explicit consistency guarantee. A mechanism
must not claim a stronger simultaneous-filesystem-state guarantee than it can
establish through sequential reads and stats. Future Git/tree-backed,
filesystem-snapshot, validated/optimistic, retry-based, or other observation
mechanisms remain possible. Filesystem watcher events are triggers or dirty-set
hints, never authoritative repository truth or a SnapshotDelta by themselves.
An observation that cannot satisfy its declared completeness/consistency
contract must not masquerade as a complete snapshot.

Snapshot identity must be deterministic, reproducible under equivalent snapshot
semantics, address-sensitive where address is state, sensitive to identity-
relevant resource attributes, insensitive to irrelevant ephemeral metadata,
and traversal-order independent where order has no semantics. It must represent
working-tree/non-Git state and permit efficient physical computation/reuse.
Merkle-compatible or cryptographic approaches are motivated possibilities, but
this ADR selects no digest algorithm, flat-versus-hierarchical construction,
serialization, persistent structure, or storage representation.

Do not create a magical persistent file/resource identity. A repository
resource occurrence is instead contextual: a snapshot plus a repository-
relative address/path, independently referring to reusable content-derived
identity. Exact production naming, including whether `ResourceOccurrence` is
used, is open. ContentIdentity is deterministic, address-independent, reusable
across snapshots and potentially repositories, and independent of irrelevant
occurrence metadata. Exact raw-versus-normalized content semantics and digest
construction remain open; parsed, normalized, and derived-representation
identities are separate from foundational ContentIdentity. Identical content has
stable content identity across snapshots and locations under applicable content
semantics:

- an edit changes content identity;
- a move changes occurrence/address but can preserve content identity;
- a copy creates another occurrence referring to the same content identity;
- deletion removes the occurrence; deletion/recreation of identical content
  need not assert historical object continuity.

`RENAMED_FROM`, `MOVED_FROM`, `COPIED_FROM`, and entity evolution are derived
knowledge, not foundational identity. Likewise, symbols, document sections,
and other repository entities may have structural identity only within the
source/knowledge state establishing them. Cross-snapshot entity continuity is
future derived knowledge with evidence, never hidden inside an identity
primitive.

### SnapshotDelta and incremental maintenance

**RepositorySnapshot**, **SnapshotDelta**, and **IncrementalMaintenance** are
separate concepts. A SnapshotDelta is a relationship/difference between two
identified repository states. It may describe direct structural facts such as
an address added/removed, same address with changed/unchanged content, or the
same ContentIdentity at another address. It does not define snapshot identity,
make a snapshot an ordered mutation history, establish rename/copy/continuity,
or become authoritative state merely because watcher events occurred. Its
concrete model and persistence remain open.

**IncrementalMaintenance** is the process for efficiently establishing
repository intelligence applicable to a repository state. It does not define
repository state or require a full recomputation: applicable knowledge may be
reused while inapplicable or missing knowledge is derived as needed. Immutable
snapshots and incremental maintenance are therefore complementary, not
contradictory. Persistent data structures, content-addressed stores, Merkle
DAGs, and cache layouts are possible mechanisms, not this architecture.

Snapshot completeness and repository-intelligence completeness are distinct.
A valid snapshot may exist while analyzers fail or desired knowledge is absent,
provided such intelligence incompleteness is represented rather than silently
treated as complete. Conversely, unreadable or excluded material permits a
snapshot only when the declared snapshot/observation contract classifies it
accordingly.

Git remains optional support, provenance, and optimization: it may later offer
committed-tree observation, enumeration, content acceleration, change hints, or
historical access, but repository identity, snapshot identity, and working-tree
state remain VCS-independent. Retention is similarly separate from meaning.
Evicting a snapshot representation, cached content, DerivedKnowledge, or an
index does not change the historical meaning of its identity; the architecture
preserves future replay, comparison, debugging, provenance inspection, and
historical reasoning without requiring indefinite persistence.

### Repository subjects and source occurrences

**Subjecthood** and **derivation** are orthogonal. A **RepositorySubject** is
an identifiable thing within a repository state about which repository
intelligence can make assertions. **DerivedKnowledge** instead answers what is
known about repository things, from which dependencies, through which
derivation, and with what provenance/applicability. Analysis can establish a
RepositorySubject without making subjecthood a pre-existing filesystem fact:
parsing may establish that an identifiable Python method exists, and later
analysis may derive knowledge about that method. Thus being derived through
analysis does not make a thing ineligible to be a subject.

RepositorySubject deliberately covers heterogeneous repository artifacts, not
only code. An analyzer may establish a Python module, class, function, method,
or nested function; a Markdown document or section; a configuration table or
entry; or a workflow, job, or step. This is not a closed kind taxonomy.
Independent referential identity is justified when a repository-intelligence
domain needs to attach knowledge, relationships, queries, or dependencies to a
thing independently. Statements, expressions, parameters, and blocks are
therefore neither universally subjects nor universally excluded.

A **SourceOccurrence** is an identifiable/addressable source span or anchor
within a ResourceOccurrence: for example a declaration, reference/use, call
site, import occurrence, literal, or another source anchor. It can participate
in provenance and relationships without becoming a RepositorySubject, and is
only snapshot-locally addressable/identifiable. A source occurrence can
declare, define, or reference a subject, but source location is not semantic
subject identity. A snapshot, path, and range can locate a method; harmless
line insertion can change that locator without changing the subject an analyzer
recognizes. Concrete subject identifiers, locators, fingerprints, and matching
algorithms remain open.

RepositorySubject identity is snapshot-local. There is no foundational global
semantic entity intended to survive arbitrary repository evolution. Same
logical entity, rename/move/copy, evolution, split, and merge claims between
subjects in different snapshots are DerivedKnowledge with future evidence,
confidence, or ambiguity where appropriate.

AST and parser nodes are analysis artifacts by default, not subjects merely
because they appear in a parse tree. A `FunctionDef`-like node can establish a
function subject; a parser-internal node without independent repository-
intelligence identity need not. Conversely, a future analyzer may establish a
fine-grained subject when it has a justified identity model.

Names and qualified names are not foundational RepositorySubject identity.
Declared name, containment, qualified-name, and name-resolution facts are
DerivedKnowledge. A resolved semantic entity may itself be a RepositorySubject,
but this architecture neither requires a separate foundational `Symbol`
abstraction nor prevents a future analyzer from adding justified symbol-specific
semantics.

### Distinct decomposition semantics

Three non-equivalent decompositions must remain separate. **Analyzer-established
structural decomposition** analyzes repository material into identifiable
structural subjects, such as a module, class, method, or nested function. It is
reusable repository intelligence. **Repository-semantic decomposition** may
derive timeout branches, failure paths, lifecycles, authorization interactions,
behavioral regions, or responsibilities. These are DerivedKnowledge by default,
not automatically foundational subjects; a future analyzer can establish a
semantic subject only with a justified independent identity model.

**Purpose-relative decomposition** is downstream: ADR-0003/ADR-0004 allow an
information purpose to lead to subordinate demands such as timeout
configuration, enforcement, handling, evidence, and tests. Those demands are
not RepositorySubjects merely because acquisition was decomposed. Similarly, a
coherent Context disclosure can combine a signature, source region, exception type,
tests, and a knowledge projection without making that purpose-relative
composition a RepositorySubject.

### DerivationDefinition, Derivation, execution, and DerivedKnowledge

**DerivationDefinition** is the identified reusable semantic computation: for
example Python structural analysis under grammar semantics, import resolution,
call analysis, or continuity analysis. It answers what semantic computation
exists. It is not necessarily a callable, class, plugin, Tool, package,
executable, worker, or source-code digest. Implementation binding belongs to
later capability/execution design.

The DerivationDefinition and its result vocabulary define what each result
semantically asserts. DerivedKnowledge does not strengthen that meaning merely
by being immutable or reusable. Conceptually, `MAY_CALL(A, B)`,
`MUST_CALL(A, B)`, and `CANNOT_CALL(A, B)` would be different propositions if a
particular knowledge family defined them: a conservative possible target is not
a definite call with lower confidence. Predicate names are illustrative rather
than a universal repository ontology; a concrete family may use another
representation, including qualified values, when its semantics remain explicit.
The definition semantics must make proposition meaning, relevant semantic
qualification, and any coverage/exhaustiveness obligations available wherever
correct interpretation or evaluation requires them. A name such as `CALLS`
alone is insufficient if it hides whether the result means definite,
possible, conservative, unresolved, partial, or exhaustive. This requires an
interpretable family contract, not one universal qualifier schema or evaluator
API.

A **Derivation** is the identified semantic application of a
DerivationDefinition to explicit direct semantic dependencies. It is not its
execution attempt. A parse derivation can therefore mean PythonParse applied to
ContentIdentity X; a changed dependency or incompatible definition semantics
can establish a different derivation. The concrete identity construction is
open. The invariant is:

> Equal derivation identities imply equivalent derivation semantics for
> identical relevant inputs.

Definition identity/compatibility concerns semantic behavior, not merely
implementation source/build identity. A compatible refactor need not establish
incompatible definition semantics, while a small implementation change can.
Semantic-versioning, compatibility declarations, implementation digests, and
other mechanisms remain open.

A **DerivationExecution** is a particular attempt to realize a Derivation; it
may establish zero or more DerivedKnowledge artifacts. This is conceptual
terminology, not a new repository-specific Attempt model. Existing specialized
`InteractionAttempt` and terminal Evidence retain their execution/observation
ownership. Future derivation execution must use compatible execution/evidence
semantics rather than making execution records repository truth.

The same semantic separation can be realized simply as computation semantics,
semantic computation key, execution record, and semantic result(s), respectively.
It does not require four services, repositories, lifecycle managers, or one
production class per concept. Concrete model, API, storage, and sharing forms
remain open.

Any change capable of changing results—such as parser behavior, analysis
configuration, embedding model, or relationship-resolution semantics—must be
reflected in definition compatibility, derivation identity, or applicability.
A downstream ranking-policy change must not affect repository knowledge that
does not depend on it.

Grammar/language version, toolchain semantics, feature flags, and environment
state likewise participate only where actually consumed. Unchanged repository
content alone never justifies reuse when relevant derivation semantics changed.

**DerivedKnowledge** is a foundational repository-intelligence concept, not a
required Python base class or a universal container for semantic assertions. It
is semantic repository intelligence established by an identified Derivation
over explicit identified dependencies, with result/value and provenance. Its
meaning is exactly the meaning established by that DerivationDefinition and
result vocabulary, including any relevant assumptions, approximation,
ambiguity, uncertainty, scope, or completeness semantics. DerivedKnowledge does
not mean hard, infallible, Boolean-like fact. It can express definite, possible,
necessary, conservative over-approximate, explicitly under-approximate,
ambiguous, unresolved, bounded, exhaustive, partial, or other qualified
repository-relative relationships, classifications, semantic properties, and
results when the relevant derivation semantics define those propositions. Its
identity should be reproducibly associated with derivation, dependencies, and
result semantics, not merely an arbitrary UUID. Exact digest construction is
open, including whether result participates directly when determinism permits
derivation plus dependencies to determine it.

DerivedKnowledge is immutable and not foundationally snapshot-owned. It
retains derivation, direct dependencies, value, provenance, and stable identity
sufficient for reference, replay, evaluation, and reuse; applicability to a
state is assessed separately. Values remain heterogeneous: structural results,
relationships, diagnostics, collections, projections, assertions, and other
results rather than a universal key-to-scalar shape. RepositorySubjects remain
distinct from knowledge about subjects, and relationships remain typed
DerivedKnowledge values.

One Derivation may establish zero or more separately referable knowledge
artifacts. Execution, derivation, and result granularity are distinct and may
be refined without requiring one monolithic result or maximal atomization. Zero
produced knowledge is not proof of semantic absence unless derivation semantics
explicitly establish exhaustive coverage; positive results likewise do not prove
the result set exhaustive. A derivation capable of establishing exhaustive
coverage must represent that claim/evidence explicitly. Concrete grouping,
coverage, and cardinality APIs remain open.

Not every internal computation output, temporary value, parse node, traversal
datum, score, intermediate structure, or implementation artifact automatically
becomes DerivedKnowledge. DerivedKnowledge is semantic knowledge worth
establishing and referencing under repository-intelligence semantics. One
derivation can establish one result, many independently referable results, a
meaningful grouped result, or a combination with shared structure/provenance.
The appropriate result granularity depends on semantic referential needs,
applicability/reuse and downstream dependency needs, and operational cost; it
does not require maximum fragmentation or one monolithic result set.

Nor does every semantic assertion elsewhere in the system automatically become
DerivedKnowledge. Provenance-bearing information is not automatically
repository intelligence. ADR-0003 RelevanceEvidence and ADR-0004
purpose-relative Context synthesis can be semantic, deterministic,
reproducible, and provenance-bearing without acquiring DerivedKnowledge
identity, applicability, persistence, or reuse semantics. Repository-relative
declarations, definitions, references, imports, call/inheritance/override/
implementation/test relationships, cycles, reachability, and other reusable
structural or semantic assertions remain characteristic DerivedKnowledge when
an identified repository Derivation establishes their stated meaning. This is a
jurisdiction boundary, not a restriction to only certain or infallible facts.
Evaluation judgments remain outside the boundary as well. An evaluator can
assess a DerivedKnowledge result against a fixture or oracle without making
“this analyzer result was correct for this evaluation” repository
DerivedKnowledge. Benchmark outcomes, statistical estimates, human ratings,
resource measurements, and execution failures retain their evaluation or
execution semantics even when deterministic and provenance-bearing.

The architecture does not introduce a universal Claim, Assertion, Proposition,
Belief, or TruthRecord layer spanning repository intelligence, retrieval
evidence, Context synthesis, and authority judgments. Those responsibilities
have different identity, applicability, purpose, and lifecycle semantics. A
future specialized subsystem may use claim-like structures when concrete
requirements justify them without redefining DerivedKnowledge as a universal
epistemic container.

#### Epistemic derivation and representational transformation

A **representational transformation** changes how already available information
is exposed without intentionally establishing a materially new semantic
assertion. Source extraction, selecting a method signature, formatting,
source-preserving projection, and lossless structural packaging can require
computation without thereby producing DerivedKnowledge.

An **epistemic derivation** establishes a materially new semantic assertion. A
repository derivation that establishes a possible call, resolved reference,
dependency cycle, transitive reachability result, or another explicitly defined
repository semantic can establish DerivedKnowledge. Lossy compression or a
summary can also cross this semantic boundary when it asserts an interpretation
rather than merely representing existing information.

The distinction is semantic, not a class, protocol, enum, or mandatory artifact
taxonomy. Not every epistemic derivation belongs to repository intelligence:
ADR-0004 may establish purpose-relative synthesized information for disclosure
without promoting it to DerivedKnowledge. Whether such synthesis later merits
independent identity, persistence, caching, querying, or reuse remains open.

#### Semantic-result coverage, completeness, and absence

**Semantic-result coverage** is the conceptual account of what result space an
identified derivation or result set claims to have accounted for under stated
scope, assumptions, and derivation semantics. It can vary by subject, region,
relationship family, language feature, configuration, or another semantic
domain within one execution. It is distinct from ADR-0004 purpose-relative
disclosure coverage, which asks what information a proposed Context disclosure
contributes toward an InformationNeed.

Execution success is not semantic completeness and does not imply one global
`complete: bool`. Zero results do not prove absence; positive results do not
prove exhaustiveness; partial semantic analysis is not execution failure; and
unsupported semantic territory is not negative knowledge. Absence of a
knowledge artifact normally means unknown or not established. It acquires
negative semantic force only when the identified derivation semantics and
sufficient semantic-result coverage justify that inference. The architecture
therefore selects no global open-world or closed-world policy.

Semantic-result coverage is not provenance. Provenance explains origin and
support; coverage states the accounted-for semantic result space. Coverage can
itself require support and replayable semantics without requiring a standalone
artifact, identity, persistence model, or production class. Concrete coverage,
grouping, and publication representations remain open.

A Derivation records **direct semantic dependencies**, whose role in the
computation is preserved conceptually. Content X can be source content;
namespace knowledge can be resolution namespace; configuration can be
resolution configuration. Dependency identity alone is not always enough when
role changes the computation. Direct dependencies need not flatten transitive
closure: a derivation consuming K2 need not claim direct consumption of Content
X merely because K2 depends on it. Transitive applicability follows the
dependency structure; closures, reverse indexes, and dirty sets are maintenance
optimizations.

Semantic dependencies are not incidental execution inputs. Source content,
grammar semantics, namespace, and resolution configuration can be semantic;
worker count, trace ID, temporary directory, logging configuration, execution
timestamp, and scheduling choice do not automatically become semantic merely
because execution consumed them. Actual derivation semantics are authoritative.
Semantic consumption is therefore not an instrumentation-level trace of every
byte, AST node, temporary path, log field, worker setting, or operational object
touched during realization. The finalized record captures the semantic
support/applicability boundary established by derivation semantics, not every
implementation access.

Dependency granularity must be sufficient for correct semantic applicability.
Finer granularity is an incremental-maintenance optimization, justified only
when its reuse or avoided recomputation outweighs additional dependency-record,
reverse-index, comparison, persistence, maintenance, and analyzer complexity.
Whole-snapshot, resource/content, subject/region, and finer structural scopes
are all possible where their semantics justify them. Maximum theoretical
precision is not an architectural objective, and no universal granularity is
selected.

The applicability rule is:

> DerivedKnowledge is applicable when its explicit semantic dependencies are
> satisfied under the same relevant derivation semantics.

Dependencies are heterogeneous semantic inputs, not a universal `(path,
ContentIdentity)` representation and not necessarily ResourceOccurrences. A
parse of Content X may depend on X plus parser/grammar semantics but not its
address; qualified module naming can depend on repository-relative address; an
import resolution can depend on local content plus wider namespace/resolution
state. Dependencies may include ContentIdentity, ResourceOccurrence,
RepositorySubject, SourceOccurrence, other DerivedKnowledge, snapshot-scoped
facts, derivation configuration, language/toolchain semantics, or another
explicitly identified semantic input. Actual consumed dependency scope, rather
than a fixed local/relational category, is authoritative.

Dependencies and provenance differ. A dependency identifies semantic input
whose satisfaction affects derivation/applicability; provenance explains how a
result was established and what supports it. They can overlap without being the
same record. Derivation-level provenance can explain shared computation and
dependencies, while knowledge-specific provenance can identify SourceOccurrences
or other support for one resulting assertion. Neither physical duplication nor a
provenance schema is required here. Common definition, broad dependency,
analyzer-semantics, or execution-lineage information need not be duplicated for
every result merely because result-specific support may be narrower. Structural
sharing, compact references, bounded support, lazy traversal, and selective
persistence remain future representation choices, not weaker provenance
semantics.

Provenance explains origin and support. It does not by itself establish
authority, semantic certainty, correctness, or truth. Those concerns can depend
on the claim, purpose, derivation semantics, source role, uncertainty,
completeness, conflict, and other future assessment semantics; no universal
authority or truth score is selected here.

The conceptual boundaries are therefore:

- the semantic assertion/result is what repository-relative meaning was
  established;
- semantic dependencies are the direct inputs whose state bears on
  applicability and replay;
- assumptions and semantic scope qualify the conditions and interpretation
  under which the result means what the DerivationDefinition says it means;
- provenance explains production, origin, and support;
- semantic-result coverage describes the accounted-for result space;
- applicability asks whether immutable knowledge still applies under another
  relevant state or condition; and
- execution Evidence records what occurred while attempting realization.

Language/toolchain semantics, configuration, supported feature sets,
environment assumptions, and analysis scope can participate in assumptions,
scope, dependencies, or definition semantics according to their actual role.
The distinctions do not require one production object per concept or one
universal metadata bag.

#### External semantic dependencies and observation

Repository-intelligence semantics admit an open, heterogeneous dependency
universe. Configuration, language version/mode and semantics, compiler or
interpreter/toolchain semantics, dependency-resolution state, build features,
target platform, semantically relevant environment values, generated inputs,
external schemas/resources, and other state outside repository contents can be
semantic inputs where an identified derivation actually consumes them. These
are illustrative families, not a closed ontology or a requirement for one
foundational class per family. According to their role, they can participate in
DerivationDefinition semantics, direct semantic dependencies,
assumptions/scope, provenance where appropriate, and applicability.

Semantically relevant external state must not remain an invisible ambient
dependency. If it can change a derivation's meaning or result, the finalized
derivation/dependency/assumption-scope semantics must account for it according
to its role, with corresponding provenance where appropriate. A dependency
needs enough identity, value, reference, constraint, or other semantic
representation to support correct derivation meaning, applicability,
provenance, and the intended replay strength. This does not require every input
to have independent nominal identity, persistence, or a standalone artifact: a
value, reference, constraint, existing identified object, inline observation,
or another suitable representation can be sufficient.

The semantic thing that matters, its relevant state/value, and how that state
was observed or established are distinct roles. An observation of semantic
state must not claim stronger identity, consistency, completeness, equivalence,
or other semantic guarantees than its mechanism establishes. Merely recording
a label such as a language version need not establish how it was observed or
what that observation guarantees. Observation remains a semantic requirement,
not a universal `StateObservation` model: a future implementation may represent
it inline, independently identify it, share it among derivations, derive it from
another semantic artifact, or use a domain-specific structure.

Identity, state/value equality, semantic equivalence, compatibility, and
applicability remain distinct. Dependency satisfaction need not always be exact
identity equality. It can use identity, value equality, semantic equivalence,
compatibility, constraint satisfaction, or another relation defined by the
dependency domain and the DerivationDefinition's actual sensitivity. For
example, two observed CPython patch releases can remain distinct states while
both satisfy a derivation whose semantics require only a compatible Python 3.12
language range. This does not select a universal equivalence algorithm,
compatibility framework, or applicability API, and identity must not be
redefined merely to increase reuse.

No foundational universal `WorkspaceSnapshot`, `EnvironmentSnapshot`, or other
composite of repository contents plus toolchains, platform, dependencies,
environment, configuration, generated state, and external resources is
accepted. Such a composite would generally be coarser than the actual semantic
dependencies and difficult to observe under one meaningful consistency
contract. Narrower domain-specific or composite observations remain permitted
when evidence justifies them; they are semantic dependencies among others, not
the foundational identity of repository intelligence.

One RepositorySnapshot can therefore support multiple simultaneous semantic
interpretations. Derivations over the same repository state may legitimately
consume different language/toolchain versions, platforms, feature sets, build
configurations, or dependency-resolution states. Repository state is not the
semantic interpretation of that state, and multiple configurations do not by
themselves require separate RepositorySnapshots or a universal workspace
snapshot. Enumeration and product-space analysis remain unselected mechanisms.

Generated material does not create a binary choice between RepositorySnapshot
membership and external dependency. Committed generated files can be
ResourceOccurrences when included by snapshot policy. Other generated or
analysis-visible material can be established through derivation without being
misrepresented as observed repository contents, or can belong to a future
analysis-universe/resource representation. External generator inputs can
themselves be semantic dependencies. Concrete generated-resource semantics and
representations remain open; generated material alone does not expand
RepositorySnapshot responsibility.

PATH-selected tools, environment variables, external filesystem resources,
registry state, remote schemas, platform semantics, resolution state, and
similar ambient influences are examples of possible hidden dependencies, not a
mandatory taxonomy. Bounded access and finalized dynamic dependency accounting
remain required, while sandboxing, hermetic execution, access mediation,
tracing, instrumentation, and dependency-enforcement mechanisms remain open.

Replay has multiple strengths with different retention requirements:

- provenance inspection explains which inputs/state were believed to support a
  historical result and how it was produced;
- semantic replay or reconstruction recovers enough semantic state to reproduce
  or reassess the derivation/result meaning; and
- operational replay recreates a historical executable environment and reruns
  the computation.

Supporting provenance inspection or applicability does not require retaining
every compiler binary, package registry, container, virtual machine, or other
executable artifact. Conversely, retained semantic identity does not prove that
the executable artifact or historical environment remains reconstructable.
Retention, artifact stores, environment reconstruction, and concrete replay
mechanisms remain open.

External dependencies and their observations also bound negative or exhaustive
knowledge. Claims such as no unresolved imports, no references to a subject, or
all implementations of an interface cannot claim closure beyond the dependency
resolution, configuration/plugin state, generated/external resources, scope,
assumptions, observations, and semantic-result coverage their derivation
establishes. No universal closed-world flag follows.

Applicability, invalidation discovery, rederivation, and caching/reuse lookup
are distinct. Applicability is the semantic question whether knowledge applies;
invalidation discovery is how maintenance efficiently detects lost
applicability; rederivation obtains needed replacement/new knowledge; and a
cache lookup asks whether applicable knowledge is already available. Reverse
dependency indexes, dirty sets, red/green or build-style engines, watcher hints,
Merkle structures, and persistent caches may support those operations but do
not define applicability.

Snapshot provenance and applicability differ. One immutable DerivedKnowledge
artifact first derived while examining S1 can be applicable to S1 and S2 when
its actual dependencies and derivation semantics hold; it need not be copied or
rebound per snapshot. If it does not apply at S2, its immutable historical
derivation result and provenance remain unchanged rather than becoming
universally invalid. This preserves targeted reuse, caching, persistence, replay,
provenance, and potentially distributed derivation without claiming universal
cross-snapshot continuity.

Applicability is external to immutable knowledge state: conceptually it is an
assessment over knowledge dependencies, derivation semantics, and relevant
state/environment, not a mutable `currently_valid` flag inside knowledge. The
assessment may later be provenance-bearing and evaluable without selecting that
model now.

A failed DerivationExecution is execution evidence, not automatically
DerivedKnowledge or a semantic negative fact. A separate successful analyzer
can derive a diagnostic such as a syntax error, but a parser crash does not do
so by itself. Likewise, partial execution does not make independently
established artifacts false or historically invalid: supported qualified call
results produced before another region fails can remain knowledge when their own
derivation/provenance semantics support them. They do not establish a complete
call graph. Transactional publication, buffering, and partial-result APIs are
open. Execution timestamp, worker/machine identity, cache location, mutable
Attempt record, or success flag do not by themselves govern applicability.

Determinism is not correctness or certainty, and confidence is not completeness.
A deterministic derivation can consistently produce an incorrect or heuristic
result. It can also establish precisely qualified repository intelligence such
as a possible call, may-alias relation, unresolved reference, conservative
reachability result, or analysis under explicit assumptions. Those are not
downgraded versions of an unqualified fact: their qualification is part of the
DerivationDefinition and result semantics. Confidence, alternatives, ambiguity,
uncertainty, scope, and completeness belong to derivation- or knowledge-specific
semantics where meaningful. Possible, necessary, ambiguous, conservative,
unsupported, unresolved, heuristic, and probabilistic results are not presumed
to occupy one common certainty axis. No universal confidence/certainty field,
`MAY | MUST | UNKNOWN` enum, probability, truth score, or epistemic scalar is
required for every DerivedKnowledge artifact. A specialized derivation may
produce a numeric probability only when its DerivationDefinition identifies the
probabilistic quantity and its interpretation.

### Repository-intelligence capability boundary

A repository-intelligence **capability** is defined first by the compatible
DerivationDefinition semantics it can realize, not by an arbitrary operation it
exposes. A DerivationDefinition can be known even where no current environment
can realize it. The architecture therefore distinguishes known semantic
computation, supported semantics, currently available realization, and an
execution's outcome.

Semantic capability and implementation binding are distinct responsibilities.
Multiple bindings can realize compatible definition semantics, and future
selection can consider availability, incremental state, platform, performance,
cost, and language/toolchain support without changing the requested knowledge.
One concrete object may later combine capability and binding representations;
that operational choice must not collapse semantic definition identity,
implementation identity, availability, or historical knowledge meaning.
Registration/discovery can expose available realizations, but its runtime or
configuration contents do not create DerivationDefinition meaning. Historical
Derivations and DerivedKnowledge retain their meaning when an implementation is
unregistered, replaced, or unavailable.

The boundary is:

```text
required semantic derivation
    -> maintenance / realization planning
    -> available semantic capability
    -> implementation realization
    -> execution
    -> DerivedKnowledge
```

Maintenance/planning determines what semantic work is required; the capability
boundary determines whether/how admitted work can be realized; execution
performs a selected realization. An individual capability does not own global
reuse/cache decisions, prerequisite derivation planning, caller information
needs, eager/lazy maintenance policy, or global scheduling.

Capability realization receives bounded access to declared repository state and
semantic inputs through an execution boundary capable of accounting for what it
consumes. Unrestricted ambient `analyze(repo_root)` access to a live filesystem
is not the foundational model. Efficient in-process access remains permitted;
the architecture does not require RPC or a Tool call for every read. Semantic
dependencies can be discovered dynamically during realization, but every
semantically relevant dependency actually consumed must become explicit in the
finalized dependency/provenance record. Expected dependencies alone do not
govern replay or applicability. “Consumed” is semantic rather than a demand for
an undifferentiated access trace: dynamically discovered support must be
captured when it affects semantic applicability, not merely because an
implementation touched it operationally.

Repository intelligence is deterministic and LLM-independent foundationally,
and observational with respect to the repository state it analyzes. A capability
must not silently gain Agent authority, invoke arbitrary model-visible Tools,
send model requests, expand its authority, or mutate the analyzed repository.
Operational side effects outside that stateâ€”for example cache/index writes,
temporary files, persistence, or execution evidenceâ€”remain possible but are
not selected mechanisms. LLM-assisted or nondeterministic analysis requires
explicitly different derivation, evidence, and governance semantics rather than
masquerading as this substrate.

This foundational preference concerns realization reproducibility and the
currently accepted capability boundary; it does not make DerivedKnowledge mean
a semantically certain result. Semantic meaning belongs to the
DerivationDefinition/result vocabulary, while operational determinism describes
how a realization behaves. A future learned or probabilistic analyzer could,
after explicit architectural acceptance, establish a repository-relative
prediction, classification, heuristic result, or bounded approximation whose
qualified proposition is defined by its DerivationDefinition. It must not
silently strengthen `model predicts X` into `X is true`. No learned analyzer,
model identity, probability representation, validation policy, or execution
infrastructure is selected here.

Model output does not become DerivedKnowledge merely because temperature is
zero, execution is reproducible, provenance is recorded, multiple models agree,
a human agrees, or a model reports high confidence. A later repository
Derivation can independently establish the corresponding repository semantics.
Whether learned, model-assisted, or validated interpretive analysis can become
reusable repository intelligence remains unresolved; this does not prohibit a
future learned analyzer with explicitly accepted derivation, evidence, and
governance semantics.

Repository-intelligence admission differs from ADR-0001 model Tool
authorization. The former may constrain repository/snapshot, resources,
configured realizations, and bounded time/memory for internal deterministic
work; the latter governs untrusted model-proposed actions. Common governance or
execution primitives may later be reused without merging responsibilities.

Retrieval consumes repository intelligence and must not silently own arbitrary
derivation merely because knowledge is absent. Additional knowledge acquisition
crosses an explicit repository-intelligence maintenance/realization boundary so
cost, latency, provenance, concurrency, replay, and incremental work remain
observable. Repository Intelligence is neither Tool, Agent, retrieval, Context
compiler, nor generic Runtime ownership.

Capability execution must eventually correlate requested semantic work,
DerivationDefinition, actual consumed dependencies, produced knowledge,
semantic-result coverage and partial/exhaustive claims where relevant,
diagnostics, and terminal outcome. This is execution evidence, not
applicability or completeness authority. Unknown
semantics, known-but-unsupported semantics, supported-but-unavailable
realization, admission denial, execution failure, successful zero result,
successful partial result, and successful exhaustive result remain distinct
future outcomes; no error hierarchy or evidence schema is selected.

Independent derivations may realize concurrently, but individual capabilities
do not own global dependency scheduling or concurrency policy. Future
maintenance/planning and scheduler mechanisms can order actual dependencies and
exploit independence without becoming capability semantics.

Dependency scope is separate from knowledge value shape. Syntax trees, lexical
tokens, and locally declared symbols often have narrow content-scoped
dependencies; resolved imports, cross-file references, calls, inheritance,
test, documentation, and governance relationships often have broader ones.
These examples are explanatory rather than a fixed local/relational category:
future analyzers can become more precise without changing the architecture. The
architecture does not freeze `IntrinsicKnowledge` or `RelationalKnowledge` as categories:
“`foo.py` defines `Foo`” can be relational in value shape while depending only
on one resource. DerivedKnowledge may depend on other DerivedKnowledge.

Thus a B-content change can make B parsing inapplicable to a later state, then
affect B symbol knowledge and cross-resource relationships depending on it,
while unrelated A knowledge remains applicable. Dependency granularity may be
refined from resource/content to subjects, source occurrences, facts, graph
regions, or other structural units where its cost is justified by useful reuse
or avoided recomputation; coarser correct scopes remain valid. Incremental
parser edit history is likewise an optimization: its result remains attributable
to new content/state and identified derivation semantics, never snapshot
identity.

### Repository-relative conflict and source-role knowledge

Semantic conflict is defined by the relevant knowledge vocabulary, not by
matching predicate labels, arguments, or source strings. Two assertions conflict
only when their propositions are semantically comparable and incompatible under
compatible assumptions and scope. Conceptually, a family might define
`MUST_CALL(A, B)` and `CANNOT_CALL(A, B)` as incompatible despite different
predicate labels; two values of a functionally single-valued property might
conflict under the same scope; assertions under mutually exclusive
configurations might not conflict at all. These examples define no universal
predicates or conflict ontology.

An identified repository Derivation may establish reusable repository-relative
conflict, divergence, agreement, or consistency knowledge when its comparison
semantics, scope compatibility, dependencies, and coverage are explicit. For
example, a future derivation could establish a defined divergence between
accepted architecture and current implementation. Such a result can be
DerivedKnowledge. This does not create a universal conflict graph, mandatory
`CONFLICT` predicate, automatic pairwise conflict materialization, or truth-
arbitration engine. Purpose-relative judgment about which source to trust for a
particular task remains downstream under ADR-0004.

Repository intelligence may likewise establish source/resource role,
governance status, temporal status, location/identity, and semantic relationship
knowledge useful to downstream authority assessment. A role such as
implementation, test, configuration, documentation, accepted architecture,
experiment, or generated material can be DerivedKnowledge when an identified
Derivation establishes its repository-relative meaning. Roles can be multiple,
granularity-specific, ecosystem-specific, derived, or absent where irrelevant.
No mandatory `source_role` field on every ResourceOccurrence/RepositorySubject
and no closed universal source-role taxonomy is accepted.

### Two graph families

The architecture distinguishes two non-equivalent graph families.

The **derivation dependency graph** answers what knowledge depends on which
inputs or prior knowledge. It supports provenance, applicability assessment,
invalidation discovery, rederivation, and reuse:

```text
content -> parse knowledge -> symbol knowledge -> resolved-reference knowledge
```

This structure explains how knowledge was produced and its direct/transitive
semantic dependencies; it is not the repository semantic graph or a required
graph-store abstraction.

The **repository semantic/knowledge relationship graph** answers how resources,
subjects, source occurrences, and concepts relate. Eventual typed relationships may include
`DEFINES`, `REFERENCES`, `IMPORTS`, `CALLS`, `INHERITS`, `TESTS`/`EXERCISES`,
`DOCUMENTS`, `GOVERNS`, and change relationships. It supports repository
understanding, traversal, structural retrieval, impact analysis, and Context
discovery.

Those labels illustrate relationship families rather than asserting one
unqualified Boolean meaning. Each family's DerivationDefinition/result
vocabulary defines whether a relationship is definite, possible, necessary,
conservative, ambiguous, unresolved, scoped, or otherwise qualified.

These graphs are not one graph merely because both use edges. The derivation
dependency graph is not the repository semantic graph, and no universal
semantic repository graph is accepted. Neither family must share storage or use
a graph database. Semantic graph architecture is independent of physical
storage.

Relationships are DerivedKnowledge values: subject, typed predicate, object,
and relevant evidence/metadata. They do not need a separate foundational
`RelationshipId`; their derivation, dependencies, provenance, and reproducible
knowledge identity provide lineage. One universal canonical repository graph is
not accepted.

Multiple **typed graph views** are a first-class repository-intelligence
capability. A view is a reusable relational projection over selected node
identities and relationship semantics, not the semantic authority for those
relationships. Conceptual views can include containment, definition/reference,
import, call, inheritance, test, documentation, governance, or change
relationships; this is not a closed taxonomy or mandatory implementation list.
Graph views support deterministic repository navigation, multi-hop reasoning
outside the LLM, structural retrieval, change-impact reasoning, Context
efficiency, and future coding-agent repository understanding.

Graph infrastructure is distinct from relationship knowledge and graph-view
semantics. Where identities and relationship meanings are compatible, shared
mechanics may compose typed views for such work as adjacency lookup, bounded
traversal, reachability, or subgraph projection. It does not define what
`CALLS`, `IMPORTS`, `TESTS`, or another relationship means, require every view
to compose with every other, create a universal node ontology, or select a graph
API/query language. Cross-view traversal remains typed and bounded by allowed
relationship families, node compatibility, direction, depth, result/work limits,
and other purpose-derived constraints.

`GraphNode` is not RepositorySubject by definition. Each graph view chooses the
node domain appropriate to its semantics. Views should reuse
RepositorySubject or SourceOccurrence identity when those are the represented
things: a containment graph can connect subjects, a reference graph can connect
a SourceOccurrence to a RepositorySubject, and a call graph can connect
function/method subjects. A control- or data-flow graph may instead require
derivation-local basic-block, statement, or instruction nodes without promoting
them to global repository subjects. Containment is likewise typed relationship
knowledge, not a universal hierarchy encoded into subject identity; this admits
module/function, module/class/method, document/section, and workflow/job/step
structures without imposing one repository tree.

Graph maintenance follows the same DerivedKnowledge semantics and actual
dependencies. Applicable relationship results may be reused and other results
selectively rederived, with analyzer-specific projections maintained without
rebuilding every graph after every repository change. Some broadly useful
views may justify reusable materialization or incrementally maintained
adjacency/index structures; specialized or expensive analyses can remain lazy,
task-triggered, selectively materialized, cached, or incrementally maintained
where worthwhile. No eager/lazy policy, initial view sequence, graph algorithm,
storage/database technology, or materialization representation is selected.

A graph view can be an on-demand projection over relationship knowledge, a
reusable index/adjacency structure, or a persisted representation. These are
physical realization choices, not semantic authority: graph indexes, cached
neighborhoods, and materialized projections remain rebuildable views over
applicable relationship knowledge rather than an independent source of truth.
This decision does not choose separately maintained graphs, one unified typed
graph substrate, or relation/index structures with graph projections. Typed
relationship meaning, direction, provenance, qualification, applicability, and
view-specific node domains are the accepted semantic commitment; topology is a
derived operational view unless a future consumer establishes a stronger
representation requirement.

Repository intelligence defines no foundational universal `Chunk`. Fixed token
windows, arbitrary line chunks, syntax-aware slices, graph neighborhoods,
subject combinations, and other bounded units can be useful downstream for
retrieval or disclosure, but do not define repository identity. They may be
constructed dynamically without becoming subjects.

The resulting boundary is conceptual rather than a required class diagram:

```text
Repository -> RepositorySnapshot -> ResourceOccurrence -> SourceOccurrence
ResourceOccurrence -> ContentIdentity
analysis/derivation may establish RepositorySubject

identified dependencies -> Derivation -> DerivedKnowledge
```

Subjects and source occurrences can be dependencies, referents, provenance
anchors, or values in DerivedKnowledge. Repository intelligence supplies that
reusable knowledge downstream; ADR-0003 owns purpose-relative discovery and
RelevanceEvidence, while ADR-0004 owns purpose-relative disclosure composition
and representation. This is not a containment pipeline.

### Repository intelligence and Context

Repository intelligence produces deterministic knowledge independently of an
LLM. Context is purpose-relative selection, transformation, representation,
and model/task disclosure of relevant information. Retrieval produces evidence
for possible relevance; ranking is not repository truth and remains distinct
from final selection; Context compilation remains distinct from retrieval.

Context preparation can perform a purpose-relative epistemic synthesis without
making the result repository DerivedKnowledge. Such synthesis remains explicit
about origin and support and preserves assumptions, uncertainty, conflicts, and
purpose-relative status where material to correct interpretation. ADR-0004 owns
its planning, realization, and disclosure semantics. Repository intelligence
continues to own reusable repository-relative assertions established by
identified Derivations.

Future mechanisms may combine exact/identifier, lexical, structural,
relationship/graph, optional semantic, and historical/change-based retrieval.
They may preserve multiple relevance signals, use task-sensitive deterministic
or learned ranking, and select representations such as whole files, source
regions, symbols, or document sections. Deduplication, overlap, diversity,
ordering, budgeting, provenance-bearing disclosure, disclosure history, and
reuse remain necessary pressure, not selected mechanisms.

Repository-derived model content is untrusted data, not policy, instruction, or
execution authority. Progressive disclosure may provide high-confidence initial
orientation, accept bounded requests for more information, and compile targeted
follow-up Context without forcing topology rediscovery. A model request remains
descriptive: materialization, validation, authorization, and execution remain
outside the model call. Repeated compilation does not make a compiler an
orchestration loop; orchestration remains above deterministic retrieval and
Context compilation.

Evaluation pressure includes retrieval/context quality, calls, input/output/
total tokens, repository operations and repeated reads, task success,
iterations, elapsed time, and cost. The intended long-term outcome is reduced
expensive-model repository archaeology, progressively reduced Codex dependence,
and eventually local Qwen-family models capable of primary or sole coding-work
roles. No metric, harness, model policy, or worker loop is selected here.

RepositorySnapshot identity is not the whole identity of an evaluated
repository-intelligence condition. Two evaluations can share repository state
while differing in consumed external semantic inputs, derivation/analyzer
semantics, available knowledge or graph views, semantic-result coverage, or
maintenance/reuse state relevant to the experiment. Evaluation must retain the
actual relevant basis for its claim. This does not introduce a universal
`RepositoryIntelligenceSnapshot`, `KnowledgeClosure`, or `IntelligenceClosure`.

### Identity taxonomy

| Concept | Accepted semantic identity |
|---|---|
| Repository | Nominal logical identity across changing states. |
| RepositorySnapshot | Immutable, logically complete successfully observed state under explicit snapshot/observation semantics. |
| SnapshotDelta | Difference relationship between snapshots, not repository state or identity. |
| IncrementalMaintenance | Process for efficiently establishing applicable intelligence; not snapshot state. |
| Resource occurrence | Contextual snapshot plus repository-relative address. |
| Content | Content-derived identity reusable for identical content. |
| Source occurrence | Snapshot-local source anchor/address within a ResourceOccurrence; not automatically a subject. |
| RepositorySubject | Snapshot-local structural/semantic referent about which repository intelligence can make assertions. |
| DerivationDefinition | Semantic identity of reusable computation, not necessarily implementation binding. |
| Derivation | Semantic application of a definition to direct semantic dependencies. |
| DerivationExecution | Particular realization attempt, distinct from derivation and knowledge. |
| DerivedKnowledge | Immutable repository-relative semantic result whose qualified proposition is defined by its DerivationDefinition/result vocabulary; reproducible identity is tied to derivation/dependencies/result semantics. |
| Relationship | DerivedKnowledge value shape, not an independent foundational identity. |

## Decision consequences

| Change | Required consequence |
|---|---|
| Edit content | New snapshot and changed-content identity; knowledge whose dependencies changed may not apply to the later state while unrelated knowledge can remain applicable. |
| Move/rename unchanged content | New snapshot and occurrence/address; same content identity and potentially reusable content-local knowledge. Rename continuity remains derived. |
| Copy unchanged content | Distinct occurrences may refer to one content identity. |
| Delete | The new snapshot lacks the occurrence; globally retained knowledge of its content need not be destroyed. |
| Git branch/checkout change | New snapshot; unchanged content knowledge may still be reusable. |
| Parser/analyzer semantic upgrade | Snapshot can remain identical; incompatible definition/derivation semantics make affected knowledge inapplicable until rederived. |
| Ranking-policy change | Repository knowledge remains applicable unless it explicitly depends on ranking. |
| Cross-resource resolution | A B change need not affect A local parse/symbol applicability, but can affect relationship knowledge depending on B. |

## Deferred and open pressure

This ADR intentionally leaves open: SubjectId and SubjectKind representation;
subject locators, fingerprints, matching, and cross-snapshot continuity
algorithms; snapshot data model, policy API, observation protocol, retry/
quiescence/consistency mechanics, and policy-to-state-identity relationship;
hash/digest and Merkle/flat identity construction; raw-versus-normalized
ContentIdentity semantics; ignored/generated files, binaries, symlinks,
submodules, multiple roots, and filesystem race/atomicity semantics;
SnapshotDelta model/persistence, watcher implementation, snapshot retention/
eviction, persistence, cache, serialization, derivation-dependency storage,
reverse dependency indexes, invalidation algorithms, maintenance engine/
scheduler, eager-versus-lazy maintenance, graph storage, cross-repository
content reuse, and concrete external/environment-dependent derivation semantics,
including dependency value/reference/constraint representation, observation,
domain identity/equality/equivalence/compatibility, generated resources,
retention, and replay strength; parser/analyzer
technology, incremental parsing, and analyzer/plugin APIs; concrete
DerivationDefinition/Derivation/DerivedKnowledge models and identities,
result-vocabulary/qualification and assumptions/scope representation,
dependency-role/referent and provenance schemas, definition compatibility/
versioning, applicability algorithms/APIs, semantic-result coverage,
result grouping/cardinality and exhaustive-coverage representation,
partial-result publication, execution/Attempt/Evidence integration,
implementation bindings, capability registration,
catalog/discovery, selection, lifecycle, admission, dependency-provider and
execution-context APIs, dynamic dependency tracking, static declaration format,
process/subprocess/native execution, governance reuse, evidence schema, result
publication, partial-result transaction semantics, and package ownership;
specialized confidence/probability evidence for knowledge families that define
such quantities; conflict/divergence detection and source-role analyzers/
taxonomies where useful; lexical choices such as grep/BM25/trigram; embeddings,
vector storage, graph algorithms, learned ranking, task-sensitive strategy
selection, call graphs, historical co-change, change impact, test/code,
documentation/code, and ADR/governance relationships; disclosure-history and
Context caching ownership; progressive-acquisition orchestration; and evaluation
infrastructure and exact metrics.

It also leaves open whether and under what evidence learned, model-assisted, or
validated interpretive assertions can become reusable repository intelligence;
their validation, qualification, promotion, identity, persistence, caching, and
governance semantics; and any future concrete representation of uncertainty,
semantic-result coverage/completeness, conflict, source role, or authority
beyond the distinctions accepted here.

## Status and implementation boundary

This decision settles semantic architecture only. It does not claim that any
new production types, protocols, RepositorySubject/SourceOccurrence models,
DerivationDefinition/Derivation/DerivedKnowledge models, execution bindings,
capability protocols/registries/schedulers/dependency providers, indexes,
parsers, graph views, persistence,
retrieval, ranking, Context compiler, Tool, Agent, Runtime loop, or evaluation
system exists. B-0002 retains the unimplemented repository-intelligence and
coding-Context pressure. B-0008 is superseded as the earlier narrow
root-navigation investigation whose semantic question is now answered here.
