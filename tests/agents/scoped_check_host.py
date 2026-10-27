# Copyright (c) 2026
# ruff: noqa: D103, EM101, TRY003, PLR2004, PLR0915, PLR0912, C901, TRY301, COM812, E402 -- guards precede framework imports; literal schedules
"""Independent scoped-source and fixed-check host; no application data."""

from __future__ import annotations

import asyncio
import contextlib
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


from devtools.agents.model_tools import (
    execute_model_tool_call,
    normalize_tool_descriptor,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import (
    discover_repository_resource_addresses,
)
from devtools.context.retrieval import build_source_search_index
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from devtools.resources.commands import Command, CommandExecutor
from devtools.resources.filesystem import TextFile, write
from devtools.tools import ToolDescriptor, ToolRunner
from devtools.tools.checks import (
    FixedCheck,
    FixedCheckPlan,
    FixedCheckTool,
)
from devtools.tools.errors import ToolInputError
from devtools.tools.source import ScopedSourceTool, SourceScope

TEXT = "# \u03c0 prefix\r\ndef answer():\r\n    return 7\r\n# tail\r\n"
REGION = "def answer():\r\n    return 7"
READ = ToolDescriptor("inspect_region", "Acquire the exact authorized region.", "{}")
CHECK = ToolDescriptor("check_literal", "Request the fixed check.", "{}")


@dataclass(frozen=True)
class SourceInvocation:
    """Host-selected exact source region, never a model-selected path."""

    option: SourceRangeDisclosureOption
    descriptor: ToolDescriptor = READ

    def materialize(self, serialized_arguments: str) -> SourceRangeDisclosureOption:
        """Refuse model expansion and return the host-fixed region."""
        if json.loads(serialized_arguments) != {}:
            raise ValueError("Unadmitted source arguments")
        return self.option


@dataclass(frozen=True)
class CheckInvocation:
    """Host-owned fixed check selection with no executable arguments."""

    descriptor: ToolDescriptor = CHECK

    def materialize(self, serialized_arguments: str) -> str:
        """Refuse model argv and select the immutable literal check."""
        if json.loads(serialized_arguments) != {}:
            raise ValueError("Unadmitted command arguments")
        return "literal"


class IndependentInteraction:
    """Native protocol double with literal response and feedback expectations."""

    source = InteractionSource("independent-scoped-library-host")

    def __init__(self) -> None:
        """Retain every actual request, never invoke inference."""
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Require correlated exact source/check feedback on continuation."""
        self.requests.append(request)
        if len(self.requests) == 1:
            return ModelResponse(
                "Inspect the exact region.",
                self.source,
                tool_calls=(ModelToolCall(READ.name, "{}", "region-1"),),
            )
        last = request.prompt.messages[-1]
        assert last.role == "tool"
        if len(self.requests) == 2:
            assert last.tool_call_id == "region-1"
            assert json.loads(last.content)["text"] == REGION
            return ModelResponse(
                "Check the authorized source.",
                self.source,
                tool_calls=(ModelToolCall(CHECK.name, "{}", "check-2"),),
            )
        assert last.tool_call_id == "check-2"
        assert json.loads(last.content) == {
            "exit_code": 0,
            "stdout": "checked:7\n",
            "current": True,
        }
        return ModelResponse("Known source and fixed check complete.", self.source)


async def run(scenario: str) -> dict[str, Any]:
    with contextlib.suppress(ImportError):
        __import__("apps.qwen")
    with contextlib.suppress(PermissionError):
        (CANONICAL / "apps/qwen/tasks.py").read_bytes()
    assert len(DENIED) == 2
    root = resolve_path(Path.cwd())
    assert not root.value.is_relative_to(CANONICAL)
    path = resolve_path(root.value / "module.py")
    write(TextFile(path, TEXT), overwrite=False)
    executor = CommandExecutor()
    for argv in [
        ("init", "-q"),
        ("add", "--", "module.py"),
        (
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "Authored source",
        ),
    ]:
        assert (
            await executor.execute(Command("git").args(*argv).cwd(root))
        ).exit_code == 0
    repository = Repository.new()
    address = RepositoryResourceAddress("module.py")
    scope = SourceScope.observe(
        root=root,
        repository=repository,
        addresses=(address,),
        maximum_resource_bytes=4096,
    )
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=root,
        maximum_resource_count=4,
        maximum_traversal_entry_count=16,
        requested_addresses=(address,),
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery, selected_addresses=(address,)
        ),
        snapshot=scope.snapshot,
    )
    index = build_source_search_index(
        scope.snapshot, corpus=corpus, window_lines=2, overlap_lines=0
    )
    unit = next(
        u for view in index.views for u in view.units if u.qualified_name == "answer"
    )
    assert TEXT[unit.start : unit.end] == REGION
    from dataclasses import replace  # noqa: PLC0415 -- deliberate foreign input

    if scenario == "foreign":
        unit = replace(
            unit,
            resource=replace(
                unit.resource, address=RepositoryResourceAddress("outside.py")
            ),
        )
    option = SourceRangeDisclosureOption(
        "Verify literal function",
        unit,
        unit.start,
        unit.end,
        5 if scenario == "partial" else 1024,
    )
    read = SourceInvocation(option)
    read_tool = ScopedSourceTool(scope, maximum_bytes=1024)
    code = (
        "from pathlib import Path; import sys; "
        'assert Path("module.py").read_bytes() == ' + repr(TEXT.encode()) + "; "
        'sys.stdout.buffer.write(b"checked:7\\n")'
    )
    if scenario == "failed-check":
        code = "raise SystemExit(7)"
    elif scenario in {"lost-ack", "cancel-effect"}:
        code = 'from pathlib import Path; Path("effect").write_text("entered")'
    check = FixedCheck(
        "literal",
        Command(sys.executable)
        .args("-I", "-B", "-c", code)
        .cwd(root)
        .with_timeout(Duration.seconds(10)),
    )
    check_tool = FixedCheckTool(FixedCheckPlan(root, (check,), scope))
    check_entries: list[tuple[str, ...]] = []
    original = check_tool.executor.execute

    async def execute(command: Any) -> Any:  # noqa: ANN401 -- instrument canonical executor
        check_entries.append(tuple(command.argv))
        result = await original(command)
        if scenario == "lost-ack":
            raise OSError("Acknowledgment lost after known effect")
        if scenario == "cancel-effect":
            raise asyncio.CancelledError("Cancelled after known effect")
        return result

    check_tool.executor.execute = execute  # type: ignore[method-assign]
    model = IndependentInteraction()
    messages: tuple[PromptMessage, ...] = (
        PromptMessage("user", "Inspect the permitted region and run the fixed check."),
    )
    definitions = (normalize_tool_descriptor(READ), normalize_tool_descriptor(CHECK))
    feedback: list[str] = []
    selected: list[str] = []
    data: dict[str, Any] | None = None
    acquisition: dict[str, Any] | None = None
    checked: dict[str, Any] | None = None
    outcome, error = "success", None
    try:
        if scenario == "range":
            SourceRangeDisclosureOption("invalid", unit, unit.start, unit.end + 1, 1024)
        for turn in range(3):
            response = await model.send(
                ModelRequest(Prompt("", "messages", messages), tools=definitions)
            )
            assert response.source == model.source
            assert response.usage is None
            if not response.tool_calls:
                break
            call = response.tool_calls[0]
            messages += (
                PromptMessage("assistant", response.content, response.tool_calls),
            )

            async def admit(
                requested: ModelToolCall,
                _arguments: object,
                *,
                expected: ModelToolCall = call,
                origin: ModelResponse = response,
            ) -> None:
                assert requested is expected
                assert requested in origin.tool_calls
                if scenario == "cancel-admission":
                    raise asyncio.CancelledError("Before Tool entry")

            selected.append(call.provider_call_id or "")
            if turn == 0:
                if scenario == "stale":
                    write(TextFile(path, "changed\n"))
                disclosure = await execute_model_tool_call(
                    call,
                    invocation=read,
                    tool=read_tool,
                    admit=admit,
                    runner=ToolRunner(),
                )
                item = disclosure.items[0]
                assert item.native_provenance is option
                data = {
                    "text": item.text,
                    "span": list(option.span),
                    "requested": [unit.start, unit.end],
                    "partial": option.truncated,
                    "content_identity": str(item.content_identities[0]),
                    "snapshot": str(scope.snapshot.id),
                }
                acquisition = data
                assert option.span == (12, 17 if scenario == "partial" else 39)
                if scenario == "partial":
                    assert item.text == "def a"
                    assert option.truncated
                    outcome = "partial-acquisition"
                    break
                assert item.text == REGION
                if scenario == "incomplete-feedback":
                    ModelRequest(
                        Prompt(
                            "",
                            "messages",
                            (
                                *messages,
                                PromptMessage("user", "Continue without Tool feedback"),
                            ),
                        ),
                        tools=definitions,
                    )
                    raise AssertionError("Incomplete feedback accepted")
                if scenario == "stale-check":
                    write(TextFile(path, "changed after read\n"))
            else:
                invocation = CheckInvocation()
                if scenario == "unadmitted-check":
                    check_tool.plan.select("model-shell")
                result = await execute_model_tool_call(
                    call,
                    invocation=invocation,
                    tool=check_tool,
                    admit=admit,
                    runner=ToolRunner(),
                )
                checked = {
                    # The actual Command result remains bound to the host plan.
                    "exit_code": result.command_result.exit_code,
                    "stdout": result.command_result.stdout.decode(),
                    "current": result.inputs_current,
                }
                assert result.command_result.command is check.command
                if not result.passed:
                    raise ValueError("Fixed check failed")
                data = checked
            assert call.provider_call_id is not None
            feedback.append(call.provider_call_id)
            messages += (
                PromptMessage(
                    "tool", json.dumps(data), tool_call_id=call.provider_call_id
                ),
            )
    except (ValueError, ToolInputError, OSError, asyncio.CancelledError) as failure:
        outcome, error = "refused-or-incomplete", type(failure).__name__
    assert not any(
        name.split(".")[0] in {"apps", "scripts", "experiments"} for name in sys.modules
    )
    return {
        "scenario": scenario,
        "outcome": outcome,
        "error": error,
        "model_calls": len(model.requests),
        "feedback": feedback,
        "selected": selected,
        "source": TEXT,
        "disclosure": acquisition,
        "check": checked,
        "check_entries": check_entries,
        "effect": (root.value / "effect").exists(),
        "usage": None,
        "denied": DENIED,
        "scope": str(scope.snapshot.id),
        "framework": ScopedSourceTool.execute.__code__.co_filename,
    }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(run(sys.argv[1])), sort_keys=True))  # noqa: T201 -- subprocess protocol
