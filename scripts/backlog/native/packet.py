# Copyright (c) 2026
# ruff: noqa: PLR2004, EM101, TRY003 -- finite operational receipts and formatter compatibility
"""One-file prospective native packet, separate from the Qwen CodingTask wire."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from devtools.agents.coding.protocol import CHECK, EDIT, READ
from devtools.agents.model_tools import normalize_tool_descriptor
from devtools.context import RepositoryResourceAddress
from devtools.evaluation.preflight import OracleComparison, check_oracle_expectations
from devtools.models.interaction import InteractionSource, ModelSettings
from scripts.backlog.intake import _digest


@dataclass(frozen=True, slots=True)
class NativeTask:
    """Integration's bounded source/check view of a native packet, not CodingTask."""

    source: str
    tests: tuple[str, ...]
    oracle: str

    @property
    def oracle_sha256(self) -> str:
        """Retain the existing integration oracle identity convention."""
        import hashlib  # noqa: PLC0415

        return hashlib.sha256(self.oracle.encode()).hexdigest()


def task_view(task: dict[str, Any]) -> NativeTask:
    """Read only the prospective native source/check contract."""
    validate(task)
    return NativeTask(task["source"], tuple(task["tests"]), task["oracle"])


def validate(task: dict[str, Any]) -> None:  # noqa: C901, PLR0912
    """Refuse unsupported scope, missing provenance and unbounded worker policy."""
    if set(task) != {
        "objective",
        "source",
        "read_paths",
        "tests",
        "oracle",
        "obligations",
        "preflight",
        "worker",
        "settings",
        "budgets",
        "capture",
    }:
        raise ValueError("Exact native task fields required")
    if (
        not task["objective"].strip()
        or not task["oracle"].strip()
        or task["capture"] != "bounded-full-v1"
    ):
        raise ValueError("Objective, withheld acceptance and explicit capture required")
    source = task["source"]
    if not source.startswith("src/devtools/") or not source.endswith(".py"):
        raise PermissionError("Native v1 repairs one existing framework Python file")
    if not all(
        part.isidentifier()
        for part in source.removeprefix("src/").removesuffix(".py").split("/")
    ):
        raise PermissionError(
            "Native acceptance requires an importable Python module address",
        )
    for key in ("read_paths", "tests"):
        paths = task[key]
        if (
            not isinstance(paths, list)
            or len(paths) > 16
            or len(set(paths)) != len(paths)
        ):
            raise ValueError("Distinct bounded paths required")
        for path in paths:
            RepositoryResourceAddress(path)
            if (
                not path.endswith(".py")
                or not path.startswith(("src/devtools/", "tests/"))
                or path.startswith("tests/experiments/")
            ):
                raise PermissionError("Unsupported native read/check path")
    RepositoryResourceAddress(source)
    if not task["tests"] or any(not p.startswith("tests/") for p in task["tests"]):
        raise ValueError("Public tests are required")
    worker = task["worker"]
    if set(worker) != {"actor", "source", "profile"} or any(
        not isinstance(v, str) or not v.strip() for v in worker.values()
    ):
        raise ValueError("Exact worker actor/source/profile required")
    InteractionSource(worker["source"])
    settings = ModelSettings(**task["settings"])
    if settings.maximum_output_tokens is None or settings.maximum_output_tokens > 8192:
        raise ValueError("A finite worker output limit is required")
    ceilings = {
        "model_calls": 8,
        "proposals": 3,
        "acquisitions": 6,
        "call_seconds": 120,
        "wall_seconds": 1200,
        "prompt_bytes": 32768,
        "source_bytes": 32768,
        "capture_bytes": 1048576,
    }
    if set(task["budgets"]) != set(ceilings) or any(
        type(task["budgets"][k]) is not int or not 1 <= task["budgets"][k] <= n
        for k, n in ceilings.items()
    ):
        raise ValueError("Native budgets exceed the supported finite profile")
    if task["budgets"]["call_seconds"] > task["budgets"]["wall_seconds"]:
        raise ValueError("Native call timeout exceeds the process budget")
    if (
        not isinstance(task["obligations"], list)
        or not 1 <= len(task["obligations"]) <= 16
    ):
        raise ValueError("Caller-authored information obligations required")
    names = []
    for obligation in task["obligations"]:
        if (
            set(obligation) != {"name", "predicate", "path", "criterion"}
            or not obligation["name"].strip()
            or not obligation["predicate"].strip()
            or obligation["criterion"] != "current-whole-resource-v1"
        ):
            raise ValueError(
                "Native v1 supports explicit current whole-source information criteria",
            )
        if obligation["path"] not in {source, *task["read_paths"], *task["tests"]}:
            raise PermissionError("Obligation target outside read scope")
        names.append(obligation["name"])
    if len(set(names)) != len(names):
        raise ValueError("Duplicate obligation identities")
    preflight = task["preflight"]
    if (
        set(preflight) != {"reference", "comparisons", "controls_reference"}
        or not preflight["reference"].strip()
        or not preflight["controls_reference"].strip()
    ):
        raise ValueError("Independent preflight/control provenance required")
    issues = check_oracle_expectations(
        obligations=tuple(names),
        comparisons=tuple(OracleComparison(**r) for r in preflight["comparisons"]),
    )
    if issues:
        msg = f"Acceptance preflight incomplete: {issues}"
        raise ValueError(msg)
    if len(str(task).encode()) > 131072:
        raise ValueError("Native task packet exceeds its bound")


def fingerprint(task: dict[str, Any]) -> str:
    """Bind the exact prospective task; never use the Qwen definition digest."""
    validate(task)
    return _digest(task)


def tool_definitions() -> list[dict[str, Any]]:
    """Freeze the actual finite native schema, not a model-selected Tool registry."""
    return [asdict(normalize_tool_descriptor(d)) for d in (READ, EDIT, CHECK)]
