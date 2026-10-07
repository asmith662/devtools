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
there with isolated validation. **Effectiveness remains UNKNOWN. Stop before
independent adjudication.** Production parameters are unchanged; R1.7 follows
completed R1.6, and true BM25F remains mandatory after R1.7. No R1.6b prerequisite
is justified by the retained variant audit; Localization continuation is preserved.
