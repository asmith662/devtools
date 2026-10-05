# Case 0007 Stage D joined analysis

## 1. Experiment integrity

Verified chain: `e495c0af → 3e22a159 → ba6a035a → 005b4348`; all pinned digests and internal Stage A/B/C integrity records match.
Exact join: 521/521 resources; 11/11 obligations; 9/9 anchors; 12/12 lanes; 11/11 routed lanes; 9/9 grounds; 25/25 specs; 5,731/5,731 cells. Duplicate identities: 0; missing/unexpected identities: 0. Routed candidates map one-to-one to native candidates; generated targets and Reference supports join the frozen snapshot.
Stage B mechanics recompute as {'generated': 20, 'result-bound-exceeded': 3, 'no-target': 2}; 16 fixed hypotheses, 9 Reference families, 16 children, 32 hypotheses, 40 member occurrences, and 19 unique structural resources.

## 2. Blind gold

All obligations are APPLICABLE. Gold has 30 distinct REQUIRED units, 56 obligation-relative unit judgments, 27 unique required resources, 55 REQUIRED cells, 78 HELPFUL_ONLY cells, and 5,598 UNNECESSARY cells. Unresolved, inherent discovery, and task gaps are all zero.
The 432 acceptable combinations span 19–24 resources; 4 combinations have the minimum size of 19.

| Obligation | Applicability | Distinct REQUIRED units | Unit judgments | REQUIRED cells |
|---|---|---:|---:|---:|
| declaration-identity | APPLICABLE | 3 | 3 | 3 |
| binding-reexports | APPLICABLE | 4 | 4 | 4 |
| module-membership | APPLICABLE | 2 | 2 | 2 |
| explicit-exposure | APPLICABLE | 8 | 8 | 8 |
| unsupported-behavior | APPLICABLE | 5 | 5 | 5 |
| snapshot-provenance | APPLICABLE | 8 | 8 | 8 |
| reference-integration | APPLICABLE | 4 | 4 | 4 |
| package-api | APPLICABLE | 4 | 4 | 4 |
| tests | APPLICABLE | 13 | 13 | 12 |
| documentation | APPLICABLE | 4 | 4 | 4 |
| validation | APPLICABLE | 1 | 1 | 1 |

## 3. Lexical baselines

Global native ranking has 518 positive resources. Task completion is at depth 346; the complete 27-resource alternative universe and best 19-resource sufficient combination also complete at depth 346 and 346, respectively. The global task-completion prefix contains 346 unique resources.
Own-native maximum completion depth is 192; obligation prefixes total 661 occurrences and 249 unique resources (+230 over 19; 13.11×). Prefix labels: {'HELPFUL_ONLY': 59, 'REQUIRED': 47, 'UNNECESSARY': 555}.
Routed maximum completion position is 255; prefixes total 796 occurrences and 378 unique resources (+359 over 19; 19.89 times). Prefix labels: {'HELPFUL_ONLY': 53, 'REQUIRED': 49, 'UNNECESSARY': 694}.
Routing improved 4 obligations (declaration-identity, binding-reexports, snapshot-provenance, package-api), left 4 unchanged, and worsened 3 (explicit-exposure, reference-integration, tests).

## 4. Actual structural surfaces

| Surface | Unique resources | Obligation/resource cells | REQUIRED cells / 55 | REQUIRED unit judgments / 56 | Distinct REQUIRED units / 30 | Complete obligations |
|---|---:|---:|---:|---:|---:|---:|
| OWNER | 8 | 11 | 10 | 10 | 9 | 1/11 |
| MIRROR | 5 | 5 | 0 | 0 | 0 | 0/11 |
| REFERENCE | 8 | 8 | 0 | 0 | 0 | 0/11 |
| OWNER_MIRROR | 13 | 16 | 10 | 10 | 9 | 1/11 |
| ALL | 19 | 24 | 10 | 10 | 9 | 1/11 |

Full structural output has 19 unique resources and 24 obligation/resource cells. It covers 9/27 required resources somewhere, but only 10/55 correctly assigned REQUIRED cells and 10/56 unit judgments. The 19-resource union intersects the four minimum sufficient combinations by 5, 5, 5, and 6 resources; it equals none. Only package-api has a complete generated witness alternative. Module-membership has resource-set reachability but no single hypothesis with the complete pair.
The actual structural union is 1.00 times the minimum sufficient resource count by cardinality. That equality is not sufficiency: the best identity intersection is 6/19, with no complete minimum combination and no complete 11-obligation combination.

| Surface | Type | Candidate surface | REQUIRED cells | Complete obligations |
|---|---|---:|---:|---:|
| Global lexical completion | Ranked prefix | 346 | 55/55 | 11/11 |
| Own-native prefixes | Ranked, obligation-local | 249 | 47/55 | 11/11 |
| Routed prefixes | Ranked, obligation-local | 378 | 49/55 | 11/11 |
| OWNER/MIRROR | Unranked structural | 13 | 10/55 | 1/11 |
| OWNER/MIRROR/REFERENCE | Unranked structural | 19 | 10/55 | 1/11 |
| Sufficient gold bound | Semantic lower bound | 19–24 | 55/55 | 11/11 |

## 5. Marginal Reference contribution

Relative to OWNER/MIRROR, Reference adds 8 cells and 6 unique resources. Added-cell labels: {'HELPFUL_ONLY': 2, 'UNNECESSARY': 6}. New REQUIRED cells and unit judgments: 0 and 0; new distinct REQUIRED units: 0. It adds 1 unique resource that occurs in REQUIRED gold somewhere, but zero REQUIRED cells in its generated obligation. It adds 2 helpful resources and 5 unique resources never REQUIRED. Cell yield is 0.000; unique-resource yield is 0.167.
Reference creates 0 new complete obligations and 0 newly complete alternatives. The one resource-set-only obligation remains module-membership; no Reference child supplies its full witness structure.

## 6. Reference family-by-family results

Targets below are exact distinct diagnostic targets. Only generated children count as observed output.

| Family | Obligation | Seed | Result | Targets | Work | Children | REQUIRED / helpful / unnecessary targets | Complete alternative in child |
|---|---|---|---|---:|---|---:|---|---|
| owner-plus-reference-g-binding | binding-reexports | g-binding | generated | 2 | 407/4096 complete=True | 2 | 0 / 1 / 1 | none |
| references-g-binding | binding-reexports | g-binding | generated | 2 | 407/4096 complete=True | 2 | 0 / 1 / 1 | none |
| owner-plus-reference-g-membership | module-membership | g-membership | generated | 6 | 407/4096 complete=True | 6 | 0 / 1 / 5 | none |
| references-g-membership | module-membership | g-membership | generated | 6 | 407/4096 complete=True | 6 | 0 / 1 / 5 | none |
| owner-plus-reference-g-module | snapshot-provenance | g-module | result-bound-exceeded | 20 | 407/4096 complete=True | 0 | 0 / 4 / 16 | none |
| references-g-module | snapshot-provenance | g-module | result-bound-exceeded | 20 | 407/4096 complete=True | 0 | 0 / 4 / 16 | none |
| owner-plus-reference-g-reference | reference-integration | g-reference | no-target | 0 | 407/4096 complete=True | 0 | 0 / 0 / 0 | none |
| references-g-reference | reference-integration | g-reference | no-target | 0 | 407/4096 complete=True | 0 | 0 / 0 / 0 | none |
| package-plus-module-consumer | package-api | g-module | result-bound-exceeded | 20 | 407/4096 complete=True | 0 | 0 / 0 / 20 | none |

## 7. Overflow and no-target diagnostics

All three result-bound overflows retained 20 exact targets each; none contains a REQUIRED resource for its obligation. Across the three diagnostic sets, admitting all targets would add 60 child candidates, 40 distinct obligation/resource cells ({'HELPFUL_ONLY': 4, 'UNNECESSARY': 36}), and 20 unique resources. It would add 52 unnecessary target occurrences, zero REQUIRED cells/units/resources, and no new complete obligation or alternative. The union would grow to 31 resources. This post-hoc calculation is not observed treatment.
The two no-target families both used g-reference (the derivation function) and completed the exact search with zero targets. A frozen source import shows `references/declarations/analysis.py` imports the exact `PythonDeclarationReferenceKnowledge` class grounded by g-reference-fact. That is an evidence-backed alternate Reference seed candidate, but no projection was run and the same analysis.py resource was already generated as an OWNER in reference-integration, so no new resource-cell credit is assigned. The missing route file `references/declarations/resolution.py` is reached by the direct-import relation; `references/docs/overview.md` is a documentation contract, not a referencer target.

## 8. Witness-structure alignment

Across 32 generated hypotheses: {'PARTIAL_MATCH': 17, 'NO_GOLD_MATCH': 14, 'EXACT_STRUCTURAL_MATCH': 1}. At the obligation-level, module-membership is RESOURCE_MATCH_WRONG_STRUCTURE: separate owner hypotheses collectively contain its alternative resources, but none contains the complementary pair. A complete 19-resource combination is not realized; no full 11-obligation combination is resource-set complete.

## 9. Miss classification

Of 55 REQUIRED cells, 45 remain uncovered. Non-overlapping primary causes: {'PROJECTION_ABSTAINED': 21, 'NO_RECIPE': 13, 'PROJECTION_NO_TARGET': 2, 'CROSS_ROLE_NONSTRUCTURAL': 9}; the counts sum to 45. No overflow miss is assigned because none of the overflowed targets is REQUIRED in its obligation. `NO_RECIPE` accounts for explicit-exposure, documentation and validation paths; cross-role candidates do not count for another obligation.
Reference-specific causes across required misses: {'REQUIRES_OTHER_TYPED_RELATION': 6, 'EXACT_REFERENCE_FACT_ABSENT': 13, 'NO_REFERENCE_RECIPE': 33, 'WRONG_REFERENCE_SEED': 1, 'WITNESS_NOT_REFERENTIAL': 2}. The six currently missing resources found by the direct-import probe are `REQUIRES_OTHER_TYPED_RELATION`; the reference overview is `WITNESS_NOT_REFERENTIAL`.

## 10. Operator reachability

All 9 exact grounded owners are REQUIRED somewhere in the gold (8 distinct owner resources because the module interpretation owner is grounded twice). Eight of nine grounding requests participate in at least one recipe obligation where their owner is REQUIRED; g-module-identity is helpful-only in its snapshot recipe. Owner resources yield 10 required cells. Mirror yields zero required cells. Reference yields zero required cells, although one added resource is REQUIRED under a different obligation. Reachability partition: {'REQUIRES_OTHER_TYPED_RELATION': 6, 'OWNER_REACHABLE': 10, 'NONSTRUCTURAL_OR_POLICY': 39}. The residual bucket means no typed route was proven here, not that every such resource is ontologically nonstructural.

### Direct static import relation probe (counterfactual, not treatment)

A one-hop source-import scan over frozen contents sees 51 edges across grounded owner/obligation pairs, maximum fanout 9. It reaches 6 currently missing REQUIRED cells (6 unit judgments), including: binding-reexports:src/devtools/context/python/imports/declarations.py, binding-reexports:src/devtools/context/python/imports/resolution.py, reference-integration:src/devtools/context/python/references/declarations/resolution.py, snapshot-provenance:src/devtools/context/repository/identity.py, snapshot-provenance:src/devtools/context/repository/resource.py, snapshot-provenance:src/devtools/context/repository/snapshot.py. The resulting candidate resource union would be 28 before any recipe structure review. This is static evidence supporting one bounded relation family, not a generated result.

## 11. Runtime and cost

The complete Stage B generation call took 1,130.740 seconds. Per-component projection, grounding replay, support validation, candidate-association validation, and serialization times were not captured; no attribution is made.

## 12. Architectural decision

Decision: CONTINUE STRUCTURAL BREADTH with exactly one next relation family: direct one-hop static Python import dependency. The blind archive shows bounded fanout (maximum 9) and exact missing REQUIRED targets in binding, module-membership, snapshot-provenance, and Reference integration. Do not add a general documentation graph. After this relation is evaluated, assess witness assembly; Case 0007 alone does not justify a general evidence resolver yet because only 10/55 required cells are present in observed structural output.
Reference value is LOW for this observed treatment: zero new REQUIRED cells, zero new complete obligations, and 6 new resources for 8 cells. The unprojected g-reference-fact seed limits what can be concluded about the operator itself. Overflow did not matter. Routing worsened three obligations and expanded its unique prefix union from 249 to 378; this is further evidence to park routing as a primary discriminator, not to remove it in this analysis.
This case does not justify changing result bounds, treating the numerical 19=19 match as sufficiency, implementing public-export RI, or accessing confirmation.

## Limitations

- The eligible frame contains no docs/implementation_ledger.md or historical reports/research artifacts linked by documentation. Their contents and any additional historical handoff requirements cannot be adjudicated; no extra mandatory witness is invented.
- No export implementation or export-specific tests exist in this packet. Static list __all__ is demonstrated in RI facades; an annotated empty tuple occurs in the benchmark facade. The search also finds a dynamic __all__ fixture in a different bounded RI test. These examples do not supply a complete future language for static __all__, reassignment/mutation, unsupported __getattr__, or general public API policy; the task authorizes conservative bounded design, not inference from every occurrence.
- Imported-member resolution's function-only one-facade contract is narrower/different from shared conservative direct class/function binding lookup. Its target selection is native declaration matching, not a universal runtime/decorator binding proof. Preserve the actual contracts; do not silently broaden or repair existing RI under the export task. No execution outcomes or future validation pass/fail evidence are available or claimed.
- Independent session work used only the supplied user task and blind packet. Runtime model identity/effort is selected by the host; the adjudication artifacts make no unverifiable model or session-reset attestation.
- Captured generation timing covers the full generation call; no component timings separate projection, grounding replay, support validation, association validation, or serialization.
- Resource-level witness completion tests exact obligation/resource membership in one generated hypothesis; fine-grained unit coverage is reported separately.
- Overflow targets are used only in the labeled post-hoc counterfactual and never counted as observed generated children.

Confirmation outcomes were not accessed. Treatment was not rerun. No production source or frozen Stage A/B/B.5/C artifact was modified.
