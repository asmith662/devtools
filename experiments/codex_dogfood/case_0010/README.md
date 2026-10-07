# Case 0010 — prospective canonical BM25 parameter comparison

This case is selected after committed development analysis, from the documented
missing explicit line-range representation in Context Planning. It is a realistic
caller-directed feature spanning source, tests, docs and validation/configuration,
not a task selected from gold or to reverse individual Case 0009 ranks. The task
itself is not implemented. Ten caller obligations and exact query strings are in
`protocol.py` and frozen `treatment.json`.

Stage A uses the starting R1.5 Git snapshot `b1f8413`, broad established eligibility,
and native repository/snapshot/corpus values. No current-content substitution or
study metadata enters the corpus. All arms use canonical lexical analysis, native
independent content/filename scorers, stable corpus ties and identical queries.
Only k1, b and filename weight differ. A is (1.2, 0.75, 0.25); B, C and D are the
deduplicated development-selected completion, burden and robust challengers.

Stage A is committed before `execute run`. The runner refuses retries, builds
shared indexes once, executes each query once per arm, captures complete positive
ranks and exact field evidence, then validates with R1.5. Replay reconstructs
captures without reexecuting treatments. Costs separate shared construction,
actual per-query scoring and diagnostic construction. No effectiveness analysis
is performed before independent gold. Decision thresholds are frozen in
`treatment.json` and the [development protocol](../../bm25_sensitivity/PROTOCOL.md).

`packet build` consumes only the sealed Stage A frame and creates the complete
blind packet with explicit archive/payload digest scopes and strict metadata
whitelists. The prepared external sterile workspace contains exactly the five
blind inputs, no Git checkout, links, treatments or gold. Fresh Stage C must run
there with isolated validation. Clean independent Stage C is now committed and
the intentionally unblinded [Stage D analysis](analysis.md) is complete:
**MIXED / NO SAFE REPLACEMENT**. All arms reach the complete REQUIRED universe;
no challenger passes the exact frozen improvement and obligation-safety gates.
Production parameters remain unchanged. R1.7 is next, followed by mandatory R2
true BM25F. No R1.6b prerequisite is justified; Localization continuation remains.

`python -m experiments.codex_dogfood.case_0010.analyze verify` verifies committed
chain/input hashes, replays all 44 R1.5 capture lanes, validates clean gold and
alternative completions, and reproduces `analysis.json` and `analysis.md` exactly.
It never reruns treatment queries. Focused validation is
`uv run pytest --no-cov tests/experiments/bm25_sensitivity/test_analysis.py`.
The eight sealed Stage C files are immutable and excluded from formatting checks;
their historical blindness attestations are unchanged by this later Stage D join.
