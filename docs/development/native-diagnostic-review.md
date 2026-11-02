# Governed diagnostic review of blocked native candidates

`WorkCycle.native.diagnostic_reviewer` independently investigates an authenticated
unsuccessful native candidate. It is a second explicit administrative purpose of
the existing bounded [review operation](native-independent-review.md), not a new
Agent hierarchy, coding loop, integration pathway or Evidence database.

Acceptance review still requires a qualified `REVIEW_CANDIDATE`, successful public
and private acceptance, known effects and released custody. Its gate, original
schemas, manual decision path and integration readers are unchanged. Diagnostic
v1 accepts a released **BLOCKED native result** with an authenticated candidate
archive. It produces attributed findings, not an acceptance recommendation.
Successful candidates and legacy Qwen results are outside this historical reader.

## Operator entry and separate authority

```text
uv run python -m scripts.backlog native-diagnostic-prepare B-0050 --archive <exact-candidate.json> --policy <review-policy.json>
uv run python -m scripts.backlog native-diagnostic-authorize B-0050 --reference <operator-decision> --expires <ISO-time>
uv run python -m scripts.backlog native-diagnostic-proposal B-0050
```

A trusted configured host injects a real supported ModelInteraction into
`await cycle.native.diagnostic_reviewer.execute(item, interaction=model,
profile=approved_profile, authorize=current_host_decision)`. Preparation does not
dispatch. The existing default-No confirmation applies to authorization; a fresh
grant and current host dispatch consent bind the actual subject, actor/session,
profile, source/Tool scope, finite budgets, principal and expiry. Original coding
grants and acceptance-review grants confer no diagnostic authority.

There is one non-replayable `diagnostic-reviewer/` slot under the existing native
work-item folder. It does not reuse or replace the consumed coding slot or the
acceptance `reviewer/` slot. Prospective records are
`backlog-native-diagnostic-{subject,authorization,dispatch,proposal}-v1`, written by
the existing immutable WorkCycle writer. Observations reuse
`backlog-native-observation-v1` and bounded native Capture. An intent precedes
entry; uncertain completion or failed proposal persistence never authorizes replay.

The policy reuses the existing review actor's closed fields and ceilings. A fresh
session, distinct coder/reviewer actor and host independence attestations remain
mandatory. Same model weights and different labels do not prove judgment diversity.
No paid fallback, service switch or automatic model retry follows from failure.

## Exact historical evidence and current Context

The host explicitly supplies a canonical resource containing the exact escaped
`source_text` and `native_patch_text`, with their recorded hashes. B-0050 uses
`docs/research/code-audit/live-native64-20261101/unaccepted-candidate.json`.
Display `.py.txt`/`.diff.txt` copies may undergo Git newline normalization and are
not candidate authority. The reader verifies the archived UTF-8 bytes against the
terminal candidate hash, the patch against an exact baseline-to-candidate diff,
and original native source/patch bytes when present. Missing local duplicate
copies are disclosed; the exact content-authenticated archive remains required.

The reader authenticates original assignment/packet/baseline identity, historical
authorization/dispatch/result/execution bindings, observation hashes and the
Checkout release. Historical expiry does not erase the observation or create new
authority. No historical result is converted into a passing candidate. Missing or
tampered core authentication refuses preparation, rather than manufacturing facts.

The subject discloses original task/obligations, baseline and Git identity,
candidate/diff, actual edit intent/completion facts, public check history including
failures/truncation qualifications, terminal disposition, custody and acknowledged
or unresolved effects. Missing historical test materializations and unselected or
changed current inputs receive explicit status. Public success is limited evidence.
Private acceptance may be failed or not executed; neither is promoted to a pass.

Private implementation, counterexamples, expected results, private diagnostic
output, host controls and worker reasoning/conversation are withheld. Private
acceptance exposes only qualified outcome, exit status, elapsed time and input
currentness, when executed. The original result identity also binds withheld data.
The reviewer receives no reference repair. A failed outcome alone does not reveal
the hidden cause. Diagnostic findings must not be scored as blind discovery when
their facts were already disclosed in public evidence.

Current source is independently selected and identity-bound under fresh read-only
authority. It may include relevant dependencies beyond the old coding inventory.
It is not silently relabeled as historical source. The candidate is never installed
for review. Source changes after preparation invalidate the subject; an active
Checkout owner blocks entry. Absent historical temporary tests need not be recreated
or added to original authority merely to read current dependencies.

The operation reuses SourceScope, SourceSearchIndex, scoped source/navigation Tools,
Context range materialization and native call correlation. It advertises only
`read_source`, `find_source` and `read_source_unit`. Search results are versioned
metadata, not disclosed source or proof that a region was assessed. Exact reads
retain current provenance, physical boundaries and source identities. Each bounded
source/navigation operation consumes the existing read allowance; duplicate native
call identities are refused. Only one Tool operation is admitted per response.
No edits, checks, arbitrary shell or Git Tools exist.

## Budget-aware diagnostic continuation

New diagnostic subjects bind `continuation` with schema
`native-diagnostic-finalization-v1` and one reserved model call. This prospective
policy is part of the exact approved subject; earlier subjects without it retain
their recorded execution policy. Existing acceptance review is unchanged.

Before every model entry, the existing reviewer supplies and captures a
`native-diagnostic-budget-v1` view: used/remaining model calls (remaining includes
the impending call), completed/remaining acquisitions, current authorized resource
identities, and whether source Tools are available. Complete historical baseline
and candidate text is already in the subject and needs no confirming reread.
Matching current baseline identity establishes equivalence to that baseline;
it does not establish equivalence to the uninstalled candidate.

The view is nested under `budget` in a standard
`backlog-native-observation-v1` envelope; its own schema never replaces the
observation schema. The first B-0051 live records exposed that collision before
this correction. Those original records retain their actual budget-view schema
and hashes; they are qualified historical evidence, not rewritten envelopes.

The last approved call is reserved for synthesis. Exhausting acquisitions earlier
also selects synthesis immediately. Synthesis advertises no source Tools and asks
for a structured diagnosis or an explicit insufficient-evidence conclusion. A
single-call approval therefore permits synthesis only. No extra call is added,
and the host never invents a conclusion. Authority expiry, changed evidence,
Context/capture capacity, timeout or unusable output can still prevent completion.

The latest host budget view is active Context metadata, not source evidence or
authority. Prior requests, budget views and Tool disclosures remain in the
immutable captured history. This does not introduce lossy compaction or turn
budget metadata into a source witness.

Diagnostic refusals distinguish `REVIEW_TOOL_BATCH_LIMIT` (multiple operations
in one response), `REVIEW_ACQUISITION_BUDGET_EXHAUSTED` (total allowance consumed),
and `REVIEW_FINALIZATION_TOOLS_UNAVAILABLE` (reserved synthesis). Pre-entry refused
calls retain native call identities and `tool_effect_entered: false`. Operations
that entered the Tool runner keep their original intent/completion/uncertainty
semantics. No automatic retry follows a refusal or uncertain effect.

## Findings and trusted evaluation

### Structured response delivery

New diagnostic subjects additionally bind `delivery` with schema
`native-diagnostic-response-delivery-v1` and rule `single-json-fence-v1`.
It is part of the subject approved by the host. Historical subjects without
this marker keep strict raw-content parsing; unknown delivery rules are refused.
Acceptance review's parsing, eligibility and authority are unchanged.

The llama.cpp adapter already offers provider-owned
`LlamaCppRequestSettings(response_format="json_object")`. Portable ModelSettings
has no structured-output setting or capability negotiation, and the closed native
review policy admits only its existing output-token/thinking settings. This
increment does not inject an unapproved provider extension, add schema generation,
or claim live qualification of provider-enforced JSON. It uses a narrow,
provider-neutral presentation boundary in the diagnostic owner instead.

The stages remain separate:

1. ModelInteraction returns its ordinary response; Capture retains the complete
   request and original response, including content, termination and reported usage.
2. Source, output limits, response capacity and Tool permissions are checked before
   any presentation admission. A Tool request during synthesis is still refused.
3. New diagnostic deliveries optionally unwrap exactly one complete triple-backtick
   fence, unlabelled or labelled lowercase `json`. Only surrounding ASCII spaces,
   tabs, CR/LF and opening-line horizontal whitespace are allowed; separators may
   be LF or CRLF. The closing fence must be exact and occupy its own line.
   Bare JSON passes unchanged. No JSON substring is searched for or repaired.
4. The complete candidate payload goes through the unchanged strict JSON/object
   parser and closed diagnostic conclusion validator. Prose, additional blocks,
   unsupported labels, malformed fences/JSON, extra or missing fields, duplicate
   members, wrong candidate identity and invalid claims/references remain refused.
5. Factual claims still require independent host evaluation. A valid schema does
   not certify a source location or make an inferred defect true.
6. The existing immutable proposal writer determines the final durable
   `proposed`/`blocked` disposition. A diagnostic proposal remains advisory and
   cannot enter acceptance or integration.

Raw content is never rewritten. New returned-response observations separately
retain its UTF-8 SHA256. A `review-response-delivery` observation nests its facts
under `delivery` inside the standard observation envelope: complete request and
response identities, raw-content hash, exact candidate payload and its UTF-8 hash,
normalization rule, strict-validation outcome and validated-advisory/refused status.
Wrapper refusal records no payload hash; parse/schema refusal retains the actual
candidate payload and failure. These are validation facts, not host acceptance.
If Capture or final proposal persistence fails, the dispatch claim remains;
no parsed payload authorizes replay or manufactures a durable successful result.

The semantic-compaction `summary_payload` helper has a deliberately different
summary-specific contract (labelled JSON only and stricter content exclusions).
It and the filesystem Markdown heading reader are unchanged. Diagnostic delivery
does not introduce a general Markdown parser, JSON-repair library or new
structured-output framework.

The exact [B-0051 response](../research/diagnostic-completion.md) now has a maintained
derived deterministic regression. Its original native proposal remains BLOCKED
with a null conclusion and its original `JSONDecodeError`. No model is redispatched
and the known incorrect claims remain incorrect after presentation admission.

The closed model conclusion uses `schema: native-diagnostic-conclusion-v1`,
`scope: diagnostic-only`, exact `candidate_sha256`, `disposition` (`findings`,
`insufficient-evidence`, `refused`), `summary`, `evidence`, `findings`,
`outstanding` and `requests`. Each finding labels its claim `observed`, `inference`
or `uncertain`, with supporting evidence references and optional attributed
physical-line locations. Locations and labels are model claims; syntactic and
reference validation is not host verification that they are correct.

Malformed output, invalid references/identity, output limits, unauthorized Tools,
exhaustion, capture failure and provider uncertainty produce a blocked proposal or
propagated persistence failure. A truthful inability/refusal is representable and
does not force a fictitious defect. Unsupported semantic findings may be retained
as attributed claims for independent host evaluation, not certified as truth.

There is no diagnostic acceptance decision. `admit` and `decide` explicitly refuse
this purpose. Native integration readers still require their original native
review/result schemas and acceptance gate. “Approved” in model prose cannot change
the blocked result, issue an install grant or authorize publication/closeout.

The trusted supervisor records usefulness, unsupported/incorrect claims and blind
discovery separately, bound to the exact proposal. That evaluation is evidence,
not native candidate acceptance. Suggested validation or engineering work returns
to the supervisor and requires its own authority; no review-driven repair loop is
launched. B-0043 and the original failed tasks remain open.

The B-0051 sampler-setting gap remains recorded in its
[original outcome](../research/native-scope-followup.md). No sampler pass-through,
server-default change or attribution of failure to temperature is introduced here.

The [first blind operational measurement](../research/native-diagnostic-review.md)
completed three real model calls but exhausted two acquisitions without a final
conclusion and did not identify the known defect. The host rejected its partial
root-cause claim as incorrect. This proves bounded dispatch, preservation and
authority isolation, not useful model judgment. The inherited exhaustion message
conflated the one-Tool response rule with the total read cap; its final response
contained one requested read, but both permitted acquisitions were already used.
The prospective continuation policy corrects that distinction without changing
or replaying the original result. Completion, factual correctness and engineering
utility are evaluated separately in subsequent live observations.
