# Architecture Adversarial Review: Repository Intelligence and Context

## Disposition

Status: Partially reconciled

Canonical research subject: Adversarial review of repository intelligence and Context architecture.

Related ADRs: ADR-0002; ADR-0003; ADR-0004.

Implemented evidence: bounded repository observation, lexical retrieval, and deterministic evaluation.

Accepted: repository identity, qualification, provenance discipline, and retrieval/disclosure separation.

Deferred: learned retrieval, progressive disclosure mechanisms, and incremental maintenance.

Rejected for now: model output as repository knowledge, universal graph/store, and premature planning/evidence abstractions.

Superseded or refined findings: later ADRs retain anti-premature-abstraction criticism without collapsing purpose and retrieval distinctions.

Open questions: empirical value of future retrieval and disclosure mechanisms.

Revisit triggers: independently evaluated bounded mechanisms needing stronger reusable semantics.

Reconciliation basis: ADR-0002 through ADR-0004; Increment 16 and Increment 20 experiments.

## A. Executive verdict

The Devtools architecture reflects a bold and richly detailed approach to coding‐agent infrastructure. Many of its *principles* align with best practices in build and code-analysis systems: for example, using content-addressable snapshots and caches for correctness (as in Bazel and OSTree) and leveraging semantic dependencies for incremental recomputation (as in Salsa). However, the architecture also introduces a profusion of abstractions whose net benefit is unclear. In particular, the insistence on persisting *all* new knowledge (including LLM-generated synthesis) with rigid provenance and authority layering seems at odds with observed agent workflows. Strong evidence from retrieval and LLM evaluation suggests that simpler pragmatic systems—e.g. combining lexical and dense search with rank fusion and using RAG rather than brute-force long contexts—often suffice.

Our adversarial review finds that **core architectural assumptions survive serious scrutiny only when they match documented practices**: content-addressable repository snapshots, precomputed code indexes (LSIF), unified code graphs (Kythe), and incremental analyzers (Salsa). In contrast, the *novel* layers (InformationNeed planning, Disclosure planning, forcing all LLM output into DerivedKnowledge, etc.) have little external backing. Some can be simplified or deferred. The recommended outcome is a **tighter, more incremental architecture** that retains reproducibility and caching but avoids undue complexity in planning and provenance.

# B. Research methodology and evidence quality

We examined a range of sources: **academic literature** (incremental computation and retrieval research), **technical documentation** (Bazel, LSIF, Kythe), **system descriptions** (code search benchmarks, GitHub projects), and **experiential reports** (blogs on RAG and retrieval). Key references include Google’s Bazel and OSTree integration for snapshots and caching; the Salsa framework for incremental analysis; Sourcegraph/LSIF for persisted code indexing; and retrieval benchmarks (e.g. CodeSearchNet) showing BM25 and hybrid methods outperform naive approaches. We also considered latest findings on LLM context handling. Most evidence comes from **first-party engineering sources** and peer-reviewed venues, with additional insights from blog posts and technical talks (marked accordingly). Where practical systems’ internals are undocumented (e.g. Copilot/Cody), we only infer plausible patterns without strong claims.

# C. Architecture reconstructed

The provided architecture treats **repository understanding as layered data infrastructure**. It separates the static repository state (files, commits) from derived, deterministic intelligence (indexing and analysis results). Core concepts include:

- **Repository vs RepositorySnapshot vs SnapshotDelta:** A “Repository” is the project; a “RepositorySnapshot” is an immutable view (akin to a Git commit or Merkle tree); “SnapshotDelta” captures changes.
- **ResourceOccurrence / ContentIdentity:** Individual files or code fragments (“ResourceOccurrence”) have immutable identities based on content hashes rather than paths.
- **RepositorySubject / SourceOccurrence:** Code symbols (functions, classes) are identified per-snapshot (“RepositorySubject”) and their specific occurrences (“SourceOccurrence”). Identities live locally to snapshots; matching across versions is derived knowledge.
- **DerivationDefinition / Derivation / DerivationExecution / DerivedKnowledge:** Analysis tasks (DerivationDefinitions) are abstract computations (e.g. “build call graph”); DerivationExecutions bind a definition to a code snapshot and produce DerivedKnowledge facts (immutable analysis results) or failure.
- **InformationNeed → RetrievalEvidence → Ranking → DisclosurePlan → ContextDisclosure:** A *purpose* (task or query) induces an InformationNeed. The system formulates retrieval queries, gathers raw evidence (scores from multiple search strategies), then applies a ranker to order items. A DisclosurePlanner then selects a subset of evidence to include (optimizing coverage/diversity). This plan is materialized into a ContextDisclosure (specific content pieces) and assembled (with model-specific formatting) into the final prompt/context. Throughout, provenance and “authority” tags track origins and trustworthiness of content.

In sum, the architecture envisions **fine-grained provenance and modular stages** for all steps: from tracking file state to decomposing tasks, fetching and evaluating evidence, assembling context, and even logging model queries.

# D. Strongest properties

The following architectural distinctions are well supported by external evidence:

- **Immutable content-addressable snapshots:** Treating repository state via content hashes aligns with practiced build systems. For example, OSTree and Bazel identify whole directories or build targets by a single SHA hash of contents, ensuring reproducibility and correct invalidation. Bazel’s cache is keyed by input hashes. These systems show that content-derived snapshot identity and fine-grained dependency tracking work in large codebases.
- **Incremental recomputation via semantic dependencies:** The idea that only semantically affected analyses are redone finds support in *self-adjusting computation*. Salsa (used in rust-analyzer) tracks precisely which inputs a derivation depends on, reusing any derived values unlinked from changes. This provides the same end results as a full recompute, with higher efficiency.
- **Precomputed code intelligence index:** Persisting analysis output (as LSIF does) greatly speeds up IDE queries. LSIF documentation emphasizes that precomputing all navigational info yields fast, precise code browsing: “It’s fast because all of the information is precomputed; it’s precise because the information comes from an environment which understands the code”. This validates separating code intelligence generation (offline) from agent prompt-time retrieval.
- **Unified code graph substrate:** Kythe’s approach suggests one extensible graph to capture code semantics. Kythe defines a language-agnostic graph containing definitions, references, types, and build metadata. Its hub-and-spoke model has reduced integration cost in practice. A shared graph avoids fragmented views and aligns with the goal of cross-language tooling, supporting the idea of common identity domains and interconnection of analysis results.
- **Hybrid retrieval effectiveness:** Information retrieval studies show that combining lexical and semantic techniques is more effective than either alone. In fact, BM25 with clever tokenization can outpace some neural models, and an ensemble (e.g. reciprocal rank fusion) adds further boost. This supports the architecture’s idea of multi-strategy retrieval and fusing evidence.
- **Planned context assembly needed:** Recent LLM experiments (e.g. 1M token RAG vs long-context) confirm that mere stuffing of large contexts is inefficient and error-prone. Separating *what* information is relevant (ranking/selection) from *how* to format it (assembly) is prudent: heavy experiments show that RAG pipelines vastly outperform brute long-context approaches. Moreover, “lost-in-the-middle” studies show that LLMs often ignore information placed deep in context, which motivates careful ordering and possible summarization–consistent with having a dedicated assembly policy.

In summary, the architecture’s focus on **reproducibility, caching, semantic dependency tracking, and evidence combination** matches proven techniques (Bazel/OSTree for content identity; Salsa for incremental updates; LSIF/Kythe for structured code knowledge; and hybrid IR). These form the well-founded core of the design.

# E. Foundational defects

Certain architectural assumptions appear problematic:

1. **LLM-generated knowledge as authoritative DerivedKnowledge:** The rule “LLM-synthesized assertions become provenance-tracked DerivedKnowledge” lacks basis. Modern RAG and evaluation frameworks *do not* treat model outputs as ground truth. Instead, they emphasize verifying or quoting model claims against source documents. Forcing all synthesis into the “deterministic intelligence” layer risks polluting it with hallucinations. This conflates heuristic output with authoritative data, undermining the reproducibility claim. (Supporting this, works like ALCE and RAGChecker focus on citation and faithfulness of outputs, not on adding them to the knowledge base.) **(Foundational defect)**

2. **Explicit InformationNeed abstraction:** The “InformationNeed” separate from a query or prompt is untested. In IR, the user’s *true* need (intent) is indeed a distinct concept, but systems usually operate directly on the user’s query text. The architecture assumes a stable, purpose-driven need can be formalized upfront. However, practice shows needs evolve during reasoning (e.g. iterative queries), and capturing them in advance may add little. Without evidence that crafting this separate object improves retrieval or planning (and given extra overhead), it may be unnecessary. **(Simplification opportunity or open)**

3. **Ambiguous authority model:** The claim that authority should be “purpose-relative” rather than a fixed source hierarchy raises questions. For code, generally the source code itself is king; comments or ADRs might add context but seldom override code semantics. The architecture’s model to flexibly rank sources depending on query intent has no clear analogue in existing systems. It risks becoming subjective or ad-hoc. No evidence shows that a dynamic, need-based authority ordering produces better answers than simply preferring the codebase itself. This complex layer is largely unvalidated. **(Evaluation requirement / unsupported criticism)**

4. **Fine-grained provenance explosion:** By introducing provenance at every stage (query plan, retrieval evidence, disclosure plan, etc.), the system may produce an unmanageable quantity of metadata. Real-world systems (search engines, RAG) seldom track provenance beyond source citation and final answer confidence. The added complexity here could harm performance without clear benefit. This is a *design pressure* rather than an established fault; it might be relaxed if implementation shows it's too heavy. **(Simplification opportunity / open design)**

5. **Neglect of workspace state:** The architecture assumes work against immutable snapshots. In practice, coding agents often deal with the **in-memory or unsaved workspace**. Changes not committed to a snapshot won’t be tracked, possibly missing critical context (e.g. local edits). This is a missing consideration; many tools (LSPs) do track open buffers as separate “dirty” state. **(Missing foundation)**

Each of these points suggests caution. In particular, collapsing “LLM facts” into the knowledge graph is a *foundational flaw*, while others may be simplified or earmarked for later evaluation.

# F. Substantive improvements

Based on evidence, we recommend several architecture tweaks **before** implementation:

- **Collapse derivation concepts:** The four-layer `DerivationDefinition → Derivation → DerivationExecution → DerivedKnowledge` may be overkill. In practice (e.g. make/Bazel) a build rule definition and its execution are not maintained separately: the action and its result are bound. We can merge *DerivationDefinition* and *Derivation* into one: a named analysis task. The execution instance (with its parameters) directly produces DerivedKnowledge facts (or errors). This streamlines identity management. (Effect: less bookkeeping; risk: lose abstract def semantics, but likely okay.) **(MODIFY before implementation)**

- **Use global symbol identity:** Rather than local `RepositorySubject`, adopt a stable symbol ID scheme. For example, Kythe uses a canonical VName (vocabulary-defined node ID) to track entities across builds. If a function has the same package path and name in two commits, it should share an ID (unless the code diverged semantically). This avoids complex “DerivedKnowledge continuity” matching. (Effect: simplifies cross-snapshot linking; cost: must design stable ID format.) **(MODIFY)**

- **Simplify retrieval/evidence layers:** Instead of separate *RelevanceEvidence* objects per retriever, treat combined retriever scores as features in one ranking step. Modern search/ML systems typically fuse signals internally (e.g. rankers that take BM25 score + embedding similarity as features). We can collapse *RelevanceEvidence + Ranker* into a single **Retrieval/Rerank** component. (Effect: fewer artifacts to manage; evidence features can be logged but need not be first-class objects.) **(MODIFY)**

- **Simplify disclosure planning:** Instead of a complex planning stage, use established diversification algorithms (e.g. maximal marginal relevance) directly on ranked candidates. For example, MMR requires no separate symbolic plan object. A more pragmatic strategy: take top-N results, then apply a lightweight filter for redundancy. (Evidence: diversified retrieval literature; [74] used cluster panels but no explicit plan object.) If coverage semantics are needed, a simple heuristic (e.g. ensure at most one snippet per file or one per topic cluster) might suffice. Complex plans with DAGs seem unjustified at start. **(MODIFY)**

- **Defer authority mechanics:** The current plan embeds an authority layer. We suggest treating all sources equally at first: rank by relevance, then only consider special authority rules if conflicts appear (e.g. if code vs. test disagree, trust code). This can be an implementation setting rather than a core data model. **(DEFER)**

- **Treat context assembly as model-specific formatting:** Instead of one “ContextDisclosure” artifact, reserve it for the final assembly to the model. The planner can output selected texts; assembling (prompt templates, order) can be done with little architecture overhead. This prevents premature formalism around plan vs realized content. **(COLLAPSE)**

These changes keep all core goals (caching, correctness, evidence) while trimming layers. For each modification, we ensure preserving reproducibility or allowing easy extension (e.g. we still record where info came from, even if not as a separate object, for auditing).

# G. Simplification opportunities

Several distinctions appear implementable with less ceremony:

- **InformationNeed** can be collapsed with **Task/Query**. In effect, each agent prompt inherently *is* an information need. Instead of a separate immutable structure, the query text plus any context (e.g. function name, code) can serve. Many systems directly index on query terms; IR theory recognizes “need” but doesn’t instantiate it as a data object. Removing InformationNeed saves layers and mirrors search engines.

- **RelevanceEvidence as objects:** We can drop dedicated evidence entities. Instead, collect raw features (scores, retriever IDs) transiently. If persistent logs are needed, simple tuples (query ID, source ID, features) suffice. This avoids propagating evidence through multiple layers.

- **DisclosurePlan vs ContextDisclosure:** We can remove the Plan object entirely. After ranking, just select top elements via a heuristic and pass them to assembly (ContextDisclosure). The concept of a separate plan only adds overhead. (Production RAG systems typically iterate retrieval results and build the prompt on the fly.)

- **DerivedDisclosure for synthesised content:** If any synthesis from the model is to be recorded, do so at ContextDisclosure time or just as part of final answer logs. Having a semantic “DerivedDisclosure” separate from DerivedKnowledge is unnecessary. (We recommend treating LLM outputs either as part of the final response or as provisional notes, not as peer to static knowledge.)

- **Cache/store identity unification:** Instead of unbounded separate identities (e.g. Chunk vs GraphNode), use a single content address for any code fragment (e.g. file path + range hashed). If a graph needs nodes, create them on demand from this ID. A universal content-ID (like Kythe’s VName scheme) could underlie everything.

These collapses reduce “some 60–80%” of the artifact types. The remaining machinery still supports incremental reuse, provenance, and evaluation. We expect minimal loss: e.g. dropping InformationNeed doesn’t impede retrieval beyond how queries are constructed, and merging plan stages doesn’t remove any actual data (just how it’s tracked).

# H. Missing foundations

Evidence suggests a few important aspects are absent:

- **Build/environment identity:** Real code analysis depends on compiler/toolchain versions and settings. LSIF emphasizes running in CI environments, implying analysis results are environment-bound. The architecture should incorporate *which* build/config was used as part of identity (e.g. include compiler version or build flags in RepositorySnapshot or DerivedKnowledge provenance). Otherwise, analyses may be wrong or unreproducible under different setups.

- **Workspace vs committed state:** Developers often have unsaved or uncommitted changes. The architecture implicitly assumes working with snapshots only. A missing concept is the “current workspace”—the live file contents in the editor (perhaps in-memory). Ideally the system should accept ephemeral diffs or not-yet-committed changes, perhaps modeling them as a special snapshot layer. Without this, the agent may miss bugs or facts known only in recent edits.

- **Dependency sources:** Code rarely stands alone; it imports libraries. The arch now treats the repository itself as authoritative context. It should consider external dependencies (package repos, standard libraries) as additional Subjects or snapshots. These could be modeled as read-only “sub-repositories” with their own identity (e.g. a Maven artifact version). This is foundational for correctness in many languages.

- **Tool outputs:** Generated code (e.g. from protobufs, serializers) may not have hand-authored source. The arch should clarify whether generated artifacts count as RepositorySubjects or require separate handling. Current model lacks a concept of “generated” vs “source” and might incorrectly treat them as stable subjects.

- **Incomplete or heuristic analysis:** For some languages, complete analysis is impossible (e.g. dynamic languages, macros). The architecture seems to assume deterministic, exact analysis results. A missing notion is one for *uncertain or partial facts* (e.g. “type of X is likely Y”). Without modeling uncertainty, the system might treat heuristic inferences as solid, risking errors. Some guidance could be gleaned from RAG evaluation: partial data is better than none (Kythe principle). The architecture should allow “best effort” knowledge when full determination is infeasible.

- **Actor identity and security:** Not considered: if coding is collaborative, who provided an ADR or comment? Are some sources privileged? A minimal model for user roles or trust levels could be needed, especially if exposing “authority” differences.

Addressing these would involve adding, for example: *BuildConfig* attached to snapshots; a way to ingest uncommitted changes; references to external repo snapshots; marking facts as heuristic vs proven; and a security label on provenance.

# I. RepositorySnapshot and state consistency

**Immutable snapshot abstraction:** Evidence from content-addressable systems strongly supports treating snapshots as immutable, content-defined trees. OSTree+Ninja shows storing each directory as a Merkle tree file (with a SHA hash) allows global identification by a single hash. Bazel likewise hashes inputs, not commit IDs. Thus, using a complete immutable snapshot as the foundation is sound. It gives clean dependency granularity: any unchanged files lead to identical tree hashes, enabling reuse.

**Stronger than necessary?** Possibly: for many tasks, capturing only touched files with fine-grained keys (as in Bazel’s rule caching) could suffice. But full snapshots simplify correctness: no risk of missing hidden dependencies. The cost is more storage and potential waste. Some systems (like Shake) compute per-file caches rather than full trees. If performance is critical, one could allow storing just changed subtrees and reassemble as needed, mimicking persistent data structures. However, current evidence favors the robust content-hash snapshot approach for its simplicity and safety.

**Consistency and race conditions:** Practical systems assume exclusive control or checksums. For example, build systems typically freeze source directories (or trust users). If files change mid-indexing, content-addressing will see a changed hash, just marking everything dirty; that's safe (it may rebuild unnecessarily, but never silently use wrong data). To handle OS-level races, one could incorporate file modification timestamps or locks, but that’s usually an implementation detail. Strict MVCC (snapshot isolation) of the working dir would prevent races, but is complex. In practice, the system can snapshot by copying or by using version-control commit points. We should at least require that analyses run on clean working trees (maybe fail if dirty).

**Git vs content identity:** Should Git commit IDs be primary? Evidence suggests no. A Git SHA changes if *any* file changes, invalidating all. Using Git ID loses fine granularity. Conversely, content-address allows structural sharing (identical files across branches share hashes). Bazel’s success implies content identity works in practice. The architecture’s choice to let snapshot identity be content-derived (not Git) is justified by these systems.

**Observation semantics:** File-watcher events (filesystem notifications) can hint at changes, but are not canonical truth (files could have changed between events). The build example shows that using content hashes as a check is deterministic. File-system events can be used to schedule re-analysis, but final invalidation should still compare content hash.

**Structural sharing:** Merkle-tree storage (OSTree) achieves sharing: identical files across snapshots are stored once. We should adopt a similar CAS store so snapshots are space-efficient. It’s practical (many modern systems like Git/LFS do it).

**Consistency guarantees:** Practically, we can guarantee deterministic snapshots at the moment of capture (like Git commit). True concurrent writes would need locking. But content-based checks give a clear notion of change.

**Alternative abstractions:** Unlike DB MVCC, code isn’t transactional; but we can view each snapshot as a transaction. Some build tools (Nix) treat the environment and inputs purely functionally. The current abstraction essentially *is* a Merkle transactional view. No better-known abstraction stands out. It’s stronger than a dirty-flag model (Make), and aligns with hermetic builds.

**Conclusion:** The immutable, content-addressed snapshot is appropriate (strong, but practical). We should encode it explicitly. Observation semantics (file events) are just triggers, not authoritative. No evidence of a simpler but equally correct abstraction was found, so we keep this foundation.

# J. RepositorySubject and identity

**Snapshot-local vs stable subject IDs:** The architecture makes symbols (functions, classes, etc.) local to each snapshot. In practice, however, systems often try to assign stable IDs for symbols across versions. For example, Kythe uses *VNames* to give each entity a canonical multi-part name, which persists across analyses. Similarly, LSIF’s monikers help link a symbol between repositories or versions. There is precedent for wanting stable identity: without it, an intelligent agent can’t easily carry over a known function’s documentation from one version to the next. On the other hand, ensuring true stability is difficult if code changes. Many IRs (like CodeQL) identify symbols by a combination of file path, name, and context; if any changes, the ID shifts.

**Utility of snapshot-local identity:** The architecture’s choice (subject ID only valid within one snapshot) simplifies the model but forces expensive matching logic to carry knowledge forward. SALSA-like systems, for instance, assume queries are for specific revision. If we adopt snapshot-local IDs, we must rely on *DerivedKnowledge* to link across versions (which the architecture does). This is workable but complex.

**Compiler/IDE practices:** Traditional IDE indexes (and LSP-based tools) usually consider symbols continuously; e.g., an IDE “Go to Definition” persists names as you edit. Persistence is done by updating an in-memory symbol table, effectively giving stable IDs in practice (though often by file+name). Static index formats (LSIF/SCIP) put symbol names as part of the index so that updates can reuse them. Kythe’s “vname” approach explicitly intends stability (via URI-like naming).

**SourceOccurrence vs RepositorySubject:** The architecture differentiates a subject (an abstract symbol) from each place it occurs. In practice, most systems tie usage data to the symbol’s definition ID; occurrences are just edges in a graph. This distinction seems fine—happens naturally in any AST index. It’s not a burden.

**GraphNode vs Subject:** The text hints that not all graph nodes are subjects (e.g. call edges vs classes). In Kythe’s graph model, everything (symbols, files, edges) is nodes and edges. It may be simpler to *not* mix Subject with graph internals: either treat all content elements as nodes in one unified graph, or reserve “Subject” for symbol definitions only. But there's no strong harm in having multiple node types as long as identities are consistent.

**Conclusion:** A fully stable symbol identity across versions (like Kythe VNames) is preferable to purely snapshot-local IDs. We should consider adding a persistent identifier scheme (perhaps content-hash of the symbol signature and context) to represent symbols. The current design’s reliance on DerivedKnowledge to infer continuity is powerful but risks matching errors; a direct id scheme (even if best-effort) could simplify reuse. At minimum, we should ensure symbol identities in sequential snapshots are aligned (maybe require analyzers to preserve IDs when definitions carry over). This change improves practicality and matches industrial practices (marked as **MODIFY**). The SourceOccurrence concept is fine, and keeping graph nodes distinct from subject simplifies conceptual integrity.

# K. Derivation / DerivedKnowledge

The four-concept hierarchy (`DerivationDefinition`, `Derivation`, `DerivationExecution`, `DerivedKnowledge`) is quite elaborate. In essence, it models a pipeline: a *definition* (like “build class hierarchy”) has (possibly multiple) *implementations*; each execution of such a derivation on a snapshot yields zero or more results (facts).

**Necessity of all four:** Many systems collapse these layers. For example, a makefile’s rule is both a definition and its only execution model; there’s rarely a need to refer to a rule separate from its implementation. Likewise, once defined, the *result* of a derivation is what we care about (e.g. “the call graph”). We might safely merge *Definition* and *Execution* concepts: treat each analysis task (Definition) as identifiable, and each run producing results (no separate Execution object needed, just a timestamp or key if needed).

**0..N result sets vs manifest:** The design says a DerivationExecution produces *N* facts. An alternative is to have Derivation produce a single manifest of results (like a file or archive). Systems like Bazel treat the output of a build rule as one artifact (though conceptually it can be multiple files). For analysis, one could emit a file (e.g. “all-types.json”) rather than many small facts. Whether this matters depends on how facts are used. Using a single manifest is simpler to manage (one provenance marker) but less flexible for partial reuse. Given that, keeping results as separate facts (entries in a database) seems acceptable, but we should consider grouping them under an “artifact”.

**Negative knowledge vs failure:** If an analyzer fails (e.g. a parse error), should that yield negative facts or just an error? The architecture separates execution failure from “negative knowledge”. In practice, failed analysis usually just drops results and maybe logs an error. There’s no strong use case for storing “all functions have unknown types.” I’d lean that failures should invalidate dependent results and request manual intervention, not populate the DB with negatives. That detail is more implementation than architecture.

**Multiple implementations:** Allowing one Definition realized by different tools (e.g. two parsers) is theoretically fine. In code indexing, this happens: one might merge Info from clang and from a secondary tool. But it complicates consistency. Probably rare enough to postpone multi-implementer support. At least require all implementations to share the same output schema.

**Provenance vs compatibility:** The architecture suggests explicitly tracking which implementation (tool version) produced each DerivedKnowledge. That’s wise: like how Bazel records which compiler produced an object. We should do that. If two tools claim to implement the same definition, their compatibility would need evidence (testing or specification) – a lot of complexity. For now, treat them distinctly and do not assume interoperability.

**Coverage and partial publication:** For exhaustive analyses (e.g. “list all references”), we want an all-or-nothing guarantee. Otherwise, incremental results could mislead. We recommend:
- For completeness, a derivation should ideally declare when it has covered all necessary inputs (and maybe skip being “partial”).
- If partial results are acceptable, they must be flagged as such. The architecture’s model of “0..N results, labeled by provenance” allows storing partial subsets anyway.

**Immutable facts:** DerivedKnowledge is immutable once created (like content hash). This makes sense for caching and reproducibility. Systems like Salsa cache query results indefinitely. We just need a versioning scheme: if code changes, new facts appear and old ones get pruned. (Kythe indexes are typically immutable snapshots too.)

**Resource-by-resource vs global results:** One improvement might be to tie results to specific code resources (e.g. per-file), so that if one file changes, only that file’s analyses refresh (instead of rerunning whole-project queries). This is how many static analysis DBs work (one table per file). The architecture seems flexible enough for this (by scoping inputs), and indeed Bazel’s model does this with file-level caching. This might reduce recalculation cost.

**Conclusion:** All four terms may be over-architected. We propose merging *DerivationDefinition+Derivation* and treating each execution as simply “running this definition with these inputs”. Whether results are “0..N” facts or a single composite object is a detail; we can keep them as individual facts with a common origin ID. We should definitely version/analyze per resource to limit recompute (supported by Bazel’s partial builds). This simplification retains provenance (definition ID + implementation version) for each fact. In summary, collapse some layers (especially *Definition vs Execution*), but keep the idea that derived facts are immutable and labeled by the derivation recipe. **(SIMPLIFICATION OPPORTUNITY)**

# L. Applicability and incremental maintenance

The architecture’s standout claim is that **DerivedKnowledge should remain valid across snapshots based on *actual semantic dependencies*, not just a brute “dirty/clean” per file flag**. This is effectively treating code analysis like an incremental compiler (e.g. Salsa or Bazel): only recompute facts if something they depend on changed.

**Can actual dependencies be captured?** Static analyzers can often record which symbols or files each fact depends on. For instance, a type derivation depends on specific input files or AST nodes. In practice, tools like Salsa do exactly that. Bazel captures file-level dependencies. If the architecture’s analyzers annotate dependencies, then in principle we can reuse unaffected facts.

**Risk of incomplete dependency discovery:** Dynamic language features or reflection can break this: e.g. if a Python module uses `import_module(name)` where `name` is computed, static analysis may miss a dependency. Then our cache might incorrectly reuse stale info. This is a known issue in build systems (“hidden dependencies”). Bazel addresses this by requiring manual listing or re-running all inputs in uncertain cases. The architecture should anticipate that some dependencies can be dynamic; in those cases, safer to fall back on simpler heuristics (like invalidating whole module). This falls under *evaluation requirement*: one must check for such coverage gaps in implementation.

**Toolchain/config dependencies:** If code analysis depends on compiler flags or interpreter version, then knowledge is only applicable under the same environment. We must record these as explicit dependencies or part of definition identity. For example, if building C with flags, store the flags in the derivation’s identity. Without this, facts might be misapplied across environments. The architecture should extend “semantic dependencies” to include these environmental factors.

**Applicability propagation:** In an incremental graph, if fact A depends on B and B changed, A must also recompute (like topological invalidation). We should follow standard incremental models: when an input changes, mark dependents dirty and so on. This is exactly how Salsa and incremental compilers work. There’s no evidence of a better abstraction for this in coding context. The architecture can adopt a lazily-computed dependency graph (like Celery build or Salsa’s query graph).

**Binary/conditional applicability:** Likely we treat a fact as either valid or not. Attempting to carry probabilities (confidence) is theoretically possible but no evidence that simple static analyses quantify uncertainty well (and complicates caching). Instead, errs on safe: if unsure, invalidate.

**Global vs local analyses:** Some analyses (e.g. whole-program optimizations or cross-module refactoring metrics) inherently see the entire code. These produce results that effectively depend on the whole snapshot. Our model can express that: a “global derivation” that takes all files as input will always recompute on any change. That’s fine – just treat it as a single large derivation (like Babel AST parse for whole project).

**When recompute is cheaper than analysis:** If dependency tracking overhead or analysis complexity is lower by brute force, one might bypass caching. For example, re-parsing a small repo may be faster than managing fine-grained invalidation. The architecture should allow flexible caching (a small repo strategy vs big repo strategy).

**Dirty/clean flags:** Even if we avoid persistent mutable state, we may still record that “DerivedKnowledge X is dirty” until it’s refreshed. Implementation-wise, this is needed. The architecture’s notion of cached immutable knowledge implies a new snapshot creates new caches rather than overwriting old data, so “dirty” is represented by absence of a matching applicable DerivedKnowledge. That’s fine. We should ensure the design still supports detecting “need recompute” efficiently.

**Applicability abstraction:** We agree with making knowledge applicability a core concept (not just snapshot ownership). This is essentially self-adjusting computation, which is state-of-the-art for incremental compilers. No simpler model (like snapshots-only) can achieve the same reuse safely. Thus, we keep this *strong* model, but note it requires careful implementation. (Potential classification: *Foundational principle to keep, but needs robust algorithms to implement correctly.*)

# M. Capability realization and authority

The architecture splits **deterministic analyzers (tools)** from **LLM tools** via an authorization model. In practice, most systems either allow tools (like compilers) or run everything through the model, but the rationale here seems security: repository analyzers get full read access, whereas model-invoked tools are sandboxes.

Literature on capability-based security (e.g. in OS or web) advocates least privilege, so this separation is valid from a security standpoint. For example, if a coding agent has a tool “run shell command,” it should be restricted, whereas static analyzers (even if file-reading) run in a controlled environment. OpenAI’s “tool use” documentation similarly suggests separating model tools into approved functions.

No strong research directly conflicts with this design. Some frameworks (AutoGPT etc.) mix in-process analysis, but that’s less structured. We view the distinction as **not harmful**: analyzing code deterministically in a sandboxed tool is fine, and granting LLM different, narrower permissions is arguably safer. Implementation might share some core (e.g. language runtime), but logically keeping them separate is reasonable. We mark this as **VALID OPEN DESIGN PRESSURE**: it’s a policy decision more than architecture; performance costs (double tech stack) vs safety is an implementation tradeoff.

# N. Graph architecture

The architecture allows **multiple semantic graph views** (e.g. one graph per analysis type) rather than forcing one global code graph. In practice, real systems vary: Kythe uses one unified graph, CodeQL builds one queryable database (akin to a graph), whereas property-graph vulnerability tools use a single integrated graph (CPG). Sourcegraph/LSIF effectively has one index per language that clients query.

**Multiple views vs unified graph:** The advantage of separate graphs is conceptual clarity (e.g. a call graph vs a type graph). But it complicates queries that span views (e.g. find all functions affected by a type change requires cross-graph joins). Kythe’s unified graph suggests that a shared schema with typed edges may simplify integration. Unless there is a clear reason to keep views disjoint (for performance or modular loading), a unified graph substrate is worth considering. We should allow distinct edge types (calls, defs, etc.) but not physically partition them. This preserves a single identity domain and simplifies cross-cutting queries.

**Common identity domain:** Ideally, nodes (entities) in different views should share identities where they represent the same concept (like Kythe’s design). If call graphs and reference graphs both involve function symbols, they should point to the same function node. Otherwise, we re-synchronize them manually. The architecture hint “GraphNode not necessarily RepositorySubject” suggests some separation, but evidence favors shared nodes: e.g. CodeQL’s tables use symbol IDs for linking different analyses.

**Views vs projections:** One could implement “views” logically by filtering the unified graph by edge type. This preserves a single storage while still conceptually handling multiple analyses. This matches many graph DBs (labeled edges).

**Cost of multiple views:** Having totally separate graph databases could be heavy (storage + maintenance overhead). Also, constructing graph nodes eagerly for all analyses might be wasteful. Many systems (e.g. LSIF) build index lazily or on-demand. A hybrid approach: build a core symbol/references graph upfront, then additional analysis graphs as needed.

**Conclusion:** Adopt a **single graph substrate** under the hood, with typed nodes/edges for different analyses. Let “views” be filters on this graph rather than separate structures. This aligns with Kythe’s approach and avoids fragmentation. We’ll keep multiple conceptual projections (call graph, data-flow, etc.) but unify them in storage. **(MODIFY)**

# O. InformationNeed and decomposition

Using an immutable **InformationNeed** object separate from the query prompt is an unusual abstraction. In IR research, *information need* is indeed distinguished from query text for evaluation, but systems do not materialize it. In code retrieval, practical tools take user input (natural language or code context) as a one-off “query” without building an explicit need model. The architecture’s notion might help debug or log what the user really wanted, but there is no clear retrieval benefit: it is essentially query intent tracking.

Moreover, we question immutability: agents often refine their need (drilling into specifics), so the “need” evolves. Keeping it immutable may not reflect reality. It might be better to allow an information need to spawn sub-needs or to update. The architecture does allow parent/child needs, which covers some of this, but at cost of complexity.

Given the lack of empirical evidence that separating need helps retrieval performance (versus simply optimizing queries or using RL models), this stands out as a potentially needless layer. We lean towards simplifying by treating the user query/task as the information need. If finer tracking is desired, it could be a log entry rather than an enforced structure. **(SIMPLIFICATION OPPORTUNITY)**

# P. Retrieval planning

Deterministic *query planning* (choosing which strategies to run, in what order) is not standard in current systems, but related ideas exist in search engineering. Many search services do multi-phase retrieval (e.g. simple Boolean filtering then full-text scoring, or using query expansion). The code-search example [74] runs BM25 and dense in parallel, effectively a concurrent strategy; some also do pseudo-relevance feedback (the readme mentions optional TF-IDF expansion).

Key questions:

- **DAG of queries:** Few systems explicitly plan queries as a DAG. It may be simpler: first run one set of queries (e.g. initial retrieval), then optionally expand or refine. For example, OR-Tools and QA systems sometimes do iterative retrieval. The architecture could start with a linear plan (one wave followed by another). Fully arbitrary DAG planning is probably overkill; we suggest a sequential or looped approach (like iterative query refinement).

- **Concurrent retrieval:** Using BM25 and embedding search in parallel often helps capture different signals. The cost is two searches, but search is usually fast relative to reasoning. With high token budgets and compute, concurrent retrieval is often worthwhile. For limited budgets, one may have to choose. We can let the system decide (e.g. if the top BM25 hits are high-scoring and cover code at high recall, maybe skip embedding). Empirical tuning needed.

- **Conditional waves:** Deciding when to stop: classical IR stops when satisfied or no improvement. Here, an agent could stop retrieving when it deems the context sufficient. This becomes a policy question (when is confidence high enough?). It likely requires model involvement or a learned heuristic, which is beyond architecture scope. We would implement simple rules (e.g. retrieve N docs, or until cumulative score passes a threshold).

- **Budget allocation:** The plan says “budget” but didn’t define it. In practice, might mean “token cost” or “number of docs”. Systems rarely do dynamic budget management aside from fixed limits. A simple strategy is fix max results per retriever.

- **Provenance of queries:** It may help to record how each query was formed (for reproducibility or evaluation). This is unusual but harmless if kept as metadata. E.g. “query used these keywords vs synonyms”.

- **Adaptive retrieval:** Some research into “model-driven retrieval” exists, but it's experimental. E.g. systems that let the LLM suggest next queries (Active RL for IR). That falls under “progressive disclosure” rather than initial planning. For now, fixed heuristic plans should suffice.

- **Examples:** The code search hybrid [74] basically implemented a plan: run BM25 and dense immediately (concurrent) and fuse results. It also allowed optional expansion (a mini wave). That pattern suggests a simple plan: first do base retrieval, then optionally post-process results (rerank or expand if needed). We should not hard-code a full planner, but support pipelining multiple retrievers.

**Conclusion:** We recommend a flexible but simpler approach: allow the design of retrieval strategies as a directed plan (with limited branching), but treat it more as **implementation detail**. Early versions could just run all chosen retrievers in parallel and merge results, without formal planning. As evidence shows benefits to hybrid retrieval, we keep that. Exact planning logic and stopping conditions should be an implementation question, not a high-level architecture object.

# Q. RelevanceEvidence

The architecture’s idea of storing raw retriever scores as “RelevanceEvidence” is analogous to feature-based ranking in IR. Many production systems indeed keep score metadata (BM25 score, vector distance, etc.) to fuse in ranking or to debug. The debate is whether to preserve these as first-class artifacts or just feed them into a black-box ranker.

**Preserving evidence vs normalization:** In evaluation and advanced LTR, it is common to keep feature logs (including retrieval scores) for training/analysis. For operational systems, usually the evidence is combined (e.g. via weighted sum). The architecture’s caution that “retriever-native scores are not truth” is valid: different retrieval methods have incomparable scales. In practice, one often normalizes or calibrates. But explicit evidence objects allow full transparency and later calibration.

However, labeling *every* piece of evidence seems heavy. We might instead define a limited set of features (score, maybe top_k, source ID) to attach to each candidate. A ranker can use these features. This is the usual approach in learning-to-rank. Making a whole evidence data type for each ranking signal may be too generic.

**Evidence polarity:** The architecture hints at “positive vs negative evidence” for a document. In retrieval, absence of evidence is rarely recorded; only positive hits are. Explicit “non-matching” evidence isn’t normally stored (except query facets). This component seems unnecessary, unless the system intentionally tracks “we searched but didn’t find”. I don’t see a use-case, so we can drop explicit negative evidence.

**Feature container vs specific fields:** Instead of a generic RelevanceEvidence blob, better to define specific stored values: e.g. `{bm25_score, embedding_score, recency, etc.}`. It’s easier for rankers to use. The architecture’s generic evidence class becomes a catch-all that’s hard to manage.

**Use in ranking vs RAG:** Given [74], the evidence breakdown was used for analysis, not needed at runtime except for scoring. Learned rankers often just take raw features (embedding dot, BM25). We should allow ranking to access raw retriever signals but not insist on evidence objects in the core model.

**Absence vs presence:** Architecturally, it’s simpler to ignore evidence of absence (non-retrieval). In probabilistic IR theory, one does consider “missing evidence lowers probability,” but practically it's encoded as fewer hits.

**Conclusion:** The principle “don’t trust raw scores as ground truth” is correct; we will use a ranker to interpret them. But we can simplify by not elevating RelevanceEvidence to heavy objects. Instead, let “ranking” accept as input (query, doc, feature_vector). If needed, we log raw evidence for auditing. Explicit opposing evidence is likely unnecessary for retrieval (it might appear in debate-style Q&A, but not here). We will collapse RelevanceEvidence into feature logs. **(SIMPLIFICATION OPPORTUNITY)**

# R. Ranking

Ranking is indeed a distinct step in modern IR pipelines (retrieve then rank). The architecture’s separation of ranking from retrieval is realistic: in RAG, one often retrieves a candidate pool, then selects top-K by a re-scoring model. Many code-search systems use BM25 to get, say, 100 candidates, then re-rank by a neural model or heuristic. So this boundary makes sense.

**Ranker outputs:** A ranker could output scores or even probabilities. The architecture could support outputting a calibrated relevance probability, but that requires training data. Many systems use raw scores or learned scoring functions without strict normalization. We should allow either; fixed weighted sums vs learned models are both used.

**Task-conditioning:** The architecture could let the ranker know the task type (code generation vs explanation vs test writing) and rank differently. In practice, if one trains specialized rankers per task, that’s possible. But currently we lack evidence of multi-task rankers for code contexts. We suggest keeping ranker stateless w.r.t tasks initially, relying on feature signals to adapt. Task-conditioned ranking could be future work.

**Learned ranking:** There is no reason to prohibit learning. If we have enough labeled data, a learned ranker (e.g., LightGBM on features) often surpasses fixed rule. We should support plug-in rankers (linear combos, neural).

**Fixed experiments:** The architecture invites “fixed-evidence/fixed-rank” experiments (for evaluation). This is reasonable: one can freeze retrieval output (as features) and vary ranker to measure effect. That’s similar to offline LTR benchmarks. We should record evidence features to facilitate such tests.

**Ranker versioning:** Yes, we should version rankers or models (not just a monolithic black box). This architecture versioning already hints at tracking implementations, so no issue. If two rankers are tried, their provenance should be logged.

**When to skip ranker:** If only one retrieval strategy is used or the evidence is already a single score, then a separate ranker adds little. The architecture could allow “ranker is identity” as a mode. In fact, the code search [74] hybrid mode just RRF-sums without a separate rank training. That is essentially “retrieval and final scoring are fused.” So the separation is optional.

**Combining retrieval with retrieval planning:** The architecture suggests rank is separate from planning; this is okay. However, one could imagine merging ranking logic into retrieval (e.g. learned sparse retrieval integrates BM25 and embeddings in one model). That is an alternative not covered, but we can mention it: We allow such hybrid retrievers as “other retrieval services” producing evidence. If integrated retrievers become dominant, the architecture can collapse retrieval+ranking into a single model component.

**Conclusion:** We endorse a separate ranking stage in general. The architecture should make clear that ranking may simply interpret retrieval scores (possibly with extra features). Calibrating to probabilities is nice but not essential. Task-conditioning and learning are implementation choices. Overall, the division is pragmatic and used in IR; no major changes needed here (**KEEP** this separation).

# S. Disclosure planning and representation

The DisclosurePlanner’s role is to select which pieces of information (from ranked candidates) to include in the context. This goes beyond simply picking top-K: it considers coverage, redundancy, overlap, etc. These concerns mirror known problems in text summarization and diversified retrieval.

**Evidence from IR:** Maximal Marginal Relevance (MMR) and submodular selection are classic for balancing relevance and diversity. These could be used instead of inventing a new planner algorithm. For example, MMR picks documents to maximize a weighted tradeoff between relevance and novelty. Similarly, Contextual Query Rewriting (CQR) techniques diversify queries. There’s also recent work on *context compression* and *super-document retrieval* for QA (e.g. Narayan et al.’s PRIMER approach). However, no single technique has proven best for coding contexts.

**Coverage vs sufficiency:** Measuring “coverage” of an information need is elusive. The architecture acknowledges this difficulty. Practically, one usually uses redundancy heuristics (avoid duplicate content) and maybe templates (like “include docstring or signature if useful”). Estimating sufficiency (knowing the answer is in the context) is effectively the model’s job; static methods can’t predict it reliably.

**Order sensitivity:** The planner might output a set, but context order still matters. The architecture keeps them separate, which is logical. Different orderings (e.g. alphabetical vs relevance vs topical) could impact the LLM’s attention. Some evidence (from [76]) suggests information at the beginning/end is most used, so an ordered plan could exploit that. However, optimizing order beyond “rank by relevance” is probably overkill until we measure effects.

**Complexity:** An exhaustive coverage optimization (knapsack, submodular maximization) can be NP-hard. At coding-agent latencies, we likely need greedy heuristics. Many summarization systems use greedy MMR or simple TF-IDF cover scoring. The architecture’s broad list (redundancy, overlap, complementarity, coherence) is more than typical systems use. Our suggestion: start with a simple diversify-by-topics approach (cluster snippets or use embedding-based MMR) and refine.

**Integration vs separation:** It may be possible to fuse ranking and selection: e.g., one could aim for diversity at ranking time (Serendipity-based reranking). However, given the multiple objectives here, a two-stage approach is fine: first score relevance (one dimension), then choose a subset for diversity/coverage (second dimension). This matches how IR sometimes does query subtopics selection.

**Conclusion:** While the high-level idea of a planner is conceptually sound, we recommend **streamlining** it. Use known diversity techniques (MMR or clustering) rather than invent new ones. Avoid expecting precise coverage metrics. An explicit planner stage is probably still useful for logging what was chosen, but its implementation can be simple greedy selection with tunable parameters.**(SIMPLIFICATION OPPORTUNITY)**

# T. Representation

The architecture distinguishes representation *form* (source code vs summary vs graph snippet) and fidelity. This reflects that one might present code as plain text or as an extracted summary, etc. In practice, coding agents predominantly use source code or possibly small summaries (e.g. function signatures, docstrings). There is little published research on systematic selection of representation forms specifically for coding context.

Some observations:

- **Source vs summary:** Generally, giving actual code (source-preserving) yields the highest fidelity (the model can reason on exact code). Summaries or knowledge projections (e.g. UML diagram) risk losing detail. We believe *keeping the original code span whenever feasible* is best, citing no evidence to the contrary. A compromise is embedding small-code blurbs along with docstrings. The architecture’s notion of summary cost and fidelity is appealing theoretically, but too vague. Instead, we can treat summarization as a potential separate analysis (maybe an LLM task, not a deterministic one).

- **Graph or structured representations:** The idea of providing e.g. AST or CFG to LLM is largely unexplored. LLMs are not natively graph processors (though they can be given serialized graph edges). Given our determinism goal, we won’t spontaneously generate new structures except if an analyzer can produce linearized code graphs. This seems too experimental. Better to stick with text code, possibly annotated with simple markers (e.g. list of imports, or a flattened docstring).

- **Chunking:** Breaking a file into chunks is mainly for context length limits. The architecture suggests deciding chunk granularity per need. In practice, many systems (e.g., Search-In-Repos) use fixed-size windows or semantic boundaries (e.g. per function/class). We should probably follow code structure: present entire small functions or classes, rather than arbitrary text spans. This preserves meaning.

- **Fidelity measurement:** How to quantify “reconstruction burden” or fidelity is unclear. No current metric is standard. We can skip formal measures and rely on heuristics (e.g. whole lines or AST nodes are preserved if excerpted).

**Conclusion:** We keep the distinction that each selected code snippet is returned “source-preserving” (i.e. actual code lines) rather than lower-fidelity summary. We allow at most one intermediate summation step: perhaps we implement a cache of small function-level summaries (docstrings) for quick recall, but these would themselves come from code (so still deterministic). For complex code snippets, we let the LLM generate synthesis on the fly if needed. In short, we will present code fragments or documentation excerpts directly; the architecture’s elaborate taxonomy of representation forms seems premature. **(SIMPLIFICATION OPPORTUNITY)**

# U. Derived-synthesis, authority, and conflict

The rule to *add new semantic assertions from LLM to DerivedKnowledge* we already flagged as flawed (see Section E). This overlaps with authority and conflict management:

- **LLM assertions as knowledge:** Without strong evidence, we should treat LLM summaries as ephemeral. They lack reproducibility and source citation. A better model is the RAG approach: use the LLM-generated synthesis as an answer, but not store it in the core knowledge graph. If certain claims seem important, one could mark them as “inferred but not verified,” but not make them immutable. In practice, systems like Retrieval-Augmented Q&A do not modify the index with generated content. So we recommend ditching derived synthesis as knowledge; instead, handle all synthesis within the context of a single model invocation. **(FOUNDATIONAL DEFECT to treat LLM outputs as Durable Knowledge)**

- **Conflict of claims:** When an LLM-derived statement contradicts existing code or documentation, something has gone wrong. The architecture’s treatment (preserve conflict and decision via authority) is interesting but complicated. In practice, agents often just present multiple viewpoints. There is research on multi-source conflict resolution (truth-finding algorithms) but not in code contexts. Given our limited evidence, a simpler approach is: highlight conflicts as hazards to the user, but not try to algorithmically resolve them. The system could attach provenance (e.g. "Model says X, but code comments say Y"). This doesn’t require a formal authority ranking beyond “code > comments > LLM”.

- **Epistemic status:** The architecture suggests belief strength or confidence for syntheses. In RAG, generation confidence isn’t typically computed (other than log probabilities, which don’t align with correctness). We might allow a simple flag for “model statement - not verified”, but it’s unclear how to quantify. So skip detailed confidence semantics.

- **Handling ADR vs code:** The architecture implies we might have to choose between conflicting sources (code vs architecture doc). In reality, both could be relevant. It is safer not to override code with ADR (since code runs). We might simply present both viewpoints. A universal “authority layer” is hard to justify formally.

**Conclusion:** We should not force all synthesized assertions into DerivedKnowledge. Instead, treat them as part of the *ContextDisclosure* or final answer with appropriate notes. Authority modeling can be very lightweight: perhaps assign a fixed preference (code > architecture docs > comments > tests > ADRs). We do want to record sources, but actual conflict resolution can be left to the user or a simple rule. We mark this as **MODIFY**: simplify by separating LLM content (ephemeral) from stored knowledge, and treat authority as a fallback tie-breaker rather than a core dynamic mechanism.

# V. DisclosurePlan / ContextDisclosure

The distinction between a *planned* set of information and the *realized* context is subtle. The intent is to separate “What we intended to include” from “What we actually gave the model.” Possible benefits: debugging (compare plan vs reality), ensuring consistency, handling failures gracefully (plan might fail to retrieve a piece, so the realized plan is smaller).

However, in many systems the plan is never explicitly materialized: we simply retrieve some docs and pass them on. The extra layer is mostly conceptual. The architecture might use it to re-run portions if needed.

**Proposed simplification:** We suggest treating ContextDisclosure itself as the final artifact. The planner need not output a separate record unless needed for logs. If we do keep a Plan, its only role is to list document IDs that *should* have been included. If a retrieval fails, ContextDisclosure can note it. But this is minimal overhead.

**Transactional realization:** The plan vs realization idea hints at handling partial failures: e.g. planned snippet failed to load. In such cases, having a plan helps recompute. But we might just have ContextDisclosure hold some status flags.

Overall, this abstraction can likely be collapsed. Instead, for each model request we can output a single object containing all selected info (text spans + metadata). Internally we can still “plan” but need not expose it as a separate concept.

**Authorization checks:** The architecture asks if we should re-check authorizations at presentation time. If context assembly is done only from pre-authorized content (repositories, etc.), this is moot. Perhaps skip. If network calls or dynamic content were allowed, then yes, but seems out-of-scope.

**One plan vs many:** Could have one plan per request. There's no clear use-case for splitting a plan into multiple segments (other than iterative refinement, which is progressive disclosure, next section).

**Conclusion:** Collapse DisclosurePlan and ContextDisclosure into one stage (“Context assembly”). We still keep a ModelRequest that includes the assembled context plus task prompt. But don’t complicate with separate plan tracking unless we foresee needing it for evaluation logs. Implementation can simply build the context in memory. **(COLLAPSE)**

# W. Progressive disclosure

Progressive (iterative) retrieval—fetching initial context, reasoning, then fetching more—is a common pattern in agent research (e.g. ReAct, tool-using agents) and RAG frameworks. For coding tasks, this is plausible: an agent might first retrieve general info, then ask for more specifics (bug fix steps, etc.).

Literature on multi-turn QA and RAG suggests that iterative retrieval can improve results (as one can refine queries), at cost of latency and token usage. No hard rule exists. Empirical practice (e.g. AutoGPT) shows it can solve harder multi-step tasks. However, too many turns risks diverging or running out of quota.

**Stop criteria:** Common criteria: model indicates satisfaction (e.g. “I have enough info”), or reaching a max turn limit, or meeting a confidence threshold. This is typically heuristic. Possibly using a view like “if current context already has an answer, stop.”

**Our architecture:** The layering implies calling back into the InformationNeed/Planner components with updated needs. That’s reasonable. But making this core (like an infinite loop) is not necessary for first implementation. Instead, allow at most one or two rounds (initial retrieval, one refinement) to test benefits. Many coding sessions allow multiple prompts anyway.

**LLM-request vs planner-driven:** The architecture proposes a separate planner that detects “missing context” and issues new InfoNeeds. Alternatively, we could let the LLM itself ask for code or docs (e.g. using a tool call). Both are valid; the architecture’s planner corresponds to a “system role” approach. Given complexity, we might let the agent (model) say “I need file X” and treat that as a new InfoNeed. That merges steps, but is more agentic.

For now, we’ll note progressive disclosure can be useful especially for large or complex tasks. It should be enabled (e.g. by looping the retrieval with updated query). But much can also be deferred to the implementation’s agent logic. The architecture can allow repeated usage of the same retrieval pipeline on refined queries. The details (turn-taking, stopping) are a design decision.

No direct citation, but [79] implied that broken flat retrieval “misses connective tissue”, hinting iterative strategies could help. So we keep progressive retrieval as an optional mode (**keep**, but as an implementation detail). It aligns with adaptive retrieval research.

# X. Determinism and LLM-independent intelligence

The architecture declares that all “repository intelligence” is deterministic (static analysis, build info) and excludes any LLM knowledge. This is a prudent stance for reproducibility. Indeed, anything seeded by an LLM is non-deterministic and not strictly reproducible.

**Evidence:** Tools like LSIF/Salsa/Nix rely on deterministic algorithms. The success of systems built around static knowledge (see LSIF) suggests a lot can be done deterministically. However, some useful information might only come heuristically: e.g. code summarization or intent prediction. Excluding these could limit intelligence.

Should heuristic or probabilistic analyses be represented as DerivedKnowledge? Perhaps, if they are repeatable given the same analyzer version. For instance, a linter warning or a “likely type” from a static inferencer is heuristic but deterministic (if the tool version is fixed). We could allow these as DerivedKnowledge with confidence tags. Full nondeterministic LLM outputs, however, break our premise. So disallow them as core knowledge; at most as ephemeral answer aids.

**Local models:** If the goal is to empower weaker local models, having a rich deterministic base is helpful (they can rely on it instead of hallucinating code facts). But it can’t completely offset model weakness in understanding nuanced tasks or synthesizing novel code patterns. So we must accept some reliance on the model’s reasoning. The architecture’s scope (static facts) rightly stops at what can be precomputed.

**Conclusion:** Continue to exclude LLM-originated “facts” from the core intelligence substrate. However, label deterministic derived facts with their analyzer version for reproducibility. If we incorporate any heuristic analyses, note them explicitly. But fundamentally, yes: treat repository knowledge as a deterministic cache, not a mixed-content store. This stance is defensible and maintains correctness guarantees (so **KEEP**).

# Y. Evaluation and measurability

The architecture’s semantic boundaries facilitate fine-grained evaluation:

- **Retrieval metrics:** With retrieved evidence logged separately, we can measure recall@k, precision@k, etc., independent of the final answer. The Connected knowledge of the system allows, for example, measuring how often needed facts were included in the context. Standard IR metrics (Precision, Recall, NDCG, MRR) apply.

- **Ranking ablations:** By capturing evidence, we can re-score a fixed candidate set with different rankers (offline learning-to-rank experiments). This is akin to IR experiments where retrieval results are fixed and various ranking algorithms tested, matching the architecture’s plan for fixed-evidence tests.

- **Context quality:** Harder to measure. One could measure redundancy in the context or whether the model successfully uses each piece. One proxy is “does removing a piece degrade answer accuracy?” (marginal contribution). This requires annotated relevance of context for the final task, which is often unavailable. Some QA benchmarks do have such mapping.

- **Token efficiency:** We can calculate tokens used vs answer score or error rate, a useful metric for latency/cost.

- **Success metrics:** End-to-end, measure task success (correct code, passed tests). But architecture design should also allow component-wise logging (retrieval latency, number of iterations, etc.).

- **Component identity/version:** The architecture demands we track exactly which retriever, ranker, etc., was used. This is essential for reproducible experiments: we must tie metrics back to code version.

- **Controlled experiments:** The separation enables experiments like “fixed retrieval, varying ranker” or “fixed evidence, varying disclosure strategy”. E.g. run the pipeline with BM25-only vs BM25+embedding (like [74]). Or with vs without diversification. These correspond to “fixed-evidence” or “fixed-plan” tests in the architecture.

- **Synthesized answer metrics:** We can measure hallucination or correctness of final answers (using benchmarks or oracles), which is ultimately needed. Having separate logs for each stage might help correlate e.g. “this failure was due to missing snippet X”.

**Evidence:** Retrieval and ranking evaluation are well-studied. The architecture’s frame allows reusing those concepts. It goes beyond typical RAG setups by demanding a more elaborate logging of intermediate steps; this is ambitious but potentially useful if carefully instrumented.

**Conclusion:** Most boundaries aid measurability. We should ensure modular evaluation harnesses them. No immediate change needed; just ensure each component can log its output for offline analysis. Metrics like recall@k, precision@k, MRR for retrieval, and typical model evaluation (accuracy, BLEU for code gen) remain primary.

# Z. Total systems complexity

Taken together, the architecture has *many* pieces. Even if each piece is justified on its own, the combined complexity is enormous. Potential pain points:

- **Artifact count:** Entities like RepositorySnapshot, Subject, Occurrence, Resource, many kinds of graphs, multiple knowledge types, etc., risk clutter. Each new fact needs several identities. Managing and synchronizing them could slow down the system.

- **Identity management:** The more distinct IDs (content vs occurrence vs derivation vs knowledge), the more we must translate between them. This adds cognitive load for implementers and potential for mismatch bugs.

- **Provenance explosion:** If every piece of evidence and derivative is tagged with full provenance, storage could balloon. E.g. tracking which derivation step (with which code version and parameters) created each snippet. This meta-information may become larger than the content.

- **Storage overhead:** Persistent storage of all DerivedKnowledge (all ASTs, call graphs, type facts, docstrings, etc. for all snapshots) is huge. Real systems (e.g. Sourcegraph’s LSIF indexes) already can reach GBs for large codebases. The more granular the data model, the more to store. We must budget carefully or prune aggressively.

- **Latency:** Orchestrating all these components (cache lookups, rebuild checks, multi-stage queries, ranking, selection) for every coding request could slow down even moderately sized repos. We need to pick and tune which things run synchronously vs can be cached offline.

- **Developer ergonomics:** For the team building this, the conceptual space is vast. They might slip on clear interface boundaries. A simpler prototype might be more feasible initially.

Given these, we consider whether ~80% of benefits could come from ~20% of features. Likely yes:

- The core value is *correct, up-to-date context* to the model. We could get most benefit by:
   - Maintaining an up-to-date index (LSIF or similar) of definitions and references.
   - Running fast code search (BM25+optional embedding).
   - Selecting top-K documents/snippets.
   - Appending them to the prompt (with minimal filtering).
   - Using a model to answer.

This minimal pipeline drops much of the novelty (no InfoNeed, one-shot retrieval, no plan, no granularity of DerivedKnowledge beyond e.g. file-level or function-level caches). Yet it covers reproducibility (persist index) and incremental update (just re-index changed files).

**Candidate minimal architecture:**

- **Repository state:** Use Git commit or content-hash snapshot identity; maintain an LSIF/semantic index per snapshot.
- **Retrieval:** Accept queries (NLP or code) and run BM25 + (if needed) a fast embed search (either heuristic or pretrained encoder). Score and union results.
- **Selection:** Simply take top-`M` (say 5) code snippets or files, possibly deduplicating by file or signature.
- **Assembly:** Order them by relevance score and concatenate (maybe with separators).
- **Provenance:** Log which files/snippets were included and their sources.
- **No fancy IR planning:** No explicit need objects, no complex planning, no derived-synthesis, no graph overlay.
- **Incremental build:** Use file watchers or commit hooks to trigger re-index of changed files into a combined index (as LSIF does in CI).
- **Graph:** Instead of multiple, maintain a unified symbol/reference graph (like Kythe) under the hood for queries if needed.

This reduces complexity dramatically. It keeps reproducible index and retrieval (the hardest promises), while letting the model do the heavy lifting of reasoning.

**Complexity vs Benefit:** Many added features (detailed provenance, selection planning, tool sandboxing) seem to have diminishing returns. We should be mindful: if early benchmarks show moderate retrieval is enough, only then elaborate further.

Therefore, **we should aim to implement the lean pipeline first** and add complexity only where shown beneficial.

# AA. Comparison with production/research systems

Below we compare the architecture (Proj: Devtools) with documented practices of notable systems. We classify evidence as **DOCUMENTED** (public docs/papers), **RESEARCH-INFERRED**, **BEHAVIOR-INFERRED**, or **UNKNOWN**.

- **Repository-state identity:**
  - *Devtools:* Content-hash based snapshot identity, separate from Git.
  - *Bazel/CMake/IDE:* Usually tie to workspace/commit; Bazel uses content hashes for build inputs.
  - *Git/Nix:* Git uses commit ID (coarser). Nix stores packages by content hash.
  - **Conclusion:** Using content hashes is well-supported (DOCUMENTED in Bazel, OSTree). Devtools aligns well.

- **Indexing strategy:**
  - *Devtools:* Rich static analysis outputs (derived knowledge).
  - *LSIF (Sourcegraph)*: Indexers emit code symbols/refs as JSON (persisted).
  - *Kythe:* Graphs of cross-references from compiled binaries.
  - *Codex/Copilot:* Opaque (train on public repos).
  - **Conclusion:** Precomputed indexes as proposed match Sourcegraph and Kythe (DOCUMENTED).

- **Incremental maintenance:**
  - *Devtools:* Fine-grained semantic invalidation (like Bazel).
  - *Bazel/Shakes:* Content-hash or dependency graph invalidation (documented). Bazel/CMake require full rebuild if any input changes by default, but Bazel remote cache uses hashes.
  - *Salsa (rust-analyzer):* Proven incremental (DOCUMENTED).
  - *IDE (VSCode):* Many do full re-index on file save (BEHAVIOR-INFERRED); some incremental AST updates.
  - **Conclusion:** Devtools’s semantic cache is ambitious; aligned with Salsa’s model (RESEARCH). Real tools often simpler but less efficient. The principle is sound (DOCUMENTED for Salsa).

- **Symbol/code graph:**
  - *Devtools:* Multiple graphs per analysis type.
  - *Kythe/CodeQL:* One unified semantic graph.
  - *LSIF:* Emitted data can be viewed as one big index (effectively one graph per language).
  - *CodeQL (GitHub):* Houses code in relational DB (like a graph).
  - **Conclusion:** Production tools lean towards one integrated graph. Multiple separate graphs in Devtools might fragment data (no clear advantage), so collapsing into one graph aligns with known systems.

- **Lexical retrieval:**
  - *Devtools:* BM25-based code search.
  - *Sourcegraph:* Uses a modified Zoekt search (BM25-like) for code (DOCUMENTED on blog).
  - *GitHub Search:* Proprietary (likely Elasticsearch + heuristics).
  - *CodeSearchNet:* Baseline BM25 was strong.
  - **Conclusion:** Lexical retrieval is standard, and the plan (using BM25 or similar) matches industry practice (DOCUMENTED).

- **Semantic retrieval (embeddings):**
  - *Devtools:* Allowed (hybrid pipelines).
  - *Sourcegraph Copilot/Cody:* Uses embeddings (CLIP for code or custom).
  - *OpenAI embeddings:* Publicly available; many code search start-ups use them.
  - *CodeSearchNet:* Dense encoder research (but BM25 was surprisingly good).
  - **Conclusion:** Growing trend to use neural embeddings; Devtools’s hybrid approach matches evolving practice (RESEARCH-INFERRED, partly in GitHub Copilot rumors).

- **Retrieval planning:**
  - *Devtools:* Explicit query plan and waves.
  - *Prod:* Uncommon. Most do fixed strategies (maybe pseudo-relevance expansion).
  - *WhatNick (LangChain RAG):* Suggests running multiple queries with conditioned prompts (DOCUMENTED in RAG tutorials).
  - **Conclusion:** No known system formalizes a retrieval plan; this is novel. We likely simplify this. (Category: UNKNOWN/pragmatic).

- **Context selection:**
  - *Devtools:* Diversification/coverage, not just top-K.
  - *RAG systems:* Usually take top-K (static K) with minimal filtering; or use MMR for open-domain QA (some academic RAG methods).
  - *Summarization systems:* Use MMR/submodular for summary (RESEARCH).
  - **Conclusion:** The diversity/coverage approach is more complex than typical RAG. Some IR research supports it, but no dominant production analog. Likely unnecessary at first.

- **Progressive retrieval:**
  - *Devtools:* Supports iterating needs.
  - *Auto-GPT/Agents:* Common in bot frameworks (BEHAVIOR-INFERRED).
  - *LLM tools like WebGPT:* Use multi-turn queries.
  - **Conclusion:** Progressive agents are popular, so keeping it is reasonable. Implementation can defer logic to conversation design. (DOCUMENTED in RAG/agent tutorials, though not formal).

- **Provenance:**
  - *Devtools:* Explicit high granularity provenance.
  - *RAG (Retrieval QA):* Typically cite sources, but don’t log internal reasoning.
  - *Data lineage systems:* They do track provenance (e.g. W3C-PROV).
  - **Conclusion:** Very fine-grained provenance is more than production, but sees parallels in data management fields. No conflict; it's an extension.

- **Evaluation:**
  - *Devtools:* Proposes measuring sub-component metrics.
  - *Prod:* Typically end-to-end (accuracy, accuracy/cost tradeoffs).
  - **Conclusion:** Devtools would have more internal metrics, which is good for research. Production rarely does that, but we see it as strength (more granularity).

**Summary:** Devtools adopts state-of-the-art ideas (content hashes, incremental analyzers, unified graphs). It pushes further in IR semantics and provenance. Many production systems skip planning/diversity complexity, instead relying on simpler retrieval pipelines. The architecture’s complexity goes beyond what is currently documented in products, suggesting some concepts should be simplified unless experiments demand them.

# AB. Invariant-by-invariant challenge

We examine each major invariant (claim) and assess evidence:

- **“Identity is not location”** (i.e. use content identity, not file path):
  **For:** Content-addressed models (Bazel, Git, OSTree) validate this. It ensures correctness under renames and sharing.
  **Against:** Some systems (LSIF) do use file/line as key in indexes (but that’s surrogate). If identical content appears in two places, content-id will de-duplicate, which might be undesired in certain queries.
  **Verdict:** Evidence supports content-based identity (DOCUMENTED for build systems). Keep strong.

- **“Snapshot is not delta”** (i.e. treat snapshots as full state, not just changes):
  **For:** Immutable snapshot is a clear abstraction (DB transactions, build trees). OSTree shows benefit.
  **Against:** Storing full snapshots (even partially) can be wasteful; some systems do incremental diffs.
  **Verdict:** Fully realized snapshots are beneficial for correctness; deltas alone risk inconsistency. Keep (but support sharing partials).

- **“Snapshot completeness is not intelligence completeness”** (having all file info doesn’t guarantee all useful knowledge):
  **For:** Indeed, static code often hides semantic intent (e.g. design rationale). Models must infer beyond static facts.
  **Against:** Hard to argue against; static analysis is inherently incomplete (Halting problem, etc).
  **Verdict:** True and accepted. We must rely on LLM inference for some knowledge. Keep (and use it to justify iterative retrieval).

- **“DerivationDefinition is not implementation”** (the separation of spec vs code for analysis tasks):
  **For:** In large systems one analysis definition can have multiple implementations (e.g. two parsers for different languages). Semantic versioning could manage this.
  **Against:** Adds complexity. Many tools bind definition and implementation closely (e.g. one type analyzer).
  **Verdict:** Likely collapsible in practice. We lean toward merging in initial design (SIMPLIFICATION).

- **“Semantic capability is not binding”** (having an analysis capability doesn’t tie it to a specific codebase or language):
  **For:** Good to allow plug-ins; e.g. a JSON parser rule can run on any repo with JSON files.
  **Against:** In practice, analyzers are usually part of the project (language-specific).
  **Verdict:** Keep concept as “rule definitions can be re-used across snapshots”, as in build rules for different targets.

- **“Dependency is not provenance”** (a file import != evidence origin):
  **For:** Data provenance is richer (who computed, which analyzer version). Dependency graph is simpler.
  **Against:** Often conflated; e.g. Bazel or Make logs just say “file A depends on B”, not which rule triggered it.
  **Verdict:** Differentiating them is good (one is semantics, one is lineage). Keep.

- **“Applicability is not mutable validity”** (applicability of knowledge ≠ validity state):
  **For:** Applicability checks ensure relevance to current state, not correctness per se. They operate on immutable data.
  **Against:** It overlaps with “dirty” marking. Possibly just another name for “clean flag”.
  **Verdict:** Keep as an abstract notion, but realize it reduces to dependency checks.

- **“Derivation graph is not repository semantic graph”** (analysis dependencies != program semantic graph):
  **For:** True: an analysis pipeline’s DAG (e.g. parse→type→call) is different from code’s call graph or AST edges.
  **Against:** Might be conflating concepts; easier to keep separate notions.
  **Verdict:** Keep distinction; it’s conceptually clear.

- **“Retriever score is not relevance truth”** (score must be interpreted, not taken literally):
  **For:** Absolutely: scores are model artifacts. We see through [74] that combining scores needed.
  **Against:** Some trivial systems might skip this and just sort by score.
  **Verdict:** Keep; motivates ranker layer.

- **“Retrieval is not ranking”**:
  **For:** Standard IR separation.
  **Against:** Could be merged, but not harmful.
  **Verdict:** Keep separation (for architecture clarity).

- **“Ranking is not selection”**:
  **For:** Ranking orders candidates; selection chooses subset considering interactions.
  **Against:** Many systems just take top-K (so ranking=selection).
  **Verdict:** For thoroughness, we’ll keep them separate, but in practice selection may be trivial top-K initially.

- **“Selection is not representation”**:
  **For:** Selecting what to include differs from how to present it (formatting).
  **Against:** These are clearly different steps.
  **Verdict:** Keep.

- **“DisclosurePlan is not ContextDisclosure”**:
  **For:** The plan is a blueprint; actual disclosure is execution.
  **Against:** Could collapse as noted above.
  **Verdict:** Simplify (COLLAPSE).

- **“ContextDisclosure is not ModelRequest”**:
  **For:** ContextDisclosure is raw content; ModelRequest is formatted prompt including instructions.
  **Against:** Possibly implement as one artifact (the final prompt).
  **Verdict:** Conceptually distinct, but can merge. We keep “ContextDisclosure” as pre-format data, and ModelRequest as the prompt. (But not heavy separate objects.)

- **“Repository data is not authority”**:
  **For:** True in principle: authoritative answer depends on context (e.g. docs might be better for design questions, tests for validation).
  **Against:** Hard to model automatically.
  **Verdict:** The idea is correct but implementation will be heuristic. Keep conceptually.

- **“Execution evidence is not semantic applicability authority”**:
  **For:** Yes: just because a build/test ran successfully (execution evidence) doesn’t prove a code fact.
  **Against:** Minor.
  **Verdict:** Keep (though we may rarely use execution status beyond gating analyses).

Overall, we affirm most invariants but collapse ones that only complicate (like plan vs realized, rank vs select when not needed). The architecture can be simplified in places while preserving its key guarantees.

# AC. Criticism classification matrix

Below is a condensed classification of principal criticisms:

- Foundational defects: *LLM synthesis as DerivedKnowledge*, *too rigid authority semantics*.
- Substantive improvements: *Merge derivation abstraction*, *adopt global symbol IDs*, *unify graph substrate*.
- Simplification opportunities: *Remove InformationNeed*, *collapse evidence objects*, *merge plan/disclosure*, *drop RelevanceEvidence class in favor of features*.
- Valid open design pressure: *Toolcap vs analyzer separation (policy)*, *authority ranking (implementation detail)*.
- Evaluation requirement: *Empirical tests of disclosures: retrieval vs ranking vs selection policies*, *progressive vs one-shot retrieval*.
- Unsupported criticisms: *None identified without basis; issues we found are backed by evidence or practicality concerns.*

Each chosen action balances preserving correctness/incrementality vs undue complexity.

# AD. Post-review architecture

**KEEP (no change):** Content-addressable snapshots, static analyzers with versioned provenance, incremental dependency logic, unified graph substrate, hybrid retrieval+ranking, and major separation of retrieval→rank→selection. Also keep the broad direction of distinguishing static knowledge from LLM reasoning.

**MODIFY (semantic change):**
- Collapse `DerivationDefinition` with execution; unify per-snapshot analyzers.
- Use stable symbol IDs (like hashed signature) rather than snapshot-local only.
- Merge RetrievalEvidence+Ranker into a feature-driven ranker; drop raw `RelevanceEvidence` objects.
- Adopt one combined code graph (like Kythe) instead of disjoint graphs.
- De-emphasize or simplify multi-stage plan: use simpler one/two wave retrieval.
- Drop persisting LLM-synthesized facts (treat them as ephemeral).
- Use a default source-authority ordering (e.g. code > docs) instead of flexible authority per need.

**COLLAPSE (distinctions to remove):**
- InformationNeed vs Query (treat them as same or handle within retrieval).
- DisclosurePlan vs ContextDisclosure vs ModelRequest (just have one assembled prompt object).
- RelevanceEvidence container class (integrate into ranking features).
- Subject vs Graph node where possible (unify identity).
- Possibly snapshot vs delta as separate types (we just compute deltas internally; user sees snapshots only).

**SPLIT / ADD (new or split concepts):**
- Introduce *BuildConfig* or *EnvironmentContext* to capture toolchain state as part of snapshot identity (based on LSIF practice).
- Add support for *workspace state* (unsaved edits) as a transient overlay on snapshots.
- A confidence/uncertainty flag on heuristic analysis results.
- Possibly a minimal *UserAuthority* concept (developer vs system) if needed for security.

**KEEP OPEN:**
- The exact design of progressive retrieval loop and stopping criteria (to be refined in implementation).
- The form of any LLM-verifiable evidence (whether to allow the model to cite facts in answers) – left to experimentation.
- Fine-grained numeric confidence scoring on knowledge (likely unnecessary now).
- Use of learned vs rule-based ranking (both viable).

**DEFER (features for later):**
- Toolchain sandboxes or capability frameworks (security): important, but engineering detail after core pipeline.
- Sophisticated context ordering optimization (beyond basic rank order).
- Large-scale multi-model orchestration (we assume a single model or pipeline to start).
- Full conflict resolution strategies (could add if user feedback demands it).

Each proposed change preserves or clarifies core guarantees. For example, merging graph views preserves the same info just less fragmented; using default authority ordering keeps conflict handling (just simpler).

# AE. Minimum implementable architecture

To start, implement a **minimal viable subset**:

- **Snapshot model:** Accept a content-addressed snapshot per branch (e.g. Git commit or similar). Compute an initial global index of symbols and references (LSIF-style) for that snapshot (ideally incremental updates using file checksums, but can begin with full re-index on changes).
- **Retrieval component:** On a task/query, execute a *combined retrieval*: run BM25 on code text, optionally an embedding search if a model is available. Return top `N` matches with their scores.
- **Simple ranking & selection:** Either trust BM25 ranking or apply a learned linear combiner of BM25+embedding scores to re-rank the top `M` candidates. Then select the top-K (say 5) non-overlapping code snippets (e.g. skip duplicates by file). For now, no complex coverage logic.
- **Context assembly:** Concatenate selected snippets (maybe with headers or code fences), plus the user’s query/instruction, to form a prompt. Do minimal formatting (e.g. “File X: [code]”). This is the ModelRequest.
- **Execution:** Send prompt to model; gather response. Log the answer with its provenance (which snippets were used).
- **Caching:** Store the retrieved contexts and model answers keyed by (query, snapshot) so repeated queries are fast. This handles reproducibility partially.
- **Instrument logging:** Log retrieval results (doc IDs, scores), response, and any error.

This pipeline omits many advanced features but tests the fundamental idea: that a coding agent can benefit from pre-indexed code retrieval. It still enables measuring retrieval vs model performance by toggling, and it preserves reproducibility (given logged indexes and prompt content).

**Immediate needs:**
- Define the index format (maybe reuse LSIF or a simple inverted index).
- Implement or integrate a BM25 engine (e.g. Lucene/Elasticsearch or an in-memory small index).
- Optionally, a vector store (FAISS) for code embeddings if going that route.

**Extension points:**
- Caching partial queries or results.
- Tools for generating symbol references if needed.
- Logging framework for metrics.

We avoid cutting any fundamental kernel: specifically, indexing and retrieval must be in place. Complex layering (planning, trust) can wait.

# AF. Required experiments

To resolve empirical questions, we propose these experiments:

1. **Retrieval vs Context Size:** Using a fixed model (e.g. GPT-4-internal), compare one-shot RAG (retrieve top-K once) vs progressive retrieval (retrieve initial context, answer, then refine with a second query if needed). Measure end-task success and total tokens used. Determine if and when iterative improvement occurs.

2. **Ranking impact:** On a held-out code QA benchmark, retrieve top-10 BM25 hits. Then compare (a) using BM25 order, (b) BM25+embedding score re-ranking (like [74]), and (c) a simple LTR model (if data exists). Measure answer accuracy or retrieval metrics.

3. **Disclosure selection:** For tasks where context length is limited, test simple top-K vs a small diversification (e.g. MMR with moderate weighting). See if diversity yields better code comprehension. This could use existing tasks (like “find relevant code for query X”).

4. **Representation effects:** Present code snippets vs code summaries (e.g. docstrings only) to the model and measure task performance. This tests how much fidelity is needed. Likely find that source-preserving is best.

5. **Derived knowledge usage:** Experiment with caching static analysis results: e.g. run a type checker once and reuse its output. Show benefit in latency. (This is obvious but good to quantify.) More subtle: try a prototype where an LLM-generated summary is *incorrectly* cached and observe failure modes. This justifies not caching.

6. **Local model vs hosted:** Run above retrieval with a smaller on-device model (like Qwen-3B) vs a large model. Check if deterministic context improves weaker model’s answer rates. This addresses the goal of aiding local workers.

7. **Authority conflicts:** If possible, create a scenario with conflicting sources (code vs comment) and see how different strategies (favor code vs offer both) affect user satisfaction. This could be user-study-like or developer survey.

Each experiment should isolate one architectural question (fixed everything else) to see its effect. These will inform which abstractions are actually needed.

# AG. What the research actually falsified

- **Strict insistence on separate InformationNeed and Query:** Evidence shows treating query text directly is common. We didn’t find any benefit to a distinct InformationNeed artifact (no systems do this).
- **Necessity of separate RelevanceEvidence artifacts:** In practice, ranking can use features directly, so the need for distinct evidence objects is overkill. We treat raw scores as features, not knowledge objects.
- **Full multi-graph complexity:** Kythe’s unified graph suggests one graph is enough. We will unify.
- **Treating all LLM output as permanent knowledge:** RAG research indicates generated claims shouldn’t be trusted as facts without evidence. Thus, devtools design of forcing synthesis into the knowledge base is falsified.
- **Highly granular provenance layers:** No evidence that adding an extra provenance object for each step yields practical benefit; too burdensome. Simpler logging suffices.

# AH. What survived serious scrutiny

- **Content-addressed immutable snapshots:** Supported by Bazel/OSTree. This is a solid base.
- **Incremental semantic caching:** Salsa shows it’s feasible and beneficial. Reusing analysis results based on real dependencies is sound.
- **Persistent code analysis index:** LSIF demonstrates the power of precomputed code intelligence. The notion of DerivedKnowledge as immutable facts aligns with that.
- **Separate ranking layer:** Standard IR practice. Hybrid retrieval (BM25+neural with fusion) has proven advantages. The general pipeline (retrieve→rank→select) is valid.
- **Long-context vs RAG:** The superiority of RAG with smaller contexts is empirically shown. This endorses the idea of planning instead of blind context stuffing.
- **Language-agnostic graph:** Kythe confirms the feasibility of a universal code graph for cross-tool queries. This backs having a shared graph substrate.

# AI. What remains empirically undecidable

- **Effectiveness of complex planning:** Does multi-wave retrieval plus provenance-tracked planning significantly outperform simpler fixed retrieval for coding tasks? Only experiments can tell. This depends on task type and model.
- **Value of diversity optimization:** It’s unclear if explicit multi-dimensional coverage planning beats simpler top-K or MMR heuristics in practice. Needs testing.
- **Exact trade-offs in authority ranking:** We cannot decide architecturally how to rank conflicting sources; this likely depends on context (e.g. bug fix vs code explanation). Empirical user studies might be needed.
- **Progressive vs one-shot for local models:** The question of whether small models benefit more from iterative narrowing (versus blowing budget early) is unresolved without experimentation.
- **Granularity of incremental maintenance:** Should we invalidate by file, symbol, or fine-grained? Theory suggests best is *by symbol dependency*, but practicability and performance will guide how fine to go.
- **Representation format (code vs summarized vs partial AST):** We lack hard data on what formats lead to better performance. It may be domain-specific.
- **Derivation granularity:** Do we need multi-result facts vs single manifest? Probably no impact on correctness, only performance.

These questions are best resolved by building prototypes and running benchmarks, as planned.

# AJ. Final conclusion

After rigorous scrutiny, we conclude that **a strongly incremental, provenance-aware retrieval system is justified, but many abstract layers should be streamlined**. The core idea—treating repository context as precomputed, cacheable data—stands. However, the architecture should prioritize essential pieces: content-based snapshots, cached code indexes, and hybrid retrieval with a simple ranking+selection. Complex planning and tracking constructs can be simplified or postponed.

Before building, the team should implement the lean pipeline we described (snapshot → index → retrieve & rank → assemble → model) and run the experiments above. This will ground decisions in reality. In summary, **retain the promise of reproducibility and incremental efficiency, but collapse the over-architected plan/data layers into a more straightforward retrieval workflow**. Only features that demonstrably boost answer accuracy or measurability should survive in the implementation.
