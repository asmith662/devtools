# Supervisor decision before delegation

Baseline: `63d5466ef4d6f0734ed2ba65827c42bba59e04d5`.
This is a task-specific engineering decision within existing ownership, not a
new framework, public protocol, or architectural promotion.

1. **Representation:** `devtools.agents.coding.navigation.complete_inventory`
   is the accepted model-authored Stage A representation. Its original full-file
   identity and current-parent reconciliation are recorded separately. It derives
   all rows from the actual `SourceScope.snapshot`, checks currentness, editable
   membership and bounded complete serialization. It does not search or read source.
2. **Initial integration point:** `RepositoryCodingHost.__init__` establishes
   `self.messages` before disclosure/check index bookkeeping. That is the owner
   for initializing the objective plus complete-inventory presentation prefix.
   Substantive metadata/message composition belongs in existing `navigation.py`;
   the repository host should perform only narrow orchestration using explicit
   text/scope/editable/bound values. Navigation must not import the repository
   host or introduce a second state owner. Worker chooses actual implementation.
3. **Preparation point:** `RepositoryCodingHost.prepare`, after its currentness
   check and before `prepare_navigation`/`build_request`, is the owner for refreshing
   derived inventory against the current scope. Preserve the objective first,
   exactly one complete inventory immediately after it, and optional candidate
   metadata afterward. Repeated preparation must not grow the prefix. Once source
   or check indices are registered, refresh must not shift or rebind them. Native
   messages/results and prior immutable request records must remain unchanged.
   The inventory is explicitly derived current Context, not a historical Tool fact.
4. **Assembly/capacity:** `build_request` remains the existing pure native-schema
   assembly seam. Inserting metadata only there would misalign original-history
   indices and the semantic-compaction history guard. Put the required metadata
   in the host's prepared message representation instead. Existing `prepare`
   full-request measurement/projection is authoritative. Inventory is mandatory
   metadata, never an eligible source disclosure or omit-able search result.
   Representation overflow or full-request overflow must fail before model entry.
5. **Refresh:** `apply` already executes authorized source effects, observes a new
   SourceScope, verifies installed contents against the admitted after-image, assigns
   `self.scope`, clears stale active disclosures and rebuilds the RI index. Preserve
   that mechanism. The next `prepare` must derive inventory from that verified scope;
   a construction-time snapshot cache cannot satisfy lifecycle behavior.
6. **Candidate coexistence:** `task_entry` explicitly ranks a bounded lexical subset
   and sets `complete_inventory=False`. It cannot represent the complete authorized
   surface. `prepare_navigation` currently requires `len(messages)==1`; reconcile
   this objective-only assumption with the new metadata prefix while preserving
   candidate idempotence, existing optional navigation behavior and native Tools.

Source: repository.py constructor/request/preparation/application methods;
navigation.py `prepare_navigation`/`task_entry`; accepted Stage A source;
SourceScope; Prompt; projection's existing eligibility; public focused checks.
This decision supplies ownership and requirements, not reference code or a patch.

Feasibility: repository.py is 32,383 bytes (385 remaining), current navigation.py
14,952 bytes, reconciled Stage A navigation.py 16,595 bytes. A nonexecuted,
syntax-only stand-in with explicit value routing for initialization and refresh
plus an import measured 32,613 bytes, 155 below the unchanged ceiling. It contained
no inventory logic and was never installed or sent to the worker. This establishes
room for narrow wiring; an actual proposal must still pass exact admission.
Region/aggregate/batch limits and current witnesses remain unchanged.

One cohesive Stage B responsibility is delegated: representation consumption plus
complete initial/refresh/capacity lifecycle. There is no conditional second worker
stage. Partial or unused helper code will not be integrated as completion.
