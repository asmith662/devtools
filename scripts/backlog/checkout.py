# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, SLF001, TRY301, TRY300 -- concrete single-checkout administration
"""Exclusive, recoverable source ownership for WorkCycle's ordinary branches.

This is a checkout transaction, not execution authority. A surviving owner record
requires explicit reconciliation; its age never authorizes another writer.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import stat
import sys
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Self

from devtools.context import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.resources.filesystem import TextFile, write
from scripts.backlog.coordinator import git
from scripts.backlog.intake import _digest, load_json

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path
    from types import TracebackType

    from scripts.backlog.work import WorkCycle


@contextmanager
def _transition(root: Path) -> Iterator[None]:
    """Fence cooperating processes/threads across effects, not just admission.

    This stable local file is never removed or replaced. The OS releases its
    advisory lock on close/process exit; its existence is not a stale lease.
    Unsupported/network filesystem locking is not a supported custody boundary.
    """
    path = root / ".local/backlog/checkout.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = _entry(path)
    if entry is not None and (not stat.S_ISREG(entry.st_mode) or _link(entry)):
        raise PermissionError("Checkout lock must be a regular local file")
    # A descriptor is necessary for OS locking; filesystem atomic text writes
    # do not supply this primitive. Do not unlink this inode even after release.
    with path.open("a+b") as stream:
        try:
            if sys.platform == "win32":
                import msvcrt  # noqa: PLC0415 -- native Windows lock boundary

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl  # noqa: PLC0415 -- native POSIX lock boundary

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise PermissionError("Checkout transition in progress") from error
        try:
            yield
        finally:
            # Closing releases even on cancellation or an interrupted finalizer.
            stream.close()


def _entry(path: Path) -> os.stat_result | None:
    """Inspect lexical presence, including dangling links; fail closed on errors."""
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def _link(entry: os.stat_result) -> bool:
    """Include Windows junctions and other reparse points, not only symlinks."""
    return stat.S_ISLNK(entry.st_mode) or bool(
        getattr(entry, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


async def _collisions(root: Path, revision: str) -> None:
    """Refuse unknown entries or traversed aliases before a Git branch effect."""
    names = await _paths(root, "ls-tree", "-r", "--name-only", revision)
    current = await _paths(root, "ls-files")
    for name in names:
        path = root
        parts = RepositoryResourceAddress(name).value.split("/")
        for index, part in enumerate(parts):
            path /= part
            entry = _entry(path)
            if entry is None:
                break
            relative = "/".join(parts[: index + 1])
            if index == len(parts) - 1:
                if name not in current:
                    raise PermissionError(
                        "Untracked/ignored path collides with target: " + name
                    )
            elif _link(entry):
                raise PermissionError("Branch target traverses a link: " + relative)
            elif not stat.S_ISDIR(entry.st_mode):
                if relative in current:
                    break  # Git owns this tracked file-to-directory transition.
                raise PermissionError(
                    "Branch target crosses unknown entry: " + relative
                )


async def fingerprint(path: Path) -> str:
    """Use Git's non-writing, unfiltered blob identity for opaque source bytes."""
    return await git(path.parent, "hash-object", "--no-filters", "--", str(path))


async def untracked(root: Path) -> dict[str, str]:
    """Record ordinary untracked files without disclosing their content."""
    names = await _paths(root, "ls-files", "--others", "--exclude-standard")
    return {name: await fingerprint(root / name) for name in names}


async def _paths(root: Path, *arguments: str) -> set[str]:
    """NUL-delimited Git paths preserve Unicode, spaces and quoted characters."""
    return set(
        filter(None, (await git(root, *arguments, "-z", trim=False)).split("\0"))
    )


async def idle(root: Path) -> None:
    """Refuse unfinished Git operations and tracked/index changes."""
    await _operations(root)
    if await git(root, "status", "--porcelain", "--untracked-files=no"):
        raise PermissionError("Tracked source/index is not clean")


async def _operations(root: Path) -> None:
    """Never interfere with an externally started Git operation."""
    for name in (
        "MERGE_HEAD",
        "CHERRY_PICK_HEAD",
        "REVERT_HEAD",
        "rebase-merge",
        "rebase-apply",
        "index.lock",
        "BISECT_LOG",
    ):
        path = resolve_path(
            await git(root, "rev-parse", "--git-path", name), base_directory=root
        ).value
        if path.exists():
            raise PermissionError(
                "Active Git operation requires reconciliation: " + name
            )


class Checkout:
    """Serialize one source operation and return to its original ordinary branch."""

    def __init__(  # noqa: PLR0913 -- exact branch scope and permitted Git effects
        self,
        cycle: WorkCycle,
        operation: str,
        branch: str,
        revision: str,
        *,
        files: list[dict[str, Any]] | None = None,
        create: bool = False,
        commit_allowed: bool = False,
    ) -> None:
        """Bind exact branch/base and the only permitted temporary file changes."""
        self.cycle = cycle
        self.root = cycle.root
        self.folder = self.root / ".local/backlog/checkout-owner"
        self.operation = operation
        self.branch = branch
        self.revision = revision
        self.files = files or []
        self.create = create
        self.commit_allowed = commit_allowed
        self.record: dict[str, Any] = {}
        self._sealed: str | None = None

    def _save(self) -> None:
        """Atomically checkpoint host-owned recovery information."""
        write(
            TextFile(
                resolve_path(self.folder / "owner.json"),
                json.dumps({**self.record, "sha256": _digest(self.record)}, indent=2)
                + "\n",
            )
        )
        self._sealed = _digest(self.record)

    def _owned(self) -> None:
        """Require the exact last journal, including its nonreusable generation."""
        value = load_json(self.folder / "owner.json")
        digest = value.pop("sha256", None)
        if (
            self._sealed is None
            or digest != self._sealed
            or _digest(value) != digest
            or value.get("root") != str(self.root)
        ):
            raise PermissionError("Checkout owner changed; reconciliation required")

    def source_path(self, relative: str) -> Path:
        """Reject aliases as well as escapes at the exact-file authority boundary."""
        raw = self.root / RepositoryResourceAddress(relative).value
        resolved = resolve_path(raw).value
        if resolved != raw or not resolved.is_relative_to(self.root):
            raise PermissionError("Source scope aliases or escapes canonical checkout")
        return resolved

    def expect(self, path: str, text: str) -> None:
        """Admit exact host-validated proposal bytes before applying them."""
        with _transition(self.root):
            self._owned()
            self._expect(path, text)

    def _expect(self, path: str, text: str) -> None:
        """Update the journal while already holding the transition fence."""
        entry = next(f for f in self.record["files"] if f["path"] == path)
        content = text.encode()
        digest = hashlib.new(
            self.record["object_format"],
            b"blob " + str(len(content)).encode() + b"\0" + content,
            usedforsecurity=False,
        ).hexdigest()
        if digest not in entry["expected"]:
            entry["expected"].append(digest)
            self._save()

    async def __aenter__(self) -> Self:
        """Claim before switching; refuse rather than stash unrelated work."""
        await self.cycle._coordinator()
        with _transition(self.root):
            return await self._enter()

    async def _enter(self) -> Self:  # noqa: C901 -- fenced branch admission
        """Keep admission, journal installation and branch effects indivisible."""
        self.folder.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Share Intake's admission mutex, then retain exclusive source
            # ownership across model/validation waits without blocking revoke.
            with self.cycle.intake._writer():
                self.folder.mkdir()
        except FileExistsError as error:
            raise PermissionError(
                "Checkout owned; explicit recovery required"
            ) from error
        try:
            await idle(self.root)
            original = await git(self.root, "branch", "--show-current")
            if not original:
                raise PermissionError("A named administrative branch is required")
            await git(self.root, "check-ref-format", "refs/heads/" + self.branch)
            await git(self.root, "cat-file", "-e", self.revision + "^{commit}")
            await _collisions(self.root, self.revision)
            current = await _paths(self.root, "ls-files")
            branch_head = await git(
                self.root,
                "for-each-ref",
                "--format=%(objectname)",
                "refs/heads/" + self.branch,
            )
            if branch_head != self.revision and (branch_head or not self.create):
                raise PermissionError("Target branch/base revision changed")
            entries = []
            for file in self.files:
                path = self.source_path(file["path"])
                if _entry(path) is not None and file["path"] not in current:
                    raise PermissionError(
                        "Untracked edit target must not be overwritten"
                    )
                entries.append({"path": file["path"], "expected": []})
            self.record = {
                "schema": "backlog-checkout-owner-v1",
                "generation": secrets.token_hex(32),
                "operation": self.operation,
                "pid": os.getpid(),
                "at": str(Timestamp.now()),
                "root": str(self.root),
                "return_branch": original,
                "return_head": await git(self.root, "rev-parse", "HEAD"),
                "branch": self.branch,
                "revision": self.revision,
                "object_format": await git(
                    self.root, "rev-parse", "--show-object-format"
                ),
                "commit_allowed": self.commit_allowed,
                "untracked": await untracked(self.root),
                "files": entries,
            }
            self._save()
            for file in self.files:
                self._expect(file["path"], file["text"])
            if not branch_head:
                await git(self.root, "branch", self.branch, self.revision)
            if original != self.branch:
                await git(self.root, "switch", self.branch)
            for file in self.files:
                self.source_path(file["path"])
            self.record["activated"] = True
            self._save()
            return self
        except BaseException:
            # Once a Git effect was attempted, retain ownership for inspection.
            if not self.record:
                self.folder.rmdir()
            raise

    async def finish(self) -> None:
        """Discard only authenticated temporary edits, preserving all other bytes."""
        with _transition(self.root):
            self._owned()
            await self._finish()

    async def _finish(self) -> None:  # noqa: C901, PLR0912 -- fenced restoration/release
        """Hold the same fence until all source effects and owner release finish."""
        await _operations(self.root)
        branch = await git(self.root, "branch", "--show-current")
        if branch != self.branch and (
            (self.record.get("activated") and not self.record.get("returning"))
            or branch != self.record["return_branch"]
        ):
            raise PermissionError("Checkout branch changed; recovery required")
        if not self.record["commit_allowed"] and await git(
            self.root, "rev-parse", "HEAD"
        ) != (self.revision if branch == self.branch else self.record["return_head"]):
            raise PermissionError("Checkout HEAD changed; recovery required")
        allowed = {f["path"]: f for f in self.record["files"]}
        changed = await _paths(self.root, "diff", "--name-only", "HEAD")
        if not changed <= set(allowed):
            raise PermissionError("Unexpected source changes; recovery required")
        present = await untracked(self.root)
        original = self.record["untracked"]
        if any(present.get(p) != h for p, h in original.items()) or not set(
            present
        ) <= set(original) | set(allowed):
            raise PermissionError("Untracked evidence changed; recovery required")
        tracked = await _paths(self.root, "ls-tree", "-r", "--name-only", "HEAD")
        indexed = await _paths(self.root, "ls-files")
        for name in changed | (set(present) - set(original)):
            if await fingerprint(self.root / name) not in allowed[name]["expected"]:
                raise PermissionError("Unreviewed source bytes; recovery required")
        for name in allowed:
            if name in changed and name in tracked:
                await git(
                    self.root,
                    "restore",
                    "--source=HEAD",
                    "--staged",
                    "--worktree",
                    "--",
                    name,
                )
            elif name in changed or (name in present and name not in original):
                if name in indexed:
                    await git(
                        self.root, "restore", "--source=HEAD", "--staged", "--", name
                    )
                (self.root / name).unlink()
        await idle(self.root)
        if self.record["return_branch"] != branch:
            if (
                await git(self.root, "rev-parse", self.record["return_branch"])
                != self.record["return_head"]
            ):
                raise PermissionError("Administrative branch moved; recovery required")
            await _collisions(self.root, self.record["return_head"])
            self.record["returning"] = True
            self._save()
            await git(self.root, "switch", self.record["return_branch"])
        if await untracked(self.root) != original:
            raise PermissionError("Untracked evidence changed across branch switch")
        history = self.folder.parent / "checkout-history"
        history.mkdir(exist_ok=True)
        sealed = {
            **self.record,
            "finished_at": str(Timestamp.now()),
            "final_head": await git(self.root, "rev-parse", "HEAD"),
        }
        self.cycle._save(history / (_digest(sealed) + ".json"), sealed)
        # One local directory rename is the release point. A crash cannot leave
        # an empty owner directory with no journal to authenticate for recovery.
        # Retain the original journal; never unlink a replacement owner's claim.
        self.folder.rename(history / ("released-" + _digest(sealed)))

    async def __aexit__(
        self,
        _kind: type[BaseException] | None,
        _error: BaseException | None,
        _trace: TracebackType | None,
    ) -> None:
        """Keep ownership on unknown bytes; otherwise restore even on cancellation."""
        await self.finish()


async def recover(cycle: WorkCycle, *, authorize: bool, expected_owner: str) -> None:
    """Explicit host reconciliation after the recorded process has stopped.

    Never redispatches, repeats validation, transfers authority or discards
    unknown bytes. The operator must first establish the old process is stopped.
    """
    if not authorize:
        raise PermissionError("Explicit stopped-owner reconciliation required")
    await cycle._coordinator()
    with _transition(cycle.root):
        path = cycle.root / ".local/backlog/checkout-owner/owner.json"
        value = load_json(path)
        digest = value.pop("sha256", None)
        if (
            digest != expected_owner
            or _digest(value) != digest
            or value.get("root") != str(cycle.root)
            or value.get("schema") != "backlog-checkout-owner-v1"
        ):
            raise PermissionError("Checkout recovery identity mismatch")
        checkout = Checkout(
            cycle, value["operation"], value["branch"], value["revision"]
        )
        checkout.record = value
        checkout._sealed = digest
        await checkout._finish()
