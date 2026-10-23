# Retained binding verification v1

`verification_v1.py` is a maintained, experiment-specific read-only analysis
adapter added after the original study. It is not part of the original sealed
treatment, collection manifest, adjudication protocol or published reports.
Those files and their historical behavior remain unchanged.

The original `unblind_records` checks bijection and set membership but does not
reconstruct each canonical address/neutral-ID pair. The original Increment24
loader also uses positional joins. Do not use either unchecked entry point as
the integrity boundary for new analysis.

Use `verified_unblind_records` for an existing native captured-case frame, or
`verify_artifact_bindings(capture=..., package=..., mapping=..., frozen=...)`
for the four already parsed retained artifact envelopes. Both return the
existing `UnblindedAdjudication` representation, preserving original records,
unjudged values and frozen fingerprints. They never acquire source, run a
retrieval policy, regenerate ranks/metrics, adjudicate, write files or publish.

Supported artifact versions are hidden capture v1, neutral mapping v1, corrected
blinded package v2 and frozen adjudication v2. Older, invalidated, incomplete or
inconsistent artifacts fail closed with `ValueError`; there is no automatic
repair or migration. Canonical material membership/order and the frozen
producer's exact neutral-ID preimage are reconstructed. Existing package/freeze
loaders authenticate their internal identities. The new adapter additionally
checks capture/mapping set identities, canonical pairs, positional order,
question/frame and address visibility.

**Internal consistency is not independent provenance authentication.** Before
using supplied envelopes, authenticate original bytes against independently
retained hashes/custody. Rehashing altered payloads does not make them original.
This verifier establishes no correctness of the human judgments, scientific
effectiveness, current source freshness or execution/publication authority.

The audit authenticated the original four archive members against the existing
archive manifest and verified all96 original pairs across six cases without
rerunning judgment or ranking. The observed synthetic weakness is not evidence
of historical corruption. Evidence and remaining compatibility limits belong in
the current RI audit report; the original study remains historical.

Permanent tests in `tests/experiments/purpose_relative_admission/test_verification_v1.py`
use synthetic producer frames and independent adversarial swaps/reordering.
Run these with `uv run pytest --no-cov` and the exact test path. Do not run the
outcome-dependent report tests or old study controllers to validate this adapter.
Scoped Ruff/formatting and strict mypy apply to the two new Python files, with
`--follow-imports=silent` retaining the frozen dependency implementations.

This is not a controller engineering change: no scientific dispatcher or
production `src/`, `apps/`, `scripts/` or protected test file changes. The bounded
deterministic/static/integrity checks apply; the protected production gate is
not rerun for this experiment-specific verifier. Its existing100% coverage
requirement and experiment-test exclusion remain unchanged.
