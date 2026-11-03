# Copyright (c) 2026
"""Direct-maintainer backlog completion remains separate from worker candidates."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, cast

import pytest

from scripts.backlog.coordinator import git
from tests.scripts.backlog import test_work


@pytest.fixture
def direct_fixture(tmp_path: Path) -> dict[str, Any]:
    """Reuse the tiny authored coordinator fixture without an execution attempt."""
    fixture_factory = cast("Any", test_work.fixture)
    return cast("dict[str, Any]", fixture_factory.__wrapped__(tmp_path))


async def prepare_direct_fixture(f: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Publish one independently authored implementation commit to fixture main."""
    root = Path(f["root"])
    await git(root, "branch", "-m", "main")
    await git(root, "config", "user.name", "Fixture Maintainer")
    await git(root, "config", "user.email", "fixture@example.invalid")
    source = root / "src/devtools/resources/filesystem/models/markdown/file.py"
    source.write_text(source.read_text() + "\n# direct repair\n")
    await git(
        root,
        "add",
        "--",
        "src/devtools/resources/filesystem/models/markdown/file.py",
    )
    await git(root, "commit", "-m", "Direct fixture implementation")
    commit = await git(root, "rev-parse", "HEAD")
    remote = root.parent / "origin.git"
    await git(root, "init", "--bare", str(remote))
    await git(root, "remote", "add", "origin", str(remote))
    await git(root, "push", "origin", "main:refs/heads/main")
    receipt = root / ".local/validation/direct.json"
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(
        json.dumps(
            {
                "status": "passed",
                "executed_commit": commit,
                "configured_coverage_percent": 100.0,
                "command": ["uv", "run", "python", "scripts/validate_development.py"],
                "passed": 12,
                "skipped": 0,
            },
        ),
    )
    spec = {
        "implementation_commit": commit,
        "validation_commit": commit,
        "implementation_by": "Codex direct maintainer",
        "remote": "origin",
        "destination": "main",
        "validation_receipt": ".local/validation/direct.json",
        "obligations": ["Preserve existing backlog and source contracts."],
        "remaining_obligations": [],
        "evidence": [
            "src/devtools/resources/filesystem/models/markdown/file.py",
            "tests/resources/filesystem/models/markdown/test_file.py",
        ],
    }
    return spec, commit


def test_direct_completion_closes_only_with_exact_destination_and_review(
    direct_fixture: dict[str, Any],
) -> None:
    """Record direct provenance without manufacturing a native candidate receipt."""

    async def run() -> tuple[dict[str, Any], Path, Path, list[dict[str, Any]], str]:
        f = direct_fixture
        spec, commit = await prepare_direct_fixture(f)
        item_path = Path(f["intake"].approved_item(f["item"])["path"])
        seen: list[dict[str, Any]] = []

        def authorize(request: dict[str, Any]) -> bool:
            seen.append(request)
            return True

        record = await f["cycle"].integration.direct_closeout(
            f["item"],
            spec,
            reviewer="Codex",
            review_reference="fixture://independent-completion-review",
            rationale=(
                "The direct implementation and every declared obligation were reviewed."
            ),
            authorization_reference="fixture://operator-direct-completion",
            authorize=authorize,
        )
        return record, item_path, Path(f["root"]), seen, commit

    record, item_path, root, seen, commit = asyncio.run(run())
    assert seen[0]["operation"] == "direct-backlog-completion"
    assert record["decision"] == "COMPLETE_PARENT"
    assert record["implementation_commit"] == commit
    assert record["validation_commit"] == commit
    assert record["protected_validation"]["executed_commit"] == commit
    assert record["completion_review"]["reviewer"] == "Codex"
    assert "- status: CLOSED" in item_path.read_text()
    assert "| CLOSED |" in (root / "docs/backlog/overview.md").read_text()


def test_direct_completion_rejects_mismatched_protected_commit(
    direct_fixture: dict[str, Any],
) -> None:
    """A passing receipt for another tree cannot authorize a direct closeout."""

    async def run() -> None:
        f = direct_fixture
        spec, _ = await prepare_direct_fixture(f)
        item = f["item"]
        receipt = Path(f["root"]) / spec["validation_receipt"]
        value = json.loads(receipt.read_text())
        value["executed_commit"] = "0" * 40
        receipt.write_text(json.dumps(value))
        with pytest.raises(PermissionError, match="Exact protected development"):
            await f["cycle"].integration.direct_closeout(
                item,
                spec,
                reviewer="Codex",
                review_reference="fixture://review",
                rationale="Fixture mismatch must refuse.",
                authorization_reference="fixture://operator",
                authorize=lambda _: True,
            )

    asyncio.run(run())


def test_direct_completion_requires_exact_operator_authorization(
    direct_fixture: dict[str, Any],
) -> None:
    """The direct evidence contract does not turn passing validation into authority."""

    async def run() -> None:
        f = direct_fixture
        spec, _ = await prepare_direct_fixture(f)
        with pytest.raises(PermissionError, match="Explicit direct-completion"):
            await f["cycle"].integration.direct_closeout(
                f["item"],
                spec,
                reviewer="Codex",
                review_reference="fixture://review",
                rationale="All declared obligations are complete.",
                authorization_reference="fixture://operator-denial",
                authorize=lambda _: False,
            )

    asyncio.run(run())
