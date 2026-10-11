# Case 0013 blind publication validation

The Stage B checkpoint is 2937e49feb566443f943b91267c59b60b2c7494a.
Its complete immutable native-value reconstruction passed without treatment
re-execution. All 168 sealed capture files matched physical, staged and
committed Git blob bytes. Stage A remains unchanged.

Pre-execution focused capture/native-routing/durability tests: 103 passed.
Additional authority-tamper regression: one passed. Post-capture focused
capture/packet tests: 33 passed, with the expensive full native reconstruction
test deselected because the capture CLI had just completed that reconstruction.
Standalone packet regressions after the publisher path repair: six passed.
The protected development profile passed: 1,588 tests, two skips, 100% branch
coverage. No confirmation or reserve profile was run.

The first two packet CLI processes stopped before writing packet files because
relative destinations lacked the explicit base required by the canonical path
API. The publisher now uses devtools.core.paths.resolve_path with repository
ROOT as the explicit base. A focused regression proves relative publication
and overwrite refusal. Empty failed-publication directories were preserved in
ignored operational storage. No Stage A or native capture bytes changed.

Two subsequent independent Python processes built exactly equal five-file
packets. PREPARATION.json records all four digest scopes, exact metadata
allowlist, fresh stable destination and standalone validator PASS. Only
original task/obligation/resource semantics enter the packet. No frame,
treatment, purpose, role, query, locator, rank, score, cost or result metadata
is added. Original task/source identifiers remain intact.

Scoped Ruff, formatter check and strict mypy passed. The standalone packet
validator is checked with INP001 excluded because this deliberately flat
five-file workspace is not a Python package; its source is checked normally.
Git worktree and staged diff checks passed before publication.

GOLD=NOT_CREATED. EFFECTIVENESS=UNKNOWN. U3 OUTCOME=NOT_SELECTED.
MODEL=GPT-6 Astra; REASONING=High; reviewer_started=false.
The maintainer reviews Stage B before starting a completely fresh session
inside the prepared sterile workspace. No reviewer was started by this task.
