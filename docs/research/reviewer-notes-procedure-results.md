# First unattended reviewer-note procedure comparison

**Standing authorization worked; factual reviewer accuracy did not improve.**
Eight genuine Qwen generations ran through fresh `WorkCycle.routine.local`
grants with **zero per-run operator approvals**. Explicit inspection-time
guidance produced one valid early provisional note, versus none with the
existing procedure. Neither reviewer identified the known defect; both proposed
incorrect acceptance and neither final review was strictly admitted.

## Authority and frozen design

The experiment starts from synchronized `main`
`28425b5c2b32bb181f716251fea5baa2df3a021f` under active standing version
`26b93f4ae7ca8dcfbf228f62dd0ffa4ea94057cf953e529e2f7db61e27f46978`.
The [actual grants and ledgers](code-audit/reviewer-notes-procedure-20261105/authority.json)
bind one executed parent allowance of eight calls and two children of four
calls/three reads each. Child budgets are carved from the parent, not added
to it. Every generation uses `local.interact` with measured input and current
provider qualification. Each source read uses `local.enter/complete` around
the existing native read-acquisition owner. There is no manual child grant,
historical approval reuse, new operator-control event or native WorkCycle slot.

The [frozen packet](code-audit/reviewer-notes-procedure-20261105/frozen.json),
identity `482e7291b75c6138f3b1ec85bfe101a1a80b42acd43c33340eafad8df7eaa788`,
defines one alternating pair of four-turn reviews. Both enable the unchanged
`ReviewNotes` procedure, use the same authenticated full baseline/candidate,
public task and fallible historical leads, and retain the strict native Tool
and conclusion contracts. Fresh episode/subject/source identities differ to
isolate the actors; the callable schema structure is unchanged.

The existing arm receives the current production working-note instructions.
The explicit arm adds the prospectively frozen instruction to create one compact
provisional hypothesis/question during inspection, name its evidence, reconsult
its real sequence, check contradictions and revise only with support. Unknown
coordinates must not be guessed: existing unanchored hypotheses remain allowed.
No parser, anchor validator or conclusion schema is relaxed.

Before turn three, both lose prior inspection exchanges and reconstruct their
own captured checkpoint. Original full source remains available. Only the
current bounded working view is projected; accepted note text is omitted from
active assistant history as in NativeReviewer. Valid notes-only inspection
responses would be supported without extra calls; all six actual inspections
instead deliver native source reads. This host composition differs from the
older calibration's accumulating note projections, equally for both new arms.
Historical percentages are therefore not a controlled comparison to this pair.

The exact [independent grader](code-audit/reviewer-notes-procedure-20261105/grader-only.json)
retains SHA256
`76a21c1bd6c751d450a947f500817b6e8c5cdbb2e47be39e2dd924703311ac04`
from the [previous comparison](reviewer-working-memory-effectiveness.md).
No grader implementation, expected disposition, corrected lead annotations or
verified conclusion enters either actor's Context. The archived candidate
retains SHA256 `ea9619b09ebaca244b358179fecc7c952be37e07edac66ba5171f19b3af3b119`;
the 5,910-byte baseline retains
`a5510a1b30945060c3d1438f0832cc8ffe5d9ee6248d5e24bd66feea6c5fb645`.
The baseline fixture is not current production and the candidate is never installed.

The pinned `qwen38-local` endpoint, GGUF, image, native template, 64K service,
q4_0 KV cache and inherited sampling remain unchanged. Thinking is disabled;
all calls reserve 2,048 output tokens with a 16,384 input-token ceiling. There
are at most eight calls, 16,384 reserved output tokens, six reads, 120 seconds
per call, 1,020 seconds overall and 4 MiB capture. No retries or per-call human
permission occur. Exact request settings and provider observations are retained.

## Every generation

| Call | Procedure / turn | Input tokens | Output tokens | Seconds | Actual result |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | Existing / inspect 1 | 6,963 | 58 | 18.163 | Read; no authored note |
| 2 | Explicit / inspect 1 | 7,216 | 200 | 19.267 | Read plus one valid provisional note |
| 3 | Existing / inspect 2 | 7,707 | 908 | 48.841 | Read plus unstructured prose labelled working notes |
| 4 | Explicit / inspect 2 | 8,955 | 62 | 11.704 | Read; no requested revision/check note |
| 5 | Existing / inspect 3 | 7,888 | 88 | 11.669 | Read after checkpoint reconstruction |
| 6 | Explicit / inspect 3 | 8,874 | 62 | 11.387 | Authored note exposed, then read; no explicit reconsultation/check |
| 7 | Existing / final | 8,694 | 1,538 | 81.073 | Native accept proposal; malformed companion notes |
| 8 | Explicit / final | 9,658 | 720 | 48.126 | Native accept proposal; missing required acceptance evidence |

All eight responses finish with `tool_calls`; none truncates. All six source
reads complete. [Raw calls](code-audit/reviewer-notes-procedure-20261105/calls.json)
preserve exact UTF-8 request/response bytes, native IDs, usage, timings,
normalization, per-call provider observations and consumed routine entries.

| Measurement | Existing | Explicit inspection guidance |
| --- | ---: | ---: |
| Valid authored notes during inspection | 0 | 1 |
| Valid authored revisions/supersessions | 0 | 0 |
| Explicit later reconsultation of authored note | Not available | Not demonstrated |
| Note-linked contradiction checks | 0 | 0 |
| Input / output tokens | 31,252 / 2,592 | 34,703 / 1,044 |
| Cached prompt tokens reported by server | 2,572 | 2,560 |
| Sum of measured generation-call latency | 159.746 s | 90.484 s |
| Strictly admitted final proposal | 0/1 | 0/1 |
| Factually correct final review | 0/1 | 0/1 |

The explicit arm uses 11.04% more input tokens, 59.72% fewer output tokens and
43.36% less measured call latency in this pair. The existing arm's long prose
analysis and final response explain much of the difference. Fixed order,
uncontrolled sampling and caching preclude a causal performance estimate.
The executed packet takes 252.24 seconds, comfortably within its limits.

## What the model actually remembered

The explicit first note is a provisional hypothesis about the candidate's regex
and the `C#`/`C# #` cases. Its source anchor is exactly `candidate[0:1] == "#"`:
the file's copyright/comment prefix. **The anchor is literally valid but does
not support the regex claim.** The claim is not promoted to a verified fact.
This is successful protocol adoption, not relevant evidence verification.

The [retained episode records](code-audit/reviewer-notes-procedure-20261105/episode-records.json)
show that authored sequence 1 persists and is exposed on turns two and three,
including reconstruction from saved JSON before turn three. Qwen then returns
only source reads, with empty assistant content, despite the request to name,
check or revise that note. The model's latent use is unknown; no explicit
reconsultation or note-linked contradiction check is demonstrated.

After the third read, the checkpoint contains the authored hypothesis and three
automatic literal quotations. The 8,192-byte projection retains only recent
source sequences 3 and 4, explicitly reporting two omitted notes. The authored
sequence is therefore absent from the **final model request**. It is not stale
or deleted; bounded projection has omitted the active claim before synthesis.
This is a measured Context-selection limitation, not evidence of model recall.

The existing arm does reason during inspection: its second response contains
908 tokens of prose headed `Working notes:` and useful ordinary-case traces.
It partially questions a historical claim while misattributing its target to
baseline. That prose does not use the note protocol, is never admitted as
working state, and is discarded at reconstruction. Its late final note block
has extra prose after JSON, invalid `inference` note kinds and incorrect `r`
quotes for the candidate's first character. Actual admission stops at the JSON
extra-data error; these records are not repaired into successful notes.

## Factual review and strict disposition

Both raw final proposals accept the candidate. Both miss the frozen true defect:
`# ##` produces `##` instead of the required empty title. Ordinary examples
`# C#`, `# C# #` and `# Title #` are traced to correct final titles, but they do
not establish the complete contract. Both infer preserved empty-title/lookup
behavior from unchanged consumer code while overlooking the changed regex
producer. The explicit summary also invents trailing whitespace in its `# C#`
trace. The existing conclusion calls `# C###` unspecified despite the task's
general attached-hash rule.

Neither proposes a genuine blocking defect. The existing arm supplies four
advisory findings; the explicit arm supplies none. Fewer findings is not better
factual accuracy when false assertions remain in an incorrect acceptance summary.
Execution caveats are acknowledged but do not justify acceptance.

Both native proposal calls carry the correct subject/candidate identities.
Existing-arm processing first rejects malformed companion notes; a separate
host-only diagnostic also rejects its verbose obligation identifiers. The
explicit proposal uses the correct obligation names but lacks the unchanged
required acceptance references (`task`, `baseline`, `public-checks`, `acceptance`,
`custody`). Those absent records are not fabricated. This gate failure is
separate from the independently false recommendation. The
[scores](code-audit/reviewer-notes-procedure-20261105/scores.json) and
[source-bound counterchecks](code-audit/reviewer-notes-procedure-20261105/host-claim-checks.json)
preserve all failures. Counterchecks inspect AST regex literals and perform only
matching plus `.strip()`; candidate code is never imported or executed. These
are public diagnostic checks, not new private acceptance or hidden holdouts.

## Pre-entry diagnostic and preservation

An earlier preflight created automatic grants but consumed **zero model entries**.
The generation capture tap intercepted `/apply-template` token measurement;
the next measurement response collided with its filename. The saved HTTP-200
body contains a rendered `prompt`, and both child model-entry ledgers are empty.
The original frozen packet, unused grants and failure are retained in authority
evidence. A prospective correction disables only the generation tap during
measurement. Exact requests, sources, settings and scoring remain unchanged;
fresh standing grants bind the corrected driver. No model call is replayed,
no operator is interrupted, and total genuine generations remain eight.

No production input, standing policy, persistent service, Inspector, historical
attempt or native slot is modified. No comprehensive suite is repeated.
Publication checks cover frozen/grant/source identities, raw byte round trips,
budgets, actual note reconstruction/projection, factual-score consistency,
links, layout and Git integrity. See the
[manifest](code-audit/reviewer-notes-procedure-20261105/manifest.json) and
[validation receipt](code-audit/reviewer-notes-procedure-20261105/validation.json).

## Next productive improvement

Prioritize **source-bound evidence verification** over broad coding-memory rollout.
The reviewer can store a note yet cite an irrelevant character and infer
behavioral equivalence from unchanged consumers. The smallest useful next
integration should reuse fixed public-check/source owners to provide bounded,
versioned observations of a claimed producer output, then let the reviewer
reconsult that evidence. Keep private oracles excluded and avoid arbitrary
reviewer code execution or a new verification framework.

Also preserve the compact active hypothesis/contract in the existing bounded
Context selection, or clearly surface its omission before finalization. More
storage would not fix a claim that is irrelevant-anchored or unavailable at the
decision point. A later coding-worker increment should qualify one return-value
producer/consumer relationship with relevant anchors to both units and prove
it survives projection before an edit. This pair does not establish that benefit.

[Candidate playbook v5](code-audit/reviewer-notes-procedure-20261105/candidate-playbook-v5.json)
records the early-note adoption signal and the negative factual results. It
remains unqualified and inactive; one matched pair proves no statistical optimum,
universal prompt or reliable reviewer accuracy. No next implementation is started.
