# Checkout custody correction

This correction addresses proposals69688104 (owner fencing),30bd833e (recovery
consent) and3b2f566b (filesystem custody). The [original audit](../research/execution-ownership-and-recovery-audit.md)
and immutable probes retain the pre-repair behavior.

## Ownership invariant

An operation bound to epoch A must not restore or release source controlled by
a legitimate replacement B. Checkout uses one persistent local
`.local/backlog/checkout.lock` file, separate from its durable owner journal.
Windows uses a nonblocking native byte-range lock; POSIX uses nonblocking `flock`.
Each contender opens its own descriptor, excluding cooperating threads and
processes, not only tasks in one event loop. Contention refuses. The file is
never unlinked, replaced or treated as a stale claim; its existence is not authority.

The lock spans initial admission and all branch-entry effects, journal expectation
updates, and complete restoration/finalization/release. Recovery acquires it before
authenticating the confirmed journal and retains it through effects and release.
R2 cannot release A or admit B while R1 pauses before restoration. An old operation
that runs after B enters fails its journal comparison before effects.

New v1 journals include a cryptographic random custody generation, not a task grant
or parallel domain identity hierarchy. Each object retains its last sealed journal
digest. Normal finish and expectation updates require that exact on-disk journal.
Recovery requires the exact digest displayed to the trusted caller. Even a journal
update within the same generation invalidates old consent. Existing valid v1
journals without a generation remain recoverable by exact confirmed digest; no
historical generation is invented and no original record is rewritten.

## Consent and interruption

The CLI displays a journal snapshot and passes its digest with the genuine
default-No decision. `recover(..., authorize=..., expected_owner=...)` requires
that digest; all maintained callers migrated. No Boolean-only fallback exists.
Changed, foreign, corrupt, unsupported or missing journals refuse. A new owner
requires a new display/decision. The operator must first establish that the old
owner and any managed-command descendants are quiescent; a PID alone is not proof.

OS locks release on descriptor close or process termination. Failed recovery
retains its journal. A checkpoint before returning branches permits a fresh
decision to reconcile a crash just after that switch. Release is one same-volume
directory rename into `checkout-history/released-<completion-digest>/`, retaining
the owner journal and avoiding an unlink/rmdir crash window with an empty claim.
Existing completion records remain append-only. Before rename, custody remains;
after rename, the journal is retained and the old claim is absent.

This is not a transaction system, distributed lock, sandbox or power-loss durability
guarantee. It requires a trusted local filesystem supporting these locks and
same-volume rename. Network filesystems and uncooperative external writers or
removal of the lock file are outside the guarantee. Never delete the lock file as
cleanup. Quiesce old unfenced administration processes before upgrading.

If an owner dies with a Git child possibly still running, settle that child and
observe actual Git/index/source state before recovery. Cancellation is not
rollback; no blind retry follows an unknown result. Unknown bytes, unfinished Git
operations, moved refs and missing/corrupt journals require reconciliation. The
pre-existing initial-admission window before the first journal is installed can
still require manual custody reconciliation after hard termination; missing
journals never authorize automatic claim clearing.

## Filesystem custody

Branch-target checks use lexical `lstat`, including nested components, rather than
dereferenced `exists()`. Traversed symlinks and Windows reparse points refuse before
Git effects. Dangling file/directory links and supported junctions remain existing
entries. Ordinary ignored/untracked collisions refuse; safe absent targets and
compatible tracked transitions remain supported. Classification errors refuse.
The return-branch switch uses the same check. No unknown entry is deleted to switch.

Tests use real Windows links, nested links, existing/dangling junctions, literal
outside-target bytes, entry identities and a safe noncolliding ignored-link control.
Unavailable fixture capabilities report explicitly; they are not passing
reproductions. Windows execution does not establish execution of the POSIX branch.

## Validation and boundaries

All three independent baseline failures were reproduced before source changes.
Selected permanent regressions also execute pinned original Git bodies in memory;
their legacy API adapter drops only the new digest keyword. They fail for the
actual defects, not collection errors. Corrected schedules cover R1/R2/B exclusion,
stale normal finish/expectation updates, replaced/disappeared/no consent, legitimate
and legacy recovery, unknown bytes, real process exit after restore/return,
cancellation, failed release and thread/process contention.

Focused/static checks and the full committed-tree protected gate are required;
exact outcomes and publication identities are recorded in repair closeout evidence.
Checkout still owns serialization/recovery, not task or publication authority.
WorkCycle/delegation, Qwen limits, Tool validation and review remain unchanged.
Broader custody0385a359, validation-closure d58697fd and cohesion39c6663a are separate.
The next validation/publication audit and188 RI histories are unchanged here.
