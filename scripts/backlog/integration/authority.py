# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, SLF001, PLR2004 -- closed local-host contract
"""Separate standing integration authority; coding grants never confer it."""

from __future__ import annotations

import getpass
import re
from typing import TYPE_CHECKING, Any

from devtools.context import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from scripts.backlog.coordinator import git
from scripts.backlog.intake import _digest
from scripts.backlog.work import _load

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from scripts.backlog.work import WorkCycle

ACTIONS = ("install", "validate", "publish", "promote", "verify", "closeout")


def policy_check(value: dict[str, Any]) -> None:  # noqa: C901, PLR0912 -- closed policy
    """Validate exact paths, destinations, effects and bounded reservations."""
    if set(value) != {
        "sources",
        "tests",
        "oracles",
        "remote",
        "destinations",
        "worktree_root",
        "actions",
        "protected",
        "corrections",
        "parent_close",
        "max_integrations",
        "max_files",
        "max_bytes",
        "validation_seconds",
    }:
        raise ValueError("Unsupported integration policy fields")
    for name in ("sources", "tests", "oracles", "destinations", "actions"):
        if (
            not isinstance(value[name], list)
            or not value[name]
            or len(value[name]) > 100
            or any(not isinstance(v, str) for v in value[name])
        ):
            raise ValueError("Explicit bounded integration selectors required")
    if not set(value["actions"]) <= set(ACTIONS):
        raise ValueError("Unknown integration action")
    for name in ("protected", "corrections", "parent_close"):
        if type(value[name]) is not bool:
            raise ValueError("Explicit boolean integration effects required")
    for name, prefix in (("sources", "src/devtools/"), ("tests", "tests/")):
        for path in value[name]:
            RepositoryResourceAddress(path)
            if not path.startswith(prefix) or not path.endswith(".py"):
                raise ValueError("Integration requires exact source/test paths")
    if any(not re.fullmatch(r"[a-f0-9]{64}", v) for v in value["oracles"]):
        raise ValueError("Integration acceptance code must be pinned")
    for name, limit in (
        ("max_integrations", 100),
        ("max_files", 20),
        ("max_bytes", 262144),
        ("validation_seconds", 1800),
    ):
        if type(value[name]) is not int or not 1 <= value[name] <= limit:
            raise ValueError("Invalid integration allowance")
    resolve_path(value["worktree_root"])
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", value["remote"]):
        raise ValueError("Invalid existing remote name")


class IntegrationAuthority:
    """Use the same coordinator, trusted-host confirmation and atomic writer."""

    def __init__(self, cycle: WorkCycle) -> None:
        """Bind the existing WorkCycle owner."""
        self.cycle = cycle

    def folder(self, identity: str) -> Path:
        """Confine grant identities before accessing operational records."""
        if not re.fullmatch(r"[a-f0-9]{64}", identity):
            raise ValueError("Invalid integration grant identity")
        return self.cycle.intake._path(".local/backlog/integration-grants/" + identity)

    async def issue(
        self,
        policy: dict[str, Any],
        *,
        reference: str,
        expires: Timestamp,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Issue only under an actual local maintainer decision, default deny."""
        await self.cycle._coordinator()
        policy_check(policy)
        for branch in policy["destinations"]:
            await git(self.cycle.root, "check-ref-format", "refs/heads/" + branch)
        if not reference.strip() or expires.value <= Timestamp.now().value:
            raise PermissionError("Decision provenance and future expiry required")
        grant = {
            "schema": "backlog-integration-grant-v1",
            "principal": getpass.getuser(),
            "reference": reference,
            "issued_at": str(Timestamp.now()),
            "expires_at": str(expires),
            "coordinator": str(self.cycle.root),
            "coordinator_branch": await git(
                self.cycle.root, "branch", "--show-current"
            ),
            "remote_url": await git(
                self.cycle.root, "remote", "get-url", policy["remote"]
            ),
            "policy": policy,
            "supervisor": "Codex",
            "scope": "development-integration-only; no model or scientific dispatch",
        }
        if authorize is None or not authorize(
            {"operation": "issue-integration-grant", "grant": grant}
        ):
            raise PermissionError("Genuine integration grant consent required")
        await self.cycle._coordinator()
        if Timestamp.now().value >= expires.value:
            raise PermissionError("Integration grant expired during consent")
        with self.cycle.intake._writer():
            folder = self.folder(_digest(grant))
            folder.mkdir(parents=True)
            return self.cycle._save(folder / "grant.json", grant)

    async def revoke(
        self,
        identity: str,
        *,
        reference: str,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Stop subsequent stages; already published commits are not rolled back."""
        await self.cycle._coordinator()
        record = _load(
            self.folder(identity) / "grant.json", "backlog-integration-grant-v1"
        )
        if record["principal"] != getpass.getuser() or not reference.strip():
            raise PermissionError("Issuing host principal and provenance required")
        if authorize is None or not authorize(
            {
                "operation": "revoke-integration-grant",
                "grant": record,
                "reference": reference,
            }
        ):
            raise PermissionError("Genuine revocation consent required")
        with self.cycle.intake._writer():
            return self.cycle._save(
                self.folder(identity) / "revocation.json",
                {
                    "schema": "backlog-integration-revocation-v1",
                    "grant": identity,
                    "reference": reference,
                    "principal": getpass.getuser(),
                    "at": str(Timestamp.now()),
                },
            )

    async def admit(  # noqa: C901 -- fixed scope, expiry and effect admission
        self, identity: str, plan: dict[str, Any], action: str
    ) -> dict[str, Any]:
        """Authenticate current authority independently of coding/review evidence."""
        await self.cycle._coordinator()
        folder = self.folder(identity)
        grant = _load(folder / "grant.json", "backlog-integration-grant-v1")
        policy = grant["policy"]
        policy_check(policy)
        now = Timestamp.now().value
        if (
            grant["sha256"] != identity
            or grant["principal"] != getpass.getuser()
            or grant["coordinator"] != str(self.cycle.root)
            or grant["supervisor"] != "Codex"
            or not Timestamp.from_isoformat(grant["issued_at"]).value
            <= now
            < Timestamp.from_isoformat(grant["expires_at"]).value
            or (folder / "revocation.json").exists()
        ):
            raise PermissionError(
                "Integration grant expired, revoked or differs from host"
            )
        if (
            action not in policy["actions"]
            or plan["remote"] != policy["remote"]
            or plan["destination"] not in policy["destinations"]
            or plan["remote_url"] != grant["remote_url"]
            or await git(self.cycle.root, "remote", "get-url", plan["remote"])
            != grant["remote_url"]
        ):
            raise PermissionError("Integration action/remote/target outside grant")
        if (
            plan["oracle_sha256"] not in policy["oracles"]
            or not set(plan["tests"]) <= set(policy["tests"])
            or len(plan["files"]) > policy["max_files"]
            or sum(len(f["text"].encode()) for f in plan["files"]) > policy["max_bytes"]
            or plan["validation_seconds"] > policy["validation_seconds"]
        ):
            raise PermissionError("Integration code or resource allowance exceeded")
        for f in plan["files"]:
            if f["path"] not in policy["sources"] + policy["tests"] or (
                f["author"] != "Qwen"
                and f["path"] in policy["sources"]
                and not policy["corrections"]
            ):
                raise PermissionError("Unapproved source/test addition or correction")
        for path in (plan["worktree"], plan["verification_worktree"]):
            resolved = resolve_path(path).value
            allowed = resolve_path(policy["worktree_root"]).value
            if not resolved.is_relative_to(allowed) or resolved in (
                allowed,
                self.cycle.root,
            ):
                raise PermissionError("Integration worktree outside grant")
        if plan["parent_complete"] and not policy["parent_close"]:
            raise PermissionError("Parent backlog closeout is not delegated")
        if action == "promote" and plan["destination"] in {"main", "master"}:
            configured = (
                await git(
                    self.cycle.root,
                    "config",
                    "--get-all",
                    "devtools.integrationProtectedTarget",
                    missing_ok=True,
                )
            ).splitlines()
            if (
                not policy["protected"]
                or plan["remote"] + ":" + plan["destination"] not in configured
            ):
                raise PermissionError(
                    "Protected promotion requires grant AND repository policy"
                )
        return grant
