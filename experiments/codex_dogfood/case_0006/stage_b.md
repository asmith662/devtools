# Case 0006 Stage B

Execution kind: `RECOVERY`; recovery ID: `case-0006-stage-b-recovery-1`; prior failed executions: `1`.
**STAGE B RECOVERY CAPTURED - NOT ADJUDICATED. No effectiveness analysis was performed.**

Stage A commit: `e7aed4162672dd859a0a8a33a2b718dda8425495`.
Recovery protocol commit: `56f18901b5acae47b9c07811dd18eb4770c56285` (`Freeze Case 0006 Stage B recovery`).
Attempt 1 is retained in `stage_b_attempt_1.md`: its post-generation correspondence check matched complementary members by list position, while production canonicalizes members by identity/key. It exited before native outputs were persisted. This recovery is the sole authorized additional treatment execution.
Execution entry point: `capture.py --execute`; all treatment inputs were loaded from the digest-verified committed native archive.

## Invocation counts and runtimes

- Lexical acquisition: 1 call, 0.119348s.
- Role routing: 1 call, 0.302585s.
- Explicit frozen grounding requests: 9 calls, 0.197677s; dispositions `{'unsupported': 8, 'resolved': 1}`.
- Witness generation: 1 plan execution, 0.169875s; production validation checked 14 recipe-member references using exact cached grounding results, with zero additional resolver executions.
- The recovery raw native capture is `stage_b_recovery_raw.pkl.gz`; it is retained as `INCOMPLETE_UNVALIDATED` audit material after successful canonical finalization. Its SHA-256 is `9b501f58374e442dd3f0ae4b2246a17a3cebc0fa3e99581873e5d579b3130c9e`.

## Mechanical outcomes

- Generated hypotheses: 0; member occurrences: 0; unique targets: 0.
- Generation dispositions: `{'unsupported-source': 9}`; projection dispositions: `{'unsupported-source': 14}`.
- Projection operators: `{'OWNER_RESOURCE': 12, 'MIRRORED_RESOURCE': 2}`; summed examined-resource count: 0.
- Generated target origin check (resolved grounding plus frozen structural projection): `True`.
- Attached supports: lexical 0, role 0, routed 0.
- Global lane identity and routed candidate retention/order checks passed. No generated rank or position was recorded.

## Output files and SHA-256

- `capture.pkl.gz`: `ed461a0c7414db4f9bb4f812b2a70312084061f88c51168aeb8903fbb091e8a7`
- `retrieval.json`: `e0389939d08c788075735a9b1c8af24c11989e67f7276729e38984598753ed0a`
- `routing.json`: `30fd995a2e8784167faeee8b40b3bc1928666711b01c08fe96efe4b5cc51d510`
- `grounding.json`: `54bed798d6a9209b3c5ec09ad765e5e7ee80ff7bd4cb8c2f9dd0845aa8ed1503`
- `generation.json`: `90b1dff07ee8351dcfcf1c297b07b2038ce2f4e63560d36ee1a1c48a3882f91a`
- `stage_b.md` contains the execution record; its digest is retained in `stage_b_integrity.json`.

All canonical Stage B outputs refuse overwrite. The raw checkpoint was retained after correspondence, frame, routing, grounding, recipe-binding, and target-origin checks passed. Incomplete native checkpoints are marked unvalidated and are resumed without repeating completed operations. This record contains execution/integrity facts only; no resources have been judged and no candidate surface has been evaluated for effectiveness.
