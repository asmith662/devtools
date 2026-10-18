# Read-only operator dashboard adoption pilot

This repository-local, non-installable consumer reuses the pinned MIT TencentDB
MemoryPanel React/Tea shell and components; see [provenance](web/UPSTREAM.md).
It does not implement Tencent memory services or a new Devtools authority API.

From the isolated dashboard checkout, using Python 3.14 and Node 24/npm 11:

```powershell
npm ci --ignore-scripts --prefix experiments/operator_dashboard/web
npm run build --prefix experiments/operator_dashboard/web
uv run --python C:/Python314/python.exe python -m experiments.operator_dashboard.project --source C:/Users/recoveryadmin/Workspace/tools/devtools/.local/worktrees/qwen-context-worker
npm start --prefix experiments/operator_dashboard/web
```

Open **http://127.0.0.1:4173/**. Ctrl+C stops the preview. The only served content
is `web/dist`, not a repository root. Host is fixed to loopback; untrusted Host
headers receive 403, non-GET/HEAD requests receive 405, CORS is disabled, and CSP
restricts network access to this origin. Do not publish or forward this port.
Snapshots contain private local metadata and must stay ignored.

The build deletes the old snapshot. Rerun projection after each build or when
records change, then reload the browser. Missing export displays an explicit
error. A generated snapshot is historical observation, never current admission.

## Data and truth boundaries

Work Portfolio calls `Intake.queue/get` to authenticate proposals and review
history, reads canonical B-item Markdown status, and calls `WorkCycle.status`
to authenticate available assignment/result receipts. Pending, approved,
review-candidate, escalation and reconciliation dispositions remain distinct.
Legacy B-items without intake approval are listed as canonical inventory, not
approved executable assignments. A recorded grant's presence is shown explicitly
without claiming freshness or authorization. Missing assignments are reported.

Worker Activity reads only `.local/qwen-coding-worker/*/result.json` in supported
v1/v2 schemas, retaining result identity, timestamp, disposition, test/oracle exit
codes, repairs, elapsed time and reported input/output/cache/reasoning categories.
Provenance distinguishes **LOCAL_MODEL_RECEIPT**, **SCRIPTED_HOST_TEST_ONLY** and
unclassified observations. Scripted tokens are not live model consumption. No
cross-record token total is calculated. Cache/reasoning are subsets, unknown is
not zero, and local observations do not describe account quota.

All evidence references are plain local paths with exact UTF-8 byte hashes,
not arbitrary filesystem-serving links. No prompts, complete logs, credentials,
scientific journals or sealed evidence are projected. The original records stay
authoritative; projection has no calls to capture, review, approve, authorize,
execute, merge or memory-writing operations. JSON errors are surfaced. Source
HEAD, branch and dirty flag identify the selected checkout. Export is not an
atomic cross-file transaction; reconcile inconsistent records before refreshing.

## Validation

The 2026-10-18 pilot displayed source checkout `cf975fc15cd09ea65aa2ea58e1bcd59ec642bf3f`:
one pending Python 3.12 proposal, no approved intake proposals or real assignments,
the canonical backlog inventory, and four worker receipts. Two are explicitly
scripted preparations. The two local-model receipts preserve Markdown ACCEPTED
(2 calls, 8,178 input / 525 output, 34.76 seconds) and Python source task
REPAIR_BUDGET_EXHAUSTED (3 calls, 19,587 input / 1,848 output, 105.74 seconds).
No new inference was performed. Missing assignment and authority data is shown
as missing, rather than populated with synthetic bridge demonstrations.

Acceptance: three projection tests, three React/jsdom tests, TypeScript build,
Ruff, formatter and strict affected-module mypy checks passed. The installed
Chrome smoke displayed both views and each actual receipt without page errors;
POST returned 405 and an untrusted Host returned 403. Final Vite build took 4.31
seconds and UI tests 1.46 seconds. All 363 preexisting coordinator proposal,
worker and work evidence files in the preservation baseline remained byte-identical.
No framework production behavior or active work-cycle source was changed.

```powershell
uv run --python C:/Python314/python.exe python -m pytest --no-cov tests/experiments/operator_dashboard -q
uv run ruff check experiments/operator_dashboard tests/experiments/operator_dashboard
uv run ruff format --check experiments/operator_dashboard tests/experiments/operator_dashboard
uv run mypy --follow-imports=silent experiments/operator_dashboard tests/experiments/operator_dashboard
npm test --prefix experiments/operator_dashboard/web
npm run format:check --prefix experiments/operator_dashboard/web
```

Optional real-data browser smoke, with the preview running (no browser download):

```powershell
Push-Location experiments/operator_dashboard/web
$env:CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
$env:DASHBOARD_SMOKE_OUTPUT = 'C:/Users/recoveryadmin/Workspace/tools/devtools/.local/dashboard-smoke'
node browser-smoke.mjs
Pop-Location
```

The smoke switches both views, checks each actual worker receipt, captures
screenshots and verifies method/Host refusal. It never invokes models. Framework
source is unchanged, so no scientific or full protected suite is required by this
pilot's scope; focused script/UI tests are the acceptance gate.

## Future opportunities and intake constraint

The four source-derived investigation payloads in `opportunities/` are **inputs,
not captured proposals or approved backlog work**. Existing equivalents were
checked: graph/RI pressure is retained in B-0002/B-0008 and current retrieval docs;
layered and procedural Memory already appears in the canonical roadmap. Each
input links that pressure rather than inventing another B-number or claiming an
external project's behavior is implemented here.

Only the designated coordinator can call `Intake.capture`. It is the protected
active `qwen-context-worker` checkout. Capture would add pending queue files there;
this assignment also prohibits modifying that checkout. Until the maintainer
resolves that overlap, these inputs remain uncaptured, not a second queue. No
coordinator relocation or alternate intake was introduced. After permission,
run the existing CLI from that coordinator for each selected input:

```powershell
uv run python -m scripts.backlog capture C:/Users/recoveryadmin/Workspace/tools/devtools/.local/worktrees/operator-dashboard/experiments/operator_dashboard/opportunities/codegraph.json
```

Use `layered-memory.json`, `procedural-skills.json` and `knowledge-wiki.json` for
the other inputs. Capture creates only PENDING_REVIEW; review/implementation are
separate. Existing active assignments, Python 3.12 proposal and scientific state
remain unchanged. The next dashboard decision is whether this limited static
metadata surface merits maintained adoption; no write controls or backend follow
automatically.
