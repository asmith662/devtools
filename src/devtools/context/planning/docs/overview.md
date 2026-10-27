# Explicit repository Context plans

The devtools.context.planning package owns the first production
[ADR-0004](../../../../../docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
DisclosurePlan and ContextDisclosure values. A caller supplies a purpose,
an observed RepositorySnapshot, and an ordered set of concrete disclosure
choices. plan_disclosures records that choice; it does no retrieval, ranking,
automatic selection, cost optimization, or sufficiency assessment.

`SourceSearchDisclosureOption` also accepts an explicitly selected
`RepositorySourceUnit` from [multi-resolution retrieval](../../retrieval/docs/overview.md#selectable-source-representations).
It uses this same plan/materialization contract, authenticating retained
snapshot/resource state and disclosing source pointers, exact spans and original
text. Retrieval mode and rank do not select disclosure or establish sufficiency.
The existing whole-resource option remains available for file expansion.

`SourceRangeDisclosureOption` extends this same owner with caller-selected,
bounded exact source ranges. `materialize_source_range` records/materializes a
normal disclosure plan, retaining the original resource/content identity and
the requested/actual half-open character spans. UTF-8 byte truncation remains
explicit; this retained-state operation does not read the live filesystem.
The [scoped source Tool](../../../tools/docs/source-checks.md) owns separate
live source admission. No retrieval score establishes authority or readiness.

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

## Caller-selected repository-map metadata

`choose_repository_map_disclosure(purpose=..., snapshot=..., view=...,
symbols=chosen_symbols)` records an explicit ordered selection from an existing
canonical RepositoryMapView. The resulting RepositoryMapDisclosureOption uses
the same plan/materialize/render/assemble APIs and can coexist with whole-source
and qualified-reference options. It emits paths, kinds, lexical names, subjects,
exact declaration coordinates, snapshot/content identities and original selected
native symbols as provenance. It does not emit bodies, signatures, ranks or
unselected symbols; metadata is orientation, not sufficiency or exact source.

Blank/empty/duplicate/inconsistent choices and incompatible retained source fail
closed. Factory and materialization reuse canonical map validation; realization
also rechecks retained resource values. Selected resources are deduplicated in
first-selected order with aligned content identities. Choice identity binds
purpose, snapshot/repository and ordered declaration evidence. No automatic
selection, budget, tree renderer or source expansion policy is introduced.
Tests: tests/context/planning/test_repository_map.py. Delivery and native failure
remain separately attributed in apps/qwen/evaluation/map-disclosure-26/README.md.

## Exact source from represented map symbols

`choose_repository_map_source_disclosure(purpose=..., snapshot=...,
map_disclosure=..., symbol=..., source_index=...)` expands one symbol explicitly
represented by an existing RepositoryMapDisclosureOption. The caller supplies
an existing SourceSearchIndex for the same retained snapshot and an admitted
resource corpus; there is no implicit indexing, search or acquisition.

The returned immutable RepositoryMapSourceDisclosureOption retains the selected
symbol and exact RepositorySourceUnit. It authenticates canonical map membership,
represented selection and admitted source frame; existing UTF-8 offset and unit
identity helpers construct the exact RI declaration span. Materialization
reauthenticates the coupling and delegates text presentation to the existing
SourceSearchDisclosureOption, retaining (symbol,unit) as native provenance.
Source purpose may differ from orientation purpose; mixed plans still require
matching purposes as before. No existing representation identities change.

RI spans use one-based physical lines and zero-based UTF-8 columns, exclusive
end. They include declaration headers/bodies and nested content, but exclude
preceding decorators outside the RI span even if a source-search symbol expands
to them. Unicode, CRLF/LF and no final newline remain exact. No silent whole-file
fallback/truncation occurs. State/scope/metadata mismatch fails; later disk changes
do not rewrite retained evidence. Metadata and source remain distinct options.
Both compose with existing plans, materialization, rendering and request assembly.
This is caller-directed orientation-to-source, not automatic worker adoption,
selection, capacity policy or sufficiency. Tests: tests/context/planning/test_map_source.py.

The original RI coordinates remain authoritative in `unit.occurrence.source_range`.
Generic source-search rendered line labels retain that component's documented
logical `splitlines` convention; the adapter does not redefine those labels.
