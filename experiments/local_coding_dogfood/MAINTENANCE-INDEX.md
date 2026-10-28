# Real local-model maintenance observations

This separate index preserves the original synthetic-case collection checkpoint
and [Case 0001/0002 index](CASE-INDEX.md) byte-for-byte.

| Case | Real backlog obligation | Observed result |
| --- | --- | --- |
| [0003](case_0003/REPORT.md) | B-0035 first-request repository discoverability | Five real requests; Prompt-byte refusal before editing; no production change |

This is one failed real maintenance attempt, not a success-rate estimate. Original
entry records remain closed. Read-only verification:

```text
uv run python experiments/local_coding_dogfood/case_0003/verify.py
```

No model is invoked. Another attempt requires separate authorization and a new
linked freeze; do not overwrite this result or silently substitute a repair.
