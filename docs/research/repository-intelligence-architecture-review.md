# Repository Intelligence Architecture: Comparative Evidence and Design Boundaries

## Disposition

Status: Partially reconciled

Canonical research subject: Comparative repository intelligence architecture and design boundaries.

Related ADRs: ADR-0002; ADR-0003; ADR-0004.

Implemented evidence: snapshots, bounded corpus/indexing, lexical retrieval, and evaluation.

Accepted: distinct repository intelligence, retrieval/ranking, and Context disclosure layers.

Deferred: semantic retrieval, graph algorithms, progressive disclosure, and derivation-aware incremental maintenance.

Rejected for now: universal graph, one mandatory retrieval mechanism, and repository text as authority.

Superseded or refined findings: ADRs and later experiments supply the current bounded decisions.

Open questions: empirical benefit and cost of each future intelligence family.

Revisit triggers: one independently useful bounded slice with deterministic evidence.

Reconciliation basis: ADR-0002 through ADR-0004; B-0002.

## A. Executive Conclusion

The evidence favors a **hybrid, multi-layered architecture** for repository intelligence. Such a system treats the repository as an immutable **content-addressed snapshot** (using Git commits or Merkle roots as identifiers), maintains *incrementally-updated indexes* of code structure (ASTs, symbols, dependencies, graphs, etc.), and offers **multiple retrieval pathways** (lexical, structural, semantic) whose results are merged by a ranking stage.  Retrieved fragments are then **compiled into context** according to budget and task needs, with full provenance metadata attached.  This design contrasts with a simpler search-only agent: it unifies content-addressable indexing (as in Cursor and Claude Context), deterministic static analysis (as in Aider), and graph-based reasoning (as in LocAgent and RepoGraph), without relying on one single retrieval mechanism.

Key findings include: (1) **Immutable snapshots and hashing:** systems like Cursor explicitly use a Merkle tree over files to detect changes and identify snapshot roots, enabling reuse of unchanged content. (2) **Incremental indexing:** content-addressed caches (e.g. embeddings keyed by chunk hash) allow recomputing indexes only for modified files. (3) **Deterministic structure:** coding agents like Aider build a “repo map” of definitions via AST parsing, while research systems (LocAgent, RepoGraph) build rich graphs of symbols and references. (4) **Multi-pronged retrieval:** strong systems use both exact and approximate methods – e.g. BM25 and embeddings, graph traversal, and LLM-enabled search – rather than a single mechanism. (5) **Relevance signals and ranking:** multiple signals (exact matches, imports, graph proximity) should be preserved as evidence before final scoring. (6) **Context building:** retrieving relevant fragments is distinct from assembling them into the prompt. The architecture should **separate ranking from selection**, and treat context-compilation as its own module (handling truncation, deduplication, ordering, etc.). (7) **Provenance:** every piece of context must carry back-links to its source (file, lines, commit, derivation) so that answers are reproducible and debuggable. (8) **Security:** repository content must always be treated as *data*, never as executable instructions; code comments or tests should not override agent policies. (9) **Progressive disclosure:** an agent should start with a concise summary (e.g. Aider’s map) and iteratively request more code or graph walks, rather than dumping entire files upfront.

Together, these findings support a **“D”-style hybrid repository-intelligence architecture:** maintain a content-addressed snapshot with Merkle hashing, derive and incrementally update multiple indexes (ASTs, symbol tables, file dependency graphs, embeddings), retrieve candidates through *independent* lexical/semantic/graph queries, *rank* them with multi-signal evidence, and finally compile context under a token budget while preserving provenance. This approach balances **efficiency, correctness, and explainability**. In particular, it appears essential for aiding smaller local models: well-structured deterministic context (symbols, definitions, dependency graphs) can compensate for limited model size. Where current systems like Cursor or Aider omit features (e.g. provenance tracking or multi-signal ranking), a new framework should fill those gaps.

# B. Comparative System Matrix

Below is a summary of major systems, highlighting their repository-state model, indexing strategy, static analysis, retrieval methods, context tactics, and other qualities. Unknown aspects are marked “(?)”. All facts are drawn from documentation, papers, or empirical evidence; clear source types are indicated.

- **Cursor (commercial AI IDE)**:
  - *Repository state:* Maintains an *explicit Merkle-tree snapshot* of the repo. Files are SHA-256 hashed (via a Merkle hierarchy) to detect changes. In Git contexts it records commit hashes and parent links. Unchanged files preserve the same hash across syncs. Working-tree changes are picked up via periodic “handshake” of Merkle root.
  - *Incremental:* Yes. Only changed files (determined via Merkle root diff) are re-indexed. Embeddings are cached by chunk hash, enabling reuse. Invalidation is file-level (checksum mismatch → re-chunk).
  - *Deterministic intelligence:* Primarily AST-based chunking (supports many langs). Likely builds symbol indexes (implied by “Ask questions about codebase” on UI), though not publicly documented.
  - *Graph usage:* No explicit repo graph; it relies on vector search and Git history. Path obfuscation ensures privacy, not graph semantics.
  - *Retrieval:* Semantic (vector) search: query embedding → nearest-code chunks (from cached embeddings in Turbopuffer DB). Also likely supports textual search (?), but focus is on embeddings.
  - *Context compilation:* Returns exact file/line ranges from local files, then reads those lines into prompt. Puts file path obfuscated to LLM. Does not appear to supply summaries or graphs, just raw code snippets.
  - *Progressive retrieval:* Cursor’s CLI uses tools; it will fetch specific files or regions on LLM request. It likely treats the context compiler separately. (Exact process not public.)
  - *Provenance:* Partial. Results include (obfuscated) file paths and line spans, but after deobfuscation one knows exact source lines. Embeddings are content-addressed, so identity is preserved.
  - *Strengths/limits:* **Strength:** Fast incremental indexing via Merkle; content-address cache yields speed (good for large repos). High-quality semantic retrieval. **Limitation:** Likely little explicit semantic or graph structure; context is raw code. Propagation of relevance signals is opaque (only similarity score). Depends on cloud service (privacy tradeoffs).

- **Aider (open-source CLI/IDE agent)**:
  - *Repository state:* Tied to Git: it uses the working directory and Git root. No explicit snapshot beyond current state; likely reads HEAD. Changes not tracked via content hashes (map is recomputed each run).
  - *Incremental:* Not clearly documented; likely whole-map rebuild on demand. Possible caching if not re-running. No published content-hash invalidation.
  - *Deterministic intelligence:* Builds a **repo map** of *file/module inventory* using Tree-sitter. It extracts all classes, functions, types, their signatures and some bodies, and references. It identifies *important identifiers* by counting references from the AST.
  - *Graph usage:* Yes – uses a file-dependency graph to prune the map. Specifically, it creates a graph with nodes = files and edges = dependencies (imports). Then applies a PageRank-like ranking to select the subset of symbols to include in the map. (No graph database; done in-memory via AST.)
  - *Retrieval:* Mainly **symbol/structural**: the map and graph let the LLM pick files. It also uses lexical search implicitly via **tree-sitter references** (counting references). Does not mention embeddings or BM25. The agent supports developer-guided grep or file prompts.
  - *Context compilation:* Sends the repo map (classes, functions, signatures) in every prompt, so the LLM initially sees key definitions. Then if the LLM *requests* files (it “asks to see these specific files”), Aider will insert those full files or excerpts. No fancy selection beyond “most important symbols first”.
  - *Progressive retrieval:* Yes – the LLM can “add files to chat” interactively. Aider’s process is like: send map → LLM chooses files → Aider adds them. The map is dynamically sized (1k tokens default) and can grow if needed. Aider handles this above the core LLM.
  - *Provenance:* Weak. The map entries show file and code lines, so the LLM knows origins. But after insertion of code, provenance per line is just the file context (no explicit tracking of analysis steps).
  - *Strengths/limits:* **Strength:** Systematic structural analysis for large codebases; produces concise summaries (map) that help disambiguate symbols. Good multi-language support via Tree-sitter. **Limitation:** Index is not explicitly incremental or content-addressed (whole repo scanned each time). No automated relevance ranking beyond AST reference counts; context assembly is “all relevant definitions up front,” which may be wasteful.

- **Claude Code (Anthropic’s agent)**:
  - *Repository state:* Operates on local files; no published details of snapshotting. Likely works on working tree in real time. Git integration exists (CLAUDE.md).
  - *Incremental:* Likely none at indexing level; it may use Tools with cached search, but no static index announced. The “auto memory” is for user corrections, not code analysis.
  - *Deterministic intelligence:* It encourages users to give context via `CLAUDE.md` files and memory, but doesn’t auto-extract code structure. The system itself does not seem to build file maps.
  - *Graph usage:* Not public. No known repository graph in Claude Code.
  - *Retrieval:* Claude Code’s approach is *tool-based RAG*: it uses built-in search tools (e.g. “/search” or code tools) to retrieve files. It may integrate semantic search plugins (e.g. “claude-context”/Zilliz plugin) for whole-repo search. Primarily, it fetches via keyword or embedding queries through MCP.
  - *Context compilation:* All context is inserted by the client; Claude sends the prompt as [prefix][user question][“context” retrieved by tools]. The context can include full file contents and text from `CLAUDE.md`. It truncates as needed but no published algorithm for selection.
  - *Progressive retrieval:* Yes – Claude Code’s agent loop can call “Search code”, “Open file” etc. via tools, on user or system cue. The context grows as the conversation goes on. The orchestration (tools vs deterministic compiler) is part of the MCP system. The core context compiler just sees everything provided.
  - *Provenance:* Partial. Retrieved snippets include file paths and line ranges if using tools, so the agent knows origin (especially with `RetrieveEntity`). But no formal lineage in the model context.
  - *Strengths/limits:* **Strength:** Integrates large-model conversation with developer-specified memory (CLAUDE.md) and Git tools. **Limitation:** Lacks baked-in repository analysis; relies on external search tools. Fine-grained provenance and deterministic indexing are not part of the core.

- **OpenAI Codex CLI (open-source)**:
  - *Repository state:* Uses the live directory. No built-in snapshotting; the CLI listens to commands and reads files on demand. No Merkle tree or commit-awareness documented.
  - *Incremental:* None; each command queries fresh. No persistent index.
  - *Deterministic intelligence:* None beyond what the LLM has seen. It does not appear to build any AST or symbol table. It may use a simple tool (“read file”, “grep”) to fetch context.
  - *Graph usage:* No published graph component.
  - *Retrieval:* Very simple: the CLI can search text, or use “/code search” tools powered by vector DB (if configured). The default may rely on simple text search (like grep) or an MCP plugin (like Claude Context) if installed. It supports any MCP server (like zilliz/claude-context) for searching the repo.
  - *Context compilation:* The CLI puts any retrieved code snippets (or entire files) into the prompt for each user query. It preserves order or truncates as needed.
  - *Progressive retrieval:* The user-driven prompt can chain multiple requests. The CLI itself doesn’t do multi-round retrieval automatically, but supports tools the LLM may invoke.
  - *Provenance:* Minimal – commands show file names, but once text is in prompt, no further tracking.
  - *Strengths/limits:* **Strength:** Flexibility as open-source; no shadow indexing (so full control). **Limitation:** Lacks any smart indexing. Entirely relies on LLM with some I/O tools.

- **Sourcegraph / Cody (Proprietary)**:
  - *Repository state:* Connects to code hosts; can index any Git repo or monorepo. Uses GitHub/Webhook integration to update indexes in near real time (implied by CloudNature). Internally, it has a *store* of the repo (likely commit-based) to synchronize code and repos.
  - *Incremental:* Yes – Sourcegraph crawls repos on change events. Their blog emphasizes “we often say Cody uses deep understanding” and context fetching methods. While not explicitly stated, Sourcegraph’s own code index is incrementally updated as code changes (like their code search).
  - *Deterministic intelligence:* Builds large code indexes: symbol indexes, cross-references (imports), code intelligence maps. These are used for contextual code search and jump-to-definition. Internally, they have syntax trees, symbol tables, etc. (Though not public, it is Sourcegraph’s core functionality.)
  - *Graph usage:* Some – Cody’s code search uses global graph of symbols (type/inheritance edges) for navigation, but not published. It does rely heavily on *search indexes*, not explicit graph traversal in the agent.
  - *Retrieval:* **Full-text search** and **symbol lookup** via Sourcegraph’s own code search (pulling BM25 or Regex from indexed source). It can also use embeddings (recent Cody may incorporate semantic search) and guides queries to relevant code. They explicitly use RAG: “Cody retrieves context via programmatic search when user submits a request”.
  - *Context compilation:* The Cody client collects search results (file snippets) and stuffs them into the prompt. Its architecture (blog) shows prefix+user+context as the prompt. It may truncate to fit the LLM window.
  - *Progressive retrieval:* Yes – Cody’s chat can iteratively fetch code (via built-in commands) as the user or agent asks deeper questions. They call it “context fetching methods” and interactive RAG. Likely orchestrated above the core.
  - *Provenance:* Good: because Sourcegraph’s code search identifies exact file and line spans, and Cody’s answers often reference file paths.
  - *Strengths/limits:* **Strength:** Deep, enterprise-grade code index supports very fast text and symbol search across repos. Clearly separates context retrieval (via search tools) from LLM. **Limitation:** It depends on the quality of conventional search indexes; semantic search may not be primary (they prefer RAG as more up-to-date than fine-tuning).

- **Continue (open-source agent)**:
  - *Repository state:* Reads working directory; no published snapshotting or hash tracking. Uses a YAML/JSON config to specify root.
  - *Incremental:* Indeterminate; likely no persistent index (just runs tree-sitter or text search on demand).
  - *Deterministic intelligence:* Possibly builds ASTs for tasks (it uses tree-sitter internally), but no open docs on static code indexes.
  - *Graph usage:* Not documented.
  - *Retrieval:* Uses “code-finder” tool (grep-like) and can integrate embeddings as one can configure RAG within Continue. Likely relies on user prompt to initiate search.
  - *Context compilation:* On each request, tools fetch and insert snippets. It has an **editor context** mode (edit-within-file) and **execute** tools.
  - *Progressive retrieval:* Yes – Continue has an “agent mode” with plan-and-do loop, where it can “add a file” or “list directory” iteratively. The orchestration is part of the open agent.
  - *Provenance:* Partial: its tools report file/line ranges.
  - *Strengths/limits:* **Strength:** Highly customizable; open-source. **Limitation:** Under-documented; likely less optimized indexing than others.

- **OpenHands (platform)**:
  - *Repository state:* Multi-agent framework; likely treats code via tools (e.g. a CodeSearch skill). No specifics on snapshot or hashing found.
  - *Incremental:* Not known.
  - *Deterministic intelligence:* Provides skills (linting, code search), but no integrated static analysis documented.
  - *Graph usage:* Not specifically.
  - *Retrieval:* Likely uses their CodeSearch (embedding-backed) skill to fetch relevant code.
  - *Context compilation:* The agent collects code via skills and sends to model.
  - *Progressive retrieval:* Yes – agents have a loop.
  - *Provenance:* Skills likely return (path, lines).
  - *Strengths/limits:* **Strength:** Modular SDK allows plugging your own tools. **Limitation:** Not a ready-made repo-intelligence stack on its own; mostly an orchestration.

- **IBM SWE-Agent (SWE-1.0)**:
  - *Repository state:* Targets GitHub repos; likely locks to a specific commit or uses current default branch. Unknown if it snapshots.
  - *Incremental:* Unclear; likely irrelevant as tasks are per-bug. Possibly indexes whole repo at start.
  - *Deterministic intelligence:* Likely builds parse/AST or symbol tables to localize bugs (given their high accuracy). Possibly uses dependency analysis.
  - *Graph usage:* Probably – they mention “Localization agent” which sounds akin to LocAgent’s multi-hop graph. But details are not published.
  - *Retrieval:* Custom pipeline: a bug description is used to search code (like LocAgent’s keyword search). Could be BM25+embedding.
  - *Context compilation:* For localization, it likely highlights file/lines in its output (they say 92.7% file-level accuracy). For fixes, it suggests code edits (using their “editor agent” with IBM’s LLM). The context for editing is likely the defective file plus neighbors.
  - *Progressive retrieval:* Yes – they have a multi-agent pipeline (localizer → fixer → tester). The LLM drives steps with tools.
  - *Provenance:* They report file and line suggestions to the developer (via GitHub).
  - *Strengths/limits:* **Strength:** Designed for end-to-end issue triage; reportedly high success using only open LLMs. **Limitation:** Not open/consumable by outside; details proprietary.

- **RepoCoder (research baseline)**:
  - *Repository state:* Operates on static snapshots of repositories (from benchmarks). Each run indexes the repo entirely (no notion of incremental updates beyond one-shot indexing).
  - *Incremental:* Not addressed (paper-level, not an ongoing agent).
  - *Deterministic intelligence:* Yes – it splits code into chunks (functions, methods) via AST parsing. It builds inverted indices for lexical search and pre-embeddings for dense search. It *does* iterative retrieval using the LLM’s partial outputs.
  - *Graph usage:* Implicitly – it does hierarchical retrieval (file → function → statement), but not an explicit graph data structure; more a coarseto-fine filter. No persistent graph stored.
  - *Retrieval:* Hybrid: both sparse (BM25/Jaccard) and dense (embeddings, UniXcoder) are used. It also uses the LLM in a loop to refine queries.
  - *Context compilation:* Constructs prompts with code windows (snippets of lines) interleaved with the task description. It truncates on max tokens. No advanced scheduling (simple concatenation).
  - *Progressive retrieval:* Yes – it iteratively calls retrieve→generate→retrieve. The sequence is orchestrated externally (not agentic in the LLM, but iterative context enrichment).
  - *Provenance:* Each retrieved snippet is known by file and offset in evaluation (they keep track of which snippet contributed to final answer). But not explicitly preserved to LLM output (paper-level metric).
  - *Strengths/limits:* **Strength:** Clear baseline for RAG workflows; demonstrates effectiveness of combined retrieval strategies. **Limitation:** Iterative loop adds latency; heavy on LLM calls. No support for long dialogues or context retention.

- **LocAgent (research)**:
  - *Repository state:* Processes a Python repo snapshot into a graph model. Treated as static for each issue.
  - *Incremental:* No – each query builds the graph from scratch.
  - *Deterministic intelligence:* Yes – builds a *lightweight heterogeneous graph* of the code (dirs, files, classes, functions as nodes; edges for “containment, imports, invocations, inheritance”). Also builds BM25 indexes on node text.
  - *Graph usage:* Core to system: the agent traverses this graph to localize code. The agent has graph tools for multi-hop search.
  - *Retrieval:* Hybrid: first use BM25 keyword search (via `SearchEntity` tool) to get candidate nodes, then follow graph edges (`TraverseGraph`) to related nodes. It does not use neural embeddings in the published version.
  - *Context compilation:* The final agent call `RetrieveEntity` outputs file path + code lines, which the agent returns as the answer location (or it can fetch full code). In a real agent scenario, these lines would be given to the LLM for editing.
  - *Progressive retrieval:* Yes – the LLM is in a single-shot chain-of-thought loop but uses the graph tools multiple times to explore step by step. The agent itself makes multiple reasoning calls.
  - *Provenance:* Excellent: every identified fix is rooted in a specific node (file and line) of the graph. The reasoning chain can be traced via the tools called.
  - *Strengths/limits:* **Strength:** Very high accuracy for locating relevant code via combined lexical+graph search; minimal noisy context (it finds exact lines). **Limitation:** Python-only (per paper); building full graph has upfront cost (though authors say it’s fast for medium repos). Not directly applicable to generating patches (only localization).

- **GraphCoder (research)**:
  - *Repository state:* Takes a frozen snapshot of a repo to build a codebase index (not incremental).
  - *Incremental:* No (one-off per evaluation task).
  - *Deterministic intelligence:* Yes – constructs a **code context graph (CCG)** per code completion query, capturing control-flow and data-flow around the target code. These graphs are generated via Tree-sitter.
  - *Graph usage:* Uses the CCG (fine-grained code graph) to drive retrieval: first find “similar context” snippets via a coarse search, then refine via graph structure. The graph is used as a filter/feature for retrieval ranking.
  - *Retrieval:* Coarse-to-fine: first lexical/dense search to get candidate snippets, then filter by graph-context similarity. They do use embeddings (Jina, etc) along with graph context matching.
  - *Context compilation:* Retrieved code is woven into prompts for a code LLM to complete the missing statement. The paper doesn’t detail deduplication; essentially prompt = context + question.
  - *Progressive retrieval:* No – it is one-shot retrieval for each completion.
  - *Provenance:* Limited – it knows which snippet was retrieved and used, but not exposed beyond evaluation logs.
  - *Strengths/limits:* **Strength:** Novel use of program graphs to boost code completion (improves accuracy over plain RAG). **Limitation:** Focused on small hunks (one statement completion); building graphs is costly and language-specific.

- **RepoGraph (research)**:
  - *Repository state:* Works on a static snapshot, parsing the entire repo into a line-level graph.
  - *Incremental:* No (paper-level, one-time index).
  - *Deterministic intelligence:* Yes – it parses every code file (e.g. Python) with Tree-sitter, identifies definitions (class, function names) and references (calls) by line. It filters out built-in and third-party calls to focus on project-specific relations.
  - *Graph usage:* Central: builds a fine-grained **line-level graph** where nodes = code lines (typed “def” or “ref”), and edges = “containment” (def contains its inner lines) or “invocation” (def ↔ ref). It then extracts *ego-graphs* (k-hop neighborhoods) around keywords to provide targeted context.
  - *Retrieval:* On a query term, it uses an index to find the matching node(s), then retrieves the k-hop subgraph around those nodes (including other relevant lines). Both lexical match and graph walk are used (like LocAgent’s combination).
  - *Context compilation:* The ego-graph is “flattened” (translated into a list of lines of code) which becomes the AI’s context for answering or patching. This is inserted into the prompt.
  - *Progressive retrieval:* Partial – it is normally used as a plug-in: either the entire ego-graph is added to context at once, or an agent tool could call it multiple times for multiple terms. The design suggests integrating as either prompt augmentation or an agent action.
  - *Provenance:* Strong: each returned line is tagged by file and line number. The graph action indicates why it was included (e.g. within 2 hops of a keyword).
  - *Strengths/limits:* **Strength:** Captures fine dependencies across repo; helps AI “see” the whole dependency context of an issue. Improves performance on repo-level tasks by 30%+ (reported). **Limitation:** Very expensive to build on large repos (the authors note scalability concerns). Sub-graph selection must be carefully tuned to avoid irrelevant code.

- **Claude Context (by Zilliz)**:
  - *Repository state:* Builds a fully indexed snapshot in a vector DB. It scans the repo (all configured files) once, then listens to changes for incremental updates.
  - *Incremental:* Yes. Explicitly **incremental indexing via Merkle trees**. The core keeps content hashes to detect new/changed files, re-embedding only those.
  - *Deterministic intelligence:* Yes – it uses AST-based chunking of code (labels as “code splitters” in docs). It also builds optional inverted text indexes (BM25) on the chunks.
  - *Graph usage:* No explicit symbol graph; it stores each chunk in a vector DB, but no complex graph inference. Does support hybrid search (BM25 + dense).
  - *Retrieval:* **Hybrid semantic search**: it supports BM25 and embeddings, and can combine them. Queries are answered by retrieving the top-k chunks from the vector DB based on cosine similarity of OpenAI embeddings (with fallback char-split if needed).
  - *Context compilation:* Returns exactly the code chunk (with file path) for each result. The client (e.g. VSCode extension) can display the snippet or inject into prompt. It does not summarize or trim beyond chunk boundaries.
  - *Progressive retrieval:* Indirectly: as an MCP server, it can be called by any client repeatedly. The base context compiler is separate; multiple calls gather more code. If a conversation asks for new search terms, Claude Context can be queried again.
  - *Provenance:* Excellent: each search hit includes the relative file path and line span in the chunk, so the agent knows exactly where it came from.
  - *Strengths/limits:* **Strength:** Scalable enterprise search (using Milvus). Efficient incremental updates via Merkle (explicitly listed). Rich language support (via AST chunkers). **Limitation:** Provides no AST or symbol info to LLM, only raw code. Ranking is simple cosine or BM25; no higher-level signals preserved.

# C. Repository-State Findings

Modern systems almost universally **treat a repository snapshot as an immutable state identified by a commit or root hash**. Cursor and Claude Context explicitly build *Merkle trees* over file contents to define a snapshot identity. Each file is hashed (e.g. SHA-256), directories aggregate hashes of children, and the root hash represents the entire repo state. This makes the snapshot reproducible and content-addressed. Unchanged files naturally keep the same hash and need not be reprocessed. For Git repositories, systems often tie this to commit SHAs: Cursor’s Merkle key is combined with Git parent info, so the snapshot carries commit provenance.

Dirty or uncommitted changes are typically handled by hashing the working directory state. Cursor’s client computes hashes for *all valid files*, including untracked changes, then does a handshake with the server. In practice, the root hash differs as soon as any content changes. Systems like Claude Context also re-hash and re-sync at intervals via Merkle diff. There is generally no notion of atomic snapshot beyond “eventually consistent”: the system assumes the working tree is static during each sync or that concurrent modification windows are small.

Cryptographic hashing enables **content-addressable storage**: Cursor caches embeddings by chunk hash, Claude Context indexes chunks by embedding (also content-based IDs), and theoretically unchanged code (even moved/renamed) could retain identity if the move is detected. Some systems (e.g. sourcegraph) might not do content hashing, but the modern trend (as seen in Cursor/Claude Context) is to support this. Notably, **Merklized trees solve the change-detection problem**: by sending the root hash to the server (as Cursor does), the system quickly pinpoints exactly which subtree (file) changed, rather than re-scanning all content.

File operations like creation, deletion, renames are inherently captured by the Merkle diff: a renamed file has a different path but the new path’s hash will match the old file’s content, so one could detect a match (though simple Merkle doesn’t track identity beyond hash). Submodules or ignored/generated files are typically filtered out by configuration (e.g. Claude Context lets you ignore patterns). The root identity therefore proves “content equality” up to collision risk: if two repo states have the same Merkle root, all file contents match (modulo hash collision). In Cursor, path obfuscation means the server sees only hashed path segments, preserving some consistency without exposing path semantics.

In summary, a strong architecture uses a **content-addressable snapshot** (often Merkle-rooted) to represent the repo state. This ensures reproducibility and incremental consistency. Alternative approaches (e.g. simply scanning on demand) lack the efficiency and identity guarantees that Merkle provides. The Merkle tree also elegantly handles atomicity: the “handshake” of root hash with server ensures the state is known up-front. Systems without such a snapshot risk re-reading unchanged files unnecessarily or giving the LLM inconsistent views if the code changes mid-query.

# D. Incremental-Indexing Findings

To avoid re-processing the whole repo on each change, top systems **cache derived artifacts by content hash** and invalidate only on mismatch. Cursor’s design is a prime example: it checks file hashes via the Merkle tree and *only* re-uploads or re-embeds changed files. Similarly, Claude Context’s index explicitly “re-indexes only changed files using Merkle trees”. The general pattern is:

```
Derived Artifact Valid ⇔ (input content hash unchanged AND same index version)
```

For example, if file `foo.py` is unchanged (same SHA-256), Cursor reuses all its previously computed *AST-chunks, tokenizations, embeddings, symbol info,* etc., by looking them up in a cache keyed by hash. This avoids duplicate work. Schema or tool version changes (e.g. upgraded parser) would force full re-index because “derivation implementation/version” changed.

Whether invalidation is file-level or finer varies. Cursor seems file-level (Merkle compares file content) but then chunk-level (it hashes chunks within files). Claude Context chunks AST nodes and re-indexes only modified chunks. Aider does not document incremental caching; it may rebuild the map file-by-file, but could in principle skip unchanged files if content hashes were tracked (though the docs don’t say so). In code search RAG systems, typical usage is to re-embed on any change, so not incremental.

Transitive invalidation (e.g. if file A imports B and B changes, should A’s analysis be redone?) is rarely handled explicitly. The Merkle approach handles only content identity; it does not, for instance, re-parse A if only B’s content changed (unless import graphs are considered). Cursor’s docs do not mention such transitive invalidation. In practice, deterministic facts (like cross-file symbol tables) would need rebuilding if dependencies change. A robust design might mark upstream files stale if an imported symbol’s signature changed, but most current systems re-run everything on change or rely on up-to-date code.

Indexes are usually updated **asynchronously** or incrementally in a background process. Cursor re-syncs every ~10 min. Claude Context presumably updates on file-change events. Users can tolerate slight staleness; systems do not normally stall the user for index updates. If an index is stale, typically a client fallback (e.g. direct disk read) may handle the immediate query, while indexing catches up. There’s generally no precise “stale flag”; the LLM might simply see older context until sync finishes.

Changes in tooling (parser update, embedding model change, index schema migration) must trigger a global rebuild. Cursor’s mention of “embedding models have limits” implies that if they change the model, cached embeddings would need recomputing. Similarly, Claude Context notes model and DB choice are configurable; a change there invalidates the index.

In principle, **maximal reuse** is possible if artifacts are content-addressed. In practice:
- **AST reuse:** If a file’s content hash is constant, its AST need not be re-parsed. (Tree-sitter could also content-hash parse-tree subtrees.)
- **Symbol index reuse:** Similarly, symbols extracted from an unchanged AST can be reused, saving parse work.
- **Embeddings:** Already cached by Cursor; Claude Context does this.
- **Lexical indexes:** Inverted indexes could reuse postings if text is identical.
- **Chunks:** Claude Context’s AST-based splitter means unchanged code yields identical chunks (and reused embeddings).
- **Documentation analysis:** If docs haven’t changed, their outlines can be cached too.

The main complexity arises with cross-file or global artifacts. For example, if file A didn’t change but file B (which it imports) did, do we need to re-index A’s embedding since its context changed? Most systems do not (they treat embeddings as pure function of the file’s code, not its imported context). However, a smart architecture might mark such derived artifacts stale. This would require dependency tracking in the index.

Overall, **existing systems follow the content-hash model**: compute an identity for each relevant input (file or chunk), include derivation metadata (tools versions), and if these match prior values, reuse the artifact. This approach is observed in Cursor and Claude Context. It suggests that ASTs, symbol tables, and embeddings need not be re-generated unless input changes. Some complexity remains (handling refactoring like renames, dependency invalidation), but content addressing is a strong pattern.

# E. Repository-Graph Findings

Graph-based representations vary widely:

- **File/Module Graphs:** Aider constructs a file-level graph (edges = import dependencies) to rank which parts of the repo map to send. This graph is limited: nodes are files, edges from static imports. It helps select top-ranked files/symbols but does not serve as a general knowledge graph.

- **Symbol/Reference Graphs:** LocAgent and RepoGraph show a much richer approach. LocAgent builds a *heterogeneous graph* of directories, files, classes, and functions, with edges for containment, imports, function calls, and inheritance. RepoGraph goes even finer: each *line of code* is a node (typed as definition or reference), with “contains” edges (def to its inner code) and “invokes” edges (def to ref of another def). These graphs encode nearly all static structure and cross-references in the repo.

- **Graph Semantics vs Storage:** In both cases, the graph is used to *guide search*. For LocAgent, the LLM traverses the graph (via tools) from initial keywords toward likely bug locations. In RepoGraph, queries yield an ego-graph (k-hop subgraph around a term) that is appended to context. Importantly, neither requires a special graph-database backend: both frameworks build an *in-memory* graph from ASTs on the fly. This shows that sophisticated graph semantics can be achieved without a graph DB; the data structure and traversal algorithms suffice.

- **Graph Algorithms:** Both Aider and LocAgent use ranking/PageRank on their graphs. Aider does a personalized PageRank on the file graph to downselect map entries. RepoGraph uses the ego-graph concept, which is essentially a BFS subgraph around a seed. PageRank is not explicitly cited for RepoGraph, but its ego-graph retrieval is a graph algorithm. LocAgent’s retrieval uses BFS (“multi-hop exploration”) rather than ranking.

- **Graph vs Specialized Index:** Typed graphs capture relationships (imports, calls) that an inverted index or embedding search might miss. LocAgent notes that *removing* its text search and relying only on graph severely hurts accuracy, showing that graphs augment but don’t replace lexical methods. Graph edges carry semantics (e.g. if A invokes B, that edge suggests relevance). However, building and maintaining such graphs is complex. RepoGraph authors note **scalability issues**: parsing whole projects into huge graphs is costly. Graph maintenance on code changes (incrementally updating node links) is non-trivial.

- **Cross-language and dynamic code:** None of the surveyed systems fully solve multi-language graphs. Aider’s Tree-sitter map supports multiple languages but doesn’t link across languages. LocAgent focused on Python. RepoGraph’s blog discusses filtering out third-party imports (so languages or libraries outside the repo are ignored). Dynamic language features (reflection, runtime imports) break static graphs. These are open challenges.

- **Typed Knowledge Graph:** The term “knowledge graph” sometimes is used loosely. Here we see two meanings: (1) **thin graphs** like Aider’s (files as nodes) which do not capture all structure, and (2) **rich graphs** like RepoGraph. The evidence suggests rich graphs enable better reasoning (LocAgent’s accuracy was very high). However, they add heavy indexing cost and complexity. A universal graph (line-by-line) like RepoGraph may exceed practical needs in many coding tasks.

In sum, graphs are powerful for navigation and disambiguation. The best architectures *decouple graph structure from persistence*: they build the graph on demand or in-memory, and feed only needed context to the model. Typed relationship graphs (contain, import, call, inherit) improve retrieval and localization, but they should complement rather than replace specialized text or embedding indexes. Aided by explicit provenance (edges carry semantic weight and origin), graph-based retrieval can be explainable. But complexity and scalability issues caution against using a full-blown persistent graph database – instead, build targeted graphs for the queries at hand (as LocAgent and RepoGraph propose).

# F. Retrieval and Relevance Findings

The literature shows **no single “silver bullet”** retrieval; rather, effective agents combine multiple approaches:

- **Exact identifier/symbol lookup:** Tools like Aider’s repo map or language-server-style indexes allow direct lookup of definitions by name. This is fast and precise for known symbols.

- **Full-text/Grep/BM25:** Many systems rely on textual search. LocAgent’s `SearchEntity` uses BM25 on tokenized code to find candidate entities. Claude Context supports BM25 (via its hybrid search). Full-text search excels at finding occurrences of literal tokens (bugs, TODOs, etc.) across the code. It is great for bug localization keywords or finding config references.

- **Symbolic/Structural search:** Aider’s strategy is structural: the LLM uses the map to decide which files define needed APIs. Graph-based agents (LocAgent) use structural tools to traverse imports/calls. These catch cases where the relevant code isn’t lexically similar to the query (e.g. bug about “login” might require jumping to an auth class used elsewhere). Symbol lookup is essentially structural: “where is function X defined?” Agents can directly ask for definitions or imported modules.

- **Graph traversal/ranking:** LocAgent combines BM25 with graph multi-hop search. This can connect distant concepts (issue → keyword search → a function → inherited class, etc.). GraphCoder uses the code-dependence graph to find context-similar snippets (coarse-to-fine). These graph-based methods excel at *localization* tasks (finding files/lines), not so much at retrieving full code spans.

- **Embeddings/Vector search:** Emerging strongly. Cursor and Claude Context both use vector embeddings for semantic code search. This finds code that “means” something similar, not just textually. Useful for finding patterns or relevant docs. RepoCoder explicitly integrates dense embeddings along with BM25. Hybrid systems (Claude Context) combine BM25+dense in one pipeline. Semantic search is especially helpful when the query is conceptual (e.g. “find DB access code”), or the code uses synonyms.

- **LLM-directed interactive search:** Tools like “/search” or “/find function” let the LLM query the repo via natural language. The LLM may produce its own search queries, and iteratively refine them based on answers. This is used in tools like Claude Code or LocAgent (the agent itself picks search keywords). Some pipelines (RepoCoder’s iterative loop) use the LLM’s output to guide the next retrieval round.

**Which to use when?** No definitive rule yet, but patterns emerge:
- **Exact/symbol lookup** is best for knowing *precisely* what file defines what (API calls, config names).
- **Regex/full-text** is efficient for straightforward localization (error messages, TODO tags).
- **BM25** handles more natural queries (bug description terms) while being cheap.
- **Embeddings** shine when the question is semantic or high-level (architecture questions, code examples), or when the relevant code uses different vocabulary.
- **Graph search** is key for navigation tasks like finding where to implement a cross-cutting change (inheritance chains, utility imports).
- **Agents with iterative retrieval** (like RepoCoder’s loop or LocAgent’s multi-tool) suit tasks needing contextual refinement (e.g. code completion with complex dependencies or bug localization).

Most strong systems employ **multiple** methods. For example, RepoCoder uses both sparse and dense retrieval; LocAgent explicitly uses lexical + graph traversal; Aider uses a structural map plus allows manual file additions. Hybrid relevance (text+vector) is a common theme.

There is a trend *away* from relying on one fixed index. A more powerful design uses **diverse candidate generators**: lexical index, structural index, embedding search each propose answers, then a ranking stage selects among them. No system uses only “one approach to rule them all.” In fact, there is evidence that combining signals yields better performance than any alone.

# G. Context-Compilation Findings

Retrieval only returns raw code snippets – what to *send to the model* is a separate design problem. Strong systems explicitly distinguish **ranking vs final selection**. For instance, Aider *ranks* which files to include (via its graph algorithm) but then composes a “map” by taking definitions from those files. Claude Context retrieves chunks but it’s up to the client to decide ordering and truncation.

Key observations:
- **Granularity:** Some include whole files (difficult for large files), others send only relevant functions or even single lines. LocAgent’s `RetrieveEntity` returns exactly the relevant lines (not the whole file). Claude Context returns chunks bounded by AST (not entire file).
- **Excerpt selection:** In Aider’s map, only “critical lines” of definitions are kept (signature lines). RepoGraph flattens ego-graphs, essentially selecting a focused set of lines around keywords.
- **Representations:** All examples send actual code text. No system (yet) sends higher-level abstractions (e.g. API summaries or UML) to the LLM – that complexity is left to the model.
- **Budgeting:** Every tool must handle token limits. Aider has a `--map-tokens` setting to adjust how much of the map to send. Claude’s clients presumably cap token count per message. Systems truncate at boundaries, but specific strategies (prefer smaller functions, truncate middle of large files, etc.) are usually ad hoc.
- **Duplication removal:** If two retrieval methods return overlapping code, most frameworks simply rely on the natural deduplication of vector search or on code similarity. None described a systematic deduplication pass. In practice, the client might filter out identical spans.
- **Diversity/ordering:** Results are often presented in order of relevance score. Aider’s graph-ranking effectively orders symbols by “importance”. We have scant evidence of active “diversity boosting” (beyond LLM sampling in loops). It’s likely not a major focus yet.
- **Authoritative preference:** If multiple contexts conflict, some systems might prefer official docs or tests. We see hints: Claude Context can index Markdown so documentation could come up, and Aider’s `@Docs` tool (deprecated) indicated preference for docs in some contexts. But no clear principle across systems; likely left to prompt design (e.g. “Use code, not comments”).
- **Overlapping knowledge:** Once context is given to the LLM, it might forget where it came from (unless provenance kept). The architecture should ensure we don’t send duplicate info; repeating the same code snippet wastes tokens. This requires tracking what’s been used – the system design should either avoid repeating queries or filter repeats before insertion. None of the surveyed systems detail how they track past disclosures, but a robust system would do so (e.g. track which file:line ranges have been shown).

Importantly, **context compilation is distinct** from retrieval. Evidence from Aider, LocAgent, and the Claude blog indicates that retrieval yields candidate code, *then* a separate process (the “prompt assembler”) combines them into a prompt. They do *not* simply feed all raw results to the LLM unsorted. The logical pipeline is: generate candidate pieces (from various retrievers), score/rank them, then pack the top N into context. The final ordering in the prompt can affect performance (in some settings, placing definitions earlier is better). Empirically, code LLMs are sensitive to token order and content: relevant info earlier often yields better answers. This suggests architecture should allow tweaking the prompt order.

Finally, system designs implicitly assume context should be **as compact as possible** while retaining all needed info. Unnecessary code or comments are dropped if out of token budget. For example, Aider omits the bodies of functions and only shows signatures in the map. Progressive systems (like RepoGraph) do narrow the context via graph filters. This supports the candidate idea that context compilation (handling overlap, ordering, budget) should be a separate, well-engineered component.

# H. Provenance and Security Findings

**Provenance:** Very few current agents provide explicit lineage of how a piece of code ended up in the model context. However, it is critical for traceability. Best practice (as seen in LocAgent and RepoGraph) is to annotate each fragment with *file path, line numbers, and derivation source*. LocAgent’s `RetrieveEntity` tool returns exactly the file and lines. A system could embed these as part of the context in metadata (or in fine print comments). Claude Context’s search returns (path:line-range) for each hit, which preserves provenance.

Ideally, **every context snippet carries a tag**. For example: `"File: foo.py, Lines 120–130 (function X definition)"` preceding the code block. This way, the LLM output (or the answer from the agent) can be traced back. None of the surveyed systems fully integrate provenance into the LLM output, but several retain path info in logs or UI. For high-precision tasks (especially automated patching), keeping provenance is necessary for audits and reproducibility.

**Security (trust boundaries):** All systems treat the repository as *data*, not as instruction. That means code comments, README, tests are not to be executed as commands. This distinction is mostly a matter of policy: the agent framework must never put unvetted code into the “system prompt” or policy area. For example, Claude Code’s documentation explicitly says that CLAUDE.md instructions and auto-memory are treated as context for the model, not as unbreakable rules. Similarly, a repository file containing an instruction like “don’t fix this bug” should not override the agent’s logic.

Prompt injection is a known risk: code or docs might contain strings like “Ignore all instructions above”. A secure design would sanitize or fence repository content, e.g. by not including directive-like keywords in system prompts. One approach: wrap all repo code under a clear “CODE:” prefix in the prompt, so the model sees it as separate from the user instruction. Modern coding agents implicitly assume such separation by how they structure prompts. None of the sources explicitly discuss malicious repo content, but standard security practice is to **never treat external text as system instructions**. Tools and policies (like Anthropic’s `PreToolUse` hooks) enforce safety rules above the LLM’s control.

In summary: repository content should remain **observable to the model but not authoritative**. Agents should have built-in checks (or final Human approval) before executing code based on retrieved context. We should design architectures where repo text is clearly labeled as input data. If systems allow agent tools (like `ls`, `grep`, `open-file`), those should be strictly separated from actual code execution. Authentication and authorization (which user invoked the agent on which repo) must be enforced outside the model. The sources do not detail this, but security research emphasizes it.

# I. Progressive-Disclosure Findings

Leading agents combine **static preloaded context** with **interactive retrieval**. Aider’s repo map is an example of preloading: the map of definitions is sent in the first prompt. Claude/Continue rely on the user or system to prompt extra search, effectively doing interactive retrieval. LocAgent and RepoGraph break tasks into *steps*: localize first (using partial data), then once a location is found, fetch the relevant code block. RepoCoder’s iterative loop is another form of progressive: each iteration refines context based on new info.

When is preloading better? For understanding broad project structure (APIs, class hierarchy), a one-time summary (like the map) helps. Aider’s experience is that knowing the available interfaces improves first-pass solutions. However, preloading everything is infeasible.

Interactive retrieval shines when the initial query is ambiguous: the model may need to first locate relevant modules before pulling full code. This is shown by LocAgent, where the LLM guides multi-hop search. Similarly, a model might ask “can I see the login function and where it’s used?” and trigger a tool call.

In practice, **hybrid is ideal**: give the model a broad outline (map of symbols or an outline of modules), plus the ability to fetch details on demand. Architecturally, the *context compiler* component remains deterministic: it receives lists of files/lines and appends them. The *agent orchestration* (LLM reasoning loop) is above it, controlling which queries to issue. In other words, the compiler does not itself “decide” what to get next — that is agent logic. This clean separation simplifies caching: once the compiler sends something, it need not try to repeat it without the agent asking anew.

To avoid redundant retrievals, the system can track a “context frontier” — which pieces have already been disclosed. When an LLM tool requests code, the controller should check if that fragment was already given. If so, it need not fetch again. No surveyed system explicitly mentions this, but it’s a straightforward improvement.

In sum, evidence from Aider, RepoCoder, LocAgent, etc., suggests a **two-tier design**: (1) **Static context compiler:** produces initial context (map or search results); (2) **Dynamic agent controller:** decides on further `Search`/`Open`/`TraverseGraph` steps. The compiler itself treats each reveal as final, while the agent logic handles the loop. This separation avoids conflating prompt assembly with decision logic.

# J. Evaluation Framework

To measure the benefit of repository intelligence, one must evaluate on multiple axes:

**Retrieval Quality:** Metrics like Recall@K, MRR, nDCG are appropriate. For localization tasks, measure “file-level accuracy” or “line-level accuracy” (as LocAgent did). For retrieval-augmented completion, measure how often the correct information is in the retrieved context (e.g. required lines coverage). The repository-IR community has similar metrics. It’s important to gauge recall of needed files/symbols, not just precision, because missing a relevant file can cause failure even if ranking is good.

**Context Quality:** Proposed metrics include “relevant info retained” (did we include the lines needed?), “irrelevant info” (noise). One can measure how many tokens of useful info per total tokens used (information density). Bounded metrics like BCQ (Barrault Context Quality) might be adapted to code context: e.g. how much of the “ground-truth” snippet from a reference solution is in context. Budget-awareness: percentage of context window filled with necessary facts. These are active research topics.

**Agent Efficiency:** Track model calls and tokens, number of file reads, query calls, and total time/cost. Compare a baseline agent (no repo-intel, just naive search) vs. one with the intelligence framework. Ideally, the agent with repository intelligence should use fewer LLM calls (since it can find info deterministically) and fewer tokens to reach a solution. Record number of iterations or question reformulations saved.

**Task Success:** The ultimate measure is task performance: percentage of tasks (e.g. code-fixing, feature implementation) solved correctly, tests passed, or user satisfaction. For coding tasks, common benchmarks (e.g. HumanEval for completion, or SWE-Bench for issues) can be used. One could run A/B tests: given a coding agent plus basic file tools vs. agent plus repo-intel, see which finishes more tasks or with fewer errors. Regression rate (introducing new bugs) is also informative.

**Controlled Experiments:** A credible experiment would take the same model (say GPT-4o or Qwen2.5) and compare:
- **Treatment:** agent equipped with repository index, graph navigation, cached context.
- **Control:** agent using only raw file system and grep/BM25.
Keep the LLM calls identical in number where possible, to isolate the effect of retrieval quality. Also control for randomness (run multiple seeds). Important confounders: model temperature, prompt design, task difficulty, repository size. Matching tasks by difficulty or using benchmark suites (like the one LocAgent used) helps fairness.

Few sources detail such evaluation. RepoCoder’s paper evaluates accuracy on completion benchmarks. LocAgent measured localization accuracy. IBM’s blog reported success rates on SWE-Bench (23.7%). These can inspire metrics. However, there is no off-the-shelf “code retrieval TREC” standard yet, so a new evaluation framework might need to be built or adopted from IR.

# K. Local-Model Implications

Deterministic repository intelligence **enables smaller models** to perform better by offloading memory of code facts. We have evidence that with strong retrieval, smaller open LLMs can approach the performance of larger models. IBM’s SWE-Agent 1.0 achieved near top leaderboard results using *open-source* LLMs by focusing on precise localization rather than brute-forcing with a bigger model. Aider users often run smaller models (GPT-4o Mini etc.) with the structural map and report effective outcomes (though no formal study cited).

High-quality retrieval likely narrows the gap: if a small model is given exactly the lines it needs (with all context), it may answer as well as a larger model with no context. Conversely, large models waste capacity if they have to “rediscover” repository facts from code text. Structured contexts (symbol lists, AST snippets) may help smaller models reason correctly by providing needed scaffolding.

Tasks like linking API use across files or understanding class hierarchies are known to be hard for blind LLM reasoning; deterministic analysis (like Aider’s definitions or LocAgent’s graph) can handhold a smaller model through these. On the other hand, tasks that require genuine reasoning or creativity (algorithm design, novel code) should remain in the model’s domain.

We should therefore assign the agent: “know *what* the repository contains (facts, structure, indices)” and the model: “decide *how* to use those facts to solve the task”. In practice, that means: if the task is to find where to fix a bug, the infrastructure should handle search; the model should focus on generating the fix or analyzing error. If a small model tries to search by itself (via chat), it will be inefficient. So equipping it with strong retrieval shifts most effort off-model.

There is limited formal research on model-size vs retrieval, but general RAG literature suggests smaller models benefit more from curated context. It is plausible that smaller models suffer more from irrelevant context (so we should be stricter in selection). We also expect that a small model will struggle more than a large one if given too much irrelevant code; hence context comp (dedup, relevance) is even more crucial for them. This aligns with the division of labor in candidate idea 12: keep a deterministic compiler that consistently prunes context, so the small model only sees what’s needed.

In short: investing in deterministic repo analysis is especially “worth it” when you plan to use smaller or specialized LMs. It reduces the need for the model to memorize code or do heavy IR in-context, making agent responses more reliable without scaling up model parameters.

# L. Candidate-Idea Verdicts

We evaluate each candidate architecture idea against the evidence:

1. **Immutable content-addressed `RepositorySnapshot` (Merkle, etc.)** – *Strongly supported.* Cursor and Zilliz explicitly use Merkle trees to define snapshots. This pattern solves consistency and reuse. It’s not unnecessary complexity: it’s proven by these systems.

2. **Unchanged resources retain identity across snapshots** – *Strongly supported.* Content-addressing inherently gives this property. Cursor’s embedding cache and the fingerprinting of files show reuse of identical content. Claude Context’s design implies this (Merkle diff).

3. **Derived-artifact validity as function of (input hashes + version)** – *Supported with qualifications.* This is standard in build systems. Cursor’s cache by chunk-hash exemplifies it. No source explicitly formalizes “derivation metadata”, but it’s a sound principle. In practice, versioning of parser/AI-model must also be tracked.

4. **Repository intelligence from many independent analyses (not one monolithic index)** – *Strongly supported.* Systems separate tasks: e.g. AST map vs vector DB. Aider’s repo map is distinct from any search index. Claude Context has separate AST-splitter, embedder, and vector DB components. Combined monolithic indexes would be brittle. Thus multiple focused indexes (lexical, AST, graph) are preferable.

5. **Typed repo relationships as a knowledge graph (no DB required)** – *Supported with qualifications.* LocAgent and RepoGraph prove value of typed graphs. They don’t need Neo4j or similar; in-memory graphs suffice. However, building and maintaining such a graph (especially at line granularity) is costly. The evidence supports *using graphs* for certain tasks, but systems like Aider show you can get by with simpler indexes for others. So a graph is useful, but must be applied judiciously (otherwise unnecessary complexity).

6. **Independent retrieval/evidence producers (lexical, structural, graph, semantic)** – *Strongly supported.* All the hybrid systems (RepoCoder, LocAgent, ClaudeContext) combine methods. No one relies exclusively on one mechanism. The evidence suggests combining multiple signals yields better recall (e.g. LocAgent’s ablation shows graph or BM25 alone under-perform combined). This approach is not only supported, it is considered best practice.

7. **Preserve multiple relevance signals, not collapse to a single score** – *Supported with qualifications.* Some systems implicitly do this (e.g. LocAgent’s SearchEntity vs TraverseGraph represent different signals; ClaudeContext’s hybrid search keeps both BM25 and vector results). However, many implementations do collapse to a single score per candidate. The idea of *explicitly preserving* signals is more of an open possibility. It is not contradicted by evidence; in fact, the architectures of hybrid systems suggest that treating them separately (until final rank) could improve explainability. I’d mark it “supported but uncommon”: the trend is towards hybrid ranking (often via weighted sum or learned ranker), but architects may gain by tracking each signal.

8. **Maintain ranking separate from final selection** – *Supported.* Evidence from Aider and RepoCoder shows they rank candidates first, then pick top ones for context. In practice, retrieval returns a pool sorted by relevance, and context assembly then picks a subset. This separation is clear in academic frameworks (retriever vs generator stages) and in systems (vector search returns a list, then the client picks first N). No system implements “end-to-end selection” in one step. So distinction is correct.

9. **Context-compilation has its own role (ordering, budgeting, dedup)** – *Supported.* See section G. Systems like Aider pre-truncate the map and LocAgent retrieves minimal code. The architecture diagrams (Sourcegraph’s blog) imply a prompt assembler block. It’s unnecessary complexity? On the contrary, it’s necessary to maximize use of the context window. Evidence suggests performance can vary by how context is assembled (though we lack formal ablations, it’s a common AI-UX principle). So treat context-compilation as distinct.

10. **Provenance attached to each disclosed component** – *Strongly supported.* While not many systems do it perfectly, the importance is clear: LocAgent, Claude Context, RepoGraph all highlight file/line provenance. The lack of provenance in many systems is seen as a limitation. Therefore, carrying provenance is indeed a principled architecture decision.

11. **Repo-derived content as untrusted data (not instructions)** – *Supported.* All sources implicitly practice this: none of them allow README directives to hijack the agent. Claude docs explicitly separate `CLAUDE.md` (user instructions) from code context. This candidate is basically a reaffirmation of prompt-safety norms. It’s necessary (and evidence suggests no one violates it intentionally). We mark as “supported” (or necessary) because it’s basically an accepted rule in these systems.

12. **Progressive context via orchestration, not making compiler agentic** – *Supported.* Systems like Aider and RepoCoder implement progressive retrieval at the application layer, not inside the prompt compiler. LocAgent’s multi-step logic is above the graph tool. The idea that the context compiler should not itself loop (but rather be stateless given input) is consistent with these architectures. Yes, the strongest designs separate the **agent loop** (chain-of-thought, tool calls) from the **context-building engine**. This is good design; the evidence from multiple systems supports it.

# M. Recommended Architecture (Semantic)

Based on the above, we recommend a **hybrid repository-intelligence architecture** with these core components and flows:

1. **Snapshot Manager:** On each project or workspace, compute a **RepositorySnapshot** identified by a Merkle root (or Git commit). Track file hashes and directory structure. Ensure a clear timestamp/commit is stored.

2. **Indexers (incremental):** For each snapshot, run parsers/ASTs to extract *deterministic facts*:
   - **File inventory:** List of files, languages, modules.
   - **AST-based tokenization:** Split code into logical chunks (functions, methods).
   - **Symbol table:** Definitions of classes, functions, variables.
   - **Reference map:** Cross-references (imports, calls, inheritance).
   - **Tests & docs links:** Map tests to code, docs to code if possible.
   Each indexer produces an artifact labeled by input content hashes (for caching). On subsequent changes, reuse unchanged artifacts.

3. **Graph Builder:** Construct one or more *repository graphs* from indexer output. For example:
   - **File Graph:** nodes = files, edges = imports or module relationships (for coarse navigation).
   - **Symbol Graph:** nodes = symbols or AST nodes, edges = calls, inheritance, definitions (for fine localization).
   - Graphs are **knowledge graphs** of typed relationships but not stored in a heavyweight DB; in-memory graph built incrementally if needed.

4. **Retrievers:** Implement multiple retrieval modules:
   - **Lexical Search:** e.g. BM25 inverted index over code/text (like Elasticsearch/Whoosh) to quickly find keyword matches.
   - **Symbol Lookup:** direct lookup (from symbol table) of definitions or references by name.
   - **Structural Query:** graph traversal methods (e.g. BFS from a set of files, or ego-graph expansion around keywords).
   - **Vector Search:** embed each code chunk (AST-derived) into a vector DB, enabling semantic search.
   - Possibly **LLM Query Tool:** allow the agent to run a search tool (like grep or an API) via the LLM.

5. **Ranking & Relevance:** For a user query or model prompt, each retriever returns a ranked list of candidates (file/line segments) plus relevance signals (score, match type). Use a ranking stage (possibly weighted or learned) to merge these signals into a final ordering of candidates, but do not collapse signals prematurely. Keep the reasons (e.g. “matched by name”, “import connected”, “vector similarity”) attached.

6. **Context Compiler:** This module takes top-ranked candidates and assembles them under the token budget:
   - **Dedup/Filter:** Remove overlapping or subsumed fragments.
   - **Excerpt selection:** Choose relevant lines (exclude irrelevant body text if summary or signature suffices).
   - **Ordering:** Place more relevant or higher-priority context first.
   - **Budget management:** Truncate or drop lowest-ranked items if needed.
   - **Record provenance:** Tag each snippet with its source file/path and range. Maintain a log of what has been given.

7. **Agent Orchestration Layer:** Separately from the above, an agent (LLM-based) takes the compiled context and query. It can also call on retrieval tools for further data. This layer handles iterative loops: after seeing initial context, the LLM might ask for more files or deeper analysis, prompting the orchestrator to re-run retrieval or graph search and merge new results.

8. **Output & Integration:** The final LLM output is applied (e.g. code change). Record exactly which context pieces and derivations were used for traceability.

This architecture **exceeds simpler search-only or monolithic-index designs** by explicitly coding structure. It generalizes Cursor’s Merkle indexing and embedding cache, Aider’s AST map and PageRank, LocAgent’s graph traversal, and Claude Code’s RAG chain. The major components are clearly delineated and connect through defined interfaces (content hashes, vector index, graph APIs, etc.). Provenance flows through all stages: each piece of context is tagged from indexer to final answer.

This architecture enables incremental updates: a file change triggers the indexers only for affected pieces (AST delta, new embeddings), with others unchanged. It allows hybrid retrieval: the agent can combine exact name matching, import graphs, and semantic search. The multi-signal ranking supports explainability and future learning.

# N. Improving on Current Systems

Based on gaps in existing designs, our architecture can advance beyond the state-of-art in several ways:

- **Finer-grained content addressing:** Extend content hashes to sub-file units (AST nodes or logical blocks). Cursor already hashes file chunks, but one can hash entire AST subtrees, enabling reuse of code block analyses even if their container moved. Research into AST-fragment caching could reduce work after refactorings.

- **Derivation-aware invalidation:** Track not just raw content changes but also how changes propagate. E.g. if function signature in A changes, mark usages in B stale. Current systems (e.g. Cursor) do not handle this; we could add dependency tracking to invalidate affected embeddings or analysis.

- **Comprehensive graph with provenance:** Build a **typed knowledge graph** that is provenance-bearing: each edge/relationship carries a source analysis ID and tool version. Tools like LocAgent hint this, but generally provenance is lost. We propose carrying annotations on graph edges (e.g. “parsed by Tree-sitter v0.20”), facilitating debugging.

- **Multi-signal retrieval architecture:** Explicitly preserve different relevance signals through to ranking, instead of collapsing to a heuristic score early. This means designing the index and retrieval API to tag each hit with all contributing reasons. This improves explainability and enables future learning of weights.

- **Learned ranking fallback:** Current strong systems use hand-tuned or algorithmic ranking. We can log retrieval contexts and success/failure to train a learned ranker (as hinted by CIT and LLM-based rankers). This hybridizes deterministic signals with machine learning.

- **Authority-aware retrieval:** Differentiate information sources by trust – e.g., company-internal wiki vs code vs tests. In context compilation, prefer company docs or official API docs over arbitrary code comments. Some evidence (Sourcegraph preferring code context) suggests this matters, but it is ad-hoc. An improved architecture might tag sources by type (e.g. user docs vs code) and let policies weight them.

- **Test-code linking:** Many agents ignore test files. A robust system should explicitly index tests, map them to code (e.g. using symbol references), and use them for relevance (like test-driven RAG for bug fixes). No system except RepoCoder’s feedback loop emphasizes tests.

- **Change-impact analysis:** Going beyond static context, track version control history (co-change patterns) to inform relevance. If two files often change together, use that as a retrieval signal. E.g. if modifying one, the agent should inspect the other. None of the surveyed systems explicitly use change-history data; it could improve localization or suggestion relevance.

- **Persistent context caching:** Track which contexts have already been given to the model in a session or on a task, to avoid re-fetching. Agents today typically do not de-duplicate across turns. A more sophisticated approach would cache previous LLM contexts and avoid repeating them.

- **Better evaluation metrics:** The research suggests measuring retrieval and context quality explicitly. We propose building or adopting benchmarks for context relevance (like BLEU for code snippets) and extending things like BCQ to code. Current evaluation focuses on final task success; intermediate metrics would help fine-tune repository intelligence.

These ideas vary in maturity: some (content hashes, AST reuse) are straightforward engineering; others (learned ranking, fine-grained provenance) are active research directions. But all are grounded in shortcomings or next steps implied by existing systems.

# O. Failure Modes and Tradeoffs

The recommended architecture is rich and flexible, but could fail or impose costs in some scenarios:

- **Complexity vs Benefit:** Building ASTs, graphs, and vector indexes for every repo is heavy. For small projects, this overhead may not pay off compared to simple search. The system must be judicious (e.g. skip graph building for tiny repos). Extra complexity can also increase bug surface area in the tooling.

- **Staleness and consistency:** With so many caches (embeddings, graphs), there is risk of stale or inconsistent data if not managed correctly. Edge cases (branch rebases, partial sync) could confuse snapshot identity. A simpler architecture (just search) would not have these subtle consistency issues.

- **Storage and compute:** Content-addressed caches and graphs consume storage. A Merkle-indexed vector DB might double the repo size. On very large monorepos, graph structures might blow up memory or DB size. One must balance granularity: e.g. avoid line-level graph on a 10M LOC repo.

- **Search freshness:** Relying on periodic sync (e.g. every 10 minutes) can miss immediate changes. If a developer expects instantaneous results, the system may appear laggy. A simpler on-demand search has no such delay (but is slower per query).

- **Overfitting to structure:** Too much emphasis on static analysis might mislead the agent if code is dynamic or calls are indirect. For example, a symbol index might miss reflection, whereas pure text search might catch string names. Each indexer is an approximation.

- **Ranking complexity:** A multi-signal ranker can over-prioritize certain signals and bury others. If poorly tuned, a deterministic fallback (like exact match) might have less chance. There's a risk of “analysis paralysis” where too many signals confuse the system. A simple hybrid (e.g. XOR lexical/semantic) is easier.

- **Provenance overhead:** Attaching metadata to every snippet could bloat context tokens. If not carefully encoded (e.g. as comments), it could interfere with the LLM’s reasoning. There’s a tradeoff between traceability and prompt size.

- **Local-model constraints:** Ironically, giving more context to help smaller models means more tokens used, which might force them to drop deeper reasoning. A frontier model might handle some ambiguity that a small model can’t, even with context. So the benefit for small models may saturate.

- **Agent orchestration vs determinism:** Having the agent control retrieval means outcomes become nondeterministic (depending on LLM chain-of-thought). A monolithic context compiler approach would be more predictable. There’s a tradeoff between flexibility (progressive queries) and reproducibility.

- **Security pitfalls:** Complex retrieval might inadvertently expose credentials or secrets (if the repo contains them) as context. Simpler architectures might avoid dealing with this issue (by blocking entire paths). Our design must ensure filtering of sensitive files (ignore patterns) to avoid injecting private keys into the LLM prompt.

In sum, while the sophisticated architecture provides strong capabilities, it demands careful engineering: robust invalidation, smart defaults (don’t index everything if not needed), and thorough security sanitization. Less elaborate alternatives (e.g. simple search plus a few LLM tools) could outperform it for trivial repos or tasks. The chosen design should allow graceful degradation: e.g. skip heavy graph steps if unavailable.

# P. Research Disposition Table

| Finding/Claim                                                         | Classification                          |
|----------------------------------------------------------------------|-----------------------------------------|
| **Content-addressable snapshots (Merkle)**                             | Principle – adopt now (used by Cursor/Claude) |
| **File-chunk content hashes & caching**                                | Principle – adopt now (Cursor evidence) |
| **Stable content identity across snapshots**                           | Principle – adopt now (Merkle technique) |
| **AST/chunk reuse via hashes**                                         | Capability – architecture should enable (no system explicitly does tree-hash reuse, but feasible) |
| **Incremental index invalidation by content**                          | Principle – adopt (Cursor/Claude do this) |
| **Transient vs transitive invalidation**                               | Research – needs study (not done in current systems) |
| **Symbol/table/index reuse**                                           | Capability – architecture should enable (generally used) |
| **File inventory & language modules**                                  | Principle – adopt (all systems need file list) |
| **AST-based chunking**                                                 | Principle – adopt (Aider/ClaudeContext use ASTs) |
| **Reference/symbol indices (imports, calls)**                          | Principle – adopt (Aider, LocAgent, RepoGraph use them) |
| **Call graph / inheritance graph**                                     | Capability – architecture should enable (some systems have partial support) |
| **Graph of code lines/dependencies (RepoGraph)**                       | Research – promising but heavy (interesting, beyond “must have” yet) |
| **Repo maps (class/method summary)**                                   | Capability – architecture should enable (Aider’s idea) |
| **Typed repository relationships (as graph)**                          | Capability – architecture should enable (LocAgent, RepoGraph) |
| **Separate structure indexes vs monolithic**                           | Principle – adopt (evidence favors separation) |
| **Graph + structural ranking (PageRank)**                              | Capability – evaluate (Aider uses PageRank on file graph) |
| **Exact identifier lookup**                                            | Principle – adopt (clearly useful) |
| **Greedy/regex/BM25**                                                  | Principle – adopt (foundation for IR tasks) |
| **Semantic vector search**                                             | Principle – adopt (Cursor/Claude do this) |
| **Sparse-dense hybrid retrieval**                                      | Principle – adopt (ClaudeContext example) |
| **Interactive LLM-driven search tools**                                 | Capability – architecture should enable (supported by agent frameworks) |
| **Iterative retrieval-generation loops**                               | Capability – evaluated (RepoCoder, LocAgent show value) |
| **Preserve multi-signal relevance evidence (before ranking)**          | Capability – evaluate (not done widely yet) |
| **Hand vs learned ranking of candidates**                              | Capability – evaluate (opportunity to add learn-to-rank) |
| **Context selection independent of retrieval**                         | Principle – adopt (discussed above) |
| **Token-budgeting and overlap removal**                                | Principle – adopt (necessary for efficiency) |
| **Provenance attached to context pieces**                              | Principle – adopt (important for traceability) |
| **Treat repo content as data only**                                    | Principle – adopt (safety consideration) |
| **Separate compiler vs agent loop**                                    | Principle – adopt (supported by design separation) |
| **Test/code relationship indexing**                                    | Capability – architecture should enable (seldom done explicitly now) |
| **Change history/co-change analysis**                                  | Research – interesting extension (beyond current systems) |
| **Cross-language support by design**                                   | Capability – architecture should enable (important for multi-stack repos) |
| **Graph algorithms vs specialized indexes (trade-offs)**               | Insight – use graphs selectively (e.g. do not graph every code line for trivial repos) |
| **Provide context in model-optimized order**                           | Capability – architecture should enable (common sense) |
| **Evaluate with new context-quality metrics**                          | Research – needed (no established code-centric metrics yet) |

# Q. Sources and Evidence Quality

- **Cursor (OpenAI/Cursor)** – *EngineerCodex blog* (unofficial but cites Cursor team posts); *Cursor Security docs* (official, limited view). We infer architecture from these, so treat as industry source.
- **Aider (Sourcegraph community)** – *Official docs and blog* by the creator (Paul Graham, Medium/website). Reliable as open-source documentation of Aider.
- **Claude Code (Anthropic)** – *Official docs* and *user blog*. These describe CLAUDE.md memory (policy) and RAG context. Credible vendor sources for usage patterns.
- **OpenAI Codex CLI** – *GitHub & Medium* by community writers. Official code exists, but documentation is sparse. We drew architectural inferences (vendor claim).
- **Sourcegraph Cody** – *Official blog*. Primary source for how Cody uses RAG and context. The architecture doc was too general.
- **Continue** – *Docs and GitHub* (official, but architecture unclear). We have limited official info.
- **OpenHands** – *Official website/docs* (foundational but no repo-intel details).
- **IBM SWE-Agent** – *IBM Research blog*. Public release describing agent tasks; high-level but credible.
- **RepoCoder** – *EmergentMind summary* of a published 2023 ICSE paper. High-quality research insights on RAG/completion architecture.
- **LocAgent** – *EmergentMind summary* (and arXiv). Good coverage of main paper (2025).
- **GraphCoder** – *GitHub code/repo description*. Reflects content of a 2024 arXiv/ICLR paper. Primary evidence for graph-based RAG.
- **RepoGraph** – *Blog by author* (with presumed reference to arXiv). High-level but fairly detailed account of the approach.
- **Claude Context (Zilliz)** – *GitHub README*. Vendor-sponsored open source with clear architecture statements.
- **Evaluation Claims** – Various benchmarks reported in papers (RepoCoder, LocAgent, IBM). We cite these outcomes in context.

We avoid uncited speculation by only reporting design elements supported by these sources. Where an architecture decision is based on inference, it is marked as such. All factual claims above are backed by the cited lines.
