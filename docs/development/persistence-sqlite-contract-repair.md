# SQLite Conversation contract repair

The three P2 contracts established by the [Persistence/Recovery audit](../research/persistence-and-recovery-audit.md) are implemented and independently verified on accepted main. Audit PR #37 was already merged at starting main `3b8644cfb2dc11d383f30855fbce19764081d6c4`. This increment changes only the existing SQLite owner, its maintained test family and package contract; it does not implement autonomous recovery architecture or observation Option B.

## Verified delivery

Production **`233b170eba86a596ff622cc0bd8ac5e170d2e6ca`**, tree `146c079d8db639e242cc7c421fb3d103726dcf26`, was normally merged through PR #38 into independently observed main **`c6ca6a2f64d729a8192cde1109e68b4a1830c7d2`**. The accepted tree matches the protected candidate. Three logical implementation commits remain separately reviewable:

| Existing proposal | Commit | Delivered boundary |
| --- | --- | --- |
| `3e07840c-7021-4395-939e-b75a47c5374e` | `acb65fb3813877adfa73e285e9d812debf0e2339` | One read transaction across session, ordered History and current refs |
| `77a31939-9c99-4a60-9016-622843cc10f3` | `1f25cbbd1c78fe85a5d03dd9afcf65e0a34386d6` | Atomic fresh installation with reservation/version recheck |
| `794a4df3-e51e-4927-8f43-c7dd3cb6535c` | `233b170eba86a596ff622cc0bd8ac5e170d2e6ca` | Text-class admission before semantic restoration |

The full gate applies to their combined final committed executable tree. Shared test guards are not represented as independently protected-gate validated intermediate trees. The [machine receipt](../research/code-audit/persistence-sqlite-repair-20261026.json) retains exact commits/blobs, physical validation inputs, original failures, commands, timestamps, durations, exits, runtime versions, schema catalog and post-main evidence.

## Independently established original failures

Permanent regressions were added before production edits. On the authenticated original implementation, **nine tests failed, 34 controls passed, zero setup errors**:

- A real WAL writer committed B/thread-b between the maintained reader's History and ref queries; independent witness queries proved the intervening commit, while public load returned A/thread-b.
- Authorizer faults at table, index and version installation left partial v0 storage; ordinary retry refused it. No database deletion was used to obtain either result.
- Each of the four demonstrated BLOB columns was admitted instead of refusing. A genuine load-to-Runtime deterministic consumer entered its fake interaction once with an invalid continuation, rather than refusing before entry.

Later coverage adds late-index rollback, native transaction failures, default-journal schedules, concurrent first initialization, unknown-database custody, Unicode/empty content and an independently authored JSON v1 fixture. One intermediate literal-test placement mistake and intermediate staging EOF whitespace were corrected; they are excluded from the original defect evidence. No model, user database or scientific controller was involved.

## Coherent reads under WAL and rollback journaling

`SqliteConversationStore.load` explicitly starts a deferred SQLite read transaction, covering the session row, ordered message occurrences and source-keyed refs. The connection context commits successful reads or rolls back failures; the existing finally closes its owned connection. Missing records still return None. Source ordering, repeated-message aliasing, semantic IDs and original domain/native errors remain supported.

The WAL regression actually permits the writer to commit while the paused reader exists. The reader returns the complete older A/thread-a and an independent fresh read sees B/thread-b. No Python mutex serializes the two calls.

The default DELETE-journal regression preserves the normal 5000ms busy timeout and observes the writer attempting its actual commit before releasing the reader; the reader retains A/thread-a and the writer eventually commits B/thread-b. A separate test-only zero-wait writer proves the held read lock can refuse commit with SQLite OperationalError, roll back its candidate and settle both connections; after release, a subsequent explicit save succeeds. The tests do not require a rollback-journal writer to finish while the reader still holds its lock, nor use an indefinite wait.

Cleanup controls cover missing rows, malformed data, denied BEGIN, denied query and denied COMMIT. SQLite transaction failures remain native errors; malformed stored semantic state remains PersistenceFormatError. These controls do not claim rollback of arbitrary external model or Tool effects.

## Atomic initialization and conservative custody

Fresh initialization obtains BEGIN IMMEDIATE, then rechecks user_version after the reservation. Only a still-empty v0 database is initialized. The seven owned DDL statements execute individually in that same transaction with the version update. This avoids executescript's implicit commit of an existing legacy transaction. No SQL parser, backend, migration system or generic transaction abstraction is added.

Controlled denials during a table, first index, later index and schema-version update leave no installed user objects and allow ordinary retry on the same file. Connections close with no active transaction. A deterministic two-caller schedule forces both first observations to be v0; the waiting caller rechecks installed v1 and both complete normally. This is a bounded local SQLite concurrency result, not a guarantee for arbitrary network filesystems or unrelated DDL actors.

Existing unrelated nonempty and unknown partial v0 databases remain refused. A retained unknown-row fixture verifies the original database bytes and rows survive refusal. Existing valid v1 stores remain readable/writable. The actual sqlite_master catalog—tables, columns, constraints and indexes—matches the authenticated original catalog exactly on both tested engines. The private implementation represents owned DDL as individual statements; the persisted schema/version and public methods are unchanged.

Schema installation is atomic as its own unit. A later first save can still fail after a valid empty v1 schema was installed; the API does not claim the file itself must vanish after every failed save. Unknown old partial installations are not automatically reclaimed.

## Stored text and actual Runtime consumption

SQLite TEXT affinity alone permits BLOB storage. The decoder now checks `messages.content`, `messages.source`, `conversations.source` and `conversations.value` before constructing their semantic values. It never calls str() or guesses an encoding for these fields. A field-specific TypeError with no stored private value becomes the existing PersistenceFormatError cause. Permanent sentinel tests verify both diagnostic levels omit the payload.

Existing timestamp, ID, role, position, dangling-message and reference checks remain unchanged. Valid Unicode, NUL/whitespace and empty content, source ordering, global immutable message reuse and duplicate occurrences remain valid. The literal JSON-to-SQLite-to-JSON case independently protects v1 field spelling and UTC microseconds.

The malformed continuation is refused by public load before Runtime/model entry; valid loaded Conversations still propagate the stored ref to Runtime. Caller-coordinated checkpoints remain explicit. Neither Runtime nor Qwen gained automatic saving or any altered lock, ModelInteraction, EvidenceSink, Tool or acceptance behavior.

## Final validation and compatibility limits

On committed `233b170eba86a596ff622cc0bd8ac5e170d2e6ca`, the unchanged full protected command `uv run python scripts/validate_development.py` passed **3218 tests, two optional live skips, 100% configured production branch coverage**, exit 0, total elapsed **1156.732676 seconds**. No threshold, exclusion, selector or scientific protocol was changed. Supported Ruff, 635-file formatting and configured 521-file strict mypy pass. The final focused consumer run passed **310 tests, one opt-in live skip**, including all **54 Persistence cases**. The accepted-main Persistence/Conversation/Runtime run passed **151 tests, one optional live skip** in 24.34 seconds (25.125928 seconds including the recorded command wrapper). Both 16-case native compatibility checks passed again after merge; exact commands and identities are in the receipt.

Installed CPython **3.12.13 / SQLite 3.53.1** and **3.14.3 / SQLite 3.50.4** each passed **16 isolated public-API/schema/process-restart cases** against actual maintained source. The 3.12 interpreter has neither pytest nor pytest-cov. No runtime/dependency installation was performed, and no full 3.12 suite or complete compatibility matrix is claimed. The full configured pytest/coverage gate runs on 3.14.3. The engine versions differ and are recorded, not assumed equivalent toolchains.

Before/after physical hashes of declared tracked source/test/app/script/package-document/configuration inputs, Git identities and exact command records authenticate the accepted executable tree. This is not universal ignored/environment/toolchain dependency closure or cache-reuse authority; broader validation closure remains separate. JSON/JSONL, local file links, layout, 67 Intake chains and whitespace are checked. All thirteen forensic files, 903 historical RI ledger rows, original experiments and historical refs are preserved.

## Canonical disposition and remaining architecture

Each original UUID receives its own append-only ADVISORY implemented-and-merged evidence. Administrative PENDING_REVIEW remains; it is not another instruction to implement the delivered scope. No duplicate proposal, B-number, approval, grant or parent closure is created. Original eleven-path audit/probe records remain historical; three changed source/test/package-doc versions have explicit maintenance overlays rather than transferred old review credit.

Broader B-0027/B-0028/B-0011/B-0034 remain open: automatic durable agent state, stale-checkpoint conflict policy, orphan/global row retention, incomplete Evidence/usage/Tool-effect persistence, uncertain acknowledgment after commit and cross-process execution coordination/recovery. Conversation persistence is not a generic Agent checkpoint or exactly-once external-effect mechanism.

Observation Option B remains preferred in principle and unapproved. Four conditions still require a concrete decision: per-invocation correlation (interaction/provider observation), failure of secondary reporting (Inspector/report composition), privacy-safe payload/retention (capture policy), and mandatory-versus-optional evidence admission before actions (trusted Qwen host/WorkCycle acceptance). A new persistence backend is not a prerequisite for optional capture reporting. No callback suppression, timestamp clamping, retry or usage refund was introduced.

## Next bounded comprehensive review

Move to the existing dashboard HTTP-to-operator-disclosure flow: freeze `apps/operator_dashboard/server.py`, `tests/apps/operator_dashboard/test_server.py`, `apps/operator_dashboard/web/src/App.tsx`, `apps/operator_dashboard/web/src/Inspection.tsx` and `apps/operator_dashboard/web/src/App.test.tsx`. Reuse or target `project.py`/`details.py` only with matching prior Evidence/operator review and maintenance identities. Trace endpoint/root/path admission, record disclosure, errors, cache/freshness and the browser's completion/validation/publication claims. Verify real local request/projection boundaries and frontend tests without live models or mutation endpoints.

These paths are a next-task recommendation, not a newly executed or frozen audit here. Remaining Qwen/application cohesion, developer/scientific tooling and cross-cutting consolidation follow the canonical inventory. RI original fixtures 93/93 and experimental paths 606/606 retain their defined completion; 188 historical exact versions remain separate in seven families, with no new credit. A+C remains unapproved. No next cohort or successor dossier was started.

`repair:persistence-sqlite:233b170e:20261026`.
