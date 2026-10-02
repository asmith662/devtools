# Repository-map baseline: frozen design and diagnostic replay

## Scope and evidence inspected

Started from clean `main` at `a24a70cc0511ce6fc56969ea7d46b438f79a7df0`.
This checkpoint implements a bounded repository-map retrieval channel, retains
Personalized PageRank (PPR), and evaluates only **diagnostic Case 0002**.
No Case 0003, prospective outcome, live model test or three-channel fusion is
manufactured. No sealed confirmation outcome is joined into this experiment.

Inspected governing taxonomy/documentation map, central architecture/roadmap,
ADR-0003, relevant ADR-0004, B-0002/B-0008 and backlog metadata/overview;
canonical Context Planning/graph research; Retrieval and graph documentation;
production typed projection, PPR, RRF, lexical analysis/scoring; Python
function/class/method declarations and Reference consumers; retained graph and
typed-graph experiments; existing Context/disclosure tests and dogfood capture
and blind adjudication protocol. No authority contradiction was found that
requires changing taxonomy, domain ownership, lifecycle or durable compatibility.

## Actual Aider implementation versus this adaptation

Primary evidence inspected on 2026-10-01:
[Aider implementation](https://github.com/Aider-AI/aider/blob/main/aider/repomap.py),
[raw implementation](https://raw.githubusercontent.com/Aider-AI/aider/main/aider/repomap.py)
and [official repository-map documentation](https://aider.chat/docs/repomap.html).
The inspection uses public `main`, not a pinned release or a performance claim.
Relevant implementation functions are `get_tags_raw`, `get_ranked_tags`,
`get_ranked_tags_map_uncached`, `render_tree`, and `to_tree`.

| Hypothesis | Aider implementation evidence | devtools decision |
| --- | --- | --- |
| Structural importance | PageRank on a symbol-labelled file multigraph; global fallback when no personalization exists | Separate query-independent dependency importance |
| Task relevance | Mentioned identifiers/files, chat files and path components affect weights/personalization | Separate canonical symbol/path BM25 |
| Definition/reference relation | Tags grouped by textual identifier, references linked to files defining that name | Only bounded resolved production RI declaration targets |
| Symbol representation | Ranked definition tags retain file/name/line; source tree snippets render selected lines | Exact RI declaration/subject/span retained before resource projection |
| Resource ranking | File PageRank plus flow distributed across identifier-labelled edges to definitions; remaining files can be appended | Explicit max ranked-symbol score per file; symbol and resource orders both exposed |
| Diffusion/PPR | NetworkX PageRank; explicit task/chat personalization when available | Existing query-seeded PPR retained independently; shared arithmetic |
| Compact disclosure | Token-budget search over ranked tag prefixes, source-tree rendering, chat-file exclusion and special-file inclusion | Context-owned future representation; no Retrieval rendering or special-file authority inference |

Aider's edge construction uses square-root reference frequency and naming,
identifier-mention, chat-source and definition-ambiguity multipliers. These are
heuristics over its tag model, not resolved repository relationship truth.
Its symbols are identifiers on **file edges**, not necessarily independent
symbol graph nodes. It ranks definitions using source file PageRank shares of
outgoing weighted edges. It does not compute our separate uniform global symbol
prior and then fuse it with symbol BM25. Those are explicit devtools adaptations.
The inspected code is neither a breadth-first neighborhood enumerator nor a
system that avoids Personalized PageRank. Calling the old PPR channel a full
Aider-style repository map would overstate what it implemented.

Adopted: definition/reference orientation, compact symbol identity, global
structural importance as distinct evidence, task relevance, and symbol-first
output with explicit resource correspondence. Not copied: textual identifier
resolution, language-tag fallback, naming heuristics, chat-file boosts,
special-file insertion, mutable mtime caches, token-budget rendering or
NetworkX dependency. RI remains deterministic knowledge; rank policies remain
Retrieval decisions under ADR-0003.

## Architecture alternatives and frozen choice

1. More typed query-personalized diffusion: retains relational value, but does
   not independently test global importance and compact symbol relevance.
2. Incoming-reference counts alone: explainable but lacks recursive source
   importance and normalized dependency-family contributions.
3. Literal Aider file multigraph/tag matching: violates the repository's
   stronger resolved-RI provenance model and imports heuristic weights without
   evidence for them here.
4. Global PageRank on all typed navigation edges: declaration count, outward
   containment and path navigation can create prominence unrelated to reference
   importance. Kept for PPR research, excluded from this importance hypothesis.
5. **Chosen:** resource-uniform global PageRank on resolved dependencies plus
   owner return, canonical compact symbol BM25, explicit symbol RRF and maximum
   symbol resource projection. This is a coherent bounded repository-map ranking
   hypothesis, not an automatic Context compiler or universal resource ranker.

See the [production contract](../../src/devtools/context/retrieval/repository_map/docs/overview.md)
for API, full formulas, direction/family semantics, tie rules, snapshot checks,
size-bias limits and architecture diagram. The shared stationary walk and shared
resource RRF arithmetic replace duplicated computation; existing PPR remains
canonical and reproducible. No experiment is imported by production.

Global importance restarts uniformly on observed resources. Imports contribute
resource-to-resource; References/direct bases contribute source-resource-to-exact
symbol; method/class/function ownership returns flow to class/resource. Active
families share row capacity equally, and unique fact supports divide that share.
Outward containment, package/mirror navigation and reverse dependencies are
excluded. Damping=0.85, L1 tolerance=1e-10, maximum iterations=200. Global masses
and native incoming fact flow remain visible.

Task relevance uses the existing Unicode-word/casefold analyzer and BM25
(k1=1.2, b=0.75) over `name-or-Class.method path`. No declaration body or new
tokenizer is introduced. Positive importance and positive symbol BM25 ranks
combine with equal RRF constant 60; a query with no symbol lexical match abstains.
Global-only symbols otherwise remain candidates. Resource scores take the best
symbol, never sum declarations. The result retains both orders and provenance.
Optional resource BM25/map RRF also uses constant 60. Raw score scales are never
added. Resource BM25 remains the lexical baseline and required non-code channel.

## Prospective protocol and why no new case exists

Before any diagnostic retrieval, `freeze.json` fixed production hashes,
algorithms, relation families, parameters, aggregation, channels and metrics.
Its diagnostic archive/adjudication hashes identify retained Case 0002; they
are not a new prospective freeze. The algorithm was not changed after outcomes. Final formatter-only changes
retain original source hashes and freeze digest plus verified identical Python
AST fingerprints in the manifest; no parameter or executable semantics changed.
Replay uses LF-normalized UTF-8 source hashes so Git CRLF checkout conversion
does not break reproduction; raw initial/checkpoint hashes remain provenance.

The investigation did not establish a legitimate independent next development
task. The repository-map implementation is real authorized work, but its
relevant source/architecture requirements were exposed during this investigation;
self-labelling that same increment cannot produce a fresh blind task. Broader
configuration/governance RI and compact Context-map disclosure remain pressure,
not authorization to invent work for an evaluation. Therefore prospective
**evaluation** stops pending the next naturally occurring task; production
implementation and validation proceed. No Case 0003 is created.

For that task, before retrieval or resource judgments, retain:

- exact repository snapshot and eligible observed frame/content identities;
- the complete independently justified real prompt and separately written short
  InformationNeed, with no ranked-resource clues;
- this algorithm/configuration freeze and full/short lexical arms, typed-core PPR,
  map ranking and equal BM25/map RRF; no three-channel arm;
- actual-required-count accounting, recall at 5/10/20/50/100, complete coverage
  depth, helpful/unnecessary/unjudged prefixes, lexical misses rescued,
  promotions/displacements and RI provenance, costs and ranking volume.

Run retrieval, retain outputs separately, then follow the dogfood protocol:
export only the neutral eligible frame, exact snapshot and real task to an
independent read-only adjudicator; withhold retrieval and agent provenance.
Freeze required/helpful/unnecessary/unresolved judgments and check exact identity
coverage **before** joining channel ranks. Partial coverage must stay partial;
unknowns are not unnecessary. Sealed confirmation outcomes remain unavailable.
No label from Case 0002 chooses a weight, threshold, mixture or policy.

## Case 0002: diagnostic, never tuning evidence

The retained snapshot has 302 resources and ten required obligations/resources,
five helpful-only resources and 287 unnecessary resources. `diagnostic_results.json`
retains complete rankings, required movements, symbol evidence and support facts.
Run `uv run python -m experiments.repository_map_baseline.evaluate` to reproduce.
Production hashes must match the freeze before ranking; development adjudication
joins only after every channel's ranking completes. No new adjudication is claimed.
The ablations (global-symbol-only and compact-symbol-BM25-only) were frozen before
retrieval to help diagnose the two parts; they are not alternative parameters.

Recall values below are fractions of all ten required resources. A dash means
incomplete required coverage, not a last rank among only the resources found.

### Full prompt

| Channel | @5 | @10 | @20 | @50 | @100 | Last required | Helpful prefix | Unnecessary prefix | Ranked resources |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bm25 | 0.3 | 0.4 | 0.6 | 1.0 | 1.0 | 43 | 5 | 28 | 299 |
| typed_ppr | 0.0 | 0.1 | 0.2 | 0.6 | 0.9 | 146 | 5 | 131 | 301 |
| repository_map | 0.3 | 0.4 | 0.4 | 0.6 | 0.7 | ? | 0 | 143 | 150 |
| bm25_map_rrf | 0.4 | 0.5 | 0.6 | 0.7 | 0.9 | 139 | 5 | 124 | 300 |
| global_symbol_only | 0.0 | 0.0 | 0.1 | 0.4 | 0.7 | ? | 0 | 91 | 98 |
| symbol_bm25_only | 0.4 | 0.4 | 0.5 | 0.7 | 0.7 | ? | 0 | 143 | 150 |

### Short InformationNeed

| Channel | @5 | @10 | @20 | @50 | @100 | Last required | Helpful prefix | Unnecessary prefix | Ranked resources |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bm25 | 0.2 | 0.4 | 0.5 | 0.6 | 1.0 | 87 | 5 | 72 | 285 |
| typed_ppr | 0.0 | 0.0 | 0.2 | 0.5 | 0.9 | 175 | 5 | 160 | 294 |
| repository_map | 0.2 | 0.2 | 0.2 | 0.4 | 0.7 | ? | 0 | 96 | 103 |
| bm25_map_rrf | 0.2 | 0.3 | 0.4 | 0.8 | 0.9 | 152 | 5 | 137 | 285 |
| global_symbol_only | 0.0 | 0.0 | 0.1 | 0.4 | 0.7 | ? | 0 | 91 | 98 |
| symbol_bm25_only | 0.2 | 0.2 | 0.3 | 0.6 | 0.6 | ? | 0 | 42 | 48 |

For incomplete map/ablation channels, helpful/unnecessary counts describe the
**entire returned inventory**, since no complete-coverage prefix exists.
For complete BM25, PPR and fusion channels, counts extend through the last
required resource. All these labels are retained development judgments;
there are no newly inferred unnecessary labels. No required lexical miss is
rescued: both resource BM25 lists already contain all ten required resources.

### Important full-prompt movements and provenance

| Resource | Resource BM25 | Typed PPR | Map | Symbol BM25 alone | Map winning symbol |
| --- | ---: | ---: | ---: | ---: | --- |
| experiments/codex_dogfood/capture.py | 3 | 17 | 3 | 1 | capture_codex_dogfood_retrieval |
| src/devtools/context/retrieval/composition.py | 13 | 6 | 1 | 4 | _require_snapshot_resource |
| src/devtools/context/retrieval/lexical/bm25.py | 33 | 36 | 4 | 2 | retrieve_repository_text_documents_by_bm25 |
| src/devtools/context/retrieval/structural.py | 37 | 50 | 7 | 5 | retrieve_python_direct_structural_resources |
| tests/context/retrieval/test_composition.py | 19 | 44 | 50 | 26 | _compose |
| tests/context/retrieval/test_structural.py | 38 | 69 | 54 | 27 | _facts |
| tests/experiments/test_codex_dogfood_capture.py | 9 | 42 | 45 | 13 | _case |

`composition.py` wins with `_require_snapshot_resource`: global symbol rank 19,
metadata lexical rank 30, supported by an incoming Reference. `bm25.py` wins
with `retrieve_repository_text_documents_by_bm25`: global rank 85 and metadata
rank 22, seven incoming supports. `structural.py` wins with
`retrieve_python_direct_structural_resources`: global rank 59 and metadata rank
37, sixteen supports. These are real resolved dependencies, not hand-added task
edges. Exact fact identities, source nodes and flow are in the JSON artifact.
Capture remains map rank 3; helper-heavy test resources are displaced. The full
prompt contains broad path terms including `py`, `src`, `context`, `retrieval`
and `tests`, so all 1,210 symbols have positive metadata lexical support. That
is a limitation of this compact lexical field for broad prompts, not a reason
to introduce a new tokenizer after observing this case.

For the short need, compact symbol BM25 misses `composition.py` entirely; global
importance brings it into the map at rank 43 (resource BM25 49, typed PPR 15).
This is a **symbol lexical miss**, not a required resource BM25 miss. The map
puts structural implementation at 4 (resource BM25 20, PPR 29), but test
resources at 55/56/60. Importance therefore supplies distinct recall evidence
inside the symbol view without establishing superior universal ranking.

### Cost and volume

- Core input: 1,512 nodes and 3,598 edges; dependency map: 1512 nodes,
  1907 edges, 1210 symbols and 302 resources.
- Current RI derivation plus all four retained graph views: 16.390s.
  This is a combined replay construction cost, not map-only cost.
- Map view construction: 0.055s; global importance: 0.045s,
  131 iterations, converged. Global importance is reused across query arms.
- full_prompt: resource BM25 0.010s; PPR 0.390s; map ranking 0.029s; fusion 0.003s. 1210 lexical symbols, 1210 ranked symbols, 150 map resources.
- short_information_need: resource BM25 0.006s; PPR 0.371s; map ranking 0.014s; fusion 0.004s. 358 lexical symbols, 586 ranked symbols, 103 map resources.

Timings are single warm local observations, not comparative throughput benchmarks.

## Diagnosis and remaining boundaries

1. **Useful global signal missing from PPR?** It supplies distinct symbol
   importance and rescues the short-need symbol miss for composition; however
   PPR ranks that resource higher. No prospective usefulness claim is established.
2. **Does symbol relevance improve ranking?** Several implementation ranks improve
   versus resource BM25/PPR. Full-prompt symbol-only recall is stronger than the
   importance-combined map at some depths, so the mixture is not yet validated.
3. **Required resources invisible to structural RI?** `AGENTS.md`,
   `docs/roadmap.md`, `pyproject.toml` remain without legitimate cross-resource
   structural relations and have no supported symbols. The map omits them.
4. **Benefiting categories?** Connected Python implementation declarations,
   particularly retrieval implementation, improve in this diagnostic. Results
   for tests are mixed; shared test helpers can acquire structural importance
   while test obligations themselves are not RI facts.
5. **Primarily lexical categories?** Governance, documentation, configuration,
   declaration-free resources and concepts present only in bodies/signatures.
6. **Fusion improves complete depth?** No: full prompt 43 to 139, short need
   87 to 152. It preserves recall but is not promoted as a default.
7. **Multiple specialized channels?** The case demonstrates complementary
   native evidence and differing category coverage. It supports retaining the
   portfolio, not claiming a universal structural ranker or general fused gain.
8. **Additional RI facts?** Explicit resolved documentation links and qualified
   document-to-symbol references, configuration ownership/entry-point bindings,
   and source-grounded test-target relations could materially expose missing
   categories. These require independently justified scoped RI derivations;
   path conventions, centrality and importance do not prove them. More complete
   dynamic-instance method resolution would help only within legitimate bounded
   static semantics, preserving unresolved outcomes.

Compact Context can later disclose the map's existing paths, kinds, names,
parents and exact spans. Signature extraction and class tree rendering are not
already implemented by these ranks. Context must choose that representation
explicitly and retain source/knowledge provenance; Retrieval must not hide a
budgeted renderer or sufficiency decision.

The exact next recommended increment is the frozen multi-channel advisory
comparison on the next naturally occurring independent task. It resolves the
unanswered transfer question before tuning relation weights, choosing default
fusion, or building a broad map renderer. This checkpoint starts none of those
production increments.


## Validation

Ruff, formatting checks on all 18 touched Python files, mypy (568 files), and
`git diff --check` pass. All diagnostic rankings and judgment metrics reproduce
exactly after the final formatter-only changes. Six focused map tests cover
identity, reference contribution, ownership, aggregation, task relevance,
missingness, ties, snapshots and reproducibility. Five additional RI/Context
regression tests cover malformed membership frames, qualified function Context
support, empty base-binding frames and retained Reference identity/projection;
these close pre-existing uncovered production validation branches.

The default `uv run pytest` invocation ran 1,759 passing tests, two skipped live
tests and seven failing repository benchmarks: the local `.venv` exceeds the
existing 10,000-resource discovery bound. It also automatically ran pre-existing
historical retained-confirmation audit tests; their outcomes did not enter this
design or diagnostic evaluation. Subsequent protected runs exclude the 22
retained-confirmation-dependent artifact tests. A temporary ignored validation
fixture uses a bounded repository corpus only as cwd for the seven affected
benchmarks, keeping original test and production imports/algorithms. The final
protected run has **1,749 passed, two live skips, 22 deselected, and 100.00%
production statement/branch coverage** (7,992 statements, 1,838 branches).
No production discovery limits or filtering semantics were changed to hide the
environment issue. The isolated-copy attempts before preserving original import
and cwd boundaries failed on intentionally omitted historical artifacts; they
are not reported as successful full-suite runs. `validation.json` retains the
exact excluded/bounded test identities and conditions. This is a qualified
regression pass, not a claim that the unmodified local `uv run pytest` passed.

Staged diff validation passes before the single checkpoint commit. No push,
Docker/model service mutation, live acceptance or next production increment is
performed. No confirmation result is joined into this retrieval experiment.
