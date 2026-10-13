# Copyright (c) 2026
# ruff: noqa: ANN401 -- serialized Git publication boundary
"""Own canonical publication and stop on Git advancement or ambiguous effects."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from experiments.codex_dogfood.case_0009.artifacts import digest, put_binary
from experiments.orchestration.storage import exclusive, require, safe

if TYPE_CHECKING:
    from pathlib import Path


class Repository:
    """Provide one serialized publisher; workers never obtain this object."""

    def __init__(
        self,
        root: Path,
        remote: str = "origin",
        *,
        push: bool = True,
    ) -> None:
        """Bind the worktree and frozen external publication policy."""
        self.root, self.remote, self.push_enabled = (
            resolve_path(root).value,
            remote,
            push,
        )
        self.lock = asyncio.Lock()
        self.expected_head = ""

    async def git(self, *args: str) -> bytes:
        """Use the canonical managed command owner for Git, without shell parsing."""
        result = await CommandExecutor(
            output_policy=CommandOutputPolicy(max_stdout_bytes=64 << 20),
        ).execute(
            Command("git")
            .args("-c", "core.longpaths=true", *args)
            .cwd(resolve_path(self.root)),
        )
        require(
            not result.failed and not result.stdout_truncated,
            "Git operation failed/ambiguous: "
            + " ".join(args[:2])
            + ": "
            + result.stderr.decode(errors="replace")[:1000],
        )
        return result.stdout

    async def authenticate(
        self,
        expected: str | None = None,
        owned_prefix: str | None = None,
    ) -> str:
        """Require synchronized clean main; never fetch/reset/discard advancement."""
        head = (await self.git("rev-parse", "HEAD")).decode().strip()
        require(
            resolve_path(
                (await self.git("rev-parse", "--show-toplevel")).decode().strip(),
            ).value
            == self.root,
            "Exact worktree root required",
        )
        require(
            not expected or head == expected,
            "Unexpected main advancement; preserve staged results",
        )
        require(
            (await self.git("branch", "--show-current")).strip() == b"main",
            "Main branch required",
        )
        require(
            not await self.git("diff", "--cached", "--name-only")
            and not await self.git("diff", "--name-only"),
            "Unexpected tracked/index changes; preserve results",
        )
        for address in (
            (await self.git("ls-files", "--others", "--exclude-standard"))
            .decode()
            .splitlines()
        ):
            require(
                owned_prefix is not None and address.startswith(owned_prefix + "/"),
                "Unexpected untracked worktree changes",
            )
        if self.push_enabled:
            require(
                (await self.git("rev-parse", self.remote + "/main")).decode().strip()
                == head,
                "origin/main differs",
            )
            require(
                (await self.git("ls-remote", self.remote, "refs/heads/main"))
                .decode()
                .split()[0]
                == head,
                "Actual remote main differs",
            )
        self.expected_head = head
        return head

    async def commit(
        self,
        boundary: str,
        prefix: str,
        files: dict[str, bytes],
        subject: str,
        validate: Any,
    ) -> str:
        """Apply/validate/commit/push exactly one owned boundary under a lock."""
        async with self.lock:
            await self.authenticate(self.expected_head, prefix)
            attributes = safe(self.root, prefix + "/.gitattributes")
            if not attributes.exists():
                put_binary(attributes, b"* -text -whitespace\n")
            for address, raw in files.items():
                destination = safe(self.root, prefix + "/" + address)
                require(not destination.exists(), "Publication refuses overwrite")
                put_binary(destination, raw)
            receipt = {
                "boundary": boundary,
                "parent_head": self.expected_head,
                "sha256": {p: digest(raw) for p, raw in sorted(files.items())},
            }
            exclusive(
                safe(self.root, prefix + "/publications/" + boundary + ".json"),
                receipt,
            )
            await validate(boundary, tuple(prefix + "/" + p for p in files))
            for address, raw in files.items():
                require(
                    safe(self.root, prefix + "/" + address).read_bytes() == raw,
                    "Candidate changed during publication validation",
                )
            require(
                (await self.git("rev-parse", "HEAD")).decode().strip()
                == self.expected_head
                and not await self.git("diff", "--name-only")
                and not await self.git("diff", "--cached", "--name-only"),
                "Main changed during validation; STOP without discarding files",
            )
            await self.git("add", "--", prefix)
            await self.git("diff", "--cached", "--check")
            await self.git("commit", "-m", subject)
            head = (await self.git("rev-parse", "HEAD")).decode().strip()
            require(
                (await self.git("rev-parse", "HEAD^")).decode().strip()
                == receipt["parent_head"],
                "Main advanced during commit; local checkpoint preserved, push refused",
            )
            self.expected_head = head
            if self.push_enabled:
                # Ambiguous failures stop; no blind retry or forced push.
                await self.git("push", self.remote, "main")
            await self.authenticate(head)
            return head
