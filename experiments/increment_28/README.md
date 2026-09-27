# Increment 28: task-relative import-use evidence

This development-only experiment enriches the **fixed** Increment-27 direct
module-import candidate population. It adds no candidates, changes no top-five
admission, and does not alter Repository Intelligence or production retrieval.

## Frozen proposition and population

For one outgoing support, a qualified AST read of its imported local binding
inside that lexical seed's **saved winning query-scored window** is evidence
that this import path is used in a task-matching source region. The source is
the exact historical parent snapshot. The relation must already be a uniquely
resolved, direct, directed module import in the Increment-27 artifact. The
primitive classification belongs to each support; candidate summaries retain
every support. Incoming-only candidates have no analogous seed-uses-import
proposition and remain separate.

The only population is the 24 frozen Increment-27 development InformationNeeds:
109 structural case/resource pairs, including 99 outgoing pairs and 10
incoming-only pairs. The 14 Increment-27 held-out cases and suspended
Increment-26 confirmation were neither materialized nor evaluated. All 120
canonical first-five seeds have a saved positive winning window. The 499
retained outgoing support paths in this population use `from package import
name` (495) or `from package import name as alias` (4). The code also defines
the local binding for `import package` and `import package as alias`; those
forms contribute no retained outgoing support in this frozen population.

## Bounded source semantics

`SUPPORTED` requires an AST `Name` read of the imported local binding, wholly
within the saved half-open character window, outside the import statement.
For unaliased dotted `import package.submodule`, the full dotted target prefix
must appear as an attribute chain; a read of `package` alone does not qualify
for `package.submodule`. The analysis checks the direct import alias against
the retained declaration ordinal and UTF-8 source span. It verifies the saved
window's exact text, hash, ordinal, source bounds, and identity against the
parent source before inspecting AST reads. Python AST byte columns are mapped
back to Unicode character offsets in that exact source.

Unshadowed function, async-function, and lambda reads may qualify. An
additional module binding of the name (including pattern capture), wildcard
import, named-expression assignment, `global`/`nonlocal` declaration, dynamic
`exec`/`globals`/`locals` call, or competing function
binding prevents a definite negative conclusion. Relevant reads in class,
comprehension, or annotation contexts, or across a window boundary, remain
`INDETERMINATE`. A source-grounded read that is valid under these rules yields
`SUPPORTED`; with no valid read and unresolved relevant syntax, the state is
`INDETERMINATE`. `NO_QUALIFYING_OCCURRENCE` is reserved for covered syntax
with no qualifying in-window read. This is an experiment-local conservative
binding check, not a general Python reference resolver. Occurrence count is
retained for audit and is not a relevance score.

## Pre-outcome checkpoint

The freeze is `import_use_freeze.json`; the source-grounded support and
candidate artifact is `import_use_evidence.json`. Both have deterministic
content identities. The evidence binds the existing candidate and saved
window identities and contains no usefulness outcomes or changed paths.

| Surface | Pairs | Supports | SUPPORTED supports | NO_QUALIFYING_OCCURRENCE supports | INDETERMINATE supports | Pairs with support | Cases with support |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All outgoing | 99 | 499 | 193 | 251 | 55 | 58 | 23 |
| Outgoing absent from every saved positive lexical universe | 52 | 165 | 45 | 108 | 12 | 30 | 17 |

Among all outgoing pairs, 28 have only `NO_QUALIFYING_OCCURRENCE` supports
and 31 have at least one `INDETERMINATE` support. On the hard lexical-escape
surface, those counts are 19 and 9. These categories may overlap with the
supported-pair category when a candidate has multiple supports. The 10
incoming-only pairs are preserved without import-use classification.

The pre-outcome artifact was validated and committed before any usefulness
join. The post-checkpoint analysis of existing frozen judgments is recorded
separately after that commit. The pre-outcome checkpoint is
`8809c478d0d0509e4eb921740eed2d4f78a2216e`.

## Post-checkpoint development join

`import_use_development_results.json` mechanically joins exact frozen
Increment-27 usefulness outcomes after the evidence checkpoint. It creates no
judgments and keeps `UNJUDGED` distinct. The 99 outgoing pairs contain 31
`USEFUL`, 49 `NOT_USEFUL`, and 19 `UNJUDGED` outcomes.

| Exclusive evidence category | Pairs | USEFUL | NOT_USEFUL | UNJUDGED | Useful among binary judgments |
| --- | ---: | ---: | ---: | ---: | ---: |
| At least one SUPPORTED path | 58 | 22 | 25 | 11 | 22/47 (46.8%) |
| Only NO_QUALIFYING_OCCURRENCE paths | 28 | 3 | 17 | 8 | 3/20 (15.0%) |
| No support, at least one INDETERMINATE path | 13 | 6 | 7 | 0 | 6/13 (46.2%) |

Among all 41 pairs without a supported path, 9 of 33 binary-judged pairs are
useful (27.3%). The 22 supported useful pairs span 15 cases; removing any one
case leaves the supported-versus-without-supported binary-judgment fraction
positive by roughly 16 to 25 percentage points. These are descriptive
selected-development comparisons, not validated probabilities. A candidate
may have a supported and an indeterminate support at once: 31 pairs have at
least one indeterminate path, including pairs assigned the exclusive
SUPPORTED category. The high usefulness among these pairs warns against
treating unknown binding evidence as a negative.

The 52 outgoing candidates absent from every saved positive lexical universe
contain 10 `USEFUL`, 30 `NOT_USEFUL`, and 12 `UNJUDGED` outcomes. Qualified use
retains eight of the ten known useful hard escapes across eight cases:

| Hard-escape category | Pairs | USEFUL | NOT_USEFUL | UNJUDGED |
| --- | ---: | ---: | ---: | ---: |
| SUPPORTED | 30 | 8 | 16 | 6 |
| NO_QUALIFYING_OCCURRENCE | 19 | 1 | 12 | 6 |
| INDETERMINATE | 3 | 1 | 2 | 0 |

The broad contrast does **not** establish additional discrimination beyond
existing coarse signals. In particular, for candidates with exactly one
structural support, supported paths have 2 USEFUL and 8 NOT_USEFUL outcomes,
while candidates without a supported path have 4 USEFUL and 10 NOT_USEFUL.
Across the 11 exact strata that contain both groups when matched on support
count, distinct seed count, and best seed rank, there are only 55 pairs: the
supported group has 8 USEFUL / 13 NOT_USEFUL and the other group has 7 USEFUL /
16 NOT_USEFUL. Most strata are too small for a stable contrast. Larger support
counts also make it more likely that at least one support qualifies. No
threshold, weighted score, or classifier was selected from these outcomes.

The result supports further bounded diagnostic work on whether import-use
evidence adds information conditional on the coarse structural features. It
does not authorize a production reference resolver, fusion rule, ranking
change, learned ranker, or held-out confirmation.
