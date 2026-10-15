# Copyright (c) 2026
# ruff: noqa: ANN401, PLC0415, PLR2004 -- frozen experiment orchestration metadata
"""Immutable approved plan and bounded case/stage transport models."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require, safe

SCHEMA = "experiment-controller-plan-v2"
LEGACY_SCHEMA = "approved-experiment-controller-v1"
STAGES = ("prepare", "packet", "B", "C", "import", "D")
BOUNDARIES = ("PACKET", "B", "C", "D")


class StageState(StrEnum):
    """Represent scheduler status, distinct from scientific outcomes."""

    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    DEAD = "DEAD"
    QUARANTINED = "QUARANTINED"


@dataclass(frozen=True)
class CasePlan:
    """Bind one case's immutable frame and explicitly disclosed Stage A files."""

    identity: str
    frame_json: str
    inputs_json: str

    @property
    def frame(self) -> dict[str, Any]:
        """Return a copy of the exact owning frame."""
        import json

        return dict(json.loads(self.frame_json))


@dataclass(frozen=True)
class RunPlan:
    """Store canonical immutable metadata; no mutable scientific semantics."""

    canonical: bytes

    @classmethod
    def parse(cls, value: Any) -> RunPlan:
        """Reject unsupported stages, retry policy and ambiguous authority."""
        require(
            set(value)
            == {
                "schema",
                "name",
                "attempt",
                "stage_a",
                "cases",
                "commands",
                "semantic",
                "publication",
                "validation",
                "concurrency",
                "timeouts",
                "retry",
                "implementation",
                "controller_implementation",
                "cache",
            }
            | ({"approval"} if value.get("schema") == LEGACY_SCHEMA else set())
            | ({"adopted_branches"} if "adopted_branches" in value else set()),
            "Run-plan field contract",
        )
        require(
            value["schema"] in {SCHEMA, LEGACY_SCHEMA}
            and value["retry"] == "NEVER_SCIENTIFIC",
            "Unsupported plan/retry policy",
        )
        require(
            type(value["attempt"]) is int and value["attempt"] > 0,
            "Explicit positive attempt required",
        )
        stage_a = value["stage_a"]
        require(
            set(stage_a) == {"checkpoint", "protocol", "integrity"}
            and isinstance(stage_a["checkpoint"], str)
            and re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", stage_a["checkpoint"]),
            "Stage A requires a full immutable Git object identity",
        )
        if value["schema"] == LEGACY_SCHEMA:
            safe(Path.cwd(), value["approval"])
        for name in ("protocol", "integrity"):
            artifact = stage_a[name]
            require(
                set(artifact) == {"path", "sha256"}
                and isinstance(artifact["sha256"], str)
                and re.fullmatch(r"[0-9a-f]{64}", artifact["sha256"]),
                "Stage A artifact contract",
            )
            safe(Path.cwd(), artifact["path"])
        require(
            set(value["commands"])
            == {
                "prepare",
                "prepare_validate",
                "packet",
                "packet_validate",
                "B",
                "B_validate",
                "C_validate",
                "import",
                "import_validate",
                "D",
                "D_validate",
            },
            "Fixed experiment stages required",
        )
        require(
            len(value["cases"]) > 0
            and len({c["id"] for c in value["cases"]}) == len(value["cases"]),
            "Unique ordered cases required",
        )
        adopted = value.get("adopted_branches", {})
        require(
            isinstance(adopted, dict)
            and (not adopted or value["schema"] == SCHEMA)
            and set(adopted) <= {c["id"] for c in value["cases"]},
            "Prospective adoption case contract",
        )
        for binding in adopted.values():
            require(
                set(binding) == {"path", "sha256", "compatibility_sha256"}
                and all(
                    isinstance(binding[k], str)
                    and re.fullmatch(r"[0-9a-f]{64}", binding[k])
                    for k in ("sha256", "compatibility_sha256")
                ),
                "Exact adoption seal and compatibility digests required",
            )
            safe(Path.cwd(), binding["path"])
        for case in value["cases"]:
            require(
                set(case) == {"id", "frame", "inputs"}
                and set(case["frame"])
                >= {"repository_id", "snapshot_id", "corpus_id", "parent_tree"},
                "Case/frame contract",
            )
            safe(Path.cwd(), case["id"])
            require("/" not in case["id"], "Case identity is one path component")
            require(
                case["inputs"]
                and all(
                    set(item) == {"path", "name", "sha256"}
                    and len(item["sha256"]) == 64
                    for item in case["inputs"]
                ),
                "Explicit case disclosure hashes required",
            )
            require(
                len({item["name"] for item in case["inputs"]}) == len(case["inputs"]),
                "Duplicate disclosed input",
            )
            for item in case["inputs"]:
                safe(Path.cwd(), item["path"])
                safe(Path.cwd(), item["name"])
        require(
            set(value["concurrency"]) == {"cases", "workers", "semantic"}
            and all(type(n) is int and n > 0 for n in value["concurrency"].values()),
            "Bounded concurrency required",
        )
        require(
            all(
                type(n) in (int, float) and n > 0 and isfinite(n)
                for n in value["timeouts"].values()
            )
            and set(value["timeouts"]) == {"worker", "validation", "grace"},
            "Timeout contract",
        )
        require(
            set(value["publication"])
            == {"root", "remote", "branch", "subjects", "push"}
            and set(value["publication"]["subjects"]) == set(BOUNDARIES),
            "Publication boundaries required",
        )
        require(
            value["publication"]["branch"] == "main",
            "Controller publication requires main",
        )
        require(
            value["publication"]["root"].startswith("experiments/"),
            "Experiment publication ownership required",
        )
        safe(Path.cwd(), value["publication"]["root"])
        require(
            type(value["publication"]["push"]) is bool
            and isinstance(value["publication"]["remote"], str)
            and re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._-]*",
                value["publication"]["remote"],
            ),
            "Publication push/remote contract",
        )
        require(
            all(
                isinstance(command, list)
                and command
                and all(isinstance(a, str) for a in command)
                for command in value["commands"].values()
            ),
            "Direct frozen argv required",
        )
        require(
            value["semantic"]["kind"] in {"codex", "process"},
            "Unsupported semantic launcher",
        )
        require(
            all(
                isinstance(value["semantic"][key], str) and value["semantic"][key]
                for key in ("model", "reasoning", "prompt_file")
            ),
            "Frozen semantic configuration required",
        )
        safe(Path.cwd(), value["semantic"]["prompt_file"])
        environment = value["semantic"]["environment_allowlist"]
        require(
            isinstance(environment, list)
            and all(
                isinstance(name, str)
                and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name)
                and name not in {"PYTHONPATH", "PYTHONSTARTUP", "CODEX_HOME"}
                for name in environment
            ),
            "Environment allowlist contract",
        )
        if value["semantic"]["kind"] == "codex":
            require(
                isinstance(value["semantic"].get("model_id"), str)
                and value["semantic"]["model_id"]
                and value["semantic"].get("cli_version") == "0.162.1",
                "Frozen account model ID and supported Codex CLI version required",
            )
        else:
            command = value["semantic"].get("argv")
            require(
                isinstance(command, list)
                and command
                and isinstance(command[0], str)
                and command[0]
                and all(isinstance(arg, str) and "\0" not in arg for arg in command),
                "Semantic process requires direct frozen argv",
            )
        require(
            set(value["validation"]) == {"local", "checkpoint", "final"}
            and all(
                isinstance(commands, list)
                and commands
                and all(
                    isinstance(argv, list)
                    and argv
                    and isinstance(argv[0], str)
                    and argv[0]
                    and all(isinstance(arg, str) and "\0" not in arg for arg in argv)
                    for argv in commands
                )
                for commands in value["validation"].values()
            ),
            "Explicit validation tiers required",
        )
        require(value["implementation"], "Pinned adapter implementation required")
        for address, sha in value["implementation"].items():
            safe(Path.cwd(), address)
            require(
                isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha),
                "Implementation digest contract",
            )
        cache = value["cache"]
        require(
            set(cache)
            == {"enabled", "observation_semantics", "configuration", "surfaces"}
            and type(cache["enabled"]) is bool
            and isinstance(cache["configuration"], dict)
            and isinstance(cache["observation_semantics"], str)
            and cache["observation_semantics"]
            and isinstance(cache["surfaces"], list)
            and (cache["surfaces"] or not cache["enabled"]),
            "Cache plan contract",
        )
        for surface in cache["surfaces"]:
            safe(Path.cwd(), surface)
        require(
            value["controller_implementation"],
            "Approved controller implementation required",
        )
        return cls(json_bytes(value))

    @property
    def value(self) -> dict[str, Any]:
        """Return decoded copies so callers cannot mutate the frozen plan."""
        import json

        return dict(json.loads(self.canonical))

    @property
    def cases(self) -> tuple[CasePlan, ...]:
        """Retain prospective case order."""
        return tuple(
            CasePlan(
                c["id"],
                json_bytes(c["frame"]).decode(),
                json_bytes(c["inputs"]).decode(),
            )
            for c in self.value["cases"]
        )

    def identity(self, controller_sha256: dict[str, str]) -> str:
        """Derive run identity from inputs/configuration/code, never timestamps."""
        return digest(
            json_bytes(
                {"plan": self.value, "controller_implementation": controller_sha256},
            ),
        )


def validation_tier(boundary: str, changed_paths: tuple[str, ...]) -> str:
    """Require final full validation for final result or production changes."""
    return (
        "final"
        if boundary == "D" or any(p.startswith("src/devtools/") for p in changed_paths)
        else "local"
        if boundary == "LOCAL"
        else "checkpoint"
    )
