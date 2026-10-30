# B0035-Thinking-0001: prospective paired Stage B assessment

Starting main: `5d026524d3a5b0ddea352bb966e736c9d225a765`.
One off treatment followed by one on treatment, independently frozen before
either inference. Prior outcomes are supplementary, never substituted controls.
No outcome-dependent changes, retries, extra hints or third treatment are allowed.

Both start from repaired Stage A SHA-256
`3a3aba918649eaf9240fede6efb15289fcbbb93999ac6fa9b2649020776c936c`
and original repository host. The same task, thirteen exact source disclosures,
repository/snapshot identity, source scope, native Tools, checks and independent
oracles are used. They reuse the established Stage B preparation without exposing
reference logic or withheld acceptance to the worker. A fresh Checkout and fresh
source witnesses apply in each episode; historical candidate acceptance is not
production publication authority. Neither worker sees the other's output.

## Treatment and resource parity

The only request-setting difference is `ModelSettings.thinking_enabled=False`
versus `True`, translated by the existing provider to the template boolean.
Both retain explicit temperature 0.7, top_p 0.8, top_k 20, min_p 0 and presence
penalty 1.5. Official profile data contains alternative thinking sampling, but
sampling changes are not necessary to enable the mode and would confound this
comparison. No reasoning-effort setting, server restart or provider change occurs.
The installed template defaults enabled reasoning to `xhigh`; we retain that
default rather than silently selecting another effort. Its mode-specific system
instruction and generation prefix are part of the documented treatment. Initial
requests measure 29,960/29,959 host bytes and 7,988/8,024 provider-template tokens
(off/on). The native rendered prompts are 28,224/28,422 bytes respectively.

Each gets ten acting calls, six source/search actions, four proposals, at most
three applications/two natural check-feedback repairs, no auxiliary summaries,
8,192 generated tokens per request, 430 seconds transport timeout, 450 seconds
including measurement per call, 1,140 seconds shared-process time inside a
1,200-second outer watchdog. Both get identical resource ceilings, not guaranteed
equal consumption. The twenty-minute wall bound limits aggregate compute before
the theoretical ten-call output maximum in slow cases. No hidden call reservation.

At the historical 22-23 tokens/second, 8,192 tokens take about 356-373 seconds;
430 seconds leaves bounded serving overhead. This doubles a historically exhausted
4,096-token thinking allowance and quadruples the prior Stage B ceiling for both
treatments. It is a credible opportunity, not a guarantee against long reasoning.
An output-limit response is incomplete and dispatches no edit. A timeout retains
unknown entry/effect qualifications and is not retried. Reasoning and final output
share the generated-token ceiling; separate reasoning usage may remain unknown.

Each complete host request remains at most 32,768 bytes. The provider measurement
must be at most 24,064 input tokens, reserving 8,192 output plus 512 safety tokens
inside the unchanged 32K serving window. Native template prefix and retained
reasoning can change measured tokens and later serialized bytes; those costs are
part of the treatment, not silently excluded. Both use unchanged deterministic
projection watermarks 24,576/20,000 and unchanged source/edit limits.

## Admission, preflight and scoring

Editable modules remain repository.py and navigation.py. The host has 737 bytes
of headroom; navigation has space for coherent presentation responsibility. The
model must choose implementation and grounded anchors; no source-size relaxation,
new file or supervisor patch is authorized. Public focused tests remain readable.

Preflight must establish current Stage A behavior/quality acceptance, intended
baseline Stage B failures, independent oracle controls, matched exact initial
requests apart from the boolean, and two prospective affordable continuations.
All preflight artifacts are staged outside an active Checkout and reconciled
after release. Freeze hashes bind the common runner, source and unchanged oracles.

Record calls before first edit, active witnesses, source reads and historical
repeats, refusals, proposals, admissions, actual installations, managed checks,
feedback consumption, repairs, independent acceptance, request bytes, provider
tokens, model seconds and total wall time. Generated prose/reasoning is not an
edit. Early incorrect edits do not outrank independently correct implementations.
Native call selection, dispatch, acknowledged effects and refusals stay distinct.

A candidate requires full focused and withheld B-0035 checks, the additional
integration predicates, Stage A regressions, existing compatibility, Ruff,
formatting, strict typing and independent architectural review. Any production
acceptance additionally requires the unchanged protected gate and ordinary
integration/publication authority. If both succeed, choose by correctness,
minimality and ownership, not preferred mode. No combining failing patches.

If neither succeeds, archive both and restore production; do not publish an orphan
helper. One unseeded sample per mode cannot estimate success rates or establish
general causal superiority. Sequential cache/warmth, shared working-set pressure,
fixed exploration allowance and possible truncation limit interpretation. Preserve
raw responses and known usage; unknown reasoning/cache subtotals remain unknown.

## Stop boundaries

No paid fallback, model replacement/download, arbitrary shell, worker Git authority,
Codex implementation or framework change. A material provider compatibility defect
or unavailable credible reasoning treatment stops comparison for a separate
decision. Uncertain calls are not replayed. An ordinary failed treatment does not
invalidate the independently frozen second treatment after verified restoration.
