# Structural Repository Retrieval for `devtools`: Typed Repository Knowledge, Graph Views, and Candidate Generation

## Executive conclusion

The strongest minimal architecture supported by the evidence is **not “build a repository graph.”** It is:

> **Keep deterministic repository relationships as native, typed Repository Intelligence with direction, provenance, qualification, snapshot identity, and dependency state; maintain only the indexes needed to traverse those facts efficiently; and, for retrieval experiments, construct ephemeral typed structural projections from selected relationship families around explicitly identified seeds.**

This is materially different from both “one universal graph” and “many permanently maintained graph views.”

A unified heterogeneous graph **can** preserve relation semantics: Joern's Code Property Graph is explicitly a directed, edge-labeled, attributed multigraph with typed nodes and multiple relation kinds, and it combines syntax, control-flow, data-flow, and higher-level overlays. That proves that “one graph” need not mean “untyped semantic soup.” It does **not** prove that `devtools` needs either a universal graph domain abstraction or graph storage. Joern itself moved away from general-purpose graph-database storage, while Kythe makes the opposite architectural distinction especially clear: canonical analysis facts may be stored neutrally and transformed into separate serving indexes or graph forms according to the query workload. citeturn14view0turn14view2

Conversely, separate typed graph views are useful **semantically**, but there is little justification for independently materializing and maintaining an imports graph, calls graph, references graph, inheritance graph, tests graph, and so on. The same effect can usually be obtained more safely from canonical relation knowledge plus source- and target-keyed indexes. SCIP is a useful counterexample to “repository intelligence requires a graph database”: its language-agnostic index represents enough semantic information to power definition, reference, and implementation navigation without making a universal graph abstraction the center of the architecture. citeturn14view1

The research literature likewise does not establish graph retrieval as a generally superior repository-retrieval paradigm. Successful systems use quite different structures for quite different tasks: Aider ranks a file dependency/reference graph to compress a repository map; RepoGraph retrieves k-hop neighborhoods around definition/reference structure; LocAgent uses four explicit relation families plus lexical entity indexes and an LLM-controlled type-aware traversal; GraphCoder uses control/data-dependence structure for code completion; RANGER combines a large knowledge graph, embeddings, Cypher, and MCTS. Those results are evidence that **particular structural relations can supply useful evidence**, not that graphness itself is the source of the gain. citeturn21view0turn19view2turn18view0turn19view3turn19view0

The existing `devtools` evidence makes one conclusion particularly strong: **do not run another experiment that conflates structural candidate generation with fixed-K admission.** Your Increment 20–24 results chiefly falsified a particular way of inserting import-derived candidates into K=5. They did not adequately test whether typed structural relationships enlarge the consideration surface usefully because the candidate-generation question was entangled with displacement and ranking. The fact that lexical top-15 contained all 18 known-useful resources in the supplied frozen material makes lexical widening the mandatory control for any next experiment.

My recommendation for Increment 25 is therefore:

**Test bounded, one-relation-hop candidate generation at resource level from lexical seeds using existing qualified imports plus one new, independently valuable Repository Intelligence family: declaration-grounded references, with call-position references available as a narrower subtype.** Compare each family independently, their union, and their overlap against lexical widening at the **same candidate volume**. Preserve direction and exact path provenance. Do not put the results into K=5. Do not run PageRank. Do not perform unconstrained multi-hop traversal. Do not construct a production `Graph`, `GraphNode`, `GraphEdge`, generic `Candidate`, normalized relevance score, vector database, or learned ranker.

At the same time, `devtools` should **not let a structural research program delay semantic retrieval evaluation**. Recent repository-localization work reports substantial gains from dense retrieval over BM25 on some benchmarks, while RepoCoder, Repoformer, RANGER, and other systems show that semantic and structural signals are often complementary rather than substitutes. The fair sequence is therefore: **structural and pretrained-semantic retrieval should be evaluated as separate arms on the same frozen cross-repository tasks, concurrently at the research level; they should not yet be combined in production.** citeturn18view0turn6academia39turn6academia38turn19view0

The resulting architecture remains faithful to the distinctions you already have:

\[
\text{repository fact}
\ne
\text{retrieval evidence}
\ne
\text{purpose usefulness}
\ne
\text{ranking/capacity}
\ne
\text{Context disclosure}.
\]

Nothing found in this investigation provides a compelling reason to collapse those boundaries.

## What structural retrieval actually means

For `devtools`, I would define **structural repository evidence** narrowly:

> **Evidence whose retrieval signal comes from a repository relation, topology, program structure, or repository-history structure whose truth can be established independently of the current InformationNeed.**

That definition matters. “A calls B” may be Repository Intelligence. “B will probably help answer this InformationNeed because A calls B” is retrieval interpretation. “B is more useful than C for this bug-fixing need” is purpose-relative relevance. “B gets one of five slots” is ranking/capacity. “Expose only B's signature rather than its body” is Context disclosure.

This definition does not require that the underlying representation literally be a graph. An adjacency index, cross-reference table, symbol index, parent-child index, or temporal co-change table can all expose structural evidence.

A useful taxonomy is:

| Structural family | Repository fact | Typical node/domain level | Likely retrieval role | Principal danger |
|---|---|---|---|---|
| **Containment / declaration structure** | file contains class; class contains method; occurrence realizes declaration | occurrence, subject, resource | seed grounding, granularity conversion, navigation | confusing “nearby/contains” with relevance |
| **Binding / reference structure** | occurrence refers to declaration/subject | occurrence → subject | find consumers, definitions, implementations, change impact | ambiguous names and partial static resolution |
| **Imports / module dependencies** | module/resource contains qualified import of another module/subject | resource/module | dependency context, configuration/package tracing | broad utility modules become hubs; import ≠ runtime dependency |
| **Calls / invocation** | call occurrence resolves or may resolve to callable subject | occurrence/subject | behavioral neighborhood, caller/callee candidate generation | dynamic dispatch; large caller sets; library utility hubs |
| **Inheritance / implementation / type structure** | class extends base; method overrides; implementation satisfies known contract | subjects | interface changes, implementations, subtype effects | implicit protocols and dynamic typing |
| **Test / verification structure** | test statically references production subject; coverage execution observes test→code | test/resource/subject | bug fixing, validation, impact analysis | static relation and dynamic coverage are different facts |
| **Build / configuration structure** | target uses source; package exposes entry point; config selects plugin/test suite | build target/resource/subject | build failures, packaging, executable topology | language/tool-specific semantics |
| **Control/data-flow structure** | value/control dependence exists under an analysis definition | statement/expression | completion, security, precise behavioral questions | high derivation cost; language-analysis complexity |
| **Repository topology** | same package/directory/workspace; path ancestry | resource | cheap locality prior/control condition | physical proximity is weak semantic evidence |
| **Temporal/change structure** | resources changed together under a stated history/window definition | resource/subject across snapshots | historical localization, maintenance coupling | correlation is not dependency; snapshot/history leakage |
| **External-dependency structure** | repository declaration resolves to package/library artifact | subject/resource → external subject | API migration, build/config understanding | explosive external universe and version-state ambiguity |

Containment is particularly important to avoid misclassifying. It is often essential infrastructure for structural retrieval—e.g. map a lexically retrieved file to its declarations, or a referenced declaration back to its owning resource—but that does not make containment itself a strong relevance relation. A file containing a function does not imply that every sibling function should become a retrieval candidate.

Likewise, **repository topology should probably remain a weak structural baseline rather than a privileged relation family**. Path locality is cheap and sometimes useful, but it is exactly the sort of relation against which semantic relationships should prove that they are doing more than returning nearby files.

The literature reinforces the importance of distinguishing relation families. LocAgent represents directory/file/class/function nodes but keeps `contain`, `import`, `invoke`, and `inherit` as separate directed relations; its traversal API lets the agent choose relation types, node types, direction, and hop count. That design is important evidence for *typed composition*, even though it does not establish that LocAgent's single heterogeneous physical graph is the best representation for `devtools`. citeturn18view0

The same point appears in more general heterogeneous-network research. Multilayer-network work treats multiple relationship layers as information that can be retained rather than automatically collapsed, while heterogeneous information-network methods such as meta-path ranking explicitly assign meaning to particular sequences of relation types. These ideas are relevant to repository retrieval because `calls`, `imports`, `contains`, and `inherits` have distinct meanings; they do **not** imply that repository traversal should immediately adopt random-walk or meta-path-ranking machinery. citeturn10academia38turn11academia22

**Mathematical graph complements are not the relevant notion of complementarity.** A complement graph replaces adjacency with non-adjacency on the same vertex universe. Repository retrieval instead asks whether different *evidence relations* cover different useful resources or fail in different ways. Graph-sandwich results likewise address a different formal problem. They should not influence this architecture unless a future retrieval problem is explicitly formulated in those terms.

The relevant idea is **evidence-layer complementarity**:

\[
C_{\text{imports}}(q),\;
C_{\text{references}}(q),\;
C_{\text{calls}}(q),\;
C_{\text{semantic}}(q),\ldots
\]

can remain separately attributable even if their candidate sets are eventually unioned. Their intersections can themselves become useful observations without declaring a universal score:

\[
r \in C_{\text{calls}}(q) \cap C_{\text{semantic}}(q)
\]

means “this resource received two independently interpretable supports,” not “its relevance is 0.83.”

That distinction is central to the minimal architecture.

## Existing-system evidence

The strongest publicly documented systems do **not** converge on one graph architecture.

| System / research | What is actually documented | What it establishes | What it does **not** establish |
|---|---|---|---|
| **Aider** | Repository map contains key symbols and definitions; Tree-sitter derives definitions/references. For large repos Aider ranks a graph whose nodes are source files and whose edges represent dependencies, selecting repo-map material under a token budget. citeturn21view0turn21view1 | Structural/reference information can help compress global repository context. | That Aider maintains a universal repository knowledge graph, or that its graph is a general candidate-retrieval architecture. |
| **Sourcegraph Cody** | Current docs list keyword search, Sourcegraph Search, and a Code Graph as distinct context sources; Code Graph uses relationships/interconnections among code elements. citeturn21view2 | Production coding assistance can combine lexical/search and structural evidence. | Public docs cited here do not expose enough ranking detail to reproduce a single “Cody graph retrieval algorithm.” |
| **SCIP / Sourcegraph code intelligence** | Language-agnostic indexing protocol supports go-to-definition, references, and implementations; multiple language-specific indexers emit the protocol. citeturn14view1 | Rich code relations can be represented and served without making a graph DB the domain model. | Retrieval relevance or agent candidate ranking. |
| **Cursor** | I could not verify from a current primary technical description that Cursor uses a single repository graph, nor find sufficiently detailed public ranking/graph semantics to support that claim. | Nothing architectural should be inferred from the phrase “codebase understanding.” | Claims that Cursor proves a universal repo graph architecture should be treated as unverified. |
| **RepoGraph** | Builds repository-level definition/reference structure with `contain` and `invoke` style relations and retrieves k-hop ego neighborhoods; plugging it into multiple SWE-bench systems improved reported outcomes. citeturn19view2turn8view0 | A small, task-specific structural representation can augment other software-engineering systems. | That arbitrary relationship expansion is useful, or that its line-level graph should become a general RI model. |
| **LocAgent** | Directed heterogeneous graph with directory/file/class/function nodes and `contain`, `import`, `invoke`, `inherit` relations; also builds exact/name/BM25 indexes and exposes type-aware BFS traversal. citeturn18view0 | Typed, directional graph exploration plus lexical/entity lookup can support localization. | Pure graph advantage: agent reasoning, lexical indexes, multiple trajectories, and fine-tuning are intertwined with the result. |
| **GraphCoder** | Uses a code-context graph containing control-flow and data-/control-dependence, followed by coarse-to-fine retrieval for repository-level completion; reports improvements over its retrieval baselines. citeturn19view3 | Fine-grained flow structure can matter for completion tasks. | That data/control-flow is cost-effective for general issue retrieval. |
| **RepoCoder** | Iterative retrieval-generation retrieves repository context and regenerates code, reporting improvements over in-file and vanilla retrieval approaches. citeturn6academia39 | Retrieval and generation can be iterated; semantic/context matching can help repository completion. | A structural-graph recommendation. |
| **Repoformer** | Learns when cross-file retrieval is likely to help rather than retrieving indiscriminately; its experiments report that unnecessary retrieval can be avoided without reducing performance. citeturn6academia38 | More context/retrieval is not automatically better; selection can eventually be learned. | That `devtools` presently has the evidence or dataset to train such a selector. |
| **SWE-agent** | Focuses on an Agent-Computer Interface that lets an LM navigate files, edit code, execute commands/tests, and observe results. citeturn16academia39 | Strong repository work need not begin with a structural graph. | That graph retrieval is required for capable software agents. |
| **Agentless** | Uses a deliberately simpler localization → repair → validation workflow and reported competitive SWE-bench results without a complex autonomous exploration architecture. citeturn17academia39 | Simpler retrieval/localization pipelines remain serious baselines. | That agentic/structural exploration cannot add value. |
| **RANGER** | Constructs a repository knowledge graph with hierarchical/cross-file information and textual descriptions/embeddings; entity queries use Cypher and natural-language queries use MCTS-guided graph exploration. It reports that BM25 + RANGER performs especially well on CrossCodeEval. citeturn19view0 | Graph, lexical, and embeddings can be complementary. | That this heavy stack is the minimal solution or appropriate next experiment for `devtools`. |
| **SWE-Explore** | 2026 benchmark isolates repository exploration over 848 issues, 203 repositories, and 10 languages, scoring coverage, ranking, and context efficiency; authors report agentic explorers above classical retrieval and strong relationship between exploration metrics and repair behavior. citeturn19view1 | Evaluating repository exploration separately from end-to-end repair is increasingly well motivated. | A specific structural algorithm recommendation. |

Aider is especially useful for correcting a common overstatement. Its documentation literally says that graph ranking operates on a graph where **source files are nodes and dependency relationships form edges**, and its Tree-sitter map obtains definitions and references to identify important identifiers. That is a graph, but it is a graph built for a specific repository-map/token-budget problem. Calling this “Aider uses a single repository graph” without qualification makes a storage/ranking implementation sound like a universal semantic model. citeturn21view0turn21view1

Sourcegraph provides a complementary lesson: Cody's public documentation names keyword search, Sourcegraph Search, and Code Graph separately. That architecture is much closer to your current evidence-family distinction than to a graph-monoculture interpretation. citeturn21view2

RepoGraph and LocAgent are the strongest direct evidence that structural relations can help software-engineering localization, but they differ substantially. RepoGraph uses a relatively small relation vocabulary and neighborhood extraction; LocAgent uses a larger heterogeneous schema, lexical indexes, type-aware graph traversal, and LLM planning. In LocAgent's own comparison, its graph is not sufficient by itself: the runtime begins by linking issue keywords to entities through exact/name/BM25 indexes and only then traverses structure. citeturn18view0turn19view2

LocAgent is also important for semantic retrieval. On its Loc-Bench table, the paper reports substantially higher localization accuracy for an E5 dense retriever than BM25 at several file/module/function cutoffs. That is one benchmark, not a universal result, but it is enough to reject an architecture process that insists structural retrieval must be exhausted before pretrained semantic retrieval receives a fair evaluation. citeturn18view0

SWE-agent and Agentless are equally important negative controls. SWE-agent demonstrates that carefully designed repository interaction tools can yield useful behavior without a precomputed graph, while Agentless demonstrates that a relatively simple staged localization workflow can compete with more elaborate agents. They warn against equating representational sophistication with retrieval effectiveness. citeturn16academia39turn17academia39

Finally, recent research increasingly evaluates **exploration/localization as its own capability**, rather than allowing repair success to hide retrieval failures. SWE-Explore's separation of coverage, ranking, and context efficiency is conceptually aligned with what Increment 25 should do: candidate recall should be measurable before final ranking or agent behavior. citeturn19view1

## Graph representation and structural algorithms

The most important representation decision is not “one graph or many graphs.” It is:

> **Which facts are canonical, and which representations are derived query/serving views?**

That distinction is well established in mature code-intelligence systems. Kythe explicitly separates its persistent analysis-data representation from “serving” representations and says indexes such as denormalized adjacency tables or graph triples may be extracted for different purposes. Joern, by contrast, intentionally provides one typed property-graph intermediate representation and overlays, yet even Joern's documentation notes that it replaced its earlier use of general-purpose graph databases with its own backend as limitations became apparent. citeturn14view2turn14view0

### Representation alternatives

| Architecture | Semantic strengths | Main risks | Incremental/scale implications | Recommendation |
|---|---|---|---|---|
| **One heterogeneous typed graph** | Easy cross-relation traversal; common query language; relation labels can preserve semantics | Encourages generic traversal over semantically incomparable edges; universal node identity/schema pressure; hub effects; graph abstraction may leak into domain model | One substrate can simplify some indexes but invalidation across derived relations can become coupled | **DEFER as physical option; reject as required semantic abstraction** |
| **Independently maintained typed graphs** | Very explicit semantics; difficult to accidentally mix relations | Duplicate node identity, repeated storage/indexes, inconsistent invalidation; composition awkward | Every graph becomes another materialized derivative to rebuild and synchronize | **REJECT as default physical design** |
| **Common canonical typed-relation substrate + projections** | Preserves types while allowing controlled composition | May drift toward generic Graph/Edge abstractions if overgeneralized | Good if common storage eventually has demonstrated operational value | **Plausible eventual implementation, but unnecessary to introduce now** |
| **Native relation/index structures + query-time projections** | Smallest architecture; each relation keeps its true domain semantics; graph-like traversals possible through adjacency indexes | Cross-family queries require an explicit projection/traversal operator | Fine-grained invalidation; no duplicated graph state; projections can be ephemeral | **ACCEPT NOW** |

The last option is strongest for `devtools`.

For example, a reference derivation need not yield:

```text
GraphEdge(source_node, target_node, type="reference")
```

It can yield a native fact closer to:

```text
ReferenceOccurrence
    source_occurrence
    referenced_subject
    resolution_state
    provenance
    applicable_snapshot
```

with an index from `referenced_subject → reference occurrences` and whatever reverse mapping is useful. A retrieval experiment can then traverse:

```text
seed resource
  → declarations contained by seed
  → incoming reference occurrences
  → owning resources
```

without turning those four objects into permanent universal `GraphNode` instances.

This also gives a clean answer to “typed graph views”: **retain the notion, weaken its architectural status.** A typed graph view is a useful *query interpretation* over Repository Intelligence, not necessarily a persisted domain object. Imports, references, calls, inheritance, and tests can each expose graph-shaped projections when needed.

That design is consistent with SCIP's protocol-level approach to semantic navigation and Kythe's canonical-facts-versus-serving-index distinction. citeturn14view1turn14view2

### Candidate-generation algorithms

The key algorithms differ greatly in the relevance assumptions they smuggle in.

| Method | Implied relevance hypothesis | Type/direction handling | Hub/fan-out behavior | Candidate generation vs ranking | Cost / maintenance | Verdict |
|---|---|---|---|---|---|---|
| **Typed one-hop expansion** | Directly related resources are sometimes useful | Native and explicit | Easily measured and bounded | Strong candidate generator | Query cost proportional to visited adjacency | **EXPERIMENT NEXT** |
| **Bounded typed BFS** | Relevance can propagate several relation steps | Good if each step is typed | Fan-out multiplies rapidly | Candidate generation | Local traversal but potentially explosive | **DEFER until one-hop earns it** |
| **Explicit meta-path traversal** | A particular relation sequence has stable semantic meaning | Excellent | Can be bounded by schema/path | Good candidate generator for a known purpose | Efficient with indexes for short paths | **DEFER, but promising** |
| **Unconstrained multi-hop expansion** | Any short path means relevance | Usually destroys semantic interpretability | Severe combinatorial/hub noise | Poor generator | Potentially large neighborhoods | **REJECT FOR NOW** |
| **Personalized PageRank / random walk** | Random-walk mass from seeds approximates relevance | Requires relation weighting or layer design for heterogeneous graphs | Degree normalization helps some hubs but can diffuse through them | Primarily ranking/prior; can generate by top scores | Iterative query/precomputation; harder incremental behavior | **DEFER** |
| **Global PageRank/centrality** | Globally important code is likely useful | Typically relation-specific weighting required | Often elevates widely referenced infrastructure | Better for repository-map/context salience than task retrieval | Usually global recomputation/approximation | **DEFER** |
| **Spreading activation** | Relevance attenuates over paths | Needs hand-selected edge weights/damping | High-degree spread is a major problem | Generation + ranking become entangled | Arbitrary hyperparameters | **REJECT FOR NEXT EXPERIMENT** |
| **Shortest-path distance** | Structurally close nodes are more relevant | Dangerous when heterogeneous edges are flattened | Hubs shorten paths artificially | Better as evidence describing already surfaced candidates | BFS-like for unweighted projections | **DEFER as evidence feature** |
| **Neighborhood overlap / structural similarity** | Similar neighborhoods imply analogous responsibility | Can remain relation-specific | High-degree sets need normalization | Useful for sibling/implementation analogies, not general retrieval | Set intersections/indexes | **DEFER / task-specific** |
| **Subgraph extraction** | Depends entirely on how seeds/subgraph boundaries are chosen | Excellent if typed | Boundary determines fan-out | A packaging/transport operation, not relevance algorithm | Straightforward once graph view exists | **Useful mechanism, not retrieval theory** |
| **Relation-support aggregation** | Multiple independent supports may be more informative than one | Excellent if supports remain separate | Does not inherently solve fan-out | Descriptive candidate evidence now; ranking later | Cheap after generation | **MEASURE NEXT, do not score yet** |
| **LLM/MCTS graph exploration** | Model reasoning can decide which structural branch matters | Potentially excellent | Agent can prune but at substantial inference cost | Agentic retrieval/ranking combined | Many model calls/state transitions | **DEFER** |
| **Learned graph ranker/GNN** | Training distribution teaches relevance propagation | Can encode typed relations | Can learn hub behavior, or overfit it | Learned candidate/ranking | Dataset/training/serving complexity | **REJECT FOR NOW** |

LocAgent's type-aware BFS is evidence that short typed traversal can be operationally useful; RANGER is evidence that much heavier graph exploration can work; neither makes the heavier method an appropriate starting point. citeturn18view0turn19view0

Aider's use of graph ranking is also better interpreted as **global context compression** than as proof of a general retrieval algorithm: it chooses repository-map content under a token budget and emphasizes highly referenced identifiers. That is a different objective from finding every resource that may satisfy an InformationNeed. citeturn21view0

The strongest minimal hypothesis is consequently not “PageRank will solve the import-expansion problem.” It is:

> **Some relation families have enough semantic specificity that one typed relation hop from a plausible seed has better marginal useful-resource yield than simply looking farther down the lexical ranking.**

That is measurable before choosing any graph-ranking algorithm.

## Relationship families and evidence complementarity

Not every relation deserves to become new Repository Intelligence simply because it might improve a retrieval benchmark. The strongest candidates are relations that have independent code-intelligence value.

### Relationship-family priorities

**Declaration-grounded references should be first.** Definition/reference indexes are foundational capabilities in conventional code intelligence—SCIP explicitly targets go-to-definition, find-references, and find-implementations—and they are also the basis of Aider's repository-map analysis. A reference relation can support navigation, impact analysis, diagnostics, agent understanding, and retrieval without retrieval being its reason for existence. citeturn14view1turn21view1

For Python, the relation should not pretend that every syntactic identifier use has an exact unique declaration. Preserve the distinction among exactly resolved, qualified/conditional, ambiguous, and unresolved references. Retrieval can later decide whether any of those states is useful evidence.

**Call relationships should preferably emerge as a semantic specialization of reference/call-site knowledge rather than as an immediately separate “call graph platform.”** A call-site occurrence whose target is declaration-grounded can support caller→callee and callee→caller views. LocAgent's use of invocation edges and GraphCoder's more fine-grained flow results both suggest behavioral relations can outperform mere file topology in appropriate tasks. citeturn18view0turn19view3

**Inheritance / implementation relations are also strongly justified independently of retrieval.** They support definition navigation, implementation search, change impact, type understanding, and refactoring. LocAgent includes inheritance as one of only four core relation types, while SCIP explicitly treats “find implementations” as a first-class code-intelligence operation. citeturn18view0turn14view1

**Test relationships are promising but should be decomposed rather than invented as one vague `TESTS` edge.** Useful repository facts include “this resource is classified as test code,” “this test declaration references this production declaration,” “this test target depends on this build target,” and, if executions are recorded, “this execution observed this test covering this occurrence.” The last is execution-derived knowledge with a different provenance/environment than static references. A 2026 Repository Intelligence Graph preprint reports benefits from deterministic build/test architectural maps, although its CMake/CTest focus and evaluation setup make it suggestive rather than decisive for general retrieval. citeturn7academia39

**Build/configuration/package relations deserve high long-term priority**, particularly for autonomous engineering agents. Bugs involving entry points, plugins, test discovery, packaging, generated code, workspace boundaries, or CI frequently cannot be understood from Python calls alone. The same 2026 RIG work is useful evidence that build/test structure can be actionable repository knowledge, while Kythe's architecture also explicitly incorporates build information into analysis. citeturn7academia39turn14view2

**History/change coupling is best treated as a distinct temporal evidence family, not smuggled into a snapshot “dependency graph.”** A 2025 repository-memory study augments code-localization agents using historical commits, linked issues, and summaries of actively evolving code and reports localization improvements on SWE-bench variants. That establishes history as a credible complementary signal; it does not turn co-change into a structural dependency fact. citeturn15academia42

**Control/data-flow should be deferred for general `devtools` retrieval.** GraphCoder's code-completion results show that these relations can be valuable when the task itself is tied to a local completion point and statement-level context. The derivation burden and task specificity make them a poor candidate for the next general-purpose structural experiment. citeturn19view3

### Complementarity across retrieval families

The most useful way to think about the evidence portfolio is by **failure modes**, not by which retriever seems most modern.

**Lexical retrieval** is strong when issue language, names, identifiers, error strings, filenames, or domain terms overlap the relevant resource. Your local evidence already demonstrates how strong that can be. Its main weakness is vocabulary mismatch and implicit dependency: a report can describe a symptom without naming the implementation responsible.

**Structural retrieval** can bridge an explicit seed to a lexically dissimilar neighbor when the relevant relation is represented. Its weakness is that relationships express repository structure, not task relevance. Utility functions, framework bases, registries, popular interfaces, and common configuration modules can have enormous structural neighborhoods while being irrelevant to a particular need.

**Semantic embeddings** can bridge natural-language/code and synonym/concept mismatch without requiring a structural path. Their weakness is that semantic similarity does not establish operational dependency; two implementations may look semantically alike but never participate in the same behavior. LocAgent's E5-vs-BM25 results demonstrate semantic gains on its localization benchmark, while repository-level dense/neural retrieval research reports further gains from learned semantic representations on repository search tasks. citeturn18view0turn15academia41

This yields a natural complementarity matrix:

| Pair | What the second signal can recover | Characteristic joint failure |
|---|---|---|
| **Lexical + structural** | unnamed dependencies, callers/callees, implementations, tests | lexical seed is wrong or structural relation absent/noisy |
| **Lexical + semantic** | vocabulary mismatch, paraphrases, conceptual matches | structurally necessary but textually/semantically dissimilar dependencies |
| **Structural + semantic** | semantic signal identifies entry point; structure follows behavior, or structure narrows semantic search | neither has an adequate seed / relationship representation |
| **Lexical + structural + semantic** | broadest orthogonality | candidate explosion and ranking become the dominant problem |

RANGER is a useful existence proof for the last combination: it enriches graph nodes with textual descriptions/embeddings and reports that pairing its retrieval with BM25 produces strong CrossCodeEval results. But RANGER's MCTS and rich graph are precisely why it should be read as evidence of **complementarity**, not copied as Increment 25. citeturn19view0

RepoCoder similarly supports iterative semantic/context retrieval, while Repoformer is a warning that retrieved context may be unhelpful enough that learning *whether to retrieve* becomes beneficial. Together they reinforce the principle that candidate volume must be measured rather than treated as free. citeturn6academia39turn6academia38

One particularly promising future composition is:

\[
\text{semantic or lexical seed}
\rightarrow
\text{typed structural expansion}
\]

rather than:

\[
\text{query}
\rightarrow
\text{universal graph traversal}.
\]

But even that should not be assumed. Increment 25 should measure whether lexical-seeded structure actually has unique yield. A later factorial experiment can replace lexical seeds with semantic seeds and determine whether structure is useful because of its relationship signal or merely because it gets better starting points.

## What the `devtools` evidence falsifies, and what Repository Intelligence should learn

### The failure of Increment 20–24

Taken literally, the supplied `devtools` evidence falsifies substantially less than “structural retrieval did not work,” but substantially more than “we merely need a slightly different import weight.”

It falsifies confidence in the tested **directional import reservation/admission mechanism** on the frozen surface:

- protecting lexical ranks 1–4 and conditionally replacing rank 5 did not improve known-useful coverage;
- it displaced a useful lexical rank-5 result;
- one of two relationship admissions was not useful;
- qualification did not discriminate usefully enough;
- imports produced only one unique useful recovery beyond lexical top-5;
- that recovery supplied no additional known-useful coverage beyond lexical top-15;
- a subsequent deterministic ranking formulation also failed to improve the baseline.

The critical methodological lesson is that the experiments entangled two independent questions:

\[
\text{Does structural evidence surface useful resources?}
\]

and

\[
\text{Should one of those resources displace lexical rank 5?}
\]

The second can fail while the first succeeds. Conversely, the first can produce one genuinely useful candidate while still being economically worthless because it generates fifty irrelevant neighbors. Candidate-generation recall and candidate-volume/yield therefore have to be observed directly.

The experiments also provide a strong control insight. On those six frozen InformationNeeds, **lexical widening from five to fifteen was more valuable than the tested relationship machinery**: top-15 contained all 18 known-useful resources in the frozen material. That is local evidence only, but it means that every future structural claim in `devtools` must answer:

> Why not simply inspect more lexical results?

Candidate-volume-matched lexical widening should consequently become the default structural-retrieval control.

What remains unresolved is large:

- whether references or calls have higher yield than imports;
- whether a lexically surfaced declaration has useful callers/callees outside lexical top-N;
- whether different relation families recover different misses;
- whether test/build/type relations are highly conditional on InformationNeed purpose;
- whether a wider lexical seed set produces better structural starts;
- whether multi-hop typed paths ever add enough recall to justify their fan-out;
- whether structural retrieval is primarily useful below lexical rank 15 on other repositories;
- whether semantic retrieval dominates both;
- and whether structural candidates become more valuable to an agent after Context disclosure selects precise declarations/regions rather than whole resources.

Nothing in Increment 20–24 resolves those questions.

### Repository Intelligence implications

The next RI addition with the best independent justification is **reference knowledge**.

Its canonical semantics should concern repository facts, not retrieval:

> A `SourceOccurrence` syntactically denotes, resolves to, may resolve to, or cannot be resolved to one or more `RepositorySubject`s under a stated derivation definition.

From that, call-site specialization can be derived where the syntactic role is invocation. Reverse reference lookup, caller/callee views, implementation lookup, and retrieval expansion become consumers.

That direction is strongly aligned with established code-intelligence representations such as SCIP and with Aider's definition/reference extraction. citeturn14view1turn21view1

Inheritance/implementation knowledge is the next obvious independent family. Test classification and build/configuration knowledge should follow where they are semantically well defined. Do **not** manufacture a generic `RELATED_TO` relation to give retrieval more edges.

History should be modeled separately. A co-change observation needs a derivation definition including history range, commit filtering, rename handling, generated-file policy, and support count. It says something like “A and B were jointly changed in N qualifying changes under history H,” not “A depends on B.” Recent repository-memory research makes history worth studying, but does not justify collapsing it with snapshot structure. citeturn15academia42

### Incremental maintenance and large repositories

The canonical-relation/query-projection design scales better conceptually than maintained graph copies.

Tree-sitter itself is designed for incremental parsing and can efficiently update syntax trees after edits, demonstrating that syntax-derived layers need not always be rebuilt globally. citeturn21view3 `devtools` already has stronger snapshot/content identities than many research prototypes, so the natural maintenance unit is the relation derivation dependency:

- unchanged content with unchanged derivation dependencies can reuse its derived facts;
- changed source invalidates locally derived references/declarations;
- changes that alter exported/resolution surfaces can invalidate dependent cross-file resolutions;
- query-time projections require no independent invalidation because they are reconstructed from applicable canonical facts.

That is preferable to maintaining N synchronized graph views with their own node/edge lifecycles.

High-degree hubs must become a first-class **measurement**, not a hidden score correction. A module imported by 2,000 files is truthful structural knowledge. Whether those 2,000 resources should be candidates is a retrieval problem. The RI layer should preserve the relation; the structural generator should report that its bounded expansion encountered a hub.

For monorepos, workspace/package/build-target boundaries are useful relation facts and possible traversal constraints, but they should not become absolute relevance boundaries. Cross-package changes are real. External dependencies should normally act as terminal identities during repository-context generation: retaining “A imports external package X” may be useful, but expanding from X into arbitrary external source repositories is a distinct multi-repository retrieval problem.

Multiple languages further favor typed native relations. SCIP's common protocol demonstrates that definition/reference concepts can be normalized across many language indexers, but it still relies on language-specific producers. citeturn14view1 `devtools` should similarly normalize semantics only when the semantics really align. A qualified Python invocation should not silently acquire the same authority as an exactly resolved relation in a language/toolchain with stronger static binding.

## Recommended Increment-25 experiment and retrieval sequencing

Increment 25 should answer one narrow question:

> **Given a lexical or directly resolved repository seed, do specific deterministic relation families surface useful resources that lexical widening would otherwise miss, at a candidate-volume cost low enough to justify keeping structural generation in the retrieval portfolio?**

It should **not** answer “which five resources should enter Context?”

### Experimental hypotheses

The primary hypotheses should be:

**Reference hypothesis.** Declaration-grounded one-hop reference expansion has higher marginal useful-resource yield than qualified imports and candidate-volume-matched lexical widening.

**Call-specificity hypothesis.** References originating in call position provide higher yield/lower fan-out than generic references.

**Complementarity hypothesis.** Import, generic-reference, and call-reference families recover meaningfully different useful resources; their union adds useful coverage rather than just duplicates.

**Support hypothesis.** Resources surfaced through more than one independently meaningful relation family are descriptively more often useful. Measure this; do **not** turn it into a score yet.

**Seed-width hypothesis.** Structural yield changes materially between lexical top-5 and top-15 seeds. This directly tests whether the prior import results were partly an artifact of too-narrow starting points.

Do not put multi-hop traversal in the primary hypotheses. A single semantic relationship hop is enough to test whether the relation family contains useful retrieval signal at all.

### Evidence families and generator mechanics

Use three structural families:

| Arm | Source knowledge | Traversal |
|---|---|---|
| **Import** | existing qualified Python import relations | incoming and outgoing independently |
| **Reference** | new declaration-grounded reference knowledge | declaration ↔ referring occurrence/resource |
| **Call-position reference** | reference occurrence syntactically acting as a call target | caller→callee and callee→caller independently |

Containment participates only in identity/granularity translation:

```text
lexical resource seed
    ↓ contained declarations
reference/call relation
    ↓ opposite subject/occurrence
owning resource candidate
```

Do not count containment itself as a relevance hop.

For every surfaced resource, retain native provenance such as:

```text
seed resource
seed lexical rank
seed declaration
relation family
relation direction
source occurrence
target subject
resolution/qualification state
result resource
```

This is experimental trace data. It does not require a generic production `CandidateEvidence` abstraction.

Candidate output should initially be at `ResourceOccurrence`/resource level because that makes direct comparison to the existing lexical evaluation straightforward. Preserve the subject/occurrence path so later Context disclosure can decide whether to expose a declaration, reference region, signature, body, or whole resource.

### Seed conditions

Run at least these independent seed conditions:

\[
N = 5,\quad N = 15
\]

using the existing lexical ranking.

An InformationNeed containing an exactly identifiable declaration/resource should remain in the **direct-resolution stratum**, not be forced through lexical discovery. Structural expansion from a directly resolved resource may be evaluated separately, but the direct resource itself is not evidence that heterogeneous retrieval succeeded.

Do not use ground-truth changed files to manufacture seeds.

### Traversal bounds

For the primary experiment:

- exactly **one semantic relationship hop**;
- relation family and direction are never collapsed;
- repository-local targets only;
- no recursive expansion from newly generated candidates;
- external dependency identities are terminal;
- self-resource results are removed from “new resource” counts but provenance may be retained;
- duplicate resource results are deduplicated for volume while retaining every supporting path.

Avoid “take the best 20 graph neighbors,” because that quietly introduces a graph ranking algorithm.

Instead, treat excessive fan-out as a result. Define a pre-registered operational overflow threshold for the implementation—based on acceptable experiment resource consumption, not a relevance claim—and when an expansion exceeds it, mark that seed/family/direction as **overflowing** rather than silently selecting a privileged subset. Report the raw degree/count even if candidate material is not subsequently loaded.

This turns hub behavior into evidence about whether a relation is practical.

### Baselines

The decisive baseline is not merely BM25 top-5.

For a structural generator that adds \(m\) distinct resources to lexical top-\(N\), compare it with:

\[
\text{lexical top-(}N+m\text{)}.
\]

That is the candidate-volume-matched lexical control.

Also retain:

- lexical top-5;
- lexical top-15;
- import one-hop alone, reproducing the family implicated in prior work without K=5 admission;
- a deterministic count-matched random-resource control;
- a simple path/topology control, such as nearby same-package resources, where it can be defined without content-derived ranking.

The random and topology controls answer different questions: “does *any* expansion help because there are more candidates?” and “is typed structure better than cheap repository locality?”

### Metrics

Candidate generation should report at least:

\[
\text{candidate recall}
=
\frac{\text{known-useful resources surfaced}}
     {\text{known-useful resources}}
\]

plus **unique structural recovery**:

\[
U_{\text{struct},N}
=
\left|
\text{Useful}
\cap
(C_{\text{struct}} \setminus C_{\text{lexical},N})
\right|.
\]

The most important efficiency measure is **marginal useful yield**:

\[
Y
=
\frac{\text{unique useful resources added}}
     {\text{unique new resources generated}}.
\]

Also record candidate volume, per-seed and per-relation fan-out distributions, maximum degree, overflow frequency, relation-family overlap, direction-specific yield, qualification-specific yield, number of distinct supporting paths, and purpose-stratified usefulness.

Do **not** report a single weighted “retrieval score” combining those dimensions.

For ranking, optionally compute only retrospective oracle questions such as “if a later ranker could perfectly choose among the generated surface, what useful resources were available?” Do not design a new ranker inside Increment 25.

### Purpose-relative labels

Structural facts should be generated without declaring them relevant.

Each candidate is then judged against the frozen InformationNeed. That usefulness annotation should ideally be blind to whether the resource came from lexical, import, call, or random control until the usefulness decision has been recorded.

Stratify the resulting data by frozen purpose categories—bug diagnosis, implementation change, testing, interface understanding, build/configuration, and similar classes—but do not initially allow purpose to turn relation families on/off. Otherwise a failed purpose-routing policy can once again obscure whether the structural family itself had useful evidence.

### Leakage protections

The experiment should freeze, before evaluation:

- repository snapshot;
- InformationNeed;
- lexical query construction;
- known-useful annotations or annotation procedure;
- relation derivation definition;
- relation-resolution qualification;
- seed widths;
- traversal depth;
- operational fan-out limits;
- semantic model, if the semantic comparator is included.

Relationship derivation must never consume the solution patch, known-useful set, or post-snapshot changes.

If tasks are sourced from historical issues, the structural snapshot must correspond to the pre-fix state. Change/history retrieval should be excluded from this experiment unless it has its own leakage-safe cutoff.

Ground-truth patch files should not be treated as a complete definition of usefulness. They identify changed locations, not every piece of context a developer or agent legitimately needed. SWE-Explore's use of successfully solving agents' consulted code regions is an interesting complementary labeling source, but such trajectories are still observations of particular successful paths rather than exhaustive relevance judgments. citeturn19view1

### Falsification criteria

The structural hypothesis should be considered **falsified for the tested relation families**, rather than rescued with another ranking trick, if on held-out repositories:

- reference/call expansion provides no consistent unique useful recovery over candidate-volume-matched lexical widening;
- useful yield is indistinguishable from simple topology/random expansion;
- gains occur only on `devtools` or on purposes used to design the generator;
- useful gains require fan-out large enough that structural consideration is operationally unattractive;
- qualification/direction/path evidence does not identify any reproducible high-yield subfamily;
- or the union of typed families mostly duplicates lexical results without useful marginal coverage.

If that happens, the correct conclusion is **not** “try PageRank.” It is “these deterministic structural candidate-generation hypotheses have weak marginal value; prioritize semantic retrieval/history or agent-driven exploration instead.”

If one-hop references clearly add useful candidates at modest volume, the next structural experiment—not Increment 25 itself—can test **specific pre-registered two-step meta-paths**. It should not test arbitrary depth-2 traversal.

### Cross-repository strategy

The frozen `devtools` needs should remain in Increment 25 as a regression/control set because they embody the negative import evidence.

They cannot adjudicate the main hypothesis alone, because lexical top-15 already reaches all 18 known-useful resources on that frozen surface. Any experiment whose only evaluation set has a lexical-recall ceiling of 100% at rank 15 is structurally biased toward demonstrating duplication rather than unique recall.

The next dataset should therefore be constructed **independently of retrieval performance**. Do not go looking for issues where BM25 happens to fail and then call structural retrieval successful.

A strong bounded strategy is:

1. freeze the hypotheses on `devtools`;
2. add independently selected Python repositories spanning materially different size, package topology, test organization, and architectural style;
3. use one subset only for derivation/debugging;
4. freeze all traversal parameters;
5. evaluate on repositories that were not inspected while designing the generator;
6. later repeat with additional languages only after their relation semantics/derivers are independently trustworthy.

Cross-repository splitting matters more than merely increasing the number of tasks from one repository. Repository-specific naming conventions, package structure, central utility modules, and test organization can make a relation heuristic look far more stable than it is.

SWE-Explore's scale—203 repositories and ten languages—and LocAgent's attempt to create a fresh localization benchmark both reflect the broader recognition that repository exploration should be evaluated over diverse, temporally controlled tasks rather than a single codebase. citeturn19view1turn18view0 Increment 25 need not approach that scale, but its conclusion should remain explicitly provisional until held-out repositories confirm it.

### Semantic-retrieval sequencing

Pretrained semantic retrieval should be **concurrent in research, separate in interpretation, and later in production integration**.

That means the structural implementation need not depend on embeddings, but the same frozen evaluation should preferably have an offline semantic arm. This prevents a classic architectural error: spending several increments optimizing a weaker structural family before testing a readily available orthogonal baseline.

No model training is required.

The first semantic experiment should probably compare at least two representation levels:

- resource/chunk representations for natural-language-to-code discovery;
- declaration/subject representations combining identity/signature/documentation/body information where appropriate.

Do not begin by embedding every DerivedKnowledge record or serializing the entire relation store into vectors. A relation such as `A imports B` already has a better native representation.

LocAgent's entity-level indexing and repository-completion work such as RepoCoder suggest that function/declaration-level representations can matter, while its dense-retrieval baseline shows that pretrained representation retrieval can outperform BM25 on some localization tasks. citeturn18view0turn6academia39

No vector database is architecturally required to run this experiment. For bounded research sets, embeddings can be precomputed and searched with a simple exact nearest-neighbor implementation or disposable evaluation index. A production ANN/vector-store decision should follow demonstrated scale and retrieval value, not precede them.

Only after independent lexical, structural, and semantic arms are measured should you test:

\[
\text{lexical seeds}
\rightarrow
\text{structure}
\]

versus

\[
\text{semantic seeds}
\rightarrow
\text{structure}
\]

versus unions of their independently surfaced candidates.

### Learned-ranking boundary

There is currently no evidence in the supplied `devtools` experiments that justifies model training.

A learned ranker becomes justified only when all of the following are true:

**First**, deterministic candidate generators produce a recurring ranking problem: useful and useless candidates coexist at volumes large enough that capacity selection matters.

**Second**, you possess purpose-relative labels across multiple repositories, relation families, directions, lexical/semantic signals, and negative candidates.

**Third**, simple transparent policies—lexical rank, relation family/direction, exactness, evidence multiplicity, seed rank, hub degree, semantic similarity—have been evaluated and leave meaningful headroom.

**Fourth**, evaluation can be split by repository and preferably by time so that the model cannot merely memorize project-specific patterns.

**Fifth**, there is enough repeated evidence to evaluate generalization of the ranker rather than simply its fit to one repository. There is no defensible universal sample-count threshold; the key requirement is sufficient independent positive and negative variation to estimate held-out repository performance.

Repoformer demonstrates that learned selective retrieval can be valuable when sufficient training data exists, and repository-level neural-search research reports large gains from learned reranking based on repository histories. Those are reasons to preserve learned ranking as a future option, not reasons to create training infrastructure before the deterministic evidence portfolio is understood. citeturn6academia38turn15academia41

## Architecture decisions, ADR implications, and preserved alternatives

### Architecture decisions

| Classification | Recommendation | Rationale |
|---|---|---|
| **ACCEPT NOW** | Preserve `repository truth != retrieval evidence != purpose usefulness != ranking/capacity != Context disclosure` | Every successful external system examined still requires some equivalent separation; no evidence justifies collapsing them. |
| **ACCEPT NOW** | Preserve relation-native semantics, direction, qualification, provenance, snapshot/dependency state | Required both for truthful RI and interpretable retrieval. |
| **ACCEPT NOW** | Treat exact/direct declaration or resource resolution separately from heterogeneous discovery | RANGER itself distinguishes entity queries from natural-language exploration, reinforcing this separation. citeturn19view0 |
| **ACCEPT NOW** | Make canonical typed relations plus traversal indexes the default representation | Smallest architecture that enables structural experiments without graph-domain commitment; consistent with SCIP/Kythe-style fact/index separation. citeturn14view1turn14view2 |
| **ACCEPT NOW** | Treat typed graph views as ephemeral semantic/query projections, not necessarily persisted objects | Preserves their useful semantics without maintaining redundant graph state. |
| **ACCEPT NOW** | Measure candidate generation before ranking | Supported both by the `devtools` failure analysis and by recent exploration-focused evaluation such as SWE-Explore. citeturn19view1 |
| **EXPERIMENT NEXT** | Declaration-grounded reference RI | Independently valuable code intelligence and strongest next structural relation. |
| **EXPERIMENT NEXT** | Call-position reference subset | Tests whether stronger behavioral specificity improves yield. |
| **EXPERIMENT NEXT** | One-hop incoming/outgoing reference/call candidate generation | Smallest meaningful expansion hypothesis. |
| **EXPERIMENT NEXT** | Import/reference/call arms independently and unioned | Directly tests relationship-family complementarity. |
| **EXPERIMENT NEXT** | Top-5 vs top-15 seed widths | Separates structural weakness from seed-width weakness. |
| **EXPERIMENT NEXT** | Candidate-volume-matched lexical widening | Essential control after current empirical evidence. |
| **EXPERIMENT NEXT** | Offline pretrained-semantic baseline on the same frozen tasks | Prevents structural confirmation bias without production commitment. |
| **EXPERIMENT NEXT** | Cross-repository held-out validation | Necessary before architectural generalization. |
| **DEFER** | Purpose-based relation routing | First learn which relation families have useful conditional distributions. |
| **DEFER** | Explicit two-hop/meta-path generators | Only justified if one-hop structural signal is real. |
| **DEFER** | Personalized PageRank/random walks/centrality | They primarily add ranking assumptions before direct relation yield is established. |
| **DEFER** | History/change candidate generation | Promising, but semantically temporal and deserves an independent experiment. |
| **DEFER** | Test/build/config expansion | Important RI families, but avoid expanding Increment 25 too far. |
| **DEFER** | Data-/control-flow RI for general retrieval | Strong task-specific evidence from GraphCoder, insufficient cost/value case for general repository retrieval. citeturn19view3 |
| **DEFER** | Common physical relation substrate / graph database | Consider only after query and maintenance workloads demand it. |
| **DEFER** | Production embedding/vector infrastructure | First demonstrate semantic candidate value. |
| **DEFER** | Learned ranking | Requires cross-repository labeled candidate data and demonstrated deterministic ranking limits. |
| **REJECT FOR NOW** | Universal `Graph` as a core domain requirement | Graph shape is a view/representation choice, not a demonstrated repository semantic primitive. |
| **REJECT FOR NOW** | Generic `GraphNode` / `GraphEdge` as replacements for native domain facts | Would erase or weaken domain semantics to satisfy an unproven representation choice. |
| **REJECT FOR NOW** | Independently maintained graph copy for every relationship family | Creates redundant identity/invalidation complexity without demonstrated benefit. |
| **REJECT FOR NOW** | Untyped or indiscriminate relationship expansion | Existing import evidence already demonstrates truth ≠ relevance; heterogeneous paths make this worse. |
| **REJECT FOR NOW** | Universal normalized relevance score | Different evidence families do not yet have empirically calibrated comparable scales. |
| **REJECT FOR NOW** | Another protected-top-4 / replace-rank-5 structural policy | The supplied evidence directly undermines that line of experimentation. |
| **REJECT FOR NOW** | GNN / learned graph retriever | No training-data or baseline justification. |
| **REJECT FOR NOW** | Mathematical graph-complement machinery | It addresses a different notion of complementarity. |

### ADR implications

Because the actual text of ADR-0002, ADR-0003, and ADR-0004 was not supplied, the following are **implication-level amendments**, not claims about their current wording.

**ADR-0002 should be amended if it governs Repository Intelligence semantics.** It should state that deterministic repository relations retain their native subject/occurrence/resource domains, direction, qualification, provenance, applicability, derivation definition, and snapshot/dependency semantics. It should explicitly avoid making a universal graph data model normative. Graph-shaped projections may be derived from those facts without changing their authority or semantics.

It should also clarify that references, calls, inheritance/implementation, test relationships, build relationships, and temporal coupling may each be legitimate DerivedKnowledge **only when independently meaningful as repository knowledge**. Retrieval demand alone is not sufficient justification.

**ADR-0003 should be amended if it governs retrieval.** The important addition is an explicit conceptual distinction between:

\[
\text{evidence surfacing/candidate generation}
\]

and

\[
\text{ranking/capacity}.
\]

It should permit structural evidence generators to operate over RI while forbidding the implication that a repository relationship is itself relevant. Exact/direct resolution should remain distinct. Structural generator output should preserve relation/path provenance rather than immediately normalize heterogeneous evidence into one score.

ADR-0003 should also make **candidate-volume-matched lexical widening** a required baseline for structural experiments, given the local Increment 20–24 evidence.

**ADR-0004 should receive little or no semantic change if it primarily governs Context disclosure.** Structural candidate generation should not dictate disclosure granularity. A resource surfaced by a call relation might ultimately contribute only a declaration signature, a small implementation region, derived knowledge, or nothing after capacity decisions. The most useful amendment would be to require that downstream disclosure remain able to trace selected material to the evidence/subject that motivated it.

**A new ADR is justified only after Increment 25 if structural generation survives falsification.** Its subject should not be “the repository graph.” A better scope would be:

> **Structural retrieval projections over deterministic Repository Intelligence**

Such an ADR could specify the stable contract between relation knowledge and retrieval: permitted seed domains, relation-family selection, direction, bounded path semantics, provenance, candidate target domain, and handling of fan-out. Physical graph storage should remain a replaceable implementation choice.

If Increment 25 fails, no new graph ADR is warranted.

### Research findings that should be preserved even if not adopted

Several negative or deferred findings are important enough to retain as research record.

**A unified heterogeneous graph is not inherently semantically lossy.** Joern demonstrates that typed nodes, labeled directed edges, multiple edge types, and overlays can coexist in one graph. Therefore the argument against a universal graph in `devtools` should be “it is not yet necessary and risks premature generalization,” not “one graph cannot preserve types.” citeturn14view0

**Graph storage and graph semantics are orthogonal.** Kythe explicitly separates persistent facts from optimized serving forms, while Joern demonstrates the alternative of a graph-native IR. Both are viable design points. citeturn14view0turn14view2

**Separate graph views are also not automatically superior.** They make semantics obvious but can duplicate identity/index/invalidation machinery. The recommendation for typed views is semantic, not a requirement to materialize independent graph instances.

**Aider is evidence for graph-ranked repository context, not proof of universal graph retrieval.** Its documented file graph serves repo-map compression and reference importance. citeturn21view0turn21view1

**Cursor should not be used as architectural evidence without better primary documentation.** The widespread assertion that Cursor maintains or retrieves from “one repository graph” could not be verified to the standard required here.

**Sourcegraph is evidence for heterogeneous context acquisition.** Its public Cody architecture explicitly lists keyword search, Sourcegraph Search, and Code Graph as complementary context sources. citeturn21view2

**RepoGraph is positive evidence for bounded graph neighborhoods, but relation vocabulary and task matter.** Its result does not rehabilitate arbitrary one-hop import expansion. citeturn19view2

**LocAgent is stronger evidence for controlled typed traversal than for a universal graph.** Its agent explicitly chooses relation types, entity types, directions, and hops, and its system also relies on exact/name/BM25 indexes. citeturn18view0

**GraphCoder preserves the possibility that fine-grained control/data-flow structure may be highly valuable for code-completion or security-style tasks.** Deferring it for `devtools` general retrieval is a sequencing judgment, not evidence that the relation family lacks value. citeturn19view3

**Multi-hop structural retrieval remains unresolved.** One-hop import failure does not falsify multi-hop typed paths. But generic multi-hop expansion is too unconstrained to be the next experiment. A later meta-path experiment should be based on demonstrated relation-specific yield.

**Personalized PageRank remains a plausible future ranking mechanism.** It is not rejected theoretically; it is deferred because using it now would combine relevance propagation, degree normalization, relation weighting, and candidate ranking before direct structural evidence has been shown to add useful candidates.

**History is a credible future evidence family.** Recent repository-memory research reports localization gains from commit/issue history, but temporal coupling should retain temporal semantics rather than become a pseudo-dependency edge. citeturn15academia42

**Semantic retrieval has enough external evidence that it must remain a first-class competing hypothesis.** Dense retrieval outperforms BM25 on portions of LocAgent's localization evaluation, RepoCoder demonstrates retrieval-generation gains, and RANGER's best-performing combinations include both graph and non-graph evidence. Structural research should therefore compete against semantic retrieval rather than precede it indefinitely. citeturn18view0turn6academia39turn19view0

**Learned retrieval/ranking is a legitimate future capability but currently premature.** Repoformer and neural repository-search work demonstrate that learned selection/reranking can provide value, yet `devtools` presently has much more to learn from deterministic evidence generation before it has a defensible cross-repository training target. citeturn6academia38turn15academia41

Most importantly, the existing negative import result should be preserved without either minimizing or overgeneralizing it:

> **Imports are valid Repository Intelligence. The tested import-based top-5 admission mechanisms were not useful on the independently validated frozen `devtools` surface. Lexical widening was the stronger retrieval action there. Whether other typed structural relations generate genuinely complementary candidates remains an open empirical question.**

That is the right foundation for Increment 25

## Disposition

**Status: reconciled research evidence.** This investigation informs
[ADR-0002](../architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
for typed relationship semantics, reference-knowledge pressure, and the
semantic-versus-physical graph distinction, and
[ADR-0003](../architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md)
for structural candidate generation, lexical-widening controls, heterogeneous
evidence families, external validity, and later shadow progression. It does not
itself authorize implementation.

Accepted now are the separation of native typed relationship knowledge from
physical graph representation; bounded, directed, one-hop structural
candidate-generation as the next offline hypothesis; candidate-generation
evaluation separately from ranking/capacity; and a scientifically defensible
lexical-widening control. Declaration-grounded reference knowledge is a
promising next Repository Intelligence hypothesis, not a selected final model.

Deferred or rejected for now are a universal repository graph, graph database,
generic graph API, independently maintained graph per relationship family,
recursive or undirected expansion, PageRank/centrality, universal normalized
relevance, production embeddings/vector infrastructure, learned ranking, and
shadow execution of directional-reservation-v1. Pretrained semantic retrieval
remains a distinct competing evidence-family hypothesis rather than learned-
ranking training.

Revisit physical graph/storage choices only when concrete consumers and
measured query/maintenance workloads justify them; richer paths only after
one-hop relation-specific value; learned decisions only with diverse
repository-separated labels and credible targets; and production or shadow
progression only after offline and independent-repository validation.
