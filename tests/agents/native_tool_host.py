# Copyright (c) 2026
# ruff: noqa: D103, EM101, TRY003, PLR2004, PLR0915, PLR0912, C901, TRY301 -- literal failure schedule, no production policy
"""Standalone non-application consumer; executed from an authored repository."""

from __future__ import annotations

import asyncio
import importlib.abc
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence
    from importlib.machinery import ModuleSpec
    from types import ModuleType

CANONICAL = Path(__file__).resolve().parents[2]
DENIED: list[str] = []


class NoApplications(importlib.abc.MetaPathFinder):
    """Refuse application imports before resolving their implementation."""

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None = None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        """Refuse forbidden domains without invoking their loaders."""
        del path, target
        if fullname.split(".", maxsplit=1)[0] in {"apps", "scripts", "experiments"}:
            DENIED.append("import:" + fullname)
            raise ImportError("Application import denied")
        return None


def guard_files(event: str, args: tuple[Any, ...]) -> None:
    """Deny checkout data outside framework/dependencies and this literal host."""
    if event != "open" or not isinstance(args[0], (str, bytes)):
        return
    value = args[0].decode() if isinstance(args[0], bytes) else args[0]
    path = Path(value).resolve()
    if path.is_relative_to(CANONICAL) and not (
        path.is_relative_to(CANONICAL / "src" / "devtools")
        or path.is_relative_to(CANONICAL / ".venv")
        or path == Path(__file__).resolve()
    ):
        DENIED.append("file:" + path.relative_to(CANONICAL).as_posix())
        raise PermissionError("Application/configuration file access denied")


sys.meta_path.insert(0, NoApplications())
sys.addaudithook(guard_files)

from devtools.agents.model_tools import (  # noqa: E402 -- guards precede framework import
    execute_model_tool_call,
    normalize_tool_descriptor,
)
from devtools.context import (  # noqa: E402
    Repository,
    RepositoryResourceAddress,
    observe_repository_resources,
)
from devtools.context.planning import (  # noqa: E402
    choose_whole_resource_disclosure,
    materialize_disclosure_plan,
    plan_disclosures,
)
from devtools.core.paths import ResolvedPath, resolve_path  # noqa: E402
from devtools.core.time import Duration  # noqa: E402
from devtools.models.interaction import (  # noqa: E402
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from devtools.resources.commands import (  # noqa: E402
    Command,
    CommandExecutor,
    CommandResult,
)
from devtools.resources.filesystem import TextFile, write  # noqa: E402
from devtools.tools import ToolDescriptor, ToolRunner  # noqa: E402
from devtools.tools.command import CommandTool  # noqa: E402
from devtools.tools.filesystem import ReadRepositoryFileTool  # noqa: E402

TEXT = "def answer():\n    return 7\n"
SOURCE = "lib/answer.py"
SCHEMA = (
    '{"type":"object","properties":{"path":{"const":"lib/answer.py"}},'
    '"required":["path"],"additionalProperties":false}'
)
READ_DESCRIPTOR = ToolDescriptor("inspect_exact", "Read exact source.", SCHEMA)
CHECK_DESCRIPTOR = ToolDescriptor("verify_literal", "Run fixed check.", "{}")


@dataclass(frozen=True)
class ReadInvocation:
    """Host-selected exact read input, with no application-specific task type."""

    path: ResolvedPath
    descriptor: ToolDescriptor = READ_DESCRIPTOR

    def materialize(self, serialized_arguments: str) -> ResolvedPath:
        """Produce the sole authorized semantic path or refuse."""
        if json.loads(serialized_arguments) != {"path": SOURCE}:
            raise ValueError("Unadmitted read arguments")
        return self.path


@dataclass(frozen=True)
class CheckInvocation:
    """Model requests a named check; only the host supplies executable argv."""

    command: Command
    descriptor: ToolDescriptor = CHECK_DESCRIPTOR

    def materialize(self, serialized_arguments: str) -> Command:
        """Produce only the host's immutable fixed Command."""
        if json.loads(serialized_arguments) != {}:
            raise ValueError("No model-supplied argv")
        return self.command


class IndependentInteraction:
    """A different native ModelInteraction with literal normalized responses."""

    source = InteractionSource("independent-library-consumer")

    def __init__(self, scenario: str) -> None:
        """Retain literal schedule and actual native requests."""
        self.scenario = scenario
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Return a known normalized response without inference."""
        self.requests.append(request)
        if len(self.requests) == 1:
            name = "unavailable" if self.scenario == "unauthorized" else "inspect_exact"
            arguments = (
                '{"path":"elsewhere"}'
                if self.scenario == "arguments"
                else json.dumps({"path": SOURCE})
            )
            call = ModelToolCall(
                name,
                arguments,
                None if self.scenario == "missing-id" else "read-1",
            )
            calls: tuple[ModelToolCall, ...] = (
                (call, call) if self.scenario == "duplicate-id" else (call,)
            )
            if self.scenario in {
                "lost-result",
                "cancel-effect",
                "tool-exception",
                "partial-batch",
            }:
                calls += (ModelToolCall("inspect_exact", arguments, "effect-2"),)
            source = (
                InteractionSource("foreign")
                if self.scenario == "foreign-source"
                else self.source
            )
            return ModelResponse("Read the literal function.", source, tool_calls=calls)
        previous = request.prompt.messages[-1]
        assert previous.role == "tool"
        if len(self.requests) == 2:
            assert previous.tool_call_id == "read-1"
            assert json.loads(previous.content)["text"] == TEXT
            return ModelResponse(
                "Now check it.",
                self.source,
                tool_calls=(ModelToolCall("verify_literal", "{}", "check-1"),),
            )
        assert previous.tool_call_id == "check-1"
        assert json.loads(previous.content) == {"exit_code": 0, "stdout": "checked:7\n"}
        return ModelResponse("Literal source and fixed check agree.", self.source)


class EffectTool:
    """Test-only effect with missing acknowledgment; not an editing engine."""

    name = "fixture_effect"
    description = "One already-authorized fixture effect."

    def __init__(self, events: list[str], *, cancel: bool, fail: bool) -> None:
        """Select deterministic loss/cancellation after one known entry."""
        self.events = events
        self.cancel = cancel
        self.fail = fail

    def validate(self, arguments: ResolvedPath) -> None:
        """Require exact fixture bytes before possible write."""
        assert arguments.value.read_text() == TEXT

    async def execute(self, arguments: ResolvedPath) -> TextFile:
        """Enter once; preserve either no write or a known unacknowledged effect."""
        self.events.append("effect-entered")
        if self.fail:
            raise OSError("Tool failed before write")
        write(TextFile(arguments, "known effect\n"))
        if self.cancel:
            raise asyncio.CancelledError("after effect")
        raise OSError("acknowledgment lost")


async def run(scenario: str) -> dict[str, Any]:
    # Prove both guards actively refuse before any application content is read.
    try:
        __import__("apps.qwen")
    except ImportError:
        pass
    else:
        raise AssertionError("Import guard inactive")
    try:
        (CANONICAL / "apps/qwen/tasks.py").read_bytes()
    except PermissionError:
        pass
    else:
        raise AssertionError("File guard inactive")
    root = resolve_path(Path.cwd())
    assert not root.value.is_relative_to(CANONICAL)
    path = resolve_path(root.value / SOURCE)
    path.value.parent.mkdir()
    write(TextFile(path, TEXT), overwrite=False)
    executor = CommandExecutor()
    for argv in [
        ("init", "-q"),
        ("add", "--", SOURCE),
        (
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "Authored literal source",
        ),
    ]:
        result = await executor.execute(Command("git").args(*argv).cwd(root))
        assert result.exit_code == 0
    repository = Repository.new()
    address = RepositoryResourceAddress(SOURCE)
    snapshot = observe_repository_resources(
        repository=repository,
        root=root,
        addresses=(address,),
        maximum_resource_bytes=4096,
    )
    identity = snapshot.resource_at(address).content_identity
    choice = choose_whole_resource_disclosure(
        purpose="Verify literal function",
        snapshot=snapshot,
        resource_address=address,
    )
    context = materialize_disclosure_plan(
        plan=plan_disclosures(
            purpose="Verify literal function",
            snapshot=snapshot,
            disclosures=(choice,),
        ),
        snapshot=snapshot,
    )
    assert snapshot.resource_at(address).content == TEXT
    assert context.items[0].native_provenance is snapshot.resource_at(address)
    read = ReadInvocation(path)
    check_code = (
        "import sys; from pathlib import Path; "
        'assert Path("lib/answer.py").read_text() == '
        '"def answer():\\n    return 7\\n"; '
        'sys.stdout.buffer.write(b"checked:7\\n")'
    )
    check = CheckInvocation(
        Command(sys.executable)
        .args(
            "-B",
            "-c",
            check_code if scenario != "check-failed" else "raise SystemExit(9)",
        )
        .cwd(root)
        .with_timeout(Duration.seconds(10)),
    )
    definitions = (
        normalize_tool_descriptor(read.descriptor),
        normalize_tool_descriptor(check.descriptor),
    )
    messages: tuple[PromptMessage, ...] = (
        PromptMessage("user", "Verify the authorized function."),
    )
    model = IndependentInteraction(scenario)
    events: list[str] = []
    feedback: list[str] = []
    check_outcome: dict[str, Any] | None = None
    entered: list[str] = []
    outcome = "success"
    error: str | None = None
    try:
        for _turn in range(3):
            response = await model.send(
                ModelRequest(Prompt("", "messages", messages), tools=definitions),
            )
            if response.source != model.source:
                raise ValueError("Foreign response source")
            assert response.usage is None
            if not response.tool_calls:
                break
            calls = response.tool_calls
            ids = [call.provider_call_id for call in calls]
            if not all(ids) or len(set(ids)) != len(ids):
                raise ValueError("Missing or duplicate native call identities")
            messages += (PromptMessage("assistant", response.content, calls),)
            for call in calls:
                assert call.provider_call_id is not None
                if scenario == "stale":
                    write(TextFile(path, "changed outside this call\n"))

                async def admit(
                    selected: ModelToolCall,
                    arguments: ResolvedPath | Command,
                    *,
                    expected: ModelToolCall = call,
                    origin: ModelResponse = response,
                ) -> None:
                    if selected is not expected or selected not in origin.tool_calls:
                        raise ValueError("Foreign call identity")
                    if scenario == "cancel-admission":
                        raise asyncio.CancelledError("before effects")
                    current = observe_repository_resources(
                        repository=repository,
                        root=root,
                        addresses=(address,),
                        maximum_resource_bytes=4096,
                    )
                    if current.resource_at(address).content_identity != identity:
                        raise ValueError("Stale source identity")
                    if isinstance(arguments, ResolvedPath):
                        assert arguments == path
                    else:
                        assert arguments is check.command
                    assert selected.provider_call_id is not None
                    events.append("admitted:" + selected.provider_call_id)

                if call.provider_call_id == "effect-2":
                    entered.append(call.provider_call_id)
                    await execute_model_tool_call(
                        call,
                        invocation=read,
                        tool=EffectTool(
                            events,
                            cancel=scenario == "cancel-effect",
                            fail=scenario == "tool-exception",
                        ),
                        admit=admit,
                        runner=ToolRunner(),
                    )
                    raise AssertionError("Missing acknowledgment must not return")
                if call.name == read.descriptor.name:
                    entered.append(call.provider_call_id)
                    actual = await execute_model_tool_call(
                        call,
                        invocation=read,
                        tool=ReadRepositoryFileTool(root),
                        admit=admit,
                        runner=ToolRunner(),
                    )
                    assert isinstance(actual, TextFile)
                    assert actual.content == TEXT
                    data = {
                        "text": actual.content,
                        "content_identity": str(identity),
                        "snapshot": str(snapshot.id),
                    }
                elif call.name == check.descriptor.name:
                    entered.append(call.provider_call_id)
                    checked: CommandResult = await execute_model_tool_call(
                        call,
                        invocation=check,
                        tool=CommandTool(executor),
                        admit=admit,
                        runner=ToolRunner(),
                    )
                    check_outcome = {
                        "exit_code": checked.exit_code,
                        "stdout": checked.stdout.decode(),
                    }
                    if checked.failed:
                        raise ValueError("Host fixed check failed")
                    data = check_outcome
                else:
                    raise ValueError("Operation not host-selected")
                feedback.append(call.provider_call_id)
                messages += (
                    PromptMessage(
                        "tool",
                        json.dumps(data),
                        tool_call_id=call.provider_call_id,
                    ),
                )
        else:
            raise AssertionError("Unexpected extra model turn")
    except (ValueError, OSError, asyncio.CancelledError) as failure:
        outcome = (
            "cancelled"
            if isinstance(failure, asyncio.CancelledError)
            else "refused-or-incomplete"
        )
        error = str(failure)
    assert not any(
        name.split(".")[0] in {"apps", "scripts", "experiments"} for name in sys.modules
    )
    return dict(  # noqa: C408 -- explicit named report fields
        scenario=scenario,
        outcome=outcome,
        error=error,
        model_calls=len(model.requests),
        shared_entries=entered,
        events=events,
        feedback_ids=feedback,
        source=path.value.read_text(),
        content_identity=str(identity),
        snapshot=str(snapshot.id),
        check=check_outcome,
        usage=None,
        denied=DENIED,
        framework_file=execute_model_tool_call.__code__.co_filename,
    )


if __name__ == "__main__":
    print(json.dumps(asyncio.run(run(sys.argv[1])), sort_keys=True))  # noqa: T201 -- subprocess protocol
