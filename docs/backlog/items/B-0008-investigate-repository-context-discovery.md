# B-0008 — Investigate repository-context discovery for coding harnesses

- type: INVESTIGATION
- status: BACKLOG
- decision_maturity: NEEDS_INVESTIGATION
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: minimum selected repository information for one bounded coding-worker story
- primary_domain: context
- supporting_domains: resources, tools, agents, models, experiments
- parent: B-0002

## Problem / value

Determine the smallest relevant-information boundary a frozen coding-worker
story needs: inventory/addressability, known-resource resolution, discovery,
selection, bounded transformation, provenance, freshness, disclosure, and
eventual model-facing compilation.

Current deterministic evidence proves bounded nonrecursive listing and text
reading through Resources adapted by Tools. A scripted Qwen controller begins
at repository-relative `.` with no target path or directory supplied, descends
through direct listings, discovers `reading.py` only from its parent listing,
and reads its bounded textual source through the existing Tool boundary.

This proves root-origin repository fact acquisition and controller-directed
navigation. It does not prove reusable repository inventory, ranking, symbol
search, retrieval, Context selection, budgeting, or Context compilation.

- hard_dependencies: none
- pressure_dependencies: none
- operational_dependencies: resources filesystem, core paths, core regex
- promotion_trigger: one coding-worker story identifies its minimum selected information
- validation_level: INTEGRATION
