# Copyright (c) 2026
"""One frozen real-model consumer; all coding/repair sequencing is framework-owned."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
import tempfile
import urllib.request
from dataclasses import asdict, is_dataclass, replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

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
from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Stopwatch, Timestamp
from devtools.models.interaction import InteractionSource, ModelSettings, PromptMessage
from devtools.models.interaction.providers.llama_cpp import LlamaCppInteraction
from devtools.models.interaction.providers.llama_cpp_request_settings import (
    LlamaCppRequestSettings,
)
from devtools.observability.commands.inspection import completed_observation
from devtools.observability.commands.models import CommandOrigin, CommandPattern
from devtools.observability.commands.patterns import summarize_patterns
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolDescriptor, ToolRunner
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.repository.validation import (
    ChangeValidationPlan,
    CheckSelection,
    InspectAndValidateTool,
)
from devtools.tools.source import SourceScope
from scripts.qwen.llama_cpp_profile import (
    QWEN38_27B_UD_IQ4_XS,
    QWEN38_INSTRUCT_SAMPLING,
)

CASE = Path(__file__).resolve().parent
CANONICAL = CASE.parents[2]
STATE = CANONICAL / ".local/local-coding-dogfood-0001"
CONTAINER = "devtools-qwen38-llama-cpp"
BASE = "8f1466ec0f7b71984a63cb6b0512d075b8e282a4"
READ = tuple(
    RepositoryResourceAddress("stockroom/" + p)
    for p in ("events.py", "keys.py", "projection.py", "reports.py")
)
EDIT = RepositoryResourceAddress("stockroom/projection.py")
PROCEDURE = ToolDescriptor(
    "inspect_and_validate_change",
    "Inspect authorized repository changes and run the fixed focused acceptance check.",
    '{"type":"object","maxProperties":0}',
)
OBSERVATIONS = []
RECORDS = []


def plain(value):
    if is_dataclass(value):
        return {k: plain(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def save(path, value, *, fresh=False):
    text = json.dumps(plain(value), ensure_ascii=True, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if fresh and path.exists():
        raise FileExistsError(path)
    write(TextFile(resolve_path(path), text), overwrite=not fresh)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_files():
    return {
        str(p.relative_to(CASE)).replace("\\", "/"): digest(p)
        for p in sorted(CASE.rglob("*"))
        if p.is_file()
        and (p.suffix in {".py", ".md"} or p.name == ".gitignore")
        and "__pycache__" not in p.parts
    }


async def managed(command, label, *, retain=True):
    timer = Stopwatch()
    result = await CommandExecutor(
        output_policy=CommandOutputPolicy(
            max_stdout_bytes=131072, max_stderr_bytes=65536
        )
    ).execute(command)
    timer.stop()
    observation = completed_observation(
        result,
        origin=CommandOrigin(
            "local-dogfood-host", "stock-replay", "primary-0001", label
        ),
        pattern=CommandPattern(
            command.executable.rsplit("/", 1)[-1]
            .replace("\\", "/")
            .rsplit("/", 1)[-1]
            .replace(":", "_"),
            label,
            ("opaque",),
            (sys.platform,),
        ),
    )
    OBSERVATIONS.append(observation)
    RECORDS.append(
        {
            "label": label,
            "exit_code": result.exit_code,
            "seconds": timer.elapsed.total_seconds,
            "stdout": result.stdout.decode(errors="replace") if retain else None,
            "stderr": result.stderr.decode(errors="replace") if retain else None,
            "stdout_truncated": result.stdout_truncated,
            "stderr_truncated": result.stderr_truncated,
        }
    )
    return result


async def git(root, *args):
    result = await managed(
        Command("git")
        .args(*args)
        .cwd(resolve_path(root))
        .with_timeout(Duration.seconds(30)),
        "git-" + str(len(RECORDS)),
    )
    if result.exit_code != 0:
        raise RuntimeError("Authored repository Git operation failed")
    return result.stdout.decode().strip()


async def service_identity():
    template = "{{json .Config.Cmd}}"
    result = await managed(
        Command("docker")
        .args("inspect", CONTAINER, "--format", template)
        .with_timeout(Duration.seconds(20)),
        "service-config",
        retain=False,
    )
    if result.exit_code:
        raise RuntimeError("Configured local service unavailable")
    args = json.loads(result.stdout)
    model_path = (
        args[args.index("--model") + 1]
        if "--model" in args
        else args[args.index("-m") + 1]
    )
    fingerprint = await managed(
        Command("docker")
        .args(
            "inspect",
            CONTAINER,
            "--format",
            '{{index .Config.Labels "devtools.qwen.profile-sha256"}}',
        )
        .with_timeout(Duration.seconds(20)),
        "service-profile",
    )
    image = await managed(
        Command("docker")
        .args("inspect", CONTAINER, "--format", "{{.Config.Image}}")
        .with_timeout(Duration.seconds(20)),
        "service-image",
    )
    expected = QWEN38_27B_UD_IQ4_XS
    mounts = await managed(
        Command("docker")
        .args("inspect", CONTAINER, "--format", "{{json .Mounts}}")
        .with_timeout(Duration.seconds(20)),
        "service-mount",
        retain=False,
    )
    selected = next(
        m for m in json.loads(mounts.stdout) if m["Destination"] == model_path
    )
    if selected["RW"] or selected["Type"] != "bind":
        raise RuntimeError("Expected read-only pinned artifact bind mount")
    artifact = resolve_path(selected["Source"]).value

    def hash_artifact():
        # Genuine external model-artifact boundary: stream, never load into RAM.
        with artifact.open("rb") as source:
            return hashlib.file_digest(source, "sha256").hexdigest()

    async with asyncio.timeout(60):
        actual_sha = await asyncio.to_thread(hash_artifact)
    if actual_sha != expected.expected_sha256:
        raise RuntimeError(
            "Installed GGUF content identity differs from selected profile"
        )
    if image.stdout.decode().strip() != expected.image_build_identity:
        raise RuntimeError("Serving image differs from pinned profile")
    with urllib.request.urlopen("http://127.0.0.1:8080/props", timeout=10) as response:
        props = json.loads(response.read(131073))
    with urllib.request.urlopen(
        "http://127.0.0.1:8080/v1/models", timeout=10
    ) as response:
        models = json.loads(response.read(65537))
    if "qwen38-local" not in {x["id"] for x in models["data"]}:
        raise RuntimeError("Expected served model alias is unavailable")
    return dict(
        profile=plain(expected),
        profile_fingerprint=fingerprint.stdout.decode().strip(),
        artifact_sha256=expected.expected_sha256,
        image=image.stdout.decode().strip(),
        endpoint="http://127.0.0.1:8080",
        served_model="qwen38-local",
        available_models=[x["id"] for x in models["data"]],
        context=props.get("default_generation_settings", {}).get("n_ctx"),
        chat_template_sha256=hashlib.sha256(
            str(props.get("chat_template", "")).encode()
        ).hexdigest(),
    )


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


async def procedure(root, scope, revision, label):
    tool = InspectAndValidateTool(
        ChangeValidationPlan(
            checks(root, scope),
            revision,
            frozenset((EDIT,)),
            (CheckSelection("focused-acceptance"),),
        ),
        origin=CommandOrigin(
            "local-dogfood-host", "stock-replay", "primary-0001", label
        ),
    )
    try:
        report = await ToolRunner().execute(tool, None)
    finally:
        if tool.last_report is not None:
            OBSERVATIONS.extend(tool.last_report.observations)
    return report


async def prepare():
    if (CASE / "freeze.json").exists() or (STATE / "ENTERED.json").exists():
        raise RuntimeError("Task already frozen or entered; no automatic regeneration")
    STATE.mkdir(parents=True, exist_ok=True)
    if (
        await git(CANONICAL, "rev-parse", "HEAD") != BASE
        or await git(CANONICAL, "diff", "--name-only")
        or await git(CANONICAL, "diff", "--cached", "--name-only")
    ):
        raise RuntimeError("Canonical tracked/index baseline diverged")
    if (CANONICAL / ".local/backlog/checkout-owner").exists():
        raise RuntimeError("Canonical Checkout custody is occupied")
    identity = await service_identity()
    root = Path(tempfile.mkdtemp(prefix="devtools-local-coding-"))
    for source in (CASE / "fixture").rglob("*"):
        if source.is_file() and "__pycache__" not in source.parts:
            destination = root / source.relative_to(CASE / "fixture")
            destination.parent.mkdir(parents=True, exist_ok=True)
            write(
                TextFile(resolve_path(destination), source.read_text(encoding="utf-8")),
                overwrite=False,
            )
    write(
        TextFile(resolve_path(root / ".gitignore"), "__pycache__/\n*.pyc\n"),
        overwrite=False,
    )
    await git(root, "init")
    await git(root, "add", "--all")
    await git(
        root,
        "-c",
        "user.name=Devtools authored fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-m",
        "Freeze authored stock replay task baseline",
    )
    revision = await git(root, "rev-parse", "HEAD")
    repository = Repository.new()
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=repository,
        addresses=READ,
        maximum_resource_bytes=32768,
    )
    initial = await procedure(root, scope, revision, "baseline-procedure")
    if (
        initial.status != "failed"
        or len(initial.checks) != 1
        or b"Ran 5 tests" not in initial.checks[0].result.command_result.stderr
        or b"failures=3" not in initial.checks[0].result.command_result.stderr
    ):
        raise RuntimeError(
            "Focused baseline did not reproduce the specified three behavioral failures"
        )
    hidden = await managed(
        Command(sys.executable)
        .args("-B", str(CASE / "heldout.py"), str(root))
        .cwd(resolve_path(root))
        .with_timeout(Duration.seconds(30)),
        "baseline-heldout",
    )
    if (
        hidden.exit_code != 1
        or b"Ran 8 tests" not in hidden.stderr
        or b"failures=5" not in hidden.stderr
    ):
        raise RuntimeError(
            "Heldout baseline failed outside the five specified behavioral assertions"
        )
    prompt = (
        (CASE / "objective.md").read_text(encoding="utf-8")
        + "\nAdmitted source manifest (character lengths):\n"
        + json.dumps({str(r.address): len(r.content) for r in scope.snapshot.resources})
    )
    save(STATE / "initial-prompt.json", {"content": prompt}, fresh=True)
    frozen = dict(
        schema="local-coding-dogfood-freeze-v1",
        at=str(Timestamp.now()),
        canonical_main=BASE,
        task_root=str(root),
        task_revision=revision,
        repository_id=str(repository.id),
        snapshot_id=str(scope.snapshot.id),
        source_snapshot=plain(scope.snapshot),
        files=frozen_files(),
        task_files={
            str(p.relative_to(root)).replace("\\", "/"): digest(p)
            for p in root.rglob("*")
            if p.is_file() and ".git" not in p.parts
        },
        prompt_sha256=digest(STATE / "initial-prompt.json"),
        service=identity,
        limits=dict(
            model_calls=5,
            proposals=2,
            tool_actions=8,
            call_seconds=180,
            wall_seconds=900,
            input_tokens=28160,
            output_tokens=4096,
            context_tokens=32768,
            prompt_bytes=32768,
            disclosure_bytes=8192,
            region_bytes=4096,
            source_bytes=32768,
            aggregate_bytes=8192,
            operations=2,
        ),
        settings=dict(
            thinking_enabled=False,
            maximum_output_tokens=4096,
            sampling=QWEN38_INSTRUCT_SAMPLING,
        ),
        required_witnesses=[
            "stockroom/events.py",
            "stockroom/keys.py",
            "stockroom/projection.py",
        ],
        edit_scope=[str(EDIT)],
        baseline=dict(procedure=plain(initial), heldout=RECORDS[-1]),
        privacy="Only authored synthetic task source, normalized responses and bounded fixed-test diagnostics; no personal logs/environment/credentials. Command analytics omit payloads.",
    )
    frozen["task_digest"] = hashlib.sha256(
        json.dumps(frozen, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    save(CASE / "freeze.json", frozen, fresh=True)
    save(STATE / "prepare-records.json", RECORDS)
    print(
        json.dumps(
            {
                "task_root": str(root),
                "revision": revision,
                "snapshot": str(scope.snapshot.id),
                "digest": frozen["task_digest"],
                "baseline_focus_failures": 3,
                "baseline_heldout_failures": 5,
            }
        )
    )


class ProcedureInvocation:
    descriptor = PROCEDURE

    def materialize(self, arguments):
        if json.loads(arguments) != {}:
            raise ValueError("The command plan and scope are host-fixed")
        return None


class Host(RepositoryCodingHost):
    """Experiment-only composition of existing coding host and command procedure."""

    async def prepare(self, progress):
        request = await super().prepare(progress)
        request = replace(
            request, tools=(*request.tools, normalize_tool_descriptor(PROCEDURE))
        )
        self.requests[-1] = request
        return request

    def classify(self, response):
        if (
            response.tool_calls
            and all(
                c.name in {"read_source", "validate_candidate", PROCEDURE.name}
                for c in response.tool_calls
            )
            and any(c.name == PROCEDURE.name for c in response.tool_calls)
        ):
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
            raise ValueError("Acquisition batch exceeds frozen action budget")
        ready = False
        for call in response.tool_calls:
            if call.name != PROCEDURE.name:
                ready = (
                    await super().acquire(replace(response, tool_calls=(call,)))
                    or ready
                )
                continue
            effect = self.progress.claim_action(call.provider_call_id)
            tool = InspectAndValidateTool(
                ChangeValidationPlan(
                    checks(self.scope.root.value, self.scope),
                    self.revision,
                    frozenset((EDIT,)),
                    (CheckSelection("focused-acceptance"),),
                ),
                origin=CommandOrigin(
                    "local-model",
                    "stock-replay",
                    "primary-0001",
                    "selected-" + str(self.progress.actions),
                ),
            )
            try:
                report = await execute_model_tool_call(
                    call,
                    invocation=ProcedureInvocation(),
                    tool=tool,
                    admit=self.authorize,
                    runner=ToolRunner(),
                )
            finally:
                if tool.last_report is not None:
                    OBSERVATIONS.extend(tool.last_report.observations)
            effect.acknowledged = True
            self.procedure_reports.append(
                {
                    "trigger": "model",
                    "call_id": call.provider_call_id,
                    "report": plain(report),
                }
            )
            self.messages.append(
                PromptMessage(
                    "tool",
                    json.dumps(
                        {
                            "status": report.status,
                            "checks": [
                                {
                                    "status": c.status,
                                    "exit_code": c.result.command_result.exit_code
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
                    ),
                    tool_call_id=call.provider_call_id,
                )
            )
        return ready

    async def check(self, proposal):
        del proposal
        effect = CodingEffect("check", (), check_name="focused-acceptance")
        self.progress.effects.append(effect)
        report = await procedure(
            self.scope.root.value,
            self.scope,
            self.revision,
            "host-check-" + str(len(self.check_results)),
        )
        self.procedure_reports.append(
            {"trigger": "deterministic-host-validation", "report": plain(report)}
        )
        self.check_results.append(
            tuple(c.result for c in report.checks if c.result is not None)
        )
        if report.error is not None:
            raise report.error
        if report.status not in {"passed", "failed"}:
            raise RuntimeError("Fixed procedure returned incomplete/refused validation")
        effect.acknowledged = True
        return report.status == "passed"


class MeasuredInteraction:
    def __init__(self):
        self.delegate = LlamaCppInteraction(
            endpoint="http://127.0.0.1:8080",
            model="qwen38-local",
            source=InteractionSource("local-dogfood-qwen38-iq4xs"),
        )
        self.records = []

    @property
    def source(self):
        return self.delegate.source

    async def send(self, request):
        number = len(self.records) + 1
        if number > 5:
            raise RuntimeError("Frozen inference envelope exhausted")
        effective = replace(
            request,
            provider_settings=LlamaCppRequestSettings(**QWEN38_INSTRUCT_SAMPLING),
        )
        record = dict(
            number=number,
            at=str(Timestamp.now()),
            request=plain(effective),
            inference_entered=False,
        )
        self.records.append(record)
        save(STATE / f"request-{number}.json", record, fresh=True)
        async with asyncio.timeout(20):
            count = await self.delegate.count_input_tokens(effective)
        record["measured_input_tokens"] = count
        if count > 28160 or len(json.dumps(plain(effective)).encode()) > 32768:
            save(STATE / f"request-{number}-capacity.json", record)
            raise RuntimeError("Frozen Context/capacity envelope refused request")
        timer = Stopwatch()
        record["inference_entered"] = True
        save(STATE / f"request-{number}-entry.json", record, fresh=True)
        try:
            response = await self.delegate.send(effective)
        except BaseException as error:
            record.update(
                error_kind=type(error).__name__, error=str(error), outcome="unknown"
            )
            raise
        else:
            record.update(response=plain(response), outcome="normalized-response")
            return response
        finally:
            timer.stop()
            record.update(
                seconds=timer.elapsed.total_seconds, completed_at=str(Timestamp.now())
            )
            save(STATE / f"request-{number}-outcome.json", record, fresh=True)


async def run():
    frozen = json.loads((CASE / "freeze.json").read_text())
    if (
        frozen_files() != frozen["files"]
        or digest(STATE / "initial-prompt.json") != frozen["prompt_sha256"]
    ):
        raise RuntimeError("Frozen task/host/oracle inputs diverged")
    root = Path(frozen["task_root"])
    if await git(root, "rev-parse", "HEAD") != frozen["task_revision"] or await git(
        root, "status", "--porcelain"
    ):
        raise RuntimeError("Frozen task checkout changed")
    if await git(CANONICAL, "rev-parse", "HEAD") != BASE:
        raise RuntimeError("Canonical baseline changed before primary entry")
    save(
        STATE / "ENTERED.json",
        {
            "at": str(Timestamp.now()),
            "task_digest": frozen["task_digest"],
            "maximum_seconds": 900,
        },
        fresh=True,
    )
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=Repository(RepositoryId.parse(frozen["repository_id"])),
        addresses=READ,
        maximum_resource_bytes=32768,
    )
    if str(scope.snapshot.id) != frozen["snapshot_id"]:
        raise RuntimeError("Frozen source snapshot diverged")
    corpus = define_repository_text_corpus(
        discovery=discover_repository_resource_addresses(
            repository=Repository(scope.snapshot.repository_id),
            root=scope.root,
            requested_addresses=READ,
            maximum_resource_count=8,
            maximum_traversal_entry_count=128,
        ),
        selected_addresses=READ,
    )
    admissions = []
    applied = []

    def archive(current):
        candidate = STATE / "candidate"
        for source in (CASE / "fixture").rglob("*"):
            if source.is_file() and "__pycache__" not in source.parts:
                destination = candidate / source.relative_to(CASE / "fixture")
                destination.parent.mkdir(parents=True, exist_ok=True)
                write(
                    TextFile(
                        resolve_path(destination), source.read_text(encoding="utf-8")
                    ),
                    overwrite=False,
                )
        for address, text in current.items():
            if text is None:
                raise RuntimeError("Unknown/missing candidate source")
            write(TextFile(resolve_path(candidate / address.value), text))
        save(
            STATE / "candidate-hashes.json",
            {
                str(p.relative_to(candidate)).replace("\\", "/"): digest(p)
                for p in candidate.rglob("*")
                if p.is_file()
            },
        )

    def restore(address, text):
        if address != EDIT or text is None:
            raise RuntimeError("Unknown restoration scope")
        write(TextFile(resolve_path(root / address.value), text))

    async def authorize(call, arguments):
        if call.name not in {
            "read_source",
            "replace_source",
            "validate_candidate",
            PROCEDURE.name,
        }:
            raise PermissionError("Operation not authorized")
        admissions.append(
            {
                "call_id": call.provider_call_id,
                "name": call.name,
                "arguments": plain(arguments),
            }
        )

    async def apply_changes(changes):
        if any(c.address != EDIT for c in changes):
            raise PermissionError("Foreign edit target")
        applied.append(plain(changes))
        write_source_changes(scope.root, changes)

    def readiness(snapshot, witnesses):
        covered = {
            str(o.unit.resource.address)
            for o in witnesses
            if o.snapshot_id == snapshot.id
            and o.span
            == (0, len(snapshot.resource_at(o.unit.resource.address).content))
        }
        if not set(frozen["required_witnesses"]) <= covered:
            raise ValueError("Required full current source witnesses missing")

    objective = CodingObjective(
        json.loads((STATE / "initial-prompt.json").read_text())["content"],
        scope,
        (EDIT,),
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
        readiness=readiness,
        settings=ModelSettings(maximum_output_tokens=4096, thinking_enabled=False),
    )
    host.revision, host.procedure_reports = frozen["task_revision"], []
    interaction = MeasuredInteraction()
    timer = Stopwatch()
    result = await run_coding_agent(
        interaction,
        limits=CodingLimits(5, 2, 8, Duration.seconds(180), Duration.seconds(900)),
        host=host,
    )
    timer.stop()
    save(
        STATE / "worker-result.json",
        dict(
            at=str(Timestamp.now()),
            result=plain(result),
            accepted=result.accepted,
            seconds=timer.elapsed.total_seconds,
            admissions=admissions,
            applied=applied,
            procedures=host.procedure_reports,
            requests=interaction.records,
            messages=plain(host.messages),
            source_disclosures=plain(host.disclosures),
            original_scope=plain(scope),
            final_scope=plain(host.scope),
        ),
        fresh=True,
    )
    candidate = STATE / "candidate"
    heldout = await managed(
        Command(sys.executable)
        .args("-B", str(CASE / "heldout.py"), str(candidate))
        .cwd(resolve_path(candidate))
        .with_timeout(Duration.seconds(30)),
        "final-heldout",
    )
    focused = await managed(
        Command(sys.executable)
        .args("-B", "acceptance.py")
        .cwd(resolve_path(candidate))
        .with_timeout(Duration.seconds(30)),
        "final-focused",
    )
    restored_status = await git(root, "status", "--porcelain")
    save(
        STATE / "outcome.json",
        dict(
            at=str(Timestamp.now()),
            task_digest=frozen["task_digest"],
            worker_accepted=result.accepted,
            worker_disposition=result.disposition,
            candidate_validated=result.candidate_validated,
            worker_completed=result.completed,
            failure_phase=result.failure_phase,
            error_kind=None if result.error is None else type(result.error).__name__,
            error=None if result.error is None else str(result.error),
            model_requests=result.progress.model_calls,
            inference_entries=sum(r["inference_entered"] for r in interaction.records),
            proposals=result.progress.proposals,
            tool_actions=result.progress.actions,
            applied_batches=len(applied),
            seconds=timer.elapsed.total_seconds,
            heldout_exit=heldout.exit_code,
            focused_exit=focused.exit_code,
            restored_git_status=restored_status,
            procedures=host.procedure_reports,
            command_records=RECORDS,
            command_observations=plain(OBSERVATIONS),
            patterns=plain(summarize_patterns(tuple(OBSERVATIONS))),
        ),
        fresh=True,
    )
    print(
        json.dumps(
            {
                "accepted": result.accepted,
                "disposition": result.disposition,
                "model_requests": result.progress.model_calls,
                "applied_batches": len(applied),
                "focused_exit": focused.exit_code,
                "heldout_exit": heldout.exit_code,
                "seconds": timer.elapsed.total_seconds,
            }
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    asyncio.run(prepare() if parser.parse_args().mode == "prepare" else run())
