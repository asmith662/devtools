# Copyright (c) 2026
# ruff: noqa: ANN401, PLC0415 -- lazy capacity import avoids runtime identity cycle
"""Windows MXC semantic-worker access and compatible engineering smoke identity."""

from __future__ import annotations

import json
import platform
import tomllib
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
        "schema": "host-disclosure-semantic-runtime-v3",
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
        "provider": "BUILTIN_OPENAI",
        "provider_transport_retries": "BUILTIN_RUNTIME_DEFAULT",
        "underlying_request_count": "UNKNOWN",
        "automatic_scientific_retries": 0,
        "auto_compact_token_limit": 1000000000,
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
    require(
        not workspace.exists() or not any(workspace.iterdir()),
        "Semantic CWD must be empty",
    )
    filesystem = {
        ":root": "deny",
        ":minimal": "read",
        ":tmpdir": "deny",
        ":slash_tmp": "deny",
        ":workspace_roots": "deny",
    }
    settings = {
        "model_provider": "openai",
        "windows.sandbox": "mxc",
        "default_permissions": "semantic-worker",
        "permissions.semantic-worker.filesystem": filesystem,
        "permissions.semantic-worker.network.enabled": False,
        "web_search": "disabled",
        "project_doc_max_bytes": 0,
        "model_auto_compact_token_limit": 1000000000,
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


def preflight(argv: list[str]) -> dict[str, Any]:
    """Validate our closed generated settings, not live model compatibility.

    The installed 0.162.1 debug-model path does not validate exec configuration.
    Reserved built-in provider IDs cannot be overridden. This profile permits
    no custom provider tables at all and never edits the user's configuration.
    """
    parsed: dict[str, Any] = {}
    boolean = {
        "model_provider": str,
        "project_doc_max_bytes": int,
        "model_auto_compact_token_limit": int,
        "windows.sandbox": str,
        "default_permissions": str,
        "web_search": str,
        "model_reasoning_effort": str,
        "permissions.semantic-worker.filesystem": dict,
        "permissions.semantic-worker.network.enabled": bool,
        "suppress_unstable_features_warning": bool,
        "tools.view_image": bool,
    }
    features = {
        "skip_host_skill_discovery",
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
    }
    for index, argument in enumerate(argv):
        if argument != "-c":
            continue
        require(index + 1 < len(argv), "Missing configuration override")
        assignment = argv[index + 1]
        key = assignment.split("=", 1)[0]
        value = tomllib.loads(assignment)
        require(
            "model_providers" not in value,
            "Provider tables forbidden; built-in provider IDs are reserved",
        )
        expected = (
            bool
            if key.startswith("features.") and key[9:] in features
            else boolean.get(key)
        )
        require(expected is not None, "Unsupported generated configuration key: " + key)
        for part in key.split("."):
            require(
                isinstance(value, dict) and part in value,
                "Unsupported configuration shape",
            )
            value = value[part]
        require(type(value) is expected, "Unsupported configuration value type")
        require(
            key not in parsed or parsed[key] == value,
            "Conflicting configuration overrides",
        )
        parsed[key] = value
    return {
        "schema": "semantic-config-preflight-v1",
        "status": "PASS",
        "scope": "KNOWN_SHAPES_AND_RESERVED_PROVIDER_RULES; NOT_LIVE_COMPATIBILITY",
        "cli_version": "0.162.1",
        "overrides": parsed,
        "provider": "BUILTIN_OPENAI",
        "provider_transport_retries": "BUILTIN_RUNTIME_DEFAULT",
        "underlying_request_count": "UNKNOWN",
        "automatic_scientific_retries": 0,
    }


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
    transport_binding = config.get("transport_receipt")
    if transport_binding is not None:
        from experiments.orchestration.workers.capacity import (
            authenticate as authenticate_transport,
        )
        from experiments.orchestration.workers.capacity import authenticate_files

        require(
            config["model_id"] == "gpt-6-sol"
            and config["reasoning"] == "High"
            and config["runtime"] == configuration(),
            "Transport-only compatibility requires unchanged Sol/High treatment",
        )
        root = Path(__file__).resolve().parents[3]
        path = safe(root, transport_binding["path"])
        require(
            digest(binary(path)) == transport_binding["sha256"],
            "Transport receipt digest differs",
        )
        receipt = load(path)
        authenticate_transport(
            receipt,
            {**config, "model_id": "gpt-6-astra", "bounded_response": True},
        )
        authenticate_files(root, receipt)
        return
    capacity_binding = config.get("capacity_receipt")
    if capacity_binding is not None:
        from experiments.orchestration.workers.capacity import (
            authenticate as authenticate_capacity,
        )
        from experiments.orchestration.workers.capacity import authenticate_files

        require(
            isinstance(capacity_binding, dict)
            and set(capacity_binding) == {"path", "sha256"},
            "Capacity receipt binding required",
        )
        root = Path(__file__).resolve().parents[3]
        path = safe(root, capacity_binding["path"])
        require(
            digest(binary(path)) == capacity_binding["sha256"],
            "Capacity receipt digest differs",
        )
        authenticate_capacity(load(path), config)
        authenticate_files(root, load(path))
        return
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
