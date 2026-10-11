# Case 0015 selection

SELECTION_CRITERIA.json was written before final task authoring. Selection used bounded direct inspection of current filesystem/persistence documentation, backlog records and source/tests. No lexical index, document frequencies, query execution or prospective scores were obtained. No prior-case gold was read for selection.

| Candidate | Decision | Reason |
|---|---|---|
| Strict bounded filesystem reads | SELECTED | Concrete documented allocation-before-rejection limitation; future evolution explicitly names chunk-bounded reads. Existing read contract, codecs, rich models, errors, paths, tests and validation establish six meaningful obligations. |
| Source-format-preserving structured writes | REJECTED | Documented future pressure, but exact formatting fidelity and supported formats require broader consumer choices before a bounded task can be authored. |
| Persistence process-loss recovery | REJECTED | B-0028 requires a real owning-domain recovery consumer; selecting it now would add unresolved durable state and lifecycle policy. |

The selected task is realistic future work, distinct from prior Context Planning and command-result rendering work. Its vocabulary naturally includes read, reading.py, file formats, codecs, rich model identifiers, byte bounds, errors and validation. Current evidence spans multiple contracts and implementations, so ranking can affect acquisition burden. This rationale predicts no BM25F improvement and provides no task-specific field weight tuning.

The task is a prospective information need only. This checkpoint implements neither bounded filesystem reads nor any production retrieval change. The existing filesystem roadmap remains future work.
