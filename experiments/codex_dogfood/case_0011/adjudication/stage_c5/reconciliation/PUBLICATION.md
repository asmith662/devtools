# Case 0011 neutral C.5 reconciliation preparation

This checkpoint prepares review inputs only. Reconciled C.5 mapping = PENDING.
Stage D = BLOCKED. U1 effectiveness = UNKNOWN. No reconciliation was performed.

The fresh adjudicator receives only the [five-file packet](packet/INSTRUCTIONS.md),
never the comparison publication, source audit, model metadata or chronology.

Sterile workspace: `C:\Users\RECOVE~1\AppData\Local\Temp\case_0011_c5_reconciliation_final_z8s60abm`.

Exact files: `INSTRUCTIONS.md`, `packet.json.gz`, `manifest.json`,
`integrity.json`, `validate_packet.py`.

| Digest scope | SHA-256 |
| --- | --- |
| Archive | da7caf25860f4803838e850f7b3d06d696e95a50ab39cc4ee2635e794961f550 |
| Canonical payload | 4f5357b3c35eec80c338c03559bf4a1f97e9d34746a77291af9d18365100a2a9 |
| Manifest | a753ec0fa40818fd236ff980bca0724390661f73a9704fe0cbdb8a72527d57c8 |
| Integrity record | a88d5a22e19b2b1ce8366c2bb25ff7954066921352e2f8024e4d014bf6e419db |

The archive and canonical payload digests are distinct and both verified.
The integrity record binds the manifest and every other packet file; its own
external digest is above. Exact files are byte-identical in the repository and
sterile workspace. Double-build, overwrite refusal, no-leakage, source-ordering,
frame bindings, proposition coverage and exact whitelist checks pass.

There are 110 propositions: 32 pair-label disputes, 12 agreed-direct rationale
comparisons, 11 unit-status disputes, seven need-classification disputes,
10 alternative member/completeness disputes, 32 granularity propositions and
six collective-set propositions. All 12 alternatives remain in the semantic
frame. Alternative disputes include changed member causes even when aggregate
incompleteness agrees. No agreed DOES_NOT_COVER mappings inflate the packet.

Two competing positions are numbered separately by ascending canonical claim
SHA-256; no global reviewer position exists. Single-position granularity and
collective audits are unconfirmed propositions, not fabricated disputes.
The role mapping is retained only in
[the outside-packet source audit](../reliability/source_audit.json).
Do not supply that audit or this publication to the fresh reviewer.

Every two-position decision permits ACCEPT_POSITION_1, ACCEPT_POSITION_2,
REPLACE_WITH_RECONCILED_JUDGMENT and UNRESOLVED. Every granularity category remains
available. Collective claims require explicit sufficiency and minimality reasons
for each member. No majority voting or preference for greater coverage or smaller
or broader need sets is allowed. The frozen direct rule remains separate from
the secondary granularity-aware diagnostic; no reviewed unit is altered.

The packet exposes only task, obligation, InformationNeed and reviewed-unit
semantics, alternatives, anonymized claims/rationales, granularity and collective
propositions. Author/provenance/model/chronology metadata and treatment fields are
excluded by projection. Negative tests reject injected forbidden fields, source
identities, paths, reordered positions, changed bytes and unexpected files.
No treatment or confirmation data was accessed in preparing this checkpoint.

Next step: Start a fresh treatment-blind C.5 reconciliation session from the
prepared sterile workspace and resolve only anonymized mapping, coverage, need
classification, granularity and collective-coverage disagreements.

The operational `.local/codex-result.md` handoff is excluded from scientific
hashes, packets and evidence. No result exists in this prepared workspace yet.
