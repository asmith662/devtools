# B-0050 failure analysis and B-0051 native continuation

One genuinely approved B-0051 coding episode completed **BLOCKED**. Qwen made
five actual calls, acquired all four source resources, authored two admitted
edits and attempted a third proposal. It did not complete public validation;
private acceptance and independent review were not entered. Source was restored,
Checkout released and the persistent 64K service remained healthy. No model
candidate was installed or published as executable code.
Starting authenticated local and remote main:
`1e724c60f6cc82e4333193cfb0dac231dde50ab0`.

Existing Intake captured proposal
`cdbe84f8-5f1d-47a9-a421-131db4966a1e`. After the actual operator replied
`+approve`, the existing reviewer published **B-0051**, with review SHA256
`895a81126d69a19a73e861498ce49e3ffe87696377b53ac24ddeaf85f21a5857`. The real
operator prompt binds review scope SHA256
`cd70180a428f07a7f5f2e48ccfa688d517668368c05c0ed75d674fbd53f9d4fa`.
The existing callback returned false for preview and subsequently consumed the
actual scope-bound human decision; it did not manufacture consent. The new
WorkCycle slot was unused at preparation. A second genuine `+approve` authorized
the exact coding episode below; that slot is now consumed.

## What the first implementation failure established

The [B-0050 episode](live-native64-maintenance-task.md) produced two real
model-authored replacements of `_contains_nested_import` in
`context/python/imports/members.py`. The first starts traversal at the supplied
node's children. It skips encountered function/class declarations, but fails to
exclude a supplied function/class root: its imports are already in the work
list. Three public namespace cases therefore still failed. The second adds the
root exclusion and passes all 61 public/maintained tests. This is observable
code behavior, not an explanation of the model's internal reasoning.

The private conditional-local failure has a different second cause. The repaired
predicate correctly ignores a local import in a helper beneath a module `if`.
Direct import analysis finds exactly one facade import. However,
`modules/declarations.py::lookup_python_module_declaration` separately walks
every descendant of the module control-flow statement, including the helper's
body. It counts the local import as another module binding and returns
`ambiguous`. The facade consumer honors that canonical refusal. It must not
ignore it to manufacture a successful resolution.

The [exact archived candidate reproduction](code-audit/native-scope-followup-20261101/historical-causal-reproduction.json)
observes `unsupported` with the installed consumer and `ambiguous` with the
unaccepted B-0050 consumer. Neither observation is a completed repair. The
[recorded-helper evaluation](code-audit/native-scope-followup-20261101/first-and-second-patch-analysis.json)
executes only the exact historical functions, without a supervisor correction.
The original source, records, private outcome and consumed slots are unchanged.

## Bounded next responsibility

The complete original facade repair now demonstrably spans two owners. Native
v1 permits one editable implementation file. The proposed next item is therefore
a **linked canonical prerequisite**, editing only
`src/devtools/context/python/modules/declarations.py`. The original consumer
repair and broader B-0049/B-0050 obligations remain open. This prospective
narrowing received genuine human Intake review; it is not a claim that the
one-file profile can complete the whole parent task.

The canonical lookup must distinguish module bindings from unrelated local
function, async-function and class bodies, including under module control flow.
It must retain exact current direct target/provenance and existing conservative
behavior for genuine module stores, definitions, aliases, star imports,
pattern/handler captures and dynamic calls. This is bounded static declaration
lookup, not execution or a complete Python scope interpreter.

## Acceptance frozen before any new acting request

The [38-case public matrix](code-audit/native-scope-followup-20261101/public-matrix.json)
covers direct and wrapped local namespaces, nested namespaces, conditionals,
loops and exception handling; direct function/async/class/import/absent targets;
aliases; genuine module competition; patterns, handlers, stars and existing
dynamic uncertainty. The revealed B-0050 category is public regression evidence
and is no longer independent hidden acceptance.

The [12 separately authored holdouts](code-audit/native-scope-followup-20261101/holdouts.json)
use distinct local stores, deletion, declarations, annotations, non-ASCII/CRLF
source provenance, absence, real module with/mapping/handler captures, decorated
target refusal and existing dynamic uncertainty. They are not copies of the
newly public local-import cases. The worker and reviewer must not receive these
implementations or expected outcomes. Host-only evidence is not model read scope.
No reference correction was authored.

The [complete baseline evaluation](code-audit/native-scope-followup-20261101/behavioral-baseline.json)
checks all cases: 17/38 public and 8/12 private cases fail, with 21 and four
passing controls respectively. All 17 existing module-selection tests pass.
An initial public harness mistakenly accessed a nonexistent analysis attribute;
the original failed receipt is retained. Its correction accesses
`derivation.dependency.snapshot_id`; expected outcomes did not change. Saved-ID
recovery then observes one failing grouped public test and three passing groups.
The matrix counts are semantic cases, not pytest item counts.

Prospective checks remain frozen task artifacts, not intentionally failing tests
installed in the protected main suite. Their temporary materialization is removed
before publication; the production implementation is unchanged.

## Proposed operation and explicit limits

The [prospective packet](code-audit/native-scope-followup-20261101/task.json) uses
existing WorkCycle, Checkout, `LlamaCppInteraction`, `native-context-v1`, source
navigation, grounded replacement, managed checks and custody. It permits eight
model calls, six acquisitions and three proposals including two repairs, 2,048
output tokens/call, 120 seconds/call and 900 seconds total. Independent limits
remain 128 KiB/request, 32 KiB editable source, 64 KiB disclosure and 960 KiB native
capture plus 64 KiB support. Provider input is measured: 62,464 input tokens,
2,048 output reservation and 1,024 safety tokens within actual 65,536 capacity.
Deterministic projection remained enabled. The operator separately approved the
exact assignment and dispatch scope before model entry.

The unchanged pinned provider is healthy with one actual 65,536-token slot; no
restart, download, service change or benchmark occurred. Native portable requests
disable thinking and cap output; they reject provider-specific request settings.
Although the adapter supports sampling parameters, injecting a low-variance
override through a wrapper would rewrite the approved request. No bypass is used.
The prospective profile discloses unchanged server defaults (temperature 1.0,
top-p about .95, top-k 20, min-p about .05, presence penalty zero); it does not
claim optimal coding settings. A native settings extension would be separately
authorized production work. The prior 128-token neutral capacity probes did not
prove sustained 2,048-token generation quality.

This is a supervised continuation informed by historical feedback, not an
independent first attempt. Only the diagnosis and public categories are supplied;
the prior conversation, hidden oracle and any reference repair are excluded.
Coding and reviewer grants remain distinct. A failed private candidate cannot
enter acceptance review. A possible future read-only diagnostic review of failed
candidates is recorded as a separate obligation, not implemented here.

## Validation and preservation checkpoint

The maintained interface ran the public baseline and saved-ID recovery after the
specific harness correction. An initial recovery request was correctly refused
because the prospective test had no maintained owner; supplying the reviewed
explicit group allowed execution. Original failures retain their actual status.
No production correction or passing full-task result is implied.

Focused execution selected existing module-selection, native Context and
llama.cpp adapter contracts: **167 passed in 15.14 seconds**. Supported-root Ruff,
format verification, strict mypy, layout and diff checks passed. The
[integrity receipt](code-audit/native-scope-followup-20261101/integrity-preparation.json)
authenticates 1,059 unchanged protected executable input hashes and Git blobs,
245 preserved historical hashes, the original 13 forensic files, 903 RI rows,
unchanged consumed B-0049/B-0050 records and the registered Inspector feature
worktree. No source edit, provider mutation or new comprehensive run occurred.
Existing protected evidence concerns unchanged framework inputs only; it is not
a pass about a new candidate. No production executable source is published here.

The preparation checkpoint was ordinarily published as
`4e818c4c412cc237708e01a3f5510349fc49d6c0` before inference. The earlier pending
integrity snapshot retains its original timestamp and meaning; the genuine
subsequent approval and terminal evidence are additional records, not rewritten
history. Broader facade repair, review-driven repair, failed-candidate diagnostic
review, automatic selection and closeout remain open.

## Actual authorized episode

Assignment SHA256:
`47a414bee5aaba90ee1ecdcb1795e4563f153c14e20b99392fad2505ceff391c`.
Coding grant:
`1a5d65819a57918783af5f90f791148f657819ac6664dc389d2b33a81ef9b86f`.
Result:
`0d3cf5f97dba9561e5d448611024d4ab753320ed1cb4a10ff8b61bbd0ab100b2`.
The [actual operator decision](code-audit/native-scope-followup-20261101/coding-operator-approval.json)
binds scope digest
`13944b788e7f4e5f2e6826ddb6d450fef381ed8118191efe46f59535425c09ff`,
including finite budgets, expiry, provider reservation and source restoration.
The owner used `feat/native-scope-b-0051-20261101` in the canonical checkout and
returned to `main`. Neither historical slot was replayed.

The [episode receipt](code-audit/native-scope-followup-20261101/episode.json)
retains all normalized requests/responses, exact native Tool identifiers,
35 authenticated observations, public output, authority, custody and support
measurements. Qwen selected four whole-resource `read_source` requests: editable
declarations, read-only bindings, maintained selection tests and expanded public
checks. Total exact source acquired: 32,973 bytes, no duplicate acquisitions.
It did not select `find_source`, `read_source_unit` or an explicit
`validate_candidate` call; existing managed public validation followed admitted
edits automatically. No motivation is inferred from those Tool choices.

The model's third call correctly described the unscoped `ast.walk` problem, but
its actual replacement introduced `lambda: nonlocal_marker := None`, which is
invalid Python. Both test modules failed collection: two errors, no executed
test passes. The fourth call removed that syntax error but retained a call to
`_scan_module_level_bindings` without defining it. Public validation then
reported **two failed, 19 passed**; the grouped failing tests stop at `NameError`,
so this is not 38 fully evaluated semantic cases. The fifth response proposed
replacing the original loop text, which had already been removed. The host
returned the correctly correlated refusal, `Old text must match exactly one
source region`. Three attempted proposals exhausted the approved allowance;
only two were admitted. No extra sample, host-written repair or replay followed.

This is a model implementation/current-source repair failure. All five calls
returned normally with Tool proposals and without output-limit truncation.
Public collection/runtime errors were accurately delivered to subsequent calls.
There is no observed provider error, missing authorized source, Context-capacity
failure or unexplained Tool effect. A larger output allowance or different
sampling setting is not established as a remedy by this observation.

| Measurement | Actual observation |
| --- | --- |
| Model calls / admitted edits / attempted proposals | 5 / 2 / 3 |
| Cumulative input / output tokens | 52,845 / 1,378; retained Context counted repeatedly |
| Maximum response | 608 output tokens; approved ceiling 2,048 |
| Native / outer driver time | 155.151 / 159.095 seconds |
| Adapter interaction time | 117.452 seconds; nonstreaming first-token timing unavailable |
| Managed public check time | 0.813220 + 0.862554 = 1.675774 seconds |
| Private checks / reviewer inference | Neither entered |
| Largest request / measured input | 82,505 bytes / 19,671 tokens |
| Capture | 331,758 native + 7,837 support = 339,595 bytes within 1 MiB |
| Projection | No omitted exchanges, no shortened source, no pressure warnings |
| Resource samples | Four; sampled GPU high 14,738 MiB, free GPU low 1,313 MiB |
| Host free physical / virtual memory low | 784,564 / 5,527,188 KiB; sampled observations, not continuous extrema |

Machine projection status `reduced` includes source-state annotations that can
increase serialized size. It is not claimed as measured compression here.
The [provider-after receipt](code-audit/native-scope-followup-20261101/provider-after.json)
authenticates the same container, pinned image/settings and healthy actual 64K
slot, without OOM termination or any service mutation.

The terminal source and native patch are preserved as an
[exact escaped unaccepted artifact](code-audit/native-scope-followup-20261101/unaccepted-candidate.json),
not a reviewable candidate or production implementation. Private acceptance was
never entered: none of its 12 cases is reported as a candidate pass. Existing
review-subject admission refused the blocked result. No reviewer authorization,
reviewer model request, host review decision, integration plan, installation,
publication of model code or closeout occurred. B-0051 and its parents remain
unresolved. A separate prospective reviewer composition was not executed.

The [final integrity receipt](code-audit/native-scope-followup-20261101/integrity-final.json)
verifies exact restored protected hashes/blobs, candidate/patch bytes, original
historical records, release and Inspector registration. An archival helper hit a
nested-event-loop error only in its final synchronous verification after saving
the observations; a separate synchronous verifier completed that check. This
local reporting error is distinct from the completed model outcome and caused
no redispatch or source correction.

## Next bounded improvement

The concrete configuration gap is approved per-request sampling in the native
assignment: the existing adapter can express it, but the native guard rejects it.
A small prospective native contract integration could permit an explicit coding
sampler without changing server defaults or rewriting captured requests. This is
not implemented, and these observations do not prove lower temperature would fix
the syntax, missing-helper or stale-edit failures. Further live work requires a
new genuinely reviewed related item and fresh authority; B-0051 is now consumed.
No additional Context framework or capacity benchmark is justified by this run.
