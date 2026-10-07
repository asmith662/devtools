# Case 0011 Stage B review — NOT GOLD

Effectiveness UNKNOWN. Human inspection is not Stage C adjudication. Maintainer comments/labels belong in separate MANUAL_AUDIT. All routes are CANONICAL_RESOURCE_BM25 with k1=1.2, b=0.75, filename weight=0.25; no routing, fusion or reformulation.

[Stage A review](STAGE_A_REVIEW.md) preserves the full prompt, all interpretations, exact queries, analyzed terms and hints. The complete positive rows and term contributions are hash-bound in results.json.gz and trace.json. Top five here are an inspection window, not a retrieval limit.

## Unjudged result counts and duplicates

| Arm | Queries | Positive occurrences | Unique union | Duplicate occurrences |
|---|---:|---:|---:|---:|
| A | 1 | 529 | 529 | 0 |
| B | 9 | 2523 | 484 | 2039 |
| C | 18 | 4766 | 497 | 4269 |

Duplicate occurrences = returned occurrences minus distinct union, not a relevance judgment. Every query pair's intersection/only counts are retained in trace.json.

## A.task — Arm A

Obligation: None. Need: None.

Exact query:

```text
Add an optional caller-directed UTF-8 byte ceiling to copied ModelRequest assembly for explicitly planned repository Context.
The caller supplies an already materialized ContextDisclosure from a DisclosurePlan and an optional maximum Context byte count; None retains existing unlimited behavior.
Count the exact rendered Context text that would be appended, including its headings and separators, encoded as UTF-8; exclude the caller's original task text from this count and preserve existing newline handling.
Accept a nonnegative integer ceiling, reject booleans and other invalid values, allow equality at the boundary, and reject an oversized disclosure before creating a modified request.
Reject rather than truncate, omit items, change representation, or silently select a smaller plan; a zero ceiling permits only zero-byte rendered Context.
Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.
Keep capacity checking in common Context Planning without a dependency on a language-specific adapter or Retrieval, and preserve existing whole-resource and qualified-reference choices.
Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.
Update governing architecture and package documentation and run protected development validation with the established tooling configuration.
Do not implement automatic selection, token estimation, truncation, query changes, semantic resolution, persistence, or agent execution.
```

Native analyzer terms: `add, an, optional, caller, directed, utf, 8, byte, ceiling, to, copied, modelrequest, assembly, for, explicitly, planned, repository, context, the, supplies, already, materialized, contextdisclosure, from, a, disclosureplan, and, maximum, count, none, retains, existing, unlimited, behavior, exact, rendered, text, that, would, be, appended, including, its, headings, separators, encoded, as, exclude, s, original, task, this, preserve, newline, handling, accept, nonnegative, integer, reject, booleans, other, invalid, values, allow, equality, at, boundary, oversized, disclosure, before, creating, modified, request, rather, than, truncate, omit, items, change, representation, or, silently, select, smaller, plan, zero, permits, only, item, order, native, provenance, snapshot, content, frame, checks, prompt, role, every, field, failure, must, leave, objects, unchanged, keep, capacity, checking, in, common, planning, without, dependency, on, language, specific, adapter, retrieval, whole, resource, qualified, reference, choices, follow, public, package, exports, validation, error, conventions, focused, tests, boundaries, non, ascii, ceilings, foreign, stale, frames, preservation, update, governing, architecture, documentation, run, protected, development, with, established, tooling, configuration, do, not, implement, automatic, selection, token, estimation, truncation, query, changes, semantic, resolution, persistence, agent, execution`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': ['ModelRequest', 'ContextDisclosure', 'DisclosurePlan']}. Execution count: 1. Positive resources: 529. Query seconds: 0.021986300.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 225.039370414 | 225.039370414 | 0.000000000 | 0.000000000 |
| 2 | `docs/architecture.md` | 204.586763249 | 203.198993589 | 5.551078640 | 1.387769660 |
| 3 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 201.680577664 | 199.020529756 | 10.640191634 | 2.660047909 |
| 4 | `docs/roadmap.md` | 195.677048225 | 195.677048225 | 0.000000000 | 0.000000000 |
| 5 | `docs/backlog/epics/B-0002-coding-context-substrate.md` | 191.671873725 | 191.055306856 | 2.466267475 | 0.616566869 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| add | 34 | 2.735684165 | 0.064030 | 34 | UNKNOWN / UNKNOWN / UNKNOWN |
| an | 217 | 0.894444639 | 0.408663 | 217 | UNKNOWN / UNKNOWN / UNKNOWN |
| optional | 53 | 2.296961835 | 0.099812 | 53 | UNKNOWN / UNKNOWN / UNKNOWN |
| caller | 97 | 1.696791111 | 0.182674 | 97 | UNKNOWN / UNKNOWN / UNKNOWN |
| directed | 27 | 2.962457485 | 0.050847 | 27 | UNKNOWN / UNKNOWN / UNKNOWN |
| utf | 99 | 1.676485845 | 0.186441 | 99 | UNKNOWN / UNKNOWN / UNKNOWN |
| 8 | 120 | 1.484993736 | 0.225989 | 120 | UNKNOWN / UNKNOWN / UNKNOWN |
| byte | 31 | 2.826655944 | 0.058380 | 31 | UNKNOWN / UNKNOWN / UNKNOWN |
| ceiling | 3 | 5.023880521 | 0.005650 | 3 | UNKNOWN / UNKNOWN / UNKNOWN |
| to | 207 | 0.941512150 | 0.389831 | 207 | UNKNOWN / UNKNOWN / UNKNOWN |
| copied | 6 | 4.404841312 | 0.011299 | 6 | UNKNOWN / UNKNOWN / UNKNOWN |
| modelrequest | 39 | 2.600342817 | 0.073446 | 39 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |
| for | 400 | 0.283929723 | 0.753296 | 400 | UNKNOWN / UNKNOWN / UNKNOWN |
| explicitly | 55 | 2.260260469 | 0.103578 | 55 | UNKNOWN / UNKNOWN / UNKNOWN |
| planned | 15 | 3.535803465 | 0.028249 | 15 | UNKNOWN / UNKNOWN / UNKNOWN |
| repository | 217 | 0.894444639 | 0.408663 | 217 | UNKNOWN / UNKNOWN / UNKNOWN |
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| the | 331 | 0.473015680 | 0.623352 | 331 | UNKNOWN / UNKNOWN / UNKNOWN |
| supplies | 24 | 3.077970372 | 0.045198 | 24 | UNKNOWN / UNKNOWN / UNKNOWN |
| already | 38 | 2.625985248 | 0.071563 | 38 | UNKNOWN / UNKNOWN / UNKNOWN |
| materialized | 23 | 3.119643068 | 0.043315 | 23 | UNKNOWN / UNKNOWN / UNKNOWN |
| contextdisclosure | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| from | 408 | 0.264151575 | 0.768362 | 408 | UNKNOWN / UNKNOWN / UNKNOWN |
| a | 351 | 0.414433778 | 0.661017 | 351 | UNKNOWN / UNKNOWN / UNKNOWN |
| disclosureplan | 14 | 3.602494840 | 0.026365 | 14 | UNKNOWN / UNKNOWN / UNKNOWN |
| and | 382 | 0.329914836 | 0.719397 | 382 | UNKNOWN / UNKNOWN / UNKNOWN |
| maximum | 27 | 2.962457485 | 0.050847 | 27 | UNKNOWN / UNKNOWN / UNKNOWN |
| count | 55 | 2.260260469 | 0.103578 | 55 | UNKNOWN / UNKNOWN / UNKNOWN |
| none | 311 | 0.535244151 | 0.585687 | 311 | UNKNOWN / UNKNOWN / UNKNOWN |
| retains | 62 | 2.141476933 | 0.116761 | 62 | UNKNOWN / UNKNOWN / UNKNOWN |
| existing | 88 | 1.793640937 | 0.165725 | 88 | UNKNOWN / UNKNOWN / UNKNOWN |
| unlimited | 2 | 5.360352757 | 0.003766 | 2 | UNKNOWN / UNKNOWN / UNKNOWN |
| behavior | 61 | 2.157606315 | 0.114878 | 61 | UNKNOWN / UNKNOWN / UNKNOWN |
| exact | 147 | 1.282815314 | 0.276836 | 147 | UNKNOWN / UNKNOWN / UNKNOWN |
| rendered | 21 | 3.208590554 | 0.039548 | 21 | UNKNOWN / UNKNOWN / UNKNOWN |
| text | 168 | 1.149707740 | 0.316384 | 168 | UNKNOWN / UNKNOWN / UNKNOWN |
| that | 106 | 1.608498504 | 0.199623 | 106 | UNKNOWN / UNKNOWN / UNKNOWN |
| would | 8 | 4.136577326 | 0.015066 | 8 | UNKNOWN / UNKNOWN / UNKNOWN |
| be | 139 | 1.338578888 | 0.261770 | 139 | UNKNOWN / UNKNOWN / UNKNOWN |
| appended | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| including | 35 | 2.707110793 | 0.065913 | 35 | UNKNOWN / UNKNOWN / UNKNOWN |
| its | 170 | 1.137908193 | 0.320151 | 170 | UNKNOWN / UNKNOWN / UNKNOWN |
| headings | 8 | 4.136577326 | 0.015066 | 8 | UNKNOWN / UNKNOWN / UNKNOWN |
| separators | 16 | 3.473283108 | 0.030132 | 16 | UNKNOWN / UNKNOWN / UNKNOWN |
| encoded | 32 | 2.795403400 | 0.060264 | 32 | UNKNOWN / UNKNOWN / UNKNOWN |
| as | 163 | 1.179830499 | 0.306968 | 163 | UNKNOWN / UNKNOWN / UNKNOWN |
| exclude | 5 | 4.571895397 | 0.009416 | 5 | UNKNOWN / UNKNOWN / UNKNOWN |
| s | 112 | 1.553690268 | 0.210923 | 112 | UNKNOWN / UNKNOWN / UNKNOWN |
| original | 45 | 2.458931163 | 0.084746 | 45 | UNKNOWN / UNKNOWN / UNKNOWN |
| task | 78 | 1.913544865 | 0.146893 | 78 | UNKNOWN / UNKNOWN / UNKNOWN |
| this | 143 | 1.310308454 | 0.269303 | 143 | UNKNOWN / UNKNOWN / UNKNOWN |
| preserve | 50 | 2.354670153 | 0.094162 | 50 | UNKNOWN / UNKNOWN / UNKNOWN |
| newline | 24 | 3.077970372 | 0.045198 | 24 | UNKNOWN / UNKNOWN / UNKNOWN |
| handling | 14 | 3.602494840 | 0.026365 | 14 | UNKNOWN / UNKNOWN / UNKNOWN |
| accept | 20 | 3.256218603 | 0.037665 | 20 | UNKNOWN / UNKNOWN / UNKNOWN |
| nonnegative | 8 | 4.136577326 | 0.015066 | 8 | UNKNOWN / UNKNOWN / UNKNOWN |
| integer | 21 | 3.208590554 | 0.039548 | 21 | UNKNOWN / UNKNOWN / UNKNOWN |
| reject | 52 | 2.315830320 | 0.097928 | 52 | UNKNOWN / UNKNOWN / UNKNOWN |
| booleans | 3 | 5.023880521 | 0.005650 | 3 | UNKNOWN / UNKNOWN / UNKNOWN |
| other | 101 | 1.656584691 | 0.190207 | 101 | UNKNOWN / UNKNOWN / UNKNOWN |
| invalid | 63 | 2.125603583 | 0.118644 | 63 | UNKNOWN / UNKNOWN / UNKNOWN |
| values | 142 | 1.317301490 | 0.267420 | 142 | UNKNOWN / UNKNOWN / UNKNOWN |
| allow | 1 | 5.871178381 | 0.001883 | 1 | UNKNOWN / UNKNOWN / UNKNOWN |
| equality | 20 | 3.256218603 | 0.037665 | 20 | UNKNOWN / UNKNOWN / UNKNOWN |
| at | 81 | 1.876040469 | 0.152542 | 81 | UNKNOWN / UNKNOWN / UNKNOWN |
| boundary | 70 | 2.021030780 | 0.131827 | 70 | UNKNOWN / UNKNOWN / UNKNOWN |
| oversized | 8 | 4.136577326 | 0.015066 | 8 | UNKNOWN / UNKNOWN / UNKNOWN |
| disclosure | 52 | 2.315830320 | 0.097928 | 52 | UNKNOWN / UNKNOWN / UNKNOWN |
| before | 77 | 1.926365553 | 0.145009 | 77 | UNKNOWN / UNKNOWN / UNKNOWN |
| creating | 5 | 4.571895397 | 0.009416 | 5 | UNKNOWN / UNKNOWN / UNKNOWN |
| modified | 2 | 5.360352757 | 0.003766 | 2 | UNKNOWN / UNKNOWN / UNKNOWN |
| request | 90 | 1.771293639 | 0.169492 | 90 | UNKNOWN / UNKNOWN / UNKNOWN |
| rather | 58 | 2.207616735 | 0.109228 | 58 | UNKNOWN / UNKNOWN / UNKNOWN |
| than | 65 | 2.094593347 | 0.122411 | 65 | UNKNOWN / UNKNOWN / UNKNOWN |
| truncate | 2 | 5.360352757 | 0.003766 | 2 | UNKNOWN / UNKNOWN / UNKNOWN |
| omit | 5 | 4.571895397 | 0.009416 | 5 | UNKNOWN / UNKNOWN / UNKNOWN |
| items | 74 | 1.965844364 | 0.139360 | 74 | UNKNOWN / UNKNOWN / UNKNOWN |
| change | 27 | 2.962457485 | 0.050847 | 27 | UNKNOWN / UNKNOWN / UNKNOWN |
| representation | 82 | 1.863845196 | 0.154426 | 82 | UNKNOWN / UNKNOWN / UNKNOWN |
| or | 262 | 0.706392407 | 0.493409 | 262 | UNKNOWN / UNKNOWN / UNKNOWN |
| silently | 23 | 3.119643068 | 0.043315 | 23 | UNKNOWN / UNKNOWN / UNKNOWN |
| select | 29 | 2.892253226 | 0.054614 | 29 | UNKNOWN / UNKNOWN / UNKNOWN |
| smaller | 2 | 5.360352757 | 0.003766 | 2 | UNKNOWN / UNKNOWN / UNKNOWN |
| plan | 22 | 3.163128180 | 0.041431 | 22 | UNKNOWN / UNKNOWN / UNKNOWN |
| zero | 58 | 2.207616735 | 0.109228 | 58 | UNKNOWN / UNKNOWN / UNKNOWN |
| permits | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| only | 178 | 1.092054888 | 0.335217 | 178 | UNKNOWN / UNKNOWN / UNKNOWN |
| item | 124 | 1.452337773 | 0.233522 | 124 | UNKNOWN / UNKNOWN / UNKNOWN |
| order | 79 | 1.900886468 | 0.148776 | 79 | UNKNOWN / UNKNOWN / UNKNOWN |
| native | 92 | 1.749434845 | 0.173258 | 92 | UNKNOWN / UNKNOWN / UNKNOWN |
| provenance | 64 | 2.109978266 | 0.120527 | 64 | UNKNOWN / UNKNOWN / UNKNOWN |
| snapshot | 151 | 1.256057864 | 0.284369 | 151 | UNKNOWN / UNKNOWN / UNKNOWN |
| content | 171 | 1.132060223 | 0.322034 | 171 | UNKNOWN / UNKNOWN / UNKNOWN |
| frame | 46 | 2.437191177 | 0.086629 | 46 | UNKNOWN / UNKNOWN / UNKNOWN |
| checks | 22 | 3.163128180 | 0.041431 | 22 | UNKNOWN / UNKNOWN / UNKNOWN |
| prompt | 58 | 2.207616735 | 0.109228 | 58 | UNKNOWN / UNKNOWN / UNKNOWN |
| role | 71 | 2.006946040 | 0.133710 | 71 | UNKNOWN / UNKNOWN / UNKNOWN |
| every | 71 | 2.006946040 | 0.133710 | 71 | UNKNOWN / UNKNOWN / UNKNOWN |
| field | 50 | 2.354670153 | 0.094162 | 50 | UNKNOWN / UNKNOWN / UNKNOWN |
| failure | 67 | 2.064515891 | 0.126177 | 67 | UNKNOWN / UNKNOWN / UNKNOWN |
| must | 129 | 1.412962608 | 0.242938 | 129 | UNKNOWN / UNKNOWN / UNKNOWN |
| leave | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |
| objects | 23 | 3.119643068 | 0.043315 | 23 | UNKNOWN / UNKNOWN / UNKNOWN |
| unchanged | 45 | 2.458931163 | 0.084746 | 45 | UNKNOWN / UNKNOWN / UNKNOWN |
| keep | 22 | 3.163128180 | 0.041431 | 22 | UNKNOWN / UNKNOWN / UNKNOWN |
| capacity | 18 | 3.358872757 | 0.033898 | 18 | UNKNOWN / UNKNOWN / UNKNOWN |
| checking | 1 | 5.871178381 | 0.001883 | 1 | UNKNOWN / UNKNOWN / UNKNOWN |
| in | 270 | 0.676371391 | 0.508475 | 270 | UNKNOWN / UNKNOWN / UNKNOWN |
| common | 17 | 3.414442608 | 0.032015 | 17 | UNKNOWN / UNKNOWN / UNKNOWN |
| planning | 28 | 2.926739402 | 0.052731 | 28 | UNKNOWN / UNKNOWN / UNKNOWN |
| without | 187 | 1.042864644 | 0.352166 | 187 | UNKNOWN / UNKNOWN / UNKNOWN |
| dependency | 68 | 2.049809744 | 0.128060 | 68 | UNKNOWN / UNKNOWN / UNKNOWN |
| on | 65 | 2.094593347 | 0.122411 | 65 | UNKNOWN / UNKNOWN / UNKNOWN |
| language | 18 | 3.358872757 | 0.033898 | 18 | UNKNOWN / UNKNOWN / UNKNOWN |
| specific | 54 | 2.278442788 | 0.101695 | 54 | UNKNOWN / UNKNOWN / UNKNOWN |
| adapter | 33 | 2.765098051 | 0.062147 | 33 | UNKNOWN / UNKNOWN / UNKNOWN |
| retrieval | 94 | 1.728043655 | 0.177024 | 94 | UNKNOWN / UNKNOWN / UNKNOWN |
| whole | 30 | 2.858916806 | 0.056497 | 30 | UNKNOWN / UNKNOWN / UNKNOWN |
| resource | 154 | 1.236449393 | 0.290019 | 154 | UNKNOWN / UNKNOWN / UNKNOWN |
| qualified | 38 | 2.625985248 | 0.071563 | 38 | UNKNOWN / UNKNOWN / UNKNOWN |
| reference | 65 | 2.094593347 | 0.122411 | 65 | UNKNOWN / UNKNOWN / UNKNOWN |
| choices | 20 | 3.256218603 | 0.037665 | 20 | UNKNOWN / UNKNOWN / UNKNOWN |
| follow | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| public | 60 | 2.174000124 | 0.112994 | 60 | UNKNOWN / UNKNOWN / UNKNOWN |
| package | 89 | 1.782404864 | 0.167608 | 89 | UNKNOWN / UNKNOWN / UNKNOWN |
| exports | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| validation | 49 | 2.374670820 | 0.092279 | 49 | UNKNOWN / UNKNOWN / UNKNOWN |
| error | 85 | 1.828127113 | 0.160075 | 85 | UNKNOWN / UNKNOWN / UNKNOWN |
| conventions | 8 | 4.136577326 | 0.015066 | 8 | UNKNOWN / UNKNOWN / UNKNOWN |
| focused | 11 | 3.834296454 | 0.020716 | 11 | UNKNOWN / UNKNOWN / UNKNOWN |
| tests | 204 | 0.956075514 | 0.384181 | 204 | UNKNOWN / UNKNOWN / UNKNOWN |
| boundaries | 50 | 2.354670153 | 0.094162 | 51 | UNKNOWN / UNKNOWN / UNKNOWN |
| non | 62 | 2.141476933 | 0.116761 | 62 | UNKNOWN / UNKNOWN / UNKNOWN |
| ascii | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| ceilings | 1 | 5.871178381 | 0.001883 | 1 | UNKNOWN / UNKNOWN / UNKNOWN |
| foreign | 27 | 2.962457485 | 0.050847 | 27 | UNKNOWN / UNKNOWN / UNKNOWN |
| stale | 38 | 2.625985248 | 0.071563 | 38 | UNKNOWN / UNKNOWN / UNKNOWN |
| frames | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| preservation | 5 | 4.571895397 | 0.009416 | 5 | UNKNOWN / UNKNOWN / UNKNOWN |
| update | 34 | 2.735684165 | 0.064030 | 34 | UNKNOWN / UNKNOWN / UNKNOWN |
| governing | 7 | 4.261740469 | 0.013183 | 7 | UNKNOWN / UNKNOWN / UNKNOWN |
| architecture | 46 | 2.437191177 | 0.086629 | 46 | UNKNOWN / UNKNOWN / UNKNOWN |
| documentation | 29 | 2.892253226 | 0.054614 | 29 | UNKNOWN / UNKNOWN / UNKNOWN |
| run | 78 | 1.913544865 | 0.146893 | 78 | UNKNOWN / UNKNOWN / UNKNOWN |
| protected | 14 | 3.602494840 | 0.026365 | 14 | UNKNOWN / UNKNOWN / UNKNOWN |
| development | 22 | 3.163128180 | 0.041431 | 22 | UNKNOWN / UNKNOWN / UNKNOWN |
| with | 221 | 0.876220900 | 0.416196 | 221 | UNKNOWN / UNKNOWN / UNKNOWN |
| established | 52 | 2.315830320 | 0.097928 | 52 | UNKNOWN / UNKNOWN / UNKNOWN |
| tooling | 11 | 3.834296454 | 0.020716 | 11 | UNKNOWN / UNKNOWN / UNKNOWN |
| configuration | 53 | 2.296961835 | 0.099812 | 53 | UNKNOWN / UNKNOWN / UNKNOWN |
| do | 62 | 2.141476933 | 0.116761 | 62 | UNKNOWN / UNKNOWN / UNKNOWN |
| not | 335 | 0.461021533 | 0.630885 | 335 | UNKNOWN / UNKNOWN / UNKNOWN |
| implement | 16 | 3.473283108 | 0.030132 | 16 | UNKNOWN / UNKNOWN / UNKNOWN |
| automatic | 18 | 3.358872757 | 0.033898 | 18 | UNKNOWN / UNKNOWN / UNKNOWN |
| selection | 59 | 2.190667177 | 0.111111 | 59 | UNKNOWN / UNKNOWN / UNKNOWN |
| token | 24 | 3.077970372 | 0.045198 | 24 | UNKNOWN / UNKNOWN / UNKNOWN |
| estimation | 2 | 5.360352757 | 0.003766 | 2 | UNKNOWN / UNKNOWN / UNKNOWN |
| truncation | 7 | 4.261740469 | 0.013183 | 7 | UNKNOWN / UNKNOWN / UNKNOWN |
| query | 69 | 2.035316737 | 0.129944 | 69 | UNKNOWN / UNKNOWN / UNKNOWN |
| changes | 37 | 2.652302556 | 0.069680 | 37 | UNKNOWN / UNKNOWN / UNKNOWN |
| semantic | 74 | 1.965844364 | 0.139360 | 74 | UNKNOWN / UNKNOWN / UNKNOWN |
| resolution | 80 | 1.888386305 | 0.150659 | 80 | UNKNOWN / UNKNOWN / UNKNOWN |
| persistence | 53 | 2.296961835 | 0.099812 | 53 | UNKNOWN / UNKNOWN / UNKNOWN |
| agent | 50 | 2.354670153 | 0.094162 | 50 | UNKNOWN / UNKNOWN / UNKNOWN |
| execution | 123 | 1.460402333 | 0.231638 | 123 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): from, for, and. No MIXED_INTENT or relevance failure is asserted before gold.

## B.ownership — Arm B

Obligation: ownership. Need: None.

Exact query:

```text
Context Planning capacity assembly ownership dependency
```

Native analyzer terms: `context, planning, capacity, assembly, ownership, dependency`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 264. Query seconds: 0.007432900.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 21.396403280 | 19.726764379 | 6.678555604 | 1.669638901 |
| 2 | `src/devtools/context/planning/docs/overview.md` | 15.380804107 | 15.380804107 | 0.000000000 | 0.000000000 |
| 3 | `docs/architecture.md` | 14.487689298 | 14.487689298 | 0.000000000 | 0.000000000 |
| 4 | `docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md` | 14.394230941 | 14.394230941 | 0.000000000 | 0.000000000 |
| 5 | `docs/backlog/epics/B-0002-coding-context-substrate.md` | 13.573440303 | 12.956873434 | 2.466267475 | 0.616566869 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| planning | 28 | 2.926739402 | 0.052731 | 28 | UNKNOWN / UNKNOWN / UNKNOWN |
| capacity | 18 | 3.358872757 | 0.033898 | 18 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |
| ownership | 46 | 2.437191177 | 0.086629 | 46 | UNKNOWN / UNKNOWN / UNKNOWN |
| dependency | 68 | 2.049809744 | 0.128060 | 68 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, dependency, ownership. No MIXED_INTENT or relevance failure is asserted before gold.

## C.ownership.assembly-owner — Arm C

Obligation: ownership. Need: case-0011-context-utf8-ceiling/ownership/assembly-owner.

Exact need: Which common Context Planning contract owns copied ModelRequest assembly?

Exact query:

```text
Context Planning copied ModelRequest assembly
```

Native analyzer terms: `context, planning, copied, modelrequest, assembly`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': ['ModelRequest']}. Execution count: 1. Positive resources: 252. Query seconds: 0.006725800.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 18.479600854 | 18.479600854 | 0.000000000 | 0.000000000 |
| 2 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 16.358533448 | 14.688894547 | 6.678555604 | 1.669638901 |
| 3 | `src/devtools/context/python/function/request_assembly.py` | 12.816443303 | 12.816443303 | 0.000000000 | 0.000000000 |
| 4 | `tests/context/python/function/test_request_assembly.py` | 12.546351927 | 12.546351927 | 0.000000000 | 0.000000000 |
| 5 | `src/devtools/context/python/function/docs/overview.md` | 11.554609122 | 11.554609122 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| planning | 28 | 2.926739402 | 0.052731 | 28 | UNKNOWN / UNKNOWN / UNKNOWN |
| copied | 6 | 4.404841312 | 0.011299 | 6 | UNKNOWN / UNKNOWN / UNKNOWN |
| modelrequest | 39 | 2.600342817 | 0.073446 | 39 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, modelrequest, planning. No MIXED_INTENT or relevance failure is asserted before gold.

## C.ownership.dependencies — Arm C

Obligation: ownership. Need: case-0011-context-utf8-ceiling/ownership/dependencies.

Exact need: What dependency constraints separate common Context Planning from language-specific adapters and Retrieval?

Exact query:

```text
Context Planning dependency language-specific adapter Retrieval
```

Native analyzer terms: `context, planning, dependency, language, specific, adapter, retrieval`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 274. Query seconds: 0.007529600.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 18.066934666 | 18.066934666 | 0.000000000 | 0.000000000 |
| 2 | `docs/documentation_map.md` | 16.551477864 | 16.551477864 | 0.000000000 | 0.000000000 |
| 3 | `docs/backlog/epics/B-0002-coding-context-substrate.md` | 16.148060196 | 15.531493328 | 2.466267475 | 0.616566869 |
| 4 | `docs/architecture.md` | 15.752322145 | 15.752322145 | 0.000000000 | 0.000000000 |
| 5 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 14.815182142 | 13.739112337 | 4.304279222 | 1.076069806 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| planning | 28 | 2.926739402 | 0.052731 | 28 | UNKNOWN / UNKNOWN / UNKNOWN |
| dependency | 68 | 2.049809744 | 0.128060 | 68 | UNKNOWN / UNKNOWN / UNKNOWN |
| language | 18 | 3.358872757 | 0.033898 | 18 | UNKNOWN / UNKNOWN / UNKNOWN |
| specific | 54 | 2.278442788 | 0.101695 | 54 | UNKNOWN / UNKNOWN / UNKNOWN |
| adapter | 33 | 2.765098051 | 0.062147 | 33 | UNKNOWN / UNKNOWN / UNKNOWN |
| retrieval | 94 | 1.728043655 | 0.177024 | 94 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, retrieval, dependency. No MIXED_INTENT or relevance failure is asserted before gold.

## B.bytes — Arm B

Obligation: bytes. Need: None.

Exact query:

```text
rendered Context UTF-8 byte count headings separators newline task
```

Native analyzer terms: `rendered, context, utf, 8, byte, count, headings, separators, newline, task`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 306. Query seconds: 0.007972800.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `tests/context/python/function/test_request_assembly.py` | 22.579887132 | 22.579887132 | 0.000000000 | 0.000000000 |
| 2 | `src/devtools/context/python/function/request_assembly.py` | 21.991680860 | 21.991680860 | 0.000000000 | 0.000000000 |
| 3 | `src/devtools/resources/filesystem/docs/models.md` | 20.618948222 | 20.618948222 | 0.000000000 | 0.000000000 |
| 4 | `src/devtools/resources/filesystem/models/text.py` | 19.674874931 | 19.674874931 | 0.000000000 | 0.000000000 |
| 5 | `tests/context/repository/test_discovery.py` | 19.330249707 | 19.330249707 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| rendered | 21 | 3.208590554 | 0.039548 | 21 | UNKNOWN / UNKNOWN / UNKNOWN |
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| utf | 99 | 1.676485845 | 0.186441 | 99 | UNKNOWN / UNKNOWN / UNKNOWN |
| 8 | 120 | 1.484993736 | 0.225989 | 120 | UNKNOWN / UNKNOWN / UNKNOWN |
| byte | 31 | 2.826655944 | 0.058380 | 31 | UNKNOWN / UNKNOWN / UNKNOWN |
| count | 55 | 2.260260469 | 0.103578 | 55 | UNKNOWN / UNKNOWN / UNKNOWN |
| headings | 8 | 4.136577326 | 0.015066 | 8 | UNKNOWN / UNKNOWN / UNKNOWN |
| separators | 16 | 3.473283108 | 0.030132 | 16 | UNKNOWN / UNKNOWN / UNKNOWN |
| newline | 24 | 3.077970372 | 0.045198 | 24 | UNKNOWN / UNKNOWN / UNKNOWN |
| task | 78 | 1.913544865 | 0.146893 | 78 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, 8, utf. No MIXED_INTENT or relevance failure is asserted before gold.

## C.bytes.rendered-boundary — Arm C

Obligation: bytes. Need: case-0011-context-utf8-ceiling/bytes/rendered-boundary.

Exact need: What exact rendered Context text, headings and separators are appended during assembly?

Exact query:

```text
rendered Context headings separators appended assembly
```

Native analyzer terms: `rendered, context, headings, separators, appended, assembly`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 263. Query seconds: 0.007009000.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `tests/context/python/function/test_request_assembly.py` | 14.207700210 | 14.207700210 | 0.000000000 | 0.000000000 |
| 2 | `src/devtools/context/python/function/request_assembly.py` | 13.505199699 | 13.505199699 | 0.000000000 | 0.000000000 |
| 3 | `tests/context/python/function/test_cross_resource_pipeline.py` | 11.264208841 | 11.264208841 | 0.000000000 | 0.000000000 |
| 4 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 10.521096088 | 9.445026283 | 4.304279222 | 1.076069806 |
| 5 | `src/devtools/resources/filesystem/docs/models.md` | 9.946740578 | 9.946740578 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| rendered | 21 | 3.208590554 | 0.039548 | 21 | UNKNOWN / UNKNOWN / UNKNOWN |
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| headings | 8 | 4.136577326 | 0.015066 | 8 | UNKNOWN / UNKNOWN / UNKNOWN |
| separators | 16 | 3.473283108 | 0.030132 | 16 | UNKNOWN / UNKNOWN / UNKNOWN |
| appended | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, rendered, separators. No MIXED_INTENT or relevance failure is asserted before gold.

## C.bytes.encoding — Arm C

Obligation: bytes. Need: case-0011-context-utf8-ceiling/bytes/encoding.

Exact need: What existing UTF-8 and newline handling contracts preserve exact rendered text?

Exact query:

```text
UTF-8 newline exact rendered text
```

Native analyzer terms: `utf, 8, newline, exact, rendered, text`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 273. Query seconds: 0.007562400.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `tests/context/python/test_source_candidacy.py` | 17.499062546 | 17.499062546 | 0.000000000 | 0.000000000 |
| 2 | `tests/context/repository/test_discovery.py` | 17.045941021 | 17.045941021 | 0.000000000 | 0.000000000 |
| 3 | `tests/context/python/function/test_rendering.py` | 16.379302441 | 16.379302441 | 0.000000000 | 0.000000000 |
| 4 | `tests/context/python/function/test_cross_resource_pipeline.py` | 15.493563882 | 15.493563882 | 0.000000000 | 0.000000000 |
| 5 | `tests/context/python/function/test_request_assembly.py` | 15.197889435 | 15.197889435 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| utf | 99 | 1.676485845 | 0.186441 | 99 | UNKNOWN / UNKNOWN / UNKNOWN |
| 8 | 120 | 1.484993736 | 0.225989 | 120 | UNKNOWN / UNKNOWN / UNKNOWN |
| newline | 24 | 3.077970372 | 0.045198 | 24 | UNKNOWN / UNKNOWN / UNKNOWN |
| exact | 147 | 1.282815314 | 0.276836 | 147 | UNKNOWN / UNKNOWN / UNKNOWN |
| rendered | 21 | 3.208590554 | 0.039548 | 21 | UNKNOWN / UNKNOWN / UNKNOWN |
| text | 168 | 1.149707740 | 0.316384 | 168 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): text, exact, 8. No MIXED_INTENT or relevance failure is asserted before gold.

## B.ceiling — Arm B

Obligation: ceiling. Need: None.

Exact query:

```text
optional maximum byte count None integer validation reject boundary truncate
```

Native analyzer terms: `optional, maximum, byte, count, none, integer, validation, reject, boundary, truncate`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 354. Query seconds: 0.008115700.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/models/interaction/usage.py` | 16.975524452 | 16.975524452 | 0.000000000 | 0.000000000 |
| 2 | `tests/models/interaction/test_models.py` | 15.545208416 | 15.545208416 | 0.000000000 | 0.000000000 |
| 3 | `src/devtools/models/interaction/models.py` | 15.277209056 | 15.277209056 | 0.000000000 | 0.000000000 |
| 4 | `docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md` | 13.294125073 | 13.294125073 | 0.000000000 | 0.000000000 |
| 5 | `src/devtools/resources/filesystem/reading.py` | 12.252278814 | 12.252278814 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| optional | 53 | 2.296961835 | 0.099812 | 53 | UNKNOWN / UNKNOWN / UNKNOWN |
| maximum | 27 | 2.962457485 | 0.050847 | 27 | UNKNOWN / UNKNOWN / UNKNOWN |
| byte | 31 | 2.826655944 | 0.058380 | 31 | UNKNOWN / UNKNOWN / UNKNOWN |
| count | 55 | 2.260260469 | 0.103578 | 55 | UNKNOWN / UNKNOWN / UNKNOWN |
| none | 311 | 0.535244151 | 0.585687 | 311 | UNKNOWN / UNKNOWN / UNKNOWN |
| integer | 21 | 3.208590554 | 0.039548 | 21 | UNKNOWN / UNKNOWN / UNKNOWN |
| validation | 49 | 2.374670820 | 0.092279 | 49 | UNKNOWN / UNKNOWN / UNKNOWN |
| reject | 52 | 2.315830320 | 0.097928 | 52 | UNKNOWN / UNKNOWN / UNKNOWN |
| boundary | 70 | 2.021030780 | 0.131827 | 70 | UNKNOWN / UNKNOWN / UNKNOWN |
| truncate | 2 | 5.360352757 | 0.003766 | 2 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): none, boundary, count. No MIXED_INTENT or relevance failure is asserted before gold.

## C.ceiling.validation — Arm C

Obligation: ceiling. Need: case-0011-context-utf8-ceiling/ceiling/validation.

Exact need: What existing validation and error conventions apply to optional nonnegative integer limits and invalid booleans?

Exact query:

```text
optional nonnegative integer limits booleans validation error
```

Native analyzer terms: `optional, nonnegative, integer, limits, booleans, validation, error`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 156. Query seconds: 0.006760800.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/models/benchmarks/storage.py` | 16.643603861 | 16.643603861 | 0.000000000 | 0.000000000 |
| 2 | `tests/models/interaction/test_models.py` | 15.793658163 | 15.793658163 | 0.000000000 | 0.000000000 |
| 3 | `src/devtools/context/localization/identity.py` | 11.946382020 | 11.946382020 | 0.000000000 | 0.000000000 |
| 4 | `docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md` | 10.046245339 | 10.046245339 | 0.000000000 | 0.000000000 |
| 5 | `tests/resources/commands/test_models.py` | 9.898855496 | 9.898855496 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| optional | 53 | 2.296961835 | 0.099812 | 53 | UNKNOWN / UNKNOWN / UNKNOWN |
| nonnegative | 8 | 4.136577326 | 0.015066 | 8 | UNKNOWN / UNKNOWN / UNKNOWN |
| integer | 21 | 3.208590554 | 0.039548 | 21 | UNKNOWN / UNKNOWN / UNKNOWN |
| limits | 19 | 3.306229024 | 0.035782 | 19 | UNKNOWN / UNKNOWN / UNKNOWN |
| booleans | 3 | 5.023880521 | 0.005650 | 3 | UNKNOWN / UNKNOWN / UNKNOWN |
| validation | 49 | 2.374670820 | 0.092279 | 49 | UNKNOWN / UNKNOWN / UNKNOWN |
| error | 85 | 1.828127113 | 0.160075 | 85 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): error, optional, validation. No MIXED_INTENT or relevance failure is asserted before gold.

## C.ceiling.rejection — Arm C

Obligation: ceiling. Need: case-0011-context-utf8-ceiling/ceiling/rejection.

Exact need: What assembly contract permits rejection before modifying a request, without truncating or omitting items?

Exact query:

```text
assembly reject request truncate omit items unchanged
```

Native analyzer terms: `assembly, reject, request, truncate, omit, items, unchanged`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 191. Query seconds: 0.007808700.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/python/function/request_assembly.py` | 14.014658758 | 14.014658758 | 0.000000000 | 0.000000000 |
| 2 | `tests/context/python/function/test_request_assembly.py` | 12.274212355 | 12.274212355 | 0.000000000 | 0.000000000 |
| 3 | `src/devtools/observability/evidence/model_interaction.py` | 11.669861868 | 11.669861868 | 0.000000000 | 0.000000000 |
| 4 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 10.702332973 | 10.108763878 | 2.374276382 | 0.593569095 |
| 5 | `tests/context/python/function/test_cross_resource_pipeline.py` | 10.599030231 | 10.599030231 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |
| reject | 52 | 2.315830320 | 0.097928 | 52 | UNKNOWN / UNKNOWN / UNKNOWN |
| request | 90 | 1.771293639 | 0.169492 | 90 | UNKNOWN / UNKNOWN / UNKNOWN |
| truncate | 2 | 5.360352757 | 0.003766 | 2 | UNKNOWN / UNKNOWN / UNKNOWN |
| omit | 5 | 4.571895397 | 0.009416 | 5 | UNKNOWN / UNKNOWN / UNKNOWN |
| items | 74 | 1.965844364 | 0.139360 | 74 | UNKNOWN / UNKNOWN / UNKNOWN |
| unchanged | 45 | 2.458931163 | 0.084746 | 45 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): request, items, reject. No MIXED_INTENT or relevance failure is asserted before gold.

## B.request — Arm B

Obligation: request. Need: None.

Exact query:

```text
copied ModelRequest original task Prompt role fields preservation
```

Native analyzer terms: `copied, modelrequest, original, task, prompt, role, fields, preservation`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': ['ModelRequest']}. Execution count: 1. Positive resources: 167. Query seconds: 0.006981500.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/python/function/request_assembly.py` | 16.635127184 | 16.635127184 | 0.000000000 | 0.000000000 |
| 2 | `src/devtools/context/planning/rendering.py` | 15.959973344 | 15.959973344 | 0.000000000 | 0.000000000 |
| 3 | `tests/context/python/function/test_request_assembly.py` | 15.604787767 | 15.604787767 | 0.000000000 | 0.000000000 |
| 4 | `tests/observability/evidence/test_model_interaction.py` | 14.859511791 | 14.859511791 | 0.000000000 | 0.000000000 |
| 5 | `src/devtools/context/python/function/docs/overview.md` | 14.112750959 | 14.112750959 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| copied | 6 | 4.404841312 | 0.011299 | 6 | UNKNOWN / UNKNOWN / UNKNOWN |
| modelrequest | 39 | 2.600342817 | 0.073446 | 39 | UNKNOWN / UNKNOWN / UNKNOWN |
| original | 45 | 2.458931163 | 0.084746 | 45 | UNKNOWN / UNKNOWN / UNKNOWN |
| task | 78 | 1.913544865 | 0.146893 | 78 | UNKNOWN / UNKNOWN / UNKNOWN |
| prompt | 58 | 2.207616735 | 0.109228 | 58 | UNKNOWN / UNKNOWN / UNKNOWN |
| role | 71 | 2.006946040 | 0.133710 | 71 | UNKNOWN / UNKNOWN / UNKNOWN |
| fields | 16 | 3.473283108 | 0.030132 | 16 | UNKNOWN / UNKNOWN / UNKNOWN |
| preservation | 5 | 4.571895397 | 0.009416 | 5 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): task, role, prompt. No MIXED_INTENT or relevance failure is asserted before gold.

## C.request.copy — Arm C

Obligation: request. Need: case-0011-context-utf8-ceiling/request/copy.

Exact need: How does copied ModelRequest assembly preserve all fields other than the appended Context?

Exact query:

```text
copied ModelRequest assembly fields preserve Context
```

Native analyzer terms: `copied, modelrequest, assembly, fields, preserve, context`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': ['ModelRequest']}. Execution count: 1. Positive resources: 276. Query seconds: 0.006913700.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 14.198366354 | 14.198366354 | 0.000000000 | 0.000000000 |
| 2 | `src/devtools/context/python/function/request_assembly.py` | 12.816443303 | 12.816443303 | 0.000000000 | 0.000000000 |
| 3 | `tests/context/python/function/test_request_assembly.py` | 12.546351927 | 12.546351927 | 0.000000000 | 0.000000000 |
| 4 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 12.456645625 | 11.380575819 | 4.304279222 | 1.076069806 |
| 5 | `docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md` | 11.141614573 | 11.141614573 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| copied | 6 | 4.404841312 | 0.011299 | 6 | UNKNOWN / UNKNOWN / UNKNOWN |
| modelrequest | 39 | 2.600342817 | 0.073446 | 39 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |
| fields | 16 | 3.473283108 | 0.030132 | 16 | UNKNOWN / UNKNOWN / UNKNOWN |
| preserve | 50 | 2.354670153 | 0.094162 | 50 | UNKNOWN / UNKNOWN / UNKNOWN |
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, preserve, modelrequest. No MIXED_INTENT or relevance failure is asserted before gold.

## C.request.prompt — Arm C

Obligation: request. Need: case-0011-context-utf8-ceiling/request/prompt.

Exact need: How are the original task text and Prompt role preserved when Context is appended?

Exact query:

```text
original task text Prompt role Context appended
```

Native analyzer terms: `original, task, text, prompt, role, context, appended`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 352. Query seconds: 0.007938700.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/python/function/request_assembly.py` | 15.499683006 | 15.499683006 | 0.000000000 | 0.000000000 |
| 2 | `src/devtools/context/planning/rendering.py` | 15.187432241 | 15.187432241 | 0.000000000 | 0.000000000 |
| 3 | `tests/context/python/function/test_request_assembly.py` | 14.583023294 | 14.583023294 | 0.000000000 | 0.000000000 |
| 4 | `tests/agents/conversation/history/test_history.py` | 14.038860669 | 14.038860669 | 0.000000000 | 0.000000000 |
| 5 | `tests/context/localization/test_lexical.py` | 13.188778525 | 13.188778525 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| original | 45 | 2.458931163 | 0.084746 | 45 | UNKNOWN / UNKNOWN / UNKNOWN |
| task | 78 | 1.913544865 | 0.146893 | 78 | UNKNOWN / UNKNOWN / UNKNOWN |
| text | 168 | 1.149707740 | 0.316384 | 168 | UNKNOWN / UNKNOWN / UNKNOWN |
| prompt | 58 | 2.207616735 | 0.109228 | 58 | UNKNOWN / UNKNOWN / UNKNOWN |
| role | 71 | 2.006946040 | 0.133710 | 71 | UNKNOWN / UNKNOWN / UNKNOWN |
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| appended | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, text, task. No MIXED_INTENT or relevance failure is asserted before gold.

## B.frame — Arm B

Obligation: frame. Need: None.

Exact query:

```text
ContextDisclosure DisclosurePlan repository snapshot content frame provenance order
```

Native analyzer terms: `contextdisclosure, disclosureplan, repository, snapshot, content, frame, provenance, order`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': ['ContextDisclosure', 'DisclosurePlan']}. Execution count: 1. Positive resources: 303. Query seconds: 0.007288500.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 26.190814079 | 26.190814079 | 0.000000000 | 0.000000000 |
| 2 | `src/devtools/context/planning/materialization.py` | 18.784401864 | 18.784401864 | 0.000000000 | 0.000000000 |
| 3 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 16.885620810 | 16.885620810 | 0.000000000 | 0.000000000 |
| 4 | `docs/architecture.md` | 16.087033320 | 16.087033320 | 0.000000000 | 0.000000000 |
| 5 | `tests/context/planning/test_plan.py` | 15.323331853 | 15.323331853 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| contextdisclosure | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| disclosureplan | 14 | 3.602494840 | 0.026365 | 14 | UNKNOWN / UNKNOWN / UNKNOWN |
| repository | 217 | 0.894444639 | 0.408663 | 217 | UNKNOWN / UNKNOWN / UNKNOWN |
| snapshot | 151 | 1.256057864 | 0.284369 | 151 | UNKNOWN / UNKNOWN / UNKNOWN |
| content | 171 | 1.132060223 | 0.322034 | 171 | UNKNOWN / UNKNOWN / UNKNOWN |
| frame | 46 | 2.437191177 | 0.086629 | 46 | UNKNOWN / UNKNOWN / UNKNOWN |
| provenance | 64 | 2.109978266 | 0.120527 | 64 | UNKNOWN / UNKNOWN / UNKNOWN |
| order | 79 | 1.900886468 | 0.148776 | 79 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): repository, content, snapshot. No MIXED_INTENT or relevance failure is asserted before gold.

## C.frame.binding — Arm C

Obligation: frame. Need: case-0011-context-utf8-ceiling/frame/binding.

Exact need: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Exact query:

```text
ContextDisclosure DisclosurePlan repository snapshot content frame checks
```

Native analyzer terms: `contextdisclosure, disclosureplan, repository, snapshot, content, frame, checks`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': ['ContextDisclosure', 'DisclosurePlan']}. Execution count: 1. Positive resources: 290. Query seconds: 0.007663900.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 23.789420635 | 23.789420635 | 0.000000000 | 0.000000000 |
| 2 | `src/devtools/context/planning/materialization.py` | 18.784401864 | 18.784401864 | 0.000000000 | 0.000000000 |
| 3 | `tests/context/planning/test_plan.py` | 15.323331853 | 15.323331853 | 0.000000000 | 0.000000000 |
| 4 | `src/devtools/context/planning/__init__.py` | 14.933144112 | 14.933144112 | 0.000000000 | 0.000000000 |
| 5 | `src/devtools/context/__init__.py` | 13.588083915 | 13.588083915 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| contextdisclosure | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| disclosureplan | 14 | 3.602494840 | 0.026365 | 14 | UNKNOWN / UNKNOWN / UNKNOWN |
| repository | 217 | 0.894444639 | 0.408663 | 217 | UNKNOWN / UNKNOWN / UNKNOWN |
| snapshot | 151 | 1.256057864 | 0.284369 | 151 | UNKNOWN / UNKNOWN / UNKNOWN |
| content | 171 | 1.132060223 | 0.322034 | 171 | UNKNOWN / UNKNOWN / UNKNOWN |
| frame | 46 | 2.437191177 | 0.086629 | 46 | UNKNOWN / UNKNOWN / UNKNOWN |
| checks | 22 | 3.163128180 | 0.041431 | 22 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): repository, content, snapshot. No MIXED_INTENT or relevance failure is asserted before gold.

## C.frame.items — Arm C

Obligation: frame. Need: case-0011-context-utf8-ceiling/frame/items.

Exact need: What contracts retain item order, exact item text and native disclosure provenance?

Exact query:

```text
item order exact text native disclosure provenance
```

Native analyzer terms: `item, order, exact, text, native, disclosure, provenance`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 303. Query seconds: 0.008001700.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 18.011594101 | 18.011594101 | 0.000000000 | 0.000000000 |
| 2 | `docs/architecture.md` | 14.976951387 | 14.976951387 | 0.000000000 | 0.000000000 |
| 3 | `src/devtools/context/planning/rendering.py` | 14.156002770 | 14.156002770 | 0.000000000 | 0.000000000 |
| 4 | `docs/documentation_map.md` | 13.839485565 | 13.839485565 | 0.000000000 | 0.000000000 |
| 5 | `src/devtools/context/retrieval/docs/overview.md` | 13.644404338 | 13.644404338 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| item | 124 | 1.452337773 | 0.233522 | 124 | UNKNOWN / UNKNOWN / UNKNOWN |
| order | 79 | 1.900886468 | 0.148776 | 79 | UNKNOWN / UNKNOWN / UNKNOWN |
| exact | 147 | 1.282815314 | 0.276836 | 147 | UNKNOWN / UNKNOWN / UNKNOWN |
| text | 168 | 1.149707740 | 0.316384 | 168 | UNKNOWN / UNKNOWN / UNKNOWN |
| native | 92 | 1.749434845 | 0.173258 | 92 | UNKNOWN / UNKNOWN / UNKNOWN |
| disclosure | 52 | 2.315830320 | 0.097928 | 52 | UNKNOWN / UNKNOWN / UNKNOWN |
| provenance | 64 | 2.109978266 | 0.120527 | 64 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): text, exact, item. No MIXED_INTENT or relevance failure is asserted before gold.

## B.exports — Arm B

Obligation: exports. Need: None.

Exact query:

```text
Context Planning public package exports assembly
```

Native analyzer terms: `context, planning, public, package, exports, assembly`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 282. Query seconds: 0.007238200.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 15.739032439 | 14.069393538 | 6.678555604 | 1.669638901 |
| 2 | `docs/documentation_map.md` | 12.755939352 | 12.755939352 | 0.000000000 | 0.000000000 |
| 3 | `src/devtools/context/planning/docs/overview.md` | 12.456931405 | 12.456931405 | 0.000000000 | 0.000000000 |
| 4 | `docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md` | 12.444077607 | 12.444077607 | 0.000000000 | 0.000000000 |
| 5 | `docs/backlog/epics/B-0002-coding-context-substrate.md` | 11.634545291 | 11.017978422 | 2.466267475 | 0.616566869 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| planning | 28 | 2.926739402 | 0.052731 | 28 | UNKNOWN / UNKNOWN / UNKNOWN |
| public | 60 | 2.174000124 | 0.112994 | 60 | UNKNOWN / UNKNOWN / UNKNOWN |
| package | 89 | 1.782404864 | 0.167608 | 89 | UNKNOWN / UNKNOWN / UNKNOWN |
| exports | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, package, public. No MIXED_INTENT or relevance failure is asserted before gold.

## C.exports.public-boundary — Arm C

Obligation: exports. Need: case-0011-context-utf8-ceiling/exports/public-boundary.

Exact need: What public Context Planning package exports expose copied assembly to callers?

Exact query:

```text
public Context Planning package exports copied assembly
```

Native analyzer terms: `public, context, planning, package, exports, copied, assembly`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 282. Query seconds: 0.007597500.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 17.283121187 | 17.283121187 | 0.000000000 | 0.000000000 |
| 2 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 15.739032439 | 14.069393538 | 6.678555604 | 1.669638901 |
| 3 | `docs/documentation_map.md` | 12.755939352 | 12.755939352 | 0.000000000 | 0.000000000 |
| 4 | `docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md` | 12.444077607 | 12.444077607 | 0.000000000 | 0.000000000 |
| 5 | `src/devtools/context/localization/roles/docs/overview.md` | 12.085994719 | 12.085994719 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| public | 60 | 2.174000124 | 0.112994 | 60 | UNKNOWN / UNKNOWN / UNKNOWN |
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| planning | 28 | 2.926739402 | 0.052731 | 28 | UNKNOWN / UNKNOWN / UNKNOWN |
| package | 89 | 1.782404864 | 0.167608 | 89 | UNKNOWN / UNKNOWN / UNKNOWN |
| exports | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| copied | 6 | 4.404841312 | 0.011299 | 6 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, package, public. No MIXED_INTENT or relevance failure is asserted before gold.

## B.tests — Arm B

Obligation: tests. Need: None.

Exact query:

```text
tests copied assembly UTF-8 newline invalid ceiling snapshot frame preservation
```

Native analyzer terms: `tests, copied, assembly, utf, 8, newline, invalid, ceiling, snapshot, frame, preservation`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 321. Query seconds: 0.007305100.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 17.192955664 | 17.192955664 | 0.000000000 | 0.000000000 |
| 2 | `tests/context/python/function/test_request_assembly.py` | 14.715309464 | 14.715309464 | 0.000000000 | 0.000000000 |
| 3 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 13.621246539 | 13.027677444 | 2.374276382 | 0.593569095 |
| 4 | `tests/context/repository/test_discovery.py` | 13.528691948 | 13.528691948 | 0.000000000 | 0.000000000 |
| 5 | `tests/context/python/project_configuration/test_configuration.py` | 13.333544739 | 13.333544739 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| tests | 204 | 0.956075514 | 0.384181 | 204 | UNKNOWN / UNKNOWN / UNKNOWN |
| copied | 6 | 4.404841312 | 0.011299 | 6 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |
| utf | 99 | 1.676485845 | 0.186441 | 99 | UNKNOWN / UNKNOWN / UNKNOWN |
| 8 | 120 | 1.484993736 | 0.225989 | 120 | UNKNOWN / UNKNOWN / UNKNOWN |
| newline | 24 | 3.077970372 | 0.045198 | 24 | UNKNOWN / UNKNOWN / UNKNOWN |
| invalid | 63 | 2.125603583 | 0.118644 | 63 | UNKNOWN / UNKNOWN / UNKNOWN |
| ceiling | 3 | 5.023880521 | 0.005650 | 3 | UNKNOWN / UNKNOWN / UNKNOWN |
| snapshot | 151 | 1.256057864 | 0.284369 | 151 | UNKNOWN / UNKNOWN / UNKNOWN |
| frame | 46 | 2.437191177 | 0.086629 | 46 | UNKNOWN / UNKNOWN / UNKNOWN |
| preservation | 5 | 4.571895397 | 0.009416 | 5 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): tests, snapshot, 8. No MIXED_INTENT or relevance failure is asserted before gold.

## C.tests.text-boundaries — Arm C

Obligation: tests. Need: case-0011-context-utf8-ceiling/tests/text-boundaries.

Exact need: Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Exact query:

```text
tests fixtures exact text non-ASCII newline boundary
```

Native analyzer terms: `tests, fixtures, exact, text, non, ascii, newline, boundary`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 377. Query seconds: 0.008216900.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `tests/context/python/function/test_materialization.py` | 14.180194322 | 14.180194322 | 0.000000000 | 0.000000000 |
| 2 | `src/devtools/resources/filesystem/docs/json.md` | 14.147554958 | 14.147554958 | 0.000000000 | 0.000000000 |
| 3 | `tests/context/python/function/test_declarations.py` | 13.010504832 | 13.010504832 | 0.000000000 | 0.000000000 |
| 4 | `tests/context/python/function/test_rendering.py` | 11.315885109 | 11.315885109 | 0.000000000 | 0.000000000 |
| 5 | `src/devtools/resources/filesystem/codecs/json.py` | 11.011126526 | 11.011126526 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| tests | 204 | 0.956075514 | 0.384181 | 204 | UNKNOWN / UNKNOWN / UNKNOWN |
| fixtures | 11 | 3.834296454 | 0.020716 | 11 | UNKNOWN / UNKNOWN / UNKNOWN |
| exact | 147 | 1.282815314 | 0.276836 | 147 | UNKNOWN / UNKNOWN / UNKNOWN |
| text | 168 | 1.149707740 | 0.316384 | 168 | UNKNOWN / UNKNOWN / UNKNOWN |
| non | 62 | 2.141476933 | 0.116761 | 62 | UNKNOWN / UNKNOWN / UNKNOWN |
| ascii | 12 | 3.750914845 | 0.022599 | 12 | UNKNOWN / UNKNOWN / UNKNOWN |
| newline | 24 | 3.077970372 | 0.045198 | 24 | UNKNOWN / UNKNOWN / UNKNOWN |
| boundary | 70 | 2.021030780 | 0.131827 | 70 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): tests, text, exact. No MIXED_INTENT or relevance failure is asserted before gold.

## C.tests.frame-rejection — Arm C

Obligation: tests. Need: case-0011-context-utf8-ceiling/tests/frame-rejection.

Exact need: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Exact query:

```text
tests foreign stale repository snapshot content frame rejection
```

Native analyzer terms: `tests, foreign, stale, repository, snapshot, content, frame, rejection`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 373. Query seconds: 0.007866600.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `tests/context/localization/association/test_hypothesis.py` | 19.437687725 | 19.437687725 | 0.000000000 | 0.000000000 |
| 2 | `tests/context/localization/resolution/test_resolution.py` | 18.752792261 | 18.752792261 | 0.000000000 | 0.000000000 |
| 3 | `src/devtools/context/python/project_configuration/docs/overview.md` | 16.964068443 | 16.964068443 | 0.000000000 | 0.000000000 |
| 4 | `tests/context/python/project_configuration/test_configuration.py` | 15.704706162 | 15.704706162 | 0.000000000 | 0.000000000 |
| 5 | `src/devtools/context/localization/association/references.py` | 14.939944187 | 14.939944187 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| tests | 204 | 0.956075514 | 0.384181 | 204 | UNKNOWN / UNKNOWN / UNKNOWN |
| foreign | 27 | 2.962457485 | 0.050847 | 27 | UNKNOWN / UNKNOWN / UNKNOWN |
| stale | 38 | 2.625985248 | 0.071563 | 38 | UNKNOWN / UNKNOWN / UNKNOWN |
| repository | 217 | 0.894444639 | 0.408663 | 217 | UNKNOWN / UNKNOWN / UNKNOWN |
| snapshot | 151 | 1.256057864 | 0.284369 | 151 | UNKNOWN / UNKNOWN / UNKNOWN |
| content | 171 | 1.132060223 | 0.322034 | 171 | UNKNOWN / UNKNOWN / UNKNOWN |
| frame | 46 | 2.437191177 | 0.086629 | 46 | UNKNOWN / UNKNOWN / UNKNOWN |
| rejection | 4 | 4.772566093 | 0.007533 | 4 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): repository, tests, content. No MIXED_INTENT or relevance failure is asserted before gold.

## C.tests.request-preservation — Arm C

Obligation: tests. Need: case-0011-context-utf8-ceiling/tests/request-preservation.

Exact need: Which tests establish copied-request preservation and invalid argument validation?

Exact query:

```text
tests copied request preservation invalid argument validation
```

Native analyzer terms: `tests, copied, request, preservation, invalid, argument, validation`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 284. Query seconds: 0.032552600.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/agents/integrations/codex/docs/cli.md` | 9.522116872 | 9.522116872 | 0.000000000 | 0.000000000 |
| 2 | `tests/context/localization/routing/test_routing.py` | 9.310418776 | 9.310418776 | 0.000000000 | 0.000000000 |
| 3 | `docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md` | 9.079260046 | 9.079260046 | 0.000000000 | 0.000000000 |
| 4 | `src/devtools/context/python/project_configuration/docs/overview.md` | 8.338799919 | 8.338799919 | 0.000000000 | 0.000000000 |
| 5 | `docs/development/validation.md` | 7.581926235 | 6.121079213 | 5.843388087 | 1.460847022 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| tests | 204 | 0.956075514 | 0.384181 | 204 | UNKNOWN / UNKNOWN / UNKNOWN |
| copied | 6 | 4.404841312 | 0.011299 | 6 | UNKNOWN / UNKNOWN / UNKNOWN |
| request | 90 | 1.771293639 | 0.169492 | 90 | UNKNOWN / UNKNOWN / UNKNOWN |
| preservation | 5 | 4.571895397 | 0.009416 | 5 | UNKNOWN / UNKNOWN / UNKNOWN |
| invalid | 63 | 2.125603583 | 0.118644 | 63 | UNKNOWN / UNKNOWN / UNKNOWN |
| argument | 11 | 3.834296454 | 0.020716 | 11 | UNKNOWN / UNKNOWN / UNKNOWN |
| validation | 49 | 2.374670820 | 0.092279 | 49 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): tests, request, invalid. No MIXED_INTENT or relevance failure is asserted before gold.

## B.documentation — Arm B

Obligation: documentation. Need: None.

Exact query:

```text
architecture package documentation Context capacity rendering assembly
```

Native analyzer terms: `architecture, package, documentation, context, capacity, rendering, assembly`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 275. Query seconds: 0.007251900.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 22.035191530 | 22.035191530 | 0.000000000 | 0.000000000 |
| 2 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 18.932514586 | 17.856444780 | 4.304279222 | 1.076069806 |
| 3 | `docs/architecture.md` | 16.544999858 | 15.157230198 | 5.551078640 | 1.387769660 |
| 4 | `docs/documentation_map.md` | 16.311575788 | 16.311575788 | 0.000000000 | 0.000000000 |
| 5 | `docs/backlog/epics/B-0001-architecture-documentation-integrity.md` | 15.167407755 | 13.901806756 | 5.062403994 | 1.265600999 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| architecture | 46 | 2.437191177 | 0.086629 | 46 | UNKNOWN / UNKNOWN / UNKNOWN |
| package | 89 | 1.782404864 | 0.167608 | 89 | UNKNOWN / UNKNOWN / UNKNOWN |
| documentation | 29 | 2.892253226 | 0.054614 | 29 | UNKNOWN / UNKNOWN / UNKNOWN |
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| capacity | 18 | 3.358872757 | 0.033898 | 18 | UNKNOWN / UNKNOWN / UNKNOWN |
| rendering | 20 | 3.256218603 | 0.037665 | 21 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, package, architecture. No MIXED_INTENT or relevance failure is asserted before gold.

## C.documentation.architecture — Arm C

Obligation: documentation. Need: case-0011-context-utf8-ceiling/documentation/architecture.

Exact need: What governing architecture documentation distinguishes Context capacity from automatic selection?

Exact query:

```text
architecture documentation Context capacity automatic selection
```

Native analyzer terms: `architecture, documentation, context, capacity, automatic, selection`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 260. Query seconds: 0.007412800.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 17.952880587 | 17.952880587 | 0.000000000 | 0.000000000 |
| 2 | `docs/architecture.md` | 15.210932427 | 13.823162767 | 5.551078640 | 1.387769660 |
| 3 | `docs/roadmap.md` | 14.055869440 | 14.055869440 | 0.000000000 | 0.000000000 |
| 4 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 14.046704966 | 13.564204256 | 1.930002841 | 0.482500710 |
| 5 | `docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md` | 13.848088828 | 13.848088828 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| architecture | 46 | 2.437191177 | 0.086629 | 46 | UNKNOWN / UNKNOWN / UNKNOWN |
| documentation | 29 | 2.892253226 | 0.054614 | 29 | UNKNOWN / UNKNOWN / UNKNOWN |
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| capacity | 18 | 3.358872757 | 0.033898 | 18 | UNKNOWN / UNKNOWN / UNKNOWN |
| automatic | 18 | 3.358872757 | 0.033898 | 18 | UNKNOWN / UNKNOWN / UNKNOWN |
| selection | 59 | 2.190667177 | 0.111111 | 59 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, selection, architecture. No MIXED_INTENT or relevance failure is asserted before gold.

## C.documentation.package — Arm C

Obligation: documentation. Need: case-0011-context-utf8-ceiling/documentation/package.

Exact need: What package documentation describes rendered Context and copied assembly contracts?

Exact query:

```text
package documentation rendered Context copied assembly contracts
```

Native analyzer terms: `package, documentation, rendered, context, copied, assembly, contracts`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 268. Query seconds: 0.007502200.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `src/devtools/context/planning/docs/overview.md` | 16.517397428 | 16.517397428 | 0.000000000 | 0.000000000 |
| 2 | `docs/documentation_map.md` | 14.583636248 | 14.583636248 | 0.000000000 | 0.000000000 |
| 3 | `tests/context/python/function/test_request_assembly.py` | 14.207700210 | 14.207700210 | 0.000000000 | 0.000000000 |
| 4 | `src/devtools/context/python/function/request_assembly.py` | 13.505199699 | 13.505199699 | 0.000000000 | 0.000000000 |
| 5 | `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` | 13.199623496 | 12.123553691 | 4.304279222 | 1.076069806 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| package | 89 | 1.782404864 | 0.167608 | 89 | UNKNOWN / UNKNOWN / UNKNOWN |
| documentation | 29 | 2.892253226 | 0.054614 | 29 | UNKNOWN / UNKNOWN / UNKNOWN |
| rendered | 21 | 3.208590554 | 0.039548 | 21 | UNKNOWN / UNKNOWN / UNKNOWN |
| context | 234 | 0.819187901 | 0.440678 | 234 | UNKNOWN / UNKNOWN / UNKNOWN |
| copied | 6 | 4.404841312 | 0.011299 | 6 | UNKNOWN / UNKNOWN / UNKNOWN |
| assembly | 13 | 3.673953804 | 0.024482 | 13 | UNKNOWN / UNKNOWN / UNKNOWN |
| contracts | 11 | 3.834296454 | 0.020716 | 11 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): context, package, documentation. No MIXED_INTENT or relevance failure is asserted before gold.

## B.validation — Arm B

Obligation: validation. Need: None.

Exact query:

```text
protected development validation tooling configuration tests
```

Native analyzer terms: `protected, development, validation, tooling, configuration, tests`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 251. Query seconds: 0.007140400.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `docs/development/validation.md` | 23.398644758 | 21.937797736 | 5.843388087 | 1.460847022 |
| 2 | `docs/backlog/items/B-0047-protected-development-validation-profile.md` | 21.158677994 | 19.256866812 | 7.607244728 | 1.901811182 |
| 3 | `src/devtools/context/python/project_configuration/docs/overview.md` | 17.125318017 | 17.125318017 | 0.000000000 | 0.000000000 |
| 4 | `docs/backlog/overview.md` | 15.162593812 | 15.162593812 | 0.000000000 | 0.000000000 |
| 5 | `tests/scripts/test_validate_development.py` | 14.439350953 | 14.439350953 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| protected | 14 | 3.602494840 | 0.026365 | 14 | UNKNOWN / UNKNOWN / UNKNOWN |
| development | 22 | 3.163128180 | 0.041431 | 22 | UNKNOWN / UNKNOWN / UNKNOWN |
| validation | 49 | 2.374670820 | 0.092279 | 49 | UNKNOWN / UNKNOWN / UNKNOWN |
| tooling | 11 | 3.834296454 | 0.020716 | 11 | UNKNOWN / UNKNOWN / UNKNOWN |
| configuration | 53 | 2.296961835 | 0.099812 | 53 | UNKNOWN / UNKNOWN / UNKNOWN |
| tests | 204 | 0.956075514 | 0.384181 | 204 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): tests, configuration, validation. No MIXED_INTENT or relevance failure is asserted before gold.

## C.validation.protected-entry — Arm C

Obligation: validation. Need: case-0011-context-utf8-ceiling/validation/protected-entry.

Exact need: What established entry point runs protected development validation?

Exact query:

```text
protected development validation entry point
```

Native analyzer terms: `protected, development, validation, entry, point`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 72. Query seconds: 0.006483300.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `docs/backlog/items/B-0047-protected-development-validation-profile.md` | 26.986408845 | 25.084597663 | 7.607244728 | 1.901811182 |
| 2 | `tests/scripts/test_validate_development.py` | 21.926919755 | 21.926919755 | 0.000000000 | 0.000000000 |
| 3 | `src/devtools/context/python/project_configuration/docs/overview.md` | 19.510075902 | 19.510075902 | 0.000000000 | 0.000000000 |
| 4 | `docs/development/validation.md` | 17.770001940 | 16.309154919 | 5.843388087 | 1.460847022 |
| 5 | `docs/backlog/overview.md` | 12.111096868 | 12.111096868 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| protected | 14 | 3.602494840 | 0.026365 | 14 | UNKNOWN / UNKNOWN / UNKNOWN |
| development | 22 | 3.163128180 | 0.041431 | 22 | UNKNOWN / UNKNOWN / UNKNOWN |
| validation | 49 | 2.374670820 | 0.092279 | 49 | UNKNOWN / UNKNOWN / UNKNOWN |
| entry | 24 | 3.077970372 | 0.045198 | 24 | UNKNOWN / UNKNOWN / UNKNOWN |
| point | 11 | 3.834296454 | 0.020716 | 11 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): validation, entry, development. No MIXED_INTENT or relevance failure is asserted before gold.

## C.validation.configuration — Arm C

Obligation: validation. Need: case-0011-context-utf8-ceiling/validation/configuration.

Exact need: What established tooling configuration constrains test, type and style validation?

Exact query:

```text
tooling configuration test type style validation
```

Native analyzer terms: `tooling, configuration, test, type, style, validation`.

Route: {'mechanism': 'CANONICAL_RESOURCE_BM25', 'reason': 'U1_CONTROLLED_LEXICAL_ONLY', 'exact_hint_routed': False, 'exact_hints_detected': []}. Execution count: 1. Positive resources: 220. Query seconds: 0.007657600.

| Rank | Resource | Score | Content | Filename (raw) | Filename (weighted) |
|---:|---|---:|---:|---:|---:|
| 1 | `docs/development/validation.md` | 13.397360031 | 11.936513009 | 5.843388087 | 1.460847022 |
| 2 | `src/devtools/context/python/project_configuration/docs/overview.md` | 12.372416907 | 12.372416907 | 0.000000000 | 0.000000000 |
| 3 | `docs/backlog/items/B-0047-protected-development-validation-profile.md` | 10.106256351 | 9.536392523 | 2.279455310 | 0.569863828 |
| 4 | `src/devtools/context/localization/roles/docs/overview.md` | 10.059850606 | 10.059850606 | 0.000000000 | 0.000000000 |
| 5 | `AGENTS.md` | 8.818416492 | 8.818416492 | 0.000000000 | 0.000000000 |

| Term | Content DF | IDF | Content fraction | Effective matching resources | REQUIRED / HELPFUL / UNNECESSARY yield |
|---|---:|---:|---:|---:|---|
| tooling | 11 | 3.834296454 | 0.020716 | 11 | UNKNOWN / UNKNOWN / UNKNOWN |
| configuration | 53 | 2.296961835 | 0.099812 | 53 | UNKNOWN / UNKNOWN / UNKNOWN |
| test | 71 | 2.006946040 | 0.133710 | 71 | UNKNOWN / UNKNOWN / UNKNOWN |
| type | 146 | 1.289618061 | 0.274953 | 146 | UNKNOWN / UNKNOWN / UNKNOWN |
| style | 9 | 4.025351691 | 0.016949 | 9 | UNKNOWN / UNKNOWN / UNKNOWN |
| validation | 49 | 2.374670820 | 0.092279 | 49 | UNKNOWN / UNKNOWN / UNKNOWN |

High-footprint terms (descriptive only): type, test, configuration. No MIXED_INTENT or relevance failure is asserted before gold.

## Exact hints remain lexical-only

- `ModelRequest`: [{'start': 61, 'end': 73, 'text': 'ModelRequest'}, {'start': 1007, 'end': 1019, 'text': 'ModelRequest'}]; NOT_ROUTED_IN_U1; literal query usage: ['A.task', 'C.ownership.assembly-owner', 'B.request', 'C.request.copy'].
- `ContextDisclosure`: [{'start': 170, 'end': 187, 'text': 'ContextDisclosure'}]; NOT_ROUTED_IN_U1; literal query usage: ['A.task', 'B.frame', 'C.frame.binding'].
- `DisclosurePlan`: [{'start': 195, 'end': 209, 'text': 'DisclosurePlan'}]; NOT_ROUTED_IN_U1; literal query usage: ['A.task', 'B.frame', 'C.frame.binding'].

## Cost scope

Shared content index construction: 0.433378300 seconds. Total 28 queries: 0.247917100 seconds. These are one-run descriptive observations, not latency benchmarks. Native per-query filename index construction is included; R1.5 projection/verification is separate.

STOP BEFORE GOLD. Next: fresh independent Stage C with only task/obligation/resource packet; then separate blind C.5 with needs and clean gold but no queries/results; then Stage D.
