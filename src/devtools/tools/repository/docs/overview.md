# Repository inspection and change validation

`GitInspectionTool(root, origin=...)` accepts only None through ToolRunner and
returns exact revision/path-status observations for a host-selected checkout.
It uses managed Commands, native executable discovery and porcelain-v1 -z,
without staging, switching, cleaning or publishing. It rechecks HEAD/status and
qualifies instability; it is not an atomic content snapshot or filesystem lock.

`InspectAndValidateTool(ChangeValidationPlan(...), origin=...)` performs one
deterministic inspect/scope/select/fixed-check/reinspect procedure. CheckSelection
names an existing immutable FixedCheckPlan entry and optionally a path condition.
Required check/acceptance semantics are host policy. Environment-name admission
applies to explicit Command overrides, not inherited-process isolation.

The report distinguishes passed, failed, skipped, refused, incomplete and
cancelled. It retains known bounded FixedCheckResults and original failure
objects; normalized command observations omit their payloads. Cancellation
propagates after last_report is retained. One Tool instance is bound to one
invocation origin; a fresh explicit invocation uses a new instance/origin.
There is no retry, rollback, cross-process lock or publication certificate.

See the [full contracts and actual consumers](../../../../../docs/development/command-capabilities.md).
