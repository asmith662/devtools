# P3 reviewer finalization: bounded follow-up

Eight explicitly approved calls, executed against `main` at
`262d357e2604ff13db13458f1c89b8713952ae08` on 2026-11-05 UTC, separate output
completion from factual review. **A reliable conclusion contract was not
established.** Concise instructions and a larger reservation each resolve the
observed truncation, but complete delivery still frequently contains false claims.
Only **2/8** responses satisfy the complete factual contract. No production code,
budget, parser, standing authority or service configuration was changed.

## Authenticated starting result and production boundary

The [15-call calibration](llm-harness-calibration-results.md) is preserved.
Its exact P3-json and P3-call bodies both ended `length` at 384 output tokens.
P3-json produced prose; P3-call produced truncated native arguments. The latter
correctly selected rejection in its visible prefix but claimed hashes were
stripped while also reporting the supplied nonempty title `##`.

The existing production owners already separate transport from trusted review:
[delivery](../../scripts/backlog/native/review/delivery.py) requires exact subject,
candidate, source, request/settings and Tool definitions, a fresh single proposal
ID and normal `TOOL_CALL` termination; [proposal parsing](../../scripts/backlog/native/review/proposal.py)
then checks grounded reference names and the conclusion shape. This does not
prove a cited causal statement is true. The follow-up reuses pure parsers without
manufacturing a native review event or host acceptance.

[Actor construction](../../scripts/backlog/native/review/actor.py) uses
`ModelSettings(**config["settings"])`: the reservation is per-review configuration,
with a general 1–8,192-token guard. The active standing policy caps it at **2,048**;
all three archived B-0052 review configurations also reserved 2,048. Consequently
the original experimental 384-token ceiling is not a production default.
The [environment evidence](code-audit/llm-harness-p3-followup-20261105/environment.json)
retains those settings and source identities. The policy still does not authorize
generic calibration; a separate actual operator approval covered this packet.

## Frozen comparison

The [plan](code-audit/llm-harness-p3-followup-20261105/plan.json) and
[requests](code-audit/llm-harness-p3-followup-20261105/requests.json) were frozen
before any new generation. Approval scope was
`5f13e14200bb7e79b4fbacab350202d3a4fad1f4a9635e54ce598c0026f0ed24`;
plan SHA256 was
`0a836352b060ae2881173dc4043b4a6dd5d0a583dde5bf7daf32ffd229b6a986`;
request-set SHA256 was
`46f5d6a03e0f57539dd7c1b1a8bf7156b06fb0dd3d43ef63ced7d87826c4516a`.
The [authorization receipt](code-audit/llm-harness-p3-followup-20261105/authorization.json)
records the actual `+approve`; the prior fifteen-call approval was not reused.

The factorial design is original/concise system instruction × 384/2,048 output
ceiling × two repetitions. The concise variant appends the exact frozen directive:
finalize with one native proposal, aim below 300 generated tokens, use short
essential findings, complete required fields, omit a source walkthrough and check
factual/causal claims. It supplies no expected verdict or replacement code.
The original system text remains intact. Prompts within each instruction variant
are identical across ceilings; only `max_tokens` changes. No new model-visible
cell labels or output-budget numbers were introduced. Original/384 wire bytes
exactly match the published P3-call request.

The first block runs original/384, concise/384, concise/2,048, original/2,048;
the second reverses that order. There are four unique request bodies, each used
twice. The typed adapter exposes no seed, so these are repeated matched conditions,
not common-seed pairs. P3-json is not repeated: native delivery is held fixed.

Task, candidate, public counterexample, evidence, obligations, native Tool schema,
model, template and sampling remain fixed. The same `qwen38-local` model serves at
localhost:8080, GGUF SHA256 `40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`,
image SHA256 `7625abb46c6bb8357e214f949b409a152c0944228e5a653fbab112f98ad2de7e`,
template SHA256 `12827f24b742ea4e80cdc12dbcf9622227056b9f797252a3149263d4f9aaadce`.
The persistent 64K service, Jinja template, q4_0 K/V caches and inherited sampling
are unchanged. Thinking is false; neither `tool_choice` nor `response_format` is
injected. No native WorkCycle attempt or actual Tool execution occurs.

Approved maxima were eight generations, 8,192 input tokens each, 2,048 output
tokens per call and 9,728 total, 120 seconds per call, 1,020 seconds wall,
2 MiB capture and 65,536 raw response bytes per call, with zero retries. All
calls returned within those limits. No inference followed this packet.

## All eight actual results

T = native proposal delivery; S = complete schema **and normal termination**;
I = exact subject/candidate identities; F = grounded, noncontradictory findings;
R = parsed correct rejection. `?` means unavailable from incomplete JSON.
Both obligations and citations are required separately; all seven parseable
objects include them. All eight remain within scope with zero Tool effects.

| Instructions / ceiling / repetition | Input/output tokens | Seconds | T/S/I/F/R | Result |
| --- | --- | --- | --- | --- |
| Original / 384 / 1 | 3,933 / 384 | 23.987 | 1/0/1/0/1 | `length`; complete arguments, false causal claim |
| Concise / 384 / 1 | 4,061 / 352 | 20.687 | 1/1/1/0/1 | Complete; internally contradictory capture explanation |
| Concise / 2,048 / 1 | 4,061 / 408 | 17.719 | 1/1/1/1/1 | Complete, grounded rejection |
| Original / 2,048 / 1 | 3,933 / 597 | 25.997 | 1/1/1/0/1 | Complete; even an empty title falsely called a failure |
| Original / 2,048 / 2 | 3,933 / 724 | 30.994 | 1/1/1/0/1 | Complete; false additional `# C# #` defect |
| Concise / 2,048 / 2 | 4,061 / 662 | 28.967 | 1/1/1/0/1 | Complete; false additional `# Title #` defect |
| Concise / 384 / 2 | 4,061 / 325 | 13.790 | 1/1/1/1/1 | Complete, grounded rejection |
| Original / 384 / 2 | 3,933 / 384 | 17.096 | 1/0/?/0/? | `length`; malformed JSON, visible contradictory reasoning |

| Condition | Delivery-admitted | Factually valid complete reviews | Output tokens, repetitions 1 / 2 |
| --- | --- | --- | --- |
| Original / 384 | 0/2 | 0/2 | 384 / 384 |
| Concise / 384 | 2/2 | 1/2 | 352 / 325 |
| Original / 2,048 | 2/2 | 0/2 | 597 / 724 |
| Concise / 2,048 | 2/2 | 1/2 | 408 / 662 |

All eight raw HTTP responses were 200 with a native proposal envelope and fresh
ID. Seven normalized through the adapter; the final original/384 response raised
`LlamaCppResponseError: Model Tool call arguments must be valid JSON.` The first
original/384 response has complete argument JSON but terminates `length`, so the
unchanged production delivery contract would still refuse it. Valid JSON alone
therefore cannot establish delivery admission, much less correct review.

Generation-loop wall time was **179.627 seconds**, including 179.237 seconds in
adapter calls. Usage was **31,976 input and 3,836 output tokens**; raw server
usage reports 27,887 cached input tokens. All input measurements match returned
prompt usage; peak input is 4,061. Capture used 316,755 bytes. No input Context
projection or compaction occurred. Unequal prefix caching means the latency
figures are observations, not a causal performance ranking.

## Factual grading and negative findings

The prospective rubric requires every substantive summary, finding and causal
assertion to agree with the supplied source/case. It does not count a correct
`reject` string or named references as proof. The
[per-claim scores](code-audit/llm-harness-p3-followup-20261105/scores.json) preserve
the claim, verdict and reason for every failure.

- Concise/384/1 says the text capture is empty and the closing branch consumes
  `##`, yet stripping yields `##`. That explanation is internally inconsistent:
  stripping an empty capture cannot yield hashes.
- Original/2,048/1 states that returning the required empty title would also fail,
  then suggests literal-hash semantics inconsistent with the task.
- Original/2,048/2 invents a defect for `# C# #`; concise/2,048/2 invents one for
  `# Title #`. The frozen candidate captures `C#` and `Title`, respectively.
- The first original/384 response claims that one hash is consumed as a closing
  suffix while a later hash remains in title text; this contradicts the actual
  complete `##` capture. The final truncated response visibly invents an empty
  capture and a second space; its full verdict/identities remain unadmitted.

[Trusted host counterchecks](code-audit/llm-harness-p3-followup-20261105/host-claim-checks.json)
extract the regex string literal from the frozen candidate with AST literal
inspection and apply only regex matching plus the source's `.group("text").strip()`.
They import or execute no candidate module. `# ##` captures `##`; `# C# #`
captures `C#`; `# Title #` captures `Title`. These are post-response checks of
model claims under the frozen factual rubric, **not new hidden acceptance or
independent holdouts**. Two host-only receipt/extraction mistakes were corrected
and recorded; neither involved inference, source mutation or changed grading.

No response is recoverable by a single complete JSON-fence normalization. Partial
JSON was not repaired and prose was not promoted to Tools. Four of the six
delivery-admitted conclusions still fail factual review. The two successful
conclusions stay grounded in the supplied mismatch rather than add false defects.

## Decision and smallest next correction

The original P3 failure was **delivery-limited at 384 tokens and also exposed
reasoning/evidence-use failures**. At the already-supported 2,048-token ceiling,
completion succeeds in all four calls; factual correctness succeeds in only one.
Increasing the ceiling is sufficient for this fixture's delivery, not its review
quality. There is **no justified production token increase or parser relaxation**.

Concise instructions improve observed low-budget completion, but only one of two
reviews is factual at either ceiling; all four exceed the soft 300-token target.
Neither variant qualifies as a reliable production conclusion contract. Two
repetitions on the same disclosed public case cannot establish reliability or an
optimal profile. A longer answer is not evidence of better reasoning.

The single smallest **candidate** production correction is confined to the
existing finalization instruction: prioritize a concise observed mismatch and
exact evidence, omit unverified causal explanations/extra defects, and state
specific uncertainty where necessary. The tested addendum is not promoted: it
already asks for factual checking and still produces false claims. The remaining
blocker is source-grounded reviewer reasoning, not serialization. No executable
change is justified as a proven fix by this packet, and none is implemented here.

[Candidate playbook v3](code-audit/llm-harness-p3-followup-20261105/candidate-playbook-v3.json)
records the settings, exact instructions, measurements, negative results and
confidence; v1/v2 and their manifests remain unchanged. It is not activated policy
or universal memory. Any further live qualification needs its own finite scope.

The next prioritized capability remains **source-grounded working notes and
role-specific memory through existing Context and Repository Intelligence
owners**. Retained facts/inferences should cite exact source versions/ranges or
public cases and retain unknowns, with role-scoped retrieval. No memory database,
agent hierarchy, new backlog task or implementation is introduced here.

## Preservation and validation

The [manifest](code-audit/llm-harness-p3-followup-20261105/manifest.json) binds the
frozen inputs, authorization, environment, raw
[calls](code-audit/llm-harness-p3-followup-20261105/calls.json), scores and local
driver invocation record. Exact request bodies are deduplicated by hash without
changing bytes; each actual call links its body and preserves its raw response,
native IDs, normalization/admission error, timing and usage. Original local
receipts remain in `.local/llm-harness-p3-followup/`.

[Validation](code-audit/llm-harness-p3-followup-20261105/validation.json) covers
frozen/evidence hashes, four-request/eight-call consistency, raw byte round trips,
score consistency, local links, layout and Git integrity. No protected suite is
run for this evidence-only publication. Inspector, provider configuration,
standing authority, historical attempts, B-0053 closure and existing untracked
source-grounding artifacts are preserved.
