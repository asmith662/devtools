# Devtools read-only operator console

This repository-local consumer retains the Tencent MemoryPanel React/Tea shell,
list/detail panels, page header and status components. The pinned upstream MIT
attribution remains in [UPSTREAM.md](web/UPSTREAM.md) and every build's license.
No Tencent backend, database, authority service or worker instrumentation is added.

## Start locally

Prerequisites: Python 3.14, Node 24/npm 11, project Python dependencies, and the
existing frontend dependencies (`npm ci --ignore-scripts --prefix
apps/operator_dashboard/web` once after checkout).

From the dashboard checkout, **one operator command** builds the frontend and
serves both UI and API:

```powershell
uv run --python C:/Python314/python.exe python -m apps.operator_dashboard.server --build --worker-root .local/qwen-coding-worker --raw-details
```

Open **http://127.0.0.1:4174/**; Ctrl+C stops this console. This replaces the V1
static preview workflow on 4173. Do not start Vite preview for live supervision.
Omit `--raw-details` to hide prompts, responses, native arguments, patches and
validation output. The flag deliberately enables disclosure of trusted local
worker records; it grants no execution authority. `--worker-root` is explicit,
repeatable host configuration and cannot be changed by an HTTP client. No model,
Docker or worker service is started. `--port` may select another loopback port.

The server authenticates the configured `devtools.backlogCoordinator` through
existing Git/common-directory checks at startup. It does not relocate it. The
configured canonical checkout remains the coordinator; a historical branch or
commit printed in an old receipt is not its current identity. The dashboard's
branch is not an alternative backlog. Only read-only Git HEAD inspection occurs
per overview.

## Fresh views and evidence

UI opens and view changes fetch current data. Refresh rereads the selected source
records; visible pages also poll once per 60 seconds. Last successful observation
is shown with local time and its UTC source. Fetch errors retain previously loaded
data explicitly as STALE. Historical receipt presence never establishes a running
worker, fresh admission, approval or implementation authority. There is no new
persistent data store. Legacy `project` export remains available for offline
metadata inspection, but live startup does not read or serve `data.json`.

- Work Portfolio reuses `Intake.queue/get/duplicates`, canonical Markdown and
  `WorkCycle.status`. Select proposals for complete discovery, parent, benefit,
  affected resources, evidence, uncertainty, dependencies, duplicate hints and
  authenticated review history. Select backlog items for all recorded metadata,
  dependency/split relationships, dedicated recorded disposition sections and
  original body. Existing Markdown sections come from the canonical filesystem
  Markdown model. Source body is rendered as readable plain text, never unsafe
  HTML. Linked intake publication reviews are shown when recorded. Unspecified
  rationale, priorities, acceptance and decisions remain NOT_RECORDED; lifecycle
  status is not an inferred reason or grant. Missing standardized rationale fields
  are a metadata gap for later review, not new metadata authored by this UI.
- Worker Activity groups by explicit task name, or the legacy task's recorded
  baseline source when no task-name field exists. A human-readable Markdown label
  is identified from that legacy source contract. No cross-run session identity
  is manufactured. Same directory names in different configured roots retain
  separate reference-derived URL selectors, not new scientific/work identities.
- Real local-model receipts and scripted host tests have separate filters and
  provenance labels. The current inventory is five pending proposals, 41 leaf
  backlog items, zero real assignments, two local-model runs and two scripted
  preparations. Canonical epics can be resolved by their existing B-number detail
  route; the overview retains its existing leaf-item inventory.
- Each actual run opens its frozen objective, recorded model/profile, bounds,
  usage, start/end and elapsed time, repair count and per-turn history. Context
  records retain representation, source/snapshot identities, byte/span and token
  information where captured. Host acquisition is distinct from model Tools.
- Turns use `result.json` stage entries and their exact `turn-NN/request.json`,
  `response.json` and `proposal.patch`. Native `propose_edit` names/argument JSON,
  provider-call IDs and host proposal IDs remain correlated. Host validation argv,
  exit codes and stdout/stderr remain separate from model proposals. Feedback is
  the exact JSON substring following the archived HOST FEEDBACK marker in that
  request, not reconstructed from later logs. Source-before/after versions and
  per-turn reported usage are retained. No command shown in the UI is executable.

Historical Markdown has two turns: TESTS_FAILED then ACCEPTED. Python source
segments has three TESTS_FAILED turns and REPAIR_BUDGET_EXHAUSTED. Those outcomes
are unchanged. Requests contain flattened user-role prompt captures, not a native
multi-message chat history; continuation identifiers and reasoning are commonly
null and shown as NOT_CAPTURED. Absent raw files are not fabricated. Scripted
usage is synthetic. Missing usage remains unknown; cached input/reasoning output
are subsets and are never added to input/output totals. Local usage is not quota.

## Security and bounded disclosure

The Python stdlib HTTP server binds only 127.0.0.1 and serves a closed static-asset
list plus GET/HEAD `/api/overview`, `/api/proposals/<UUID>`,
`/api/backlog/<B-number>` and `/api/runs/<indexed-selector>`. Strict Host, exact
same-origin Origin when supplied, and Fetch-Site checks reject cross-origin
access. No CORS permission is emitted. Mutation/preflight methods are refused.
Queries, traversal/encoded paths, arbitrary files and roots are not accepted.
Symlink resolution is checked against configured roots. No model, Git mutation,
backlog write or approval endpoint exists.

Response limit is 2 MiB; oversized responses fail visibly with 503. Raw text
fields display at most 16,000 characters, with original character count and
TRUNCATED labels. Source files are read using canonical bounded filesystem APIs
and remain unchanged. At most ten archived turns are displayed, with explicit
truncation/count if exceeded (current worker runs have at most three). The only
raw sidecars read are the closed per-turn list above, plus freeze/result metadata;
no arbitrary recorded path, global usage ledger, session directory, oracle-runner
source, sealed scientific evidence or credential file is followed. File hashes
identify observed archived bytes, not signed provenance or current authority.
Cross-file reads are not an atomic snapshot; inconsistent records must be
reconciled at the owning domain rather than repaired by the dashboard.

## Focused verification

```powershell
uv run --python C:/Python314/python.exe python -m pytest --no-cov -p no:cacheprovider tests/apps/operator_dashboard -q
uv run ruff check apps/operator_dashboard tests/apps/operator_dashboard
uv run ruff format --check apps/operator_dashboard tests/apps/operator_dashboard
uv run mypy --follow-imports=silent apps/operator_dashboard tests/apps/operator_dashboard
npm test --prefix apps/operator_dashboard/web
npm run format:check --prefix apps/operator_dashboard/web
```

With the local console running, browser verification uses installed Chrome/Edge,
not a browser download:

```powershell
Push-Location apps/operator_dashboard/web
$env:CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
$env:DASHBOARD_SMOKE_OUTPUT = 'C:/Users/recoveryadmin/Workspace/tools/devtools/.local/dashboard-v2-smoke'
node browser-smoke.mjs
Pop-Location
```

The browser inspects actual proposal/backlog details and the two genuine run
histories, native arguments, patches, filters and Refresh; screenshots and a
verification receipt remain local. Isolated fixtures test newly added proposals
and receipts without restart/build, missing messages, rejected origins/methods,
traversal, response limits, distinct roots and unchanged source evidence. No live
model call or controller regression suite is needed. Production framework code,
coordinator metadata and worker execution are unchanged. Tea's legacy React peer
and forwardRef warnings and the roughly 729 kB JS bundle remain known limitations.
The next useful improvement is operator review of these detail/disclosure choices;
missing native conversation capture requires separately authorized worker work.

## Integration dependency maintenance (2026-10-24)

The main-derived integration candidate pins Vite 6.4.4 and Vitest 4.1.12 in
`web/package.json` and the dependency lock. These replace the recorded vulnerable
Vite 6.4.1 / Vitest 3.2.4 development dependencies; no server exposure, frontend
application behavior, Python dependency or execution authority is added.
Install with the existing `npm ci --ignore-scripts` procedure and run the tests,
format check and build above. The dated integration report records the actual
audit and validation results; a dependency-audit result is not a guarantee about
future advisories. Tea's existing React peer warnings and bundle-size warning
remain distinct from the repaired dependency findings.
