# Oracle integrity for bounded coding evaluations

The supervisor owns task expectations, diagnostic feedback and withheld acceptance.
Before live entry, use the following preflight as a required gate for a newly
authored deterministic evaluation. This is empirical validation of the declared
finite cases, not mathematical proof, model authority or a general certificate.

1. Write concrete observable obligations and boundary semantics. Include normal,
   edge and empty inputs, identity/mutation constraints where applicable, and
   explicit units/coordinates. Keep focused diagnostics separate from withheld
   acceptance; neither may disclose the intended implementation.
2. Derive nontrivial expectations independently: a finite reference, mathematical
   invariant, unit-cell enumeration or direct byte/identity calculation. Record
   the method and its scope. Copying literals into a second table is not an
   independent cross-check. Review reference provenance independently of the
   candidate implementation.
3. Use `devtools.evaluation.preflight.check_oracle_expectations` to compare the
   recorded values and require exact obligation coverage, distinct named cases,
   documented derivations and normal/boundary/empty coverage. It reuses Evaluation
   identity coverage and performs no execution. The caller retains the supplied
   `OracleComparison` records. This detects disagreement and missing declarations;
   it cannot verify that a claimed independent derivation was honestly obtained.
4. Execute the actual oracle predicates against the independently justified
   positive observations. Include wrong-value/missing/foreign-value negative
   controls. Execute the starting implementation and establish assertion failures
   for the intended obligation, with passing unaffected controls. Existing pytest
   and managed Commands/FixedCheckTool remain the execution owners. A nonzero exit
   alone is insufficient: distinguish assertion failure from collection/import,
   runtime, encoding, timeout, cancellation and unavailable-result errors. Treat
   any ambiguous or incomplete preflight as a blocker before inference.
5. Freeze exact source/test/controller hashes, observed outputs, check selection,
   environment, scopes and finite budgets. Require the same hashes at live entry.
   Record any failure without changing the oracle after model output. The host
   must reject live entry unless all these checks pass; the comparison function
   alone does not authorize it.

Evaluation owns comparison validity; task-specific predicates and reference
methods remain with the evaluation's host. No registry, test DSL, Command runner,
coding loop, universal reference implementation or new authority owner is added.

## Reliability-0001 review

The half-open reservations `[1,3)` and `[5,8)` intersect `[2,6)` in `[2,3)` and
`[5,6)`: each has length one. Independently enumerating occupied unit cells gives
`{2,5}`, also two. The frozen expected three is incorrect. The new maintained
comparison test rejects it. Original frozen artifacts and actual false feedback
remain unchanged.

The second proposal had two exact anchors in the same current file that both
included `intervals.sort()`, `total = 0`, and `current_start, current_end =
intervals[0]`. Atomic admission correctly rejected their overlap before any
application. Each native call received `REFUSED` / `Edit anchors overlap.`;
the original calls and source were retained. With only two proposals authorized,
that refusal exhausted the primary run. The shared process would allow a newly
selected proposal if budget remained; it never splits/replays an old batch.
For this two-anchor case, the relationship is recoverable from the exact supplied
anchors and common refusal. No defect requiring an edit-engine change is
established, so this increment preserves those semantics. More detailed conflict
indices may be useful in a separately justified multi-edit usability change.

## New maintenance scope

The authorized follow-up revisits B-0035's first-request inventory obligation.
It is a real missing neutral-host capability, not a new synthetic task. The
new linked evaluation freezes independent metadata/identity/privacy predicates
and separately withheld continuation/currentness checks. It does not reopen or
change Case 0003 or Reliability-0001. Source, proposal and Context limits remain
unchanged. In particular, the existing 32,648-byte repository owner has only
120 bytes of margin under the 32,768-byte resulting-source ceiling; this is a
recorded feasibility constraint, not authorization to raise the limit.

## Observed maintenance result

The [frozen follow-up](../../experiments/local_maintenance_feedback/REPORT.md)
passed its independent oracle preflight, then made eight real local-model
requests and two proposals. Both were refused for resulting-source size;
no application or worker validation occurred. Independent grading of the exact
unchanged archive retained the original inventory failures. No model-authored
production repair was integrated and no supervisor patch replaced it.

This delivers a reusable finite preflight comparison plus an actual supervised
consumer; it does not demonstrate successful local maintenance or effective
validation-feedback repair. Source-owner self-editability is the next measured
constraint. Original cases, limits, adaptive policy, effect authority and
historical outcomes remain unchanged. The complete protected validation receipt
identifies the committed implementation and physical inputs separately.

## Committed validation

The unchanged `uv run python scripts/validate_development.py` gate passed
**3830 tests, 2 optional skips**, with configured **100% production
line/branch coverage**, on committed implementation
`9aae92ca8ac176c3a15940028b7a64a671da1ba1` (tree
`18236317f4086eb21c0bc53f606ca362e912841d`). The captured command ran from
`2026-10-29T14:37:13.759031+00:00` to `2026-10-29T14:59:38.148761+00:00`,
elapsed 1344.156475 seconds, exit 0. Physical input hashes remained
unchanged. The [machine-readable receipt](../research/code-audit/supervisor-feedback-20261029.json)
records exact commands, versions, source/test blobs, input identities and outcomes.

The focused suite passed 439 tests. Ruff, supported formatter checks, strict
mypy and repository layout passed on the same committed executable inputs.
The independent retained-attempt verifier passed without inference or effect
replay. JSON/JSONL, canonical Intake, local links, whitespace, original-case,
forensic and historical-reference checks are recorded separately. Python 3.14.3
on Windows was tested; no new comprehensive Python 3.12 compatibility result is
claimed. Retained experiment tests were hashed for preservation but remained
excluded from protected collection under the unchanged profile.

These checks establish the supported preflight implementation and existing
repair semantics, not successful B-0035 maintenance. Documentation-only closeout
preserves the validated executable inputs; actual accepted-main publication is
independently recorded in the receipt after ordinary Git integration.
