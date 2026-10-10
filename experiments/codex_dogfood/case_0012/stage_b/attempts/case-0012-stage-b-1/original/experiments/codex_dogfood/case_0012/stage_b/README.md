# Case 0012 Stage B capture

Stage A is immutable at 4ff6d3950e6c0be834f136a649c1a127f91fdba3.
This directory owns the distinct Stage B TRACE.md/trace.json layer; parent traces
remain unchanged. No gold, effectiveness or final U2 outcome is produced here.

`execute` authenticates Stage A, exclusively claims execution, journals entry before
each operation and atomically persists its complete native return before continuing.
Method grounding subcalls are separately observed without changing their inputs.
`finalize` and `verify` read captured native state only and never call retrieval,
resolution or presentation again. Failed/entered calls block recovery execution.
Partial finalization accepts only identical deterministic artifact bytes.

The native graph uses trusted Python pickle inside a canonical atomic text envelope
with deterministic gzip/base85 and physical SHA-256. It is loaded only from this
own authenticated scientific capture, never from an adjudicator/untrusted packet.
Per-return pickle hashes record first serialization bytes; replay authenticates the
stored graph envelope, not repickle stability. The exclusive binary claim is a
documented experiment boundary because the existing atomic filesystem writer has
no O_EXCL creation contract. Atomic text updates reuse the native fsynced substrate;
parent-directory power-loss durability remains filesystem-dependent.

Canonical native JSON is streamed through stdlib JSONEncoder with exactly the
frozen serializer's field/type/ordering/indent/newline semantics. Fixture tests
compare full bytes and frozen projection identities. A scoped memoized identity
adapter computes the same frozen behavioral hashes without expanding the native
index graph into memory. Neither treatment functions nor frozen source are changed.
Complete native returns/provenance remain in raw_checkpoint.json; complete exact
accounts are also in exact_resolutions.json.gz. Native lexical object sections
are indexed by native_lexical.json. Canonical rows and their scores/contributions
are in lexical.json; exact-first views reference those original rows.

The neutral packet builder reads only Stage A semantics/contents; its standalone
validator uses stdlib only. Production capture verification gates its publication.
Independent processes must produce identical packet bytes before publication into
a fresh stable sterile workspace. No adjudication is performed in this checkpoint.
