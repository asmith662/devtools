# Captured-input Stage D analyzer

This non-installable experiment owner consumes committed sealed Stage B and the
sole authoritative primary per case at Stage C import checkpoint
`2a93f91d96ebd8deb927550822e4e2c40f2bd1db`. It introduces no framework abstraction,
public API, persistence contract, ranking or production behavior. Dependencies
are the existing experiment artifact/normal proof substrates and the unchanged
Stage A ordinal decision functions. It never invokes scientific acquisition,
Reference derivation, PPR, RRF, a model, historical child access or holdout access.

Run `uv run python -m experiments.structural_discrimination.stage_d.analyze build`
once. BUILD preflights all output directories and refuses overwrites. Run
`uv run python -m experiments.structural_discrimination.stage_d.analyze verify`
in a separate process: it freshly authenticates Stage A, the normal sealed Stage
B proofs and committed primary bytes, reconstructs every output and requires
byte equality including integrity/source/input hashes. After publication,
`verify --checkpoint COMMIT` additionally anchors all result bytes to Git.
No deep replay fallback exists. Operational validation receipts are separate
from scientific output and never rewrite primary judgments.

Case-owned `stage_d/` folders retain analysis, all pair traces, validation and
integrity. `results/` owns cohort analysis/review and import authentication.
Every projected cell points to its original immutable primary. Semantic units,
spans, alternatives and witnesses remain in the primary. Case 0019 sufficiency
and indispensability stay conditional on future provider-contract semantics.

Tests mutate synthetic/copy inputs and derived outputs, never scientific files.
Frozen category boundary tests reuse the Stage A decision contract. All results
are development diagnostics; no retrospective threshold or cohort gate exists.
