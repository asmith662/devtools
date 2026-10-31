# First live native maintenance task: approved preparation

Starting main was `fd6af0d951a57718233680a971d135b415e160e4`, synchronized with
origin. The independent Inspector worktree remains on `feat/agent-inspector`.

The Intake API reported 68 proposal chains, 67 pending and one approved. The
previously approved B-0048 constructor repair is delivered and its WorkCycle slot
is consumed. The suggested SQLite text, Windows drive-relative path, dangling
entry and literal Codex prompt repairs already have current guards/regressions;
none was replayed. B-0035 remains closed.

The actual remaining defect is a narrower residual of proposal
`ff4c4110-9c3b-480d-8f0f-77cf4610b700`: an import inside an unrelated helper,
async helper or class makes a valid module facade reexport unsupported. This is
a current RI false negative with one implementation owner,
`src/devtools/context/python/imports/members.py` (21,395 bytes). Module-level
conditional imports and genuine competing bindings must remain conservative.
No general Python scope evaluator or new public contract is proposed.

The operator approved the existing real default-No Intake review and publication
prompts. [B-0049](../backlog/items/B-0049-prevent-one-facade-import-fallback-from-overriding-competing-pattern-or-handler-bindings.md)
retains the original proposal unchanged; its
[review](../backlog/proposals/ff4c4110-9c3b-480d-8f0f-77cf4610b700/review-0003.json)
explicitly narrows this prospective episode and retains broader historical
pressure. Intake approval grants no execution, integration or closeout authority.

The [frozen task](code-audit/live-native-task-20261031/task.json),
[selection evidence](code-audit/live-native-task-20261031/triage.json),
[public checks](code-audit/live-native-task-20261031/public-checks.py.txt),
[failed baseline](code-audit/live-native-task-20261031/public-baseline.json) and
[private baseline](code-audit/live-native-task-20261031/private-baseline.json)
were prepared before any acting inference. Three public cases fail and four
controls pass. Independent private cases have six expected failures and twelve
passing/neutral controls. The private implementation is excluded from worker
and reviewer Context. No reference patch was authored.

The public diagnostic is temporarily materialized at the exact authorized test
address, explicitly invoked, and archived as text. It is not a permanent failing
test installed on main. Native custody must return the original implementation.
Any accepted model candidate remains archived pending separate integration
authority. This observation task does not publish that executable candidate.

Proposed worker limits are eight calls, six acquisitions, three proposals,
2,048 output tokens per call, 120 seconds per call and 900 seconds total.
Separate review limits are three calls, two reads, 2,048 output tokens,
120 seconds per call and 360 seconds total. Both use the existing stateless
llama.cpp adapter with thinking disabled, fresh independently controlled inputs
and separate grants. The native portable profile cannot override provider
sampling. The actual unchanged serving settings must be shown and approved;
they are a qualified limitation, not claimed optimal settings. No shared service
mutation, new backend loader, model download or paid fallback is authorized.

Preparation precedes separate genuine default-No coding authorization and
dispatch, and, only for a lawful successful candidate, review authorization and
dispatch. The model proposal cannot approve itself. A trusted host disposition
and authenticated read-only integration plan remain later distinct operations.
No task closure or candidate installation follows automatically. B-0043 stays open.

This evidence-only preparation leaves supported executable inputs unchanged.
Focused repository-owned validation and authenticated historical protected inputs
apply under the assignment's observation-only allowance; no fresh comprehensive
pass is asserted. Final observations and exact limitations will be added after
the separately approved episode, including a negative or blocked result.
