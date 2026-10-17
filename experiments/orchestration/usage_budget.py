# Copyright (c) 2026
# ruff: noqa: ANN401, PLR0913, PLR0917, PLC0415, COM812 -- bounded controller admission/measurement composition
"""Reserve declared observed-usage allowances before scientific entry.

This local manifest is not a billing service or execution authority. The
controller supplies already authenticated scientific authority. A crashed
reservation remains charged until explicit reconciliation; no call is retried.
"""

from pathlib import Path
from typing import Any

from devtools.core.time import Timestamp
from devtools.governance.usage import BudgetScope, UsageAmount, UsageBudget
from devtools.models.interaction.usage import ModelUsage
from devtools.observability.usage import Attribution, Purpose, UsageWindow, report
from devtools.observability.usage.collection import reconcile
from devtools.observability.usage.ingestion import from_capture
from devtools.observability.usage.models import UsageObservation
from devtools.observability.usage.storage import load as observations
from devtools.observability.usage.storage import save as save_observations
from devtools.observability.usage.storage import writer
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import load, require, save


def reserve(
    root: Path,
    plan: Any,
    run_id: str,
    case: str,
    stage: str,
    *,
    authorized: bool,
    require_configured: bool = False,
) -> Any:
    """Reserve a complete logical call before ENTERED; reject conflicts/re-entry."""
    if "usage_budget" not in plan:
        return None
    require(authorized, "Budget does not grant scientific execution authority")
    policy = plan["usage_budget"]
    key = case + "/" + stage
    if key not in policy["calls"]:
        return None
    call = policy["calls"][key]
    identity = run_id + "/" + key
    ledger_path = root / ".local/usage/ledger.json"
    path = ledger_path.parent / "reservations.json"
    with writer(ledger_path):
        state: Any = (
            load(path)
            if path.exists()
            else {"schema": "experiment-usage-reservations-v1", "calls": {}}
        )
        require(
            identity not in state["calls"],
            "BUDGET_BLOCKED: invocation already reserved; no retry",
        )
        require(
            not require_configured or ledger_path.exists(),
            "BUDGET_BLOCKED: observed usage ledger required at reservation",
        )
        local = _assess_call(root, policy, run_id, stage, call, state)
        require(
            not require_configured or bool(local["limits"]),
            "BUDGET_BLOCKED: configured policy required at reservation",
        )
        admission = {
            "invocation": identity,
            "run_id": run_id,
            "case": case,
            "stage": stage,
            "model": call["model"],
            "input_upper": call["input_upper"],
            "output_upper": call["output_upper"],
            "settled": False,
            "timestamp": str(Timestamp.now()),
            "policy_sha256": digest(json_bytes(policy)),
            "status": "BUDGET_RESERVED",
            "weekly_limits": "UNSET"
            if not local["limits"]
            else "CONFIGURED_OBSERVED_SCOPES",
        }
        state["calls"][identity] = admission
        save(path, state)
    return admission


def _assess_call(
    root: Path,
    policy: Any,
    run_id: str,
    stage: str,
    call: Any,
    state: Any,
) -> Any:
    """Share existing numeric policy between reservation and read-only preview."""
    own = [v for v in state["calls"].values() if v["run_id"] == run_id]
    require(
        len(own) < policy["fresh_call_limit"],
        "BUDGET_BLOCKED: experiment fresh-call limit",
    )
    require(
        sum(v["model"] == call["model"] for v in own)
        < policy["model_call_limits"][call["model"]],
        "BUDGET_BLOCKED: model call limit",
    )
    return _check_local(
        root,
        run_id,
        stage,
        call,
        state,
        UsageAmount(1, call["input_upper"], call["output_upper"]),
    )


def _observed_for_scope(
    observed: tuple[UsageObservation, ...],
    scope: BudgetScope,
    identity: str,
    model: str | None,
) -> tuple[UsageObservation, ...]:
    """Select reconciled original consumption, retaining relevant conflicts."""
    selected: list[UsageObservation] = []
    for component in reconcile(observed):
        attrs = [component.attribution]
        if component.conflict:
            attrs = [
                (r.original_attribution or Attribution())
                if r.execution_origin == "ADOPTED"
                else r.attribution
                for r in component.observations
            ]
        if (not model or any(r.model == model for r in component.observations)) and any(
            (scope != BudgetScope.PROJECT or attr.project == identity)
            and (scope != BudgetScope.EXPERIMENT or attr.experiment == identity)
            and (scope != BudgetScope.STAGE or attr.stage == identity)
            for attr in attrs
        ):
            require(
                not component.conflict, "BUDGET_BLOCKED: conflicting observed usage"
            )
            selected.extend(component.consumption)
    return tuple(selected)


def _check_local(
    root: Path, run_id: str, stage: str, call: Any, state: Any, proposed: UsageAmount
) -> Any:
    """Apply the existing configured-scope policy without allocating a reservation."""
    ledger_path = root / ".local/usage/ledger.json"
    # Optional local numeric constraints are never silently configured.
    local_path = ledger_path.parent / "policy.json"
    local = load(local_path) if local_path.exists() else {"limits": []}
    applicable = []
    for item in local["limits"]:
        scope = BudgetScope(item["scope"])
        if item.get("model") and item["model"] != call["model"]:
            continue
        if scope == BudgetScope.PROJECT and item["identity"] != "devtools":
            continue
        if scope == BudgetScope.EXPERIMENT and item["identity"] != run_id:
            continue
        if scope == BudgetScope.STAGE and item["identity"] != stage:
            continue
        applicable.append(item)
    require(
        not local["limits"]
        or any(
            any(value is not None for value in item["limits"].values())
            for item in applicable
        ),
        "BUDGET_BLOCKED: no applicable numeric policy for invocation",
    )
    observed = observations(ledger_path)
    if applicable:
        require(ledger_path.exists(), "BUDGET_BLOCKED: observed usage ledger required")
        last = load(ledger_path.parent / "backfill.json")
        age = (
            Timestamp.now().value - Timestamp.from_isoformat(last["observed_at"]).value
        ).total_seconds()
        require(
            0 <= age <= local.get("max_observation_age_seconds", 300),
            "BUDGET_BLOCKED: refresh metadata-only usage baseline before launch",
        )
    for item in applicable:
        scope = BudgetScope(item["scope"])
        model = item.get("model")
        require(
            not model
            or not any(
                g["dimension"] == "model"
                and g["value"] in {"UNKNOWN", "MIXED"}
                and g["fresh_invocations"]
                for g in report(observed, UsageWindow.rolling(Timestamp.now()))[
                    "groups"
                ]
            ),
            "BUDGET_BLOCKED: model attribution UNKNOWN or MIXED",
        )
        selected = _observed_for_scope(observed, scope, item["identity"], model)
        summary = report(selected, UsageWindow.rolling(Timestamp.now()))
        require(
            not summary["conflicting_invocations_excluded"],
            "BUDGET_BLOCKED: conflicting observed usage",
        )
        consumed = UsageAmount(
            None
            if summary["unallocated_timestamp_observations"]
            else summary["fresh_invocations"],
            None
            if summary["unknown_category_observations"]["input_tokens"]
            or summary["unallocated_timestamp_observations"]
            else summary["tokens"]["input_tokens"],
            None
            if summary["unknown_category_observations"]["output_tokens"]
            or summary["unallocated_timestamp_observations"]
            else summary["tokens"]["output_tokens"],
        )
        pending = [
            v
            for v in state["calls"].values()
            if not v["settled"]
            and (not model or v["model"] == model)
            and (scope != BudgetScope.EXPERIMENT or v["run_id"] == run_id)
            and (scope != BudgetScope.STAGE or v["stage"] == stage)
        ]
        reserved = UsageAmount(
            len(pending),
            sum(v["input_upper"] for v in pending)
            if all(v["input_upper"] is not None for v in pending)
            else None,
            sum(v["output_upper"] for v in pending)
            if all(v["output_upper"] is not None for v in pending)
            else None,
        )
        rule = UsageBudget(
            scope,
            item["identity"],
            UsageAmount(**item["limits"]),
            model,
        )
        decision = rule.check(consumed, reserved, proposed)
        require(decision.allowed, "BUDGET_BLOCKED: " + ",".join(decision.reasons))

    return {**local, "limits": applicable}


def preview(root: Path, plan: Any, run_id: str) -> Any:
    """Assess the entire fresh inventory in memory; never reserve or authorize."""
    if "usage_budget" not in plan or "economics" not in plan:
        return {"status": "UNAVAILABLE", "reason": "Forecast or fresh inventory absent"}
    path = root / ".local/usage/reservations.json"
    state = load(path) if path.exists() else {"calls": {}}
    policy = plan["usage_budget"]
    local = root / ".local/usage/policy.json"
    configured = local.exists() and bool(load(local)["limits"])
    if configured and not (root / ".local/usage/ledger.json").exists():
        return {
            "status": "UNAVAILABLE",
            "reason": "Configured budget has no observed usage ledger",
        }
    for key, call in policy["calls"].items():
        identity = run_id + "/" + key
        require(
            identity not in state["calls"],
            "BUDGET_BLOCKED: existing reservation requires reconciliation",
        )
        stage = key.split("/")[1]
        _assess_call(root, policy, run_id, stage, call, state)
        state["calls"][identity] = {
            **call,
            "run_id": run_id,
            "stage": stage,
            "settled": False,
        }
    return {
        "status": "BUDGET_CHECK_PASS" if configured else "UNSET",
        "fresh_calls": len(policy["calls"]),
        "reservation_created": False,
    }


def consumption(root: Path, plan: Any, run_id: str) -> Any:
    """Assess observed consumption/outstanding reservations through the same policy."""
    folder = root / ".local/usage"
    if not (folder / "ledger.json").exists() or "usage_budget" not in plan:
        return {"status": "UNAVAILABLE"}
    state = (
        load(folder / "reservations.json")
        if (folder / "reservations.json").exists()
        else {"calls": {}}
    )
    decisions = {}
    for key, call in plan["usage_budget"]["calls"].items():
        try:
            local = _check_local(
                root, run_id, key.split("/")[1], call, state, UsageAmount(0, 0, 0)
            )
            decisions[key] = {
                "status": "BUDGET_CHECK_PASS" if local["limits"] else "UNSET"
            }
        except (ValueError, OSError, KeyError) as error:
            decisions[key] = {"status": "BUDGET_BLOCKED", "reason": str(error)}
    return {
        "status": "BUDGET_CHECK_PASS"
        if decisions
        and all(v["status"] == "BUDGET_CHECK_PASS" for v in decisions.values())
        else "UNAVAILABLE_OR_BLOCKED",
        "decisions": decisions,
    }


def verify(root: Path, run_id: str, case: str, stage: str) -> Any:
    """Authenticate the existing reservation; never create a second call claim."""
    state = load(root / ".local/usage/reservations.json")
    value = state["calls"][run_id + "/" + case + "/" + stage]
    require(not value["settled"], "BUDGET_BLOCKED: completed call cannot be repeated")
    return value


def capture(
    root: Path,
    run_id: str,
    case: str,
    stage: str,
    measurement_path: Path,
    *,
    accepted: bool | None = None,
    failure_class: str | None = None,
) -> None:
    """Retain every available invocation outcome, including validation failure."""
    ledger_path = root / ".local/usage/ledger.json"
    path = ledger_path.parent / "reservations.json"
    if not measurement_path.exists():
        # A missing capture is not a zero-token call. Keep a terminal UNKNOWN
        # observation linked to the reserved logical invocation. This permits
        # explicit later metadata reconciliation without another model launch.
        with writer(ledger_path):
            state = load(path)
            admission = state["calls"][run_id + "/" + case + "/" + stage]
            identity = admission["invocation"] + ("/Sol" if stage == "B" else "")
            unknown = UsageObservation(
                timestamp=Timestamp.from_isoformat(admission["timestamp"]),
                backend="Codex",
                provider="OpenAI",
                model=admission["model"],
                reasoning_effort="High",
                execution_profile="SEMANTIC_WORKER",
                invocation_id=identity,
                thread_id=None,
                turn_id=None,
                response_id=None,
                usage=ModelUsage(),
                source="DEVTOOLS_MISSING_CAPTURE",
                source_digest=digest(json_bytes(admission)),
                attribution=Attribution(
                    "devtools",
                    Purpose.SCIENCE,
                    run_id,
                    case,
                    stage,
                ),
                failure_class=failure_class or "USAGE_CAPTURE_UNAVAILABLE",
            )
            save_observations(ledger_path, (*observations(ledger_path), unknown))
            admission.update(settled=True, usage_observed=False)
            save(path, state)
        return
    measured = load(measurement_path)
    timestamp = Timestamp.now()
    observed = from_capture(
        measured,
        timestamp=timestamp,
        source="DEVTOOLS_RUNTIME",
        source_digest=digest(measurement_path.read_bytes()),
        attribution=Attribution("devtools", Purpose.SCIENCE, run_id, case, stage),
    )
    from dataclasses import replace

    observed = replace(
        observed,
        accepted=accepted,
        validated=accepted if accepted is not None else observed.validated,
        failure_class=failure_class or observed.failure_class,
    )
    with writer(ledger_path):
        save_observations(ledger_path, (*observations(ledger_path), observed))
        state = load(path)
        state["calls"][run_id + "/" + case + "/" + stage]["settled"] = True
        save(path, state)


def adoption(
    root: Path,
    run_id: str,
    case: str,
    original: Any,
    origin_run: str,
) -> None:
    """Record dependency use without moving original consumption into this week."""
    ledger_path = root / ".local/usage/ledger.json"
    from dataclasses import replace

    record = from_capture(
        original,
        timestamp=Timestamp.now(),
        source="DEVTOOLS_ADOPTION",
        source_digest=digest(json_bytes(original)),
        attribution=Attribution("devtools", Purpose.SCIENCE, run_id, case, "B"),
    )
    with writer(ledger_path):
        existing = observations(ledger_path)
        old = next(
            (
                r
                for r in existing
                if r.invocation_id == record.invocation_id
                and r.execution_origin == "EXECUTED"
            ),
            None,
        )
        record = replace(
            record,
            execution_origin=type(record.execution_origin).ADOPTED,
            original_timestamp=old.timestamp if old else None,
            original_attribution=Attribution(
                "devtools",
                Purpose.SCIENCE,
                origin_run,
                case,
                "B",
            ),
        )
        save_observations(ledger_path, (*existing, record))
