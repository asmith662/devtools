# True BM25F experiment infrastructure

This non-installable experiment owns two-field observations/statistics adaptation, union df, normalized tf, contribution provenance, deterministic ranking, comparison and lossless traces. It depends on canonical repository identities and lexical primitives read-only. Production never imports it. No promotion or production interface is authorized. Case 0015 is a future consumer after separate execution authorization; synthetic fixtures are the only scoring inputs at Stage A.

CONTENT is exact whole-resource decoded text. FILENAME is `PurePosixPath(address).stem`, tokenized by the same Unicode `\w+`/casefold analysis. Length is observation count; each average includes every eligible document, including empty fields. No path, extension, symbols or identifier subtokens are added.

For each distinct query term:

```text
normalized_tf_f = tf_f / (1-b_f+b_f*length_f/average_length_f)
combined_tf = 1.0*normalized_tf_CONTENT + 0.25*normalized_tf_FILENAME
df_union = count(documents containing term in at least one field)
idf_union = ln(1+(N-df_union+0.5)/(df_union+0.5))
term_score = idf_union * ((1.2+1)*combined_tf) / (1.2+combined_tf)
score = sum(term_score in distinct query encounter order)
```

Both b values are 0.75; all query multipliers are 1.0. Empty fields contribute zero. Union df counts a document once across fields. Positive weights preserve the canonical positive content-or-filename candidate set. Equal scores retain original collection order. The implementation preserves native Arm A channel grouping and verifies candidate identity without a repair union.

## Controlled mathematical examples — synthetic only

Take two synthetic resources: `alpha.txt` contains `alpha alpha`; `quiet.txt` contains `quiet quiet`. Both content lengths are 2 and both filename lengths are 1, hence averages 2 and 1. Query `alpha` has content df=1, filename df=1, union df=1, N=2, and IDF=ln(2). The matching document has normalized tf 2 and 1; weighted aggregate 2.25.

True BM25F = `ln(2) * 4.95 / 3.45`.

Independent additive BM25 = `ln(2) * (4.4/3.2 + 0.25*2.2/2.2)` = `ln(2)*1.625`.

These differ. Counting the cross-field document twice would also change IDF incorrectly. This fixture proves the architectural change without obtaining any prospective Case 0015 score.

If only CONTENT has the queried term and content weight=1, union df equals content df and BM25F reduces algebraically to ordinary content BM25 (binary floating grouping can differ by rounding). If filename has no observations in any document, its average is zero and its contribution is zero. Field averages always remain independent; queries do not alter them.

`trace.py` serializes every float as `float.hex`, preserves canonical observations and identity binding, reconstructs scores and rejects tamper. Its fixed telescoping diagnostics replace field IDFs with union IDF, move field weights inside independent saturations, then combine into a single saturation. Field-normalization inputs stay unchanged from A; exact per-field denominators explain interaction with lengths. Native channel-grouping residual is explicit. Diagnostics are unranked counterfactual arithmetic, not additional arms or causal proof by score delta alone.

`gates.py` retains disciplined R1.7 integer gain/safety thresholds with R2 outcomes, independently frozen for B versus A. It additionally handles complete zero-retrieval-depth task-backed witnesses explicitly. No term-role or query-weighting implementation is reused. `pytest.ini` isolates controlled fixtures from production coverage configuration. No fixture contains Case 0015 resources, task evidence or effectiveness labels.

Run controlled tests with `uv run pytest -c experiments/bm25f/pytest.ini experiments/bm25f experiments/codex_dogfood/case_0015 -q`. No Stage B command exists here.
