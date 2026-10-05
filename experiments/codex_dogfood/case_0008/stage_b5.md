# Case 0008 Stage B.5 — Blind adjudication packet

**FROZEN — treatment-free packet for a fresh Stage C adjudicator**

## Source and scope

The packet was reconstructed exclusively from the committed Stage A archive
`inputs.pkl.gz` and the allowlisted Stage A semantic treatment fields: exact
task, purpose, anchors, and obligations. Stage A is
`3eda8c6027f72a51109ed78f5684a6bbb59c65bd`; its archive SHA-256 is
`9eb0f6de7c9150390807ab872d159bbcf4c8853632b48c8395d3dd9d347be5d5`.

The Case-level history records Stage B generation recovery
`case-0008-stage-b-generation-recovery-1` (successful capture checkpoint
`348887c5e8f9969259734563319bb2d6ec715a3f`). This history is intentionally
outside the blind packet and is not a source for packet construction.

## Blind inputs

- `adjudication/blind_manifest.json` — SHA-256
  `d1096ba811f050a74a0232caa34245bc6de7f263494155e97c3e0ebbf147b6e0`
- `adjudication/blind_resources.json.gz` — SHA-256
  `cae456fa325a435de599da24a75ed3a3728d568b4bfc613b5b6851537a98c09d`

The frame is RepositoryId
`fe2c8984-a021-4342-9e31-404a6cf07707`, SnapshotId
`72a021a8a4778ffdc7f37152b5d31efb6a2ea93de82edc8c940ec76be5e641aa`, and
CorpusId
`8843f263c69d0d1b07b1fa343e63c07873827f0c3a842e7a28e50d1c8b65b93b`. The
packet contains 523 frozen resources, 11 shared anchors, and 13 obligations.
Resource address, content identity, UTF-8 content, order, and frame identity
were checked against Stage A.

## Blindness and validation

The blind manifest is constructed from a strict allowlist. Lexical queries and
results, role preferences/evidence, grounding requests/results, structural
recipe/operator choices, branching/bounds/fanout, generated outputs, and
recovery metadata are excluded. Ordinary repository text and exact task terms
are preserved as evidence.

The builder reads only Stage A files. Tests tripwire Stage B semantic paths and
production treatment imports/operations. Stage B semantic artifact contents
were not read while building or validating the packet. Stage A verification,
schema/frame validation, deterministic reconstruction, overwrite refusal,
tamper rejection, and content-identity mismatch checks passed. Focused tests
passed (8 tests); scoped Ruff and format checks passed; diff checks passed.

No treatment operation was executed. No adjudication or effectiveness analysis
was performed. Confirmation outcomes were not accessed.

## Reproduction

Run `python experiments/codex_dogfood/case_0008/build_adjudication_packet.py
verify` to reconstruct and verify the committed packet from Stage A inputs.
The `build` command refuses to overwrite either packet file.
