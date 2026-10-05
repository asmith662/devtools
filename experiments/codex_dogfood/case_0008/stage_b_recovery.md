# Case 0008 Stage B generation-only recovery protocol

**PARTIAL STAGE B — NOT CANONICAL**
**GENERATION NOT CAPTURED**
**NOT ADJUDICATED**

The original execution is `2fed596a-f43d-4d35-9e32-e8a609366a6f`. Attempt 1 is preserved in `stage_b_attempt_1.json` and `stage_b_attempt_1.md`; its raw capture is immutable at the recorded digest. Recovery identity `case-0008-stage-b-generation-recovery-1` is separate.

## Authorization

The only additional treatment call authorized is one combined generation API execution against the unchanged Stage A recipes/bounds/frames and the exact captured lexical acquisition, routing view, and 11 groundings. Additional lexical, routing, grounding, and any other treatment executions are zero. Recovery consumes the separate `stage_b_generation_recovery_raw.pkl.gz`; it does not rewrite Attempt 1 raw state.

If the authorized generation call is entered and does not return, it is never called again. If a return cannot be durably captured, mark Case 0008 `CAPTURE_FAILED`; obtain effectiveness evidence in a new prospective case.

## Object graph preflight

The production `build_candidate_witness_view` checks shared identity, not value equality, for `routing.acquisition is acquisition`, `routing.role_evidence is role_evidence`, and `routing.global_retrieval is acquisition.full_task_retrieval`. Candidate support validation also requires each lexical support's match to be the exact match instance at its native lane/rank; routed support must be the exact candidate instance in the retained routed lane; role support must be the exact evidence instance in the retained role evidence. Recovery preserves these references by sourcing acquisition, role evidence, and routing from the captured routing view. Snapshot/task/resource/frame and grounding checks are value/frame validation, not additional shared-instance invariants in the inspected path.

The mechanical preflight constructs the generation plan and checks the aliases above. It does not call `generate_witness_hypotheses` and executes no projection. Recipes are reconstructed from the 29 frozen specs and captured grounding values, then compared against the Attempt 1 bound recipes; any difference stops recovery.

## Durable return

The future recovery entry point first persists `IN_PROGRESS`. When the production API returns, it stores the native return and invocation count in the recovery raw file before invoking validation or serialization. An in-progress state is ambiguous and cannot be retried. A captured return is finalized from recovery raw without another generation invocation.

Only after a successful captured return may canonical Stage B outputs be finalized. They must identify `execution_kind=GENERATION_RECOVERY`, original execution id, recovery id, one prior failed attempt, and the original durable lexical/routing/grounding source. Future Stage B.5 input generation remains Stage-A-only and excludes all recovery metadata.
