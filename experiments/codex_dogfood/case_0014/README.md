# Case 0014: prospective query-term discrimination

R1.7 Stage A freezes a proposed completed-command-result diagnostic renderer,
six mandatory queries, task-only term roles and A/B/C contribution multipliers.
The feature is not implemented. Retrieval, prospective indexing, treatment
scoring and gold are absent.

Read [STAGE_A_REVIEW.md](STAGE_A_REVIEW.md), [TRACE.md](TRACE.md),
[trace.json](trace.json), [SELECTION.md](SELECTION.md) and
[SELECTION_CRITERIA.json](SELECTION_CRITERIA.json).

Verify: `uv run python -m experiments.codex_dogfood.case_0014.freeze --verify`.
Controlled tests: `uv run pytest -c experiments/query_term_weighting/pytest.ini
experiments/query_term_weighting experiments/codex_dogfood/case_0014`.

Maintainer reviews the frozen Stage A. Only after authorization execute the
prospective lexical treatments once. No Stage B execution command is supplied.
Future gold is one treatment-blind GPT-6 Astra / High primary, no automatic
second reviewer. True BM25F remains mandatory immediately after R1.7.
