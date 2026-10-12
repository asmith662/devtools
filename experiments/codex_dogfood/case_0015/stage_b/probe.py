# Copyright (c) 2026
# ruff: noqa: T201 -- synthetic launcher probe
"""Synthetic-only stable-record launcher probe, never prospective resources."""

from __future__ import annotations

import sys
from pathlib import Path

from experiments.bm25f.test_scoring import fixture
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal
from experiments.codex_dogfood.case_0015.stage_b.records import PreparedFrame


def main() -> None:
    """Write a tiny synthetic return or replay it in another process."""
    root = Path(sys.argv[2]).resolve()
    if sys.argv[1] == "write":
        state = fixture(("synthetic.txt", "synthetic"))
        journal = Journal.start(root, {"execution": "synthetic-launcher-probe"})
        journal.call(
            "frame",
            {},
            lambda: PreparedFrame(state.collection, state.snapshot),
        )
        journal.complete()
    elif sys.argv[1] == "read":
        journal = Journal.load(root)
        journal.ready()
        value = journal.state["values"]["frame"]
        if type(value).__module__ != PreparedFrame.__module__:
            raise ValueError("Foreign durable record")  # noqa: EM101, TRY003
    else:
        raise ValueError("Synthetic probe mode")  # noqa: EM101, TRY003
    print("SYNTHETIC STABLE RECORD PASS")


if __name__ == "__main__":
    main()
