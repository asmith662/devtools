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

## Current reviewed checkpoint

Primary Stage C, independent Stage C-R, reliability comparison, reconciliation
and reviewed gold are COMPLETE. Source adjudications remain immutable. The
[reviewed reliability conclusion](adjudication/reviewed/REVIEWED_GOLD.md) is the
architecture-grade Case 0011 target; primary-only conclusions were unsafe.
The separate [C.5 packet transparency document](adjudication/stage_c5/C5_PACKET_REVIEW.md)
is PREPARED only. C.5 adjudication and Stage D are NOT PERFORMED; U1 effectiveness
is UNKNOWN. [Current status](adjudication/STATUS.md) supersedes historical status
wording above; no treatment result had been joined at that historical checkpoint.

## Current Stage D checkpoint

Stage D is COMPLETE. The [joined analysis](stage_d/analysis.md) selects
**INFORMATION_NEED_AUTHORING_DEFECT** under the exact frozen omitted-unit
precedence. All arms reach 16 required resources, 23 owning cells and 32 units
by resource support, but this manually authored need set directly covers only
15/32 units. Collective diagnostics cover 18/32; neither completes any of the
12 alternatives. On the same 15 covered units, C improves five depths and
regresses ten, increasing unique prefix resources 220 to 371 and unnecessary
occurrences 337 to 737. This is a Case-0011-local verdict on the authored set.

The [practical review](stage_d/STAGE_D_REVIEW.md), [machine trace](stage_d/trace.json)
and [human trace](stage_d/TRACE.md) form a separate Stage D layer. Original
Stage A/B traces, task gold and every C.5 source/reconciled artifact remain frozen.
The [ownership resolution](stage_d/OWNERSHIP_RESOLUTION.md) records consolidation
after the conflicting writer was terminated; [validation](stage_d/validation.md)
records the completed checks. This section supersedes earlier historical status
and the then-current adjudication status without rewriting frozen publications.

One canonical package owns inputs, metrics, diagnostics, reporting and tests:

```text
uv run python -B -m experiments.codex_dogfood.case_0011.stage_d.analyze verify
```

`build` publishes once and refuses overwrite. Verification reconstructs captured
R1.5 evidence without rerunning retrieval. It authenticates the historical
Stage A C5_PROTOCOL placeholder and its reviewed-gold preparation version at
their proper commits; the original current-worktree Stage A verifier remains
unchanged and consequently cannot replay the superseded placeholder at today's
path. `-B` keeps sterile packet directories free of import caches.

U2 exact-hint routing and U3 need/mechanism routing remain future; R1.7 remains
retained, true BM25F mandatory, and downstream Localization continuation intact.
No next increment or production behavior changed.
