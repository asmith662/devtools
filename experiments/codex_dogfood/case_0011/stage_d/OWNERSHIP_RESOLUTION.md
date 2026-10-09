# Case 0011 Stage D ownership resolution

Decision: **MERGE_BOUNDED_COMPONENTS**.

## Incident and exclusive ownership

Two interactive Codex sessions wrote incompatible untracked Stage D components
in one checkout. A scoped Ruff inspection exposed modules the authorized turn
had not created; both entry points expected different functions from the same
reporting module. The turn stopped without discarding either implementation.
The first resume found the older session's unfinished mutating Ruff fix/format
call and stopped again. The user subsequently terminated that competing session.
The final resume verified its process was absent and only the surviving
interactive session remained. Daemon/host/wrapper processes are not independent
repository writers. No competing files changed between inspection and backup.

Before consolidation, all 11 untracked partial files were inventoried with path,
byte size, SHA-256 and UTC modification time and backed up byte-for-byte under
the ignored operational directory `.local/case_0011_stage_d_parallel_conflict/`.
Every copy and original matched the manifest before replacement or deletion.
That backup and the result handoff are operational only, excluded from scientific
inputs, artifacts and the commit.

## Preserved graphs and exact file sets

Implementation 1, from the competing session:

```text
stage_d/analyze.py -> inputs.py + metrics.py + reporting.py
test_analysis.py -> analyze.py + inputs.py + metrics.py
reporting vocabulary expected: summary / trace / inspect
```

Original set: `stage_d/analyze.py`, `inputs.py`, `metrics.py`, `test_analysis.py`,
`pytest.ini`, `.gitattributes`, and a reporting module later overwritten by the
other writer. The backup preserves the actual shared-file state at reconciliation,
not a claimed reconstruction of lost bytes.

Implementation 2, from the interrupted authorized turn:

```text
case_0011/analyze.py -> stage_d/diagnostics.py + reporting.py
stage_d/replay.py -> case_0011/analyze.py + retained R1.5 adapters
reporting vocabulary: enrich / report / review
```

Original set: case-level `analyze.py` plus `stage_d/__init__.py`, `diagnostics.py`,
`replay.py`, and the shared `reporting.py`.

## Comparison and criteria

| Concern | Implementation 1 | Implementation 2 | Resolution |
| --- | --- | --- | --- |
| Ownership/entry point | Separate package loader, metrics and CLI | Case-level module mixes all three | One Stage D package with responsibility leaves |
| Frozen loading | Canonical identity coverage; historical protocol binding | Broader committed-directory verification and native/content checks | Archive lineage/current checks plus canonical identity coverage |
| Scientific join | Reviewed builders, frame/cell/projection checks | Exact statements, contributions and tie order | Stronger checks from both |
| Alternatives | Correct A/B complementary sets and identity tie | Correct A/B and all six combinations | Implementation 2 accounting |
| Responsibility | Direct needs; some B comparisons follow C ownership | Every gold owning B obligation and validated collective member | Gold ownership; show each lane separately |
| Metric coverage | Missing same-18-unit B burden | Both matched subsets, unit oracle and obligation surfaces | Implementation 2 matched subsets |
| Failure attribution | Conservative positive-hit/overtaker partition | Concrete U05 query and U27 representation evidence | Bounded explanations; separate earliest stage and contributors |
| R1.5 | Integrated captured-row replay | Duplicate loader/replay entry | One loader performs retained diagnostic reconstruction |
| Reporting/trace | Expected API conflicts with current shared module | Complete practical input/need/unit/query review | Only enrich / report / review |
| Serialization | Canonical JSON/digests/overwrite refusal | Same, separate frozen trace links | One artifact pipeline |
| Tests | Independent prefix/byte tests; API mismatch | No completed suite | Adapt independent tests and add tamper/binding checks |
| Validation | Unfinished Ruff fix/format/mypy request | Preliminary calculations; Ruff failed | Fresh consolidated validation; no inherited pass claim |

Neither size nor recency was an adoption criterion. Scientific correctness,
complete Stage D coverage, deterministic replay, canonical substrates/R1.5 reuse,
clear module ownership, minimal duplication, coherent API, testability, nearby
case consistency and smallest safe rework favor this bounded merge.

## Final ownership and supersession

```text
analyze.py -> inputs.load -> reviewed builders + captured R1.5 reconstruction
           -> metrics.evaluate -> diagnostics.diagnose
           -> reporting.enrich / report / review
test_analysis.py -> the same canonical package pipeline
```

`inputs.py` owns authentication and one loader; `metrics.py` owns set/prefix/alternative
calculations; `diagnostics.py` owns captured diagnostic interpretation;
`reporting.py` owns the single reporting API; `analyze.py` owns publication/replay.
This is non-installable, Case-0011-local experiment code depending on supported
devtools substrates. No framework abstraction is promoted.

Retained/reworked from implementation 1: package structure, canonical
identity-coverage use, focused-test structure/configuration and byte-preservation
attributes. Retained/reworked from implementation 2: input/lineage checks,
metrics, same-unit comparisons, oracle, diagnostics and practical review.
Case-level `analyze.py` and duplicate `stage_d/replay.py` were removed only after
verified backup. Implementation 1's metric/CLI/test modules were superseded in
place. No summary/trace/inspect compatibility API or parallel loader/engine/entry
point/test suite remains.

Frozen Stage A/B/C/C.5 artifacts, reviewed gold, reconciliations, query captures
and sealed traces were untouched. Both historical C5_PROTOCOL.md versions are
authenticated at their respective commits. This changes only new Stage D code
and reporting, not scientific inputs or production semantics.
