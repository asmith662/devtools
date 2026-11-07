# Copyright (c) 2026
"""Base product imports must not load an optional numerical distribution."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor


def test_agent_and_independent_inspector_import_without_optional_numerical_modules(
    tmp_path: Path,
) -> None:
    """Deny numerical imports in a fresh actual one-process Python host."""
    code = """
import importlib.abc,site,sys
site.addsitedir(sys.argv[1])
class NoNumerics(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in ('numpy','scipy','sklearn','threadpoolctl'):
            raise ImportError('optional numerical import forbidden by base control')
sys.meta_path.insert(0,NoNumerics())
import devtools.agents.coding
import devtools.agents.learning.process
import devtools.learning.integrations.local.inspection
assert not {'numpy','scipy','sklearn','threadpoolctl'} & set(sys.modules)
print('base-imports:PASS')
"""
    result = asyncio.run(
        CommandExecutor(contained=True).execute(
            Command(str(getattr(sys, "_base_executable", sys.executable)))
            .args("-S", "-c", code, str(Path(sys.prefix) / "Lib/site-packages"))
            .cwd(resolve_path(tmp_path))
            .with_environment({"PYTHONPATH": "", "PYTHONDONTWRITEBYTECODE": "1"})
            .with_timeout(Duration.seconds(30)),
        ),
    )
    assert result.succeeded, result.stderr.decode()
    assert result.stdout.strip() == b"base-imports:PASS"
