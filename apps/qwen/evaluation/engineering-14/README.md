# Engineering 14: task-local successful command exit codes

## Useful maintained obligation

Developer tools use nonzero statuses for ordinary outcomes: actual `git diff
--no-index` returned 1 with a valid difference during qualification. Commands
previously classified it failed with no per-command opt-in. This capability lets
both Qwen and Codex callers declare expected statuses through the existing typed
Command/Tool boundaries. It is not execution authority, shell support or a new
policy framework. No duplicate Git, validation, editing or closeout Tool was built.

The discovery is `d9416198-66c7-40b9-b566-e2a8806a81b5`, still PENDING_REVIEW; local
development/publication authority comes from the current trusted assignment,
not proposal approval. Parent B-0009 stays open. The task is new to maintained
Qwen evaluation identities, checked before inference; it is a single fresh
development case, not a controlled comparison or general-proficiency benchmark.

## Frozen independent contract

[Task](task.json) and [manifest](manifest.json) freeze baseline
`89fb5d0316e4a0237cadf128d6593c4a00a26023`, oracle `8503ade1b8692531ed651ffe31fec200d73b4e2ed35a1e63220b0eec5e929f56` and limits:
24 requests, 1800 worker seconds, six proposals, 16 components, 32 read/check actions,
8192 requested output, existing 4096 region/8192 aggregate/16384 patch bytes.
Thirty admitted resources contain plausible owners/dependencies; edit targets
are not disclosed in the initial prompt. The verified 32K/q4 K,V/thinking-off
Qwen3.8-27B IQ4_XS service and worker are unchanged.

The public contract adds immutable `success_exit_codes: frozenset[int]`, default
`frozenset({0})`, plus variadic replacement and default-reset fluent methods.
Empty sets accept no exit; codes are ints excluding bool, including int subclasses
and literal negative statuses. Every fluent input must validate before deduplication
can conceal a boolean equal to an integer. All existing value/fluent/hash behavior
survives. Result success is exact raw-code membership in its own Command's set;
failure is its complement. Executor/Tool/handle events, identity, bytes, output
limits, stdin/environment and errors retain their existing contracts.

Preflight on Python 3.14.3 passed full positive model/real-child/Tool/handle fixtures
through a host-only adapter using the actual executor. The negative baseline
executor fails opted-in child classification. Baseline oracle failure is the
missing public capability; 88 original regressions pass. A relative-path fixture
mistake was corrected before inference. An unrelated existing formatter issue in
tools/disclosure.py is recorded and unchanged; all permitted source quality checks
pass. No private reference, oracle code or permanent tests were exposed to Qwen.

## Genuine implementation and behavioral repair

Qwen inferred owner paths from the public API, inspected the model/result,
package exports, Tool bridge and existing tests, searched for prior behavior,
and requested baseline tests. There were 10 direct reads, two searches and one
fixed test check; 13 successful non-edit actions disclosed 25,394 source-text bytes
within 48,639 response bytes. It did not inspect or modify the executor; reuse
through the existing result/Tool paths is independently checked.

Turn 9 atomically admitted six edits across Command and CommandResult. All 88
regressions and source Ruff/format/typing passed, but behavioral acceptance found
that `(1, True)` could lose the boolean during deduplication. The actual diagnostic
and current versions reached turn 10. Qwen changed the correct fluent-method owner
to validate raw arguments first. The unchanged full oracle then passed, preserving
earlier passing behavior and all regressions. This is one genuine behavioral
repair, not incomplete-interface completion, a lint fix or a seeded failure.
No Codex implementation hints/patches, worker edits or additional session occurred.

Final result: **ACCEPTED**, 10 requests, two admitted transactions, seven edit calls,
zero refusals, one behavioral repair. Worker runtime 212.997 seconds; 136,805 input /
3115 output tokens. Final input 25,533 tokens leaves 5187 safe generation tokens after
2048 safety. No whole native exchange was omitted and no Context budget failure
occurred. Exact per-turn requests, tools, versions, tests and usage are indexed in
[results](results.json); raw immutable evidence is under
`.local/qwen-coding-worker/engineering-14/devtools-success-codes/`.

## Review, validation and publication

The exact Qwen model source is
`899208f3a7d6a8dfed73dda4d42dbfd279bda8bb587a0fa80510abc49515a05f`;
result source is
`1ebf20c0c88591042513f5c62b6868449b846f67f329819fb28a8890b55b98ff`.
The executor and Tool adapter remain unchanged. Independent review confirmed
frozen/slotted invariants, raw-argument validation, structural equality/hash,
membership interpretation and preservation of execution facts. Codex supplied 28
permanent regressions, not semantic or mechanical replacements of Qwen code.

Existing WorkCycle local closeout authenticated the candidate, ran 116 focused
tests, scoped Ruff/format/strict typing and one protected gate, bound the exact
Codex review and feature-published `73e5ee07ee490ac6aa9319892585e937fec9a876`. Full-project mypy checks 497 files.
Protected validation: 2,301 passed, two skipped, 100% production branch coverage;
527.25 pytest seconds/532.16 pipeline seconds. Exact logs are indexed in results.json.
A separate actual post-publication Git diff through CommandTool retains raw exit 1
and reports succeeded=True under the explicit 0,1 set; this is a supervisor probe,
not another Qwen task. Main remains
`862bda2d3d1d812893f84ab69691fc068ecce268`; this is feature publication, not protected
adoption or backlog promotion. One physical checkout and 13 forensic files survive.

No Pi rerun, paid baseline, model download/service mutation, repository copy or
scientific experiment occurred. Worker time is separate from qualification,
independent tests/review and protected validation. Codex usage, active coordination,
RAM/VRAM peaks and energy costs are UNKNOWN/NOT_MEASURED.

Keep Qwen as the primary engineer using the unchanged harness. The first attempt
still violated an explicit type requirement; this repair does not establish
arbitrary-task reliability or model parity. The next concrete Commands obligation
is the previously exposed noninteger/bool output-limit validation issue, with its
exception contract independently requalified before a development continuation.
