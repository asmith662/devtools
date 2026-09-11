# B-0012 — Investigate governed effect semantics

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: FOUNDATIONAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: governance boundary for externally meaningful operations
- parent: B-0005

## Problem / value

Determine the boundary for reusable operations that cause effects.

## Established invariants / uncertainty

Tool admission or discoverability is not authorization. Commands and existing
Tools remain independent local contracts. Do not create universal Tool, Effect,
Capability, or Operation nouns yet.

Future investigation must separately ask whether an agent/model may know about
or be shown a capability, whether it is relevant enough for the current
model-facing surface, and whether a concrete proposed invocation is authorized
to execute. These may share a boundary or remain local; separate systems are
not assumed.

It must also distinguish capability inventory, access/availability, disclosure,
contextual relevance, concrete authorization, eligible implementations or
bindings, and selection among already eligible bindings. Visibility does not
imply execution authority; authorization does not require model visibility;
eligibility does not select an implementation; and routing must not manufacture
authority.

Future live evidence should distinguish disclosure denial (the capability does
not appear in the effective model-facing surface) from execution denial (a
known/requested capability cannot cause its unauthorized effect).

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0013, B-0014, B-0020
- operational_dependencies: real mutating harness capability
- consumers: future Qwen/Codex harnesses and mutation bridges
- established_invariants: tool admission or discoverability is not authorization
- unresolved_semantics: capability inventory/access, model surface and discovery, disclosure/relevance/authorization, eligible binding and selection, effect outcome, idempotency, and reconciliation boundaries
- risk_if_deferred: bounded harnesses use explicit local effects first
- risk_if_implemented_early: lowest-common-denominator operation framework
- promotion_trigger: mutation crosses reusable harness boundary
- validation_level: NONE
- live_validation_trigger: a real harness exposes a mutating operation across a reusable boundary
- related: B-0005, B-0009, B-0013, B-0014, B-0020
