# Case 0015 metadata-only capture recovery

Original scientific authority remains Stage A commit
`d7e28de0e103bdf0e494a0156311fa1c14b6c9f8`. Every sealed Stage A artifact and
implementation stays byte-identical. No task, field, query, parameter, statistical,
score, tie, gate or gold semantics change.

Attempt `case-0015-stage-b-1` is FAILED_AUDIT_ONLY. Its immutable events establish
two returns followed by `index:native-prepare` FAILED_NO_RETURN. No treatment or
reference executed. The local native builder returned before the enormous
`repr(...).encode()` allocation failed; operation 3's return is unrecoverable.
The attempt must never resume. This is an operational capture/fingerprint defect,
not an R2 scientific failure or effectiveness result. `attempt1_sources/` preserves
the exact capture sources bound by that failed start claim, for audit only.

The capture-only amendment lives in the sibling Stage B package. `fingerprint.py`
streams domain-separated schema `case-0015-field-state-fingerprint-v2`. Each record
has an eight-byte big-endian arity, followed by typed, length-prefixed UTF-8 scalar
values (integers decimal; floats lossless hex). Records retain exact frame and
document identities/order/text, all canonical field observations and coordinates,
document lengths, ordered tf/observation groups, field N/averages/df, and ordered
postings referencing canonical document positions. Global document statistics are
never expanded per posting. Memory is bounded by a scalar/resource record and a
document-position map; work is proportional to retained compact state.

The frozen scorer imports its old repr validator. The adapter binds the identical
frozen function code, closure and defaults to a globals mapping differing only in
`validate_state`, pointing to bounded metadata validation. It does not patch
production or the frozen module, change arithmetic, or rank intermediate stages.
Synthetic tests prove exact result identity, mutations, forbidden rich repr,
incremental encoding and a generous tracemalloc bound independent of machine RSS.

`records.py` owns stable `PreparedFrame` and `PreparedFields` imported types,
schemas `case-0015-prepared-frame-v2` and `case-0015-prepared-fields-v2`. A real
synthetic `python -m` writer and independent reader validate durable replay.
`legacy.py` temporarily binds original `__main__` types solely for read-only
authentication of attempt 1, restores prior bindings, and refuses all other
attempt identities. Attempt 2 uses native stable imported identities.

The recovery checkpoint includes no successful capture, packet, sterile workspace,
gold, effectiveness or outcome. Stage C drafts are strict allowlist infrastructure;
actual packet construction requires successful committed attempt 2. The new attempt
executes its own complete 17-operation schedule, exclusively, with initial counts
zero. It binds both original Stage A and the recovery checkpoint and may never
reuse failed-attempt returns or retry a failed operation.

Ownership is experiment-local capture metadata and factual failed audit. Dependents
are Case 0015 capture/replay/publication only; dependencies point to canonical
`devtools` primitives and existing experiment durability. No reusable framework
type, production interface, architecture decision or backlog resolution is added.
Documentation impact is owned here and in separate case STATUS; frozen historical
Stage A documents remain intact. Confirmation/reserve are NOT_ACCESSED.
