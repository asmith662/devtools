# Case 0007 Stage B.5 — blind packet

**Packet prepared for a fresh independent Stage C session. No adjudication or
effectiveness analysis has occurred.**

## Experiment history and source

- Stage A: `e495c0af2cf57efa3a63016165b41cbba65d26a5`.
- Stage B checkpoint acknowledged: `3e22a159e65b59bffab8d83dc5c49519dd8e90b6`.
- Stage A source archive: `inputs.pkl.gz`.
- Stage A source archive SHA-256:
  `797eeb0d246f4745e5166b063b36b0dcffe84d2e2cb5fc87e36b89ae4eb2892d`.
- Stage B semantic output artifacts were not opened or deserialized.
- No production treatment operation ran while building or verifying this packet.

## Blind packet

- `adjudication/blind_manifest.json` SHA-256:
  `1367dd6840ed59ec03da3b02588ee896a64cbbe1af7415e61e7962e9a077ecb8`.
- `adjudication/blind_resources.json.gz` SHA-256:
  `b3f435ded07aef88bbb9b374788d8357870d22d6c18853b28e0fa9ce8f6cf855`.
- Frozen frame: 521 resources, 9 shared anchors, and 11 obligations.
- RepositoryId: `fe2c8984-a021-4342-9e31-404a6cf07707`.
- SnapshotId: `404104e498a8d33118b52d5bad41c0ff4a8792d4ae23a2790628b796b91f34fd`.
- CorpusId: `a2aaec768f650e9d8928fc1ed1a79eb5650472537b1d3538d740480c6a1b1f87`.

The packet was constructed with an explicit field allowlist from Stage A task
semantics and the archived snapshot resources. Resource order follows the
frozen snapshot. Repository content was retained as opaque evidence. Treatment
queries, preferences, grounding locators/results, generation recipes/operators,
bounds, candidates, and output statistics are absent from the blind files.

## Verification

- Stage A integrity and committed identities verified, including the native
  archive and frozen implementation digests.
- Reconstructed packet bytes matched both committed packet files exactly.
- All 521 frozen resource occurrences, addresses, native content identities,
  and exact archived UTF-8 contents were retained.
- Manifest and nested schemas passed allowlist checks; resource records contain
  only native occurrence identity, address, content identity, and content.
- Stage B file-access and production-treatment-operation tripwires passed.
- Rebuild refused to overwrite an existing packet; read-only verification
  remained successful and packet digests stayed unchanged.
- Tampered resource archive was rejected by deterministic reconstruction.
- Focused tests: 5 passed (`pytest --no-cov`).
- Scoped Ruff check and formatting passed. `git diff --check` and
  `git diff --cached --check` passed.

## Next step

Start a fresh GPT-6 Sol Medium session and perform blind Stage C using only:

- `experiments/codex_dogfood/case_0007/adjudication/blind_manifest.json`
- `experiments/codex_dogfood/case_0007/adjudication/blind_resources.json.gz`
