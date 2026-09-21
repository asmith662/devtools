# Repository Intelligence and Context System Architecture

## Disposition

Status: Partially reconciled

Canonical research subject: Repository intelligence and Context system architecture.

Related ADRs: ADR-0002; ADR-0003; ADR-0004.

Implemented evidence: bounded corpus, lexical retrieval, exact declaration retrieval, and source materialization.

Accepted: deterministic intelligence is distinct from model behavior and Context is purpose-relative.

Deferred: semantic/vector retrieval, change impact, progressive disclosure, and local-model performance claims.

Rejected for now: heavy vector stores, autonomous multi-agent orchestration, generic plugins/events, and self-learning production loops.

Superseded or refined findings: later ADRs and purpose-relative research define current semantic boundaries.

Open questions: empirical value and ownership of future retrieval strategies.

Revisit triggers: bounded experiments with independently useful evidence.

Reconciliation basis: ADR-0002 through ADR-0004; roadmap; B-0002.

## A. Executive conclusion

The evidence points to a **hybrid architecture** that front-loads deterministic code analysis and uses precise retrieval before invoking the LLM. In practice, existing agents have started moving in this direction: e.g. Cursor and Aider *index the entire codebase* upfront rather than streaming files piecemeal through the model. Likewise, industry reports note that exact-match search (grep/BM25) often outperforms semantic vectors for code, and that making retrieval an interactive tool yields big savings. On the generation side, techniques like **prompt condensation** (OpenHands) and prompt trimming (LangChain) have already cut token usage by roughly 2×–65%.

**Proposed next steps (evidence-based):**
- **Deterministic repo intelligence:** Build and maintain a **repository index/graph** (file list, symbol table, import/call graph, tests/docs mapping) outside the LLM. For example, LocAgent explicitly parses the repo into a code graph, and GraphCoder leverages dependency graphs. This lets us answer “where is X defined?” or “which modules import Y?” without any LLM token cost.
- **Lexical/structural retrieval first:** Use exact-match search on identifiers, filenames, error strings, etc., with optional graph expansion. Industry experience (e.g. Anthropic’s Claude Code team) shows that “exact-match search beat semantic search” on code, and iterative search beats one-shot retrieval. We should prioritize grep/BM25 and structural neighbors, and only fall back to embeddings or model parsing when needed.
- **Budgeted context compilation:** Rank retrieved files/snippets by relevance and trim strictly to the available token budget. Remove overlaps and irrelevant parts so that the model sees only *dense, high-value content*. (Agent benchmarks use metrics like *budgeted context yield* to tune this.)
- **Progressive disclosure via tools:** Don’t dump a massive context at once. Start with a compact context packet and allow the model to issue *“give me more info”* tool calls for unresolved questions. Recent analyses emphasize making retrieval an explicit loop, which can halve token use without hurting accuracy.
- **Lean agent prompts:** Minimize all fixed prompt overhead. LangChain’s Deep Agents v0.7, for example, cut base prompt length by ~65% with no loss. This means providing tight tool schemas and stripping unnecessary boilerplate.

In summary: **Offload every fact you can** (file lists, symbols, dependencies, test mappings, ADRs, etc.) to a deterministic subsystem. Use precise, possibly multi-modal retrieval to gather only the *needed* context. Give the model *only the smallest, most relevant context* (with provenance) to solve the next step. This model-independent pipeline should dramatically cut Codex token usage while keeping correctness high.

# B. Current-state problem model

Currently, agents spend most of their token budget on **“finding and parsing code,”** not on generating solutions.  Analyses show that a typical coding task involves inspecting several files and thousands of lines. For example, the SWE-Explore benchmark found the “core” context of solved tasks averaged **4.3 files (~1,578 lines)**.  Concretely, tokens go into:

- **Exploration cost:** Using tools (e.g. `search`, `ls`, opening files) to discover *where* relevant info lives. Each search or directory listing often requires a model prompt or response.
- **Comprehension cost:** Feeding retrieved code into the model to understand it. Thousands of lines mean thousands of tokens.  (SWE-Explore reports about 1,500 lines of code per task.)
- **Historical/context cost:** Carrying forward all prior conversation history, tool responses, and decisions. Each turn adds prompts and replies that the model must reread or store.
- **Execution/feedback cost:** After editing code, reading tool outputs (diffs, compile messages, test failures) back into context. These often duplicate information the tools already have.
- **Coordination/overhead cost:** Tokens spent on planning or reflection (“What should I do next?” loops), which adds to context without producing new code. Note LangChain found most planning turns were unnecessary in practice.
- **Irrelevant-context cost:** Tokens consumed by unneeded or off-topic code. If the model fetches a broad file for a narrow query, it wastes tokens on the extra content.

Importantly, studies show *all* agents behave similarly when exploring the repo. For instance, SWE-Explore observed that different systems (Codex, Claude Code, OpenHands, etc.) reached nearly identical file coverage and efficiency profiles. In short, **every agent ends up rediscovering the same code context**, so all pay these costs. Our aim is to shift as much of this repeated work as possible out of the LLM and into fast offline analysis, while still maintaining high task success.

# C. State of the art

Several recent systems illustrate different approaches to feeding LLMs repository context:

- **Sourcegraph Cody:** Uses the Sourcegraph search API to fetch context from code. By querying filenames, symbols, and patterns, it can retrieve relevant snippets before asking the LLM. This effectively performs lexical search on indexed repos.
- **Cursor AI:** Indexes the *entire* codebase for context. The company touts that Cursor “indexes your entire codebase so that it can provide results with full context”, implying a local project-wide search engine.
- **Aider:** Builds a full “map of your entire codebase” to support tasks. Aider’s documentation specifically says it creates a project-wide index to enable large-context reasoning.
- **OpenHands (Ilya2023):** Introduces **context condensation**, an online summarization step to remove redundant chat history. They report **2× per-turn cost reduction** with similar task success by only summarizing when the context grows too large.
- **LangChain Deep Agents:** A modular agent framework. In v0.7, the LangChain team trimmed the base prompt (tool descriptions, system text) significantly, reporting about **65% fewer input tokens** on code tasks. They stress that prompt engineering can greatly cut token usage.
- **GraphCoder (ASE 2024):** An academic code-completion system that builds a *Code Context Graph (CCG)* combining control-flow and data dependencies. It performs a coarse-to-fine retrieval of snippets via this graph, improving exact-match and identifier-match accuracy while using *less time* than baseline retrieval.
- **LocAgent (ACL 2025):** Constructs a directed heterogeneous graph of the codebase (modules, functions, imports, etc.) and has the LLM traverse it for code localization tasks. It achieved comparable localization accuracy to state-of-art models with **~86% less inference cost**.
- **RepoCoder/Repoformer (EMNLP’23 / ICML’24):** Research on repository-level code completion. RepoCoder uses iterative retrieval+generation to utilize multi-file context. Repoformer extends this with *selective retrieval*: the model learns to decide *when not to retrieve*, yielding about **70% inference speedup** on completion tasks (i.e. skipping unnecessary lookups).
- **HyRACC (Forge 2025):** A hybrid RAG framework for code completion that *combines* lexical (BM25) and semantic (vector) indices. The authors report gains in accuracy and much faster CPU/GPU usage compared to baselines.

In summary, the state of the art shows two trends: (1) **Full-code indexing and search** (Cody/Cursor/Aider) to retrieve context, and (2) **agentic context optimization** (OpenHands, Deep Agents, Repoformer) to reduce tokens. Notably, none rely on a single monolithic strategy: strong systems use combinations of lexical search, code graphs, and careful prompting. We must transfer the best of these ideas into our architecture: comprehensive indexing (file/symbol/dependency) paired with smart context selection and adaptive retrieval.

# D. Token-reduction evidence

Empirical results show large savings are possible, but the exact *quantity* depends on what is measured:

- **Input token count:** LangChain’s Deep Agents v0.7 cut base prompt tokens by **≈65%** (from ~6k to ~2k base tokens) with no drop in task performance. Anthropic similarly reports trimming “over 80%” of Claude Code’s system prompt on newer models without loss. These are mostly static prompt-engineering wins, not code-context per se.
- **Inference latency/calls:** Repoformer claims up to **70% faster inference** by skipping unneeded retrieval, essentially reducing the number (and length) of LLM calls. Note this is speed, not token count, but implies far fewer calls.
- **Token efficiency per turn:** OpenHands reports **~2× cost reduction per turn** through context condensation (summarization), while still solving as many tasks (54% solve rate vs 53% baseline).
- **Overall task cost:** LocAgent’s graph-based approach yielded the same code-localization accuracy at roughly **86% less compute** (fewer tokens and calls) compared to the prior best models. HyRACC (hybrid RAG) similarly notes big GPU and latency gains.
- **Error reduction:** One vendor (Augment Code) reports their context engine (feeding ~200K tokens) cut hallucinations by ~40%, though this is a proprietary claim and not independently verified.

In short, *claims of “~70% reduction” should be interpreted cautiously.* Repoformer’s “70%” refers to latency, Deep Agents’ “65%” to prompt tokens, and others to various metrics. We have not found any universal 70% figure across all categories. But collectively, multiple studies demonstrate **large (2–3× or more) improvements** in token usage or cost through context engineering. We will use these as targets: e.g., a successful architecture might plausibly cut Codex calls by a similar factor on average.

# E. Retrieval evidence

**Lexical retrieval (grep/BM25):** By far the strongest signal for code is exact matching on identifiers or filenames. Code typically has unique names (every function, import, or config key is a precise string), so grep-style search is extremely effective. In fact, a recent commentary shows that for code “exact-match search beat semantic search”, and “BM25 remains a strong baseline when queries contain explicit identifiers”. We should leverage this: lexical search (e.g. ripgrep, Lucene/BM25) is cheap and accurate on common code queries (function names, classes, error strings). Its weakness is missing synonyms or higher-level intent if no exact token matches.

**Semantic retrieval (embeddings):** Vector-based search can find related code even without shared tokens (e.g. paraphrased docs or concept matches). This can help on queries like “function that sorts a list” where no exact keyword appears. However, empirical evidence indicates embeddings can be brittle. CORE-Bench shows pretrained code embeddings suffer a “sharp drop” in agentic retrieval tasks compared to standard code search. LinkedIn analyses similarly note that embeddings introduce “fuzziness” that hurts precision on code, since LLM-free grep is already highly precise. Agent Retrieval Bench found that a 4B-code embedding model did achieve the best MRR on some tasks, but no embedding method uniformly outperformed text search. In practice, we may use embeddings only as a backup or for tasks where lexical cues fail.

**Learned ranking:** End-to-end learned retrievers (BERT/MLP rankers) have not yet proven essential at the repository scale. Training a lightweight relevance model on devtools-specific data (as in the CIT project) may help if we have labeled examples, but it should remain optional. For now, we can rely on simple scoring (BM25 scores, TF-IDF, or an embedding dot-product) and focus on deterministic features. If we do incorporate a learned ranker, it should return scores or ranks—not gate inclusion—so we can still override or combine it.

**Structural retrieval (graphs):** Using code structure is promising when lexical similarity is insufficient. GraphCoder builds a *code context graph* capturing control- and data-flow, and performs a “coarse-to-fine” retrieval over it, improving completion accuracy. LocAgent’s heterogeneous code graph enables multi-hop file localization. Anecdotally, graph-augmented search helps on broad queries: one report found that when lexical signals are weak, traversing a code dependency graph can recover the right file. These methods tend to be deterministic once the graph is built. We should consider adding an import/call graph to help find neighbors of a known file, especially for impact analysis.

**Hybrid approaches:** The best solution may combine methods. For example, the HindSight project (99P Labs) fused BM25 and dense vectors in a single index, allowing a query to match either exactly or semantically. HyRACC explicitly constructs both a BM25 index and a KNN vector index, and uses a hybrid retrieval process. A practical pipeline is to first generate lexical candidates, optionally expand them via the dependency graph, then (if needed) re-rank or add semantic matches. The evidence suggests no single method suffices; BM25 can be the backbone (especially when the query has identifiers) with embeddings or graph steps to augment coverage. We should aim for a flexible retriever that can plug in multiple sources of relevance.

# F. Task dependence

Yes – retrieval needs vary by task type. The new **Agent Retrieval Bench (ARB)** explicitly categorizes tasks (e.g. *code→test*, *comment→code*, *stacktrace→code*, *edit→ripple*, *no-retrieval needed*, etc.) and finds that *“task-level winners [among retrieval methods] differ substantially”*. In other words, the best retriever for a stack trace might not be best for finding tests from code, etc. ARB’s results bear this out: for some tasks the Qwen-4B embedding model had the highest MRR, for others the 8B had the best recall, and for others the structural RepoMap index maximized recall under a token budget. Crucially, **no single retrieval approach dominated all tasks**.

This implies our system should either (a) **combine multiple signals** (lexical + structural + semantic) and let the context compiler weigh them, or (b) quickly classify the task and pick a specialized strategy. Given simplicity, a combined multi-evidence approach is safer initially: e.g. collect both keyword matches and graph neighbors and let ranking sort them. We may tag tasks by type (e.g. if the prompt looks like a bug report, use one style; if it’s a feature request, another), but we should not hard-code a single retriever.

# G. Selective retrieval

The question of “should we sometimes not retrieve anything?” has mixed evidence. On one hand, *Repoformer* showed that a model can learn to **skip retrieval** when it’s unnecessary, yielding a ~70% speedup (i.e. saving calls on easy queries). On the other hand, ARB found that simply thresholding retrieval (“selective abstention”) did **not** improve success on tasks where no external context was actually needed. In practice, we suggest a cautious approach: allow an explicit decision step (possibly learned) to bypass retrieval *only* when we are quite sure the question is self-contained. For example, if the query is about a change that only affects one file already in the prompt, we might skip. But if there’s any doubt, better to retrieve something than miss needed context. This can initially be deterministic (e.g. if no identifiers appear in the task description, skip; else retrieve). We can revisit a learned gating policy later once we have more data.

# H. Repository representation

We must choose *what units* to retrieve. Possibilities include whole files, file *regions*, functions/methods, classes, or even single lines. Benchmarks use different definitions: SWE-Explore treats “context” as *regions* (file+line spans). ARB considers file-level contexts. In practice, a **hierarchical approach** is promising:

- **First pass:** retrieve relevant whole files (or large chunks). This ensures no source of truth is missed.
- **Context compiling:** within selected files, we can extract just the needed parts. For example, if a file is large, we might take only the most relevant function or excerpt. Extracting at the function/method level (via AST) or section (e.g. comment block) can save tokens. GraphCoder’s graph retrieval essentially does “coarse (file) then fine (snippets)”.
- **Task-specific granularity:** Some tasks naturally operate on small units. For instance, adding a test to a function might only need that function’s body plus its callers. Others (like architecture questions) might need entire documents.

As a first cut, our retrieval can work at **file-level plus optional line ranges**. We can refine later: for example, only retrieve the lines defining a class or function, rather than the full file. This would likely come after the initial implementation, unless file lengths become prohibitive. In any case, we should track provenance of even sub-file snippets.

# I. Repository intelligence

We should precompute as much useful knowledge about the repo as possible. Key candidates include:

- **File inventory:** A list of all source files (with paths and basic metadata). (Trivial to compute and update; baseline requirement.)
- **Symbol index:** Mapping from defined symbols (functions, classes, constants) to their file and line. This is deterministic via AST/parsing; once built, it lets us answer “where is `foo()` defined?” instantly.
- **Imports/dependency graph:** A graph of module imports (and, if possible, a static call graph). For Python, we can parse imports easily; call-graph or inheritance analysis is more complex but adds power. Graph-based retrievers (LocAgent, GraphCoder) rely on this structure.
- **Test–code mapping:** Associations between test files and source code (e.g. tests usually import or reference the code they test). Parsing test files or using naming conventions can build this. If a file changes, we can pre-identify which tests might break.
- **Documentation/ADR links:** If ADRs or design docs exist (e.g. an `adr/` folder), index them too. For example, Open SWE uses an `AGENTS.md` for architecture rules. We should parse such docs for key phrases or associations to code (e.g. “Network module uses X protocol”).
- **Architectural metadata:** Any explicit annotations (e.g. ownership tags in docs, backlog issue IDs, or configuration mappings). This is more custom, but if present it should be captured.

For each of these, we should use existing tools or build a one-off index. All are deterministic (code parsing, static analysis) and can be cached or incrementally updated. The payoff is high: the model won’t waste tokens reconstructing this information. For example, a quick AST scan can give us the entire symbol index; a grep or parser build for each file can update on code changes. These can be integrated into `devtools.repository` components. In sum, any fact that can be “looked up” in code (file-to-symbol, import links, etc.) should be extracted once and reused.

# J. Architecture/documentation intelligence

In addition to code, we should incorporate *architectural knowledge* from documents. Repositories often have ADRs, design docs, or README sections that define architecture decisions and constraints. We should index these specially:

- If the repo has an ADR (e.g. devtools uses `adr/0001-*.md`), parse it for context. For instance, map ADR IDs to described changes and affected packages. Treat accepted ADRs as normative rules.
- Likewise, parse any explicit “requirements” or architecture files. The Open SWE example takes an `AGENTS.md` that encodes testing conventions and design rules, and injects it into the system prompt. We should do similar: any such file is parsed and its content linked to code modules.
- Track **document authority:** which docs are official (e.g. `CONTRIBUTING.md`, `CODEOWNERS`, ADRs) versus explanatory (e.g. blog post, outdated notes). We might tag them in metadata (e.g. DocumentIndex).
- Build a small index of “architecture to code” links. For example, if an ADR says “feature X lives in module Y”, record that link so the agent doesn’t have to guess.

This effort ensures the LLM isn’t repeatedly reading dry docs. Instead, it can be given the distilled essence (or at least not have to search for the relevant section on its own). We should encode this information as additional metadata or even as pre-generated summary nodes in the repository index if practical.

# K. Change-impact intelligence

A highly valuable feature is **automatic impact analysis** for code changes. Given a proposed diff or changed symbol, we can deterministically identify likely affected areas:

- **Static call/import analysis:** Use the dependency graph to find all callers or importers of the changed function/module. Those callers likely need edits or testing.
- **Test selection:** Identify tests that reference the changed code (by name or import). For example, if function `foo()` is altered, grep test files for `foo` to flag which tests to rerun.
- **Documentation/ADR linkage:** If docs or ADRs reference the changed symbols (e.g. “We use method X for Y”), surface those.
- **Historical co-change:** As a heuristic, look at version control history: which files often changed together. If file A was frequently edited alongside B, treat them as co-dependent.
- **Change ripples:** Use the call graph to propagate impact: e.g. if A→B→C, a change in C might eventually affect A. We can precompute reachable sets if needed.

Implementing this does not require ML: it’s classical software analysis. Even a simple static analysis (like running pylint or custom AST scans) can mark dependent code. The context system could, for example, automatically append “Based on the changes, you may also want to check X.py and Y.py” to the context packet. This would cut down on post-hoc debugging loops by highlighting risk areas deterministically.

# L. Context compilation

Retrieval is just the first step – we must then compile a bounded “context packet” to feed the LLM. This involves:

1. **Candidate collection:** Gather files/fragments from the retrieval step (lexical results, graph neighbors, etc.).
2. **Ranking:** Score them by relevance. We might use a simple heuristic (e.g. number of query terms covered) or a lightweight model. Crucially, we keep *all* high-quality candidates, not just one, so we don’t starve the LLM of context.
3. **Budget allocation:** Given the model’s token limit, select top candidates until the budget is exhausted. ARB uses *Budgeted Context Yield* (BCY) to evaluate this: it measures how many ground-truth context lines we cover under a token limit. For example, RepoMap achieved the best BCY at 8K tokens, meaning its selection packed the most useful info per token. We should aim to maximize BCY for our tasks.
4. **Excerpts vs full text:** If a file is large, we may include only the most relevant excerpt (e.g. a function body) instead of the entire file. Deduplication is important: if two files share content (unlikely in code, but possible in docs), remove duplicates.
5. **Ordering:** Put the most relevant context first in the prompt to influence the model earlier.
6. **Provenance tagging:** Attach metadata to each snippet (file path, line numbers) so the model knows the source. This will be part of the final `ContextPacket`.

Throughout, we should track metrics: for example, line-level precision/recall as defined in SWE-Explore. We want high precision (most provided lines are useful) and high recall (capturing the core context). In short, context compilation must be token-aware, prioritize diversity and relevance, and maintain traceability of origins.

# M. Progressive disclosure

We will not dump **all** context at once. Instead, adopt a **progressive disclosure** approach: start with a minimal context packet and let the model *request more information* when needed. This can be implemented via the tool-call boundary already in `devtools`. For example, the model might generate a `ToolCall(name="get_context", args={"query": "find function definitions"})` if it hits a wall.

This design is backed by evidence. One analysis explicitly advises: *“Stop treating retrieval as a single pre-model step. Make it a tool the agent can call multiple times.”*. The advantage is that the initial prompt stays small, and only ambiguous or missing pieces trigger extra LLM usage. In practice, OpenHands showed that delaying context condensation until later preserved cost savings. We anticipate trade-offs (more LLM calls vs shorter prompts), but for expensive APIs it often pays off. Weak models especially benefit, since they can iteratively gather limited chunks rather than digest a massive context in one go. We should implement at least a basic mechanism: after each LLM response, check if it issued a “fetch more” tool call; if so, collect the requested snippets and continue the conversation. This ensures the model gets exactly what it needs in stages.

# N. Context caching and reuse

To maximize efficiency, we should cache at multiple levels:

- **Index caches:** The repository index (file list, symbol table, graphs) should be persisted across runs. Only rebuild or update it when the repo changes. This saves re-parsing code on every request.
- **Embedding/summary caches:** If we generate file summaries or embeddings for chunks, cache them keyed by file hash. Invalidation occurs on edits. This way we don’t recompute expensive summaries or vector encodings repeatedly.
- **Prompt caches:** Many LLM providers automatically cache the system prompt prefix between calls. We can leverage this by reusing identical context whenever possible. OpenHands notes that by only condensing *after* the context grows, they allow the first N turns to reuse the same base prompt. We should similarly avoid regenerating identical prompt segments.
- **Task-local caches:** Within a single task, we can cache tool results. E.g., if the model asks “what is the signature of `foo`?” multiple times, we do it once.
- **Session memory:** Depending on design, we might cache the context packet between subquestions. However, since we already have the conversation transcript, this is inherently cached in the chat history.

Invalidation is crucial: any cache derived from source code must be cleared when that code changes. For repository snapshots, tie all caches to the commit hash. If the repo updates (different commit/branch), rebuild the index/symbols for the new snapshot.

We should maintain metadata (like file hashes) to know what’s fresh. Overall, smart caching can amortize analysis cost without introducing staleness, as long as we track versions.

# O. Local-model feasibility

Because our target includes a local Qwen model (assume a high-end consumer GPU, e.g. ≤48GB VRAM), our architecture must be **lightweight** in memory and compute:

- **Finite context windows:** Qwen’s context size may be smaller than Codex’s. Keep prompts well under, say, 8K tokens for safety. This is another reason for aggressive context pruning and progressive calls.
- **CPU-based retrieval:** Avoid heavy neural models for retrieval. BM25 (whoosh or SQLite FTS) is CPU-friendly and can handle large repos on disk. Even a small embedding model like `embeddinggemma-300M` (a 300M-parameter code embedder) reportedly *runs efficiently on CPU* and yields good code search performance. If we do use vector search (e.g. FAISS), we should ensure it fits in RAM or runs on CPU (few users have GPUs for FAISS).
- **Memory footprint:** Storing entire codebase embeddings might be too large. We might skip embeddings altogether or use very sparse ones. Any in-memory index (hash tables, tries) should be designed to fit under 16–32 GB for large repos.
- **Inference GPU usage:** If Qwen is, say, 7B or 13B (likely for a local setting), ensure other models (e.g. embedding model) can run on CPU. We can run Qwen on GPU and do search/ranking on CPU. Tools like FAISS have CPU modes, or we use simple linear scans for small codebases.
- **Latency:** Local inference is slower than cloud, so minimizing LLM calls (as we aim to do) also saves wall-clock time. Disk-based indexes may slow retrieval, but small tasks (<100ms) are usually acceptable.

In summary, we should lean on classical IR (BM25, keyword search) and small embedding models designed for CPU (like `embeddinggemma`). We should avoid requiring any multi-billion-parameter indexing models or massive vector DBs unless later evidence justifies them. The architecture must function efficiently with limited memory/VRAM.

# P. CIT 52600 relationship

The classroom ML project should be completely optional in the production system, with clean interfaces. Concretely:

- **Expose a retrieval interface:** `devtools` can define a function (or class) like `rank_files(task_query, context_features) -> List[(file_path, score, metadata)]`. The ML experiment can implement this interface. `devtools` will call it but treat it as a black box.
- **Scoring, not gating:** The ranker should return scores or rankings, **not** make final include/exclude decisions. That lets the deterministic pipeline still apply budgets and other filters.
- **Swappable component:** Our architecture should have a “retrieval” module with a plug-in point. Initially the module will use BM25/heuristics; we’ll reserve the option to switch in the ML ranker later (e.g. via configuration). This requires defining a minimal “RetrievalCandidate” and “RankingResult” type in our code (see section W).
- **No knowledge poisoning:** Learned components should not write back into the repository model. They just inform selection. So any ML result is *advisory*.
- **Benchmark outputs:** The ML work should measure IR metrics (Recall@K, MRR, BCY) on held-out tasks. It should also ideally show end-to-end impact (e.g. on an agent solver). Only if we see consistent, significant gains (e.g. an extra 10–20% recall@budget, or substantial BCY improvement) should we consider replacing or augmenting the rule-based retriever.
- **Decoupling:** During development, the ML ranker can be a separate process/script that reads repos and tasks from disk. We should not hard-code any ML library into `devtools`. Instead, define clear data formats (e.g. JSON for queries and score outputs) so the ML team can iterate independently. Once validated, a small model could be imported as an optional dependency.

In short, design a thin experimental seam: a `RetrievalStrategy` interface that the class project can implement or ignore, so we don’t entangle ML code with core logic prematurely.

# Q. Evaluation architecture

We need both IR-style and end-to-end metrics:

- **IR metrics:** For retrieval quality, use standard measures like *Recall@K*, *MRR*, *nDCG*, etc., on labeled tasks. Importantly, use *token-aware metrics*: e.g. *Budgeted Context Yield (BCY)* as in ARB, which measures how much relevant context (lines) is returned under a token budget. We should also consider *precision and recall at the line level* (SWE-Explore’s definitions) to ensure we’re not returning too much fluff.
- **Token efficiency:** Metrics like *useful tokens delivered per token used*. For example, the fraction of provided context that the model actually cites (precision) or the fraction of ground-truth context it got (recall). We can adapt the line-level prec/rec from [55†L441-L449] by tagging which lines the model ultimately used.
- **Task success:** Ultimately, measure the end result: task solution correctness. E.g. did the code compile or pass tests? Did it meet the specification? This must remain the primary criterion.
- **Cost metrics:** Count *total LLM input+output tokens*, *number of LLM calls*, and (if comparing Cloud vs local) *monetary cost*. Also track *wall-clock latency*. For local runs, measure *GPU/CPU time*.
- **Efficiency metrics:** Combine success and cost, e.g. *tasks solved per 10k tokens* or *tokens per successful task*. The goal is clear: maximize success while minimizing expensive token usage.
- **Retrieval-specific:* If we label the “ground truth” files for a task, we can compute Recall@K of the retrieval before compilation. But we must always tie it back to agent efficiency.

To summarize: use a mix of retrieval metrics (Recall@K, MRR, BCY) and end-to-end metrics (token count, calls, success rate). In particular, BCY and recall-per-token capture retrieval under budget. The final litmus test is lower Codex/Qwen usage with equal or better task accuracy.

# R. Codex baseline measurement

Before any changes, we should instrument the existing workflow to collect:

- **Model API usage:** Log every Codex call. Record the number of input tokens (prompt + any retrieved context supplied), output tokens, and whether it was a “thinking” call or final answer.
- **Tool usage:** Count how many times each tool is invoked: file reads, directory listings, searches, AST parses, test runs, etc. Distinguish repeated accesses (same file read twice, etc.).
- **Files examined:** Log which files were actually fetched by tools. We can then compare “relevant vs irrelevant files” by mapping them to ground truth later.
- **Task stages:** Label each model call by phase (exploration vs code generation vs validation). For example: “search for symbol X” vs “write function Y”. This may be inferred by prompt templates.
- **Success outcomes:** Record whether the final solution passed all tests or was accepted, and how many iterations were needed. Also note if any errors or hallucinations occurred.

A minimal harness can wrap the existing agent run and collect these stats. We don’t need a full telemetry system; even print logs or structured JSON outputs could suffice. The key is to quantify: *What percentage of tokens went to discovery vs creation?* *How many calls did each category of tool incur?* *How many times did the model re-open the same file?* Having this baseline data is critical for evaluating any improvements.

# S. Controlled experiment

Design a **before/after study** to measure the impact of repository intelligence:

- **Control:** The current `devtools` agent uses Codex without any new preprocessing. It receives the task prompt and can use tools (file reads, search) normally.
- **Treatment:** The enhanced pipeline. Codex now gets the same task prompt *plus* a *precompiled context packet* (e.g. a few top files/snippets from our retrieval) and still has access to tools if it needs more. We ensure all other conditions (Codex model settings, timeout) are identical.

We run both versions on a suite of test tasks covering different categories (bugfix, new feature, refactor, docs update, etc.). For each run, collect the metrics from the baseline study. Key measurements: *total Codex tokens*, *number of Codex calls*, *file reads*, and of course *task success*. We also inspect qualitative differences: did the Codex plan fewer steps? Was the patch smaller or needed fewer revisions?

We expect the **treatment** to use fewer tokens/calls for the same or better success rate. (A slight increase in calls could be acceptable if tokens drop significantly.) It’s important to check that no tasks break under the new context (i.e. ensure success remains high). Possible confounders: the model’s output could change unpredictably; to control this, we might fix the random seed or use the same few model samples. We should run enough tasks to see consistent patterns (at least 10–20 tasks of each type). The experiment’s success criterion is a statistically significant drop in Codex usage (tokens or calls) while maintaining full correctness on the tasks.

# T. Security/trust

When feeding repository content into an LLM, we must assume it’s untrusted input. Potential issues include **prompt injection** via code comments or README files, maliciously crafted docstrings, or dependencies containing bad instructions. Our system should guard against this:

- **Provenance tagging:** Always label context with its source path and commit. E.g. prefix code snippets with “// From file `config.py`” or similar. This helps prevent mixing code comments with system instructions. It also aids audit trails.
- **No code execution of content:** Treat all code and docs as passive context, never execute them as commands. Our architecture already enforces this (the model suggests edits, but `devtools` executes them).
- **Versioning:** Include the repository’s snapshot ID in the context packet so we know exactly which version the model saw. If the repo updates, we won’t accidentally trust stale context.
- **Sanitize where needed:** For any data that could be interpreted as a prompt (e.g. YAML frontmatter, magic comments), ensure it’s clearly inside code fences or escaped so the model recognizes it as non-instructional.
- **Monitoring:** Log what context is given to the model. In case of unexpected behavior, we can trace if a malicious comment slipped through.

We should not overengineer (no need for full formal verification), but these boundaries and labels ensure we don’t let LLM-generation be directly driven by unvetted content. Essentially, maintain a strict “source vs instruction” partition and keep provenance with every token.

# U. Failure taxonomy

We must anticipate and detect failure modes:

- **Missed-relevant-file:** A truly relevant file never entered the candidate set (maybe our query was too narrow). *Detection:* check if a known gold file was absent from top-K retrieval. *Mitigation:* widen search or allow more aggressive expansion.
- **Ranking error:** A relevant file was retrieved but ranked too low (beyond budget). *Detection:* if the final solution is wrong, see if gold info was in the candidate list at all. Monitor recall@K during development. *Mitigation:* adjust scoring or include more candidates.
- **Graph omissions:** A dependency graph may not capture dynamic imports, so some callers could be missed. *Detection:* if tests fail unexpectedly, see if a caller wasn’t in graph. *Mitigation:* fall back to lexical search if graph is incomplete.
- **Stale data:** Index or summaries are outdated (due to code changes). *Detection:* compare snapshot ID; if code changed without re-index, flag it. *Mitigation:* always re-index or invalidate on commit.
- **Context overload:** Too much irrelevant code is included, confusing the model. *Detection:* low precision metric (SWE-Explore’s precision). *Mitigation:* tighten relevance filtering, drop less-relevant candidates.
- **Insufficient context:** We cut too aggressively. *Detection:* model repeatedly asks for “more code” tool calls or fails on simple questions. *Mitigation:* increase budget or initial context.
- **Model overtrust:** If we give the model partial info, it might confidently produce code without checking broader impacts. *Detection:* look for logical errors in patches. *Mitigation:* enforce sanity checks (tests, linting).
- **Search diversion:** The model fixates on a retrieved snippet that isn’t actually needed. *Detection:* like hallucination, the model bases its answer on wrong context. *Mitigation:* could involve clarification questions or requery.

For each run, we should log diagnostics: which candidates were selected, their scores, which ones the model cited in answers, etc. This observability (e.g. tracking “ground-truth file F was candidate #10 but dropped”) will let us debug failures of retrieval/ranking. Over time, we refine based on these signals.

# V. Recommended target architecture

Below is a high-level architecture diagram (in Mermaid) that separates the deterministic and model-driven components. Key layers are clearly labeled:

```mermaid
flowchart LR
    subgraph "Deterministic Repo Intelligence"
        A[File Inventory & AST] --> B[Symbol Index];
        B --> C[Dependency Graph (imports/calls)];
        C --> D[Test & Doc Mapping];
        D --> E[Other Metadata (ADRs, config)];
    end

    Task[Task Prompt] --> F[Retrieval (Lexical/Structural)];
    F --> G[Candidate List];
    G --> H[Context Compilation & Budgeting];
    H --> I[Context Packet (final prompt)];
    I --> J[LLM Interaction (Codex/Qwen)];
    J --> K[Tool Execution (edits, tests)];
    K --> L[Evidence & Outcomes (diffs, results)];
    L --> M[Evaluation & Logging];
    M --> A;  %% Feedback: may trigger index updates or analysis
```

- **Deterministic Repo Intelligence:** Precomputed data (file/symbol lists, code graphs, ADR/doc indices). Owned by the repository analysis subsystem (no LLM involvement).
- **Retrieval (optional/learned):** Generates candidate contexts from the intelligence layer (lexical search and graph traversal). This can optionally include a learned scorer.
- **Context Compilation:** Ranks candidates, truncates for token budget, and assembles the prompt (with provenance annotations).
- **Model Interaction:** The LLM takes the compiled context and produces output (proposed edits or answers).
- **Execution:** Proposed edits are applied (e.g. code writes, test runs) entirely outside the LLM.
- **Evaluation:** Results (diffs, test statuses) are fed back to possibly update logs or indexes.

This diagram ensures a clear boundary: **no raw code or search happens inside the LLM**. Instead, the model works with a carefully curated `Context Packet` and tools it can call.

# W. Minimal semantic model

Below are the core abstractions we anticipate in the system (only those needed immediately):

- **RepositorySnapshot:** Uniquely identifies a repo state (e.g. a commit hash or branch). *Owner:* repo manager. *Purpose:* tag which version of files/indices we’re using. *Deterministic.* *Not included:* actual file contents. *Use now:* needed for caching and provenance.
- **RepositoryIndex:** Contains file inventory, languages, and basic metadata for the snapshot. *Owner:* deterministic repo intelligence. *Purpose:* fast file-level queries (list all `.py` files, etc.). *Deterministic.* *Not:* symbol details or content. *Slice:* build it first.
- **SymbolIndex:** Maps a symbol name (or pattern) to file locations (and possibly line numbers). *Owner:* deterministic repo intelligence. *Purpose:* answer “where is `Foo` defined?” quickly. *Deterministic.* *Not:* actual symbol usage or docstring. *Slice:* build from AST of each file.
- **DependencyGraph:** A directed graph of code entities (modules/functions) with edges for imports and calls. *Owner:* deterministic analysis. *Purpose:* determine related files (impacted modules, called functions). *Deterministic.* *Not:* dynamic behavior (e.g. runtime duck typing). *Slice:* can be partial; at least build import graph first.
- **RetrievalQuery:** A structured object representing what to search for (e.g. keywords, symbols, or error traces). *Owner:* context compiler/agent. *Purpose:* standardize queries to retrieval engines. *Data-only.* *Not:* actual results. *Slice:* generated on-the-fly per agent request.
- **RetrievalCandidate:** A candidate context snippet (file or lines) plus a raw relevance score. *Owner:* retrieval module. *Purpose:* hold initial search hits before filtering. *Data-only.* *Not:* final context or full LLM prompt. *Slice:* output by the retrieval function.
- **RankingResult:** An ordered list of RetrievalCandidates with final scores. *Owner:* context compiler. *Purpose:* intermediate ranked list before applying token budget. *Data-only.* *Not:* truncated context. *Slice:* result of sorting candidates.
- **ContextBudget:** Represents token/size constraints (e.g. “max 4000 tokens”). *Owner:* context compiler. *Purpose:* guide trimming of context. *Data-only.* *Not:* specific content. *Slice:* simply an integer parameter.
- **ContextPacket:** The final prompt content sent to the model (concatenated snippets with possible summary lines). *Owner:* context compiler. *Purpose:* model’s input. *Data-only.* *Not:* provenance. *Slice:* built just before each LLM call.
- **ContextProvenance:** Metadata mapping parts of the ContextPacket back to source files/locations. *Owner:* context compiler. *Purpose:* enable traceability and trust (the model can “cite” where info came from). *Data-only.* *Not:* user instructions. *Slice:* accompany each context packet.

Each of these is **strictly data-oriented**, with no embedded logic. They answer specific needs: snapshotting, file listing, symbol lookup, candidate ranking, and bounding the model prompt. This minimal set covers our immediate architecture; any other abstraction can be added later only if new requirements emerge.

# X. Gap analysis against current `devtools`

- **Already sufficient:**
  - Repository root management, normalized paths, file read APIs (with root-scoping).
  - Snapshot/commit handling.
  - Basic Python module inventory and markdown rendering (for local context).
  - Preliminary context compiler framework and tool-call interfaces.

- **Should be extended:**
  - The on-disk index: persist file lists and any parse results across runs.
  - Module inventory: expand from Python-only to other languages as needed.
  - Path normalization: already good, just ensure it supports symbolic links, submodules, etc.
  - Context compiler: currently experimental; needs robust token counting and selection logic.

- **Missing now (needed):**
  - **Symbol index:** mapping of all functions/classes to files (currently not fully implemented).
  - **AST-based analysis:** parsing code to extract imports, definitions.
  - **Dependency graphs:** compute import/call graphs.
  - **Test–code linkage:** detect which tests cover which modules.
  - **Architecture doc parsing:** ingest ADRs/`AGENTS.md`.
  - **Token budgeting:** enforce a context token limit and prune candidates.
  - **Candidate ranking:** deterministic scoring (e.g. TF-IDF or BM25) of retrieval hits.
  - **Context provenance tagging:** record file/line sources in context packet.

- **Useful later:**
  - **Vector embeddings:** an optional index if the ML project succeeds (CIT).
  - **Knowledge graph/semantic index:** a rich cross-file graph (beyond imports), only if necessary.
  - **Interactive subagent infrastructure:** for more complex multi-step tasks (only if we build multi-agent features).
  - **Internal telemetry framework:** for production monitoring (beyond needed experimentation).

- **Should NOT be built (yet):**
  - A monolithic, ever-growing code knowledge graph – complexity is high and likely overkill initially.
  - A generic plugin or orchestration engine for arbitrary agents.
  - Complex ML models (rankers, summarizers) in production without evidence.
  - Autonomous code-modifying agents (do not let the system self-improve context filtering unsupervised).
  - A proxy for caching provider prompts – those are already handled by the LLM layer.

In summary, build incrementally on top of existing `devtools` parts: reinforce the indexing and analysis layers first, then layering retrieval and context selection. Avoid speculative features until core functionality proves stable.

# Y. Implementation roadmap

We propose a phased rollout, each with clear goals and metrics:

1. **Phase 1 – Repository Intelligence (Indexing):**
   - **Objective:** Build deterministic repo indices (file list, symbol table, imports).
   - **Slice:** Implement a `RepositoryIndex` class that scans the repo: collects all file paths and languages, parses each Python file’s AST to extract function/class definitions, and records import statements.
   - **Acceptance:** Able to answer queries like “what files define symbol X?” and “what modules import Y?” correctly. Verified by unit tests on `devtools` itself.
   - **Metrics:** Correctness of index (e.g. >95% symbols found), build time, memory usage.
   - **Stop/Go:** Stop when indexing is reliable and significantly faster than doing the same search via the model. Check that agent queries for definitions now route to this index (e.g. a tool call uses it).

2. **Phase 2 – Lexical Retrieval Tool:**
   - **Objective:** Add a deterministic search tool (e.g. using Whoosh or Python’s `re`) for finding candidate files.
   - **Slice:** Expose a new `search_code(query)` function that returns top-N files/snippets matching identifiers or regexes.
   - **Acceptance:** For known queries (e.g. “Config” or bug trace), it finds the relevant file. Unit tests on example queries.
   - **Metrics:** Precision/recall of search on test queries. Reduction in Codex calls for symbol lookup (via manual experiments).
   - **Stop/Go:** Stop when the tool reliably finds intended files for test cases, and we see a drop in Codex usages in a small trial (say 10% fewer calls).

3. **Phase 3 – Context Compiler & Budgeting:**
   - **Objective:** Implement context assembly: ranking candidates, truncating to token budget, and creating the final prompt.
   - **Slice:** Write the `ContextCompiler` that takes a ranked list of files (from Phase 2) and a token limit, and constructs `ContextPacket` (trimmed text with provenance).
   - **Acceptance:** It should honor a hard token limit (no overflows) and include the highest-scoring content first. Write integration tests to simulate compilation.
   - **Metrics:** On a set of queries, measure BCY or recall of relevant snippets under budgets (from small cases). Also measure that final token count ≤ budget.
   - **Stop/Go:** Stop when the compiled context includes known-needed info (e.g. ground-truth snippets) for test cases, and ensures no token overflow.

4. **Phase 4 – Tool Integration & Progressive Retrieval:**
   - **Objective:** Tie it all into the agent loop. Allow the model to issue context-tool calls and feed them back.
   - **Slice:** Modify the agent logic so that model prompts first get the compiled context from above. Implement a `retrieve_more(query)` tool that invokes retrieval and compilation mid-dialog.
   - **Acceptance:** In a live run, the model can ask for more files (e.g. “ToolCall: get_context”) and the system provides them. Test via scripted dialogues.
   - **Metrics:** Measure if the agent actually uses fewer initial tokens (compared to control). Count extra calls made to context tool. Ensure task success is unimpaired.
   - **Stop/Go:** Stop when the agent correctly obtains additional context when needed (we can simulate a task where more info is required and it must request it).

5. **Phase 5 – Evaluation & Iteration:**
   - **Objective:** Fully evaluate the new system on a benchmark of tasks (like the Codex baseline suite).
   - **Slice:** Run the Control vs. Treatment experiment described in (S) on 20–50 tasks.
   - **Acceptance:** Achieve a statistically significant reduction in model tokens/calls (e.g. 20–30% less) with equal or better success rate.
   - **Metrics:** Total tokens per task, calls per task, tasks solved, etc.
   - **Stop/Go:** If the new pipeline meets or exceeds the baseline on these metrics, proceed to release it; otherwise refine the components (e.g. add more candidates or adjust ranking).

Each phase builds on the previous. We avoid doing anything too complex upfront (no ML in V1). After Phase 5, we’ll revisit whether to integrate optional ML rankers (CIT) or to extend to other languages. Each phase has clear deterministic acceptance tests (unit tests and small scale runs) before we move on.

# Z. First implementation slice

**Smallest impactful feature:** *Deterministic symbol search.*

Implement a new tool in `devtools.repository`, say `find_symbol(symbol_name: str) -> List[FileReference]`. This will use the already-built (Phase 1) symbol index to return the file(s) where the symbol is defined (and possibly its signature). For example, given `"read_bytes"`, it might return `/devtools/lib/filesystem.py: def read_bytes(...)`.

- **Inputs:** A symbol or query string; the existing repository index.
- **Outputs:** A list of file paths (with optional line numbers) sorted by relevance.
- **Semantic boundary:** This tool is purely deterministic and not model-driven. The LLM can call it via a Tool (e.g. `get_context("symbol:read_bytes")`). It does not execute code, only looks up the index.
- **Existing code reuse:** We already have file parsing in `devtools`. We would create or extend a `SymbolIndex` component. This is separate from the model and lives in the codebase.
- **Tests:** For a known symbol (e.g. `"devtools.filesystem"` or a unique class name in the repo), `find_symbol` should return the correct file path. Add unit tests using known symbols from the `devtools` repo.
- **Benchmark task:** Pick a simple task where the agent currently asks Codex “where is X defined?”. Instead, feed it via the new tool. Measure: how many Codex calls/tokens it saves. Even a 10–20% reduction on these lookups validates the slice.
- **Deployed metric:** Track how many times `find_symbol` is called and how often it succeeds in eliminating a Codex query.

This slice is small (a few hundred lines of index lookup) but can cut out many tokens that Codex would otherwise use to answer definition queries. We explicitly defer anything ML or multi-file beyond symbol lookup. Features *not* included yet: semantic similarity, call graph lookup, context ranking, or any generative changes.

# 37. Final decision questions

1. **Is retrieval actually the highest-leverage immediate problem?**
   **Yes.** The largest waste in our current workflow is the model re-searching the codebase. Deterministic tools can answer most “where is X?” and “what files are relevant?” questions much faster. Insights from actual agents (e.g. Claude Code’s team) confirm that switching from end-to-end LLM search to dedicated search engines gave the biggest gains.

2. **One retrieval strategy or multiple seams?**
   **Multiple.** Tasks vary and signals differ. The evidence (Agent Retrieval Bench) shows *no single* strategy dominates. We should design a flexible pipeline that can use lexical, structural, and (optionally) semantic retrieval in tandem. Building abstract interfaces (see W) lets us plug in new methods later.

3. **Separate candidate generation and ranking?**
   **Yes.** Generate a broad candidate set first (e.g. all files matching the query or graph neighbors), then apply a ranking filter and budget cutoff. This prevents missing relevant files (a candidate gen failure can’t be fixed by reranking) and matches the coarse-to-fine approach of GraphCoder and others.

4. **Should retrieval sometimes be skipped?**
   **Conditionally.** We should skip retrieval only if we’re confident no external context is needed (e.g. trivial queries). Repoformer showed a learned policy can do this in 70% of cases. But benchmarks caution that gating is tricky (selective skipping didn’t improve results for “no-context” cases). For now, err on the side of retrieving unless the query is obviously self-contained.

5. **What repository representation first?**
   **File-level (with sub-block extraction).** Start by retrieving entire files or large chunks. File-level is simplest and safe. Then allow trimming inside files (e.g. extracting just the function or section needed) to save tokens. In practice, retrieving a file and then slicing it in the context compiler gives a good balance.

6. **What deterministic repo intelligence is highest immediate value?**
   **File/symbol indexing and imports.** The *symbol index* (function/class definitions) is top priority: it answers “where is this defined?” in O(1) without the model. The *import graph* (or simple module dependency map) is next: it quickly identifies which files bring in others. These will reduce most “discover code” queries immediately.

7. **What should remain model-driven?**
   **Semantic reasoning and creative tasks.** Once we supply the relevant context, the model should do the actual software reasoning: interpreting requirements, writing/refactoring code, and synthesizing changes. Ambiguous instructions, high-level design choices, and anything requiring understanding intent or writing novel code should stay with the LLM.

8. **What should remain deterministic?**
   **Everything we can compute cheaply.** This includes file reads, parsing, indexing, search, and any static analysis (AST parse, call graph). Even some summarization could be done deterministically (e.g. extracting docstrings or function signatures). The principle is: if it’s a straightforward computation on code, do it in code, not in the LLM.

9. **Should ML enter the production context compiler now?**
   **No, not yet.** We have no evidence from our own data that an ML ranker will significantly outperform well-tuned BM25/lexical methods. ML should remain for the separate CIT experiment. We should wait for that project’s results before adding a trained model to the pipeline.

10. **What CIT evidence would justify later ML integration?**
   If the experiment shows an ML ranker improves a key metric like Recall@K or BCY by a substantial margin (e.g. >10% relative) *across tasks*, without incurring too much cost, then integration is warranted. Specifically, if ML ranking produces a higher task success per token consumed (or notably higher BCY under the same budget) on held-out tasks, that’d justify rolling it in.

11. **Smallest architecture that allows future methods?**
   We need a simple abstraction for *candidates and scores*. For example, a `RetrievalResult` object that holds a list of `(candidate_path, score)` pairs. The context compiler only reads from this list. New methods (BM25, graph, embeddings) can all produce or augment this list. As long as they output into the same type, we can add methods without redesign. In other words, design a single “candidate list + ranking” interface now and make each strategy fill it.

12. **How to represent relevance without an authoritative ranker?**
   We should expose **scores or weights**, not just a yes/no. For instance, every candidate could carry a “relevance score” (numeric or heuristic) and possibly features. The context compiler can then apply a threshold or top-K. We might also include a confidence estimate. The key is that no single subsystem “vetoes” a candidate outright. The final inclusion is a joint decision by the compiler.

13. **How should context budget affect selection?**
   We simply stop including content once the token budget is reached, favoring higher-scoring parts first. If budgets are tight, we may include only partial files or top functions. We could also divide the budget among multiple candidates (e.g. 50% to the top file, 25% to second, etc.) to ensure diversity. In practice, we’ll trim low-scoring snippets last. In short: sort by relevance and cut off strictly by token count, possibly with rules to ensure at least one snippet per candidate if there’s space.

14. **How should Codex/Qwen request additional info?**
   Via our **Tool interface**. For example, the model can output a special JSON or function call like `ToolCall { name: "get_file_context", args: {"path": "foo.py", "lines": [10,50]} }`. The agent runtime will recognize this and fetch the file lines, then continue the conversation. This keeps the retrieval *explicit* and separate from the LLM’s generation.

15. **How will we know if the new architecture actually worked?**
   By comparing the baseline and treatment metrics from step S. Specifically, we should see lower *total tokens* and *fewer model calls* on the treatment side, without a drop in task success rate. We can also do ablation: check that the retrieved context was used (e.g. did the solution cite the provided file?). We should write down before/after statistics for an evaluation set. A clear pass criterion is something like “average tokens per task dropped by X% and no less than Y% of tasks still succeeded,” according to our controlled experiment.

16. **Which existing `devtools` capabilities should be reused?**
   - **Path/file utilities:** The normalized path resolution and secure file read functions are robust; reuse them for all indexing and context fetching.
   - **Module inventory code:** If there’s already Python module scanning, reuse it for symbol indexing or extend it.
   - **Context compiler framework:** Any existing code for assembling prompts (even experimental) can be extended.
   - **Model interface:** The `ModelRequest/Response` abstractions and tool wiring are already in place; we build on that.

17. **Which existing context-compiler assumptions to abandon?**
   - Do not assume the model will discover the full repo layout on its own. We shouldn’t feed it long directory listings or rely on it reading every file.
   - Don’t assume the conversation history is the primary “memory” – we’ll use our own caches.
   - Don’t assume more context is always better; empirical results show it hits diminishing returns.
   - Avoid treating the model as a black-box proofreader of its own work; we’ll insert validation (tests) and use retrieval as needed.

18. **What should the next implementation story be?**
   As detailed in Phase 1 above: **build the symbol/file index and a simple lexical search tool**. This provides an immediate win (faster lookup of definitions) and lays the groundwork for the context compiler. The first user story could be: “As a coding agent, given a task mentioning symbol ‘X’, I want to call `find_symbol('X')` to get its definition location, so that I don’t have to ask Codex to search for it.” This is concrete, testable, and avoids touching ML.

19. **What should explicitly NOT be built yet?**
   - **Giant knowledge graph:** It would be tempting to model every relationship, but that’s premature. Start simpler.
   - **Large vector DB:** Unless the CIT project shows clear value, avoid a heavy vector store.
   - **Autonomous agents:** Don’t add multi-agent orchestration or self-modification frameworks – focus on static retrieval enhancements.
   - **Generic plugin/event systems:** Only build abstractions we immediately need, not a full plugin infrastructure.
   - **Self-learning loops in prod:** We won’t let the agent rewrite its own code or re-train itself unsupervised.

20. **Long-term for local Qwen parity with Codex – which context infra matters most?**
   The more we encode knowledge *outside* the model, the more even a weaker local model can succeed. Thus: **rich deterministic context** is key. This includes thorough file/symbol indexing, import/call graphs, and change-impact analysis. If a local Qwen only needs to reason about the core issue (rather than discovering context from scratch), it can perform on par with Codex. In practice, fine-tuning Qwen for code and giving it well-formed context (the “packets” we build) will maximize its effectiveness. So the top priority is building out that repository intelligence infrastructure – it gives the local model almost all the clues it needs, compensating for its smaller scale.
