# Case 0006 Stage D joined analysis

## 1. Frozen experiment integrity

Verified chain: Stage A `e7aed4162672dd859a0a8a33a2b718dda8425495` → recovery protocol `56f18901b5acae47b9c07811dd18eb4770c56285` → recovery capture `aae9da9741924dfa599b55b4fb913163caf96131` → Stage B.5 `e076632a5e38d9d598c0fc109a12b52b424ecf22` → Stage C `e3c1fa5144e318a2ee5985bfaf5730833ef43d4d`.
All 21 listed/pinned artifacts match their frozen digests and committed blobs. Starting checkout was clean `main` at `e3c1fa5144e318a2ee5985bfaf5730833ef43d4d`.
Recovery provenance: execution kind RECOVERY, ID `case-0006-stage-b-recovery-1`, prior failed execution count 1. Attempt 1 failed in the experiment harness's complementary-member list-order correspondence after treatment and before persisting semantic outputs. The preauthorized recovery matched by frozen member identity/key; treatment remained byte-identical and recovery outputs were durably captured. No effectiveness impact is inferred.

## 2. Primary frozen measurements

Identity joins: resources 531/531; obligations 10/10; shared anchors 10/10; lexical lanes 10/10; role preferences 10/10; grounding requests 9/9; recipes 9/9; gold cells 5,310/5,310. Duplicate, missing and unexpected resource identities: 0. All 2,069 routed-lane candidates map to exact native candidates and survive routing; the global lane is unchanged.
Gold: 22 distinct required units, 33 required unit judgments, 18 unique required resources, 28 REQUIRED cells, 25 HELPFUL_ONLY cells, and 5,257 UNNECESSARY cells. All ten obligations apply. There are four valid combinations of alternatives, each with 20 units in 16 resources (minimum and maximum sufficient union both 16). No unresolved gold, inherent discovery, or task-interpretation gap.

## 3. Baseline lexical and routing comparison

Global native BM25 has 528 positive-match candidates and reaches 33/33 REQUIRED unit/resource occurrences. Best acceptable completion depths by obligation: hypothesis-records 20, member-complementarity 73, generated-integration 80, accepted-promotion 73, assessment-readiness 73, provenance-frame 155, package-integration 78, tests 43, documentation 7, validation 67. Global task-complete obligation depth: **155**. Full 18-resource witness-universe depth: 155; best 16-resource gold combination depth: 155.
Own-obligation native maximum of the ten independently best completion depths: **58**. Routed maximum of ten best completion positions: **195**. Routing changed obligation completion positions: 6 improved, 3 unchanged, 1 worsened; empty validation-role preference control: True.
Native prefixes: 205 summed occurrences, 81 unique resources (5.06× the 16-resource sufficient bound; excess 65). Routed prefixes: 284 summed occurrences, 216 unique resources (13.50×; excess 200). Prefix cell classes are retained per obligation in JSON.

| Surface | Candidate surface type | Size | Required coverage | Complete-obligation coverage |
| --- | --- | ---: | ---: | ---: |
| Global lexical | ranked native BM25 | 528 | 33/33 unit/resource occurrences | 10/10 at task-complete depth 155 |
| Own native prefixes | ranked prefixes | 81 unique; 205 occurrences | 28/28 REQUIRED cells in prefixes | 10/10; max depth 58 |
| Routed prefixes | ranked prefixes | 216 unique; 284 occurrences | 28/28 REQUIRED cells in prefixes | 10/10; max position 195 |
| Actual generation | unranked set | 0 | 0/28 | 0/10 |
| Sufficient gold bound | semantic lower bound | 16 | 100% by definition | 10/10 |

## 4. Actual generation result

Observed recovery output: 9 recipes, 14 member attempts (12 OWNER_RESOURCE and 2 MIRRORED_RESOURCE); all 9 recipes and 14 members ended `unsupported-source`. Generated hypotheses 0, member occurrences 0, unique targets/resources 0, and generated obligation/resource occurrences 0. REQUIRED resource-cell coverage 0/28; REQUIRED unit-judgment coverage 0/33; unique REQUIRED resources 0/18; complete acceptable witness structures 0/10. Generated precision is **undefined** because there are zero generated candidates.

## 5. Grounding failure diagnosis

Eight exact Python declaration locators were supported locator forms, matched an exact module in the frozen 399-interpretation universe, and produced native `PythonModuleDeclarationLookup` evidence. All eight named classes exist once as direct module-body ClassDefs in the frozen snapshot. Each has a decorator (`@dataclass`); the frozen class RI emits `PythonClassDeclarationKnowledge` for direct ClassDefs, but `lookup_python_module_declaration` appends an unsupported binding marker for every decorated direct definition before consulting that class fact. The lookup returns NOT_DECLARATION, which `_ground_declaration` maps to UNSUPPORTED with the captured generic reason. Primary classification for all eight: **DECLARATION_KIND_MISMATCH**. This is not a missing module universe, locator spelling mismatch, absent class, or public-export path mismatch.
| Request | Anchor → exact declaration | Frozen owner resource | Disposition | Captured reason | Gold relevance |
| --- | --- | --- | --- | --- | --- |
| g-hypothesis | hypothesis → `devtools.context.localization.association.hypothesis.CandidateWitnessHypothesis` | `src/devtools/context/localization/association/hypothesis.py` | unsupported | Relevant syntax cannot establish the requested direct declaration. | hypothesis-records=REQUIRED, member-complementarity=REQUIRED, generated-integration=REQUIRED, accepted-promotion=REQUIRED, provenance-frame=REQUIRED, tests=REQUIRED |
| g-candidate-view | candidate-view → `devtools.context.localization.association.hypothesis.CandidateWitnessView` | `src/devtools/context/localization/association/hypothesis.py` | unsupported | Relevant syntax cannot establish the requested direct declaration. | hypothesis-records=REQUIRED, member-complementarity=REQUIRED, generated-integration=REQUIRED, accepted-promotion=REQUIRED, provenance-frame=REQUIRED, tests=REQUIRED |
| g-generation-view | generation-view → `devtools.context.localization.generation.contract.WitnessGenerationView` | `src/devtools/context/localization/generation/contract.py` | unsupported | Relevant syntax cannot establish the requested direct declaration. | generated-integration=REQUIRED |
| g-grounding-view | grounding-view → `devtools.context.localization.grounding.view.AnchorGroundingView` | `src/devtools/context/localization/grounding/view.py` | unsupported | Relevant syntax cannot establish the requested direct declaration. | generated-integration=REQUIRED |
| g-witness-set | witness-set → `devtools.context.localization.obligation.WitnessSet` | `src/devtools/context/localization/obligation.py` | unsupported | Relevant syntax cannot establish the requested direct declaration. | member-complementarity=REQUIRED, accepted-promotion=REQUIRED, assessment-readiness=REQUIRED |
| g-supported-witness | supported-witness → `devtools.context.localization.assessment.SupportedWitness` | `src/devtools/context/localization/assessment.py` | unsupported | Relevant syntax cannot establish the requested direct declaration. | accepted-promotion=REQUIRED, assessment-readiness=REQUIRED, provenance-frame=REQUIRED |
| g-assessment | assessment → `devtools.context.localization.assessment.LocalizationAssessment` | `src/devtools/context/localization/assessment.py` | unsupported | Relevant syntax cannot establish the requested direct declaration. | accepted-promotion=REQUIRED, assessment-readiness=REQUIRED, provenance-frame=REQUIRED |
| g-readiness | readiness → `devtools.context.localization.readiness.LocalizationReadiness` | `src/devtools/context/localization/readiness.py` | unsupported | Relevant syntax cannot establish the requested direct declaration. | assessment-readiness=REQUIRED, tests=REQUIRED |
| g-validation | quality → `scripts/validate_development.py` | `scripts/validate_development.py` | resolved | Exact address identifies one observed resource occurrence. | HELPFUL_ONLY |

All eight failed declaration-owning resources appear in at least one 16-resource sufficient union, and all are REQUIRED for at least one obligation (see the full per-obligation classification in JSON). The ninth request, `g-validation`, resolved its exact address `scripts/validate_development.py`; that file is HELPFUL_ONLY for the validation obligation, while the REQUIRED validation contract is documented in `docs/development/validation.md`.

## 6. Gold miss classification

Every actual required resource cell is missed. Primary causes partition the 28 cells without double-counting: GROUNDING_UNSUPPORTED 12, NO_RECIPE 8, OPERATOR_CAPABILITY_GAP 8. Grounding also contributes to 8 operator-limited cells, so contributing reasons overlap and are not added to the primary total.
Per-obligation: hypothesis-records TREATMENT_ADDRESSABLE (1 required resource cells); member-complementarity TREATMENT_ADDRESSABLE (2 required resource cells); generated-integration PARTIALLY_ADDRESSABLE (4 required resource cells); accepted-promotion PARTIALLY_ADDRESSABLE (3 required resource cells); assessment-readiness PARTIALLY_ADDRESSABLE (3 required resource cells); provenance-frame PARTIALLY_ADDRESSABLE (3 required resource cells); package-integration NOT_ADDRESSABLE (3 required resource cells); tests PARTIALLY_ADDRESSABLE (4 required resource cells); documentation NOT_ADDRESSABLE (4 required resource cells); validation NOT_ADDRESSABLE (1 required resource cells)
No recipe was authored for package-integration, documentation, or validation. The validation address was grounded, but no recipe promoted the exact required documentation contract. For tests, the frozen mirror recipes can reach test examples but omit the complementary production candidate-validation and readiness resources.

## 7. Post-hoc counterfactual diagnostic — NOT OBSERVED TREATMENT OUTPUT

Assuming only that all eight exact frozen declaration requests resolve to their exact direct ClassDef referents, while retaining every recipe/operator and captured mirror fact, the frozen recipes would materialize 8 hypotheses with 13 members and 7 unique targets. 1 mirrored member has no captured target. Coverage is 12/28 REQUIRED resource cells, 15/33 unit judgments, and 7/18 unique REQUIRED resources. It completes alternatives for 2/10 obligations and complete structures for 2/10: hypothesis-records, member-complementarity. Remaining misses: 16/28.
Fixing grounding alone does not make generation competitive by coverage with lexical/routed prefixes: it reaches 42.9% of REQUIRED cells and 38.9% of unique required resources, with only two complete obligations; the own-native and routed completion prefixes reach all ten. Generated candidates remain unranked. Exact recipe-by-recipe overlaps and missing complementary resources are in the JSON.

## 8. Architectural interpretation

Observed primary bottleneck: conservative decorated-class direct-declaration grounding; under the explicit counterfactual 12 required resource-obligation cells become reachable. Independently, owner/mirror operator coverage leaves 8 cells unreachable even after resolving named declarations, and three no-recipe obligations account for 8 cells. Task interpretation is sufficient; role routing preserves all candidates and is not the generation bottleneck. The counterfactual recipe structures exactly match gold resource structures only for hypothesis-records and member-complementarity; five obligations are partial and three are not addressable.
Gold also points to distinct typed relations: public facade/export-to-declaration links; exact imports/references between view and contract modules; documentation ownership/authority navigation; and a task-frame association for provenance. The required test gold combines production source contracts with tests, beyond the mirror-only test recipes. Package, documentation and validation require another acquisition/association route; OWNER/MIRRORED alone cannot express their gold targets.
Minimum justified next change: specify a narrow deterministic bridge from existing direct class syntax RI to grounding for explicitly decorated module-body class declarations, with explicit treatment of decorator ambiguity and no claim of runtime/public binding from a ClassDef alone. Measure that with newly authored complete alternatives/relations in a new prospective case. This case does not justify embeddings, BM25/LLM linking, ranking/resolution policy, broad graph expansion, or broad superiority claims.

## 9. Recovery qualification

All joined Stage B outputs remain identified as RECOVERY `case-0006-stage-b-recovery-1`. The sole additional execution was preauthorized. Attempt 1's failed correspondence check retained no semantic output; recovery changed only harness member-order matching, not treatment. Durable recovery output does not alter the measured effectiveness or explain the zero candidate surface.

## 10. Limitations

This is one prospective configuration and no threshold was frozen. Counterfactual results are resource-level assumptions, not rerun production behavior; no generated rank/depth is defined. The recovery limitation is the earlier capture correspondence failure. Confirmation remains sealed and was not accessed. No Retrieval, routing, grounding or generation stage was rerun. Production source, Stage A treatment, capture/recovery artifacts, Stage B.5 packet and Stage C judgments were not modified.

Next bounded increment: define and validate the narrow decorated-ClassDef grounding contract, then freeze a new prospective case whose recipes explicitly cover source, test, package, documentation, task-frame and validation witnesses before any acquisition. Do not implement an automatic resolver policy.
