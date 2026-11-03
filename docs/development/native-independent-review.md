# Governed independent native review

This is **acceptance review**. A separate
[diagnostic purpose](native-diagnostic-review.md) reuses the bounded read-only
operation for authenticated blocked history, with distinct schemas/grants and no
acceptance or integration authority. None of the acceptance gates below is relaxed.

New subjects use [structured callable conclusion delivery](structured-acceptance-review.md)
through existing model-neutral request/response values. The callable transports
only a proposal; source Tools and host acceptance retain their existing authority.

`WorkCycle.native.reviewer` composes a bounded model-neutral review of the exact
candidate produced by [native maintenance](native-maintenance-handoff.md). It is
repository administration under `scripts/backlog/native/review/`, using existing
ModelInteraction, native Tool composition, Context source materialization, native
candidate authentication and WorkCycle's immutable writer. Runtime, framework
Agents, coding loops and legacy Qwen contracts are unchanged. B-0043 stays open.

## Operator and trusted host

The existing `native-review` command still accepts a separately approved manual
decision. The actor path adds these administrative operations:

```text
uv run python -m scripts.backlog --root <root> native-review-prepare <item> --policy <review-policy.json>
uv run python -m scripts.backlog --root <root> native-review-authorize <item> --reference <host-decision> --expires <ISO-time>
uv run python -m scripts.backlog --root <root> native-review-proposal <item>
uv run python -m scripts.backlog --root <root> native-review-decide <item> --proposal <sha256> --decision accept --reference <host-decision> --rationale <independent-assessment>
```

Authority commands require the existing genuine interactive default-No host
confirmation. A configured trusted Python host injects an actual ModelInteraction:

```python
proposal = await cycle.native.reviewer.execute(
    item, interaction=review_model, profile="approved-profile",
    authorize=current_host_decision,
)
```

Preparation grants no effects. Dispatch requires both a persisted unexpired
review-only approval and current host consent. The actual packet, not just a
role name, is shown to the authority callback. There is no CLI provider loader,
model registry or external Codex-to-ModelInteraction impersonation. A supported
adapter must implement the real boundary and honor approved settings.

The closed policy contains `actor`, `source`, `profile`, `independence`,
`read_paths`, `settings` and `budgets`; `review.actor.policy` defines exact fields
and ceilings. Independence requires a host-attested fresh session and provenance
reference, plus explicit false `implementation_participant` and
`privileged_reference_access` declarations. Actor identity must differ from the
coder. The same model family may fill both roles with separately provisioned
sessions. Different strings, hashes and an empty continuation are not proof of
meaningful independence: the trusted host must actually provision and assess it.
No coder grant or legacy standing approval is inherited.

## Subject and disclosure

Before preparation, dispatch, each read/model operation, and host disposition,
the owner reauthenticates assignment/result/candidate identities, current restored
baseline, declared source/check inputs, configuration and Checkout release.
Missing, changed, unresolved or unsuccessful terminal evidence blocks entry.
Historical public failures before a successful repair remain disclosed failures.

The explicit subject contains the task objective and information obligations,
authorized edit/read/check scope, exact baseline and archived candidate text,
diff, public check history with diagnostics, qualified private-acceptance outcome,
custody/effect facts, the coding Localization readiness/disclosure observations,
and environment limitations. Information readiness is not proof of behavioral
correctness. Content references bind each
disclosed group; the result identity also binds undisclosed original evidence.
Private acceptance implementation, controls, diagnostics, worker reasoning and
raw coding conversation are excluded. No reference solution is disclosed.
Private outcome availability is not evidence of exhaustive behavioral coverage.

Only approved assignment source/test addresses enter the read-only SourceScope.
Model-selected `read_source` uses existing scoped source Tools and Context range
materialization. It reads restored baseline/dependencies, clearly distinguished
from archived candidate text. Review never installs candidate bytes to inspect
them. There are no edits, invented checks, shell, Git, Checkout mutation,
integration, publication or backlog-approval Tools. Source/evidence text is
untrusted data; its instructions confer no authority.

Acceptance review supports a bounded batch of `read_source` calls in one model
response. Each call consumes one acquisition, independently of the number of
model responses. Before any Tool entry, the whole batch must have unique fresh
call IDs, admitted names/arguments/ranges, authorized current source, enough
remaining acquisitions, and capacity for all results in the complete next
request and capture. Predictions use the existing snapshot-bound Context range
options; they are not completed acquisitions or model-visible source evidence.
Capacity reservation is conservative and may refuse a batch that lacks headroom
for the next request and bounded response. Smaller authorized ranges remain
available. New subjects carry `completion: native-review-completion-v1`.
For those subjects, known preflight refusals with unique fresh call IDs return
correlated Tool feedback with zero entered effects and the remaining allowance.
The refused batch consumes its model call but no acquisitions. Recovery stays
inside the original call, read, time, Prompt and capture limits. Authority loss,
stale inputs, ambiguous entry, missing/repeated IDs and persistence failure still
terminate. Historical subjects without this policy retain their old behavior.

Acceptance and diagnostic review share the budget-view implementation. Each
prospective acceptance request reports remaining calls/acquisitions, supplied
baseline/candidate identities and source eligibility. The last approved call,
or a call after acquisition exhaustion, has no source Tools and requests the
structured conclusion or explicit insufficient evidence. No call is added.
Refusal feedback is recorded as prepared; only the next captured request proves
its inclusion in model input. Actual completed reads alone become evidence.

Admitted reads execute sequentially through existing Tools with authority and
currentness checks before each entry. The assistant Tool-call batch is retained
once; each result carries its original call ID and separate source identity.
This is not an atomic transaction: earlier completed reads remain completed if
a later operation fails. Known completions and unresolved entry are recorded
separately, with no retry after uncertainty or persistence failure. Only actually
completed disclosures enter review evidence. Coding/editing Tool safety and
diagnostic-review batch/finalization policy are unchanged.

The complete initial subject and retained read exchanges must fit the approved
Prompt budget. No hidden reduction creates fictitious completeness. Native v1
caps calls, reads, per-call/total time, output tokens, response bytes and capture.
Provider continuation is not inherited; requests use explicit retained messages.
Timeout, malformed response, exhaustion, missing conclusion, output limit,
unauthorized read or capture failure produces a blocked proposal, never implicit
acceptance. Dispatch intent precedes model entry. One slot prevents replay,
including when proposal persistence fails or model completion remains uncertain.

The legacy v1 path has **one reviewer subject/dispatch slot per native assignment**.
`prepare` creates `reviewer/` once; it has no attempt selector. Standing authority
also refuses a consumed review slot before issuing a decision. A blocked attempt
cannot be overwritten, moved aside, or renewed by changing actor/session labels.
The prospective [bounded continuation](native-review-continuation.md) now permits
one distinct v2 subject after the authenticated, known unentered legacy batch
barrier, plus one v3 subject after the closed v2 remaining-budget interruption.
All preceding dispatches remain consumed. Exact selection is required for
new authority, host disposition and integration readers; there is no implicit
latest-result rule, engineering-rejection retry or general restart capability.

## Proposal and host decision

Prospective `backlog-native-review-{subject,authorization,dispatch,proposal}-v1`
records share the existing work-item folder under `reviewer/`. Bounded native
observation records retain actual request/response and read intent/result facts.
They are local content-authenticated records, not signatures or a universal
Evidence store. Failure to persist propagates and leaves the dispatch claim.

The closed JSON conclusion has `disposition` (`accept`, `reject`, or
`insufficient-evidence`), `summary`, `evidence` reference names, `findings`,
`outstanding`, `requests` and `assessed_obligations`. Each finding names its
support and labels `observed` or `inference` and `blocking` or `advisory`.
These are attributed model assessments; an `observed` label is not host-certified
truth. The reviewer can identify an apparent defect, question coverage, reject,
or request further inspection/validation. It cannot invent evidence references.
Acceptance proposals require the objective and supplied obligations assessed,
core evidence cited and no unresolved blocking findings, obligations or requests.
This checks structural completeness, not the quality of engineering judgment.

New subjects additionally bind `delivery: native-review-response-delivery-v1`
with rule `single-proposal-call-v1`. Requests disclose the subject/candidate-bound
`submit_review_proposal` schema alongside inspection reads; synthesis retains
only the proposal callable. Exactly one fresh identified call supplies the closed
conclusion above. Text-only, mixed and unsupported delivery fails. Historical
subjects without the marker retain strict raw-content parsing. Host admission
reparses the captured final request/call without repeating ModelInteraction.

`decide` reauthenticates the exact proposal and subject and requires current
unexpired host authority. The host sees the actual proposal and approves or
rejects it through the existing native review operation. A favorable proposal
can still be rejected. An adverse or insufficient proposal cannot be accepted.
Such results return to the supervisor; no repair/review loop is launched.

The existing native review schema retains its meaning as a host decision. Actor
decisions additionally bind `proposal_sha256`; the candidate reader authenticates
that chain before the existing integration-plan owner consumes it. Expiry is
checked for new review effects/decisions, not used to erase a historical valid
decision. Review records never grant installation, publication or parent closeout.
The original administrative decision path remains available independently.

## Assurance and remaining work

Maintained authored-repository tests use neutral scripted ModelInteraction
responses, actual coding checks/custody, read Tools, proposal persistence, host
disposition and the existing integration-plan consumer. They establish lifecycle
mechanics and truthful refusals, not real model judgment or engineering competence.
Development uses impact previews and targeted saved-failure recovery. Publication
requires the unchanged protected coverage gate.

Live use still needs separately approved worker/reviewer adapters, actual session
independence assessment, task/check scope and finite model execution authority.
No inference, service change or paid fallback is authorized by this delivery.
Planning, task selection, automatic review-driven repair, durable restart and
autonomous publication/closeout remain separate. The next competence step is one
separately authorized bounded live coder-and-reviewer task with predeclared
acceptance, independent provenance and retained failure/rejection evidence.

## Delivery evidence

The [authenticated delivery receipt](../research/code-audit/native-review-20261031.json)
retains protected source/input identities, environment qualifications, actual
failed development observations, selection reasons and an authored episode through
the existing integration-plan consumer. Tested executable commit:
`a34bdaa7e7f320d8746c13d57d98a27b4f564673`.

Exactly one repository comprehensive run passed: 4,019 tests, two optional skips,
100% configured production line and branch coverage, 2,511.48 seconds including
command overhead. All 1,054 protected inputs remained unchanged. The added review
scenarios contribute 32 tests; the entire native maintenance/review file has 53.
The complete protected suite has additional real authored-repository work and is
not claimed to run faster than its predecessor.

During development, the 201-test shared-contract selection passed in 115.13
seconds. Seven failed-ID/correction/evidence-boundary cases passed in 173.74
seconds, and the final review-scope consumer passed in 36.19 seconds. The prior
51-case native run took 652.36 seconds with 50 passes and one assertion failure:
the fixture expected Python's missing-file exception instead of the filesystem
domain's actual refusal. The earlier consumer run also retained its two fixture
serialization failures. Both failed invocations remain failed; focused recovery
preceded the single final comprehensive run. The observed 478.62-second
difference between the broader native run and recovery is a scope counterfactual,
not a controlled performance benchmark or a pass for omitted tests.
