# Codex advisory retrieval dogfood, Case 0002

## Task and prospective boundary

Starting commit: `66704dcc94e46e8fb88d3dc52cbea591e0e399a1` on clean `main`.
The active roadmap explicitly said cases without qualified structural seeds
needed a lexical-only capture path before they could use the dogfood protocol.
Case 0002 therefore asked Codex to implement that bounded path in
`experiments/codex_dogfood/capture.py`, add focused tests, and update the
protocol documentation. This was a real experiment-owned Python implementation
task, materially different from Case 0001's documentation correction. The
roadmap contained no comparably bounded, selected production Python task that
could be implemented without opening a deferred architecture decision. The
task did not authorize a production retrieval, Evaluation, or Context change.

The frozen implementation boundary kept seeded capture, production BM25,
direct structural retrieval, snapshot-bound composition, Evaluation, Context,
and Codex integration unchanged. The full task prompt named the production
`structural.py` and `composition.py` contracts because the new zero-seed path
must preserve their nonempty-seed and snapshot rules. Those two paths were
declared as Case 0002's structural seeds before retrieval; no seed was chosen
from retrieval output. The separately written short InformationNeed and all
intended validation obligations are in `pre_retrieval.json`.

## Scientific sequence and immutable boundary

The pre-retrieval freeze contained the exact task prompt, short need, starting
commit, 302-resource observed snapshot and eligible corpus, BM25 settings
(`k1=1.2`, `b=0.75`), complete 302-document lexical work bound, two qualified
seed origins, already-derived production RI inputs, and validation obligations.
Case ID: `cde8f37ad2e0b6f05a9d9713e07f62fd8a52931c1ba0ef5686129f4aeba56ddb`.
The pre-retrieval JSON SHA-256 is
`d9fa624f8b78f38e46192f2ab1d83ec6cfa9e9b02aaeeff6f640f752395d3d1c`.
Both lexical arms used the same frozen index and settings. Direct structural
retrieval used the declared seeds; each arm was composed against the snapshot.
The advisory orientation listed all 299 surfaced addresses in neutral address
order, without asserting relevance or sufficiency.

The edit-capable Codex CLI host was interrupted while its first ephemeral
session was still progressing. That trace contains one truncated final JSONL
line and no `turn.completed`; its existing edits were preserved. Resume of its
ephemeral thread was unavailable, so a fresh continuation session received the
same advisory handoff plus an explicit continuation note. It completed the
implementation and ends in `turn.completed`. The post-run observation freezes
both traces, the exact continuation handoff, commands, searches, direct opens,
modified paths, focused validation, patch, and reported continuation token
usage. First-session token usage is unavailable. The host interruption affects
telemetry completeness, not the pre-task retrieval capture or blind boundary.

The neutral adjudication frame contains only the exact task, starting commit,
snapshot ID, and all 302 eligible addresses and content identities. It excludes
retrieval ranks and supports, the orientation, both agent traces, patch, and
post-task state. An isolated export reproduced every pre-task snapshot content
identity. A fresh ephemeral read-only adjudicator saw only that export and the
neutral frame. Its trace contains no file change and ends in `turn.completed`.
The raw judgment affirmed every unlisted eligible resource unnecessary. It was
validated and frozen **before** any provenance join, with the production
`compare_identity_coverage` kernel used solely for generic identity accounting.
The judgment has never been revised after unblinding.

- Neutral frame SHA-256: `f8a8dc34d1fda959aec606015f56bf028d67139963ace3ad9e25d6ee7fc8c829`.
- Blind raw judgment SHA-256: `7b31debd8d583ae20b3d90ce91b2446a3900cec1b162fa8ad0facb69bf45371f`.
- Completed blind trace SHA-256: `5927886b0ac3420251e0436a36e5bad1776f1576d31a70b89c474cd30245044e`.
- Adjudication identity: `9cfc3a6d43c8e579a1075c933782c80a6db9f189da237cb5ed82badffec00443`.
- Frozen adjudication SHA-256: `427c2936db23d1a04538c74420b565e50c7e8e480abfd1b7899a07231b2da9e2`.
- Identity coverage: expected 302, observed 302, no duplicates, missing or
  unexpected addresses; `is_exact=true`.

The full native input and capture objects were retained as deterministic gzip
archives (`inputs.pkl.gz` and `capture.pkl.gz`). The compact JSON inventory
also retains native lexical scores, content and filename contributions, ranks,
and structural seeds, directions, families, and fact identities. The archives
are historical Python pickles: inspect their recorded provenance and load only
in a trusted matching checkout. `analyze.py` verifies artifact hashes and
recomputes `joined_analysis.json` from the immutable labels and retained
provenance:

- Decompressed `inputs.pkl` SHA-256: `3609a652be5e9c2a4574c3cb819832fcddb362fa5105b3a110b8dbb9c3acc240`.
- Decompressed `capture.pkl` SHA-256: `099f46ee2af6dba47b47951bcdd797c7831a33bb364adabad257ceda2b76de67`.

```text
uv run python experiments/codex_dogfood/case_0002/analyze.py
```

## Blind obligations and exact lexical reach

The independent judgment marked **10 required**, **5 helpful only**, **287
unnecessary**, **0 unresolved**, and **0 alternative groups**. Required
categories and native one-based BM25 ranks follow. No required resource had
structural support.

| Required resource | Obligation categories | Full prompt | Short need |
| --- | --- | ---: | ---: |
| `AGENTS.md` | understanding; validation | 5 | 10 |
| `docs/roadmap.md` | understanding; implementation | 2 | 2 |
| `experiments/codex_dogfood/capture.py` | implementation | 3 | 1 |
| `pyproject.toml` | configuration; validation | 43 | 71 |
| `src/devtools/context/retrieval/composition.py` | API contract | 13 | 49 |
| `src/devtools/context/retrieval/lexical/bm25.py` | API contract | 33 | 87 |
| `src/devtools/context/retrieval/structural.py` | API contract | 37 | 20 |
| `tests/context/retrieval/test_composition.py` | tests | 19 | 55 |
| `tests/context/retrieval/test_structural.py` | tests | 38 | 59 |
| `tests/experiments/test_codex_dogfood_capture.py` | tests | 9 | 6 |

Helpful-only resources were `docs/architecture.md`, ADR-0003, the architecture
taxonomy, `docs/documentation_map.md`, and the retrieval package overview.
The frozen artifact retains each exact path, content identity, and rationale.

| Lexical depth | Full prompt | Short need |
| ---: | ---: | ---: |
| 5 | 3/10 | 2/10 |
| 10 | 4/10 | 4/10 |
| 20 | 6/10 | 5/10 |
| 30 | 6/10 | 5/10 |
| 50 | 10/10 | 6/10 |
| 100 | 10/10 | 10/10 |
| Complete inventory | 10/10 | 10/10 |

The complete full-prompt inventory held 299 positive lexical matches; the
short-need inventory held 285. Neither missed a required resource. The
smallest lexical prefix with all ten required resources was **43** for the
full prompt (10 required, five helpful, 28 unnecessary) and **87** for the
short need (10 required, five helpful, 72 unnecessary). Across each complete
inventory, 284 and 270 resources respectively were unnecessary. The short
formulation helped the capture implementation (rank 1 versus 3), its test
(6 versus 9), and the structural contract (20 versus 37); the full prompt
helped the tail obligations, especially the BM25 API (33 versus 87),
composition API (13 versus 49), and two fixture tests (19/38 versus 55/59).

## Structural evidence and actual exploration

Direct structural retrieval produced four candidates in each arm:
`src/devtools/context/python/imports/relations.py`,
`src/devtools/context/python/modules/membership.py`,
`src/devtools/context/python/references/analysis.py`, and
`src/devtools/context/retrieval/__init__.py`. The supports used Imports and
immediate package membership; there was no Reference/direct Call support for
a required resource. All four candidates were already lexical matches and
were adjudicated unnecessary. **No required resource had Import, Reference/
Call, or membership support; structure rescued no lexical miss and added no
required reach.** This is the direct production projection, not Graph-1 or
Graph-2 traversal. The seeds were themselves required API resources, while
direct projection emits their neighbors rather than the seeds, which limits
what this case says about structural retrieval on other tasks.

The two Codex sessions recorded 36 completed commands and three searches
despite the advisory inventory. `Get-Content` commands yielded 30 direct-open
events across 16 distinct paths. Codex directly opened nine of ten required
resources; `pyproject.toml` was not a direct open, although its configured
checks were run. It opened three helpful-only resources (taxonomy,
documentation map, retrieval overview), three unnecessary resources (the
B-0008 item, repository resource model, and snapshot model), and the Case 0001
README outside this case's eligible frame. Search results and incidental reads
are not counted as direct opens. No reliable file-byte or read-token totals
were available.

The patch modified three required resources (`capture.py`, its test, and the
roadmap) plus helpful-only `docs/documentation_map.md`; modification did not
change their blind roles. The explicit focused pytest target was the required
capture test. The two required fixture test files were directly opened but not
separate pytest targets. The final Codex continuation reported four focused
tests passing, plus Ruff, mypy, and diff checks. The report preserves the
earlier failed or interrupted checks rather than treating every command as a
success. No retrieval miss required agent recovery.

At case-record finalization, 15 focused capture/composition/structural tests,
repository Ruff, mypy (517 source files), the reproducible analysis join, and
Git diff checks passed. The full deterministic pytest run reported **1,667
passed, two skipped, seven failed**. As in Case 0001, seven real-repository
benchmark tests traversed the local `.venv` and exceeded their
10,000-resource discovery bound; the incomplete suite reached 99.06% against
its configured 100% coverage gate. This known checkout-environment issue was
not repaired in the unrelated capture task.

## Diagnosis, limits, and next step

**Retrieval failure:** none in the prospectively eligible 302-resource frame.
Both complete lexical inventories contained every required obligation.

**Selection and handoff pressure:** observed. Complete coverage needed 43 or
87 lexical candidates, including 28 or 72 unnecessary resources, while the
neutral handoff exposed 299 addresses. Candidate generation succeeded, but a
small economical handoff would require a separate evidence-based assessment
and sufficiency decision. This case does not authorize a production Selector.

**Context pressure:** unquantified. Repeated direct opens show further reading
after addresses were surfaced, but the traces do not measure unnecessary
within-resource spans, bytes, or model input tokens. The host interruption
also leaves first-session token usage unknown. Context is therefore a possible
cost, not the demonstrated immediate bottleneck.

Together, Cases 0001 and 0002 show complete required-resource reach and deeper
tail obligations in both full-prompt and short-need lexical arms on two
different tasks. Full prompts reached complete coverage sooner in both cases
(35 versus 132; 43 versus 87), while some individual resources ranked better
under short needs. Neither case found a required structural rescue. Two tasks
in one repository, one of them about the dogfood machinery itself and one with
an interrupted agent host, cannot establish general retrieval recall,
structural ineffectiveness, the value of the advisory handoff versus unaided
Codex, a budgeted Selection rule, or a Context policy.

Next, prospectively select a different bounded **production Python** task
whose natural consumer-to-dependency relationship gives existing RI a fair
chance to surface required resources. Freeze the same inputs and blind labels
as Case 0003; if no legitimate task is ready, pause rather than invent one.
Compare exact obligation ranks, curves, and exploration across the three
cases before considering any Selection implementation. Confirmation stays
sealed.

## Record ownership

This directory retains the pre-retrieval freeze, native input/capture archives,
complete compact inventories, advisory handoffs, both Codex traces, exact
patch, post-run observation, blind prompt/schema/raw result/completed trace,
mechanical analyzer, and joined result. The neutral frame and immutable
adjudication are in the parent experiment directory. Temporary scripts used
to run the case, export the isolated snapshot, and freeze the adjudication are
one-off scaffolding and are removed from the worktree after the evidence is
captured. Production Evaluation remains only an identity-coverage dependency;
no adjudication semantics were added to it.
