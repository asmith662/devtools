# increment_27: CLOSED

## Objective and method

Increment 27 tests whether repository retrieval misses come from ranking
depth, lexical representation, path evidence, or complementary inexpensive
retrieval methods. The work is experiment-local and has not changed production
retrieval. It began with one narrow baseline question: for resources already
judged useful, where does the unchanged canonical combined lexical retriever
rank them?

The depth diagnostic runs only the 24 previously executed Increment-25/26
cases. It materializes each historical parent snapshot with the Increment-25
Git snapshot machinery and uses the existing `content BM25 + 0.25 *
filename-stem BM25` retrieval operation without changing query text, scoring,
positive-result filtering, tie ordering, or corpus construction. Complete
positive rankings are retained.

## Result and decision

Closed development-only breadth checkpoint; exact results and limits remain in README.md and the breadth production-gate synthesis. Confirmation remains sealed.

## Provenance and reproduction

The manifest binds every preserved input/output byte and the committed source revision. Existing source documents contain exact datasets, baselines, configuration, commands, per-case outcomes and scientific decision rules; their original content is unchanged. Restore using the manifest before replay. No model operation or new adjudication occurred during closeout.

## Limits and subsequent work

A closed diagnostic/development checkpoint is not confirmation, a production policy or general agent competence. Unknown outcomes remain unknown. Frozen dependency-bearing originals remain in place; the root-report archive is the only compacted current-tree payload. Local packets share the SSD and do not protect against disk loss.

## Reopening

Preserve this manifest, original revision and packet. A separately authorized continuation must identify a new linked run/protocol and reason for reopening; never overwrite these results or infer an execution grant from restoration.
