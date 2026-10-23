# Canonical repository reconciliation â€” 2026-10-19

## Operating structure and branch disposition

The canonical checkout is `C:/Users/recoveryadmin/Workspace/tools/devtools`.
Seven linked checkouts and two independent source-grounding execution/deployment
checkouts were preserved and removed. `git worktree list` now contains only this root;
`.local/worktrees` does not exist. Learned Intelligence and the unrelated repoctx
repository were not modified. No checkout, clone, repository, model operation or
scientific result was created by consolidation.

| Original branch / authenticated tip | Disposition |
| --- | --- |
| `feat/multi-resolution-search` / `c21b4922355a6f868beed9e0b71c786cc52361e8` | SUPERSEDED_OR_REDUNDANT after adoption into main at c21b4922; original history preserved. |
| `feat/qwen-context-worker` / original `3e0402bf7e6cc46b71cbbd85f152beb94007dec6` | ACTIVE_FEATURE; consolidates remaining dashboard and governed-development history. Production-safe source/standalone worker adopted separately; checkout-bound WorkCycle remains blocked. |
| `feat/operator-dashboard` / `cf696a6d5d255d0428a049d803408f7ca5caf375` | SUPERSEDED_OR_REDUNDANT as an active checkout: preserved and merged into consolidation; maintained application relocated to `apps/operator_dashboard`. Full adoption awaits the blockers below. |
| `feat/qwen-real-task` / `e84def2d08dfc59739fab8f778478d9a63604c7c` | EVIDENCE_ONLY; historical attempts immutable; necessary worker code already selectively incorporated. |
| `feat/b-0048-python312-json-object` / `75cc74f7acda36cf91e91251efae8f9b3054f02a` | EVIDENCE_ONLY baseline; accepted candidate remains operational evidence, not installed source. |
| `feat/experiment-execution-pipeline-prepare` / `2aad8a1c8ccc3cd19a0476d7da13f1d95a833d42` | INCOMPLETE_OR_BLOCKED for current deployment; engineering checkpoint preserved, not merged together with incomplete science. |
| `experiment/source-grounding-successor` / `8bf87d4bb29349b8391de3fed2680bf1f7c94f28` | INCOMPLETE_OR_BLOCKED; candidate-08 remains incomplete. |
| `chore/repository-consolidation` | SUPERSEDED_OR_REDUNDANT cleanup topic; history retained on the ordinary Qwen continuation branch. No further implementation assignment for this topic. |

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

The adopted source checkpoint is main commit `ff2b135ad7cbc9109a0b80f150e238a78e4743b6`. The continuation branch is `feat/qwen-context-worker`. The final hidden-checkout scan discovered the legacy `.local/deployments/source-grounding-successor/target` at `35d464425ef13029b0ee6151e5aea232d8489068`; its 16 operational files were preserved, compressed, extracted and verified before removal. Its Git history remains at `refs/archive/scientific-legacy-target/main` and in the complete scientific bundle. Three existing host-disclosure fixtures contain synthetic alpha/beta/gamma data, not Devtools clones; they remain preserved test evidence.

## Single-checkout governed-development continuation

The former WorkCycle/installation/verification checkout blocker is removed on
`feat/qwen-context-worker`. The existing lifecycle now uses ordinary branch
selection under exclusive, recoverable coordinator-owned source mutation.
The [integration contract](../backlog/integration.md#canonical-checkout-phase-boundary)
documents temporary exact-byte installation, tree review, feature publication,
local/remote destination promotion, verification and administrative closeout.
No worktree, repository copy or source-tree clone is created. Tiny Git fixtures
exercise real Git effects with explicitly synthetic authority and validation;
they do not establish a real protected-main integration.

B-0048's new canonical plan is recorded in its existing readiness document.
It remains blocked by missing genuine integration authority; its old coding
assignment and checkout-bound grants remain historical. Main is unchanged at
`862bda2d3d1d812893f84ab69691fc068ecce268`.

Four redundant `workspace/src` payloads were found in canonical/preserved Qwen
closeout and B-0048 preparation evidence. Every file was compared with its
decompressed member in the existing `checkout-evidence.zip`; matching baseline
source was additionally checked against recorded Git blob identities. Only
these verified payload directories were removed. Original receipts, candidate
source, historical reviews, all 13 forensic files and the unchanged recovery
packet remain. Its SHA-256 is
`5debf60d98465c920f77ea4b6ae13a4855699f912ebcef1ad1ea15aed8f4ea5e`.
The existing archive directory contains `redundant-source-payloads.json` and
`redundant-source-removal.json` with per-file recovery addresses and hashes.
This recovers 5,291,562 redundant bytes without creating another backup facility.

The dashboard dependency review and production-adoption authority remain
separate. Experiment classifications remain 24 CLOSED / nine INCOMPLETE /
two BLOCKED. No scientific result, Qwen attempt or historical authority was
changed by this continuation.

Final continuation verification: 1950 passed, two skipped, 100% production branch
coverage on Python 3.14 (398.63 seconds pytest / 400.13 seconds host). The existing
`.local/reconciliation/single-checkout-*` receipts retain focused, protected,
static and integrity evidence. Changed Python files pass Ruff/formatting; strict
mypy passes its 472-file default and 14-file administration scopes. Ten unchanged
source/document formatting differences and frozen-experiment static findings
remain outside this bounded implementation. Framework adoption still requires
reviewed integration authority; the remaining dashboard dependency blocker must
not be imported simply by merging all feature ancestry into main.

## Finite architecture and research reconciliation (2026-10-23)

This section is a Codex-authored operational charter from the user's explicit
2026-10-22 reconciliation request. It is not an imported starter document or a
new architectural decision. Earlier consolidation/engineering reports above
remain historical evidence with their original outcomes and authority limits.

### Governing direction and limits

Devtools enters a finite research, architecture/execution-lifecycle audit,
repository-hygiene planning and successor-session preparation phase. Immediate
work is not another Qwen feature or benchmark. Research mature open-source
harness mechanisms ourselves, incrementally, and compare them with actual
Devtools ownership before recommending changes.

Inventory delivered software and experiments, distinguish feature publication
from protected-main adoption, identify missing foundations and possible overlap,
review observability/trace/event pressure, and investigate developer ergonomics.
Classify generated/temporary/obsolete storage without deleting original evidence.
Capture qualified discoveries in the existing backlog instead of automatically
fixing them. Prepare a comprehensive fresh-ChatGPT-session handoff only when this
research and reconciliation are sufficiently complete.

Use one physical canonical checkout. No new clone, worktree, backup/source tree,
agent framework, execution owner, model experiment, service lifecycle change or
protected-main promotion is authorized by this phase. Learned Intelligence's
separate repository and scientific catalogs remain distinct. Existing taxonomy,
package ownership, ADRs and publication controls are unchanged.

### Starter-package custody

Expected input: `devtools-reconciliation-starter-2026-10-22.zip` containing
`01-reconciliation-charter.md`, `02-oss-harness-mechanism-review-initial.md`,
`03-audit-backlog-seeds.md` and `MANIFEST.json`.

The exact package/member files were not found in accessible canonical paths and
no attachment location was provided. Excluded caches and permission-denied
regions limit the scan. Status: **NOT_VERIFIED_NO_INPUT**; no starter hash,
imported content or deduplication of its 18 stories is claimed. Do not substitute
other local ZIPs or invent missing document bodies.

If supplied later, inspect the manifest/schema and member paths, reject traversal
or unexpected executable content, verify each original member's SHA-256 before
use, and preserve substantive source bodies/provenance. Map them into the
existing documentation/research/backlog owners and record original-to-canonical
addresses. Do not create a second authoritative backlog or research index.

### Initial checkpoint and next bounded work

The authenticated feature baseline is
`3c09641dd17b13b83c2fe84e3f1cf4920ca7186f`; protected remote main is
`5d979920d0728775ed529457c88f5b68b440c64f`. Local main remains
`862bda2d3d1d812893f84ab69691fc068ecce268`; its lag is not an unfinished Commands
integration. Commands source is already adopted; many later worker/Context/RI
increments remain feature-only or differ at the destination.

This initial checkpoint supplies:

1. [Source-backed adoption/observability inventory and backlog crosswalk](../research/architecture-reconciliation-inventory.md).
2. [Primary-source harness review cursors](../research/agent-harness-mechanism-review.md)
   and an ordered follow-up worksheet.
3. [Artifact custody inventory](artifact-custody-inventory.md), exact metadata
   limitations and a safe future cleanup procedure; no removals performed.
4. Existing pending proposal captures/advisories, unchanged canonical IDs and
   dispositions, plus refreshed navigation through the documentation map and
   research README. This is not completion of the entire architecture audit.

Next perform one source-and-test mechanism comparison of Qwen Code and Pydantic
AI at recorded upstream revisions, then DeepSeek Harness and Aider. Follow with
the complete local lifecycle/dependency/adoption and custody review. Record
facts, external observations, hypotheses and candidate decisions separately;
implementation requires its own selected, authorized increment.

### Exit conditions for the finite phase

- All meaningful capabilities have source, experiment, destination, consumer,
  test/evidence and remaining-integration classifications, including unknowns.
- Upstream mechanism findings and local observability/lifecycle gaps have exact
  source/test references and explicit semantic/authority differences.
- Original starter stories are deduplicated if the package becomes available,
  otherwise the missing-input limitation remains an explicit handoff obligation.
- Backlog candidates preserve parent/ID/disposition; no speculative abstraction,
  generic tracing system or unreviewed feature is promoted merely by discovery.
- Artifact custody/recovery and exact cleanup candidates are reviewable; any
  destructive cleanup has separate authority and safeguards.
- Current navigation/status claims are reconciled without rewriting historical
  experiments, and a comprehensive fresh-session handoff identifies actual Git
  state, decisions, evidence, unresolved obligations and the next bounded task.

Documentation/index/layout/intake integrity checks are appropriate to this
checkpoint. Production source/tests are unchanged; no new full protected gate
or inference is required merely to publish documentation and advisory intake.

## Recovered inputs and second research checkpoint (2026-10-23)

The original unavailable-input statement above is historical. The supplied transfer
ZIP and all five declared payloads are now locally authenticated; the three
original document hashes also match the original manifest. The original starter
ZIP container hash is supplied provenance, not locally recomputed. See the
[exact intake/candidate reconciliation](../research/reconciliation-input-reconciliation.md)
for custody, original byte-preserved documents and all18 canonical dispositions.

The original charter's long-horizon OpenMind/Continuum motivation and model-neutral
goals remain research direction, not a new domain or accepted Agent architecture.
Preserve its top-down, horizontal and bottom-up audit views, plus one successful
and one failed real trajectory; these deepen the existing finite-phase method.
Report-only maintenance/research roles remain hypotheses under B-0043/B-0044.
No input draft grants parallel execution, new inference or destructive cleanup.
Existing taxonomy/ADRs/backlog/index owners remain authoritative.

The [pinned Qwen Code/Pydantic AI implementation-and-test comparison](../research/agent-harness-mechanism-review.md#source-and-test-comparison-2026-10-23)
now covers correlation, continuation, exploration/loops, Context eviction,
validation/retry/permission, interruption, usage and instrumentation against actual
Devtools owners. Tests were inspected, not executed upstream. It corrects the
starter's ExternalToolset validation and mostly-empty observability assumptions.
No architecture/runtime adoption, source refactor or model experiment follows.

Next inspect DeepSeek Harness and Aider source and tests; then deepen actual local
successful/failed lifecycle joins, production adoption and custody/recovery before
the comprehensive successor-session handoff. That later research is not launched
by this checkpoint.

## Four-project research checkpoint and local audit selection (2026-10-23)

The [DeepSeek Harness/Aider source-and-test follow-up](../research/agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
completes the selected external mechanism comparisons at pinned revisions.
Session append is not automatically durable; Tool schemas/visibility are not
authorization; Aider's host matching/partial application differs from exact atomic
admission. Existing Evidence, usage, ToolRunner, Context and WorkCycle owners are
the comparison targets. No framework adoption, implementation, inference,
upstream execution or production behavior change follows.

The next [five-flow observability/lifecycle audit](../research/development-lifecycle-audit-plan.md)
has original receipt paths and fingerprints for Qwen success, rejected/incomplete
edits, Codex closeout, real source recovery and genuine source navigation.
Those inputs are selected, not yet exhaustively joined. Reauthenticate them and
report missing causal edges rather than inventing spans or replaying work.
Then finish bounded destination-adoption and artifact-custody reconciliation
before the comprehensive successor-session handoff. Historical receipts,
original18 crosswalk, backlog dispositions and protected-main authority remain.

## Executed lifecycle/observability audit (2026-10-23)

The [five-flow report](../research/development-lifecycle-observability-audit.md)
authenticates all21 selected inputs plus original stage/provider/Tool/check/
publication evidence. It separates direct byte/call/review links from inferred
clock order and missing occurrence joins. The planned turn06 expansion actually
refused; two recorded physical-file hashes differ from Git blobs solely by CRLF.
Both distinctions are documented without altering historical receipts.

Reuse current Evidence, usage and application receipts with better consumers/
joins first; generic tracing/OTel interfaces remain alternatives requiring design,
not adopted architecture. Advisory backlog evidence records incomplete model/
observer population, freshness/publication/recovery observation, exact-tree
input closure and capture-policy questions. No source, tests, runtime authority,
scientific outcome or proposal disposition changes. Next reconcile selective
destination adoption, actual feature/experiment ownership and exact-path custody,
then prepare the comprehensive successor-session handoff. Do not begin that next
phase automatically.

## Final production reconciliation checkpoint (2026-10-23)

The [completed production-adoption/experiment/architecture report](../research/production-adoption-and-architecture-reconciliation.md)
and [source/custody companion](../research/production-adoption-and-architecture-evidence-20261023.json)
complete this finite phase's repository-wide investigation checkpoint. All 35
collections have explicit dispositions; 48 overlapping capability slices cover
all 250 framework Python files, with source/test identities and actual consumer
qualifications. Eight selective destination-review groups preserve Commands main
adoption and exclude unrelated feature ancestry, historic grants and evidence.
The [extended custody inventory](artifact-custody-inventory.md) verifies packets
and eight residuals without removal; denied/uncertain regions remain HOLD.

One pending protected-validation reuse/input-closure investigation and four
existing proposal advisories preserve the backlog's current authority. No
implementation, approval, source/test change, inference, service mutation or
protected-main operation follows. The next planned checkpoint is the comprehensive
ChatGPT successor-session handoff, not another open-ended research program.
