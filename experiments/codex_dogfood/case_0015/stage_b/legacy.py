# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- explicit immutable failed-audit boundary
"""Narrow read-only compatibility solely for the failed attempt-1 launcher types."""

from __future__ import annotations

import sys
from dataclasses import make_dataclass
from typing import TYPE_CHECKING, Any

from experiments.codex_dogfood.case_0009.artifacts import binary, digest, read_json
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal

if TYPE_CHECKING:
    from pathlib import Path

HASH = "fefc01dbaefbcbe47d1e2d8edb02bb0ab76c7a18487c0828e8d02d264c86513a"


def authenticate_failed(root: Path) -> Journal:
    """Validate pinned immutable bytes, then load without invoking any operation."""
    root = root.resolve()
    if root.name != "case-0015-stage-b-1":
        raise ValueError("Legacy bindings are forbidden for other attempts")
    if digest(binary(root / "failed_audit_hashes.json")) != HASH:
        raise ValueError("Failed audit manifest tamper")
    for name, expected in read_json(root / "failed_audit_hashes.json")[
        "sha256"
    ].items():
        if digest(binary(root / name)) != expected:
            raise ValueError("Immutable failed audit tamper: " + name)
    main = sys.modules["__main__"]
    missing = object()
    old = {
        name: getattr(main, name, missing)
        for name in ("PreparedFrame", "PreparedFields")
    }
    try:
        for name, fields in (
            ("PreparedFrame", ("documents", "snapshot")),
            ("PreparedFields", ("content", "filename")),
        ):
            record = make_dataclass(
                name,
                [(f, Any) for f in fields],
                frozen=True,
                slots=True,
                namespace={"__module__": "__main__"},
            )
            record.__module__ = "__main__"
            setattr(main, name, record)
        journal = Journal.load(root)
    finally:
        for name, value in old.items():
            if value is missing:
                delattr(main, name)
            else:
                setattr(main, name, value)
    operations = journal.state["operations"]
    if [(o["identity"], o["status"], o["invocations"]) for o in operations] != [
        ("frame:prepare", "RETURNED", 1),
        ("fields:prepare", "RETURNED", 1),
        ("index:native-prepare", "FAILED_NO_RETURN", 1),
    ] or (root / "execution_completed.json").exists():
        raise ValueError("Failed audit operation boundary differs")
    if set(journal.state["values"]) != {"frame:prepare", "fields:prepare"}:
        raise ValueError("Unexpected failed-attempt scientific return")
    return journal
