# Copyright (c) 2026
# ruff: noqa: INP001, PLR2004, COM812 -- operational CLI test conventions

"""Trusted local evaluation needs no production approval or terminal ritual."""

from __future__ import annotations

import asyncio
import hashlib
import importlib.util
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen.tasks import MARKDOWN
from devtools.models.interaction import InteractionSource, ModelResponse, ModelToolCall
from scripts.backlog.coordinator import git
from scripts.backlog.intake import Intake

if TYPE_CHECKING:
    from types import ModuleType

    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelInteraction, ModelRequest


@pytest.fixture
def cli() -> ModuleType:
    """Load the operational entrypoint without relying on collection order."""
    specification = importlib.util.spec_from_file_location(
        "coding_worker_cli_test",
        Path(__file__).resolve().parents[3] / "scripts/qwen/coding_worker.py",
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@pytest.mark.parametrize("absolute", [False, True])
@pytest.mark.parametrize("task", ["markdown-fences", "python-source-segments"])
def test_report_directory_resolves_against_cwd_without_confirmation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    cli: ModuleType,
    task: str,
    *,
    absolute: bool,
) -> None:
    """A relative report is based on the caller's cwd, never the script root."""
    monkeypatch.chdir(tmp_path)
    expected = tmp_path / "new" / "run"
    value = str(expected) if absolute else "new/run"
    monkeypatch.setattr(
        "sys.argv", ["worker", "--task", task, "--report-directory", value]
    )

    async def boundary(
        _root: Path, folder: Path, *, task: CodingTask, branch: str | None
    ) -> None:
        assert folder == expected
        assert task.name in {"markdown-fences", "python-source-segments"}
        assert branch is None
        message = "resolved local boundary; no execution"
        raise SystemExit(message)

    monkeypatch.setattr(cli, "run_local_task", boundary)
    monkeypatch.setattr("builtins.input", lambda _: pytest.fail("No terminal gate"))
    with pytest.raises(SystemExit, match="resolved local boundary"):
        asyncio.run(cli.main())
    assert not expected.exists()


@pytest.mark.parametrize("invalid", ["", "\x00", "existing", "file/child"])
def test_invalid_report_directory_fails_before_dispatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    invalid: str,
    cli: ModuleType,
) -> None:
    """Empty, malformed, occupied and non-directory parent paths fail closed."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "existing").mkdir()
    (tmp_path / "file").write_text("occupied", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["worker", "--report-directory", invalid])

    async def forbidden(*_arguments: object, **_kwargs: object) -> None:
        pytest.fail("Invalid paths must be rejected before dispatch")

    monkeypatch.setattr(cli, "run_local_task", forbidden)
    with pytest.raises(SystemExit) as result:
        asyncio.run(cli.main())
    assert result.value.code == 2


@pytest.mark.parametrize("ready", [False, True])
def test_shared_local_profile_factory_never_invokes_model(
    cli: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, ready: bool
) -> None:
    """Both entrypoints reuse existing readiness/profile and client construction."""

    async def status(_root: Path) -> dict[str, object]:
        return {
            "state": "READY" if ready else "STOPPED",
            "expected_fingerprint": "fixture",
            "observed_fingerprint": "fixture",
        }

    calls = []
    client = object()

    def construct(**arguments: object) -> object:
        calls.append(arguments)
        return client

    async def command(_root: Path, *_arguments: str) -> dict[str, str]:
        return {"stdout": "fixture-head"}

    monkeypatch.setattr(cli, "_qwen_status", status)
    monkeypatch.setattr(cli, "_command", command)
    monkeypatch.setattr(cli, "LlamaCppInteraction", construct)
    if not ready:
        with pytest.raises(RuntimeError, match="MODEL_SERVICE_NOT_READY"):
            asyncio.run(cli.local_interaction(tmp_path))
        assert calls == []
    else:
        interaction, provenance = asyncio.run(cli.local_interaction(tmp_path))
        assert interaction is client
        assert calls[0]["model"] == "qwen38-local"
        assert provenance["model"] == "qwen38-local"
        assert provenance["profile"]


def test_host_definition_selects_native_worker_without_confirmation(
    cli: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The existing task contract selects read scope and truthful invocation bounds."""
    monkeypatch.chdir(tmp_path)
    task = replace(MARKDOWN, context_mode="on-demand", maximum_calls=6)
    (tmp_path / "task.json").write_text(json.dumps(asdict(task)), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        ["worker", "--task-definition", "task.json", "--report-directory", "run"],
    )

    async def dispatch(
        _root: Path, folder: Path, *, task: CodingTask, branch: str | None
    ) -> None:
        assert task.context_mode == "on-demand"
        assert task.maximum_calls == 6
        assert folder == tmp_path / "run"
        assert branch is None
        message = "local dispatch boundary reached; no call"
        raise SystemExit(message)

    monkeypatch.setattr(cli, "run_local_task", dispatch)
    with pytest.raises(SystemExit, match="boundary"):
        asyncio.run(cli.main())
    (tmp_path / "task.json").write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        asyncio.run(cli.main())
    assert error.value.code == 2


@pytest.mark.parametrize("accepted", [False, True, None])
def test_cli_reports_local_outcome_without_input(
    cli: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    accepted: bool | None,
) -> None:
    """Noninteractive local invocation is enough; unavailable service stays explicit."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["worker", "--report-directory", "run"])
    monkeypatch.setattr("builtins.input", lambda _: pytest.fail("No approval prompt"))

    async def run(*_args: object, **_kwargs: object) -> dict[str, Any]:
        if accepted is None:
            message = "MODEL_SERVICE_NOT_READY_OR_PROFILE_CHANGED"
            raise RuntimeError(message)
        return {
            "accepted": accepted,
            "disposition": "ACCEPTED" if accepted else "FAILED",
            "turns": [],
            "elapsed_seconds": 0.0,
        }

    monkeypatch.setattr(cli, "run_local_task", run)
    assert asyncio.run(cli.main()) == (2 if accepted is None else int(not accepted))


@pytest.mark.parametrize("git_newlines", [False, True])
def test_local_runner_owns_source_without_backlog_approval(  # noqa: PLR0915 -- complete branch/materialization/restoration scenario
    cli: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    git_newlines: bool,  # noqa: FBT001 -- explicit Git materialization fixture
) -> None:
    """An authored tiny repository exercises ownership/restoration, not live Qwen."""
    source = "src/devtools/example.py"
    tests = "tests/test_example.py"
    for path, text in (
        (source, "def number():\n    return 1\n"),
        ("src/devtools/__init__.py", ""),
        (
            tests,
            (
                "from devtools.example import number\n"
                "def test_existing():\n    assert number() > 0\n"
            ),
        ),
        ("docs/backlog/overview.md", "# Empty fixture backlog\n"),
        (".gitignore", ".local/\n__pycache__/\n.pytest_cache/\n"),
    ):
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="")

    class LocalModel:
        source = InteractionSource("scripted-local-fixture")

        async def send(self, request: ModelRequest) -> ModelResponse:
            assert request.tools
            return ModelResponse(
                "",
                self.source,
                tool_calls=(
                    ModelToolCall(
                        "propose_edit",
                        json.dumps(
                            {
                                "path": source,
                                "old_text": "return 1",
                                "new_text": "return 2",
                            }
                        ),
                        "edit",
                    ),
                ),
            )

    async def factory(_root: Path) -> tuple[ModelInteraction, dict[str, Any]]:
        return LocalModel(), {"model": "scripted-local-fixture"}

    def forbidden(*_args: object, **_kwargs: object) -> None:
        pytest.fail("Local evaluation must not consult backlog approval")

    monkeypatch.setattr(cli, "local_interaction", factory)
    monkeypatch.setattr(Intake, "approved_item", forbidden)
    monkeypatch.setattr("builtins.input", lambda _: pytest.fail("No approval prompt"))

    async def run() -> None:
        await git(tmp_path, "init", "--initial-branch=feat/host")
        await git(tmp_path, "config", "user.name", "Fixture")
        await git(tmp_path, "config", "user.email", "fixture@example.invalid")
        await git(tmp_path, "config", "core.autocrlf", "false")
        await git(tmp_path, "config", "devtools.backlogCoordinator", str(tmp_path))
        await git(tmp_path, "add", ".")
        await git(tmp_path, "commit", "-m", "Authored local fixture")
        head = await git(tmp_path, "rev-parse", "HEAD")
        task = replace(
            MARKDOWN,
            name="local-fixture",
            source=source,
            tests=(tests,),
            objective="Correct the demonstrated fixture value",
            baseline_revision=head,
            baseline_hashes=tuple(
                (p, hashlib.sha256((tmp_path / p).read_bytes()).hexdigest())
                for p in (source, tests)
            ),
            context=(
                (source, "number", "symbol", "file"),
                (tests, "number", "file", "file"),
            ),
            oracle="assert module.number() == 2\n",
        )
        for branch in ("main", "other"):
            with pytest.raises(PermissionError, match="feature branch"):
                await cli.run_local_task(
                    tmp_path, tmp_path / ".local/refused", task=task, branch=branch
                )
        if git_newlines:
            await git(tmp_path, "config", "core.autocrlf", "true")
            for relative in (source, tests):
                path = tmp_path / relative
                path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
            # Adopt the fixture's newline policy without changing its Git blobs.
            await git(tmp_path, "add", "--renormalize", "--", source, tests)
            assert await git(tmp_path, "diff", "--cached") == ""
        original_bytes = (tmp_path / source).read_bytes()
        result = await cli.run_local_task(tmp_path, tmp_path / ".local/run", task=task)
        assert result["accepted"]
        assert result["source_restored"]
        assert (
            result["provenance"]["execution_category"]
            == "trusted-local-development-evaluation"
        )
        assert result["provenance"]["publication_authority"] == "NONE"
        assert await git(tmp_path, "branch", "--show-current") == "feat/host"
        assert await git(tmp_path, "rev-parse", "HEAD") == head
        assert (tmp_path / source).read_text() == "def number():\n    return 1\n"
        assert (tmp_path / source).read_bytes() == original_bytes
        assert not (tmp_path / ".local/backlog/checkout-owner").exists()
        assert not (tmp_path / ".local/backlog/work").exists()
        assert not (tmp_path / ".local/backlog/delegations").exists()
        with pytest.raises(ValueError, match="already exist"):
            await cli.run_local_task(tmp_path, tmp_path / ".local/run", task=task)
        (tmp_path / source).write_text("unrelated dirty work", encoding="utf-8")
        with pytest.raises(PermissionError, match="not clean"):
            await cli.run_local_task(tmp_path, tmp_path / ".local/dirty", task=task)
        assert (tmp_path / source).read_text() == "unrelated dirty work"
        assert not (tmp_path / ".local/backlog/checkout-owner").exists()

    asyncio.run(run())
