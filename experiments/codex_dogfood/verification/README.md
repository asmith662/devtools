# Sealed and deep experiment verification

Normal verification is the standard downstream integrity path. Deep verification
may be expensive: it re-establishes raw native/canonical semantic correspondence.
A normal PASS means **capture-time deep proof = AUTHENTICATED**; it does not claim
that deep correspondence was re-executed.

This non-installable experiment package depends on existing experiment owners and
`devtools`. It adds no production Retrieval, Repository Intelligence, Context
Planning, Localization, persistence or universal Evaluation APIs.

## Proof boundary and authority

1. **Capture/deep proof** authenticates the journal, native and canonical returns,
   aliases/order/types/frame/runtime and scientific construction. Future capture
   owners call `proof.publish_proof` after authenticating their inputs. It invokes
   the strong proof once and refuses publication unless every required check
   passes. The proof binds exact input digests, proof implementation digests,
   exact result bytes, completion identity and canonical scientific artifacts.
2. **Normal downstream verification** authenticates the authoritative proof digest,
   the bound inputs and implementation, loads canonical scientific surfaces,
   authenticates primary/gold once, reconstructs downstream metrics and gates,
   executes downstream semantic/adversarial checks once and compares exact bytes.
   It does not decode raw native archives. Missing/unknown proof fails explicitly;
   it never silently falls back to forensic replay.
3. **Deep forensic replay** independently authenticates raw native/canonical
   correspondence, including shared pickle memo/alias and ordered field semantics.
   It is explicit, timed, configurable and emits progress.

A proof is not self-authenticating. Its digest must be anchored in an accepted
immutable capture publication/authoritative commit. Hashes do not independently
prove that arbitrary code executed: the trusted capture producer and its exact
implementation are part of the experimental provenance. A mutable PASS summary,
mtime, filename, earlier verifier output or unanchored proof cannot establish
trust. Each invocation authenticates authoritative bytes afresh.

Future `CompletionBindings` retains immutable canonical bytes identifying case,
execution, Repository/Snapshot/Corpus frame, protocol, schedule, journal chain,
native archive scope, canonical artifact scope, scientific source implementations,
deep verifier implementation and existing completion seal. The proof separately
hashes exact deep-result bytes and the binding document. Publication is exclusive;
the authoritative outer publication anchors the proof digest. The existing seal
is an input, avoiding a self-referential hash cycle. Capture/consumer owners must
authenticate actual inputs against those digests; this codec does not invent their
scientific validation or authorize a new capture. No new capture is run here.

## Audited Case 0016 compatibility

Case 0016 predates the explicit proof schema. `completion.authenticate` accepts
only the existing seal `b94bcd6d...9d734b0`, anchored at authoritative treatment
commit `4925f8896edc49b6162d191a6d348f78dd958a48`. Its historical evidence suffices
because the sealed producer has an audited unconditional publication invariant:

- `reporting.publish` calls `derived` before publishing any derived artifacts or
  `integrity.json`; overwrite refusal and exclusive writes protect publication.
- `derived` calls `reconstruct`, which calls the inherited `Journal.load`, checks
  completion, source/frame/schedule and all captured scientific algebra.
- `Journal.load` authenticates the claim, context, ENTERED/RETURNED chain and
  frame/runtime, decodes the ordered shared-memo native segments and compares
  exact native descriptions with canonical archives before returning.
- Only after successful construction does the producer publish validation,
  canonical scientific artifacts and the outer integrity seal. The seal binds
  all 1,888 files and all 40 capture implementation files, including the producer,
  journal loader, native graph descriptor and artifact codec. The execution
  marker also binds 172 scientific implementations through the amended Stage A.

The completion seal alone is insufficient: it precedes scientific reconstruction
and binds execution/order/chain, not its later validation. The compatibility proof
uses the accepted outer publication together with its exact producer control flow,
validation bytes and complete native/canonical artifact manifest. It is a bounded
compatibility rule for this exact accepted capture, not inference from an arbitrary
old manifest. Stage D checkpoint authentication verifies its accepted Git blob,
ancestry, original/amended Stage A, recovery, failed-attempt isolation and gold.

The chain is acyclic: Stage A/source/protocol -> claim/marker -> context/events ->
execution completion -> deep reconstruction -> validation/canonical publication ->
outer integrity -> accepted Git checkpoint -> downstream result. The adapter
checks physical hashes, source bindings, every journal envelope/order/input/chain,
completion identity and trace artifact bindings without deserializing native state.
It neither republishes nor modifies historical scientific artifacts.

## Invocation ownership and commands

`Invocation.authenticate` returns frozen `AuthenticatedInputs` containing canonical
Stage D inputs, primary gold and an immutable authenticated completion binding.
Nested historical data is read-only by contract. Native journal is absent in normal
mode. Metrics/enrichment/Markdown are constructed once, baseline and five Stage D
adversarial checks execute once each, then seven expected artifacts are compared.
No global or persisted trusted cache exists. Switching proof levels requires a new
invocation. Deep-only native memos and exact resource/state/pair/member indices,
graph-row ordering and UTF-8 span caches remain available to forensic replay.

Run the managed, bounded public entry point from the repository:

```text
python -m experiments.codex_dogfood.verification.bounded verify OUTPUT.json
python -m experiments.codex_dogfood.verification.bounded deep OUTPUT.json --deep-limit 120
```

`verify` has a 60-second hard wall. Deep mode defaults to 120 seconds, accepts an
explicit positive bound and never retries a timeout. Both refuse an existing result
path and persist phase progress. The `case_0016` module is the child/API implementation;
use `bounded` for operational runs. `gold`, `native`, `probe`, `probe-profile` and
`construction` are explicit diagnostics; construction alone is not journal proof.
The sealed historical entry points remain historical implementations, not the new
standard downstream command.

The earlier incomplete repair and decode/alias investigation remain in
[engineering diagnostics](../../performance/retrieval/verifier_repair/). Their
180-second failure and later microbenchmark gate failure are preserved as history.
The parse-once, block-decode-once, immutable-closure byte templates, exact alias
relocation, source-span and graph-row optimizations remain for deep fixtures and
forensics. They are superseded as a normal-verification performance strategy.

Focused tests cover sealed tampering, exact future proof input/result bindings,
failed-proof publication and overwrite refusal, fresh invocation authentication,
zero normal native decode, small deep mismatch/alias/type/order fixtures, exact
seven Stage D bytes and unchanged 3,084 cells, 36 REQUIRED results, 22 witnesses,
gates and GRAPH_HARMFUL. Full Case 0016 deep replay is not ordinary validation.
