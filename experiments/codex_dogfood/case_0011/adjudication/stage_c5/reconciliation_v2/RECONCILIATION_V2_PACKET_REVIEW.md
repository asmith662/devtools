# Case 0011 C.5 reconciliation v2 packet review

This repository-authored review is outside the sterile packet. Reconciliation
v2 packet = PREPARED; adjudication = NOT PERFORMED. Final reviewed C.5 mapping =
NOT AVAILABLE. Stage D = BLOCKED. U1 effectiveness = UNKNOWN.

## Why decisions only

[V1 erratum](V1_CONTRACT_ERRATUM.md): EXPERIMENTAL_CONTRACT_DEFECT, zero decisions.
The v1 bounded evidence exposes 50/576 distinct pair labels and omits 526, without
a baseline or absent-pair default. V2 resolves exactly the same propositions and
does not require the reviewer to produce unavailable full-frame values.

| Proposition category | Count |
| --- | ---: |
| PAIR_LABEL | 32 |
| DIRECT_RATIONALE | 12 |
| UNIT_STATUS | 11 |
| NEED_CLASSIFICATION | 7 |
| ALTERNATIVE_COMPLETENESS | 10 |
| UNIT_GRANULARITY | 32 |
| COLLECTIVE_COVERAGE | 6 |
| Total | 110 |

The collective propositions contain seven proposed sets; there are still exactly
six proposition decisions, with explicit payload judgments for every set.

## Reviewer contract and visible evidence

The reviewer sees only [seven packet files](packet/INSTRUCTIONS.md): instructions,
compressed blinded semantics/propositions, manifest, integrity record, standalone
validator, bounded decision validator/replay code and self-contained synthetic
schema tests. The exact whitelist excludes directories and operational handoffs.
Frozen task, obligations, 18 needs, 32 units and 12 alternatives provide semantic
context, not a complete inherited pair mapping. Existing source-neutral ordering
uses canonical claim digests separately for each proposition. Single-position
granularity and collective claims are propositions requiring confirmation.

The reviewer sees no source-role mapping, model identity, chronology, lexical
queries, analyzer terms, retrieval routes/results, result resources, answer paths,
ranks, scores, acquisition costs, arm identities, Stage D outcomes or confirmation
data. The builder reads only the existing blinded packet and the reliability
comparison bytes to compute its binding; it does not load source adjudications.

[Executable decision schema](packet/reconcile_c5_v2.py) uses version
`case-0011-c5-reconciliation-decisions-v2`. It binds packet identity, reviewed gold,
frozen needs and reliability comparison. Exactly 110 rows retain original kind,
subject and identity, one permitted decision, complete category-specific rationale
payload and supplied anonymized references. Counts, unresolved count, method and
blindness attestations are required. Accepted positions retain their values.
Replacement and unresolved decisions must preserve the bounded subject and
explicit uncertainty. Shared DIRECT labels cannot be changed by rationale review.
No full mapping or absent-pair default field is allowed. Closed output schemas
reject additional fields and all identities outside the supplied propositions.

Publication exclusively creates decisions, validation and hashes JSON files and
replays them deterministically. Synthetic schema fixtures are test-only values,
never scientific reconciliation outputs. No real decisions are created here.
Only after exact scientific whitelist validation may an operational handoff be
created; it is outside hashes, packets, evidence, obligations, needs and gaps.

## Later repository-root materialization

This checkpoint does not implement final materialization. A separate authorized
checkpoint after immutable v2 import must use both complete 576-pair mappings,
exact pair-agreement partitions, an exact agreed-pair inheritance seal, bounded
v2 decisions and the frozen unit/alternative frame. Before applying decisions,
verify all source digests, exact frame identities, and that the partition is
disjoint and exhaustive. Construct and seal a canonical sorted list of every
agreed pair's identity and label. The seal is not supplied as omitted labels to
the sterile reviewer. The current comparison records 544 agreed labels and 32
disputed labels; the 12 shared-DIRECT comparisons refine rationales only.

Inherit all agreed labels exactly. Apply reconciled label decisions only to the
32 disputed pairs. Retain shared-DIRECT rationale decisions without overriding
their agreed label. Derive all 32 unit statuses from the complete final pair
matrix, using direct before partial before ambiguous before uncovered. Check the
11 reconciled status judgments against those derived values; never silently
override either side of an inconsistency.

Derive all 18 need classifications from final mappings plus reconciled semantic
classification decisions (including formulation judgments). Apply the 32
granularity decisions and all semantically validated collective sets. Derive all
12 strict alternative states and all 12 granularity-aware alternative states from
frozen ALL-complementary memberships, keeping ANY-alternative logic separate.
Check disputed classification and alternative judgments against the derived
state. Unresolved or inconsistent judgments require an explicit later stop or
authorized resolution, never an invented default or strengthened claim.

Retain per-value provenance: INHERITED_AGREEMENT, RECONCILED_DISPUTE,
RECONCILED_SINGLE_POSITION. Derived aggregates must retain their contributing
pair/decision references and provenance categories; do not assign a single source
label that hides mixed origins. Prove exactly 576 pair mappings, 32 unit statuses,
18 need classifications, 12 strict and 12 granularity-aware alternative states,
with zero duplicate, missing or unexpected identities. Full-state consistency
and unresolved checks precede any authorization to proceed to Stage D. U1 remains
unknown until a separately authorized later analysis.

## Validation and documentation impact

Standalone checks cover hashes, canonical payload, frame, proposition identities,
categories, source neutrality, forbidden fields, treatment leakage and whitelist.
Tests reproduce the v1 omission defect, prove unchanged scientific propositions,
double-build determinism, bounded output schema, no full mapping, no absent-pair
default, replay and overwrite refusal. Exact file hashes and stable workspace are
published in [validation.json](validation.json).

This is bounded experiment protocol repair. No production source, reusable
primitive, package ownership, dependency direction, taxonomy, durable framework
schema, primary C.5 or independent C.5-R is changed. Case status and this versioned
review own current claims; the documentation map, architecture, backlog and
historical ledger need no changes. V1 history remains preserved.

Next step: Start a fresh treatment-blind reconciliation-v2 session from the
prepared stable sterile workspace and resolve only the 110 anonymized propositions.
Produce bounded reconciliation decisions only. Do not construct the complete
576-pair mapping and do not assign defaults to omitted pairs.
