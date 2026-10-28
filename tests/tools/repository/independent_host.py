# Copyright (c) 2026
# ruff: noqa: E402, EM101, TRY003, T201 -- guards precede framework imports; bounded subprocess protocol
"""A deterministic non-model host; no Qwen, Codex, scripts or experiment dependency."""

from __future__ import annotations

import asyncio
import importlib.abc
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from importlib.machinery import ModuleSpec
    from types import ModuleType
    from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DENIED: list[str] = []


class NoApplications(importlib.abc.MetaPathFinder):
    """Deny model/application-specific implementation before loading it."""

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None = None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        """Reject forbidden implementation domains; ordinary framework imports work."""
        del path, target
        if fullname.split(".", maxsplit=1)[0] in {
            "apps",
            "scripts",
            "experiments",
        } or fullname.startswith("devtools.agents.integrations.codex"):
            DENIED.append("import:" + fullname)
            raise ImportError("Application or Codex implementation denied")
        return None


def guard_files(event: str, args: tuple[Any, ...]) -> None:
    """Permit only framework/dependencies and this authored host in the checkout."""
    if event != "open" or not isinstance(args[0], (str, bytes)):
        return
    path = Path(args[0].decode() if isinstance(args[0], bytes) else args[0]).resolve()
    if path.is_relative_to(ROOT) and not (
        path.is_relative_to(ROOT / "src/devtools")
        or path.is_relative_to(ROOT / ".venv")
        or path.is_relative_to(ROOT / "tests/tools/repository")
        or path in {ROOT / "tests/__init__.py", ROOT / "tests/tools/__init__.py"}
        or (
            path.parent
            in {ROOT / "tests/__pycache__", ROOT / "tests/tools/__pycache__"}
            and path.name.startswith("__init__.")
        )
    ):
        DENIED.append("file:" + path.relative_to(ROOT).as_posix())
        raise PermissionError("Application/configuration file access denied")


sys.meta_path.insert(0, NoApplications())
sys.addaudithook(guard_files)
sys.path.insert(0, str(ROOT))

from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.resource import ContentIdentity
from devtools.context.retrieval import build_source_search_index
from devtools.observability.commands.patterns import summarize_patterns
from devtools.tools import ToolRunner
from devtools.tools.repository.validation import CheckSelection
from devtools.tools.source import ScopedSourceTool
from tests.tools.repository.fixtures import CHECK, MODULE, SOURCE, procedure, repository


async def main() -> None:  # noqa: PLR0915 -- one real independent acceptance flow
    """Acquire actual source and run the real selected procedure, with no model loop."""
    for name in ("apps.qwen", "devtools.agents.integrations.codex"):
        try:
            __import__(name)
        except ImportError:
            pass
        else:
            raise AssertionError("Import guard inactive")
    try:
        (ROOT / "apps/qwen/tasks.py").read_bytes()
    except PermissionError:
        pass
    else:
        raise AssertionError("File guard inactive")
    root = Path.cwd()
    revision, scope = await repository(root)
    repo = Repository(scope.snapshot.repository_id)
    corpus = define_repository_text_corpus(
        discovery=discover_repository_resource_addresses(
            repository=repo,
            root=scope.root,
            requested_addresses=(RepositoryResourceAddress(MODULE),),
            maximum_resource_count=4,
            maximum_traversal_entry_count=128,
        ),
        selected_addresses=(RepositoryResourceAddress(MODULE),),
    )
    index = build_source_search_index(
        scope.snapshot,
        corpus=realize_repository_text_corpus(
            definition=corpus,
            snapshot=scope.snapshot,
        ),
    )
    option = SourceRangeDisclosureOption(
        "Inspect authorized change",
        index.views[0].units[0],
        0,
        len(SOURCE),
        1024,
    )
    acquired = await ToolRunner().execute(ScopedSourceTool(scope), option)
    assert acquired.items[0].text == "VALUE = 7\n"
    provenance = acquired.items[0].native_provenance
    assert isinstance(provenance, SourceRangeDisclosureOption)
    assert provenance.unit.resource.content_identity == ContentIdentity.from_text(
        "VALUE = 7\n",
    )
    scenario = sys.argv[1]
    tool = procedure(
        root,
        revision,
        scope,
        code="raise SystemExit(4)" if scenario == "failed" else CHECK,
    )
    if scenario == "unauthorized":
        tool.plan = replace(tool.plan, allowed_changes=frozenset())
    # A real conditional selection skips a nonapplicable host-defined second check.
    second = replace(tool.plan.checks.checks[0], name="not-applicable")
    new_checks = replace(tool.plan.checks, checks=(*tool.plan.checks.checks, second))
    tool.plan = replace(
        tool.plan,
        checks=new_checks,
        selection=(
            *tool.plan.selection,
            CheckSelection(
                "not-applicable",
                frozenset({RepositoryResourceAddress("untouched.txt")}),
            ),
        ),
    )
    tool.check_tool.plan = new_checks
    report = await ToolRunner().execute(tool, None)
    assert report.before is not None
    assert report.before.revision == revision
    assert {x.path: (x.index, x.worktree) for x in report.before.changes} == {
        MODULE: ("M", " "),
        "readme.txt": (" ", "M"),
        "notes [new].txt": ("?", "?"),
    }
    assert report.status == (
        "refused"
        if scenario == "unauthorized"
        else "failed"
        if scenario == "failed"
        else "passed"
    )
    if scenario == "success":
        result = report.checks[0].result
        assert result is not None
        assert result.command_result.exit_code == 0
        assert result.command_result.command.argv[-1] == MODULE
        assert (
            result.command_result.stdout.replace(b"\r\n", b"\n")
            == b"verified:7\nPRIVATE_SENTINEL\n"
        )
        assert result.inputs_current is True
        assert (root / ".local/count").read_text() == "x"
    assert all(c.name != "not-applicable" for c in report.checks)
    assert not any(
        n.startswith(
            ("apps", "scripts", "experiments", "devtools.agents.integrations.codex"),
        )
        for n in sys.modules
    )
    output = {
        "status": report.status,
        "revision": revision,
        "snapshot": str(scope.snapshot.id),
        "content": str(ContentIdentity.from_text(SOURCE)),
        "span": option.span,
        "paths": [x.path for x in report.before.changes],
        "checks": [
            {
                "name": c.name,
                "status": c.status,
                "exit": c.result.command_result.exit_code if c.result else None,
            }
            for c in report.checks
        ],
        "patterns": [asdict(c) for c in summarize_patterns(report.observations)],
        "entered": sum(o.entered is True for o in report.observations),
        "denied": DENIED,
        "model_calls": 0,
    }
    text = json.dumps(output)
    assert "PRIVATE_SENTINEL" not in text
    print(text)


if __name__ == "__main__":
    asyncio.run(main())
