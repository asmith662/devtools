# Experimental acquisition provenance

This non-installable package belongs to repository-owned dogfood evaluation.
It depends on native Localization task/obligation/anchor/provenance identities,
canonical Retrieval analysis and existing R1.5 diagnostics. Likely consumers
are U1 and later U2/U3 experiments; production never imports it. Nothing here
promotes a production need ontology, Query superclass, persistent graph, Event
system, authorization policy, runtime loop or search controller.

InformationNeed is an immutable manually authored purpose value: stable native
task/obligation scope plus caller key, concise statement, reason/provenance and
optional explicit anchors. It is neither the obligation, its lexical query,
a resource fact, candidate, accepted witness nor satisfaction assessment.
There is no need/query generator. The trace serializer validates linkage and
renders literal inputs; it does not infer them or choose mechanisms.

The inspectable trace has stable TASK, OBLIGATION, INFORMATION_NEED, QUERY, ROUTE,
RESULT, JUDGMENT, FAILURE and NEXT_ACTION sections. U1 populates the first six;
judgments/failures remain empty until independent C and C.5 permit Stage D.
Stage A has its own immutable trace snapshot; the current trace gains a separate
Stage B result layer without changing the treatment. Exact query text and native
analyzed terms are distinct. Full captured term evidence may be hash-bound in a
compressed result artifact, with exact per-query locators from the trace.

All U1 routes are CANONICAL_RESOURCE_BM25. Literal hints are NOT_ROUTED_IN_U1,
with reason U1_CONTROLLED_LEXICAL_ONLY. Future experiments may add route records,
but this schema does not authorize exact routing or mechanism selection.
Human inspection of treatment inputs/results is not blind gold adjudication.
Any maintainer comments or labels must be stored separately as MANUAL_AUDIT.
