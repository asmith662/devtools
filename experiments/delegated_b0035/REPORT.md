# Supervised B-0035 delegation with a stable working set

**Qwen produced a real implementation that passed the behavioral checks, but
stage A was not accepted.** Its first proposal arrived on the eighth and final
call. Four focused tests passed; one Ruff line-length error failed the frozen
managed checks. No model call remained to consume that feedback. Independent
grading then passed three withheld tests, 34 compatibility tests and strict mypy.
The candidate was preserved unchanged and restored out of production. Stage B
was not entered; B-0035 remains open.

## Authenticated baseline and coherent delegation

Local and remote main were `231c3933340afe8361a2121505da84cd67918cf0`, with no
tracked/index changes or active Checkout owner. Protected executable ancestor
`72379015cf4f34f74a9282661aac8aa0362c9977` passed 3,906 tests, two optional skips
and 100% configured production line/branch coverage. Its 1,191 physical inputs
remain unchanged. The preceding ten-read/no-edit joint-Context run remains frozen;
this run neither replays it nor claims its acquisitions were continuously active.

B-0035's relevant behavior was split along existing responsibilities:

1. Complete authorized resource metadata representation in
   `devtools.agents.coding.navigation`, separate from ranked task candidates.
2. Conditional request integration/lifecycle in the repository host/navigation
   composition: first presentation, nonduplication, refresh and full capacity.

The first owner already presents native source metadata. Its 13,044-byte source
had 19,724 bytes of headroom, while repository.py had only 737 bytes. A needed
representation and a future real host consumer justify the boundary; an unused
helper alone would not justify production integration. No new module, provider,
index, Context policy, coding loop or source-size relaxation was introduced.

The supervisor supplied a callable/representation contract and public diagnostics,
not implementation logic. [Task](task.md), [protocol](protocol.md),
[freeze](freeze.json) and [runner](runner.txt) were committed at
`7f48da63048ac5de1437af6e0ba565dfa71537ae` before inference. The worker alone
selected the source actions and implementation. The independent reference and
withheld checks were outside its authorized source surface.

## Exact source and affordability

Six current RI/Context disclosures supplied navigation imports, navigation_feedback,
SourceScope, RepositoryResourceOccurrence, RepositorySnapshot and public focused
diagnostics. Total exact source was **10,151 bytes**, versus 20,457 in the prior
eleven-unit handoff. The complete initial native request was **19,640 bytes**.
These were host-selected source acquisitions, not model-selected Tool calls.

Pure prospective projection after two representative native read results measured
**22,860 and 26,157 bytes**. All initial source remained exact, without shortening.
This characterization did not execute those Tools or fabricate execution receipts.
In the actual run, all six initial units also remained exact through all eight
requests. The largest actual request was **32,374 bytes**, below the unchanged
32,768-byte cap. Older additional native exchanges were omitted as history grew
to a 50,572-byte unreduced request. No source summary or auxiliary call was used.

Metadata, host source, model-selected disclosure and current edit witnesses remained
distinct. The admitted anchor was in current exact navigation source. No hidden
oracle, supervisor implementation, invented read, expanded permission or source
creation was supplied. Full range/version accounting is in [review](review.json).

## Independent preflight and finite model envelope

The baseline failed all four representation diagnostics and all three withheld
tests for the expected missing callable. Seven independent positive controls and
four corrupted-payload controls passed. UTF-8 expectations were separately checked
against literal encoded byte sequences and the filesystem observation's byte count.
The oracle covers empty scope, complete 19-resource inventory, content/repository/
snapshot identities, editability, privacy, currentness, noncanonical observations
and complete-result capacity refusal. It is empirical cross-checking, not proof.
See [preflight](preflight.json) and its retained XML files.

Authenticated model: existing **Qwen3.8-27B**, llama.cpp `qwen38-local`, GGUF
SHA-256 `40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`.
Thinking-disabled sampling and serving configuration were unchanged. Bounds were
eight acting calls, three proposals, up to two natural check-feedback repairs,
sixteen acquisition actions, 2,048 output tokens/180 seconds per call, and a
1,140-second process budget inside a 1,200-second watchdog. Input tokens were
measured independently of serialized bytes. Existing source/disclosure/edit bounds
remained unchanged. No paid inference, download, alternate model or automatic retry
occurred. At previously observed throughput, maximum generation takes about 93
seconds; all calls here completed normally.

## Observed implementation and validation

Calls one through seven selected seven reads and one search. The worker read
resource identity code and successive navigation ranges; it then repeated the
navigation tail and an earlier range. Additional acquisition totaled **19,280
bytes**: 12,369 newly disclosed relative to the initial packet/history and 6,911
repeated bytes. One repeated read was fully active already; another restored
evicted source. One near-duplicate extended the host method disclosure by one
newline. These distinctions do not establish the model's private reasoning.

Call eight proposed `complete_inventory` before navigation_feedback. One exact
replacement was admitted and installed, growing navigation.py to **14,604 bytes**.
It uses the existing currentness check and resource fields, validates bounds and
foreign editability, orders complete rows, and refuses an unaffordable result.
The [exact candidate](evidence/candidate/src/devtools/agents/coding/navigation.py.txt)
has SHA-256 `cb2f9b18800efe302c271b2cf385646457d0a8daa3c205fa8c67b0b1b5670282`;
the [diff](candidate.diff) is model-authored. No supervisor repair was made.

The host automatically executed its fixed checks, not a model-selected validation
Tool: **4 focused tests passed**, formatting passed, Ruff failed **E501 at line
315 (95 columns versus 88)**. The native replacement result contains the truthful
failed-check feedback. It was retained but never consumed by another model call.
The process ended `model_limit`, `accepted=false`, `completed=true`, with no
primary/completion error and restored custody. There was one proposal/application,
zero natural repairs and no second-stage invocation.

Independent grading temporarily installed exactly the archived candidate under
a new guarded Checkout owner and restored original bytes afterward. **3 withheld
tests, 34 existing navigation/host compatibility tests and strict mypy over 612
files passed.** These are real candidate outcomes, not scripted worker responses.
They establish useful representation behavior within the checked cases. They do
not override the frozen lint failure, establish initial Prompt integration or
exercise the full B-0035 integration predicates. Therefore stage A is not accepted
for continuation, stage B is not attempted and no model code enters production.

Usage was **61,251 known input tokens, 932 output tokens and 69.312427 model
seconds**. The worker Checkout interval was 74.793833 seconds, including capture and release. Cache/reasoning usage remains unknown. Native IDs, original provider
bodies, normalized responses, actual history, projections, exact candidate and
both terminal/custody receipts are retained under [evidence](evidence/).

## Preservation, validation and recommendation

Both Checkout owners released normally. All generated grading/worker artifacts
remained in ignored staging until release; [reconciliation](reconciliation.json)
binds published copies to exact original bytes. Candidate Python is archived as
`.py.txt`, not installed source. Historical cases, thirteen forensic files,
903 RI rows, existing refs and 188 historical obligations remain preserved.
Historical unknown acknowledgments and wrapper exits remain unknown.

No production executable change is accepted, so the full protected gate was not
rerun. Physical/blob comparisons retain the prior protected identity. Supported
Ruff, strict typing, focused formatting, layout, JSON/native correlation, Intake,
links, whitespace and preservation checks are recorded in [validation](validation.json).
A broader formatter scan additionally found 28 unchanged historical test files;
they were not rewritten. Initial sandbox pytest temporary-directory denial and
pre-publication style cleanup are setup diagnostics, not worker test results.

This sample demonstrates an investigation-to-implementation transition and
behaviorally correct narrow code. It does **not** demonstrate completed maintenance
or effective repair. The immediate acceptance blocker was one style violation;
the operational limitation was spending seven of eight calls investigating before
the first edit, leaving no feedback-consuming opportunity. This is not repeated
semantic patch failure or evidence of a new framework defect.

Stop here. The highest-leverage next decision is a separately authorized controlled
comparison of a reasoning-enabled Qwen profile or another locally feasible coding
model on this **same delegated task and oracle**, measuring time to first proposal
and ability to finish validation/repair under the same finite envelope. The small
stable handoff should be retained. Do not add another generic Context/navigation
layer or silently finish this candidate with Codex. No comparison or follow-on
development is started by this report.

[Publication receipt](publication.json): ordinary non-force main publication was
verified at `260162248fa3882e88c1ed1f369277cdae974552`. All 69 experiment blobs
matched physical artifact bytes; all 1,191 protected inputs remained unchanged.
The following receipt-only closeout adds no implementation or execution authority.
