# Bounded coding continuation

WorkCycle's native owner administers distinct coding episodes under one canonical
engineering obligation. This differs from intra-episode edit/check/repair and
read-only reviewer continuation. Runtime and ModelInteraction gain no orchestration.

Historical assignments remain attempt 1 in their original directory.
`cycle.native.select(n)` addresses prospective children at
`.local/backlog/work/B-NNNN/attempts/NNNN/`. Each has an immutable assignment
content hash, source snapshot, actor/source/profile, finite budgets, grant,
dispatch, candidate, observations and terminal custody records. Children bind
the exact predecessor assignment/result and preserve task obligations, private
acceptance, source/read/check scope and inputs. A worker, settings and budgets
may change within current authority. Consumed slots remain immutable.

`routine-development-policy-v2` adds `coding_attempts`, a total ceiling from 1 to
100 including the original; v1 retains one slot. Increasing this finite ceiling
requires explicit policy replacement, without an executable change. The initial
two-attempt [policy](routine-coding-continuation-policy.json) was activated as
`08fcfcbfda2e51db7a7fb61a5cdd923deec75ebbff4cdad4b8e9f4520fa33662`.
Provider/profile, source, resource, Git and validation limits remain unchanged.
The local control chain is authority; this published policy transfers no grant.

## Initial eligibility

The supervisor selects an authenticated terminal public-validation failure:
`proposal_limit`, completed, no execution/completion error, complete final failed
public checks, acknowledged effects, authenticated candidate/diff and observations,
restored original source and authenticated Checkout release. The task must remain
reviewed BACKLOG with current source, tests, configuration and obligations intact.
Unknown effects, tampering, custody conflicts, authority/security errors, closed
tasks, exhausted limits and revoked current policy refuse. Historical grant
dispatch/observation times must be within its validity interval; that grant is
evidence only. A fresh current grant governs the child.

```python
child = await cycle.native.prepare_continuation(
    item, attempt=2, policy=active_policy, branch=existing_task_branch,
    task=selected_task, supervisor=supervisor_reference, disclose_public=True,
)
owner = cycle.native.select(2)
grant = await cycle.routine.authorize_native(
    active_policy, item, attempt=2, assessment=assessment, provider=qualification,
)
result = await owner.execute(
    item, interaction=selected_model, profile=selected_task["worker"]["profile"],
    authorize=cycle.routine.callback(grant["reference"]),
)
```

Preparation grants no effects. Existing authority, guarded coding host and Checkout
recheck the child/predecessor at governed boundaries. `native-continue` prepares;
`native-preview --coding-attempt N` inspects. Trusted hosts inject execution
collaborators. Eligible policy-derived grants require no interactive task approval.
Children reject manual grants at issuance and effect admission; historical root
manual-grant compatibility remains intact.

The supervisor selects disclosure explicitly. Default feedback is a factual public
failure summary; `disclose_public=True` also selects complete final public-check
output. Selection is immutable and grant-bound. Private oracle implementation,
acceptance diagnostics, preflight controls and privileged host records are excluded.
Each child acquires current source anew; no old source witnesses or Conversation
are replayed. Previous candidates remain archived.

Each attempt uses the same ModelInteraction/coding contracts. Alternate scripted
models establish deterministic mechanics, not live competence; routine execution
still requires approved providers/profiles. Acceptance/review and Integration
remain separate. This increment adds no automatic installation or completion.

Future private-acceptance continuation requires separately approved diagnostic
disclosure and private-oracle confidentiality. The identity/administration contract
does not assume public failure permanently; only initial eligibility does.
Strategy replanning, scheduling, automatic selection and legacy-worker continuation
remain outside this increment.

## Validation and implementation provenance

Codex direct maintenance implemented this slice at `d3d2733d` and corrected the
child-grant restriction at `c2651baeb63dd25b1e84e66910b33a8eec7a7d3a`.
The manual-child-grant regression failed before the correction and passed after
it. The initial protected run was deliberately interrupted for that correction;
it is not passing validation evidence.

The final 18 focused regressions passed. The unchanged protected profile,
`uv run python scripts/validate_development.py`, then passed on exact commit
`c2651baeb63dd25b1e84e66910b33a8eec7a7d3a`: **4,334 passed, 2 skipped**, with
100% configured production line/branch coverage in 4,464.92 seconds. Pytest cache
bookkeeping was disabled and tracebacks shortened to avoid the previously
observed memory failure; test selection and coverage policy were unchanged.
Maintained backlog source/test Ruff and formatting checks, strict mypy (634
source files), layout, diff and Git connectivity checks passed.

The full log and receipt are retained locally at
`.local/validation/b0033-protected-c2651bae.log` and
`.local/validation/b0033-protected-c2651bae-result.json`; focused results are in
`.local/validation/b0033-policy-guard-focused.json`. These deterministic tests
establish ownership mechanics. No live Qwen episode or review was dispatched.
