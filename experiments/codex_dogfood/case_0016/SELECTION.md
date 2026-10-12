# Case 0016 selection

SELECTION_CRITERIA.json was written before final task authoring. Inputs were
current architecture/package contracts, B-0002 future disclosure pressure, source
interfaces and the exact task texts of Cases 0011–0015. No prior gold was used.
No prospective lexical, exact-route, graph/connectivity, rank, score or candidate
surface was inspected. No claim about actual required resources is made here.

| Candidate considered | Disposition and reason |
| --- | --- |
| Caller-selected resource-pointer disclosure | Selected: bounded Context representation already motivated by B-0002 and ADR-0004; existing whole-resource/plan/materialization/assembly interfaces provide a realistic multi-package task, while policy/validation evidence remains partly lexical |
| Direct Python source-declaration disclosure | Rejected: same immediate feature as Case 0012 |
| Context disclosure manifest | Rejected: same immediate feature as Case 0013 |
| General incremental RI invalidation/cache | Rejected: broad unresolved persistence/scheduling design, unsuitable for a bounded feature task |
| New graph or configuration relationship family | Rejected: would entangle the requested feature with the treatment architecture and invite graph-oriented selection |

Selected task contains six mandatory obligations. Definition/reference structure
plausibly relates existing plan, resource, materialization and ModelRequest
interfaces; documentation, export policy and validation obligations may remain
primarily lexical. This is a hypothesis, not inspected prospective connectivity.
The feature itself remains unimplemented.
