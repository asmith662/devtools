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
