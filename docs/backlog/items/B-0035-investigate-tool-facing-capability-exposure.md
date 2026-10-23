# B-0035 — Investigate Tool-facing capability exposure

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: exposing reusable Tool semantics at a model or Agent boundary
- primary_domain: tools
- supporting_domains: models, agents, context
- split_from: B-0020

## Problem / value

Determine how a Tool's bounded contract may be described and projected for a
model or Agent without making Tools own model protocol, Action parsing,
authorization, or result reconstruction. Resources remain lower-level than
Tools.

The Qwen probes demonstrate local descriptions, bounded projections, and
action-specific materialization only. They do not establish a reusable schema
or registry.

[ADR-0001](../../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
now approves the narrow future seam: a model-agnostic bounded Tool descriptor
and invocation materialization surface, projected by composition into a
model-facing Tool definition. JSON Schema is the intended provider-independent
vocabulary, without freezing an internal representation or authorizing a
registry. This record retains the implementation and independent-consumer
pressure; it does not make a Tool automatically model-visible.

- hard_dependencies: none
- pressure_dependencies: B-0008
- operational_dependencies: stable model-facing Tool consumer
- promotion_trigger: exposure semantics are stable independently of local experiment code
- validation_level: NONE

## Recovered-input / pinned mechanism evidence (2026-10-23)

Original candidates07/15 and [pinned Tool research](../../research/agent-harness-mechanism-review.md#pydantic-ai-typed-tools-retries-and-permission-handoff)
provide concrete schema/decorator/validation-before-execution examples.
FunctionToolset derives a runtime validator, but ExternalToolset at the inspected
revision uses any_schema; its advertised schema is not host semantic admission.
Typed conversion, approved argument overrides and retries must not alter current
exact source/path/byte/version authority or charge fewer task attempts silently.
Study a transparent definition helper only after measuring real duplication and
compatibility; no replacement ToolRunner/registry/authorization layer is selected.

## DeepSeek Harness / Aider evidence (2026-10-23)

DeepSeek's defineTool derives schemas and input validation, whereas raw registry
Tools still own argument validation; policy guards, visibility and approval are
separate. Devtools ToolRunner already validates then executes. ContextTools and
CodingCommands provide two concrete definition/dispatch consumers to measure
before proposing a helper; their domain semantics must remain authoritative.
Dynamic in-process plugin loading is a trust boundary, not a requirement for
model-neutral Tools. Existing pending module/edit ergonomics reviews carry the
question; no new registry, decorator or authorization layer is selected.

See the [pinned source-and-test comparison](../../research/agent-harness-mechanism-review.md#deepseek-harness-and-aider-source-and-test-audit-2026-10-23)
and [five-flow audit plan](../../research/development-lifecycle-audit-plan.md).
Status, dependencies, decision maturity and promotion trigger remain unchanged.

## Executed five-flow lifecycle evidence (2026-10-23)

ToolRunner validates then executes once with unchanged exceptions/cancellation. Native call correlation and failure projection are application-owned, not universally instrumented by ToolRunner. Fifth selected real flow is a refused expand_source call, not source disclosure. Future definition/observation helpers need compatible call IDs, admission, primary exceptions and partial-batch semantics in ContextTools/CodingCommands; no generic Tool registry or authorization layer is selected.

See the [source/evidence audit and priority crosswalk](../../research/development-lifecycle-observability-audit.md)
and its [authenticated metadata](../../research/development-lifecycle-observability-evidence-20261023.json).
Status, dependencies, decision maturity and promotion trigger remain unchanged.
