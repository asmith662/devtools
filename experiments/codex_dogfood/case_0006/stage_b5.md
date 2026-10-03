# Case 0006 Stage B.5

**TREATMENT-FREE BLIND PACKET FROZEN. No adjudication or effectiveness analysis has been performed.**

Stage A treatment: `e7aed4162672dd859a0a8a33a2b718dda8425495`.
Stage B recovery protocol: `56f18901b5acae47b9c07811dd18eb4770c56285`; recovery capture: `aae9da9741924dfa599b55b4fb913163caf96131`; recovery identity: `case-0006-stage-b-recovery-1`. This recovery provenance is recorded only in this Case history file, outside the blind packet. The packet was built only from the digest-verified Stage A `inputs.pkl.gz` archive and explicit task-semantics allowlists. Stage B semantic result artifacts were not opened or deserialized by the packet builder or during this Stage B.5 work.
Stage A native archive SHA-256: `572b8a575e08fc0012871bbddcbe780b026be03bdca670e607a9f09988ccd402`.

## Blind packet

- `adjudication/blind_manifest.json` SHA-256: `8bf0559814df54c246514e56fb7d92937828f9e50f9e17620a2c1acdc2934b49`.
- `adjudication/blind_resources.json.gz` SHA-256: `a03cdd8dc39d56b4a719be43ca38f2ced8f4df6e0b304ec8187914040b3ebb2a`.
- RepositoryId: `d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8`.
- RepositorySnapshotId: `ba654221b65584aebdd98804369864162ac3f7da1bf8862abee06ce4d2127a55`.
- Eligible frame identity: `49c69d2db7c6616731d9c24519a48d47a13a2ee991d46aaaf33d1f5d55b212b9`.
- Frame: 531 resources; manifest includes 10 shared anchors and all 10 frozen obligations.

The manifest projects only case/task identity, exact task and purpose, repository/snapshot/frame identity, anchors with task provenance, obligations with predicates/references/status/applicability/criteria and pre-execution witness information, neutral adjudication instructions, and the resource archive digest. The resource archive preserves exactly the 531 native frozen resource occurrences in frame order, with occurrence identity (address plus content identity), address, content identity, and exact UTF-8 content.

Lexical query treatment, role treatment, grounding requests/locators/results, generation recipes/operators/results, ranks/scores/positions, support attachments, and recovery metadata are excluded from blind metadata. Repository content remains opaque and unmodified.

## Integrity and overwrite checks

The builder verified Stage A artifact/source/archive digests and repository/snapshot/corpus bindings before projection. Read-only packet verification confirmed strict schema allowlists, no forbidden treatment fields in packet structure, 531/531 exact address/content-identity/content correspondence, and deterministic reconstruction from the Stage A archive. A second build refused before replacing either packet file; both packet hashes remained unchanged, and read-only verification still passed.

An initial builder preflight used the Stage A checkpoint hash where the frozen manifest records its source snapshot HEAD; it stopped before packet creation. The check was corrected to verify the committed Stage A integrity-manifest digest and frozen source snapshot identity. No production treatment ran during this correction.

Builder: `build_adjudication_packet.py`. Focused schema/overwrite tests: 4 passed. Scoped Ruff and Ruff format checks passed. No production treatment operation ran; no production source changed. Confirmation outcomes were not accessed.
