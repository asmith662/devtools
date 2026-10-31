# Copyright (c) 2026
# ruff: noqa: COM812, E501 -- operator messages and structured receipts
"""Conservative package ownership and static reverse-import test selection."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any


def module_name(path: str) -> str:
    """Map repository Python paths to import names."""
    return (
        path.removeprefix("src/")
        .removesuffix(".py")
        .replace("/", ".")
        .removesuffix(".__init__")
    )


def imports(path: str, text: str) -> tuple[set[str], bool]:
    """Extract static imports, retaining explicit dynamic/syntax uncertainty."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return set(), True
    names: set[str] = set()
    uncertain = False
    package = module_name(path).split(".")
    if not path.endswith("/__init__.py"):
        package.pop()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = (
                ".".join(package[: len(package) - node.level + 1]) if node.level else ""
            )
            prefix = ".".join(filter(None, (base, node.module)))
            names.add(prefix)
            names.update(f"{prefix}.{alias.name}" for alias in node.names)
        elif isinstance(node, ast.Call) and (
            (
                isinstance(node.func, ast.Name)
                and node.func.id in {"__import__", "eval", "exec"}
            )
            or (
                isinstance(node.func, ast.Attribute)
                and node.func.attr
                in {
                    "import_module",
                    "run_module",
                    "run_path",
                    "spec_from_file_location",
                }
            )
        ):
            uncertain = True
    return names, uncertain


def select(root: Path, changed: list[str]) -> dict[str, Any]:  # noqa: C901, PLR0912 -- finite conservative selection rules
    """Select whole owning packages plus transitive static consumers.

    This bounded developer heuristic is not exhaustive dependency proof. It
    deliberately avoids RI retrieval ranks and constructing repository indexes.
    """
    reasons: dict[str, list[str]] = {}
    uncertainty: list[str] = []
    files = {
        p.relative_to(root).as_posix(): p
        for base in ("src", "tests", "apps", "scripts")
        for p in (root / base).rglob("*.py")
        if "__pycache__" not in p.parts
        and not p.relative_to(root).as_posix().startswith("tests/experiments/")
    }

    def add(target: str, reason: str) -> None:
        if (root / target).exists():
            reasons.setdefault(target, []).append(reason)

    seeds = {module_name(p) for p in changed if p.endswith(".py")}
    graph = {p: imports(p, f.read_text(encoding="utf-8-sig")) for p, f in files.items()}
    affected = set(seeds)
    while True:
        consumers = {
            module_name(p)
            for p, (dependencies, _) in graph.items()
            if any(
                d == a or d.startswith(a + ".") or a.startswith(d + ".")
                for d in dependencies
                if d
                for a in affected
            )
        }
        if consumers <= affected:
            break
        affected.update(consumers)
    for path in changed:
        parts = Path(path).parts
        if path.endswith(("conftest.py", "__init__.py")) or not path.endswith(".py"):
            uncertainty.append(
                f"{path}: configuration/layout/fixture or non-Python input needs explicit review"
            )
        if path not in files:
            uncertainty.append(
                f"{path}: absent/deleted or outside analyzed Python scope"
            )
        if path.startswith("tests/") and path in files:
            add(path, f"changed test: {path}")
        elif path.startswith("src/devtools/") and len(parts) > 3:  # noqa: PLR2004 -- src/domain/package/file
            add(f"tests/{parts[2]}", f"owning production package: {path}")
        elif path.startswith(("apps/", "scripts/")) and len(parts) > 1:
            add(
                f"tests/{parts[0]}/{parts[1].removesuffix('.py')}",
                f"operational owner: {path}",
            )
            add(f"tests/{parts[0]}/test_{parts[1]}", f"operational module: {path}")
        if path.startswith(("src/devtools/agents/", "src/devtools/tools/")):
            for target in (
                "tests/agents",
                "tests/tools",
                "tests/apps/qwen",
                "tests/scripts/backlog",
            ):
                add(target, f"coding/Tool/Checkout integration contract: {path}")
    for path, (_, dynamic) in graph.items():
        if module_name(path) in affected:
            if path.startswith("tests/"):
                add(path, "static reverse-import consumer")
            if dynamic:
                uncertainty.append(f"{path}: dynamic execution/import requires review")
    if not reasons:
        uncertainty.append(
            "No owning tests established; provide explicit tests or choose comprehensive"
        )
    # Collapse children already covered by a selected directory.
    reasons = {
        p: why
        for p, why in reasons.items()
        if not any(p.startswith(q + "/") for q in reasons if q != p)
    }
    return {
        "changed": sorted(changed),
        "groups": reasons,
        "uncertainty": sorted(set(uncertainty)),
        "assurance": "bounded impact argument; omitted tests are not passed",
        "comprehensive_required_for_publication": True,
    }
