# Core/Resources integrity repair - 2026-10-26

The three bounded P2 corrections are implemented and merged through normal
GitHub [PR #23](https://github.com/asmith662/devtools/pull/23). Starting
main `30f5e2ac13e1908709e182ef05d164108b17ba75`; final validated production `2240ae9f8dfa38cc598396bb2677059ceaa4534d`;
accepted main `ef0e3539a1afac20bfe65dfbac810456b5342804`, tree `e6104939b6c8a21748eb858a723814bbae16322c`.
[Exact source, regression, input and publication evidence](../research/code-audit/core-resources-integrity-repair-20261025.json).

## Corrected existing owners

| Proposal / owner | Original behavior | Corrected contract |
| --- | --- | --- |
| bdcf3bbc / `core/paths/resolution.py` | Windows drive-relative input and foreign-drive base silently use ambient CWD. | Reject the incompatible drive before normalization; preserve deterministic same-drive (case-insensitive), drive-only, ordinary relative, native rooted and absolute controls. No new path parser or authority. |
| 4cb7c397 / `filesystem/writing.py` | Dereferencing exists check treats a dangling destination entry as absent and replaces it under overwrite=False. | lstat authenticates entry presence. Only FileNotFoundError means absence; existing entries refuse, permission errors normalize and unclassified errors propagate before preparation. Exact link and referent controls pass. |
| 37a647f2 / `commands/execution.py` | Failed output/input collection returns while siblings remain pending. | Both ownership boundaries cancel and join their tasks in finally; cleanup collects secondary exceptions while original error/cancellation/timeout semantics remain. No successful result or exit is fabricated. |

Path commit `e4194453f340c7bbf02f2bfc0888d9e13607e538`; writer commit `2c7d647094a5afa49d51a5cfd12b3cd81d4630f1`;
Commands commit `2240ae9f8dfa38cc598396bb2677059ceaa4534d`. Changes are limited to three source
owners, three existing test modules and four directly related package documents.
Public exports, dependencies, application code, authorization and frozen science
are unchanged. Package I/O/roadmap wording now records delivered-main binary and
bounded-read support without rewriting their original engineering outcomes.

## Independent reproduction and regressions

Before production edits, original bounded probes independently reproduced all
three on current main. Native Windows `C:relative.txt` with a foreign explicit base
returned different paths under two temporary CWDs. A real dangling file link was
replaced without an exception under overwrite=False. A deterministic reader fault
completed its handle with one sibling reader still pending, despite fake child
kill/reap. That is an owned-task defect, not proof of a leaked real OS child.

Permanent baseline regressions produced **9 intended failures and 10 passing
controls**; all collected against original existing APIs. No fixture/import error
is counted. Literal expected outcomes cover Windows foreign/same-drive, drive-only,
rooted/absolute and ordinary relative forms. Public BinaryFile/TextFile tests cover
live/dangling file/directory symlinks, absent and existing destinations, exact native
link spelling/inode/referent bytes, allowed overwrite and inspection errors.
An independent shared order log checks fsync precedes replacement.

Three-channel async fault schedules cover stdout, stderr and stdin failures,
secondary cleanup errors, timeout, caller cancellation and successful completion.
They assert actual collector task completion, settled finally blocks, exact original
failure on repeated awaits, one child entry, kill/wait and event/result semantics.
Existing real OS-child timeout/cancellation, output bounds, stdin and ToolRunner/
Checkout/Qwen consumers pass. Cancellation remains distinct from rollback: earlier
temporary-file effects remain in the independent real control.

## Validation and supported limits

Final **committed-tree** protected gate: **2962 passed,
2 opt-in live skips, 100% configured production branch coverage**;
pytest 1040.02s / managed 1042.111s, exit0.
Supported Ruff/format, strict mypy, layout/links/Intake/whitespace checks pass with
exact committed source/test/configuration identities. The broad focused suites
pass **721 tests**; accepted-main focused checks pass **594 tests** on
identical physical executable inputs. Coverage is the unchanged configured
`devtools` profile, not a claim of exhaustive application/platform behavior.
Broad frozen/generated lint is not newly claimed green or reformatted.

Native Windows path and file/directory symlink regressions actually executed.
Capability-only skips are limited to documented missing Windows symlink privilege;
no such unavailable case is claimed passing. POSIX behavior remains native and was
not newly executed here; UNC/mapped drives and junction variants are not certified.
Rooted Windows paths retain base-drive-root semantics, not containment below base.

No-overwrite is single-operation lexical admission, **not atomic concurrent
create-if-absent**. External writers may still race; higher layers retain custody.
Normal permitted overwrite still replaces complete destination entries. There is
no new locking, directory fsync, ACL policy, sandbox or generic transaction.
Commands still manages the immediate child only. No retry, descendant cleanup,
universal spawn deadline or rollback follows. Repeated/uncooperative cancellation
and broader lifecycle policy remain B-0041 concerns.

## Canonical reconciliation and next domain

The three original UUIDs each have one append-only implemented-and-merged advisory;
Intake remains administratively PENDING_REVIEW because no delivered state exists.
That does not schedule these corrections again. No proposal, approval, B-number,
grant or parent closure was created. B-0041 and B-0006 retain their broader scopes;
older bounded-read/binary/successful-exit and Checkout/Qwen repairs stay delivered.

The six affected frozen audit rows retain their original review blobs and receive
an explicit authored-maintenance/test overlay, not invented historical credit.
All thirteen original forensic files and historical refs remain preserved.
All **ten** [Core identity/time selections](../research/code-audit/core-identity-time-next-cohort.json)
match accepted main. Their status remains FROZEN_NOT_STARTED: this is the next
actual audit, not another open-ended process/filesystem investigation. RI93/93,
606/606 and188 historical obligations remain unchanged; A+C is unapproved.
