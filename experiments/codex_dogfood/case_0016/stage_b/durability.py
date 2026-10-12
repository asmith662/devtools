# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, ANN401
"""Capture-only adapter: immutable journal owns state; no active checkpoint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.case_0012.stage_b.durability import (
    Journal as NativeJournal,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


class Journal(NativeJournal):
    """Reuse unchanged immutable event/memo schema, disabling convenience writes."""

    def save(self) -> None:
        """Publish nothing during active execution; final state is reconstructed.

        Inherited start/context/call/complete hooks reach this no-op. No mutable
        latest file or required post-return derived writer exists.
        """

    @classmethod
    def start(cls, root: Path, marker: dict[str, Any]) -> Journal:
        """Retain the exclusive claim and native exactly-once schema unchanged."""
        return cast("Journal", super().start(root, marker))

    @classmethod
    def load(cls, root: Path) -> Journal:
        """Read old/new immutable journals; loaded instances cannot invoke."""
        return cast("Journal", super().load(root))

    def call(self, identity: str, inputs: object, invoke: Callable[[], Any]) -> Any:
        """Block advancement after native or authoritative return failure."""
        if self.pickler is None or any(
            o["identity"] == identity for o in self.state["operations"]
        ):
            return super().call(identity, inputs, invoke)
        if self.state["active"]:
            raise ValueError("Unreturned scientific boundary; STOP/no retry")
        return super().call(identity, inputs, invoke)


def checkpoint_bytes(journal: NativeJournal) -> bytes:
    """Pure reconstruction; publish once after successful capture if desired."""
    return json_bytes(
        {
            "schema": "case-0012-derived-journal-summary-v2",
            "execution": journal.state["marker"]["execution"],
            "state": journal.state["state"],
            "operations": journal.state["operations"],
            "active": journal.state["active"],
            "journal_events": journal.events,
            "journal_chain_sha256": journal.chain,
        },
    )
