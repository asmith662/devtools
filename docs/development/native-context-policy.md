# Native coding Context operating policy

Operational follow-up: a [separately approved bounded trial](../research/qwen64-qualification-trial.md)
verified 64K allocation and actual 49,152-/62,464-token inference. It restored the
original 32K service. Qualification evidence does not itself authorize persistent
adoption or permit reporting 64K capacity while the actual provider remains at 32K.
The tested output ceiling was 128; larger generation budgets retain their own
acceptance requirements. No native task/grant or implementation changed.

## Ownership and implemented capability

This increment starts from synchronized main
`41303319c93c8dc1605207a171dc3ea551b1c2a6`. Agents still owns coding request
assembly and active presentation; Context owns indexed source representations
and exact materialization; Tools owns scoped operations; native WorkCycle owns
approved assignments, bounded capture and custody. ModelInteraction and serving
remain separate. There is no new Context history, parser, tokenizer, strategy
registry, scheduler or coding loop.

| Capability | Existing implementation | Native integration now |
| --- | --- | --- |
| Complete authorized inventory | `navigation.complete_inventory` | Every profile; metadata gives no source credit |
| Aggregate source admission and range recovery | Repository host plus Context materialization | Every profile; complete next-request accounting |
| Deterministic evidence-preserving reduction | `ProjectionPolicy` | Automatic in an explicitly approved `native-context-v1` profile |
| Structured semantic summary | `SummaryCompaction`, host `request_compaction()` | Existing explicit framework configuration; no native auxiliary grant added |
| Adaptive hybrid summary selection | `AdaptiveCompaction` | Existing opt-in framework configuration; native integration deferred |
| Anchored instructions/recent exchange | Protected instructions, native exchange boundaries | Reducer preserves these; no arbitrary head/tail eviction mode |
| Precise source navigation | `find_source`, `read_source_unit`, `SourceSearchIndex` | Advertised in the new profile; legacy three-Tool schema unchanged |
| Task-directed candidate presentation | `NavigationPolicy`, `TASK_FIND` | Framework opt-in; not silently added to this profile |
| Current source continuity | Projection source-status annotation, exact active disclosures | Enabled with the new profile |
| Provider token measurement | llama.cpp `count_input_tokens` | Explicit host injection and capacity qualification before dispatch |
| Context pressure | New coding `ContextPressure` facts | Existing native bounded observation writer |
| Model compaction request | Host-only semantic request seam | No native Tool; an invented request is refused, not self-authorized |
| Inspection coverage | Existing index, original calls/results, disclosures, projection provenance | Derivable task-local facts; no semantic assessment ledger added |

The B-0049 worker was offered `read_source`, `replace_source` and
`validate_candidate`. The precise navigation Tools existed but were not in that
assignment's advertised schema. Its broad read choices do not establish its
internal motivation. B-0049's task, failed episode and consumed slot remain frozen.

## Explicit prospective profile

Existing native packets without `context` retain their exact three Tool
definitions and 32,768-byte request/read/edit ceilings. Their approvals are not
upgraded. A new packet may include the following exact versioned subrecord,
validated by `NativeContext` under the existing native packet owner:

```json
{
  "schema": "native-context-v1",
  "context_tokens": 65536,
  "input_tokens": 62464,
  "reserved_output_tokens": 2048,
  "disclosure_bytes": 65536,
  "warning_bytes": 98304,
  "trigger_bytes": 114688,
  "target_bytes": 98304
}
```

For this example set the existing `budgets.prompt_bytes` to 131,072 and
`settings.maximum_output_tokens` to at most 2,048. All values remain part of the
exact assignment/task hash and require a new explicit host approval. Old
closed-field readers reject unfamiliar packets rather than granting broader
authority. Historical native assignment/result/review records and legacy Qwen
contracts retain their meaning.

The supported prospective ceiling is 128 KiB for a complete neutral serialized
request, with configurable smaller ceilings including 96 KiB. This is independent
of provider input tokens. The example reserves 2,048 generation tokens and 1,024
additional safety tokens within a qualified 65,536-token provider context.
Bytes never estimate token usage. `disclosure_bytes` bounds exact source payload
per acquisition; its metadata, escaping, pending replies, inventory and Tool
schemas still count against the complete request. The unchanged `source_bytes`
budget bounds baseline/resulting editable source and proposals at 32 KiB. Native
SourceScope independently admits resources up to 128 KiB. Larger read capacity
does not permit larger edits.

A provider qualified for 32K can use a separately approved 32K-token reservation
with the same larger byte ceiling when measured requests fit. The
[frozen-envelope measurement](../research/native-context-capacity.md) demonstrates
69,214 bytes and 17,023 actual input tokens on the restored server. The larger
byte profile is useful independently of completing the 64K operational target.

The existing capture budget remains explicit and finite (at most 1 MiB), includes
all new observations and refuses exhaustion without truncation or replay. This
profile adds no summary model, historical payload store or unbounded capture.
Operators must budget retained requests/responses within it; selecting the largest
request ceiling does not guarantee eight fully populated captured calls fit.

`cycle.native.execute(..., profile=<approved identity>,
provider_context_tokens=<observed qualified capacity>,
measure_input=interaction.count_input_tokens, ...)` binds the trusted provider
qualification and existing tokenizer adapter. It refuses missing/inadequate
qualification before claiming dispatch. The profile string must still match the
approved worker. The trusted host must verify the running provider identity and
capacity; passing an integer is not hardware attestation. No backend discovery or
provider-specific loader was added.

Each token measurement has authorization/current-input checks before and after
entry, an intent and a returned-count observation. The coding host rechecks exact
source and unchanged history after awaiting measurement. Invalid/over-limit
counts, transport failures or changed inputs prevent acting-model entry. No
tokenizer or inference request is automatically repeated. Measurements occur
within the existing finite coding wall envelope, at most once per preparation.

## Automatic projection and pressure

The prospective profile always constructs the existing deterministic
`ProjectionPolicy(trigger_bytes, target_bytes,
metadata_operations={"find_source"}, report_source_state=True)`. These are explicit
byte watermarks, not universal optimal settings. The example warns at 96 KiB and
reduces at 112 KiB toward 96 KiB, under a 128 KiB hard ceiling. Aggregate admission
uses the same effect-free projection preview, not a second budget algorithm.

Instructions, permissions, unknown/unacknowledged effects, native call correlation,
current check/repair feedback and mandatory current-source support remain
protected. Native whole-resource information obligations are unchanged: an
opaque readiness callback conservatively protects current source disclosures.
Summaries or metadata cannot satisfy those obligations. A protected minimum that
cannot fit remains an explicit refusal, even when the desired target is missed.

The original execution history and retained exact source results stay intact.
Only the active request and its exact current edit witnesses change. Derived
source-status annotations report active ranges, latest acquisition, omission and
duplicate-range information. They are metadata, not source. Source changes
invalidate prior snapshot correspondence through the existing owner.

`RepositoryCodingHost.context_pressure` and optional synchronous
`observe_context` expose immutable facts: original/final complete request bytes,
ceiling, warning threshold/pressure flag, selected policy, reduction/readiness or
refusal, measured input tokens (or unknown) and separate token reservations.
Observer failure stops entry. Native capture persists `context-pressure`,
`token-measurement-intent`, `token-measurement-returned` and
`context-projection` observations. Projection records include retained original
indices, omitted complete exchanges, shortened indices and active/invalidated
source identities. They use the existing observation boundary for future
Inspector consumption; no UI, event bus or Inspector worktree was changed.

These facts describe measured preparation and deterministic projected results.
They do not predict the next model's unknown Tool choices or its token count.
Warnings are advisory; request/token limits bind. No generated warning message is
inserted into history. A model-facing compaction Tool is deferred: the existing
host request seam requires a separately configured auxiliary interaction and
finite selection/disclosure budgets. Model output cannot create that authority.

## Grounded inspection and escalation

Use `find_source` with an exact authorized file path and `mode="symbol"` to page
functions/classes/methods, including nested/enclosing declarations. With an empty
query the existing generic Tool pages an outline; `offset` requests later pages.
Search with a query/mode across the authorized index. Results are bounded metadata,
with `partial` and `next_offset`; they are not proof that every textual occurrence
was searched or that all languages/declarations are represented. Lexical ranking
is candidate evidence, not engineering sufficiency.

Each returned unit includes resource version, snapshot, unit ID, qualified name,
half-open Unicode offsets, one-based physical lines, byte size, file ID and parent
ID. RI owns declarations; Context owns these file/symbol/physical-line-window
views. `read_source_unit` resolves a current exact ID through the existing source
Tool. `read_source` supports adjacent/smaller explicit half-open Unicode ranges or
a byte-bounded prefix. Bodies/signatures/docstrings are obtainable as exact source
ranges; no dedicated signature/docstring extraction Tool was added. Unicode
offsets, UTF-8 bytes and physical line numbers are distinct.

Indexed locations, queried metadata pages, actually disclosed text, actively
retained source witnesses and explicit actor assessments are different facts.
The existing index plus original calls/results, source disclosure identities and
projection records support a task-local inspection account and supervisor
escalation without another store. Reading or retrieving a region does not prove
it was assessed, understood or relevant. Durable semantic assessments, absence
proofs and cross-task inspection reuse remain separate work. Any account must
retain snapshot/version identity and invalidate applicability after source change.

Native Tools remain a fixed exact approved set for the episode. No phase-dependent
or just-in-time registry was added. Existing navigation reduces the need for broad
reads; this assignment does not establish its live model adoption or usefulness.

## Provider qualification and acceptance evidence

See the [bounded operational assessment](../research/native-context-capacity.md)
for actual hardware, approved trial and restoration. The source profile is usable
with a genuinely qualified provider; this increment does not assert that the
local 64K server passed qualification. It performs no B-0049 redispatch or live
coding inference.

Deterministic regressions exercise exact token/byte separation, profile identity,
provider admission, warning boundaries, projection/history preservation,
impossible minimum, stale source/history, tokenizer/capture failure and invented
compaction requests. The preserved four-read B-0049 source scenario delivers
51,544 exact UTF-8 bytes without duplicate acquisition under the larger ceiling.
The maintained native consumer uses model-selected symbol search, exact unit
read, grounded edit, real failed check, repair, public/private acceptance,
archive/restore and authenticated independent review/integration planning.
Scripted responses prove framework mechanics, not local model competence.

The protected publication policy remains 100% configured production line/branch
coverage. Focused passes and authenticated old coverage do not replace that gate.
Final receipt and executable identities are recorded in the delivery assessment.


Protected delivery: executable `2c0be91335512a3db2600dd0fafb2a690cd59355`,
4,081 passed/two optional skips, 100% configured production line/branch coverage,
one comprehensive execution. [Qualified measurements and final evidence](../research/native-context-capacity.md#protected-delivery)
preserve focused failures, drift and operational qualification limits separately.
