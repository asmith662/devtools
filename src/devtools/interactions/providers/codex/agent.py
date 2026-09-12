# Copyright (c) 2026
"""CLI-backed Interaction provider for the external Codex agent system."""

from __future__ import annotations

import shutil
import sys
from typing import TYPE_CHECKING, ClassVar

from devtools.commands import Command, CommandExecutor
from devtools.context.message import Message, MessageRole, MessageSource
from devtools.interactions import ConversationRef, InteractionTurn
from devtools.interactions.providers.codex.errors import (
    CodexCommandError,
    CodexOutputError,
)
from devtools.interactions.providers.codex.parsing import parse_codex_turn_output

if TYPE_CHECKING:
    from devtools.paths import ResolvedPath


_DEFAULT_EXECUTABLE = "codex"
_WINDOWS_EXECUTABLE = "codex.cmd"
_READ_ONLY_SANDBOX_CONFIG = 'sandbox_mode="read-only"'


class CodexAgent:
    """Send user turns to the local Codex CLI using read-only execution.

    The configured directory governs every command process and Codex's fresh
    working root. The installed 0.147.0 CLI does not expose ``--sandbox`` or
    ``--cd`` on ``exec resume``; resumed commands retain process cwd and force
    the supported read-only ``sandbox_mode`` configuration override.
    """

    _SOURCE: ClassVar[MessageSource] = MessageSource("codex")

    def __init__(
        self,
        executor: CommandExecutor,
        working_directory: ResolvedPath,
        *,
        executable: str = "codex",
    ) -> None:
        """Create a Codex CLI adapter with explicit execution dependencies.

        :param executor: Command execution collaboration used for every CLI call.
        :param working_directory: Explicit workspace used for Codex execution.
        :param executable: Codex executable name or path.
        """
        self._executor = executor
        self._working_directory = working_directory
        self._executable = _resolve_executable(executable)

    @property
    def source(self) -> MessageSource:
        """Return the stable source represented by this adapter."""
        return self._SOURCE

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> InteractionTurn:
        """Send a user prompt and return Codex's final completed response.

        :raises ValueError: If the input is not a user message or the supplied
            conversation belongs to another source.
        :raises CodexCommandError: If Codex exits unsuccessfully.
        :raises CodexOutputError: If retained stdout is truncated or does not
            contain a successful Codex JSONL turn.
        """
        if message.role != MessageRole.USER:
            msg = "CodexAgent accepts only user messages."
            raise ValueError(msg)
        if conversation is not None and conversation.source != self.source:
            msg = "Codex conversation must be owned by the codex source."
            raise ValueError(msg)

        command = self._build_command(message.content, conversation)
        result = await self._executor.execute(command)
        if result.failed:
            raise CodexCommandError(result.exit_code)
        if result.stdout_truncated:
            msg = "Codex JSONL stdout was truncated by the command output policy."
            raise CodexOutputError(msg)

        output = parse_codex_turn_output(result.stdout)
        assistant_message = Message.new(
            output.final_message,
            role=MessageRole.ASSISTANT,
            source=self.source,
        )
        return InteractionTurn(
            message=assistant_message,
            conversation=ConversationRef(self.source, output.thread_id),
        )

    def _build_command(
        self,
        prompt: str,
        conversation: ConversationRef | None,
    ) -> Command:
        """Build the installed CLI's direct-argv JSONL invocation."""
        command = Command(self._executable).cwd(self._working_directory)
        if conversation is None:
            return command.args(
                "exec",
                "--sandbox",
                "read-only",
                "--cd",
                str(self._working_directory),
                "--json",
                prompt,
            )
        return command.args(
            "exec",
            "resume",
            "-c",
            _READ_ONLY_SANDBOX_CONFIG,
            "--json",
            conversation.value,
            prompt,
        )


def _resolve_executable(executable: str) -> str:
    """Resolve only the default Windows Codex launcher for direct execution.

    Callers supplying a value other than the public default retain that exact
    value. On Windows, the npm installation's PowerShell shim is not directly
    executable by :class:`CommandExecutor`; prefer its ``.cmd`` launcher.
    When the launcher is absent, preserve the default and let the command
    domain raise its normal not-found error on execution.
    """
    if executable != _DEFAULT_EXECUTABLE or sys.platform != "win32":
        return executable

    return shutil.which(_WINDOWS_EXECUTABLE) or executable
