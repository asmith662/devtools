# Flat observed editing: matched development and confirmation

The frozen manifest and task definitions precede inference. Budget: at most eight
runs, 80 model calls, 7,200 worker seconds; each run ten calls, 4,096 output
tokens/call, 900 seconds, original q4/32K/thinking-off server and sampler.
Two development cases compare the improved Devtools interface with scoped Pi
1.3.0: immutable Command arguments and a new lazy conversion API/module/export.
A distinct file-disappearance normalization case is confirmation, run only after
freezing the chosen worker configuration. No tuning to its model result.

Both harnesses use identical pinned source, objectives, oracles, original tests,
Ruff/formatting and strict typing. Devtools allows 24 read/check/API calls plus
three atomic proposals of at most eight flat calls. Pi allows 24 total Tool
actions including edits/checks; both have ten model calls. Interfaces are the
treatment; these action populations are not identical. Two unused slots reserve
conditional independently frozen repair-only work if development produces no
genuine feedback repair. No completed run is blindly retried.

`replace_source(reference, old_text, new_text)` uses short `edit_ref` handles
returned by actual source reads. Paths, exact versions and required API evidence
are resolved by the host. Empty old text means the complete referenced span or
authorized absent file. Nonempty old text remains an exact unique source snippet.
All calls in one assistant response form one atomic proposal through the existing
transaction admission/application implementation. No staged mutation or second
patch engine exists. Native results correlate every provider call; the first
result contains shared validation and subsequent calls reference it.

Historical single-edit/nested contracts and receipts remain supported. References
are task-local observation handles, not replacement RI identities or authority.
Stale, overlapping, malformed, oversized, unobserved or unauthorized proposals
refuse without partial mutation. No suffix trimming or approximate source matching.
`diagnosis.json` distinguishes verified adapter behavior from unavailable historical
pre-decoder evidence. Actual outcomes are recorded after execution.
