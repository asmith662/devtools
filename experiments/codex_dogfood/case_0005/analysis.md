# Case 0005 Stage D joined analysis

## Frozen measurements

Stage A/B/B.5/C identities and pinned hashes verified. Join: 515/515 resources, 9/9 obligations, 9/9 query/preferences, 4,635/4,635 judgments; no duplicates, misses or unexpected identities. The global lane is unchanged, and every routed lane retains every native match exactly once.

Required gold: 27 obligation/unit occurrences, 25 distinct units, 24 unique witness-universe resources. Minimum semantically sufficient adjudicated union: **22 resources**; this is an information witness bound, not an implementation file set.

Global native: 512 positive matches; task-complete obligation depth **342**; complete 24-resource witness-universe depth **342**. All required resources and units are globally reachable. Own-lane maximum best native depth **110**; maximum best routed position **88**. These latter maxima span nine separate lanes.

| Obligation | Global best | Own native | Own routed | Native prefix | Routed prefix | Change | Required preferred / escape | Preferred size / escape size |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| semantic-ownership | 42 | 14 | 88 | 14 | 88 | +74 | 2 / 2 | 86 / 80 |
| witness-algebra | 43 | 4 | 58 | 4 | 58 | +54 | 2 / 1 | 57 / 47 |
| native-evidence | 192 | 41 | 14 | 41 | 14 | -27 | 2 / 0 | 173 / 92 |
| role-routing-integration | 70 | 29 | 4 | 29 | 4 | -25 | 2 / 0 | 204 / 98 |
| snapshot-frame | 289 | 110 | 68 | 110 | 68 | -42 | 6 / 0 | 202 / 94 |
| package-integration | 148 | 66 | 14 | 66 | 14 | -52 | 1 / 0 | 83 / 101 |
| tests | 37 | 9 | 1 | 9 | 1 | -8 | 3 / 0 | 171 / 162 |
| documentation | 11 | 13 | 13 | 13 | 13 | +0 | 4 / 0 | 96 / 78 |
| validation | 342 | 9 | 9 | 9 | 9 | +0 | 0 / 2 | 0 / 246 |

Completion improved: native-evidence, role-routing-integration, snapshot-frame, package-integration, tests. Unchanged: documentation, validation. Worsened: semantic-ownership, witness-algebra.

Native completion prefixes: **295 occurrences / 151 unique resources**. Routed: **269 occurrences / 160 unique resources**. Changes: -26 occurrences (-8.8%) and +9 unique resources (+6.0%).

Relative to the 22-resource sufficient union: native 6.86 times / +129; routed 7.27 times / +138. Prefix label occurrences (native to routed): REQUIRED 24 to 24, HELPFUL_ONLY 14 to 13, UNNECESSARY 257 to 232; unresolved 0.

Union overlap: 100 in both, 51 native only, 60 routed only. All are still present in their full routed lanes; prefix boundaries alone differ.

### Alternative-aware completion and prefix composition

- **semantic-ownership** — semantic-ownership-alternative-1: global 42, native 14, routed 88, escape needed; semantic-ownership-alternative-2: global 42, native 16, routed 98, escape needed. Best G/N/R: semantic-ownership-alternative-1 / semantic-ownership-alternative-1 / semantic-ownership-alternative-1. Prefix R/H/U: native 3/1/10; routed 3/1/84.
- **witness-algebra** — witness-algebra-alternative-1: global 43, native 4, routed 58, escape needed. Best G/N/R: witness-algebra-alternative-1 / witness-algebra-alternative-1 / witness-algebra-alternative-1. Prefix R/H/U: native 3/0/1; routed 3/2/53.
- **native-evidence** — native-evidence-alternative-1: global 192, native 41, routed 14, all preferred. Best G/N/R: native-evidence-alternative-1 / native-evidence-alternative-1 / native-evidence-alternative-1. Prefix R/H/U: native 2/3/36; routed 2/2/10.
- **role-routing-integration** — role-routing-integration-alternative-1: global 70, native 29, routed 4, all preferred. Best G/N/R: role-routing-integration-alternative-1 / role-routing-integration-alternative-1 / role-routing-integration-alternative-1. Prefix R/H/U: native 2/4/23; routed 2/2/0.
- **snapshot-frame** — snapshot-frame-alternative-1: global 289, native 110, routed 68, all preferred. Best G/N/R: snapshot-frame-alternative-1 / snapshot-frame-alternative-1 / snapshot-frame-alternative-1. Prefix R/H/U: native 6/2/102; routed 6/2/60.
- **package-integration** — package-integration-alternative-1: global 148, native 66, routed 14, all preferred. Best G/N/R: package-integration-alternative-1 / package-integration-alternative-1 / package-integration-alternative-1. Prefix R/H/U: native 1/1/64; routed 1/1/12.
- **tests** — tests-alternative-1: global 38, native 9, routed 1, all preferred; tests-alternative-2: global 51, native 27, routed 3, all preferred; tests-alternative-3: global 37, native 18, routed 2, all preferred. Best G/N/R: tests-alternative-3 / tests-alternative-1 / tests-alternative-1. Prefix R/H/U: native 1/0/8; routed 1/0/0.
- **documentation** — documentation-alternative-1: global 11, native 13, routed 13, all preferred. Best G/N/R: documentation-alternative-1 / documentation-alternative-1 / documentation-alternative-1. Prefix R/H/U: native 4/3/6; routed 4/3/6.
- **validation** — validation-alternative-1: global 342, native 9, routed 9, escape needed. Best G/N/R: validation-alternative-1 / validation-alternative-1 / validation-alternative-1. Prefix R/H/U: native 2/0/7; routed 2/0/7.

## Observations

Required unit occurrences by routed tier: {'ESCAPE': 5, 'PREFERRED_ROLE_SUPPORTED': 22}. Unique resources: preferred 21, escape 5; a resource can occur in both categories across obligations. Required escape in the best routed alternative: semantic-ownership, witness-algebra, validation.

The validation lane has an empty preference. Its complete routed order equals native order, including every required witness and completion depth.

Unit-level decomposition classifications: {'own_native_shallower': 21, 'global_shallower': 4, 'equal': 2}. Unit-level routing movement: {'routed_later': 3, 'routed_earlier': 18, 'unchanged': 6}. All 27 required occurrences reach their own native and routed lanes; all 24 witness-universe resources reach the global lane.

Helpful-only: 32 obligation/resource cells, 23 unique resources; 30 own native matches, 21 preferred and 9 escape. Rank distributions by obligation are retained in analysis.json.

### Preferred-tier quality

Precision uses all preferred candidates as denominator. Recall uses all acceptable REQUIRED witness resources, then the best routed alternative separately.

| Obligation | Required/Helpful/Unnecessary preferred | Precision, all alternatives | Recall, all alternatives | Precision, best routed alternative | Recall, best routed alternative |
| --- | ---: | ---: | ---: | ---: | ---: |
| semantic-ownership | 2/0/84 | 2.3% | 50.0% | 2.3% | 66.7% |
| witness-algebra | 2/2/53 | 3.5% | 66.7% | 3.5% | 66.7% |
| native-evidence | 2/4/167 | 1.2% | 100.0% | 1.2% | 100.0% |
| role-routing-integration | 2/2/200 | 1.0% | 100.0% | 1.0% | 100.0% |
| snapshot-frame | 6/4/192 | 3.0% | 100.0% | 3.0% | 100.0% |
| package-integration | 1/3/79 | 1.2% | 100.0% | 1.2% | 100.0% |
| tests | 3/1/167 | 1.8% | 100.0% | 0.6% | 100.0% |
| documentation | 4/5/87 | 4.2% | 100.0% | 4.2% | 100.0% |
| validation | 0/0/0 | n/a (empty tier) | 0.0% | n/a (empty tier) | 0.0% |

## Diagnostic post-hoc breakdown

Required witness ranks, routed tiers, exact selected supports, escape reasons and cross-obligation observations are recorded per unit in analysis.json. The following counts are overlapping support-kind incidences among earlier-routed preferred candidates, not unique resources or causal effects.

- **REQUIRED promoted:** kinds module-interpretation 14, python-suffix-convention 14, pytest-testpath-target 3, test-directory-convention 3, initializer-name-convention 1, mirrored-test-path 1, package-interpretation 1, package-membership 1; grouped path_or_name_convention 18, module_or_package_interpretation 15, configured_testpath_or_filename_pattern 3, mirrored_test_path 1, package_membership 1.
- **UNNECESSARY promoted:** kinds python-suffix-convention 696, module-interpretation 694, pytest-testpath-target 167, test-directory-convention 167, mirrored-test-path 85, markdown-suffix-convention 80, documentation-directory-convention 79, package-membership 78, initializer-name-convention 9, package-interpretation 8, readme-name-convention 1, readme-target 1; grouped path_or_name_convention 1032, module_or_package_interpretation 702, configured_testpath_or_filename_pattern 167, mirrored_test_path 85, package_membership 78, project_configuration_or_target 1.
- **HELPFUL_ONLY promoted:** kinds module-interpretation 12, python-suffix-convention 12, package-membership 3, documentation-directory-convention 2, initializer-name-convention 2, markdown-suffix-convention 2, package-interpretation 2, pytest-testpath-target 1, test-directory-convention 1; grouped path_or_name_convention 19, module_or_package_interpretation 14, package_membership 3, configured_testpath_or_filename_pattern 1.

Required escape categories: {'CROSS_ROLE_REQUIRED_INFORMATION': 3, 'EMPTY_CALLER_PREFERENCE_CONTROL': 2}. A preferred-role mismatch or cross-role requirement is still a retained candidate, not a false negative.

### Required escape witnesses

- semantic-ownership / owner-overview: `src/devtools/context/localization/docs/overview.md`, native 2 → routed 88; CROSS_ROLE_REQUIRED_INFORMATION; positive roles DOCUMENTATION; preferred PYTHON_CODE. Diagnostic target: evidence-to-witness reasoning across roles.
- semantic-ownership / owner-architecture: `docs/architecture.md`, native 16 → routed 98; CROSS_ROLE_REQUIRED_INFORMATION; positive roles DOCUMENTATION; preferred PYTHON_CODE. Diagnostic target: evidence-to-witness reasoning across roles.
- witness-algebra / candidate-semantics: `docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md`, native 1 → routed 58; CROSS_ROLE_REQUIRED_INFORMATION; positive roles DOCUMENTATION; preferred PYTHON_CODE. Diagnostic target: evidence-to-witness reasoning across roles.
- validation / validation-contract: `docs/development/validation.md`, native 1 → routed 1; EMPTY_CALLER_PREFERENCE_CONTROL; positive roles DOCUMENTATION; preferred (empty). Diagnostic target: caller preference (deliberately empty control).
- validation / static-configuration: `pyproject.toml`, native 9 → routed 9; EMPTY_CALLER_PREFERENCE_CONTROL; positive roles BUILD_CONFIGURATION, PROJECT_CONFIGURATION, TEST_CONFIGURATION, TOOL_CONFIGURATION; preferred (empty). Diagnostic target: caller preference (deliberately empty control).

Cross-obligation: 14 required unit occurrences have a better native rank, earlier routed position or other-lane preferred role; 11 rank better natively elsewhere, 9 route earlier elsewhere, and 4 are preferred elsewhere while escaped in their own lane. Examples: the Localization package overview and ADR-0005 escape source-oriented obligations but are preferred in the documentation lane. These other lanes are excluded from primary completion.

Alternative selection: none changed cheapest acceptable alternative from own native to routed. The global lane instead selects the third testing alternative; native and routed select the first. No cross-surface alternative is forced.

## Architectural interpretation

The nine scoped queries reduce the case-wide maximum completion depth from global 342 to own-lane native 110, while preserving global recall; the documentation obligation alone is slightly shallower globally. Positive role routing changes review order unevenly: it removes 26 summed prefix occurrences but expands the unique prefix union by 9 resources. Source-oriented preferences promote code contracts and delay required documentation in semantic ownership and witness algebra. The retained escape tier prevents candidate loss. These outcomes directly motivate evidence-to-witness resolution that reasons across resource roles and keeps alternatives explicit, rather than treating a preferred role or position as satisfaction.

The directly evidenced bottlenecks are lexical discrimination (many unnecessary candidates before completion), role discrimination (large preferred tiers and cross-role escape), and the missing evidence-to-witness resolution capability. Acquisition recall did not fail for these frozen required witnesses. The nine-obligation interpretation had no adjudicated gap, though this one task cannot prove general interpretation quality.

The next question is whether a bounded production association record can identify and retain cross-role witness hypotheses with native provenance and unresolved status, then prospectively measure its review cost. No implementation or new arm is introduced here.

## Limitations

One prospective task and one 515-resource frozen frame support only case-specific descriptive effects. Positive roles are overlapping hints. Counts before completion depend on the independently frozen witness frame and per-surface best acceptable alternative. No numeric success threshold, learned score, confirmation result or general superiority claim is inferred.
