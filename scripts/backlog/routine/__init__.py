# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, SLF001, PLR0913 -- concrete authority, formatter compatibility
"""Revocable operator policy supplying existing owners' exact-scope callbacks.

This owner issues no model call, Tool effect, source edit or integration itself.
Historical records remain readable. New references identify both policy version
and immutable decision, without changing existing durable grant schemas.
"""

from __future__ import annotations

import getpass
import re
from typing import TYPE_CHECKING, Any

from devtools.core.time import Duration, Timestamp
from scripts.backlog.intake import _digest
from scripts.backlog.routine.policy import permits_source, qualification, validate

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from scripts.backlog.work import WorkCycle


def normalized(request: dict[str, Any]) -> dict[str, Any]:
    """Exclude only host-created receipt timestamps/links, not task or scope."""
    value = dict(request)
    if "proposed_work" in value:
        return {
            k: v
            for k, v in value.items()
            if k not in {"at", "sha256", "decision_reference"}
        }
    operation = value["operation"]
    value["operation"] = operation.replace("dispatch-", "authorize-", 1)
    if "grant" in value:
        value["grant"] = {
            k: v
            for k, v in value["grant"].items()
            if k not in {"schema", "sha256", "issued_at", "reference"}
        }
    if "decision" in value:
        value["decision"] = {
            k: v for k, v in value["decision"].items() if k not in {"at", "reference"}
        }
    return value


class RoutineAuthority:
    """One prospective authorization branch of the existing WorkCycle owner."""

    def __init__(self, cycle: WorkCycle) -> None:
        """Select the existing canonical coordinator and immutable writer."""
        self.cycle = cycle
        self.folder = cycle.root / ".local/backlog/routine"

    def load(self, path: Path, name: str) -> dict[str, Any]:
        """Authenticate one prospective record with the existing bounded reader."""
        from scripts.backlog.work import _load  # noqa: PLC0415

        return _load(path, "backlog-routine-" + name + "-v1")

    def controls(self) -> list[dict[str, Any]]:
        """Authenticate the complete immutable activation/revocation/denial chain."""
        rows: list[dict[str, Any]] = []
        for n, path in enumerate(sorted(self.folder.glob("control-*.json")), 1):
            row = self.load(path, "control")
            if (
                path.name != f"control-{n:04d}.json"
                or row["previous"] != (rows[-1]["sha256"] if rows else None)
                or row["root"] != str(self.cycle.root)
                or row["principal"] != getpass.getuser()
                or row["action"] not in {"activate", "revoke", "deny"}
            ):
                raise PermissionError("Routine control chain differs from host/root")
            rows.append(row)
        return rows

    async def control(
        self,
        action: str,
        *,
        reference: str,
        policy: dict[str, Any] | None = None,
        subject: str | None = None,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Only a genuine operator may activate/replace/revoke/deny; default No."""
        await self.cycle._coordinator()
        if (
            action not in {"activate", "revoke", "deny"}
            or not reference.strip()
            or (action == "activate") != (policy is not None)
            or (action == "deny") != (subject is not None)
        ):
            raise ValueError("Exact operator control required")
        if policy is not None:
            validate(policy)
        with self.cycle.intake._writer():
            rows = self.controls()
            record = {
                "schema": "backlog-routine-control-v1",
                "root": str(self.cycle.root),
                "principal": getpass.getuser(),
                "at": str(Timestamp.now()),
                "previous": rows[-1]["sha256"] if rows else None,
                "action": action,
                "policy": policy,
                "subject": subject,
                "reference": reference,
            }
            if authorize is None or not authorize(
                {"operation": "routine-" + action, "control": record},
            ):
                raise PermissionError("Explicit operator policy decision required")
            self.folder.mkdir(parents=True, exist_ok=True)
            return self.cycle._save(
                self.folder / f"control-{len(rows) + 1:04d}.json",
                record,
            )

    def active(
        self,
        identity: str | None = None,
        subject: str | None = None,
    ) -> dict[str, Any]:
        """No wall-clock expiry on standing policy; replacement/revocation wins."""
        current = None
        denied = set()
        for row in self.controls():
            if row["action"] == "activate":
                current = row
            elif row["action"] == "revoke":
                current = None
            else:
                denied.add(row["subject"])
        if (
            current is None
            or (identity is not None and identity != current["sha256"])
            or (subject is not None and subject in denied)
        ):
            raise PermissionError(
                "Routine policy missing, changed, revoked or explicitly denied",
            )
        validate(current["policy"])
        return current

    def eligible(  # noqa: C901, PLR0912 -- closed existing owner operations
        self,
        policy: dict[str, Any],
        kind: str,
        request: dict[str, Any],
        provider: dict[str, Any] | None,
    ) -> str:
        """Keep exact native bounds and trusted-host review semantics authoritative."""
        if kind not in policy["operations"]:
            raise PermissionError("Operation outside standing policy")
        operations = {
            "coding": {"authorize-native-maintenance"},
            "acceptance-review": {"authorize-native-review-actor"},
            "diagnostic-review": {"authorize-native-diagnostic-actor"},
            "host-review": {"review-native-candidate"},
            "integration-plan": {"integration-plan"},
            "git": {"git"},
        }
        if (
            kind != "intake"
            and normalized(request)["operation"] not in operations[kind]
        ):
            raise PermissionError("Operation differs from policy purpose")
        if kind == "intake":
            proposal = request["proposed_work"]
            payload = proposal["payload"]
            if (
                payload["kind"] not in policy["categories"]
                or not any(permits_source(policy, p) for p in payload["resources"])
                or any(
                    not (permits_source(policy, p) or p.startswith("tests/"))
                    for p in payload["resources"]
                )
            ):
                raise PermissionError("Intake category/resources require escalation")
            return str(proposal["id"])
        if kind in {"coding", "acceptance-review", "diagnostic-review"}:
            if provider != {
                "configuration": policy["provider"],
                "healthy": True,
                "idle": True,
            }:
                raise PermissionError("Qualified pinned idle provider required")
            if kind == "coding":
                a = request["assignment"]
                attempt = a.get("continuation", {}).get("number", 1)
                if attempt > policy.get("coding_attempts", 1):
                    raise PermissionError("Coding attempt exceeds active policy")
                task = a["task"]
                config = task
                paths = [task["source"], *task["read_paths"], *task["tests"]]
                if (
                    not permits_source(policy, task["source"])
                    or a["backlog"]["proposal"]["payload"]["kind"]
                    not in policy["categories"]
                ):
                    raise PermissionError(
                        "Coding source/category outside routine scope",
                    )
                profile = task["worker"]["profile"]
                ceilings = policy["coding"]
                item = a["item"]
                if (
                    task.get("context", {}).get("context_tokens", 0)
                    > policy["provider"]["context_tokens"]
                ):
                    raise PermissionError("Provider context exceeds qualification")
            else:
                packet = request["packet"]
                config = packet["policy"]
                paths = config["read_paths"]
                profile = config["profile"]
                ceilings = policy["review"]
                item = packet["subject"]["item"]
            if (
                profile not in policy["profiles"]
                or not all(p.startswith(tuple(policy["read_roots"])) for p in paths)
                or config["settings"]["maximum_output_tokens"] > policy["output_tokens"]
                or any(v > ceilings[k] for k, v in config["budgets"].items())
            ):
                raise PermissionError(
                    "Profile, source or resource allowance requires escalation",
                )
            return str(item)
        if kind == "host-review":
            if not request.get("review_proposal"):
                raise PermissionError(
                    "Model proposal and existing host assessment required",
                )
            return str(request["assignment"]["item"])
        if kind == "integration-plan":
            if (
                request["spec"]["parent_complete"]
                or request["spec"]["remote"] != policy["git"]["remote"]
                or request["spec"]["destination"] not in policy["git"]["branches"]
            ):
                raise PermissionError("Plan scope requires escalation")
            return str(request["item"])
        # A permission receipt is not a Git execution or a protected-gate pass.
        argv = request["argv"]
        inputs = request.get("git_inputs")
        if (
            not request["validation_reference"].strip()
            or not isinstance(inputs, dict)
            or set(inputs) != {"head", "index_sha256", "paths"}
            or not isinstance(inputs["head"], str)
            or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", inputs["head"]) is None
            or not isinstance(inputs["index_sha256"], str)
            or re.fullmatch(r"[0-9a-f]{64}", inputs["index_sha256"]) is None
            or not isinstance(inputs["paths"], list)
            or any(
                not isinstance(path, str)
                or not (
                    permits_source(policy, path)
                    or path.startswith(("tests/", "docs/research/", "docs/backlog/"))
                )
                for path in inputs["paths"]
            )
            or argv[:1] not in (["commit"], ["push"])
            or (argv[0] == "commit" and argv != ["commit"])
            or (argv[0] == "push" and argv != ["push", policy["git"]["remote"], "main"])
        ):
            raise PermissionError(
                "Only routine commit/non-force main push may be assessed",
            )
        return "git"

    def approve(
        self,
        identity: str,
        kind: str,
        request: dict[str, Any],
        *,
        assessment: dict[str, Any],
        provider: dict[str, Any] | None = None,
    ) -> str:
        """Reserve an exact decision before the existing owner issues a grant."""
        qualification(assessment)
        with self.cycle.intake._writer():
            control = self.active(identity)
            p = control["policy"]
            subject = self.eligible(p, kind, request, provider)
            subjects = {subject}
            if kind == "intake" and request.get("publication"):
                subjects.add(request["publication"]["id"])
            elif re.fullmatch(r"B-\d{4}", subject):
                subjects.add(self.cycle.intake.approved_item(subject)["proposal"]["id"])
            for name in subjects:
                self.active(identity, name)
            expires = Timestamp.now() + Duration.seconds(p["grant_seconds"])
            if "grant" in request:
                expiry = Timestamp.from_isoformat(request["grant"]["expires_at"])
                if not Timestamp.now().value < expiry.value <= expires.value:
                    raise PermissionError("Individual grant exceeds standing lifetime")
                expires = expiry
            value = {
                "schema": "backlog-routine-decision-v1",
                "policy_version": identity,
                "subject": subject,
                "subjects": sorted(subjects),
                "kind": kind,
                "request": normalized(request),
                "assessment": assessment,
                "provider": provider,
                "at": str(Timestamp.now()),
                "expires_at": str(expires),
            }
            folder = self.folder / "decisions"
            folder.mkdir(exist_ok=True)
            record = self.cycle._save(folder / (_digest(value) + ".json"), value)
            return "routine-v1:" + identity + ":" + str(record["sha256"])

    def check_reference(
        self,
        reference: str,
        *,
        subject: str | None = None,
        kind: str | None = None,
    ) -> dict[str, Any] | None:
        """Recheck prospective authority; legacy references stay historical."""
        if not reference.startswith("routine-v1:"):
            return None
        match = re.fullmatch(r"routine-v1:([0-9a-f]{64}):([0-9a-f]{64})", reference)
        if match is None:
            raise PermissionError("Malformed routine authority reference")
        version, identity = match.groups()
        record = self.load(self.folder / "decisions" / (identity + ".json"), "decision")
        if (
            record["policy_version"] != version
            or record["sha256"] != identity
            or (subject is not None and subject not in record["subjects"])
            or (kind is not None and record["kind"] != kind)
            or Timestamp.now().value
            >= Timestamp.from_isoformat(record["expires_at"]).value
        ):
            raise PermissionError("Routine decision expired or mismatched")
        for name in record["subjects"]:
            self.active(version, name)
        return record

    def callback(self, reference: str) -> Callable[[dict[str, Any]], bool]:
        """Supply current policy-derived consent without interactive input."""

        def allowed(request: dict[str, Any]) -> bool:
            record = self.check_reference(reference)
            if record is None:
                return False
            if "proposed_work" in request:
                link = request.get("decision_reference")
            else:
                link = request.get("grant", request.get("decision", request)).get(
                    "reference",
                )
            return bool(link == reference and normalized(request) == record["request"])

        return allowed

    async def authorize_native(
        self,
        identity: str,
        item: str,
        *,
        assessment: dict[str, Any],
        provider: dict[str, Any],
        attempt: int = 1,
    ) -> dict[str, Any]:
        """Issue a fresh existing native grant, never revive a dispatch slot."""
        owner = self.cycle.native.select(attempt)
        a = owner.record(item, "assignment")
        if (owner.folder(item) / "dispatch.json").exists():
            raise PermissionError("Consumed native slot cannot replay")
        seconds = self.active(identity)["policy"]["grant_seconds"]
        expires = Timestamp.now() + Duration.seconds(seconds)
        captured: list[dict[str, Any]] = []

        def preview(request: dict[str, Any]) -> bool:
            captured.append(request)
            return False

        try:
            await owner.authorize(
                item,
                reference="prospective-policy-decision",
                expires=expires,
                authorize=preview,
            )
        except PermissionError:
            if not captured:
                raise
        reference = self.approve(
            identity,
            "coding",
            captured[0],
            assessment=assessment,
            provider=provider,
        )
        return await owner.authorize(
            a["item"],
            reference=reference,
            expires=expires,
            authorize=self.callback(reference),
        )

    async def authorize_reviewer(
        self,
        identity: str,
        item: str,
        *,
        diagnostic: bool = False,
        attempt: str | None = None,
        assessment: dict[str, Any],
        provider: dict[str, Any],
    ) -> dict[str, Any]:
        """Authorize an eligible exact subject through the existing reviewer owner."""
        owner = (
            self.cycle.native.diagnostic_reviewer
            if diagnostic
            else self.cycle.native.reviewer
        )
        owner = owner.select(attempt)
        if (owner.folder(item) / "dispatch.json").exists():
            raise PermissionError("Consumed review slot cannot replay")
        expires = Timestamp.now() + Duration.seconds(
            self.active(identity)["policy"]["grant_seconds"],
        )
        captured: list[dict[str, Any]] = []

        def preview(value: dict[str, Any]) -> bool:
            captured.append(value)
            return False

        try:
            await owner.authorize(
                item,
                reference="prospective-policy-decision",
                expires=expires,
                authorize=preview,
            )
        except PermissionError:
            if not captured:
                raise
        reference = self.approve(
            identity,
            "diagnostic-review" if diagnostic else "acceptance-review",
            captured[0],
            assessment=assessment,
            provider=provider,
        )
        return await owner.authorize(
            item,
            reference=reference,
            expires=expires,
            authorize=self.callback(reference),
        )

    def intake_review(
        self,
        identity: str,
        proposal: str,
        *,
        assessment: dict[str, Any],
        **options: Any,  # noqa: ANN401 -- forwarded review fields
    ) -> dict[str, Any]:
        """Review and publish exact routine backlog bytes without console consent."""
        if options.get("decision") not in {"APPROVED", "DEFERRED", "REJECTED"}:
            raise ValueError("Explicit non-advisory Intake decision required")
        captured: list[dict[str, Any]] = []

        def preview(value: dict[str, Any]) -> bool:
            captured.append(value)
            return False

        options = {
            **options,
            "reviewer": "trusted host " + getpass.getuser(),
            "reference": "prospective-policy-decision",
        }
        try:
            self.cycle.intake.review(proposal, **options, authorize=preview)
        except PermissionError:
            if not captured:
                raise
        reference = self.approve(identity, "intake", captured[0], assessment=assessment)
        options["reference"] = reference
        review = self.cycle.intake.review(
            proposal,
            **options,
            authorize=self.callback(reference),
        )
        if options["decision"] == "APPROVED":
            self.cycle.intake.promote(proposal, authorize=self.callback(reference))
        return review

    async def host_review(
        self,
        identity: str,
        item: str,
        *,
        proposal: str,
        attempt: str | None = None,
        accept: bool,
        rationale: str,
        assessment: dict[str, Any],
    ) -> dict[str, Any]:
        """Authenticate host judgment; never derive acceptance from JSON alone."""
        captured: list[dict[str, Any]] = []

        def preview(value: dict[str, Any]) -> bool:
            captured.append(value)
            return False

        options: dict[str, Any] = {
            "proposal": proposal,
            "accept": accept,
            "rationale": rationale,
        }
        actor = self.cycle.native.reviewer.select(attempt)
        try:
            await actor.decide(
                item,
                **options,
                reference="prospective-policy-decision",
                authorize=preview,
            )
        except PermissionError:
            if not captured:
                raise
        reference = self.approve(
            identity,
            "host-review",
            captured[0],
            assessment=assessment,
        )
        return await actor.decide(
            item,
            **options,
            reference=reference,
            authorize=self.callback(reference),
        )

    async def plan(
        self,
        identity: str,
        item: str,
        review: str,
        spec: dict[str, Any],
        *,
        assessment: dict[str, Any],
    ) -> dict[str, Any]:
        """Delegate read-only planning to the authenticated integration owner."""
        request = {
            "operation": "integration-plan",
            "item": item,
            "review": review,
            "spec": spec,
        }
        reference = self.approve(
            identity,
            "integration-plan",
            request,
            assessment=assessment,
        )
        self.check_reference(reference)
        from scripts.backlog.checkout import Checkout  # noqa: PLC0415
        from scripts.backlog.coordinator import git  # noqa: PLC0415

        # Planning retains the integration owner's distinct-admin-branch rule.
        # Existing Checkout serializes a temporary, zero-edit branch visit.
        if (
            await git(self.cycle.root, "branch", "--show-current")
            == spec["destination"]
        ):
            assignment = self.cycle.native.record(item, "assignment")
            async with Checkout(
                self.cycle,
                "routine-plan:" + reference.rsplit(":", 1)[1],
                assignment["branch"],
                assignment["base_head"],
            ):
                self.check_reference(reference)
                return await self.cycle.integration.plan(item, review, spec)
        return await self.cycle.integration.plan(item, review, spec)
