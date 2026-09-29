# Codex advisory retrieval dogfood, Case 0001

## Scope and sequence

This is one development case at starting commit
`c7096d6865e7db443ca9caaf697f836780b019c5`. The task corrected an
incorrect current-state BM25 claim in `docs/architecture.md` while preserving
historical fixed-`K=5` experiment results. The pre-task snapshot contained 299
eligible resources. The full task prompt and separately authored short
InformationNeed, corpus, BM25 settings, seed origin, and Repository Intelligence
fact identities were frozen in `pre_retrieval.json` before retrieval.

The two production lexical retrieval calls used the same 299-resource corpus
and settings, with the complete positive-match work bound. Both were composed
with the same native direct structural result. The 283-address advisory
orientation was in neutral address order, not selected or ranked for handoff.
Codex retained ordinary search, open, edit, and validation access. Its trace,
post-run patch, and observations were frozen before adjudication.

The neutral 299-resource adjudication frame omitted retrieval and agent
provenance. A fresh, read-only external adjudicator saw that frame and an
isolated export of the committed pre-task files only. It received no ranks,
support, handoff, agent actions, patch, or post-run observations. Its retained
trace ends with `turn.completed`. The raw result affirmed that every unlisted
eligible resource was unnecessary. The baseline export used committed Git blob
text; 47 snapshot content identities differed because of checkout line endings,
without a change to addresses or task obligations.

The raw judgment was validated and frozen once, before the provenance join.
The freeze requires nonblank positive and unresolved rationales, allowed
required categories, valid alternative references, a 299-resource frame, and
exact identity coverage via `devtools.evaluation.compare_identity_coverage`.
The frozen adjudication was never changed after provenance was opened.

- Case ID: `38965facc88ded47e6fb7e95be19db6699772c3b6c020c08e8a63c476b83ddef`.
- Adjudication identity: `d5dfbb4cfa3d31a070312b3e867a5e3a8a37200ee2e921bfc476a22add461da1`.
- Frozen adjudication SHA-256: `774a60082b407f87191cfc43aed709df92761d64bb97d4aeecae17ec5dd641ca`.
- Raw blind judgment SHA-256: `003a901105a48a7aab5c11e1418c387e9819ced94aa0806652a8d13fccb8a453`.
- Completed blind trace SHA-256: `5914e3da7bd1dacf1682cb07188bdd44075a494c2f50da726112de939c1c820f`.
- Identity coverage: expected 299, observed 299, no duplicate, missing, or
  unexpected addresses; `is_exact=true`.

`analyze.py` checks the retained artifact identities and mechanically joins
the immutable judgments to the retrieval and agent observations. Run
`uv run python experiments/codex_dogfood/case_0001/analyze.py` to verify that
the recomputed result exactly matches `joined_analysis.json`.

## Blind judgments and lexical reach

Seven resources were required, five helpful only, 287 unnecessary, none
unresolved, and no acceptable-alternative groups. Each rank below is native
one-based BM25 rank. Every required resource had a positive lexical rank in
both arms and no structural support.

| Required resource | Obligation categories | Full prompt | Short need |
| --- | --- | ---: | ---: |
| `AGENTS.md` | understanding; validation | 1 | 5 |
| `docs/architecture.md` | understanding; implementation | 5 | 2 |
| `docs/backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md` | understanding | 21 | 18 |
| `docs/documentation_map.md` | understanding | 4 | 1 |
| `pyproject.toml` | configuration; validation | 33 | 132 |
| `src/devtools/context/retrieval/lexical/bm25.py` | API contract | 20 | 23 |
| `tests/context/retrieval/lexical/test_filename.py` | tests | 35 | 57 |

Helpful-only resources were
`docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md`,
`docs/roadmap.md`, `src/devtools/context/retrieval/docs/overview.md`,
`tests/context/retrieval/lexical/test_bm25.py`, and
`tests/context/retrieval/lexical/test_evaluation.py`.

| Retrieval arm | Complete inventory | Required present | Smallest lexical prefix covering all seven | Helpful in prefix | Unnecessary in prefix | Unnecessary in inventory |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Full prompt | 282 | 7 | 35 candidates | 5 | 23 | 270 |
| Short need | 263 | 7 | 132 candidates | 5 | 120 | 251 |

No required obligation had a retrieval miss. The complete inventory had 17
nonmatching resources in the full arm and 36 in the short arm; none was
required or helpful. The full prompt was substantially better for this case's
complete-obligation depth, especially for `pyproject.toml` (33 versus 132) and
the direct test (35 versus 57). The short need ranked the architecture and
documentation map more highly. Both surfaced the same seven required and five
helpful resources; this one case does not establish a general query rule.

## Structural evidence and Codex exploration

Native direct structural retrieval supported four resources in both arms:
`src/devtools/context/retrieval/lexical/__init__.py`, `analysis.py`,
`filename.py`, and `scoring.py` in that package. All four were already lexical
matches and were adjudicated unnecessary. Structure added corroborating
provenance but rescued no required resource and did not improve required
reach. This direct result does not evaluate the historical Graph-1 or Graph-2
traversal experiments.

The 33,699-byte advisory handoff listed the 283-address union. Codex still ran
five searches, recorded 17 direct `Get-Content` open events across nine
resources, and repeatedly inspected relevant spans. It directly opened five
of seven required resources: the architecture document, B-0006 item,
documentation map, BM25 implementation, and combined BM25 test. It did not
directly open `AGENTS.md` or `pyproject.toml`; the trace includes a targeted
`pyproject.toml` search, and direct-open accounting does not measure all search
reads or preprovided instructions. It opened two helpful-only resources
(`test_bm25.py` and the retrieval package overview) and two adjudicated
unnecessary resources (the taxonomy and B-0001 epic).

Codex modified only the required `docs/architecture.md`. It ran focused tests
for required `test_filename.py` and helpful-only `test_bm25.py`, plus Ruff,
mypy, and Git diff checks, all recorded successful. `AGENTS.md` and
`pyproject.toml` carried blind validation obligations; neither was a direct
`Get-Content` open. The recorded task and validation outcomes were successful.
File bytes and tokens read were not reliably measured, and no unaided control
run was performed. Direct opens are observations, not relevance labels.

At case-record finalization, 20 focused lexical/Evaluation tests, repository
Ruff, and mypy passed. The full deterministic pytest run reported 1,666
passed, two skipped, and seven failures: repository-discovery benchmark tests
traversed the local `.venv` and exceeded their 10,000-resource bound. The
incomplete run consequently missed the configured 100% coverage gate. This is
a checkout-environment validation limit, separate from the completed blind
adjudication and original Codex task validation.

## Diagnosis and next step

**Retrieval failure:** none in this 299-resource frame. Both complete lexical
inventories contained every adjudicated required resource.

**Selection and handoff pressure:** real. A full-prompt lexical prefix needed
35 candidates to cover seven required obligations and included 23 unnecessary
resources; the short-need prefix needed 132 and included 120 unnecessary.
The neutral union handoff exposed 283 addresses. A small, fixed handoff would
need an evidence-based assessment and sufficiency rule, which this case alone
does not authorize.

**Context pressure:** present as a plausible within-resource reading cost.
The agent made repeated partial reads of the architecture, BM25 implementation,
and tests after their addresses were available. The trace does not quantify
bytes, tokens, or a counterfactual disclosure budget, so it does not establish
Context as the immediate bottleneck. Candidate ordering and handoff volume are
the clearest measured pressure in this case.

The next step is a prospectively frozen Case 0002 on a different bounded real
task, with the same two query arms, blind obligation adjudication, and explicit
exploration observations. Compare obligation coverage and candidate depth
across cases before choosing a budgeted Selection rule. Keep confirmation
sealed. This case does not justify tuning BM25, graph traversal, learned
ranking, a Context change, or a production Selector.

## Record ownership

The neutral frame and immutable adjudication live one level above this
directory. This directory retains the blind prompt, schema, raw judgment,
completed blind trace, pre-retrieval freeze, native retrieval inventories,
pre-agent accounting, exact handoff, Codex trace and patch, post-run
observation, mechanical join script, and joined result. These are the compact
research record. Local scripts used to export a checkout or initiate one
ephemeral adjudicator, pickle caches, the isolated checkout and zip, and
duplicate handoff copies were operational scaffolding, not committed research
artifacts. No production Evaluation behavior or package API changed.
