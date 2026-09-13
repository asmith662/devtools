# B-0020 — Capability, operation, and model-action substrate

- type: INVESTIGATION
- status: SUPERSEDED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: historical parent for separated Tool exposure, Action requests, governance, and experimental control flow
- primary_domain: tools
- supporting_domains: agents, models, governance, orchestration, experiments
- split_children: B-0035, B-0036

## Split record

The Qwen probes establish experimental evidence for proposal parsing,
action-specific materialization, Tool dispatch, bounded result projection, and
controller reconstruction. They do not promote a generic Action, Capability
registry, authorization framework, or orchestration API.

B-0035 owns Tool-facing exposure; B-0036 owns future Action request semantics.
Authorization remains B-0012/B-0013. Loop sequencing remains experiment-local
until B-0044 has sufficient evidence.
