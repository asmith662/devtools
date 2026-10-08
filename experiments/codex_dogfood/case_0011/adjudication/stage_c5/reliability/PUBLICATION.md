# Case 0011 C.5-R import and semantic reliability checkpoint

Primary C.5 = COMPLETE. Independent C.5-R = COMPLETE. C.5 reliability comparison
= COMPLETE. Reconciled C.5 mapping = PENDING. Stage D = BLOCKED. U1 effectiveness
= UNKNOWN. No reconciliation or Stage D was performed.

The [manual reliability review](C5_RELIABILITY_REVIEW.md) exposes every pair-label
disagreement, direct-rationale comparison, unit-status disagreement and
need-classification disagreement, plus alternatives, granularity and collective
sets. The [comparison JSON](c5_reliability_comparison.json) preserves exact metrics,
full identities, statements, both semantic rationales and owner-specific direct
set partitions. The immutable adjudication supplies all 576 pairs, 32 granularity
judgments, 18 classifications and 12 alternative audits.

## Immutable import and corrected hash authority

The authoritative source workspace is
`C:\Users\recoveryadmin\AppData\Local\Temp\case_0011_stage_c5_reliability_astra_918e90bc`.
The five artifacts below were copied byte-for-byte, with no reformatting,
reserialization, semantic-field renaming, modification or regeneration. This
publication and the comparison are outside the immutable C.5-R hash set.

| Artifact | Authoritative SHA-256 |
| --- | --- |
| c5r_v1_adjudication.json | c357ec905f38460ac66c15110296f7cd26102955ddfeabfe00cb88792ee4b888 |
| c5r_v1_validation.json | f80e6d990949995b7a88883651034ffedaebe610f56efe1232e7994295b46942 |
| c5r_v1_hashes.json | aaf48937463afae41ee13d7cf2ea6dcb88a8128e2d556da841aabc1f5da4ef27 |
| c5r_v1.py | 5f4b95b6581daf3748843f81445547aa177a9aca9ca0446ccbcc3a2160a19826 |
| test_c5r_v1.py | 24d7076918c32504dab8bb8fef2fa2581464d5d714a19b3212348aec950c7d41 |

Import initially stopped because a manually copied expected test-file hash in the
operator prompt disagreed with the artifact. The displayed copied digest was not
authoritative and was withdrawn by the operator. The independently sealed
`c5r_v1_hashes.json` ledger was first verified against its frozen SHA-256 above;
it was parsed with duplicate JSON keys rejected. Its unambiguous test-file digest
was a string of exactly 64 lowercase hexadecimal characters and matched the
actual test bytes. The sealed validation artifact was verified against its frozen
hash and its input identities, digests, adjudication digest and scientific
whitelist were consistent with the ledger. All ledger-declared input and output
file hashes were checked. No immutable scientific artifact was changed and no
semantic result was recomputed because of the correction. The withdrawn copied
value is excluded from scientific metadata.

Publication requires equality of sterile-source, authoritative expected,
repository-destination, staged Git blob-content and committed-worktree SHA-256
for every imported artifact. Git checks operate on bytes, avoiding shell text
conversion. The local Stage C.5 attributes disable text conversion for immutable
imports, deterministic comparison artifacts and the five-file neutral packet.
The import validation record states the required scopes; execution
and final commit verification are reported in the operator handoff.

## Validation scope and repeatability

The C.5-R sterile environment was reconstructed outside the repository from
exactly the five ledger-bound instruction/packet inputs and five immutable
outputs. Only `test_c5r_v1.py` ran there, independently yielding **12 passed**, with
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONDONTWRITEBYTECODE=1`, `--noconftest`,
`-p no:cacheprovider`, and `-o addopts=`. These checks verify input hashes,
576 unique pairs, 32 granularity judgments, 18 classifications, 12 alternatives,
deterministic replay, overwrite refusal and the exact scientific whitelist.
Immutable code style was not changed and is not a publication gate.

Run the explicit comparison test file with the same isolation flags. It checks
partitions, exact frame bindings, all disagreement subjects, deterministic
comparison replay, frozen publication bytes, packet double-build, neutral order,
leakage rejection, tamper detection, overwrite refusal and workspace whitelist.
The standalone `validate_packet.py` in the packet runs without repository imports.

Repository-authored code uses scoped Ruff `--isolated --select E4,E7,E9,F,I`,
Ruff formatter and strict mypy from this directory with normal import following.
These are standalone experiment scripts, not installable framework modules.
The access boundary limits validation to explicit semantic tests; the general
development profile is not invoked because this task prohibits unrelated case
and treatment access. No production code, framework API, durable framework
schema, taxonomy, package ownership or backlog status changed. Documentation
impact is confined to this case's publication and status files; historical
primary claims remain historical evidence.

## Binding and interpretation limits

The packet, manifest and primary provenance bind exactly the same case/task,
obligations, 18 need identities/statements, 32 unit identities/statements, full
576-pair Cartesian frame, and all 12 alternative memberships. Missing, duplicate
and unexpected pairs are zero. The frozen-needs and reviewed-gold identifiers
are authenticated manifest declarations; their original preimages and hashing
specification are not supplied and were not invented or recomputed.

Overall pair agreement is 544/576, but DIRECT Jaccard is only 12/22. Eleven unit
statuses, seven need classifications and six strict alternative completeness
decisions differ. The reliability conclusion is
SEVERE_ARCHITECTURE_RELEVANT_DISAGREEMENT. Neither adjudication alone is safe for
Stage D. The strict every-unit direct failure is robust as a Boolean; the exact
failed units and causal attribution remain disputed. The independent diagnostic
raises coverage from 20/32 strict to 26/32 granularity-aware, with six collective
units and seven proposed minimal sets. Proof structure is validated; semantic
sufficiency and minimality still require fresh reconciliation. Reviewed gold
and the frozen U1 rule are unchanged. No final U1 outcome is selected.

## Neutral packet and access boundary

The [reconciliation publication](../reconciliation/PUBLICATION.md) locates the
five-file packet and its sterile workspace. Positions are ordered separately
per proposition by canonical claim SHA-256; there is no stable global reviewer
number. Only [source_audit.json](source_audit.json), outside the packet, maps
positions to source roles. It must never be supplied to the fresh adjudicator.
Single-position granularity and collective claims require confirmation; no
opposing audit is fabricated. No agreed DOES_NOT_COVER pool is included.

Only permitted semantic outputs, packet inputs, case status/publication files,
repository-authored comparison files, Git metadata and operational verification
records were accessed. No prohibited file, lexical query string, analyzer term,
retrieval route/result, result resource, rank/score, acquisition cost, treatment
arm/result, Stage D outcome or confirmation data was accessed. The packet is
constructed by a semantic-field allowlist and checked for forbidden fields,
source identities, chronology and external paths. Semantic mentions of resolution
routes and reference analysis in frozen unit statements are preserved; they are
not retrieval routes or analyzer output data.

`.local/codex-result.md` is operational only, Git-ignored, outside scientific
hashes and packet evidence, and never a task obligation or information gap.
