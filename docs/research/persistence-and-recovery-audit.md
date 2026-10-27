# Persistence and recovery comprehensive audit

The complete maintained Persistence cohort received full source, test and package-contract review on **`206d58e271014e08cda8d18774b5fc86f406bf84`**, tree `28d902f698c42a66b240f63de32e5486d8913e91`. This is an audit checkpoint, not a production correction or whole-lifecycle signoff. Three independently reproduced P2 families remain awaiting separately authorized implementation. No P0/P1 was demonstrated within this cohort.

## Baseline, authority and exact review

Local HEAD/main/origin-main and independent remote observation agreed before review. Tracked tree/index were clean, no Checkout owner existed, and all thirteen original forensic hashes matched. All 814 retained physical production-profile inputs matched the preceding delivered repair. PRs #34–36 and both Codex corrections remain integrated. The retained protected result is **3,197 passed, two opt-in live skips, 100% configured branch coverage**, production `c39c1f0f61350ca57795dc06c8b97730918a0d99`; this documentation-only audit did not rerun that gate.

Authority remains AGENTS, the architecture taxonomy/documentation map, source/tests, accepted ADR-0001 and canonical backlog. Persistence stores representations owned by Conversation; it does not acquire Run, Memory, Evidence, workflow or publication authority. The [overall audit](comprehensive-code-audit.md) and [evidence conventions](code-audit/README.md) distinguish full bodies, targeted dependencies, test execution and historical obligations.

The [frozen cohort](code-audit/persistence-recovery-cohort.json) records all eleven exact paths/blobs and physical hashes before substantive review. No additional maintained paths were found under the two Persistence roots. The [assurance ledger](code-audit/persistence-recovery-assurance.json) records full per-file and per-function depth, failure branches, independent oracles and targeted consumers. There are **eight Python paths, three package documents and 1,397 lines**, with no remaining selected body. Known defects prevent a correctness-clearance claim despite completed review.

| Exact reviewed path | Full review and assurance conclusion |
| --- | --- |
| `src/devtools/persistence/__init__.py` | Seven canonical exports; imports do not open a database or expose predecessor runtime aliases. |
| `src/devtools/persistence/_snapshot.py` | All immutable snapshot constructors, capture, duplicate-ID checks and restoration. Explicit caller coordination; new restored object/lock and repeated-message alias reuse. |
| `src/devtools/persistence/errors.py` | Complete domain hierarchy. Version is a Format subtype; raw SQLite operational errors are not universally normalized. |
| `src/devtools/persistence/json.py` | Complete strict v1 encoding/decoding, shape/version/value checks, duplicate keys/sources, conflict paths and deterministic ordering. Pure text conversion. |
| `src/devtools/persistence/sqlite.py` | All connection, schema, transaction, write/read, conflict, position, missing-row and cleanup paths. Three confirmed P2 families below. |
| `tests/persistence/__init__.py` | Package discovery/docstring marker; no independent imports, setup or behavior. Its role, not its size, justifies disposition. |
| `tests/persistence/test_json.py` | All factories, six test bodies, parameter cases, assertions and async helper. Twenty-two cases; encoder-derived schema fixtures have an oracle limitation. |
| `tests/persistence/test_sqlite.py` | All factories, fake-interaction methods and eleven complete tests, using actual temporary SQLite files. Missing concurrency/initialization/storage-class negatives identified independently. |
| `src/devtools/persistence/docs/overview.md` | Full Conversation-state/ownership/fresh-coordination and historical schema-name contract. |
| `src/devtools/persistence/docs/json.md` | Full pure-conversion contract; callers own Resource file I/O. |
| `src/devtools/persistence/docs/sqlite.md` | Full atomic-save replacement contract; no automatic turn lock, cross-process execution lock or exactly-once claim. |

## Snapshot semantics and JSON compatibility

`capture_conversation` snapshots immutable messages from the current History, then current source-keyed refs. It reuses safe immutable identity/time/source values rather than aliasing mutable lists. Conflicting values under one MessageId refuse; identical repeated occurrences remain ordered and reconstruct to one shared immutable message object. Refs sort by source. Conversation IDs/timestamps survive reconstruction, while Python object equality and locks remain local to each reconstructed entity. A snapshot's ID is the Conversation ID, not a version token or operation ID.

Capture is synchronous, with no internal await or automatic lock acquisition. Its documented precondition is cooperative `conversation.turn()` coordination when Runtime is active. Direct mutators and different reconstructed objects/processes do not share that lock. An uncoordinated checkpoint during an awaiting model call contains the retained input and old ref; a participating checkpoint waits and captures the completed turn. This is a supported caller boundary, not a newly imposed global atomic-snapshot guarantee.

JSON uses schema version 1, the historical `session` field, ordered `history` and source-keyed `conversations`. Exact field sets, actual integer version (not bool/float), decoded duplicate keys, nonstandard constants, typed values, message conflicts and duplicate ref sources are checked. Timestamps normalize through Core Timestamp; content whitespace, valid Unicode, roles, insertion order and semantic IDs are preserved. Independent literal JSON establishes offset-to-UTC microsecond conversion and the public schema without using the encoder as the oracle. Encoding is deterministic, source-sorted, non-ASCII-preserving text with a trailing newline.

The package does not read or atomically write JSON files. Successful encoding is not a durable save. Resource write/read composition, path authority, fsync and file custody remain separate. No universal size/depth or power-loss guarantee is declared. On this CPython 3.14 host, a 1,500-level array is parsed then correctly refused as an unsupported root; this does not establish a portable recursion policy. The initial probe expectation of RecursionError was disproved and is not a product finding.

## SQLite transactions, conflicts and storage ownership

Each save/load owns a short-lived connection. Admission enables foreign keys and initializes or validates user_version 1, four required tables and required column names. Parameters bind data values. Properly created tables have immutable global message IDs, ordered per-Conversation occurrences, unique source refs and FK/check constraints. Validation of an existing tagged database checks table/column presence, not every constraint, index, collation or storage class. It is not authentication of an arbitrary externally modified database.

Save captures before connection entry; its replacement transaction preserves Conversation creation time, validates/reuses global immutable message rows, deletes/reinserts current History links and refs, then commits. Conflicting immutable values and an independently injected trigger failure roll back the entire candidate. Unknown bytes are not deleted to repair storage. Ordinary save/load finally paths close their connections, and schema-admission failure closes its owned connection.

The observed configuration is CPython **3.14.3**, SQLite **3.50.4**, Windows 11; normal connections use **DELETE journal, synchronous=2, foreign_keys=1, busy_timeout=5000ms, LEGACY transaction control (-1)**. The read-coherence probe explicitly switches its temporary database to WAL to permit a deterministic concurrent commit. Two concurrent default-journal writers preserve a complete current snapshot. Lock-contention controls shorten only the test connection timeout to 10ms, observe OperationalError without replacing the old snapshot, and succeed after release. They do not certify a new production timeout policy.

Repeated save intentionally replaces the current snapshot, including shrinking History. There is no CAS/version token, automatic merge or stale-writer refusal; a stale object can overwrite a later checkpoint. Unreferenced global message rows remain after replacement because other Conversations may share them; replacement is not secure erasure or a retention/GC policy. These limitations need host/retention decisions under B-0028, not an unrequested transaction engine.

## Confirmed P2 findings and bounded acceptance

### P2: one load mixes separately committed snapshots

Proposal **`3e07840c-7021-4395-939e-b75a47c5374e`**, owner `sqlite.py:SqliteConversationStore.load` and its read helpers.

Two real connections and barriers pause a reader after fetching History A, before reading refs. A legitimate public `save` commits B/thread-B. `load` returns **History A/thread-B** while the final DB correctly contains B/thread-B. The reader reports no active transaction across these SELECTs. The returned pair never existed in either committed snapshot.

The required guarantee is narrow: one reconstructed current-snapshot Conversation should correspond to one committed state. It is not a demand for a cross-process Agent transaction, a single snapshot across multiple independent loads or immunity to later filesystem mutation. A bounded repair should establish a consistent read boundary across the existing queries, with deterministic WAL/default-journal and cleanup/failure controls. Preserve save semantics, schema names and normal lock behavior.

### P2: failed initialization leaves a self-created partial schema

Proposal **`77a31939-9c99-4a60-9016-622843cc10f3`**, owner `_ensure_schema`.

A standard SQLite authorizer deterministically denies the second CREATE TABLE. The real first `sessions` table remains installed with **user_version=0**, although initialization raises DatabaseError and closes the connection. Ordinary retry then raises **PersistenceFormatError** for the nonempty v0 database. `with connection` does not make the DDL executescript transactional without an appropriate explicit boundary.

The narrow correction is atomic installation of the new tables/indexes/version, with intermediate failure rollback and clean retry. Preserve conservative refusal for unrelated or preexisting unknown partial databases; do not delete/reinitialize them automatically. This probe models a genuine statement failure and observes actual committed schema effects. It does not simulate disk power loss or authorize a new recovery service.

### P2: persisted non-text values bypass semantic admission

Proposal **`794a4df3-e51e-4927-8f43-c7dd3cb6535c`**, owners `_load_messages` and `_load_conversations`.

Actual updates to a valid store-created v1 database place a BLOB in each of `messages.content`, `messages.source`, `conversations.source` and `conversations.value`. SQLite TEXT affinity permits these values. Public load returns bytes-valued runtime content/source/ref fields rather than PersistenceFormatError. The frozen dataclasses trust typed values; `.strip()` also works on bytes, so those wrappers do not establish external representation validity. A deterministic Runtime consumer actually forwards a bytes-valued continuation to its fake interaction. No live provider is invoked.

Validate semantic text at the storage decoding boundary before constructing the existing values. Refuse unsupported storage classes with controlled Format errors; do not guess encodings or coerce bytes into strings. Cover all four columns plus legitimate Unicode, empty content, timestamps/IDs/roles, duplicate occurrences and actual Runtime restoration. A global model/Conversation validation redesign is unnecessary for this bounded correction.

No existing bounded SQLite proposal was found during canonical duplicate checking. B-0027/B-0028 own broader representation/durability pressure; these three proposals are independently testable siblings sharing one implementation owner. None approves implementation or closes a parent.

## Actual consumers and restart behavior

Exact import/API searches find no maintained non-test caller of the Conversation JSON helpers or SQLite store. The store is an implemented public capability, not an automatically operating native recovery subsystem. The maintained SQLite test and independent probe construct a Conversation, save/load into a fresh object, call Runtime with its stored ref, receive a replacement, and explicitly save again. Without that last save, a fresh load still returns the old state. Runtime imports neither Persistence nor a save hook.

Native Qwen instead owns PromptMessage history and separate request/response/stage/Tool/validation records. `coding_loop` imports `_save` from `development_task`; that helper composes TextFile and Resource write for app JSON. Those records are not this Conversation schema or normalized Evidence ingestion. WorkCycle/Checkout authority/journals and usage snapshots retain their independent owners. Imports/availability are not actual automatic adoption.

Actual temporary child processes exercise process restart and interruption. A fresh child loads A/thread-A. Exit **71** after candidate writes but before commit recovers A through SQLite; exit **72** after real commit but before normal return recovers B despite no success receipt. The connection hooks schedule failure at the maintained save boundary. These are real process exits with deterministic test injection, not power-loss, hardware failure or arbitrary OS interruption certification. No automatic retry is performed.

Conversation persistence does not retain InteractionAttempt stage, provider entry, ModelInteraction occurrence IDs, usage, Tool calls/results, source mutations, authorization, review or publication receipts. An input-only restored History cannot distinguish never-started from possible external completion. Replaying a prompt can duplicate effects; a late stale save can overwrite newer checkpoint state. Existing B-0034 reconciliation obligations remain separate.

## Evidence and unapproved observation policy

ModelInteractionInspector retains process-local completed Evidence. ExecutionInspector retains attempts/terminal Evidence locally before an optional synchronous EvidenceSink. Sink responsibility is not a specified durable commit/fsync certificate. Neither has a production adapter to this Conversation-only store; callback success does not prove restart survival. Conversation snapshot success does not certify Evidence capture or model nonentry.

Option B remains preferred in principle and **unapproved/unimplemented**. Returning a known response while separately exposing capture failure does not require changing these Conversation backends or creating a new store. A real durable requirement would need an approved domain-owned failure/Evidence representation, occurrence identity, storage/acknowledgment contract and actual consumer. Reusing an existing app journal may be sufficient for a chosen host, but that is an explicit decision, not automatic normalized Evidence adoption.

The four approval requirements remain: invocation correlation at interaction/provider observation; secondary-report failure at Inspector/report composition; privacy-safe payload and retention under capture policy; and mandatory-versus-optional Evidence admission by a trusted host before actions. A host may refuse workflow acceptance while retaining a known response, without retrying, refunding unknown usage or redefining Runtime attempt success. The [decision brief](../development/model-observation-policy-decision-brief.md) receives evidence only.

## Quality, oracle gaps and architecture assessment

The private shared snapshot is cohesive: both formats reuse semantic capture/conflict/restoration, while wire conversion stays format-specific. Core identity/time values and domain ownership are respected. Strict Persistence JSON should not be replaced by the generic Filesystem codec's different model/duplicate/type contract. Repeated field construction alone does not justify an ORM or universal serializer. Most save/load/error paths are small and testable.

The main deficiencies are misplaced trust at SQLite admission and transaction scopes that differ from the intended logical unit. Narrow owner-local text validation and explicit existing SQLite transaction boundaries are preferable to modifying global values or adding infrastructure. No reusable abstraction or durable schema change is approved here.

Existing tests use actual temporary databases and independent row-count/ref assertions, meaningful rollback/conflict checks and deterministic values. However, most JSON negative fixtures start from the encoder, and the primary round trip couples both sides of the schema. The audit adds a literal schema oracle. SQL tests omitted read interleaving, interrupted first DDL, malformed storage classes, busy behavior and before/after-commit process loss. A passing production coverage gate does not establish these contracts.

Raw SQLite corruption/locking/connection errors remain sqlite3 errors; semantic/schema failures use Persistence exceptions. Package documentation does not promise universal I/O normalization. Parser/file resource caps, full schema/constraint authentication, retention/GC, cross-runtime/SQLite/filesystem compatibility and power-loss durability remain explicit limitations or future decisions, not speculative new P2s. An initial probe mistakenly relied on connection context managers to close handles, causing Windows temporary cleanup failure; it was corrected with explicit close and excluded from product evidence.

## Validation, canonical reconciliation and finite next scope

Maintained tests: **130 passed, one opt-in live skip**, including all **33 Persistence cases**; targeted Evidence/usage/Tool/Qwen consumers: **129 passed**. Final independent set: **33 cases, seven desired-contract violations in three P2 families, 26 agreeing controls/qualified limitations, zero harness errors or unexpected controls**. Commands, UTC timestamps, durations, exit codes, physical input hashes, SQLite configuration and full authored reproducer are in the [probe record](code-audit/persistence-recovery-probes.json) and assurance ledger. No source/test/configuration change or full protected run is part of this audit.

Three canonical pending proposals are captured through Intake, without B-numbers, reviews, approvals, grants or implementation authority. Existing proposal histories and delivered repairs remain unchanged. B-0027/B-0028/B-0011/B-0034 receive append-only findings; no status, maturity, dependency or parent closure changes. The [checkpoint](code-audit/persistence-recovery-checkpoint.json) records identity/JSON/links/layout/Intake/whitespace checks and original forensic/RI custody. Publication follows ordinary branch/PR requirements; accepted main must be independently observed before claiming integration.

**Exact next bounded assignment:** separately authorize these three SQLite corrections in `src/devtools/persistence/sqlite.py`, existing `tests/persistence/test_sqlite.py`, and directly necessary documentation/maintenance overlays. Require independent pre-fix regressions, coherent-read/default/WAL controls, initialization rollback/retry/refusal, malformed-field and Runtime restoration tests, plus supported static checks and the unchanged full protected gate on committed executable inputs. Keep the three contracts separately reviewable; do not migrate schema, add a backend or implement observation policy.

After that increment, move to remaining application/Qwen/dashboard consumer surfaces and developer/scientific infrastructure using the existing domain inventory, followed by cross-cutting reconciliation. Remaining Tools/Core/Resources/dependency surfaces must retain their actual review depths rather than inheriting closure from related repairs. Full lifecycle correlation, privacy/retention, validated-input closure, application cohesion and unapproved decisions remain actionable backlog work. RI original fixtures **93/93** and experimental paths **606/606** stay complete at their defined depth; **188 exact historical versions** remain a separate seven-family assurance program, with **no new credit** here. A+C remains unapproved. No next cohort or successor dossier begins in this assignment.

`audit:persistence-recovery:206d58e2:20261026`.

## Delivered maintenance overlay

The three independently reproduced P2 families are implemented through normal PR38, production `233b170eba86a596ff622cc0bd8ac5e170d2e6ca`, verified main `c6ca6a2f64d729a8192cde1109e68b4a1830c7d2`. Original eleven-path bodies/probes remain historical evidence; three changed versions are separately overlaid. [Delivered correction](../development/persistence-sqlite-contract-repair.md); [exact validation](code-audit/persistence-sqlite-repair-20261026.json). Broader recovery/retention/Evidence/consumer obligations and unapproved observation policy remain unchanged. `repair:persistence-sqlite:233b170e:20261026`.
