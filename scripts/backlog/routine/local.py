# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, SLF001, PLR2004, C901, COM812 -- closed authority guards
"""Exact local-work grants and consumed entries under the existing routine owner.

No Agent loop, Tool dispatcher, shell executor or independent policy store lives
here. Trusted hosts keep Context selection and existing effect owners; this
boundary supplies revocable authority and a finite, immutable resource account.
"""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import asdict
from typing import TYPE_CHECKING, Any, cast

from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.identity import RepositoryId
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.tools.source import SourceScope
from scripts.backlog.intake import _digest
from scripts.backlog.routine.policy import LOCAL, qualification

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from devtools.core.time import Duration
    from devtools.models.interaction import (
        ModelInteraction,
        ModelRequest,
        ModelResponse,
    )
    from scripts.backlog.routine import RoutineAuthority

COUNTERS = {
    "model_calls",
    "total_output_tokens",
    "reads",
    "checks",
    "capture_bytes",
    "delegations",
}


def eligible(  # noqa: PLR0912 -- closed exact-scope admission guards
    policy: dict[str, Any],
    request: dict[str, Any],
    provider: dict[str, Any] | None,
) -> str:
    """Admit an exact public-resource plan; prose and model output confer no power."""
    if (
        "local" not in policy["operations"]
        or policy["schema"]
        not in {"routine-development-policy-v3", "routine-development-policy-v4"}
        or request["operation"] != "authorize-routine-local"
    ):
        raise PermissionError("Explicit local-work policy amendment required")
    scope = request["scope"]
    if not isinstance(scope, dict) or set(scope) != {
        "subject",
        "plan_sha256",
        "repository",
        "actor",
        "role",
        "roles",
        "purpose",
        "profile",
        "inputs",
        "tools",
        "checks",
        "budgets",
        "private_oracle",
    }:
        raise ValueError("Closed exact local-work scope required")
    local = policy["local"]
    if any(
        not isinstance(scope[k], str) or not scope[k].strip() or len(scope[k]) > 256
        for k in ("subject", "actor")
    ):
        raise ValueError("Exact task and actor provenance required")
    if (
        scope["private_oracle"] is not False
        or scope["role"] not in local["roles"]
        or scope["purpose"] not in local["purposes"]
        or scope["profile"] not in local["profiles"]
        or not isinstance(scope["roles"], list)
        or not set(scope["roles"]) <= set(local["roles"])
        or not isinstance(scope["tools"], list)
        or not set(scope["tools"]) <= set(local["tools"])
    ):
        raise PermissionError(
            "Role, profile, Tool or private disclosure requires escalation",
        )
    configuration = policy["provider"]
    ceilings = local["budgets"]
    output_ceiling = policy["output_tokens"]
    if policy["schema"] == "routine-development-policy-v4":
        enrolled = local["provider_profiles"][scope["profile"]]
        if scope["role"] not in enrolled["roles"] or not set(scope["roles"]) <= set(
            enrolled["roles"]
        ):
            raise PermissionError("Role outside enrolled provider profile")
        configuration = enrolled["provider"]
        ceilings = enrolled["budgets"]
        output_ceiling = ceilings["output_tokens"]
    RepositoryId.parse(scope["repository"])
    if (
        not isinstance(scope["inputs"], dict)
        or len(scope["inputs"]) > 64
        or not isinstance(scope["checks"], dict)
        or len(scope["checks"]) > 32
    ):
        raise ValueError("Bounded exact source and fixed-check inventories required")
    for path in scope["inputs"]:
        RepositoryResourceAddress(path)
        if not path.startswith(tuple(local["read_roots"])) or path.startswith(
            ".local/backlog/",
        ):
            raise PermissionError("Resource outside local public-read authority")
    for digest in [
        scope["plan_sha256"],
        *scope["inputs"].values(),
        *scope["checks"].values(),
    ]:
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise ValueError("Authenticated plan/source/check identities required")
    limits = scope["budgets"]
    if (
        not isinstance(limits, dict)
        or set(limits) != set(LOCAL)
        or any(
            type(limits[k]) is not int or not 0 <= limits[k] <= maximum
            for k, maximum in ceilings.items()
        )
        or limits["wall_seconds"] == 0
    ):
        raise PermissionError("Finite local resource allowance exceeded")
    if limits["model_calls"] and (
        provider != {"configuration": configuration, "healthy": True, "idle": True}
        or not 0 < limits["output_tokens"] <= output_ceiling
        or not 0
        < limits["input_tokens"]
        <= configuration["context_tokens"] - limits["output_tokens"]
        or limits["call_seconds"] == 0
    ):
        raise PermissionError("Qualified pinned provider and reserved Context required")
    return str(scope["subject"])


def narrow(allowed: dict[str, Any], scope: dict[str, Any]) -> None:
    """Apply the same subset rule at delegation preparation and consumed entry."""
    if (
        any(
            scope[k] != allowed[k]
            for k in ("subject", "plan_sha256", "repository", "purpose", "profile")
        )
        or scope["role"] not in allowed["roles"]
        or not set(scope["roles"]) <= set(allowed["roles"])
        or not set(scope["tools"]) <= set(allowed["tools"])
        or any(
            allowed[k].get(n) != v
            for k in ("inputs", "checks")
            for n, v in scope[k].items()
        )
        or any(v > allowed["budgets"][k] for k, v in scope["budgets"].items())
    ):
        raise PermissionError("Delegation cannot expand parent permissions")


class LocalWork:
    """A bounded consumer of RoutineAuthority decisions, not a new framework."""

    def __init__(self, owner: RoutineAuthority) -> None:
        """Borrow the canonical routine policy, decision and writer owner."""
        self.owner = owner

    def sources(self, scope: dict[str, Any]) -> SourceScope:
        """Reuse canonical RI/Tool scope/currentness and content identities."""
        source = SourceScope.observe(
            root=resolve_path(self.owner.cycle.root),
            repository=Repository(RepositoryId.parse(scope["repository"])),
            addresses=tuple(RepositoryResourceAddress(p) for p in scope["inputs"]),
            maximum_resource_bytes=scope["budgets"]["source_bytes"],
        )
        if {
            str(r.address): str(r.content_identity) for r in source.snapshot.resources
        } != scope["inputs"]:
            raise PermissionError("Local source identity drift")
        return source

    async def authorize(
        self,
        identity: str,
        scope: dict[str, Any],
        *,
        assessment: dict[str, Any],
        provider: dict[str, Any] | None = None,
        parent: str | None = None,
    ) -> dict[str, Any]:
        """Fresh exact policy-derived consent; never consult an interactive prompt."""
        await self.owner.cycle._coordinator()
        qualification(assessment)
        self.owner.cycle.intake._source_idle()
        policy = self.owner.active(identity)["policy"]
        request: dict[str, Any] = {
            "operation": "authorize-routine-local",
            "scope": scope,
        }
        eligible(policy, request, provider)
        request["parent"] = parent
        if parent is not None:
            previous = self.check(parent)
            narrow(previous["request"]["scope"], scope)
        request["source_snapshot"] = str(self.sources(scope).snapshot.id)
        if parent is not None:
            reserved = self.enter(
                parent,
                "delegate",
                {"scope": scope},
                provider=provider,
            )
            request["parent_entry"] = reserved["sha256"]
            request["grant"] = {"expires_at": previous["expires_at"]}
        reference = self.owner.approve(
            identity,
            "local",
            request,
            assessment=assessment,
            provider=provider,
        )
        record = self.owner.check_reference(reference, kind="local")
        if record is None:
            raise PermissionError("New local grant was not authenticated")
        return {"reference": reference, "decision": record}

    def check(self, reference: str) -> dict[str, Any]:
        """Revocation, expiry, parent authority, exact source and finite wall time."""
        self.owner.cycle.intake._source_idle()
        record = self.owner.check_reference(reference, kind="local")
        if record is None:
            raise PermissionError("Policy-derived local authority required")
        request = record["request"]
        if request["parent"] is not None:
            self.check(request["parent"])
            reservations = self.records(request["parent"])
            if not any(
                row["sha256"] == request["parent_entry"]
                and row["operation"] == "delegate"
                and _digest(row["payload"]["scope"]) == _digest(request["scope"])
                for row in reservations
            ):
                raise PermissionError("Child differs from consumed parent reservation")
        scope = request["scope"]
        elapsed = cast(
            "Duration", Timestamp.now() - Timestamp.from_isoformat(record["at"])
        )
        if elapsed.total_seconds >= scope["budgets"]["wall_seconds"]:
            raise PermissionError("Local wall budget exhausted")
        if str(self.sources(scope).snapshot.id) != request["source_snapshot"]:
            raise PermissionError("Local source snapshot drift")
        return record

    def records(self, reference: str) -> list[dict[str, Any]]:
        """Authenticate this grant's ordered consumed entries, not unrelated history."""
        identity = reference.rsplit(":", 1)[-1]
        if re.fullmatch(r"[0-9a-f]{64}", identity) is None:
            raise PermissionError("Exact local grant reference required")
        folder = self.owner.folder / "local" / identity
        rows: list[dict[str, Any]] = []
        for n, path in enumerate(sorted(folder.glob("entry-*.json")), 1):
            row = self.owner.load(path, "local-entry")
            if (
                path.name != f"entry-{n:04d}.json"
                or row["reference"] != reference
                or row["previous"] != (rows[-1]["sha256"] if rows else None)
            ):
                raise PermissionError("Local entry chain integrity failure")
            rows.append(row)
        return rows

    def complete(
        self,
        reference: str,
        entry: dict[str, Any],
        result: dict[str, Any],
        *,
        outcome: str = "returned",
    ) -> dict[str, Any]:
        """Retain observed completion even after revocation; never restore authority."""
        with self.owner.cycle.intake._writer():
            decision = self.owner.load(
                self.owner.folder
                / "decisions"
                / (reference.rsplit(":", 1)[-1] + ".json"),
                "decision",
            )
            if outcome not in {
                "returned",
                "unknown-or-failed",
            } or not any(
                _digest(entry) == _digest(row) for row in self.records(reference)
            ):
                raise PermissionError(
                    "Completion must bind an authentic consumed entry",
                )
            limits = decision["request"]["scope"]["budgets"]
            size = len(json.dumps(result).encode())
            if size > limits["response_bytes"]:
                outcome = "unknown-or-failed"
                result = {"oversized_result_sha256": _digest(result), "bytes": size}
            folder = self.owner.folder / "local" / decision["sha256"]
            return self.owner.cycle._save(
                folder / (entry["sha256"] + "-result.json"),
                {
                    "schema": "backlog-routine-local-result-v1",
                    "entry": entry["sha256"],
                    "outcome": outcome,
                    "result": result,
                },
            )

    def enter(
        self,
        reference: str,
        operation: str,
        payload: dict[str, Any],
        *,
        provider: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Consume before effects; unknown/failed entries remain spent."""
        with self.owner.cycle.intake._writer():
            record = self.check(reference)
            scope = record["request"]["scope"]
            limits = scope["budgets"]
            policy = self.owner.active(record["policy_version"])["policy"]
            cost = dict.fromkeys(COUNTERS, 0)
            size = len(json.dumps(payload).encode())
            cost["capture_bytes"] = 2 * size + 16384
            if operation == "model":
                eligible(policy, record["request"], provider)
                req = payload["request"]
                maximum = req["settings"]["maximum_output_tokens"]
                if (
                    type(maximum) is not int
                    or not 0 < maximum <= limits["output_tokens"]
                    or type(payload["input_tokens"]) is not int
                    or not 0 <= payload["input_tokens"] <= limits["input_tokens"]
                    or len(json.dumps(req).encode()) > limits["prompt_bytes"]
                    or not {t["name"] for t in req["tools"]} <= set(scope["tools"])
                ):
                    raise PermissionError("Model request exceeds exact local grant")
                cost["model_calls"] = 1
                cost["total_output_tokens"] = maximum
                cost["capture_bytes"] += 2 * limits["response_bytes"]
            elif operation == "read":
                if (
                    payload["path"] not in scope["inputs"]
                    or type(payload["maximum_bytes"]) is not int
                    or not 0 < payload["maximum_bytes"] <= limits["source_bytes"]
                ):
                    raise PermissionError("Read outside exact local grant")
                cost["reads"] = 1
                cost["capture_bytes"] += 2 * payload["maximum_bytes"]
            elif operation == "check":
                if (
                    payload["name"] not in scope["checks"]
                    or scope["checks"][payload["name"]] != payload["definition_sha256"]
                ):
                    raise PermissionError("Check outside exact local grant")
                cost["checks"] = 1
            elif operation == "delegate":
                eligible(
                    policy,
                    {"operation": "authorize-routine-local", "scope": payload["scope"]},
                    provider,
                )
                narrow(scope, payload["scope"])
                overhead = cost["capture_bytes"]
                cost = {k: payload["scope"]["budgets"][k] for k in COUNTERS}
                cost["delegations"] += 1
                cost["capture_bytes"] += overhead
            elif operation != "evidence":
                raise PermissionError("Local effect requires separate authority")
            rows = self.records(reference)
            for prior in rows:
                if prior["operation"] in {"model", "read", "check"}:
                    path = (
                        self.owner.folder
                        / "local"
                        / record["sha256"]
                        / (prior["sha256"] + "-result.json")
                    )
                    if (
                        not path.exists()
                        or self.owner.load(path, "local-result")["outcome"]
                        != "returned"
                    ):
                        raise PermissionError(
                            "Unknown or failed local effects require reconciliation",
                        )
            if any(
                cost[k] + sum(r["cost"][k] for r in rows) > limits[k] for k in COUNTERS
            ):
                raise PermissionError("Consumed local resource budget exhausted")
            folder = self.owner.folder / "local" / record["sha256"]
            folder.mkdir(parents=True, exist_ok=True)
            return self.owner.cycle._save(
                folder / f"entry-{len(rows) + 1:04d}.json",
                {
                    "schema": "backlog-routine-local-entry-v1",
                    "reference": reference,
                    "at": str(Timestamp.now()),
                    "previous": rows[-1]["sha256"] if rows else None,
                    "operation": operation,
                    "payload": payload,
                    "cost": cost,
                    "meaning": "Consumed permission only; no unknown replay.",
                },
            )

    async def interact(
        self,
        reference: str,
        request: ModelRequest,
        *,
        interaction: ModelInteraction,
        qualify: Callable[[], Awaitable[dict[str, Any]]],
        measure: Callable[[ModelRequest], Awaitable[int]],
    ) -> ModelResponse:
        """One model-neutral call, captured before host disposition."""
        record = self.check(reference)
        limits = record["request"]["scope"]["budgets"]
        if str(interaction.source) != record["request"]["scope"]["actor"]:
            raise PermissionError("Interaction actor differs from exact local grant")
        async with asyncio.timeout(limits["call_seconds"]):
            count = await measure(request)
            entry = self.enter(
                reference,
                "model",
                {
                    "request": asdict(request),
                    "input_tokens": count,
                    "source": str(interaction.source),
                },
                provider=await qualify(),
            )
            try:
                remaining = (
                    record["request"]["scope"]["budgets"]["wall_seconds"]
                    - cast(
                        "Duration",
                        Timestamp.now() - Timestamp.from_isoformat(record["at"]),
                    ).total_seconds
                )
                response = await asyncio.wait_for(interaction.send(request), remaining)
            except (Exception, asyncio.CancelledError) as error:
                self.complete(
                    reference,
                    entry,
                    {"error": type(error).__name__ + ": " + str(error)},
                    outcome="unknown-or-failed",
                )
                raise
            maximum = request.settings.maximum_output_tokens
            invalid = response.source != interaction.source or (
                response.usage is not None
                and response.usage.output_tokens is not None
                and maximum is not None
                and response.usage.output_tokens > maximum
            )
            captured = self.complete(
                reference,
                entry,
                {"response": asdict(response)},
                outcome="unknown-or-failed" if invalid else "returned",
            )
            self.check(reference)
            if invalid or captured["outcome"] != "returned":
                raise PermissionError("Returned response exceeds local authority")
            return response
