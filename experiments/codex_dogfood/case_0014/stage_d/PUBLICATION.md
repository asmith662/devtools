# Case 0014 Stage D publication validation

The authorized gold publication was committed and pushed at
`466e0a7a473d5baf7ff0fd75ec9ae3031760649a`. A publication metadata mistake changed
the sealed Stage A README. Historical-seal authentication caught it before
effectiveness analysis; its original exact bytes were restored and pushed at
`c43d46607e55d7999ac0277cd196ca9d9e07b9b5`. Stage D authenticates both checkpoints
and every current Stage A seal. Primary/reviewed scientific bytes did not change.

Validation performed:

- Sterile `python -B stage_c_builder.py --verify`: PASS, exact-byte replay,
  preservation of all five original packet files, 26 rejected adversarial mutations.
- Reviewed gold: 23 focused tests passed. After its final-newline serialization
  repair, two affected replay/hash/overwrite tests passed again. Scoped Ruff,
  formatter check and strict mypy passed.
- `uv run python scripts/validate_development.py`: 1,588 passed, two opt-in live
  skips, 100% production branch coverage. The protected profile excluded
  `tests/experiments/` before collection. Subsequent changes affect experiment
  code and status documentation; production source and the protected test inputs
  retain their original seals.
- Final Stage D and generic weighting/gate tests: 64 passed with
  `uv run python -m pytest -c experiments/query_term_weighting/pytest.ini
  --import-mode=importlib experiments/codex_dogfood/case_0014/stage_d
  experiments/query_term_weighting -q`.
- Final scoped Ruff, formatter check and strict mypy passed. Working and staged
  diff checks passed. Imported immutable primary files were not reformatted,
  lint-fixed or type-check edited.
- Separate build and read-only verification processes reconstruct scientific
  JSON, Markdown, trace and integrity bytes exactly. Focused tests cover every
  witness/prefix/unique/label/byte arithmetic, required-rank and integer gates,
  exact frame/candidate/contribution identity, tampering and overwrite refusal.

The sole C-versus-A outcome is QUERY_TERM_WEIGHTING_HARMFUL. Stage D scientific
hashes cover the seven generated artifacts through `integrity.json`, whose own
digest is reported externally to avoid a cycle. This publication record and
README are separate mutable documentation; tests and code are repository-owned.
No `.local` file participates in a scientific hash or outcome.

No native scientific operation, second reviewer, reliability adjudication,
reconciliation, confirmation/reserve access, sequential search or production
behavior change occurred. SEARCH_POLICY_FAILURE = NOT_ASSESSED. R2 true BM25F
design/freeze is NEXT / MANDATORY and has not begun.
