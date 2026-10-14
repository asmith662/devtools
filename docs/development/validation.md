# Development validation

## Protected development test profile

Run the ordinary repository test suite with:

```text
uv run python scripts/validate_development.py
```

The command runs pytest against `tests/` and ignores `tests/experiments/` before
recursive collection. The experiment test tree contains retained replay and
outcome-dependent tests alongside other experimental checks, so the protected
profile excludes the tree by its repository role rather than inspecting test
names, retained data, or confirmation outcomes to decide what to run. The
ordinary production, unit, integration, and operational-script tests outside
that tree remain in scope. Case 0003 additionally named its capture and
synthetic protocol tests explicitly for that experiment; the general profile
does not carry those case-specific additions.

The profile uses the project pytest configuration without overriding it. This
preserves strict configuration and marker checks, branch coverage, and the
100% production coverage threshold. Pytest's exit code is returned by the
command, so a failed test or coverage gate fails the command.

This profile validates development behavior. It does not validate confirmation
judgments or retained outcomes. Confirmation validation is a separate activity
that requires explicit authorization and a separately reviewed invocation.
Never remove the experiment-tree exclusion to make this profile pass.

## Other quality gates

The protected command runs tests only. Run the applicable static checks as
separate commands:

```text
uv run ruff check .
uv run ruff format --check
uv run mypy
git diff --check
```

When changes are staged, also run `git diff --cached --check`. This profile is
test selection, not a general validation pipeline or confirmation mechanism.

## Approved experiment-controller validation tiers

The [experiment controller](../../experiments/orchestration/README.md) automates
fixed scientific checkpoints without changing the protected production profile.
For experiment-only intermediate PACKET, B and C publications, focused stage
contracts, deterministic validation/replay, sealed integrity and declared focused
suites are sufficient. These are CHECKPOINT validations; LOCAL checks support
implementation work. They do not justify bypassing a failed scientific validator.

Final D publication requires FINAL: complete experiment verification, the full
protected development command above and supported-source static checks, once at
that boundary. The controller's mandatory static floor is Ruff over `src`, `tests`
and `experiments/orchestration`, strict mypy over `src`, protected `tests` (excluding
`tests/experiments/`) and `experiments/orchestration`, and formatter verification
of `experiments/orchestration`. The approved plan additionally freezes complete
verification and applicable static checks for active experiment adapters.
Immutable imported scientific builders and retained historical programs are inputs,
not supported implementation source to normalize or lint retrospectively. Unchanged
production formatting is not rewritten by an artifact publication. Changed
production source retains its applicable formatting checks. Any change under
`src/devtools/` also requires FINAL before publication.
Controller engineering increments themselves run protected development validation
before their final publication. No tier relaxes the production branch-coverage
gate or authorizes confirmation, live models or historical scientific deep replay.
An execution-approval-only publication adds no source or scientific result. Its
bounded checkpoint checks authenticate the committed prospective plan, exact
Stage A and implementation/disclosure hashes, authority schema/digest and clean
synchronized Git state. Approval commit/push must authenticate before scientific
entry. It does not repeat the protected suite or launch a worker. Changes to the
approval implementation itself remain controller engineering changes and require
the full protected profile before publication; final D validation is unchanged.
The synthetic temporary-repository fixture replaces framework validation only in
its test subclass; the shipped controller always schedules the mandatory commands.

Scientific run payloads additionally use explicit Git data attributes to retain
original CRLF and meaningful whitespace. Their byte hashes, schemas and
stage-specific deterministic validators remain mandatory; imported data are not
code to normalize. Controller implementation files retain whitespace checks.
