# Copyright (c) 2026
"""Build explicit synthetic snapshots and native RI inputs for role tests."""

from pathlib import Path

from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.project_configuration import (
    PythonConfigurationFrame,
    PythonConfigurationResolutionAnalysis,
    analyze_python_project_configuration,
    resolve_python_project_configuration,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.core.paths import ResolvedPath


def snapshot(tmp_path: Path, resources: dict[str, str]) -> RepositorySnapshot:
    """Observe only explicitly supplied resources, never the actual repository."""
    for address, content in resources.items():
        path = tmp_path / address
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000075"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in resources),
        maximum_resource_bytes=1024 * 1024,
    )


def configuration_targets(
    observed: RepositorySnapshot,
    config: str = "pyproject.toml",
    root: str = ".",
) -> PythonConfigurationResolutionAnalysis:
    """Supply explicit tool and module frames to the existing configuration RI."""
    module_root = PythonModuleRoot(root)
    modules = interpret_python_module_resources(
        observed,
        module_root=module_root,
        resource_addresses=tuple(item.address for item in observed.resources),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=observed.repository_id,
        interpretations=modules.interpretations,
    )
    return resolve_python_project_configuration(
        observed,
        analyze_python_project_configuration(
            observed,
            address=RepositoryResourceAddress(config),
        ),
        universe=universe,
        frame=PythonConfigurationFrame(module_root, module_root),
    )
