# Investigation-transition-0001

**Outcome: the bounded read-only diagnostic did not establish an
investigation-to-implementation transition.** It demonstrated a task-directed
search and additional source selection, but no expressed implementation hypothesis,
source-supported engineering decision or specific blocker. B-0035 remains open.
There is no candidate, repair, worker validation or model-authored production change.

## Identity and authority

The [protocol](protocol.md) and [freeze](freeze.json) preceded inference. Freeze
digest is `ca6a2b2843edbd0ce2585aa052f08e5ab9626bc260b65d21d1a22dcac4b029a8`.
The validated executable commit was `c2bc06f4f604c6ccb87279f6315bfa87b59ce6fa`;
the run entered from `27d7d14a1c318b58ce4b2aeb72dd3e5926d7802d`, which added only
the freeze and documentation/evidence. The configured Qwen3.8-27B quantized artifact
SHA-256 was `40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`.
The read-only bind-mounted model, pinned llama.cpp b10868 image, profile fingerprint,
chat template, sampling and 32K profile were authenticated. Thinking remained
disabled; there was no provider substitution, auxiliary inference or setting change.

The host supplied seven exact method/contract units through ScopedSourceTool and
ToolRunner, amounting to 15,275 source bytes on this revised source. They were
explicit host disclosures, not model-selected reads. No hidden oracle or patch
was supplied. The initial complete request was 27,684 bytes. Its source-status
annotation added 1,912 bytes including message-list serialization overhead.

Only search and source-read operations were advertised and admitted. Editing,
checks, arbitrary shell and publication were unavailable. The shared coding
process enforced four acting calls, six acquisition actions, 90 seconds per call,
360 seconds agent wall time, and an outer 420-second bound. Input was capped at
28,160 measured tokens, output at 4,096 tokens, complete requests at 32,768 bytes
and each disclosure at 8,192 bytes. No limit was raised.

## Observed trajectory

| Request | Complete bytes | Input/output tokens | Model-selected action | Outcome |
| --- | ---: | ---: | --- | --- |
| 1 | 27,684 | 6,977 / 55 | Task query scoped to repository.py | Eight relevant metadata candidates |
| 2 | 32,768 | 9,795 / 63 | Read `[17325,20600)` | 3,275 exact source bytes |
| 3 | 32,364 | 8,123 / 63 | Read `[20600,24500)` | 3,900 exact source bytes |
| 4 | 32,768 | 8,108 / 63 | Read `[17325,20600)` again | 3,275 exact bytes retained, not consumed |

The query was `metadata resource inventory prompt messages repository_id
snapshot_id source_acquired`. Search returned prepare/build_request and related
host methods. The additional ranges contain classification, native read/feedback
and acquisition mechanics; they are relevant implementation information, not
unauthorized or arbitrary files. Their selection is observable partial progress.
However, all four ordinary response contents were empty, and the responses
contained no explanation identifying a missing obligation or proposed engineering
change. Navigation alone does not establish the predeclared transition criterion.
This is not proof that the model could never solve the task or that further source
investigation was irrational.

All four core repository-host methods and both public diagnostic assertions stayed
fully active. The seventh supplied unit, SourceScope, was partially presented on
request two to make room for the latest metadata exchange and status annotation;
it was fully present again on requests three and four. Host-selected user-role
source is not automatically protected against partial presentation. Required task
instructions remained exact. This qualification prevents confusing initial
acquisition with uninterrupted complete availability.

On request three the older search exchange was omitted. On request four the
first additional source exchange was omitted and the second additional read was
presented as `[20600,24154)`, 3,554 of its original 3,900 bytes. The repeated range
was therefore absent before the model requested it again. It was a valid
redisclosure of evicted source, not an automatic Tool replay or a repeat of source
still fully active. Temporal association does not prove why the model chose it.
The final repeat's feedback never reached a fifth request, so this run does not
demonstrate actual consumption of a positive repeat-count annotation.

## Independent assessment and limitations

[Independent review](review.json) joins each original native call to exactly one
retained feedback message and records all projected source spans. Four Tool
dispatches were acknowledged, with no known ambiguous effect. Three reads disclosed
10,450 bytes over 7,175 unique ASCII source positions; only the first two read
results were consumed. No invalid range, source refusal, provider normalization
failure or capacity refusal occurred. The worker stopped at `model_limit`.

Known usage was **33,003 input and 244 output tokens**. Inference took
**53.359243 seconds**, the shared process **54.329113 seconds**, and the complete
managed wrapper including service authentication and administration **81.216612
seconds**. Cached/reasoning usage was not reported and remains unknown. Generated
token count does not establish private reasoning quality.

The worker was free to respond in plain text. It chose four native operations.
The annotation did not induce an observable implementation decision in this
sample. Its nonzero byte cost contributed to pressure; opting in is not free.
The host-selected working set, read-only decision instructions and annotation
all differ from the predecessor, so this is not a controlled causal estimate of
any one change. There was no edit authority, so it cannot measure edit correctness.

The strongest justified next step is a separately authorized **decision checkpoint
diagnostic**, using existing ModelInteraction and the same exact methods to obtain
a concrete action/uncertainty report before another full B-0035 trial. Determine
whether a response-only decision turn can elicit a source-supported hypothesis;
do not add another retrieval layer or infer that automatic Tool choice is forced.
Any such future protocol should budget the status overhead and explicitly protect
source contracts it requires continuously. It is not authorized or executed here.

## Custody, retention and framework validation

The canonical Checkout owner was released normally. Original source, index and
forensic files were unchanged. While owned, every generated artifact stayed under
ignored staging; exact bytes were copied into [evidence](evidence/) only after
release. The original entry, native request/outcome pairs, projections, source
results, wrapper exit zero and [release receipt](evidence/checkout-release.json)
are retained. Wrapper success means successful controlled execution, not task
success. Earlier unknown grading-wrapper exits remain unchanged and unknown in
their original experiment.

The shared projection implementation passed **3,899 protected tests**, two optional
skips and 100% configured production line/branch coverage. Independent scripted
tests exercise actual navigation, repeat disclosure, edit admission, managed
fixed validation and restoration, plus continued rereading and honest stopping.
Those scripted successes are not live maintenance results. See the
[implementation contract](../../docs/development/investigation-transition.md) and
[delivery receipt](../../docs/research/code-audit/investigation-transition-20261029.json).

The frozen predecessors, thirteen forensic files, 903 RI ledger rows, retained
refs and 188 unresolved historical RI-version obligations are preserved. This
case is closed to further inference; a new diagnostic requires a new identity
and explicit authorization.
