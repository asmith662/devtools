# Native model/Tool composition

`devtools.agents.model_tools` composes the existing model and Tools domains.
ADR-0001 keeps those domains independent; this Agents owner depends on both.
The module owns two operations, not a coding loop or execution engine:

- `normalize_tool_descriptor(descriptor)` projects an explicit `ToolDescriptor`
  into an immutable `ModelToolDefinition`. It grants no execution authority.
- `execute_model_tool_call(call, *, invocation, tool, admit, runner)` binds the
  normalized call name to the host-selected `ToolInvocation.descriptor`,
  materializes candidate typed input, awaits required host admission, and calls
  the supplied existing `ToolRunner` once. It returns the Tool-defined result
  unchanged. ToolRunner remains the sole semantic validation/execution owner.

The host selects the actual Tool independently of its native operation name.
For example, a single repository Tool may support several disclosed operations;
its `Tool.name` need not equal the selected descriptor's name. No registry,
automatic capability discovery or model-controlled Tool selection is installed.

`ToolInvocation.materialize` must be effect-free. `admit` is an async callable
receiving the original `ModelToolCall` and materialized input. It must raise to
refuse and return `None` to admit. It is an explicit host decision, not a
permission boolean or a substitute for Tool semantic validation. A mistakenly
synchronous callback fails before ToolRunner entry. Scope, budgets and permitted
arguments remain the trusted host's responsibility.

The caller authenticates the model response source and pending invocation frame.
Before any member of a native feedback batch executes, the caller must refuse
missing, duplicate or foreign call identities. Complete continuation is still
validated by `Prompt`/`PromptMessage`. `ModelToolCall` retains its existing optional
ID for direct uses that do not build native feedback. The composition operation
does not create IDs, infer a batch, build feedback or deduplicate across calls.

Selection or materialization failure does not enter admission or ToolRunner.
Admission refusal does not enter ToolRunner. ToolRunner validates before execution.
Original exceptions and cancellation propagate, including after a Tool effect.
One operation delegates once; this is not exactly-once execution across repeated
host invocations. No retry, rollback, fabricated result or durable evidence is
provided. The host retains known earlier batch results and must reconcile an
unknown effect before deciding whether any further action is safe.

## Operational consumers and independent acceptance

Qwen's `ContextTools.dispatch` and `CodingCommands.dispatch` select operations from
their existing trusted task definitions and delegate through this shared owner.
Their task-specific JSON tuple materializer remains application-owned. Original
source/currentness checks, fixed check argv, bounds, journals, result decoration,
failure behavior and higher host authority remain there. The legacy Qwen
`normalize_tool_descriptor` import is a direct compatibility re-export.

The standalone maintained host in `tests/agents/native_tool_host.py` uses an
independent `ModelInteraction`, repository observation, Context planning, an exact
`ReadRepositoryFileTool`, native correlated Prompt continuation and a fixed
`CommandTool`. It runs from a tiny authored repository under guards denying
application imports and checkout data access outside framework/dependencies.
It requires no Qwen task, profile, prompt, journal or application implementation.
Its optional fixture-only effect tests uncertainty; it is not a reusable editor.

This composition operation does not itself own source acquisition, fixed checks
or the goal-directed coding lifecycle. Subsequent authorized migrations provide
scoped source/fixed-check Tools and the [bounded coding Agent](../coding/docs/overview.md)
above it. Runtime, observation policy and Codex's external-Agent semantics remain
unchanged; no general orchestration owner is introduced.
