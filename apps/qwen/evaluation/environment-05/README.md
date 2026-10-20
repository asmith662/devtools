# Actual model, reference harness and coding environment — 05

All ten budgeted genuine local runs completed. This is a two-task development
comparison, not a held-out estimate, Codex comparison or general proficiency claim.
The frozen baseline is `44c98aeb341bf9d9e306d57a07fe8fa6db5c3305`.
[Results](results.json) retain usage, dispositions, source and raw-evidence hashes.
Prior Cohorts 01–04 and their negative results remain immutable.

## Verified weights and runtime

The mounted GGUF is **14,252,845,984 bytes**, SHA-256
`40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`.
Full local hashing matches the pinned upstream LFS object and size for
`unsloth/Qwen3.8-27B-GGUF`, revision
`16b6ae91d7429915de9e9a1c859c604731c78088`,
`Qwen3.8-27B-UD-IQ4_XS.gguf`. GGUF v3 has 866 tensors, model name
Qwen3.8-27B, architecture `qwen35`, native training context 262,144.
The architecture label is recorded metadata, not evidence of the wrong model.

llama.cpp `b10868-304665fe7` runs the pinned CUDA image
`sha256:7625abb46c6bb8357e214f949b409a152c0944228e5a653fbab112f98ad2de7e`.
Actual argv/props/logs establish 32,768 Context, one slot, full GPU offload,
Flash Attention and q4_0 K/V. The service is published only at loopback :8080.
The embedded/native chat template uses structured assistant/tool calls; its
captured SHA is `12827f24b742ea4e80cdc12dbcf9622227056b9f797252a3149263d4f9aaadce`.
Baseline metadata/server sampling is temperature 1, top-p .95, top-k 20,
min-p .05, presence penalty 0; thinking is explicitly disabled per request.
The actual defaults differ from the manufacturer's nonthinking recommendation.

The [Qwen model card](https://huggingface.co/Qwen/Qwen3.8-27B/blob/main/README.md)
and [Unsloth guidance](https://unsloth.ai/docs/models/qwen3.8) describe thinking
controls and sampling. Optional named request presets now make those settings
explicit; the maintained default remains unchanged. Medium thinking used a real
template control and 12,288 output tokens, including reasoning. Provider usage
does not partition reasoning tokens; returned reasoning text is preserved.

## Genuine outcomes

| Condition | Task | Result | Calls | Input/output tokens | Worker seconds |
|---|---|---|---:|---:|---:|
| Original Devtools | portable dot components | proposal refusal | 9 | 88,253 / 1,968 | 146.62 |
| Original Devtools | strict JSON overflow | proposal refusal | 10 | 73,954 / 3,654 | 196.27 |
| Pi 1.3.0 | portable dot components | accepted | 7 | 29,257 / 1,670 | 86.59 |
| Pi 1.3.0 | strict JSON overflow | accepted | 6 | 28,772 / 1,792 | 93.82 |
| Improved, old byte cap | strict JSON overflow | Context refusal | 7 | 35,111 / 1,634 | 98.44 |
| Improved, measured capacity/q4 | strict JSON overflow | accepted | 8 | 69,235 / 1,641 | 93.31 |
| Same worker, q8 K/V | strict JSON overflow | accepted after behavioral repair | 10 | 107,087 / 2,365 | 152.07 |
| Thinking off, 12,288 output | strict JSON overflow | accepted | 6 | 40,166 / 1,244 | 68.40 |
| Thinking medium, 12,288 output | strict JSON overflow | accepted after typing repair | 6 | 50,904 / 5,184 | 257.61 |
| Final, explicit instruct sampler | portable dot components | proposal refusal | 10 | 71,826 / 1,956 | 100.99 |

Total: **79 model calls**, **594,565 input / 23,108 output tokens**,
**1,294.13 worker seconds**, within 100 calls / 9,000 seconds. One additional
preparation refusal dispatched zero inference calls and remains separately recorded.
Pi prompt totals include cached reads; comparing only its uncached input would
understate consumption. Pi result `started_at` was written after execution;
its SDK message timestamps and measured elapsed duration are retained instead
of claiming that field is a valid start time. Coordination tokens, active Codex
time, electrical energy and monetary compute costs are UNKNOWN. No paid fallback.

## What the comparison established

The [MIT Pi harness](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent)
was pinned to npm `@earendil-works/pi-coding-agent@1.3.0`; installation used
`--ignore-scripts` in ignored local state. Node 24.14/npm 11.9 supported it.
Its SDK supplied native read/edit tools and its own conversation/system builder.
Host wrappers restricted paths and exposed fixed validation; bash, arbitrary
writes, extensions and cloud fallback were disabled. This is a scoped Pi SDK
comparison, not the unrestricted stock CLI. The same endpoint, weights, baseline,
objectives, oracle, original regressions, Ruff, formatting and typing were used.
Pi allowed 16 total Tool actions versus the original worker's eight Context/API
actions plus three proposals; native editing/API-evidence contracts also differ.
Thus 0/2 versus 2/2 demonstrates practical harness friction, not an isolated causal
effect or calibrated population advantage. One Pi ownership-receipt reconciliation
was host coordination after successful process exit, not a model rerun or code repair.

Original Devtools proposals used prose where exact API evidence IDs were required,
even on tasks with no required API assumptions. Schema descriptions, empty-ID
requirements and refusal feedback now agree. The old conservative byte projection
later rejected a 43,792-byte repair containing only **14,923 actual input tokens**.
The provider now counts its actual native template/schema using `/apply-template`
and `/tokenize` before dispatch. Input + requested output + 2,048 safety tokens must
fit 32,768; a separate transport bound remains. No larger Context was warranted.

The q8 experiment actually offloaded 66/66 layers with CUDA Flash Attention,
1,088 MiB CUDA KV (544 MiB each K/V), and no observed CPU attention fallback.
GPU use rose from approximately 14,006 to 14,510 MiB of 16,376 MiB. Model CUDA
buffer was 12,726.35 MiB; initial baseline container RAM was 10.48 GiB.
Cold startup took about 4m44s, separate from task runtime. Diagnostic verbosity
also differed, so latency is descriptive. Baseline q4 serving was restored.
Both cache conditions accepted; one pair does not establish an accuracy benefit.
Medium reasoning preserved behavior through a real typing repair but cost more
on this task. No alternate serving profile was made the default.

The final path run returned otherwise relevant old source followed literally by
JSON closing syntax (`"}]}]}`). All three proposals were refused without mutation.
The host did not strip, approximate-match, repair or retrospectively accept them.
This remains an unresolved model/native argument-construction limitation.

## Coding environment and closeout

Task-opted-in native `git_inspect` and `run_check` expose fixed scoped operations
over existing managed Commands/ToolRunner. Fixed tests, oracle, Ruff, formatting
and strict typing return archived full logs and bounded feedback. Installed API
inspection remains an allowlist of host-selected objects/signatures/docstrings
and installed distribution versions; arbitrary imports/execution are prohibited.
These particular tasks had no required API targets: their results do not establish
live use of API inspection. Explicit new paths require observed absence and use
the existing atomic edit/application/restoration machinery; creation is currently
deterministically verified, not demonstrated by these two live tasks.

The shared WorkCycle integration entry authenticates a local accepted result,
installs exact candidate bytes with independently attributed maintained tests,
runs the shared validation, obtains exact-subject Codex review and can commit/push
an explicitly authorized ordinary feature. Protected development validation is
required for publication, and interrupted commits reconcile by tree/parent/trailer.
No model-facing Tool can publish; backlog closeout and protected target promotion
retain the existing separate authority. Mechanical formatting is opt-in and
AST-equivalent; semantic or typing fixes remain Qwen repair work.

Selected maintained-source candidate: q4 measured JSON, SHA-256
`3578f489eb7daa10445c1302708bd5b13e1ae0209b1580204fd0aa3afb05ba4e`.
Its integration receipt, independent tests, final validation and feature commit
are recorded in the completion section/results after closeout. Other evaluated
candidates remain evidence. The duration, regex, timestamp and B-0048 historical
candidates are not silently integrated or reclassified by this assignment.

The next priority is reliable native edit argument construction and precise
source-mismatch diagnostics, followed by fresh diverse paired tasks. There is
still no fair paid Codex baseline or evidence of general Codex parity.

## Completed maintained-source integration and verification

Shared closeout reached `FEATURE_PUBLISHED` in commit
`d09f4cf22fa0fb99910990de5753313f13b28449` on `feat/qwen-context-worker`.
The exact selected Qwen source hash above is installed in maintained source,
alongside 15 independently authored permanent regressions (32 JSON tests total).
Codex reviewed the actual source, reconstructed native proposal anchors and exact
candidate bytes, and recorded the subject-bound `ACCEPT_RECOMMENDED` decision.
Eight native runs replayed in memory: seven admitted transactions authenticated
their observed regions and final candidates, with request/response hash and native
message/call correlation checks. No model inference was used for this audit.

The protected gate passed **2,110 tests, two skipped, 100% production branch
coverage**, in 471.78 seconds. An earlier gate passed all tests but failed coverage
at 97.27% because the existing integration bootstrap imported Devtools before
coverage started. The bootstrap and its real-subprocess regression were corrected,
then the required gate passed; the coverage threshold was not relaxed. Independent
test preparation also exposed Windows decoding, lint and typing defects in host
test drafts. Only those independently authored drafts were corrected, not Qwen's
code or the frozen oracle. Separate validation directories retain these failures.

Final maintained-tree Ruff passes; changed-file formatting passes for 24 Python
files; strict mypy passes 485 files; layout and Git diff checks pass. Two test-only
formatting corrections after the gate are AST-equivalent and their 134 focused
regressions pass. Whole-tree formatting still identifies 58 unchanged files;
unscoped scans additionally encounter historical scientific payload findings and
a Ruff renderer panic. Those unrelated files were preserved.

The original q4 service is restored: 32,768 Context, one slot, exact embedded/server
template match, approximately 14,000 MiB GPU and 9.474 GiB container RAM at final
idle observation. Recorded q4 decode rates were 20.92–24.19 tokens/s; q8 rates
20.94–23.48 tokens/s. Prefix caching affects prefill timings; these are slot
observations, not an independent hardware benchmark. The current server's default
permissive CORS/no-key configuration is preserved, behind its loopback publication.

Protected main remains `862bda2d3d1d812893f84ab69691fc068ecce268`.
There is one physical checkout and the 13 pre-existing forensic files remain
untracked and untouched. No Qwen attempts beyond the ten-run budget, paid fallback,
scientific execution, backlog closure or protected promotion occurred. Observed
assignment timestamps begin `2026-10-19T23:58:14.481688Z`; the final results record
the completion timestamp. This span includes long gaps and is not measured active
Codex time. Coordination usage, electrical consumption and monetary costs remain
UNKNOWN.
