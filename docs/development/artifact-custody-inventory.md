# Initial artifact custody and hygiene inventory

Observed 2026-10-23 at feature `3c09641dd17b13b83c2fe84e3f1cf4920ca7186f`.
This is an inventory and future review procedure, **not deletion authority**.
No artifact, model cache, directory, branch, scientific receipt or permission was
removed/changed. Source is not being reorganized by this documentation audit.

The [existing reconciliation](reconciliation.md) and
[experiment recovery contract](../../experiments/README.md) remain authoritative.
[Dated metadata evidence](reconciliation-inventory-20261023.json) contains exact
root/major directory entries, observed cache paths, denied paths, legacy custody
locations and forensic fingerprints. Names/counts are metadata, not a complete
content/size or restore audit. No private prompts, usage ledger contents, secrets
or Learned Intelligence catalogs were imported into this inventory.

## Root and major ownership

| Exact path | Ownership / classification | Current disposition |
|---|---|---|
| `.git/` | Canonical Git objects/config/refs | KEEP; one registered checkout. No permission/config mutation |
| `src/` | Reusable maintained framework | KEEP; Python/package docs are not temporary artifacts |
| `tests/` | Maintained tests plus separately excluded experiment tests | KEEP; tests/experiments exclusion is not disposal permission |
| `docs/` | Architecture, research, development custody and canonical backlog | KEEP; indexes retain distinct authority |
| `apps/` | Maintained Qwen and operator dashboard applications | KEEP; feature-only does not mean disposable |
| `scripts/` | Developer/operator entry points and WorkCycle composition | KEEP; not another framework domain |
| `experiments/` | Historical protocols, data, source and result evidence | KEEP; collection state and frozen bindings govern reuse |
| `.local/` | Mixed operational evidence, archives, drafts, candidates and caches | HOLD; never recursively treat the entire directory as cache |
| `codex-handoff/` | Ignored successor/local completion handoff | KEEP latest; durable decisions belong in canonical docs |
| `.venv/` | Generated locked development environment | Potentially recreatable, not approved for removal; no rebuild in this phase |
| `.uv-cache-audit/` | Ignored dependency/cache data | Custodian review required; not a source checkout or blanket cleanup target |
| `.idea/` | Local IDE settings | User-owned; no cleanup authorization |
| `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/` | Generated tool caches | Cache candidates only after exact-path and active-process/custody checks |
| `.coverage` | Generated coverage database | Candidate only after protecting authoritative coverage logs/exact-tree evidence |
| `.gitignore`, `.gitattributes`, `AGENTS.md`, `README.md`, `pyproject.toml`, `uv.lock` | Maintained root policy/configuration | KEEP; do not rewrite them to hide unexpected artifacts |

The metadata scan saw 91 immediate .local directories and 757 immediate files,
including this audit's ignored scratch material. It recorded 476 cache-directory
occurrences while deliberately not reading their contents. Counts are snapshots,
not proof of cleanup eligibility or recursive disk usage. Top-level source/test/
docs/apps/scripts/experiments and .local directories are enumerated in the JSON.

## Evidence and authority custody

| Exact path / bounded group | Dependency and reason to retain | Eligibility |
|---|---|---|
| `.local/archives/repository-2026-10-19/preservation-manifest.json` | Original checkout/address and file identity map | KEEP; recovery authority is historical provenance, not fresh execution authority |
| `.local/archives/repository-2026-10-19/checkout-evidence.zip` | 4,744,403-byte observed packet; original preservation report documents extraction/hash checks | KEEP; historical restore verification not rerun here |
| `.local/archives/repository-2026-10-19/legacy-target-evidence.zip` | 1,437,098-byte observed legacy target packet | KEEP; never recreate a second Devtools checkout to inspect it |
| `.local/archives/repository-2026-10-19/original-forensics.zip` | 80,627-byte packet supporting original forensic custody | KEEP; original 13 files remain in place |
| `.local/archives/experiments-2026-10-19/` | Collection packets, manifests and restore evidence | KEEP; same-SSD archives are not off-volume backup |
| `.local/preserved-root/` | Historical root evidence and original path bindings; seven scan regions here/elsewhere were unreadable | HOLD; no deduplication/deletion based only on archived-looking names |
| `.local/preserved-checkouts/` | Eight residual preservation directories listed below | HOLD; compare actual files with archive member manifests before considering residual removal |
| `.local/backlog/` | Grants, assignments, reviews, candidates, integration/recovery records | KEEP; old paths/grants remain historical and cannot be rewritten into authority |
| `.local/qwen-coding-worker/` | Original native requests/responses, proposals, validation and failed outcomes | KEEP; accepted production source does not obsolete original failed receipts |
| `.local/closeout-candidates/` | Exact candidates, reviews and protected-validation evidence | HOLD; identify sole evidence and publication dependencies first |
| `.local/commands-integration-20261022/` | Destination-specific Commands integration/provenance/gate evidence | KEEP; merged main source does not replace its audit trail |
| `.local/experiment-runs/`, `.local/experiment-failures/`, `.local/deployment-receipts/` | Execution history; names alone do not establish terminality or safe replay | HOLD; inspect manifests/owners before cleanup selection |
| `.local/usage/` | Private normalized local usage ledger/reports | KEEP/private; no ingest or account-wide completeness claim here |
| `.local/tencent-source.zip`, `.local/tencent-inspection/`, `.local/tencent-public/` | Prior external-discovery materials, not the requested starter ZIP | HOLD; identify original intake/research dependencies before pruning vendor/build copies |
| `.local/reconciliation-20261023/` | This audit's metadata/intake/validation scratch | Keep through checkpoint/handoff verification; later exact-path review only |

The 13 original untracked files live below the two `experiments/source_grounding/runs/`
identities `b34e9e288e30f7289e14453f8a2f9ca8acd6940dee05037486c403c803b5d2c6`
and `b6cd4408b4dbc86a50c335f4a364898ff3b45c123becb7b6865c34208d3e1982`.
The JSON records their exact individual paths and Git blob fingerprints. They
are preserved forensic evidence, not accidental untracked cache files.

### Residual checkout-named preservation directories

All are under `.local/preserved-checkouts/`:

- `experiment-execution-pipeline-prepare/`
- `legacy-deployment-target/`
- `multi-resolution-search/`
- `operator-dashboard/`
- `qwen-context-worker/`
- `qwen-real-task/`
- `scientific-execution/`
- `source-grounding-successor/`

Observed children include.local, historical experiment evidence, metadata and
handoffs; the scan found no Git marker under these residual directories. They
are not registered active Devtools worktrees. That does not prove every payload
is redundant. The original reconciliation's removal/compaction statements must
be read alongside this current residual metadata, without rewriting history.

`.git/worktrees`, `.local/worktrees` and
`.local/deployments/source-grounding-successor/target` were absent. No new
worktree/clone/source-copy directory was created to perform the audit.

### Nested Git fixtures are not Devtools checkouts

Five Git markers were observed:

1. `.local/host-disclosure-live-smoke/direct/fixture-repository/.git`
2. `.local/host-disclosure-smoke-failure/runtime/direct/fixture-repository/.git`
3. `.local/host-disclosure-smoke-v2-success/runtime/direct/fixture-repository/.git`
4. `.local/navigation-tests/test_scripted_native_map_sourc0/.git`
5. `.local/qwen-coding-worker/native-map-28/scripted-refresh/authored-fixture/.git`

Read-only Git inspection identified the first three as small alpha/beta/gamma
fixtures and the latter two as six-file demo/read-only/test fixtures. The fourth
required an escalated read after a permission refusal; no ACL changed. These
match the documented independently authored deterministic fixtures, not Devtools
source-tree copies. Preserve them until their test/evaluation evidence custody
is decided; do not confuse their Git markers with a second canonical checkout.

## Reviewable cleanup candidates, not approved removals

| Exact candidate paths | Required precondition before any future removal |
|---|---|
| `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `.coverage` | No active validator; preserve passing exact-tree logs and distinguish database from evidence |
| `apps/operator_dashboard/web/node_modules/` | Confirm lockfile/runtime dependencies, active dashboard state and independent rebuild procedure |
| `.local/cache/operator_dashboard/web/node_modules/` | Identify whether historical browser/build evidence references this retained cache |
| `.local/qwen-coding-worker/environment-05/pi/node_modules/` | Frozen comparison provenance/custody review before treating dependencies as reproducible |
| `.local/tencent-public/node_modules/`, `.local/tencent-public/dist/` | Confirm external-discovery/vendor/build ownership; do not assume source/download payloads are redundant |
| `.local/reconciliation/permission-blocked-dashboard-cache/` | Existing quarantined residual; explicit OS permission review, no takeown/ACL repair authorized here |
| `.local/validation/single-checkout-app-debug/` | Earlier scanner reported denied access; identify contents and owner before classifying |
| `.local/pytest-native-continuation-1/` | Current metadata scan PermissionError; opaque, not approved cache |
| `.local/preserved-root/devtools/case0003-unit1/`, `case0003-unit2/`, `case0003-unit3/`, `case0003-unit4/`, `case0003-neighbors1/`, `case0003-final/` | PermissionError regions; original source identities/packet dependencies first |
| The eight preserved-checkout residuals above | Verify each surviving member against original archives and references; no whole-group deletion by name |

The machine record enumerates the remaining observed cache paths individually.
Its skipped names include.git, virtualenv/dependency trees and generated caches;
symlinks/junctions were not followed. Excluded or unreadable areas remain an
inspection limitation. Their contents and unique data cannot be declared absent.

## Safe future cleanup procedure

1. Select a small exact-path allowlist with owner, candidate classification,
   original source/review/run dependencies and explicit deletion authority.
   Leave unknown/unreadable/evidence-bearing paths on hold.
2. Authenticate the one canonical checkout, tracked/index/untracked state,
   Checkout ownership and relevant active processes. Preserve the 13 forensic
   identities and all original branch/archive refs. Never remove an owner lease
   to force progress; existing recovery owns interrupted source operations.
3. Revalidate each relevant archive/member manifest and restore procedure using
   a bounded data-only location when separately authorized. Do not create a
   Devtools source checkout, rewrite receipts or convert restored grants into
   current authority. Establish off-volume recovery needs rather than assuming
   same-SSD packets protect against disk loss.
4. Produce a dry-run path/identity/size/dependency list. Resolve every absolute
   target inside the intended allowed directory, reject aliases/junction escapes,
   and require a separate decision for unknown or permission-restricted data.
5. If later authorized, use one Windows shell and native literal-path operations
   end to end. No cross-shell generated deletion commands, forceful permission
   changes, broad.local deletion or model-cache removal by inference.
6. Recheck Git/forensics, archive recoverability, layout and source/evidence
   references; record actual removals and retained holds. This document executes
   none of those destructive steps.

The pending [custody investigation](../backlog/proposals/0385a359-399f-40bb-aed4-caf5239c9fc8/proposal.json)
retains these questions without implementing a cleanup framework or granting
deletion. No external local repository, personal model sessions or separate Learned
Intelligence storage was traversed.

## Final production reconciliation checkpoint (2026-10-23)

The [completed production reconciliation](../research/production-adoption-and-architecture-reconciliation.md)
and its [machine evidence](../research/production-adoption-and-architecture-evidence-20261023.json)
now add bounded streaming member verification and measured residual/cache sizes.
No extraction, restore execution, source copy, ACL change or deletion occurred.
All sizes below are observed bytes, not promised disk reclamation. Active
python/node processes were observed but their roles were not authenticated;
therefore no cache was declared idle and no generated cache was removed.

### Reauthenticated recovery packets

- All 24 CLOSED experiment packet hashes and every member match original
  manifests. These are same-SSD packets, not off-volume recovery.
- `checkout-evidence.zip`: 4, 744, 403 bytes; SHA-256
  `5debf60d98465c920f77ea4b6ae13a4855699f912ebcef1ad1ea15aed8f4ea5e`;
  all 1638 members match `preservation-manifest.json`. Seven ordinary residuals
  below also match their original manifest and packet bytes.
- `legacy-target-evidence.zip`: 1, 437, 098 bytes; SHA-256
  `9870af7eb5d811be230968e44df0ffc4c62fb067441c03343ca0f100ca564454`;
  all 16 members match `legacy-target-manifest.json` and surviving target files.
  Its private usage ledger is hash-verified, not copied into public documentation.
- `scientific-execution.bundle` retains the earlier recovery identity
  `a21eb21acfa34bc135d54f187ee2352208a7fc0879a805ac90239ab23319d060`
  and 1, 579, 402, 674-byte package record. Fresh full bundle hash/unbundle/restore
  was not performed. Keep package/verification/restore records and historical refs.
- Original13 forensic files remain at the same source-grounding paths and are
  rechecked against their recorded Git fingerprints before publication.

### Exact residual and generated-path dry run

This is metadata/custody inspection, not a deletion plan executed. Manifest
member equality establishes no currently unique bytes among the verified
residual payloads, but not dispensability: receipts/grants retain original paths,
same-volume recovery is limited and process/evidence dependencies need review.
No whole-preservation deletion is authorized from duplicate bytes alone.

| Exact path | Measured bytes / files | Uniqueness, custody and disposition |
|---|---|---|
| `.local/preserved-checkouts/experiment-execution-pipeline-prepare` | 6, 578, 669 / 418 | 418 current members match general manifest/packet; HOLD for path/custody dependency review |
| `.local/preserved-checkouts/legacy-deployment-target` | 13, 903, 310 / 16 | 16 current members equal separate legacy manifest/packet; HOLD for custody/dependency review |
| `.local/preserved-checkouts/multi-resolution-search` | 457, 819 / 12 | 12 current members match general manifest/packet; HOLD for path/custody dependency review |
| `.local/preserved-checkouts/operator-dashboard` | 11, 294 / 3 | 3 current members match general manifest/packet; HOLD for path/custody dependency review |
| `.local/preserved-checkouts/qwen-context-worker` | 2, 197, 774 / 198 | 198 current members match general manifest/packet; HOLD for path/custody dependency review |
| `.local/preserved-checkouts/qwen-real-task` | 467, 301 / 91 | 91 current members match general manifest/packet; HOLD for path/custody dependency review |
| `.local/preserved-checkouts/scientific-execution` | 15, 912, 261 / 181 | 181 current members match general manifest/packet; HOLD for path/custody dependency review |
| `.local/preserved-checkouts/source-grounding-successor` | 2, 307, 405 / 141 | 141 current members match general manifest/packet; HOLD for path/custody dependency review |
| `.local/preserved-root` | 183, 715 / 14 | Lower bound; denied/unknown contents HOLD, no ACL or ownership change |
| `.local/reconciliation/permission-blocked-dashboard-cache` | 0 / 0 | Lower bound; denied/unknown contents HOLD, no ACL or ownership change |
| `.local/validation/single-checkout-app-debug` | 47, 002 / 22 | Readable metadata does not establish regenerability/uniqueness; HOLD until owner/source/evidence dependencies qualified |
| `.local/pytest-native-continuation-1` | 0 / 0 | Lower bound; denied/unknown contents HOLD, no ACL or ownership change |
| `.mypy_cache` | 125, 530, 341 / 18 | Generated cache/build candidate; lock/config evidence retained, active-use ownership unqualified; future exact-path review, NO REMOVAL |
| `.ruff_cache` | 390, 018 / 1005 | Generated cache/build candidate; lock/config evidence retained, active-use ownership unqualified; future exact-path review, NO REMOVAL |
| `.pytest_cache` | 1, 588, 047 / 5 | Generated cache/build candidate; lock/config evidence retained, active-use ownership unqualified; future exact-path review, NO REMOVAL |
| `apps/operator_dashboard/web/node_modules` | 154, 223, 129 / 10947 | Generated cache/build candidate; lock/config evidence retained, active-use ownership unqualified; future exact-path review, NO REMOVAL |
| `apps/operator_dashboard/web/dist` | 1, 021, 989 / 4 | Generated cache/build candidate; lock/config evidence retained, active-use ownership unqualified; future exact-path review, NO REMOVAL |
| `.local/cache/operator_dashboard/web/node_modules` | 154, 223, 129 / 10947 | Generated cache/build candidate; lock/config evidence retained, active-use ownership unqualified; future exact-path review, NO REMOVAL |
| `.local/tencent-public/node_modules` | 201, 564, 681 / 18739 | Generated cache/build candidate; lock/config evidence retained, active-use ownership unqualified; future exact-path review, NO REMOVAL |
| `.local/tencent-public/dist` | 2, 887, 798 / 7 | Generated cache/build candidate; lock/config evidence retained, active-use ownership unqualified; future exact-path review, NO REMOVAL |
| `.local/worktrees` | not measured | Absent at inspection; no cleanup performed |
| `.git/worktrees` | not measured | Absent at inspection; no cleanup performed |
| `.local/deployments/source-grounding-successor/target` | not measured | Absent at inspection; no cleanup performed |

The seven ordinary residuals' current hashes agree with the original general
manifest; the eighth uses its separately authenticated legacy packet. None has
become a new source checkout. `.local/worktrees`, `.git/worktrees` and the old
`.local/deployments/source-grounding-successor/target` remain absent.

Denied regions remain exact HOLD paths:

- `.local/preserved-root/devtools/case 0003-unit1/`
- `.local/preserved-root/devtools/case 0003-unit2/`
- `.local/preserved-root/devtools/case 0003-unit3/`
- `.local/preserved-root/devtools/case 0003-unit4/`
- `.local/preserved-root/devtools/case 0003-neighbors1/`
- `.local/preserved-root/devtools/case 0003-final/`
- `.local/reconciliation/permission-blocked-dashboard-cache/.pytest_cache/`
- `.local/pytest-native-continuation-1/`

`single-checkout-app-debug` is now readable (47, 002 observed bytes); this does
not itself qualify it for cleanup. Nested independently authored Git fixtures
listed earlier remain KEEP/HOLD, not Devtools duplicate checkouts.

### Collection payload and archive distinctions

The current-file rehash bound was64MiB per collection: 1073 original entries
EXACT, 5697 NOT_REHASHED within the bound, 22 expected compacted root-report
absences, one CURRENT_BYTES_DIFFER. `experiments/qwen/docs/overview.md` now has
later maintained-application documentation appended after the original 7131-byte
snapshot (current 24787 bytes); the original archived member still authenticates.
This is an evolved current document versus frozen evidence, not authority to
rewrite either. Full current-tree freshness of every large dogfood/controller
payload is not claimed. Every collection manifest/summary is fingerprinted and
all CLOSED archive members verify independently of these bounded current checks.

Archived research transfer/starter packages, Qwen raw request/response/proposal
and validation receipts, live/failed Checkout state, Git fixtures, scientific
packets, denied regions and unknown assets remain HOLD/KEEP. Exact custody
dependencies include original frozen manifest paths, the five-flow audit's
297 files/21 selected inputs, WorkCycle/recovery seals and forensic hashes.
Successful code publication never makes failed original receipts disposable.

The earlier safe future cleanup procedure remains applicable: qualify an exact
allowlist, canonical ownership/active processes, original evidence links, archive
recoverability and any off-volume requirement; then a separately authorized
Windows literal-path deletion with verified resolved targets. Never recurse over
`.local/` or preservation directories, alter ACLs, follow junction escapes,
delete model caches or remove an unknown lease. **Actual removals: zero paths,
zero bytes.** The existing custody proposal remains PENDING_REVIEW.
