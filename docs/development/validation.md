# Development validation

> WorkCycle/delegation/integration fixtures now use tiny authored repositories
> and ordinary branches in one checkout. They create no linked worktrees or
> Devtools source-tree copies. The normal protected profile applies unchanged.


## Everyday development and failure recovery

Use `uv run python -m scripts.validation` with an explicit mode and a fresh
`--output .local/validation/<name>.json`. Without `--execute`, it saves a plan.
No missing selection ever defaults to comprehensive testing.

| Mode | Example arguments after the command | Purpose |
| --- | --- | --- |
| targeted | `targeted --test tests/core --execute --output .local/validation/core.json` | Explicit tests or inferred owning tests, without coverage |
| impact | `impact --base HEAD --output .local/validation/impact.json` | Explain changed paths, owning packages and static consumers |
| recover | `recover --previous .local/validation/core.json --correction "fixed boundary" --test tests/core --execute --output .local/validation/repair.json` | Failed IDs plus correction impact; original result retained |
| comprehensive | `comprehensive --execute --output .local/validation/final.json` | Exact protected profile, with phase timing and input receipt |

Selections use current Python AST imports, transitive reverse import consumers,
whole owning test packages and declared coding/Tool/Checkout integration groups.
They do not use lexical similarity or retrieval ranking. This operational
heuristic avoids building RI indexes: RI's qualified static facts also cannot
establish runtime dependency closure. There is no historical per-test coverage
context map to authorize finer selection. Changes include the base-to-working
tree diff (including index), deleted paths and executable untracked files;
`--changed` adds declared paths for scenario previews. Renames are treated as
deletion plus addition. Public facades, fixtures, non-Python configuration,
dependencies, missing owners and dynamic execution produce explicit uncertainty.
Automatic uncertain execution is refused. Review the plan and supply explicit
`--test` groups or deliberately choose comprehensive validation. Explicit groups
remain local checks and do not resolve uncertainty or authorize publication.

Static analysis cannot prove monkeypatch, reflection, subprocess, plugin or
runtime-configuration dependencies. Maintainers must include relevant contracts
and broaden uncertain or architectural changes. Package/layout/global-fixture,
shared protocol and validation-policy changes require the final protected gate.
All ordinary final publications still require that gate; this amendment changes
the development loop, not release assurance. WorkCycle and integration's fixed
validators and fresh-only acceptance remain unchanged.

After failure, retain the original receipt and inspect phase failures. Assertion
and fixture failures have node IDs; collection, configuration, interruption,
internal errors and empty selection are distinguished. Exit 1 without a failed
phase can mean the coverage gate failed. Diagnose those conditions and explicitly
select the necessary group; do not pretend they are assertion failures. Name the
actual correction or new diagnostic purpose, rerun failed IDs and correction
impact, then broaden only for a concrete reason. The tool never automatically
retries. A terminated process may leave only its intent: that is unknown, not
passing evidence. Run comprehensive validation on the final committed stable
candidate. If it fails, repair using focused tests before another final run.

Comprehensive mode starts a fresh managed Python interpreter so framework import
statements are instrumented from first import. Coverage data and child output
are retained beside the unique receipt; `COVERAGE_FILE` is explicitly redirected
there to prevent nested coverage checks from replacing another invocation's data.

Receipts retain argv, changed paths, selection reasons/uncertainty, phase outcomes,
failure text, setup/call/teardown durations, native exit, wall duration, Git HEAD,
index blobs, physical SHA256 inputs, Python/platform, installed distributions and
an inherited-environment fingerprint (values are not disclosed). Before/after
comparison rejects input drift. Tracked files outside executable/configuration
scope, ignored configuration, services and external inputs are not authenticated
closure. Receipts are local observations, not new durable framework schemas.
Previous results may inform diagnosis and timing; acceptance remains fresh-only.
Matching declared inputs do not establish external equivalence. Omitted tests
are not passed and partial tests never establish global coverage. Recovery links
the previous receipt and leaves its comprehensive failure intact.

Pytest's existing cache may assist manual `--lf --lfnf=none --no-cov` diagnosis,
but is not input-authenticated evidence and is not used to manufacture a pass.
The maintained recovery command uses saved IDs rather than mutable cache state.
No third-party pytest dependency, worker pool or shared service is added. Phase timings are retained
for future measured fixture optimization. See [delivery evidence](intelligent-validation.md).

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

### Freshness and reusable claims

The fixed integration validator records a fresh command invocation, not complete
transitive file, toolchain or environment closure. Its reports declare
`reuse_policy: fresh-only-v1`. Local closeout cannot reuse a saved passing result
to authorize a new feature commit; it reruns protected validation. An unchanged
Git tree does not authenticate ignored configuration or installed dependencies.
Existing scoped CodingCommands `is_current` reuse is a different claim and remains
available for unchanged declared inputs; it confers neither independent review
nor publication authority. See the [local integration contract](../backlog/integration.md).

Pre-commit validation is not proof of HEAD-sensitive post-commit behavior. A
delayed local push validates the exact existing commit. Developer production
repairs must run their final protected gate on committed executable inputs and
authenticate those inputs through publication; broader HEAD/toolchain closure
remains an explicitly tracked obligation.

Run `uv run python scripts/validate_layout.py` for canonical root ownership.
Default strict mypy checks maintained framework, tests and applications;
retained experiments/generated programs and `tests/experiments/` have explicit
experiment-specific checks. This avoids interpreting immutable generated
scientific builders as duplicate supported modules. The protected pytest
profile and 100% production branch-coverage requirement are unchanged.

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

Active experiment adapter static commands must name deterministic maintained
implementation file addresses. LOCAL, CHECKPOINT and FINAL must not recursively
discover `runs/`, generated PREPARATION/PACKET programs or immutable primary bytes.
Generated payloads retain packet schemas, exact byte identity, hashes, standalone
validators and deterministic replay; excluding them from implementation style
checks does not waive scientific validation. The source-grounding scope regression
materializes hostile generated payloads and verifies maintained defects still fail.
