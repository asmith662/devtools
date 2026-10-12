# Copyright (c) 2026
# ruff: noqa: D103, S101, PLR2004, COM812
"""Controlled synthetic graph/PPR/RRF/diagnostic fixtures, never Case 0016."""

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
from devtools.context.retrieval.graph.pagerank import GraphRankingSettings
from devtools.context.retrieval.graph.walk import stationary_distribution
from devtools.core.paths import ResolvedPath
from experiments.task_conditioned_graph.diagnostic import (
    definitions,
    render_map,
    validate_definitions,
)
from experiments.task_conditioned_graph.evidence import (
    graph_evidence,
    validate_evidence,
)
from experiments.task_conditioned_graph.ranking import fuse, rank, seed_union
from experiments.task_conditioned_graph.seeds import resolve_exact_seeds
from experiments.task_conditioned_graph.view import build_reference_view, require_view
from tests.context.retrieval.test_composition import _lexical
from tests.context.retrieval.test_structural import _facts


def test_native_reference_projection_count_sqrt_provenance(tmp_path: Path) -> None:
    snapshot, _, refs, _ = _facts(tmp_path)
    view = build_reference_view(snapshot, (*refs, refs[0]))
    assert len(view.edges) == 1
    edge = view.edges[0]
    assert str(edge.source) == "consumer.py"
    assert str(edge.target) == "pkg/target.py"
    assert edge.weight == pytest.approx(3**0.5)
    assert edge.probability == 1
    assert set(edge.references) == set(refs)
    assert all(
        r.target_resource == snapshot.resource_at(edge.target) for r in edge.references
    )
    assert all(r.occurrence.resource_address == edge.source for r in edge.references)
    assert all(
        r.target_subject == r.target_declaration.subject for r in edge.references
    )
    assert view == build_reference_view(snapshot, tuple(reversed(refs)))
    assert tuple(map(str, view.nodes)) == tuple(sorted(map(str, view.nodes)))


def test_unresolved_no_guessed_edge_self_reference_and_degree(tmp_path: Path) -> None:
    texts = {
        "left.py": "def f():\n    pass\n",
        "right.py": "def g():\n    pass\n",
        "source.py": (
            "from left import f\nfrom right import g\n"
            "f()\nf()\nf()\nf()\ng()\nunknown()\n"
        ),
        "self.py": "def h():\n    pass\nh()\n",
        "disconnected.md": "policy",
    }
    for name, text in texts.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000016")
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(n) for n in texts),
        maximum_resource_bytes=1024,
    )
    interpreted = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=tuple(
            r.address for r in snapshot.resources if str(r.address).endswith(".py")
        ),
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpreted.interpretations,
    )
    source = derive_python_declaration_references(
        snapshot,
        resource_address=RepositoryResourceAddress("source.py"),
        module_universe=universe,
    )
    own = derive_python_declaration_references(
        snapshot,
        resource_address=RepositoryResourceAddress("self.py"),
        module_universe=universe,
    )
    assert len(source.references) == 5
    assert any(
        a.reference is None and a.source_text == "unknown" for a in source.assessments
    )
    view = build_reference_view(snapshot, (*source.references, *own.references))
    edges = {str(e.target): e for e in view.edges if str(e.source) == "source.py"}
    assert edges["left.py"].weight == 2
    assert edges["left.py"].probability == pytest.approx(2 / 3)
    assert edges["right.py"].probability == pytest.approx(1 / 3)
    assert any(
        e.source == e.target == RepositoryResourceAddress("self.py") for e in view.edges
    )
    lexical = _lexical(tmp_path, snapshot, query_text="unknown")
    result = rank(snapshot, view, lexical)
    assert "disconnected.md" not in {str(r.address) for r in result.resources}
    assert "self.py" not in {str(r.address) for r in result.resources}
    assert {str(r.address) for r in result.resources} == {
        "left.py",
        "right.py",
    }
    # Degree normalization makes 4 references twice, not four times, 1 reference.
    rows = {str(r.address): r for r in result.resources}
    assert rows["left.py"].score / rows["right.py"].score == pytest.approx(2)


def test_uniform_seeds_ppr_flow_graph_novel_and_native_rrf(tmp_path: Path) -> None:  # noqa: PLR0915 -- complete provenance fixture
    snapshot, _, refs, _ = _facts(tmp_path)
    lexical = _lexical(tmp_path, snapshot, query_text="value")
    view = build_reference_view(snapshot, refs)
    exact = snapshot.resource_at(RepositoryResourceAddress("unrelated.py"))
    assert seed_union(snapshot, lexical, (exact, exact)) == (
        RepositoryResourceAddress("consumer.py"),
        exact.address,
    )
    result = rank(snapshot, view, lexical, (exact, exact))
    assert len(result.exact) == 1
    rows = {str(r.address): r for r in result.resources}
    states = {str(s.address): s for s in result.states}
    assert states["consumer.py"].direct_restart_mass == pytest.approx(0.15 / 2)
    assert states["unrelated.py"].direct_restart_mass == pytest.approx(0.15 / 2)
    assert states["consumer.py"].stationary_mass > 0
    assert states["consumer.py"].incoming_structural_flow == 0
    assert "consumer.py" not in rows
    assert "unrelated.py" not in rows
    assert rows["pkg/target.py"].seed is False
    assert (
        states["pkg/target.py"].direct_restart_mass
        == states["pkg/target.py"].dangling_return_mass
        == 0
    )
    assert states["pkg/target.py"].incoming[0][1] == rows["pkg/target.py"].score
    assert sum(s.stationary_mass for s in result.states) == pytest.approx(1)
    for row in result.states:
        assert row.stationary_mass == pytest.approx(
            row.direct_restart_mass
            + row.dangling_return_mass
            + row.incoming_structural_flow,
            abs=1e-10,
        )
    fused = dict(fuse(result))
    assert fused[RepositoryResourceAddress("consumer.py")] == 1 / 61
    assert exact.address not in fused
    assert fused[RepositoryResourceAddress("pkg/target.py")] == 1 / 61
    assert set(fused) == {
        RepositoryResourceAddress("consumer.py"),
        RepositoryResourceAddress("pkg/target.py"),
    }
    assert result == rank(snapshot, view, lexical, (exact,))
    encoded = graph_evidence(result)
    assert encoded == graph_evidence(result)
    validate_evidence(encoded, result)
    assert refs[0].identity.encode() in encoded
    assert b'"referenced_expression"' in encoded
    with pytest.raises(ValueError, match="tamper"):
        validate_evidence(encoded + b" ", result)
    projected = definitions(result)
    assert len(projected) == 1
    assert projected[0].definition == refs[0].target_declaration.identity
    assert projected[0].name == "f"
    assert projected[0].incoming_flow == pytest.approx(
        rows["pkg/target.py"].score, abs=1e-10
    )
    assert {key for key, _ in projected[0].reference_flows} == {
        r.identity for r in refs
    }
    assert projected[0].header.startswith("def f():")
    validate_definitions(projected, result)
    flow = 0.85 * states["consumer.py"].stationary_mass * view.edges[0].probability
    assert rows["pkg/target.py"].score == flow
    assert projected[0].incoming_flow == pytest.approx(flow)
    assert all(
        s.pair_flow == flow and s.per_occurrence_flow == flow / 3
        for s in projected[0].occurrence_flows
    )
    assert {s.reference for s in projected[0].occurrence_flows} == set(refs)
    assert all(
        s.source_resource == "consumer.py" and s.definition_owner == "pkg/target.py"
        for s in projected[0].occurrence_flows
    )
    with pytest.raises(ValueError, match="aggregation"):
        validate_definitions((replace(projected[0], incoming_flow=99),), result)
    mapped = render_map(projected)
    assert mapped["effectiveness_arm"] is False
    assert render_map(projected, budget=mapped["utf8_bytes"])["admitted"] == 1
    assert render_map(projected, budget=mapped["utf8_bytes"] - 1)["admitted"] == 0
    assert render_map(projected, budget=0)["text"] == ""


def test_no_seeds_abstains_exact_only_and_stable_ties(tmp_path: Path) -> None:
    snapshot, _, refs, _ = _facts(tmp_path)
    lexical = _lexical(tmp_path, snapshot, query_text="no_positive_candidate")
    view = build_reference_view(snapshot, refs)
    result = rank(snapshot, view, lexical)
    assert result.resources == ()
    assert result.seeds == ()
    assert result.iterations == 0
    assert fuse(result) == ()
    exact = tuple(
        snapshot.resource_at(RepositoryResourceAddress(n))
        for n in ("unrelated.py", "pkg/__init__.py")
    )
    result = rank(snapshot, view, lexical, exact)
    assert result.resources == ()
    assert all(s.stationary_mass == 0.5 for s in result.states if s.seed)
    assert all(s.incoming_structural_flow == 0 for s in result.states)


def test_exact_native_literal_resolution_existing_absent_and_no_fuzzy(
    tmp_path: Path,
) -> None:
    snapshot, _, _, _ = _facts(tmp_path)
    existing = RepositoryResourceAddress("consumer.py")
    future = RepositoryResourceAddress("future.py")
    result = resolve_exact_seeds(
        snapshot, "consumer.py future.py", (existing, existing, future)
    )
    assert result.resources == (snapshot.resource_at(existing),)
    assert result.absent == (future,)
    assert len(result.locators) == 2
    with pytest.raises(ValueError, match="literal"):
        resolve_exact_seeds(snapshot, "consumer", (existing,))


def test_top_ten_seed_bound(tmp_path: Path) -> None:
    texts = {f"f{i:02}.py": "signal\n" for i in range(12)}
    for name, text in texts.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000016")
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(n) for n in texts),
        maximum_resource_bytes=1024,
    )
    lexical = _lexical(tmp_path, snapshot, query_text="signal")
    # Twelve positives must supply ten lexical seeds, not every positive result.
    from devtools.context.retrieval.lexical.bm25 import (  # noqa: PLC0415
        retrieve_repository_text_documents_by_bm25,
    )

    lexical = retrieve_repository_text_documents_by_bm25(
        query=lexical.query, index=lexical.index, maximum_results=12
    )
    assert len(lexical.matches) == 12
    assert len(seed_union(snapshot, lexical, (snapshot.resources[-1],))) == 11
    result = rank(snapshot, build_reference_view(snapshot, ()), lexical)
    assert len(result.resources) == 0
    assert len([s for s in result.states if s.stationary_mass > 0]) == 10
    assert len(fuse(result)) == 12
    assert dict(fuse(result))[snapshot.resources[-1].address] == 1 / 72


def test_kernel_restart_dangling_and_convergence() -> None:
    scores, _, converged = stationary_distribution(
        [[(1, 1)], []], [1, 0], damping=0.85, tolerance=1e-10, maximum_iterations=200
    )
    assert converged
    assert scores == pytest.approx([1 / 1.85, 0.85 / 1.85], abs=1e-10)
    one, iterations, converged = stationary_distribution(
        [[(1, 1)], []], [1, 0], damping=0.85, tolerance=1e-10, maximum_iterations=1
    )
    assert one == pytest.approx([0.15, 0.85])
    assert iterations == 1
    assert not converged


def test_tampered_foreign_stale_and_conflicting_reference_rejected(
    tmp_path: Path,
) -> None:
    snapshot, _, refs, _ = _facts(tmp_path)
    view = build_reference_view(snapshot, refs)
    with pytest.raises(ValueError, match="mismatch"):
        require_view(
            snapshot, replace(view, edges=(replace(view.edges[0], weight=99),))
        )
    with pytest.raises(ValueError, match="snapshot"):
        build_reference_view(
            replace(
                snapshot,
                repository_id=RepositoryId.parse(
                    "00000000-0000-4000-8000-000000000099"
                ),
            ),
            refs,
        )
    with pytest.raises(ValueError, match="differs"):
        build_reference_view(
            snapshot, (replace(refs[0], target_resource=snapshot.resources[-1]),)
        )
    with pytest.raises(ValueError, match="conflicting"):
        build_reference_view(
            snapshot, (refs[0], replace(refs[0], direct_call=not refs[0].direct_call))
        )
    lexical = _lexical(tmp_path, snapshot, query_text="value")
    result = rank(snapshot, view, lexical)
    with pytest.raises(ValueError, match="membership/ranks"):
        fuse(
            replace(
                result,
                resources=(
                    replace(result.resources[0], rank=99),
                    *result.resources[1:],
                ),
            )
        )
    with pytest.raises(ValueError, match="personalization"):
        fuse(replace(result, seeds=()))
    with pytest.raises(ValueError, match="converge"):
        rank(
            snapshot, view, lexical, settings=GraphRankingSettings(maximum_iterations=1)
        )
    with pytest.raises(ValueError, match="Exact seed"):
        seed_union(
            snapshot, lexical, (replace(snapshot.resources[0], content="tampered"),)
        )
    with pytest.raises(TypeError):
        build_reference_view(snapshot, (object(),))  # type: ignore[arg-type]


@pytest.mark.parametrize("budget", [-1, True, 1.2])
def test_map_invalid_budget(budget: int) -> None:
    with pytest.raises(ValueError, match="budget"):
        render_map((), budget=budget)


def test_map_non_ascii_exact_byte_budget(tmp_path: Path) -> None:
    snapshot, _, refs, _ = _facts(tmp_path)
    result = rank(
        snapshot,
        build_reference_view(snapshot, refs),
        _lexical(tmp_path, snapshot, query_text="value"),
    )
    projected = definitions(result)
    unicode_rows = (replace(projected[0], header="def café(): …"),)
    mapped = render_map(unicode_rows)
    assert mapped["utf8_bytes"] == len(mapped["text"].encode("utf-8"))
    assert mapped["utf8_bytes"] > len(mapped["text"])
    assert render_map(unicode_rows, budget=mapped["utf8_bytes"] - 1)["omitted"] == 1


def test_ranking_does_not_parse_or_use_native_frontier(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    snapshot, _, refs, _ = _facts(tmp_path)
    lexical = _lexical(tmp_path, snapshot, query_text="value")

    def forbid(*_args: object, **_kwargs: object) -> None:
        msg = "No parsing, BFS or frontier acquisition"
        raise AssertionError(msg)

    monkeypatch.setattr("ast.parse", forbid)
    monkeypatch.setattr(
        "devtools.context.retrieval.structural.retrieve_python_direct_structural_resources",
        forbid,
    )
    result = rank(snapshot, build_reference_view(snapshot, refs), lexical)
    assert len(result.resources) == 1
