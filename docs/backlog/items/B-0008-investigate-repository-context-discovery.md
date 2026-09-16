# B-0008 — Investigate repository-context discovery for coding harnesses

- type: INVESTIGATION
- status: SUPERSEDED
- decision_maturity: READY_FOR_DESIGN
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: minimum selected repository information for one bounded coding-worker story
- primary_domain: context
- supporting_domains: resources, tools, agents, models, experiments
- parent: B-0002

## Superseded investigation

This investigation preserved the then-unresolved question of the minimum
repository-information boundary for a frozen coding-worker story. Its narrow
deterministic evidence remains historically accurate: bounded root-origin
listing and text reading prove repository fact acquisition and controller-
directed navigation, not reusable repository intelligence.

[ADR-0002](../../architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md)
supersedes the unresolved semantic premise. It establishes Repository and
RepositorySnapshot identity, Derivation and DerivedKnowledge validity,
dependency-scoped incremental reuse, relationship semantics, and the
Repository-intelligence/Context distinction. The broader unimplemented pressure
is retained by B-0002; this status does not claim any production implementation
or that the former navigation experiment established retrieval or compilation.

## Historical problem / value

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
- related: ADR-0002; B-0002
- semantic_decision: RESOLVED
- promotion_trigger: historical only; superseded by ADR-0002 semantic decision
- validation_level: INTEGRATION
