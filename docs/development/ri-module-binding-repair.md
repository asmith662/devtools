# Python module-binding integrity repair — delivered

Production correction is merged through [PR #5](https://github.com/asmith662/devtools/pull/5).
Implementation `ab994225872840bddcf66149256aaa7d46f7f9da`, accepted main `9ffc559fa5a6175d4d25f025ddb310553200fe53`, tree
`d2edc5b9a437e192982f6c368d3ba7503c75b16c`. Audit [PR #4](https://github.com/asmith662/devtools/pull/4)
first merged at `48a01216dde95ad2b7034844f3954fdc404f232e`. [Exact validation and identity evidence](../research/code-audit/ri-binding-repair-20261024.json)
binds these claims; the original audit and synthetic evidence remain unchanged.

## Correctness and repair boundary

An earlier `def f` or `class f` remained falsely RESOLVED after module-level
`case f`, `case [*f]`, `case {**f}` or `except Exception as f`. Those names are
string AST attributes, not `Name(Store)` nodes. Genuine source observation and
baseline-compatible permanent tests produced28 failures and4 valid source-order
passes before correction. Original twelve synthetic recipes independently exposed
local/imported Reference and base facts; no input source was executed or model run.

`python/modules/bindings.py` now extracts only pattern/handler names and walks
compound syntax iteratively without entering nested function/class namespaces.
Module declaration lookup, Reference module bindings and local direct-base
bindings reuse that inventory. Existing function-local scope analysis reuses
only the name extractor, retaining its own traversal. No parser, general scope
engine, runtime evaluator, identity hierarchy or public reexport was added.

Visible competing bindings retain conservative ambiguity even when a later
statement could overwrite them at runtime. A pattern capture is not equated
with the different lifetime of an exception alias: after the handler clears its
alias, the analysis cannot claim that an old declaration was restored. Direct
base evaluation retains its before-child cutoff; later module statements do
not retroactively alter that local base assessment. Existing source/dependency
identities and positive controls remain unchanged. Source declaration syntax
selection still finds the original declaration independently of binding truth.

## Permanent regressions and validation

43 new parametrized cases across existing Reference, binding, base and native
ContextTools test modules specify literal source and outcomes independently.
They cover function/class declarations, all four capture/alias forms, both
declaration orders, local/imported/qualified References and bases, later base
bindings, unrelated/nested scopes, handler use and exit, wildcard/unnamed syntax,
and retained declaration/source selection. Real ToolRunner dispatch now omits
false relationships while exposing the exact observed source. Existing ordinary
assignment, stale/foreign frames, source integrity, Unicode/physical lines and
Commands checks remain in the focused/full profiles. A fixture writer was
corrected to preserve authored LF bytes rather than implicitly translate them.

- Final affected suites:531 passed. Strict configured mypy:520 files, PASS.
- Maintained Ruff:PASS. Supported formatter:634 files, PASS.
- Exact committed protected gate:2808 passed,2 live skips;
 100% production branch coverage, no missing lines/branches, elapsed
 766.58 seconds. Canonical command and exclusions unchanged.
- Post-main bounded verification:239 passed; exact elapsed/hash in the evidence.
- Preliminary formatting including retained `tests/experiments` reported28
 existing discrepancies; none was reformatted. The supported check explicitly
 excludes that frozen tree. Broad root scientific Ruff/panic work was not run.

The first intermediate post-fix run exposed the fixture's LF/CRLF assertion;
another intermediate test requested undisclosed `inspect_source` rather than
the fixture's allowed `read_source`. Both tests were corrected without weakening
production checks. Final focused/static/gate results bind the final code. No
failed tests, coverage branches or validation thresholds were excluded to pass.

Accepted main has the exact committed production tree. Physical executable input
digests before/after Git checkout differ only for individually authenticated
LF/CRLF representations. Package Markdown also had a mixed-newline pre-gate
representation recorded with its committed blob; main materializes that same
Git blob canonically. Both hash domains and the unavailable old physical-byte
limitation are explicit. They are not claimed byte-identical. The post-main tests
exercised the actual installed representation; no executable-input exception.

## Production, backlog and audit disposition

[Pending16b27e74](../backlog/proposals/16b27e74-f553-40a8-b342-c3458a7b7a01/proposal.json)
has an append-only ADVISORY recording **implemented, validated and merged;
bounded acceptance criteria satisfied**. No implementation/adoption work remains
for the reproduced family. Intake has no delivered/closed proposal state;
PENDING_REVIEW is administrative review, not a request to code the repair again.
No unnecessary B-number, approval, grant or parent closure was invented.

Three previously fully reviewed fixture records receive authenticated new-blob
delta evidence: unchanged functions compare AST-equal, newly authored bodies
and `_snapshot` newline preservation were inspected. No new audit-cohort path
credit is granted: original fixtures stay57/93 with36 remaining; older versions
stay7 full/170 unreviewed/26 tip-delta-only; experimental source review stays606/606
at its defined depth. The next assurance cohort was not launched.

No native model behavior/effectiveness, edit-authority bypass or task completion
claim follows from deterministic tests. A+C remains unapproved. Runtime Python,
dynamic namespaces and broader execution semantics remain outside the bounded
resolver. Existing source-integrity repairs remain delivered and untouched.
All thirteen original forensic files, historical science and branch refs survive.
Normal GitHub rules/permissions/checks/reviews were authenticated at each merge;
no protection setting or ref was deleted, bypassed or rewritten.

Immediate continuation is the already selected RI assurance cohort and remaining
historical semantic versions, then the separately scoped Execution/ToolRunner/
Checkout/WorkCycle audit. No successor-session dossier is prepared here.
