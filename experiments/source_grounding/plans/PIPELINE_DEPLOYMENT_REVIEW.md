# Candidate-08: authorized execution stopped, scientific result incomplete

## Current terminal disposition (2026-10-17)

**CONTROLLER_FAILED / INCOMPLETE.** Exact human authority was authenticated and
published, fresh admission passed, and the existing pipeline dispatched the
controller once. Case 0022 C failed deterministic packet validation before gold
entry. Concurrent case 0024 B completed its one Sol/High turn and validated, then
the controller quarantined all surviving B results. No Astra call, gold import,
B/C/D publication or Stage D analysis occurred. No scientific retry was made.

The exact plan digest remains
`ea90029ffcf3c7bd90cd670bd7ffe35e3c97b6bcc20e353cd23b5480ad0c3b4e`, run
`1d83144558006cd381eadfde2a22856aa8f86c8c30587d3db4de16403fbb1115`.
Pinned source/plan commit remains `f9b96b374ee87a734dd4f8a4735f37cecd26663c`.
The target and accepted local publication main advanced only through canonical
approval `60d0cd247b6341a463c362fb18e67f4cba55cc9a` and PACKET
`b5a3c824928985098347f0ccc8d39db8088e5810`. Later authoring documentation is
separate from the authenticated execution source.

The trusted host used its actual `recoveryadmin` principal and the actual user-role
grant in message `msg_01a14a24-240e-7c60-8753-dff2c5b6f02c`; user-message SHA-256
`27c8a19ece5eac5e8de1bf65ea2a20a9d4edecd1fdfc8450da43cceb0dd05fbd`.
`Controller.approve(ApprovalRequest(..., kind="TRUSTED_HOST"))` published the
once-only exact-run grant. Approval-file SHA-256:
`391a40ca629433c680ffa9b5833e11ec26677b2993609506ccef888b34d23285`.
No principal/reference was invented; this is the existing host trust contract,
not a new cryptographic identity mechanism.

| UTC milestone | Observed disposition |
| --- | --- |
| 13:58:33–13:59:24 | Fresh preparation READY_FOR_APPROVAL; startup and budget preview PASS |
| 14:59:55–15:02:38 | Canonical approval publication and authentication |
| 15:56:15–15:57:48 | Fresh pipeline admission ADMITTED, 93.06 s |
| 16:03:02–16:03:53 | PACKET checks/publication; 145 tests and scoped static checks PASS |
| 16:04:43–16:04:44 | C22 packet validation failed before scientific entry |
| 16:06:51–16:07:27 | One Sol/High B24 turn, managed-process duration 35.774961 s |
| 16:35:42 / 16:36:07 | B24 local capture completed / final validation PASS |
| 16:36:33 | Controller BLOCKED; all surviving B results quarantined |
| 16:39:05 | Pipeline CONTROLLER_FAILED, total 2,570.47 s |

The execution attempt is `c888d086-3fd3-41ef-a832-628aed9f5347` under the
existing external `budget-correction/preparation` receipt root below. Its
`experiment-execution-v1` result payload SHA-256 is
`d750f1760b6c3c09bb56d86dcbd838687fe7acd7fed45471e2925e5653245e07`.
Canonical verification authenticates the available evidence with PASS; it does
not establish scientific completeness. Status/history report CONTROLLER_FAILED.
An earlier host observation failure interrupted admission before dispatch intent;
its retained attempt `cd888e5a-4197-441d-a4c6-2a2323f686db` had no controller
dispatch or scientific entry. It was not a scientific retry.

### Exact blocker and observation limitation

The bound `discrimination/lifecycle.py` packet validator invokes the CLI-version
check in `root.parent / (case + "-candidate-cli-preflight")`. Initial PACKET
validation created that log directory and reported the expected `codex-cli
0.162.1`. C22 admission repeated validation with the same parent/case path.
`workers/process.py` then refused exclusive `stdout.log` creation with
`FileExistsError`, before C ENTERED or budget reservation. Existing evidence was
not overwritten or deleted. C23/C24 remained queued; no gold call was dispatched.

The actual controller return records BLOCKED and quarantine. Its journal-only
projection instead says `APPROVED; SAFE_QUEUED_WORK_MAY_RESUME`, since the
pre-entry failure has no scientific FAILED journal. This projection does not
override the terminal pipeline failure or authorize resumption. No resume,
repair, code change, successor, extra call or further approval is part of this task.
A separately authorized review of this concrete adapter defect is required
before considering any future scientific action.

### Scoped economics and scientific conclusion

Canonical observed usage reports one fresh Sol/High invocation, two adopted
dependencies, 46,245 input tokens, 3,609 output tokens, zero cached/cache-write
input and 917 reasoning-output tokens. Reasoning is included in output; categories
are not added together. The scoped report has no missing invocation usage or
attribution conflict, but retains one unallocated timestamp observation and
PARTIAL / OBSERVED_LOCAL_AND_DEVTOOLS / NOT_ACCOUNT_WIDE coverage. Provider-reported
model identity, model-only duration, underlying HTTP request count, dollar cost
and Codex coordination consumption remain unknown. The managed B24 stage took
about 1,911 s including local capture/proof/validation, distinct from model-process
duration. Its one canonical reservation settled; read-only consumption assessment
passes. Observed treatment acceptance does not mean scientific cohort acceptance.

Policy bytes and exact-run limits remain unchanged: four calls, 1,756,679 forecast
input and 191,923 forecast output tokens. These are admission/reservation allowances,
not provider runtime ceilings. Canonical metadata was refreshed during admission;
post-run refresh at `2026-10-17T16:36:52.856489+00:00` remained partial with no import
failures. No allowance was raised, reset or transferred.

No source/target/pursuit-usefulness estimates, retention/reduction results or
selective-pursuit conclusion can be calculated from this incomplete cohort.
The frozen ESTIMATION_FIRST procedure was not retuned or run on missing gold.
Production retrieval, Context selection and coding-agent behavior are unchanged.

The [machine review packet](pipeline-deployment-readiness.json) records the current
receipt and recovery identities. `authorized-20261017/` under the persistent root
below holds grant/publication evidence, scoped usage, final integrity and recovery
verification. The existing accepted same-SSD recovery facility preserves Git
approval/PACKET objects plus new external journals, worker evidence, policy and
receipts, with actual restore/hash verification; it does not protect against SSD
loss. No new repository, remote or backup infrastructure was created.

The next program checkpoint is **B: consolidate active Devtools engineering for
integrated agent use**, without starting it here. Candidate-08 remains scientifically
incomplete. Subsequent sequence is D0 bounded non-learned coding-agent benchmark,
C Learned Intelligence integration, D1 learned comparison, then E continued
autonomy/retrieval development. No later milestone is implemented by this closeout.

## Provenance, recovery and validation

The frozen protocol SHA-256 remains
`6962c790c4d6767b7560ede8bbc70c7922312902fe273483c81b351a2b74750f`;
policy SHA-256 remains
`c0694b2d2aeba8e3961b3feb7403ff5531f18ce2f11452b6476226c773fa6ba6`.
Engineering checkpoint is `f19d4fdfb957301f154373a9f6974cb09f5eb9c5`, Stage A
binding is `15df9e18f59189c0c0512ef641e9723eeaafa39f`, and the plan/source
publication is `f9b96b374ee87a734dd4f8a4735f37cecd26663c`. No successor or
implementation change was made during this execution. Candidate-06/07 plans and
all 13 historical forensic files remain unchanged. All 30 frozen scientific
artifacts and 430 bound source files pass exact byte/hash comparison.

Persistent receipt root:
`C:/Users/recoveryadmin/Workspace/tools/devtools/.local/deployment-receipts/source-grounding-successor/candidate/budget-correction`.
The preparation result is `preparation/4f96efc2-1c37-4c4a-83d3-4ce07cae56b6/result.json`;
the terminal result is `preparation/c888d086-3fd3-41ef-a832-628aed9f5347/result.json`.
The host audit and scoped usage are in `authorized-20261017/` there. All referenced
pipeline stage hashes authenticate through existing receipt readers.

Active publication is
`C:/Users/recoveryadmin/Workspace/tools/devtools/.local/deployments/source-grounding-successor/publication.git`.
The existing backup base is
`C:/Users/recoveryadmin/Workspace/tools/devtools-publication-backups/source-grounding-successor`.
Its original sealed package and earlier source/policy increment remain intact.
The new 1,693,697-byte Git bundle (prerequisite pinned source F9) has SHA-256
`8f675d5b43fb4e4d17437101dfe1af77d1650a2942167a6f768472f77527fef1`.
The 140,051,185-byte external archive has SHA-256
`f75976b686909105c9fdfe8d0df9d9a1dc9c026d2e4df22696d8631d3c06a9a8`;
manifest SHA-256 is
`d3fd6692f6a7fbfe82f0c4c207fa39ea416d1e713f06711e484479603cd4ccdc`.
The existing restored bare repository fast-forwarded to PACKET and passed full
Git fsck, exact plan and approval checks. All 1,967 external members restored in
isolation with matching hashes. Verification finished at 16:42:15 UTC in 146.01 s.
This covers current-run worker evidence (including quarantined/adopted bytes),
scientific journals, controller observations, pipeline attempts, grant evidence,
policy and reservations. It excludes unrelated private sessions/global usage
ledger and future evidence. Restored bytes/refs are verified, not a new scientific
execution or a demonstration of provider access from a relocated checkout.

This task ran no broad controller regression suite or full development gate:
production source was unchanged. Prior engineering validation remains historical
(258 controller tests; 1,662 protected tests, two skips, 100% production branch
coverage; scoped statics). Actual PACKET passed its frozen 145-test/static gate;
B24 passed its frozen capture proof/validation. Available-evidence controller
verification, receipt integrity, status/history, restoration and whitespace checks
pass. No confirmation/reserve evidence or historical semantic judgments were
inspected by the operator.

For observation, run the existing pipeline `status` or `history` with the exact
plan, target and receipt root above, from the pinned target's own interpreter.
Read-only `reconcile` is available for later evidence reconciliation. **Do not
execute, resume or approve this failed run again based on this report.** The
once-only grant and unused numeric allowance are not authority for replacement
work. Protected main and the completed pipeline feature remain unchanged; no
scientific acceptance or production promotion follows from this incomplete run.
