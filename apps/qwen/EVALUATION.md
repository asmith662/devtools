# Native Context worker acceptance and evaluation

Latest checkpoint: [native cohort 02](evaluation/native-cohort-02/README.md)
contains one accepted source-grounded coding task and one held-out repair-budget
failure with explicit exception-contract/lint tension. Eleven real local requests
used 53,865 input / 2,085 output tokens. No paid Codex comparison or production
candidate integration occurred; general reliability and successful live behavioral
repair remain open.

## Current native coding evidence

[Cohort 01](evaluation/native-cohort-01/README.md) has five real local runs over
three tasks: duration passed frozen behavioral checks (28 existing tests and
oracle), CSV failed across three worker conditions, and the held-out source task
failed read bounds before editing. Independent Ruff review requires style rework
for the duration candidate. Totals: 25 requests, 141,083 input / 7,341 output
tokens, 439.08 seconds worker time. No candidate was installed in production.

Trusted local evaluation no longer requires backlog/grant/terminal approval.
The direct API already supported it; the maintained CLI now uses the same worker
and source owner without those gates. Production WorkCycle authority remains.
Measured corrections add safe version/proposal refusal feedback and bounded
current-source retention. They improve host behavior, but CSV acceptance did not
improve. The held-out outcome was not used to tune another worker or rerun.

The Qwen effectiveness goal remains **OPEN**. There is no controlled Codex
comparison, no measured cost superiority and no proof of general coding or
native test-feedback repair reliability. The next priority is source-exact edit
grounding, task-relevant retention and actionable read bounds on fresh cases.

Prepared-Context and on-demand native Tools use the same coding loop.
Scripted models establish host correctness, not Qwen competence. Historical
results are immutable; this increment issued no coding grant.

## Reproducible bounded comparison

Retain this small, unblinded regression population of genuine development tasks:

| Case | Frozen source baseline | Independent acceptance | Historical prepared result |
| --- | --- | --- | --- |
| Markdown fences (`apps.qwen.tasks.MARKDOWN`) | `d9a118315450b1e3df8bc00b6bbc29798845877b` | existing tests + eight-scenario oracle | accepted; 2 calls, 1 repair; 8,178 input / 525 output; 34.76 s |
| Python AST segments (`apps.qwen.tasks.SOURCE_SEGMENTS`) | `11225000d7c1e728fa1313f92a0c54214b75a426` | existing tests + 48-combination oracle | rejected; 3 calls, 2 repairs; 19,587 / 1,848; 105.74 s |
| JSON object compatibility (archived B-0048 definition) | `75cc74f7acda36cf91e91251efae8f9b3054f02a` | pinned Python 3.12/3.14 oracle + existing JSON tests | accepted candidate; 3 calls, 2 repairs; 15,390 / 530; 101.10 s worker |

The first two definitions freeze source/test/oracle hashes. B-0048's archived
assignment is `179531289e28506c6a87508990a7d7aa0d14c76263d098c2a50ae099e659e298`;
task identity `3ea9361853c830c05920196a78b138b926dd9738bd7dc0eebbfe6d84c7987032`.
These are historical baselines, not instructions to replace current files,
resume B-0048 or reuse its old grant. Its accepted source remains unintegrated.

For a prospective separately authorized comparison, freeze equal objective,
source/test hashes, admitted corpus, independent oracle, profile and output/time
bounds. Change only `context_mode`; use three total requests for a matched-call
comparison. A separately labeled exploratory arm may permit ten on-demand
requests, but cannot claim a one-variable comparison. Derive mode variants with
`dataclasses.replace(task, context_mode="on-demand")`; their distinct digests
require actual assignment review and authority. Use a new approved work identity
when required, never reset a consumed dispatch. All branch operations use the
single canonical checkout.

For each admitted run record acceptance, baseline oracle failure, model calls,
native calls requested/attempted/returned, localized paths/units/spans, disclosed
source/result bytes, provider input/output tokens, model/validation/wall time,
repairs, refusals, interruptions and supervisor intervention. Unknown consumption
remains UNKNOWN. Report per-case results; different tasks/protocols do not show
Codex savings or cost superiority. Familiar historical cases and this small
population cannot establish generalization. No on-demand coding outcomes have
yet been measured with real Qwen.

Reproduce host acceptance without inference:

```powershell
uv run pytest --no-cov tests/apps/qwen tests/scripts/qwen/test_coding_worker.py tests/scripts/backlog/test_delegation.py
```

Scripted end-to-end acceptance exercises native search/read, a failed edit,
actual test feedback, corrected proposal and unchanged Markdown oracle in the
same loop. Other regressions cover LF/CRLF, exact scope, drift/aliases, expansion,
relationships, malformed/mixed calls, exhaustion, cancellation, selection,
restoration and the existing delegated WorkCycle. None is labeled live competence.

## Measured read-only native conformance — 2026-10-19

The assignment authorized read-only local smoke tests, not coding. The unchanged
Qwen3.8-27B UD-IQ4_XS/llama.cpp profile used 32,768 Context tokens, thinking off,
at most three requests and 512 requested output tokens/request. No edit or
command operation was disclosed.

| Request | Native actions | Input / output | Model seconds | Termination |
| --- | --- | --- | --- | --- |
| 1 | two source searches (symbol, file) | 868 / 89 | 10.087 | tool_call |
| 2 | two versioned source-range reads | 4,835 / 287 | 16.302 | tool_call |
| 3 | final answer | 6,449 / 269 | 13.126 | normal_stop |

Total: **12,152 input / 645 output tokens, four accepted reads, 40.037 s** wall
time (39.515 s summed model wait). New Tool JSON was 9,962 bytes, including 2,136
exact source UTF-8 bytes. Peak observed prompt occupancy was 19.68%. Cache,
reasoning and Codex coordination usage were unavailable. This is not coding-task
economics or a comparison with Codex.

Qwen found `_extract_source_segment`, read it and its byte-offset helper, and
described UTF-8 byte-column coordinates. Subsequent requests contained the actual
native assistant calls and correlated Tool results. Both scoped source/test files
were unchanged. This proves live search/read continuation, not successful coding,
automatic Context sufficiency or superior ranking.

Private receipts: `.local/qwen-coding-worker/native-context-read-only-02/`, with
frozen task/tools/settings, requests/responses/results and profile provenance.
Task digest `f440fc86fb1d8c794e67a6184c648d98275242ccd787f473f21884152c952f0d`;
result digest `77eada8eb5df492922f44bdd41906c6d0bf4e0d3e6fd61a665f1899e66fe2c90`.
This ran pre-commit code; final hardening is checked deterministically, not
represented as another live run.

`native-context-read-only-01` remains a pre-dispatch failure with **zero model
requests**: recursive discovery encountered inaccessible preserved evidence.
The canonical discovery API now supports explicit-address metadata probes and
both worker modes use them. No failed model invocation was retried.

## Local development and production authority

Earlier assignments incorrectly treated deleted-checkout standing delegation as
a prerequisite for local coding evidence. Those grants remain historical and
invalid; they were not rewritten. The maintainer explicitly corrected the
boundary: a trusted local host invocation may perform bounded evaluation using
the existing task, source owner and worker, without backlog promotion, grants
or terminal confirmation. No new authorization mechanism was introduced.

Governed WorkCycle production progression, integration, protected publication
and privileged effects retain separate authority. Local evaluation outcomes are
evidence and candidates only. No pending proposal or B-0048 slot was promoted,
reset or redispatched. Qwen remains the immediate workstream; this checkpoint
does not recommend switching to Learned Intelligence or another major system.


## Source-grounded native cohort 02

The maintained working set retains all current observed source regions instead
of pinning arbitrary prefixes. Authorized range errors are recoverable; native
edits require observed current source; optional frozen Ruff/format gates feed
bounded repair. Two fresh cases ran: regex consistency ACCEPTED (4 calls), command
output limits REPAIR_BUDGET_EXHAUSTED (7 calls, 2 repairs). Total 53,865 input /
2,085 output tokens and 122.62 worker seconds. The held-out first edit passed
behavior but conflicted with Ruff TRY004; repairs failed to reconcile the explicit
ValueError contract. This task-design tension limits the conclusion. No active
source exchanges were evicted and all admitted edits reconstruct exactly.

See `apps/qwen/evaluation/native-cohort-02/README.md` and `results.json` for fixed
criteria, raw evidence references and limitations. One genuinely accepted native
coding case is evidence of capability, not general reliability or measured
superiority. Live successful behavioral repair and a fair Codex comparison remain
open. The historical duration style-rework candidate and all cohort 01 records
remain unchanged. No candidate was integrated or protected source published.
