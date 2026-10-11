# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, EM101, TRY003 -- frozen JSON rehydration boundary
"""Restore frozen task-only bases and explicit native preparation universes."""

from __future__ import annotations

from typing import Any

from devtools.context.localization.identity import (
    LocalizationAnchorIdentity,
    LocalizationObligationIdentity,
)
from devtools.context.python.modules.interpretation import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from experiments.codex_dogfood.acquisition.needs import InformationNeed
from experiments.codex_dogfood.case_0012.stage_b.execute import provenance
from experiments.codex_dogfood.case_0013 import protocol
from experiments.exact_hint_routing.extraction import extract
from experiments.exact_hint_routing.models import (
    ExactHintObservation,
    HintAssociation,
    HintCategory,
)
from experiments.exact_hint_routing.routing import ExactFrame
from experiments.exact_hint_routing.serialization import project
from experiments.mechanism_routing.policy import Arm, RoutingBasis, decisions


def snapshot(image: dict[str, Any]) -> RepositorySnapshot:
    """Restore only sealed retained resources, without filesystem reacquisition."""
    m = image["metadata"]
    return RepositorySnapshot(
        RepositorySnapshotId(m["snapshot_id"]),
        RepositoryId.parse(m["repository_id"]),
        tuple(
            RepositoryResourceOccurrence(
                RepositoryResourceAddress(r["address"]),
                ContentIdentity(r["content_identity"]),
                r["text"],
                r["encoding"],
                r["byte_size"],
            )
            for r in image["resources"]
        ),
    )


def modules(s: RepositorySnapshot, metadata: dict[str, Any]) -> Any:
    """Interpret only sealed address/root selections; no declaration parsing."""
    interpretations: list[Any] = []
    for root in dict.fromkeys(m["root"] for m in metadata["module_universe"]):
        selected = tuple(
            RepositoryResourceAddress(m["address"])
            for m in metadata["module_universe"]
            if m["root"] == root
        )
        interpretations.extend(
            interpret_python_module_resources(
                s, module_root=PythonModuleRoot(root), resource_addresses=selected
            ).interpretations
        )
    universe = define_python_module_interpretation_universe(
        repository_id=s.repository_id, interpretations=interpretations
    )
    if universe.identity != metadata["module_universe_identity"]:
        raise ValueError("Native module universe differs")
    return universe


def assemble(
    s: RepositorySnapshot,
    universe: Any,
    addresses: tuple[RepositoryResourceAddress, ...],
    metadata: dict[str, Any],
) -> ExactFrame:
    """Validate explicit native frame and declaration address universe."""
    frame = ExactFrame(s.repository_id, s.id, s, universe, addresses)
    frame.validate()
    if frame.identity != metadata["frame_identity"]:
        raise ValueError("Native exact frame differs")
    return frame


def purposes(t: dict[str, Any]) -> tuple[RoutingBasis, ...]:
    """Rehydrate exact caller-authored meanings; verify extraction without lookup."""
    bases = []
    for item in t["acquisition_intents"]:
        n = item["need"]
        obligation = LocalizationObligationIdentity(
            protocol.TASK_ID, n["obligation"]["value"]
        )
        need = InformationNeed(
            n["key"],
            obligation,
            n["statement"],
            n["reason"],
            provenance(n["provenance"]),
            tuple(
                LocalizationAnchorIdentity(protocol.TASK_ID, a["value"])
                for a in n["anchors"]
            ),
        )
        h, a = item["hint"], item["association"]
        hint = None
        if h is not None:
            span = provenance(h["provenance"]).span
            if span is None:
                raise ValueError("Missing frozen hint span")
            hint = ExactHintObservation(
                protocol.TASK_ID,
                h["text"],
                span,
                h["rule"],
                h["syntactic_form"],
                HintCategory(h["category"]),
                provenance(h["provenance"]),
            )
        association = None
        if a is not None:
            if hint is None:
                raise ValueError("Association without frozen hint")
            association = HintAssociation(
                hint.identity, obligation, a["reason"], provenance(a["provenance"])
            )
        b = RoutingBasis(need, hint, association, provenance(item["provenance"]))
        if {"identity": b.need.identity, "role": b.role.value, **project(b)} != item:
            raise ValueError("Frozen routing purpose differs")
        bases.append(b)
    observed = tuple(
        d.observation
        for d in extract(protocol.TASK_ID, t["task_text"])
        if d.observation is not None
    )
    if {(h.identity, h.category) for h in observed} != {
        (b.hint.identity, b.hint.category) for b in bases if b.hint is not None
    }:
        raise ValueError("Frozen extraction differs")
    return tuple(bases)


def policy(arm: Arm, bases: tuple[RoutingBasis, ...], t: dict[str, Any]) -> Any:
    """Time each arm's policy independently and reject any post-outcome drift."""
    ds = decisions(arm, bases)
    if [{"identity": d.identity, **project(d)} for d in ds] != t["route_decisions"][
        arm.name
    ]:
        raise ValueError("Frozen arm policy mismatch")
    return ds
