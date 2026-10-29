# Adaptive-0001: real local continuation

The real local summarizer produced useful-looking, cited notes **but no admissible
summary**: both responses wrapped JSON in Markdown fences despite JSON-only
instructions. Existing strict validation rejected both and preserved deterministic
fallback. No acting model consumed summary text. This experiment therefore does
not establish a semantic-compaction benefit, even though one fallback continuation
solved the task.

## Freeze and method

The [protocol](protocol.md), [final freeze](freeze.json), [original history](history.json),
[service identity](service.json) and [comparison](comparison.json) retain the exact
inputs and outcomes. The final freeze SHA-256 is
`b824858161605655542c5e8f36fbf0830b9ab4c6c68d3f8a450cf91d179b3458`.
One authored history combined verbose inventory/search metadata with an executed
counterexample to global event-ID suppression, current failed-check evidence,
and two exact source reads. It was not a prior live acting-model trajectory.
The repeated metadata is an explicit pressure fixture, not natural discovery
performance. No original local dogfood case was changed or re-entered.

Before inference, a dry run showed the initial 18,000-byte target retained the
semantic exchange. The final target was fixed at 12,000 to exercise its omission.
The earlier preflight freeze is retained separately. A keyword-only invocation
argument was also corrected before inference. No model result informed either
correction. The original request stayed 40,010 bytes; A/B/C used identical initial
acting requests after fallback, 4,306 bytes under the unchanged 32,768 ceiling.
Provider sampling/settings were unchanged; no seed or deterministic-generation
claim is made. Fixed order and provider caching may confound latency comparisons.

The installed artifact was streamed and SHA-256 verified against the existing
Qwen3.8-27B UD-IQ4_XS profile, with pinned llama.cpp image and 32K service capacity.
The service was already running; this task neither restarted nor replaced it.
The acting and auxiliary interactions have separate source identities, request
records, entry facts, call bounds and usage. No paid/cloud inference occurred.

## Observed comparison

| Treatment | Acting / auxiliary calls | Auxiliary seconds | Total seconds | Edits | Outcome |
|---|---:|---:|---:|---:|---|
| A deterministic | 2 / 0 | 0 | 30.026 | 0 | Invalid source continuation range; stopped before editing |
| B explicit semantic | 3 / 1 | 34.595 | 50.630 | 1 | Summary rejected; fallback candidate passes 4 focused and 5 held-out cases |
| C adaptive | 1 / 1 | 36.583 | 39.434 | 0 | Summary rejected; invalid source range; stopped before editing |

A acting usage: 2,856 input + 102 output tokens. B acting: 4,801 + 328;
auxiliary: 3,992 + 610. C acting: 1,236 + 51; auxiliary: 3,992 + 820.
These are provider-reported counts, separate from serialized host bytes and
measured input counts. Cache/reasoning counts are unavailable, not inferred zero.
No monetary-cost estimate or hardware throughput generalization is made.

The neutral host's 4,306-byte first request becomes 4,439 bytes after the
experiment adapter binds the unchanged provider sampling settings. The adapter
independently enforces the same 32,768-byte hard ceiling on that effective
ModelRequest before entry. Both auxiliary effective requests are 18,030 bytes
and measure 3,992 input tokens; all initial acting inputs measure 1,236 tokens.
These are serialized ModelRequest sizes, not HTTP wire or tokenizer equivalences.

Deterministic projection omitted both authored metadata exchanges, keeping exact
objective/restrictions, current failed-check result and source disclosures.
It reclaimed 35,704 bytes (89.24%). No execution was repeated to reconstruct
Context. B's subsequent requests were 5,700 and 6,378 bytes; A's second request
was 5,525. C made only its initial acting request. Source/currentness/native
validation stayed enabled throughout. Summary attempts received normal-stop
responses, but neither passed structural validation or reached adoption.

## Semantic adjudication

For both raw summaries, manual comparison with the original disclosed records
finds the following supported statements: global ID suppression was rejected;
streams may share an ID; rejected events must not reserve IDs; the implementation
still failed and no edit had occurred. Neither invented a passing check, completed
task, new permission or source witness. C additionally retained the actual probe
exit 1 and AssertionError. B omitted that numeric/check detail. Neither retained
the exact expected/observed mapping or a concrete next action. Both retained
low-value `source_acquired: false` metadata, accurately historical but potentially
confusing if read as current availability. Both classify some conclusions as
objective/uncertainty rather than a precise execution-state account.

The raw notes cite the correct disclosed record indices/digests. This does not
override their actual format rejection. No post-hoc fence stripping was applied
to a continuation, and no corrected summary or model retry was substituted.
Semantic fidelity here is a manual, limited adjudication of two outputs from one
source history, not a general accuracy result. The acting models had **no** chance
to use these notes, so H2 is only partially informed and H3 remains untested.

C's opening note associates event-ID suppression with record 3, which only says
"Retained authored investigation". The paired record 4 supplies that topic; the
single cited record does not support the full paraphrase alone. This is a concrete
attribution weakness despite valid digest membership, not an invented execution.

## Continuation and independent review

A requested `focused.py[0:439]`, received it, then requested `[439:878]` although
the file has 663 characters. C requested `[0:1536]`. Source validation refused
both oversized ranges before a read effect could complete. Their progress retains
an unacknowledged Tool dispatch; this is not silently relabeled as no attempt.
No source mutation occurred. The host archived original bytes and restored known
state; an archive does not imply a produced candidate. Held-out failure is expected.

B read `[0:598]`, then redundantly read the already disclosed `[560:598]`, and
proposed one exact replacement. Independent inspection confirms that its change
filters rejected events before identity reservation and keys accepted retries by
stream and event ID. It preserves first accepted occurrence, zero/negative deltas,
interfaces and read-only `rules.py`. Four fixed examples and five held-out literal
cases pass. The framework acknowledged the edit and check, archived exact candidate
bytes and restored the original. No Codex edit, repair turn or publication of this
fixture candidate occurred. The observed success belongs to deterministic fallback,
not semantic compaction. Divergent sampled trajectories preclude a causal A/B claim.

The original held-out B process passed assertions but failed while printing Unicode
through Windows cp1252. Its exit/error is retained in `grade.json`. Re-executing
only the same oracle and unchanged archived candidate with `-X utf8` exited zero;
`grade-utf8.json` preserves this correction. No oracle assertion, candidate or
primary model run was changed. This is a reporting harness error, not a product
or model defect.

## Decision and limits

H1 is supported for this pressure fixture: deterministic projection fit cheaply.
H2 has limited positive semantic evidence but failed operational format compliance.
H3 is not established. H4's conservative entry/fallback rules operated, but the
automatic auxiliary call bought no demonstrated continuation value and added
36.6 seconds. Keep adaptive summarization explicitly opt-in; these observations
do not justify universal thresholds or enabling it on every request.

The host's value label is also a limitation: several facts in the rejected probe
were redundant with the protected objective. Even an adopted summary might add
little beyond those exact instructions and source. The policy detects omission
of host-valued records, not semantic novelty or proven usefulness. Future hosts
should reserve that label for distinct prior progress; this study cannot justify
automatic inference merely because omitted text contains a decision or failure.

The highest-leverage next local-agent improvement is bounded source-read usability:
present exact resource lengths/available next ranges and return recoverable,
qualified invalid-range feedback before any effect, without widening scope or
retrying uncertain operations. Two treatments stopped at this boundary. Separately,
summary format compliance needs a small governed contract evaluation (inspect
provider-boundary structured-output support versus a strictly specified envelope),
not silent parser relaxation or an extra hidden summary call.

The neutral RepositoryCodingHost consumed the adaptive policy through the existing
coding process. Qwen's legacy application adapter still has a separate deterministic
continuation presentation; its task hashes and protocols were not migrated or
silently changed. This is neutral-host adoption and regression compatibility,
not full legacy Qwen application adoption. No restart, durable Evidence store,
provider-native opaque compaction, broader A+C or observation Option B is delivered.
