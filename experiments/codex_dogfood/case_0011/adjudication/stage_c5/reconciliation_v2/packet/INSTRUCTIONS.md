# Case 0011 C.5 reconciliation v2: bounded decisions only

This packet authorizes semantic decisions for exactly 110 supplied propositions.
It contains no reconciliation output. Do not perform Stage D or determine U1.

## Exact sterile preflight

Work only from this stable directory. Run `python -B validate_packet.py` before
opening the compressed payload. Its exact seven-file whitelist is:
`INSTRUCTIONS.md`, `packet.json.gz`, `manifest.json`, `integrity.json`,
`validate_packet.py`, `reconcile_c5_v2.py`, `test_reconcile_c5_v2.py`.
No subdirectories, .git, repository checkout, symlinks, junctions, reparse points,
prior outputs or .local directory are allowed. Stop on any failure. Do not repair
or overwrite packet bytes. Compare the printed archive, canonical payload,
manifest and integrity SHA-256 with the operator's external digest record.
Integrity is a scientific input check, not proof that a proposition is true.
Run `python -B -m unittest -v test_reconcile_c5_v2` for self-contained schema tests;
their synthetic placeholders are not semantic decisions or review evidence.

Use only the supplied task, obligations, frozen InformationNeed and reviewed-unit
semantics, alternative memberships and anonymized propositions. Do not seek a
repository checkout, source adjudications, source locations or external evidence.
Do not access lexical queries, analyzer terms, retrieval routes/results, result
resources, answer-resource paths, ranks, scores, costs, arms, model identities,
chronology, Stage D outcomes or confirmation data. Stop if exposed.

## WHY THIS PACKET DOES NOT CONTAIN 576 PAIR LABELS

Agreed pairs are inherited later by a deterministic repository-root materializer.
The reviewer is responsible only for disputed propositions. Omitted pairs must
not be adjudicated or defaulted. This packet deliberately supplies no complete
inherited mapping baseline and declares no absent-pair default.

Do not derive the final 576-pair mapping.
Do not assign labels to omitted pairs.
Do not assume omitted pairs are DOES_NOT_COVER.
Do not reconstruct source adjudications.
Do not calculate final full-frame unit/need/alternative counts.
Resolve only the 110 supplied propositions.

Do not construct complete unit, need or alternative coverage tables, Stage D
metrics or U1 outcomes. Report only decision-category counts and proposition
coverage. No unrestricted fresh adjudication is permitted.

## Scope, neutrality and decisions

Decide exactly 32 PAIR_LABEL, 12 DIRECT_RATIONALE, 11 UNIT_STATUS,
7 NEED_CLASSIFICATION, 10 ALTERNATIVE_COMPLETENESS, 32 UNIT_GRANULARITY and
6 COLLECTIVE_COVERAGE propositions: 110/110 identities, each exactly once.
Frozen semantic identities are immutable. Position numbers are assigned per
proposition by ascending canonical claim SHA-256; there is no global source
number. The single-position propositions require confirmation and have no
opposing position. Do not infer authorship or chronology.

Two-position vocabulary: ACCEPT_POSITION_1, ACCEPT_POSITION_2,
REPLACE_WITH_RECONCILED_JUDGMENT, UNRESOLVED.
Single-position vocabulary: CONFIRM_PROPOSITION,
REPLACE_WITH_RECONCILED_JUDGMENT, UNRESOLVED.
No majority voting, automatic preference for greater coverage, or automatic
preference for smaller or broader need sets. Preserve uncertainty. Strict direct
coverage remains distinct from the secondary granularity-aware diagnostic.

## Versioned closed decision schema

The executable contract is `reconcile_c5_v2.check_decisions(packet, artifact)`.
Output top-level fields, with no extras:

- schema: `case-0011-c5-reconciliation-decisions-v2`
- packet_identity: canonical payload SHA-256 from the manifest
- bindings: exact packet bindings (reviewed gold, frozen needs, reliability comparison)
- decisions: rows sorted by identity, exactly matching the manifest's 110 identities
- decision_category_counts: exact counts of decision vocabulary values, omit zero entries
- unresolved_count: exact count of UNRESOLVED rows
- method: scope `BOUNDED_110_PROPOSITION_DECISIONS_ONLY`, nonempty procedure,
  provenance `TREATMENT_BLIND_SEMANTIC_RECONCILIATION`; never name a model or source
- blindness_attestations: all eight booleans in `reconcile_c5_v2.ATTESTATIONS` true;
  if any cannot truthfully be attested, stop without publishing scientific outputs

Each row has exactly identity, kind, subject (copied from the proposition),
decision, payload and evidence_references. References are a sorted unique
nonempty list of `proposition:<identity>/position_1` and, where supplied,
`proposition:<identity>/position_2`. Acceptance must reference its chosen position.
All judgments require nonempty semantic rationale, including unresolved judgments.
Null components mean inapplicable, never an absent-pair default.

Payload fields:

- PAIR_LABEL / DIRECT_RATIONALE: label, rationale, covered_component,
  missing_component, complete_unit_counterfactual. Subject retains need and unit
  identity. Label is DIRECTLY_COVERS, PARTIALLY_COVERS, DOES_NOT_COVER or AMBIGUOUS.
  Explain sought and established facts and whether a complete need answer
  establishes the complete unit. Partial coverage requires both components.
  Otherwise components may be null only when inapplicable. Acceptance retains
  the selected label. Unresolved pair-label disputes use AMBIGUOUS; shared-DIRECT
  comparisons retain DIRECTLY_COVERS even if their rationale remains unresolved.
- UNIT_STATUS: status and rationale. Status is COVERED, PARTIAL_ONLY, UNCOVERED
  or AMBIGUOUS_ONLY. Acceptance retains selected status. Unresolved uses
  AMBIGUOUS_ONLY as an uncertainty judgment pending later consistency checks.
  Do not construct statuses for undisputed units.
- NEED_CLASSIFICATION: classification and rationale. Classification is NECESSARY,
  USEFUL_REDUNDANT, PARTIAL_ONLY, UNNECESSARY, MISFORMULATED or AMBIGUOUS.
  Acceptance retains selected classification; unresolved uses AMBIGUOUS.
  Do not infer misformulation merely from limited pairwise coverage.
- ALTERNATIVE_COMPLETENESS: strict_direct_complete (boolean; null only if
  unresolved), granularity_aware_state, rationale, members. Diagnostic state is
  FULLY_DIRECTLY_COVERED, FULLY_COVERED_ONLY_COLLECTIVELY, INCOMPLETE or AMBIGUOUS
  where supplied by any position; otherwise null. Acceptance retains the chosen
  strict value and diagnostic value where the chosen position supplies one.
  Members list exactly all frozen alternative members sorted by unit, each with
  unit and rationale. Do not combine units across alternatives.
- UNIT_GRANULARITY: classification and rationale. Classification is
  ATOMIC_FOR_NEED_MAPPING, COLLECTIVELY_COVERABLE, OVERCOMPOUND_FOR_PAIRWISE_MAPPING
  or AMBIGUOUS_GRANULARITY. Confirmation retains the proposed category;
  unresolved uses AMBIGUOUS_GRANULARITY. Do not change frozen units.
- COLLECTIVE_COVERAGE: rationale and sets. Retain every proposed set in supplied
  order (seven sets within six propositions). Each set has exactly needs
  (unchanged supplied order), classification, rationale, contributions,
  minimality_analysis. Classification is VALID_MINIMAL_COLLECTIVE_SET,
  VALID_BUT_NOT_MINIMAL, INSUFFICIENT or AMBIGUOUS. Confirmation requires all
  proposed sets VALID_MINIMAL_COLLECTIVE_SET; unresolved uses AMBIGUOUS.
  Contributions list each set member sorted by need, with need,
  distinct_contribution and removal_analysis. Explain complete sufficiency,
  distinct contributions and why removing each member does or does not lose a
  necessary fact. Replacement judges the supplied sets; it does not add sets.

No unresolved output grants permission for final materialization to invent a
label, override an agreement or silently cure an inconsistency.

## Immutable publication and replay

Keep the manual artifact in memory until validation succeeds. Call
`reconcile_c5_v2.publish(root, artifact)` from Python with this workspace as root.
It checks preflight, all schema fields, exact proposition coverage, anonymized
references and forbidden content, and double-replays deterministic bytes before
exclusive creation of exactly these three scientific outputs:
`c5_reconciliation_v2_decisions.json`, `c5_reconciliation_v2_validation.json`,
`c5_reconciliation_v2_hashes.json`. Refuse overwrite, including partial prior
publication. A failed partial write is not permission to retry or replace files.

Run `python -B reconcile_c5_v2.py --validate-completed`. This verifies the exact
ten-file scientific whitelist and recomputes all decision, validation and hash
bytes. Hashes bind decisions and validation; record the hashes-file digest
externally to avoid recursive self-hashing. Packet hashes remain unchanged.

Only after scientific whitelist validation succeeds may the operational
`.local/codex-result.md` handoff be created. It is excluded from scientific hashes,
packets and evidence; never treat it as an obligation, InformationNeed, witness,
required resource or gap. After creating it, rerun scientific validation only on
an exact ten-file copy without the operational handoff. Do not import an
unvalidated artifact. Report decisions only and stop for repository-root import.
