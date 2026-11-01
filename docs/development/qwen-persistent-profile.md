# Persistent qualified Qwen profile

The operator separately approved persistent adoption on 2026-11-01, including
exclusive provider access, one 64K launch, one short inference and exact 32K
rollback on failure. The adoption succeeded. The provider remains on **65,536
tokens**, with one slot, and the exclusive operational reservation has ended.
This grants no native task, review, integration or backlog-closeout authority.

The [authenticated adoption receipt](../research/code-audit/qwen64-persistent-adoption-20261101.json)
retains the actual approval, dispatch intent, original and adopted container
configuration, source/artifact identities, complete logs, requests/responses,
timings, resource samples and historical-preservation checks. The earlier
[temporary qualification](../research/qwen64-qualification-trial.md) remains
unchanged, including its mandatory 32K restoration.

## Configuration and lifecycle

The existing `scripts/qwen/llama_cpp_profile.py` keeps
`QWEN38_27B_UD_IQ4_XS` at its historical 32K settings and adds the qualified
`QWEN38_27B_UD_IQ4_XS_64K` value. Only context size differs. Both retain:

- Qwen3.8-27B UD-IQ4_XS, revision `16b6ae91d7429915de9e9a1c859c604731c78088`.
- GGUF SHA256 `40fac4050e940397dbf13087afd50f4734a11805bf9d65ef8ddd7483470e6199`.
- llama.cpp `server-cuda-b10868`, image digest
  `sha256:7625abb46c6bb8357e214f949b409a152c0944228e5a653fbab112f98ad2de7e`.
- All GPU layers, flash attention on, q4_0 K/V, zero CPU FFN layers, one sequence.

The supported service command defaults to 64K across fresh CLI invocations:

```powershell
uv run python scripts/qwen/llama_cpp_service.py status
uv run python scripts/qwen/llama_cpp_service.py start --cache-root "$env:USERPROFILE/.cache/huggingface/hub" --readiness-timeout-seconds 600
```

The exact 32K fallback remains selectable without changing shared configuration:

```powershell
uv run python scripts/qwen/llama_cpp_service.py stop
uv run python scripts/qwen/llama_cpp_service.py start --context-size 32768 --cache-root "$env:USERPROFILE/.cache/huggingface/hub" --readiness-timeout-seconds 600
uv run python scripts/qwen/llama_cpp_service.py status --context-size 32768
```

These are operational instructions, not standing permission to interrupt other
consumers. Coordinate and authorize any later service change. A running profile
mismatch is refused; `start` does not silently replace it. The 64K fingerprint is
`c86e124b80988509063f74d694b99120817f76eec1ce899740f6f61a0437c965`;
the original 32K fingerprint remains
`03758e5bc51c9aa9fbdd1850c1f25541d1eba76a80a54b74598886d882264bf1`.

One fresh container/model launch and a repeated supported `start` were verified. The repeated
command returned the same READY container without acquisition/restart or a
reversion to 32K. No second cold restart, host-boot persistence or new automatic
restart/fallback manager is claimed. Existing Docker restart settings are unchanged.

## Measurements and operating limits

Container start to observed READY took **223.059 seconds**; the service start
operation took 224.579 seconds including its preparation. The complete bounded
driver took 260.465 seconds. No rollback or second 64K launch was needed.
Artifact verification read the cached GGUF before startup; these timings are
not a controlled cold-cache comparison.

The short `LlamaCppInteraction` request had 511 measured input tokens and a
128-token output ceiling. It returned 49 tokens and an accurately parsed native
`read_source` proposal. No fictional Tool operation executed. Wall time was
7.512 seconds; provider-reported prefill was 5.069 seconds and generation was
20.523 tokens/second. First-token latency was not exposed by the nonstreaming
adapter. The existing 49,152-/62,464-token measurements were not repeated.

Across 18 samples, GPU use peaked at **14,724 MiB**, with at least 1,327 MiB free.
Windows free physical memory briefly fell to **203,640 KiB** (about 199 MiB),
and free virtual memory to 1,068,968 KiB. Later free physical memory recovered
to roughly 8 GiB; a post-validation observation retained about 6.2 GiB free.
Docker and HTTP health remained healthy. Startup pressure is severe
even though this operation completed. There was no observed CUDA allocation
failure or OOM kill. Logs preserve the auto-fit warning concerning explicitly
selected GPU layers; it did not prevent loading or inference.

Keep the 600-second readiness allowance and inspect actual loading progress.
Do not interpret an ordinary readiness poll or the old 180-second deadline as
proof of OOM. Future failure recovery should preserve diagnostics, restore the
exact original 32K profile once under genuine authority, and avoid restarting an
original-profile process that is credibly still loading.

## Native coding admission and next task

The service profile is configuration, not proof of current runtime capacity.
Before a fresh task dispatch, verify health, model/fingerprint and `/slots`:
one slot must actually report `n_ctx=65536`. Supply that observed capacity and
the supported tokenizer to native qualification. Count the complete templated
request plus its explicit generation reservation; do not assume capacity from
the CLI default. If the running provider is 32K, qualify against 32K instead.

The [native Context policy](native-context-policy.md) remains unchanged:
up to 128 KiB independent serialized-request capacity, deterministic projection,
precise `find_source`/`read_source_unit` and bounded reads, 1 MiB episode capture,
and existing edit/source-currentness and authority limits. Larger token context
does not enlarge editable files or grant additional calls/capture. This adoption
does not qualify 2,048-token generation, reviewer judgment or engineering competence.

The next authentic obligation is B-0049's unresolved narrow facade-scope repair
in `src/devtools/context/python/imports/members.py`: imports in unrelated nested
helpers/classes must not invalidate a valid module reexport, while genuine
competing bindings remain conservative. Its original slot is consumed. Prepare
a genuinely reviewed linked item with a new canonical identity and unused slot,
refresh source identities and public/private acceptance, then obtain separate
exact-scope coding and reviewer grants. Keep private oracle implementation out
of model Context. Do not fabricate a new B-number or replay B-0049. The next
measurement should be real edit/check/repair and, if eligible, independent review.

Validation passed: 34 focused profile/controller tests, then 273 provider/service
and native Context tests; supported-root Ruff, formatting, strict mypy, layout,
Intake, JSON/JSONL, documentation links and historical/ref preservation checks.
The controller's explicit executable profile-selection change required one final
protected run on committed candidate `8376bbc1845f9606de64e5409ec134636c13184a`:
**4,088 passed, two optional skips, 100% configured production line/branch
coverage** (14,247 statements, 3,644 branches, zero missing/partial). Pytest took
2,548.43 seconds; the maintained command receipt took 2,550.986 seconds. No
test-failure repair or second comprehensive invocation was needed. All 1,059
protected input identities and executable Git blobs match the tested candidate.
The final evidence commit changes documentation only.

The original stdout is authoritative for test-case counts. Its 4,088 passing
cases are distinct from 4,103 passing call-phase reports, which include unittest
subtests. The receipt retains both with that qualification. No historical result
was relabeled and operational observations were not substituted for coverage.
