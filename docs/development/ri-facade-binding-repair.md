# One-facade imported-member binding repair

Delivered production correction for pending proposal
[ff4c4110-9c3b-480d-8f0f-77cf4610b700](../backlog/proposals/ff4c4110-9c3b-480d-8f0f-77cf4610b700/proposal.json).
Starting integrated main: `368ae557ff2eb9f9dad69dfcbc3bcc7264ae942c`. Production commit:
`cf9db4af17516dc19092f1ae18c197783f1f5b3d`. Accepted through [GitHub PR #8](https://github.com/asmith662/devtools/pull/8),
verified main `5a5485e98908922722ba2a4b177094364c1aac31` and tree `39596bf80f77e52068127f3b1affe636e801e045`.
This is bounded maintainer-authorized development, not a WorkCycle receipt,
architecture approval, scientific result or new autonomous-agent evaluation.

## Independent failure before production changes

Real retained-source/AST probes reproduced simple MatchAs, starred MatchStar,
mapping-rest MatchMapping and ExceptHandler aliases competing with a facade
import. Direct module lookup correctly refused; the old imported-member resolver
and References fallback incorrectly produced a target function. Actual admitted
ContextTools dispatch through ToolRunner exposed the same false target. Plain
facade and ordinary-assignment controls behaved correctly. Source fixtures were
never executed and no model was invoked.

Permanent independent negative tests collected on the original implementation:
**25 assertion failures, two passing controls, zero collection errors**.
They additionally proved the same chain could ignore final-target rebinding or
an unknown decorator. These are production code-path counterexamples, not
evidence of historical scientific corruption or edit-authority bypass.
Original audit evidence remains unchanged in
[the source/role audit](../research/ri-configuration-role-closure-audit.md).

## Implemented boundary

- `python/imports/members.py` reuses `modules.bindings.iter_non_name_bindings`
  within each module-body statement, excluding nested function/class namespaces.
  `PATTERN_OR_HANDLER` support anchors the containing retained facade statement.
  Canonical module lookup also guards namespace uncertainty and the final target
  binding; syntactic function presence is insufficient. No second parser,
  binding-name extractor or generic evaluator was introduced.
- `python/references/declarations/resolution.py` permits fallback only for
  unresolved/non-declaration direct members. An authoritative ambiguous outcome
  is retained and never upgraded. Native source/dependency identities and valid
  deterministic ordering remain intact.
- Seven production-commit paths comprise two source files, three permanent test
  modules and two package contracts. Exports, configuration, lockfile, Commands,
  edit authorization, module/base owners and WorkCycle are unchanged.

The one-facade contract remains direct sync/async functions, not recursive or
class reexports. Direct/imported class References remain supported. Capture and
handler lifetimes differ; both conservatively prevent unique binding claims on
either side of a facade import. This is not runtime later-use evaluation.
Nested-local/unrelated names, valid aliases, before-import Reference refusal,
ordinary assignments, stale/foreign frames and inconsistent nominal content
retain independent tests. Syntactic declaration discovery remains available.

## Final committed implementation validation

- Focused module/import/Reference/base/function/source/Planning/native Tool suites:
  **565 passed**. Post-promotion bounded suites also passed; exact receipts below.
- Supported `ruff check src tests apps scripts`: PASS.
- Supported formatter check excluding retained `tests/experiments`: PASS,
  **634 files**. Existing COM812 compatibility warning is not hidden or a failure.
- Configured strict mypy: PASS, **520 source files**.
- `uv run python scripts/validate_development.py` ran on clean committed
  `cf9db4af17516dc19092f1ae18c197783f1f5b3d`: **2842 passed, 2 live skips,100% production branch
  coverage**, zero missing lines/branches; pytest 836.83s,
  managed elapsed 838.63s. Thresholds and exclusions unchanged.
- Exact input manifest `c7be73b5c444ea7e090e70900ed95007ecfa2ac150f89bb16c864d0ecb303085` and tree bind the actual gate;
  post-gate committed executable blobs did not change. GitHub accepted the same tree.

The physical gate manifest and post-main manifest differ only for
`imports/docs/overview.md` and `references/declarations/resolution.py`:
Git checkout converted LF bytes to CRLF. The evidence independently verifies
the old hash equals the canonical blob's LF bytes and the new hash equals that
same blob's CRLF bytes. No non-newline source/configuration change occurred.
Post-main305 tests include the binding, exact-source, physical-line, Commands
and actual ToolRunner regressions. Physical hashes are not misreported as equal;
the protected gate authenticates the exact committed tree and the post-main
checks authenticate its destination checkout behavior.

The [exact validation/merge/fixture/Intake evidence](../research/code-audit/ri-facade-repair-20261024.json)
contains commands, actual exits, log hashes, source/test blobs, original observed
inputs and final coverage totals. Local main was safely fast-forwarded after
API and independent remote Git confirmation. No protection setting, review,
grant or receipt was fabricated; no historical ref was deleted.

## Backlog and remaining audit

The original P1 UUID receives append-only **implemented-and-merged** ADVISORY
evidence. Intake has no delivered/closed enum; no approval, B-number or parent
closure is invented. Do not schedule this bounded implementation/adoption again.
The delivered three-owner proposal16b27e74 remains separate. Physical-line,
exact-name, historical SourceSpans, scientific binding verification/consumer and
historical recovery concerns retain their own owners and custody.

No next audit cohort was launched. Original fixture credit remains **67/93**
(four substantive bodies and22 namespace paths remain), historical experiment
source **606/606**, older versions **15 full/168 unread/20 tip-only**. The two
already-reviewed RI fixture records now retain explicit authored-delta evidence;
this does not grant unrelated path/version credit. The application test delta
is covered by the production commit and actual deterministic ToolRunner tests.
Next: close the four substantive fixtures/namespace surfaces, begin the coherent
Execution/ToolRunner/Checkout/WorkCycle audit, and continue188 historical versions
in the established responsibility groups. A+C is still recommended and
unapproved. The broader audit and successor-session handoff remain unfinished.

All13 original forensic file hashes remain preserved. Final documentation-only
closeout uses this same ordinary branch and a normal PR; its containing commit
and GitHub history authenticate publication without direct main writes.
