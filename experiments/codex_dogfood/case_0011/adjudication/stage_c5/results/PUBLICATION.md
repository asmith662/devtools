# Primary Case 0011 Stage C.5 publication

Current status: independent C.5-R and the reliability comparison are COMPLETE.
The [reliability checkpoint](../reliability/PUBLICATION.md) reports severe
architecture-relevant disagreement and prepares a neutral reconciliation packet.
Reconciled C.5 mapping is PENDING; Stage D remains BLOCKED; U1 effectiveness is
UNKNOWN. The primary-checkpoint account below is historical, including its
then-pending independent review. Its immutable artifacts and claims are preserved.

Primary C.5 semantic mapping is COMPLETE and immutable. The independently
reviewed C.5-R adjudication is PENDING; a reviewed/reconciled C.5 mapping is NOT
AVAILABLE. Stage D is BLOCKED. U1 effectiveness is UNKNOWN. This primary result
is not final architecture-grade truth.

## Frozen artifacts and validation

The nine imported artifacts are byte-for-byte copies from the authoritative
primary workspace
`C:\Users\recoveryadmin\AppData\Local\Temp\case_0011_stage_c5_sterile_5ade1674`.
The import preserves bytes without reserialization or formatting. This
repository-authored publication is outside the immutable output hash set. The
exact source SHA-256 values are:

| Artifact | SHA-256 |
| --- | --- |
| `c5_mappings_v1.json` | `34313eec3f4e0c312bf3de2923f3bbe91fd1bdb0d566163d324720c24cf6afaf` |
| `c5_unit_coverage_v1.json` | `2065848e47af40899fe6c9a6af9a394c4eb1a14292bffdbc92847421214722a6` |
| `c5_need_classifications_v1.json` | `9a9745f0e0503012b42d6d10a302c50999ddcb3a55b74272c977f5ac78ac516f` |
| `c5_statistics_v1.json` | `d29177945ff226a0985a3b9e412d8d7406f85075ef97619e88117ee92571d086` |
| `c5_method_provenance_v1.json` | `0056d7e26bff312294c866c0884d49e7ea80d3574d471be4fb0726f7fb94d43c` |
| `c5_validation_v1.json` | `3f19b37e406cfa339b4cca9052046ce314a70ee47e86ab98bdf12bfc81a9818c` |
| `c5_output_digests_v1.json` | `ebcaf209e76a87f6484738a3db3cd620c11521d5124aa2df0a37c8e0942f0188` |
| `adjudicate_c5_v1.py` | `a43af6d73fe3f5eb4124e55516c3602ae3fce1ad667e326387ef4801a9a2e215` |
| `test_c5_v1.py` | `5f56260f3b65361822eab9dc9088d82ed39590d4909d9dd21ab0841c257c07f8` |

Validation requires equality of source, expected, repository destination, staged
Git blob content and committed worktree SHA-256 for every listed artifact.
Primary validation reconstructs a separate sterile workspace from the four
frozen packet inputs and nine immutable outputs, then runs only the explicit
`test_c5_v1.py` with plugin autoload and bytecode generation disabled. Its
scientific whitelist excludes `.local/codex-result.md`.

## Primary semantic results

The frame contains 18 InformationNeeds, 32 reviewed required units and all 576
need/unit pairs. Duplicate, missing and unexpected pairs are zero; every need is
classified and every unit accounted for.

| Mapping label | Count |
| --- | ---: |
| `DIRECTLY_COVERS` | 13 |
| `PARTIALLY_COVERS` | 59 |
| `DOES_NOT_COVER` | 504 |
| `AMBIGUOUS` | 0 |

| Unit coverage | Count |
| --- | ---: |
| `COVERED` | 13 |
| `PARTIAL_ONLY` | 17 |
| `UNCOVERED` | 2 |
| `AMBIGUOUS_ONLY` | 0 |

| Need classification | Count |
| --- | ---: |
| `NECESSARY` | 9 |
| `USEFUL_REDUNDANT` | 0 |
| `PARTIAL_ONLY` | 9 |
| `UNNECESSARY` | 0 |
| `MISFORMULATED` | 0 |
| `AMBIGUOUS` | 0 |

No witness alternative has every member directly covered. This is a semantic
coverage result and says nothing about retrieval or U1 effectiveness.

The two uncovered unit statements are preserved exactly:

1. `Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values.`
2. `Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference.`

The result supports INFORMATION-NEED COVERAGE FAILURE. It does not yet
distinguish conclusively between UNDER-DECOMPOSED / UNDER-SPECIFIED INFORMATION
NEEDS and NEED-TO-UNIT GRANULARITY MISMATCH: a reviewed required unit can combine
several semantic contracts while an InformationNeed intentionally asks a narrow
question. Do not assign INFORMATION_NEED_AUTHORING_DEFECT before independent
reliability and granularity review.

## Independent review boundary

The separate C.5-R workspace contains only `C5_INSTRUCTIONS.md`,
`manifest.json`, `packet.json.gz`, `integrity.json`, and `C5_R_INSTRUCTIONS.md`.
It contains the same four frozen C.5 packet inputs byte-for-byte. It contains no
primary judgments or results. The independent adjudicator must freeze its own
full mapping, unit coverage, need classifications, alternative coverage,
granularity audit and collective-coverage diagnostics before any comparison.
Comparison is deferred. The granularity and collective-coverage audits are
supplementary and cannot change the frozen gold or direct-coverage rule.

Treatment wiring was previously exposed to the construction operator, as
recorded in the existing access disclosure. This import/preparation did not
access treatment files, arm wiring, retrieval outputs, or confirmation data.
The independent reviewer receives only the sterile packet. No Stage D work was
performed.
