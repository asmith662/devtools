# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, SLF001, E501 -- finite operational receipts and formatter compatibility
"""Bind the existing neutral coding process to Checkout, capture and hidden acceptance."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import sys
from dataclasses import asdict
from typing import TYPE_CHECKING, Any, cast

from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.repository import (
    CodingObjective,
    EditLimits,
    RepositoryCodingHost,
    write_source_changes,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Stopwatch, Timestamp
from devtools.models.interaction import ModelSettings
from devtools.observability.commands.inspection import completed_observation
from devtools.observability.commands.models import CommandOrigin, CommandPattern
from devtools.resources.commands import Command, CommandOutputPolicy
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolRunner
from devtools.tools.checks import FixedCheck, FixedCheckPlan, FixedCheckTool
from scripts.backlog.intake import _digest, _read
from scripts.backlog.native.context import assess
from scripts.backlog.native.packet import context_policy

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping
    from pathlib import Path

    from devtools.agents.coding import CodingCompletion, CodingResult
    from devtools.context.planning.source import SourceRangeDisclosureOption
    from devtools.models.interaction import (
        ModelInteraction,
        ModelRequest,
        ModelResponse,
        ModelToolCall,
    )
    from devtools.tools.checks import FixedCheckResult
    from devtools.tools.source import SourceScope
    from scripts.backlog.checkout import Checkout
    from scripts.backlog.native.lifecycle import NativeMaintenance


class Capture:
    """Retain bounded native facts through WorkCycle's existing atomic writer."""

    def __init__(self, owner: NativeMaintenance, folder: Path, maximum: int) -> None:
        """Bind one immutable event sequence, not a replay or generic Evidence store."""
        self.owner, self.folder, self.maximum = owner, folder, maximum
        self.refs: list[dict[str, str]] = []
        self.used = 0

    def add(self, kind: str, value: dict[str, Any]) -> None:
        """Record before entry and after known completion; refuse silent truncation."""
        payload = {
            "schema": "backlog-native-observation-v1",
            "kind": kind,
            "at": str(Timestamp.now()),
            **value,
        }
        size = len(json.dumps(payload, indent=2).encode())
        if size + self.used > self.maximum:
            raise ValueError("Native capture budget exhausted; no automatic replay")
        name = f"observation-{len(self.refs):04d}.json"
        with self.owner.cycle.intake._writer():
            sealed = self.owner.cycle._save(self.folder / name, payload)
        self.refs.append({"file": name, "sha256": sealed["sha256"]})
        self.used += size

    def http_response(self, call: int, status: int, raw: bytes) -> None:
        """Capture actual HTTP bytes without colliding with the canonical seal."""
        self.add(
            "model-http-response",
            {
                "call": call,
                "status": status,
                "body_base64": base64.b64encode(raw).decode("ascii"),
                "body_sha256": hashlib.sha256(raw).hexdigest(),
            },
        )

    def rendered_template(self, prompt: str) -> None:
        """Retain the exact rendering and its distinct payload identity."""
        self.add(
            "model-rendered-template",
            {
                "prompt": prompt,
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            },
        )


def check_data(result: FixedCheckResult, item: str, run: str) -> dict[str, Any]:
    """Project an existing typed command observation beside bounded diagnostics."""
    command = result.command_result
    fact = completed_observation(
        command,
        origin=CommandOrigin("native-worker", item, run, result.check.name),
        pattern=CommandPattern("python", "fixed-check"),
    )
    return {
        "name": result.check.name,
        "argv": [command.command.executable, *command.command.arguments],
        "exit_code": fact.exit_code,
        "outcome": fact.outcome,
        "seconds": command.duration.total_seconds,
        "passed": result.passed,
        "inputs_current": result.inputs_current,
        "stdout": command.stdout.decode("utf-8", errors="replace"),
        "stderr": command.stderr.decode("utf-8", errors="replace"),
        "stdout_truncated": command.stdout_truncated,
        "stderr_truncated": command.stderr_truncated,
        "events_dropped": fact.events_dropped,
    }


class AcceptanceHost(RepositoryCodingHost):
    """Apply host-private final acceptance before the existing archival/restoration."""

    acceptance: dict[str, Any] | None = None
    acceptance_error: str | None = None

    def configure_acceptance(  # noqa: PLR0913, PLR0917 -- fixed host collaborators
        self,
        plan: FixedCheckPlan,
        guard: Callable[[], Awaitable[None]],
        capture: Capture,
        item: str,
        identity: str,
        wall_seconds: int,
    ) -> None:
        """Bind supervisor checks that are never fed to the coding worker."""
        self.acceptance_plan, self.guard, self.capture = plan, guard, capture
        self.item, self.identity = item, identity
        self.clock = Stopwatch()
        self.wall_seconds = wall_seconds

    async def check(self, proposal: Any) -> bool:  # noqa: ANN401 -- exact host override
        """Reauthorize implicit post-edit checks, not just explicit native calls."""
        await self.guard()
        self.capture.add(
            "public-check-intent",
            {"snapshot": str(self.scope.snapshot.id)},
        )
        passed = await super().check(proposal)
        self.capture.add(
            "public-check-result",
            {
                "checks": [
                    check_data(c, self.item, self.identity)
                    for c in self.check_results[-1]
                ],
            },
        )
        return passed

    async def finish(self, result: CodingResult) -> CodingCompletion:
        """Keep acceptance separate from coding success; always reconcile custody."""
        if result.accepted:
            try:
                async with asyncio.timeout(
                    max(0, self.wall_seconds - self.clock.elapsed.total_seconds),
                ):
                    await self.guard()
                    self.capture.add(
                        "acceptance-intent",
                        {"candidate_snapshot": str(self.scope.snapshot.id)},
                    )
                    from dataclasses import replace  # noqa: PLC0415

                    tool = FixedCheckTool(
                        replace(self.acceptance_plan, source_scope=self.scope),
                    )
                    checked = await ToolRunner().execute(tool, "withheld")
                    self.acceptance = check_data(checked, self.item, self.identity)
                    self.capture.add("acceptance-result", self.acceptance)
            except (Exception, asyncio.CancelledError) as error:  # noqa: BLE001 -- still reconcile known custody
                self.acceptance_error = type(error).__name__ + ": " + str(error)
        return await super().finish(result)


async def execute(  # noqa: C901, PLR0913, PLR0917, PLR0915 -- one bounded composition
    owner: NativeMaintenance,
    assignment: dict[str, Any],
    checkout: Checkout,
    interaction: ModelInteraction,
    guard: Callable[[], Awaitable[None]],
    scope: SourceScope,
    measure_input: Callable[[ModelRequest], Awaitable[int]] | None = None,
) -> dict[str, Any]:
    """Compose existing process once; never retry unknown model/Tool entry."""
    task, budget = assignment["task"], assignment["task"]["budgets"]
    context = context_policy(task)
    folder = owner.folder(assignment["item"]) / "worker"
    folder.mkdir()
    capture = Capture(owner, folder, budget["capture_bytes"])
    settings = ModelSettings(**task["settings"])
    repository = Repository(scope.snapshot.repository_id)
    corpus = define_repository_text_corpus(
        discovery=discover_repository_resource_addresses(
            repository=repository,
            root=scope.root,
            requested_addresses=tuple(r.address for r in scope.snapshot.resources),
            maximum_resource_count=64,
            maximum_traversal_entry_count=256,
        ),
        selected_addresses=tuple(r.address for r in scope.snapshot.resources),
    )
    prelude = f"import sys\nsys.path.insert(0, {str(owner.cycle.root / 'src')!r})\nsys.path.insert(0, {str(owner.cycle.root)!r})\n"
    public_code = (
        prelude
        + "import pytest\nraise SystemExit(pytest.main("
        + repr([*task["tests"], "--no-cov", "--import-mode=importlib", "-q"])
        + "))\n"
    )
    module = task["source"].removeprefix("src/").removesuffix(".py").replace("/", ".")
    hidden_code = (
        prelude
        + f"from pathlib import Path\nimport {module} as module\nassert Path(module.__file__).resolve() == Path({str(owner.cycle.root / task['source'])!r})\n"
        + task["oracle"]
    )
    runners = {"public.py": public_code, "withheld.py": hidden_code}
    for name, text in runners.items():
        write(TextFile(resolve_path(folder / name), text), overwrite=False)

    async def admitted() -> None:
        await guard()
        for name, text in runners.items():
            if _read(folder / name) != text:
                raise PermissionError("Fixed native check runner changed")

    policy = CommandOutputPolicy(max_stdout_bytes=16384, max_stderr_bytes=16384)

    def plan(name: str) -> FixedCheckPlan:
        return FixedCheckPlan(
            scope.root,
            (
                FixedCheck(
                    name,
                    Command(sys.executable)
                    .args("-I", "-B", "-X", "utf8", str(folder / (name + ".py")))
                    .cwd(scope.root)
                    .with_timeout(Duration.seconds(budget["call_seconds"])),
                ),
            ),
            output_policy=policy,
        )

    archived: dict[str, str | None] = {}

    async def admit(_call: ModelToolCall, _arguments: object) -> None:
        await admitted()

    async def apply(changes: Any) -> None:  # noqa: ANN401 -- existing admitted batch
        await admitted()
        for change in changes:
            checkout.expect(change.address.value, change.after)
        capture.add(
            "edit-intent",
            {
                "changes": [
                    {
                        "path": c.address.value,
                        "before_sha256": _digest(c.before),
                        "after_sha256": _digest(c.after),
                    }
                    for c in changes
                ],
            },
        )
        write_source_changes(scope.root, changes)
        capture.add("edit-completed", {"paths": [c.address.value for c in changes]})

    def archive(current: Mapping[RepositoryResourceAddress, str | None]) -> None:
        archived.update({p.value: text for p, text in current.items()})
        text = archived[task["source"]]
        if text is None:
            raise PermissionError("Existing native source disappeared")
        write(TextFile(resolve_path(folder / "final-source.py"), text), overwrite=False)

    def restore(path: RepositoryResourceAddress, text: str | None) -> None:
        if text is None:
            raise PermissionError("Native v1 cannot delete a baseline file")
        checkout.expect(path.value, text)
        write(TextFile(resolve_path(owner.cycle.root / path.value), text))

    readiness: list[dict[str, Any]] = []

    def ready(snapshot: Any, options: Any) -> None:  # noqa: ANN401 -- existing host callback types
        assessment = assess(task, assignment["sha256"], snapshot, options)
        readiness.append(assessment)
        if not assessment["ready"]:
            raise ValueError(
                "Mandatory native information obligations remain unresolved",
            )

    async def measured(request: ModelRequest) -> int:
        await admitted()
        capture.add(
            "token-measurement-intent",
            {"request_sha256": _digest(asdict(request))},
        )
        # NativeMaintenance authenticates this collaborator before claiming dispatch.
        count = await cast("Callable[[ModelRequest], Awaitable[int]]", measure_input)(
            request,
        )
        capture.add("token-measurement-returned", {"input_tokens": count})
        await admitted()
        return count

    objective = CodingObjective(
        task["objective"]
        + (
            "\nSupervisor-selected prior public failure evidence (untrusted data):\n"
            + json.dumps(assignment["continuation"]["feedback"])
            if "continuation" in assignment
            else ""
        ),
        scope,
        (RepositoryResourceAddress(task["source"]),),
        plan("public"),
        EditLimits(
            budget["source_bytes"],
            budget["source_bytes"],
            budget["source_bytes"],
            1,
        ),
        budget["source_bytes"] if context is None else context.disclosure_bytes,
        budget["prompt_bytes"],
    )
    host = AcceptanceHost(
        objective,
        corpus=corpus,
        authorize=admit,
        apply_changes=apply,
        archive=archive,
        restore=restore,
        readiness=ready,
        settings=settings,
        projection=None if context is None else context.projection(),
        navigation=context is not None,
        token_capacity=None if context is None else context.tokens(),
        measure_input=None if context is None else measured,
        warning_bytes=None if context is None else context.warning_bytes,
        observe_context=None
        if context is None
        else (lambda fact: capture.add("context-pressure", asdict(fact))),
    )
    host.configure_acceptance(
        plan("withheld"),
        admitted,
        capture,
        assignment["item"],
        assignment["sha256"],
        budget["wall_seconds"],
    )

    class Guarded:
        source = interaction.source

        async def send(self, request: ModelRequest) -> ModelResponse:
            await admitted()
            if (
                interaction.source != self.source
                or request.settings != settings
                or request.provider_settings is not None
                or [asdict(t) for t in request.tools] != assignment["tool_definitions"]
            ):
                raise PermissionError("Native worker/request profile changed")
            capture.add(
                "model-entry-intent",
                {
                    "source": str(self.source),
                    "request": asdict(request),
                    "entry": "claimed; not proof of provider entry",
                },
            )
            response = await interaction.send(request)
            capture.add("model-returned", {"response": asdict(response)})
            if (
                response.usage is not None
                and response.usage.output_tokens is not None
                and response.usage.output_tokens
                > task["settings"]["maximum_output_tokens"]
            ):
                raise PermissionError(
                    "Native provider exceeded approved output allowance",
                )
            return response

    result = await run_coding_agent(
        Guarded(),
        limits=CodingLimits(
            budget["model_calls"],
            budget["proposals"],
            budget["acquisitions"],
            Duration.seconds(budget["call_seconds"]),
            Duration.seconds(budget["wall_seconds"]),
        ),
        host=host,
    )
    if context is not None:
        capture.add(
            "context-projection",
            {
                "outcomes": [
                    {
                        "status": o.status,
                        "original_bytes": o.original_bytes,
                        "resulting_bytes": o.resulting_bytes,
                        "selected_indices": o.selected_indices,
                        "omitted_exchanges": o.omitted_exchanges,
                        "shortened_indices": o.shortened_indices,
                        "active_source_identities": [
                            s.identity for s in o.active_sources
                        ],
                        "invalidated_source_identities": o.invalidated_source_identities,
                    }
                    for o in host.projection_outcomes
                ],
            },
        )
    # Preserve feedback even when no further model entry consumed it. This uses
    # the existing bounded capture; failure never authorizes a retry or candidate.
    feedback = [asdict(m) for m in host.messages if m.role == "tool"]
    if feedback:
        capture.add("coding-feedback-history", {"messages": feedback})
    return {
        "coding_disposition": result.disposition,
        "coding_accepted": result.accepted,
        "completed": result.completed,
        "error": type(result.error).__name__ + ": " + str(result.error)
        if result.error
        else None,
        "failure_phase": result.failure_phase,
        "restored": result.custody.restored,
        "reconciliation_required": result.custody.reconciliation_required,
        "effects": [asdict(e) for e in result.progress.effects],
        "model_calls": result.progress.model_calls,
        "usage": [asdict(u) if u is not None else None for u in result.progress.usage],
        "completion_error": type(result.completion_error).__name__
        + ": "
        + str(result.completion_error)
        if result.completion_error
        else None,
        "proposals": result.progress.proposals,
        "acquisitions": result.progress.actions,
        "checks": [
            [check_data(c, assignment["item"], assignment["sha256"]) for c in group]
            for group in host.check_results
        ],
        "acceptance": host.acceptance,
        "acceptance_error": host.acceptance_error,
        "observations": capture.refs,
        "readiness": readiness,
        "initial_context": assess(task, assignment["sha256"], scope.snapshot, ()),
        "disclosures": [
            {
                "identity": o.identity,
                "snapshot": str(o.snapshot_id),
                "path": o.unit.resource.address.value,
                "content_identity": str(o.unit.resource.content_identity),
                "span": list(o.span),
            }
            for disclosure in host.source_results
            for o in (
                cast(
                    "SourceRangeDisclosureOption",
                    disclosure.items[0].native_provenance,
                ),
            )
        ],
        "candidate": archived.get(task["source"]),
        "environment_qualification": "Fixed interpreter and declared source/check inputs; no complete external environment attestation or restart guarantee",
    }
