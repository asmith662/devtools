# Canonical repository reconciliation â€” 2026-10-19

## Operating structure and branch disposition

The canonical checkout is `C:/Users/recoveryadmin/Workspace/tools/devtools`.
Seven linked checkouts and the independent source-grounding execution checkout
were preserved and removed. `git worktree list` now contains only this root;
`.local/worktrees` does not exist. Learned Intelligence and the unrelated repoctx
repository were not modified. No checkout, clone, repository, model operation or
scientific result was created by consolidation.

| Original branch / authenticated tip | Disposition |
| --- | --- |
| `feat/multi-resolution-search` / `c21b4922355a6f868beed9e0b71c786cc52361e8` | SUPERSEDED_OR_REDUNDANT after adoption into main at c21b4922; original history preserved. |
| `feat/qwen-context-worker` / `3e0402bf7e6cc46b71cbbd85f152beb94007dec6` | SUPERSEDED_OR_REDUNDANT as an active checkout: all history retained in the consolidation branch. Production-safe source fixes and standalone worker can be adopted separately; checkout-bound WorkCycle remains blocked. |
| `feat/operator-dashboard` / `cf696a6d5d255d0428a049d803408f7ca5caf375` | SUPERSEDED_OR_REDUNDANT as an active checkout: preserved and merged into consolidation; maintained application relocated to `apps/operator_dashboard`. Full adoption awaits the blockers below. |
| `feat/qwen-real-task` / `e84def2d08dfc59739fab8f778478d9a63604c7c` | EVIDENCE_ONLY; historical attempts immutable; necessary worker code already selectively incorporated. |
| `feat/b-0048-python312-json-object` / `75cc74f7acda36cf91e91251efae8f9b3054f02a` | EVIDENCE_ONLY baseline; accepted candidate remains operational evidence, not installed source. |
| `feat/experiment-execution-pipeline-prepare` / `2aad8a1c8ccc3cd19a0476d7da13f1d95a833d42` | INCOMPLETE_OR_BLOCKED for current deployment; engineering checkpoint preserved, not merged together with incomplete science. |
| `experiment/source-grounding-successor` / `8bf87d4bb29349b8391de3fed2680bf1f7c94f28` | INCOMPLETE_OR_BLOCKED; candidate-08 remains incomplete. |
| `chore/repository-consolidation` | ACTIVE_FEATURE for the combined maintained dashboard and governed-development work not safely adopted into main. This is the one continuation branch; historical branches remain refs, not additional implementation checkouts. |

Original local and remote refs were authenticated. The B-0048 baseline had no
remote branch; preserve its commit through existing branch/history rather than
publishing an unimplemented source branch. No historical ref was reset or rebased.
The unique scientific approval/PACKET tip is retained locally as
`refs/archive/scientific-execution/main` at
`b5a3c824928985098347f0ccc8d39db8088e5810`. It was not uploaded to a new service.

## Preserved evidence and recoverability

`.local/archives/repository-2026-10-19/preservation-manifest.json` records 1,651 file identities,
original checkout paths and canonical destinations, including the 13 forensic
files retained in place. The 1,638 copied files under
`.local/preserved-checkouts/` were compressed into
`.local/archives/repository-2026-10-19/checkout-evidence.zip`, extracted and individually hashed.
The scientific Git bundle in that directory is complete, verified and unbundled
successfully into the existing canonical object store. No backup repository was
created. Its original Git configuration is retained alongside it.

The coordinator's exact backlog, assignment, delegation, candidate, result,
review and integration records were also copied byte-for-byte to
`.local/backlog/`; worker run records are at `.local/qwen-coding-worker/`.
Shared local Git configuration now designates the canonical root. Historical
receipts still show the original paths. They are not rewritten or reissued.
Old checkout-bound grants, assignments and integration plans cannot become fresh
authority here. No backlog approval, model dispatch or B-0048 promotion was
repeated. Four external discoveries remain pending review.

Only an inaccessible obsolete pytest cache remains quarantined at
`.local/reconciliation/permission-blocked-dashboard-cache/`. Native deletion,
ownership recovery and ACL modification were refused by Windows. No source
checkout or registration remains there. Its removal requires OS permission
repair; no broader permission changes were attempted.

The [experiment contract](../../experiments/README.md) inventories 35 collections:
24 closed checkpoints with compressed, extracted/hash-verified packets, nine
incomplete and two blocked. The original packets total 22,210,215 bytes; a separately restore-tested Qwen main compilation additionally preserves earlier measured reports. Twenty-two old root
reports were compacted; frozen/cross-referenced originals remain in place.
The archive manifests and individual summaries preserve negative results and
sealed/unfinished boundaries. Local archives share the SSD and do not provide
disk-loss protection. Do not delete `.local/archives` or preservation packets as
ordinary caches.

## Maintained ownership and verification

Root investigation dossiers moved to `docs/research/`; root JSON reports moved
into the recoverable experiment archive. The dashboard, MIT notices and locked
React dependencies moved to `apps/operator_dashboard`; the existing worker and
its dependency closure moved to `apps/qwen`. Corresponding deterministic tests
moved to `tests/apps`. Current consumers use the maintained addresses; original
attempts and their old source identities remain historical evidence. No Qwen
implementation was regenerated or substituted.

`scripts/validate_layout.py` checks permitted root ownership and forbidden
secondary-checkout storage without deleting anything. AGENTS documents the same
rules. It is a bounded layout guard, not a Git management framework.

Focused application/Intake/CLI/RI/Markdown validation: 211 passed in 9.12 seconds.
Relocated scripted worker tests: 102 passed in 45.02 seconds. Strict mypy over
483 maintained source/test/tool files passed. Affected Ruff/formatting passed.
Dashboard React: six tests passed; production build passed (4.15 seconds), with
the existing bundle-size/React peer warnings. Browser smoke passed against
actual preserved Markdown (two turns) and source-segment (three turns) records,
proposal/backlog details, Refresh and read-only/origin checks; screenshots and
receipt are in `.local/reconciliation/dashboard-smoke/`.

The full consolidated branch's protected profile was not run: its legacy
WorkCycle/delegation/integration fixtures explicitly create linked worktrees.
This conflicts with the maintainer's absolute prohibition for this assignment.
An initially combined focused invocation was stopped before those fixtures;
the replacement focused selections excluded them, without modifying or waiving
the canonical gate. No production-main claim is based on that partial profile.
The production-safe selection must pass the normal protected profile separately.

## Remaining blockers and next operating decision

1. WorkCycle preparation requires a second target checkout; integration install
   and destination verification create worktrees. Keep these operations blocked
   until they support the newly required one-checkout branch workflow. This
   assignment does not build an alternate executor or silently transfer grants.
2. Dashboard adoption retains actual working UI/API but its existing dependency
   audit reports four findings (one moderate, one high, two critical). The audit
   is `.local/reconciliation/npm-audit.json`. No forced upgrade was applied.
   The maintained application remains a local-only feature candidate; no network
   service was exposed and no unreviewed dependency change entered main.
3. B-0048's accepted source SHA-256
   `9b31553ec9982cba4886eaed39e6ddb0941598b57d3d0442771083f2fd4fd88f`
   and review `23a5dcbedbb4f6980068a8fc29ae94d1e436cc3a7078f585bb762fcb2cdc95ae`
   remain preserved. Integration authority was absent, and path relocation also
   makes its old plan stale. The object slice is not integrated; sibling list/CSV
   compatibility keeps the parent obligation open. Do not redispatch Qwen.
4. Candidate-08 recovery requires exact preserved source/publication identities,
   fresh compatible operational bindings and independently valid authority.
   Cleanup does not grant any retry, successor or scientific execution.
5. Learned Intelligence integration, precise Context Tools, structured model
   continuation, atomic working checkpoints, layered long-term Memory and
   Context-size benchmarking remain planned work, not implemented cleanup.

Use ordinary branch switching in the canonical checkout for the next review.
The next concrete engineering decision is reconciling the existing WorkCycle's
physical-checkout assumptions; the dashboard dependency maintenance can be
reviewed independently. This is a specific compatibility gap, not a request
for a new orchestration or storage architecture.


## Verified production checkpoint

Main adopts multi-resolution search through its original c21b4922 ancestry, the exact accepted Qwen Markdown source (SHA-256 a5510a1b30945060c3d1438f0832cc8ffe5d9ee6248d5e24bd66feea6c5fb645), the Codex Python materializer correction, standalone apps/qwen and its deterministic tests, existing proposal/B-0048 records, layout rules and experiment metadata. It excludes dashboard/governed execution/integration code. No unrelated scientific ancestry was imported.

Final unchanged protected profile: 1818 passed, 2 skipped, 100% production branch coverage; 89.31 seconds pytest / 90.71 seconds host. The first run had one actual-project configuration fixture missing the newly selected apps resource (1817 passed, 1 failed, 100% coverage). The fixture was synchronized without relaxing assertions; the final profile then passed. Main Ruff, formatting, strict mypy (457 files), layout and diff checks passed. Protected logs and both terminal timing receipts are under .local/reconciliation. The default mypy scope now names maintained source/tests/apps instead of immutable generated experiments; production coverage was not changed.

Fourteen legacy root .devtools evidence files were additionally moved, hash-verified, to .local/preserved-root/devtools. Their independent root-runtime-manifest.json is in the repository archive directory. All 13 forensic files remain at their original paths, byte-identical and untracked.
