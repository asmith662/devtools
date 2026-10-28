# Copyright (c) 2026
"""One real repository-discovery case; the framework owns the coding/repair loop."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

import support as s

from devtools.agents.coding import CodingLimits, run_coding_agent
from devtools.agents.coding.models import CodingEffect
from devtools.agents.coding.repository import (
    CodingObjective,
    EditLimits,
    RepositoryCodingHost,
    write_source_changes,
)
from devtools.agents.model_tools import (
    execute_model_tool_call,
    normalize_tool_descriptor,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.identity import RepositoryId
from devtools.context.retrieval import search_repository_source
from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Stopwatch, Timestamp
from devtools.models.interaction import ModelSettings, PromptMessage
from devtools.observability.commands.models import CommandOrigin
from devtools.observability.commands.patterns import summarize_patterns
from devtools.resources.commands import Command, CommandOutputPolicy
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolDescriptor, ToolRunner
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.repository.validation import (
    ChangeValidationPlan,
    CheckSelection,
    InspectAndValidateTool,
)
from devtools.tools.source import SourceScope

BASE = "559ad49033e0d2389b68fa321cee870506e814aa"
CASE, CANONICAL, STATE = s.CASE, s.CANONICAL, s.STATE
READ = tuple(
    RepositoryResourceAddress(p.relative_to(CASE / "fixture").as_posix())
    for p in sorted((CASE / "fixture").rglob("*"))
    if p.is_file() and "__pycache__" not in p.parts
)
EDITABLE = tuple(
    a for a in READ if a.value.startswith("releasevault/") and a.value.endswith(".py")
)
LIST = ToolDescriptor(
    "list_repository",
    "List authorized snapshot resources, sizes and read/edit permissions. Metadata only, not acquired source.",
    '{"type":"object","maxProperties":0}',
)
SEARCH = ToolDescriptor(
    "search_source",
    "Search existing file/symbol/window retrieval by query. Returns ranked metadata, not source. Read selected ranges separately; full file lengths are supplied.",
    '{"type":"object","properties":{"query":{"type":"string","minLength":1,"maxLength":256}},"required":["query"],"additionalProperties":false}',
)
PROCEDURE = ToolDescriptor(
    "inspect_and_validate_change",
    "Inspect authorized changes and execute host-fixed focused acceptance. No command/scope arguments.",
    '{"type":"object","maxProperties":0}',
)


def decode(arguments, fields):
    def pairs(values):
        result = dict(values)
        if len(result) != len(values):
            raise ValueError("Duplicate Tool argument member")
        return result

    value = json.loads(arguments, object_pairs_hook=pairs)
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError("Tool arguments differ from the frozen schema")
    return value


class Invocation:
    def __init__(self, descriptor):
        self.descriptor = descriptor

    def materialize(self, arguments):
        if self.descriptor.name == SEARCH.name:
            query = decode(arguments, {"query"})["query"]
            if not isinstance(query, str) or not query.strip() or len(query) > 256:
                raise ValueError("Search query requires bounded nonempty text")
            return "search", query
        decode(arguments, set())
        return ("list", None) if self.descriptor.name == LIST.name else None


class DiscoveryTool:
    """Case composition over existing grounded discovery and canonical retrieval."""

    name = "repository_discovery"
    description = "Read-only scoped repository metadata; no source effect."

    def __init__(self, host):
        self.host = host

    def validate(self, arguments):
        self.host.scope.check_current()
        if arguments[0] not in {"list", "search"}:
            raise ValueError("Unavailable discovery operation")

    async def execute(self, arguments):
        scope = self.host.scope
        if arguments[0] == "list":
            return {
                "snapshot": str(scope.snapshot.id),
                "source_acquired": False,
                "resources": [
                    {
                        "path": str(r.address),
                        "characters": len(r.content),
                        "content_identity": str(r.content_identity),
                        "editable": r.address in self.host.objective.editable,
                    }
                    for r in scope.snapshot.resources
                ],
            }
        result = search_repository_source(
            self.host.index, query=arguments[1], mode="mixed", maximum_results=6
        )
        return {
            "snapshot": str(scope.snapshot.id),
            "source_acquired": False,
            "query": result.query,
            "mode": result.mode,
            "hits": [
                {
                    "path": str(h.unit.resource.address),
                    "unit": str(h.unit.id),
                    "kind": h.unit.kind,
                    "qualified_name": h.unit.qualified_name,
                    "span": [h.unit.start, h.unit.end],
                    "file_characters": len(h.unit.resource.content),
                    "content_identity": str(h.unit.resource.content_identity),
                    "rank": h.rank,
                    "score": h.score,
                    "evidence": [
                        {"view": e.view, "rank": e.rank, "score": e.match.score}
                        for e in h.evidence
                    ],
                }
                for h in result.hits
            ],
        }


def checks(root, scope):
    return FixedCheckPlan(
        resolve_path(root),
        (
            FixedCheck(
                "focused-acceptance",
                Command(sys.executable)
                .args("-B", "acceptance.py")
                .cwd(resolve_path(root))
                .with_timeout(Duration.seconds(30)),
            ),
        ),
        source_scope=scope,
        output_policy=CommandOutputPolicy(max_stdout_bytes=8192, max_stderr_bytes=8192),
    )


def procedure_tool(root, scope, revision, label):
    return InspectAndValidateTool(
        ChangeValidationPlan(
            checks(root, scope),
            revision,
            frozenset(EDITABLE),
            (CheckSelection("focused-acceptance"),),
        ),
        origin=CommandOrigin(
            "local-dogfood-host", "release-order", "primary-0002", label
        ),
    )


async def execute_procedure(tool):
    try:
        return await ToolRunner().execute(tool, None)
    finally:
        if tool.last_report is not None:
            s.OBSERVATIONS.extend(tool.last_report.observations)


class Host(RepositoryCodingHost):
    """Experimental Tool exposure, never a second model/repair state machine."""

    async def prepare(self, progress):
        request = await super().prepare(progress)
        request = replace(
            request,
            tools=(
                *request.tools,
                *(normalize_tool_descriptor(d) for d in (LIST, SEARCH, PROCEDURE)),
            ),
        )
        self.requests[-1] = request
        return request

    def classify(self, response):
        allowed = {
            "read_source",
            "validate_candidate",
            LIST.name,
            SEARCH.name,
            PROCEDURE.name,
        }
        if response.tool_calls and all(c.name in allowed for c in response.tool_calls):
            self.scope.check_current()
            self.messages.append(
                PromptMessage("assistant", response.content, response.tool_calls)
            )
            return "acquire"
        return super().classify(response)

    async def acquire(self, response):
        if (
            len(response.tool_calls)
            > self.progress.limits.tool_actions - self.progress.actions
        ):
            raise ValueError("Frozen acquisition budget exceeded")
        ready = False
        for call in response.tool_calls:
            if call.name in {"read_source", "validate_candidate"}:
                before = len(self.messages)
                ready = (
                    await super().acquire(replace(response, tool_calls=(call,)))
                    or ready
                )
                for message in self.messages[before:]:
                    if message.role == "tool":
                        self.acquisitions.append(
                            {
                                "kind": "source"
                                if call.name == "read_source"
                                else "model-check",
                                "call_id": call.provider_call_id,
                                "name": call.name,
                                "arguments": call.arguments_json,
                                "result": json.loads(message.content),
                            }
                        )
                continue
            effect = self.progress.claim_action(call.provider_call_id)
            if call.name in {LIST.name, SEARCH.name}:
                descriptor = LIST if call.name == LIST.name else SEARCH
                value = await execute_model_tool_call(
                    call,
                    invocation=Invocation(descriptor),
                    tool=DiscoveryTool(self),
                    admit=self.authorize,
                    runner=ToolRunner(),
                )
                self.acquisitions.append(
                    {
                        "kind": "retrieval"
                        if call.name == SEARCH.name
                        else "inventory",
                        "call_id": call.provider_call_id,
                        "name": call.name,
                        "arguments": call.arguments_json,
                        "result": value,
                    }
                )
            else:
                tool = procedure_tool(
                    self.scope.root.value,
                    self.scope,
                    self.revision,
                    "model-procedure-" + str(self.progress.actions),
                )
                try:
                    report = await execute_model_tool_call(
                        call,
                        invocation=Invocation(PROCEDURE),
                        tool=tool,
                        admit=self.authorize,
                        runner=ToolRunner(),
                    )
                finally:
                    if tool.last_report is not None:
                        s.OBSERVATIONS.extend(tool.last_report.observations)
                self.procedures.append(
                    {
                        "trigger": "model",
                        "call_id": call.provider_call_id,
                        "report": s.plain(report),
                    }
                )
                value = {
                    "status": report.status,
                    "checks": [
                        {
                            "status": c.status,
                            "exit_code": c.result.command_result.exit_code
                            if c.result
                            else None,
                            "stdout": c.result.command_result.stdout.decode(
                                errors="replace"
                            )
                            if c.result
                            else None,
                            "stderr": c.result.command_result.stderr.decode(
                                errors="replace"
                            )
                            if c.result
                            else None,
                        }
                        for c in report.checks
                    ],
                }
            effect.acknowledged = True
            self.messages.append(
                PromptMessage(
                    "tool", json.dumps(value), tool_call_id=call.provider_call_id
                )
            )
        return ready

    async def propose(self, response):
        result = await super().propose(response)
        self.proposal_events.append(
            {
                "snapshot": str(self.scope.snapshot.id),
                "calls": s.plain(response.tool_calls),
                "admitted": result is not None,
                "source_disclosures": [
                    {
                        "path": str(d.unit.resource.address),
                        "content_identity": str(d.unit.resource.content_identity),
                        "span": d.span,
                        "snapshot": str(d.snapshot_id),
                    }
                    for d in self.disclosures
                ],
                "changes": s.plain(result),
            }
        )
        return result

    async def check(self, proposal):
        del proposal
        effect = CodingEffect("check", (), check_name="focused-acceptance")
        self.progress.effects.append(effect)
        report = await execute_procedure(
            procedure_tool(
                self.scope.root.value,
                self.scope,
                self.revision,
                "host-check-" + str(len(self.check_results)),
            )
        )
        self.procedures.append(
            {"trigger": "deterministic-host-validation", "report": s.plain(report)}
        )
        self.check_results.append(
            tuple(c.result for c in report.checks if c.result is not None)
        )
        if report.error is not None:
            raise report.error
        if report.status not in {"passed", "failed"}:
            raise RuntimeError(
                "Fixed check procedure refused or has incomplete acknowledgment"
            )
        effect.acknowledged = True
        return report.status == "passed"


async def grade(root, label, *, reference=False, focused=False):
    argv = ["-B", str(CASE / "oracle.py"), str(root)]
    if reference:
        argv.append("--reference")
    if focused:
        argv.append("--focused")
    return await s.managed(
        Command(sys.executable)
        .args(*argv)
        .cwd(resolve_path(root))
        .with_timeout(Duration.seconds(30)),
        label,
    )


async def prepare():
    if (CASE / "freeze.json").exists() or (STATE / "ENTERED.json").exists():
        raise RuntimeError("Case already frozen/entered; preserve it, never regenerate")
    STATE.mkdir(parents=True, exist_ok=True)
    if (
        await s.git(CANONICAL, "rev-parse", "HEAD") != BASE
        or await s.git(CANONICAL, "diff", "--name-only")
        or await s.git(CANONICAL, "diff", "--cached", "--name-only")
    ):
        raise RuntimeError("Canonical baseline or tracked custody diverged")
    if (CANONICAL / ".local/backlog/checkout-owner").exists():
        raise RuntimeError("Canonical Checkout owner occupied")
    identity = await s.service_identity()
    if identity["context"] != 32768:
        raise RuntimeError("Selected actual model context differs from frozen profile")
    root = Path(tempfile.mkdtemp(prefix="devtools-local-coding-case2-"))
    for file in (CASE / "fixture").rglob("*"):
        if file.is_file() and "__pycache__" not in file.parts:
            target = root / file.relative_to(CASE / "fixture")
            target.parent.mkdir(parents=True, exist_ok=True)
            write(
                TextFile(resolve_path(target), file.read_text(encoding="utf-8")),
                overwrite=False,
            )
    write(
        TextFile(resolve_path(root / ".gitignore"), "__pycache__/\n*.pyc\n"),
        overwrite=False,
    )
    await s.git(root, "init")
    await s.git(root, "add", "--all")
    await s.git(
        root,
        "-c",
        "user.name=Devtools authored fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-m",
        "Freeze authored release catalog task",
    )
    revision = await s.git(root, "rev-parse", "HEAD")
    repository = Repository.new()
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=repository,
        addresses=READ,
        maximum_resource_bytes=32768,
    )
    baseline = await execute_procedure(
        procedure_tool(root, scope, revision, "baseline-procedure")
    )
    hidden = await grade(root, "baseline-heldout")
    positive_focused = await grade(
        root, "reference-focused", reference=True, focused=True
    )
    positive_hidden = await grade(root, "reference-heldout", reference=True)
    if (
        baseline.status != "failed"
        or b"Ran 7 tests" not in baseline.checks[0].result.command_result.stderr
        or b"failures=4" not in baseline.checks[0].result.command_result.stderr
    ):
        raise RuntimeError(
            "Baseline focused failures differ from the authored four assertions"
        )
    if (
        hidden.exit_code != 1
        or b"Ran 10 tests" not in hidden.stderr
        or b"failures=3" not in hidden.stderr
    ):
        raise RuntimeError(
            "Baseline heldout failures differ from the authored three assertions"
        )
    if positive_focused.exit_code or positive_hidden.exit_code:
        raise RuntimeError(
            "Independent finite-reference positive oracle control failed"
        )
    prompt = (CASE / "objective.md").read_text(encoding="utf-8")
    s.save(STATE / "initial-prompt.json", {"content": prompt}, fresh=True)
    frozen = dict(
        schema="local-coding-dogfood-freeze-v2",
        at=str(Timestamp.now()),
        canonical_main=BASE,
        task_root=str(root),
        task_revision=revision,
        repository_id=str(repository.id),
        snapshot_id=str(scope.snapshot.id),
        source_snapshot=s.plain(scope.snapshot),
        files=s.frozen_files(),
        task_files={
            p.relative_to(root).as_posix(): s.digest(p)
            for p in root.rglob("*")
            if p.is_file() and ".git" not in p.parts
        },
        prompt_sha256=s.digest(STATE / "initial-prompt.json"),
        available_resources=[str(a) for a in READ],
        editable=[str(a) for a in EDITABLE],
        required_source_witnesses=None,
        service=identity,
        limits=dict(
            model_calls=6,
            proposals=3,
            repair_opportunities=2,
            acquisition_actions=16,
            call_seconds=180,
            agent_wall_seconds=1080,
            outer_wall_seconds=1200,
            input_tokens=28160,
            output_tokens=4096,
            prompt_bytes=32768,
            disclosure_bytes=8192,
            source_bytes=32768,
            region_bytes=4096,
            aggregate_bytes=8192,
            operations=2,
        ),
        settings=dict(
            thinking_enabled=False,
            maximum_output_tokens=4096,
            sampling=s.QWEN38_INSTRUCT_SAMPLING,
        ),
        tools=[
            "list_repository",
            "search_source",
            "read_source",
            "replace_source",
            "validate_candidate",
            PROCEDURE.name,
        ],
        baseline=s.plain(baseline),
        oracle_controls=s.RECORDS[-3:],
        scoring=dict(
            worker_success="CodingResult.accepted and known completed/restored custody",
            candidate_correct="All frozen focused and heldout tests pass on exact archived candidate; no codex intervention",
            discovery="Report separately listing/search results, chosen reads, actual source text consumed, and grounding of admitted targets; no mandatory target file",
            repair="Only actual failed-check feedback consumed by a later inference and a corrective model edit counts; never force failure",
            incomplete="Failure/limit/stopped/malformed/unknown outcomes remain qualified; heldout alone does not turn incomplete worker into success",
        ),
        privacy="Authored synthetic source/tests only; no personal logs, secrets or raw environment analytics.",
    )
    frozen["task_digest"] = s.hashlib.sha256(
        json.dumps(frozen, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    s.save(CASE / "freeze.json", frozen, fresh=True)
    s.save(STATE / "prepare-records.json", s.RECORDS)
    print(
        json.dumps(
            dict(
                task_root=str(root),
                revision=revision,
                snapshot=str(scope.snapshot.id),
                digest=frozen["task_digest"],
                resources=len(READ),
                editable=len(EDITABLE),
                baseline_focused_failures=4,
                baseline_heldout_failures=3,
                reference_focused_exit=positive_focused.exit_code,
                reference_heldout_exit=positive_hidden.exit_code,
            )
        )
    )


async def run():
    frozen = json.loads((CASE / "freeze.json").read_text(encoding="utf-8"))
    if (
        s.frozen_files() != frozen["files"]
        or s.digest(STATE / "initial-prompt.json") != frozen["prompt_sha256"]
    ):
        raise RuntimeError("Frozen source/host/oracle changed")
    root = Path(frozen["task_root"])
    if (
        await s.git(root, "rev-parse", "HEAD") != frozen["task_revision"]
        or await s.git(root, "status", "--porcelain")
        or await s.git(CANONICAL, "rev-parse", "HEAD") != BASE
    ):
        raise RuntimeError("Frozen task or canonical baseline diverged")
    s.save(
        STATE / "ENTERED.json",
        {"at": str(Timestamp.now()), "task_digest": frozen["task_digest"]},
        fresh=True,
    )
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=Repository(RepositoryId.parse(frozen["repository_id"])),
        addresses=READ,
        maximum_resource_bytes=32768,
    )
    if str(scope.snapshot.id) != frozen["snapshot_id"]:
        raise RuntimeError("Frozen snapshot mismatch")
    corpus = define_repository_text_corpus(
        discovery=discover_repository_resource_addresses(
            repository=Repository(scope.snapshot.repository_id),
            root=scope.root,
            requested_addresses=READ,
            maximum_resource_count=24,
            maximum_traversal_entry_count=128,
        ),
        selected_addresses=READ,
    )
    admissions, applied = [], []

    def archive(current):
        candidate = STATE / "candidate"
        for file in (CASE / "fixture").rglob("*"):
            if file.is_file() and "__pycache__" not in file.parts:
                target = candidate / file.relative_to(CASE / "fixture")
                target.parent.mkdir(parents=True, exist_ok=True)
                write(
                    TextFile(resolve_path(target), file.read_text(encoding="utf-8")),
                    overwrite=False,
                )
        for address, text in current.items():
            if text is None:
                raise RuntimeError("Missing/unknown candidate source")
            write(TextFile(resolve_path(candidate / address.value), text))
        s.save(
            STATE / "candidate-hashes.json",
            {
                p.relative_to(candidate).as_posix(): s.digest(p)
                for p in candidate.rglob("*")
                if p.is_file()
            },
        )

    def restore(address, text):
        if address not in EDITABLE or text is None:
            raise RuntimeError("Refuse unknown/foreign restoration")
        write(TextFile(resolve_path(root / address.value), text))

    async def authorize(call, arguments):
        if call.name not in frozen["tools"]:
            raise PermissionError("Operation outside frozen authority")
        admissions.append(
            {
                "call_id": call.provider_call_id,
                "name": call.name,
                "typed_input_kind": type(arguments).__name__,
            }
        )

    async def apply_changes(changes):
        if any(c.address not in EDITABLE for c in changes):
            raise PermissionError("Unauthorized editing surface")
        applied.append(s.plain(changes))
        write_source_changes(scope.root, changes)

    objective = CodingObjective(
        json.loads((STATE / "initial-prompt.json").read_text())["content"],
        scope,
        EDITABLE,
        checks(root, scope),
        EditLimits(4096, 32768, 8192, 2),
        8192,
        32768,
    )
    host = Host(
        objective,
        corpus=corpus,
        authorize=authorize,
        apply_changes=apply_changes,
        archive=archive,
        restore=restore,
        settings=ModelSettings(maximum_output_tokens=4096, thinking_enabled=False),
    )
    host.revision = frozen["task_revision"]
    host.acquisitions, host.proposal_events, host.procedures = [], [], []
    interaction = s.MeasuredInteraction()
    timer = Stopwatch()
    result = await run_coding_agent(
        interaction,
        limits=CodingLimits(6, 3, 16, Duration.seconds(180), Duration.seconds(1080)),
        host=host,
    )
    timer.stop()
    s.save(
        STATE / "worker-result.json",
        dict(
            at=str(Timestamp.now()),
            result=s.plain(result),
            accepted=result.accepted,
            seconds=timer.elapsed.total_seconds,
            admissions=admissions,
            applied=applied,
            acquisitions=host.acquisitions,
            proposals=host.proposal_events,
            procedures=host.procedures,
            requests=interaction.records,
            messages=s.plain(host.messages),
            original_scope=s.plain(scope),
            final_scope=s.plain(host.scope),
        ),
        fresh=True,
    )
    candidate = STATE / "candidate"
    hidden = await grade(candidate, "final-heldout")
    focused = await s.managed(
        Command(sys.executable)
        .args("-B", "acceptance.py")
        .cwd(resolve_path(candidate))
        .with_timeout(Duration.seconds(30)),
        "final-focused",
    )
    restored = await s.git(root, "status", "--porcelain")
    s.save(
        STATE / "outcome.json",
        dict(
            at=str(Timestamp.now()),
            task_digest=frozen["task_digest"],
            worker_accepted=result.accepted,
            disposition=result.disposition,
            candidate_validated=result.candidate_validated,
            completed=result.completed,
            failure_phase=result.failure_phase,
            error_kind=type(result.error).__name__ if result.error else None,
            error=str(result.error) if result.error else None,
            model_requests=result.progress.model_calls,
            inference_entries=sum(r["inference_entered"] for r in interaction.records),
            proposals=result.progress.proposals,
            acquisition_actions=result.progress.actions,
            applied_batches=len(applied),
            seconds=timer.elapsed.total_seconds,
            focused_exit=focused.exit_code,
            heldout_exit=hidden.exit_code,
            restored_git_status=restored,
            command_records=s.RECORDS,
            command_observations=s.plain(s.OBSERVATIONS),
            patterns=s.plain(summarize_patterns(tuple(s.OBSERVATIONS))),
        ),
        fresh=True,
    )
    print(
        json.dumps(
            dict(
                accepted=result.accepted,
                disposition=result.disposition,
                calls=result.progress.model_calls,
                proposals=result.progress.proposals,
                applied=len(applied),
                focused_exit=focused.exit_code,
                heldout_exit=hidden.exit_code,
                seconds=timer.elapsed.total_seconds,
            )
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    asyncio.run(prepare() if parser.parse_args().mode == "prepare" else run())
