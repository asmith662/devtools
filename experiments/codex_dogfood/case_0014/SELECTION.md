# Prospective task selection

SELECTION_CRITERIA.json was written first, before task, queries or frame
observation. Selection used existing contracts and future capability pressure,
never rankings, document frequencies, prior-case gold or treatment outcomes.

Candidates considered:

| Candidate | Decision | Reason |
|---|---|---|
| Repository snapshot delta inspection | Rejected | Snapshot/change protocol pressure requires broader semantic design; too close to earlier Context tasks. |
| Advanced provider streaming (B-0046 pressure) | Rejected | Consumer/lifecycle ownership and incomplete integration requirements would dominate this small query-side experiment. |
| General coding-context continuation (B-0002) | Rejected | Canonical backlog concern is broad, with unresolved architecture; it is not a bounded implementable feature. |
| Completed command-result diagnostic renderer | Selected | Existing commands docs explicitly leave text decoding as future work; immutable completed results give a narrow pure presentation seam with nontrivial byte, retention, event-loss and failure contracts. |

No backlog item supplied a smaller direct feature without deciding unresolved
architecture. This task is a proposed future resource-commands capability, not
implementation authorization. Selection inspections: commands models/result.py,
models/output.py, errors.py, public exports, docs/{overview,command,execution,events}.md
and tests/resources/commands/test_models.py; architecture taxonomy/documentation
map and B-0002/B-0046 pressure. The feature spans six mandatory obligations and
mixes literal symbols/paths, domain facts and ordinary work verbs naturally.

The broad eligible source/test/doc/config universe is independent of the task.
Prior experiment material and whole resources carrying prior-case markers are
excluded by a frozen general leakage rule, never by relevance or term frequency.
Original retained resource text is unmodified. No prospective rankings were
available or used. The feature is not implemented by this checkpoint.
