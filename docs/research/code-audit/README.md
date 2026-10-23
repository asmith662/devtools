# Code audit evidence ledger

This is dated research metadata for the [comprehensive audit](../comprehensive-code-audit.md)
and [RI domain report](../repository-intelligence-code-audit.md), based on feature
`95efbf711c3644fb32d269d85927000cd8f4aaa9` and remote main
`5d979920d0728775ed529457c88f5b68b440c64f`. It is neither a runtime registry nor
an alternative source, architecture or backlog authority. Raw provider receipts,
scientific captures and preserved archives remain in their original custody.

| File | Contents and qualification |
| --- | --- |
| [checkpoint.json](checkpoint.json) | Changed-path/hash overlay and actual test/integrity receipts for this documentation checkpoint; containing Git commit binds its own identity |
| [coverage.json](coverage.json) | Counts, methods, scope limits, directory census and 13 forensic fingerprints |
| [refs.json](refs.json) | All ref names, exact remote advertisement, ancestry and disposition |
| [tip-deltas.json](tip-deltas.json) | Code/config/test differences per distinct tip; not an instruction to integrate |
| [commit-identities.json](commit-identities.json) | Ordered SHA list; integer `commits`, `tips`, `commit` fields below index this array |
| [commits.jsonl](commits.jsonl) | Reachable headers/parents, with explicit unreviewed status |
| [repository-files.jsonl](repository-files.jsonl) | All historical paths and path/blob versions, occurrence commits, tip membership, current/main blobs and review depth |
| [history-edges.jsonl](history-edges.jsonl) | All reachable root/parent/merge changes; no rename inference |
| [ri-modules.jsonl](ri-modules.jsonl) | Every current RI/Evaluation module, physical SHA, Git blobs, 481 function/method cursors, classes, imports, resolved static call sites, tests and limitations |
| [tests.jsonl](tests.jsonl) | Exact tests, function assertions/raise statements; assertion indexing is not full fixture review |
| [subsystem-reviews.json](subsystem-reviews.json) | Substantive algorithm and quality review for twelve subsystem groups |
| [experiment-collections.jsonl](experiment-collections.jsonl) | 31 relevant research-family scopes, 606 Python algorithm/test/fixture modules and 126 captured-metadata artifacts; not 31 independent trials |
| [experiment-cases.jsonl](experiment-cases.jsonl) | All 24 dogfood cases, exact protocol/result cursors, nested artifact inventories, bounded conclusions and omitted work |
| [experiment-units.jsonl](experiment-units.jsonl) | 14,276 captured case references/arm/lane occurrences with exact artifact hash and JSON pointer; repeated references are not distinct trials or a claim of individual semantic review |
| [agent-use.json](agent-use.json) | Six original native receipt series, call IDs, source versions/spans and independent fresh hashes; long/edit source arguments reduced to size/hash, never copied raw |
| [physical-line-reproduction.json](physical-line-reproduction.json) | Actual installed-Python/maintained-API outcomes for 27 independently authored tiny fixtures |

JSONL is one record per line and UTF-8. Identities are strings unless the field
is explicitly a commit-array index. Blob equality means exact Git object bytes;
physical SHA means the observed checkout bytes. `NOT_REVIEWED` is deliberate.
Source inspection of a current blob does not inherit to prior or future blobs.
`ASSERTION_INDEXED_NOT_FULL_FIXTURE_REVIEW` preserves the important remaining
test-review boundary. A static call site is not proof that any model saw it.

Reproduce the census in the one checkout with read-only Git object operations:

```text
git for-each-ref --format=%(refname)%09%(objectname)%09%(subject)
git ls-remote origin
git ls-tree -rlz <each distinct tip>
git log --all --format=%H%x09%P%x09%aI%x09%s
git log --all --root -m --raw -z --format=@%H --no-renames --no-abbrev
git rev-list --objects --all
git cat-file --batch-check
```

Parse NUL-delimited paths rather than splitting filenames on whitespace. Include
every merge parent and root; without that, intermediate/deleted paths and
merge-resolution differences can be missed. AST call indexing resolves imports
and package reexports conservatively; local rebinding, dynamic dispatch and
instance methods require manual source tracing. No archived pickle was loaded,
historical operation replayed, source tree duplicated or unreachable object
promoted into authority.

The physical-line reproduction uses the existing tiny `_index` helper in
`tests/context/retrieval/source/test_search.py`. For each separator VT, FF, FS,
GS, RS, NEL, LS, PS and each physical newline LF, CRLF, CR, author:
`value = "a<separator>b"<newline>def target():<newline>    return 1`.
Parse with installed `ast`, build the existing source index, select `target`,
and compare its text to `ast.get_source_segment` and the existing physical-line
function materializer. Repeat with a space control. All inputs are valid Python;
no arbitrary UTF-8 coordinates or model output is manufactured.

The remaining work column in the reports takes precedence over an optimistic
interpretation of an index count. Future audits append version-specific evidence
and conclusions; they must not rewrite frozen historical scientific records.
