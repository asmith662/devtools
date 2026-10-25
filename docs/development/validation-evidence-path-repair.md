# Validation evidence, Commands custody and Git path repair — 2026-10-25

Three independently reproduced defects are repaired on main through normal
GitHub [PR #17](https://github.com/asmith662/devtools/pull/17). Starting main
`6e82319ecc0088d36f86fc1e30d7915f5fa1a2e0`; validated production `1a9e3ff1e56aebb8522c4d437d46de5f31679389`;
accepted main `ae88c69267961cf6a73bf41454a08cb8f97a14c4`, tree `26a93efebe7731ae1953eca7de0b0e67884b9cef`.
[Exact evidence and input identities](../research/code-audit/validation-evidence-path-repair-20261025.json).

## Corrections and bounded guarantees

| Owner | Original behavior | Corrected contract |
| --- | --- | --- |
| `integration/local.py`, `validation.py` | Same result/base/files inherited passed evidence after ignored `.ruff.toml` changed; fresh Ruff failed but closeout committed. | Fresh-only protected validation before every new commit. Saved/legacy/unrecognized proof never reused. Unpublished committed replay validates its exact active HEAD; accepted identical remote ref is observation, with no current eligibility claim. |
| `apps/qwen/commands.py`, `change_checks.py` | Fresh adapter completed its command, then collided with existing `coding-command-01.json`. | Atomic directory reservation and durable intent precede command entry. Existing names remain unavailable across instances. Only the reserved journal is completed; persistence failure never retries an external effect. Bundle/change-report consumers share this allocator. |
| `integration/lifecycle.py`, `local.py` | Git quoted `tests/test_π.py` was treated as a different filename. | Existing Checkout NUL-delimited reader owns staged/untracked/replay/closeout path sets. Exact scope/content refusal remains. |

Commands fix `4422a6d973068548a0b0421a8abb20b4ff5c8bc7`;
path fix `175878f17af0f00ab30163a7d1301db43abd238c`;
freshness fix `1a9e3ff1e56aebb8522c4d437d46de5f31679389`. No framework parser, executor, dependency engine,
authority layer, configuration or model policy changed. Framework `src/`, frozen
science, root configuration/dependencies and historical refs remain intact.

## Independent tests and validation

Original probes ran before edits on authenticated main. The single-real-Ruff
fixture never claims to execute the full protected gate. New permanent negatives
also expose original receipt collision, stale passing eligibility and exact Unicode
population refusal. An initial plugin import failure and a transient fixture-owner
mistake are explicitly excluded from product evidence.

Permanent tests use actual ToolRunner, real managed checks, literal source files,
Checkout/Git, local commits and bare remotes. They cover existing receipt
immutability, overlapping adapters, failed pre-entry reservation/intent,
post-entry persistence ambiguity without retry, unexpected source bytes,
unsupported profiles, absent semantic review, delayed committed validation,
same-commit remote observation, Unicode/special names and unplanned/modified files.
The maintained freshness suites preserve unchanged scoped reuse and reject
test/configuration/runner/selector drift while ignoring unrelated scoped artifacts.

Final **committed** protected gate: **2903 passed,
2 opt-in live skips, 100% configured production branch coverage**;
pytest 1112.8s, managed 1114.868s, exit0.
Supported Ruff/format and strict mypy pass with identical input hashes. Exact
post-main executable inputs match that gate; **265 focused post-main tests pass**.
Coverage is the unchanged `devtools` profile, not a new claim of exhaustive
application/script branch coverage. Broad frozen/generated science lint is not
reported green or reformatted.

## Remaining boundaries and canonical disposition

Existing proposals d58697fd,84a5d9b1,b0c02dbf receive append-only delivered evidence;
no new proposal, approval, B-number, grant or parent closure.
Six advisory records were appended across the three existing proposals: three
repeat the same rationale after a private closeout helper failed and retried with
an incorrect reference-key check. All immutable records remain preserved and the
helper is corrected. This duplicates no implementation, proposal or authority;
the exact hashes and unchanged states are recorded in the evidence artifact. Intake remains
administratively PENDING_REVIEW and must not schedule these delivered repairs again.
For d58697fd this is **partial bounded delivery**: transitive inputs, toolchains,
environment, cross-profile reuse and HEAD-sensitive validation remain open.
There is no supported whole-protected-profile cache; scoped CodingCommands
`is_current` reuse remains available under its existing declared-input contract.
A nonprotected preview can supply the candidate subject for semantic review;
the commit invocation itself runs protected validation, avoiding an unnecessary
extra protected preview. Review and validation are still separate requirements.

Reservations survive interruption and need no stale-lock cleanup. Trusted local,
cooperating writers are required; neither exactly-once external effects nor
power-loss durability is established. A receipt/validation hash is not semantic
review or publication authority. UTF-8 path identity follows the existing contract.
Windows exercised Unicode, spaces, ampersands and parentheses. Literal filesystem
quotes/newlines are POSIX-only cases and were not executed here.

All 13 forensic files and scientific history remain preserved. Prior RI, worker and
Checkout repairs remain delivered. RI93/93 original fixtures,606/606 experiment
source and188 historical exact-version obligations are unchanged; A+C is unapproved.
The next [frozen Evidence/usage/custody/projection cohort](../research/code-audit/execution-evidence-next-cohort.json)
has not begun. Wider review/publication/durability and framework auditing remain active.
