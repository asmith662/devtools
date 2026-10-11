# Case 0015 — prospective true BM25F

R2 CURRENT / STAGE_A_FROZEN. Effectiveness NOT_EVALUATED. Stage B NOT_EXECUTED.

The first R2 slice isolates two existing fields: whole exact content and the canonical filename stem. Arm A is unchanged independent content BM25 + 0.25 filename BM25. Arm B combines normalized field tf before one union-IDF saturation. All query multipliers are 1.0. No production feature or retrieval behavior changes.

Read STAGE_A_REVIEW.md, TRACE.md, protocol.json and frame.json. resources.json.gz owns exact eligible content. integrity.json seals authored/generated artifacts and implementations. Run `uv run python -B -m experiments.codex_dogfood.case_0015.freeze --verify` for observation-only replay. Synthetic fixtures live in experiments/bm25f and do not use this prospective frame.

Maintainer reviews frozen Case 0015 R2 Stage A. Only after authorization execute canonical additive BM25 and true BM25F prospectively exactly once. No Stage B entry point is provided here. No gold exists.
