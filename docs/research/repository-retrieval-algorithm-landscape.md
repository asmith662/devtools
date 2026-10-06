# Repository Retrieval Algorithm Landscape and Minimum Strong Retrieval Architecture for AI Software-Engineering Agents

## Disposition

Status: Historical prospective recommendation, reconciled into the roadmap and B-0002.

Current qualification: the [retrieval foundation](../architecture/retrieval.md)
owns implemented state and empirical limits. The
[roadmap](../roadmap.md#current-sequencing) now mandates R1 code-aware
representation followed by unconditional R2 true BM25F, with separately
attributable comparison arms. The original body below remains research evidence;
its conditional future sequence does not override current mandatory experiments.

Accepted / current direction: Investigate foundational retrieval variables
before further evidence-family escalation. Diagnose candidate coverage, ranking,
and Context disclosure separately. Increment 27 is repository-retrieval-
foundations falsification: retrieval-unit choice, code-aware lexical
representation, fielding, retrieval depth, deterministic query clues, cheap
fusion, and related inexpensive hypotheses are legitimate questions. Typed
structural evidence remains a valid available evidence family. Exact/direct
resolution remains distinct where the InformationNeed permits it.

Preserved but suspended: Increment 26 development evidence remains scientifically
valid. Its sealed CodeRankEmbed confirmation is preserved and suspended, not
rejected or completed.

Deferred / conditional: A broader evidence-family comparison depends on
foundational results and a decision-worthy gap; no later increment is selected.
Lightweight learned ranking awaits a credible high-recall heterogeneous
candidate pool and appropriate labels. Further dense/neural retrieval awaits
foundational results that justify escalation. Generic graph/vector
infrastructure requires demonstrated workload need. Broader production
promotion awaits independent-repository falsification and later supporting
evidence.

Not concluded: BM25 is the final retrieval solution; structural retrieval is
generally superior to lexical retrieval; dense retrieval is disproven; one
universal repository graph is required; one universal relevance score is
appropriate; or any one retrieval family is the final architecture.

## Executive conclusion and evidence posture

The central conclusion is adversarial to the usual “BM25 → embeddings → graphs → smarter embeddings” progression:

> **`devtools` does not yet have evidence that the next important retrieval investment should be a more sophisticated retrieval model. The highest-information next experiments are cheaper: retrieval-unit choice, code-aware lexical representation, fielding, query decomposition, broader candidate K, rank fusion, and separation of candidate generation from final context disclosure.**

This conclusion does **not** mean dense retrieval failed, structural retrieval was premature in the sense of being scientifically worthless, or BM25 is likely to be sufficient forever. Current coding-agent evidence actually argues against all three simplifications. Agent Retrieval Bench (ARB) finds substantial complementarity among lexical retrieval, repository maps, and modern embeddings, with different task families producing different winners; simple Reciprocal Rank Fusion of Qwen3 embeddings and RepoMap improves over either component on aggregate metrics. CORE-Bench likewise finds that modern embedding models can outperform BM25 on some repository-level retrieval settings, while also showing a severe transfer gap from conventional code-search benchmarks to realistic issue-driven repository search. citeturn13search1turn13search4turn5view2

The more defensible interpretation is:

**The current `devtools` experiments have discovered real complementarity, but the experiment sequence has skipped several cheaper confounders.** In particular, the local observation that lexical top-15 contained all 18 previously known-useful resources is a major warning that evaluating a candidate generator principally at `K=5` can conflate *candidate-generation failure* with *early-ranking failure*. Likewise, all eight useful CodeRankEmbed-only top-five discoveries in the development experiment existed at deeper positive lexical ranks. That is evidence that the semantic configuration improved *ordering* and *top-K exposure* on those cases; it is not evidence that it discovered a previously lexically unreachable evidence class. This is **devtools-local evidence**, not a universal conclusion about dense retrieval.

The most important conceptual correction is therefore:

\[
\text{repository truth}
\neq
\text{candidate evidence}
\neq
\text{usefulness}
\neq
\text{ranking}
\neq
\text{context disclosure}.
\]

A symbol definition can be repository truth and be exactly resolvable without “retrieval.” A file can be a useful candidate while being too large to disclose whole. A retriever can have excellent Recall@50 while being poor at top-five ranking. A ranking can be good while wasting the model's context budget. And an agent can recover from an imperfect initial ranking by taking a second targeted action. Recent benchmarks increasingly expose these distinctions: ARB reports both rank metrics and budgeted context yield; SWE-Explore evaluates ranked code regions under a fixed line budget; CORE-Bench distinguishes precise issue-to-edit localization from broader supporting-context retrieval. citeturn13search7turn16search5turn14view2

### Bottom-line recommendations

**Increment 26 should remain suspended.** Do not execute the sealed 16-case confirmation of the present CodeRankEmbed configuration now. Preserve the frozen experiment and artifacts. It remains scientifically useful as evidence about *that representation, corpus realization, and query configuration*. But confirmation would answer a lower-value question while large inexpensive uncertainties remain. Dense retrieval as a family should **not** be abandoned: ARB and CORE-Bench provide current evidence that stronger modern embedding models, including Qwen3-family models and in-domain adaptations, can materially outperform basic lexical baselines on some repository tasks. citeturn5view2turn15view2

**Increment 27 should become a retrieval-hypothesis falsification increment, not another model experiment.** Its primary purpose should be to determine whether the remaining apparent gains from structural and semantic retrieval survive after controlling for retrieval unit, `K`, code tokenization, fields, query representation, and cheap fusion.

The minimum strong architecture that the evidence currently supports is approximately:

> **exact/symbol/path resolution + code-aware sparse candidate generation over multiple units/fields + a small portfolio of typed structural evidence + rank-based fusion + bounded reranking + progressive disclosure.**

That is not a claim that this architecture will ultimately beat learned retrieval. It is the **least expensive architecture that should be falsified before adding neural retrieval as a production dependency**.

Current external evidence also argues strongly against a universal single retriever. ARB's task-level winners differ: embeddings are strong for some code-to-test and broader semantic tasks, while RepoMap is especially strong on trace-to-code; rank and context-budget winners also differ. CORE-Bench's issue localization and broader-context levels exhibit different retrieval characteristics, and query rewriting does not consistently help. citeturn5view2turn14view2

I use the following evidence labels implicitly throughout:

| Evidence class | Meaning |
|---|---|
| **Established IR** | Mature IR algorithms or controlled general-IR evidence |
| **Code retrieval** | Source-code search/localization evidence, often snippet/function oriented |
| **Coding-agent** | Repository-state, issue-driven, workflow, or coding-agent evidence |
| **Devtools-local** | Results supplied in the research brief; useful but not externally generalizable |
| **Inference/recommendation** | Architectural or experimental judgment derived from the evidence rather than directly established by a paper |

The current evidence hierarchy matters. CodeBERT, GraphCodeBERT, UniXcoder, SPLADE, and ColBERT are important representation or retrieval results, but most were not originally validated on the exact repository-context problem `devtools` is solving. Conversely, ARB, CORE-Bench, and SWE-Explore are directly aligned but extremely recent and should not yet be treated as settled consensus. CodeSearchNet-style success is particularly insufficient as proof of repository-agent effectiveness; CORE-Bench was explicitly motivated by this mismatch. citeturn8search4turn8search17turn8search2turn19search1turn19search6turn15view0


## Retrieval design space and comparative taxonomy

The largest design mistake would be to treat names such as “BM25,” “graph,” or “embedding” as complete retrieval strategies. A repository retriever is a composition:

\[
R =
(\text{need interpretation},
\text{query representation},
\text{retrieval unit},
\text{document representation},
\text{matching},
\text{fields},
\text{candidate breadth},
\text{fusion},
\text{reranking},
\text{disclosure}).
\]

Two systems both called “BM25” can therefore behave very differently. A file-level BM25 index over unsplit source text with aggressive English stemming is testing a substantially different hypothesis from BM25 over function-level units with identifiers decomposed, exact symbol names separately indexed, paths separately weighted, and file disclosure performed only after function retrieval. Likewise, changing the retrieval unit can plausibly produce a larger effect than swapping BM25 for BM25+, because length normalization, term density, distractor dilution, and context-budget efficiency all change together.

### Algorithmic taxonomy

The following tables together constitute the requested comparative taxonomy. Complexity is deliberately qualitative. For posting-list systems, query cost depends on postings touched; for neural models it depends strongly on model size, sequence length, batching and hardware; ANN indexes do not have one practically meaningful universal complexity bound.

| Family | Typical unit | Representation and match | Approx. query work | Code suitability | Main strength | Main failure mode | Evidence quality | `devtools` tested? | Would testing add new information? |
|---|---|---|---|---|---|---|---|---|---|
| Exact grep / literal search | line, file | raw characters/tokens; exact match | Scan corpus unless indexed; extremely cheap on normal repos | **Very high** for explicit error strings, config keys, APIs | No semantic ambiguity; explainable | Vocabulary mismatch | Established practice; coding-agent tools use it | Indirectly | Yes, if promoted to explicit routing baseline |
| Exact symbol/path resolution | declaration, symbol, resource | parsed symbol/path identities | Near-constant lookup plus result enumeration after index | **Very high** | Solves resolvable needs deterministically | Cannot infer unnamed conceptual relevance | Strong compiler/tooling basis | Repository Intelligence partially supports it | Yes, as a retrieval-routing baseline |
| Fuzzy/edit-distance symbol search | symbols/paths | strings, edit distance/trigrams | Vocabulary dependent; cheap if indexed | High for misspelled known entities | Typo/abbreviation tolerance | Many false positives as corpus-wide semantic search | Mature string matching; limited agent evidence | No | Modest |
| Jaccard / Dice | chunks/files | token or n-gram sets | Posting/set overlap | Medium | Simple non-probabilistic lexical control | Ignores term rarity/frequency unless augmented | Established | No | Modest; useful sanity control |
| TF-IDF cosine | chunk/file/function | sparse weighted term vectors | Sparse dot products/postings | High baseline | Simple, transparent, useful for ML features | Weak saturation/length behavior vs modern lexical methods | Established IR; extensive code-search heritage | Not as current production ranker | Yes, especially for CIT project |
| BM25 / Lucene BM25 | file/chunk/function | sparse terms; TF saturation + IDF + length normalization | Posting traversal + top-K | High | Strong, cheap, mature lexical baseline | Vocabulary mismatch; field/unit sensitivity | Very strong established IR | **Yes** | Parameter sensitivity adds some information |
| BM25L / BM25+ | file/chunk | BM25 with lower-bound / delta corrections | Same family as BM25 | Medium-high | Changes long-document / low-TF behavior | Likely second-order if tokenization/unit is wrong | Established IR; little direct agent evidence | No | Low-cost but moderate information |
| ATIRE / Robertson / adaptive BM25 variants | file/chunk | alternate IDF/saturation formulations | Similar to BM25 | Medium-high | Tests formulation sensitivity | Usually same lexical hypothesis | Established/implementation evidence varies | No | Low-medium |
| BM25F / fielded sparse retrieval | file/function | term evidence separated by content/path/name/symbol/etc. | Multiple field postings; still cheap | **Very high** | Encodes source-code evidence types explicitly | Requires field/weight tuning | Established structured IR; obvious code fit | Only primitive weighted filename arm | **High** |
| Character n-gram retrieval | symbol/chunk/file | character 3–5 grams + TF-IDF/BM25/Jaccard | More/larger postings | High as auxiliary | Naming-style, partial-string and typo robustness | Storage and noisy substring matches | Strong generic text evidence; limited modern agent evidence | No | **High per implementation cost** |
| Identifier-subtoken retrieval | symbol/function/file | camel/snake/hyphen decomposition | Ordinary sparse search | **Very high** | Bridges `AuthenticationError` ↔ `authentication_error` | Over-splitting/abbreviations | Code-retrieval evidence supports identifier preprocessing | Unknown/current baseline not fully specified | **High** |
| Query-likelihood language model | file/chunk | smoothed document language model, rank by \(P(q\mid d)\) | Posting/statistics work | Medium | Genuinely different probabilistic lexical hypothesis | No strong reason yet to expect code-agent superiority | Established IR | No | Medium-low |
| PRF / repository expansion | any lexical unit | first-pass results generate expansion terms | Roughly two retrieval passes | Medium-high | Can bridge repository-local vocabulary | Topic drift, self-reinforcing bad seeds | Established IR; software-query-reformulation literature | No | Tier-two value |
| Typed structural relation lookup | symbols/files | imports, refs, calls, inheritance, test relations | Adjacency lookup; bounded traversal cheap | **Very high for matching task types** | Retrieves lexically invisible but connected artifacts | Only useful when relation matches information need | Strong code-analysis basis; emerging agent evidence | **One import-member slice yes** | **High** for other relation families |
| Repository map / centrality | files/symbols | symbol/reference graph + compact summaries | Cheap after graph construction/ranking | High for navigation | Token-efficient overview, global context | Centrality ≠ task relevance | Production evidence from Aider; ARB direct benchmark evidence | No | High |
| Co-change/history retrieval | file/change/commit | temporal co-change, commits, issues | Cheap once history features indexed | High for ripple/impact tasks | Adds evidence absent from current source text | Historical accidents, stale relationships | Software-evolution literature; limited modern agent retrieval evidence | No | Medium |
| SPLADE / learned sparse | chunk/function/file | neural sparse vocabulary weights and expansion | Sparse postings after query encoding | Plausibly high | Semantic expansion with inverted-index behavior | Neural indexing/query model; no strong code-agent proof yet | Strong general IR, weak direct code-agent evidence | No | New hypothesis, but expensive enough for Tier 3 |
| Dense bi-encoder | chunk/function/file | one learned vector/unit, cosine or dot product | Query encoder + ANN/exact vector search | High where lexical mismatch matters | Semantic matching; fixed vector per item | Can miss exact identifiers; index/model/invalidation complexity | Strong code-search + current agent evidence | **CodeRankEmbed development arm** | Yes, but only after cheaper confounders |
| Multi-vector / ColBERT-style | chunk/function | token-level vectors + late MaxSim interaction | Candidate retrieval plus many vector comparisons | Potentially high | Fine-grained semantic/token matching without full cross-encoding | Large indexes, more query work | Strong generic IR; little direct repository-agent evidence | No | Genuinely new but low immediate priority |
| Logistic / linear-SVM ranking | candidates | lexical/structural/features or TF-IDF | Very cheap CPU inference | **High** with good features | Cheap learned decision boundary | Requires labels; linear feature interactions | Strong ML methods; direct code-agent validation needed | No | **High**, especially with CIT |
| GBDT / LambdaMART LTR | candidates | heterogeneous engineered features | Cheap bounded-candidate CPU scoring | **Very high** fit to devtools evidence | Learns nonlinear combinations/rank ordering | Labels/leakage, feature drift | Strong ranking evidence; LambdaMART mature | No | **High** if candidate recall is already good |
| Cross-encoder reranker | 20–100 candidates | jointly encoded query+candidate | One expensive neural inference/candidate or batching | High potential | Much richer interaction than bi-encoder | Latency/GPU/token cost | Strong generic ranking evidence; repository evidence less established | No | Tier 3 |
| LLM reranking | 10–100 candidates | prompt/context + model reasoning | Highest per-query/model-call cost | Potentially high | Can use nuanced task intent | Cost, latency, nondeterminism, position effects | Increasing practice; weak reason to make first-line retriever | No | Low priority now |

BM25 remains worth decomposing rather than treating as a single immutable algorithm. In its common form, term contribution combines inverse document frequency, saturating term frequency, and document-length normalization. Lucene's current `BM25Similarity` defaults to `k1=1.2`, `b=0.75` and uses the non-negative IDF form

\[
\log\left(1 + \frac{N-df+0.5}{df+0.5}\right).
\]

Lucene explicitly documents `k1` as controlling TF saturation and `b` as controlling document-length normalization. citeturn21view2

BM25+, BM25L, Robertson-style BM25, Lucene BM25 and ATIRE should be understood primarily as **formula-level lexical sensitivity tests**, not five radically different retrieval hypotheses. BM25L and BM25+ modify the low-frequency/length-normalization behavior by introducing a \(\delta\)-style correction; Robertson, Lucene and ATIRE differ in scoring/IDF conventions. `bm25s` implements all five and allows the IDF method to be selected separately. citeturn21view0turn21view1

That makes them cheap to test, but the likely information gain is smaller than testing whether a Python function should be represented as a whole file, an AST unit, a symbol-name field and an identifier-subtoken field. A result such as “BM25+ beats Lucene BM25 by 2%” would not settle the larger architectural question.

`rank_bm25` is useful as a small comparison implementation and exposes Okapi BM25, BM25L, BM25+, BM25-Adpt and BM25T; the latter adaptive variants broaden formula sensitivity further. But there is currently far less direct repository-agent evidence for choosing those adaptive forms than for investigating code-aware representation and fielding. citeturn0search2

### Operational taxonomy

| Family | Indexing cost | Incremental update | Storage | Query latency | CPU/GPU | Invalidation complexity |
|---|---|---|---|---|---|---|
| Exact indexed symbols/paths | Low–moderate parser/index pass | Excellent for changed files; dependencies may require resolution refresh | Very low–low | Excellent | CPU | Low–moderate |
| Grep without index | None | None | None | Corpus scan every query | CPU | None |
| TF-IDF/BM25 | Low | Usually straightforward per changed unit, depending implementation | Low–moderate sparse postings | Excellent | CPU | Low |
| Character n-grams | Moderate | Straightforward but more postings | Moderate–high vs token index | Good | CPU | Low |
| BM25F / multi-field sparse | Low–moderate | Good; update changed fields | Moderate | Excellent–good | CPU | Low–moderate |
| Relation indexes | Parser/static-analysis cost | Good for local facts; cross-file resolution may propagate | Low–moderate | Excellent | CPU | Moderate |
| Unified structural graph | Moderate–high | Can propagate across reference edges | Moderate | Excellent for indexed traversals | CPU | Moderate–high |
| Repository-map centrality | Moderate after relations built | Centrality may need recomputation/approximation | Low–moderate | Excellent after ranking | CPU | Moderate |
| Co-change/history | Moderate one-time history processing | Cheap for new commits | Low–moderate | Excellent | CPU | Moderate snapshot semantics |
| SPLADE | High neural document encoding | Re-encode changed units | Sparse but potentially substantial vocabulary postings | Query neural encoding + sparse retrieval | GPU desirable; CPU possible slower | Moderate–high |
| Dense bi-encoder | High one-time corpus encoding | Re-embed changed units only if snapshot/index design is sound | \(N\times d\) vectors plus ANN index | Query encode + fast vector search | GPU helpful; small encoders can use CPU | **High enough to design carefully** |
| Late interaction | Very high token-vector encoding | Re-encode changed units | **High**, even with compression | Higher than single-vector dense | GPU usually desirable | High |
| Lightweight LTR | Training offline; feature indexes reused | Model independent of repo update unless features change | Tiny model | Excellent for bounded candidate list | CPU | Low–moderate |
| Cross-encoder rerank | No corpus vector index required | Trivial corpus side | Model only | Moderate–high for 20–100 candidates | GPU strongly helpful | Low |
| LLM rerank | No special index | Trivial corpus side | None beyond provider/model | High + network/model latency | External GPU/API typically | Low data-index complexity, high operational cost |

The important correction to the CodeRankEmbed timing result follows directly from this table: **905 seconds for eight tasks is evidence against the experimental realization that repeatedly encoded historical corpora, not against index-once dense retrieval.** Production dense retrieval normally precomputes document embeddings and incurs corpus encoding when the repository index is built or units change; query time is then dominated by one query encoding plus vector search. ColBERT makes the same offline/online separation but stores multiple token vectors rather than a single vector per document. citeturn19search6turn19search18

The correction cuts both ways. “We could precompute it” is not a free pass. Dense retrieval introduces model/version identity, embedding-dimensionality compatibility, snapshot consistency, changed-unit detection, deleted-unit removal, index compaction, ANN persistence, model migration and potentially hardware-specific serving. That is substantially more lifecycle machinery than a sparse term index. The correct comparison is therefore **amortized agent economics**, not “905 seconds versus milliseconds” and not “query ANN lookup versus BM25” in isolation.

### `bm25s` specifically

`bm25s` is unusually well matched to the *experimental* needs of `devtools`. It provides Robertson, ATIRE, BM25L, BM25+, and Lucene variants; Lucene is the default. It supports configurable splitters, stemming, stopwords and reusable tokenizer vocabularies. It can persist its index, reload it with memory mapping, and use generator tokenization to reduce indexing memory. citeturn21view0

Its implementation moves substantial scoring work to index time: the technical report describes eagerly calculating query-token/document scores where terms occur and storing them in SciPy sparse matrices, making retrieval largely sparse slicing and summation. The authors report very large throughput gains over `rank_bm25` on BEIR, but those are **author-reported generic-IR implementation benchmarks**, not evidence of better code retrieval. citeturn21view1

That distinction yields a nuanced recommendation:

> **Use `bm25s` as an experiment engine and likely reference implementation before deciding whether it should become the production implementation.**

It can cheaply answer questions such as “Does BM25+ matter?”, “Does Lucene BM25 behave differently?”, and “Does custom source-code tokenization dominate the variant?” without requiring `devtools` to implement every formula itself. It should remain underneath an experiment-local adapter so its API does not become a domain abstraction.

One production caveat deserves explicit validation: its public documentation prominently describes building, saving, loading and mmap-ing indexes, but does not document a first-class arbitrary insert/delete/update workflow comparable to a continuously mutable search service. That is not proof that incremental strategies cannot be built around it; it means **incremental index maintenance should be tested explicitly before production adoption**. citeturn21view0

Maintaining an in-house BM25 makes sense only if `devtools` needs unusually specialized incremental behavior, field semantics, deterministic snapshotting, or code-specific scoring that the library cannot provide cleanly. Maintaining a home-grown standard BM25 merely to avoid a dependency has negative scientific value if it makes variant reproduction and cross-checking harder.


## Code-aware lexical, structural, learned, and agentic retrieval

### Code-specific lexical retrieval is a larger design space than “BM25”

Source code creates at least four lexical channels that ordinary prose retrieval does not cleanly distinguish:

\[
\text{surface spelling}
\quad+\quad
\text{identifier morphology}
\quad+\quad
\text{program namespace}
\quad+\quad
\text{filesystem/module namespace}.
\]

For the example family

```text
AuthenticationError
authentication_error
authentication-error
authenticateUser
authenticate_user
AuthError
```

a whitespace-oriented word tokenizer can treat these as unrelated or partially unrelated terms. A code-aware representation can retain **both** exact identity and normalized/subtoken evidence:

```text
exact:       AuthenticationError
normalized:  authenticationerror
subtokens:   authentication error
char grams:  aut auth uthe ...
symbol:      AuthenticationError
```

The crucial word is **both**. Replacing exact source identities with only normalized words would throw away information. Exact `AuthenticationError` is stronger evidence than merely sharing `authentication` and `error`.

Identifier splitting is not a speculative modern-LLM idea. Software-engineering research has long treated identifier segmentation as important preprocessing because identifiers encode natural-language concepts in concatenated forms; empirical feature-location work found that better splitting can improve IR-based feature localization in at least some conditions. citeturn20search0turn20search1

That evidence should nevertheless be scoped correctly. Those studies are older feature-location experiments, not proof that one splitter maximizes 2026 coding-agent performance. The cheap and defensible experiment is therefore to test a conservative deterministic splitter:

- preserve exact identifier;
- case-fold an auxiliary form;
- split snake_case, kebab-style text and obvious path separators;
- split camel/Pascal case;
- optionally retain common acronym runs;
- index both original and split forms.

Character n-grams represent a **different** hypothesis. They tolerate spelling and segmentation variation without requiring the system to decide that `Auth` means `Authentication`; they may therefore recover abbreviations, partial symbols and typos. Their cost is substantially more postings and the possibility that incidental substrings dominate. There is much less strong modern repository-agent evidence for char n-grams specifically, so they belong in Tier 1 because they are *cheap to falsify*, not because they are already proven.

Stemming deserves caution. English stemming can help issue prose, comments and docstrings, but source identifiers are not ordinary prose. Stemming `resolver`, `resolve`, and `resolution` may be useful in a comment field, while modifying exact API or class names can destroy high-value evidence. The best initial hypothesis is **field-specific analysis**: no stemming for exact symbol/path/identifier fields; optional stemming for prose/comment/query fields. This is an inference rather than established agent evidence.

The same applies to stopwords. Removing English grammatical words from prose can reduce noise. Aggressively discarding programming-language keywords is harder to justify because words such as `async`, `yield`, `class`, `import`, `raise`, or decorator-related tokens can themselves be diagnostic. BM25's IDF already attenuates globally common terms. Code-specific stoplists should therefore be experimentally learned or deliberately minimal, not assumed.

### Fielded retrieval should precede exotic retrieval

The current production score

\[
BM25(content) + 0.25\;BM25(filename\_stem)
\]

is already a primitive fielded retriever. Its weakness is not that it is “wrong”; it is that it hard-codes one coefficient across two independently scored views while omitting several source-code-native fields.

A stronger inexpensive experiment would separate:

| Field | Why it can carry distinct evidence |
|---|---|
| exact filename | Issues often name or imply artifacts |
| path components | Package/domain ownership and architecture |
| module/import name | Python namespace identity |
| declaration/symbol names | High-precision program concepts |
| identifier subtokens | Naming morphology |
| source body | General implementation evidence |
| comments/docstrings | Natural-language semantics |
| import targets | Dependency vocabulary |
| tests/test names | Behavior and regression language |
| config/build metadata | Build/dependency failures |
| commit/change features | Historical coupling |

BM25F was designed precisely for documents with heterogeneous weighted fields rather than treating the document as one undifferentiated bag. Its strategic importance here is greater than the distinction between BM25 and BM25+, because it tests a source-code-specific hypothesis: **a match in a declaration name is not equivalent to the same token appearing in a comment or 4,000-line source body.** Structured-field extensions of BM25 explicitly model weighted fields and their normalization rather than merely summing arbitrary scores after the fact. citeturn11search0turn11search28

There are two good experiments:

1. proper BM25F-style field scoring; and
2. separate field retrievers fused by RRF.

The second is especially attractive at first because it prevents score-scale quirks from masquerading as evidence importance.

### Retrieval unit may be a bigger variable than the scoring formula

There is no good evidence that “file” is the universally correct retrieval unit for an agent. Modern directly relevant benchmarks already disagree operationally: ARB is deliberately file-level; CORE-Bench uses AST/LangChain-derived repository chunks for issue and broader-context retrieval; SWE-Explore evaluates ranked code regions under a line budget. citeturn13search1turn14view3turn16search5

That does **not** prove chunks beat files. Because the benchmark tasks, qrels and metrics differ, cross-benchmark comparisons cannot isolate unit choice. It instead proves that unit is important enough to control experimentally.

A particularly strong architecture for `devtools` may be:

\[
\text{retrieve small semantic/program units}
\rightarrow
\text{aggregate evidence to resource}
\rightarrow
\text{disclose declaration/window/file as needed}.
\]

For example, a 3,000-line utility module may rank poorly at file-level BM25 because its relevant five-line function is lexically diluted and length-normalized. Function-level retrieval may expose that function easily. But the agent might ultimately need the full file around the function to edit safely. **Retrieval unit therefore need not equal disclosure unit.**

Tier-1 unit ablations should compare:

- whole resource;
- top-level function/class/method declaration units;
- AST-aware chunks with bounded fallback windows;
- fixed windows as a control;
- resource aggregation from child-unit scores.

A method-level hit should carry its parent file identity without pretending the file itself was the scored unit.

### Query processing deserves its own experiment family

`InformationNeed != query text` is exactly right.

A stack trace, review comment, feature request and anchored edit expose different observable evidence. A deterministic query-analysis layer can extract without an LLM:

```text
quoted error strings
paths
module-like strings
CamelCase identifiers
snake_case identifiers
function/class names
stack-frame symbols
package names
configuration keys
natural-language residual terms
```

These can route to different evidence channels while preserving the raw text.

CORE-Bench provides unusually relevant evidence against assuming that LLM query rewriting is automatically beneficial: its rewritten issue queries often fail to improve retrieval and can reduce performance, which the authors attribute to loss of request-specific context. citeturn14view2

That makes expensive LLM rewriting a poor Tier-1 investment. Deterministic extraction and multiple cheap query views should come first.

Pseudo-relevance feedback and repository-vocabulary expansion remain legitimate IR hypotheses. They can bridge terms such as a user-facing feature name to repository-local terminology by using initial results as expansion evidence. Their failure mode is topic drift: a bad initial top result can make the second search more confidently wrong. They are best placed after the basic lexical system is well characterized.

### Structural retrieval without graph ideology

The existing `devtools` structural experiment is scientifically valuable. It volume-matched the structural additions against lexical widening and found useful candidates unique to both arms; five useful structural candidates had no positive lexical rank. That is **strong devtools-local evidence for the tested relation family being complementary**.

It does not support a graph database.

A direct import/member relation can be represented perfectly well by specialized indexes:

```text
outgoing_imported_member[source_resource] -> targets
incoming_reference[target_symbol]         -> sources
callers[function]                          -> caller_functions
callees[function]                          -> target_functions
subclasses[class]                          -> derived_classes
tests_for[symbol_or_resource]              -> tests
```

For one-hop and relation-specific queries, these structures are simpler and often semantically clearer than converting all facts into generic nodes and edges.

A graph earns its architectural cost when the recurring required operations are themselves graph-shaped:

- arbitrary typed multi-hop path queries;
- relation composition selected dynamically at runtime;
- shortest/reachable path reasoning;
- neighborhood aggregation across many relation families;
- global graph algorithms such as centrality;
- repeated traversal where a common graph execution substrate materially simplifies implementation.

Recent systems show that those operations can be useful, but not that every repository intelligence system needs the substrate. RepoGraph models code using definition/reference structure; LocAgent uses a heterogeneous repository graph with entities and relations such as imports, calls and inheritance for repository localization. These are evidence that richer structural representations can help particular agent/localization systems, not evidence that a graph database is intrinsically superior to typed relation indexes. citeturn12search0turn12search26

Aider is especially instructive because its repository map is not “graph retrieval” in the simplistic sense. It gives the model compact symbol/signature information and uses a dependency graph ranking mechanism to decide which portions fit into a token budget. Its documentation explicitly describes a map containing files and important symbols and a graph ranking process over file dependencies, constrained by a map token budget. citeturn18view0

ARB supplies stronger independent relevance for this idea: its Aider-style RepoMap is highly competitive, and on the benchmark's 8K-token context-yield metric it outperforms the individual lexical and embedding baselines reported by the benchmark authors. It is especially strong on trace-to-code. citeturn5view2turn13search7

That suggests a valuable distinction:

> A repository map may be more useful as **compact disclosure/navigation intelligence** than as the canonical candidate generator.

Centrality can identify globally important interfaces, but globally important code is not necessarily relevant to a specific bug. PageRank or other centrality should therefore be a feature or map-budget heuristic, not presumed universal relevance.

Untested structural families with plausible task-specific value include definitions/references, callers/callees, inheritance, test-to-code relationships and historical co-change. Each should be tested as a **named relation hypothesis**, not as “more graph.”

### Sparse, dense, and late interaction

These families represent genuinely different hypotheses.

**Classical sparse retrieval** assumes usefulness is strongly indicated by explicit token correspondence, modified by rarity, frequency, fields and normalization. It is exceptionally attractive for software because many diagnostic signals are literal: symbol names, stack frames, exceptions, filenames, command-line options and configuration keys. CORE-Bench explicitly notes the usefulness of sparse retrieval for exact identifiers, APIs, filenames, stack traces and configuration keys. citeturn14view0

**Learned sparse retrieval** such as SPLADE retains a vocabulary-indexed sparse representation but learns token weighting and vocabulary expansion. SPLADE adds explicit sparsity regularization and learned expansion, aiming to retain inverted-index characteristics while bridging vocabulary mismatch; later SPLADE work improves training/pooling and effectiveness. citeturn19search1turn19search5

The key missing evidence is direct: there is currently far stronger generic-IR support for SPLADE than repository-level coding-agent support. It is therefore a genuinely interesting Tier-3 hypothesis, not an obvious successor to BM25.

**Single-vector dense retrieval** compresses each candidate into one learned vector and can match conceptually similar text without explicit term overlap. CodeBERT established joint natural-language/code representation and code-search capability; GraphCodeBERT added data-flow-aware pretraining; UniXcoder incorporated code structure and multimodal code/text pretraining. These are important code-representation results, but their original code-search tasks are not equivalent to issue-driven repository retrieval. citeturn8search4turn8search17turn8search2

Current code-specific models broaden the landscape considerably. CodeRankEmbed is a compact 137M bi-encoder trained for code retrieval; newer Jina code embeddings are based on coding-model backbones; Nomic has released a dedicated code embedding family; and Qwen3-Embedding includes general embedding models that current agent-retrieval benchmarks evaluate competitively. citeturn9search0turn9search5turn9search2turn9search30

Crucially, this means the `devtools` CodeRankEmbed experiment cannot stand in for “dense retrieval.” CORE-Bench itself reports materially different results across CodeRankEmbed, Jina, Qwen and other models. On its difficult issue-to-edit regimes, its 137M CodeRankEmbed result is often below stronger modern models; its in-domain Qwen3 fine-tunes improve dramatically across repository-difficulty strata. citeturn15view2turn15view3

At the same time, CORE-Bench is a warning against model-leaderboard extrapolation. Qwen3-Embedding-8B's performance drops substantially from its conventional code-understanding level to issue-to-edit and broader-context levels. The benchmark's primary conclusion is precisely that conventional code-retrieval quality overstates readiness for agentic repository search. citeturn14view2turn15view0

**Late interaction** occupies the space between a single dense vector and a full query/document cross-encoder. ColBERT independently encodes query and document representations but preserves token-level vectors and performs a cheap late interaction rather than collapsing every document to one vector. ColBERTv2 reduces the storage burden through residual compression while retaining multi-vector matching. citeturn19search6turn19search18

This gives late interaction a clear theoretical appeal for code: an identifier token, API token and natural-language concept can each find a strong local counterpart rather than competing to survive a single-vector bottleneck. But the price is a much larger index and more query-side similarity computation. There is not yet comparably strong direct evidence that ColBERT-style repository retrieval gives `devtools` enough value to justify that cost. It belongs behind single-vector and learned-sparse tests, not in front of them.

### Learned ranking is a separate question from pretrained retrieval

This distinction is strategically important:

\[
\text{pretrained dense representation}
\neq
\text{train a devtools ranker}.
\]

A lightweight learned ranker could consume:

```text
BM25 content score/rank
path score
filename score
exact identifier match
subtoken overlap
char-ngram rank
symbol/declaration match
import/reference relation
caller/callee relation
test relationship
retrieval-family agreement count
candidate size
candidate type
query/task type
semantic similarity, if available
change/co-change features
```

and learn only how those features correlate with usefulness.

That is a much smaller hypothesis than teaching a neural encoder what source code means.

Logistic regression and linear SVM are attractive first learned baselines because their failures are easy to interpret and inference cost is negligible. Gradient-boosted trees are especially attractive when the signals are heterogeneous and nonlinear. LambdaMART is the ranking-specialized version of this idea: it combines boosted decision trees with LambdaRank-style ranking gradients and has a long-established learning-to-rank pedigree. citeturn10search3

This family becomes particularly compelling if the next experiment finds:

\[
Recall@50 \text{ high}
\quad\text{but}\quad
Recall@5/MRR/\text{context yield low}.
\]

That is the signature of a **ranking problem rather than a candidate-generation problem**.

CORE-Bench provides contemporary evidence that learning can matter substantially: its repository-domain supervised fine-tuning uses disjoint training repositories and same-repository negatives, and its Qwen3 fine-tuned variants materially improve over their zero-shot counterparts. This is neural representation fine-tuning rather than lightweight feature LTR, but it establishes the broader point that task/repository-distribution alignment matters. citeturn15view0turn15view2

### Fusion and bounded reranking

Fusion is one of the strongest cheap opportunities in the entire design space.

A simple union answers:

> “Did any evidence family find this?”

Interleaving answers:

> “Can we expose diversity without calibrating scores?”

Reciprocal Rank Fusion approximately scores a candidate by

\[
RRF(d)=\sum_r\frac{1}{k+\operatorname{rank}_r(d)}
\]

over contributing rankers. The important property for `devtools` is not the exact constant; it is that the method combines **ranks rather than raw scores**, so a BM25 score, graph score and cosine similarity do not have to pretend to live on a common numeric scale. RRF was introduced as a simple rank-fusion method and has remained attractive for heterogeneous systems for exactly this reason. citeturn10search18

Current coding-agent evidence is unusually favorable. ARB reports that RRF between Qwen3-Embedding-8B and RepoMap raises aggregate MRR from the best individual result to a higher fused value and also improves Recall@20; the fusion is especially strong on trace-to-code. citeturn5view2

That result should not be imported as “Qwen + graph is the answer.” It supports the **fusion hypothesis**: heterogeneous evidence families have complementary error patterns.

Weighted RRF is a natural next step only after plain RRF. CombSUM and CombMNZ can work when scores are sensibly normalized, but their dependence on score comparability is a disadvantage when one ranker produces BM25 units, another graph weights and another cosine similarities. Learned fusion becomes appropriate once enough labels exist.

Reranking should also be staged by cost:

\[
\text{deterministic features}
\rightarrow
\text{linear/GBDT/LambdaMART}
\rightarrow
\text{cross-encoder}
\rightarrow
\text{LLM reranker}.
\]

A cross-encoder can be economically sensible if it only sees 20–100 candidates. It is much harder to justify as first-stage retrieval because query/document joint encoding cannot normally be precomputed in the same way as bi-encoder document embeddings. An LLM reranker has an even higher bar: every ranking decision consumes model latency, tokens and potentially API cost.

### Progressive disclosure may dominate one-shot perfection

There is mounting code-agent evidence that retrieval should be considered interactive rather than a single “top-five files” operation.

RepoFormer, published at ICML 2024, learns when retrieval should be skipped for repository-level code completion and reports large online-serving speedups without degrading its task metric; importantly, its result is about **code completion**, so it should not be generalized uncritically to issue-resolution agents. citeturn19search3turn19search15

RepoCoder uses iterative retrieval and generation rather than assuming one retrieval pass is final, and RLCoder explicitly learns retrieval usefulness and a stop signal in repository-level completion. citeturn6academia35turn19academia39

ARB supplies directly agent-oriented evidence of complementary search behavior: static retrievers find context that logged agents miss, while agents also reach useful context absent from a particular static ranking. citeturn5view3

SWE-Explore goes further by evaluating repository exploration under a fixed line budget and reports that modern agentic explorers form a stronger tier than classical retrieval on its benchmark, while line-level coverage and efficient ranking remain differentiators. Its relevance labels are derived from successful trajectories, however, so that benchmark can partly reflect how successful contemporary agents explore rather than an immutable definition of all useful context. citeturn16search5

These results support an architecture such as:

```text
InformationNeed
    ↓
exact/path/symbol resolution when possible
    ↓
cheap diverse candidate generation
    ↓
compact file + symbol + match summaries
    ↓
agent chooses what to inspect
    ↓
targeted relation/search follow-up
    ↓
small exact disclosure
    ↓
optional further search
```

This may be operationally superior to spending a second per agent turn chasing a marginal improvement in a one-shot top-five ranker.


## Operations, benchmarks, and what the literature actually establishes

### Index-once versus query-time economics

The correct cost model for an autonomous software-engineering agent is approximately

\[
C_{\text{lifetime}} =
C_{\text{build}}
+
\sum C_{\text{incremental update}}
+
\sum C_{\text{query}}
+
\sum C_{\text{context tokens}}
+
\sum C_{\text{model calls}}.
\]

Optimizing only `C_query` or Recall@K can make the overall system worse.

For sparse lexical retrieval, indexing is CPU-cheap, storage is relatively compact, and repeated queries are extremely cheap. `bm25s` goes further by eager index-time scoring and mmap-able sparse persistence. citeturn21view1turn21view0

For dense retrieval, a sufficiently expensive initial embedding pass can be reasonable when a repository lives for many agent turns. The unit that changes should be re-embedded; unchanged units should not. This makes an index-once dense experiment scientifically necessary before concluding that CPU embedding cost is prohibitive.

But repository snapshots create hidden costs. Consider:

```text
commit A: file x.py → embedding X_A
commit B: x.py modified → embedding X_B
branch C: old x.py restored
model v2: all vectors incompatible with v1
chunking policy changes: all unit IDs may shift
symbol parser changes: AST units may shift
```

A trustworthy dense index must know **which repository state and representation policy its vectors describe**. Sparse indexes have the same truth problem in principle, but neural representations make rebuilds more expensive.

Late interaction magnifies this because each unit carries many vectors. SPLADE pushes more computation toward neural indexing while preserving sparse retrieval. Cross-encoder reranking does the opposite: almost no repository-side neural index, but recurring query-time model work.

For a coding agent that may issue dozens of repository queries per task, that distinction is decisive.

### Context tokens are an operational resource, not just an evaluation afterthought

ARB's result that the best MRR system and best 8K-token context-yield system differ is exactly the behavior `devtools` should expect. citeturn13search7turn5view2

Whole-file ranking encourages a misleading metric:

\[
\text{“relevant file retrieved”}
\]

even when the relevant evidence occupies 20 lines of a 4,000-line file.

A more agent-economic metric is:

\[
\text{useful evidence per disclosed token}.
\]

SWE-Explore's fixed-line-budget formulation and ARB's budgeted context yield independently reinforce the need for such a measure. citeturn16academia25turn13search7

Thus `devtools` should log at least:

- retrieval latency;
- index build/update time;
- candidate count;
- candidate bytes/tokens;
- disclosed tokens;
- useful disclosed tokens or judged units;
- downstream agent actions after initial retrieval;
- external model calls and their monetary cost where applicable.

### Important systems and benchmarks

| System / benchmark | What it actually tests or contributes | Evidence quality | Main caution for `devtools` |
|---|---|---|---|
| **CodeSearchNet** | Large-scale NL↔function code search | Important historical code-search benchmark | Function/docstring retrieval is not issue-driven repository context; CORE-Bench explicitly identifies this gap. citeturn15view0 |
| **CodeBERT** | Code/NL pretrained representation, including code search | Peer-reviewed code-representation evidence | Not direct repository-agent evidence. citeturn8search4 |
| **GraphCodeBERT** | Adds data-flow structure to code representation | Peer-reviewed | “Graph helps representation learning” ≠ “graph database needed for retrieval.” citeturn8search17 |
| **UniXcoder** | Unified code/text/structure representation | Peer-reviewed | Mostly representation/code-search evidence. citeturn8search2 |
| **RepoFormer** | Selective RAG for repository-level completion | ICML 2024, strong primary evidence | Completion task, not arbitrary SWE-agent retrieval. citeturn19search15 |
| **Aider RepoMap** | Compact repository symbols + dependency-based ranking within token budget | Strong production implementation evidence | Not a controlled proof that PageRank-like ranking is universally optimal. citeturn18view0 |
| **ARB** | File-level coding-workflow retrieval, 427 cases / 25 repos, four retrieval tasks + abstention | Very recent primary benchmark/preprint, highly aligned | Small repository count; benchmark composition matters; authors report four largest repos dominate sample count. citeturn13search1turn5view2 |
| **CORE-Bench** | Conventional code understanding + issue-to-edit + broader-context retrieval | Very large, recent primary benchmark/preprint | Level-3 labels partly arise from agent trajectories and LLM relevance judging; do not treat labels as perfect human truth. citeturn14view2turn14view3 |
| **SWE-Explore** | Ranked code-region exploration under fixed line budget | Very recent primary benchmark | Ground truth derived from successful trajectories; can reflect agent behavior. citeturn16search5 |
| **RepoGraph / LocAgent** | Structural repository representations and graph-guided localization | Direct repository/localization research | System-level gains do not isolate “graph DB” as causal mechanism. citeturn12search0turn12search26 |
| **SPLADE** | Learned sparse expansion | Peer-reviewed/general IR | Strong retrieval evidence but limited direct repository-code evidence. citeturn19search29 |
| **ColBERT/ColBERTv2** | Multi-vector late interaction | Peer-reviewed/general IR | Index-size and runtime tradeoffs; little direct coding-agent validation. citeturn19search6turn19search18 |
| **bm25s** | High-performance Python BM25 variants and persistence | Open-source + technical report | Implementation quality/speed evidence, not code-relevance evidence. citeturn21view1 |
| **rank_bm25** | Simple Python implementations of multiple variants | Reproducible OSS | Convenient baseline/reference rather than proof of effectiveness. citeturn0search2 |

ARB is particularly valuable because it operationalizes the user's “purpose-relative retrieval” concern. It contains code-to-test, comment-to-context, trace-to-code and edit-to-ripple tasks, plus cases where returning no local context is appropriate. It reports that no one retrieval family dominates: Qwen3-Embedding models lead some rank/recall measures, RepoMap leads the reported token-budget yield, and task-level winners differ. citeturn13search1turn13search7

Its benchmark-composition analysis is also a warning against leaderboard worship: the authors report that the four largest repositories comprise a majority of samples and that model rankings can shift under repository-equal rather than sample-weighted aggregation. citeturn5view2

CORE-Bench complements ARB by operating at much larger scale. It includes more than 5,000 issue-to-edit queries across hundreds of repositories and a broader-context level containing thousands of queries and more than 100,000 relevance judgments; it reconstructs repository states before the corresponding change and uses AST-aware or related chunking. citeturn14view2turn14view3

However, its Level-3 construction is not an oracle supplied entirely by human developers. The benchmark extracts browsed context from coding-agent trajectories, subjects it to LLM relevance voting and validates utility with allowlisted agent reruns. That is sophisticated and useful, but it also means the benchmark partially operationalizes “useful context” through contemporary agent behavior and model judgments. citeturn14view2

CORE-Bench's embedding fine-tuning experiment is highly relevant to future Learned Intelligence. It trains on 628 repositories and 53,301 queries with same-repository negatives, keeps its training repositories disjoint from the SWE-bench family used in its target evaluation, and reports substantial gains after in-domain fine-tuning. citeturn15view0

That result is **pressure toward learned retrieval**, not a reason to implement it now. It says that if `devtools` eventually learns a ranker or representation, repository-local hard negatives and task-aligned supervision matter.

### Purpose-relative retrieval

The evidence supports a portfolio mindset more strongly than a universal retriever:

| Information need | Cheap evidence likely to have unusually high value |
|---|---|
| symbol → declaration | exact symbol index first |
| symbol → references | reference index first |
| stack trace → implementation | exact frames, path/symbol search, structural neighborhood; ARB shows RepoMap strength here. citeturn5view2 |
| implementation → tests | naming/path/import/reference evidence + lexical semantics |
| test → implementation | symbols/imports/call edges + lexical |
| feature request → modules | lexical/subtokens/path + semantic retrieval potentially valuable |
| bug report → implementation | error strings + lexical + task semantics; potentially dense |
| edit → ripple | references/calls/tests/co-change; ARB explicitly treats ripple as a distinct task. citeturn13search7 |
| architecture question | repository map/module/symbol summaries and relationship traversal |
| docs question | prose/comment/docs field should receive more weight |
| build/config problem | exact strings, filenames, paths, configuration keys |
| change-impact question | current references plus historical coupling |

This does not require eleven hard-coded retrieval products. It means `InformationNeed` may eventually influence which evidence generators run and how results are combined. The stable domain concept is the **purpose/need**, not “DenseRetrieverForBugReports.”


## Critical audit of `devtools` and the major untested hypotheses

The prior work was scientifically useful but probably **sequenced inefficiently**.

### `K=5` is a serious confounder

The strongest internal warning is already present in the supplied evidence:

> lexical top-5 recovered 10/18 known-useful resources, while top-15 contained all 18.

That means the prior baseline demonstrated a substantial ranking-depth effect *before* structural or semantic complexity was introduced.

A top-five comparison can therefore make a second retriever appear to discover a “new kind” of evidence when it merely promotes a candidate from lexical rank 8 to rank 3.

That is exactly what happened for all eight useful semantic-only candidates in the development CodeRankEmbed experiment: every one had a positive deeper lexical rank.

This does **not** invalidate the semantic result. Promotion from rank 51 to rank 5 can be operationally important. It changes its scientific meaning:

> The experiment demonstrated **ranking complementarity/top-K promotion**, not demonstrated lexical reachability failure.

Future candidate-generator experiments should plot recall curves at least across a useful range such as `K={1,3,5,10,15,20,50,100}` where corpus size permits, then evaluate final disclosure separately.

### Whole-file retrieval may be a larger problem than BM25

The current evidence does not isolate this variable.

If an information need targets one method in a large resource, whole-file BM25 changes term density, length normalization and context cost simultaneously. Dense file embeddings also have to compress an entire large file into one vector, which can be an even more severe representational bottleneck.

Thus moving from file-BM25 to file-embedding can preserve the largest confound.

This should have been tested before drawing architectural conclusions from either family.

### Filename weighting is useful but primitive

`content BM25 + 0.25 × filename-stem BM25` is a sensible cheap baseline, but `0.25` encodes an unverified global assumption about one field. It ignores path, module, declaration, identifier and test evidence. A proper field ablation or rank fusion can reveal whether the existing filename contribution is helping because filenames are genuinely useful or merely compensating for poor source tokenization.

### Query representation is underexplored

If the current lexical retriever searches raw InformationNeed text, then “BM25 weakness” may partly be “query representation weakness.”

Before adding semantic infrastructure, test whether deterministic extraction of:

```text
error literals
path fragments
symbols
stack frames
identifier subtokens
quoted strings
package/module names
natural-language residual text
```

changes retrieval enough to explain the gap.

CORE-Bench's negative/mixed result for automatic rewriting is a warning that simplification is not automatically beneficial; preserving raw request evidence alongside extracted query views is safer. citeturn14view2

### BM25 parameters and variant should be checked, but not fetishized

`k1`, `b`, IDF convention and BM25+/L corrections are inexpensive sensitivity tests. `bm25s` makes them trivial to run reproducibly. citeturn21view0

But spending an entire architectural increment optimizing `k1` to the second decimal would be misplaced. Unit, tokenization and fields encode stronger hypotheses.

A sensible experiment should test a **small preregistered grid**, report whether conclusions are robust, and stop.

### Structural retrieval probably began early, but the experiment was worth doing

The structural experiment was well chosen in one important respect: it compared additional structural candidates with candidate-volume-matched lexical widening. That avoids an easy confound where “structural retrieval wins” merely because it returns more candidates.

Its result—useful candidates unique to both arms and several useful structural candidates with no positive lexical rank—is genuine evidence that at least the tested import-member relationship accesses evidence not reducible to lexical depth in the frozen cases.

So the correct audit is:

> **Sequenced early, but scientifically productive.**

It now belongs as one evidence family in the cheap portfolio rather than as a mandate for generalized graph infrastructure.

### Dense retrieval also began early, and confirmation should stop for now

The CodeRankEmbed development experiment answered several useful questions:

- deterministic replay was achievable;
- semantic ranking was complementary at top K;
- this realization was very expensive on CPU because corpora were repeatedly encoded;
- useful semantic-only top-K candidates were nevertheless lexically reachable deeper down;
- lexically unreachable semantic candidates were not useful in the eight development needs.

That is enough information to change the next experiment.

Running the sealed confirmation now would mostly refine an estimate for a configuration that is not yet being compared against the strongest cheap baseline and whose corpus computation does not model a proper persistent dense index.

Therefore:

> **Increment 26: remain suspended.**

Not “dense retrieval rejected.”
Not “experiment invalid.”
Not “run confirmation to be thorough.”

The frozen confirmation set is more valuable preserved for a future genuinely competitive comparison than consumed now.

### Candidate generation may already be much closer to solved than ranking

The local top-15 finding makes this plausible.

ARB independently contains a related clue: across several of its positive task families, the union of evaluated baselines leaves relatively few examples missed by *every* baseline at top-20, indicating substantial portfolio coverage even while individual rankers differ. citeturn5view2

This suggests an important diagnostic decision tree:

```text
Is Recall@50 poor?
    yes → candidate-generation problem

Is Recall@50 high but top-5 / MRR poor?
    yes → ranking problem

Are ranks good but useful tokens / budget poor?
    yes → disclosure/unit problem

Does the agent cheaply recover after one inspection?
    yes → progressive-search problem may matter more than one-shot rank

Are some need classes systematically bad?
    yes → purpose-conditioned evidence problem
```

Do not answer a ranking problem by adding ever more candidate generators.

### Major untested hypotheses

| Untested or under-tested hypothesis | Cost | Information value | What it could falsify |
|---|---:|---:|---|
| Broader `K` / recall curves | Tiny | **Very high** | “We need another candidate generator” |
| File vs function/class/AST-unit retrieval | Low | **Very high** | “Ranking algorithm is the main weakness” |
| Exact symbol/path/error routing | Low | **Very high** | Retrieval for deterministic needs |
| Exact identifier + subtoken indexing | Low | **Very high** | Semantic model needed for naming variation |
| Path/module/symbol/test fields | Low | **Very high** | Current lexical baseline is representative |
| BM25F or separate-field RRF | Low | High | Neural retrieval needed for field semantics |
| Char n-gram auxiliary ranker | Low–moderate | High | Embeddings needed for spelling/morphology |
| Deterministic query extraction | Low | High | Raw-task lexical retrieval is sufficient |
| BM25 formulation/parameter sensitivity | Tiny | Medium | Current baseline happened to be poorly parameterized |
| Lexical + structural RRF | Tiny | **Very high** | Learned fusion required |
| Lexical variants + structural + RepoMap union | Low | High | Dense required for candidate recall |
| Deterministic candidate reranking | Low | High | ML ranker required |
| LR/SVM/GBDT/LambdaMART | Moderate | **High if recall already sufficient** | Neural reranker required |
| References/callers/tests relation families | Moderate | High by task | Generic graph required |
| Co-change/history features | Moderate | Medium-high for ripple | Semantic retrieval needed for change impact |
| Repository vocabulary expansion/PRF | Moderate | Medium | Neural semantic expansion required |
| Persistent-index dense retrieval | Moderate–high | High | Dense operationally unjustified |
| SPLADE | High | High but later | Dense necessary for semantic expansion |
| ColBERT/late interaction | High | Medium currently | Single-vector representation insufficient |
| Cross-encoder reranking | High recurring cost | Medium-high if ranking remains hard | Lightweight ranker insufficient |
| LLM rewriting/reranking | High recurring cost | Low current priority | Deterministic/neural bounded ranking insufficient |


## Evaluation and falsification program

A scientifically defensible program should **separate candidate-generation experiments from ranking and disclosure experiments**.

### Evaluation population and split discipline

Local `devtools` InformationNeeds are valuable for fast iteration but insufficient for architectural claims.

Use at least three evidence strata:

**Internal development set:** frozen `devtools` needs for rapid diagnosis.

**External validation repositories:** repositories absent from all tuning. ARB is attractive because its tasks represent distinct workflows and use frozen base commits. citeturn13search1

**External broader-context test:** selected CORE-Bench tasks, ideally preserving its repository-separated discipline and exact repository-state filtering. citeturn14view3

SWE-Explore can provide a complementary region/budget evaluation rather than another file-retrieval score. citeturn16search5

Any learned experiment must split by **repository**, not merely random query. Random query splitting allows repository vocabulary, architecture, naming conventions and even nearly identical change contexts to leak across train/test.

Temporal leakage should also be checked wherever the corpus is historical: the retriever must only see the repository state that existed at the InformationNeed's snapshot. CORE-Bench explicitly reconstructs pre-change repository states for this reason. citeturn14view2

### Metrics should reflect the stage being tested

For **candidate generation**:

\[
Recall@K
\]

is primary. MRR is not a pure candidate-generation metric because it rewards ranking position.

Report recall curves, not one K.

For **ranking**:

- MRR;
- NDCG@K;
- Recall@small-K;
- pairwise wins/losses on known-useful resources.

CORE-Bench uses NDCG@10 for top-rank quality and Recall@100 for context coverage, illustrating the distinction. citeturn14view2

For **disclosure/capacity**:

\[
\text{useful resources per 1K tokens}
\]

\[
\text{useful code lines per disclosed line}
\]

\[
\text{gold/useful coverage at token budget } B
\]

ARB's budgeted context yield and SWE-Explore's line-budget evaluation provide precedents. citeturn13search7turn16academia25

For **economics**:

\[
\frac{\text{useful candidates}}{\text{query ms}},
\quad
\frac{\text{useful context}}{\text{CPU second}},
\quad
\frac{\text{downstream successes}}{\$},
\]

plus absolute index-build, update and disk cost.

For **agents**, ultimately measure downstream task success and search cost. But retrieval-only experiments remain necessary because end-to-end agent outcomes have high variance and can hide which subsystem caused an improvement.

### Do not label every changed file “relevant” without qualification

Patch files are convenient ground truth, but “must be edited” and “useful for understanding” are different concepts. CORE-Bench explicitly separates issue-to-edit localization from broader context for this reason. citeturn14view2

`devtools` evaluation should ideally have graded judgments:

```text
2 = directly necessary / strongly useful
1 = useful supporting context
0 = not useful for this InformationNeed
```

This allows NDCG and context-yield metrics to represent supporting information without pretending every potentially useful file must be edited.

### Falsification gates

The experiment ladder should have explicit stop conditions.

**Before structural expansion:** if code-aware lexical + exact resolution reaches the desired candidate recall and downstream search cost, do not add more structure merely because structure is available.

**Before lightweight ML:** if RRF/deterministic reranking achieves equivalent ranking within a predeclared practical effect margin, do not train a ranker.

**Before dense retrieval:** if cheap portfolio recall and context yield are already adequate, or remaining failures are predominantly resolvable by relation indexes, do not add a vector index.

**Before late interaction:** demonstrate that a competitive single-vector dense model produces errors plausibly caused by representation compression and that those errors matter downstream.

**Before cross-encoder/LLM reranking:** show that bounded cheap LTR leaves economically important ordering errors.

The practical effect margin should be chosen from agent economics, not statistical convenience. A one-point Recall@20 increase that adds 500 ms to every agent action may be negative; a one-point improvement obtained through a one-time index cost and effectively free queries may be worthwhile.

### Falsification-oriented experiment sequence

The recommended ordering is:

```text
measurement correctness
        ↓
exact resolution/routing
        ↓
K and retrieval-unit ablation
        ↓
code-aware lexical representation
        ↓
fielded sparse retrieval
        ↓
cheap heterogeneous fusion
        ↓
typed relation additions
        ↓
deterministic / lightweight learned ranking
        ↓
persistent-index neural retrieval
        ↓
neural sparse vs dense comparison
        ↓
late interaction
        ↓
expensive neural/LLM reranking
```

This differs subtly but importantly from the sequence proposed in the research brief. **Structural retrieval should not necessarily wait until after fusion as a whole.** Existing import-member structural evidence already exists and is cheap at query time, so it should participate in early fusion experiments. What should wait is *additional graph infrastructure*.

### Priority matrix

| Tier | Hypothesis | Why now / why later | Exit criterion |
|---|---|---|---|
| **Tier 1** | `K`/recall-depth curves | Essentially free and directly challenges prior conclusions | Know whether misses are reachability or ranking |
| **Tier 1** | Exact symbol/path/error routing | Cheap; avoids probabilistic search for deterministic needs | Measure percentage of needs/candidates resolved exactly |
| **Tier 1** | File vs declaration/AST-unit retrieval | Could dominate scoring-algorithm differences | Find unit/disclosure policy with best recall and token yield |
| **Tier 1** | Identifier splitting + exact identifiers | Strong code-specific rationale, trivial compute | Quantify gains by task |
| **Tier 1** | Path/filename/module/symbol/content fields | Current 0.25 filename score is incomplete | Determine independent field value |
| **Tier 1** | Lucene/Robertson/BM25+/BM25L/ATIRE sensitivity | `bm25s` makes it cheap | Establish whether formula choice is material |
| **Tier 1** | Char n-gram auxiliary | Cheap distinct morphology hypothesis | Keep only if unique useful candidates justify storage |
| **Tier 1** | RRF / union of lexical + existing structural | Very low complexity; ARB supports complementarity | Determine whether cheap fusion closes current gaps |
| **Tier 1** | Compact repository/symbol map disclosure | Aider/ARB suggest high token-efficiency value | Measure downstream navigation and context yield |
| **Tier 2** | References/callers/callees/test relations | Relation-specific value plausible after lexical controls | Add only relations with unique useful yield |
| **Tier 2** | PRF/repository vocabulary expansion | Cheapish semantic bridge but topic-drift risk | Retain only if robust cross-repo |
| **Tier 2** | Deterministic feature reranker | Cheap if top-K recall good | See whether handcrafted ordering solves top-K |
| **Tier 2** | LR / linear SVM | Direct CIT synergy, negligible inference | Beat deterministic ranking cross-repository |
| **Tier 2** | GBDT / LambdaMART | Best fit to heterogeneous evidence if labels adequate | Show stable gain across repositories/tasks |
| **Tier 2** | Co-change/history features | Purpose-specific, especially ripple | Demonstrate unique value on change-impact tasks |
| **Tier 2** | Purpose-conditioned portfolios | ARB task variation supports pressure | Show task conditioning beats universal fusion robustly |
| **Tier 3** | Persistent dense retrieval with competitive current model | Genuine semantic hypothesis but requires index lifecycle | Must beat strong cheap portfolio on useful/economic metric |
| **Tier 3** | SPLADE/learned sparse | Distinct semantic-expansion hypothesis | Justified if lexical vocabulary mismatch remains |
| **Tier 3** | Cross-encoder reranking | Expensive but bounded | Only if lightweight ranker leaves material errors |
| **Tier 3** | Late interaction / ColBERT | Large index and weak direct code-agent evidence | Require single-vector failure evidence |
| **Defer** | Generic unified graph/database | No demonstrated operation currently requires it | Reconsider after repeated multi-hop generic graph needs |
| **Defer** | Unbounded multi-hop traversal | High false-positive/complexity risk | Require task-specific evidence |
| **Defer** | PageRank/centrality as universal relevance | Centrality and need-relative relevance differ | Use only as map/feature unless validated |
| **Defer** | LLM query rewriting | CORE-Bench shows rewriting can hurt | Only after deterministic query views fail |
| **Defer** | LLM reranking on every query | High recurring latency/tokens/cost | Require downstream benefit unattainable cheaper |
| **Defer** | Training a custom foundation retriever | Data/compute/infra far beyond current evidence need | Reconsider after simpler supervised ranking is saturated |
| **Defer now** | Increment 26 CodeRankEmbed confirmation | Answers a lower-priority configuration question | Preserve frozen set; revisit only if still decision-relevant |

### What Increment 27 should actually become

A good scope would be:

> **Increment 27: Repository Retrieval Foundations — unit, representation, fielding, fusion, and ranking-depth falsification.**

It should not add a generic retrieval framework.

Its experimental matrix should include four controlled blocks.

**Retrieval depth and unit.** Evaluate file, declaration/AST unit and possibly fixed-window control at multiple `K`; record both unit recall and parent-resource recall.

**Lexical representation.** Compare current tokenization with exact identifiers + normalized subtokens; optional char n-gram auxiliary; small BM25-variant/parameter sensitivity grid.

**Fields and query views.** Content, filename, path, module, declaration/symbol, comments/docstrings, tests where identifiable; raw InformationNeed plus deterministic identifier/path/error extraction.

**Fusion/ranking.** Union/interleaving/RRF across the strongest cheap lexical views and the already-existing imported-member structural arm. Then test one deterministic feature reranker if the candidate pool is demonstrably high recall.

Every run should record separately:

```text
index build time
index size
incremental update time
query time
candidate count
candidate unit
candidate parent resource
native score/rank
evidence family
usefulness judgment
resource/token size
disclosure budget
```

That dataset will be considerably more valuable for later Learned Intelligence than another isolated model leaderboard result.


## Learned Intelligence, CIT convergence, and architectural implications

### Lightweight ML should probably become the next learned direction

The CIT 52600 project is unusually well aligned with the highest-value remaining scientific question:

> Once cheap heterogeneous candidate generation is reasonably high recall, can a lightweight learned model rank repository context better than BM25 or hand-built fusion?

The planned methods map cleanly onto unresolved hypotheses:

| CIT method | `devtools` question it can answer |
|---|---|
| TF-IDF + Logistic Regression | Does supervised lexical relevance beat unsupervised term weighting? |
| TF-IDF + Linear SVM | Does a maximum-margin sparse decision boundary improve ranking/classification? |
| Gradient-boosted feature ensemble | Can lexical + field + structural + metadata evidence be combined better than fixed weights/RRF? |
| Embeddings + MLP | Does learned semantic representation add useful ranking information once candidate generation is controlled? |
| BM25 baseline | Necessary anchor for all comparisons |

ARB is particularly useful because its distinct workflow tasks make it possible to test whether one learned ranker generalizes or task-conditioned models are required. citeturn13search1

CORE-Bench supplies a much larger issue-driven corpus and demonstrates both the value and danger of in-domain learning. Its authors use repository-disjoint training relative to the SWE-bench evaluation family and same-repository negative sampling, a design worth emulating. citeturn15view0

For the CIT project to generate maximally useful `devtools` evidence:

**Use repository-separated splits.** Do not randomly split query-document pairs.

**Use repository-local hard negatives.** Random files from unrelated repositories make classification artificially easy. CORE-Bench's same-repository negative construction is a useful precedent. citeturn15view0

**Separate candidate generation from ranker evaluation.** Fix a candidate pool—perhaps top 50 or union-of-retrievers—and train models to rank within it. Otherwise improved retrieval recall and improved learned ranking become impossible to disentangle.

**Macro-average by repository and task as well as micro/sample-weight.** ARB demonstrates that repository imbalance can alter conclusions. citeturn5view2

**Include economics.** Training time is less important than repeated inference latency, feature computation and context savings.

**Do not force embeddings into the production architecture just because “embeddings + MLP” is a course arm.** It is an experimental comparator.

A particularly high-value CIT experiment is:

```text
Candidates =
union(
    code-aware lexical top-N,
    exact/symbol evidence,
    current structural additions
)

Features =
[
    lexical ranks,
    field ranks,
    exact-name indicators,
    subtoken overlap,
    structure indicators,
    family-agreement count,
    resource type/size,
    optional dense similarity
]

Models =
logistic regression
linear SVM
GBDT
LambdaMART if practical

Compare against =
BM25
RRF
deterministic feature scoring
```

That experiment can answer whether the next production investment should be **better training/ranking** rather than another retriever.

### Clean boundary with Learned Intelligence

The retrieval subsystem should own:

```text
candidate generation
repository-specific feature meaning
feature extraction
InformationNeed/task metadata
candidate/usefulness evaluation contracts
application of a supplied model
fusion/disclosure policy
```

Learned Intelligence should eventually own generic reusable concerns such as:

```text
training execution
model artifact/version management
hyperparameter/search machinery
train/validation lifecycle
model serialization
generic predictor loading/runtime
provenance/metrics
```

The exact interface should not be over-designed now.

Architecturally, B-0002 should be able to say roughly:

> “Score these candidates using learned capability version X and feature schema Y.”

It should not implement “our own mini-ML platform” because repository retrieval happened to need logistic regression.

### Supported architectural implications now

The following boundaries have enough evidence to be treated as durable:

**Repository truth is separate from retrieval evidence.** Exact symbols/imports/references belong to Repository Intelligence even when a retriever later uses them.

**Context disclosure is separate from ranking.** Small-unit retrieval and whole-resource disclosure must be allowed to differ.

**InformationNeed is separate from query text.** Raw user text is one observation, not the semantic definition of the need.

**Index identity must include repository state.** This is necessary for any cached sparse, structural or learned representation.

**Evidence provenance should be retained.** A candidate should be able to say “found by content lexical at rank 7, symbol exact at rank 1, imported-member relation from seed X,” because that provenance is valuable for evaluation and future rankers.

**Exact resolution should not be forced through a probabilistic ranker.** A known qualified symbol is a resolution problem first.

**Multiple candidate evidence families must be composable.** The local structural result and ARB fusion evidence both support this. citeturn5view2

### Architectural pressure, but not yet a justified abstraction

There is pressure toward:

- a common experiment record for candidate/evidence observations;
- explicit retrieval-unit identities with parent-resource projection;
- field-aware lexical indexes;
- purpose/task metadata;
- index lifecycle/version metadata;
- rank fusion as a reusable operation;
- optional learned scorer consumption;
- compact repository/symbol summaries;
- incremental indexing.

These are pressures because multiple experiments are likely to need them. They should become canonical only after recurring use demonstrates stable semantics.

### Explicitly not justified

The evidence does **not** presently justify:

- a generic graph database as core architecture;
- a universal “graph retriever” abstraction;
- mandatory vector-database infrastructure;
- a canonical `DenseRetriever` domain concept merely because one experiment used embeddings;
- SPLADE-specific abstractions;
- ColBERT/multi-vector infrastructure;
- a universal normalized `relevance_score` shared across BM25, relations and embeddings;
- a single universal top-K;
- automatic LLM query rewriting;
- automatic LLM reranking;
- generic multi-hop traversal;
- PageRank as repository relevance;
- a parallel model-training framework inside retrieval;
- training a custom neural retriever;
- assuming a single retrieval unit;
- assuming a candidate's retrieval unit is its disclosure unit.

Most importantly:

> **An experiment-local implementation of BM25+, RRF, char n-grams, LambdaMART, SPLADE or ColBERT does not create a durable domain entity of the same name.**

The durable concepts are more likely to be things such as repository evidence, information need, retrieval unit, candidate, purpose-relative usefulness, resource identity, repository snapshot, disclosure and learned capability. Even several of those should remain provisional until usage stabilizes.


## Final decision and minimum strong retrieval architecture

The research changes the interpretation of the existing roadmap.

### Increment 26

**Recommendation: remain suspended.**

The sealed semantic confirmation should **not proceed now**.

The exact reasons are cumulative:

1. The development result shows semantic top-K complementarity but no useful candidate wholly unreachable by deeper lexical retrieval.
2. The local lexical top-15 result already raises a serious `K=5` confound.
3. The current lexical baseline does not yet test important code-specific representations, fields or units.
4. The dense experiment repeatedly encoded historical corpora, so its operational cost is not a fair production architecture test.
5. CodeRankEmbed is only one dense model; recent CORE-Bench evidence shows substantial variation among modern retrievers and stronger results from newer/larger or in-domain models. citeturn15view2turn15view3
6. External evidence still supports dense retrieval as a real future hypothesis, so confirming this particular configuration would neither validate nor falsify the family.
7. The frozen confirmation set is more valuable if reserved until there is a decision-worthy contest between a strong cheap baseline and a realistic index-once semantic system.

If later Tier-1/Tier-2 results show that semantic evidence remains decision-relevant, re-enter dense retrieval with a proper persistent index and at least one currently competitive model, not repeated corpus encoding.

### Increment 27

**Recommendation: make it the Retrieval Foundations Falsification Matrix.**

The minimum experiment set should be:

```text
current file BM25
    vs
same BM25 at broader K
    vs
code-aware identifier/subtoken BM25
    vs
fielded content/path/name/symbol retrieval
    vs
AST/declaration-unit retrieval
    vs
cheap fusion of those views
    + current imported-member structural evidence
```

Only after that, if candidate recall is high but rank quality poor:

```text
deterministic rerank
    vs
RRF
    vs
lightweight ML ranker
```

A char-n-gram auxiliary arm and a small BM25 variant sensitivity sweep are sufficiently cheap to include without turning them into architecture.

### The falsification ladder

**Tier 1 — test immediately**

Exact resolution; K curves; retrieval-unit ablation; code-aware tokenization; exact identifier + subtokens; fielded retrieval; char n-gram auxiliary; small BM25-variant sensitivity; raw-vs-deterministically-extracted queries; RRF/union with the existing structural family; repository/symbol-map progressive disclosure.

These experiments are inexpensive and can falsify the need for almost everything below them.

**Tier 2 — only if Tier 1 leaves identifiable gaps**

Additional typed relations such as references, callers/callees and test links; change/co-change evidence; PRF/repository vocabulary expansion; deterministic candidate reranking; logistic regression; linear SVM; gradient boosting/LambdaMART; purpose-conditioned fusion.

This tier attacks specific observed error modes rather than generic sophistication.

**Tier 3 — require evidence before infrastructure**

Persistent-index dense retrieval with a competitive modern model; neural sparse retrieval such as SPLADE; bounded cross-encoder reranking; potentially late interaction.

Dense should move earlier within this tier than ColBERT because single-vector indexes are operationally simpler and there is direct 2026 coding-agent evidence for competitive embedding retrieval. ARB reports strong Qwen3 embedding results, while CORE-Bench shows both strong modern embeddings and meaningful in-domain adaptation gains. citeturn13search1turn15view2

**Reject/defer at present**

Generic graph infrastructure, generalized multi-hop graph search, always-on LLM query rewriting, always-on LLM reranking, custom foundation-model retrieval training, and production multi-vector infrastructure.

These may eventually be justified. Nothing in the present evidence makes them the cheapest answer to a demonstrated problem.

### The minimum strong production hypothesis

If forced to design the smallest serious repository-context system today, I would build the following:

```text
Repository Intelligence
│
├─ exact resource/path/module/symbol resolution
├─ typed relation indexes
│    ├─ imports
│    ├─ definitions/references
│    └─ additional relations only when validated
│
├─ code-aware sparse indexes
│    ├─ source content
│    ├─ exact identifiers
│    ├─ identifier subtokens
│    ├─ filename/path/module
│    ├─ symbol/declaration names
│    └─ comments/docs/tests as separate evidence fields
│
InformationNeed
│
├─ preserve raw text
├─ deterministic extraction of code-specific clues
└─ task/purpose metadata when known
│
Candidate generation
│
├─ exact resolution where applicable
├─ sparse field/unit searches at reasonably broad K
├─ current validated structural relations
└─ optional repository-map evidence
│
Cheap fusion
│
└─ union / RRF
│
Bounded ranking
│
├─ deterministic features initially
└─ lightweight learned ranker if evidence justifies it
│
Context disclosure
│
├─ compact symbol/resource summaries
├─ declaration/window inspection
├─ agent-directed follow-up search
└─ exact larger disclosure only when useful
```

No vector database is required by that architecture.

No graph database is required.

No learned model is required initially.

But none of those possibilities is architecturally prohibited.

That is an important difference between **minimality** and **premature exclusion**.

### What to build or test first, second, and third

**First: strengthen and properly characterize cheap retrieval.**

Test `K`, retrieval unit, exact resolution, code-aware identifiers, fields and deterministic query extraction together with token-budget metrics. This is first because the current local evidence already says `K=5` can hide lexically reachable useful resources, and because none of the neural or structural experiments establishes that the current lexical *representation* is strong.

The objective is not “make BM25 win.” It is:

> **Determine the true ceiling of inexpensive code-aware sparse retrieval and exact repository intelligence.**

**Second: combine complementary cheap evidence and diagnose whether the residual problem is recall or ranking.**

Fuse the strongest lexical views with the already-proven local structural slice using union/RRF; add compact repository/symbol map disclosure; examine Recall@20/50 versus top-rank and context-yield metrics.

ARB provides direct contemporary evidence that heterogeneous fusion can improve repository retrieval and that different task types favor different families. citeturn5view2turn13search7

If broad candidate recall is already high, stop inventing candidate generators.

**Third: learn ranking before buying expensive retrieval, unless the miss analysis clearly demands semantic candidate generation.**

Use the CIT 52600 work to test LR/SVM/GBDT/LambdaMART-style ranking over the rich cheap evidence pool. This route is CPU-cheap, operationally simple, scientifically interpretable and directly compatible with the planned Learned Intelligence boundary.

Only if the remaining misses are consistently **lexically and structurally unreachable yet semantically recognizable** should the next experiment be persistent-index dense or learned-sparse retrieval.

That is the decisive falsification principle:

> **Do not ask “what is the strongest retriever we can build next?” Ask “what is the cheapest experiment that could prove we do not need it?”**

On the evidence available today, the most plausible destination is not a single perfect retriever. It is a small, purpose-aware portfolio:

\[
\boxed{
\text{exact repository intelligence}
+
\text{strong code-aware sparse retrieval}
+
\text{a few validated typed structural signals}
+
\text{cheap rank fusion}
+
\text{optional lightweight learned ranking}
+
\text{progressive disclosure}
}
\]

with neural sparse, dense, late-interaction and expensive reranking retained as escalation paths rather than presumed architectural foundations.

That conclusion is consistent with the strongest current coding-agent evidence: repository retrieval is heterogeneous, rank and context efficiency are not the same objective, task winners differ, static retrieval and interactive agents are complementary, and conventional code-search success does not reliably predict issue-driven repository retrieval. citeturn13search1turn13search4turn16search5
