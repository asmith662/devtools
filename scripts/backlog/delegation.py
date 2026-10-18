# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, SLF001, PLR2004 -- bounded repository authority
"""Standing local-host authority for the existing backlog/Qwen consumer only.

Hashes identify records, not principals. The trusted host authenticates issue and
revocation interactively; only its designated supervisor may consume the grant.
Reservations are never refunded, including partial writes and uncertain dispatch.
"""

from __future__ import annotations

import getpass
import re
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from devtools.context import RepositoryResourceAddress
from devtools.core.time import Timestamp
from scripts.backlog.intake import _digest
from scripts.backlog.work import SCOPE, _load
from scripts.qwen.llama_cpp_profile import QWEN38_27B_UD_IQ4_XS

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from devtools.models.interaction import (
        ModelInteraction,
        ModelRequest,
        ModelResponse,
    )
    from experiments.qwen.tasks import CodingTask
    from scripts.backlog.work import WorkCycle

PROHIBITED = (
    "protected publication",
    "scientific execution",
    "credentials",
    "external financial operations",
    "model-authored commands",
    "grant expansion",
)
PER_TASK = {"calls": 3, "output_tokens": 4096, "seconds": 900, "edits": 3}


def validate_policy(policy: dict[str, Any]) -> None:  # noqa: C901, PLR0912 -- closed policy validation
    """Admit a closed concrete policy, never a generic policy expression."""
    if set(policy) != {
        "categories",
        "sources",
        "tests",
        "oracles",
        "per_task",
        "total",
    }:
        raise ValueError("Standing policy fields differ from the supported contract")
    for field in ("categories", "sources", "tests", "oracles"):
        values = policy[field]
        if not isinstance(values, list) or not values or len(values) > 100:
            raise ValueError("Expected bounded nonempty policy lists")
        if any(not isinstance(v, str) for v in values) or len(set(values)) != len(
            values
        ):
            raise ValueError("Expected distinct text policy values")
    if not set(policy["categories"]) <= {"bug", "refactor", "enhancement"}:
        raise PermissionError(
            "Only reviewed routine maintenance categories are supported"
        )
    for field, prefix in (("sources", "src/devtools/"), ("tests", "tests/")):
        for path in policy[field]:
            RepositoryResourceAddress(path)
            if not path.startswith(prefix) or not path.endswith(".py"):
                raise PermissionError(
                    "Only exact repository Python paths are supported"
                )
    # Consequential infrastructure cannot become routine through a label.
    for path in policy["sources"]:
        if path.startswith(
            tuple(
                "src/devtools/" + p + "/"
                for p in (
                    "governance",
                    "orchestration",
                    "agents",
                    "models",
                    "tools",
                    "runtime",
                    "persistence",
                    "resources/commands",
                )
            )
        ):
            raise PermissionError("Consequential source requires manual authorization")
    if any(not re.fullmatch(r"[0-9a-f]{64}", v) for v in policy["oracles"]):
        raise ValueError("Host-owned acceptance code must be pinned by SHA-256")
    for field, bounds in (
        ("per_task", PER_TASK),
        (
            "total",
            {
                "tasks": 100,
                "calls": 300,
                "output_tokens": 1228800,
                "seconds": 90000,
            },
        ),
    ):
        if not isinstance(policy[field], dict) or set(policy[field]) != set(bounds):
            raise ValueError("Explicit task and cumulative allowances required")
        for key, bound in bounds.items():
            value = policy[field][key]
            if type(value) is not int or not 1 <= value <= bound:
                raise ValueError("Standing allowance exceeds supported bounds")


class Delegations:
    """Use WorkCycle's coordinator, immutable receipts and exclusive writer."""

    def __init__(self, cycle: WorkCycle) -> None:
        """Select the existing concrete work owner."""
        self.cycle = cycle

    def folder(self, identity: str) -> Path:
        """Confine content-addressed grant lookup to the coordinator."""
        if not re.fullmatch(r"[0-9a-f]{64}", identity):
            raise ValueError("Invalid delegation identity")
        return self.cycle.intake._path(".local/backlog/delegations/" + identity)

    def active(self, identity: str) -> dict[str, Any]:
        """Recheck revocation, time, host and complete fixed policy."""
        folder = self.folder(identity)
        grant = _load(folder / "grant.json", "backlog-qwen-delegation-v1")
        now = Timestamp.now().value
        if (
            grant["sha256"] != identity
            or grant["coordinator"] != str(self.cycle.root)
            or grant["principal"] != getpass.getuser()
            or grant["supervisor"] != "Codex"
            or grant["scope"] != SCOPE
            or grant["prohibited"] != list(PROHIBITED)
            or not Timestamp.from_isoformat(grant["issued_at"]).value
            <= now
            < Timestamp.from_isoformat(grant["expires_at"]).value
            or (folder / "revocation.json").exists()
            or (folder / "blocked.json").exists()
        ):
            raise PermissionError(
                "Standing grant expired, revoked or differs from host/scope"
            )
        validate_policy(grant["policy"])
        return grant

    async def issue(
        self,
        policy: dict[str, Any],
        *,
        principal: str,
        reference: str,
        expires_at: Timestamp,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Issue only through genuine trusted-host consent; default deny."""
        await self.cycle._coordinator()
        validate_policy(policy)
        now = Timestamp.now()
        if (
            principal != getpass.getuser()
            or not reference.strip()
            or expires_at.value <= now.value
        ):
            raise PermissionError(
                "Actual host principal, provenance and future expiry required"
            )
        grant = {
            "schema": "backlog-qwen-delegation-v1",
            "principal": principal,
            "decision_reference": reference,
            "issued_at": str(now),
            "expires_at": str(expires_at),
            "coordinator": str(self.cycle.root),
            "supervisor": "Codex",
            "scope": SCOPE,
            "policy": policy,
            "model": "qwen38-local",
            "endpoint": "http://127.0.0.1:8080",
            "profile_sha256": _digest(asdict(QWEN38_27B_UD_IQ4_XS)),
            "prohibited": list(PROHIBITED),
        }
        if authorize is None or not authorize(
            {"operation": "issue-standing-delegation", "grant": grant}
        ):
            raise PermissionError("Interactive standing delegation consent required")
        await self.cycle._coordinator()
        if Timestamp.now().value >= expires_at.value:
            raise PermissionError("Delegation expired during confirmation")
        with self.cycle.intake._writer():
            folder = self.folder(_digest(grant))
            folder.mkdir(parents=True)
            return self.cycle._save(folder / "grant.json", grant)

    async def revoke(
        self,
        identity: str,
        *,
        principal: str,
        reference: str,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Revocation prevents subsequent admission; it cannot roll back a call."""
        await self.cycle._coordinator()
        grant = _load(
            self.folder(identity) / "grant.json", "backlog-qwen-delegation-v1"
        )
        if (
            grant["sha256"] != identity
            or principal != grant["principal"]
            or principal != getpass.getuser()
            or not reference.strip()
        ):
            raise PermissionError(
                "Actual issuing principal and revocation provenance required"
            )
        record = {
            "schema": "backlog-qwen-revocation-v1",
            "delegation": identity,
            "principal": principal,
            "reference": reference,
            "at": str(Timestamp.now()),
        }
        if authorize is None or not authorize(
            {
                "operation": "revoke-standing-delegation",
                "grant": grant,
                "revocation": record,
            }
        ):
            raise PermissionError("Interactive revocation consent required")
        await self.cycle._coordinator()
        with self.cycle.intake._writer():
            return self.cycle._save(self.folder(identity) / "revocation.json", record)

    def check(
        self, identity: str, assignment: dict[str, Any], task: CodingTask
    ) -> dict[str, Any]:
        """Read-only applicability; no authority or allowance is created."""
        grant = self.active(identity)
        self.eligible(grant["policy"], assignment, task)
        return grant

    @staticmethod
    def eligible(
        policy: dict[str, Any], assignment: dict[str, Any], task: CodingTask
    ) -> None:
        """Check a proposed policy without issuing or activating any grant."""
        validate_policy(policy)
        if (
            assignment["backlog"]["proposal"]["payload"]["kind"]
            not in policy["categories"]
            or task.source not in policy["sources"]
            or not set(task.tests) <= set(policy["tests"])
            or task.oracle_sha256 not in policy["oracles"]
        ):
            raise PermissionError(
                "Task category, source, tests or acceptance code outside delegation"
            )
        requested = {
            "calls": task.maximum_calls,
            "output_tokens": task.output_tokens,
            "seconds": task.wall_seconds,
            "edits": task.maximum_calls,
        }
        if any(v > policy["per_task"][k] for k, v in requested.items()):
            raise PermissionError("Task exceeds delegated limits")

    async def review(  # noqa: PLR0913 -- exact decision provenance
        self,
        item: str,
        identity: str,
        *,
        reference: str,
        rationale: str,
        disposition: str,
        result_sha256: str | None = None,
    ) -> dict[str, Any]:
        """Record trusted Codex supervision, never worker-provided authority."""
        folder = self.cycle._folder(item)
        assignment = _load(folder / "assignment.json", "backlog-qwen-assignment-v1")
        if result_sha256 is None:
            task = await self.cycle._validate(assignment)
            self.check(identity, assignment, task)
            allowed = {"APPROVE_ROUTINE", "REJECT"}
        else:
            await self.cycle._coordinator()
            self.active(identity)
            result = _load(folder / "result.json", "backlog-qwen-result-v1")
            authorization = _load(
                folder / "authorization.json", "backlog-qwen-authorization-v1"
            )
            if (
                result["sha256"] != result_sha256
                or authorization.get("delegation") != identity
            ):
                raise PermissionError("Result/authority differs from supervisory scope")
            allowed = {"ACCEPT_RECOMMENDED", "REWORK_RECOMMENDED", "ESCALATE", "REJECT"}
            if (
                disposition == "ACCEPT_RECOMMENDED"
                and result["disposition"] != "REVIEW_CANDIDATE"
            ):
                raise PermissionError(
                    "Failed work cannot receive acceptance recommendation"
                )
        if disposition not in allowed or not reference.strip() or not rationale.strip():
            raise PermissionError(
                "Explicit in-scope supervisory disposition and provenance required"
            )
        record = {
            "schema": "backlog-qwen-supervision-v1",
            "delegation": identity,
            "assignment_sha256": assignment["sha256"],
            "result_sha256": result_sha256,
            "reviewer": "Codex",
            "host_principal": getpass.getuser(),
            "reference": reference,
            "rationale": rationale,
            "disposition": disposition,
            "at": str(Timestamp.now()),
            "integration_authorized": False,
        }
        with self.cycle.intake._writer():
            self.active(identity)
            if result_sha256 is None:
                for path in folder.glob("supervision-*.json"):
                    previous = _load(path, "backlog-qwen-supervision-v1")
                    if (
                        previous["delegation"] == identity
                        and previous["result_sha256"] is None
                    ):
                        raise PermissionError(
                            "Existing supervisory decision requires reconciliation"
                        )
            return self.cycle._save(
                folder / ("supervision-" + _digest(record) + ".json"), record
            )

    def authority(
        self, grant: dict[str, Any], assignment: dict[str, Any], task: CodingTask
    ) -> None:
        """Reconcile the exact reservation and supervisory decision at dispatch."""
        identity = grant["delegation"]
        standing = self.check(identity, assignment, task)
        if (
            grant["principal"] != standing["principal"]
            or grant["decision_reference"] != standing["decision_reference"]
            or not re.fullmatch(r"[0-9a-f]{64}", grant["supervision"])
        ):
            raise PermissionError(
                "Assignment authority differs from standing principal"
            )
        review = _load(
            self.cycle._folder(assignment["item"])
            / ("supervision-" + grant["supervision"] + ".json"),
            "backlog-qwen-supervision-v1",
        )
        reservation = _load(
            self.folder(identity) / "reservations" / (assignment["item"] + ".json"),
            "backlog-qwen-reservation-v1",
        )
        if (
            review["sha256"] != grant["supervision"]
            or review["delegation"] != identity
            or review["assignment_sha256"] != assignment["sha256"]
            or review["disposition"] != "APPROVE_ROUTINE"
            or review["result_sha256"] is not None
            or reservation["assignment_sha256"] != assignment["sha256"]
            or reservation["sha256"] != grant["reservation"]
        ):
            raise PermissionError(
                "Delegated authority lacks exact supervision/reservation"
            )

    async def authorize(
        self, item: str, identity: str, supervision: str
    ) -> dict[str, Any]:
        """Reserve worst-case allowance and bind existing per-assignment authority."""
        if not re.fullmatch(r"[0-9a-f]{64}", supervision):
            raise ValueError("Invalid supervisory decision identity")
        folder = self.cycle._folder(item)
        assignment = _load(folder / "assignment.json", "backlog-qwen-assignment-v1")
        task = await self.cycle._validate(assignment)
        with self.cycle.intake._writer():
            grant = self.check(identity, assignment, task)
            reservations = self.folder(identity) / "reservations"
            reservations.mkdir(exist_ok=True)
            if (
                (folder / "authorization.json").exists()
                or (folder / "dispatch.json").exists()
                or (folder / "worker").exists()
            ):
                raise PermissionError(
                    "Existing authority/dispatch requires reconciliation"
                )
            requested = {
                "tasks": 1,
                "calls": task.maximum_calls,
                "output_tokens": task.maximum_calls * task.output_tokens,
                "seconds": task.wall_seconds,
            }
            used = dict.fromkeys(requested, 0)
            for path in reservations.iterdir():
                record = _load(path, "backlog-qwen-reservation-v1")
                for key in used:
                    used[key] += record["allowance"][key]
            if any(
                used[k] + v > grant["policy"]["total"][k] for k, v in requested.items()
            ):
                raise PermissionError("Cumulative standing allowance exhausted")
            # Validate supervision before any reservation, using its immutable record.
            review = _load(
                folder / ("supervision-" + supervision + ".json"),
                "backlog-qwen-supervision-v1",
            )
            if (
                review["delegation"] != identity
                or review["assignment_sha256"] != assignment["sha256"]
                or review["disposition"] != "APPROVE_ROUTINE"
                or review["result_sha256"] is not None
            ):
                raise PermissionError("Exact pre-dispatch Codex review required")
            reservation = self.cycle._save(
                reservations / (item + ".json"),
                {
                    "schema": "backlog-qwen-reservation-v1",
                    "assignment_sha256": assignment["sha256"],
                    "allowance": requested,
                    "at": str(Timestamp.now()),
                },
            )
            return self.cycle._save(
                folder / "authorization.json",
                {
                    "schema": "backlog-qwen-authorization-v1",
                    "item": item,
                    "assignment_sha256": assignment["sha256"],
                    "scope": SCOPE,
                    "principal": grant["principal"],
                    "decision_reference": grant["decision_reference"],
                    "issued_at": str(Timestamp.now()),
                    "expires_at": grant["expires_at"],
                    "delegation": identity,
                    "supervision": supervision,
                    "reservation": reservation["sha256"],
                },
            )

    def model(self, grant: dict[str, Any], provenance: dict[str, Any]) -> None:
        """Verify the existing local factory's observed profile before inference."""
        standing = self.active(grant["delegation"])
        service = provenance.get("service", {})
        if (
            provenance.get("model") != standing["model"]
            or provenance.get("endpoint") != standing["endpoint"]
            or _digest(provenance.get("profile")) != standing["profile_sha256"]
            or service.get("state") != "READY"
            or not service.get("expected_fingerprint")
            or service.get("observed_fingerprint") != service["expected_fingerprint"]
        ):
            raise PermissionError("Model/environment differs from standing delegation")

    def guard(
        self, grant: dict[str, Any], task: CodingTask, interaction: ModelInteraction
    ) -> ModelInteraction:
        """Recheck standing authority before every existing worker invocation."""
        owner = self

        class Guarded:
            source = interaction.source
            calls = 0

            async def send(self, request: ModelRequest) -> ModelResponse:
                owner.active(grant["delegation"])
                if (
                    self.calls >= task.maximum_calls
                    or request.settings.maximum_output_tokens != task.output_tokens
                    or request.settings.thinking_enabled is not False
                    or [tool.name for tool in request.tools] != ["propose_edit"]
                ):
                    raise PermissionError(
                        "Invocation differs from reserved worker limits"
                    )
                self.calls += 1  # Uncertain outcomes retain the attempted invocation.
                response = await interaction.send(request)
                if (
                    response.usage
                    and response.usage.output_tokens is not None
                    and response.usage.output_tokens > task.output_tokens
                ):
                    with owner.cycle.intake._writer():
                        path = owner.folder(grant["delegation"]) / "blocked.json"
                        if not path.exists():
                            owner.cycle._save(
                                path,
                                {
                                    "schema": "backlog-qwen-overrun-v1",
                                    "at": str(Timestamp.now()),
                                    "output_tokens": response.usage.output_tokens,
                                },
                            )
                return response  # Preserve the original response in worker evidence.

        return Guarded()
