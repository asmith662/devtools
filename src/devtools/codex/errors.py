# Copyright (c) 2026
"""Codex adapter errors."""

from __future__ import annotations


class CodexError(Exception):
    """Base error raised by the Codex adapter."""


class CodexCommandError(CodexError):
    """Raise when the Codex CLI completes with a nonzero exit code."""

    def __init__(self, exit_code: int) -> None:
        """Create an error for a completed unsuccessful Codex command.

        :param exit_code: Exit status reported by the Codex CLI.
        """
        self.exit_code = exit_code
        super().__init__(f"Codex CLI exited with code {exit_code}.")


class CodexOutputError(CodexError):
    """Raise when Codex JSONL output cannot represent a successful turn."""
