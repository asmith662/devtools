# Copyright (c) 2026
# ruff: noqa: D103, S101, PLR2004, COM812
"""Synthetic prospective-amendment proofs; no Case 0016 graph or retrieval."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath
from experiments.task_conditioned_graph.diagnostic import definitions
from experiments.task_conditioned_graph.ranking import (
    RankedResource,
    Ranking,
    fuse,
    rank,
)
from experiments.task_conditioned_graph.view import build_reference_view
from tests.context.retrieval.test_composition import _lexical
from tests.context.retrieval.test_structural import _facts


def _fixture(tmp_path: Path, texts: dict[str, str]) -> Ranking:
    for name, text in texts.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000016")
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(n) for n in texts),
        maximum_resource_bytes=4096,
    )
    interpreted = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=tuple(r.address for r in snapshot.resources),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpreted.interpretations,
    )
    refs = tuple(
        f
        for r in snapshot.resources
        for f in derive_python_declaration_references(
            snapshot, resource_address=r.address, module_universe=universe
        ).references
    )
    return rank(
        snapshot,
        build_reference_view(snapshot, refs),
        _lexical(tmp_path, snapshot, query_text="signal"),
    )


def test_seeded_and_referenced_positive_flow_not_stationary_score(
    tmp_path: Path,
) -> None:
    snapshot, _, refs, _ = _facts(tmp_path)
    view = build_reference_view(snapshot, refs)
    lexical = _lexical(tmp_path, snapshot, query_text="value")
    target = snapshot.resource_at(RepositoryResourceAddress("pkg/target.py"))
    result = rank(snapshot, view, lexical, (target,))
    state = next(s for s in result.states if s.address == target.address)
    assert state.seed
    assert state.direct_restart_mass > 0
    assert state.dangling_return_mass > 0
    assert state.incoming_structural_flow > 0
    assert result.resources[0].score == state.incoming_structural_flow
    assert result.resources[0].score < state.stationary_mass


def test_seed_only_or_total_stationary_ranking_cannot_fuse(tmp_path: Path) -> None:
    snapshot, _, refs, _ = _facts(tmp_path)
    result = rank(
        snapshot,
        build_reference_view(snapshot, refs),
        _lexical(tmp_path, snapshot, query_text="value"),
    )
    seed = next(s for s in result.states if s.seed)
    invented = RankedResource(seed.address, 1, seed.stationary_mass, seed=True)
    with pytest.raises(ValueError, match="seed-only or stationary"):
        fuse(replace(result, resources=(invented,)))
    target = result.resources[0]
    state = next(s for s in result.states if s.address == target.address)
    with pytest.raises(ValueError, match="seed-only or stationary"):
        fuse(
            replace(
                result, resources=(replace(target, score=state.stationary_mass + 0.1),)
            )
        )
    with pytest.raises(ValueError, match="provenance"):
        fuse(
            replace(
                result,
                states=tuple(
                    replace(s, incoming_structural_flow=99)
                    if s.address == target.address
                    else s
                    for s in result.states
                ),
            )
        )


def test_self_reference_seed_has_structural_flow(tmp_path: Path) -> None:
    result = _fixture(tmp_path, {"seed.py": "# signal\ndef f():\n    pass\nf()\n"})
    state = result.states[0]
    assert state.seed
    assert state.stationary_mass == pytest.approx(1)
    assert state.incoming_structural_flow == pytest.approx(0.85)
    assert result.resources[0].score == pytest.approx(0.85)
    projected = definitions(result)
    assert sum(flow for _, flow in projected[0].reference_flows) == pytest.approx(
        state.incoming_structural_flow
    )
    assert state.incoming_structural_flow == sum(flow for _, flow in state.incoming)


def test_map_orders_definition_flow_before_parent_resource_rank(tmp_path: Path) -> None:
    result = _fixture(
        tmp_path,
        {
            "source.py": (
                "# signal\nfrom left import a,b,c\nfrom right import d\n"
                "a()\nb()\nc()\nd()\nd()\n"
            ),
            "left.py": "def a(): pass\ndef b(): pass\ndef c(): pass\n",
            "right.py": "def d(): pass\n",
        },
    )
    projected = definitions(result)
    assert str(result.resources[0].address) == "left.py"
    assert projected[0].address == "right.py"
    assert projected[0].parent_rank == 2
    assert projected == tuple(
        sorted(projected, key=lambda p: (-p.incoming_flow, p.parent_rank, p.definition))
    )


def test_equal_propagated_scores_use_canonical_address_ties(tmp_path: Path) -> None:
    result = _fixture(
        tmp_path,
        {
            "source.py": "# signal\nfrom z import f\nfrom a import g\nf()\ng()\n",
            "z.py": "def f(): pass\n",
            "a.py": "def g(): pass\n",
        },
    )
    assert result.resources[0].score == result.resources[1].score
    assert [str(r.address) for r in result.resources] == ["a.py", "z.py"]
