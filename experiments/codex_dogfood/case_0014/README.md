# Case 0014: prospective query-term discrimination

R1.7 Stage A freezes a proposed completed-command-result diagnostic renderer,
six mandatory queries, task-only term roles and A/B/C contribution multipliers.
Stage B is captured once. The sole completed treatment-blind Astra / High primary
is imported byte-for-byte and [reviewed gold](adjudication/reviewed/REVIEWED_GOLD.md)
retains every semantic field unchanged. The feature is not implemented.

Read [STAGE_A_REVIEW.md](STAGE_A_REVIEW.md), [TRACE.md](TRACE.md),
[trace.json](trace.json), [SELECTION.md](SELECTION.md) and
[SELECTION_CRITERIA.json](SELECTION_CRITERIA.json).

Verify: `uv run python -m experiments.codex_dogfood.case_0014.freeze --verify`.
Controlled tests: `uv run pytest -c experiments/query_term_weighting/pytest.ini
experiments/query_term_weighting experiments/codex_dogfood/case_0014`.

The [gold publication](adjudication/reviewed/PUBLICATION.md) authenticates the
completed sterile packet and primary, with no reconciliation or second reviewer.
This checkpoint publishes gold only; effectiveness remains UNKNOWN and outcome
NOT_SELECTED until Stage D. Stage D is authorized after this checkpoint validates,
commits and pushes. True BM25F remains mandatory immediately after R1.7.
