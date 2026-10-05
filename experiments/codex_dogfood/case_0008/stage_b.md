# Case 0008 Stage B — generation-only recovery

**CAPTURED VIA GENERATION-ONLY RECOVERY — NOT ADJUDICATED**

Execution identity: `2fed596a-f43d-4d35-9e32-e8a609366a6f`.
Repository / snapshot / corpus: `fe2c8984-a021-4342-9e31-404a6cf07707` / `72a021a8a4778ffdc7f37152b5d31efb6a2ea93de82edc8c940ec76be5e641aa` / `8843f263c69d0d1b07b1fa343e63c07873827f0c3a842e7a28e50d1c8b65b93b`.

## Invocation accounting

Attempt 1 failed during candidate-association alias validation before any projection. The frozen recovery used the original durable lexical, routing, and grounding capture; none was rerun. One combined generation API call returned and was durably captured before correspondence validation and canonicalization.
Recovery identity: `case-0008-stage-b-generation-recovery-1`; prior failed attempts: 1; successful recovery call: 1 (1316.840868s).

- lexical: 1 invocation(s), 1.360410s
- routing: 1 invocation(s), 1.665974s
- grounding:g-assessment: 1 invocation(s), 0.335915s
- grounding:g-candidate: 1 invocation(s), 0.163981s
- grounding:g-generation: 1 invocation(s), 0.025897s
- grounding:g-grounding: 1 invocation(s), 0.024052s
- grounding:g-witness-set: 1 invocation(s), 0.023612s
- grounding:g-supported-witness: 1 invocation(s), 0.023747s
- grounding:g-task: 1 invocation(s), 0.022368s
- grounding:g-obligation: 1 invocation(s), 0.023386s
- grounding:g-readiness: 1 invocation(s), 0.026976s
- grounding:g-evidence: 1 invocation(s), 0.022627s
- grounding:g-package: 1 invocation(s), 0.022566s
- generation: 1 invocation(s), 1316.840868s

## Mechanical generation counts

```json
{
  "branching_children": 19,
  "branching_families": 14,
  "family_outcomes": {
    "DIRECT_IMPORT_DEPENDENCY_RESOURCE": {
      "children": 7,
      "dispositions": {
        "GENERATED": 3,
        "NO_TARGET": 3
      },
      "duplicate_branch_failures": 0,
      "families": 6,
      "fixed_owner_target_collisions": 0,
      "maximum_complete_fanout": 3,
      "median_complete_fanout": 1.0,
      "one_target": 0,
      "result_overflow": 0,
      "several_targets": 3,
      "unique_targets": 7,
      "work_overflow": 0,
      "zero_target": 3
    },
    "REFERENCING_RESOURCE": {
      "children": 12,
      "dispositions": {
        "GENERATED": 2,
        "NO_TARGET": 6
      },
      "duplicate_branch_failures": 0,
      "families": 8,
      "fixed_owner_target_collisions": 0,
      "maximum_complete_fanout": 6,
      "median_complete_fanout": 0.0,
      "one_target": 0,
      "result_overflow": 0,
      "several_targets": 2,
      "unique_targets": 6,
      "work_overflow": 0,
      "zero_target": 6
    }
  },
  "fixed_hypotheses": 15,
  "fixed_outcomes": {
    "GENERATED": 9,
    "NO_TARGET": 6
  },
  "member_occurrences": 47,
  "obligation_resource_cells": 32,
  "operator_obligation_resource_cells": {
    "DIRECT_IMPORT_DEPENDENCY_RESOURCE": 7,
    "MIRRORED_RESOURCE": 1,
    "OWNER_RESOURCE": 14,
    "REFERENCING_RESOURCE": 12
  },
  "operator_unique_resources": {
    "DIRECT_IMPORT_DEPENDENCY_RESOURCE": 7,
    "MIRRORED_RESOURCE": 1,
    "OWNER_RESOURCE": 8,
    "REFERENCING_RESOURCE": 6
  },
  "structural_unions": {
    "ALL": 19,
    "OWNER_MIRROR": 9,
    "OWNER_MIRROR_IMPORT": 14,
    "OWNER_MIRROR_REFERENCE": 14
  },
  "support_member_counts": {
    "members_structural_only": 0,
    "members_with_global_lexical": 47,
    "members_with_own_lexical": 45,
    "members_with_role": 47,
    "members_with_routed_escape": 0,
    "members_with_routed_preferred": 45
  },
  "total_hypotheses": 28,
  "unique_generated_resources": 19
}
```

## Artifact digests

- capture.pkl.gz: `0ad8b7b48274ca67d9ee669cecbf2ae553a89c3476b80a8ea3bf413ae8bcaf30`
- retrieval.json: `6ae883a05393120c2da7df442bb9ef704b8fb7d2c9ebf6f2e3cdae7c6e415f58`
- routing.json: `6c68dd32d2b6047c426e59b0731229225eefd1d99b115539391a60d8847ef24f`
- grounding.json: `1211f59ce778da4c1badd57d7b65b45a953780af2856177dbeb00cf31ddd75a4`
- generation.json: `b12f519e214382ce1fd76b19e0af995342f20a71b6fb32d4563cf64fe4a0709f`
- stage_b_integrity.json: `7e3aa54d8384879bfc9143efcb60224f270747780be9cff9849918f91ed39e80`

Treatment identities/specs were captured and mechanically joined. These are execution counts only; no candidate was labeled REQUIRED, helpful, unnecessary, complete, sufficient or effective.
