# Native coding cohort 02

Two fresh host-frozen cases exercise source/value consistency and command-output
configuration admission. `manifest.json` binds baseline, task/oracle identities
and the cumulative 20-request / 1,800-second live budget. The existing worker
retains 10 requests, eight reads, three proposals, 4,096 output tokens and 900
seconds per case. No paid model comparison is authorized.

`regex-span-consistency` is development; `command-output-integer-limits` is held
out until development changes are fixed. Both require original regressions,
independent acceptance, scoped Ruff and formatting. Baselines must pass existing
tests and fail their oracle before inference. No solution is included in prompts.
These are two small maintenance cases, not a representative proficiency estimate.

Use the existing direct runner, for example:

```powershell
uv run --python C:/Python314/python.exe python scripts/qwen/coding_worker.py --task-definition apps/qwen/evaluation/native-cohort-02/regex-span-consistency.json --report-directory .local/qwen-coding-worker/native-cohort-02/development/regex-span-consistency
```

Raw evidence and deterministic archived-CSV replay are under the ignored
`.local/qwen-coding-worker/native-cohort-02/`. Historical cohort 01 stays unchanged,
including the duration behavioral candidate requiring style rework. Accepted local
results remain review candidates without production integration authority.

## Recorded outcomes

Worker `111975be67f97f4095674d5a37e680ad05097f94` ran both cases unchanged.

| Case | Final disposition | Model calls | Input / output tokens | Worker seconds |
| --- | --- | ---: | ---: | ---: |
| Regex span consistency | ACCEPTED (tests + oracle + Ruff + format) | 4 | 15,893 / 773 | 45.31 |
| Command output integer limits (held-out) | REPAIR_BUDGET_EXHAUSTED | 7 | 37,972 / 1,312 | 77.31 |

The regex result passed seven existing tests and eight independent consistency
scenarios plus a public-search assertion; independent strict mypy also passed
using a read-only shadow file. Its exact candidate SHA-256 is
`42430b144215d244ff97f189377b3bdd18765dddbfad5c65381a96dfbe69ce91`.
It remains an evidence candidate, not maintained source or a protected publication.

The held-out first proposal passed 22 independent scenarios and ten regressions
but failed Ruff TRY004 (prefer TypeError for invalid types). Its first repair
changed ValueError to TypeError and broke the task's required ValueError contract.
The final repair added an unused hybrid exception class without changing the
raised TypeError. Ruff/format/tests passed; the oracle still failed. This is a
real bounded repair failure under a host-defined exception-contract/lint tension.
The tension should have been flagged during task preparation; it confounds a clean
model-competence interpretation. The frozen checks and failed outcome remain
unchanged. No held-out-driven worker tuning, extra attempt or replacement code ran.

All four admitted edits were grounded in actual current source in the model's
active input. Independent deterministic reconstruction reproduces their exact
recorded final source bytes. Both runs omitted zero exchanges; peak observed
input occupancy was 21.43% and 26.90%. The held-out recovered one invalid version
and two out-of-bounds reads, then read current edited source. Source and diagnostics
were visible when repairs failed. Conservative file-version invalidation may
require reacquisition of unchanged regions; the worker does not infer their
continued validity.

Total: 11 requests, 53,865 input / 2,085 output tokens, 122.62 worker seconds
(116.83 summed model wait, 3.84 validation), 12 Context actions (nine returned,
three refused), four admitted proposals, two unsuccessful repair cycles.
Raw acquisition disclosed 10,893 cumulative source bytes; repeated/edited versions
are not a unique-repository-byte count. Cache, reasoning, energy and Codex
coordination consumption remain UNKNOWN. No paid model baseline was invoked.

Archived CSV replay retained all observed source in 33,013 / 33,367 bytes, versus
the historical selector's 16,429 / 19,553-byte requests with missing code. This
demonstrates harness retention, not a rerun or improved model success rate.
Fresh cases are small and different from cohort 01, so outcomes are not a matched
before/after comparison. Successful live behavioral repair and general proficiency
remain open. The duration behavioral/style-rework candidate is preserved unchanged.

Next: preflight task exception/lint contracts, then use fresh multi-region tasks
to measure requirement-preserving repair and avoid version-dependent calls before
versions are known. Do not weaken prior acceptance or tune to this held-out case.
A fair Codex comparison needs separately budgeted, solution-isolated paired cases.
Qwen remains the primary workstream.


Final engineering verification: 2,030 protected tests passed, two skipped,
100% production branch coverage (445.74 s); configured strict mypy passed 478
files, scoped Ruff/format and layout checks passed. The earlier full run exposed
one obsolete delegated fixture that proposed after search without a source read;
the fixture now reads the authorized target and the final gate passes. Production
authority semantics were unchanged. No scientific-controller suite was run.
