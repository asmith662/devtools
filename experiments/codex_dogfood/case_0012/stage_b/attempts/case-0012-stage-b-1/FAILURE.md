# Permanently aborted Case 0012 Stage B attempt 1

Execution: `case-0012-stage-b-1`. Stage A:
`4ff6d3950e6c0be834f136a649c1a127f91fdba3`. Scientific disposition:
ABORTED_CAPTURE_INFRASTRUCTURE_FAILURE. Effectiveness: NOT_EVALUABLE.
Authoritative use: AUDIT_ONLY.

Original scientific failure artifacts and capture sources are preserved under
`original/` byte for byte. `inventory.json` records every originally untracked
Stage B file and packet builder: relative path, byte size, SHA-256, modification
time. `audit.json` binds frame, operation history and previously exposed mechanics.
The original source location was removed only after copied hashes were verified.
The ignored operational backup is not part of this scientific record.

| Sequence | Operation | Entered | Actual return | Durable return |
| --- | --- | --- | --- | --- |
| 1 | index-build | 1 | 1 | 1 |
| 2 | lexical:global | 1 | 1 | 1 |
| 3 | lexical:source | 1 | 1 | 1 |
| 4 | lexical:choices | 1 | 1 | 1 |
| 5 | lexical:integrity | 1 | 1 | 1 |
| 6 | lexical:materialization | 1 | 1 | 0 |

No identity occurs twice. Four lexical returns plus index are recoverable.
Materialization remains ENTERED in durable state; its missing value is never
inferred. The disclosed traceback reached the post-return `Journal.call` save
after `result = invoke()`, returned status and serialization digest computation.
Native `filesystem.writing._atomic_write` attempted `os.replace` of a sibling
temporary file onto `raw_checkpoint.json`. PermissionError [WinError 5] became
FilesystemPermissionError. This is a returned-value capture/publication failure,
not a failed native lexical operation. A Windows reader without delete sharing is
a possible contributor; the exact locking handle was not established.

Exact routes = 0; grounding subcalls = 0; presentation calls = 0; arm assemblies
= 0; Stage C = not performed; gold absent. No operation was retried.

Attempt-1 outputs MUST NOT be joined with attempt 2 to form official treatments.
They MUST NOT receive gold labels or contribute to effectiveness metrics. The
four overlapping deterministic returns MAY be used solely for replay/consistency
comparison against fresh attempt 2. Attempt 1 is immutable, cannot be resumed,
and remains recoverable in Git history.
