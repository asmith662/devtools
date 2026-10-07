# R1.6 pre-outcome development protocol

Frozen before any alternative-parameter outcomes. Experimental evaluation only;
production retrieval, query strings/weights and Localization remain unchanged.
Primary target: RANKING_DISCRIMINATION_FAILURE. Parameter effects are mechanics,
not independent semantic relevance or witness satisfaction.

## Historical eligibility and frame

Cases 0004–0007 and 0009 are ELIGIBLE: each completed independently judged experiment
retains exact native snapshot/corpus/index inputs, full-task and every obligation
query, whole-resource canonical BM25 captures, complete obligation-relative gold,
unit linkage and acceptable ALL alternatives. The input audit pins the exact
files. All 8/9/10/11/13/9 obligations have queries; no missing query is invented.
Only native canonical lexical lanes are replayed; routing/generation/identifier
treatments are excluded. Recovery histories in Cases 0006/0008 and the clean-only
Case 0009 gold remain qualified; invalid provisional gold is never used.

Earlier Cases 0001–0003 / Increment 27 judged top-five development evidence are
PARTIALLY_ELIGIBLE for top-K variant context only, INELIGIBLE for this study's
full obligation/completion selection: their judged useful pools do not provide
the same complete REQUIRED-cell/unit/alternative contract. No confirmation or
reserve artifacts are opened. No current content substitutes for historical text.
Case 0008 is PARTIALLY_ELIGIBLE: its native baseline reproduces, but assessment-
applicability lacks obligation.py and grounding-provenance lacks resource.py in
their respective positive universes. Full max-own and full-prefix baseline ratios
are undefined. Canonical k1/b and positive filename weights cannot create absent
lexical overlap; disabling filename can only lose overlap. Keep all 180 Case 0008
points for global/reach/partial diagnostics and require reach safety there, but
omit it from complete-metric medians/minimax. The historical maximum 177 applies
only to completable obligations. This correction supersedes the initial protocol
at 985088576bbe6493e87d3be1b3ca5d012cbe9780, after baseline eligibility validation
and before any nonbaseline configuration was scored. Five selection cases plus
one supplementary case are related development tasks, not independent samples
of all coding work.

## Fixed scoring and grid

- Baseline: k1=1.2, b=0.75, filename weight=0.25.
- k1: 0.6, 0.9, 1.2, 1.5, 1.8, 2.4.
- b: 0, 0.25, 0.5, 0.75, 1.
- Filename weight: 0, 0.1, 0.25, 0.5, 1, 2.
- Full Cartesian product: 180 configurations, no new points after outcomes.

Canonical Unicode word spans/casefold, distinct query terms, positive scores,
whole-resource corpus, independent content/filename BM25 statistics, canonical
IDF/TF arithmetic and stable corpus tie order remain fixed. Only the three
parameters vary. Use existing native scorers and R1.5 decomposition/replay;
baseline ranks and scores must reproduce retained captures before grid analysis.
Index/statistics can be reused. Shared invariant term evidence plus configuration,
rank/score digests and R1.5 replay suffice to reconstruct every grid score. Keep
representative complete diagnostics, including overtakers and query footprints.

## Metrics and alternatives

Every case/configuration retains REQUIRED global resource reach, own-cell reach,
own-unit judgments/distinct-unit reach; global sufficient completion; each own
obligation's best complete ALL alternative; maximum own completion; prefix
occurrences/unique union/composition; gold minimum sufficient union and excess;
own-lane summed REQUIRED/helpful/unnecessary top-5/10/20 (denominators retained).
Global completion is the maximum of each obligation's best acceptable depth:
independently choosing one accepted alternative per obligation is valid, without
mixing members inside alternatives. Enumerate sufficient unions independently.
Tie equal-depth alternatives by frozen alternative identity. A MISS is null,
never a fabricated large rank. Incomplete own completion has no complete prefix;
report bounded observed prefixes separately and exclude from challenger selection.

Normalize global, max-own, prefix-union and prefix-occurrence metrics by that
case's current baseline. Retain exact rational numerator/denominator for selection
and absolute values. Five complete-baseline cases drive selection; Case 0008
retains available ratios only and participates in safety checks. No raw
cross-case rank sum or single quality scalar.
Report full surfaces, Pareto relationships, worst-case ratios and per-case effects.

## Challenger selection, committed code in protocol.py

Select at most three distinct nonbaseline configurations among complete,
reach-safe configurations. Safety requires no baseline REQUIRED global-resource,
own-cell or own-unit loss on any case; set differences, not just counts, are checked.

1. Completion role: minimum median max-own ratio; then worst max-own ratio;
   then median prefix-union ratio; distance; lexicographic (k1,b,weight).
2. Burden role: minimum median prefix-union ratio; then worst prefix-union ratio;
   then median max-own ratio; distance; lexicographic.
3. Robust role: minimum worst across cases of max(max-own ratio, union ratio);
   then median of these per-case worst ratios; then median global-completion
   ratio; distance; lexicographic.

Distance is the sum of absolute differences in ordinal grid index divided by
each grid's last index. It is only a tie break, not quality. Exclude baseline from
role selection; an equivalent nearest challenger is still a valid prospective
comparison, not development proof of improvement. Deduplicate and preserve roles.

## Diagnostics, cost and variants

For baseline one-factor slices and selected challengers, retain R1.5 diagnostics
for deterministic largest required rank gain/regression per case; ties use
obligation/resource identity. Explain TF saturation for k1, document/average
length for b, filename contributions/collisions for weight, and query DF/IDF/yields.
Parameter-pair surfaces summarize remaining-parameter slices; interactions are
not allocated causal effects. Diagnose failures rather than only aggregate changes.

Development grid time is analysis replay, never production runtime. Report shared
statistics/index construction separately. Prospective arms share one content/
filename index build but execute every query once per arm; capture median, p95,
sum and actual per-query scoring time. Limit median and p95 query scoring to 3x
baseline; shared index construction is identical across arms, not multiplied.
Diagnostic construction is excluded from query scoring time and measured separately.

BM25+/BM25L audit must document actual retained/library formulas, IDF, delta,
background handling, scoring provenance and judged support. A different formula
is not a parameter arm. Increment 27 BM25+ evidence and installed BM25L support
are inspected without executing a new variant benchmark. Preserve their open
questions and make an explicit before-BM25F sequencing decision in the audit.

## New prospective Case 0010

After development analysis/selection is committed, freeze a realistic new task
with source/test/docs/config obligations and identical caller-authored queries
for all arms. Export the starting R1.5 Git snapshot (before this development
analysis), using broad established source/test/docs/config eligibility. Exclude
experiments, research/reports, confirmation/reserve and this study's metadata.
Task selection must not inspect prospective gold or treatment ranks. Do not
implement the task. Baseline plus unique selected challengers; no post-execution arm.

Freeze Stage A before executing each arm exactly once. No effectiveness join
before independent sterile Stage C. A future parameter candidate requires:
no REQUIRED resource/cell/unit loss; global and max-own depths <=1.05x baseline;
at least 10% prefix-union OR max-own improvement; no obligation depth >1.25x;
at least half obligations nonworse; median/p95 query cost <=3x; development
worst max-own/union ratio <=1.25 (avoids a clear historical pathology).
These gates justify later adoption consideration, not production changes.

Future outcomes: NONBASELINE_PARAMETER_CANDIDATE if any challenger passes;
BASELINE_ROBUST if all challengers are reach-safe, all global/max-own/union ratios
are within 0.95–1.05 and none passes meaningful improvement; otherwise
MIXED / NO SAFE REPLACEMENT. A verified scorer/identity defect stops the study
as CONCRETE SCORING DEFECT. Do not evaluate these outcomes before gold.

Build a full-frame treatment-free packet using explicit archive_sha256 and
canonical_payload_sha256. Validate whitelist/leakage and deterministic double
build; prepare a new external sterile directory with only blind inputs, no Git,
treatment links or outputs. STOP before Case 0010 Stage C. R1.7 follows R1.6's
prospective completion; R2 remains mandatory, Localization continuation unchanged.
