# Qwen worker acceptance, budgets and response correspondence repair

Starting main `58495350009fda815602f1b50bcfb69cc085b4e6`. Three bounded implementation commits are retained in the
normal production PR#11, now merged as `6c4267e8bd47d8ac897e01230fa843db74f34a81`. The source/test
tree is independently authenticated against production `18f6ac247bf5d1173e8b488910557207ccfaf92c` and tree
`3fbd979b78461a12dd465c83650ec00bab8b2b7c`. This report records delivered behavior, not a new Agent,
transaction system, sandbox or execution authority.

Implementation commits: `c3f63c419cfedfc4aae9e2d9c4eba469db3162de`
(frozen-input acceptance), `2da5f714e273f01bef1addc0a540803cb78a6b84`
(proposal budgets), `06361e355409e7a1943c9956abc2956e58558c25`
(response provenance), followed by fixture-only
`18f6ac247bf5d1173e8b488910557207ccfaf92c` (two capacity producer labels).

## Original reproductions

The tiny authored-repository audit probe reran on unchanged main before source
edits. Prepared candidate code changed a frozen test yet returned ACCEPTED with
`source_restored=True` and `original_unchanged=False`. Prepared cap1 allowed two
admitted proposals after a failed first check. A native interaction selected as
audit-selected returned audit-foreign, and its Tools still ran. Native frozen-test
drift already refused; Runtime already refused the source mismatch. No live model
or publication bypass was established.

The corrected permanent tests also ran against exact original Git module bodies
loaded in memory under their canonical modules: three intended behavioral assertion
failures and one Runtime control pass. No source checkout/copy or import failure
was used as a reproducer. Initial fixture/admission/query and wrapper preparation
errors are retained as limitations, not counted as defect reproductions.

## Maintained boundaries and behavior

- **Frozen input acceptance:** `coding_loop.validate_workspace` reuses
  `CodingCommands` fixed-check journaling and returns raw diagnostics to the host.
  One bound plan survives baseline checking and all turns. Validation authenticates
  before/between/after checks, follows the existing bundle order (tests, oracle,
  then applicable quality/typing checks), records NOT_RUN rather than imaginary
  success and rejects source/plan drift. Final acceptance also requires actual
  `original_unchanged` and current immutable inputs. Unexpected bytes remain for
  reconciliation; known admitted source restoration remains separately recorded.
- **Proposal budgets:** existing proposal admission/increment and exhaustion now
  apply to both modes. Refused attempts consume one proposal without becoming
  admitted mutations; native batch components remain one proposal. Absolute
  model-call caps, default bounds and native six-proposal behavior remain intact.
  Zero remains invalid at task admission. The prepared prompt distinguishes the
  two limits, and receipt counters reflect actual attempts/refusals/admissions.
- **Response correspondence:** capture selected source before invocation, archive
  actual response/usage/call IDs, then refuse a foreign label before Tools or
  proposals. RESPONSE_VALIDATION_FAILED is terminal, with no redispatch. Runtime's
  private comparison is not a public reusable validator; the application keeps
  the same simple equality contract without depending on Runtime/Conversation.

Changed owners: `apps/qwen/coding_loop.py`, `commands.py`, `tasks.py`, package
README and existing `tests/apps/qwen/test_coding_loop.py`. No framework exports,
ToolRunner, Runtime, Checkout, WorkCycle, model configuration or dependencies
changed. Existing journals retain their schema; additive integrity/source fields
record the stronger checks. Frozen historical receipts remain untouched.

Two existing `test_environment.py` doubles returned measured-fixture/compact-fixture
while configuring capacity-fixture as their selected source. Initial broad focus
had848 passes/two failures; the first complete gate had2865 passes/two failures/two
live skips and100% configured coverage, and was correctly rejected. Only those two
response producers were changed to `self.source`; capacity assertions and limits
were preserved. All three affected capacity cases pass. The final gate below is
the required new run on that committed fixture-corrected tree, not a relabeled
earlier result. Configured coverage measures `devtools`; application behavior is
independently protected by the explicit worker regressions.

## Permanent regressions and validation

Tiny real Git/observation/admission fixtures exercise `run_coding_task`, literal
candidate text and independent oracles in prepared/native modes. Cases include
test mutation, read/runner/config drift between checks, late acceptance drift,
legitimate success, caps1/2/zero, refused/admitted accounting, independent call
caps, two regions in one proposal, returned response source/usage/call evidence
and refusal before dispatch. Existing cancellation, unknown-source preservation,
native six-proposal, ContextTools, restoration and Checkout/delegation tests remain
in the focused and protected suites. The existing diagnostic test now supplies its
newly authored host test hash explicitly rather than calling deliberate input drift
a valid frozen baseline; its independent primary-failure assertions are preserved.

Committed-tree protected gate: **2867 passed, 2 live skips**,
pytest 906.36s; managed 908.225s. Production branch
coverage is **100%**, zero missing lines/branches. Exact source/test/configuration
inputs are hashed before/after. Focused: **638 passed,
0 skipped**. Supported Ruff, supported formatting (634 files),
configured strict mypy (520 files) and post-main regressions pass. This is actual
The post-main run passed116 tests in109.24s, with identical physical inputs to
the committed gate.
This is destination evidence, not a previous gate. Frozen/generated broad-tool limitations
are not relabeled green, and no frozen science is reformatted or replayed.

## Delivery and remaining scope

Existing proposals41a497a8,660900a1 and751451cb each receive append-only
implemented-and-merged ADVISORY evidence with exact commits, PR and main. Intake
has no delivered/closed proposal state: no duplicate proposal, approval, B-number,
grant or parent closure was invented. Their bounded implementation should not be
rescheduled. Existing d58697fd general check-input closure/reuse and39c6663a
application cohesion remain separate open work.

Candidate code execution is not an OS sandbox. Sampling current hashes is not
proof that no transient/external effect happened. The repair does not confer
publication authority, prove semantic task completion or make A+C approved.
Known source restoration, unchanged frozen inputs, check PASS, review and
publication remain distinct claims.

Original RI fixtures93/93 and experimental source606/606 keep their defined
review dispositions. The188 historical exact-version obligations remain in the
same seven families (168 unread/20 tip-only;15 full). No new audit credit is
assigned. Next is the existing Checkout/WorkCycle ownership, grant/delegation,
interruption and ambiguous-effect recovery cohort; it was not launched.

[Exact validation, code identities, reproductions, forensics and Intake evidence](../research/code-audit/qwen-worker-contract-repair-20261024.json)
retain the independently verified production state. Documentation-only closeout
is published through a separate normal PR on the same ordinary branch, preserving
all13 original forensic files and historical refs. The ignored completion records
identify the final closeout merge; they are not a successor-session dossier.
