# Case 0008 Stage D joined analysis

This report joins the frozen Stage A treatment, the qualified Stage B recovery capture, Stage B.5 packet, and independent Stage C judgments. It does not change or rerun them.

## 1. Integrity and recovery qualification

Starting HEAD was `c7df5f50c16433cbaff9c0d9bd013b9833f03670`. Identity join: 523/523 resources, 13/13 obligations, 11/11 grounding anchors, 14/14 lexical lanes, 13/13 routed lanes, 29/29 generation specs, and 6799/6,799 resource/obligation cells. Duplicate, missing and unexpected identities are all zero. Routed candidates map to and preserve their exact native candidates; the global lane is unchanged. All generated targets and support sources join to the frozen snapshot. Reference fact IDs and Import relation IDs/source modules/dependency targets validate against the frozen provenance.
Verified ancestry: Stage A `3eda8c6027f72a51109ed78f5684a6bbb59c65bd`; generation-recovery protocol `3d6cb9597742ebd78946d1291f145770904b2248`; Stage B recovery `348887c5e8f9969259734563319bb2d6ec715a3f`; Stage B.5 `9eb910d2c9dc6fa0947e6640917c8072ed4ba010`; Stage C `c7df5f50c16433cbaff9c0d9bd013b9833f03670`. All are ancestors of the starting HEAD and frozen artifact Git blobs equal the clean checkout. Committed Stage A/Stage B integrity entries and all named blind/Stage C SHA-256 digests match. The recovery raw and `stage_b.md` actual digests are recorded in JSON but were not separately pinned by the canonical Stage B integrity artifact.

Recovery provenance is `GENERATION_RECOVERY` (`case-0008-stage-b-generation-recovery-1`), original execution `2fed596a-f43d-4d35-9e32-e8a609366a6f`. The initial generation attempt failed before projection during harness alias validation and exposed no candidate output. Generation-only recovery was pre-frozen, invoked once, durably captured, and left treatment unchanged; lexical retrieval, routing and grounding were reused without rerun. Generation took 1316.840868 seconds. The canonical integrity record does not independently list the recovery raw archive digest; it does pin all five canonical Stage B outputs. This is recorded as a limitation.

## 2. Blind gold

Stage C says all 13 obligations apply. Gold contains 35 distinct REQUIRED information units, 71 obligation-relative REQUIRED unit judgments, 22 unique REQUIRED resources across alternatives, 50 REQUIRED cells, 54 HELPFUL_ONLY cells, 6,695 UNNECESSARY cells and zero unresolved cells. All REQUIRED judgments were inferable at task start; inherent discovery and task-interpretation gaps are zero. Gold has 15 acceptable alternatives and four cross-obligation combinations: two have 21-resource unions and two have 22-resource unions.

## 3. Lexical baselines

The global positive surface has 520 resources. Global task-complete depth is 361; the full 22-resource required universe completes at depth 361; the two minimum 21-resource combinations complete at depths [361, 361]. Own-obligation native maximum best completion depth is 177; its prefixes sum to 552 occurrences, union to 241 resources (241/21, +220), and include 41 REQUIRED, 28 helpful and 483 unnecessary cells. Per-alternative and per-obligation depths, reach/misses, and every REQUIRED occurrence's global/native rank are in `analysis.json`.

## 4. Role routing

Maximum routed completion position is 243. Routed prefixes sum to 950 occurrences, union to 394 resources (394/21, +373), with 41 REQUIRED, 20 helpful and 889 unnecessary cells. Versus native best depths, 3 obligations improve, 7 are unchanged and 3 worsen. Case 0008 strengthens parking role routing as a primary discriminator: the routed prefix union is substantially larger and maximum completion depth is worse, while the frozen safety lanes remain intact.

## 5. Operator surfaces

| Surface | Type | Unique candidates | REQUIRED cells | REQUIRED unit judgments | Distinct units | Complete obligations | Unique REQUIRED resources |
|---|---|---:|---:|---:|---:|---:|---:|
| Global lexical completion | ranked | 520 positive surface | 50 | 71 | 35 | 13/13 @ 361 | 22 |
| Own-native prefixes | ranked | 241 | 41 | — | — | 13/13 @ 177 | — |
| Routed prefixes | ranked | 394 | 41 | — | — | 13/13 @ 243 | — |
| OWNER/MIRROR | unranked | 9 | 14 | 23 | 18 | 2/13 | 8/22 |
| OWNER/MIRROR/REFERENCE | unranked | 14 | 14 | 23 | 18 | 2/13 | 8/22 |
| OWNER/MIRROR/IMPORT | unranked | 14 | 15 | 24 | 19 | 2/13 | 10/22 |
| ALL FOUR | unranked | 19 | 15 | 24 | 19 | 2/13 | 10/22 |
| Gold lower bound | semantic | 21 | full | 71 | 35 | 13/13 | 22 |

OWNER covers 14/50 REQUIRED cells, 23/71 unit judgments, 18/35 units and 8/22 unique required resources; it completes candidate-integration and readiness-integration. MIRROR covers 0 REQUIRED cells/units/resources. REFERENCE covers 0 REQUIRED cells/units/resources. IMPORT covers 2/50 cells, 3/71 judgments, 3/35 units and 4/22 resources (some resource coverage occurs in the wrong obligation). OWNER/MIRROR equals OWNER for REQUIRED coverage. Adding Reference leaves those values unchanged. Adding Import raises combined coverage to 15/50 cells, 24/71 judgments, 19/35 units and 10/22 resources.
Package-api is applicable. OWNER alone reaches the existing public facade and covers 1 of its 2 REQUIRED unit judgments; the complementary ownership ADR remains missing, so the frozen alternative is incomplete. This supports respecting the existing facade, not inventing a separate package-export projection.

## 6. Reference marginal

Over OWNER/MIRROR, Reference adds 11 obligation/resource cells and 5 resources: zero REQUIRED cells, unit judgments, distinct units or unique REQUIRED resources; 3 helpful and 8 unnecessary cells. Cell and unique-required-resource yields are both 0%. It newly completes no obligation and makes no additional obligation resource-set-reachable. Mechanical outcomes: 8 families, 6 zero-target, 2 several-target, 12 children, 6 distinct targets, median fanout 0.0, maximum 6, and zero result/work overflows. The Case 0007 low marginal REQUIRED-cell result replicated in Case 0008.

| Reference family | Obligation | Seed | Outcome | Targets | Children | R/H/U target cells | New complete/reachable |
|---|---|---|---|---:|---:|---|---|
| frontier-consumers | frontier-semantics | assessment | NO_TARGET | 0 | 0 | 0/0/0 | False/False |
| assessment-consumers | assessment-applicability | assessment | NO_TARGET | 0 | 0 | 0/0/0 | False/False |
| candidate-consumers | candidate-integration | candidate | NO_TARGET | 0 | 0 | 0/0/0 | False/False |
| accepted-witness-consumers | witness-boundary | witness | NO_TARGET | 0 | 0 | 0/0/0 | False/False |
| grounding-consumers | grounding-provenance | grounding | NO_TARGET | 0 | 0 | 0/0/0 | False/False |
| frame-consumers | frame-identity | frame | NO_TARGET | 0 | 0 | 0/0/0 | False/False |
| readiness-consumers | readiness-integration | readiness | MULTI_TARGET | 6 | 6 | 0/1/5 | False/False |
| tests-readiness-consumers | tests | readiness | MULTI_TARGET | 6 | 6 | 0/3/3 | False/False |

The zero-target result is exact to each captured seed. The capture cannot distinguish global absence of a referential fact from a seed mismatch; the blind gold does not label witness information by relation type. No generic Reference failure is inferred.

## 7. Import marginal

Import over OWNER/MIRROR adds 6 cells and 5 resources: +1 REQUIRED cell, +1 unit judgment, +1 distinct unit and +2 unique REQUIRED resources; it adds one helpful and four unnecessary cells. Yields are 16.7% of new cells and 40.0% of new resources. Over OWNER/MIRROR/REFERENCE it adds the same +1 REQUIRED cell, +1 unit judgment, +1 distinct unit and +2 unique REQUIRED resources, with 6 cells and 5 resources total; yields are the same. Neither comparison newly completes an obligation nor creates new resource-set reachability. Mechanical outcomes: 6 families, 3 zero-target, 3 several-target, 7 children, 7 distinct targets, median fanout 1.0, maximum 3, and zero result/work overflows. This is measurable but not substantial task-level value.

| Import family | Obligation | Seed | Source module | Outcome | Targets/children | R/H/U target cells | Required targets |
|---|---|---|---|---|---:|---|---|
| frontier-dependencies | frontier-semantics | assessment | — | NO_TARGET | 0/0 | 0/0/0 | False |
| assessment-dependencies | assessment-applicability | assessment | — | NO_TARGET | 0/0 | 0/0/0 | False |
| candidate-dependencies | candidate-integration | candidate | src/devtools/context/localization/association/hypothesis.py | MULTI_TARGET | 2/2 | 0/0/2 | False |
| grounding-dependencies | grounding-provenance | grounding | src/devtools/context/localization/grounding/view.py | MULTI_TARGET | 2/2 | 1/1/0 | True |
| frame-dependencies | frame-identity | frame | — | NO_TARGET | 0/0 | 0/0/0 | False |
| readiness-dependencies | readiness-integration | readiness | src/devtools/context/localization/readiness.py | MULTI_TARGET | 3/3 | 1/0/2 | True |

The three zero-target Import families are frontier-semantics/assessment, assessment-applicability/assessment and frame-identity/frame. They establish no direct dependency result for those exact seeds. The blind packet does not determine whether another seed would have yielded a required target or whether those required contracts are dependency-shaped. The three several-target families are candidate-integration (2, no required target), grounding-provenance (2, one REQUIRED plus one helpful target) and readiness-integration (3, one REQUIRED target); each family's remaining targets are unnecessary in its obligation context. These direct dependencies do correspond to some gold complementary contracts (grounding contract and readiness assessment), but they do not complete new obligations.

## 8. Hypothesis structure

Across 28 hypotheses the classifications are {'PARTIAL_MATCH': 7, 'NO_GOLD_MATCH': 18, 'EXACT_STRUCTURAL_MATCH': 3}. There are no RESOURCE_MATCH_WRONG_STRUCTURE cases: the observed pattern is limited candidate match (3 exact, 7 partial, 18 with no gold alternative resource match), rather than systematic mis-authored complementarity. All-four structural hypotheses completely satisfy blind alternatives for candidate-integration, readiness-integration; resource-set reachability identifies the same two obligations, so no additional obligation has its resources scattered across the surface while lacking one complete hypothesis. No operator combination completes the overall 13-obligation sufficient witness combination. Recipe-level details and operator-family alignment are retained in `analysis.json`.

## 9. Miss analysis

All-four structural coverage leaves 35 REQUIRED obligation/resource cells uncovered. The nonoverlapping primary causes are {'NO_RECIPE': 12, 'OPERATOR_CAPABILITY_GAP': 23}: 12 cells have no structural recipe (acquisition-contract, orchestration-boundary, documentation and validation); 23 are not reached by the frozen typed projections. Of the misses, 14 are Markdown authority/documentation resources. No miss is assigned to work/result overflow or recovery failure. The captures do not establish that a missed resource is reachable by an untested direct relation; zero missed witnesses are clearly shown to require another deterministic typed relation. Import subcategories in JSON are scoped to the captured seeds. Gold states required information, not that a direct import is itself a required witness relation.

## 10. Operator reachability

At least one structural operator reaches 19 unique resources in total, including 10 resources REQUIRED somewhere. Import has 2 targets also in OWNER, 0 also in MIRROR, 0 also in REFERENCE, and 5 unique-to-Import targets. OWNER carries the broadest correctly assigned required coverage. Import adds distinct resources, but most marginal cells are unnecessary and no new obligation is completed. Per-obligation labels for all unique Import targets and the resource-level operator reachability matrix are in `analysis.json`. All 11/11 grounded owner resources are REQUIRED somewhere; across captured seed/recipe contexts, 18 seed-obligation contexts have REQUIRED owner relevance. This checks seed quality, not candidate sufficiency.

## 11. Candidate efficiency

| Surface | Unique resources | Relative to 21 | Excess/shortfall |
|---|---:|---:|---:|
| Own-native | 241 | 241/21 | +220 |
| Routed | 394 | 394/21 | +373 |
| OWNER/MIRROR | 9 | 9/21 | -12 |
| OWNER/MIRROR/REFERENCE | 14 | 14/21 | -7 |
| OWNER/MIRROR/IMPORT | 14 | 14/21 | -7 |
| ALL FOUR | 19 | 19/21 | -2 |

The actual all-four union is 19 resources, so it cannot equal any sufficient gold combination of at least 21 resources. It intersects each of the two minimum combinations by 10/21 (Jaccard 0.333); each minimum combination has 11 required resources missing and 9 structural extras. The 19-versus-21 cardinality check is conclusive even before obligation-relative structure: no complete sufficient combination is realized.

## 12. Generation cost

Recovery generation took 1316.840868 seconds. Captures provide separate lexical, routing and grounding invocation timings, but no per-operator generation component timings, so this runtime cannot be assigned to OWNER, MIRROR, Reference or Import. A replay/validation cost concern is reasonable to track, but optimization should follow the value decision; this Stage D task made no optimization change.

## 13. Stopping decision

Import adds some direct dependency evidence but the all-four 19-resource union is smaller than every sufficient gold union, covers only a subset of obligation-relative required cells, and assembles no complete sufficient task combination. Remaining mandatory acquisition, orchestration, documentation and validation witnesses are policy/authority evidence without natural deterministic structural reach. Continue with structural hypotheses plus lexical/other acquisition candidates feeding evidence-to-witness resolution; do not expand relations from this case.

Keep OWNER, MIRROR, REFERENCE and IMPORT as bounded native evidence/candidate channels; stop expanding structural breadth on this evidence. The next phase should test evidence-to-witness resolution over generated hypotheses plus lexical safety candidates and other acquisition evidence, using obligation criteria and accepted witness algebra. Resolution cannot recover absent candidates, so structural hypotheses must be combined with the lexical safety lane rather than treated as a complete candidate source. This is not an automatic ranking or resolution policy recommendation.

## 14. Limitations

The data describe one frozen repository snapshot. The Stage B generation results are a generation-only recovery capture, not a clean one-pass execution; the first attempt failed before candidate projection and provides no effectiveness evidence. The recovery raw file lacks a separate canonical SHA-256 pin. No confirmation outcome was accessed. The analysis did not rerun any lane/operator, alter treatment/judgments/source, implement the task or implement this recommendation. The packet records a historical implementation ledger outside the eligible frame as a limitation; confirmation remains sealed.
