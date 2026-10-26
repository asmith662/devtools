# Comprehensive code audit program — 2026-10-23

ModelInteraction/Serving audit on `a7a49cc18f3b40a5bf4e3897ca30d9a5cddc30d1`:30 complete source/test/export/marker reviews;321 cohort and113 consumer tests pass.44 independent cases identify five new pending P2 repairs; existing observer/backward-clock policy remains B-0011/B-0046/ADR-0001, not a new approval. [Report](model-interaction-and-serving-audit.md); [exact depth/identity/probe evidence](code-audit/model-interaction-serving-assurance.json). No executable changes/new protected gate/live inference. Earlier filesystem/Duration and RI/worker/Checkout repairs remain delivered. RI93/93,606/606,188 historical obligations and unapproved A+C unchanged. Next: bounded demonstrated repairs and explicit observation-policy decision, then broader Agents/Runtime/Persistence review; no automatic new audit cohort. Earlier notices are dated history. `audit:model-interaction-serving:a7a49cc1:20261026`.

Delivered follow-through: [CSV strings, compatible JSON member lookup and Python3.12 structured initialization](../development/filesystem-contract-repair.md), production `39c583ba2b252b44b998b8fbf6e8ef6ecf163294`, normal PR#29, verified main `2b20f6119b5cbcdda2fcc78c276178fbcde780ee`. Final committed gate3077 passed/2 opt-in live skips/100% configured production branch coverage;275 focused tests/15 subtests and246 consumer tests pass;8 maintained stdlib tests plus12 original compatibility cases pass on each3.12.13/3.14.3 interpreter. [Exact receipt](code-audit/filesystem-contract-repair-20261026.json). CSV67f7d086 and JSON1671955c have append-only implemented-and-merged evidence; do not repeat their scope. B-0048 constructors are delivered; broader runtime matrix remains open. AuditPR#28 is integrated. Next major audit is ModelInteraction/serving; no new cohort begun. RI93/93,606/606,188 historical obligations and A+C-unapproved unchanged. Earlier notices are dated history. `repair:filesystem-contracts:39c583ba:20261026`.

Filesystem codecs/structured models reviewed on `26bd8053ab8ad8323dd3273b4b0e986de05388e9`:43 exact paths,41 new complete bodies/export/marker surfaces and two unchanged prior codec reviews reused.228 focused tests pass;61 independent representation/native compatibility cases retain existing CSV P2, existing B-0048 object/list/CSV3.12 failures and new JSON member-lookup P2 `1671955c-42ca-4fa0-94a3-2bee570e0f0f`. No executable changes, repair or new protected gate. [Report](filesystem-codecs-and-models-audit.md); [exact depth/identity evidence](code-audit/filesystem-codecs-models-assurance.json). Duration and prior Core/Resources repairs stay delivered. RI93/93,606/606,188 historical obligations and A+C-unapproved unchanged. Next: separately authorized bounded repairs, then ModelInteraction/serving. Earlier notices are dated history. `audit:filesystem-codecs-models:26bd8053:20261026`.

Delivered follow-through: [Duration factory-input correction](../development/duration-factory-input-repair.md), production `171699ac6de9ddb15f51b4cee440b8ee412646be`, normal PR#26, verified main `7bc03e9d22c919314103375934f4bf74cac5e27d`. Final committed gate3035 passed/2 opt-in live skips/100% configured production branch coverage;415 focused and415 post-main tests pass. [Exact receipt](code-audit/duration-factory-repair-20261026.json). Existing ea7c18ff records implemented-and-merged evidence; do not schedule the factory repair again. Arithmetic represented-result semantics remain unchanged. PR#25 audit integration is complete; historical findings below retain their dated meaning. Remaining codecs/models, B-0048,188 historical RI versions and unapproved A+C remain separate. `repair:duration-factory:171699ac:20261026`.

Core Identity/Time audit completed against `32c91a17e8df961fc0a834399d8b72c51fbab919`: all ten frozen source/test bodies fully reviewed;249 focused maintained tests pass;48 deterministic probes retain six reproduced negative-factory cases under existing Duration proposal ea7c18ff, two arithmetic-policy qualifications and documented wall-clock observation limits. No production source/tests or new protected gate. [Report](core-identity-and-time-audit.md) and [exact evidence](code-audit/core-identity-time-assurance.json). Existing Core/Resources PR23 repairs stay delivered; RI93/93,606/606 and188 historical obligations are unchanged; A+C remains unapproved. Next: separately authorize the bounded Duration correction, then remaining filesystem codecs/structured models and ModelInteraction/serving. Earlier notices retain their dated meaning. `audit:core-identity-time:32c91a17:20261026`.

Delivered follow-through: [deterministic paths, filesystem entry custody and Commands collector cleanup](../development/core-resources-integrity-repair.md), production `2240ae9f8dfa38cc598396bb2677059ceaa4534d`, PR#23, verified main `ef0e3539a1afac20bfe65dfbac810456b5342804`. Final committed gate 2962 passed/2 opt-in live skips/100% configured production branch coverage;721 broad focused and594 post-main tests pass. Original bdcf3bbc/4cb7c397/37a647f2 retain implemented-and-merged evidence; do not schedule these bounded repairs again. Higher-layer authority/concurrency, broader B-0041/B-0006 and platform limits remain separate. All ten Core identity/time pins match main and remain unaudited; that is next. RI93/93,606/606,188 historical obligations and A+C-unapproved status are unchanged. Earlier notices below retain their dated meaning.

Current audit: [Core paths, filesystem and managed Commands](core-paths-filesystem-and-commands-audit.md), baseline `0e240ec102e9d54c92a3e85071586a9a8e74b308`. All twelve frozen bodies reviewed;479 focused tests pass;14 independent probes establish three pending P2 scopes (Windows drive-relative policy, generic-writer dangling-entry custody, failed-collector task cleanup). No production fix or new protected gate. Source/version/consumer/platform limits are explicit. Core identity/time is selected next and not started. RI93/93,606/606,188 historical obligations and A+C-unapproved status are unchanged. Earlier notices below remain dated history.

Delivered follow-through: [provider-local usage, partial/conflicting facts and operator identity integrity](../development/usage-evidence-integrity-repair.md), production `8f34dbdee381cf4493dd1f5e2a5508653dfe2891`, PR#20, verified main `3e59c20f4c9276a7f28682a127ff95428e673564`. Final committed gate 2937 passed/2 opt-in live skips/100% configured production branch coverage;350 focused post-main tests and13 frontend tests pass. Existing bbba08b8/ca5a0aac/a823db65 retain implemented-and-merged evidence; do not schedule these repairs again. Broader B-0011/B-0023/B-0034 consumers and d586 closure remain open. All12 Core/Resources pinned bodies match main and remain unaudited: that is the next major domain. RI93/93,606/606,188 historical obligations and A+C-unapproved status are unchanged. Earlier notices below retain their dated meaning.

Current audit: [Evidence, usage custody and actual operator consumers](evidence-usage-and-operator-audit.md), baseline138adc07. All12 frozen bodies reviewed;149 Python and7 frontend tests pass. Three new P2 proposals (bbba08b8 provider aliases;ca5a0aac partial facts;a823db65 missing operator identity join) await bounded repair. Native app records are not automatically normalized framework Evidence; B-0011/B-0023/B-0034 retain concrete consumer/recovery pressure. Prior repairs remain delivered; broader d586 closure stays open. Next major domain is frozen Core/Resources, not another automatic narrow lifecycle audit. RI93/93,606/606 and188 historical obligations are unchanged; A+C remains unapproved. Earlier notices below are dated history.

Delivered bounded follow-through: [validation freshness, command receipt custody and Git path identity](../development/validation-evidence-path-repair.md), production `1a9e3ff1e56aebb8522c4d437d46de5f31679389`, PR#17, verified main `ae88c69267961cf6a73bf41454a08cb8f97a14c4`. Committed gate 2903 passed/2 opt-in live skips/100% configured production branch coverage; 265 focused post-main tests pass. Existing proposals d58697fd/84a5d9b1/b0c02dbf retain implemented-and-merged evidence; broader d586 input closure/HEAD/toolchain work remains open. No delivered bounded repair should be repeated. RI93/93,606/606,188 historical obligations and A+C-unapproved status are unchanged. Next Evidence/usage cohort is frozen and not started; earlier pending notices below are dated history.

Current audit: [validation freshness, review, publication and durable evidence](validation-review-publication-audit.md), baseline5b0bb0b7. Ten frozen bodies fully reviewed;252 focused tests pass. Existing d58697fd now has independently reproduced P1 stale protected-validation reuse evidence; new P2 records84a5d9b1 (post-check receipt collision) and b0c02dbf (Git-quoted Unicode population refusal) await repair. No production changes or new gate in this checkpoint. Local lost-acknowledgment Git retry/divergence controls pass; GitHub fault behavior is not inferred. Previous bounded source/worker/Checkout repairs remain delivered. RI93/93,606/606 and188 historical obligations are unchanged; A+C remains unapproved. Prioritize bounded reuse repair, then the selected Evidence/usage cohort, which has not begun. Earlier notices below are dated history.

Delivered follow-through: [Checkout fencing, exact recovery consent and filesystem custody](../development/checkout-custody-repair.md), production `ce1a8ea523cdfe9772c7e8b5ed0479528d3aba50`, PR#14, verified main `f54b4a0a6d1b81be805b2d1d63ea43f23df0100a`. Full committed-tree gate 2889 passed/2 opt-in live skips/100% configured production branch coverage. Proposals69688104/30bd833e/3b2f566b retain implemented-and-merged advisory evidence; do not repeat these repairs. Broader custody, check-input closure and cohesion remain separate. RI93/93,606/606 and188 historical obligations are unchanged. A+C remains unapproved; the next frozen validation/publication audit has not begun. Earlier pending-repair statements below are dated history.

Current integrated-main audit: [Checkout, WorkCycle, delegation and recovery](execution-ownership-and-recovery-audit.md), baseline `264915928a9045795d5e07c728ffa1aaba4c1704`. All nine selected bodies reviewed;114 focused tests pass. Three independently reproduced P1 Checkout defects are pending: replacement-owner recovery/finalization fencing (69688104), displayed-owner consent binding (30bd833e), and ignored dangling-link preservation (3b2f566b). No production fix in this checkpoint. See [next validation/publication scope](code-audit/execution-validation-next-cohort.json). The three prior worker repairs remain delivered; do not schedule them again. RI fixtures93/93, experimental source606/606 and188 historical obligations are unchanged. A+C remains unapproved. Earlier notices below are dated history.

Delivered bounded worker repairs: [acceptance, budgets and response correspondence](../development/qwen-worker-contract-repair.md); production `18f6ac247bf5d1173e8b488910557207ccfaf92c`, normal PR#11, verified main `6c4267e8bd47d8ac897e01230fa843db74f34a81`. Three existing proposals41a497a8/660900a1/751451cb now have implemented-and-merged advisory evidence; do not repeat their bounded implementation. Broader check-input/cohesion work remains open. RI fixture93/93, historical188 and A+C-unapproved status are unchanged. Next is the already frozen Checkout/WorkCycle/delegation recovery audit; it was not launched. Earlier pending-repair notices are dated history.

Current integrated-main audit: [RI fixture closure and actual task-to-edit review](ri-fixture-closure-and-execution-audit.md), starting `4d36ce586e106bfc7f89b1dd3c5931e73e1f5084`; [exact evidence](code-audit/ri-fixture-execution-assurance.json). Original fixtures **93/93** individually reviewed (four substantive bodies and22 marker-only surfaces newly closed; augmented ledger94/94). Historical experimental source606/606 is unchanged; **188 older versions remain** (168 unread/20 tip-only;15 full). The first operational slice independently reproduces two P1 prepared-worker bugs (frozen-input acceptance and proposal-cap enforcement) and one P2 foreign-response admission bug. Three new pending proposals and three existing advisory updates; no production fix or new protected gate. Prior source/binding repairs remain delivered. Prioritize bounded worker repairs, then Checkout/WorkCycle authority and recovery; [next exact operational scope](code-audit/execution-ownership-next-cohort.json). A+C remains unapproved; earlier counts/priorities below are dated history, not current instructions.

Current main457def assurance: [configuration/role and closure review](ri-configuration-role-closure-audit.md) and [exact ten-fixture/eight-version evidence](code-audit/ri-config-role-assurance.json). Original fixtures **67/93** (26 remain: four substantive,22 namespace); history **15 full/168 unread/20 tip-only**. New one-facade fallback P1 has a distinct pending repair; direct lookup/bases PR5 and both source-integrity fixes remain delivered. Repair that bounded facade path, then finish the final current-fixture cohort and transition to the documented operational workflow audit while responsibility-grouped historical work remains explicit. Historical experiment source606/606 is unchanged. A+C remains unapproved. Earlier overlay counts/priorities below are dated history, superseded by this checkpoint.

Current integrated-baseline checkpoint: [RI assurance and architectural cohesion](ri-assurance-and-cohesion-audit.md), main `5f53f5ac`. All twelve selected fixtures and seven historical bodies reviewed; eleven new fixture paths bring original coverage to **57/93**, with **36** remaining. Historical versions: seven full,170 unreviewed,26 tip-delta-only. Experimental source review stays606/606. One new pending production binding bug and eight append-only advisories; no source/policy implementation. Both prior RI repairs are delivered on main. Earlier candidate/completion notices below are dated evidence, superseded for current integration/counts. A+C remains unapproved; no successor dossier.

## Disposition and authority

Current audit checkpoint: [RI experimental source completion and proposed main repair adoption](ri-experimental-completion-and-main-adoption.md).
All32 final selected paths have applicable full-body review:606/606 historical
experimental paths now have version-specific dispositions, not independent
revalidation of every judgment or completion of Repository Intelligence.
Ten new maintained fixture reviews bring the original universe to45/93; including
the separately added regression it is46/94, with48 current fixtures remaining.
177 older NOT_REVIEWED versions and26 tip-delta-only versions retain their depth.
The exact eight-path main-adoption patch is proposed only; main remains unchanged.
Three new pending proposals and seven advisories preserve existing authorities.
Task-obligation A+C remains unapproved; no new domain or successor dossier begins.

This begins the maintainer-directed deep code review. It supersedes the earlier
reconciliation's recommendation to prepare the final successor-session dossier.
That dossier is **postponed**. The previous inventories remain useful dated
evidence, not proof of implementation review or agent adoption.

The [RI audit](repository-intelligence-code-audit.md) is the first domain report.
The [coverage ledger](code-audit/README.md) records exact versions and remaining
work. Neither is a runtime source registry, architectural decision, scientific
judgment, backlog authority or implementation grant. Taxonomy, accepted ADRs,
source/tests and canonical backlog retain their established authority.

## Authenticated landscape

Baseline feature `feat/qwen-context-worker`:
`95efbf711c3644fb32d269d85927000cd8f4aaa9`.
Remote main: `5d979920d0728775ed529457c88f5b68b440c64f`.
Local main remains `862bda2d3d1d812893f84ab69691fc068ecce268`; it is not the
destination baseline. Remote advertisements and exact ref names are preserved
in [refs.json](code-audit/refs.json).

The canonical checkout is the sole registered worktree. At entry there was no
Checkout owner, staged change or tracked worktree change; the same 13 forensic
files remained untracked. Their fresh fingerprints are in the ledger. They
were not incorporated into this documentation change or treated as new code.

| Census | Count | Meaning |
| --- | ---: | --- |
| Named local/archive/remote-tracking refs | 92 | Existing names; not 92 maintained implementations |
| Additional remote advertisements | 9 | Eight heads and the merged PR head; overlap with local objects |
| Distinct tip commits | 40 | Every tip tree inspected through Git objects |
| Reachable commits | 496 | Headers/ancestry inventoried; not all diffs reviewed |
| Distinct paths at tips | 7,977 | Includes apps, frontend, scripts, tests, experiments, docs and configuration |
| Tip path/blob versions | 8,452 | Exact shared and different versions, not filename-only counts |
| Paths in reachable parent-edge history | 8,239 | Includes deleted and intermediate paths missing at tips |
| Historical path/blob versions | 10,676 | All root and merge-parent changes, with review state |
| Parent-edge change records | 11,626 | Rename detection disabled; no inferred continuity |
| Reachable objects | 15,764 | 496 commits, 4,874 trees, 10,394 blobs |
| Current Python files statically indexed | 1,329 | Includes experiment/application/test code; parsing is not semantic review |

The census includes all reachable named refs, not unreachable objects or every
reflog entry. Git blob identity and current physical-file SHA-256 are separate:
checkout newline conversion may change physical bytes. Current review never
propagates automatically to a historical blob. Non-Python code is inventoried
but not implicitly reviewed by the Python call-site index.

## Ref purposes and maintenance significance

Every ref has an individual count, ancestry comparison and shared destination
delta in the ledger. These groupings explain disposition, not authority:

| Ref family | Purpose and disposition | What remains |
| --- | --- | --- |
| Current feature and its remote | Active maintained source plus accumulated research/application history | Domain review and selective destination decisions; not wholesale promotion |
| Remote main | Actual protected destination, including Commands PR #1 | Preserve its destination-only documentation and composition test |
| Commands integration / PR head | Original main-derived bounded integration, merged | Provenance only; do not reopen the PR |
| Local main | Historical local destination pointer | Do not mistake its age for missing remote adoption |
| Multi-resolution search / dashboard | Earlier capability branches, consolidated/superseded as active checkouts | Different retained versions still need their own review where relevant |
| Qwen local/cohort/development/map/review tips | Earlier task and review checkpoints, mostly ancestors of current feature | Original receipts and version-specific semantics; existence does not imply success |
| Qwen real-task | Divergent historical worker experiments | 19 commits unique to that tip relative to feature; inspect before any adoption |
| Pipeline preparation | Incomplete execution infrastructure checkpoint | Three unique commits; no inferred completed science |
| Source-grounding successor | Incomplete/blocked scientific branch | Twelve unique commits; original failed entry and forensic custody remain |
| Scientific execution archive | Preserved approval/PACKET history | Twelve unique commits; old path-bound grants are not current authority |
| Scientific legacy target archive | Preserved historical target | Five unique commits; no current execution permission |
| B-0048 and consolidation topics | Candidate/admin/cleanup history | No automatic source installation or renewed authority |

“Unique to a tip” is Git ancestry, not semantic novelty. Main has two commits
not in feature ancestry, and the Commands integration tip one; reviewed Commands
source bytes are already adopted. [Tip deltas](code-audit/tip-deltas.json) list
each affected code/config/test path and its current feature/main blob. No
checkout, cherry-pick, rebase, ref rewrite or integration was performed.

## Coverage rules

Review is recorded per **path and blob**, not per directory label. The ledger
distinguishes inventory, substantive source inspection, assertion indexing,
consumer tracing, experiment reconciliation, verified agent use and qualified
gaps. `AUDIT_COMPLETE` requires all applicable dimensions; it is not assigned
merely because a file was parsed or a test passed.

The first pass inspected all 118 current RI/Context/Evaluation Python modules
(481 function/method definitions plus model/export surfaces), and traced selected
application owners. It did not completely inspect all 92 RI test modules'
fixture bodies, every historical implementation revision, or every experiment
controller/judgment cell. Those distinctions are explicit in the domain report
and per-file records. Repository-wide review is **not complete**.

## Remaining domain schedule

Exact paths and versions for every row are in `repository-files.jsonl`; these
are review filters, not a second list of hand-selected files. Shared tests belong
to each relevant owner; review one exact version once and retain cross-references.

| Order | Domain / exact maintained roots | Required depth and safety focus |
| --- | --- | --- |
| 1, underway | `src/devtools/context/`, `src/devtools/evaluation/`; native adapters and relevant experiments | Finish outstanding historical/fixture/controller review alongside the source/consumer findings already established |
| 2 | `src/devtools/execution/`, `src/devtools/tools/`, `scripts/backlog/`, `apps/qwen/change_checks.py`, `commands.py`, `development_task.py`, `edits.py`, `coding_loop.py` and their tests | Exact mutation/validation input closure, cancellation, atomic application, Checkout restoration, review and remote publication; prioritize the existing pending reuse investigation |
| 3 | `src/devtools/core/`, `src/devtools/resources/` and mirrored tests | Path/identity/time/encoding bounds, filesystem atomicity, Commands subprocess composition; preserve destination-only main tests |
| 4 | `src/devtools/model_serving/`, `src/devtools/models/`, `src/devtools/agents/`, `src/devtools/conversation/`, `src/devtools/runtime/` and any historical predecessor paths | Provider failure/usage, model-neutral contracts, Conversation versus execution, exactly one-invocation Runtime; audit branch-unique implementations too |
| 5 | `src/devtools/observability/`, `src/devtools/persistence/` and consumers | Actual Evidence/measurement/event/storage usage, incomplete realization, loss and capture policy; no generic Trace by assumption |
| 6 | Remaining `apps/qwen/`, `apps/operator_dashboard/` including frontend/lock/configuration | Worker state/Context/diagnostics, dashboard exposure/security and maintainability; code size alone does not justify splitting |
| 7 | Remaining `experiments/`, `scripts/`, `tests/`, root dependency/build and operational configuration | Controllers, archived algorithms, eligibility/oracle boundaries, dependency reproducibility and developer tooling; distinguish frozen historical fixtures from maintained runtime |
| 8 | All historical-only and differing blobs not yet dispositioned | Destination semantics, actual consumers and archive dependencies; no archival existence equals maintenance |

Some named domain roots may exist only in historical versions; the census,
rather than an assumed package name, determines the actual files. No later
domain audit, source fix, cleanup or model run is launched here.

Memory foundations must be checked against actual source and the existing
Memory backlog, rather than assuming Conversation or persistence implements
Memory. Likewise, the non-Python dashboard, lockfiles, shell/PowerShell commands,
configuration, archived script paths and developer tooling remain explicit census
members even though they do not appear in the current Python call index.

## Checkpoint verification

Focused existing RI/Evaluation regressions: **912 passed in 30.99 seconds** with
`uv run pytest --no-cov tests/context tests/evaluation -q`.
The new independent physical-line exercise has three controls and 24 adverse
cases; the latter deliberately report the existing bug, not a passing fix.
No experiment test/controller, scientific treatment, provider or inference ran.
Documentation/layout/Intake and final preservation checks are recorded in the
checkpoint completion record. No protected production gate is warranted for
this documentation/backlog-only change.

The [checkpoint manifest](code-audit/checkpoint.json) binds changed-path physical
hashes, verification counts and canonical Intake receipts. It is the overlay on
the frozen baseline census: new audit documents are not falsely presented as
files that already existed at the starting commit. It excludes its own hash;
the containing Git commit supplies that identity.

## RI follow-up checkpoint

The [deeper RI implementation/fixture review](ri-deep-audit-followup.md) repairs
the confirmed source-index defect under explicit maintainer assignment, with a
separate source commit and exact-final-tree protected gate. It adds48 substantive
experimental path reviews,26 historical tip-delta reviews and an explicit
93-path fixture-depth overlay. Three newly qualified deficiencies enter pending
Intake; four existing integration/reuse proposals receive stronger acceptance.
The inherited census and first checkpoint manifest are preserved.

RI historical review remains incomplete:177 older exact versions,558 experimental
paths without full follow-up depth and unread test bodies remain enumerated in
the overlay. The next major domain remains execution/ToolRunner/Checkout/WorkCycle;
carry those RI obligations forward. No final successor-session dossier is due.

## Branch integration assurance overlay (2026-10-24)

The [whole-feature destination candidate](feature-branch-integration-20261024.md) joins completed production work and main-only Commands with fresh protected validation. The [evidence overlay](code-audit/branch-integration-20261024.json) records exact source/dependency/test identities and one additional full real-source import fixture review. This is compatibility evidence, not completion of the remaining non-RI domain audits. Protected-main promotion is the immediate separate decision.
