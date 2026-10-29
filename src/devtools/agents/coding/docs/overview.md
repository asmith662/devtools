# Bounded coding Agent

The Agents coding package coordinates one host-bounded source/edit/check/repair
objective. It depends on ModelInteraction, native Prompt, existing Agents
model/Tool composition, ToolRunner, RI/Context, scoped source/fixed checks and
managed Resources. Runtime and Conversation retain their narrower contracts.

- `process.run_coding_agent` owns the finite model/proposal phase sequence,
  response-source and native ID checks, continuation and terminal reconciliation.
- `models` owns coding-specific limits and factual candidate/terminal outcomes.
- `repository.RepositoryCodingHost` composes real repository Context acquisition,
  exact current edit admission, fixed validation and feedback. Hosts explicitly
  supply authorization and application/archive/restoration collaborators.
- `projection` selects valid complete native exchanges and affordable exact source
  through existing Context materialization. The neutral host's optional
  `ProjectionPolicy` separates retained original facts from active Prompt/edit
  witnesses; default task and capacity behavior remain unchanged.
- `compaction` optionally obtains bounded, cited working-state notes through a
  separately selected ModelInteraction. A trusted host explicitly requests it
  and independently selects outbound disclosure and eligible replacement.
  Original history, exact recent/check evidence, source witnesses and custody
  remain authoritative; generated notes never certify effects or acceptance.
- `edits.replace_exact_text` admits one unique bounded literal anchor without
  language/task or repository governance defaults.
- `custody.SourceCustody` retains canonical known-source correspondence and
  refuses unknown-byte restoration. It is not Checkout, a transaction or store.

Use `CodingLimits` with an explicit interaction and a `CodingHost` composition.
For existing UTF-8 text repairs, supply `CodingObjective`, an authenticated
`SourceScope`, a fixed check plan, a corpus and host callbacks to
`RepositoryCodingHost`. `write_source_changes` is an optional per-file Resource
effect; it grants no scope and does not roll back earlier writes on later failure.

The Qwen compatibility adapter and the independent guarded repository host both
invoke this process; neither implements a second model/repair loop. Unknown
usage stays absent. A dispatch acknowledgment is not external-effect rollback.
Candidate validation remains distinct from worker completion, independent review
and publication. Source observations are not a lock or universal input closure.
Completion effects remain bounded host responsibilities. Transient continuation
and effect notes are not durable task restart or safe replay.

See the [contract, consumers and limitations](../../../../../docs/development/bounded-coding-agent.md).
The [active projection contract](../../../../../docs/development/active-context-projection.md)
documents byte watermarks, complete-schema assembly, protected feedback,
source-witness invalidation, qualified failures and future summary boundaries.
The [semantic compaction contract](../../../../../docs/development/semantic-context-compaction.md)
defines auxiliary budgets, provenance validation, privacy, exact-context
preservation and deterministic fallback. It requires neither a Qwen consumer nor
a live/provider-specific summarizer. Qwen's existing continuation policy remains
separate; the shared coding process and legacy outputs remain unchanged.
