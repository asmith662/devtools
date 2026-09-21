# Repository Information Boundaries: Derivation, Representation, and Context

## Disposition

Status: Reconciled

Canonical research subject: Boundaries among repository derivation, representation, and purpose-relative Context.

Related ADRs: ADR-0002; ADR-0004.

Implemented evidence: bounded source-preserving materialization and rendering.

Accepted: deterministic repository derivation and purpose-relative synthesis remain distinct.

Deferred: concrete authority, conflict, uncertainty, synthesis, and representation mechanisms.

Rejected for now: automatic promotion of model-generated or Context-specific assertions to DerivedKnowledge.

Superseded or refined findings: ADR-0004 provides current transformation-versus-epistemic-derivation vocabulary.

Open questions: validation and reuse of synthesized representations.

Revisit triggers: an identified reusable repository-relative semantic assertion or synthesis consumer.

Reconciliation basis: ADR-0002; ADR-0004; architecture taxonomy.

## A. Executive Conclusion

The investigation finds that **`DerivedKnowledge` is currently overextended** by treating every new semantic assertion as part of the persistent repository knowledge. We recommend **narrowing the scope of `DerivedKnowledge` to truly deterministic, repository-level facts** (with provenance and confidence annotations), and treating interpretive or task-driven inferences as separate, transient artifacts. All assertions should preserve provenance and uncertainty, but **only those grounded in reproducible analysis of the repository (or rigorously validated by independent evidence) should be promoted into the durable knowledge store**. ADR-0004’s rule should be changed: *semantic assertions must be explicit and provenance-tracked, but need not automatically become `DerivedKnowledge`.* Instead, model-generated or purpose-specific claims should by default remain in the “context” layer or in a separate epistemic category, only elevated when corroborated. This avoids **laundering LLM guesses as repository truth** – after all, LLMs can produce confident-sounding falsehoods – while preserving correctness, auditability, and reuse of genuinely deterministic facts.

# B. Current Architecture Reconstructed

The supplied architecture splits **immutable repository state** from **derived repository intelligence**. A `RepositorySnapshot` and its `ResourceOccurrences` (files, code spans, etc.) form the ground truth.  Over this snapshot, *semantic analyses* (the **Derivations**) produce `DerivedKnowledge`: persistent assertions (facts) about the code. Each `DerivedKnowledge` item includes its *semantic content*, its *DerivationDefinition*, explicit *semantic dependencies* (e.g. code AST nodes, call edges), and *provenance/support*. The design promises that any derived fact is traceable to its origin, reproducible by re-running the derivation (for replay or verification), and cacheable across unchanged snapshots.

Separately, the architecture defines an **InformationNeed → Retrieval → Plan → Materialization → Context** pipeline (ADR-0003/0004). A high-level *InformationNeed* (e.g. a user bug query) triggers retrieval of relevant repository elements, guided by `RelevanceEvidence`. A `DisclosurePlan` then selects which code snippets or facts to include, and `ContextDisclosure` materializes them into the prompt.  In sum, the intent is that **static analysis yields a database of repository facts (DerivedKnowledge), and context assembly pulls from that database (plus raw code) to feed the LLM**. For example, Sourcegraph’s platform “functions as an engine that understands code” by indexing all repos and their code symbols, and Cody (Sourcegraph’s assistant) uses RAG (retrieval) to include relevant code context with each query. This mirrors the design: repository facts are stored (like a code index), and model input is assembled by retrieval from that store.

# C. Strongest Case for Current Architecture

The **`DerivedKnowledge` abstraction has strong motivations**. By capturing analysis results as first-class objects, we get:

- **Reproducibility and determinism.** Only deterministic analyses are stored, so we can always re-run and verify facts. Systems like Sourcegraph explicitly separate *imprecise, on-the-fly* search results from *precise, index-based code intelligence*. DerivedKnowledge behaves like a materialized view: once computed, it yields stable answers without recomputation. Incremental maintenance (analogous to database IVM) can update only what changed, rather than recomputing everything.

- **Explicit provenance and auditability.** Each fact carries its derivation, dependencies, and source references. This is crucial for trust: provenance metadata enables “deterministic grounding for reasoning” and is foundational for explainable AI. In practice, KGs and data platforms attach source URIs, timestamps, and derivation steps to facts so one can answer “where did this come from?” rather than treating it as opaque.

- **Stable referability and reuse.** Facts in DerivedKnowledge can be indexed, cached, and re-used across queries and snapshots as long as dependencies hold. Like materialized views in a database, these stored inferences avoid redundant work. They enable efficient search over semantic relations (e.g. call graphs, symbol tables) rather than purely text search.

- **Correctness and testing.** Storing derived facts allows offline evaluation: one can unit-test the analyzer that produces DerivedKnowledge, detect regressions, and measure factual accuracy. In contrast, if all analysis results were hidden in the model pipeline, testing would be harder.

Thus, a properly-scoped DerivedKnowledge supports correctness, caching, and auditability in a way that opaque “one-shot” context generation cannot.

# D. Falsification: Challenges to Current Architecture

Despite these benefits, **forcing every semantic claim into `DerivedKnowledge` has downsides**:

- **Mixing task-specific and general knowledge.** Not all useful reasoning should inflate the global repository store. For example, lexical TF-IDF or graph distance scores help rank code for this particular query, but do not represent enduring code facts. Even deterministic, reproducible evidence (like “function *f* is reachable from *g* in 2 hops”) is *purpose-relative* and might vary with what path one seeks. Our precedent was `RelevanceEvidence`: these are deterministic, record query-specific relevance cues (documented as provenance-bearing) but we decided **not** to make them DerivedKnowledge. Similarly, contextual inferences (why A is relevant to bug X) should not silently become repository facts.

- **LLM hallucinations and brittleness.** Model-generated statements can appear authoritative but may be wrong. For example, an LLM might assert *“This module uses a façade pattern”* or *“Payment is validated before fraud check”* without explicit code evidence. If we promote such claims to DerivedKnowledge, we risk *laundering* them as facts. In truth, they are hypotheses that might require external validation. The Nature study on hallucinations showed that models “fabricate specific, confident responses” rather than admitting uncertainty. Architecture must guard against treating these fabrications as canonical.

- **Epistemic mismatch.** Static analyses often produce **over-approximate** or **conservative** results (e.g. “possible call from A to B”) rather than absolute truth. Lumping all these into an untyped ontology conflates certainty levels. For instance, Sourcegraph’s “search-based” code intelligence (regex matches) is fast but imprecise. If we consider every possible match as a firm fact, we could propagate errors.

- **Excessive storage and complexity.** Converting every intermediate into a durable artifact leads to a “knowledge explosion.” Many transformations (e.g. composite signature reports, context bundles) have no intrinsic meaning beyond representation. Creating IDs and schemas for every nuance (compression vs projection vs synthesis) invites needless complexity. History in information systems suggests favoring a simpler core ontology and keeping ephemeral data in logs.

- **Provenance confusion.** Although provenance helps, it doesn’t guarantee truth. If we overload DerivedKnowledge with interpretive claims, we mix raw facts (supported by code) and conclusions (supported by LLM heuristics) under one roof. The system might give undue weight to well-proven but still uncertain inferences. In contrast, separating them maintains a clear provenance-based distinction: “this claim is backed by code; that claim comes from an agent’s reasoning.”

In practice, leading systems illustrate this split: e.g., CodeQL or Kythe store code relations (defines, calls) derived from static analysis, but they do not incorporate LLM interpretations or IR ranking signals into the code index. Retrieval-augmented systems (Sourcegraph Cody, Cursor) **keep the model’s output out of the knowledge store**. Instead they pass retrieved facts *into* the model, without writing model outputs back to a central repository. This architectural pattern suggests that *DerivedKnowledge is best kept for true repository facts*, while model-driven synthesis should stay in the execution context or a separate layer.

# E. Taxonomy of Derived Information

We distinguish several distinct transformation types. Not all should become permanent facts:

- **A. Structural/Semantic Repository Fact** (e.g. “Method `A` calls `B`”): **Natural DerivedKnowledge.** It’s a concise semantic assertion grounded in code structure.

- **B. Deterministic Projection** (e.g. “A calls B, C, and D”): This is a trivial aggregation of A, so it doesn’t add new knowledge per se. It can be derived on the fly or stored; if reused often, caching makes sense, but semantically it’s equivalent to multiple A-statements.

- **C. Deterministic Aggregation** (e.g. “Module `M` has 27 public functions”): This is a numeric summary of facts. It can be stored as DerivedKnowledge if useful (like a materialized summary), but one must track its dependencies (function list). If only needed on demand, it could be computed at request time rather than as a first-class fact.

- **D. Deterministic Relational Synthesis** (e.g. “`A` transitively reaches `C` through `B`”, or “`A,B,C` form a cycle”): These are new semantic facts computed by graph analysis. They seem valid as DerivedKnowledge, since they reveal implicit structure not explicit in a single source. They are reproducible and repository-relative, so arguably fit ADR-0002.

- **E. Source-Preserving Transformation** (e.g. “extract method signature”, “pretty-print code”): No new semantics, just change of representation. This should *not* be treated as DerivedKnowledge. It belongs to materialization (formatting) rather than knowledge.

- **F. Composite Representation** (e.g. packaging together signature, callers, tests as one unit): Merely a convenient assembly for display. It yields no new fact beyond its parts. Thus it is a representation artifact, not separate knowledge. It can be materialized per request but doesn’t need an ID or provenance beyond its components.

- **G. Lossless Compression** (e.g. encoding ASTs in a compact form): If it’s truly lossless, it’s just a representation of existing knowledge. One might store it for efficiency, but conceptually it isn’t new information. It belongs with representation/materialization, not semantic substance.

- **H. Lossy Compression/Summarization** (e.g. “Payment flow: validate → fraud-check → persist”): This abstracts away detail. Such summaries can mislead if over-trusted. They should **not** be in DerivedKnowledge unless they meet strict criteria (see D & I). Usually better treated as ephemeral in-context hints.

- **I. Semantic Synthesis** (e.g. “PaymentService coordinates validation, fraud, persistence”): This is an interpretation not directly in code. It is neither a raw fact nor a deterministic derivation. It’s the kind of useful insight an LLM might produce. It should be *tagged as interpretive, task-independent knowledge* only if corroborated (e.g. found in architecture docs). Otherwise, it remains outside the repository knowledge core.

- **J. Architectural Interpretation** (e.g. “This implements an outbox pattern”): High-level inference about design intent. Valuable but inherently subjective. It belongs to documentation or analysis commentary, not core `DerivedKnowledge`. If captured, it must carry heavy caveats and provenance (e.g. “source: architecture doc or LLM”), but likely not reified as repo knowledge.

- **K. Task-Relative Synthesis** (e.g. “For bug X, relevant path is C→D→E”): This is explicitly purpose-specific. It should *not* be global repository knowledge. It can be returned in the context disclosure for the current bug, but caching it as a repository fact (without context) would be meaningless or misleading for other tasks.

- **L. Retrieval Observation** (e.g. “Method `M` was ranked 2nd for query Y”): This is evidence of the retrieval process and query, not of the repository itself. It is per-query data. It should be tracked for reproducibility of the run (logs) but not stored as DerivedKnowledge.

- **M. Ranking/Selection Reasoning** (e.g. “We chose `M` over `N` because… unsatisfied coverage”): This explains context planning decisions. It is context-specific and non-repeatable outside that plan. It belongs to the disclosure plan/log, not to repository knowledge.

Each category suggests a treatment:

- **Repository-derived facts (A, D)** should be `DerivedKnowledge`.
- **Deterministic aggregates/heuristics (B, C)** could be derived knowledge if validated frequently; otherwise, they can be recomputed as needed.
- **Source transformations & representations (E, F, G)** are **not new knowledge**; they belong in the materialization layer.
- **Summaries and syntheses (H, I, J)** are *knowledge-like* but require clear labeling. They might appear in context but should carry provenance/confidence (or remain ephemeral).
- **Task-specific or retrieval data (K, L, M)** are ephemeral and should **not** be stored as repository knowledge.

In short, **`DerivedKnowledge` should represent content that is repository-intrinsic and stable.** Transformations or context-driven insights should either live in the context engine or have a distinct marker outside the core ontology.

# F. Epistemic Derivation vs Representational Transformation

A useful boundary is **“does it assert new semantic content?”** Epistemic derivation produces assertions that can be true or false (e.g. call relations, dependency paths). Representational transformations merely change how information is expressed (e.g. pretty-printing, signature extraction). If the transformation does not *intend* to assert something beyond what’s in the source, it is purely presentational. For example, extracting a method’s signature from code is just giving a canonical view of the code fact (the code already *is* that signature); no new knowledge is created. In contrast, computing “`A` transitively calls `C`” is a new fact inferred from the call graph.

This distinction is foundational: **only epistemic derivations (new assertions) warrant provenance and potential storage**. Representational changes should be reversible and don’t need a semantic identity. Architecturally, repackaging or formatting should remain in materialization or formatting code, not become tracked knowledge. Thus the boundary is: if something is a *logical consequence* (a claim) rather than just a *representation variant*, it belongs on the knowledge side. This is analogous to the way databases treat views: a view that computes a new join-result is different from simply showing the table rows in a new format.

# G. Deterministic Repository Intelligence

The architecture’s emphasis on determinism is largely sound: repository facts should come from stable analyses, not from fluctuating models. This ensures reproducibility and cacheability. However, determinism should not be taken to mean “perfect truth.” Many static analyses are deterministic but **approximate** (sound or complete with respect to some assumptions). The ontology could allow **qualitative tags** or confidence scores on DerivedKnowledge.

For example, a static analyzer might deterministically assert “may-call(A,B)” versus “must-call(A,B).” Both derive from code but have different epistemic status. Our architecture could model this by flagging uncertain facts or by having separate fact types (e.g. “possible call” vs “confirmed call”). The current design doesn’t forbid this, but it should allow it: not all determinism implies certainty.

There’s room to question whether *only* strictly deterministic processes should feed DerivedKnowledge. One might consider including the outputs of heuristic or learned code analyses if they are reproducible given the same inputs. For instance, a neural parser that deterministically produces an AST (when seed is fixed) could arguably feed facts. The key is not *how* the fact is computed, but whether it is stable and justifiable. Even temperature-zero LLM calls are not truly bit-for-bit deterministic (and their “training sources” are opaque), so they should not directly generate DerivedKnowledge without vetting.

Thus, we keep the principle: **repository knowledge is to be produced by reproducible processes** (whether classical or learned) and to the extent possible be deterministic. Heuristics can contribute, but their results must be treated with caution (e.g. labeled as “heuristic result”). The boundary should remain that *evidence* used in derivations is deterministic from repository state. At the very least, **replayability** is crucial – if we run the derivation steps again on the same snapshot, we should get the same fact (even if it’s just “possible call”).

# H. Heuristic/Probabilistic Analysis

In practice, many static analyzers already embed heuristics or probabilistic models. This means a **firm-cut “deterministic vs LLM” dichotomy is too simplistic**. For example, a Python type inference engine might guess types via patterns; a call graph tool might use machine learning for incomplete code. These outputs may not be true facts but have utility. Should they be DerivedKnowledge? Possibly, but with explicit uncertainty.

The architecture should accommodate **confidence or status fields** on DerivedKnowledge. For example, a fact could be tagged *“likely”*, *“possible”*, or carry a numeric confidence. Indeed, [29] suggests storing confidence in provenance metadata. Knowledge graphs can annotate triples with certainty scores. We might likewise allow a DerivedKnowledge tuple to include a confidence score or an evidence list. This blurs “derived knowledge” and “evidence” but enriches the representation.

So rather than excluding all non-certain outputs, we can extend `DerivedKnowledge` to have epistemic qualifiers. The rule should be: if an analyzer deterministically emits a claim (even if uncertain), *it can be recorded*, but **with an epistemic tag** (e.g. “this is a heuristic inference”). Purely speculative inferences (like an arbitrary LLM claim) would require an even weaker tag or be kept out of the core and treated like comment. Thus, heuristic analyzer claims can qualify as DerivedKnowledge, provided their uncertainty is explicit. The metadata/provenance model (see next sections) must then distinguish them, and evaluation tools must track their reliability.

# I. LLM-Generated Knowledge

LLMs can generate extremely valuable insights (e.g. summarizing a module’s role) that static tools struggle with. However, they are **inherently nondeterministic and opaque**. Therefore, **LLM outputs should *not* automatically become `DerivedKnowledge`**. They should enter the system as *observations to be scrutinized*. Possible approaches:

- Treat LLM claims as **evidence** or annotations, not base facts. Keep them in the context/disclosure layer with provenance (model version, prompt, temperature). They inform the model dialogue but are flagged as “from LLM” and carry no intrinsic authority.

- Only **promote an LLM-generated assertion** to DerivedKnowledge if it is validated. Validation could be: a subsequent deterministic analysis confirms it, or a human curator agrees, or multiple independent models corroborate it. At that point, it is no longer just a model’s guess. Some teams call this “fact-checking” the LLM output. It might require an extra pipeline step (e.g. ask the LLM to provide sources, cross-check with search). If validated, it becomes a new static fact, but with attached proof.

- Even when an LLM is used with temperature=0, it is not necessarily truth-preserving. It may still hallucinate confidently. The Nature study warns that models “optimizing accuracy… incentivize guessing over admitting uncertainty”. A zero-temp model might still produce plausible falsehoods if the data isn’t explicit. We must not confuse a deterministic call to an LLM with a classical deterministic analysis.

- If we want to capture some interpretive knowledge, we might extend DerivedKnowledge with an epistemic type (like “inferred_by_model” vs “inferred_by_analysis”). Alternatively, use a separate concept (see comparisons below). The key is, **model-produced info is second-class until corroborated**. By default it should remain local to the context plan (e.g. a `ContextInsight` object), not stored globally.

In short, **LLM contributions should by default remain outside `DerivedKnowledge`.** The latter stays the domain of reproducible repository facts. If we do bring a model insight in, it must carry a provenance chain including the model/prompt and likely an uncertainty weight (e.g. a probability or grade of confidence). This prevents “hallucinated pattern” from becoming canon. Provenance here is not enough; the system also needs a mechanism to question and update or discard such assertions.

# J. Provenance, Support, Authority, Confidence, Uncertainty

A central tenet: **Provenance is not the same as authority.** Attaching a source to a claim only shows where it came from, not whether it’s true or primary. For example, a claim “X calls Y” might be derived from code (strong authority) or guessed by a model (weak authority), even if both are recorded with provenance.

From knowledge representation practice, we should store *who/what produced each fact, when, and how*, but also track *credibility and type* of that producer. Potential distinctions:

- **Source Role:** Tag whether a source is e.g. “original code”, “static analyzer v3.1”, “LLM(WinogradPrompt)”, “user-assertion”. Analyzers and code are high-authority, while model or user claims may be lower.
- **Evidence/Support:** List of underlying items justifying the fact (e.g. specific AST nodes, test cases, documentation citations). If multiple independent supports exist, confidence can rise.
- **Epistemic Status:** One could label facts as *certain*, *likely*, *possible*, etc., based on the method. For example, an LLM claim might default to “hypothesis”, whereas a static analysis result is “inferred_fact”.
- **Confidence Score:** Numeric or categorical score indicating belief strength (some KGs use probabilities). The probabilistic KG example shows explicitly combining evidence to yield “99% confident” rather than a binary flag. We might borrow this: each DerivedKnowledge could include a confidence metric.
- **Time/Version:** When the fact was derived and by what version of analysis tools or models (part of provenance). This helps in change management and known drift.

By including these fields, the system can reason about trust: e.g., if two sources conflict, the one with higher authority or confidence might be preferred, or both could be kept with comments. The provenance metadata should answer: *what type of claim is this, and who made it?* As Inference Systems notes, provenance tracking in KGs links each fact to its origin and derivation steps, which allows transparency. But we should *not* collapse all such metadata into a single “score” – each axis (source, confidence, method) is meaningful. For instance, a chain-of-custody model (immutable logs) is useful for audits, but authority judgments happen at a higher reasoning level.

In practice, a fact record might look like:
```
Claim: A calls B (exact)
Provenance: determined by static analyzer S (v2.4) at timestamp T, based on AST from file F at commit C.
Confidence: 1.0 (sound analysis)
Status: confirmed.
```
versus
```
Claim: A handles exceptions in B (interpreted)
Provenance: LLM ChatGPT-4 (prompt P) at time T, supported by doc: [patentXYZ].
Confidence: 0.65 (heuristic).
Status: hypothesis.
```

Such distinctions allow the system (and the human user) to see that the first is authoritative code-derived knowledge, while the second is a model guess that should be treated cautiously. Importantly, **no design should obscure the difference between “fact” and “claim” or automatically trust everything with provenance attached.**

# K. Conflict and Completeness

**Conflict preservation:** The architecture must allow *coexistence* of contradictory evidence rather than silently merging it. For example, if the implementation suggests one behavior and documentation suggests another, both should be tracked. This is akin to a truth-maintenance system in AI: it keeps multiple “justifications” for beliefs. We should avoid laundered summaries. A `DerivedKnowledge` item might even explicitly record that “source A asserts X, source B asserts not X,” flagging a conflict. The model-input could then highlight the discrepancy, rather than suppress it. This helps debugging and ensures the agent doesn’t become overconfident.

**Completeness and absence:** We must also not treat missing information as negative evidence. Just because we found no call from `A` to `B` in a partial analysis doesn’t mean it never happens. Summaries must qualify claims. For example, saying “A never calls B” is only valid if the analysis was exhaustive. Instead, a safer phrasing is “no calls A→B were found in the tested code under the given assumptions.” In repositories, there may be hidden files or dynamic behaviors. The provenance should include the *scope of analysis*: e.g. “within module M’s static call graph (incomplete in Python)”. In knowledge graphs, data lineage tools often compute a *completeness ratio* to explain missing data. We should do similar: every DerivedKnowledge should note if it’s contingent on assumptions (e.g. “static analysis with no runtime info”). In essence, missing facts should be treated as “unknown” unless guaranteed by the type of analysis. Our system can use provenance to determine if an assertion implies absence (e.g. only a sound, complete analysis can prove no-calls); otherwise it stays tentative.

# L. Purpose and Applicability

**Repository facts vs. task relevance:** By design, repository `DerivedKnowledge` should be task-agnostic: it encodes what the code *is*, not what the current goal *needs*. The statement “`A` calls `B`” is always true in that repo (assuming we have analyzed it). In contrast, “`A` is relevant to bug X” depends on the task (bug X’s context). The architecture already respects this by distinguishing core knowledge from query-specific evidence (information need, relevance).

Concretely, **purpose-relative inferences should generally *not* become part of the reusable knowledge base.** For example, if we infer that “the failure path for bug Y goes through modules M→N→P”, that is only meaningful for that bug. Caching it globally as fact “M→N→P is a critical path” could mislead another query. Instead, such inferences should remain tagged with their purpose (e.g. with a bug ID or model session ID).

That said, some meta-knowledge might be reusable. For instance, if multiple bugs consistently implicate the same module, one might learn a generalized fact about it (e.g. “Module M has many uncaught exceptions”). But even then, this should probably come from aggregating many queries offline, and with careful statistical treatment, not from any single context build.

In summary, **`DerivedKnowledge` should contain broadly valid facts**. Anything tied to a specific InformationNeed or user intent is in the context scope. This separation avoids contaminating the general knowledge graph with specialized claims.

# M. Context Preparation Responsibilities

To avoid conflation of concerns, we propose clearer boundaries for each stage:

- **Disclosure Planning:** This stage should *select* from existing knowledge (source content, DerivedKnowledge facts) and possibly request standard transformations (e.g. get this function’s snippet). It **should not compute new semantic assertions**. It can decide which pieces of knowledge or code to include, and which known summarizations to apply (e.g. “use function signature and docstring”). The plan could include placeholders for later steps (like “include call graph snippet of X”). But it defers creation of any new information until materialization.

- **Materialization:** This stage *executes* the plan by retrieving and formatting the selected elements. It should realize the plan via retrieval and any required transformations (e.g. truncating code, generating a summary). It still should not inject new facts arbitrarily. If summarization is part of the plan, it will call the model to produce that summary, but that output should be treated as labeled evidence (not as feed for other steps unless explicitly used in plan). Materialization can annotate content with provenance. If it performs any synthesis (like summarizing or translating code to pseudocode), it should record that as a model call with associated uncertainty. But it should not write these syntheses back into DerivedKnowledge unless a validation sub-step exists.

- **ContextDisclosure:** This final assembled context may include native code, documented DerivedKnowledge facts, and optional synthesized text (with provenance notes). The architecture should ensure that everything in the context is traceable. Ideally, each segment of the disclosure can be linked back to either a `ResourceOccurrence` or a `DerivedKnowledge` id or an LLM query ID. The context is essentially ephemeral and tailored for the model. It may certainly contain interpretive material if needed, but again with provenance markers.

- **Model-Input Assembly:** This is purely representational (templating, ordering). It should not alter semantic content. It may drop low-priority items if token budget is exceeded (as in Cursor’s Priompt). If so, those items were already in the plan, just omitted. It should never *combine facts* or infer during assembly — its job is to format the disclosure into a prompt. Any summarization/truncation here must not change meaning: it should only remove or compress (e.g. “omit the middle lines”, not “paraphrase the logic”).

In sum, **only dedicated analysis components should create or modify semantic facts**. Context planning picks and chooses what to show, materialization renders it, and assembly packages it. If any step needs a new assertion (e.g. “summarize this function”), that is technically a query to the model (like a subtask) and should be tracked just like any other model call. That output can appear in the context but must carry the flag “generated synthesis” – it should not retroactively alter `DerivedKnowledge` unless there’s an explicit pipeline to evaluate and ingest it.

# N. Compression and Summarization

Compression and summarization blur lines between transformation and synthesis. We distinguish:

- **Source-Preserving Extraction:** Pulling out relevant pieces (e.g. just the signature or docstring) is lossless relative to repository meaning. This is fine as representation work.

- **Deterministic Structural Summary:** E.g., generating a control-flow graph or an AST skeleton. These compress but systematically (could even be lossless structurally). They can be derived knowledge if stored as a formal artifact, but usually they’re just for display. If stored, treat them as data linked to source, not as independent facts.

- **LLM-Generated Summaries:** E.g., “This module implements a pipeline…” are lossy and not guaranteed factual. They should **not be in DerivedKnowledge**. They can appear in context to aid the model, but always flagged as “LLM-synthesis”. Given the high risk of hallucination in summarization tasks, treat these as “nuggets to double-check” rather than knowledge base entries.

- **Task-Conditioned Summaries:** Summaries shaped by the specific question (e.g. summarizing error-handling because the bug is an exception). These are doubly contextual: both lossy and purpose-relative. They belong entirely in the context construction step and should not persist.

Thus, compression differences matter: any **lossy compression (summarization)** that reduces or abstracts information can create **new assertions implicitly** and must be treated like a synthesis. Unless a summary can be verified by code, it cannot be trusted as DerivedKnowledge. In practice, it’s safest to keep such compressions out of the knowledge store; at most, one might cache certain *validated* canonical summaries (like a proven design pattern description) but only as documented facts.

# O. Identity, Lifecycle, Persistence, and Caching

Not every semantic element needs a global ID or storage. We should minimize what we persist:

- **Durable facts:** If something is truly repository knowledge (call graph edges, type relations, etc.), it should get an identity (maybe a tuple key) and live in the DerivedKnowledge store. These have life-cycle tied to repository snapshots.

- **Ephemeral composites:** Items created only for context (like a synthesized answer explanation or a one-off summary) need no permanent ID. They should be logged in the execution trace (for replay/eval) but not appear in the persistent graph.

- **Aggregates & caches:** Some aggregates (e.g. “module contains N functions”) could be stored if they're queried often and cheap to maintain. But they could also be computed on demand with cached dependencies. If we store them, we should only do so when it benefits performance, not as a conceptual necessity.

In essence, follow the principle “if it’s knowledge in multiple contexts, give it an ID and store it; otherwise, keep it local.” As with `InformationNeed` and `RelevanceEvidence`, the team wisely decided not every important piece needed a stable object. Similarly, we should not auto-ID every analysis output unless we need to reference it repeatedly. The lowest burden is to keep intermediate synthesis in the run context. Only when reuse is justified do we promote it.

# P. Evaluation and Replay

To measure the system’s effectiveness, we must retain enough records:

- **Factual correctness:** We should log which repository facts were retrieved and used. Evaluators can then check them against ground truth code or test cases. For example, if we said “A calls B” in context, that should match reality.

- **Synthesis fidelity:** For any generated summary or interpretation, we must compare it to the source. This could mean storing the original content (e.g. code snippet) and the LLM output, so we can annotate discrepancies. Tools exist to highlight “hallucinations” in summaries.

- **Retrieval quality:** We need to evaluate how relevant the retrieved code was for the task. For reproducibility, we should log the retrieval queries and resulting `RelevanceEvidence` scores.

- **Context usefulness:** Ultimately we measure task success (bug fixed, user satisfied). But intermediate signals matter: did the agent answer queries faster, with fewer tokens? Did context compression save tokens without losing needed info? These require logging both what was included and what was omitted due to budget. Cursor’s Priompt, for example, could report how many tokens each element contributed.

- **Hallucination/unsupported-rate:** By comparing outputs to provenance, we can compute how often the model guessed vs used a fact. If an answer statement has no backing in DerivedKnowledge or source code, that’s a hallucination. We should track this metric over time.

- **Caching efficiency:** We must verify that cached facts are invalidated correctly when code changes. Replay logs can include snapshots used, cached keys hit, etc.

We **do not need separate, formal objects for every intermediate** to evaluate. Instead, execution logs and context transcripts can suffice. For each model request, we should record: the user query, selected DerivedKnowledge ids, retrieval sets, any new synthesis (with its provenance), and final prompt. With this, we can replay the entire context construction and check each piece. This is akin to a provenance audit trail. As the Provenance systems literature notes, having an **immutable audit trail** answers *what was added when and why*. We should adopt that discipline: record every artifact (facts or syntheses) with its source info, even if it’s ephemeral. In practice, storing logs or append-only records may suffice without forcing every artifact into the persistent database.

# Q. Comparative Architecture Analysis

We consider four families (A–D) plus any stronger alternative, evaluating each dimension:

- **Architecture A — Broad DerivedKnowledge:** One unified assertion store where *any* derived claim (deterministic or model-generated, heuristic or certain, query-specific or general) is treated equally except for attached metadata.
  - *Clarity:* Low, since facts, guesses, and context all mingle under “knowledge.”
  - *Correctness:* Risky — authority/confidence must be encoded in each, else we conflate truth.
  - *Provenance:* Centralized, which is good; but we might overload provenance with purpose info (was this for bug X?).
  - *Incremental Applicability:* Complex keys would have to include task and model parameters in dependencies — heavy burden.
  - *Caching/Reuse:* Everything is cached the same way; e.g. a summary from bug X might get reused for bug Y erroneously unless marked.
  - *Evaluation:* Hard to evaluate, because distinguishing errors vs valid inferences requires digging into metadata.
  - *Complexity:* Highest — effectively a “god-object” store, mixing static and dynamic.
  - *LLM Integration:* Feels forced; we’d store LLM outputs as facts, risking hallucination propagation.
  - *Elegance:* Intuitively simple (“one knowledge base”), but semantically fragile.
  - *Risk:* **Authority laundering** is most likely here. The model’s guesses could seem as authoritative as code-derived facts because they share the same medium.

- **Architecture B — Narrow DerivedKnowledge + Synthesis Concept:** Keep DerivedKnowledge as repository facts only. Introduce a parallel concept (call it `SynthesisArtifact` or similar) for all model/heuristic outputs.
  - *Clarity:* High — there’s a clear demarcation. One could even have two classes of nodes in the knowledge graph.
  - *Correctness:* Better, since model guesses live in a different bucket, the system can treat them with extra checks.
  - *Provenance:* Both types have provenance, but we know which is which. Could reuse the same provenance fields (source, time) but `SynthesisArtifact` might require extra fields (e.g. “model prompt”).
  - *Incremental:* Some separate logic for updating synthesis artifacts (likely most are ephemeral) vs persistent facts. Maybe maintain a cache of some validated syntheses, but they’d have separate dependency rules.
  - *Caching/Reuse:* `DerivedKnowledge` cache as usual; `SynthesisArtifact` might only cache per session or be short-lived, avoiding misuse.
  - *Evaluation:* We can evaluate errors in each category separately. Good.
  - *Complexity:* Moderate — one extra class, but it aligns with the existing distinction between repository and context.
  - *Flexibility:* Good: we can later evolve `SynthesisArtifact` concept (e.g. add categories: summary, hypothesis, explanation).
  - *Risk:* Lower — minimal chance that an LLM claim sneaks into the core facts unless explicitly promoted.
  - *Implementation:* Relatively straightforward extension of current design.
  - *Overall:* This seems promising: it preserves all benefits of DerivedKnowledge for static intelligence while giving us a *first-class handle* on everything else.

- **Architecture C — Narrow DerivedKnowledge + Mostly Ephemeral Synthesis:** Similar to B but without a persistent “synthesis” schema at all. DerivedKnowledge remains only static facts; everything else is purely ephemeral execution state/logs.
  - *Clarity:* Simple ontology — only facts are formal, everything else is just data in a workflow.
  - *Correctness:* Good in the sense of not mixing fact types, but we risk losing traceability. We have to rely on execution logs to recall what was said.
  - *Provenance:* Only facts have structured provenance; contextual info’s “provenance” is just logs. Could still link it to a session ID.
  - *Incremental:* No worry about caching syntheses.
  - *Caching/Reuse:* DerivedKnowledge is cached normally; nothing else is cached (except maybe retrieval results).
  - *Evaluation:* We need to save execution traces for evaluation. That’s doable but maybe heavy.
  - *Complexity:* Easiest on the data model side. But the external logging system needs to be robust.
  - *Risk:* Lower as long as logs capture everything. The danger is if logs are incomplete or not queryable. Also, losing identity means difficult to query “what hypotheses do we have about X?” without a schema.
  - *Overall:* This is very lean. It risks forcing all contextual reasoning to be re-done for replay, but avoids polluting the knowledge base.

- **Architecture D — Shared Assertion Substrate with Profiles:** Use one assertion/provenance dependency model but mark each assertion with a *semantic profile/type*. For example, a fact could be tagged “DeterministicFact,” “HeuristicInference,” “LLMHypothesis,” etc. The storage layer doesn’t care beyond linking dependencies; semantic differences are metadata.
  - *Clarity:* Good if enforced carefully. One object type but with a “kind” attribute.
  - *Correctness:* As with B, we segregate in logic by type. But risk is if queries ignore the type. The system must always check the profile when using an assertion.
  - *Provenance:* Unified, because provenance is generic (source system, agent, time, etc.). We’d add one more attribute “schema/epistemic type”.
  - *Incremental:* All assertions live together, but the identity/dependency system is uniform. Could get complicated if we let an LLMHypothesis depend on stuff. Probably OK.
  - *Caching/Reuse:* Facts of all types could be cached; but heuristics/hypotheses should have extra cache keys (including model/prompt). This is doable.
  - *Evaluation:* The content is all in one graph, easier to query. But potential to inadvertently use a “wrong type” if profiles aren’t strictly enforced in logic.
  - *Complexity:* Slightly higher than B (we do need a taxonomy of profiles), but avoids duplicating infrastructure. It’s sort of a union-of-B and-C.
  - *Flexibility:* High — new epistemic categories can be added as new profile values without schema changes.
  - *Risk:* Moderate. If not careful, an LLMHypothesis might get mistaken for a DeterministicFact. However, with the profile field and proper API safeguards, we can minimize that.
  - *Overall:* This tries to keep one data store but semantics layered on top. It may be the simplest to implement (less code partitioning) while preserving semantic separation.

- **Architecture E — Other (Hybrid or Novel):** We may conceive e.g. a multi-tier knowledge base: one tier for hard facts, one for soft inferences, one for query logs, etc. Or a streaming/event-sourcing model where DerivedKnowledge and Synthesis are events. Without a concrete idea, we note that any richer scheme must still answer to simplicity: **introduce only what correctness demands.**

**Summary of tradeoffs:**

- The *broad-all-in-one* (A) is easiest to conceive but dangerously mixes epistemic levels. It likely fails correctness and applicability (e.g. caching fact vs hypothesis).
- *Narrow+explicit synthesis* (B) and *shared substrate with profiles* (D) are both viable: they separate static vs inferential content. B has two object types, D has one with typed metadata. Both allow similar functionality: they just distribute information differently.
- *Narrow+ephemeral* (C) is simplest but demands heavy logging; it might be safest epistemically but could hinder later analysis (we lose identity of context artifacts).
- Based on evidence and clarity, a **two-tier approach (B or D)** seems best. For example, [28]’s probabilistic KG uses a unified graph with contexts and probabilities attached. But here we might prefer either distinct classes (B) or a type field (D). The key is to maintain *semantic clarity* in use: queries should rarely mix tiers unless explicitly allowed.

# R. Recommended Architecture

**We recommend a hybrid: keep `DerivedKnowledge` narrow (deterministic repo facts) and introduce a distinct handling for everything else.** Concretely, we suggest something like Architecture B or D above. For concreteness:

- **`DerivedKnowledge` remains for repository facts**: conditions and relationships verifiable by code and analysis. These continue to require `DerivationDefinition`, dependencies, provenance. We may add metadata for confidence/ status to handle heuristic cases, but core usage stays the same.

- **Introduce a *second envelope* for non-repository assertions**, say `AssertiveClaims`. These hold any new semantic assertions (summaries, bug-paths, LLM inferences). They carry full provenance (model details, analysis rules, etc.) but live separate from DerivedKnowledge. They can be persisted or ephemeral: by default ephemeral within the context, but if an assertion gets validated or flagged as important, it could be lifted into a moderated knowledge store (perhaps even into DerivedKnowledge after review).

- All assertions (both types) should share a common backend schema for provenance/dependencies (perhaps the same database table with a discriminator column). But *logical* distinction matters: the system will treat `DerivedKnowledge` as authoritative, use it in any analysis, and only use `AssertiveClaims` when specifically requested (e.g. “show me all LLM-sourced notes on this function”).

- The **Context Disclosure** can present both but should clearly label them. For example, color-code or annotate “(suggested by model)” vs “(from code analysis)”. This prevents agent or user confusion.

- **ADR-0002** should own “truthful, reproducible semantic repository knowledge.” It continues to define how to identify repository subjects, dependencies, and facts. We would refine its definition to say *“DerivedKnowledge: reproducibly derived, repository-relative facts (possibly with confidence tags)”*. It should explicitly exclude purpose-conditioned or model-only assertions, which ADR-0002 will not cover.

- **ADR-0004** should own context planning and context artifacts. Its section on “semantic assertions become DerivedKnowledge” should be weakened: we’d rephrase it to “semantic assertions must be explicit and provenance-carrying, but may remain in the context layer unless validated as repository knowledge.” ADR-0004 will need to clarify what context vs knowledge means, likely referencing the new `AssertiveClaims` concept.

- We do **not** believe a wholly new top-level ADR is needed, but rather revision of 0002/0004. However, it may be useful to call out an architectural guideline about LLM vs static knowledge handling (perhaps as an amendment or an ADR-0005).

- **ADR-0003** (InformationNeed/Retrieval) is mostly orthogonal, but we should ensure it understands that retrieved facts should be pulled from DerivedKnowledge (static) or raw code, not from a flooded knowledge pool of ephemeral claims. It may be fine as is.

This architecture cleanly separates stable repo intelligence from on-the-fly synthesis. It preserves correctness and provenance by not blurring them. It remains simple: at its core, we still have one graph of assertions, but they are semantically typed. This should support caching of true facts across sessions, while still allowing us to capture “intuitions” during a run without polluting the core.

# S. ADR Impact

Based on the above, here are concrete impacts on the ADRs:

- **ADR-0002 (`Repository Intelligence and DerivedKnowledge`):**
  - *Continue to own:* Deterministic, schema-defined knowledge about the repository state. This includes code relationships (calls, definitions, types), structural summaries, etc. DerivedKnowledge remains the durable store for things that can be justified by repository content and reproducible analysis.
  - *Stop owning:* Ephemeral or interpretive assertions. In particular, anything that comes solely from context synthesis or is purpose-specific. For example, *task-specific relevance claims*, *LLM predictions*, *model-based similarity scores*, and *summary interpretations* should not be classified as DerivedKnowledge. The ADR text should be updated to reflect that DerivedKnowledge is only for *repository-grounded knowledge*.
  - *Additions:* ADR-0002 should acknowledge that repository-derived facts can carry uncertainty/confidence. It may define an “epistemicStatus” field (e.g. DEFINITE, POSSIBLE, HYPOTHESIS) for facts. It might also note that new claims (L2) are vetted via separate process.

- **ADR-0004 (`Context Disclosure Planning and Assembly`):**
  - *Continue to own:* The process of selecting and formatting information for model input. This includes `InformationNeed`, `RelevanceEvidence`, `DisclosurePlan`, `DisclosureOption`, and the materialization of chosen content.
  - *Change needed:* The current principle that *“new semantic assertions in Context prep become DerivedKnowledge”* should be revised. Instead, it should say something like: *“Context planning can produce new assertions (e.g. summarizations or inferences) but these are tagged with purpose and provenance; only if validated do they migrate to DerivedKnowledge.”* In practice, ADR-0004 should delineate that synthesized statements can exist in the `ContextDisclosure` (with provenance) but are not automatically added to the repository knowledge base.
  - Possibly introduce terminology in ADR-0004 for *“Context Assertions”* vs DerivedKnowledge.

- **New Responsibility:** We may not need a separate ADR for a new concept; it could be a part of ADR-0004. But to be clear, we suggest drafting an architectural guideline (perhaps a short ADR or amendment) stating: *“Repository knowledge (ADR-0002) is decoupled from context-driven assertions (ADR-0004). The system should differentiate the two in both data and process.”* This may function as an ADR-0005 or similar.

- **ADR-0003 (Retrieval):** Likely unaffected; we only need to ensure Retrieval results do not spontaneously become DerivedKnowledge. ADR-0003 already treats `RelevanceEvidence` separately, which is good.

- **ADR-0002/0004 Coordination:** We should ensure the revised ADRs do not conflict: ADR-0002 defines the scope of repository knowledge, ADR-0004 defines how context can build on it. They should explicitly reference each other. For example, ADR-0004 might say “Referenced facts come from ADR-0002 DerivedKnowledge or from raw resources.”

In summary: ADR-0002 remains the home for static, shareable knowledge. ADR-0004 handles dynamic assertions with clear provenance. No duplicative new top-level concept seems needed beyond refining these.

# T. Falsification Questions

1. **Is current `DerivedKnowledge` too broad?**
   Yes. It currently tries to capture not just static code facts but also any needed inference. For example, treating an LLM summary as DerivedKnowledge would be too broad. We argue for narrowing it to deterministic repository facts.

2. **Is it too narrow?**
   Potentially. If `DerivedKnowledge` *only* includes absolutely certain facts, it might exclude useful probabilistic facts (e.g. “likely call” from heuristic analysis). We might allow uncertain facts by marking them. So it’s not too narrow in functionality, but its definition should be expanded to allow confidence annotations rather than excluding heuristics outright.

3. **Is deterministic repository intelligence the right core boundary?**
   Yes, in spirit. The core should be repository-relative facts. However, we acknowledge this still allows heuristic analyses if they are reproducible. The key is reproducibility and provenance, not the “execution model.”

4. **Should `DerivedKnowledge` require determinism?**
   Not strictly in execution: a reproducible ML model output can feed it if fixed. But yes for outcome consistency. We should allow deterministic analyzers (which may use heuristics) to feed DerivedKnowledge *if they are labelable as uncertainty-bearing facts*. Purely stochastic (non-reproducible) processes should not feed it.

5. **Should heuristic static-analysis claims qualify?**
   If they yield reproducible outputs, **yes**, but with uncertainty tagging. For instance, a name-based override detector might say “likely monkey-patch here.” Such a claim could be in DerivedKnowledge as a “possible fact” with provenance of the heuristic. So we lean towards including them with caution, rather than excluding them.

6. **Should probabilistic analyzer claims qualify?**
   Same logic as #5. If deterministic run of a probabilistic analyzer (fixed seed) yields the same output, it could be in DerivedKnowledge with a probabilistic marker. However, if the probability model is non-repeatable or has high variance, we should treat its outputs like model outputs (not persistent facts).

7. **Should LLM-generated claims ever qualify?**
   **Not by default.** An LLM call is semantically outside pure repository analysis. Only if *validated* (see #8) should it be promoted. Unvalidated LLM statements should remain outside DerivedKnowledge.

8. **Should validated/corroborated LLM claims be promotable?**
   Yes, if they pass validation. For example, if multiple independent queries produce the same conclusion, or if a user confirms it, or if a static analysis can verify it, then it may become a DerivedKnowledge fact (with its provenance including mention of the LLM-derived origin). Essentially, treat it like any user-provided fact: it enters the knowledge base with attribution after review.

9. **Is provenance sufficient to prevent authority laundering?**
   No. Provenance alone only *tracks* origin; it doesn’t enforce trust. We must also use epistemic flags or policies. For example, even with provenance, a model-sourced fact should not be treated as equal evidence to a code-derived fact. So provenance is necessary but not sufficient; the system must interpret provenance in decision logic.

10. **Should synthesis have its own semantic abstraction?**
    Yes. We recommend at least a tagging mechanism (or separate class) for synthesized/interpretive assertions. This is not already in ADR-0002 (it only knows DerivedKnowledge as facts). A new concept (or profile) is needed to mark “this assertion comes from synthesis/LLM”.

11. **Should synthesis usually remain ephemeral?**
    By default, yes. Most synthesis (summaries, heuristics for a specific task) should stay ephemeral. We only persist it if it proves reusable. This avoids polluting the core knowledge.

12. **Should deterministic projections be `DerivedKnowledge`?**
    Yes. If a projection (like a simple aggregate) compiles existing facts, it can be stored as DerivedKnowledge (or recomputed cheaply). It’s essentially an implicit fact.

13. **Should aggregates be `DerivedKnowledge`?**
    It depends on use. Counts (like number of methods) could be stored if needed for performance. But semantically they’re not new information, just a view. They can be considered DerivedKnowledge with a dependency on the original items.

14. **Should transitive graph facts be `DerivedKnowledge`?**
    Probably yes. Facts like “A transitively reaches C” are useful, derived semantic facts. Static analysis tools commonly compute and store these (e.g. transitive closure of call graph). They fit well as DerivedKnowledge if it’s deterministic.

15. **Should summaries be `DerivedKnowledge`?**
    No. Summaries (especially lossy ones) are inherently arguable and contextual. They belong outside the repository fact store. At most, source-preserving sub-pieces (like docstrings) could be stored, but natural-language summaries by the model should not become facts.

16. **Should task-relative synthesis be `DerivedKnowledge`?**
    No. By definition, task-specific info (relevance to bug X) should not be global. It’s used only in context for that bug. Promoting it to global knowledge violates purpose independence.

17. **Should compression be repository knowledge?**
    - Lossless compression (like canonical ordering of ASTs) is not new knowledge, just formatting; so no.
    - Lossy compression (summarization) definitely not, as discussed.
    In general, *any transformation that could alter meaning should not create new knowledge*; compression is usually representation.

18. **Should materialization be allowed to create new assertions?**
    Not unless it’s an explicit part of a derivation. Materialization should only fetch and format, not deduce facts. If summarization is needed, that’s a separate derivation step (model call) that should be tracked separately. So no, materialization itself should not add unplanned assertions.

19. **Should model-input assembly ever create new semantic assertions?**
    No. Assembly is about formatting. All semantic content decisions must come from earlier stages. The assembly step should not do any reasoning, only apply the plan.

20. **Clean boundary between epistemic derivation vs representation?**
    The clean boundary is: **derivation = new logical claim, representation = alternate expression of existing claim**. Implementation-wise, any process that *splits or reorders* content without inferring new relations is representation. If in doubt, err on not calling it DerivedKnowledge. E.g. no identifiers should change identity: selecting part of code is representation; inferring edges is derivation.

21. **How should uncertainty/conflict/completeness survive synthesis?**
    They should **be propagated**. A synthesized claim must include notes like “confidence: low” or explicit “subject to incomplete evidence.” If evidence is conflicting, the synthesis should say so (or flag it). Structurally, the claim’s provenance chain should include all sources, making conflicts visible. We should not throw away original sources. In other words, if we produce a summary sentence that contradicts one source, that summary should record which sources it used and which it skipped, so an auditor can trace the gap.

22. **Applicability differences for repository facts vs task synthesis?**
    Repository facts have a broad applicability domain: they hold for all tasks and models once the snapshot is fixed. Task-relative syntheses have narrow applicability (only for a particular InformationNeed or context). The system should encode that: DerivedKnowledge facts are valid across queries until the repo changes; syntheses expire after context is built (or possibly after the agent’s session).

23. **Which artifacts need identity/persistence?**
    - **Yes (identity):** All repository facts (calls, types, definitions) and any canonical aggregates we choose to store. These should have stable references (IDs or hashes).
    - **Maybe:** Certain validated interpretations (e.g. proven design patterns) if deemed reusable beyond one session.
    - **No:** Individual context artifacts (e.g. one-off summaries, relevance scores) typically do not need a global ID. They can be transient or stored only in logs.

24. **What should be cached and under what conditions?**
    - **Cache deterministic facts** (calls, references, symbol tables) keyed on repository version. Classic.
    - **Cache aggregates** or projections if reused often (e.g. module metrics).
    - **Cache LLM outputs only in context of validity:** e.g. if we fine-tune a summarizer and want reuse, we might cache model outputs (like embeddings). But textual summaries need re-generation due to prompt variability.
    - **Applicability keys:** For a cached synthesis, the key must include not just repo version but also *task and model state*. E.g. “bug=XYZ, model=Claude-v1, prompt=…”. This is complex and usually not worth it.

25. **What should ADR-0002 own?**
    Repository grounding: the definition of `DerivedKnowledge` as deterministic, reproducible knowledge with provenance. The scope (what dependencies mean, how to declare semantic inputs). It should articulate that this is *repository-state intelligence only*. It should define semantics of determinism, dependencies, and incremetalism.

26. **What should ADR-0004 own?**
    The context/dataflow: `InformationNeed`, `RelevanceEvidence`, `DisclosurePlan`, context formatting. It should specify that this pipeline may use and generate assertions but that those outside the snapshot (i.e. not directly from code) must be tagged or treated specially. It needs clarity on the plan/materialization boundaries (we recommended above).

27. **Is a new responsibility needed between them?**
    Perhaps a joint guideline or ADR clarifying how they interact. But probably not a full separate ADR. Instead, an amendment to ADR-0004 to define “Context Assertions” as distinct from DerivedKnowledge may suffice.

28. **Which existing distinctions should be removed?**
    - If anything, the current language equating *any* “semantic assertion in context” with DerivedKnowledge should be removed.
    - The notion that *all* reproducible facts are automatically visible externally could be relaxed; some inferences (like transient query statistics) do not need to be first-class.
    - The architecture might currently treat “relevance evidence” as not DerivedKnowledge; we should ensure consistency (as a precedent, keep it outside as done).
    - We should avoid introducing extra categories (like a distinct “IntermediateKnowledge”) unless clearly needed. Minimizing new concepts is advised.

# U. Risks and Unresolved Questions

- **Validating LLM Knowledge:** When *should* an LLM-derived statement cross the bar into repository knowledge? We lack a clear policy for that. It may require human review or automated fact-checking heuristics, which themselves need design.

- **Ambiguity of “deterministic”:** Many analyses are heuristic. The architecture must balance allowing useful uncertain facts vs insisting on absolute. We need examples to tune this (e.g. type hints vs proved types).

- **Complex provenance scaling:** Capturing full provenance for every assertion may be heavy. We should choose granularity carefully (e.g. provenance for a complex synthesized summary might be just “LLM(prompt P, model M)” rather than each line’s origin).

- **Cache invalidation logic:** If we allow caching of some synthesized artifacts (like static analyses with heuristics), we must precisely determine invalidation when code changes. This is an open implementation detail.

- **Ontology complexity:** Deciding the minimal set of “epistemic types” or flags needed (fact vs heuristic vs model) without going overboard is subjective. This may evolve with experience.

- **Interplay with environment state:** We assumed “repository knowledge” is code only. But in practice, facts like import resolution can depend on the environment (project config, build). The architecture would need a way to mark facts that are environment-dependent so they aren’t wrongly reused across different setups.

These and other questions (e.g. balancing prompt budget vs including evidence, the right granularity of semantic dependencies) may need iteration during implementation.

# V. Implementation Implications

In practical terms, the first implementation (the devtools framework) should:

- **Differentiate assertion storage:** Use separate tables/collections or a discriminator for derived facts vs context claims. The schema for DerivedKnowledge can be tight on code references (file/loc, commit) and derivation signature. The context claims can reuse the same table if we add a “kind” column, or use a separate log store.

- **Provenance extension:** Ensure every stored assertion (even context claims, if stored) records its source (module name, code location, or model info). Use common provenance fields (timestamp, producer ID) across both. For LLM calls, provenance might include prompt hash or a ref to the prompt text stored elsewhere.

- **Tagging and filtering:** Modify the query API so that by default, only repository facts (`kind = “fact”`) are retrieved for answers. Context planning modules can also query “kind = any” when generating answers that may cite heuristic info (e.g. telling the user “LLM suggests X”). The engine that builds context should know to exclude model-only claims unless explicitly asked.

- **Logging context runs:** Even if we don’t persist `AssertiveClaims`, we should log them in the execution record. This could be a structured log or an in-memory trace. Key pieces: which DerivedKnowledge IDs and code spans were included, any LLM outputs used, what was dropped. This log should be queryable after the fact for debugging.

- **Cache design:** The caching layer (for facts) will work as before. The system should not cache the outputs of context-specific reasoning, unless we explicitly implement a memoization keyed by (task, model, prompt). This likely isn’t needed for v1; we can recompute context claims each time to avoid stale reuse.

- **Evaluation hooks:** Implement facilities to compare model responses against the stored facts. For example, after answering, run a validation step: check each factual claim made against DerivedKnowledge or source code. Track any mismatches. Also track frequency of “I don’t know” vs made-up answer.

- **Minimal required changes:** The existing data model (ADR-0002) needs an added field for epistemic status/confidence. ADR-0004’s planner should be adapted to output marked context assertions. APIs that create DerivedKnowledge should refuse to store if the producer is flagged as “LLM” or “task-only”.

In short, the implementation will still use a central facts database, but with extended metadata to separate distilled facts from provisional claims. The context builder will rely on that differentiation to maintain correctness.

# W. Sources

- Anonymous Sourcegraph blog and docs: “How Cody understands your codebase” and Sourcegraph architecture docs. These explain retrieval-augmented context and the distinction between text search and static code intelligence, illustrating how deterministic analysis is used in practice. They support treating repository facts (indexes) separately from model input.

- RisingWave blog on Incremental View Maintenance. This demonstrates how derived state (materialized view) can update efficiently with changes. By analogy, repository `DerivedKnowledge` can be incrementally maintained, illustrating the reuse benefit.

- Shashank Jain, “Beyond brittle facts: building a probabilistic knowledge graph” (Aug 2025). Although focused on general KGs, it emphasizes storing confidences and supporting contexts. The examples (“99% confident Delhi is capital”) illustrate combining multiple pieces of evidence with probabilities, reinforcing that knowledge can be tagged with uncertainty and explanation.

- Inference Systems article on Provenance in Knowledge Graphs. This industry whitepaper (Rev2026) details how facts should carry provenance metadata (sources, transformations, timestamps) and how provenance enables traceability and quality. Key points: every triple gets linked to sources, allowing audit trails. It also discusses completeness metrics, aligning with our need to mark missing information. We use it to justify the need for granular provenance and confidence fields.

- Paolo Perrone’s Medium article “How Cursor Actually Works” (Mar 2026). Describes Cursor’s layered approach: a “Context Engine” indexing code and a prompt assembly that drops low-priority context. It shows the use of retrieval and prompt management, supporting our view that context planning should only *select* information, not invent it, and that model prompts fit variable-length context via priority-dropping. The technical details (trees, embeddings, reranker) exemplify a practical separation of indexing vs model inference, analogous to our recommended architecture.

- Tauman Kalai et al., *Nature* 2026 “Evaluating LLMs for accuracy…”. This academic paper analyzes LLM hallucination. It provides evidence that LLMs often output confident falsehoods and tend to guess rather than admit uncertainty. We use it to warn against trusting model outputs as facts and to motivate requiring explicit uncertainty. It underpins the rule that not all confidence implies truth in model-generated content.

Each of these references supports a piece of our reasoning: how contexts should be retrieved and formed (Sourcegraph, Cursor), how derived data can be maintained (RisingWave), the necessity of rich provenance metadata (Inference Systems), and the perils of uncritically accepting LLM outputs (Nature). They justify the recommended architecture’s emphasis on distinguishing reproducible code knowledge from uncertain, context-specific inferences.
