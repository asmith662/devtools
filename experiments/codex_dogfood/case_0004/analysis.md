# Case 0004 Stage D joined analysis

This report joins the frozen Stage B BM25 capture to the independent Stage C judgments. It measures lexical acquisition reach, not semantic satisfaction.

- Task: `codex-dogfood-case-0004-repository-role-intelligence`
- Repository / snapshot: `d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8` / `3d994888fb7dc9cc1303b958acc0e6f6372f6e723a0791a6a0947a4acd5157ed`
- Eligible frame: 498/498 exact identities; 8/8 obligations; nine lanes.
- Unique required resources: 17; required units: 25.
- Global full-task lane: 17/17 required resources (recall 1.000); complete depth 325.
- Own obligation lanes: 8/8 acquisition-complete for adjudicated witnesses (1.000); obligation-wise maximum completion depth 193.

## Per-obligation acquisition

Alternative completion depth is the maximum native member rank when all members are reached; an incomplete alternative has no finite depth. `global best` applies the same frozen alternatives in the global lane.

| Obligation | Required units | Required resources | Alternatives | Lane results | Own best depth | Global best depth | Own lane result | Comparison |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| ri-ownership | 3 | 3 | 1 | 290 | 83 | 256 | True | own_shallower |
| resource-path | 4 | 4 | 1 | 302 | 193 | 260 | True | own_shallower |
| python-configuration | 3 | 3 | 1 | 224 | 5 | 220 | True | own_shallower |
| test-configuration | 5 | 5 | 2 | 291 | 58 | 197 | True | own_shallower |
| package-integration | 3 | 3 | 1 | 259 | 67 | 325 | True | own_shallower |
| tests | 1 | 1 | 1 | 364 | 10 | 85 | True | own_shallower |
| documentation | 4 | 4 | 1 | 235 | 181 | 46 | True | global_shallower |
| validation | 2 | 2 | 1 | 198 | 5 | 197 | True | own_shallower |

### Accepted alternatives

Each row is one complete acceptable information set; every listed member is conjunctive. `None` means at least one member had no positive match.

| Obligation | Alternative | Resource members (own rank) | Own depth | Global depth |
| --- | --- | --- | ---: | ---: |
| ri-ownership | ri-ownership:alternative-1 | `docs/architecture/taxonomy.md` (12), `docs/architecture.md` (2), `src/devtools/context/repository/snapshot.py` (83) | 83 | 256 |
| resource-path | resource-path:alternative-1 | `src/devtools/context/repository/resource.py` (35), `src/devtools/context/repository/snapshot.py` (18), `src/devtools/context/repository/observation.py` (41), `src/devtools/core/paths/resolution.py` (193) | 193 | 260 |
| python-configuration | python-configuration:alternative-1 | `src/devtools/context/python/project_configuration/models.py` (2), `src/devtools/context/python/project_configuration/declarations.py` (5), `src/devtools/context/python/project_configuration/resolution.py` (4) | 5 | 220 |
| test-configuration | test-configuration:alternative-1 | `pyproject.toml` (58), `src/devtools/context/python/project_configuration/docs/overview.md` (2) | 58 | 197 |
| test-configuration | test-configuration:alternative-2 | `pyproject.toml` (58), `src/devtools/context/python/project_configuration/models.py` (62), `src/devtools/context/python/project_configuration/declarations.py` (257), `src/devtools/context/python/project_configuration/resolution.py` (35) | 257 | 220 |
| package-integration | package-integration:alternative-1 | `AGENTS.md` (9), `src/devtools/context/repository/__init__.py` (33), `src/devtools/context/python/project_configuration/__init__.py` (67) | 67 | 325 |
| tests | tests:alternative-1 | `tests/context/python/project_configuration/test_configuration.py` (10) | 10 | 85 |
| documentation | documentation:alternative-1 | `docs/documentation_map.md` (2), `docs/architecture.md` (10), `src/devtools/context/python/project_configuration/docs/overview.md` (43), `docs/development/validation.md` (181) | 181 | 46 |
| validation | validation:alternative-1 | `docs/development/validation.md` (1), `pyproject.toml` (5) | 5 | 197 |

## Required-resource reach

| Category | Count |
| --- | ---: |
| Global only | 0 |
| Obligation lanes only | 413 |
| Both | 17 |
| Neither | 0 |

Required resources missed in every owning lane: 0. Required units retrieved at a better rank by another obligation lane (or only there): 14.


## Candidate union and helpful evidence

Nine lanes returned 2650 candidate occurrences over 487 unique resources (2163 repeated occurrences). The obligation lanes contained 430 unique resources; 57 appeared only globally and 0 only in obligation lanes.
11 of 498 eligible resources had no positive BM25 match in any lane; none was a required resource. Every other required lane miss described in the JSON is distinguished from a deep rank.
There were 22 helpful-only units across 19 resources. Their global ranks: {'observations': 22, 'reached': 22, 'missed': 0, 'min': 2, 'median': 63.0, 'max': 369, 'mean': 108.9090909090909, 'ranks': [2, 3, 5, 17, 29, 29, 34, 34, 35, 41, 45, 81, 82, 101, 149, 159, 187, 187, 197, 301, 309, 369]}; own-lane ranks: {'observations': 22, 'reached': 22, 'missed': 0, 'min': 1, 'median': 21.0, 'max': 201, 'mean': 45.63636363636363, 'ranks': [1, 1, 1, 2, 3, 4, 7, 9, 12, 14, 16, 26, 37, 42, 45, 45, 79, 86, 106, 127, 140, 201]}. Helpful units ranked ahead of the best globally reached required resource in 2 cases.
Taking each own lane through its own obligation's best completion depth yields 602 lane-prefix occurrences and 256 unique resources. This is not a merged ranking or a recommendation.

## Required units

Ranks are native lane ranks. `—` means no positive BM25 match in that lane.

| Obligation | Unit | Resource | Global | Own lane | Other-lane best | Rank comparison |
| --- | --- | --- | ---: | ---: | ---: | --- |
| ri-ownership | ri-ownership:taxonomy | `docs/architecture/taxonomy.md` | 16 | 12 | 6 | own_shallower |
| ri-ownership | ri-ownership:architecture | `docs/architecture.md` | 4 | 2 | 4 | own_shallower |
| ri-ownership | ri-ownership:snapshot | `src/devtools/context/repository/snapshot.py` | 256 | 83 | 18 | own_shallower |
| resource-path | resource-path:address | `src/devtools/context/repository/resource.py` | 260 | 35 | 120 | own_shallower |
| resource-path | resource-path:snapshot | `src/devtools/context/repository/snapshot.py` | 256 | 18 | 83 | own_shallower |
| resource-path | resource-path:containment | `src/devtools/context/repository/observation.py` | 116 | 41 | 49 | own_shallower |
| resource-path | resource-path:normalization | `src/devtools/core/paths/resolution.py` | 86 | 193 | 79 | global_shallower |
| python-configuration | python-configuration:models | `src/devtools/context/python/project_configuration/models.py` | 130 | 2 | 22 | own_shallower |
| python-configuration | python-configuration:declarations | `src/devtools/context/python/project_configuration/declarations.py` | 220 | 5 | 56 | own_shallower |
| python-configuration | python-configuration:resolution | `src/devtools/context/python/project_configuration/resolution.py` | 96 | 4 | 24 | own_shallower |
| test-configuration | test-configuration:actual | `pyproject.toml` | 197 | 58 | 5 | own_shallower |
| test-configuration | test-configuration:documented | `src/devtools/context/python/project_configuration/docs/overview.md` | 29 | 2 | 1 | own_shallower |
| test-configuration | test-configuration:models | `src/devtools/context/python/project_configuration/models.py` | 130 | 62 | 2 | own_shallower |
| test-configuration | test-configuration:parser | `src/devtools/context/python/project_configuration/declarations.py` | 220 | 257 | 5 | global_shallower |
| test-configuration | test-configuration:resolver | `src/devtools/context/python/project_configuration/resolution.py` | 96 | 35 | 4 | own_shallower |
| package-integration | package-integration:rules | `AGENTS.md` | 20 | 9 | 3 | own_shallower |
| package-integration | package-integration:repository | `src/devtools/context/repository/__init__.py` | 325 | 33 | 105 | own_shallower |
| package-integration | package-integration:configuration | `src/devtools/context/python/project_configuration/__init__.py` | 226 | 67 | 13 | own_shallower |
| tests | tests:regressions | `tests/context/python/project_configuration/test_configuration.py` | 85 | 10 | 3 | own_shallower |
| documentation | documentation:navigation | `docs/documentation_map.md` | 12 | 2 | 6 | own_shallower |
| documentation | documentation:architecture | `docs/architecture.md` | 4 | 10 | 2 | global_shallower |
| documentation | documentation:package | `src/devtools/context/python/project_configuration/docs/overview.md` | 29 | 43 | 1 | global_shallower |
| documentation | documentation:development | `docs/development/validation.md` | 46 | 181 | 1 | global_shallower |
| validation | validation:contract | `docs/development/validation.md` | 46 | 1 | 9 | own_shallower |
| validation | validation:settings | `pyproject.toml` | 197 | 5 | 45 | own_shallower |

## Interpretation

**Observation.** The global lane returned positive matches for 17/17 required resources. Own lanes completed 8/8 applicable obligations under at least one accepted alternative. The per-obligation table shows whether each own-lane completion depth was shallower, deeper, equal, or unreachable relative to the global lane.

**Architectural interpretation.** These results describe one task/snapshot and the frozen queries. They do not establish general superiority, a production resolution, or a reason to change Localization, Retrieval, or query policy. Contribution components are descriptive evidence, not causes.

### Frozen questions

1. Global lane reached every required resource: **True** (17/17).
2. Every required information unit appeared in its owning obligation lane: **True** (25/25); all 17 unique required resources were reached by their owning lane association(s).
3. Own-lane best completion was shallower than the global alternative depth for 7/8 obligations; per-obligation outcomes are shown above.
4. Own-lane required units ranked worse than their global rank: 5; the documentation obligation also has a worse best completion depth.
5. Required units with no positive match in their own lane: 0; unique resources missed in every owning lane: 0.
6. Required units ranked better in another obligation lane than their own (or missed by own): 14; resources missed in all owning lanes but found in another lane: 0.
7. Global full-task complete depth is 325. Repository documentation records full-task depths of 35 (Case 0001), 43 (Case 0002) and 348 (Case 0003); short-query depths are 132, 87 and 180. These unlike tasks/frames are descriptive only.
8. Own-obligation completion depths: ri-ownership=83, resource-path=193, python-configuration=5, test-configuration=58, package-integration=67, tests=10, documentation=181, validation=5.
9. Obligation-wise maximum completion depth is 193; it is the maximum of each lane's best alternative depth, not a universal merged rank.
10. There are 17 unique required resources across 25 required units.
11. The naive own-lane completion-prefix union contains 256 unique resources (602 lane-prefix occurrences).
12. Case-specifically, Python configuration and validation had the shallowest own-lane completion (rank 5); documentation (181) and resource-path (193) were deepest. Their query result counts and rank detail are retained in JSON. This describes discrimination in this case only.

Confirmation remained sealed. No retrieval was rerun, no frozen judgment or treatment was changed, and no production behavior was changed.

## Integrity and limitations

The JSON artifact records checkpoint and input SHA-256 values, exact resource/obligation join diagnostics, every required/helpful unit's ranks, each conjunctive alternative, per-lane result counts and the full obligation-lane prefix union. It distinguishes zero positive matches from deep ranks. See its `limitations` field for scope constraints.
