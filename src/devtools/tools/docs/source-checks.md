# Scoped source acquisition and fixed checks

`devtools.tools.source` and `devtools.tools.checks` are model-neutral adapters
over existing Context and Command owners. They accept no CodingTask, application
records or model profile. Host selection is permission; Tool availability and
retrieval relevance are not permission.

## Exact source

The host constructs `SourceScope.observe(root=..., repository=...,
addresses=..., maximum_resource_bytes=...)` using canonical Core paths and
Repository addresses. It retains the existing RepositorySnapshot and resource
occurrences, refusing path aliases and reusing bounded RI observation. Only
explicit addresses are authorized. The host may instead bind an already
authenticated snapshot with `SourceScope(root, snapshot, byte_bound)`.

Use existing discovery, corpus and SourceSearchIndex for file, symbol or window
selection. `SourceRangeDisclosureOption(purpose, unit, start, end, maximum_bytes)`
selects an absolute, half-open Unicode character span within that unit's parent
resource. It refuses unsupported ranges. Its bounded UTF-8 prefix never splits
a codepoint; `span`, `truncated` and the requested range distinguish partial
availability from complete acquisition. An empty file admits its empty range.

`ToolRunner.execute(ScopedSourceTool(scope, maximum_bytes=...), option)` checks
the unit's repository, snapshot and resource occurrence against host scope,
enforces the host disclosure cap and reobserves the declared source. Context's
existing plan/materialization pipeline returns a ContextDisclosure whose item
contains exact bounded text, original resource/content identities and the
range option as native provenance. No second index or identity system exists.

Historical retained materialization does not claim live currentness. The Tool's
live admission is a separate check. Sequential filesystem observations and
canonical path checks are not an atomic snapshot, filesystem sandbox or lock
against a later external writer. Access to other files is not authorized by
constructing a semantic path. Callers recheck correspondence before later effects.

For untrusted literal coordinates, use `SourceReadRequest(purpose, unit, start,
end, maximum_bytes)`. The native host may select the observed unit end for an
omitted field; an explicit null is an invalid literal. After ordinary
scope/currentness validation the Tool either
returns the canonical disclosure or `SourceReadRefusal`. The latter means the
requested interval was rejected before source materialization; it grants no
witness. `select_source_read` is the effect-free shared range decision and
`source_read_bounds` projects authorized observed length/valid range/byte bounds.
Neither helper grants scope. Operational/materialization exceptions are not
converted into refusals. A caller may return correlated refusal feedback and
let the model choose a new call; no automatic retry is implied. See the
[reliability contract](../../../../docs/development/local-agent-reliability.md).

## Fixed checks

The trusted host constructs immutable `FixedCheck(name, command)` values and a
`FixedCheckPlan(root, checks, source_scope=None, output_policy=...)`. Each
existing Command fixes argv, cwd, positive timeout, environment, stdin and exit
policy; each working directory is inside host root. Names are unique, nonblank
and host-selected. Model input may select only an admitted name, never argv.
The host owns finite plan selection, sequential execution and all task oracles.

`ToolRunner.execute(FixedCheckTool(plan), name)` verifies current canonical
root/cwd and optional source scope, then invokes the existing CommandExecutor
once. `FixedCheckResult` retains the actual CommandResult. If declared inputs
change or their post-check observation fails, the known result remains available
with `inputs_current=False` and the original secondary `input_error`.
Without a declared source scope, `inputs_current=None`: only execution facts
are established. `passed` requires successful exit, untruncated output and no
failed declared-input check. The host decides stronger acceptance requirements.

Command errors and caller cancellation propagate unchanged. The Tool does not
retry. An exception may follow an already completed effect; earlier results in
a host-controlled sequence remain facts, not a rolled-back batch. Command
events and returned values are not automatically durable Evidence receipts.

Declared text-resource equivalence is not universal dependency, ignored-config,
toolchain, environment or HEAD-sensitive validation closure. These checks are
neither protected validation nor semantic review/publication certificates.
Integration continues to own fresh protected and destination validation.

## Consumers and composition

Agents' [native composition](../../agents/docs/model_tools.md) joins selected
ModelToolCall/ToolInvocation, explicit host admission and ToolRunner. Tools and
Models remain independent. A host can project result feedback under the original
native call ID without requiring Qwen presentation or configuration.

Qwen ContextTools delegates scope observation and exact range materialization;
its schema, currentness gate, observations, active Context and obligation policy
remain local. CodingCommands delegates fixed host Command execution through the
shared check Tool. `apps.qwen.validation` preserves legacy runner/oracle and
result policy; local closeout invokes that public compatibility adapter instead
of private coding-loop helpers. It still requires the legacy task/candidate
contract. Framework-only tests exercise real source/check behavior with all
application imports and checkout application file access denied.

## Scoped navigation

`ScopedSourceNavigationTool(scope, index, maximum_results=8)` consumes a typed
`SourceNavigationRequest` over a host-selected existing `SourceSearchIndex`.
It checks scope/snapshot correspondence and currentness before returning bounded
existing source units. A query uses the maintained source search; an empty query
pages file, symbol, window or mixed views, optionally restricted to one admitted
path. It creates neither another index nor source disclosure. Units retain their
resource and span identity; callers must project only authorized bounded metadata
for model presentation, rather than serializing the internal resource content.

Agents' neutral coding host supplies the native metadata projection and resolves
an exact current unit selection into `SourceReadRequest`. Actual acquisition
still uses `ScopedSourceTool` and Context materialization. See the
[contract and consumer evidence](../../../../docs/development/source-navigation-continuity.md).

`MAXIMUM_NAVIGATION_QUERY_CHARACTERS` exposes the existing scoped query bound
to higher composition layers. Agents can select a bounded task query and supply
its own finite outline policy; neither source Tool owns task planning or grants
source/edit authority from navigation metadata.
