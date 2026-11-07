# Reviewer-model comparison: decision and qualification limits

**Neither tested configuration is ready to become the autonomous acceptance reviewer.**
Current non-thinking Qwen has a demonstrated false rejection; enabling thinking
was costly and left the correct control unfinished even at 8,192 output tokens.
Local gpt-oss-20b is feasible on this GPU and substantially faster, and judged
both completed cases correctly. However, it failed native conclusion delivery,
reference admission and a server-native formatting check. It is the next model
to **qualify**, not a proven accuracy winner or an activated production reviewer.
The evidence does not isolate an intrinsic model-capacity limit.

Twenty-two genuine generations ran. No generation was replayed, no native
coding/review slot was used, and no source candidate was installed. The
[manifest](code-audit/reviewer-model-comparison-20261105/manifest.json),
[per-call index](code-audit/reviewer-model-comparison-20261105/calls.json) and
[scores](code-audit/reviewer-model-comparison-20261105/scores.json) preserve the
actual requests, received responses, missing-response failure, source reads,
model settings, timings, token measurements and negative outcomes.

## Frozen cases and model-facing contract

Canonical main/remote started clean at `26c07ef1b26436dd10dc50c752cd63a6619c7bba`.
The [prior result](reviewer-evidence-verification-results.md) remains unchanged:
Qwen accurately copied behavioral observations but accepted a defective candidate.
Those requests used thinking disabled. The new `inspect_public_check` and
`reopen_working_note` names remain deterministically tested but not live-qualified;
this comparison uses the permitted native `read_source` and unchanged
`submit_review_proposal` schemas.

C01 is the exact archived defective P3 candidate, SHA256
`ea9619b09ebaca244b358179fecc7c952be37e07edac66ba5171f19b3af3b119`.
C02 is the published protected-validated Codex repair `7be3b522`, SHA256
`b2d08c895747382345f9f276dda3062a74a6157aab99f7e919459aee2772f92f`;
its current Git source blob is identical. Each conversation receives the original
public task, baseline, candidate, diff and authenticated public check. The model
never receives the independent recommendation labels, private oracle or coding
worker's private conclusions. No acceptance/custody record is fabricated.
Factual judgment is scored independently from full native admission.

The trusted fixed probe extracts only the regex literal through AST and applies
its `text` group followed by `strip`; candidate modules are never imported or
executed. A frozen assertion wrapper adds expected values, per-case pass/fail
and exit 1 on mismatch through existing `FixedCheckTool` and review-observation
owners. Both runs have known returned effects: C01 fails, C02 passes.

| Public input | Expected title | C01 actual | C02 actual |
| --- | --- | --- | --- |
| `# C#` | `C#` | `C#` | `C#` |
| `# C# #` | `C#` | `C#` | `C#` |
| `# Title #` | `Title` | `Title` | `Title` |
| `# ##` | empty | `##` | empty |

No new shared verification interface is necessary. The existing owners already
support actual/expected assertions and authenticated failure. The earlier probe's
exit 0 only meant observation succeeded. Prospective checks with public expected
values should assert them. Native acceptance-review entry already refuses known
public failures, so a reviewer cannot override them with an opinion. Four fixed
producer examples are not comprehensive Markdown acceptance.

All requests use explicit system/user roles, actual OpenAI-compatible Tools and
correlated native IDs. Final synthesis advertises only the proposal Tool.
`response_format` is omitted; there is no forced `tool_choice`. Qwen sends
`chat_template_kwargs.enable_thinking` false/true. Rendered prefixes independently
confirm closed/open thinking blocks; received thinking responses contain real
`reasoning_content`. Installed llama.cpp build 10868 / `304665fe7` enables Jinja
by default. Absence of an explicit launch flag is not evidence of incompatibility.

## Actual results

The initial freeze is
`17942161008a09b9f1084d96f11e3834bda36f01a04e6e215bec54d00921f284`:
two cases, thinking off/on, two repetitions, at most two calls per conversation,
2,048 output tokens including reasoning, 16,384 input tokens and 120 seconds per
call. Twelve calls ran. Within matched cases only the thinking flag changes;
source, instructions, Tools, sampling and budgets remain fixed.

The larger comparison uses the same cases, evidence, instructions and grader,
with 8,192 output tokens and 600 seconds per call. Captured Harmony rendering
sets gpt-oss native reasoning to medium. Qwen has one conversation per
case/flag; gpt-oss plans two per case. The
[frozen correspondence](code-audit/reviewer-model-comparison-20261105/frozen-correspondence.json)
authenticates all predecessor bytes, corrected drivers and unchanged initial wire
requests. Qwen executed under freeze `9aa7b08b…`; the prospectively corrected
alternate freeze is `65184dc248a9222ade1e9dc81116f0c7b7a1c060abab884c883ef6ade71305b4`.

| Configuration | Completed factual judgments | Incorrect findings / unfinished cases | Native final proposals / strict admissions |
| --- | --- | --- | --- |
| Qwen off, 2,048 | 3/4 correct | One invented blocking defect in correct control | 4 / 3, including the false rejection |
| Qwen on, 2,048 | None | All four truncated at exactly 2,048 tokens | 0 / 0 |
| Qwen off, 8,192 | 2/2 correct | No false blocking finding in these two | 2 / 0 |
| Qwen on, 8,192 | Correct rejection of C01 | C02 truncated at 8,192; no judgment | 1 / 0 |
| gpt-oss native, 8,192 | Both completed cases correct | Repeated C01 hit native parser/API failure; repeated C02 not entered | 1 / 0; other completed judgment was prose JSON |

Qwen's initial false rejection claims `# C#  ##` returns `C#  ##`; a separate
**post-hoc host-only** literal-regex check confirms baseline, C01 and C02 all
return `C#`. This diagnoses the finding without changing frozen scoring or
providing feedback to later actors. Strict admission did not catch that false
claim. Conversely, correct factual judgments with unavailable/misnamed references
were refused; no citation or conclusion validator was relaxed.

The larger non-thinking control response used 6,439 output tokens and included
18,572 characters of analytical prose plus a native proposal. Thus disabling the
thinking channel does not guarantee short output or absence of textual reasoning.
The thinking rejection used 7,857 tokens and delivered a native proposal, while
thinking on the correct control exhausted 8,192 without one. More output budget
was not a reliable reviewer-completion solution. The small unseeded samples do
not establish that the ceiling itself caused improved factual accuracy.

| Configuration | Calls | Measured input tokens | API-reported output tokens | Sum of measured call time |
| --- | ---: | ---: | ---: | ---: |
| Qwen off, 2,048 | 8 | 74,837 | 4,178 | 281.52 s |
| Qwen on, 2,048 | 4 | 33,809 | 8,192 | 404.31 s |
| Qwen off, 8,192 | 3 | 27,076 | 7,356 | 343.05 s |
| Qwen on, 8,192 | 2 | 16,906 | 16,049 | 702.31 s |
| gpt-oss native | 5 | 41,355 | 5,186 across four returned responses | 115.69 s |

For gpt-oss's failed fifth call, API usage is unavailable. Server logs separately
report 6,713 prompt and 4,944 decoded tokens, 49.35 seconds generation and 51.21
seconds total. Those counters are retained separately rather than fabricated as
an API response. The completed control took 34.57 seconds and the defective case
28.30 seconds. Startup/restoration costs are additional. Native sampling differs:
Qwen defaults temperature 1.0/top_k 20; gpt-oss defaults temperature 0.8/top_k 40;
both use approximately top_p 0.95/min_p 0.05 and an unset/random seed. No sampling
preset was silently added. These are whole-configuration comparisons, not an
isolated estimate of weight quality or an optimal sampling study.

## Delivery failures and honest recovery

A Codex-authored prospective correlation correction mistakenly removed the ID
set without initializing it per conversation. Four higher-budget Qwen responses
were actually received and their model entries completed, but the host raised
`NameError` before any source Tool dispatch. The faulty driver and results remain
unchanged. Existing response records were reconstructed with exact JSON round
trips, their native IDs retained, and existing acquisition processed the valid
read once. Only one already reserved final call was then needed, under the
**same grant**: five total Qwen generations, zero replay or budget renewal.
Independent first phases consequently preceded final synthesis; this timing-order
deviation prevents treating the run as a pristine latency experiment. The fix
was AST-checked and frozen before any gpt-oss generation.

GPT's first control delivered a native source read and acceptance proposal, but
cited unavailable references. Its defective-case repetition read the relevant
source and rejected the real empty-heading bug as prose JSON, with no native
final Tool call and invalid finding-kind/reference fields. This is a correct
code judgment, not an admitted structured review. Prose was never executed or
converted into a Tool submission.

The next gpt-oss call was consumed, then failed before HTTP response capture.
Complete server logs show `common_chat_peg_parse` rejecting
`<|channel|>final <|constrain|>submit_review_proposal…` with a
`peg-native` formatting error 500. The client reported an invalid HTTP status
line. The server remained healthy/idle, with no reported OOM. The original
unknown/failed grant completion is immutable; the packet stopped without retry
and its last planned case was not entered.

The server-logged unadmitted JSON finds the real `# ##` defect, but also makes a
false claim about emptying `# #`, misdescribes attached-suffix behavior, omits the
subject identity and uses invalid finding kinds. A separately labeled post-hoc
check confirms C01 actually returns `#` for `# #`, while baseline/C02 return empty.
This negative evidence remains visible; the parser-failed generation is not a
successful review or a clean accuracy observation. Failed-call raw HTTP headers,
body and complete reasoning were not captured; all available unparsed server
output and timing evidence are preserved. No missing response is reconstructed.

A concrete adapter defect was also reproduced **offline**, without inference:
`_parse_http_headers` accepts `200 OK` but rejects valid `500 Internal Server Error`
and `404 Not Found` because it requires exactly three whitespace-separated
words. HTTP reason phrases may contain spaces or be absent.
[RFC 9112 section 4](https://www.rfc-editor.org/rfc/rfc9112.html#section-4).
This would mask an ordinary 500; the failed call's exact raw status line remains
unobserved. Fixing this parser will improve error attribution, not make malformed
native output valid. No speculative parser/server correction was implemented here.

## Hardware, enrollment and role separation

The GPU is an RTX 4090 **Laptop**, 16,376 MiB. Qwen uses the unchanged UD-IQ4_XS
artifact, 64K Context, q4_0 K/V, Flash Attention and one slot. Its sampled GPU use
was 14,742 MiB. gpt-oss uses the already installed native MXFP4 artifact,
`ggml-org/gpt-oss-20b-GGUF` revision `15dcfc7e7c608c6161507211ed43c5b590801b4b`,
12,109,566,624 bytes, SHA256
`27cd6c432c7672cb812a92f611cf3ba7bbc35928262bb1e1253ff4ee6ae35901`.
Full streaming hashes matched at preflight and serving entry; nothing was downloaded.

The same pinned llama.cpp image served gpt-oss at 32K Context, f16 K/V, all GPU
layers requested, Flash Attention and one slot. Effective Context/alias/slots,
read-only mount, image, launch arguments, health and idle state were authenticated.
GPU samples were 12,124–12,144 MiB. Host RAM is 31.73 GiB and was under severe
pressure: gpt-oss's lowest sampled available physical RAM was about 7.4 MiB.
These are before/after samples, not peaks or robust capacity guarantees. GPU fit
is demonstrated; host-memory headroom needs qualification. Concurrent residency
was not attempted. The [earlier genuine compatibility run](../../experiments/alternative_b0035/REPORT.md)
provides historical support, not current authority.

OpenAI documents function calling, configurable reasoning and native Harmony
channels for gpt-oss; llama.cpp documents native MXFP4 local support.
[Model specification](https://developers.openai.com/api/docs/models/gpt-oss-20b),
[Harmony format](https://developers.openai.com/cookbook/articles/openai-harmony),
[llama.cpp guide](https://github.com/ggml-org/llama.cpp/discussions/15396).
Actual local failures take precedence over general support claims.

The actual operator response approved scope `9722f98d…`, preserved verbatim in
[enrollment evidence](code-audit/reviewer-model-enrollment-20261105.json).
The narrowly amended [existing authority owner](../development/reviewer-provider-enrollment.md)
was protected-validated and genuinely activated as
`4fe32fc6bd33762ce7b166fc8031e16a7bcd7584c1d9c65676a280983e0b78a9`.
Fresh local grants were automatic, with **zero per-run operator approvals**.
The native global Qwen provider, coding budgets/attempts and Integration gates
remain unchanged. Alternate native acceptance-review authority was not enrolled.

The separately approved sequential serving scope paused the authenticated idle
Qwen container, loaded only the owned pinned gpt-oss profile, removed that owned
service and restored the **same** Qwen container `d8be9569…` with identical image,
mounts, command and 64K configuration, verified healthy/idle. Inspector, the
learning worktree, preexisting source-grounding work, historical grants and
failed episodes were preserved. No cache or standing historical record was deleted.

Reviewer role instructions, Tools, conversation, source disclosures and working
notes remain host-owned through existing NativeReviewer/Context episode records.
A serving swap changes inference resources; it does not transfer coder conclusions
or make KV cache into role memory. Reconstruct each role's own authorized Context
and qualify the selected profile before entry. No scheduler, model-specific Agent
class, memory database or delegation system was added.

## Qualification decision and next bounded increment

Keep acceptance fail-closed. Do not promote either tested configuration from this
small public diagnostic. Prioritize gpt-oss for the next reviewer qualification
because of demonstrated GPU fit and lower measured inference cost; current data
does **not** establish factual superiority. Its native Harmony/Tool delivery,
reference identity and memory headroom must qualify before production adoption.
Qwen thinking at the tested limits is not a productive default. Further Qwen
prompt/memory expansion is not supported by this comparison.

The smallest next production correction is in the existing llama.cpp HTTP parser:
parse numeric status independently of a multiword/optional reason phrase and
retain bounded server-error evidence. Keep invalid framing rejected and propagate
real 500 errors; do not normalize malformed model output into successful Tools.
Then perform a small prospective native-format qualification using the enrolled
model/profile and intact strict reference rules. Any image/profile expansion
requires its actual reusable enrollment decision. Native reviewer selection
retains its separate authority; local calibration grants cannot install it.

The [candidate playbook v7](code-audit/reviewer-model-comparison-20261105/candidate-playbook-v7.json)
remains inactive, recording measurements, failures and conditions rather than
universal memory. Longer-term role-scoped episode retrieval and reviewed
procedural-memory promotion remain separate work after reviewer qualification.

## Validation and publication

Owner implementation: `d2a3b3029ce996cabb9ec6a6bf7b66695c289676`, non-force pushed
and synchronized before the qualified experiment. Development tests passed 63
cases; final profile regressions passed 12. Maintained Ruff/format (746 files),
strict default mypy (646 files), explicit owner mypy and layout passed. Broad Ruff
also traversed retained historical experiments and reported unrelated failures;
those files were not reformatted.

The final committed-input protected gate passed **4,468 tests, two opt-in skips,
100% production branch coverage**, complete unchanged inputs, in 4,833.29 seconds
under a two-hour deadline. A tool-server restart terminated an earlier incomplete
run at 1,290 seconds; its intent/progress remain separate. The fresh recovered
run was detached from the interactive session, not treated as reuse of a partial
pass. [Validation receipts](code-audit/reviewer-model-comparison-20261105/validation.json).
No executable production inputs changed after that pass, so final evidence and
documentation publication use bounded integrity/layout/link/Git checks without
another comprehensive run.
