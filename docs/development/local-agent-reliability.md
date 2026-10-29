# Source-read recovery and structured summaries

## Ownership decision

The reliability increment follows Adaptive-0001's retained failures; it does
not change adaptive thresholds. `tools.source` owns literal source-read
admission and a typed range refusal. Context still owns the validated
`SourceRangeDisclosureOption`, Unicode ranges and materialization. RI owns
repository, snapshot and content identities. The coding host projects a
Tool-defined refusal into feedback under the original native call ID. It does
not catch arbitrary execution exceptions or retry a request.

The existing provider-settings seam carries explicitly selected llama.cpp JSON
mode. The semantic compactor forwards a host-selected `ProviderRequestSettings`
without depending on a provider. Strict JSON, record membership and source
provenance validation remain separate from constrained generation. Neither
schema validity nor a citation proves that a generated causal claim is true.

These are extensions of existing Tools, Agents and ModelInteraction owners,
not new execution, Context or history abstractions. Qwen's legacy native
presentation remains an adapter; its range decision should reuse the shared
source operation while preserving its established result shape.

## Literal requests and known refusals

`SourceReadRequest` contains a selected existing RI source unit, literal start/end
and a host byte ceiling. It is not a Context witness. `ScopedSourceTool` first
checks repository, snapshot, resource, byte authority and currentness. Its
effect-free `select_source_read` then constructs the existing Context option or
returns `SourceReadRefusal`. Only range-construction failure is converted;
materialization exceptions are not caught. A normal refusal acknowledges the
Tool result but explicitly says source disclosure never entered. It consumes
the action budget and preserves the original native call ID. The model may
select another call; the framework never retries it.

The neutral `read_source` operation accepts an omitted `end` for the remainder
of the selected source, bounded by existing UTF-8 disclosure limits. An explicit
invalid interval is never clamped. Feedback supplies observed source length,
valid range, maximum disclosure bytes, actual span, continuation offset,
remaining interval and existing snapshot/content identity. Coordinates are
half-open decoded Unicode character offsets, not bytes or physical line numbers.
CRLF occupies two decoded positions. UTF-8 truncation never splits a character.
Empty files retain the existing empty-range rule. Bounds describe the observed
version; later calls still recheck currentness.

Rejected calls add no disclosure or edit witness. Host policy, editable paths,
fixed checks and source custody are unchanged. Unknown errors after possible
Tool entry retain unknown acknowledgment. Qwen keeps its task hashes, required
version arguments, journals and native JSON shape, while its range decision
delegates to `select_source_read`. Its separate continuation policy is unchanged.

## Deliberate structured generation

`SummaryCompaction.provider_settings` forwards the existing model-neutral
`ProviderRequestSettings` value to the auxiliary request only. The host can
select `LlamaCppRequestSettings(response_format="json_object")`. This emits
the documented `response_format` object on the existing provider request path;
the same payload builder remains authoritative for token measurement. Default
requests do not acquire this setting. The acting request is independently
configured. No new provider, hidden call or JSON repair exists.

The installed b10868 release resolves to
`304665fe7ac957df95e3ff8c8c4ffdf92dd6ffa3`; its
[server contract](https://github.com/ggml-org/llama.cpp/blob/304665fe7ac957df95e3ff8c8c4ffdf92dd6ffa3/tools/server/README.md)
documents JSON-constrained output. We select plain JSON-object generation and
retain the existing exact application-schema validation. This does not claim
portable JSON-schema enforcement by every provider or support for every
structured-output/native-Tool combination.

The one fresh live response still returned fenced JSON with that setting. This
is a measured interoperability limitation; the server/template root cause is
not established. After that frozen attempt, the authorized narrow alternative
was implemented: `SummaryCompaction(allow_json_fence=True)`. It accepts plain JSON
or exactly one lowercase `json` fence with LF/CRLF delimiters and ASCII outer
whitespace. Other tags, surrounding prose, nested/multiple fences, malformed or
multiple JSON documents and trailing data fail. It never repairs JSON or calls
a model. The ordinary raw-output byte and termination checks occur first; the
complete inner document then passes the unchanged schema/provenance validator.
`SummaryAttempt.normalized_json_fence` records normalization separately from
validation and adoption. Raw response content/digest remain original. The default
is strict JSON. The frozen live attempt used that default and was not replayed;
offline admission of its retained response is separate evidence.

Raw returned text remains unchanged. Termination, output size, exact record
digests, replacement coverage and source references still pass the existing
semantic-compaction checks. Failed format or provenance checks still use the
valid deterministic fallback without another auxiliary call. Exact current
source is the only edit witness; summary citations never confer that authority.

A maintained counterexample intentionally cites a real record while attributing
an unsupported cause. Membership validation cannot establish entailment. Such a
note remains marked untrusted and cannot certify checks, effects or completion.
Independent semantic assessment is required for claims of summary fidelity.

## Verification scope

The neutral host's existing authorization callback now receives the literal
`SourceReadRequest`, before range selection, so it can authorize scope without
confusing input construction with successful disclosure. Construction is not
authority or evidence. Direct callers of the existing Context disclosure option
remain compatible. The Qwen adapter retains its public input/result presentation
and delegates the range decision; its legacy continuation policy is unchanged.

See the separately frozen [live verification](../../experiments/local_agent_reliability/REPORT.md).
Its summary format, adoption, actual consumption, source usability and candidate
correctness are independent outcomes. No Adaptive-0001 result is revised and no
adaptive threshold is retuned. Durable recovery, observation Option B and broader
Context policy remain outside this increment.

## Committed implementation validation

Implementation `9593d8f541a3cf58478f77052accb80b5a99e681`, tree
`9bd9e523bd1987388b7cdb3fef62953ea7fafe96`, passed the unchanged protected
development gate: **3,821 passed, two optional skips**, with all 13,851 configured
production statements and 3,536 branches covered. The gate ran from
2026-10-29 13:14:34 to 13:36:55 UTC (1,340.008 seconds including capture).
Ruff, supported formatting, strict mypy and layout passed on that same committed
implementation. All 1,057 captured physical validation inputs remained unchanged.
These results use Windows/Python 3.14.3; no additional-runtime claim is made.

The [machine-readable receipt](../research/code-audit/local-agent-reliability-20261029.json)
retains original/final blobs, commands, versions, timings, input hashes, earlier
test corrections and two deliberately interrupted gate attempts. Neither
interrupted attempt is counted as a pass. Independent evidence verification
checked the five actual acting requests, six correlated source reads, unchanged
freeze, restoration, strict summary rejection and separately qualified offline
normalization without inference or effect replay. Documentation-only delivery
records preserve the tested executable inputs through publication.
