# B-0002 — Coding Context Substrate

- type: EPIC
- status: BACKLOG
- decision_maturity: NEEDS_INVESTIGATION
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: coding-oriented selection and assembly of relevant repository information
- primary_domain: context
- supporting_domains: resources, tools, agents, models, experiments

## Problem / value

Investigate the smallest coding-oriented Context boundary required by a bounded
worker. Context is information selected and assembled as relevant to a current
purpose; it is not Conversation state, repository storage, or Memory.

Resources provide access and Tools may adapt bounded access. Neither existing
filesystem reads nor Qwen action results establish reusable selection,
retrieval, ranking, provenance, budgeting, or compilation semantics.

- hard_dependencies: none
- pressure_dependencies: none
- operational_dependencies: resources filesystem, core paths, core regex
- children: B-0008
- promotion_trigger: B-0008 identifies minimum selected information for one frozen coding-worker story
- validation_level: NONE
