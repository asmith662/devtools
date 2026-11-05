# First live reviewer working-memory comparison

**No factual improvement was demonstrated.** Eight explicitly authorized Qwen
generations completed in one matched pair of four-turn reviews. Both conditions
read source three times and delivered native final proposal calls. The baseline
rejects for false reasons; the memory condition accepts the defective candidate
and fails strict admission. Neither produces a factually valid review.

The memory workflow restores two automatic source quotations after Context
reduction. Qwen creates no valid model-authored notes, revisions or supersessions.
Its first attempted authored note arrives alongside the final proposal, with an
invalid source interval. This measures working-state transport, but **does not
demonstrate productive maintenance or later use of the reviewer's own notes**.

## Frozen comparison and authority

Execution starts from synchronized `main` at
`eb0b68b24ad102bc9bdafa622e2010c69cc5cf2d`. The actual operator `+approve`
follows a visible request for scope
`0846357868987c9137f61b04f54a228cf45f8501b1540a81ad9f180b31c41184`.
[Authorization](code-audit/reviewer-memory-live-20261105/approval-scope.json)
and the [actual reply record](code-audit/reviewer-memory-live-20261105/operator-approval.json)
are separate; previous grants and standing routine authority are not reused.

The [frozen plan](code-audit/reviewer-memory-live-20261105/plan.json) preserves
eight generation slots, alternating baseline/memory through three inspection
turns and one final synthesis. This prospectively replaces the earlier
documentation's two-turn sketch: a four-turn condition permits creation,
revision and subsequent retrieval. There is one pair, not four replicated pairs
or eight independent reviews. Scope, scoring and model-visible source do not
change after execution begins.

Both conditions receive the complete authenticated historical baseline and
candidate, original public task requirements, and two explicitly fallible public
P3 claims. The candidate retains SHA256
`ea9619b09ebaca244b358179fecc7c952be37e07edac66ba5171f19b3af3b119`.
The exact 5,910-byte baseline retains SHA256
`a5510a1b30945060c3d1438f0832cc8ffe5d9ee6248d5e24bd66feea6c5fb645`;
its coding-assignment identity and canonical content identity are authenticated.
Read Tools access only this frozen fixture, never current production or an
installed candidate. The [subject](code-audit/reviewer-memory-live-20261105/subject.json)
contains no expected recommendation, correct-title annotations, coder conclusion
or private acceptance implementation. A preflight packet containing the public
fixture's grader-answer fields was rejected before approval or generation;
its identity and zero-entry diagnosis remain recorded.

The treatment adds the existing evidence-first procedure and bounded
`ReviewNotes` Context; it seeds no correct semantic notes. Before turn three,
both conditions lose their earlier inspection exchanges but retain the original
task and full sources. Only memory restores its own recorded checkpoint.
This is a combined procedure/state comparison, not an isolated test of storage.
It composes the production ModelInteraction, `ReviewNotes`, native read
acquisition and unchanged final-proposal validators as effect-free calibration;
it does not enter a governed native review lifecycle or consume WorkCycle slots.

The unchanged pinned `qwen38-local` service uses 64K Context, the same GGUF,
template, q4_0 KV cache and inherited sampling as the
[P3 follow-up](llm-harness-p3-followup.md): temperature 1, top-p approximately
0.95, top-k 20, min-p approximately 0.05, thinking disabled. Each call reserves
2,048 output tokens, with a 16,384-token input ceiling and 120-second deadline.
The packet permits 16,384 total output tokens, 1,020 seconds overall, six
32,768-byte read ceilings and 2 MiB capture, with zero retries. No `tool_choice`
or response-format enforcement is added. Exact settings, native IDs, wire
requests, raw responses and server properties are retained in the evidence.

## All eight generations

| Call | Condition / turn | Input tokens | Output tokens | Generation seconds | Actual result |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | Baseline / inspect 1 | 6,104 | 85 | 12.879 | One completed source read |
| 2 | Memory / inspect 1 | 6,961 | 61 | 3.816 | One completed read; no authored note |
| 3 | Baseline / inspect 2 | 6,623 | 59 | 3.394 | One completed source read |
| 4 | Memory / inspect 2 | 9,198 | 62 | 6.323 | One completed read; no authored note |
| 5 | Baseline / inspect 3 | 6,121 | 59 | 3.022 | One completed read after reduction |
| 6 | Memory / inspect 3 | 8,497 | 62 | 5.690 | Two saved quotations restored; one completed read; no authored note |
| 7 | Baseline / final | 7,540 | 769 | 45.296 | Admitted rejection; false findings |
| 8 | Memory / final | 11,473 | 1,823 | 93.673 | Native accept proposal; invalid companion note and obligation names |

All responses finish with `tool_calls`; none truncates or hits the output
ceiling. All eight native IDs are fresh and correlated. There are no generation
retries or failed source acquisitions. The
[raw calls](code-audit/reviewer-memory-live-20261105/calls.json) preserve exact
UTF-8 bodies by hash, normalized responses, timings, tokens and admission results.

| Measurement | Baseline | Working memory |
| --- | ---: | ---: |
| Generations / completed reads | 4 / 3 | 4 / 3 |
| Input / output tokens | 26,388 / 972 | 36,129 / 2,008 |
| Server-reported cached prompt tokens | 12,126 | 19,347 |
| Sum of generation latency | 64.591 s | 109.502 s |
| Native final call / matching subject and candidate IDs | Yes / yes | Yes / yes |
| Strictly admitted final proposal | Yes | No |
| Correct factual final review | No | No |
| Accepted model-authored notes / revisions | 0 / 0 | 0 / 0 |

The memory condition consumes 36.91% more input tokens, 106.58% more output and
69.53% more generation time in this pair. Prefix caching, fixed order,
uncontrolled sampling and different response lengths confound latency. These
are actual costs, not a stable performance estimate. Full packet wall time is
364.22 seconds including the host interruption below; generation time sums to
174.09 seconds. All original limits remain satisfied.

## Factual scoring and actual note use

The [frozen grader](code-audit/reviewer-memory-live-20261105/grader-only.json)
is never sent to either reviewer. Host checks extract only the candidate's
literal regex using AST inspection, then apply its matching and `.strip()`;
they never import or execute candidate code. These public diagnostic
counterchecks are not new hidden acceptance. The
[claim checks](code-audit/reviewer-memory-live-20261105/host-claim-checks.json)
and [scores](code-audit/reviewer-memory-live-20261105/scores.json) retain negative
findings separately from delivery.

Baseline proposes two unsupported findings. It claims `# C#` followed by
spaces becomes `C`; the exact candidate returns `C#`. It treats removing
trailing whitespace from `# Title ` as a new violation, although both parsers
apply `.strip()` and return `Title`. Its summary repeats the old false
`# C# #` corruption claim; the candidate returns `C#`. A rejection label is
appropriate for this candidate, but neither alleged defect identifies the
actual failure: `# ##` yields `##` instead of the required empty title.

Memory correctly traces `# C#`, `# C# #` and `# Title #`, and correctly notes
that the source delta is confined to the regex. These are limited accurate
source facts. It nevertheless asserts unchanged pure-hash/empty-heading
behavior and accepts the candidate without finding the genuine empty-title
defect. It treats speculative multiple-run behavior as outside scope without
establishing that exclusion. Its runtime caveats do not justify acceptance.
Both reviews therefore fail the prospectively defined factual criterion.

Memory's final companion note specifies `[780, 890)`, a 110-character interval,
but supplies a 157-character quotation that does not match it. The unchanged
atomic note validator rejects the batch; it creates no verified fact or
retained authored note. Independently applying the unchanged final validator
also rejects the proposal's verbose obligation descriptions in place of exact
`objective` and `current-owner` identifiers. Neither failure is repaired or
normalized into admission; no synthetic public/private/custody evidence is
invented to support its acceptance.

The [episode records](code-audit/reviewer-memory-live-20261105/episode-records.json)
show three host-created literal quotation notes, with no semantic host
attestations. Two are reconstructed from stored JSON before turn three.
After the third read, all three remain in the checkpoint, while the bounded
8,192-byte projection omits the oldest note and explicitly reports that
omission. There is no source drift. These are valid quote/identity/freshness
observations, not model-generated interpretations promoted to truth.
Final citations mention the three read receipts, but full source and a later
read remain available: citation reuse does not demonstrate reliance on saved
notes. No valid authored observation is subsequently revisited, corrected or
superseded. Active note maintenance remains unqualified.

## Host interruption and preservation

After five completed generations, a local driver equality assertion compared
JSON-decoded lists with in-memory tuple fields and stopped before call six.
The original driver and interruption are preserved. Canonical JSON digest
comparison authenticates the same state. Completed responses/read receipts
reconstruct source bindings and histories without reentering a Tool or model.
A second host-only comparison encountered the same representation mismatch
before any new entry; it is corrected the same way. The
[recovery receipt](code-audit/reviewer-memory-live-20261105/known-entry-recovery.json)
binds both driver versions. Only the three unused frozen slots resume, including
the real JSON checkpoint reconstruction, inside the original wall deadline.
No prompt variant, task, scoring rule, budget or production implementation
changes. This interruption limits operational smoothness; it is not a model
reasoning failure or an additional experimental attempt.

## Next bounded decision

The strongest immediate blocker is **model adoption of valid provisional notes
during inspection**, followed by grounded final reasoning. The smallest
candidate increment belongs in the existing reviewer instruction/budget view:
ask for one compact provisional claim or unresolved contract during inspection
and reconsult it before synthesis. A hypothesis may remain anchor-free when
exact coordinates are unknown; only exact, already disclosed quotes may anchor
a source claim. Keep note verification and the final proposal schema strict.
This is a recommendation for prospective qualification, not an implemented or
empirically proven fix. First qualify creation, revision and retrieval before
attempting to infer an accuracy benefit. Preserve public source/contract leads
and withhold grader answers; do not preload corrected notes.

For a coding worker, the smallest future consumer is one producer/consumer API
relationship, anchored to the actual return/yield contract and call site via
existing coding disclosures. Keep it provisional and reopen both versions
before an edit. This reviewer result does not establish that coding benefit.

For durable memory, start later with explicit host-selected episode retrieval
scoped to role, task and source version, with currentness checks and original
evidence reopening. No automatic cross-task promotion is justified here.
Procedural promotion should remain an explicitly reviewed, versioned playbook
entry with conditions, counterexamples and confidence.
[Candidate playbook v4](code-audit/reviewer-memory-live-20261105/candidate-playbook-v4.json)
records this negative result without activation or universal-memory promotion.

## Publication checks

The unchanged implementation's 59 focused tests passed before inference; their
receipt is retained. Documentation/evidence integrity, raw-byte round trips,
frozen hashes, scoring consistency, links, layout and Git connectivity are
checked for publication. No comprehensive protected suite is repeated for this
documentation-only result. Production inputs, service configuration, Inspector,
standing authority, historical attempts, B-0053 closure and the preexisting
untracked source-grounding work remain unchanged. The
[manifest](code-audit/reviewer-memory-live-20261105/manifest.json) and
[validation receipt](code-audit/reviewer-memory-live-20261105/validation.json)
bind the published evidence and checks.
