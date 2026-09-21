# Repository Snapshot Identity, Consistency, and Incremental Reuse

## Disposition

Status: Partially reconciled

Canonical research subject: Repository snapshot identity, consistency, and incremental reuse.

Related ADRs: ADR-0002.

Implemented evidence: content identities, identified observed snapshots, and repository-relative addresses.

Accepted: repository identity differs from path and Git identity; deltas do not define state.

Deferred: broader SnapshotPolicy, read-and-verify consistency, SnapshotDelta, incremental maintenance, and external state.

Rejected for now: Git commits, timestamps, or watcher events as foundational state identity.

Superseded or refined findings: ADR-0002 supplies accepted snapshot and applicability semantics.

Open questions: acquisition consistency and dependency-scoped reuse mechanisms.

Revisit triggers: a consumer requiring broader observation policy, maintenance, or replay.

Reconciliation basis: ADR-0002; taxonomy; repository observation implementation.

## A. Executive Conclusion

**RepositorySnapshot:** An immutable snapshot is a complete, *content-derived* view of the repository at an instant, determined by a **SnapshotPolicy**. Its identity is defined by that policy plus the set of resource *addresses* and their *ContentIdentities* (and any included file attributes). A snapshot is “complete” if it includes every repository resource specified by the policy. It need not correspond to a VCS commit; uncommitted work-tree state can be captured under a policy that includes or excludes staging.

**Identity and Content Addressing:**  Snapshot identity must be deterministic and content-based: e.g. by hashing (a Merkle tree) the policy, file paths, and normalized contents. As in Git and Kythe, identical file content should yield the same ContentIdentity, even across snapshots or repos.  Ordering or irrelevant metadata (timestamps, permissions) should be excluded or normalized.

**Logical vs Physical Completeness:** A snapshot is logically complete (contains all declared resources and content), even if internally it reuses storage from prior snapshots. Immutable snapshots and incremental reuse complement each other: unchanged files can share content IDs or cache results, avoiding full re-scan, without violating the illusion of a new immutable state. Content-addressable or persistent structures (Merkle DAGs) enable this reuse.

**Incremental Updates:** Derived intelligence from a snapshot (e.g. parsed ASTs, cross-references) should carry dependency metadata so it can be *incrementally* maintained. If file B changes and file A’s content is identical in both snapshots, any analysis of A that only depended on its own content remains valid. If an analysis depends on multiple files or global context, it is re-evaluated only when one of its *declared* inputs changes.  In short, reuse is governed by exact dependency checks, not by naïve “snapshot equals” tests.

**DerivedKnowledge Applicability:** Each piece of DerivedKnowledge includes (1) the *content identity* and *snapshot-local addresses* of all resources it depends on, and (2) the specific *derivation identity and version/configuration* used. It is applicable to a new snapshot S2 only if those content identities appear unchanged under the same derivation semantics. In other words, applicability is dependency-scoped, not simply “belongs to snapshot X” (cf. Salsa/rustc incremental query system).

**Key Recommendations:** Treat **RepositorySnapshot**, **SnapshotDelta**, and **IncrementalMaintenance** as distinct. A snapshot is state; the delta is a derived diff. Use content hashes (or Merkle-tree roots) for identity, but do not tie snapshot identity to linear change sequences. Filesystem events are only hints, not authoritative state; always verify content. Support both committed and working-tree state under policy. Enable fine-grained invalidation: only re-index those facts whose inputs changed (as in Bazel/Salsa). Preserve the accepted semantics (resource-occurrences are snapshot-local, renames are *claims*, not assumptions).

*Citations:* Git teaches that each commit is an immutable snapshot of project content. Bazel/Skyframe and Rust’s Salsa show how to record dependencies and recompute only the changed parts. Kythe uses content hashes for file identity. Tree-sitter provides incremental parsing, but parser state is an optimization – final analysis must still derive from complete content. The above principles are supported by these mature systems.

# B. Evidence from Version-Control & CAS

- **Git Commits as Snapshots:**  Every Git commit is literally a complete *content snapshot* of the repository tree (except ignored files) at that instant.  Internally, each commit object points to blobs (file contents) and tree nodes; unmodified files are reused by reference.  Git never stores “diffs” in commits; it stores full content hashes.  *“Each commit is an immutable snapshot of the entire project at a given point in time… it can never be tampered with or modified once created!”*.  In Git, content identity is the SHA of the file contents. As a result, identical content under different paths or commits has the same blob ID and need not be duplicated.

- **Content-Addressable Stores (CAS):**  Systems like Git and Kythe use content hashes (SHA) for identities. The Kythe Compilation Database spec explicitly uses SHA-256 digests of file content as the “file digest”.  *“Files and compilations are addressed via a… SHA256 digest of their contents… A file digest is… the same across all compilation databases.”*. This proves content identity is portable and repository-agnostic.

- **Persistent Data Structures:** Git’s use of Merkle trees (commits → tree → blobs) is analogous to functional persistent structures: unchanged subtrees (files) are shared across snapshots.  If designing snapshot identity, one can adopt a Merkle-tree approach: hash the root (incorporating child hashes) as the snapshot ID.  This makes snapshots deterministic and incrementally computable.  It avoids full copies, like persistent maps (Hash Array Mapped Trie) in functional languages, which also share structure across versions.

- **What Matters in a Snapshot?**  Version-control experiences (and reproducible-build advice) teach that build timestamps, ordering, or irrelevant metadata break reproducibility.  Snapshots should ignore mod-times and other OS-dependent fields. Only the *content bytes* (possibly normalized for line endings or encoding) and essential file attributes (executable bit, symlink target, etc.) should determine identity.  For example, reproducible-builds.org warns: *“Timestamps make the biggest source of reproducibility issues… It is also customary to record the date of the build in the software itself… [timestamps] are best avoided.”*.

- **Implications:**  - Snapshot identity should be deterministic, content-derived, and policy-sensitive.  It should not treat a directory listing’s arbitrary order or timestamps as significant.  - Systems like Git show it’s feasible to have immutable snapshots without copying all data each time.  - Content hashing allows sharing identical content across snapshots (or even repositories).  - The *identity* of a snapshot could incorporate a snapshot policy (analogous to how Kythe uses a “revision marker” for a corpus). For example, one could use the Git commit SHA as a revision marker or compute a custom hash representing the entire snapshot under the policy.

# C. Evidence from Build/Incremental Systems

- **Bazel (Skyframe):**  Bazel’s Skyframe is a general incremental computation engine. It records *every* input (files, targets) as an immutable node (SkyValue) keyed by a SkyKey.  Functions (SkyFunctions) declare which input nodes they depend on. Bazel then invalidates exactly the nodes whose inputs changed. As the docs state, “if all the input data of all functions is recorded, Bazel can invalidate only the exact set of nodes that need to be invalidated when the input data changes.”. This is “correct and perfect incrementality”. Bazel even goes further: if a node is invalidated but re-computes to the same value, it “resurrects” downstream nodes (change pruning), avoiding unnecessary re-work.

- **Shake (Haskell):**  Shake is a build library that tracks dependencies between build rules. A rule only re-runs if its inputs (file hashes or declared prerequisites) have changed. Shake users routinely exploit *persistent rule state* to speed up rebuilds. This is analogous to our DerivedKnowledge: a Shake rule’s output is invalidated only if its inputs (source files) are different.

- **Rust (rustc) Incremental Queries:**  Rust’s compiler uses a query-based incremental system (inspired by Salsa). It treats each compilation query (e.g. type-checking a function) as a node in a DAG. After one compilation, it knows exactly which queries read which inputs. On the next compile, only queries whose input data changed are recomputed. The doc explains: if the HIR (checked AST) for `foo` didn’t change, all dependent queries reuse their cached results. This fine-grained approach avoids redoing unchanged parts of the build.

- **Salsa (Rust Analyzer):**  Salsa is an incremental-engine library used by rust-analyzer. It *records* every derived computation (query) along with its inputs and dependencies. On an input change, Salsa “floods” the dependency graph and re-executes only affected queries, and only as needed. It also supports *early cutoffs*: if a query’s inputs changed but its output would be the same (e.g. adding a whitespace that doesn’t alter the AST), it does not re-run dependent queries. Moreover, Salsa introduced “durability” levels so that unrelated changes (e.g. user code vs. stdlib) don’t force re-checking everything. In effect, Salsa treats each piece of derived data as identified by (function name + arguments), so different analyzer versions or inputs produce separate entries.

- **General Build Lessons:**  Modern build systems consistently show that *immutable state + incremental update* is achievable. You maintain a graph of dependencies (between files or tasks) and only re-run what’s necessary. This suggests that our repository-intelligence should likewise track dependencies between derived facts and file contents, to achieve fine-grained invalidation rather than coarse rebuilding.

- **Key Takeaways:**  A repository-intelligence system can, like these tools, treat unmodified data as immutable and skip recomputing derived facts.  Snapshots serve as immutable “input states,” but the *computation graph* over that state can be updated incrementally (re-executing only invalidated nodes).  The strong emphasis on *explicit dependencies* in these systems underlines the need to record, for each piece of DerivedKnowledge, exactly which contents and analyses it depends on.

# D. Evidence from Code-Intelligence Systems

- **Tree-sitter (Incremental Parsing):** Tree-sitter is an incremental parser: it builds a concrete syntax tree (CST) for a source file and can *update* it efficiently as the file edits. This shows how local analysis (parsing) can be made incremental. However, tree-sitter ultimately produces a tree determined *solely* by the current file content (and parser grammar). Its incremental nature is purely an optimization (reusing unaffected subtrees) – it does not change the semantic content. In our terms, the *ContentIdentity* of a file is based on its raw text; a tree-sitter parse is a form of DerivedKnowledge that should still be computed as if from the full content. (Indeed, Salsa’s early-cutoff example highlights that adding a space may not change the AST, but this is a derived fact from content.)

- **Indexers (Kythe/Sourcegraph/SCIP):** Kythe and similar code-indexing systems rely on capturing precise compile actions and file contents. Kythe’s model (via a compilation database) stores *exact contents* of source files in a content-addressable store. It builds a global graph of symbols, references, etc., using those contents. While Kythe’s documentation does not explicitly cover incremental updates, its reliance on SHA256 file digests shows that file identity (and reuse across snapshots) is based on content. If a file’s content hash hasn’t changed between snapshots, the same parse/analysis could be reused. CodeQL/CodeQL-like systems (used by GitHub) primarily do static analysis over committed code, but their architectures similarly ingest each file’s content and produce facts.

- **Language Server Protocol (LSP):** Many LSP servers (e.g. for Java, Python, TypeScript) implement incremental re-indexing: they watch for file changes and update symbols/references incrementally. Though specifics vary, the principle is that a local change invalidates only the symbols/types that depend on the changed content. For example, if you rename a function, only its references and relevant type info are updated, not the entire codebase. This aligns with dependency-scoped invalidation.

- **Cross-Language Indexes:** Systems like Joern’s code property graph or Sourcegraph’s SCIP create large graphs of code facts (ASTs, call graphs, etc.). They often parse code into a language-agnostic graph. To stay incremental, they typically re-index files that changed, then update the global graph. While we found little direct documentation, the practice of treating each file (or compilation unit) separately is common: changed files yield deltas to the index.

- **Summary:** Code-intel tooling teaches that analyses should pivot on file content identity. A file’s syntax tree, tokens, or local symbol table is *local knowledge* (depending only on that file’s content). Cross-file relations (call targets, imports, inheritance) are *relational knowledge* (depending on multiple files or global state). Mature systems treat these differently. For example, if file A’s content is unchanged, its parse tree need not be re-run even if B changed (local vs relational invalidation). Conversely, if A imports B, then A’s import resolution depends on B’s content, so B’s change invalidates that fact. In practice, LSPs and indexes record such dependencies to know what to update.

# E. Evidence from Coding-Agent Repository Indexes

Public documentation on AI coding agents (Cursor, Claude Code, etc.) is scarce. However, these systems fundamentally rely on underlying code-intelligence (parsing, indexing) to answer queries. If they operate incrementally, they likely follow similar principles: maintain a local model of the repo, update it on changes, and use caching. For example, an AI agent might cache a repo’s symbol table and only update entries for edited files. No public source specifies their design, so we fall back to analogous evidence: robust code agents would treat repository contents immutably per snapshot and apply incremental diff-based updates (like build systems). We assume they would **not** rebuild indices on every query if content hasn’t changed, echoing Bazel/Salsa style dependency tracking. But without disclosures, no proprietary behavior can be cited.

# F. SnapshotPolicy Recommendation

A *SnapshotPolicy* defines exactly what repository state is captured. It should be explicitly configurable, not hard-coded. Considerations include:

- **Repository Root:** Clearly define the root directory of the repo to snapshot. (E.g. a monorepo may need multiple sub-roots or workspaces.)

- **Included Files:** Typically all source files under version control, plus any other resources needed for analysis (e.g. config files, schemas). Policy should allow inclusion/exclusion patterns (like defaulting to a VCS manifest or `.gitignore`).

- **Ignored Files:** Files matching ignore patterns (e.g. `.gitignore`, build artifacts) should be excluded by default. Generated or binary files often shouldn’t be content-indexed (unless needed). This should be configurable: e.g., exclude `node_modules`, build output dirs, large binaries, vendor libs, etc.

- **Metadata to Include:** By default, only file contents and stable attributes (path, executable bit, symlink target) should be part of snapshot identity. FS metadata (owner, timestamps, extended attributes) should be *excluded* from identity, or included only as *ignored metadata*. For example, mod-times usually cause reproducibility issues and should not affect content identity.

- **Path Sensitivity:** Case sensitivity (on Windows vs Linux) and Unicode normalization can cause differences. The policy should define normalization rules. Perhaps always canonicalize paths (case-preserving, case-insensitive on Windows) in a consistent way.

- **Empty Directories:** Git does not track empty dirs. For code-intel, empty dirs usually hold no content intelligence. We recommend excluding empty dirs from identity (they can be ignored).

- **Submodules/Nested Repos:** A snapshot policy must decide whether nested repos count as separate snapshots or part of parent. Likely, treat each VCS root independently. Submodules can either be captured by their own policy or ignored.

- **Platform Hazards:** Policies should account for platform differences: e.g. Windows CRLF vs Unix LF (normalize?), file executability bits (relevant for scripts in some languages), or path length issues. The policy should abstract such platform quirks.

- **Recommendation:** *SnapshotPolicy* should be separate from core semantics. For instance, a user can choose “use Git HEAD plus uncommitted” or “use working directory as-is.” These are policies deciding what counts as “complete state.” The architecture should not embed a single universal ignore list; rather, allow the policy to specify excludes. However, the semantic engine should provide a reasonable default (e.g. ignore `.git`, binaries).

In summary, common code-intel requirements often include source files, code config, and exclude generated artifacts. The snapshot identity must exclude non-semantic noise (timestamps, irrelevant metadata), include only policy-relevant data, and be reproducible under identical policy settings.

# G. Snapshot Observation Consistency

**Challenge:** On a live file system, files may change mid-scan, so a simple sequential read could see a nonexistent state. We must ensure that a snapshot represents a *coherent* view or else detect inconsistency.

- **Operating System Snapshots:** Ideally, use OS or filesystem snapshot capabilities (LVM, ZFS, etc.) to freeze the view. If unavailable, we simulate consistency at the application layer.

- **Index/Tree Approach:** Git itself uses the index (the tree object in HEAD) to represent a stable snapshot. For working-tree analysis, one approach is: read a list of files (e.g. from `find`), then read their contents **after** ensuring no modifications occurred. For example, one could stat all files, record mod-times, then read, then stat again to check for changes. If discrepancy, retry or report error. This “metadata-before/after” strategy is used in some backup tools and can be adapted here.

- **Atomic Lists + Verify:** A pragmatic approach: read directory listing atomically (if possible), then for each file read content and use a fast hash to verify it matches a second read (or check that mod-time didn’t change). If any mismatch, we abort or retry the snapshot capture. This yields an all-or-nothing semantics: either snapshot is of a moment in time or it fails.

- **Quiescence/Locking:** Another strategy is to require a “quiescent” period, e.g. no FS events for a short time before assuming snapshot is stable. Watchers like Watchman/Watchdog can assist: they aggregate file change events and can signal when activity stops. However, they can miss rapid changes or coalesce events. Thus we should treat watchers as *advisory triggers*, not authoritative. Inconsistent watches (lost events) should not corrupt state.

- **Retry/Detection:** Many systems simply retry on failure. For example, a tool might catch an `EIO` or file-not-found while reading and restart the snapshot process.

- **Semantic Guarantee Needed:**  We need *snapshot-level consistency*, not necessarily per-file atomicity. In practice, the requirement is that the collected snapshot state corresponds to *some* actual repository state under the policy. It is acceptable to fail and retry if we suspect inconsistency. We don’t need continuous transactional FS guarantees; instead, we ensure either (a) the snapshot matches a real consistent state or (b) we detect and abandon it.

**Recommendation:** Implement a read-and-verify protocol: e.g., record file sizes and timestamps, read contents, then re-check stats. If any changed, discard that snapshot and retry (possibly a bounded number of times). Use watchers/events only to *notify* that things changed (to trigger a new snapshot), but always verify content. If a snapshot cannot be made consistent (e.g. rapidly changing files), we may abort with an error; we should not silently accept an impossible state.

# H. Snapshot Identity

Snapshot identity should be:

- **Deterministic & Content-Derived:** It should be a function of *(snapshot policy + set of resource paths + each resource’s content identity and relevant attributes)*.  Ordering of files must not matter. For example, one could compute a Merkle root: sort entries by path, for each file combine (path, content-hash, mode-bit) into a digest, and hash all that together with the policy identifier to get a final snapshot ID.

- **Policy-Sensitive:** The identity must encode the snapshot policy (e.g. root path, ignore patterns). If the policy changes, the snapshot ID should change even if content stays same (similar to how Bazel’s workspace status affects action keys).

- **Excluding Irrelevant Metadata:** Only include file properties that affect semantics. E.g. paths and content, whether file is executable, and symlink targets. Exclude mod-time, owner, etc. (These can be recorded as *metadata* but not in identity hashing.)

- **Reproducibility:** Given the same policy on two machines with identical file contents, the snapshot ID must match. Thus avoid non-deterministic factors (like file system timestamps or traversal order).

- **ContentIdentity Integration:** One can define `SnapshotID = Hash( SnapshotPolicyID, { (path_i, ContentID_i, attributes_i) } )`. Here ContentID_i is e.g. SHA256 of file content (normalizing line-endings if policy dictates). For directories, one could either ignore them (since path listing covers all files) or include an entry.

- **Non-Git State:** The model must allow non-committed changes: e.g., if snapshot policy is “working tree,” we still compute ContentID from actual bytes. We should not *require* a Git blob ID for identity, though we can opportunistically use one if consistent.

- **Efficiency:** While the definition is logical, in practice we need to compute snapshot ID efficiently. We can cache content hashes of files as they change (like caching file digests). A Merkle tree approach (as in Bazel action cache) supports incremental recomputation of the root if sub-hashes are unchanged.

In summary, treat the snapshot as a pure function of policy and content. This ensures snapshots are immutable and comparable by ID. This approach is validated by CAS systems (Git, Kythe) and persistent data structures: they all derive a global ID from the hashes of constituent pieces.

# I. ContentIdentity

ContentIdentity is the identity of a file’s content, independent of path or repository. Semantically:

- It should reflect the exact bytes (or normalized representation) of the file. Typically, a cryptographic hash (e.g. SHA-256) of the file’s contents is used. For text files, you may choose to normalize line endings or Unicode, but this must be part of policy.

- It should **not** change due to file metadata. Changing timestamps or permissions on a file should not alter its ContentIdentity.

- If normalization rules apply (e.g. always LF endings, ignore BOM, treat capitalization differently), the identity should hash the *normalized* content consistently.

- ContentIdentity of two files (even in different repos) should match if and only if their normalized contents match bit-for-bit. This allows cross-repo reuse: e.g. an analysis result for a content blob can theoretically be reused elsewhere. (The semantics of DerivedKnowledge may still restrict cross-repo use, but the identity is shared.)

- The executable bit or file mode should *not* be part of ContentIdentity, because that’s an attribute of the file’s nature, not its content bytes. Instead, treat it as an attribute in ResourceOccurrence metadata. (Similarly, symlink targets are resource content in some sense; you may hash the link target path as “content.”)

- Generated or parsed representation: If the system supports e.g. an AST identity (hash of the AST tree), that would be a separate derived identity, not the raw ContentIdentity. Raw ContentID is always about bytes.

- Examples: Git’s blob SHA1 is a ContentIdentity of a file’s bytes (with no newline normalization by default). Kythe’s “file digest” is SHA256 of content. Build systems like Bazel use file hashes or content digests to determine if inputs changed.

Thus, **ContentIdentity = hash(bytes)**.  A change in encoding, newline, or even a comment would yield a new identity.  This aligns with evidence: *“Kythe stores the contents of a file in a content-addressable store… addressed via SHA256 of their contents”*.

# J. ResourceOccurrence and Change Semantics

- **ResourceOccurrence:** This is a file (or other resource) at a given path *within a snapshot*. Two ResourceOccurrences in different snapshots may refer to the same content or not, but by definition they are distinct objects (each is identified by its snapshot context). We should **not** globally merge them by path. Concretely: `S1/src/a.py` and `S2/src/a.py` are different ResourceOccurrences even if content is identical. However, we record that both refer to the same ContentIdentity if bytes match.

- **Same path, same content:** E.g. S1:/a.py with Content A, and S2:/a.py with Content A. These are two occurrences of identical content. Our model should allow reusing DerivedKnowledge on A from S1 in S2, but by checking dependencies. So one ResourceOccurrence does not *become* the other; rather, they share a ContentID and *we* can note that dependency graph for one can apply to the other.

- **Same content, different path:** If S1:/a.py = Content A and S2:/b.py = Content A, we have two occurrences with identical content. This by itself does *not* imply rename; it just means two files happen to be identical. We should **not** automatically infer that a.py was moved to b.py (that would be a derived rename claim, not part of core snapshot semantics). Each ResourceOccurrence is local to its snapshot and address, and has its own identity.

- **Add/Remove/Change:** The basic structural snapshot-differences are: a path added, a path removed, or a path’s content changed (ContentID changed) between S1 and S2. These are facts derivable by comparing snapshot resource lists. Interpretive changes (rename, copy, etc.) are *derived knowledge*, not fundamentals. If a.py vanishes and b.py appears with the same content, that is *observed* as “removed a.py, added b.py with same content.” A “rename” relation is extra semantic inference.

- **Summary:** ResourceOccurrences live in a specific snapshot. Identity of an occurrence = (snapshot ID + path). Two occurrences with the same content identity can share knowledge, but remain separate objects. This is consistent with the architecture’s idea that subjects/occurrences are snapshot-local. Git’s model similarly treats each commit’s file list independently; only by diff tools do we guess renames.

# K. SnapshotDelta Semantics

- **Definition:** A `SnapshotDelta` (or ChangeSet) represents the difference from S1 to S2: specifically, the set of added, removed, and changed resource addresses (with old vs new ContentIDs). It is derivable by comparing the two immutable snapshots.

- **Role vs State:** The delta is *derived data*, not authoritative state. The authoritative state is always an immutable snapshot. The delta is simply a way to compute which knowledge may be invalidated or reused. We **should not** treat the ordered sequence of changes (the “change script”) as the snapshot identity; that would break immutability. Instead, snapshot identity is content-based (see H).

- **Use in IncrementalMaintenance:** The delta can speed up invalidation: e.g., if snapshot-delta says “b.py content changed, c.py removed, d.py added,” then we know which resources to re-index from scratch. However, even without computing an explicit diff, we could just re-check each resource’s content identity against the cache. In practice, a diff is just a utility.

- **Deltas as Hints, not Truth:** One might consider watcher events or VCS diffs as providing deltas. These are only *hints* until validated against actual content. For instance, a Git diff might say file X changed, but we must still open X to get its new content identity.

- **Atomicity:** If we treat the snapshot immutably, the delta should represent *committed changes* between two stable states. We should not incorporate partial or unsynchronized edits as a "delta" unless they are snapshotted properly.

- **Recommendation:** Keep snapshot and delta concepts separate. The snapshot is the ground truth. The delta can be computed after the fact and used for incremental work. It is an *output* of comparing states, not an input that *defines* state. This ensures reproducibility: applying a delta to S1 in a different context is meaningless; instead, rebuild S2 anew from sources or from applying actual file changes, then compute delta.

# L. DerivedKnowledge Applicability

DerivedKnowledge (K) is a piece of information computed by an analyzer on some inputs in a snapshot S. Its applicability to another snapshot S' depends on two things: **(1)** whether its dependencies are unchanged, and **(2)** whether the derivation rules/configuration are unchanged.

- **Dependency-Scoped Validity:** Each K must record *exactly* which ResourceOccurrences or ContentIDs it depended on. Then K is only applicable to S' if *those same dependencies* (same content IDs at the corresponding addresses) are present in S'. For example, if K was “AST of file A”, it depends only on A’s content. If A’s content ID is unchanged, K can be reused in S'. If K was “import resolution of A to B”, it depends on content of A *and* on the identity of B (or on the global graph); any change to B or to the import graph would invalidate K.

- **Not Simply “belongs to snapshot”:** In many naive caching schemes, data is tagged by the snapshot ID. We reject that: we should reuse K even if snapshot ID changed, *provided the data it depends on is identical*. This is exactly what Salsa does: a query’s result is keyed by inputs, not by “which compile it was in”. If ContentIdentity(A)=X in both S1 and S2, then K=analysis(A) is still valid (unless the analysis changed).

- **Analogy:** Think of K as a function of inputs: if the inputs are equal, the function result is the same. The “inputs” can include file contents, compiler version, config flags, etc. If any of those differ, K must be recomputed. This aligns with the principle “if the input state is the same, the same data is returned” (hermeticity in Bazel).

- **Configuration and Analyzer Semantics:** We must consider tool version/config as part of the derivation identity (see below). If an analyzer’s logic changes, even with identical file inputs, old K cannot be blindly reused.

- **Example:** If K was “symbol table of a.py” and only a.py’s content matters, then K stays valid if a.py’s content ID is the same in S2. But if K was “a.py’s import resolved to src/x.py”, then K actually depends on src/x.py’s content too. If src/x.py changed (even if a.py didn’t), K is invalid. Thus, the applicability check must follow all dependency edges.

- **Conclusion:** DerivedKnowledge is applicable by *structural dependencies*, not by membership of a snapshot. If all actual inputs (file contents, ASTs, previously derived facts) of K remained the same, K is still valid in the new snapshot. This semantic ensures maximal reuse without sacrificing correctness.

# M. Local vs. Relational Invalidation

- **Local Knowledge:** Facts that depend on a *single* resource’s content (and nothing else) are local. Examples: a file’s parse tree, its set of defined symbols, or inline documentation summaries. If the file’s content identity doesn’t change across snapshots, all local derived facts for that file remain valid. Tools like tree-sitter demonstrate that parsing is purely a function of one file’s content. Rust’s incremental parser shows that if an input (file content) yields the same AST, dependent queries remain green.

- **Relational Knowledge:** Facts that depend on *multiple* resources or on global repository state. Examples: cross-file import bindings, reference targets, call graphs, type hierarchies, test-to-code links. If any file in that set changes, the fact may need recomputing. For instance, if K = “A imports symbol S from B”, then K depends on both A and B. A change in B’s exports invalidates K even if A’s text didn’t change.

- **Dependency-Driven Invalidation:** Mature incremental systems (Bazel, Salsa, LSP servers) naturally enforce that a derived fact is invalidated only if one of its explicit dependencies changed. They do not invalidate “everything of the same category” indiscriminately. For correctness, our system should similarly track fine-grained dependencies at the level of ResourceOccurrences or intermediate facts.

- **Implication:** Invalidation granularity should follow actual data dependencies, not static categories. We should avoid schemes like “if module X changed, invalidate entire project index”. Instead, only facts whose dependency closure intersects changed resources should be re-evaluated. This is feasible because we record dependencies during derivation.

- **Examples of Impact:** In a code repo, a file renaming (change in address) has no effect on the file’s own parsed AST, but it *is* a relational change for any analysis that indexed by path (like symbol resolution by qualified name). Our model treats the address rename as a removal+addition; derived facts tied to the old path become inapplicable (need re-derivation for the new path).

# N. Derivation Identity/Version Invalidation

The **derivation** (analyzer function or tool) and its configuration must be treated as inputs to any DerivedKnowledge.

- **Analyzer as Input:** Each DerivedKnowledge K is the result of running a specific analyzer at a specific version/configuration on certain inputs. If the analyzer changes (e.g. new version, changed grammar, different compiler flags), we cannot trust old results. In incremental systems, this is often handled by including a version hash or compiler fingerprint in the key.

- **Evidence:** Salsa shows this by encoding the *function name and arguments* in a query’s identity. We should similarly consider including an “analyzer ID” as part of a query’s signature. If the analyzer version increments, queries become mismatched and get recomputed. Bazel’s actions factor toolchain hashes into action keys, causing rebuilds when compilers change.

- **Configuration & Flags:** If an analyzer is parameterized by settings (e.g. a lint rule turned on/off, or a language dialect flag), these settings must be part of the derivation context. Changing them is equivalent to a different derivation.

- **Environment:** Some analyses depend on environment state (e.g. dynamic classpath, system libraries). Ideally, that should be captured in the dependencies or derivation ID. For now, we can treat environment differences as a cause for invalidation, to be handled by higher-level provenance (e.g. including relevant environment variables in the snapshot policy if needed).

- **Principle:** **Derivation semantics versioning is an invalidation boundary.** Unchanged content + unchanged dependencies + unchanged derivation logic = knowledge reuse. If any of those differ, knowledge is invalid. As one blog put it, queries are pure functions of their inputs. The “inputs” include more than just file text.

# O. Incremental Maintenance Architecture

The architecture should support an *incremental evaluation engine* reminiscent of Bazel/Salsa:

1. **Dependency Graph:** Maintain a graph of DerivedKnowledge nodes keyed by (derivation ID + inputs). Each node lists its direct dependencies (other nodes or ResourceOccurrences).  For each snapshot, we build or update this graph by (re)running analyses only where needed.

2. **Reuse Valid Knowledge:** On snapshot S2, start with knowledge from S1 tagged with dependencies (ContentIDs, derivation IDs). For each K, check if all its dependencies are unchanged in S2. If yes (and derivation IDs match), mark K as still valid and bind it to S2’s context.

3. **Invalidate & Recompute:** If a dependency changed or a derivation version changed, invalidate K. Then re-run the associated analysis to produce updated K. For bottom-up efficiency, one could propagate invalidation before recompute, or use red-green (as Rust does) to minimize rework.

4. **Laziness and Change Propagation:** Like Salsa, do not proactively recompute everything on a change. Instead, mark dependent nodes “dirty” and only re-run them when their results are actually needed by some top-level query. This is more relevant for on-demand queries (IDE style) than a full batch index, but the structure supports both.

5. **Durability/Scoping:** We may optionally classify parts of the graph by durability (as Salsa does) to avoid revisiting global libs on local edits. But initially, we can keep it simple: every change invalidates reachable dependents. Later, “durability” can be a refinement.

6. **Storage & Caching:** Knowledge values (ASTs, symbol tables, graphs, etc.) should be cached keyed by content and derivation, not snapshot. A content-addressable cache (like Bazel’s action cache) is ideal: K’s cache key includes hashes of its inputs and the derivation version. Upon reuse, we simply fetch from the cache. But correctness comes from checking keys, not from trusting “cache hit” alone.

7. **Graph Views:** Multiple analyses may produce different graphs (import graph, call graph, etc.). We should consider graphs as just another form of DerivedKnowledge, built on top of symbol resolution etc. Each graph projection can be maintained incrementally by reacting to changed edges/nodes. There is no need for a monolithic “rebuild all graphs” step; updates to source facts will cascade to graph facts via the dependency mechanism.

- **Flexibility:** The architecture should allow starting with coarse granularity and refining over time. For a prototype, one could invalidate per-file (re-index whole file) on any edit; later, finer units (functions, symbols) can be separate dependencies. The core semantics still hold: knowledge is valid only if all declared inputs match.

- **Incremental Parser:** Treat incremental parsing similarly: if a file’s content changed, we can attempt an incremental parse (if supported), but the final parse tree still depends only on the new content and parser version. The parse result can be reused if content identity didn't change. Ultimately, if stored by content hash, the cache key ensures only content matters.

**Conclusion:** Adopt an *explicit dependency graph* model (like Skyframe or Salsa). DerivedKnowledge nodes have attached provenance and dependency lists. On snapshot change, propagate invalidation through this graph. This aligns with principles of determinism, provenance, and fine-grained updates, and is supported by the aforementioned systems.

# P. Graph Maintenance Implications

DerivedKnowledge serves as the substrate for higher-level graphs (import graph, call graph, etc.). We propose:

- **Graph as Derived Data:** Treat each graph or projection as DerivedKnowledge *built from* underlying facts. For example, the call graph can be derived from function definitions and call-site references. Thus, when underlying facts change, the graph can be updated incrementally through the same dependency-tracking machinery.

- **Incremental Updates:** For instance, if a new function is added, simply add a node and edges to the call graph for its calls. If a call target changes, update just that edge. We should avoid rebuilding entire graphs; instead use the dependency graph of facts.

- **Derived vs Stored Graph:** In practice, one may store graph edges explicitly. If an analysis (e.g. “compute call graph of file F”) is modeled as a query, then updates to F or its dependencies will re-run that query and update the call graph entries for F only.

- **No Global Rebuild:** There is no need for a monolithic “rebuild entire import graph” operation on any change. Mature systems (like Bazel, Salsa) suggest doing only the invalidations needed. Even a complex graph algorithm (like C3 inheritance resolution) can be incremental if built as a series of smaller queries.

- **Multiple Views:** Since multiple graph views may exist, we simply run each graph-building analysis with its own dependencies. They all sit on top of the same content-derived facts. E.g., the containment graph (file hierarchy) changes only on path changes. The import graph changes on content/address changes. Each is updated in its own incremental process.

In short, graph maintenance should follow the *DerivedKnowledge paradigm*: graphs are not first-class immutable state, but emergent from the repository contents and analysis results. They benefit from the same caching/invalidation logic.

# Q. Working-Tree and Git Integration

- **Working-Tree State:** The architecture must handle uncommitted (working) changes. A SnapshotPolicy can specify “use working tree contents” (like `git ls-files` plus modifications). In that case, a snapshot is a view that includes those changes. Working-tree modifications simply produce different content identities than the last commit snapshot.

- **Git Blob/Tree IDs:** We may *use* Git blob hashes opportunistically to accelerate identifying unchanged content (e.g. `git hash-object`), since Git already does content hashing. However, **do not** rely on Git commit or index as fundamental. Git metadata (refs, branches) is orthogonal: the snapshot ID will come from our content-merkle approach, not the Git commit SHA. We can record “Git SHA1 HEAD” as a provenance marker, but the system should function on a plain file-tree too.

- **Staged vs Unstaged:** If policy includes the index (staged area) differently from HEAD, we might need a special treatment. E.g. snapshot from index might include staged changes. This complexity can be captured by defining the snapshot policy to pick either HEAD or working dir. It’s simplest to say: SnapshotPolicy chooses a view (HEAD, index, or worktree).

- **Non-Git Repos:** The system must be VCS-agnostic. Even if Git is used, avoid coupling. For example, a Mercurial user should be supported by the same core logic.

- **Git Identity as Metadata:** A Git commit ID can be recorded as metadata (e.g. “repo at commit X”), but it should not *define* our snapshot identity. This avoids tying our correctness to Git’s model. It can, however, be used for optimizations (if snapshot policy=“commit”, then snapshot ID could simply be commit hash combined with policy version).

- **Git Object Caches:** Bazel’s repository cache and other systems show that taking advantage of Git blobs is viable: if two files match a Git object ID, they are essentially the same content blob. But Git blob IDs depend on mode bits (executable) too; be aware. We should compute our own ContentID that matches Git’s when mode is normal.

- **Conclusion:** Git can *accelerate* content identity (via its efficient hashing or packfiles), but it should remain an implementation detail. The conceptual model is file content based. The system should gracefully handle non-Git projects or detached worktrees.

# R. Failure and Partial-State Semantics

- **Snapshot Observation:** A `RepositorySnapshot` should represent a *successfully observed* state. If some resources can’t be read (permission denied, missing symlink target, etc.), one of two approaches is possible:
  1. **Fail-fast:** Declare the snapshot failed and do not produce it (raise an error).
  2. **Qualified Snapshot:** Include the error as metadata and mark intelligence as incomplete.

  Given the need for reproducibility, failing the snapshot (option 1) is safer: it forces the caller to acknowledge the issue. Many systems (git, compilers) error on unreadable files. I recommend: if any required file is unreadable, the snapshot operation should fail (no partial snapshot).

- **Intelligence Completeness:** Independently, derived analysis may fail (e.g. parser error, analyzer crashes). The snapshot itself still exists (the files are known), but its intelligence is only partial. The system should distinguish “snapshot complete” from “analysis complete.” The former means all files were captured; the latter means all analyses succeeded.

- **Inconsistent Observations:** If during scanning a file vanishes or appears, our consistency checks (from G) should detect that and treat the snapshot as invalid/incomplete.

- **Post-Failure:** If a snapshot attempt fails, it can be retried. We should avoid silently swallowing failures. The user or agent may need to resolve permission issues.

- **Symlinks:** If a symlink is broken, treat that as a snapshot error unless policy says to ignore certain broken links. Similarly, if a file is locked or in use (on Windows) and unreadable, handle like unreadable file.

- **Transaction Semantics:** There is no concept of a “partial snapshot” with some files missing: that risks producing a non-existent state. We prefer either all required files present or no snapshot. However, intelligence on a snapshot can be partial (some analyzers may skip files with errors, but that’s separate from snapshot validity).

# S. Historical/Replay Semantics

- **Retaining Old Snapshots:** If we ever want to reference an old snapshot (for debugging or analysis history), the snapshot’s identity must still make sense even after it’s removed. This means the snapshot ID scheme (policy+content) must be stable and meaningful. For example, if we use a Merkle root hash as snapshot ID, that ID will still correspond to the same state if recomputed.

- **Ephemeral Storage:** We are not required to keep all snapshots forever. But if we evict an old snapshot’s data, anyone with the snapshot ID should not confuse it with something else. This is ensured by content-based identity: a fresh rebuild of that snapshot would yield the same ID only if it truly has the same content.

- **Queries Over History:** We can support queries like “what changed between S1 and S3?” by either storing the deltas or replaying the derivation. As long as snapshot IDs are content-derived, comparisons remain valid.

- **Determinism:** The snapshot ID and data must not depend on ephemeral state (like local cache contents). Always derive state from the repository and policy.

- **Conclusion:** Historical snapshots can be resurrected or referenced by their ID, because the ID encapsulates the entire state. This is similar to how Git commits remain stable references. As long as policies are consistent, the identity semantics allow meaningful historical queries even if data was pruned.

# T. Evaluation of Candidate Principles

We now assess each proposition:

1. **Immutable snapshots and incremental maintenance are complementary.** *Supported.* The evidence from Git (immutable commits) and Bazel/Salsa (incremental reuse of unchanged parts) shows these can coexist. We endorse this union.

2. **Logical snapshot completeness does not require full re-indexing.** *Supported.* Content-addressable and persistent-structure techniques allow sharing unchanged data. Bazel’s change pruning and Salsa’s caching illustrate avoiding re-work.

3. **Snapshot state, delta, and maintenance operation are distinct.** *Supported.* Treat the snapshot as data, delta as a derived diff, and maintenance as a process. Our analysis warns against conflating “sequence of edits” with state.

4. **Filesystem watcher events are hints, not authoritative.** *Supported.* We recommend using watchers only to trigger reevaluation, always verify by content. As Git’s index illustrates, the true snapshot comes from file contents, not event streams.

5. **ResourceOccurrences are snapshot-local even if ContentIdentity is reused.** *Supported.* Each file occurrence is tied to a snapshot and path. Content identity reuse is a separate matter. This matches our design and accords with Git’s per-commit tree objects.

6. **Same content at new address does not prove rename/move.** *Supported.* We treat renames as derived knowledge, not core identity. Two occurrences of the same content are just that, not automatically the same entity.

7. **DerivedKnowledge applicability should be dependency-scoped.** *Supported.* This is a core principle, reflected by Bazel and Salsa: validity hinges on dependencies. We emphasize dependency-scoped logic.

8. **Local knowledge may be reusable when content identity unchanged.** *Supported.* If content identity of a file is unchanged, its purely local analyses (syntax, local types) are still valid. Salsa’s early-cutoff example confirms whitespace-only edits don’t break local results.

9. **Relational knowledge may invalidate despite unchanged local content.** *Supported.* If an analysis combines multiple files, a change in one can invalidate facts about another. For example, a.py’s symbol resolution may break if b.py (import target) changed. This is consistent with multi-input dependency graphs.

10. **Derivation semantics/version/configuration participate in applicability.** *Supported.* Changing the analyzer or its settings is akin to changing an input. Our architecture treats the derivation identity as part of the cache key, so a new version forces recompute. This aligns with how Salsa encodes function calls.

11. **Graph maintenance should follow knowledge dependencies, not global rebuild.** *Supported (with qualification).* Graphs (imports, calls) should be updated via the same dependency graph. We do not force rebuilding entire graphs; instead, affected parts are updated by their underlying knowledge changes. This was our recommendation.

12. **Incremental parser state is an optimization, not foundational.** *Supported.* Parser internals can speed up analysis, but snapshot semantics rely only on final content. Tree-sitter is useful, but even if not used, correctness holds.

13. **Cache presence ≠ automatic applicability.** *Supported.* We must still verify dependencies. A cache hit is only valid if the keys truly match the current state. This is basic to CAS-based caches.

14. **Historical snapshot identity remains meaningful independently of retention.** *Supported.* Using content-derived snapshot IDs guarantees that identity is intrinsic and not tied to storage. If data is evicted, it can be re-generated and will match the ID only if state is identical.

15. **Snapshot completeness and intelligence completeness are distinct.** *Supported.* We must allow a snapshot to exist even if some analyses fail. Snapshot completeness means files were captured; intelligence completeness means all analyses succeeded. For robust operation, these must be treated separately.

All 15 are **supported** by our recommendations or explicitly qualified in context. None are outright rejected, though some require careful implementation to ensure correctness (e.g. watchers as hints only).

# U. Concrete Recommendation for `devtools`

**RepositorySnapshot:** Define it as an immutable object containing `{ policyID, list of (path, ContentID, [relevant attrs]) }`. ContentID = hash(file content). Attributes: at most “isExecutable” or symlink target. Ensure ordering independence.

**Snapshot Identity:** Compute an overall snapshot hash (ID) from `policyID || sorted(paths+ContentIDs+attrs)`. Use a strong hash (e.g. SHA-256). Do not bake in FS metadata except what policy says. This ID is *stable* and repository-relative. For a Git-committed snapshot policy, you may set `policyID=commitHash` (plus version), yielding snapshotID ≠ commit hash but reproducible.

**Completeness:** A snapshot is “complete” if all files matching policy were read. If any file is unreadable, the snapshot fails. Partial analysis is then up to client (snapshot exists, but derived knowledge list notes missing parts).

**Incremental Updates:** Upon a new snapshot S2, compute diffs in ContentIDs vs S1. For each DerivedKnowledge K from S1, check dependencies: if all dependencies (ContentIDs and derivationVersion) match S2, attach K to S2; otherwise mark K invalid. Then for each missing piece of knowledge, re-run its analysis on the new snapshot context.

**DerivedKnowledge Model:** Each piece of knowledge K should record:
  - **Value** (the actual derived data, e.g. AST, index entry, etc.).
  - **Dependencies:** A list of ResourceOccurrences or other K’s (ideally by ContentID and path).
  - **DerivationID:** A unique ID of the analyzer and its config version that produced K.
  - **Provenance:** If needed, metadata linking K to S1. But semantics for reuse rely only on deps and derivation.

**Applicability:** K is applicable to S2 if:
  1. K’s derivationID matches (same analyzer version/config).
  2. For each dependency (path, ContentID), S2 has the same file path with identical ContentID.
  3. If K depended on “global” state, encode that state as synthetic dependencies (e.g. a global index version).

**Incremental Maintenance Flow:**
  1. Load S1→S2 changes (delta).
  2. Propagate invalidation through K graph.
  3. For any query or required analysis not present or invalid, execute analyzer to derive new K.
  4. Cache new K keyed by deps+derivation for future reuse.
  5. Update any higher-level graph views by triggering their queries.

**Storage:** Use content-addressable caching for DerivedKnowledge. E.g. cache ASTs per file content hash, symbol resolution per (file hash, imported symbols). The cache lookup keys incorporate content and derivationID.

**Prototype Feasibility:** Initially, you can treat each file as an isolated unit of reuse: if file unchanged, reuse whole-file facts. Later refine to function-level or syntax node dependencies. The dependency graph can be coarsely at first (file→file) then finer. The semantics don’t change.

# V. What Must Be Decided Now

- **Snapshot definition:** We must finalize that a snapshot = *policy + set of (path, content hash, needed attrs)*.  All implementation should follow from this.
- **Dependency model:** We must adopt a dependency-based invalidation model (not per-snapshot). This core design enables the rest.
- **Snapshot identity scheme:** Choose content-hash based ID vs a simpler scheme. It must meet the properties (deterministic, reproducible).
- **Policy vs semantics:** Decide which file attributes count and how policy is expressed (e.g. use of .gitignore, executable bits). These affect identity and should be stable decisions.
- **Treatment of failures:** Decide if snapshot take is all-or-nothing or partial. Likely all-or-nothing for atomicity.
- **Use of VCS metadata:** Decide whether to include VCS revision markers as optional metadata in snapshots.

These choices fix the fundamentals of identity and dependency.

# W. What Should Remain Unresolved

- **Incremental parser internals:** Exactly how to do incremental parse for performance can be left to implementation. It is an optimization on top of the core model.
- **Watcher algorithms:** The exact strategy (retries, timeouts) for consistency can be tuned later.
- **Durability levels:** Salsa’s multi-version vectors for durability are advanced. We can leave that for later scaling and keep a simpler single-version approach initially.
- **Graph technology:** We do not need to choose a specific graph engine or database now; we just need the concept of incremental graph updates.
- **Cross-repo caching:** Building a global cross-repo cache for content IDs is an interesting future extension, not needed upfront.
- **Precise policy expressions:** The format of specifying includes/excludes (e.g. .gitignore parsing rules) can be refined later as needed; initial support can be minimal.

# X. Risks / Failure Modes

- **Over-invalidation (too coarse):** If we accidentally tie a DerivedKnowledge to too many dependencies, we’ll recompute more than needed (slower increments). For example, if we treat “project version” as input everywhere, a version bump invalidates all K. We mitigate by strict dependency tracking.

- **Under-invalidation (stale knowledge):** If we miss a dependency, we risk using outdated information. Example: ignoring the dependency of a symbol resolution on the full index. We counter by requiring analyzers to explicitly declare all inputs.

- **False consistency:** Treating watchers as truth might cause subtle bugs if a file changed silently. We avoid this by verifying content. A snapshot that appears “consistent” but wasn’t actually simultaneous could lead to confusing analysis.

- **Cache poisoning:** If cache keys are not carefully constructed (omit derivation version or attributes), one might reuse knowledge incorrectly across snapshots or analyzer versions. Using precise keys including derivation ID and content IDs prevents this.

- **Identity instability:** If snapshot identity included non-deterministic data (like fs order or mtime), the snapshot ID could differ across machines/builds. We design it to avoid such metadata.

- **Overdependence on Git:** Leaning too much on Git (like using commit IDs everywhere) could break non-Git repos and make working-tree updates awkward. We keep Git as an accelerator only.

- **Excessive invalidation tracking overhead:** Dependency graphs can become large. We should be careful about memory/time cost. However, this is future work; core semantics allow trading off granularity vs performance.

- **Partial/incomplete intelligence:** If analyzers fail silently, we might have a snapshot with missing facts, which could mislead agents. We should ensure that analysis failures are reported separately from snapshot validity.

Overall, the biggest risk is complexity. But since correctness relies on semantic rules (dependency tracking, content identity) rather than complex machinery, the approach remains safe: wrong behavior (stale or incorrect facts) can only occur if we violate the dependency rules, which careful design avoids.

# Y. Sources

- Git immutable snapshot model
- Bazel Skyframe incremental build
- Rust compiler incremental (query DAG)
- Salsa incremental engine (dependency/versioning)
- Tree-sitter incremental parsing
- Kythe content-addressable DB
- Reproducible builds (timestamps, metadata)
