# Case 0011 — U1 manual information-need decomposition

First explicit upstream formulation experiment. See [AUTHORING](AUTHORING.md)
for selection criteria, permitted author materials and historical-exposure limits;
[original task](task.txt) is verbatim. [Protocol](PROTOCOL.md) freezes the manual
treatment, exact gates and independent C/C.5 boundaries. [Contract inspection](CONTRACTS.md)
separates current caller semantics from experimental needs and acquisition inputs.

Stage A is committed before any query. Its immutable review/trace enumerate the
task → obligation → need → literal query → canonical route. Stage B adds current
trace.json/TRACE.md and STAGE_B_REVIEW.md, complete positive captured rows, exact
field evidence, unjudged R1.5 profiles, costs, overlap and duplicates. Human
inspection is encouraged but is NOT blind gold; store labels/comments separately
as MANUAL_AUDIT. Effectiveness remains UNKNOWN until independent C/C.5 and D.

Commands: `python -m experiments.codex_dogfood.case_0011.freeze freeze|verify`,
`python -m experiments.codex_dogfood.case_0011.execute run|verify`, and
`python -m experiments.codex_dogfood.case_0011.packet build|verify`.
Publish commands refuse overwrite. Execute is exactly once, gated on committed
inputs/code. Verify reconstructs evidence without running retrieval again.
Focused tests live under tests/experiments/codex_dogfood/acquisition/.

STOP at the prepared external Stage C workspace. No gold, C.5 packet, Stage D,
automatic need/query generation, exact routing, mechanism selector, BM25F or
semantic-resolution experiment. Production parameters/contracts remain unchanged.

Stage B is captured and the external Stage C packet is prepared. Use
`python -m experiments.codex_dogfood.case_0011.replay` for capture replay;
see [REPLAY_ERRATUM](REPLAY_ERRATUM.md). The original verifier remains frozen.
