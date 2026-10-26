# Core Identity/Time audit

## Baseline, scope and disposition

Reviewed integrated `main` at `32c91a17e8df961fc0a834399d8b72c51fbab919`.
Local HEAD and a fresh remote advertisement agreed. Tracked worktree/index were
clean, no Checkout owner existed, and all thirteen retained forensic hashes
matched. Work uses the ordinary branch `audit/core-identity-time-20261026` in the
canonical checkout. No source/test change, model call, scientific replay or new
protected production gate is part of this audit.

All ten exact source/test bodies in the [frozen selection](code-audit/core-identity-time-next-cohort.json)
received complete body review. Every selected Git blob matched before review.
The manifest's original baseline/status/priority remain selection history; its
new review overlay records completion. The three old Core/Resources P2 repairs
were already delivered through PR #23 and are not reopened.

The [per-path assurance](code-audit/core-identity-time-assurance.json) records
exact blobs, inspected functions, depth, findings, actual consumers, tests and
limits. The [independent probes](code-audit/core-identity-time-probes.json) retain
their complete authored source, literal expected/observed results, runtime and
qualifications. This is applicable-depth closure of this cohort, not all Core,
all historical versions, or autonomous-agent effectiveness.

**Result:** one existing P2 factory-input defect is independently reproduced;
no new P0/P1 is demonstrated. Identity, UTC normalization, parsing and monotonic
Stopwatch behavior satisfy their supported contracts in the reviewed controls.
Documentation drift and a concrete documented wall-clock observation limitation
have existing backlog owners. No implementation is authorized by these findings.

## Complete source and fixture review

All paths below are repository-relative. Full blob identities and function lists
are in the assurance record; additional consumer inspection is separately scoped.

| Fully reviewed path | Behavior and independent assurance | Gap/disposition |
| --- | --- | --- |
| `src/devtools/core/identity/models.py` | Runtime UUID guard; retained backing UUID; UUID4 generation; stdlib UUID parsing; canonical text; frozen dataclass equality/hash | Same concrete-class value comparison, not ordering, authority or a cryptographic uniqueness guarantee. Existing typed wrappers remain domain-owned. No primitive defect reproduced. |
| `tests/core/identity/test_models.py` | All four tests: literal UUID/string normalization, version handling, equality/hash and immutability | Version constants expressed as tuple lengths are awkward but correct. Does not independently cover cross-domain wrappers or persistence. |
| `tests/core/identity/test_uuid_invariant.py` | Complete parametrized invalid direct values on base and inherited specialization; valid construction/factories/hash/frozen state | Genuine protection of the delivered UUID constructor invariant. Arbitrary subclass overrides are outside its promise; no need to reimplement it. |
| `src/devtools/core/time/models/timestamp.py` | Aware direct construction, UTC normalization, ISO parsing, string form, arithmetic and nonnegative difference | No monotonicity or native ordering promise. Negative timestamp difference and datetime range overflow preserve explicit/native refusal. |
| `src/devtools/core/time/models/duration.py` | Five factories; timedelta-backed nonnegative invariant; totals/string; arithmetic and operand dispatch | Existing P2: raw negative input can round to zero before validation. Stored value stays nonnegative. Negative-scaling policy requires explicit compatibility qualification. |
| `src/devtools/core/time/models/stopwatch.py` | All initialization/state/context/elapsed/stop branches, monotonic clock and idempotent endpoint | Microsecond storage despite nanosecond clock; no deadline, reset, scheduler, thread-safety or persistent clock promise. |
| `src/devtools/core/time/parsing.py` | All dispatch/normalization/fallback/error branches | Naive/date-to-UTC policy is intentional. ISO acceptance delegates to stdlib; malformed supported text receives TimestampParsingError. Out-of-annotation runtime types are not a new validated protocol. |
| `tests/core/time/test_models.py` | Nine tests: UTC/frozen state, now shape, arithmetic, factories, ordinary negative and invalid operands, positive precision | Missing tiny negative raw values; nonfinite/range/DST/scaling boundaries absent. Ordinary arithmetic tests do not expose quantized negative input. |
| `tests/core/time/test_parsing.py` | Complete helpers, nine format parameters, four invalid strings, date/naive/aware/pass-through, ISO-only and error hierarchy | Meaningful literal UTC expected values. `now` test checks structure rather than controlled delegation; independent probes supplement boundary and consumer evidence. |
| `tests/core/time/test_timing.py` | All three injected-clock tests; running/stopped/idempotence/context exception behavior | Expected elapsed is constructed with the same Duration factory, and 100ns becomes zero. This can conceal conversion mistakes; independent literal 100us/400us probes supply a separate oracle. |

Public initializers for Identity, time and time.models, time errors and the four
current package documentation bodies were also fully read. Other dependencies
received targeted contract inspection only; executing their tests does not award
their entire bodies full-review credit.

## Identity, timestamp and elapsed-time contracts

Identity remains a small standard-library-backed value primitive. Its explicit
UUID guard and inherited `new`/`parse` factories are compatible with current
semantic wrappers. ConversationId, MessageId, InteractionAttemptId,
ModelInteractionId and EvidenceId compare as distinct wrapper types even for the
same UUID. Different wrapper types may share hash values without being equal;
that is valid dictionary behavior, not identity confusion. Parsing retains
standard UUID versions and canonicalizes text; identity alone grants no access
or execution authority.

Timestamp is an absolute UTC value, not a clock ordering guarantee. Direct naive
construction refuses, whereas `from_isoformat` and `parse_timestamp` intentionally
interpret timezone-less representations as UTC. Offset-normalized equality/hash,
microsecond ISO round trips, invalid dates, DST repeated-hour folds and native
range overflow behave as expected. There is no requirement for Python `<` on
Timestamp or Duration objects: existing ordering consumers compare `.value`.

Stopwatch measures elapsed time with `perf_counter_ns`, separately from wall-clock
timestamps. Literal controlled readings establish 100us while running, 400us at
stop, unchanged repeated stop and exactly three clock reads. Context exit stops
without suppressing the original exception. A 100ns interval rounds to zero by
the documented timedelta resolution; zero does not prove no execution occurred.
No Core deadline or scheduler is implemented or required by this audit.

## Existing Duration P2: independently reproduced

Existing proposal: [ea7c18ff-8ca5-46b8-a230-1bfdf92c7f74](../backlog/proposals/ea7c18ff-8ca5-46b8-a230-1bfdf92c7f74/proposal.json).
Current source blob `2ad7166e890795ddbdef968fb3f0b75d80de4ab5` is unchanged from
its original `e02c9044311036883134df955438b1b809db353b` baseline. The original task
and oracle remain in [duration-boundary.json](../../apps/qwen/evaluation/native-cohort-01/duration-boundary.json).

Independent literal expectation, reflecting that task's input-admission contract:
each negative factory input raises ValueError **before** lossy conversion.

| Actual public call | Expected | Observed current result |
| --- | --- | --- |
| `Duration.nanoseconds(-1)` | ValueError | Zero duration |
| `Duration.nanoseconds(-499)` | ValueError | Zero duration |
| `Duration.seconds(-1e-12)` | ValueError | Zero duration |
| `Duration.milliseconds(-1e-9)` | ValueError | Zero duration |
| `Duration.minutes(-1e-12)` | ValueError | Zero duration |
| `Duration.hours(-1e-14)` | ValueError | Zero duration |

Factories build timedelta first; `_validate` sees rounded zero. The invariant of
the **stored value** is not broken. The defect is accepting invalid negative raw
input inconsistently with the established factory task contract and ordinary
negative-input refusal. Positive bounded precision is documented; that does not
resolve the separately recorded negative-input admission obligation.

All five zero controls, positive half-even precision (`1/500/1500/2500ns` becoming
`0/0/2/2us`), literal positive arithmetic, ordinary negative subtraction, NaN,
infinity and divide-by-zero controls behave as specified. This is a P2 API
correctness issue; no negative stored timeout, unbounded execution, authorization
bypass or corruption of already retained values is demonstrated.

Two related probes show `Duration.nanoseconds(1000) * -0.1` and division by `-10`
also round to zero. Those are arithmetic-policy qualifications, not two new bugs
or authority to broaden the factory repair. Existing docs describe nonnegative
represented results and normal timedelta precision; a later repair must decide
explicitly whether to reject raw negative factors/divisors, preserve zero cases,
or retain represented-result semantics. Do not silently alter compatibility.

The historical [local cohort results](../../apps/qwen/evaluation/native-cohort-01/results.json)
show an accepted Duration candidate with original inputs unchanged. That is local
experimental evidence, not a merged source correction. The retained result receipt
also matches its published SHA-256 and explicitly reports `source_restored=True`.
An append-only ADVISORY
updates the existing proposal, retaining `PENDING_REVIEW` and recommending a
separately authorized bounded factory repair. No duplicate proposal, B-number,
approval, grant or implementation was created.

## Real consumers and cross-component ownership

| Actual maintained call path | Evidence and consequence |
| --- | --- |
| `CommandExecutor._run/_collect_output` | Instantiates/stops Stopwatch and supplies `Duration.total_seconds` to asyncio timeout after process creation. Selected real timeout/process tests pass. Core values do not authorize a process or promise spawn-wide/descendant rollback. |
| `WorkCycle.authorize/_execute`; `Delegations.issue/active` | Serialize UTC issue/expiry, compare `.value` with `issued_at <= now < expires_at`, recheck after confirmation, and measure execution separately with Stopwatch. Selected maintained admission/expiry tests pass. Clock trust is host policy, not proof from parsing. No real grant or worker was issued. |
| `Checkout` claim/finalize | Timestamp records custody history; generation identity and fenced transition/journal correspondence govern ownership. An old wall timestamp is not permission to recover or release an owner. PR23 generic Resource repairs and prior Checkout fencing stay delivered. |
| Conversation → JSON → SQLite | Real temporary-store probe retains literal session/message UUIDs and UTC microseconds; malformed persisted identity refuses with PersistenceFormatError. Persistence reconstructs typed IDs and ISO timestamps; it does not redefine them or confer authority. |
| `InteractionAttempt.new/_complete` → terminal Evidence | Controlled clocks exercise actual timestamp/identity producers; `occurred_at` and `observed_at` are retained separately. Entity object identity differs from wrapper/value equality. No whole Runtime audit credit follows. |
| `UsageObservation.to_dict/from_dict`; UsageWindow | UTC time survives serialization and missing original time stays unknown. `[start,end)` excludes end/missing; New York DST calendar week is 167 hours while rolling seven elapsed days are 168. This is deliberate semantic separation. |
| `LlamaCppInteraction.send` → `ModelInteractionObservation` → captured Evidence | Provider observation currently requires ordered wall timestamps; captured duration subtracts those timestamps. The optional observer path is not monotonic Stopwatch timing. See the qualified probe below. |

Controlled backward clock step: a deterministic transport double returns a valid
normalized reply once. With observation enabled, construction of
ModelInteractionObservation raises ValueError before the observer receives a
record. Forward-clock observed and backward-clock unobserved controls return the
reply. There was no live inference or actual provider-side effect.

This is a concrete manifestation of [ADR-0001's documented limitation](../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md):
observer-related failure can surface after a normalized response exists, and
caller-visible failure is not proof provider entry failed. Timestamp does not
promise monotonic wall time. Existing B-0011/ADR-0001 consumer pressure is sufficient;
the report appends evidence there rather than inventing a new clock framework or
automatically suppressing observer failure. The later model/Evidence review must
consider wall-step handling, elapsed measurement and response/observation outcome
separation with explicit semantics. Do not retry ambiguously completed work.

## Cohesion and documentation findings

The package boundaries are appropriate: Identity owns opaque UUID mechanics;
semantic wrappers live in their domains; time owns UTC/span/elapsed values;
Commands, WorkCycle, persistence and Evidence own policy and representation.
No higher-domain dependency or competing foundational parser is required.

There are two small intentional representation entry points, not competing UTC
policies: `Timestamp.from_isoformat` is ISO-only and the broader parser supports
dates/fallbacks. Both normalize to UTC. A generic registry, clock service, temporal
engine, deadline type or scope framework would exceed demonstrated need.

Current Identity overview has contradictory legacy Limitations wording: it says
direct runtime construction has no guard and typed semantic IDs do not exist,
although its Construction section and current source show both. Existing B-0006
owns the documentation correction. This audit records the discrepancy without
changing the package API/docs or treating stale wording as a new architecture.

Tests are generally focused and deterministic. Literal Identity/parser oracles
are strong; Duration tiny-negative boundaries and Stopwatch numeric-oracle
independence need improvement in a separately authorized regression increment.
Injected module clocks are sufficient for these tests; absence of a generic
Clock interface is not a defect. Finite datetime/timedelta ranges, nonfinite
conversion errors, process-local monotonic state and microsecond precision remain
qualified limits rather than promises of universal time arithmetic.

## Validation, remaining work and publication scope

Executed on Python 3.14.3/Windows, with runtime details retained in the probes:

- `uv run pytest --no-cov tests/core/identity tests/core/time -q`: **49 passed**,
  0.08s, exit 0.
- Ten selected consumer modules covering JSON/SQLite, Runtime/attempts, terminal
  Evidence, usage, Commands, WorkCycle/delegation and Checkout: **200 passed**,
  268.54s, exit 0. These executions do not grant their whole bodies review credit.
- **48 bounded independent cases**: six original factory failures reproduced,
  two explicitly qualified arithmetic boundaries, all remaining controls and the
  documented observation-limitation case behaved as recorded; no unexpected
  harness/control failures. Full source and outcomes are retained, not just a
  passing aggregate.

Initial sandbox access to the uv cache and remote Git required approved
escalation; the actual reruns above succeeded. Neither access/setup errors nor
missing guessed paths during navigation were counted as product failures.
The full protected gate was intentionally not run: no maintained executable input
changed. The prior 2,962/2-skip/100% result remains historical production evidence,
not a fresh audit result or architecture proof.

Documentation checks pass for exact selected/dependency blobs, JSON/JSONL,
all 56 Intake chains, 563 local links, layout, whitespace, thirteen preserved
forensics and no executable diff. The structured checkpoint records those checks.
Normal ordinary-branch publication confers no WorkCycle grant or implementation
authority; PR status must be reported as actually observed, not presumed merged.

**Recommended next bounded implementation:** separately authorize the existing
Duration factory-input correction with independently literal regressions,
unchanged positive rounding/API behavior, explicit arithmetic-policy treatment
and the final-tree protected gate. Do not adopt an old Qwen patch automatically.
**Next domain audit:** remaining filesystem codecs/structured models, including
the existing CSV spelling proposal and B-0048 Python-version compatibility; then
ModelInteraction/serving, Agents/Runtime, Persistence, applications and tooling.
No next cohort was launched here.

RI's original fixture review stays 93/93 (augmented 94/94), historical experimental
source stays 606/606 at defined depth, and 188 historical-version obligations stay
open in their seven responsibility families. A+C remains unapproved. This audit
does not prepare the successor-session dossier or complete the repository audit.
