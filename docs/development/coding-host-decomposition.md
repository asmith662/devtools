# Coding-host native protocol and lifecycle ownership

## Decision and maintained boundary

Baseline `0006e9131cedee4399c26e4c7cfa2f935b0ac176` has a 32,644-byte
repository host, only 124 bytes below the previous governed worker profile's
32,768-byte resulting-file ceiling. Size alone is not the architectural reason
to extract. Inspection finds native wire disclosure/materialization mixed with
stateful authorization, source refresh, Context installation and custody.

`agents.coding.protocol` now owns the existing read/edit/check Tool descriptors,
the existing callable-backed ToolInvocation implementation, argument-object
decoding, exact file/unit request materialization and whole-response operation
classification. These are one stateless native coding contract. The sole concrete
consumer is RepositoryCodingHost; independent host tests exercise each advertised
native surface. This is framework composition inside Agents under ADR-0001,
not a new model provider, schema language, ToolRunner or general dispatcher.

The owner depends on existing model-native types, ToolDescriptor, SourceReadRequest
and the navigation adapter's exact-unit binding. It does not import the repository
host, process loop, applications, Commands or custody, and cannot authorize or
execute effects. There is no reverse dependency or new mutable history owner.

RepositoryCodingHost keeps its public construction/build/prepare/receive/classify/
acquire/propose/apply/check/feedback/finish seams and the maintained EditLimits and
SourceChange import facades. Its classifier still checks source and records the
authentic assistant message before delegating the pure family decision. Its read
dispatch binds the current index, purpose and disclosure bound to the existing
Invocation with functools.partial; Tool admission and currentness validation still
occur at their existing owners. Private read wrappers were removed rather than
retained as compatibility machinery. The two maintained private descriptor imports
in projection tests migrate to the actual owner; there is no external/durable
contract for those former underscore names.

## Responsibilities deliberately retained

| Responsibility | Owner |
| --- | --- |
| Finite model/edit/check sequence and terminal reconciliation | coding.process |
| Native schemas, effect-free arguments and operation families | coding.protocol |
| Ranked candidates, inventory representation and navigation metadata | coding.navigation |
| Exact source materialization and authorization checks | Context and scoped source Tools |
| Exact replacement geometry and whole-batch admission | coding.edits |
| Complete-request preparation, active witnesses and original messages | RepositoryCodingHost with projection/compaction |
| Authorization, native correlation, action/check accounting, installed-byte verification and snapshot refresh | RepositoryCodingHost and existing host callbacks |
| Known-source archive/restoration | SourceCustody and host collaborators |

Extracting the entire acquisition dispatcher would require a broad mutable host
interface spanning progress, feedback, index, scope and validation. Moving apply
into pure edits would mix effect ownership into admission. Moving prepare into
pure projection would mix async auxiliary lifecycle with deterministic selection.
Those alternatives are rejected here. No mixin or parallel host state was added.

## Equivalence and limits

Descriptors and normalized native definitions are byte-identical to baseline for
plain, navigation and task-navigation modes. A maintained real-host preparation
test fixes those three pre-extraction wire fingerprints and verifies inventory
ordering, absence of fabricated source/effects, complete-request accounting and
idempotence. Existing neutral/guarded consumers cover source acquisition/refusal,
multi-call correlation, grounded edits, verified after-images, failed checks,
selected repairs, stale omission, empty scope, compaction fallback and custody.
All historical B-0035 focused/withheld/control/positive integration files remain
unchanged; they are independently executed against this tree.

The resulting-source ceiling remains configurable EditLimits policy, enforced on
each complete UTF-8 after-image, not a Prompt, anchor or aggregate-edit bound.
The former 124-byte margin obstructed realistic maintenance under that profile;
the extraction recovers practical room without changing admission. It does not
solve arbitrary large-file editing. Scope/currentness, native Tool/effect budgets,
timeout and unknown-effect behavior are unchanged. No local inference or service
mutation is authorized by this increment.

Exact before/after sizes, tests, committed executable identity, physical inputs and
publication are recorded in the [delivery receipt](../research/code-audit/coding-host-decomposition-20261031.json).
B-0035 stays closed. The separate B-0043 reconciliation selects a next workflow;
it does not implement or launch that workflow in this assignment.
