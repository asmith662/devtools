# Local dogfood case index

This is a maintenance view, not a rewrite of the original collection checkpoint.
The original README, SUMMARY and manifest retain their single-Case0001 meaning
and exact bytes. New cases have their own frozen inputs and closeout manifests.

| Case | Defined scope | Independent observation |
| --- | --- | --- |
| [0001](case_0001/REPORT.md) | Three prescribed source witnesses, one editable owner | Two real requests; focused and held-out pass; repair unused |
| [0002](case_0002/REPORT.md) | 18 resources, 11 possible editable owners, model-selected discovery | Five real requests; listing/search/eight reads; focused and held-out pass; repair unused |

These are separate bounded observations, not an estimated success rate or a
general effectiveness claim. Case0001's original manifest remains at
[manifest.json](manifest.json); Case0002's separate manifest is
[case_0002/manifest.json](case_0002/manifest.json). Historical results and authority
are not changed by this index.

Read-only Case0002 verification and optional frozen-oracle regrading:

```text
uv run python experiments/local_coding_dogfood/case_0002/verify.py --grade
```

This calls no model. Another inference attempt requires a separately authorized
linked case and a new freeze; do not overwrite closed evidence or entry markers.
