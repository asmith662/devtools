# Case 0006 Stage B Attempt 1

**FAILED AFTER TREATMENT; NO OUTPUTS PERSISTED.** This is an immutable execution record, not an adjudication or effectiveness report.

## Identity

- Stage A commit: `e7aed4162672dd859a0a8a33a2b718dda8425495` (`Freeze prospective bounded witness-generation case`).
- Frozen source snapshot: `492229e0e0d4661cf5287c26d18c6488a80fe8ce`.
- RepositoryId: `d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8`.
- RepositorySnapshotId: `ba654221b65584aebdd98804369864162ac3f7da1bf8862abee06ce4d2127a55`.
- Corpus identity: `49c69d2db7c6616731d9c24519a48d47a13a2ee991d46aaaf33d1f5d55b212b9`.
- The execution date/runtime environment were not retained by the failed process.

## Preflight attempt

An initial invocation stopped before any production treatment operation because the harness compared the frozen source HEAD (`492229e0e0d4661cf5287c26d18c6488a80fe8ce`) with the Stage A commit (`e7aed4162672dd859a0a8a33a2b718dda8425495`). The preflight check was corrected before the treatment execution recorded below. This initial invocation is not a treatment execution.

## Treatment execution and failure

- Lexical acquisition calls: 1.
- Role routing calls: 1.
- Distinct frozen grounding requests resolved: 9.
- Witness generation calls: 1.
- Generator grounding freshness/cache checks: 14; extra native grounding resolver executions: 0. The 14 checks reused the exact nine captured results and are not additional grounding treatment executions.
- After generation returned, post-execution correspondence validation failed. The harness matched complementary recipe members by list position, but the production recipe constructor canonicalizes member ordering by member identity/key.
- The process exited before writing any Stage B artifact. No semantic output was retained or inspected.

## Lost data and absent outputs

The process exit lost the lexical result, routed view, grounding dispositions and referents, instantiated generation result, generated hypotheses and targets, support counts, and runtimes. No semantic outcome can be reconstructed without re-executing treatment.

No committed or persisted Attempt 1 output exists for `capture.pkl.gz`, `retrieval.json`, `routing.json`, `grounding.json`, `generation.json`, `stage_b_integrity.json`, or `stage_b.md`.

## Blindness and interpretation

No adjudication, effectiveness analysis, candidate-quality inspection, retained grounding-result inspection, or retained generation-result inspection occurred. Treatment was not modified. Confirmation outcomes were not accessed.
