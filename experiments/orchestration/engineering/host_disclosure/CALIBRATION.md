# Astra/High engineering calibration

Two authorized synthetic invocations used Codex CLI 0.162.1 and the exact v3
SEMANTIC_WORKER profile. Both passed. No scientific packet, task or gold was used.
The immutable [minimal receipt](minimal-receipt.json) and
[capacity receipt](capacity-receipt.json) bind profile/implementation digests and
exact captures in their adjacent evidence directories. No further call was made.

| Measurement | Minimal | Capacity |
|---|---:|---:|
| Input Unicode characters / UTF-8 bytes | 175 / 175 | 700000 / 700000 |
| Canonical response characters / bytes | 25 / 25 | 59752 / 59752 |
| Reported input tokens | 9515 | 534177 |
| Reported cached input tokens | 0 | 0 |
| Reported cache-write input tokens | 0 | 0 |
| Reported output tokens | 20 | 8081 |
| Reported reasoning-output tokens | 0 | 410 |
| Managed process wall seconds | 5.783986 | 237.895035 |
| Observed tool calls | 0 | 0 |

Each used a fresh thread, one controlled turn, host stdin disclosure, native output
schema and sole-final-message capture. Final response and JSONL agreed. Isolated
empty CWDs were unchanged. Tools/network/user configuration/rules were disabled.
Capacity input was deterministic low-compressibility synthetic ASCII; response
schema forced 116 strings of 512 characters (91.17% of the 65536-byte envelope).
Neither invocation had an outer retry. Provider-internal transport behavior is
BUILTIN_RUNTIME_DEFAULT; underlying request/retry count is UNKNOWN.

These are workload lower-bound observations for this exact profile, not runtime
maximums, universal token capacity, model quality evidence or subscription charges.
One minimal sample is an observed invocation floor, not a statistical estimate of
fixed overhead. Raw categories remain separate; cached/reasoning subsets are not
added into invented totals. Missing turn IDs, model-only duration and reported
model identity remain UNKNOWN. Model catalog metadata is recorded separately from
empirical evidence; no exact tokenizer or effective context capacity is invented.

The response envelope is a method-owned representational ceiling, not a truncation
mechanism or a claim that the probe produced all 65536 bytes. Actual responses
must validate completely. Exact input character AND byte gates remain mandatory
before entry, including dynamically generated global consolidation input.

Candidate A1/A2 sizing and invocation-spend review are recorded in
[bounded execution](../bounded_execution/README.md). These receipts grant no
scientific execution authority and freeze no scientific Stage A or plan.
