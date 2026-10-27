# Native host obligation Context

This opt-in application composition connects the existing Localization kernel to
the native coding worker. It does not infer task obligations or implement the
broader A+C proposal. The trusted host selects the frame and its criterion-specific
decisions; the worker model cannot supply, revise or approve them.

Pass an `ObligationFrame` as `obligation_frame=` to `run_coding_task` or
`run_local_task`, or use:

```text
uv run python scripts/qwen/coding_worker.py --task-definition .local/task.json --obligation-frame .local/obligations.json --observed-edits --report-directory .local/new-run
```

The option requires an on-demand task. It is not accepted with preflight-only or
closeout, and does not alter WorkCycle assignment/delegation or publication rules.
Existing unframed tasks retain their format, digest, result fields and behavior.

## Trusted frame

The host authors JSON with exactly these fields. Placeholder hashes below must be
replaced with the actual task and native content identities:

```json
{
  "schema": "qwen-obligation-frame-v1",
  "task_definition_sha256": "<CodingTask.definition_sha256>",
  "caller": "trusted task author/reviewer",
  "obligations": [
    {
      "key": "implementation-contract",
      "predicate": "Inspect the selected implementation contract before editing",
      "query": "value implementation contract",
      "requirement": "mandatory",
      "criterion": {
        "name": "reviewed-exact-block",
        "statement": "The host-reviewed current block supplies this information"
      },
      "alternatives": [
        {
          "key": "reviewed-owner",
          "members": [
            {
              "path": "src/devtools/example.py",
              "version": "<native ContentIdentity.from_text(exact_baseline_text)>",
              "start": 0,
              "end": 40,
              "decision": "supported",
              "claim": "This block supplies the named implementation contract",
              "reason": "Explicit trusted caller review of this exact source"
            }
          ]
        }
      ]
    }
  ]
}
```

`version` is the existing RI decoded-text `ContentIdentity`, not a raw file SHA.
Coordinates are nonempty half-open Unicode character ranges. Every member must
name an existing task-authorized source/test/read path; the frame grants no new
read or edit access. The task digest binds the full objective, baseline, source
scope, fixed checks and budgets. The frame has its own normalized SHA-256 and is
archived separately as `obligation-frame.json`.

Each obligation uses an explicit host query, `mandatory` or `helpful` priority,
and the existing named `SatisfactionCriterion`. Members of an alternative are
ALL-of; distinct alternatives are ANY-of. One member per resource and distinct
resource sets per alternative match the existing native association/witness
contract. An obligation with no declared alternative remains unresolved; no empty
repository witness or non-applicability proof is invented.

Member decisions use the existing `supported`, `unresolved`, `abstained` and
`contradicted` vocabulary. They are trusted caller judgments, not facts inferred
from retrieval or proof that arbitrary prose is true. Support/contradiction is
effective only when the specified current source range has actually been disclosed
and remains in the active request. The host must review the criterion/claim link;
the kernel authenticates lineage, not semantic truth. Unjudged members cannot
become supported by reading them. A contradicted conjunct blocks its hypothesis;
it does not eliminate a different explicitly accepted alternative.

V1 is bounded to an 8,192-byte frame, eight obligations, four alternatives per
obligation, eight distinct resources per alternative and sixteen total members.
It refuses decoded duplicate JSON keys and unsupported fields. Conditional
applicability, task-only execution/review evidence, revisions, omitted-clause
rosters and model-authored frames are unsupported. Those broader decisions remain
with the existing proposal and unapproved A+C scope.

## Actual acquisition and admission

The composition acquires independent native full-task and obligation BM25 lanes
over the existing authorized file index. The complete objective/global lane and
all in-bound corpus matches remain available; rank, filename, score and missing
matches never decide satisfaction. Existing source/symbol/window search, read,
map and navigation Tools remain unchanged. Their actual source reads still use
Context Planning/materialization and ordinary ToolRunner admission.

Exact resource grounding, native candidate association, caller member resolution,
explicit complete-hypothesis promotion and `assess_localization_readiness` are
reused. Candidate reasons retain native supports; semantic support comes from the
host's declared decision, conditioned on exact source disclosure. The assessment
retains repository/snapshot, source versions, criterion/caller, member decisions,
actual Tool call IDs/ranges/text hashes, lexical lanes and a content hash of the
application assessment. Native support objects remain in memory; these bounded
application projections are not a new framework persistence schema.

Before every native request, assessment uses the selected messages, before faithful
source-block rendering and actual tokenizer counting. Removed/compacted text
does not count as available Context. Active text is checked against retained native
observations and current source. The bounded status enters the existing initial
host Prompt message. Existing byte/token/action/call/time limits still apply; no
new model Tool, action budget or hidden source-disclosure channel is added.

Before every edit proposal, source correspondence and readiness are rechecked.
Missing mandatory information produces correlated `CONTEXT_NOT_READY` proposal
feedback with the unresolved criteria and original remaining budgets. The refused
proposal consumes the existing proposal allowance; subsequent authorized reads
may obtain the missing information within the original limits. Exhaustion is
never readiness. Helpful unresolved obligations remain visible without blocking.
Ordinary source/patch admission runs independently after READY.

Witnesses freeze exact content versions. An admitted edit can invalidate an
affected witness; rereading changed code does not silently approve it against an
old criterion decision. Unchanged required resources are reauthenticated across
admitted snapshot changes and may continue supporting repair. Fresh host decisions
for changed required content need separately authorized work; V1 is not a frame
revision/restart protocol.

Readiness is explicitly **before a source-changing action**. A later check-only
turn can report an old source witness as stale while retaining the earlier READY
`edit_context_assessment` that admitted the edit. Candidate validation, installed
currentness, terminal worker completion, Checkout release, semantic review and
publication remain separate. READY does not prove task correctness or exhaustive
coverage of the original objective.

## Failure and evidence boundaries

Per-turn and terminal application records retain the assessment and exact frame
hash. Passing/failing candidate checks, unknown usage, known Tool/Git effects,
source restoration and the terminal-outcome repair remain unchanged. Cancellation
or failure never retries a possibly completed effect. A storage failure can still
leave incomplete evidence; these archives are neither exactly-once execution nor
verified resumable task state. Observation Option B, normalized Evidence ingestion,
automatic persistence and application decomposition are not implemented here.
