# Static dependency groups: prospective qualification

This is a new B-0002 implementation task, not a retry of SnapshotDelta or an
earlier Commands task. The existing settings/declarations/models owners and
public analysis/resolution APIs own the change. No new resolver, installer,
requirement parser, TOML parser or public type is needed.

Before inference, the complete existing project-configuration suite passed:
126 cases. Fixed focused task tests cover configuration and obstruction
behavior; the existing settings tests remain visible as public API examples.
One legacy settings assertion counts exactly 17 absent keys. The deliberate
coverage expansion adds the dependency-groups table, making this 18. That
assertion will be independently adapted after the model attempt; no old key or
behavior is removed. Declaration derivation deliberately advances v3 to v4,
and descriptive analysis coverage advances v2 to v3.

The oracle uses actual installed tomllib and the existing public analysis and
resolution helpers with retained repository observations. Every positive and
negative fixture parses and has independently asserted literal keys/string
values before RI assertions run. Baseline fails at `missing static
dependency-group declarations`, rather than an import, fixture or exception
failure. Ruff, formatting, strict source typing and the frozen regression
selection pass in the existing runner preflight. Engineering review considers
this small finite raw-syntax contract realizable, not mechanically proven.

An initial *pre-inference* preflight caught a Python quoting error in the
oracle's marker fixture. It was corrected before freezing the final identities
in manifest.json; both preflight receipts remain in ignored raw evidence. No
inference was spent on the broken oracle.

The specification references are [PyPA Dependency Groups](https://packaging.python.org/en/latest/specifications/dependency-groups/),
[PEP 735](https://peps.python.org/pep-0735/) and
[name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/).
The supported subset retains ordered raw strings, duplicates, exact original
names and empty groups. It makes no PEP 508 validity, installation or
importability claim. Include-group and mixed/object arrays remain qualified
unsupported in their entirety; supported siblings survive. ASCII name grammar
and normalized collisions are assessed, original semantic keys retained.
Colliding groups are all unsupported with no interpreted value, never merged.

Three existing source files (5,464 / 4,524 / 6,456 bytes) are editable. The
settings insertion and two version changes fit small exact regions within the
unchanged 4,096-byte region, 8,192 aggregate and 16,384 patch limits; whole-file
replacement is unnecessary. Related resolution/exports/public tests are
readable. Private oracle and test additions are not in the model read corpus.

The final frozen task permits 24 requests, 1,800 worker seconds, six proposals,
16 components per proposal and 32 read/check actions, with 8,192 output ceiling
and the existing exact capacity policy. No eight-response cutoff or automatic
recovery is used. Model profile remains Qwen3.8-27B IQ4_XS, 32K, q4 K/V,
thinking off. Native check_changes is enabled, with existing host freshness
authentication before acceptance. No worker/serving changes are part of this
assignment.
