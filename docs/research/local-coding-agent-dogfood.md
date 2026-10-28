# Real local-model coding-agent dogfood

One fresh bounded task passed through the reusable framework with actual local
inference. Execution baseline `8f1466ec0f7b71984a63cb6b0512d075b8e282a4`; accepted experimental
checkpoint `bfd9aa35a0e0b181a12c203ed022d8bf6203b3bd`, tree `81f47e6aa5ac8b9e968f24779c63ba54f30976f2`. The normal direct-main push was
independently verified against GitHub and Git remote state after actual
requirements inspection. No branch, PR, force operation or model publication
authority was introduced.

The selected existing service was Qwen3.8-27B UD-IQ4_XS through llama.cpp, with
matching profile, 32K context and a native-host verification of the pinned GGUF
SHA-256. It was already READY, was reused without restart/download/tuning, and
remained READY. The frozen task, settings, image/artifact identity and exact
source/oracle hashes are in [the original freeze](../../experiments/local_coding_dogfood/case_0001/freeze.json).

## Result and actual lifecycle

The independently authored stockroom package required canonical-key-aware delivery
deduplication, warehouse-scoped opaque identities, conflict refusal, one-pass
iteration and input ownership. It has interacting event/key/projection modules
plus an irrelevant report candidate. Only projection.py was editable. Before
inference, five focused tests ran with three failures; eight independent held-out
tests ran with five failures. Those exact oracles were frozen before entry and
were not disclosed through the model's Tools.

Request 1 selected three complete exact source reads. Request 2 consumed the
correlated text/snapshot/content/span feedback, then proposed one replacement.
Host readiness and edit admission succeeded; the installed candidate passed all
five focused tests through InspectAndValidateTool. It was archived, known source
was restored, and the worker returned validated/completed/accepted. Separate
grading of the archived candidate passed all eight held-out tests and a fresh
five-test focused check. The read-only verifier independently regraded the same
candidate and checks exact frozen/proposed/applied/restored correspondence.

The four offered operations were read_source, replace_source, validate_candidate
and inspect_and_validate_change. The model selected three reads and one edit;
it selected neither validation operation. The repository procedure participated
through deterministic host validation. Passing feedback was retained but was not
sent in another model request. The configured one-repair opportunity was unused;
live repair competence is not established by this result.

Actual usage: two inference calls, 2,797 input tokens, 521 output tokens, 3,318
total. Cache/reasoning counts remain unknown. Provider elapsed times were
38.185245s and 16.103570s; coding worker 55.298485s and complete controlled
evaluation 56.236926s, within the frozen 900-second outer limit. Limits were five
requests, two proposals, eight acquisition actions, 4,096 generated tokens/request,
28,160 measured input tokens inside 32K, and 180 seconds/request. No limit or task
requirement changed after output, and there was no model fallback or rerun.

## Reuse, diagnosis and limits

The existing coding process, RepositoryCodingHost, ModelInteraction/native Prompt,
Model/Tool composition, RI/Context, SourceScope/ScopedSourceTool, ToolRunner,
exact edit/custody mechanics, fixed checks, Commands and Filesystem performed the
work. Experiment-only host composition exposed the command procedure through the
existing CodingHost seam without a second coding/repair loop. There was no
demonstrated production defect or necessary production correction. Framework,
application, tests and configuration stayed unchanged.

Pre-freeze setup corrections were an experimental import-path issue and an
inefficient Docker checksum path. A diagnostic one-liner also had a syntax error.
The Docker read timed out while its hash process remained alive; the exact owned
read process was cancelled, preserving the server, and native-host hashing of the
same read-only mount succeeded. These were not model failures or corrected
follow-up model attempts. Publication uses a scoped cr-at-eol attribute to preserve
original CRLF evidence bytes while retaining whitespace checks; no original
scientific input/output was normalized.

Seventeen selected primary command observations/patterns retain normalized family,
roles, provenance and known results; private argv/output/env analytics are absent.
Bounded synthetic test diagnostics and model source/calls are separate retained
experiment records. No personal logs, credentials or cloud inference were used.
The default unobserved model adapter and ModelInteraction observation-policy
decision are unchanged. This is not complete global event capture or durable
task recovery. Scoped Tool admission is not OS isolation of adversarial Python
candidate code; no such sandbox claim is made.

## Validation, custody and next work

Committed-checkpoint protected command: `uv run python scripts/validate_development.py`.
Result: **3,640 passed, two optional live skips**, exit 0, 100% configured production branch coverage,
1453.050107s. All 923 captured physical inputs, including the
new frozen collection, stayed unchanged through validation/publication. Maintained
Ruff/formatter/configured strict mypy and layout passed. The experimental host and
verifier compiled and passed scoped import/syntax hygiene; the evidence verifier
and independent regrade passed. The production gate does not measure live model
competence or claim full experimental coverage. Exact commands/times/exit codes,
blobs, input hashes and preservation checks are in the [machine receipt](code-audit/local-coding-agent-dogfood-20261028.json).

All 13 forensic records, 903 RI ledger rows, 68 Intake chains and authored historical
refs are preserved. The 188 historical RI-version obligations, A+C, observation
Option B, durable Evidence/recovery and broader agent obligations remain open.
Existing B-0043/B-0035 receive advisory empirical evidence without status,
approval, grant or parent closure. Original experiments and sealed evaluations
were neither rerun nor reclassified.

The highest-leverage next evaluation is a separately authorized harder task
requiring source-discovery choices and, if naturally necessary, real failed-check
feedback consumption and bounded repair. The frozen artifacts and oracles are reproducible; a new stochastic generation
is not asserted to reproduce these output bytes, and no seed guarantee was
recorded. This sample had a host-selected small
corpus/owner and solved the task on its first edit. Do not infer general
effectiveness, autonomous planning or repair ability from that success, and do not
add infrastructure solely to make the model appear to select more Tools.

See [the case report](../../experiments/local_coding_dogfood/case_0001/REPORT.md),
[collection manifest](../../experiments/local_coding_dogfood/manifest.json), and
[safe provenance/regrade instructions](../../experiments/local_coding_dogfood/README.md).
