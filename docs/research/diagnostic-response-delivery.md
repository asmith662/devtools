# Strict diagnostic response delivery

This correction admits a narrowly supported presentation wrapper before the
unchanged diagnostic conclusion validator. It performs no inference and does not
reinterpret the historical B-0051 failure. Acceptance review and integration
authority remain unchanged.

Starting local and remote main were both
`e5ade5f61cf2a3cc172e83102a1141db2a0c13e2`. The executable correction is
`6868b292d32067d3e4ab94fa0e30d8f6f91f736d`.

## Exact rejection and derived regression

The [original assessment](diagnostic-completion.md) completed four Qwen calls.
Its final request advertised no Tools; the returned content terminated normally
at 1,838 output tokens and 7,851 UTF-8 bytes. That content begins with a lowercase
JSON Markdown fence. The strict parser failed at its first backtick with
`JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.

The [original proposal](code-audit/diagnostic-completion-20261101/diagnostic-records/proposal.json),
SHA256 `b76b937fcfd2c8df3889e46dc918af56a545315deb67972199e392e2aa75e788`,
remains BLOCKED with a null conclusion. Its original response and requests,
approval, consumed dispatch, source identities and custody facts are unchanged.

The maintained fixture
`tests/scripts/backlog/fixtures/b0051-diagnostic-response.json` freezes only the
bounded original response and its provenance/references. It is a test input,
not a reconstructed passing native result. The regression first reproduces the
strict rejection, then validates the complete payload under the new presentation
rule. No Qwen call or canonical WorkCycle dispatch is used.

| Identity | Observed value |
| --- | --- |
| Original returned-observation SHA256 | `19ac7463b8eb4da7148f57b031cf3eb66a7ff429a24e44bc7fc1e5788611717c` |
| Complete portable request SHA256 | `0e0a4b69206e6df66d67745abde7bf7cb61dd19edd704f9ea18cc02b28bd532d` |
| Raw content SHA256 | `8d0a07a02684d5142914e2f536446e5b6757161a0bb728d3800d6eec74d9e74e` |
| Candidate payload SHA256 | `97e6cd66c0b348987e3f507cdfc6db27229d2c3470cec573a81a252bed7ff9cd` |
| Raw / candidate bytes | 7,851 / 7,839 |
| Strict validator source SHA256 | `5939ba252147f4e29034bf4fc0c747b15fc8986612d54e4725cf4e157c886c82` |

The [derived reproduction](code-audit/diagnostic-response-delivery-20261101/derived-reproduction.json)
is new deterministic evidence. It is not administrative admission, approval or
another model execution. The existing incorrect source location ending at line
63 is retained in the validated payload: syntax/schema success does not make
that factual claim correct.

## Existing capabilities and selected boundary

`ModelRequest` supports provider-owned request extensions.
`LlamaCppRequestSettings(response_format="json_object")` already serializes the
provider's JSON-object formatting request; `json_schema` is not an accepted
setting. The adapter's existing deterministic transport tests cover that seam.
Portable ModelSettings contains only maximum output tokens and thinking control;
it has no structured-output or capability-negotiation contract. The native review
approval policy also closes its settings to those two portable fields.

Silently injecting a provider extension after capture would misstate the approved
request. Adding provider selection/serialization to review grants would exceed
this narrow correction. The selected fallback is therefore provider-neutral
presentation normalization in the existing diagnostic owner. No provider request
setting, serving default, model profile or running service is changed. No live
provider-enforced formatting is claimed or measured.

The semantic-compaction envelope helper is summary-specific and accepts only
labelled JSON with different content restrictions. The filesystem Markdown reader
indexes headings rather than delivering diagnostic payloads. Both remain unchanged;
there is no new general Markdown parser or JSON-repair library.

## Supported grammar and strict refusal

New prepared diagnostic subjects bind a prospective `delivery` marker:
`native-diagnostic-response-delivery-v1`, rule `single-json-fence-v1`.
It is included in the exact subject approved by the host. Old subjects without
the marker continue parsing raw text strictly, and unknown delivery rules refuse.

Bare JSON passes unchanged, including its original JSON whitespace. One complete
triple-backtick fence may be unlabelled or labelled lowercase `json`, with ASCII
outer whitespace and opening-line spaces/tabs. Opening and closing separators
may use LF or CRLF. The closing fence is exact and occupies its own line.
The complete inner text is retained byte-for-byte as the candidate payload;
no JSON object is reserialized, guessed, repaired or searched for in prose.

Other prose, incomplete/ambiguous fences, multiple or nested blocks, unsupported
labels/containers and extra JSON documents remain refused. A literal backtick
sequence inside a valid JSON string is data, not an extra block. The unchanged
strict parser then rejects malformed JSON, non-object containers, duplicate keys,
missing/extra fields, wrong identity/status, unavailable evidence and malformed
claims. Unsupported semantic assertions can still be retained as model claims,
subject to independent host evaluation; they are not certified by parsing.

## Capture, validation and authority

The existing ModelInteraction response is captured before presentation handling.
Its content, source, termination and usage remain untouched. New diagnostic
returned-response observations separately retain the raw-content UTF-8 hash.
Output limits, byte limits, incompatible response structures and Tool permissions
are enforced before a candidate payload can be admitted.

A standard native observation of kind `review-response-delivery` nests facts under
`delivery`, preserving the observation envelope. It records:

- Complete request and response identities and the raw-content hash.
- The exact candidate payload and its own UTF-8 hash, separately from raw content.
- The normalization rule, strict-validation outcome and validation/refusal status.
- The actual failure when wrapper recognition or validation fails.

Wrapper refusal records no candidate payload/hash and does not enter the strict
validator. JSON/schema refusal retains the attempted candidate and its hash.
These observations are validation facts. The existing immutable proposal writer
determines the final durable `proposed` or `blocked` result. A successful
presentation/validation observation cannot manufacture a persisted proposal if
Capture or final persistence fails. The dispatch claim remains non-replayable.

The model cannot use this pathway to approve its candidate, expand source access,
override private acceptance, authorize installation/integration or close backlog
work. No acceptance schema, eligibility gate, manual review decision or integration
reader is relaxed. Tool-call arguments are not presentation-normalized.

## Verification and publication evidence

The first focused delivery run passed 42 tests in 189.41 seconds. The broader
selection passed 194 tests in 543.78 seconds, including the final 44 delivery
cases, existing budget/finalization controls, persistence/non-replay, llama.cpp
contracts and both successful acceptance-review-to-integration consumers.
Supported-root Ruff/formatting, strict mypy over 625 files and layout passed.

The one protected run on the stable committed executable passed **4,173 tests,
two optional skips and 100% configured production line/branch coverage**, in
2,945.923998 receipt seconds, with unchanged inputs. It is recorded in the
[final receipt](code-audit/diagnostic-response-delivery-20261101/final-protected.json).
Its actual count, coverage and input qualification are retained with the
[integrity verification](code-audit/diagnostic-response-delivery-20261101/integrity-final.json).
Historical successful/failed receipts remain separate. No inference,
service reconfiguration or additional coding/diagnostic episode is performed.

Final checks matched 1,063 protected inputs and Git blobs and the tested Python,
platform and installed packages. The inherited-environment fingerprint retains
its invocation-specific qualification; complete cross-invocation environment
equivalence is not claimed. All 613 checked historical hashes, 13 forensic files,
903 RI rows and historical refs are preserved. Checkout ownership is released.
Inspector remains independently registered on `feat/agent-inspector`, and the
provider remains healthy with an actual 65,536-token slot and unchanged container,
image, command and mounts. No inference or service mutation occurred.

## Next authentic engineering task

The next task should be the unresolved **B-0051 canonical scope prerequisite** in
`src/devtools/context/python/modules/declarations.py`: distinguish unrelated
function/async-function/class-local bindings beneath module control flow from
genuine competing module bindings, preserving conservative handling of actual
module imports, stores, stars, pattern/handler captures and uncertainty.
Restoring the flawed original traversal is not a demonstrated repair.

This is one genuine one-file obligation, not the whole two-owner facade repair.
The B-0049/B-0050/B-0051 coding slots and both historical diagnostic slots remain
consumed. A linked continuation needs genuine Intake review, a fresh unused
WorkCycle slot, exact current source/check/private-holdout identities and explicit
finite coding authority before another Qwen episode. Do not invent a B-number.

Only a lawful candidate passing public and independent private acceptance with
known custody/effects may enter the existing acceptance reviewer under separate
fresh review authority. A trusted host must then assess its actual proposal.
Neither this recommendation nor the diagnostic delivery correction authorizes
that execution, installation, publication of candidate code or backlog closeout.
