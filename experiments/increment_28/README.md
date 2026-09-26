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
separately after that commit.
