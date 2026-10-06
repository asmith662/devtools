# Explicit repository Context plans

The devtools.context.planning package owns the first production
[ADR-0004](../../../../../docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
DisclosurePlan and ContextDisclosure values. A caller supplies a purpose,
an observed RepositorySnapshot, and an ordered set of concrete disclosure
choices. plan_disclosures records that choice; it does no retrieval, ranking,
automatic selection, cost optimization, or sufficiency assessment.

~~~text
InformationNeed / caller purpose
          |
          v
       Retrieval (optional; native evidence remains independent)
          |
          v
candidate evidence / explicitly known target
          |
          v
caller chooses representations --> DisclosurePlan
                                  /             \
                                 v               v
                      qualified Reference   whole resource
                                 \               /
                                  v             v
                            ContextDisclosure
                                  |
                          deterministic rendering
                                  |
                         copied ModelRequest / Agent
                                  |
                        later need may create another plan
~~~

DisclosurePlan binds purpose, repository and snapshot identities, ordered
choices, and optional preceding-plan identity. The plan's deterministic
identity changes when purpose, applicability, order, choice, or lineage changes.
Each concrete choice names an implemented representation and retains its own
native support. The common PlannedDisclosure protocol only permits the two
current consumers to participate in one plan; it is not a generic fact ontology,
language-independent parser, or materializer registry.

materialize_disclosure_plan rechecks the supplied snapshot and requires each
materialized item to match its planned choice. It fails on stale, missing, or
incompatible dependencies. A ContextDisclosure retains one item per choice,
exact content identities and addresses, text, and the native materialized
provenance. Rendering preserves plan order and does not infer new facts.
assemble_context_disclosure_model_request copies a caller's ModelRequest and
appends already-rendered Context after the unchanged task.

Implemented choices:

- WholeResourceDisclosureOption: explicitly chosen observed resource,
  materialized from retained snapshot content. It is a coarse representation,
  never a silent fallback.
- PythonQualifiedReferenceDisclosureOption: adapts the existing Python-specific
  qualified Reference/direct Call path. Its existing fact, derivation,
  source/target content checks, exact UTF-8 extraction, and bounded Call
  meaning remain intact.

The caller may construct a later plan with a different or refined purpose and
preceding_plan_identity. This preserves lineage but does not implement an agent
recovery controller or prove that a model retained prior information. No token
budget field is selected: ADR-0004 distinguishes hard capacity, policy budget,
and remaining capacity but selects no universal cost function. A future planner
can consume retrieval evidence and explicit constraints without changing the
plan/materialization distinction. Retrieval rank does not itself decide
representation, quantity, or adequacy.

[ADR-0005](../../../../../docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md)
places Localization before this package. The semantic kernel at
`devtools.context.localization` represents caller obligations, native witness
identities, snapshot-qualified assessments, and bounded frame readiness. It does
not provide automatic Context links. Its one-way BM25 acquisition adapter, grounding,
bounded structural generation and explicit resolution recording are implemented.
Current `plan_disclosures`
remains caller-directed; it does not resolve obligations, transfer obligation
provenance, or establish representation coverage/capacity.
