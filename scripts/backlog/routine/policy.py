# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, PLR2004 -- closed repository authority contract
"""Prospective routine-development limits, not a policy expression language."""

from __future__ import annotations

from typing import Any

from devtools.context import RepositoryResourceAddress

OPERATIONS = {
    "intake",
    "coding",
    "acceptance-review",
    "diagnostic-review",
    "host-review",
    "integration-plan",
    "git",
    "local",
}
EXCEPTIONS = {
    "architecture",
    "security",
    "destructive",
    "secrets",
    "paid",
    "service_change",
    "validation_relaxation",
}
CODING = {
    "model_calls": 8,
    "proposals": 3,
    "acquisitions": 6,
    "call_seconds": 120,
    "wall_seconds": 1200,
    "prompt_bytes": 131072,
    "source_bytes": 32768,
    "capture_bytes": 1048576,
}
REVIEW = {
    "model_calls": 8,
    "reads": 16,
    "call_seconds": 120,
    "wall_seconds": 600,
    "prompt_bytes": 262144,
    "response_bytes": 65536,
    "capture_bytes": 2097152,
}
PROTECTED = (
    "agents/",
    "models/",
    "tools/",
    "execution/",
    "governance/",
    "orchestration/",
    "persistence/",
    "resources/commands/",
)
LOCAL = {
    "model_calls": 32,
    "input_tokens": 65536,
    "output_tokens": 8192,
    "total_output_tokens": 131072,
    "reads": 64,
    "source_bytes": 131072,
    "checks": 32,
    "call_seconds": 180,
    "wall_seconds": 10800,
    "capture_bytes": 8388608,
    "delegations": 8,
    "prompt_bytes": 262144,
    "response_bytes": 65536,
}
ROLES = {"supervisor", "reviewer", "planner", "coding", "researcher"}
PURPOSES = {
    "calibration",
    "source-analysis",
    "role-evaluation",
    "working-memory",
    "prompt-playbook",
    "development",
}
LOCAL_TOOLS = {
    "read_source",
    "read_source_unit",
    "find_source",
    "submit_review_proposal",
}


def local_policy(value: dict[str, Any]) -> None:
    """Finite read-only evaluation/development scope, never native installation."""
    if not isinstance(value, dict) or set(value) != {
        "roles",
        "purposes",
        "read_roots",
        "tools",
        "budgets",
        "profiles",
    }:
        raise ValueError("Closed local-work policy required")
    for key, allowed in (
        ("roles", ROLES),
        ("purposes", PURPOSES),
        ("tools", LOCAL_TOOLS),
    ):
        values = value[key]
        if (
            not isinstance(values, list)
            or len(set(values)) != len(values)
            or not set(values) <= allowed
        ):
            raise PermissionError("Local role, purpose or Tool requires escalation")
    roots = value["read_roots"]
    profiles = value["profiles"]
    if (
        not isinstance(profiles, list)
        or not profiles
        or len(profiles) > 32
        or any(not isinstance(p, str) or not p.strip() for p in profiles)
        or len(set(profiles)) != len(profiles)
    ):
        raise ValueError("Bounded local profiles required")
    if not isinstance(roots, list) or not roots or len(roots) > 32:
        raise ValueError("Bounded local resource roots required")
    for root in roots:
        RepositoryResourceAddress(root + "probe")
        if not root.endswith("/") or not root.startswith(
            ("src/", "tests/", "docs/", "scripts/", "experiments/", ".local/"),
        ):
            raise PermissionError("Local resource root requires escalation")
    limits = value["budgets"]
    if (
        not isinstance(limits, dict)
        or set(limits) != set(LOCAL)
        or any(
            type(limits[k]) is not int or not 0 < limits[k] <= v
            for k, v in LOCAL.items()
        )
    ):
        raise ValueError("Finite local-work policy limits required")


def validate(value: dict[str, Any]) -> None:  # noqa: C901, PLR0912 -- closed policy schema
    """Keep policy activation explicit, finite and within existing owner ceilings."""
    if set(value) != {
        "schema",
        "categories",
        "edit_roots",
        "read_roots",
        "profiles",
        "provider",
        "coding",
        "review",
        "output_tokens",
        "grant_seconds",
        "operations",
        "git",
        "validation",
    } | (
        {"coding_attempts"}
        if value.get("schema")
        in {"routine-development-policy-v2", "routine-development-policy-v3"}
        else set()
    ) | (
        {"local"} if value.get("schema") == "routine-development-policy-v3" else set()
    ) or value["schema"] not in {
        "routine-development-policy-v1",
        "routine-development-policy-v2",
        "routine-development-policy-v3",
    }:
        raise ValueError("Closed routine policy required")
    if value["schema"] != "routine-development-policy-v1" and (
        type(value["coding_attempts"]) is not int
        or not 1 <= value["coding_attempts"] <= 100
    ):
        raise ValueError("Finite total coding-attempt ceiling required")
    if value["schema"] == "routine-development-policy-v3":
        local_policy(value["local"])
    elif "local" in value["operations"]:
        raise PermissionError("Local work requires the explicit v3 amendment")
    if value["validation"] != "protected-development-100-percent-v1" or value[
        "git"
    ] != {"remote": "origin", "branches": ["main"], "force": False}:
        raise PermissionError(
            "Existing protected validation and non-force Git rules required",
        )
    for key in ("categories", "edit_roots", "read_roots", "profiles", "operations"):
        items = value[key]
        if (
            not isinstance(items, list)
            or not items
            or len(items) > 100
            or any(not isinstance(s, str) or not s.strip() for s in items)
            or len(set(items)) != len(items)
        ):
            raise ValueError("Distinct nonempty bounded policy lists required")
    if (
        not set(value["categories"]) <= {"bug", "refactor", "enhancement"}
        or not set(value["operations"]) <= OPERATIONS
    ):
        raise PermissionError("Operation or category requires escalation")
    for key in ("edit_roots", "read_roots"):
        for root in value[key]:
            RepositoryResourceAddress(root + "probe.py")
            if not root.endswith("/") or not root.startswith(
                ("src/devtools/", "tests/"),
            ):
                raise PermissionError("Repository Python roots required")
    for root in value["edit_roots"]:
        if not root.startswith("src/devtools/") or any(
            root.startswith("src/devtools/" + p) for p in PROTECTED
        ):
            raise PermissionError(
                "Authority, execution and provider owners require escalation",
            )
    for name, ceilings in (("coding", CODING), ("review", REVIEW)):
        requested = value[name]
        if (
            not isinstance(requested, dict)
            or set(requested) != set(ceilings)
            or any(
                type(requested[k]) is not int or not 0 < requested[k] <= maximum
                for k, maximum in ceilings.items()
            )
        ):
            raise ValueError("Finite routine resource limits required")
    if (
        type(value["grant_seconds"]) is not int
        or not 1
        <= value["grant_seconds"]
        <= (10800 if value["schema"].endswith("v3") else 3600)
        or type(value["output_tokens"]) is not int
        or not 1 <= value["output_tokens"] <= 8192
    ):
        raise ValueError("Finite grant lifetime and output allowance required")
    p = value["provider"]
    if (
        not isinstance(p, dict)
        or set(p) != {"endpoint", "model", "image", "artifact_sha256", "context_tokens"}
        or p["endpoint"] != "http://127.0.0.1:8080"
        or not isinstance(p["model"], str)
        or not p["model"]
        or any(
            not isinstance(p[k], str)
            or len(p[k]) != 64
            or any(c not in "0123456789abcdef" for c in p[k])
            for k in ("image", "artifact_sha256")
        )
        or type(p["context_tokens"]) is not int
        or not 1 <= p["context_tokens"] <= 65536
    ):
        raise ValueError("Exact pinned local provider identity required")


def qualification(value: dict[str, Any]) -> None:
    """Require a trusted supervisor assessment, never infer safety from task labels."""
    if (
        set(value) != EXCEPTIONS | {"reference"}
        or not isinstance(value["reference"], str)
        or not value["reference"].strip()
        or any(value[k] is not False for k in EXCEPTIONS)
    ):
        raise PermissionError(
            "Exceptional or unassessed work requires human escalation",
        )


def permits_source(policy: dict[str, Any], path: str) -> bool:
    """Apply immutable exceptional-owner exclusions even under a broad root."""
    RepositoryResourceAddress(path)
    return path.startswith(tuple(policy["edit_roots"])) and not path.startswith(
        tuple("src/devtools/" + p for p in PROTECTED),
    )
