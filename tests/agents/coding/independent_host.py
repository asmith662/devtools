# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, E402 -- guards precede framework imports; literal schedules
"""Independent scoped-source and fixed-check host; no application data."""

from __future__ import annotations

import asyncio
import importlib.abc
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence
    from importlib.machinery import ModuleSpec
    from types import ModuleType

CANONICAL = Path(__file__).resolve().parents[3]
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
        or path.is_relative_to(CANONICAL / "tests" / "agents" / "coding")
        or path
        in {
            CANONICAL / "tests" / "__init__.py",
            CANONICAL / "tests" / "agents" / "__init__.py",
        }
        or (
            path.parent
            in {
                CANONICAL / "tests" / "__pycache__",
                CANONICAL / "tests" / "agents" / "__pycache__",
            }
            and path.name.startswith("__init__.")
        )
    ):
        DENIED.append("file:" + path.relative_to(CANONICAL).as_posix())
        raise PermissionError("Application/configuration file access denied")


sys.meta_path.insert(0, NoApplications())
sys.addaudithook(guard_files)


sys.path.insert(0, str(CANONICAL))
from tests.agents.coding.fixtures import (
    scenario,
)


async def main() -> None:
    """Run the same public framework process with application imports/reads denied."""
    try:
        __import__("apps.qwen")
    except ImportError:
        pass
    else:
        raise AssertionError("Import guard inactive")
    try:
        (CANONICAL / "apps/qwen/tasks.py").read_bytes()
    except PermissionError:
        pass
    else:
        raise AssertionError("File guard inactive")
    value = await scenario(
        Path.cwd(),
        sys.argv[1],
        projection="--projection" in sys.argv[2:],
    )
    assert not any(
        n.split(".")[0] in {"apps", "scripts", "experiments"} for n in sys.modules
    )
    value["denied"] = DENIED
    print(json.dumps(value, sort_keys=True))  # noqa: T201 -- bounded subprocess protocol


if __name__ == "__main__":
    asyncio.run(main())
