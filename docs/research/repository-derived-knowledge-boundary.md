# Repository Derived Knowledge Boundary: Provenance, Qualification, and Applicability

## Disposition

Status: Reconciled

Canonical research subject: Derived repository knowledge qualification, provenance, and applicability.

Related ADRs: ADR-0002; ADR-0004.

Implemented evidence: identified snapshots, bounded derivations, source occurrences, and qualified import knowledge.

Accepted: qualification, support, coverage, applicability, and execution evidence remain distinct.

Deferred: generalized confidence, authority, conflict, and completeness mechanisms.

Rejected for now: universal Claim objects and universal confidence scores.

Superseded or refined findings: ADR-0002 gives the broader derived-knowledge jurisdiction.

Open questions: reusable result grouping and cross-derivation conflict semantics.

Revisit triggers: a concrete consumer requiring shared qualification or conflict machinery.

Reconciliation basis: ADR-0002; architecture taxonomy; B-0002.

The current design defines **DerivedKnowledge** as repository-relative semantic facts produced by identified Derivations with explicit semantic dependencies (e.g. static analyses yielding call or reference edges).  In effect, DerivedKnowledge holds *infallible-seeming* facts about the code (“A DEFINES B”, “A CALLS B” etc.), even if under- or over-approximate.  By design it excludes raw retrieval data, relevance evidence, purpose-driven summaries or models’ interpretations.  This roughly matches how **static analyses** usually work: they emit definite true/false facts rather than plain observations.  For example, one survey notes that “static analyses compute properties of programs that are true in *all* executions”.  In Datalog-based analysis (e.g. Soufflé/Doop), query results are likewise logically *sound and complete* given the rules.  Thus limiting DerivedKnowledge to only those assertions that are supported by explicit derivations is defensible: it keeps the semantic graph comprised of “hard” facts rather than ephemeral or heuristic data.

However, there are edge cases.  For instance, should a deterministic model-generated code summary ever become DerivedKnowledge?  Current policy says no unless confirmed.  We must check if this exclusion causes problems.  The literature suggests caution: approaches like PR-OWL even invent probabilistic ontology languages to handle uncertainty in logical facts, but we likely do *not* want that level of complexity.  Similarly, knowledge-graph builders often attach *confidence scores* or source reliabilities to facts (e.g. truth-discovery methods infer reliability degrees from data), but we’ve chosen not to mix uncertain evidence into DerivedKnowledge.

Overall, **the DerivedKnowledge boundary seems reasonable**: it aligns with how rigorous analyses operate.  It may be incomplete (it will not represent “possible” facts or interpretations), but that is intentional.  The risk is that some useful semantic info might be omitted.  For example, knowing which parts of the code are *possibly* related (as in *may-call* relations) can be important, but the design can capture that by using separate predicates (see below).  Thus DerivedKnowledge need not “own” evidence or indeterminate facts – it should only hold the semantic results that the architecture explicitly qualifies.  There is no obvious *semantic defect* in the boundary as stated, but the architecture must then ensure that it can still preserve any support or uncertainty.  We should clearly annotate facts in DerivedKnowledge with their provenance and with any qualifiers (may/must, scope, etc.) so that the absence of confidence metadata does not imply certainty.

# Provenance, Support, Authority, Uncertainty, Completeness, Applicability

These concepts are related but distinct.  **Provenance** is simply “where did this assertion come from” (which tools, which files, which inputs).  It does *not* imply any strength of evidence.  For example, we might record that “function A calls B” was derived from a call-graph analysis at a certain commit, but that metadata alone doesn’t mean it’s authoritative – it’s just provenance.  In contrast, **support/evidence** refers to *why* we believe a fact: how many independent analyzers agree, what code constructs support it, etc.  Methods like *truth discovery* explicitly separate these: they estimate a source reliability (authority) score by observing which facts from each source match what others say.  In our context, we should likewise separate *why* a semantic fact is believed (its provenance and support) from the fact itself.

**Authority/Trust/Credibility** is a higher-level judgment about sources or claims.  Importantly, it is claim-relative and purpose-relative, not an inherent property.  Dong *et al.* call this “Knowledge-Based Trust”: a web page is “trustworthy” if its facts are mostly correct.  But this is a derived metric, not embedded in the raw semantics.  In a code repo, a function definition file might usually be authoritative about function behavior, but a failing test could be more authoritative about intended behavior in a failing case.  We agree that authority cannot be a fixed global ordering; it must be computed per claim/purpose.  In sum: **provenance** is just origin, **support** is what underpins a claim, and **authority/trust** is a separate inference (or policy) that may weight provenance and support.

**Uncertainty** comes in many flavors.  In static analysis these are typically encoded in the *semantic predicates* themselves (e.g. `MAY_CALL`, `MUST_CALL`, `CANNOT_CALL`) rather than as external metadata.  For example, alias analyses classify pointers as “must-alias” or “may-alias” or “no-alias”.  Similarly, a call-graph could yield definite calls vs possible calls.  We should follow this pattern: put most uncertainty into the predicate (domain semantics) or derivation definition.  For example, a conservative type analysis will only produce a `MAY_CAST` relation when uncertain.  That way each fact’s nature is explicit.  (We could attach a separate confidence label, but that often conflates very different meanings.)

**Completeness/coverage** is about how exhaustive a derivation is.  This is typically a property of the *derivation definition* or execution.  For instance, an analysis might say “this is an exhaustive call graph for language X up to features Y,” or conversely that “this analysis stopped early; some calls may be missing.”  We must not allow a DerivedKnowledge fact (or absence thereof) to masquerade as total knowledge unless explicitly stated.  In database terms, this is the **closed-world vs open-world** distinction: under a closed-world assumption, “we found no calls from A to B” might mean “A does not call B.”  Under open-world, it only means “we don’t know.”  As the Closed-World Assumption page notes, “what is not currently known to be true must be false” only under CWA.  We generally operate under open-world (unknown means unknown) unless an analysis is explicitly exhaustive.  Thus, completeness notes (e.g. “analysis was partial”) are vital provenance or metadata on derivations.

Finally, **applicability/scope** qualifies *when* and *where* a fact holds (environment, snapshot, language version, configuration, test context, etc.).  This too must be explicit in provenance/assumptions.  If an ADR says “function `timeout()` returns 60”, that’s about intended behavior, not current code; we shouldn’t treat it as a fact about *this* code’s repository.  So DerivedKnowledge facts should carry any scope constraints (snapshot ID, architecture target, runtime conditions) in provenance.  In summary, we keep these notions separate: provenance (origin), evidence/support (multi-source corroboration), authority (trustedness of source by role or past reliability), uncertainty (semantic qualifiers), and completeness/applicability (scope info).  None collapse into one number or score.

# Uncertainty Placement: Predicates, Metadata, or Elsewhere

Mature analysis systems overwhelmingly encode uncertainty in the logic itself, not as generic metadata.  For example:

- **Soundness vs precision**: Static analysis literature defines a sound analysis as one that *never misses* a real fact, at the cost of possible false positives.  No single confidence score is used; rather, analyses may trade off precision (have more false positives) or become unsound (allow misses).  This is handled in the *analysis semantics* or domain model, not via a probability.
- **May vs must**: As in alias analysis, distinct predicates (`MAY_ALIAS`, `MUST_ALIAS`) capture uncertainty. A common formulation is: “cannot alias”, “must alias”, or unknown (may alias).  The unknown case is explicitly labeled as “may”.  This pattern can extend to call edges, references, etc.: e.g. `MAY_CALL` vs `MUST_CALL` vs `CANNOT_CALL`.
- **Probabilistic methods**: The knowledge-graph world has formalisms (PR-OWL, probabilistic ontologies) that allow every fact to carry a probability.  But these are heavyweight (first-order Bayesian networks) and typically not used in code analysis.  We should avoid a global probabilistic layer unless absolutely needed.
- **Heuristic scores**: Some tools do assign confidence (e.g. machine-learning extractors), but in a coding framework we should treat those as advisory evidence, not part of core DerivedKnowledge.  In retrieval/RAG contexts, numeric confidence serves for ranking, but it should *not* become part of the semantic graph.

Thus **we recommend encoding uncertainty in the predicate or derivation semantics** wherever possible.  For example, define separate `MAY_` and `MUST_` predicates, or attach explicit qualifiers like “analysis was incomplete” in the provenance of the result group.  This aligns with static-analysis practice.  Generic fields like a float “confidence” would conflate very different notions (risk of false positives, partial coverage, statistical guesswork) and have no clear interpretation in a programmatic context.

# Conflict and Contradiction

A **semantic conflict** occurs when two DerivedKnowledge assertions cannot both be true given identical scope and assumptions.  For instance, `MUST_CALL(A,B)` and `CANNOT_CALL(A,B)` about the same function `A` in the same snapshot are direct contradictions.  In contrast, `MUST_CALL(A,B)` vs `MAY_CALL(A,B)` are *not* contradictory (must-call implies may-call).  Similarly, disagreement about a fact may be benign if the contexts differ: a test expecting a 60s timeout and the code using a 30s timeout are not literally the same claim – one is *expected behavior*, the other *current behavior*.

We should treat conflict detection carefully.  Conflicts arise only when:
- **Same predicate and arguments** (e.g. both are about “calls(A,B)”),
- **Same scope/conditions**, and
- **Mutually exclusive qualifiers** (e.g. one says “always”, the other “never”).

If any of these differ, it’s a disagreement of differing claims, not a logical conflict.

Should conflicts be computed and stored?  Possibly *yes* as part of repository intelligence: detecting that “accepted ADR X” conflicts with “implementation code Y” is useful knowledge.  This could be treated as its own kind of DerivedKnowledge or a view thereof.  The architecture does not explicitly forbid it, but it is currently silent.  We could treat conflict detection as just another derivation: e.g. a “CONFLICT” derivation that watches for incompatible assertions in DerivedKnowledge.  It should be fine to include conflict facts as intelligence; they can help agents reason (“note: docs says one thing, code says another”).  We should preserve conflicts rather than arbitrarily choosing one side.

How to handle them in context retrieval/disclosure?  In context planning, if two sources conflict, options include preserving both, flagging the contradiction, or using purpose-relative authority to choose.  The design says the system shouldn’t silently resolve general truth.  Instead, I recommend that conflicts remain explicit in the repository intelligence (so they can be queried), but the **final disclosure to a model** should make the disagreement clear rather than hiding one side.  For example, if code says X and docs say ¬X, a well-formed context might say “Code says X; docs say otherwise (contradiction)” or simply include both pieces.  The model can then figure it out or be instructed to prefer one source.  This decision is partly Context layer logic, but repository intelligence must at least flag the conflict.

# Authority and Source Roles

“Authority” in this system must depend on context.  A test’s value as evidence differs from a code file’s, and both differ from documentation.  We should avoid fixed hierarchies (“implementation > docs”).  Instead, every assertion should carry metadata about *source role* (e.g. “runtime config”, “source code”, “unit test”, “ADR”) and possibly temporal or governance status (accepted, draft, etc.).  Authority then becomes a function of (claim, source roles, task).

It may help to treat source roles as **DerivedKnowledge** about ResourceOccurrences (e.g. “File F has role ‘unit test’”).  These roles can be multiple and purpose-relative (e.g. a file might be both “test” and “example usage”).  The architecture should allow repository queries to tag resources with roles, but those tags need not be first-class separate entities unless we find strong use cases.  In other words, we might implement roles as a small taxonomy (an open set of labels) attached to resources.  This is more lightweight than a universal Claim abstraction.

Importantly, *provenance ≠ authority*. A fact’s provenance (code path, analysis that produced it) does not automatically rank it.  Instead, when planning context, we might assign higher “weight” to facts from certain roles (e.g. code > comments for current behavior), but this is a policy on how to assemble context, not a property of the fact itself.  The intelligence layer should just record the fact’s origin and role; any “authority score” is best computed later depending on the user’s needs.

# Completeness and Absence

We must explicitly mark how complete a derivation is.  A simple boolean “complete” flag on each *DerivationExecution* or *DerivedKnowledgeResultGroup* is useful (meaning “no more results were possible under this execution’s assumptions”).  This prevents the error of treating “no found edges” as “edge does not exist.”  For example, if `REFERENCES(A,B)` is produced but the analysis was incomplete, we cannot assume A references *only* B.  Incomplete analysis should generate a provenance note (“analysis time limited” or “language feature unsupported”).

Closed-world assumption (CWA) vs open-world assumption (OWA) must be explicit.  Only when a derivation is *guaranteed exhaustive* (e.g. parser has scanned all files, type-checker was whole-program sound) can downstream logic treat missing facts as negative.  Otherwise, absence is just *unknown*.  This aligns with database logic: CWA adds negations of unknowns, but here we **don’t** default to CWA.  Instead, every zero or partial result should carry the qualifier “maybe more exists”.  For instance, `CALLS(A,?)` might remain unknown unless the call analysis claims it enumerated *all* calls, in which case we’d mark that result set as exhaustive.

Therefore, **completeness should belong to the derivation execution and result group metadata**, not to individual facts.  A naive `complete:bool` on each fact wouldn’t capture “this analysis run was complete/imcomplete”, so better is to say “derivation X over inputs Y was complete/not-complete.”  Then “no result” from that run is understood accordingly.  This avoids needing a global “complete” flag per predicate, which would be misleading in mixed contexts.

# Conflict Detection and Semantics

As noted, semantic conflict means logically incompatible claims.  To determine this, we need well-defined comparability: same predicate name, same arguments, same scope.  For example, `MUST_CALL(A,B)` vs `MUST_CALL(A,C)` (with B≠C) are not conflicting; they just say two different things.  But `MUST_CALL(A,B)` vs `CANNOT_CALL(A,B)` are contradictory.  The system should compute compatibility of predicates as part of derivations.  In practice, one can encode conflict rules: e.g. *if* one derivation yields `MUST_CALL(x,y)` and another yields `CANNOT_CALL(x,y)`, emit a `CONFLICT_CALL(x,y)` fact.

Conflict facts themselves may be stored as DerivedKnowledge (since they are facts about facts).  They certainly depend on provenance: we should record which two sources led to the conflict.  Whether to treat conflict as “intelligence” depends on whether it’s reusable.  I lean yes, because knowing “Docs vs Code disagree on timeout” might be reusable.  So a “Conflict” derivation is just another analysis.

However, these conflict detections are context-sensitive.  If one derived call fact was under config X and the other under config Y, it’s not a real conflict unless X and Y apply together.  So conflicts should also record any differing assumptions.

# “Claim”/Assertion Abstraction

A universal *Claim* or *Assertion* object (with support, provenance, assumptions attached) is tempting but likely overkill.  It might simplify uniform handling of facts vs evidence, but it duplicates much of DerivedKnowledge plus provenance.  Most existing static-analysis and knowledge-base systems simply treat each derived fact (edge, predicate) as a ground assertion, and attach provenance links (e.g. a DAG of derivations).  For example, RDF named graphs group triples by provenance, and PR-OWL attaches probabilities to OWL axioms, but neither introduces a separate “claim” entity for every statement.

Introducing a Claim abstraction risks "explosion": every true/false result in analysis might become a distinct object with identity.  It could help conflict detection (conflicts are then between Claim instances), but conflicts can be detected at the predicate level too.  Given the evidence so far, **we should avoid a heavy Claim ontology** until/unless a need clearly emerges.  Instead, keep semantics domain-specific (predicates) and use provenance links to tie them together.  Only if we find that tasks like belief revision or multi-hop reasoning demand a uniform claim interface would we consider it.

# Confidence Scores

We strongly discourage a generic numeric confidence field on DerivedKnowledge.  In static analysis, there is rarely a calibrated probability.  Instead, tools use categorical qualifiers (sound/unsound, may/must).  In knowledge integration, “confidence” often just means “trust of the extraction method” or “support count,” and it does not translate to semantic truth.  For example, the Knowledge Vault project *does* compute probabilistic confidences for facts, but those are for ranking or truth-finding in an open web corpus, not for deterministic code semantics.

Given the risk of misinterpretation, our semantics should not assign, say, `confidence=0.82` to a call edge unless we truly have a well-defined probability model behind it.  Instead, if a fact is uncertain, represent that uncertainty in the predicate (as above) or in an evidence structure (like “this is a heuristic guess that needs checking”).  Numeric confidence is useful in ranking (retrieval) but not for underlying repository intelligence.

# Model-Generated Assertions

Modern LLMs can produce code facts (e.g. “function A calls B”) plausibly, but the architecture wisely separates these from DerivedKnowledge unless validated.  Current best practice is: a model’s output is treated as **RelevanceEvidence or a draft**, not a confirmed fact.  Only if it can be checked (via static analysis, tests, compilation) should it become durable knowledge.

There is research on fact-checking LLM outputs (e.g. verifying generated code by static analysis), but it’s still emerging.  For now, we should require *independent verification* for any model-synthesized assertion.  If multiple models agree or a human approves, that still doesn’t change the semantics without evidence.  So the architecture’s stance (“no automatic promotion just from reproducible output or confidence”) is prudent.  If we ever allow promotion, it must be contingent on something like “execute the code” or “prove the claim in an abstract interpreter.”  In short, model outputs remain separate evidence until further validation.

# Learned/Probabilistic Analyzers

Deterministic analyses (type-checkers, parsers, IR-based analyzers) fit cleanly into DerivationDefinition/Execution: they have clear inputs and outputs.  Learned or probabilistic analyzers (e.g. ML-based AST analysis) blur reproducibility.  In principle, one could define a DerivationDefinition that is “ML-based call predictor” with given model weights as part of the derivation’s identity.  But then DerivationExecution is nondeterministic unless we fix randomness seeds and input randomness.

To accommodate ML, we should require that any learned analyzer declare itself as such, and possibly attach a “confidence” or randomness level in its provenance.  It would still produce DerivedKnowledge facts (with the usual qualifiers).  The derivation semantics may be explicitly unsound or incomplete, but that is just another derivation style.  We should not *forbid* learned analyzers, but we should treat their results cautiously (like any unsound analysis): label them (in provenance) and perhaps give them lower default authority.  Crucially, learned analyzers **can fit** the Derivation model if we allow the DerivationDefinition to encapsulate a model + hyperparameters.  The architecture can mark these runs as nondeterministic.  The cost is potential loss of *applicability determinism*: repeating the analysis might not produce identical DerivedKnowledge unless we control all randomness.  We should note this trade-off but not exclude learned methods entirely.

# Retrieval, Context Planning, and Conflicts

When assembling context for a model, if we have conflicting facts from the repo intelligence (e.g. code says X, ADR says ¬X), we face choices.  The repository intelligence layer’s job is done once it flags the conflict; we should not resolve it at that stage.  Context planning (downstream) might do one of: present both sides, note the conflict, or select one based on the user’s question and purpose.  For example, if the purpose is to “explain current behavior”, we might prefer code over docs.  But the architecture should preserve both in the intelligence layer.

This means ContextDisclosure should be conflict-aware: for example, a DisclosureOption might indicate “include conflicting claims explicitly” or “favor one source”.  The model-input assembly should ensure that contradictory facts are not silently collapsed into a single statement.  Ideally, the assembly would generate natural language like “Code file A implies X, whereas ADR Y states ¬X.”  But if we simply dump both facts as text or triples, at least the contradiction is apparent.  We must be careful not to let truncation or summarization drop one side of a conflict and accidentally “resolve” it.

# Uncertainty and Model-Input Assembly

All epistemic qualifiers must survive the journey into the prompt.  For example, a `MAY_CALL(A,B)` in repository intelligence must *never* be conveyed as a definite “A calls B” in the final context.  Likewise, an analysis note “report incomplete at 2000 nodes” must not be lost such that the prompt implies completeness.  To ensure this, any materialization (serialization of knowledge) step should encode uncertainty explicitly.  Possibilities:
- Use words like “possibly” or “may” in generated text.
- Attach provenance notes like “[incomplete analysis]”.
- Structure the context (list or bullet) with qualifiers.

In practice, this means the *ContextDisclosure* objects should carry flags and we should implement templates that honor them.  The architecture already separates planning (what to include) from materialization (how to phrase it).  We must enforce that materialization never omits epistemic qualifiers.  For instance, if a `DisclosureOption` includes a DerivedKnowledge with `uncertainty=“may”`, the resulting string should literally say “A may call B” or similar.  This is a policy in the Context assembly.  Overall, the semantic strength must *not* increase through projection or summarization.

# Evaluation Metrics

We should evaluate repository intelligence separately from retrieval.  For the knowledge layer, metrics analogous to static-analysis evaluation are appropriate: **precision** (how many reported facts are correct), **recall/completeness** (how many true facts were found), **soundness** (no false negatives if claimed sound), and **strictness** (no false positives if claimed precise).  In practice, we might measure recall of known benchmarks (e.g. how many actual call edges vs missed ones) and precision (how many reported calls actually occur).

Because we also track provenance and uncertainty, other metrics include: **contradiction coverage** (does the system flag real conflicts?), **conservativeness** (rate of over-approximation vs under-approximation), and **provenance fidelity** (are derivation traces correct).  Calibration of any fuzzy scores (if used at all) would be measured by reliability diagrams etc., but we expect few numeric scores.

For Context/disclosure evaluation, one could measure **task success rate** (does the model answer questions correctly with this context?), **efficiency** (tokens used), and **semantic integrity** (are no unsupported assertions introduced?).  For example, if models often hallucinate or claim knowledge not in context, we’d attribute that to context weaknesses.

In short, repository-intelligence evaluation mirrors static-analysis benchmarks (precision/recall, soundness claims), while retrieval/context evaluation uses IR and LLM metrics (ranker quality, model accuracy, hallucination rate).  We must be careful that a context-level success (model solves task) doesn’t hide a flaw in the knowledge layer (e.g. “model reasoned correctly despite incomplete facts”).

# Efficiency and Cost

Each semantic feature we add has a cost.  We should minimize persistent storage and computation.  For example, adding per-fact confidence values increases storage, indexing, and complicates queries; since we can mostly avoid that, we should.  Detailed provenance (like full dependency trees) has overhead; but since correctness is critical, a balance is needed.  We might store derivation provenance in a compressed form or only for certain assertions.

Conflict detection and completeness tracking add overhead: we must check compatibility of many facts.  This can be expensive, so we should do it on-demand (e.g. only when needed for a query or context), not eagerly for all possible conflicts.  Multi-source inference (truth-discovery style) can explode complexity; we likely shouldn’t implement full belief-propagation.

In incremental maintenance, fine-grained qualifiers (may/must) and completeness flags could complicate updates: e.g. if code changes, a “complete analysis” might become invalid.  We should design so that replacing an outdated derivation with a new one is easy (e.g. by tagging derivations with the relevant commit ID).

Overall, prefer semantic precision with minimal machinery.  E.g. model uncertainty as separate predicates or flags rather than new object types; represent conflict as just one extra predicate rather than a whole conflict graph.  Only persist what’s needed for correctness.  Be especially wary of global layers (like a universal Claim store or confidence index) that could slow down incremental updates.

# Architectural Approaches: Tradeoffs

We evaluate the candidate designs along multiple axes:

- **Semantic correctness & clarity:**
  - *A (Predicate approach)*: Keeps semantics in domain predicates (e.g. `MAY_CALL`, `MUST_CALL`).  This is precise and aligns with static analysis practice.  No ambiguity about meaning.  However, reasoning about heterogeneous uncertainties (from different analyses) requires policy logic.
  - *B (Qualified DerivedKnowledge)*: DerivedKnowledge facts all have a common “epistemic annotation” (fields for completeness, uncertainty, source, etc.).  This unifies metadata, making it easier to query generically (e.g. “show all uncertain facts”).  But it slightly blurs domain semantics if one must read these annotations to know the fact’s status.
  - *C (Claim objects)*: Introduces a layer of abstraction so every fact is a Claim object with support links.  This can simplify meta-reasoning (conflicts, argumentation) but adds a layer of indirection for queries (we must follow claims rather than triples).  It also risks duplication of DerivedKnowledge edges as claims with identical content.  Semantic correctness remains achievable but the model is more complex.
  - *D (Evidence layer)*: Domain assertions remain simple, but separate “Evidence” or “Assessment” objects link to them, capturing support, authority, scores.  This can elegantly capture trust and uncertainty without polluting predicates.  But it means context plans must join facts with evidence explicitly.  Implementation complexity is higher (two-tier store), but queries can target the simpler fact layer if evidence is not needed.
  - *E (Hybrid)*: Keep domain-specific predicates for common cases (MAY/MUST etc.), plus a small generic frame for anything truly cross-cutting (e.g. a unified completeness flag or confidence range).  This tries to get the best of both.  In practice, it might mean DerivedKnowledge has optional fields for qualifiers, but they default based on predicate semantics.

- **Provenance & Authority:**
  - *A* provides fine control via derivation chains; authorities must be handled externally.
  - *B* might attach provenance at the fact level automatically.
  - *C* could tie support/authority to Claim objects (nice for argumentation frameworks, but heavy).
  - *D* explicitly separates facts vs support, which many truth-finding systems do.
  - *E* would likely do A’s provenance model with maybe shorthand qualifiers.

- **Uncertainty expressiveness:**
  - *A* (domain predicates) excels: may/must forms can encode most program-analysis uncertainty.
  - *B* could add an uncertainty field, but then one might wonder how that interacts with predicate-specific meaning.
  - *C* could encode uncertainty in claim confidence or support strength, but again that’s extra machinery.
  - *D* allows arbitrary uncertainty metrics in the evidence objects.
  - *E* retains domain predicates plus perhaps a small set of qualifiers (like “confidence=high/low”).

- **Completeness:**
  - *A* expects each derivation to assert its own completeness (maybe via a metadata flag).
  - *B* could enforce a uniform completeness flag on facts or groups.
  - *C* might attach coverage assertions to claims.
  - *D* could have evidence types like “verified” vs “approximate”.
  - *E* might mark derivations or include in qual fields.

- **Conflict handling:**
  - *A* must define conflict policies separately (e.g. reasoners that detect contradictory predicates).
  - *B* can standardize how conflict is represented (maybe a Claim can have contradictory supports).
  - *C* arguably is designed for contradiction (argumentation frameworks).
  - *D* can store multiple evidence objects pointing to the same assertion, making conflicts explicit (one evidence says X, another says ¬X).
  - *E* likely treats conflicts similarly to A.

- **Incremental Maintenance:**
  - *A/E* (mostly predicate-based) have straightforward incremental update: rerun affected analyses and replace facts.
  - *B/C/D* introduce indirection (especially C), which may complicate updating: you might delete a Claim and re-create it, etc.
  - *D*’s evidence objects would need maintenance too (when an analyzer result changes, its evidence needs updating).

- **Graph Compatibility:**
  - *A/E* fit nicely into graph views (each predicate is a typed edge).
  - *B/D* add annotation on nodes/edges (like labeled edges for evidence). Some graph databases handle this with edge properties or reified edges.
  - *C* might require a hyper-graph (claims refer to multiple support edges).
  - Overall, A/E are easiest for plain graph layering; B/D can work with named graphs or edge attributes.

- **Retrieval/Context Compatibility:**
  - All designs can in principle feed context.  But
    - If uncertainty is in predicates (A), context must interpret different predicate names correctly.
    - If in metadata (B/D), context builder must read annotations.
    - Claim-based (C) would need flattening into text.
  - A/E have the simplest mapping (just say “maybe” vs “must” directly).

- **Replay/Evaluation:**
  - A/E again are simplest to reproduce: facts are just re-queried.
  - B/C/D have extra state (claim IDs, evidence links) to replicate, making testing more complex.

- **Implementation Complexity & Storage:**
  - A is minimal: just store typed facts and provenance pointers.
  - B adds a few fields/flags to facts (modest overhead).
  - D/C add whole new tables/objects (potentially large).
  - Truth/fusion systems show that evidence-handling scales but with cost.
  - E (light hybrid) tries to strike balance by adding just what’s needed (e.g. a “confidence” flag instead of full evidence objects).

- **Learned-Analyzer Compatibility:**
  - In A/E, a learned analyzer can still just produce facts (maybe flagged as probabilistic).
  - B/D might provide a natural place to record the analyzer’s uncertainty or model ID.
  - C could attach a Claim to each model-derived assertion, but that’s overkill.

**Summary:** The predicate-centric approaches (A/E) score high on simplicity, compatibility with graphs, and reflection of static-analysis practice, but require careful case-by-case handling of uncertainty and conflict.  The qualified or evidence-rich approaches (B/D) offer more uniform handling of qualifiers and authority at the cost of extra layers.  Claim objects (C) promise generality (arguments, diachronic belief tracking) but are heavy.  A plausible hybrid might be: use domain-specific predicates with an **optional small qualifier set** (e.g. “certainty = {must, may, unknown}”, “completeness = {partial, full}”) embedded in metadata on DerivedKnowledge.  We can delay a full Claim/Evidence layer until a clear need arises.

# Strongest attacks on the current architecture

1. **Incomplete Semantics (absence misinterpreted as negation).**  *Concern:* Without explicit completeness info, absence of a DerivedKnowledge fact might be wrongly taken as “false”.  *Why it matters:* Agents could conclude “A does not call B” simply because the call analysis was partial, leading to wrong code changes.  *Evidence:* The closed-world assumption warns that “not known = false” is only valid if the KB is complete. *Impact:* Potentially **fatal** to correctness (misleads reasoning).  *Fix:* Must ensure every derivation flags completeness; treat missing facts as “unknown” by default.

2. **Collapsing Uncertainty into Boolean Facts.**  *Concern:* Treating every semantic assertion as DerivedKnowledge (even those with uncertainty) could hide the fact that some are only “may” facts.  *Why it matters:* If a MAY_CALL is stored simply as CALL, a model might assume certainty.  *Evidence:* Static-analysis literature (and the alias example) shows that conflating may/must loses meaning.  *Impact:* **Correctness hazard** (overstating knowledge).  *Fix:* Continue to keep distinct predicates or add qualifiers for uncertainty.

3. **No Numeric Confidence Misinterpreted as Certainty.**  *Concern:* By rejecting numeric confidence, one might mistakenly assume all facts in DerivedKnowledge are equally certain.  *Why it matters:* Some facts (e.g. from a heuristic analysis) may be much less certain than others (e.g. from a sound analysis).  *Evidence:* Truth-discovery models use reliability degrees to reflect evidence strength.  *Impact:* **Clarification needed**.  We must ensure qualifiers or provenance suffice to signal doubt.

4. **Authority Ambiguity.**  *Concern:* The policy says “authority is claim-relative, not source-type-relative”, but provides no mechanism to compute it.  *Why it matters:* In practice, some automated rule or weight may creep in (e.g. tests normally override code), leading to hidden biases.  *Evidence:* No authoritative source can replace actual evidence; e.g., even official docs can be wrong.  *Impact:* **Risk of confusion**; not fatal if left to context logic, but needs guidance.  *Fix:* Clarify how to use source roles at context time (e.g. assign weights or preferences per purpose), and record roles explicitly so users/programs can apply policies.

5. **Conflict Representation Missing.**  *Concern:* The current model doesn’t say how to *represent* conflicts in the semantic graph.  *Why it matters:* Without a clear structure, context planners might either hide contradictions or overload the graph with ad-hoc signals.  *Evidence:* Data fusion research (Dong *et al.*, 2009) shows value in explicitly representing conflicting values and source dependence.  *Impact:* **Architectural risk**: deciding conflict-handling later may be hard.  *Fix:* Introduce either a DerivedKnowledge predicate for conflict or ensure conflicts can be queried as “edges” among assertions.

6. **DerivedKnowledge vs Evidence Blurring.**  *Concern:* Some retrieval or analysis results (like RelevanceEvidence or ContextCandidates) could inadvertently be treated as DerivedKnowledge if not carefully separated.  *Why it matters:* It could pollute the semantic graph with non-reusable, task-specific data.  *Evidence:* The architecture explicitly warns this (“RelevanceEvidence is not automatically DerivedKnowledge”).  *Impact:* **Moderate**; mostly a clarificational risk.  *Fix:* Maintain strict layering: make sure derivations only consume concrete code/state, not ephemeral retrieval hits.

7. **Universal Claim Abstraction is Tempting but Dangerous.**  *Concern:* It would be easy to start thinking “we need a general Claim object to unify everything”.  *Why it matters:* That would collapse DerivedKnowledge, relevance evidence, synthesis results into one model, undoing the separation of concerns.  *Evidence:* Knowledge-representation systems warn that overly general ontologies become intractable (cf. argumentation frameworks).  *Impact:* **Dangerous** to simplicity.  *Fix:* Avoid it as the guidelines say; rely on domain facts plus provenance.

8. **Learned Analyzer Dead-End.**  *Concern:* If we insist Derivations be deterministic, we may deter ML approaches.  *Why it matters:* The architecture states we shouldn’t redesign for speculative analyzers, but ignoring ML might lock us out of future techniques.  *Evidence:* Research is active in ML-based code analysis, but as yet it’s mostly heuristic (Infer/DeepCode do ML-like checks).  *Impact:* **Not fatal**, but we should ensure learned analyzers can fit as probabilistic derivations.  *Fix:* Explicitly allow non-deterministic derivations with provenance including model version; ensure downstream code can handle potential variability.

9. **Overhead of Granular Dependencies.**  *Concern:* The design rejects “maximizing dependency granularity regardless of cost,” but if we relax too much we lose provenance fidelity.  *Why it matters:* Fine-grained semantics often require fine-grained provenance.  *Evidence:* Provenance literature (e.g., graph-based pipelining) shows trade-offs: too coarse and you lose auditability; too fine and you overwhelm the DB.  *Impact:* **Implementation risk**: choose an appropriate granularity.  *Fix:* Clarify a middle ground (e.g. dependencies on whole files or AST nodes, not individual tokens).

10. **Context Disclosure “Semantic Strengthening.”**  *Concern:* The pipeline description assumes assembly won’t introduce new assertions, but generic summarization might.  *Why it matters:* If a summarizer says “only these functions are referenced” when it didn’t verify completeness, it has strengthened semantics.  *Evidence:* Knowledge-graph QA systems caution that text generation can hallucinate facts (see LLM context hallucination literature).  *Impact:* **High** for accuracy.  *Fix:* Enforce that materialization tools copy qualifiers; e.g. use phrasing templates that include “maybe” or provenance footnotes.

These attacks are not all equally critical.  The most *fundamental* are about completeness (1) and uncertainty encoding (2) – errors here would make the entire knowledge base unsound.  Authority and conflict (4,5) are serious but can be mitigated by clear policies rather than code-level mechanics.  Others (6,7,8,9) are clarifications or potential misdesigns that should be *fixed or noted*, but are not immediate showstoppers.

# Architectural Comparison

Below is a qualitative comparison of the candidate directions (A–E):

- **A: Predicate-Semantic Approach.**
  - *Concept:* Encode all semantics in domain-specific predicates (like `MAY_CALL`, `MUST_CALL`, `CANNOT_CALL`), with minimal common apparatus.
  - *Pros:* Extremely simple; aligns with static analysis tradition. Easy graph views (each fact is a typed edge). Low storage overhead (few extra fields). Good for incremental updates. Tooling (queries, materialization) remains straightforward. No universal ontologies needed.
  - *Cons:* Harder to express cross-cutting qualifiers (like “source is unreliable”) without ad hoc means. Authority/trust must be handled in context rather than encoded in the fact. Some repeated patterns (e.g. always add “May” as separate predicate) but understandable. Conflict detection requires custom rules. May lead to some duplication (like `maybe` vs `must`).

- **B: Qualified DerivedKnowledge.**
  - *Concept:* Keep DerivedKnowledge as before but attach a small generic qualification structure to each (fields for assumptions, completeness, uncertainty, etc.).
  - *Pros:* Uniform handling of qualifiers. Tools can query all DerivedKnowledge for “all uncertain facts” without knowing the predicate. Authority levels or uncertainty type can be standardized.
  - *Cons:* More data to store (fields on every fact). Some redundancy if different predicates reuse the same qualifier semantics. If overused, can become as heavy as D. May slightly complicate graph storage (need multi-valued edges or side tables).

- **C: Universal Claim/Assertion Layer.**
  - *Concept:* Introduce a class `Claim` (or `Assertion`), under which all facts, evidences, and context statements reside. Each claim has support pointers, provenance, etc. DerivedKnowledge facts are a subtype of Claim.
  - *Pros:* Highly uniform framework. Conflicts and belief revision can target claims directly. Good for provenance and trust frameworks. Tools like argumentation engines could plug in.
  - *Cons:* Very heavy. Every relationship becomes an object with identity; graph queries must navigate through claims. Doubles as both knowledge and evidence store. Likely unnecessary overhead for most repository tasks. Encourages over-engineering (every little fact gets a persistent ID). Hard to implement incrementally.

- **D: Evidence/Assessment Layer.**
  - *Concept:* Keep assertions as domain predicates, but introduce separate **Evidence** objects (or edges) that link these assertions to support data, confidence, source reliability, etc. For example, each `CALLS(A,B)` fact might have one or more evidence records.
  - *Pros:* Very flexible: you can attach multiple evidence entries (one from static analysis, one from an LLM, one from a test). This mirrors truth-discovery systems where multiple sources vote on a fact. Authority/trust can attach to evidence objects. The base graph of facts stays clean.
  - *Cons:* Additional storage (a whole new table or graph layer of evidence). Queries need joins (fact+evidence). If not careful, can blow up (each fact with many evidence rows). Implementation is more complex. For simple tasks, it may be overkill.

- **E: Hybrid.**
  - *Concept:* Use mostly A’s domain-specific predicates *plus* a minimal set of common qualifiers. For example, every DerivedKnowledge fact has an optional “certainty” attribute that defaults to “certain” for MUST facts and “possible” for MAY facts. Or use a small ontology of roles for source type.
  - *Pros:* Leverages simplicity of A but acknowledges we need a few cross-cutting annotations. Easier to adopt gradually. Storage overhead is small. Graphs still look uniform, with some edge labels.
  - *Cons:* Slightly subjective decisions about what qualifiers are “widely necessary”. Risk of creeping complexity if qualifiers multiply. The boundary between domain semantics and qualifiers could blur.

**Tradeoffs:** A/E maximize simplicity and graph compatibility (fits with no required graph DB and incremental maintenance). They rely on disciplined use of predicates and provenance for most needs. B/D offer richer semantics at cost of complexity; they align more with academic KR/trust systems. C is too heavyweight given current goals.

Given the evidence, **the hybrid (E) approach appears most balanced**: keep domain-specific predicates (as in static analysis practice) and allow a few uniform attributes (e.g. a completeness flag, or a “confidence level” enum) on DerivedKnowledge records. Reserve adding separate evidence objects or claim identities for future if real use-cases emerge.

# Recommendations

Based on the above analysis, the recommended course is:

- **Keep** the core design: DerivedKnowledge as analysis results with explicit dependencies; separate repository-state vs derived knowledge; layered Context pipeline. These align with best practices (static analysis and knowledge graph literature) and should **not** be overhauled.

- **Amend** the current architecture to explicitly handle: completeness metadata (flag or enum on derivation results), and conflict detection. Clarify in ADRs how to represent and preserve uncertainty qualifiers in materialization. Possibly add small, standardized qualifiers (e.g. a `certainty` field with values like MUST/MAY/CANNOT, if not already encoded in the predicate name).

- **Add** source-role tagging on ResourceOccurrences or RepositorySubjects, so that facts carry labels like “from test”, “from ADR”, “from config”. These roles would then feed into authority judgments at context time.  Also add a recommended “complete” attribute on each DerivationExecution record.

- **Do not add**:
  - A full Claim/Assertion object layer at this time.
  - A universal numeric confidence field.
  - Overly granular provenance for every single intermediate.

- **Defer** integration of learned analyzers or ML-based static analysis. We should allow them in principle (by treating them as specialized DerivationDefinitions) but not re-architect the core to support them until we have concrete needs.  Also defer any aggressive belief-revision system – only minimal conflict tracking.

## Minimum Preimplementation Semantic Contract

Before coding begins, we should formalize the following semantics:

- **DerivedKnowledge facts** must carry provenance that includes at least: derivation ID, derivation definition, input dependencies, and a scope (e.g. snapshot ID, language version, config).
- **Uncertainty qualifiers** should exist in one form or another: for call/alias results, `MAY/MUST/CANNOT` predicates; for any other ambiguous results, an explicit “uncertainty” tag in metadata.
- **Completeness indicator** on every DerivationExecution (or result set) as `EXHAUSTIVE` or `PARTIAL`.  Absence of results in a `PARTIAL` run means “unknown”, not “false”.
- **Conflict rules** defined for each predicate (e.g. (MUST vs CANNOT) or contradictory data values).  Conflicts should trigger a recorded DerivedKnowledge item (or at least an alert) rather than be silently dropped.
- **Source-role annotations** on all RepositorySubjects/ResourceOccurrences (e.g. “code”, “test”, “config”, “doc”, “ADR”).  These roles should be available for context planning.
- **No generic confidence score** in the core model; if needed, only special-purpose analyses may emit their own scores in provenance.
- **No claim reification**: do not require every edge to have an identifier. We treat derived facts directly.  (All metadata attaches via provenance links, not via a separate Claim object.)

This semantic groundwork is sufficient to capture uncertainty, trust, conflict, and completeness without building unnecessary layers.  It also leaves open the option to attach more sophisticated evidence or revision logic later if evidence shows it’s needed.

By keeping the model as light as possible (predicates + minimal annotations) but rigorous about provenance and qualifiers, we ensure **semantic correctness** while preserving efficiency.  This provides a stable foundation for devtools’ repository intelligence and context disclosure.

**Sources:** We drew on static-analysis theory (soundness/precision, Datalog soundness, alias analysis may/must), knowledge-graph and uncertainty literature (closed/open world, probabilistic ontologies, truth discovery and trust), and the design’s own ADR rationale. These show that specialized predicates and provenance links (rather than a monolithic confidence or claim layer) are the norm for handling uncertainty and authority in complex knowledge systems.
