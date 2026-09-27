# Increment 29: bounded references and direct calls

**State: completed development breadth baseline.** This is the first
development-only References + Calls breadth baseline. Its question is whether
source-grounded references to resolved direct Python functions surface resources
outside the saved lexical and direct-import candidate evidence, at tolerable
fan-out. No ranking, top-five admission, or retrieval policy is tested.

## Frozen semantics and population

The population is exactly the established 24 Increment-27 development
InformationNeeds and their historical parent snapshots. The 14 Increment-27
held-out cases and suspended Increment-26 confirmation were not executed.
Seeds are the saved canonical first-five positive resources. Seed resources are
excluded from additions.

A reference is an `ast.Name` read qualified by the existing conservative
Increment-28 import-binding checker over the full parent-snapshot source. Its
direct module-body `ImportFrom` binding must resolve unambiguously through the
production module/import machinery to exactly one direct module-body
`PythonFunctionSubject`, either directly or through the already-supported
single facade. A direct call is that same qualified `Name` in the exact
`ast.Call.func` position. Every call is a reference. These claims do not cover
methods, attributes, dispatch, nested functions, arbitrary aliases, or general
Python name resolution. Unsupported and indeterminate cases do not become
negative facts.

Forward projection follows a qualified reference/call from a seed resource to
the defining resource. Reverse projection finds referencing/calling resources
for a function directly declared by a seed resource. Candidate identity is
InformationNeed, parent snapshot, and resource address. All occurrence,
binding, import-resolution, declaration, subject, seed, and direction supports
are retained. There is no candidate ranking or K admission. This experiment
uses production declaration, module, import, and one-facade resolution facts;
it does not add production Repository Intelligence.

## Frozen candidate mechanics and reach

| Measure | Result |
| --- | ---: |
| Development cases / cases with additions | 24 / 14 |
| Qualified reference occurrences / direct-call occurrences across case analyses | 4,271 / 4,271 |
| Candidate pairs / distinct resource addresses / retained supports | 71 / 22 / 198 |
| Forward / reverse candidate pairs | 36 / 35 |
| Call-tagged / reference without call pairs | 71 / 0 |
| Canonical rank 6+ / no positive canonical rank | 58 / 13 |
| Absent from canonical / BM25+ / identifier / path-only / RRF positive universes | 13 / 13 / 13 / 49 / 11 |
| Absent from all five saved positive lexical universes | 11 |
| Already in direct-import candidates | 3 |
| Absent from existing direct-import candidates | 68 |
| Absent from both saved lexical and direct-import candidates | 11 |
| Exact prior judgments / new blinded targets | 52 / 19 |

All 71 additions are outside the canonical top five because seeds are
excluded. The 11 all-lexical-universe escapes are also absent from the existing
direct-import candidate union. Reference and direct-call candidate memberships
coincide on this population; this does **not** establish that non-call
references are impossible in other tasks or repositories.

The 19 new targets span five development cases: one has forward support and 18
have reverse support. All 19 are call-tagged. None of the 19 is absent from all saved positive lexical methods;
all 19 are absent from the direct-import candidate union. The neutral input
contains only the frozen InformationNeed, parent snapshot, resource address,
parent-snapshot content, and opaque identities. It carries no origin, direction,
relation support, rank, score, or judgment.

The case-analysis work measured 5,456 Python resource analyses, 40,412 import
aliases examined, 20,524 direct function declarations, 396 indeterminate
binding analyses, and no recorded Python parse failures. These counts include
repeated analysis when development cases share a parent snapshot; they are
workload counts, not unique repository facts. Maximum candidate fan-out was 12
for one case and 12 for one seed. The complete per-case and per-seed fan-out and
resolution diagnostics are in the candidate artifact.

## Artifact bindings and judgment boundary

| Artifact | Content identity |
| --- | --- |
| `references_calls_freeze.json` | `088c5ddc45dfedeb9cf2cce2669904ce74822c9bff78bf501e763905a5394b3a` |
| `references_calls_candidates.json` | `c755333d2b53e8895bd196df9ddf34fe2b69f79abbb790b1f9535431692cf8e8` |
| `references_calls_judgment_freeze.json` | `e7135889712e59f2183fed1433f645815365ee9fd9462f48e00b4cecbafffd14` |
| `references_calls_blinded_judgment_input.json` | `5c00fbf66914df9f6ce2f6d47cf0a891b02b4ff34e69dda7ac6c12f54ef473ba` |
| `references_calls_frozen_judgments.json` | `d93eb7d3e1d62d6e202eca927538a3042f35e876b2c2b10e5a55b398fc54505a` |
| `references_calls_development_results.json` | `301c88eda08ae74916abf26f2ced77a49d7b79d308af585ecf395b9fb95d7739` |

The mechanics freeze and candidate artifact were written before any usefulness
judgment was loaded. Exact reuse supplied 52 pairs: 33 USEFUL and 19
NOT_USEFUL. All 19 remaining targets were judged from the neutral input before
candidate origins were joined: 2 USEFUL, 17 NOT_USEFUL, and 0 UNJUDGED. The
judgment artifact binds the exact neutral-input content identity and file hash.
The hidden freeze maps every opaque identity back to one candidate pair.
UNJUDGED remains a distinct state; no state was converted to NOT_USEFUL.

## Completed development result

| Surface | Candidates | USEFUL | NOT_USEFUL | UNJUDGED |
| --- | ---: | ---: | ---: | ---: |
| Reference/call union | 71 | 35 | 36 | 0 |
| Forward | 36 | 20 | 16 | 0 |
| Reverse | 35 | 15 | 20 | 0 |
| All five lexical universes absent | 11 | 4 | 7 | 0 |
| Existing direct-import candidates absent | 68 | 33 | 35 | 0 |
| Both lexical and import candidates absent | 11 | 4 | 7 | 0 |

All 35 USEFUL additions are outside the canonical top five because the five
seeds were excluded. The four useful hard escapes occur across three cases:

- `i25-ab24906f07ed`: `src/devtools/core/paths/resolution.py`;
- `i25-5fdf5fe05527`: `src/devtools/core/paths/resolution.py` and
  `src/devtools/resources/filesystem/reading.py`;
- `i25-5bdc70483eed`: `src/devtools/context/repository.py`.

**Breadth verdict:** bounded direct-call-bearing relationships established
novel candidate reach and useful reach beyond both the saved lexical family
and existing direct-import candidates on development. This is complementary
candidate evidence, not a fixed-budget ranking result or a general preference
over other families. The 71 pairs arose from 198 supports with maximum
per-case and per-seed candidate fan-out of 12. Work was finite on this
population, but the experiment did not benchmark production execution cost.
All 71 candidates were call-tagged; zero reference-only candidates mean
non-call references were not adequately tested by this workload.

A source occurrence referencing an identified function under these bounded
static rules, and its direct-call-site specialization, remain plausible
deterministic Repository Intelligence concepts. Their semantic design needs
strengthening before any production consideration. Retrieval usefulness does
not promote the experiment implementation. No production retrieval or Context
disclosure behavior changed, and confirmation remains sealed.

**Next breadth family:** Containment. Do not refine References/Calls during
this breadth pass.

**Parked backlog note:** if a later workload has meaningful non-call
references, test that surface as a separate family-specific refinement after
the breadth sprint.
