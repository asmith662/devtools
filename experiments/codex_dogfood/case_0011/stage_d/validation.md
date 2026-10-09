# Case 0011 Stage D validation

The consolidated Stage D package passes the checks below. These checks consume
the frozen capture; they do not execute Case 0011 retrieval, exact routing,
mechanism routing, reformulation or parameter reranking.

| Check | Result |
| --- | --- |
| Eight frozen checkpoints and ancestry | PASSED; 90 selected committed artifacts authenticated |
| Historical protocol authentication | Stage A placeholder and reviewed preparation version authenticated at their proper commits |
| Historical primary C.5 publication | Original publication and later historical-status preface authenticated separately |
| Exact identity joins | PASSED; 531 resources, nine obligations, 4,779 gold cells, 32 units, 18 needs, 576 mappings, 28 captured queries |
| Alternative and responsibility accounting | All 12 alternatives and six task combinations; gold B ownership, direct C responsibility and all collective members independently checked |
| Captured R1.5 diagnostic replay | PASSED; all 28 query profiles and 550 subject explanations reconstructed from captured rows |
| Lossless diagnostic archive | Canonical JSON payload, deterministic gzip with mtime zero, both digests and byte correspondence checked |
| Scientific metric checks | Raw/reach partitions, prefix occurrences/unions, duplicates, UTF-8 bytes, same-unit comparisons, oracle, failure partition, gates and outcome checked |
| Focused Stage D suite | 21 passed |
| Protected development validation | 1,588 passed, two skipped; configured production branch coverage 100% |
| Scoped Ruff | PASSED |
| Scoped formatter | PASSED |
| Strict scoped mypy | PASSED; seven source files |
| Deterministic artifact replay | PASSED; JSON, Markdown, trace, compressed explanations and digest ledger reproduce byte-for-byte |
| Overwrite refusal | Existing complete or partial output destinations reject publication before any writes |
| Tamper rejection | Input identity/text/count/rank/contribution changes, incomplete/duplicate joins and changed published bytes rejected |
| Worktree and index whitespace | PASSED |

Commands:

```powershell
uv run python -B -m pytest -c experiments/codex_dogfood/case_0011/stage_d/pytest.ini experiments/codex_dogfood/case_0011/stage_d/test_analysis.py -q
uv run python scripts/validate_development.py
uv run ruff check experiments/codex_dogfood/case_0011/stage_d
uv run ruff format --check experiments/codex_dogfood/case_0011/stage_d
uv run mypy --strict --follow-imports=silent experiments/codex_dogfood/case_0011/stage_d
uv run python -B -m experiments.codex_dogfood.case_0011.stage_d.analyze verify
git diff --check
git diff --cached --check
```

The input loader reuses canonical R1.5 mechanics for analyzer, DF/IDF and score
reconstruction. It performs zero native Case 0011 queries. Focused tests also
replace native retrieval and parameter reconfiguration with rejecting stubs.
The protected development profile excludes retained outcome-dependent experiment
tests before collection. Confirmation and reserve data were not accessed.

The initial 11-file conflict inventory and verified byte-for-byte backup are
ignored operational records. They are excluded from all scientific input and
output hashes. Publication refuses overwrites; source-only integrity-ledger
updates during consolidation were separately backed up and accepted only after
every other generated artifact reproduced identically. Frozen artifacts and
production source were untouched.

See [ownership resolution](OWNERSHIP_RESOLUTION.md) for the single-writer check
and bounded merge, [analysis](analysis.md) for the frozen decision, and
[review](STAGE_D_REVIEW.md) for exact inputs, responsibility, ranks, contributions
and failure evidence. No next increment was implemented.
