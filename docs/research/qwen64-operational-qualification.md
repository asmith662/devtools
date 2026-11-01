# Qwen 64K operational qualification — 2026-11-01

Subsequent [freshly approved execution](qwen64-qualification-trial.md) reached READY,
completed actual 49,152-/62,464-token inference and restored the exact original 32K
service. The unentered disposition below remains the historical diagnosis checkpoint;
its approval state and evidence were not retroactively rewritten.

This assessment starts from synchronized main
`17080623de9d99f25c4fb6ef017f8cb8a28ef280`. The canonical tracked/index tree was
clean and Checkout ownership absent. Inspector remains independently registered
on `feat/agent-inspector`; neither its files nor branch is part of this work.
The existing native Context implementation is unchanged.

## Validation count reconciliation

The original protected pytest stdout ends:

```text
4081 passed, 2 skipped in 2244.77s (0:37:24)
```

The original parent and child receipts contain identical phase observations.
There are 4,096 passing **call-phase records** but 4,081 distinct passing test
node IDs. Four `unittest.TestCase` methods emit successful subtest reports under
the same parent node ID, in addition to their normal parent call report:

| Method in `tests/resources/filesystem/test_structured_compatibility.py` | Call records | Extra successful subtest reports |
| --- | --- | --- |
| `test_constructors_preserve_metadata` | 4 | 3 |
| `test_inherited_post_init_runs_once` | 4 | 3 |
| `test_inherited_validation_refuses_invalid_metadata` | 7 | 6 |
| `test_public_codecs_disk_reads_and_toolrunner` | 4 | 3 |
| Total extra records | | 15 |

The source uses three constructor subtests, six invalid-metadata subtests and
three codec subtests, matching these observations. A new focused execution of
that eight-test module reproduces eight passed tests and 23 passing call records.
There was no second protected run and no disagreement between executable trees.
The narrative's **4,081 tests passed** is correct. Interpreting the delivery
receipt's `call_outcomes.passed=4096` as distinct tests is an aggregation-unit
error. `Observations` preserves phase reports; it does not promise each is a
unique test. This reconciliation does not define a generic failure aggregation
algorithm by simply keeping the last report for each ID.

The original protected receipts, stdout, coverage and
[delivery record](code-audit/native-context-policy-20261101.json) remain unchanged.
The clarification is additive: no historical count or record identity is rewritten.
The configured production line/branch coverage result remains 100%.

## What the retained startup evidence establishes

The restored original-profile container is
`723f6596044c52021beed7b764ffffbd419c0f2ee6719f25250366065bf2888b`.
Timestamped Docker logs retain these milestones:

| Event | Docker UTC timestamp | Server elapsed time |
| --- | --- | --- |
| Container started | `03:16:38.741922656` | External container boundary |
| Model loading entered | `03:16:39.583291234` | `0.00.202.746` |
| Unused MTP tensor warnings | Around `03:16:42` | About 2.673 seconds |
| Threadpool initialization | `03:21:21.930144268` | 282.547447 seconds |
| Slot/context initialization | `03:21:22.444545812` | 283.063867 seconds |
| Model loaded/listening | `03:21:22.465545261` | 283.085085 seconds |

Thus this actual 32K restoration needed approximately **283.724 seconds from
container start to model loaded**, already exceeding the old 180-second wait.
The server's `4.43...` prefix means four minutes and 43 seconds elapsed; it is
not the wall-clock observation at `04:43` cited in the earlier handoff. The
later READY observation did not measure the first instant readiness became true.

The process continued after its caller's readiness timeout and reached usable
readiness. Current inspection shows the same container alive, the HTTP health
endpoint responsive, a 32,768-token slot and no active inference sequence.
There is no explicit CUDA allocation failure in the retained log. Docker reports
`OOMKilled=false`; current cgroup counters report `oom=0` and `oom_kill=0`.

The service controller's default readiness timeout is ten minutes. It waits for
the existing `RUNNING_LOADING` state and raises on timeout without itself killing
the loader. The previous bounded driver explicitly selected 180 seconds. Its
failure cleanup then stopped and removed the 64K container. The original-profile
restoration was left loading when that same short wait failed, allowing it to
complete. The 64K process may likewise have been terminated prematurely; this is
a supported possibility, not proof it would eventually have become ready.

The previous driver saved its 64K startup log only after READY, so that log was
never saved. The original pre-trial container and trial container have both been
removed. A bounded read of retained Docker events returned no historical events
for the relevant interval. There is therefore no complete 32K/64K cold-start
comparison, no measured 64K allocation trace and no evidence supporting a 64K OOM
diagnosis. Only the restored 32K loading interval is measured.

## Resource observations and limits of causal attribution

The unchanged healthy 32K configuration uses the pinned Qwen3.8-27B UD-IQ4_XS
artifact, the existing `b10868-304665fe7` llama.cpp image, all requested GPU layers,
flash attention, q4_0 K/V and one sequence. GPU inspection observed 13,978 MiB
used and 2,073 MiB free on the 16,376 MiB RTX 4090 Laptop GPU, at zero compute
utilization. This is an idle point observation, not a 64K allocation measurement.

The restored process retains a resident high-water mark of 14,283,948 KiB
(approximately 13.6 GiB), while current RSS was about 1 GiB and process swap zero.
The Docker/WSL VM reports about 15.48 GiB total memory. Its current available
memory is high after initialization. Windows reported about 3.15 GiB physical RAM
free and about 9.2 GiB free virtual memory in the richer diagnostic snapshot;
availability varied between snapshots. These are current observations, not
historical pressure measurements during the earlier 64K load.

The large temporary resident footprint makes host/WSL memory pressure and
weight-loading/I/O delay plausible contributors. The retained log has a long
interval inside model loading before threadpool/slot initialization, but lacks
per-stage allocation and transfer timings. It cannot attribute that interval
among disk/cache behavior, scheduling, weight transfer, CUDA setup and K/V
allocation. The unused-tensor messages explicitly say those tensors are ignored;
they are not allocation-failure messages. A timeout alone proves none of these
causes. No speculative cache deletion, image rebuild or serving-variable search
is justified by the available evidence.

## Frozen prospective operational plan

The new plan requires fresh explicit operator consent and exclusive provider
reservation; the previous grant is not reused. It is concretely frozen with
existing model/serving/ModelInteraction owners and these bounds:

- One 65,536-token launch; only context size and its truthful profile label change.
  Same pinned artifact/image, flash attention, q4_0 K/V and one sequence.
- Before interruption: exact configuration snapshot, local image presence,
  bounded artifact SHA-256 verification and repeated idle-state checks. Reading
  the artifact can warm filesystem caches; no controlled cold-cache comparison
  is claimed and no caches are cleared.
- Up to 600 seconds startup observation, informed by the measured 283.7-second
  original-profile restoration rather than repeating 180 seconds.
- At most three neutral inference calls, each at most 180 seconds and 128 output
  tokens. Tokenizer-only preflight froze 511-, 49,152- and optional 62,464-token
  requests, with complete neutral sizes 1,141, 49,806 and 63,118 bytes. Reserved
  generation capacity is 2,048 tokens with at least 1,024 safety tokens. The
  actual tested output cap remains 128, not a sustained 2,048-token benchmark.
- First probe asks for a native `read_source` proposal against a fictional fixture;
  no Tool operation executes. Longer probes request a neutral bounded numeric
  response and do not assess engineering competence or long-range retrieval.
- Optional near-window probe only after healthy preceding probes, adequate time
  for restoration and at least 512 MiB free VRAM. No uncertain inference replay.
- Fifteen-second diagnostic snapshots retain process/container state, HTTP
  readiness, GPU allocation/utilization, Docker CPU/memory/I/O, Windows RAM/commit
  availability, process RSS/high-water/I/O and cgroup pressure/OOM counters.
  Full timestamped logs are retained before any stop, including unsuccessful loads.
- Existing nonstreaming `LlamaCppInteraction` performs inference. The bounded
  observer retains raw returned provider timing fields where available without
  inventing first-token timestamps. Prompt-cache reuse must be reported.
- Mandatory exact 32K restoration, reserving 600 seconds inside the 1,800-second
  overall window. A credible original-profile loader is not repeatedly killed
  when a wait expires. Observe only within remaining authority, retain its actual
  state and report blocked restoration if the overall bound is reached.

Persistent 64K adoption, 96K/128K trials, offload/cache changes, downloads, coding
tasks and B-0049 dispatch are outside this approval. The original 32K provider
with larger independent native byte budgets, actual token measurement,
deterministic projection and precise navigation remains the supported alternative.
The frozen B-0049 reconstruction already fits that combination; its consumed slot
does not become reusable.

## Execution disposition

The service trial remains unentered pending fresh operator approval. No production
executable source changed. Operational results and publication identities are
recorded separately when the approval decision and assessment are complete.

At this publication checkpoint, fresh approval was requested but not received;
the previous service grant was not reused. There was no new container launch,
stop, reconfiguration or inference. This is not an operator refusal or a failed
64K inference result. The original 32K service remains the working baseline.

The [authenticated diagnosis receipt](code-audit/qwen64-operational-diagnosis-20261101.json)
preserves the original timestamped loading log, resource observations, count
reconciliation, exact prospective requests and prepared bounded driver. That
preparation is not execution authority. A later approval must confirm current
provider reservation and bind the same exact plan before any effect.

Focused validation passed 249 distinct tests: eight compatibility tests in 0.294
seconds command time, 42 Context/profile tests in 14.489 seconds and 199 existing
provider/serving tests in 1.475 seconds. These were maintained targeted, no-coverage
runs, not live inference or a new global coverage claim. The docs-only impact
preview initially refused to infer sufficient tests; an explicit provider test
selection was then recorded. No comprehensive suite was rerun for count analysis
or this operational assessment. Existing protected evidence is retained only for
authenticated unchanged executable inputs; production coverage policy is unchanged.

The native profile cannot yet claim a qualified 65,536-token provider. A fresh,
approved task can use the known 32K provider with larger byte allowance, measured
input-token fit, finite generation reservation and existing projection/navigation.
The 1 MiB native capture ceiling still applies: eight fully populated 128 KiB
requests alone consume that entire allowance before responses or other evidence.
Task budgets must reserve capture room rather than assume every large request can
be retained. No new capture store, compaction mode or source ledger was added.

The next bounded action is the prepared coordinated 64K trial with fresh consent,
not another framework implementation or a 96K/128K parameter search. No actual
64K memory headroom, long-request latency, throughput or Tool-call result was
measured in this assignment, so neither larger context is operationally justified.
B-0049's original task and consumed dispatch remain unchanged.
