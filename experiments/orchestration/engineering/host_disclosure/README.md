# Host-disclosed semantic primaries

This bounded experiment-owned external Codex Agent adapter receives the complete
authorized packet and frozen instruction text through UTF-8 stdin. Native
`--output-schema` constrains its judgment response; `--output-last-message` is
captured separately and must equal the sole completed assistant message in the
JSONL transport. Process exit, transport, payload/schema validity, exact evidence
resolution and scientific artifact authentication are separate requirements.

The model judges content only. It uses no shell, filesystem, web, plugins, apps,
builder or persistence capability. Its empty disposable CWD contains no scientific
data and must remain unchanged. Fresh authentication-only CODEX_HOME, ephemeral
sessions, ignored user configuration/rules and deny-by-default Windows MXC
permissions retain isolation. Disabled tools and rejected tool attempts enforce
the supported runtime scope; host routing is not independently verified.

## Exact evidence representation

The two maintained packet shapes assign each disclosed source an opaque key:
SHA-256 of canonical JSON `[contract, case, frame, canonical source identity]`.
Keys are packet-local, content/identity-derived and independent of source order or
ranking. The model sees the key, original address and complete unchanged content;
the host retains the canonical document/content identities. This is a bounded
codec for blind-primary reviews, not a framework identity or localization resolver.

A cell names `source_key`. Evidence in cells and gold unit alternatives is
`{source_key, quote, occurrence}`. The quote is an exact nonempty Unicode string.
Occurrence is a positive 1-based integer among exact substring matches searched
left-to-right **including overlaps**, advancing one Python Unicode code point
after each match. No normalization, case folding, whitespace repair, fuzzy search
or contextual disambiguation occurs. For `aa` in `aaa`, occurrences 1 and 2 start
at code-point indices 0 and 1. Unpaired surrogates are rejected.

The host authenticates the disclosed key, selects exactly that occurrence, derives
`start` and exclusive `end` in the existing Unicode-character convention, verifies
`source_text[start:end] == quote`, and emits the original canonical identity and
span. Foreign keys, empty/absent quotes, missing locators, invalid occurrences and
model-authored offsets fail. This is deterministic representation projection,
never response repair. The host does not change a quote, occurrence, source,
judgment label, unit or alternative. Semantic correctness remains the model's
responsibility. The existing scientific builders still enforce completeness,
own-source evidence, usefulness, units, alternatives, gaps and witnesses.

The host serializes the canonical review and invokes the frozen standalone
builder/validator. Only authenticated artifacts become scientific authority.
Original packet/instruction bytes and their digests remain invocation provenance;
the retained stdin captures the exact projected disclosure. Model output is never
an artifact merely because the process exited successfully.

## Engineering gate

Two fresh synthetic GPT-6 Luna / Medium invocations must exercise the actual
direct C caller and nested B grounding caller of `semantic.primary`. Both require
zero tools, unchanged empty CWD, sentinel absence from input/transcript/response,
exact locator projection and complete host-built authenticated artifacts. Failed
captures are preserved without repair or retry. A successful smoke receipt binds
OS/runtime, CLI version, exact runtime/adapter/locator/schema/builder bytes and
permissions. Real-case semantic entry requires that compatible receipt; help or
version output alone is insufficient. Sandbox and transport behavior are assumed
CLI/runtime properties independent of model family; semantic quality is not.

These smokes are engineering evidence only, never gold, treatment evidence,
execution approval or permission to retry an entered scientific operation.

## Operational failure isolation

Progress uses append-only `operational-progress.jsonl` and optional best-effort
snapshots. Readers never hold the atomic replacement target used by the former
Windows progress channel. Reader/writer/observer exceptions are contained and
malformed telemetry is unavailable. Scientific journals and captures remain
independent and fail hard. Missing progress cannot imply scientific success.
Permanent tests exercise actual WinError 5 sharing contention, 5,000 updates and
observer exceptions. No arbitrary sleep is used as a sharing-lock correction.

Default stderr events are compact `HH:MM:SS +MM:SS case operation status`, with
duration, model/reasoning, PID and useful heartbeat counters where applicable.
Full commands, paths, identities and retained streams remain available on failure,
`--verbose-events` and status/debug surfaces. Heartbeats every 15 seconds establish
supervisor observation, not useful model progress or success. Final JSON remains
stdout. Read-only `status --follow` retains Ctrl-C detach-only behavior.
