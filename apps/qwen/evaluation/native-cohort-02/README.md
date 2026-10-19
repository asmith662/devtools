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
