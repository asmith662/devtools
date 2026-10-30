# Decision-checkpoint-0001

**Tools affected the observed B-0035 response, but removing them did not produce
a fully sound implementation decision. Both smaller controls reached the correct
core decision, including the control with Tools available.** Recommend option B:
complete the small source call chain using existing Context selection before
another full maintenance attempt. No production change is justified or delivered.

## Authentication and protocol

Starting local/remote main was be8c973813104a65989ae106030a1c1b1d186034.
Accepted executable c2bc06f4f604c6ccb87279f6315bfa87b59ce6fa is an ancestor of
6fbd7d1a87307c9b585c9bce558259d7440d7182 and the starting main. Source/tests/apps/
scripts/configuration and all 1,188 physical protected inputs match that executable
validation. The prior protected result remains 3,899 passed, two optional skips,
100% production coverage; it was not rerun for this evidence-only assessment.

The [protocol](protocol.md) and final [freeze](freeze.json) were committed at
f86eb0dba93d2d1367bdd9507451b805b9dcaf2d before inference. A preflight-only draft
is retained as freeze-preflight-v0.json: review caught an objective replacement
that had not updated the initial message. No model entered on that draft. The
final prompts contain the actual checkpoint instructions, with identical source
and messages in each treatment pair. Only Tools differ. The independent control
and its expected result were selected and cross-checked before any live response.

The authenticated Qwen3.8-27B GGUF SHA-256 is
40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199, served as
qwen38-local on the existing pinned llama.cpp b10868 CUDA image. Full image,
artifact/profile/template identity and sampling are in the freeze. Thinking stayed
disabled; temperature 0.7, top_p 0.8, top_k 20, min_p 0, presence_penalty 1.5.
No setting was tuned or provider substituted.

Four independent stateless calls ran in fixed order. Each had 90 seconds, 4,096
output tokens, 28,160 measured input tokens and 32,768 serialized bytes; the
inference group had a 480-second outer bound. A advertised three existing scoped
search/read schemas; B used the valid portable tools=() representation. The
adapter has no portable explicit tool_choice=none setting. A's native requests
were retained as proposed actions and never dispatched. No generated answer was
included in any subsequent request. No edit, worker check, auxiliary inference,
download, service mutation, fallback or resampling occurred.

## Measurements and independent grades

| Cell | Bytes | Input/output tokens | Seconds | Response | Grade |
| --- | ---: | ---: | ---: | --- | --- |
| B-0035 A | 27,135 | 6,859 / 48 | 16.093334 | find_source, empty ordinary content | Relevant Tool request; no explicit engineering decision |
| B-0035 B | 25,582 | 6,274 / 579 | 36.761429 | Plain next-read hypothesis | Partial; qualified uncertainty plus unsupported assumptions |
| Control A | 12,186 | 3,140 / 945 | 57.651081 | Plain atomic-refusal decision | Correct core, minor caveats |
| Control B | 10,633 | 2,555 / 1,112 | 50.658936 | Plain atomic-refusal decision | Correct core, repair caveats |

Totals: 18,828 known input tokens, 2,684 output tokens and 161.164780 inference
seconds. Token measurement matched reported input for all cells. Cached and
reasoning usage remain unknown. Fixed order/cache effects limit latency comparison.
Provider raw finish reasons were tool_calls, stop, stop, stop; normalization matched
raw contents/calls. None ended at output limit. No evidence supports a provider
or normalization defect. Short output is not a measure of private reasoning.

### B-0035

A selected the mixed query `prepare repository metadata resources content_identity
byte_size editable prompt message objective`. It was relevant but did not identify
a particular missing contract or express an implementation hypothesis.

B correctly identified that __init__ initializes objective-only messages and
identified scope.snapshot.resources and the required metadata fields. It asked
for _index and a supposed metadata-construction helper. _index was actually absent
from the supplied source, so inspecting this invoked callee is a legitimate
bounded uncertainty check. However, the model inferred existing behavior from
acceptance-test assertions; assertions are requirements, not passing results.
Its suggested helper names are expressly speculative and not observed APIs.
Its later offset near 11506 is relevant to _index; its suggested 17325..20000
range is not. It did not produce a concrete design covering refresh/idempotence,
full accounting and the complete-inventory versus candidate-shortlist distinction.
This is partial source understanding, not a correct implementation plan and not
a fabricated execution receipt. No test success or source mutation was claimed.

All seven initial units were exact and continuously present for each single call.
They support recognition of the visible initialization gap. They do not close the
initialization call chain: _index and the body of prepare_navigation/task_entry
were omitted. Independent source review shows _index only builds the source index,
while prepare_navigation supplies incomplete candidates. Those facts were not all
visible to the model. Therefore the assessment does not establish failure despite
fully sufficient Context. A valid missing-evidence request must not be mistaken for
incapability just because the reviewer knows the omitted implementation.

### Smaller real engineering control

The control characterized Devtools' existing edit-admission contract using exact
replace_exact_text and admit_source_batch units. It asked about abcd->Q and
def->R on the same ASCII abcdef version, with valid witnesses/scope/budgets.
Independent interval arithmetic gives [0,4) intersect [3,6) = {3}; a pure actual
admission preflight also refused overlapping edits without modifying an authored
fixture. Neither reference conclusion was disclosed to the model.

Both responses correctly explained overlap at d, whole-batch refusal and the
need for a new coherent proposal. A voluntarily declined Tools. Its c/d slip is
self-corrected; dominant-newline wording is inaccurate and re-reading is not
universally necessary. B's early uniqueness diversion is corrected; hypothetical
QR is not a known intended result, and sequential operations require new source
and host admission. The central decisions pass, with these qualifications retained
in [independent claim review](review.json). This tests contract interpretation,
not implementation, scientific effectiveness or automatic repair competence.

## Architectural recommendation

Select **B: working-set revision**, through the trusted host's existing Agents
task/source assembly and Context/RI materialization. Supply the small initialization
and initial-message construction callee closure, especially _index and
prepare_navigation/task_entry. Do not supply a solution patch or invent a new
navigator. Before a full maintenance trial, require a grounded hypothesis or a
specific remaining missing obligation with that closure available.

The observed B-0035 contrast makes Tool availability/action incentives a credible
interaction hypothesis; it does not prove causality or justify mandatory planning
phases. The Tool-capable control answered directly, contradicting any universal
claim that automatic Tool choice prevents decisions. The current profile is a
plausible worker for narrow source-grounded contracts, but full B-0035 maintenance
remains unestablished. Task decomposition remains a reasonable later option if
source closure alone is insufficient; another model/profile is not the first
evidence-supported remedy. No proposed follow-up is implemented or authorized here.

## Integrity and publication

Raw provider response body bytes, actual request payloads, normalized responses,
native IDs and known usage are retained under [evidence](evidence/). HTTP framing
is not captured. Original earlier diagnostics had normalized records but no raw
HTTP body capture; no missing historical wire receipts are invented. New artifacts
were staged outside the protected Checkout until normal release. Canonical source
and index remained unchanged, and no Tool was executed by a model request.

Focused native/provider/Prompt and admission/repair regressions passed 253 tests.
Pairwise payload equality, literal and actual preflight, JSON, manifest, Intake,
layout, links, whitespace, ancestry and historical hashes are verified separately.
Earlier experiments, thirteen forensic files, 903 RI ledger rows, refs and 188
historical RI-version obligations are preserved. B-0035 and B-0043 stay open.
The [manifest](manifest.json) records exact bytes under scoped artifact attributes.
The retained runner.txt is the exact probe source, not an installed production
command or authorization to rerun this closed four-call assessment.
