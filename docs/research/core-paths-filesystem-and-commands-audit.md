# Core paths, filesystem and managed Commands audit — 2026-10-25

Delivered follow-through: [deterministic paths, filesystem entry custody and Commands collector cleanup](../development/core-resources-integrity-repair.md), production `2240ae9f8dfa38cc598396bb2677059ceaa4534d`, PR#23, verified main `ef0e3539a1afac20bfe65dfbac810456b5342804`. Final committed gate 2962 passed/2 opt-in live skips/100% configured production branch coverage;721 broad focused and594 post-main tests pass. Original bdcf3bbc/4cb7c397/37a647f2 retain implemented-and-merged evidence; do not schedule these bounded repairs again. Higher-layer authority/concurrency, broader B-0041/B-0006 and platform limits remain separate. All ten Core identity/time pins match main and remain unaudited; that is next. RI93/93,606/606,188 historical obligations and A+C-unapproved status are unchanged. Earlier notices below retain their dated meaning.

Reviewed integrated main `0e240ec102e9d54c92a3e85071586a9a8e74b308`. All **twelve frozen source/test bodies**
received full substantive review; [exact per-path dispositions and probes](code-audit/core-resources-assurance.json)
separate them from targeted dependencies. **479 maintained focused tests pass**;
fourteen bounded independent probes establish three P2 repair scopes. No production
source, maintained test or executable configuration was changed. This is a domain
increment, not whole Core/Resources or autonomous-lifecycle signoff.

## Findings requiring bounded repairs

| Severity / proposal | Observed failure | Owner and acceptance |
| --- | --- | --- |
| P2 / `bdcf3bbc-7d26-4826-bfef-f0171187b864` | Windows `C:relative.txt` with the same explicit `Z:/explicit-base` resolves under different directories when only CWD changes. | `core/paths/resolution.py`: explicitly refuse incompatible drive-relative input or establish an equally deterministic supported policy. Test foreign/same-drive, absolute and rooted forms. No new parser, root authority or sandbox. |
| P2 / `4cb7c397-e664-4379-893c-c36d3a739cef` | Real supported Windows dangling link is replaced by regular bytes under `write(..., overwrite=False)`, without an error. | `filesystem/writing.py`: existing-entry refusal needs lexical inspection. Preserve link identity and ordinary writes; test public BinaryFile/TextFile callers. This is separate from delivered Checkout collision prevention. |
| P2 / `37a647f2-0cb9-4a3b-a4d6-b61e2166bd12` | Failed stdout read returns a complete failed Command handle while one blocked stderr collector remains pending and uncancelled. | `commands/execution.py`: cancel/await owned collectors on error and preserve original failure, immediate-child cleanup and normal behavior. Existing fake's immediate-EOF sibling hides this state. Parent B-0041 remains broader investigation. |

The cleanup counterexample is a deterministic I/O-fault fake, **not** an observed
leaked live process or corrupted production run. The immediate fake child is
killed/reaped correctly. Real cancellation/timeout controls pass. A real temporary
file effect remains after actual child cancellation, as required: cancellation
does not imply rollback. No P0/P1, edit-authority or protected-publication bypass
is established by these probes.

Current RI/Checkout/Qwen callers add their own address, alias and containment
checks, so the Windows primitive defect is not proof of an admitted task escape.
Generic direct absolute ResolvedPath construction is supported; that is the writer
probe's input. Intake/WorkCycle/Qwen often resolve paths before writing and may
follow a terminal link to its referent instead; no lost live journal is asserted.
The separately probed concurrent destination-create race is an **existing documented
no-lock limitation**, not a claim that the API already guarantees atomic no-clobber.

## Ownership and real consumers

| Layer | Actual responsibility and consumer evidence |
| --- | --- |
| Core paths | Absolute immutable representation and explicit parsing/resolution; existing links follow native pathlib semantics. Direct construction checks absolute only. Does not own existence, file identity, containment, authorization or a path lease. RI observation, Resource IO, Commands cwd, Checkout and Qwen compose it. |
| Filesystem reading | Binary open, stat precheck, at most finite cap+1 consumption, accumulated legal short reads, postcheck before codec decode. Byte limits are not character limits or a total-process memory cap. None intentionally opts into unbounded reads. Streams close under tested failures. |
| Native source observation | RepositoryObservation re-resolves and checks root containment, reads exact retained text and derives content identity from what was read. This authenticates retained evidence, not immutable filesystem state during/beyond IO. ContextTools and edit admission add their own later correspondence/freshness rules. |
| Filesystem writing | Format/model-specific encoding of current structured state, sibling temporary write/flush/fsync then os.replace. Normally observers see old or complete new content. No parent-directory fsync, ACL preservation, locking, multi-file atomicity or power-loss transaction. Checkout custody/Intake/usage leases remain higher-layer responsibilities. |
| Managed Commands | Immutable direct argv, binary stdin/EOF, inherited environment plus launch-time overlays, independent byte-retention caps, bounded best-effort event queue, immediate-child cleanup. Qwen fixed checks, backlog Git and CommandTool/ToolRunner are real callers. Resource availability and valid argv are not authority. |
| Handle/events | One shared task/result, one event consumer, per-channel order with unspecified stdout/stderr interleaving. Saturation may drop even CommandExited; consumers must await the actual result. Cancellation of a joined awaiter can cancel shared execution. No maintained application live-event consumer was found in the bounded search. These are not durable framework Evidence records. |

Timeout covers post-creation collection, not spawn time or a universal wall-clock
deadline. Children may have external effects before refusal/cancellation. Only the
immediate child is managed; descendant cleanup is explicitly unsupported. No retry
or general transaction abstraction follows from the identified collector defect.

## Test and platform assurance

All six selected implementation bodies and all six test bodies were read in full,
including helpers and monkeypatches. The existing cohort now records each exact
blob, role, consumer, assurance gap and disposition. Additional dependencies have
explicit FULL_BODY_READ, TARGETED or TRAVERSED depth in the evidence artifact.
Running a dependency's test did not award body-review credit.

Path tests protect ordinary native parsing/base policy but often mirror pathlib
as their oracle; foreign-drive/CWD, UNC and link boundaries were absent. Writer
tests independently check bytes/current structured state and injected cleanup
failures. Their fsync-before-replace test records two separate call lists without
asserting temporal order; it does not independently prove the ordering in its name.
The bounded-reader stream replacement is deliberate and appropriate: real stat
input plus controlled short/growing streams protects byte consumption and closure.
It is not a false retained-source integration claim. Command fakes protect local
branches; boolean kill/wait flags are not OS reaping proof. Companion real stdin
cancellation tests and this independent real after-effect probe supply bounded
OS evidence. Event-value tests protect immutable equality/hash, not delivery.

Fourteen independent probes include ordinary paths, a stable outside-root link,
real binary boundaries, same-length mutation before open, regular/dangling writer
entries, the documented concurrent no-clobber limit, real output truncation/drop,
missing cwd, blocked-input timeout, actual cancellation and injected reader failure.
Missing cwd on this Windows system raises NotADirectoryError; no universal
CommandNotFoundError misclassification is claimed. Dot components allow native
separators/rooted fragments; this is mechanical parsing, not a Python identifier
or containment validator. No maintained dot-parser caller outside exports/tests
was found. Generic reads can return changed bytes after stat: not a snapshot bug.

Native Windows file/directory symlinks were constructible. Short/long path aliases
were confirmed using directory identity rather than false string equality. UNC
network shares, ACL failures, junction races, cross-volume replacement and POSIX
execution were not tested. Permission monkeypatches do not prove those OS cases.
An async-list mistake in the added private cancellation harness was corrected;
that failed run is excluded from product evidence. No live models, scientific
controllers or Devtools source-tree copies were used.

## Cohesion, backlog and finite next scope

The existing dependency direction is sound: paths/time below Resources, Resource
adapters below Tool/application orchestration, caller-specific authority above
both. Format codecs, path resolution and managed execution have compatible real
reuse; no competing parser/executor/store is warranted. Local writer leases in
Intake/usage and Checkout fencing protect different custody contracts and should
not be collapsed into a generic transaction primitive on this evidence.

Three **new pending P2 proposals**: bdcf3bbc-7d26-4826-bfef-f0171187b864; 4cb7c397-e664-4379-893c-c36d3a739cef; 37a647f2-0cb9-4a3b-a4d6-b61e2166bd12. No approvals, grants, B-numbers or
parent closures were created. Existing hard-bound reading038c927f, binary IOb3cc8ac0
and successful-exit interpretationd9416198 receive delivered-main assurance,
not duplicate implementation schedules. B-0041 retains broader cleanup semantics;
B-0006 retains stale package-documentation adoption/wording pressure. Some current
filesystem package docs still say feature-only/promotion-pending after actual main
adoption. This report records the discrepancy without changing source semantics
or rewriting historical engineering/scientific records.

Next, separately authorize the bounded P2 repairs. The next wider audit is
[Core identity/time](code-audit/core-identity-time-next-cohort.json): ten exact
source/test bodies, not started. These underpin grants, durable IDs, timestamps,
elapsed deadlines and budget checks. Remaining codecs/structured file models,
other Core helpers and process-platform boundaries remain explicit. Then continue
ModelInteraction/serving, Agents/Runtime, Persistence and complete applications/
dashboard/developer infrastructure. No endless Evidence/RI cohort is initiated.
RI93/93 original fixtures,606/606 experimental paths and188 historical exact-version
obligations remain unchanged; A+C remains unapproved. Thirteen forensic hashes,
scientific bytes and historical refs are preserved.

## Validation and publication boundary

Focused command selects Core paths, all filesystem/Commands, Command/Filesystem
Tools and RepositoryObservation: **479 passed in4.50s**, exit0, without coverage.
It is not a new protected gate. Documentation-only validation records JSON/JSONL,
links/layout, exact source/blob identities, Intake chains and whitespace. The prior
2937-pass/two-live-skip/100% production gate is historical inherited evidence,
not replayed or relabeled as this audit's test result. Publication uses one ordinary
audit branch and the real normal GitHub PR requirements; remote acceptance is
independently authenticated in the final completion report. No production fix
has been implemented by this audit.
