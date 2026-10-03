# Case 0005 Stage B capture

**STAGE B CAPTURED — NOT ADJUDICATED.**

Stage A checkpoint: `e9764cde6dc6c2f379e4b08561974cd6b59c30d3`.
The six frozen Stage A artifact digests, exact committed artifact bytes and
production implementation bindings passed preflight. The documented Stage A
validator passed before any production acquisition/routing call. The starting
worktree and index were clean. No treatment or native input was changed.

[capture.py](capture.py) loaded the digest-verified [inputs.pkl.gz](inputs.pkl.gz)
and called `acquire_localization_lexical_evidence(native["request"])` exactly
once. It then called `route_localization_lexical_evidence(acquisition,
native["role_evidence"], native["preferences"])` exactly once over that exact
acquisition. It did not rebuild the snapshot, corpus, index, role evidence or
preferences. No additional lexical query or routing variant ran.

| Frozen output | SHA-256 |
| --- | --- |
| [capture.pkl.gz](capture.pkl.gz) | `92bd11162fc11ddc75af6e6535c10eadd50bf62701f44100e049d37353cd315a` |
| [retrieval.json](retrieval.json) | `b234079844a6d4f46793c08730c7c577213c003fadbcb511793272c8ce1ddd67` |
| [routing.json](routing.json) | `315836a83a12f5ffe263ad238796f4e2dd8fa82680752b6720bb2ac2e4a794dd` |

The native archive retains exact acquisition and routed objects, the frozen
request, role view and preferences, source digests, identity fields and timing.
The JSON files project exact native query/match order, one-based native ranks,
scores, content/filename contributions and supporting observations, and the
separate two-tier routed presentation with role-support provenance. No
usefulness, witness, applicability, satisfaction or effectiveness field exists.

The retained frame has 515 resource identities. Capture has ten native lexical
lanes (one unchanged global and nine obligation lanes) and nine independent
routed obligation views. The recorded monotonic runtimes were
`0.12892299999657553` seconds for lexical acquisition and
`0.28254759999981616` seconds for routing. They are execution observations,
not performance conclusions.

Read-only correspondence verification confirmed all ten exact query/order and
result bindings, all nine exact preference and routed-lane bindings, exact
serialized scores/contributions and provenance, immutable global-result object
identity, complete candidate retention, unique native ranks, native order
within both tiers, OR qualification from frozen positive role evidence, exact
support references, and empty-preference native-order invariance. The output
cross-references agree on Stage A, task, repository, snapshot and corpus.

Run read-only verification with:

```text
uv run python experiments/codex_dogfood/case_0005/capture.py --verify
```

The verifier compares canonical LF JSON bytes, accommodating a Windows CRLF
checkout while retaining the SHA-256 identities of the committed JSON. It
never reruns lexical acquisition or routing.

The capture command refuses any existing Stage B output before acquisition or
routing. A guarded second invocation raised `FileExistsError` without changing
artifact bytes. Scoped tests in [test_capture.py](test_capture.py) disable both
production execution functions while checking correspondence, overwrite
protection, tamper rejection, checkout line endings and
empty-preference/global preservation. All five scoped tests passed; Ruff lint,
format and diff checks passed.

No independent blind resource adjudication or joined analysis has occurred.
Confirmation remains sealed. The next step is a separate, treatment-free blind
packet construction checkpoint, followed by Stage C in a fresh session. The
packet must hide lexical queries and output, caller role preferences, role
assignments, routing tiers and routed positions.
