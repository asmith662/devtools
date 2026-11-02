# Standing routine authority and the B-0052 episode

## Delivered authority

Starting local and remote main were `ef013e7fa8f9470e1459c5ace7d635186a648495`.
The [prospective authority contract](../development/routine-development-authority.md)
was delivered in executable commit `e371a71c93b5884fcf6bd4aa7ede6632a815c0a3`.
It composes existing Intake, native WorkCycle, independent reviewers, Checkout
and integration owners. It changes no legacy Qwen grant or historical dispatch.

Native APIs already accepted trusted-host callbacks. Repeated human decisions
came from manual CLI/driver choices and the absence of a prospective policy
connecting those callbacks. Legacy Qwen standing delegation was not authority
for native coding/review and was not silently inherited.

The operator actually answered **`+yes`** to the exact default-No standing-policy
question. [Consent](code-audit/routine-authority-20261102/operator-activation-consent.json)
binds activation scope
`52a6d7ca24068e4a155d758ba33d3fe2bd2ac82be6e6c91191f2a24f2d59e97f`
and policy payload
`fd2c3c00ef9421af7beb9c1168cb292c82acb50c8c12b15cab4092e7863d84d5`.
Activation was conditional on protected validation and occurred only after it
passed and the tested executable commit was published. Active policy version is
`f712a8e21f0c07485fa46f904ea6f63a984e1fb6ae69637a5242b045fe2defcf`.
It has no inactivity expiry. Individual grants expire within 3,600 seconds.

The [activated policy](code-audit/routine-authority-20261102/activation-result.json)
allows bounded routine work in the declared Core, Context and filesystem roots,
using the pinned existing local 64K Qwen provider. Native coding limits remain
eight calls, six acquisitions, three proposals, 120 seconds/call, 900 seconds
total and 2,048 output tokens/call. Review permits four calls, three total reads,
120 seconds/call and 480 seconds total. Independent 128 KiB request, 32 KiB edited
source and capture limits remain. Service/sampling defaults were not changed.

Routine Intake, coding/repair, qualified diagnostic/acceptance review, trusted
host assessment and read-only planning can derive exact grants without another
operator prompt. Immutable decisions retain the policy version, exact owner
request, task/subject aliases, provider qualification and engineering assessment.
Native/reviewer effects recheck current authority. Denial/revocation and expired
grants fail closed. Routine Git permission assessment retains exact input/scope
and validation references; existing protection and validation owners still apply.
Exceptional architecture/security, destructive effects, secrets, paid services,
persistent serving changes, weaker validation and over-limit work still escalate.
There is no new scheduler, automatic task picker, provider registry, installation
grant, autonomous publication engine or backlog closeout.

## Actual B-0052 coding

B-0052 retained its genuine Intake review
`3d70faf533567bde040db157ebc775d30ea8b358e9c4cae0886cca58ea1da4ee`,
assignment `7489f593e0b23b4a8b118201394d738f62febf3f606d2efec83d7a5e394b33ef`,
feature `feat/native-csv-b-0052-20261102` and original source baseline `ef013e7f…`.
The old expiring coding prompt was never approved or reused. The standing owner
issued a fresh [native grant](code-audit/routine-authority-20261102/b0052-coding-grant.json)
and the existing coding process ran once.

The real Qwen3.8-27B UD-IQ4_XS worker selected:

1. `read_source` for `src/devtools/resources/filesystem/models/csv.py`.
2. `read_source` for the maintained standalone-row tests.
3. One grounded `replace_source` edit in `CsvRow.__post_init__`.

It independently added a duplicate-header check after immutable tuple capture.
No supervisor implementation or reference patch was supplied. This episode used
neither `find_source` nor `read_source_unit`; both were available. Source
acquisition and continuation worked. No repair was necessary because the first
managed public validation passed all **54 tests** in 57.34 seconds, followed by
fresh frozen independent private acceptance in 0.139 seconds.

The [exact candidate](code-audit/routine-authority-20261102/candidate.json) is
`a7471ffeec9a21cdb12ddc3bcb0cb315680f109ff70d168ade03310c24bef255`;
the native result is
`f1971ed020430afcf064e88f9cacb193ce1f0a900233759ac78aa66788d2eed2`,
with disposition **REVIEW_CANDIDATE**. Candidate and patch are retained as escaped
JSON strings with exact hashes; display copies are not byte authorities.
Source was restored, Checkout released and main resumed. No candidate was
installed or committed as production source.

Coding used three completed actual model calls, 13,384 cumulative input tokens
and 354 output tokens. Adapter time was 29.38 seconds; the full grant/episode
composition took 132.44 seconds. Peak request was 23,400 bytes with 6,297 measured
input tokens. Capture was 92,175 native observation bytes plus 4,458 supporting
bytes. Deterministic Context policy was enabled without needing pressure
reduction. This small task does not requalify high-context capacity or establish
general engineering competence. Native sampler overrides remain unsupported;
the observed persistent default temperature was 1.0.

## Genuine acceptance-review attempt

A fresh independent reviewer actor/session received the exact authenticated
task, baseline, candidate/diff, public checks, qualified private outcome and
custody facts. It did not inherit the coder conversation, private oracle or a
reference repair. The same provider/model weights were used sequentially;
session separation does not establish model diversity or independent judgment.

The [separate policy-derived grant](code-audit/routine-authority-20261102/b0052-review-grant.json)
entered one actual review call: 10,999 input tokens, 86 output tokens, 21.24
adapter seconds and 38.12 seconds overall. The templated request was within
capacity; this was not a byte/token or output-limit failure.

Qwen returned two native `read_source` requests in one response, for maintained
row tests and frozen prospective public checks. Both paths were authorized and
relevant. The existing acceptance owner permits **one Tool call per response**.
It refused the batch before either read entered: total read allowance was three,
**zero reads completed**, and three model calls remained. The failure concerns
batch shape, not total acquisition exhaustion. The model response completed
normally with Tool-call termination and empty textual content.
The existing model-facing SYSTEM did not explicitly state this per-response
batch limit; the observed refusal does not establish a failure of engineering
judgment or compliance with an explicit instruction.

The immutable [proposal](code-audit/routine-authority-20261102/native-records/reviewer/proposal.json)
is **blocked**, with null conclusion and
`PermissionError: Review permits one bounded read per response`.
No structured assessment or findings were produced, so reviewer factual quality
and judgment remain unmeasured. Host admission of that blocked proposal was
explicitly refused. No substitute manual acceptance decision, integration plan,
installation, publication of candidate source or backlog closeout occurred.
The coding and reviewer dispatch slots are consumed; there was no retry.

The [host evaluation](code-audit/routine-authority-20261102/host-evaluation.json)
finds the four-line repair supported by source and frozen checks, but does not
convert that technical assessment into missing model-review authority.
This is a positive real coding result and an incomplete connected lifecycle.

## Validation and remaining step

The initial authority selection retained two failures and nine passes. Fixing
Intake callback handling and a test status expectation was followed by two
failed-test reruns passing. Broader native/Context/delivery compatibility passed
123 tests in 967.70 seconds. Final authority regressions passed 13 tests in
64.17 seconds; the final Git-scope regression passed separately. Ruff, formatting,
strict mypy (627 files), layout and integrity checks passed.

Exactly **one** comprehensive invocation ran on committed executable candidate
`e371a71c…`: **4,186 passed, two optional skips**, 100% configured production
line/branch coverage, 2,896.14 seconds including orchestration. The
[original receipt](code-audit/routine-authority-20261102/final-protected.json)
attests stable inputs during that run. The uninstalled model candidate received
its own frozen task checks, not a manufactured comprehensive pass.

After ordinary Checkout rematerialization, only recorded LF/CRLF-equivalent
representations were reconciled. All 1,068 protected input hashes and Git blobs,
Python/runtime and installed-package qualifications still match the tested
candidate. Invocation-specific inherited environment fingerprints differ; full
cross-invocation environment equivalence is not claimed. Historical coding and
diagnostic attempts, original candidates, forensic files, RI records and
Inspector ownership remain separately preserved.

The next bounded improvement is to make acceptance-review read-batch limits
explicit and recoverable through its existing Tool-correlation/continuation
owner. Maintain total read/call budgets and acceptance gates. Preserve this
consumed result; any subsequent live review needs lawful fresh prospective
ownership, not replay. A general planner/continuous scheduler, expired one-slot
grant renewal and native installation/publication authority remain separate.
