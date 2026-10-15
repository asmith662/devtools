# Observed usage

`devtools.observability.usage` owns normalized historical usage observations and
partial-coverage reports. It composes existing `ModelUsage` and
`InvocationMeasurement`; it does not own model/agent execution, authority,
billing, or a distributed ledger. This is a narrow consumer of existing
measurements, not a general Event/Trace/Telemetry system.

`UsageObservation` contains identity, UTC timestamp, requested model (reported
model separately if known), profile, outcome, attribution and five distinct
provider categories. Missing categories/time remain None / UNKNOWN. No overlapping
total is manufactured. Attribution names project, purpose, experiment, case/stage;
UNKNOWN is explicit. A local session's project is its observed CWD basename,
not a classification inferred from private messages.

Reconciliation matches thread/turn, invocation and provider-response identities.
Disjoint responses are summed then compared with completed-turn totals. Cumulative
local turn snapshots may advance. Duplicate copies count once; conflicts are
marked and excluded. An absent turn matches a thread only when one turn is known.
Long agentic turns may switch model/effort: count one turn with MIXED attribution.
Provider response IDs do not establish underlying HTTP request/retry counts.
ADOPTED dependency use contributes no new consumption; original time/attribution
remain queryable and deduplicate against the executed record.

Reports count observed controlled attempts/active turns. Pre-turn rejection may
have UNKNOWN tokens. In-window response records allocate long-turn consumption;
aggregate-only records use their recorded timestamp. Category sums are known
subtotals with missing counts, not replacement of UNKNOWN with zero. Coverage is
always PARTIAL / OBSERVED LOCAL AND DEVTOOLS / NOT ACCOUNT WIDE.

Windows are half-open UTC intervals. Rolling days are elapsed 24-hour periods.
Calendar weeks use an IANA timezone and configurable weekday start, including DST.
Current/previous week and explicit offset-bearing intervals are supported. No
window rewrites history. Default CLI timezone is America/New_York.

Snapshots use canonical paths/filesystem atomic writes. A single-writer lease
uses exclusive directory creation because filesystem.write supplies no lock.
Contention/stale lease fails closed for explicit operator recovery, with no
background service or automatic reconciliation. Personal ledger/reports remain
ignored under `.local/usage/`, never Git.

The Codex sessions adapter streams past private content without deserializing it.
Only allowlisted usage metadata is decoded; scalar context prefixes stop before
instructions/content. Native exec stdout is filtered to identity/completion
metadata before the existing usage parser runs. Unknown shapes are unsupported.
No prompts, reasoning, final messages or tool arguments are imported.
The CLI imports native exec aggregates only for threads authenticated by a known
Codex session or retained invocation receipt. Native-looking test stdout is not
usage provenance. Unverified native records are counted as unsupported sources,
and an initial provisional import correction is archived locally. Authenticated
history is retained across windows. Arbitrary `.local` session-shaped fixtures
are not a session source.
The local session importer currently requires reported `model_provider=openai`
metadata before private content. Custom or unreported providers are unsupported,
never silently attributed to OpenAI. Provider identity is a runtime report, not
independent verification of underlying host routing.

```text
uv run python scripts/usage.py ingest
uv run python scripts/usage.py report --rolling-days 7
uv run python scripts/usage.py report --calendar-week
uv run python scripts/usage.py report --previous-week
uv run python scripts/usage.py report --experiment RUN_ID --json
uv run python scripts/usage.py report --start 2026-10-01T00:00:00-04:00 --end 2026-10-08T00:00:00-04:00
```

`--refresh` imports metadata first; `--json` emits a versioned machine report.
Forecasts use matching model/effort/profile empirical envelopes and observed
small-input floors. These are low-confidence planning ranges, not a tokenizer,
statistical confidence bound, subscription conversion or price estimate. Public
forecasts bind a private baseline digest; weekly totals/shares remain local.

Pure `devtools.governance.usage` constraints grant no execution authority. None
means UNSET limit or UNKNOWN measurement according to the named field. Unknown
required consumption/forecast blocks a configured dimension. Experiment-local
composition owns reservations, baseline freshness, pre-ENTERED admission and
outcome capture. Those lifecycle responsibilities remain outside observability.
