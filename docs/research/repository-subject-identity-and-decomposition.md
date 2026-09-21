# Repository Subject Identity and Semantic Decomposition

## Disposition

Status: Reconciled

Canonical research subject: Repository subject identity and semantic decomposition.

Related ADRs: ADR-0002.

Implemented evidence: snapshot-local function subjects and exact source occurrences.

Accepted: subjects, source anchors, retrieval units, and cross-snapshot continuity remain distinct.

Deferred: richer subject families, retrieval-unit derivations, and cross-snapshot continuity analysis.

Rejected for now: durable AST-node identities, universal symbols, and a monolithic graph/store.

Superseded or refined findings: ADR-0002 records current subject and graph-view semantics.

Open questions: appropriate semantic granularity for future disclosure units.

Revisit triggers: a language-analysis consumer requiring another durable subject family.

Reconciliation basis: ADR-0002; taxonomy; current Python declaration slice.

## A. Executive conclusion

**Recommended architecture:** Treat code **structures** (files, classes, functions/methods, tests, configuration sections, documentation sections, etc.) as the primary *repository subjects* with snapshot-local identities.  Content locations (file paths + source ranges) serve as *resource occurrences* pointing to those subjects.  All higher-level semantics (call graphs, type hierarchies, imports, data/control flow, documentation links, etc.) are **derived knowledge** computed over these subjects.  Do **not** bake ephemeral retrieval chunks (e.g. fixed token windows) into the core model; instead build them dynamically over subjects and derived edges.  Maintain strict snapshot determinism (no implicit cross-commit symbol IDs) while allowing *derived continuity clues* (e.g. rename inference) to link subjects across snapshots when needed.

- **Repository subjects:** file/module, package/directory (if applicable), class/struct, function/method (including test functions), and analogous top-level entities in non-code artifacts (e.g. a Markdown section or a configuration item).  Each subject is a uniquely identified element *within a snapshot* (e.g. “file *src/runtime.py* at commit X, class `Runtime`, method `send`” with explicit location).
- **Occurrences:** Individual **source occurrences** (references, call sites, literal spans, docstring, import statements, etc.) are *locations*, not first-class subjects.  They link to a subject but do not themselves get permanent identity beyond the snapshot.
- **Symbols:** Abstract symbols (e.g. “the symbol `Runtime.send`”) are *derived*: they can be computed (from names and scopes) and indexed, but we do not assign them standalone identities in the core data.
- **DerivedKnowledge:** Relationships (calls, subclassing, variable definitions/references, import-dependencies, test-to-code links, doc-to-code links, etc.) and semantic regions (e.g. a “failure-handling” block) are computed *on top of* the subject graph.  They must preserve provenance and invalidation semantics, but are not persistent *subjects*.
- **Retrieval units:** The system should distinguish between *index units* (subjects and their relations) and *retrieval chunks*. Retrieval may assemble multi-subject neighborhoods (e.g. a function plus its callers, or a class plus related tests) as context for queries.  No fixed “universal chunk” abstraction at indexing time – chunks are produced per-query from the subject graph.

This architecture aligns with state-of-the-art tools. For example, source-indexing systems like Sourcegraph’s SCIP treat **files and symbol declarations** as indexed units and record edges (definitions, references, imports) among them, while languages-compilers (e.g. Kythe) also separate *semantic nodes* (with stable IDs) from *anchor nodes* (text occurrences) with edges like “ref” and “defines”.  Static analysis graph tools (e.g. Code Property Graphs/Joern) make AST constructs into graph nodes with types and properties.  In contrast, retrieval-focused research (GraphCoder, RepoGraph, CocoIndex, etc.) demonstrates that *chunks should respect syntax*: functions, classes, and logical blocks make better chunks than arbitrary text windows.

In summary: **Snapshot subjects** = code entities (file, class, function, etc.) and analogous artifacts, each with explicit snapshot-bound identity. **Derived knowledge** = all graph edges, symbol tables, and semantic annotations computed from those entities. **Retrieval/disclosure** operations should build contexts *from* that core data but not assume any persistent “chunk” objects.

## B. Evidence from production systems

We compare how major production code-intelligence systems define identities and structures:

| **System**           | **Primary identities**             | **Indexed locations**    | **First-class relations**                   | **Derived vs foundational**             | **Granularity**         | **Retrieval units**         |
|----------------------|-----------------------------------|--------------------------|---------------------------------------------|----------------------------------------|-------------------------|----------------------------|
| **Sourcegraph/LSIF/SCIP** | **Files (documents):** by path/URI; **Symbols (via monikers or SCIP strings):** function/class/variable names; **Occurrences (ranges)** represent uses of symbols. No built-in concept of *symbol database* beyond linking names. | **Ranges:** text spans (for definitions, refs, hovers, etc.). Also *documents* (file-level). | Edges for “definition-of”, “reference-to”, “hover”, “completion”, **moniker edges** linking symbols across packages/projects. | Foundation: file/docs and ranges; symbols are just string IDs or exported names, not core objects. Semantic facts (like overrides, type info) are **derived** by indexers. | File-level, then named symbols within (functions, classes, etc. appear as “ranges with attached symbol info”). | Retrieval: file/AST-range; contexts built per query (e.g. “go to definition” gathers def+refs). |
| **Compiler/LSP (e.g. Clang, Roslyn, TypeScript)** | **Declarations & Definitions:** e.g. class/func definitions (each an AST node and a semantic symbol). **Symbols:** logical identifiers (often opaque IDs internally). **AST nodes:** ephemeral. | Source positions for definitions/references. The server holds AST and symbol tables in memory, not persisted globally. | e.g. `textDocument/definition`, `textDocument/references`, `textDocument/hover`. | Symbol tables (mapping names to decls) are “derived” from AST but form core model. AST nodes are analysis artifacts. | Granularity: file → module → classes → methods → variables. | Query-driven: e.g. an LSP “definition” request traverses AST/symbol links. No separate retrieval index. |
| **CodeQL (GitHub CodeQL)** | **Symbols/Entities:** represents *declarations* of classes, methods, variables as queryable entities. **AST nodes:** internal IR for queries, not persisted externally. | CodeQL builds a *QL database* per repo snapshot, keyed by location (path+byte range). | Relations like inherits, calls, dataflow are first-class in queries. | AST and edges are stored in DB; semantic relations (e.g. control/data flow) are precomputed by analysis. | Language-specific AST granularity (one graph per file, with nodes for functions, calls, etc.) | Retrieval/query: user writes QL queries over the DB. The DB isn’t exposed to the user except via queries. |
| **Joern (CPG)** | **Nodes:** code constructs (method, variable, type, call, literal, etc.) get unique node IDs. Types of nodes are predefined (METHOD, CALL, IDENTIFIER, etc.). | Every AST node, block, literal etc. appears as a node; source locations are attributes. | Edges: AST-child (“AST”), “CONTAINS”, CFG edges (“FLOWS_TO”), PDG edges (“DFG”), call edges (“CALL”), etc. | CPG merges syntactic and semantic graphs; nodes represent code elements (so partly “foundational”). E.g. “identifier name” nodes link to “declaration” nodes via “REF” edges (symbol resolution is in graph). | Very fine-grained: full AST/CFG/PDG, often at statement/expression level. | Queries: pattern search over the graph (e.g. find all call-graph paths). Retrieval is query-based on the CPG graph. |
| **Kythe** | **VNames:** Each symbol/definition is given a unique VName (like URI) encoding language, path, signature, etc. **Anchors:** text spans (positions) have IDs. | Text anchors (file spans) and file nodes.   | Edges for “defines/binding”, “ref” (uses), “child-of” (AST), “inherits”, cross-language indexing. | VNames (symbols) are foundational IDs; anchors connect code to symbols via edges (these edges are *derived* by the indexer). | Language-agnostic schema, but typical node kinds: file, namespace, type, function, variable, anchor. | Retrieval via Kythe query API (e.g. find `ref` edges). Kythe’s focus is on cross-language linking rather than natural-language search. |
| **CocoIndex (semantic search)** | Uses **AST** (via Tree-sitter) to identify syntax units (functions, classes, blocks) as chunk boundaries. It implicitly treats those as “subjects” when chunking. | Chunks (subsets of AST) limited to ~1000 tokens. Embeddings are computed per-chunk. | No explicit edges stored; retrieval via embedding similarity. | Derived: embeddings are semantic features of chunks. Structural parse yields chunks. | Granularity: syntax-level (functions, class bodies, blocks). | Retrieval: semantic search (via vector DB) of these chunks. Chunks are AST-aligned, not fixed-size windows. |
| **Meta/Glean (code index)** | **Language-specific facts:** Glean stores arbitrary facts per language (e.g. function-declaration(name,loc), inherits, etc.). It defines schema predicates per language. | Facts keyed by content (repo path + version + offsets).  | Relations like “FunctionDeclaration(name, loc, …)”, “CalledBy(caller,callee)”, etc.  | The schema and facts are **language-specific** but accessible via a unified logic query. Low-level syntax trees are not directly queried; instead high-level facts (derived from parser/analyzer) are stored. | Predicate-level granularity: e.g. one fact per function, per class, per call, etc. | Query via *Angle* logic language. Focus is code navigation and analytics; not retrieval by free-text. |
| **OpenAI/Anthropic Agent tooling** | (Undocumented) Likely indexes files and builds simple symbol tables. No public details. | Unclear. Most likely treat file+line contexts as retrieval units. | (Proprietary) | (No public architecture available.) | (No formal docs; likely similar to LSIF/AST extraction) | Retrieval: likely RAG over file chunks. |

**Key takeaways:**
- *Subjects vs. occurrences:* Almost all systems distinguish a **code entity** (file, class, function, symbol) from a text-range occurrence. For example, Kythe and LSIF both use named entities (VNames or “monikers”) for symbols/definitions and separate “anchor” nodes or ranges for source occurrences. Joern’s CPG similarly has distinct nodes for declarations vs. references.
- *Declared relationships:* Production tools make relationships (calls, uses, inheritance, etc.) first-class but store them as derived edges. LSIF explicitly represents definitions and references via edges, but it does **not** encode, say, override semantics – that remains derived by analyzers.
- *Granularity:* File and symbol (class/function) are common indexing units. Systems like Sourcegraph/SCIP index definitions at symbol granularity (functions, classes, variables). Others (Joern, CPG) go finer to statements/expressions, but at great storage cost.
- *Retrieval vs. index unit:* Most systems **separate** indexing units from retrieval assembly. For example, Sourcegraph stores symbol-level and call-edge data, but retrieval (“go to definition”) composes definitions and references at query time. CocoIndex stores function/block chunks for embedding search, not arbitrary fixed windows. Recent agent frameworks (RepoGraph, GraphCoder) even build *context graphs* on-the-fly from the static index (e.g. RepoGraph constructs an ego-graph of lines at retrieval time).

## C. Evidence from research systems

Contemporary research reinforces these patterns:

- **RepoGraph (Da et al. 2024)** uses a *line-level graph*: each node = a source line, with edges for “definition” and “reference” dependencies. Its aim is to give LLMs fine-grained context, but it still bases nodes on static code (lines) and builds sub-graphs per query.
- **GraphCoder (Zhang et al. 2024)** constructs a *code-context graph (CCG)* at statement granularity: nodes are statements, with control-flow and data-flow edges between them. This shows one can use statements as retrieval units, but even here the *index* (the CCG) is derived from static analysis (not arbitrary token chunks).
- **Agentless/Baselines:** Other works (e.g. Aider, RepoUnderstander) emphasize module/class-level indexing and dynamic RAG. For instance, Aider employs graph algorithms on a file-level call/import graph during retrieval. These all presuppose a static graph of code entities.
- **Semantic search tools:** Modern embedding-based search (CocoIndex, others) prefer **syntax-aligned chunks**. CocoIndex explicitly argues against token-based splitting: it uses Tree-sitter to split only on syntactic boundaries (functions, classes, blocks), preserving semantics in each chunk. This suggests that *intrinsic code structures* are better bases for retrieval, not arbitrary “chunks.”

**No research supports** treating *all* code as undifferentiated chunks. On the contrary, studies show hierarchical context (file→class→method→statements) improves relevance. For example, RepoGraph’s line graph outperformed flat file retrieval (SWE-bench tasks) by giving contextual edges. GraphCoder showed statement-level structure outperforms purely token-based retrieval.

## D. Lessons from compilers and static analysis

Compiler architectures and code analysis tools highlight core distinctions:

- **AST vs. Symbols:** Compilers typically parse code into an AST, then build a **symbol table** or semantic model. The AST nodes themselves (often ephemeral) do not usually become persistent identities; rather, *symbols* (declarations of types, functions, variables) are given stable identifiers in the semantic model. For example, a C compiler uses an AST to find all function declarations, each of which is a single entry in the symbol table (often with a unique ID) – the AST node is not used directly beyond parsing. Similarly, many language servers (e.g. Roslyn for C#) distinguish between `SyntaxNode` (AST) and `Symbol` (semantic entity).
- **Declaration vs. Definition vs. Reference:** Mature systems clearly separate these. A *declaration*/definition (e.g. “function foo()”) is one entity; *references* (calls to `foo`) link to it. In Kythe, a variable’s VName (unique identifier) is attached to its definition, and separate *anchor* nodes mark each occurrence of its name – edges labeled `ref` or `defines/binding` connect them. In compilers, symbols reference their declarations via pointers, and references in AST point to symbol table entries.
- **Scopes and Continuity:** Compilers explicitly manage scopes (namespaces, modules) so that symbols are unique within context. However, *across snapshots*, compilers generally do not maintain continuity. When code moves or is renamed, compilers see it as entirely new symbols. Some tools (e.g. diff/rename detectors) post-process semantic graphs to guess continuity, but this is derived. Similarly, LSIF explicitly *does not* try to assign persistent symbol IDs across arbitrary refactorings – any rename would break the identity unless monikers are used, which are generated by indexers as *derived* links.
- **Control/data flow and other analyses:** Rich code intelligence (CodeQL, Joern) computes graphs like CFG and PDG. These graphs are **derived knowledge**: they are not primary subjects but computed from the code’s AST and symbol info. For example, CodeQL stores `CFG` edges between statements in its DB, but the subjects are the statements themselves (tied to a function entity). Data-flow edges in Joern’s CPG (the DFG/PDG layers) similarly connect nodes already in the graph.
- **Index vs. Query granularity:** Many static analysis tools build coarse-grained indices (tables of symbols, references). For instance, LSIF indexers emit ranges and link them to definitions via edges, but do not precompute “relevant code chunks.” In contrast, query engines (language servers, CodeQL queries) can combine relevant parts on demand.

**Applicability:** All these systems treat named code entities (types, functions, variables, constants) as distinct semantic units with identity. They *do not* give standalone identity to generic AST nodes, expressions, or arbitrary text spans. That suggests our repository-intelligence should likewise make functions, classes, tests, and similar constructs first-class, while treating lower-level syntax elements as part of those constructs’ internal details.

## E. Recommended identity model

Based on the above evidence and the need for deterministic, snapshot-bound intelligence, we propose the following conceptual layers:

- **Repository:** Identified by a canonical origin (e.g. remote URL or unique project ID) distinct from filesystem path or working copy.
- **RepositorySnapshot:** An immutable snapshot at a particular state (e.g. a specific Git commit or configuration-determined state). All intelligence is tied to a specific snapshot ID.
- **Resource (File/Document):** A file or resource in the repo (identified by path and language). Each snapshot has Resource occurrences, each containing file content. Track *content identity* (e.g. hash) separately from the path (for cache reuse of unchanged content).
- **ResourceOccurrence:** A particular file *instance* in the snapshot (path + content). This provides context for subjects and is used for retrieval (file-level access).
- **Structural Subject (CodeEntity):** **Major code elements** parsed from the resource, including:
  - Packages/directories (if the language has explicit modules/packages).
  - Classes or similar type declarations.
  - Functions, methods, constructors.
  - (In Python: modules, classes, functions, async coroutines, etc.)
  - Tests (e.g. test function or class, if tests are separate units).
  - **Non-code artifacts:** For documentation or config files, analogous sections. For Markdown, each heading (H1/H2) could be a subject; for YAML/JSON, each top-level key or section might be a subject; etc.
Each such subject is given a unique ID *within the snapshot* (e.g. `<repo>@<commit>:<file>:<range>`). Subjects are the core nodes of the repository’s static structure.
- **Symbol (DerivedIdentity):** A logical symbol (name/namespace) can be inferred for each subject (e.g. the fully-qualified name of a method). We do **not** treat symbols as primitive identities, but we do store symbol strings on subjects and use them to link references.
- **SourceOccurrence (Usage):** Any reference to a subject in code (identifier usage, call site, import statement, literal span, etc.) is a source occurrence: it has a location (resource + range) and points to the corresponding subject ID (or possibly multiple, in case of overloaded symbols). Occurrences are *locations*, not new subjects.
- **DerivedKnowledge:** Edges and annotations computed from subjects/occurrences, e.g.:
  - **Symbol table:** map from names in scope to subject IDs.
  - **Call graph:** edge from caller-subject to callee-subject.
  - **Type inheritance/implements:** edges between type subjects.
  - **Data-flow/definitions:** e.g. assignment defines/uses variables; can be stored as subject-variable edges or separate facts.
  - **Import/dependency graph:** edges for module imports or library dependencies.
  - **Test relationships:** e.g. “test X covers function Y” (inferred from names or code analysis).
  - **Documentation links:** e.g. “doc section refers to class Z.”
  - **Change provenance:** links to indicate same subject in history (derived), or absence of changes.
All DerivedKnowledge must record its provenance (source subject or code fragment) and invalidation rules. They are *computed atop* the subject graph.

- **Graph Views:** The system should allow multiple graph projections. For instance, a **structure graph** (packages → files → classes → methods), a **call/reference graph**, a **control-flow graph (CFG)**, a **data-flow graph (DFG)**, a **documentation graph**, etc. Each graph’s nodes may be subjects or sub-parts of subjects (e.g. statements in a CFG view). These graphs can reuse the same subject identities for nodes where applicable. Relationships (edges) in these graphs are derived and typed. We do **not** mandate a single universal graph DB; implementation can use multiple indices or databases per view if desired.

- **Snapshot-Local vs. Cross-Snapshot:** All subject IDs above are inherently *snapshot-scoped*. For example, `Runtime.send` at commit S1 and at S2 (even if code moved files) get different IDs. We only derive continuity (that “these are likely the same logical method”) via diff/provenance metadata or rename tracking as *derived knowledge*. This preserves determinism and caching. If future evidence suggests linking identities across snapshots yields huge benefits, it should be layered on top, not baked in.

**Names & Responsibilities:**

- We suggest **“CodeEntity”** or **“Subject”** for the major units (class, method, etc.).
- **“ResourceOccurrence”** or simply **“Resource”** can represent a file in a snapshot.
- **“Occurrence”** for references/call sites.
- **AST nodes** remain transient: they help compute subjects and relationships, but are not first-class subjects.

## F. Recommended structural decomposition

Structural units to index as first-class subjects should be those that are stable, meaningful, and commonly needed for queries:

- **Repository:** as explained.
- **Package/Module (directory):** Treat a directory with an `__init__.py` or similar as a subject representing the Python package namespace. This supports queries like “what modules exist” or “imports graph”.
- **File/Module:** The entire file itself can be a subject (needed for file-level metadata, top-level symbols). Some systems treat the file as a container for others, but making it addressable is useful (e.g. linking a test file to code). If your model already uses the resource occurrence for the file, you can either unify them or have a distinct “file subject” for attaching cross-file relations.
- **Class (Type) declarations:** Each class or analogous type (struct, interface, enum, record) is a subject. Classes often define namespaces and fields/methods. Identity stability is moderate (class renames usually indicate different entity, but some tools may derive continuity by diff).
- **Function/Method definitions:** Each `def` or `async def` is a subject. In Python, nested functions (“function within a function”) are also subjects. Methods (functions under classes) are separate subjects (often qualified by class). Identity is generally clear (name + enclosing class/module). For free functions, fully qualified by module.
- **Tests:** If tests are functions or methods, they are already covered. If a repository uses conventions (e.g. `test_*.py` or `TestCase` classes), you may tag or index them specially. Possibly treat the test suite as separate subjects linking to code.
- **Constants, Imports, Globals:** We suggest *not* making every variable or import a subject on its own. Instead, treat module-level constants as part of the file’s subject or as named symbols derivable from the file. Imports are occurrences (file-level dependency edges) rather than separate subjects.
- **Configuration items:** E.g. a setting in a YAML or JSON file (like a Docker command or config key). These can be subjects if they correspond to behavior (e.g. a service definition in a manifest). Each key or entry path can be an identified subject (e.g. resource:path in YAML). But do this only if needed (e.g. if agents query configuration meaningfully). Unstructured data (like general text in markdown) may not need per-line subjects, but headings or section markers can.
- **Documentation sections:** In Markdown or reStructuredText, you might index headings as subjects. For example, a `## Section` in a `.md` file can have an ID and link to related code (perhaps via natural language analysis). At minimum, the file is a subject; secondarily, headings as subjects aids search (“where is concept X documented?”).

**Not-index (or low priority):** Individual statements (unless needed for data/control flow graph nodes), expressions, or arbitrary code blocks. These can be referenced within their enclosing function/class but need not be top-level subjects. Also, variables and parameters are represented as symbols on subjects (function or class), not as separate subjects.

**Rationale:** This mix balances usefulness and stability. Functions and classes are precisely what developers refer to (“where is method X?”). Tests often need to be found by naming conventions. Lower-level constructs (loops, assignments) rarely serve as independent topics. Indexing every AST node would explode storage and invalidation costs for little benefit.

## G. Recommended semantic decomposition

High-level semantic constructs (like **failure-handling blocks, lifecycle phases, architectural responsibilities**) are typically *derived knowledge*, not intrinsic. In practice:

- **Deterministic semantics:** Relations like call graph, type hierarchy, module import graph, and data-flow facts should be computed from the code and stored. These are repeatable given the snapshot. They **become part of DerivedKnowledge**. E.g. “method A calls B” is derived from AST/cfg analysis, “module X imports Y” from parse, etc. Tools like CPG and CodeQL do exactly this.
- **Heuristic/semantic regions:** Concepts such as “the region of code that handles timeouts” or “authorization boundary” are not purely mechanical. They may be extracted via rules, tests, or even ML. We recommend treating these as *derivable entities* at query-time or as future **extensions**, not as core subjects. For example, one could index *features* or *tags* attached to subjects (e.g. mark “send() has retry logic”), but only as DerivedKnowledge that can be invalidated or updated easily.
- **LLM-derived metadata:** Comments like “TODO: optimize” or a code summarization are clearly not core. They should be stored separately if at all (and likely fed into retrieval, not core index).
- **Purpose-relative chunks:** If an agent needs a concept like “timeout handling flow,” this should be constructed on-the-fly by traversing calls/CFG (or by query/AI search), not pre-indexed.

Empirical evidence suggests: **File > class > method** granularity works best for general search, and semantic clusters are query-specific. For example, retrieval results in CocoIndex are functions or logical code blocks. RepoGraph and GraphCoder focus on dependencies between code entities to capture semantics. They do not predefine things like “feature slice” – instead they let algorithms find related code.

In summary, keep the core semantic graph *strictly structural* (calls, refs, types, data-flow, test-mappings). Reserve more abstract concepts for the **info-retrieval layer** (where an agent or query can infer, say, a “failure path” by linking exception handling calls).

## H. Retrieval-unit separation

Our recommendation strongly separates *index units* from *retrieval units*. All evidence from modern systems supports this:

- **Index units = structural subjects:** The index stores code entities (files, classes, methods) and fixed relationships. For example, Sourcegraph’s LSIF index has symbols and range locations, Joern’s CPG has AST nodes, GraphQL queries.
- **Retrieval chunks = dynamic compositions:** A retrieval may combine multiple subjects or parts of them. RepoGraph retrieval builds subgraphs around keywords. GraphCoder retrieves statement subgraphs near a target. Even traditional IDE “Go to Definition” effectively returns *ranges* from potentially several files.

None of the strong systems conflate these: they all have a static index and then assemble contexts as needed. The proposed architecture follows suit: *subjects* form the index; *ContextDisclosure units* (chains of code slices from one or more subjects) are assembled later in the pipeline (§1 Context disclosure).

For example, answering “Where is the failure evidence recorded?” might retrieve one piece of code (the call to `Logger.recordFailure()`) but also include surrounding lines from `Runtime.send` and possibly tests that trigger it. These are not separate pre-indexed objects but a runtime combination of the “method” subject and related occurrences.

In contrast, a “chunk” abstraction at index time (like arbitrary 512-token splits) would ignore code boundaries and relationships, leading to context loss.

## I. Graph architecture implications

We reject a monolithic universal graph. Instead, use **multiple view-specific graphs**:

1. **Nodes:** Use appropriate node types per graph:
   - *Containment/Namespace graph:* Nodes = repository/dirs/files/classes/functions. Edges = “contains” or “module-imports”.
   - *Call graph:* Nodes = function/method subjects, edges = calls. (Nodes could optionally include file+line for precise edges but usually subject-level is enough.)
   - *Type/inheritance graph:* Nodes = classes/types, edges = “inherits/implements”.
   - *Reference graph:* Nodes = symbol declarations (or resources), edges = references (possibly labeling read/write).
   - *Control-flow graphs (per method):* Nodes = statements/instructions (sub-elements of a method), edges = “next” or “branch”.
   - *Data-flow graphs (within methods or whole program):* Nodes = variable definitions/uses, edges = “data flow”.
   - *Doc/code graph:* Nodes = documentation sections or code subjects; edges = “documents/related”.
   - *Version/change graph:* Nodes = snapshot IDs or commit objects; edges = “parent-of” and possibly links to subjects introduced/removed.

   Each graph’s nodes can mostly be drawn from *the same pool of subjects*, except CFG/DFG graphs introduce statement-level nodes as needed. It's acceptable for different graphs to have different granularity nodes.

2. **Node identity consistency:** Where possible, use the same subject ID in multiple graphs (e.g. the class `Runtime` node is the same in the containment graph and the inheritance graph). For data/control-flow, new node IDs can be scoped under a method subject.
3. **Edges connecting derived values:** Edges themselves may carry derived information (e.g. a “ref” edge has provenance of which variable or file made the reference). But typically we treat edges as relations between subject IDs or occurrence IDs.
4. **Shared substrate:** Ideally, store all subject and relationship facts in a unified data store or interoperable format. But technically, multiple specialized indices (e.g. one call-index DB, one dependency-index DB) can interoperate via joins or cross-indices. The architecture should support querying across views (e.g. find all tests related to callers of X). This can be done by either a multi-view query engine or a central graph query layer.
5. **Hierarchy:** The fundamental hierarchy (repo → package → file → class → method) should be explicit (either via stored “contains” edges or by the very identity naming). Evidence from LSP/LSIF and CPG indicates storing “contains” edges is useful. In Kythe/CocoIndex/Glean-like schemas, this containment is either implicit or explicitly queryable. We should **include containment relationships** as primary DerivedKnowledge or part of subject attributes (e.g. each subject stores its parent).

In summary, graph nodes should correspond to the chosen *subjects* (plus any finer-grained nodes needed for data/control-flow), and we should allow **multiple graph layers**. This fits e.g. CodeQL or Glean where one can query across multiple relations (inheritance, call, lexical scope) simultaneously using a logic query language.

## J. Non-code artifacts

Repository intelligence must generalize beyond Python code. Our model should treat all content as “resources” with types:

- **Markdown/Docs:** Treat each Markdown file as a resource, and consider each heading as a subject (with identity like `<file>:<heading>`). This lets you ask “where is the architecture described?” by keyword. Also indexing links in docs as edges to code subjects can connect documentation to implementation.
- **Configuration (YAML, JSON, TOML):** Treat key-paths as subjects. For instance, in `config.yaml`, the entry `server.port` is a subject under the file. This allows queries like “which services expose port 80?”.  If a config has a known schema (e.g. Kubernetes manifest), you can further attach semantics (this is a Service, this is a Deployment).
- **Build/CI scripts:** For example, each step in a CI pipeline could be a subject (“build”, “test”). At minimum, index each file. If needed, parse common syntaxes (GitHub Actions YAML) to extract jobs as subjects.
- **ADRs/Prose:** Treat sections of Architecture Decision Records as subjects. A subject could be one ADR (file) and each section within it. Link these to code if references are found.
- **Manifests/Schemas:** e.g. OpenAPI, JSON schema files: each definition or endpoint can be a subject.
- **Binary assets:** Generally omit content, but the file presence is a resource subject so queries can at least locate them.

We recommend a **typed occurrence model**: every file is a “resource occurrence”, then each language or format has its own notion of structural subjects. A unified base (file path + content) underlies all, but parsing/AST is format-specific. For non-code types, the intelligence may be simpler (e.g. key existence vs code analysis), but the framework should accommodate them as first-class if needed.

Evidence: Indexers like CocoIndex include Markdown and TOML by treating them with separate parsers. Kythe’s schema has *Comment* and *Doc* nodes. Glean’s schema allows storing arbitrary “facts” about any text. We should likewise allow extending subject types per artifact.

## K. Incremental-maintenance implications

A fine-grained identity model enables efficient updates:

- **Locality of change:** If one line in a function changes, ideally only that function’s subject (and its contents) needs re-analysis, not the entire file or repo. By assigning identity at function/class level, we can detect that e.g. only `Runtime.send` changed, leaving `Runtime` class and other methods unchanged. Similarly, if a new test is added, only the test subject (and its graph edges) is new.
- **Stable content IDs:** Recording a content hash for each resource (file) or subject’s body lets us skip reprocessing if unchanged. For instance, if `runtime.py` content ID is unchanged, reuse its cached subjects and derived data. Many systems (LSIF, Glean) use file checksums to avoid re-indexing.
- **Precise invalidation:** Derived data is tied to subjects/occurrences. If a method changes, only relationships involving that method need recomputation (calls from/to it, CFG/DFG in it). If a config setting changes, only queries depending on that setting need re-evaluation. Layered storage (as in Glean) can isolate new facts from old.
- **Snapshot layering:** Maintaining the ability to query older snapshots means storing deltas or layering. As Meta’s Glean illustrates, stackable immutable DB layers allow viewing all versions efficiently. Our subject IDs can implicitly include snapshot ID, so each layer adds or hides facts without destructive updates.
- **Fan-out concerns:** Some changes have ripple effects. E.g. modifying a widely-used header or base class will force re-indexing of many dependent files (C++). Our model doesn’t prevent this, but by isolating identities we at least only recompute necessary derived edges. Storing separate dependency indexes (like import graph) helps quickly identify affected subjects.

In short, the identity model should support: (1) recognizing when a subject’s source hasn’t changed, (2) granular invalidation of only related derived knowledge, and (3) layering of snapshot versions. We avoid coarse blobbing of subjects (no “whole repo subject”) because that would invalidate everything for small edits.

## L. Evaluation of the candidate architecture

The proposed layered model (Repository → Snapshot → ResourceOccurrence → *subjects* → DerivedKnowledge → retrieval) mostly aligns with these findings, but we refine some terms:

- **“RepositorySubject” vs “SemanticOccurrence”:** We recommend a single concept of *Subject* for the primary semantic unit (class, function, etc.). The term “SemanticOccurrence” (as in candidate) seems confusing: occurrences are best called simply “Reference” or “Usage”, and they link to a subject. So we prefer *Subject* (with identity) and *Occurrence/Usage* (location only).
- **Symbols:** The candidate treats “symbols” as potentially DerivedKnowledge. We agree: do not make symbols separate identities. For example, CodeQL doesn’t expose a “Symbol” object; it just queries declarations and references. LSIF explicitly has *no symbol database*.
- **Functions as subjects or derived:** We declare each function/method a subject. Some indexing approaches (e.g. tokenize-based search) might not, but evidence (CocoIndex, GraphCoder) shows functions are natural boundaries.
- **AST nodes identity:** No – AST nodes should not be first-class. Use them only during analysis. The CPG and Kythe examples treat statements/blocks as nodes in derived graphs, but even there they represent them within a larger subject (function). We do not assign a durable ID to every parse node.
- **Graph nodes vs knowledge:** Graph nodes *should* correspond to subjects (or explicit anchors). In control/data-flow, nodes could be statements, but those are inner details of the function subject. We can allow graph nodes that are not subjects (e.g. statement nodes in CFG), since projects like GraphCoder do, but they are derived and local to that subject’s context.
- **Hierarchy:** The hierarchy is better stored as derived edges (“contains”). We shouldn’t hard-code a tree beyond that. That allows e.g. querying different path shapes (packages vs bare files) uniformly.
- **Cleanup:** The candidate’s arrow from DerivedKnowledge to symbols/relationships/graphs/semantic regions is good, but clarify: *symbols* (in the sense of symbol table entries) belong to DerivedKnowledge, as do graph edges. Also, *semantic regions* belong in DerivedKnowledge if defined (though likely future work).

Thus, the candidate is largely on track; we’ve renamed a few abstractions for clarity and emphasized that *subjects* are the identity units, with all else derived.

## M. Concrete recommendation for **devtools**

**Conceptual Entities:**
- **Repository:** Immutable ID (e.g. URL).
- **RepositorySnapshot:** Immutable commit or build state ID.
- **Resource (file/module):** Identified by repo+snapshot+path, with content-hash.
- **CodeEntity (Subject):** Identified by repo+snapshot + “path:range” plus an internal unique ID. Types: *Module/Package, Class/Type, Function/Method, TestCase, ConfigEntry, DocSection*. These get attributes (name, signature, docstring, qualifiers).
- **Occurrence:** A record of a source-range in a resource that refers to a subject. No stable ID beyond (snapshot, file, range); considered transient.
- **AST Nodes:** Used internally but not stored as IDs.
- **Symbol name:** Stored as attribute on Subject.
- **DerivedKnowledge:** Call edges (func→func), “defines” edges (Subject→Occurrence), reference edges (Occurrence→Subject), inheritance edges (Type→Type), data/control-flow edges (Statement-level, in a per-method sub-graph), import edges (Module→Module), test-coverage edges (Test→Subject). Also, graph views are labeled (CFG edges, dependency edges, etc.).
- **Graph Views:** Maintain separate indices or query layers for: *containment graph* (packages/files/subjects), *call/reference graph*, *inheritance graph*, *CFG per method*, *DFG per method*, *documentation graph*, etc. These reuse subject IDs as node IDs except where deeper granularity is needed.
- **Retrieval Units:** No permanent “Chunk” object. Instead, support query routines that can gather: e.g. a set of subjects plus relevant occurrences (maybe limited by number of lines or by dependency radius). For disclosure, allow selection of “source snippet” around a subject or an interconnected subgraph.

**What devtools core should implement now:**
- Data model for Repository, Snapshot, Resource (with content ID), Subject (with typed entity).
- Parsers to identify structural subjects in Python and major other repo artifacts.
- Mechanism to record Occurrences (at least definitions & references) and derive a symbol table.
- Derive basic graphs (call graph, import graph, maybe name-binding reference graph) and store them.
- Keep provenance: e.g. each edge is “derived from subject X’s AST, on lines Y–Z”.
- API to query: e.g. “list all definitions of symbol X”, “list callers of function Y”, “find subjects by name/annotation”.

**Cross-snapshot:** For now, treat each snapshot independently. If desired, compute a simple diff mapping for continuity, but *do not* assign a stable cross-snapshot ID.

This layered architecture ensures:
- **Correctness/Reproducibility:** All knowledge is snapshot-derived, no hidden global state.
- **Incremental maintenance:** Fine-grained subjects mean minimal re-indexing on small edits (cache by subject).
- **Multiple graph views:** Supported by our DerivedKnowledge layer.
- **Extensibility:** New subject types or graphs (non-code artifacts, ML-based annotations) can be added as separate derived layers without reworking core.

## N. What must be decided now

Before implementation, the team must settle on:

- **Subject granularity:** Confirm which code elements get *IDs*. We recommend at minimum: file, class, function. Decide on nested functions and test identification.
- **Occurrence vs subject naming:** Choose terminology (e.g. **CodeEntity** vs **Occurrence**). How to unify doc/config subjects with code subjects.
- **Content identity scheme:** e.g. use content-hash for files (impact incremental caching).
- **Symbol handling:** Whether to index fully-qualified names now, or leave as derived only. Probably store FQN for each subject.
- **Core graph relationships:** Which edges to compute immediately (calls, imports, definitions, inheritance). These are essential.
- **Snapshot binding:** Mechanism for versioned data. Possibly a simple stack of tables (like Glean) or per-snapshot DB.
- **Persistence model:** Key-value store vs graph DB vs SQL vs layered DB (like Glean’s approach). This affects how identities are stored.

## O. What should remain unresolved

These can evolve through experimentation:

- **Coarse vs fine dropouts:** (e.g. should blocks or statements be half-identified?)  Design can start without them and add later if needed.
- **Learned/LLM-driven semantics:** How to integrate AI-derived tags (e.g. function summaries, semantic labels). This can be added as annotations on subjects, not core identity.
- **Chunking strategy:** Perfecting retrieval chunk boundaries is part of retrieval/disclosure, not core. Let our core use subjects; experiment with chunk assembly in retrieval components.
- **Cross-repo linking:** If building a multi-repo codebase tool, decide later how to unify symbols across repos. Initially, focus on single-repo.
- **Incremental strategy details:** The exact incremental diff algorithm (e.g. diffing ASTs vs text) can be designed later. The identity model should just make it possible.

## P. Risks and failure modes

Be aware of pitfalls:

- **Over-indexing:** If too many units (e.g. indexing every statement or expression), the system will be slow and memory-hungry. Evidence shows diminishing returns beyond class/function granularity.
- **Under-indexing:** Conversely, if we treat very coarse units (e.g. file-only), we lose semantic precision. Agents then have no way to navigate into code. The balance in our plan (file→class→method) is supported by practice.
- **Symbol mis-identity:** If we naively use symbol names as IDs, code that is refactored will appear broken. We avoid this by not relying on name-based identity outside a snapshot.
- **Frozen structure:** If we assume a fixed hierarchy (say, always “module→class→method”) we might miss languages without those constructs. Our model is flexible but **must not** hardcode too rigid a tree if supporting multiple languages.
- **Performance blindspots:** Graph-heavy approaches (Joern/CPG) are very powerful but often too slow to update for large repos. We should test incremental update performance early.
- **Graph DB vs other store:** A graph database might seem natural, but it can be slower or overkill compared to indexed tables or logic queries (as Glean uses). We should not prematurely adopt a single store; allow modular storage.
- **AI reliance:** Designing core around current LLM-agent use (e.g. always retrieving “semantic regions”) may lead to complexities that our system doesn’t need if the agents change methods. The architecture must remain valid even if agents evolve.

## Q. Sources

- “LSIF: Language Server Index Format” (Bäumer, VSCode blog, 2019) – explains LSIF design: *no symbol semantics in LSIF*.
- SCIP protocol docs (Sourcegraph) – defines **Document**, **SymbolInformation**, **Occurrence** structures for indexing (sourcegraph.com & scip.dev).
- Sourcegraph architecture overview – describes use of LSIF/SCIP for *precise code intelligence*, uploading index packages.
- **Joern Code Property Graph** – node and edge types for AST, CFG, PDG (nodes represent methods, calls, variables; edges represent AST, CFG, data flow).
- **Kythe documentation** – outlines a language-agnostic graph model with semantic cross-references (definitions, usages), and the notion of anchor nodes linking text spans to VName-identified entities.
- **CocoIndex blog** (Dec 2025) – demonstrates *syntax-aware chunking* with Tree-sitter (splitting on functions/classes) to preserve semantic context.
- **RepoGraph paper** (arXiv 2024) – constructs a repository-level *line graph* (nodes = code lines, edges = definition/use dependencies) to support retrieval.
- **GraphCoder paper** (arXiv 2024) – constructs a *statement-level code context graph* (nodes = statements; edges = control/data dependencies) for retrieval.
- **Meta Glean blog** (Dec 2024) – describes an indexing platform with *incremental indexing* (O(changes) vs O(repo)), using layered immutable storage.

Each of these sources provides concrete insights into how identities and decompositions are handled in practice, guiding our architectural decisions. (Sources are cited inline above.)
