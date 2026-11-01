# B-0050 failure analysis and linked canonical prerequisite

Preparation and human Intake review are complete. No new coding inference,
execution grant, candidate, reviewer inference or integration plan is asserted.
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
WorkCycle slot is unused. Coding execution still requires distinct authority.

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
narrowing requires genuine human Intake review; it is not a claim that the
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
Deterministic projection remains enabled. Exact authority is still required.

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

The next productive operation is a separately scoped coding grant for the
approved linked prerequisite. A favorable candidate
would require independent reviewer authority and separate host disposition before
read-only integration planning. Broader facade repair, review-driven repair,
failed-candidate diagnostic review, automatic selection and closeout remain open.
This checkpoint establishes improved supervision and the exact ownership boundary;
it does not establish another live-model outcome.
