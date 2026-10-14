# Copyright (c) 2026
# ruff: noqa: ANN401 -- frozen external-Agent sandbox configuration
"""Windows MXC semantic-worker access and compatible engineering smoke identity."""

from __future__ import annotations

import json
import platform
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import binary, load, require, safe

SMOKE_ADDRESS = (
    "experiments/orchestration/engineering/host_disclosure/smoke-receipt.json"
)

ENVIRONMENT = (
    "PATH",
    "SYSTEMROOT",
    "WINDIR",
    "TEMP",
    "TMP",
    "USERPROFILE",
    "APPDATA",
    "LOCALAPPDATA",
    "COMSPEC",
    "SystemDrive",
    "ProgramFiles",
    "ProgramW6432",
    "ProgramData",
    "ALLUSERSPROFILE",
    "PUBLIC",
    "HOMEDRIVE",
    "HOMEPATH",
)


def configuration() -> dict[str, Any]:
    """Freeze deny-by-default access; model identity does not select permissions."""
    return {
        "schema": "host-disclosure-semantic-runtime-v1",
        "windows_sandbox": "mxc",
        "approval": "never",
        "cli_version": "0.162.1",
        "delivery": "UTF8_STDIN",
        "response": "NATIVE_JSON_SCHEMA_AND_FINAL_MESSAGE",
        "tools": "DISABLED; TOOL_ATTEMPT_REJECTS_RESPONSE",
        "scientific_filesystem_dependency": False,
        "network": False,
        "web": "disabled",
        "fresh": True,
    }


def toml(value: Any) -> str:
    """Encode the small frozen inline TOML table for direct argv transport."""
    if isinstance(value, dict):
        return (
            "{"
            + ",".join(json.dumps(k) + "=" + toml(v) for k, v in value.items())
            + "}"
        )
    return json.dumps(value)


def overrides(value: dict[str, Any], workspace: Path) -> list[str]:
    """Deny scientific filesystem access; no model write authority is granted."""
    require(value == configuration(), "Unsupported semantic isolation/runtime binding")
    require(not any(workspace.iterdir()), "Semantic CWD must be empty")
    filesystem = {
        ":root": "deny",
        ":minimal": "read",
        ":tmpdir": "deny",
        ":slash_tmp": "deny",
        ":workspace_roots": "deny",
    }
    settings = {
        "windows.sandbox": "mxc",
        "default_permissions": "semantic-worker",
        "permissions.semantic-worker.filesystem": filesystem,
        "permissions.semantic-worker.network.enabled": False,
        "web_search": "disabled",
        "project_doc_max_bytes": 0,
        "features.skip_host_skill_discovery": True,
        "suppress_unstable_features_warning": True,
        "tools.view_image": False,
        **{
            "features." + name: False
            for name in (
                "plugins",
                "apps",
                "remote_plugin",
                "browser_use",
                "browser_use_external",
                "computer_use",
                "multi_agent",
                "memories",
                "hooks",
                "skill_search",
                "image_generation",
                "workspace_dependencies",
                "shell_tool",
                "unified_exec",
                "code_mode_host",
                "view_image",
                "goals",
                "sleep_tool",
            )
        },
    }
    return [
        argument
        for key, setting in settings.items()
        for argument in ("-c", key + "=" + toml(setting))
    ]


def identity() -> dict[str, Any]:
    """Key reusable smoke evidence to host, CLI, implementation and permissions."""
    package = Path(__file__).parent
    root = package.parents[2]
    return {
        "os": platform.platform(),
        "python": platform.python_version(),
        "cli_version": "0.162.1",
        "configuration": configuration(),
        "semantic_implementation": {
            name: digest((package / name).read_bytes())
            for name in (
                "codex.py",
                "semantic.py",
                "process.py",
                "supervisor.py",
                "evidence.py",
            )
        },
        "isolation_implementation": digest(Path(__file__).read_bytes()),
        "controller_semantic_invocation": digest(
            (package.parent / "controller.py").read_bytes(),
        ),
        "source_grounding_adapter": {
            name: digest((root / "experiments/source_grounding" / name).read_bytes())
            for name in ("workers.py", "response.py", "reviewer.py", "packets.py")
        },
    }


def authenticate(receipt: dict[str, Any]) -> None:
    """Engineering evidence is compatible only for the exact current runtime."""
    require(
        receipt["schema"] == "semantic-worker-smoke-v1"
        and receipt["status"] == "PASS"
        and receipt["runtime"] == identity()
        and receipt["runtime_sha256"] == digest(json_bytes(identity()))
        and receipt["model"] == "GPT-6 Luna"
        and receipt["reasoning"] == "Medium"
        and set(receipt["checks"])
        == {
            "direct",
            "nested",
            "isolation",
            "artifacts",
            "no_tools",
            "no_scientific_filesystem_dependency",
        }
        and all(receipt["checks"].values()),
        "Compatible successful real-worker smoke required",
    )


def authenticate_configuration(config: Any) -> None:
    """Require exact registered smoke bytes before real-case semantic entry."""
    binding = config.get("smoke_receipt")
    require(
        isinstance(binding, dict) and set(binding) == {"path", "sha256"},
        "Successful runtime smoke binding required",
    )
    root = Path(__file__).resolve().parents[3]
    path = safe(root, binding["path"])
    require(
        digest(binary(path)) == binding["sha256"],
        "Runtime smoke receipt digest differs",
    )
    authenticate(load(path))
