# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- bounded case-local JSON/CLI convention
"""Case-local stable artifacts over canonical filesystem and command substrates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import FileFormat, TextFile, read, write

CASE = Path(__file__).resolve().parent
ROOT = CASE.parents[2]
START = "d71d741f3a91bf4c4a2b40619d1b8042853f6881"


def digest(content: bytes) -> str:
    """Hash exact binary or already-normalized text bytes."""
    return hashlib.sha256(content).hexdigest()


def binary(path: Path) -> bytes:
    """Bound reads; gzip is an explicit experiment-only binary codec boundary."""
    if path.suffix == ".gz":
        with path.open("rb") as stream:
            compressed = stream.read((128 << 20) + 1)
        if len(compressed) > 128 << 20:
            raise ValueError("Compressed experiment artifact exceeds 128 MiB.")
        return compressed
    value = read(resolve_path(path), file_format=FileFormat.TEXT, max_bytes=128 << 20)
    if not isinstance(value, TextFile):
        raise TypeError("Expected text artifact.")
    return value.content.replace("\r\n", "\n").encode("utf-8")


def json_bytes(value: object) -> bytes:
    """Encode deterministic ASCII JSON with a final newline."""
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    ).encode()


def read_json(path: Path) -> dict[str, Any]:
    """Read case-owned JSON, without traversing historical outcome files."""
    value = json.loads(binary(path))
    if not isinstance(value, dict):
        raise TypeError("Expected artifact object.")
    return value


def put_text(path: Path, content: str) -> None:
    """Atomically write through the canonical substrate; never overwrite."""
    path.parent.mkdir(parents=True, exist_ok=True)
    write(TextFile(resolve_path(path), content), overwrite=False)


def put_json(path: Path, value: object) -> None:
    """Persist a case-local deterministic JSON artifact."""
    put_text(path, json_bytes(value).decode())


def put_binary(path: Path, content: bytes) -> None:
    """Exclusively publish gzip bytes where no canonical binary codec exists."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(content)


async def git(*args: str) -> bytes:
    """Access selected committed blobs using the managed command substrate."""
    result = await CommandExecutor(
        output_policy=CommandOutputPolicy(max_stdout_bytes=64 << 20),
    ).execute(Command("git").args(*args).cwd(resolve_path(ROOT)))
    if result.failed or result.stdout_truncated:
        raise ValueError("Incomplete managed Git read.")
    return result.stdout
