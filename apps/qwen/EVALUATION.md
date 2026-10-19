# Native Context worker acceptance and evaluation

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

## Authority and next checkpoint

### Fresh native coding evaluation admission — 2026-10-19

At `59f968d7dce44c6fdb01419e87dc9d12b36bb105`, the canonical coordinator
had only the historical `a5b20e0...` standing grant. The actual
`Delegations.active` check refused it because its coordinator is the deleted
worktree, rather than the canonical repository. No coding invocation, new
assignment, supervisory approval or grant was issued during this check.

An **inactive proposed policy** is available locally at
`.local/qwen-coding-worker/native-authority/policy.json`, SHA-256
`964e0946f9654b50efe3eff5d5082e79009c4bd7155a1baffad9fbd668168492`.
It passes the existing closed policy validator. It permits bug/refactor categories,
the exact JSON `list.py`, `base.py`, `conversion.py` and filesystem model
`text.py`, `base.py` source paths, plus the existing
`tests/resources/filesystem/test_json_models.py`. Per task: ten total model
requests, 4,096 requested output tokens/request, 900 seconds and three edit
proposals. Cumulative: three tasks, 30 requests, 122,880 requested output tokens
and 2,700 seconds. These are reserved/requested bounds, not provider-runtime
consumption guarantees. Model/profile and prohibited effects remain those of
the existing standing-delegation contract; no protected publication is allowed.

The sole allowed host oracle is pinned to
`ad1475355c33e6ba3173f884432bd23c2c17e47a45d2a1b3228f272bc1143fb0`.
Its local source is `native-authority/oracle.py` beneath the directory above.
It checks JSON-list construction, sequence behavior, nested immutability,
transformations, inherited validation and root-shape rejection on Python 3.12
and the worker interpreter. Independently executing the check against unchanged
source reproduced the constructor TypeError on CPython 3.12.13 and passed on
3.14.3. This is host acceptance preparation, **not a Qwen coding result**.
Exact check output is retained in `native-authority/verification.json`.

The current policy schema has a shared source allowlist, not separate grant-level
read/edit lists. Each future assignment must separately bind its one permitted
edit target and additional read-only paths. The broader allowlist makes discovery
across related modules possible; it does not authorize editing every retrieved
file in one task. This is bounded module-family discovery, not repository-wide
autonomous localization.

The single next operator action, from the canonical root in a genuine PowerShell
terminal, is to inspect the displayed policy and confirm only if acceptable:

```powershell
uv run --python C:/Python314/python.exe python -m scripts.backlog delegation-issue --policy .local/qwen-coding-worker/native-authority/policy.json --reference 'Maintainer standing decision: routine local JSON-list maintenance under displayed policy; Codex supervision; no protected publication' --expires ([DateTimeOffset]::UtcNow.AddDays(7).ToString('o'))
```

This command defaults to No and creates no coding dispatch. It is a proposed
decision reference to be adopted by the actual operator through confirmation,
not evidence that a decision already occurred. The automated session cannot
supply that maintainer terminal confirmation.

After issuance, fresh work approval remains independent: the JSON-list slice is
a prospective candidate, not yet an eligible canonical assignment. B-0048's
reviewed resource is `json/object.py` and its one WorkCycle slot was consumed.
Neither its approval nor its successful object-model candidate authorizes a
new JSON-list assignment. Use Intake to link/deduplicate the fresh slice against
the remaining B-0048 obligation and obtain the required backlog decision before
preparing its exact on-demand task and Codex review. Do not reset B-0048, reuse
its dispatch or widen its original review. The proposed three-task grant can be
reused only by independently eligible work satisfying these exact pinned checks;
new oracle code requires a separately reviewed grant.

**Disposition: BLOCKED_BY_AUTHORITY.** Zero new model calls; no coding outcome,
cost comparison or effectiveness improvement is claimed. No new worker
implementation was needed. Learning integration remains a separately scoped
boundary/acceptance review after an authorized coding evaluation.

Historical grant `a5b20e0b6ade4af3603b40521d9a3d3a3c69b3fc3fab221d14c6e1324b1946f0`
is bound to the deleted Qwen checkout. Actual canonical admission refused it:
`Standing grant expired, revoked or differs from host/scope`. It was not rewritten
or reissued. **Live coding-effectiveness evaluation is BLOCKED_BY_AUTHORITY.**

Select a genuinely unattempted approved maintenance item; freeze its canonical
branch/source/tests/oracle/read scope; obtain genuine current-root coding
delegation/manual authority with enough total calls; then use existing
`work-review`, `work-delegate`, `work-execute`, `work-status`. This note is not a
grant and does not authorize repeating B-0048. Integration requires separate
authority and review.

`src/devtools/learning` is absent. After this worker's review/adoption and a
legitimately authorized coding evaluation, the next learning step is a separately
scoped import/boundary and acceptance review of the maintained sibling Learned
Intelligence implementation, preserving provenance and comparing with this
non-learned worker. No learning package, learned routing, new resident model,
durable Memory, scheduler or multiple-worker system was implemented here.
