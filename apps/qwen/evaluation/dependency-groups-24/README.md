# Static dependency-group RI (24)

The existing Python project-configuration settings owner now recognizes a
bounded static `[dependency-groups]` subset. **Production implementation and
permanent regressions are Codex-authored fallback software. Qwen did not deliver
an accepted implementation.** No worker or serving change was made.

## Contract and qualification

Ordered arrays of raw source-declared strings retain original group names,
order, duplicates and empty arrays. A declared empty table is an empty-tuple
presence setting; an absent table contributes `("dependency-groups",)` to
`absent_keys`. Unsupported whole groups retain their semantic key, source-bound
identity and reason with `value=None`; valid siblings survive. Includes, mixed
arrays and objects are not resolved or partly extracted. These are raw strings,
not validated PEP 508 requirements, installed packages or runtime compatibility.

Name grammar follows PyPA's ASCII form. Comparison lowercases and collapses
runs of dot/underscore/hyphen; every normalized collision is unsupported while
original names remain separate keys. Invalid names are retained as unsupported.
Declaration derivation deliberately advances v3 to v4; named analysis coverage
advances v2 to a descriptive dependency-groups v3. Existing public types/exports
and six-selector resolution ownership are unchanged. Resolution rederives and
authenticates the complete analysis, including settings.

See [qualification](qualification.md), [frozen task](task.json),
[manifest](manifest.json), and [unchanged oracle data](oracle.txt). The oracle is
retained as data rather than maintained application Python; the exact same bytes
are embedded in the frozen task and original runner captures. Initial oracle
quoting was corrected before inference. All fixtures parse with installed
tomllib; the baseline fails specifically for missing declarations. All 126
existing RI tests passed before inference. The legacy 17-absent-key assertion
is deliberately adapted to 18 after adding the named table, not weakened to
hide a behavior regression. It is separately attributed Codex test maintenance.

Semantic references: [PyPA Dependency Groups](https://packaging.python.org/en/latest/specifications/dependency-groups/),
[PEP 735](https://peps.python.org/pep-0735/), and
[name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/).

## Genuine Qwen outcome

Start: `bdf4d3590a751880998c841f005930757aadd3cf` on
`feat/qwen-context-worker`. Remote main was already
`5d979920d0728775ed529457c88f5b68b440c64f`; Commands PR #1 was already merged.
No mainline change or new PR was attempted.

The frozen ceilings were 24 requests / 1,800 worker seconds / six proposals /
32 read-check actions, unchanged atomic byte/component limits. No arbitrary
eight-response cutoff or additional recovery inference was used.

Ten genuine requests consumed **173,464 input / 3,117 output tokens**, with
**244.057 worker seconds** (236.281 model seconds, 2.979 validation seconds).
The assistant made 21 native calls: 13 inspections, four searches and four
replace_source components forming one admitted atomic transaction. First edit
was on response9. It incorrectly placed dependency groups under `project`,
contrary to the top-level specification. The independent oracle failed; existing task
regressions passed. The candidate also retained Ruff/format failures. Response10
searched for private oracle expectations rather than repairing the visible
top-level ownership mismatch; searches remained confined to authorized source.

The native objective named PyPA group semantics without supplying the complete
external specification text. This limits attribution of location/name-grammar
mistakes solely to model reasoning rather than concise semantic presentation.
It does not invalidate the qualified public oracle or change the failed result.

Request11 was never dispatched: its prompt measured **31,867 tokens** after
compaction (44,852 before), exceeding 32K with 2,048 safety and the minimum
2,048 continuation output. This is a measured harness capacity limitation
alongside an independently demonstrated model implementation defect, not proof
that the unseen repair would have failed. No successful repair is claimed.

All four edit components were admitted. Thus structured refusal diagnostics
were available but **not exercised**; no admission-repair success is claimed.
Native check_changes/is_current were available in the real request schema, but
Qwen invoked neither. Host pre-review freshness was therefore not run. A scripted
or Codex-only invocation is not substituted as evidence of Qwen Tool use.

Raw original provider requests/responses, observations, candidate, diagnostics
and result remain under `.local/qwen-coding-worker/dependency-groups-24/live/`.
The original disposition remains `CONTEXT_BUDGET_FAILED`. A separate supervisor
mistake added an untracked qualification document during Checkout, correctly
blocking final cleanup. After the process stopped, that document was moved to
ignored preparation and the existing default-No stopped-owner recovery was
explicitly confirmed. Baseline source and administrative branch were restored;
no owner was deleted or evidence rewritten. This cleanup issue did not cause
the earlier behavioral or Context failure.

## Separately attributed delivery

Codex wrote the implementation anew after authenticated baseline restoration,
using the frozen public contract and existing models. No partial Qwen source
was transplanted. The unchanged oracle passes, alongside 151 focused RI cases
(25 additional scenarios), scoped Ruff/format, strict maintained mypy (509
files), layout and whitespace checks. Focused project-configuration coverage
is 100%: 331 statements, 106 branches. WorkCycle authenticates candidate hashes,
installs source/tests, runs the final protected gate and binds supervisory review
and ordinary feature publication to that exact candidate. Final publication
identities and protected evidence are recorded in results.json.

Observed inference GPU use: RTX4090 Laptop, 14,006 /16,376 MiB VRAM and 97%
utilization during response9. No model/service configuration changes occurred.
RAM, energy, paid Codex tokens/cost and active supervision time are not exposed
or comprehensively measured. Worker time is separate from preparation, cleanup,
independent implementation/review and protected-validation time.

## Remaining work

Qwen did not independently implement this feature, use shared validation or
produce accepted software. Preserve that failure; do not retry this task under
another prompt treatment or infer general inability from a blocked continuation.
Observed issues are incorrect configuration ownership, ineffective diagnostic
interpretation and Context growth after further search.

A subsequent bounded production task should integrate these new declarations
into the existing Localization repository-role consumer: its generic fallback
currently labels non-project/non-build settings as tool configuration. Qualify
dependency-group support as project configuration without inferring a test/tool
role merely from group names; preserve exact native identities, unsupported
siblings and role-input authentication. This is distinct consumer integration,
not a new retrieval or Context framework. It needs its own independently frozen
oracle and must exercise native check_changes after candidate installation.
No follow-up is launched here.

B-0002/B-0009 retain their existing broader status. This RI slice and
the accumulated Qwen worker have not been selectively adopted to protected
main. Commands adoption is already complete upstream; do not reopen it or
merge feature ancestry wholesale.

Feature publication: `7e1b10033c8793440994ef6069c9c0482dea74f8`. Exact protected source/test SHA-256 identities, check logs, timings and review subject are retained in [results.json](results.json).

The final protected gate passed once: **2,563 passed, two skipped**, 100% of
**11,780 production statements / 2,944 branches**; protected command time
697.251 seconds (pytest 695.61 seconds). Publication reused that exact installed
source/test evidence. Documentation-only updates do not change the validated
production source or tests.
