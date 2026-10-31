# Supervisor-delegated B-0035 host integration

Implement complete authorized inventory in RepositoryCodingHost's initial request
and installed-source lifecycle. The accepted Qwen-authored complete_inventory
function is installed as candidate source in navigation.py, not production yet.
This is a new worker episode. Prior calls/results are not being replayed.

The supervisor has resolved ownership; you need not search for an integration owner:
- navigation.py owns complete_inventory and metadata/message composition. Keep
  substantive composition there; no import of repository.py and no new modules.
- RepositoryCodingHost.__init__ initializes self.messages before disclosure/check
  bookkeeping. This is the initial objective/inventory presentation integration point.
- RepositoryCodingHost.prepare, after scope.check_current and before
  prepare_navigation/build_request, is the current-inventory refresh integration point.
- build_request stays the pure request/schema assembly seam. Do not introduce
  inventory only there, which would misalign source indices and compaction guards.
- apply already observes and verifies installed changes, updates self.scope and
  rebuilds the index. Consume that verified scope on the next preparation.
- prepare_navigation currently assumes an objective-only prefix (len==1). Reconcile
  that assumption so the optional ranked candidate view coexists exactly once.

These are trusted supervisor decisions grounded in the exact source below, not
model-generated conclusions or a reference implementation. You choose the code.

Required behavior:
- Exact objective remains first. One complete inventory immediately follows it;
  optional ranked candidates follow. No extra inventory-only model request.
- Use every resource in actual host-authorized scope, including empty text. Keep
  repository/snapshot/content identities, relative addresses, UTF-8 byte sizes
  and editable flags correct. Ranked candidates are incomplete and cannot substitute.
- Repeated prepare is idempotent. Refresh after verified installed source changes.
  Do not shift/rebind existing source/check message indices or change native history.
- No source content, unauthorized paths or absolute roots in inventory. Metadata
  never grants source-read credit, exact witnesses, effects or editing permission.
- Count all inventory bytes in existing complete-request accounting. Fail explicitly
  before inference if representation or mandatory full request cannot fit; projection
  must not silently discard the inventory. Preserve compaction/native Tool behavior.
- Keep currentness, admission, fixed checks, custody, budgets and authorization intact.

Editable files: repository.py and navigation.py only in src/devtools/agents/coding.
repository.py is 32,383 bytes with only 385 bytes remaining under the 32,768-byte
resulting-source ceiling; keep host orchestration small. No limit increases, new
files, tests/rule changes, unrestricted shell or publication. Existing batches allow
at most two anchored operations, 4,096 bytes per old/new region and 8,192 aggregate.
Edits require current exact active source; omitted/stale source must be reacquired.

Exact implementation/contract regions follow. Public focused diagnostics are
authorized for reading; hidden acceptance/reference code is unavailable. You may
read genuinely missing authorized source, submit grounded edits, consume real
check feedback and repair, or report a precise blocker. A search path is an exact
authorized file address, never a directory; omit it for authorized-scope search.

At most eight model requests, four acquisition attempts, three edit proposals and
three applications including two natural failed-check repairs. Preserve opportunity
to consume validation feedback. No predetermined patch or edit is forced. A plain
plan is not implementation; success requires independently accepted full lifecycle.
