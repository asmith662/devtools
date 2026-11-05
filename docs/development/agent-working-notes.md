# Source-grounded task-local working notes

`devtools.context.working` retains a bounded working state for one exact task,
actor/role and episode. This is immediate task state selected into Context, not
the taxonomy's future cross-task Memory, a repository fact database, or RI
DerivedKnowledge. The first consumer is the existing independent `NativeReviewer`.
Model identity is configuration; no model-specific branch is involved.

The [P3 follow-up](../research/llm-harness-p3-followup.md) supplied the pressure:
six delivered conclusions but only two factually valid reviews. This increment
demonstrates deterministic provenance and state boundaries, **not improved model
accuracy**. No new live inference accompanies implementation.

## Ownership and supported state

- Context owns `NoteScope`, `WorkingNotes`, immutable notes and exact source
  anchors, selecting whole records into a bounded view. Existing task/episode
  identities and canonical resource/content/snapshot wrappers are reused.
- Repository observation, source units and `SourceRangeDisclosureOption` remain
  source owners. `SourceBinding` borrows those resources with receipt references
  and already-disclosed spans. Its union/gap view derives from those spans; it
  does not acquire source or maintain an independent read ledger.
- The reviewer adapter seeds only the independently authenticated subject and
  completed read disclosures. It writes checkpoints through existing native
  `Capture` records. No new store, Runtime lifecycle or Conversation schema exists.
- Existing coding compaction remains separately bounded, fallible generated
  summarization. It is not used to authenticate these notes and receives no new
  auxiliary inference authority.

Notes distinguish source observations, hypotheses, source/API relationships,
questions and conclusions. Each has a host sequence number, claim, expected
contract, supporting exact source intervals, predecessor contradictions and
supersessions. The notebook scope binds all records to task, role and episode.
Original records remain after correction. State is derived as provisional,
contested, contradicted by a fresh host-attested counterclaim, superseded, stale,
or host-verified.

`record()` always admits a **provisional** claim, including one labeled `source`.
Matching citations or quotations do not verify the interpretation. `observe()`
can verify only an exact literal quotation from disclosed source. `attest()` is
an explicit trusted-host operation identifying a checking receipt; it is not
available through model note input and is not a framework proof of arbitrary
program semantics. A verified counterclaim is meaningful only within that stated
host check. Verification never supplies execution authority or backlog acceptance.

Source anchors retain canonical address, content identity, optional snapshot,
reference and half-open Unicode interval with its exact quote. Freshness rechecks
all those bindings and the allowed disclosure. Changed/missing source becomes
stale; it cannot admit new support or reopen as current evidence. A new snapshot
also invalidates a snapshot-bound anchor even if its text is unchanged. Questions
may explicitly lack source evidence; that absence is not proof of a defect.

## Independent reviewer integration

Create a **new** acceptance subject through the existing owner:

```python
packet = await cycle.native.reviewer.prepare(item, reviewer=config, working_notes=True)
```

The exact `review-working-notes-v1` marker and 8,192-byte projection bound enter
the frozen subject before its existing grant. Standing authorization can authorize
that prepared subject normally; the marker neither grants permission nor adds
Tools. Historical subjects without it keep their behavior. It is unavailable to
diagnostic review and does not retrofit consumed subjects/continuations. There is
no policy expansion or automatic redispatch.

The reviewer keeps its existing independent system prompt, read-only source
scope, finite calls/reads and strict `submit_review_proposal` schema. The additional
bounded Context procedure is:

**Claim → expected contract → observed evidence → contradiction/uncertainty check
→ supported finding.**

The model may send a closed `WORKING_NOTES\n` JSON companion in assistant content
alongside an existing `read_source` call. It can correct a provisional predecessor
or state missing evidence. An eight-note batch is validated completely before
adoption; extra fields such as `verification`, invented references, inaccurate
quotes or unread ranges fail. No separate model call is required per note. A
notes-only response consumes an ordinary existing call, and cannot replace the
mandatory final structured proposal or create more budget.

All original model output remains in capture. Parsed note text is excluded from
active assistant history; native call IDs/arguments/results stay correlated.
Only the bounded current notebook view is added on the next request. The existing
read batch calls the note observer **after** known completion and exact feedback
validation, never at preflight. A source quote is then recorded as a literal host
observation, without endorsing any defect interpretation.

The initial candidate always refers to immutable archived evidence. A baseline
gets a live snapshot/Tool pointer only if its path is already in the review read
scope; otherwise it too remains retained subject evidence. Candidate text can
never acquire the baseline's live identity at the same path. `SourceBinding.reopen`
rechecks the anchor and reprojects the original quote; live references provide an
existing `read_source` pointer, archived references point back to the retained
subject. Neither path silently reads the filesystem or authorizes a Tool.

The model sees verified disclosed ranges and unread gaps, separate from semantic
assessment and currently active source. Historical acquisition after reduction
does not become an edit witness. Private-oracle implementation, host diagnostics
and coding-worker private conclusions are not notebook inputs. A model can cite
only the independently selected source registry.

## Reconstruction and bounds

Checkpoints use `task-role-working-notes-v1` inside sealed native
`review-working-state` observations, with a model-response digest or completed
read origin. Original source is not copied into a second database. The adapter
`restore()` accepts a **trusted episode checkpoint**: authenticate it through the
existing native reader, reconstruct bindings from the same approved subject and
completed source-read receipts, then restore matching task/role/episode notes.
Never feed model text to checkpoint restoration or replay a consumed dispatch.

The immutable checkpoint retains notes, quotations, source identities, relations
and host check references. Reconstructed source bindings determine freshness;
stale notes remain explicit rather than regain current status. Reconstruction
does not restore grants, native attempts or permission. Tests remove historical
model messages and reconstruct the same working Context from retained state.
The reviewer still retains its existing raw source exchanges and hard prompt
budget; this increment does not add a new source-history compaction policy.

There are 32 retained records including revisions, 1,024 characters per claim or
contract, four support quotes of 512 characters, and eight model notes per batch.
Projection accounts for procedure/envelope bytes and selects complete records
within 8,192 bytes, reporting omitted notes/sources. Omission does not delete
history or claim complete coverage. Failure to fit mandatory scope fails closed.

## Deterministic evidence and next steps

Tests cover exact evidence, Unicode ranges/gaps, scope isolation, stale sources,
contradictions/revisions, bounded projection, reconstruction, private/unread
reference refusal, native read correlation and unchanged final delivery. The
bounded P3 fixtures preserve the published candidate identity and two false
claims. Matching their source quotations leaves the model claims provisional;
an explicit independent regex countercheck can support a host-attested
counterclaim. This is not a general semantic contradiction detector, hidden
acceptance, or evidence that a model reasons correctly.

The smallest coding-worker integration is to record one helper/consumer
relationship with source anchors to both return/yield and call sites, the
expected API shape and any uncertainty. Reconsult both exact sources before
editing; regenerate bindings after changes. Reuse existing coding disclosures
and active projection, rather than create another source ledger or automatically
trust a compaction summary.

Cross-task procedural memory remains separate. The first promotion mechanism
should be an explicitly reviewed, versioned playbook entry: exact role/model/
provider conditions, source/evaluation evidence, known counterexamples and
confidence, with explicit host selection/revocation. Neither one verified
quotation nor successful JSON warrants automatic promotion.

A prospective **unexecuted** effect-free comparison can use four P3 review
episodes: two baseline and two working-notes conditions, counterbalanced, each
with at most two calls, 2,048 output tokens/call and identical public evidence,
Tools, model and sampling. Maximum eight generations. Score final delivery,
identities, obligation coverage and every factual/causal claim separately;
retain all notes, source bindings, raw requests/responses, usage and timing. This
measures the combined procedure/state package, not an isolated memory effect.
Freeze exact requests, scoring, scope and duration before obtaining a fresh
single operator approval. No inference is authorized by this documentation.

## Validated implementation

Implementation `b5b1936cb288b3853f3ddef13e22276cabad0614` passed 135 focused
consumer tests, strict mypy over 641 files, supported-input Ruff/format checks,
layout and link checks. Its single protected run passed **4,406 tests with two
opt-in live Codex tests skipped**, at **100% production branch coverage**.
The managed deadline was 7,200 seconds; actual wall time was 4,135.70 seconds.
The complete receipt confirms unchanged inputs. See the compact
[validation evidence](../research/code-audit/working-notes-20261105.json) for
source identities, receipt hashes, command and limitations.

Supported-input static checks target framework/tests/apps/scripts, excluding
retained `tests/experiments/`. Root-wide Ruff additionally encounters immutable
research/generated archives; its check reported archival diagnostics and its
formatter panicked while rendering retained artifacts. Those invocations are
not called passing, and no historical artifact or global lint policy was changed.
Working-note accuracy under a live model remains unmeasured.
