# Native CSV-row end-to-end episode

## Approved preparation

Human Intake review approved B-0052, proposal `1caa2686-428f-4fdf-b052-f0b8382b44dc`,
under exact scope `e1beb6eda22046715abe3653b6f81e187e06aeb4d550c2b87f7af6310db94721`.
The [frozen record](code-audit/e2e-native-csv-20261102/frozen.json) authenticates
the original source and acceptance bytes; the [review](code-audit/e2e-native-csv-20261102/intake-result.json)
preserves the actual default-No approval. Preparation grants no coding effects.

The exported standalone `CsvRow` accepts exact duplicate headers: keyed lookup
returns the first cell while `as_dict()` retains the last. File/codec constructors
already refuse ambiguous headers. This newly reproduced model admission defect
is distinct from the delivered NONNUMERIC codec repair and the open Python-scope
obligations B-0049/B-0050/B-0051.

Only `src/devtools/resources/filesystem/models/csv.py` may change in the proposed
native episode. Reject exact duplicate names with `ValueError`; retain case,
spacing, Unicode spelling, order, immutable storage, widths, string cells and
all existing unique-name behavior. Empty standalone rows and unique blank names
remain outside the repair. No host reference implementation was authored.

Frozen public acceptance produced three intended duplicate-header failures and
51 passes (82.16 seconds). Independent predeclared holdouts cover permutations,
iterable capture and exact Unicode distinctions, with valid-input controls.
The [supervisor-only packet](code-audit/e2e-native-csv-20261102/supervisor-task.json)
contains withheld acceptance; neither its implementation nor host scoring may
enter the coder or reviewer Context. The [public checks](code-audit/e2e-native-csv-20261102/public.py.txt)
are prospective task inputs, outside normal test discovery until integration.

The proposed one-episode policy uses existing native WorkCycle and
`native-context-v1`: eight model calls, six acquisitions, three proposals,
120 seconds/call, 900 seconds total, 2,048 output tokens/call, 128 KiB requests,
960 KiB native capture plus 64 KiB supporting observations. Actual provider-token
fit, deterministic projection, read/edit witnesses, managed checks and source
restoration remain mandatory. Native portable requests do not override sampling;
the observed server defaults include temperature 1.0.

No production executable change, live inference, candidate acceptance, reviewer
dispatch, integration, installation or closeout is claimed by this preparation.
Coding and reviewer authority remain separate exact-subject decisions. The
persistent 64K service and independent Inspector worktree must remain unchanged.
