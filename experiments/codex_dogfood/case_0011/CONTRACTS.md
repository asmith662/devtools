# Current contracts inspected after manual authoring was sealed

LocalizationTaskInterpretation groups explicit caller identities, TaskProvenance,
shared LocalizationAnchors and caller-authored LocalizationObligations. Each
obligation retains its predicate, requirement, SatisfactionCriterion, optional
applicability condition and caller witness alternatives; constructors validate
task-local identity/linkage, not semantic completeness. TaskTextSpan is a native
half-open task-text reference. An anchor is caller text, not a resolved fact.

ObligationLexicalQuery associates literal caller text with one obligation and
query identity. LocalizationLexicalAcquisitionRequest supplies full_task_query,
all obligation queries, an explicit snapshot/index, result bound and settings.
acquire_localization_lexical_evidence passes full task and each exact query
unchanged to canonical BM25 independently; it generates neither obligations nor
queries, fuses no rankings, and assesses no satisfaction. Current case protocols
manually author the task and one query per obligation. U1 retains that baseline
and adds separately authored experimental needs and queries outside production.

After task/authoring/AUTHORING exact hashes were sealed, inspected task.py,
obligation.py, identity.py and lexical.py, prior case freeze/capture/packet helper
contracts, R1.5 serializers, and the Planning overview/rendering and current
plan test contract. Current rendering assembly copies a ModelRequest with only
Prompt replaced; no optional byte ceiling exists. The task remains future work.
These implementation reads do not revise the frozen manual vocabulary or needs.

Ownership: experiments/codex_dogfood/acquisition provides a non-production
purpose value and inspectable provenance projections. Case 0011 owns concrete
task composition, archived starting frame, exclusive execution and sterile
publication. Existing framework primitives own native semantic identities,
paths, file I/O, command/Git execution, BM25 and diagnostic reconstruction.
No production API, durable framework schema or dependency direction changes.
