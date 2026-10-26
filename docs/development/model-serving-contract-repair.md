# ModelInteraction/Serving contract repair

## Delivered scope and accepted identities

Initial main `a7a49cc18f3b40a5bf4e3897ca30d9a5cddc30d1` was authenticated with clean tracked/index state and all thirteen forensic hashes. Documentation-only audit PR31 normally merged as `e8b7553afca8275fc7afcfa552db65f57b6e8afc`, tree `70a0576ce803b86ba1df81751538b54a270ceea3`; local main fast-forwarded safely. No audit source or frozen evidence was rewritten.

Two owner-focused implementation commits on `feat/model-serving-contract-integrity-20261026`: Serving `c6eabd005462f022dd71869cb9d9520c2db68885` and Interaction/Tool `5125ab6a847ee1844913c006d801b01f5fea7cc4`. Final tested production tree `73c3fd7e55901f4e70758db30c4dd317168f1f20`. Normal PR32 accepted main `a602dae60b3a7c71bdd1c1231613143c309292c1`, with exact production tree `73c3fd7e55901f4e70758db30c4dd317168f1f20`. Independent remote observation, both merge parents, twelve accepted source/test/package-doc/decision-brief blobs and physical inputs were verified. No bypass, force operation, fabricated review, ref deletion, inference, Docker or model download.

## Independent baseline and permanent regressions

Before production edits, permanent public-caller tests on `e8b7553afca8275fc7afcfa552db65f57b6e8afc` produced36 expected failures and234 passing controls, no collection/setup errors, in3.73s. Initial oversized pytest-generated temporary names caused a harness error; short literal case IDs corrected that before the retained baseline. The error is not defect evidence. Exact XML, source owner identities, failure messages, test names and the unchanged original44-case audit source/results are linked in the [machine receipt](../research/code-audit/model-serving-contract-repair-20261026.json).

Permanent tests extend existing Interaction/provider/Serving modules. They use literal wire bytes, independent strict JSON parsing, registry references, deterministic read/drain/close/cancel schedules and two actual bounded local loopback connections. Current tests also cover fragmented header/body/EOF/Content-Length, truncated/oversized/invalid framing and shape, unknown/error controls and real public status/send. No test double is represented as live inference. Final focused model suites386 passed;154 targeted Runtime/Evidence/Qwen/persistent-service/Tool consumer tests passed. Post-main result: `540 passed in 88.21s (0:01:28)`. All44 original audit cases agree, including unchanged observer failure cases.

## Five separately owned corrected contracts

| Canonical proposal | Existing owner and correction | Remaining boundary |
| --- | --- | --- |
| 8c79f8ca-20c0-434d-90f8-9418f0767e57 | llama provider response decoding catches invalid UTF8 as ResponseError; non-success HTTP preserves status, bounded replacement detail and UnicodeDecodeError cause | Not proof of provider nonentry; no new response-size or retry policy |
| 333df5ec-5a67-4b3c-8b1b-71dd4f544f83 | vLLM accumulates bounded fragmented EOF/Content-Length response, refuses malformed/truncated/oversized framing and nonobject model-list JSON |65,536 total header/body bytes plus one detection byte; transfer encodings unsupported; standalone status still needs caller deadline |
| 54fe0021-8992-47b2-85bc-4bdce6ade4e0 | Both Serving adapters distinguish acquisition from owned writer finally; close and await under one-second bound on success/error/timeout/cancel, preserving primary result against expected close I/O/timeout | Repeated cancellation may interrupt wait after close; not server/process termination or rollback; llama EOF-read policy otherwise unchanged |
| a0ccec58-586d-4f46-8da8-37d26a447bf2 | Both image configs inspect terminal image component or nonempty algorithm/digest qualifier; registry-port-only/empty versions refuse | Narrow structural admission, not full OCI parser or immutable-byte proof |
| bf8cf791-ffc8-4d7f-ac6c-94613b87e181 | Model Tool values and Tools disclosure reject nonstandard constants; schema serialization rejects nonfinite representable values with existing ValueError/causality; native call normalization retains domain errors | Valid raw argument spelling, including grammar-valid large numbers, preserved; no full metaschema/duplicate-member/Resource JSON policy change |

The filesystem JsonCodec owns file/source/format models and different error/number-conversion semantics. Reusing it for schema strings or exact raw call arguments would add inappropriate file representation and lose spelling. Small private stdlib rejection hooks remain under the two existing independent domains; no new common serialization framework/dependency is promoted. Qwen's existing disclosure composition is protected through these public values, without application/runtime redesign.

## Final committed validation

`uv run python scripts/validate_development.py` on committed `5125ab6a847ee1844913c006d801b01f5fea7cc4`, tree `73c3fd7e55901f4e70758db30c4dd317168f1f20`: **3142 passed, 2 optional live skips, 100% configured production branch coverage; 1104.71 seconds pytest / 1106.669237 seconds command**, exit0. Coverage thresholds, exclusions, test selectors and gate script are unchanged. Supported Ruff `src tests apps scripts` passes; supported formatter checks635 files; configured strict mypy checks521 files. Raw Python/root-config identities are before/after command; supplemental811 tracked profile files were hashed during the gate and preserved through publication. Git-clean committed identity before/after authenticates remaining tracked inputs. This is not universal ignored/environment/toolchain closure, HEAD-equivalent reuse or a new cache. Broader d58697fd remains open.

Commands, UTC timestamps/durations/exits, physical SHA256 identities, exact Git blobs, baseline failures, final44-case output, coverage totals and post-main evidence are retained in the machine receipt. Documentation/JSON/Intake/layout/links/whitespace and forensic checks accompany this closeout. Local link checks cover file targets, not external URLs/anchors.

## Observer decision explicitly unchanged

The [unapproved decision brief](model-observation-policy-decision-brief.md) traces successful normalization followed by backwards-wall or callback failure, compares explicit post-response exception versus separately reported optional-capture failure, and recommends the latter only after concrete consumer/privacy/compatibility approval. Existing send return/exception behavior is unchanged. Observation, Runtime, Evidence and coding-loop source blobs match the audit baseline exactly; final original probes reproduce their existing limited outcomes. No suppression, clamping, retry, usage fabrication or new observer infrastructure.

## Canonical closeout and remaining audit

Five existing UUIDs receive append-only ADVISORY implemented-and-merged evidence; all remain administratively PENDING_REVIEW because no delivered state/closure authority is invented. No duplicate proposal, B-number, approval, grant or parent closure. Original audit fields remain intact under an append-only cohort maintenance overlay. The thirteen original forensic bytes, source-grounding histories, experiment branches and RI ledgers are preserved.

Remaining: explicit observer policy, broader Evidence ingestion/correlation, Serving ambiguous-startup and acquisition effects, validation-input closure, application cohesion and broader supported runtime/provider matrix. RI original fixtures93/93, experimental606/606,188 historical exact versions and unapproved A+C remain separate. Next is a bounded Agents/Runtime audit of existing Conversation/agent admission/cancellation/result consumers, with prior narrow Runtime review reused by exact identity, followed by Persistence and remaining applications/tooling. No next cohort or successor dossier starts here.

`repair:model-serving-contracts:5125ab6a:20261026`.
