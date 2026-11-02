# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, SLF001, E501 -- finite operational receipts and formatter compatibility
"""One approved native assignment to candidate review; no installation authority."""

from __future__ import annotations

import asyncio
import difflib
import getpass
import hashlib
import re
import sys
from typing import TYPE_CHECKING, Any

from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.identity import RepositoryId
from devtools.core.paths import resolve_path
from devtools.core.time import Stopwatch, Timestamp
from devtools.resources.filesystem import BinaryFile, FileFormat, read
from devtools.tools.source import SourceScope
from scripts.backlog.checkout import Checkout, idle
from scripts.backlog.coordinator import git
from scripts.backlog.intake import _digest, _read
from scripts.backlog.native.packet import (
    context_policy,
    fingerprint,
    task_view,
    tool_definitions,
)
from scripts.backlog.native.review.continuation import read_decision
from scripts.backlog.work import _load, same_backlog

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from devtools.models.interaction import ModelInteraction, ModelRequest
    from scripts.backlog.native.review import NativeReviewer
    from scripts.backlog.work import WorkCycle

SCOPE = (
    "native-one-python-v1; candidate-and-read-only-plan; no-install-publish-closeout"
)


class NativeMaintenance:
    """The native input branch of WorkCycle, sharing its one-slot/writer/Checkout."""

    def __init__(self, cycle: WorkCycle) -> None:
        """Reuse administrative ownership, never construct another coordinator."""
        self.cycle = cycle

    @property
    def reviewer(self) -> NativeReviewer:
        """Compose independent review under this native administrative owner."""
        from scripts.backlog.native.review import NativeReviewer  # noqa: PLC0415

        return NativeReviewer(self)

    @property
    def diagnostic_reviewer(self) -> NativeReviewer:
        """Inspect authenticated blocked history; confer no acceptance authority."""
        from scripts.backlog.native.review import NativeReviewer  # noqa: PLC0415

        return NativeReviewer(self, diagnostic_only=True)

    def record(self, item: str, name: str) -> dict[str, Any]:
        """Load only authenticated prospective native records."""
        return _load(
            self.cycle._folder(item) / (name + ".json"),
            "backlog-native-" + name + "-v1",
        )

    def save(self, item: str, name: str, value: dict[str, Any]) -> dict[str, Any]:
        """Append immutable operational facts using the existing writer."""
        with self.cycle.intake._writer():
            return self.cycle._save(
                self.cycle._folder(item) / (name + ".json"),
                {"schema": "backlog-native-" + name + "-v1", **value},
            )

    def observe(self, assignment: dict[str, Any]) -> SourceScope:
        """Reobserve exact declared inputs with the canonical source substrate."""
        return SourceScope.observe(
            root=resolve_path(self.cycle.root),
            repository=Repository(RepositoryId.parse(assignment["repository"])),
            addresses=tuple(RepositoryResourceAddress(p) for p in assignment["inputs"]),
            maximum_resource_bytes=131072,
        )

    def configuration(self, task: dict[str, Any]) -> dict[str, str | None]:
        """Pin check configuration without granting source disclosure rights."""
        from pathlib import Path  # noqa: PLC0415

        names = {
            "pyproject.toml",
            "uv.lock",
            "pytest.ini",
            "setup.cfg",
            ".coveragerc",
            ".python-version",
            "conftest.py",
        }
        for test in task["tests"]:
            names.update(
                (parent / "conftest.py").as_posix() for parent in Path(test).parents
            )
        values = {}
        for name in sorted(names):
            path = self.cycle.root / name
            resolved = resolve_path(path)
            if resolved.value != path or not resolved.value.is_relative_to(
                self.cycle.root,
            ):
                raise PermissionError("Native configuration aliases are not admitted")
            value = (
                read(resolved, file_format=FileFormat.BINARY, max_bytes=1 << 20)
                if path.exists()
                else None
            )
            if value is not None and (
                not isinstance(value, BinaryFile) or value.truncated
            ):
                raise ValueError("Expected complete bounded configuration input")
            values[name] = (
                hashlib.sha256(value.content).hexdigest() if value is not None else None
            )
        return values

    async def prepare(
        self,
        item: str,
        *,
        branch: str,
        task: dict[str, Any],
        supervisor: str,
    ) -> dict[str, Any]:
        """Freeze reviewed backlog, scope and evidence; preparation grants no effects."""
        await self.cycle._coordinator()
        await idle(self.cycle.root)
        if (self.cycle.root / ".local/backlog/checkout-owner").exists():
            raise PermissionError("Checkout owned; native preparation refused")
        task_view(task)
        if not supervisor.strip():
            raise ValueError("Supervisor provenance required")
        binding = self.cycle.intake.approved_item(item)
        if task["source"] not in binding["proposal"]["payload"]["resources"]:
            raise PermissionError(
                "Native edit target outside reviewed backlog resources",
            )
        await git(self.cycle.root, "check-ref-format", "refs/heads/" + branch)
        head = await git(self.cycle.root, "rev-parse", "HEAD")
        if (
            not branch.startswith("feat/")
            or branch == await git(self.cycle.root, "branch", "--show-current")
            or await git(
                self.cycle.root,
                "for-each-ref",
                "--format=%(objectname)",
                "refs/heads/" + branch,
            )
            != head
        ):
            raise PermissionError(
                "Native v1 requires a separate existing feature branch at the administrative HEAD",
            )
        addresses = sorted(
            {
                task["source"],
                *task["tests"],
                *task["read_paths"],
            },
        )
        repository = Repository.new()
        scope = SourceScope.observe(
            root=resolve_path(self.cycle.root),
            repository=repository,
            addresses=tuple(RepositoryResourceAddress(p) for p in addresses),
            maximum_resource_bytes=131072,
        )
        baseline = scope.snapshot.resource_at(
            RepositoryResourceAddress(task["source"]),
        ).content
        if len(baseline.encode()) > task["budgets"]["source_bytes"]:
            raise ValueError("Native source exceeds approved resulting-source ceiling")
        folder = self.cycle._folder(item)
        with self.cycle.intake._writer():
            folder.parent.mkdir(parents=True, exist_ok=True)
            folder.mkdir()  # Same one-slot rule as legacy WorkCycle; no redispatch slot.
            return self.cycle._save(
                folder / "assignment.json",
                {
                    "schema": "backlog-native-assignment-v1",
                    "item": item,
                    "at": str(Timestamp.now()),
                    "coordinator": str(self.cycle.root),
                    "scope": SCOPE,
                    "branch": branch,
                    "base_head": head,
                    "backlog": binding,
                    "supervisor": supervisor,
                    "task": task,
                    "task_sha256": fingerprint(task),
                    "repository": str(repository.id),
                    "inputs": {
                        r.address.value: str(r.content_identity)
                        for r in scope.snapshot.resources
                    },
                    "baseline_source": baseline,
                    "initial_snapshot": str(scope.snapshot.id),
                    "execution_authorized": False,
                    "tool_definitions": tool_definitions(task),
                    "interpreter": sys.executable,
                    "python": sys.version,
                    "configuration": self.configuration(task),
                },
            )

    async def validate(
        self,
        assignment: dict[str, Any],
        checkout: Checkout | None = None,
    ) -> SourceScope:
        """Authenticate exact packet, administrative state and declared current inputs."""
        await self.cycle._coordinator()
        stored = self.record(assignment["item"], "assignment")
        if (
            stored != assignment
            or assignment["coordinator"] != str(self.cycle.root)
            or assignment["scope"] != SCOPE
            or fingerprint(assignment["task"]) != assignment["task_sha256"]
            or assignment["tool_definitions"] != tool_definitions(assignment["task"])
            or assignment["interpreter"] != sys.executable
            or assignment["python"] != sys.version
            or assignment["configuration"] != self.configuration(assignment["task"])
        ):
            raise PermissionError("Native assignment identity/root/profile changed")
        if checkout is None:
            if (self.cycle.root / ".local/backlog/checkout-owner").exists():
                raise PermissionError(
                    "Checkout owned; native admission requires release or recovery",
                )
            if not same_backlog(
                self.cycle.intake.approved_item(assignment["item"]),
                assignment["backlog"],
            ):
                raise PermissionError("Native backlog approval changed")
            await idle(self.cycle.root)
        else:
            checkout._owned()
            if (
                await git(
                    self.cycle.root,
                    "rev-parse",
                    checkout.record["return_branch"],
                )
                != checkout.record["return_head"]
            ):
                raise PermissionError(
                    "Administrative branch changed during native work",
                )
        if (
            await git(
                self.cycle.root,
                "for-each-ref",
                "--format=%(objectname)",
                "refs/heads/" + assignment["branch"],
            )
            != assignment["base_head"]
        ):
            raise PermissionError("Native feature base changed")
        scope = self.observe(assignment)
        for resource in scope.snapshot.resources:
            if (
                checkout is not None
                and resource.address.value == assignment["task"]["source"]
            ):
                continue
            if (
                str(resource.content_identity)
                != assignment["inputs"][resource.address.value]
            ):
                raise PermissionError("Native source/check/configuration input changed")
        return scope

    async def authorize(
        self,
        item: str,
        *,
        reference: str,
        expires: Timestamp,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Obtain explicit current host approval of the complete packet, default deny."""
        assignment = self.record(item, "assignment")
        await self.validate(assignment)
        if not reference.strip() or expires.value <= Timestamp.now().value:
            raise PermissionError(
                "Native approval requires provenance and future expiry",
            )
        grant = {
            "item": item,
            "assignment_sha256": assignment["sha256"],
            "principal": getpass.getuser(),
            "reference": reference,
            "issued_at": str(Timestamp.now()),
            "expires_at": str(expires),
            "scope": SCOPE,
        }
        if authorize is None or not authorize(
            {
                "operation": "authorize-native-maintenance",
                "assignment": assignment,
                "grant": grant,
            },
        ):
            raise PermissionError("Explicit native host approval required")
        await self.validate(assignment)
        if Timestamp.now().value >= expires.value:
            raise PermissionError("Native approval expired during consent")
        return self.save(item, "authorization", grant)

    def authority(self, assignment: dict[str, Any], grant: dict[str, Any]) -> None:
        """Recheck the persisted native grant, never a legacy standing grant."""
        linked = self.cycle.routine.check_reference(
            grant["reference"],
            subject=assignment["item"],
            kind="coding",
        )
        if linked is not None and not self.cycle.routine.callback(grant["reference"])(
            {
                "operation": "authorize-native-maintenance",
                "assignment": assignment,
                "grant": grant,
            },
        ):
            raise PermissionError("Routine grant differs from exact coding scope")
        if (
            self.record(assignment["item"], "authorization") != grant
            or grant["assignment_sha256"] != assignment["sha256"]
            or grant["principal"] != getpass.getuser()
            or grant["scope"] != SCOPE
            or not Timestamp.from_isoformat(grant["issued_at"]).value
            <= Timestamp.now().value
            < Timestamp.from_isoformat(grant["expires_at"]).value
        ):
            raise PermissionError(
                "Native authorization is expired, foreign or mismatched",
            )

    async def execute(  # noqa: C901, PLR0912, PLR0913, PLR0915 -- one Checkout lifecycle and explicit qualification
        self,
        item: str,
        *,
        interaction: ModelInteraction,
        profile: str,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
        measure_input: Callable[[ModelRequest], Awaitable[int]] | None = None,
        provider_context_tokens: int | None = None,
    ) -> dict[str, Any]:
        """Claim once, invoke the shared neutral process, then archive and restore."""
        from scripts.backlog.native.execution import execute  # noqa: PLC0415

        timer = Stopwatch()
        assignment, grant = (
            self.record(item, "assignment"),
            self.record(item, "authorization"),
        )
        await self.validate(assignment)
        self.authority(assignment, grant)
        worker = assignment["task"]["worker"]
        context = context_policy(assignment["task"])
        if context is not None and (
            measure_input is None
            or type(provider_context_tokens) is not int
            or provider_context_tokens < context.context_tokens
        ):
            raise PermissionError(
                "Native Context profile requires qualified provider capacity and token measurement",
            )
        if str(interaction.source) != worker["source"] or profile != worker["profile"]:
            raise PermissionError("Configured native worker source/profile differs")
        if authorize is None or not authorize(
            {
                "operation": "dispatch-native-maintenance",
                "assignment": assignment,
                "grant": grant,
            },
        ):
            raise PermissionError("Current native dispatch approval required")
        await self.validate(assignment)
        self.authority(assignment, grant)
        folder = self.cycle._folder(item)
        if (folder / "dispatch.json").exists():
            raise PermissionError(
                "Prior native dispatch exists; reconcile, never redispatch",
            )
        pending: dict[str, Any] | None = None
        try:
            async with Checkout(
                self.cycle,
                "native:" + assignment["sha256"],
                assignment["branch"],
                assignment["base_head"],
                files=[
                    {
                        "path": assignment["task"]["source"],
                        "text": assignment["baseline_source"],
                    },
                ],
            ) as checkout:
                self.cycle._checkout = checkout
                try:
                    scope = await self.validate(assignment, checkout)
                    self.authority(assignment, grant)
                    self.save(
                        item,
                        "dispatch",
                        {
                            "assignment_sha256": assignment["sha256"],
                            "authorization_sha256": grant["sha256"],
                            "at": str(Timestamp.now()),
                            "entry": "claimed; provider/Tool entry not yet established",
                        },
                    )

                    async def guard() -> None:
                        await self.validate(assignment, checkout)
                        self.authority(assignment, grant)

                    error = None
                    facts: dict[str, Any] = {}
                    try:
                        facts = await execute(
                            self,
                            assignment,
                            checkout,
                            interaction,
                            guard,
                            scope,
                            measure_input,
                        )
                    except (Exception, asyncio.CancelledError) as failure:  # noqa: BLE001 -- preserve unknown entry; no replay
                        error = type(failure).__name__ + ": " + str(failure)
                    candidate = facts.pop("candidate", None)
                    if candidate is not None:
                        patch = "".join(
                            difflib.unified_diff(
                                assignment["baseline_source"].splitlines(keepends=True),
                                candidate.splitlines(keepends=True),
                                fromfile="a/" + assignment["task"]["source"],
                                tofile="b/" + assignment["task"]["source"],
                            ),
                        )
                        from devtools.resources.filesystem import (  # noqa: PLC0415
                            TextFile,
                            write,
                        )

                        write(
                            TextFile(resolve_path(folder / "candidate.patch"), patch),
                            overwrite=False,
                        )
                    eligible = bool(
                        error is None
                        and facts.get("coding_accepted")
                        and facts.get("restored") is True
                        and (facts.get("acceptance") or {}).get("passed")
                        and candidate != assignment["baseline_source"]
                        and candidate is not None,
                    )
                    pending = {
                        "item": item,
                        "assignment_sha256": assignment["sha256"],
                        "authorization_sha256": grant["sha256"],
                        "worker": worker,
                        "disposition": "REVIEW_CANDIDATE" if eligible else "BLOCKED",
                        "candidate_sha256": hashlib.sha256(
                            candidate.encode(),
                        ).hexdigest()
                        if candidate is not None
                        else None,
                        "execution_error": error,
                        "seconds": timer.elapsed.total_seconds,
                        "facts": facts,
                        "integration_authorized": False,
                    }
                    execution_record = self.save(item, "execution", pending)
                    pending["execution_sha256"] = execution_record["sha256"]
                finally:
                    self.cycle._checkout = None

        except (Exception, asyncio.CancelledError) as failure:
            if pending is not None:
                self.save(
                    item,
                    "result",
                    {
                        **pending,
                        "disposition": "BLOCKED",
                        "checkout_released": False,
                        "release_error": type(failure).__name__ + ": " + str(failure),
                    },
                )
            raise
        if pending is None:
            raise RuntimeError("Native execution produced no terminal facts")
        releases = []
        for path in (self.cycle.root / ".local/backlog/checkout-history").glob(
            "*.json",
        ):
            from scripts.backlog.intake import load_json  # noqa: PLC0415

            if load_json(path).get("operation") == "native:" + assignment["sha256"]:
                releases.append(_load(path, "backlog-checkout-owner-v1")["sha256"])
        if len(releases) != 1:
            raise PermissionError("Native Checkout release identity is ambiguous")
        return self.save(
            item,
            "result",
            {
                **pending,
                "checkout_released": True,
                "checkout_release": releases[0],
                "seconds": timer.stop().total_seconds,
            },
        )

    async def review(  # noqa: PLR0913 -- explicit independent decision
        self,
        item: str,
        *,
        reviewer: str,
        reference: str,
        rationale: str,
        accept: bool,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
        proposal: str | None = None,
        attempt: str | None = None,
    ) -> dict[str, Any]:
        """Independently bind exact candidate, result and checks; never install it."""
        await self.cycle._coordinator()
        await idle(self.cycle.root)
        if (self.cycle.root / ".local/backlog/checkout-owner").exists():
            raise PermissionError("Checkout owned; independent review requires release")
        assignment, result = (
            self.record(item, "assignment"),
            self.record(item, "result"),
        )
        if (
            not reviewer.strip()
            or reviewer == assignment["task"]["worker"]["actor"]
            or not reference.strip()
            or not rationale.strip()
        ):
            raise PermissionError(
                "Independent reviewer and explicit decision provenance required",
            )
        self._candidate(assignment, result)
        proposed = None
        actor = self.reviewer.select(attempt)
        if attempt is not None and proposal is None:
            raise PermissionError(
                "Continuation disposition requires an exact model proposal",
            )
        if proposal is not None:
            packet = await actor.current(item)
            actor.authority(item, packet)
            proposed = actor.admit(item, proposal, reviewer, accept=accept)
        decision = {
            "item": item,
            "assignment_sha256": assignment["sha256"],
            "result_sha256": result["sha256"],
            "candidate_sha256": result["candidate_sha256"],
            "reviewer": reviewer,
            "principal": getpass.getuser(),
            "reference": reference,
            "rationale": rationale,
            "at": str(Timestamp.now()),
            "disposition": "ACCEPT_RECOMMENDED" if accept else "REJECTED",
            "installation_authorized": False,
        }
        if proposal is not None:
            decision["proposal_sha256"] = proposal
        if attempt is not None:
            decision["review_subject_sha256"] = attempt
        if authorize is None or not authorize(
            {
                "operation": "review-native-candidate",
                "assignment": assignment,
                "result": result,
                "decision": decision,
                **({"review_proposal": proposed} if proposal is not None else {}),
            },
        ):
            raise PermissionError("Current independent host review decision required")
        self._candidate(self.record(item, "assignment"), self.record(item, "result"))
        if proposal is not None:
            packet = await actor.current(item)
            actor.authority(item, packet)
            actor.admit(item, proposal, reviewer, accept=accept)
        payload = {
            "schema": "backlog-native-review-v2"
            if attempt is not None
            else "backlog-native-review-v1",
            **decision,
        }
        with self.cycle.intake._writer():
            return self.cycle._save(
                self.cycle._folder(item) / ("review-" + _digest(payload) + ".json"),
                payload,
            )

    def _candidate(
        self,
        assignment: dict[str, Any],
        result: dict[str, Any],
    ) -> tuple[str, str]:
        import hashlib  # noqa: PLC0415

        item = assignment["item"]
        approval = self.record(item, "authorization")
        if (
            assignment["coordinator"] != str(self.cycle.root)
            or fingerprint(assignment["task"]) != assignment["task_sha256"]
            or result["assignment_sha256"] != assignment["sha256"]
            or result["authorization_sha256"]
            != self.record(item, "authorization")["sha256"]
            or result["disposition"] != "REVIEW_CANDIDATE"
            or result["worker"] != assignment["task"]["worker"]
            or approval["assignment_sha256"] != assignment["sha256"]
            or result["execution_error"] is not None
            or result.get("checkout_released") is not True
        ):
            raise PermissionError("Native candidate/result/approval mismatch")
        if not re.fullmatch(r"[a-f0-9]{64}", result["checkout_release"]):
            raise PermissionError("Invalid native Checkout release identity")
        release = _load(
            self.cycle.root
            / ".local/backlog/checkout-history"
            / (result["checkout_release"] + ".json"),
            "backlog-checkout-owner-v1",
        )
        if (
            release["operation"] != "native:" + assignment["sha256"]
            or release["root"] != str(self.cycle.root)
            or release["branch"] != assignment["branch"]
            or release["revision"] != assignment["base_head"]
            or release["final_head"] != release["return_head"]
        ):
            raise PermissionError(
                "Native Checkout release does not bind this candidate",
            )
        facts = result["facts"]
        execution_record = self.record(item, "execution")
        if (
            result["execution_sha256"] != execution_record["sha256"]
            or execution_record["facts"] != facts
            or execution_record["candidate_sha256"] != result["candidate_sha256"]
        ):
            raise PermissionError(
                "Native terminal facts differ from pre-release observation",
            )
        if (
            not facts["coding_accepted"]
            or facts["restored"] is not True
            or facts["reconciliation_required"]
            or not facts["acceptance"]["passed"]
            or any(not e["acknowledged"] for e in facts["effects"])
        ):
            raise PermissionError("Native result lacks complete check/custody evidence")
        folder = self.cycle._folder(item)
        for observation in facts["observations"]:
            if not re.fullmatch(r"observation-\d{4}\.json", observation["file"]):
                raise PermissionError("Invalid native observation address")
            if (
                _load(
                    folder / "worker" / observation["file"],
                    "backlog-native-observation-v1",
                )["sha256"]
                != observation["sha256"]
            ):
                raise PermissionError("Native observation evidence changed")
        source, patch = (
            _read(folder / "worker/final-source.py"),
            _read(folder / "candidate.patch"),
        )
        expected = "".join(
            difflib.unified_diff(
                assignment["baseline_source"].splitlines(keepends=True),
                source.splitlines(keepends=True),
                fromfile="a/" + assignment["task"]["source"],
                tofile="b/" + assignment["task"]["source"],
            ),
        )
        if (
            source == assignment["baseline_source"]
            or hashlib.sha256(source.encode()).hexdigest() != result["candidate_sha256"]
            or patch != expected
        ):
            raise PermissionError("Native candidate bytes/diff changed")
        return source, hashlib.sha256(patch.encode()).hexdigest()

    def candidate(self, item: str, review: str) -> dict[str, Any]:
        """Authenticate the prospective branch of Integration's candidate reader."""
        if not re.fullmatch(r"[a-f0-9]{64}", review):
            raise ValueError("Invalid native review identity")
        assignment, result = (
            self.record(item, "assignment"),
            self.record(item, "result"),
        )
        # Review filenames include the ordinary full record identity, as legacy supervision does.
        decision = read_decision(
            self.cycle._folder(item) / ("review-" + review + ".json"),
        )
        linked = self.cycle.routine.check_reference(
            decision["reference"],
            subject=item,
            kind="host-review",
        )
        source, patch = self._candidate(assignment, result)
        if (
            decision["sha256"] != review
            or decision["assignment_sha256"] != assignment["sha256"]
            or decision["result_sha256"] != result["sha256"]
            or decision["candidate_sha256"] != result["candidate_sha256"]
            or decision["reviewer"] == assignment["task"]["worker"]["actor"]
            or decision["disposition"] != "ACCEPT_RECOMMENDED"
        ):
            raise PermissionError("Native independent review does not authenticate")
        proposed = None
        if "proposal_sha256" in decision:
            proposed = self.reviewer.select(
                decision.get("review_subject_sha256"),
            ).admit(
                item,
                decision["proposal_sha256"],
                decision["reviewer"],
                accept=True,
            )
        if linked is not None and not self.cycle.routine.callback(
            decision["reference"],
        )(
            {
                "operation": "review-native-candidate",
                "assignment": assignment,
                "result": result,
                "decision": {
                    k: v for k, v in decision.items() if k not in {"schema", "sha256"}
                },
                "review_proposal": proposed,
            },
        ):
            raise PermissionError("Host decision differs from exact routine authority")
        return {
            "assignment": assignment,
            "result": result,
            "review": decision,
            "source": source,
            "patch_sha256": patch,
        }
