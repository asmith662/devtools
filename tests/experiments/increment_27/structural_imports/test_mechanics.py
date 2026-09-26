# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""One directed relation, saved seeds, and exact judgment-cost boundaries."""

from __future__ import annotations

import gzip
import hashlib
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.context.python.imports.declarations import (
    derive_python_import_declarations,
)
from devtools.context.python.imports.resolution import PythonImportResolutionOutcome
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from experiments.increment_25.development import write_artifact
from experiments.increment_25.task_population import TaskCard
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import (
    _read_json,
    canonical_json_bytes,
    prior_judgment_matches,
)
from experiments.increment_27.structural_imports.cost import (
    _add_prior,
    _normalize_state,
    build_cost,
)
from experiments.increment_27.structural_imports.mechanics import (
    GZIP_COMPRESSLEVEL,
    RAW_CANDIDATE_SHA256,
    _derive_relations,
    _digest,
    _module_universe,
    build_freeze,
    generate_case,
    project_direction,
    read_candidate_artifact,
)

if TYPE_CHECKING:
    from devtools.context.python.imports.relations import (
        PythonResolvedModuleImportRelation,
    )


def _module(name: str, address: str) -> SimpleNamespace:
    return SimpleNamespace(identity=name, resource=SimpleNamespace(address=address))


def _relation(
    name: str, source: SimpleNamespace, target: SimpleNamespace
) -> PythonResolvedModuleImportRelation:
    support = SimpleNamespace(
        start_line=1,
        start_column_utf8=0,
        end_line=1,
        end_column_utf8=20,
    )
    declaration = SimpleNamespace(
        derivation_identity=f"decl-{name}",
        declaration_ordinal=0,
        support=support,
    )
    resolution = SimpleNamespace(
        identity=f"resolution-{name}",
        outcome=PythonImportResolutionOutcome.RESOLVED,
        declaration=declaration,
    )
    return cast(
        "PythonResolvedModuleImportRelation",
        SimpleNamespace(
            identity=name, source=source, target=target, resolution=resolution
        ),
    )


def _ranks(*addresses: str) -> dict[str, list[dict[str, object]]]:
    return {
        method: [
            {"address": address, "rank": rank}
            for rank, address in enumerate(addresses, 1)
        ]
        for method in ("canonical", "bm25_plus", "identifier", "path", "rrf")
    }


def test_saved_development_partition_and_canonical_seed_contract() -> None:
    root = Path("experiments/increment_27")
    frozen = build_freeze(root)
    payload = cast("dict[str, Any]", frozen["payload"])
    development = payload["development_case_ids"]
    heldout = payload["heldout_case_ids_sealed"]
    assert len(development) == 24
    assert len(heldout) == 14
    assert not set(development) & set(heldout)
    assert payload["maximum_relation_count_per_path"] == 1
    baseline = _read_json(root / "canonical_positive_lexical_rankings.json")
    baseline_cases = cast("list[dict[str, Any]]", baseline["cases"])
    assert [case["case_id"] for case in baseline_cases] == development
    for case in baseline_cases:
        assert [row["rank"] for row in case["positive_lexical_ordering"][:5]] == list(
            range(1, min(5, len(case["positive_lexical_ordering"])) + 1),
        )


def test_outgoing_incoming_are_separate_reverse_lookup_and_preserve_supports() -> None:
    seed = _module("seed", "seed.py")
    target = _module("target", "target.py")
    importer = _module("importer", "importer.py")
    other_seed = _module("other-seed", "other.py")
    relations = [
        _relation("one", seed, target),
        _relation("two", seed, target),
        _relation("three", importer, seed),
        _relation("four", seed, other_seed),
        _relation("five", target, importer),  # A second edge is never followed.
        _relation("six", other_seed, target),
    ]
    seeds = [
        {
            "address": "seed.py",
            "canonical_rank": 1,
            "module_interpretation_identity": "seed",
        },
        {
            "address": "other.py",
            "canonical_rank": 2,
            "module_interpretation_identity": "other-seed",
        },
    ]
    positive = [
        {"address": address, "rank": rank}
        for rank, address in enumerate(("seed.py", "other.py", "lexical.py"), 1)
    ]
    ranks = _ranks("seed.py", "other.py", "lexical.py")
    outgoing = project_direction(
        direction="outgoing",
        seeds=seeds,
        relations=relations,
        positive=positive,
        lexical_rankings=ranks,
    )
    incoming = project_direction(
        direction="incoming",
        seeds=seeds,
        relations=relations,
        positive=positive,
        lexical_rankings=ranks,
    )
    assert [row["address"] for row in outgoing["candidates"]] == ["target.py"]
    assert outgoing["candidates"][0]["support_count"] == 3
    assert {
        path["relation_identity"] for path in outgoing["candidates"][0]["paths"]
    } == {"one", "two", "six"}
    assert outgoing["seed_overlap_path_count"] == 1
    assert outgoing["duplicates_within_seeds"] == 1
    assert outgoing["duplicates_across_seeds"] == 1
    assert outgoing["same_volume_lexical_control"]["addresses"] == ["lexical.py"]
    assert [row["address"] for row in incoming["candidates"]] == ["importer.py"]
    assert incoming["candidates"][0]["paths"][0]["source_resource"] == "importer.py"
    assert incoming["candidates"][0]["paths"][0]["target_resource"] == "seed.py"


def test_lexical_classification_and_exhaustion() -> None:
    seed = _module("seed", "seed.py")
    relations = [
        _relation("deep", seed, _module("deep", "deep.py")),
        _relation("new", seed, _module("new", "new.py")),
    ]
    seeds = [
        {
            "address": "seed.py",
            "canonical_rank": 1,
            "module_interpretation_identity": "seed",
        }
    ]
    positive = [
        {"address": address, "rank": rank}
        for rank, address in enumerate(
            (
                "seed.py",
                "filler1.py",
                "filler2.py",
                "filler3.py",
                "filler4.py",
                "deep.py",
            ),
            1,
        )
    ]
    ranks = _ranks(*(str(row["address"]) for row in positive))
    ranks["identifier"].append({"address": "new.py", "rank": 3})
    arm = project_direction(
        direction="outgoing",
        seeds=seeds,
        relations=relations,
        positive=positive,
        lexical_rankings=ranks,
    )
    by_address = {row["address"]: row for row in arm["candidates"]}
    assert by_address["deep.py"]["canonical_category"] == "deeper-positive-rank"
    assert by_address["new.py"]["canonical_category"] == "no-positive-rank"
    assert by_address["new.py"]["absent_all_saved_positive_lexical"] is False
    assert arm["same_volume_lexical_control"]["addresses"] == [
        "filler1.py",
        "filler2.py",
    ]
    exhausted = project_direction(
        direction="outgoing",
        seeds=seeds,
        relations=relations,
        positive=positive[:1],
        lexical_rankings=ranks,
    )
    assert exhausted["same_volume_lexical_control"]["lexical_exhausted"] is True


def test_only_resolved_module_outcome_creates_relation(tmp_path: Path) -> None:
    contents = {
        "src/a.py": "import unique\nimport pkg\nimport missing\n",
        "src/pkg.py": "",
        "src/pkg/__init__.py": "",
        "src/unique.py": "",
    }
    for address, content in contents.items():
        file = tmp_path / address
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")
    snapshot = observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000027")
        ),
        root=resolve_path(tmp_path),
        addresses=tuple(RepositoryResourceAddress(address) for address in contents),
        maximum_resource_bytes=1024,
    )
    corpus: Any = SimpleNamespace(
        snapshot=snapshot,
        addresses=tuple(RepositoryResourceAddress(address) for address in contents),
        corpus_id="fixture-corpus",
    )
    universe, by_address = _module_universe(corpus, ("src",))
    relations, diagnostic = _derive_relations(
        corpus, universe=universe, by_address=by_address
    )
    assert len(relations) == 1
    assert str(relations[0].target.resource.address) == "src/unique.py"
    assert diagnostic["counts"]["resolution_unresolved-in-universe"] == 1
    assert diagnostic["counts"]["resolution_resolved"] == 1
    assert diagnostic["counts"]["resolution_ambiguous"] == 1
    # The source syntax remains distinct from its single established relation.
    analysis = derive_python_import_declarations(
        snapshot,
        resource_address=RepositoryResourceAddress("src/a.py"),
    )
    assert len(analysis.declarations) == 3
    case = generate_case(
        corpus=corpus,
        baseline={
            "case_id": "development",
            "parent_snapshot_sha": "parent",
            "information_need": {"purpose": "purpose", "lexical_query": "query"},
            "positive_result_count": 1,
            "positive_lexical_ordering": [{"address": "src/a.py", "rank": 1}],
        },
        comparison={"rankings": _ranks("src/a.py")},
        roots=("src",),
    )
    assert case["seeds"] == [
        {
            "case_id": "development",
            "address": "src/a.py",
            "canonical_rank": 1,
            "status": "eligible",
            "module_interpretation_identity": by_address["src/a.py"][0].identity,
            "module_interpretation_ids": [by_address["src/a.py"][0].identity],
        }
    ]
    assert [row["address"] for row in case["arms"]["outgoing"]["candidates"]] == [
        "src/unique.py"
    ]


def _card(case_id: str) -> TaskCard:
    return TaskCard(
        case_id=case_id,
        source_commit_sha="source",
        parent_snapshot_sha="parent",
        original_subject="task",
        original_body="",
        information_need_purpose="purpose",
        lexical_query="query",
        maintenance_category="test",
        repository_domain="test",
        corpus_source_roots=("src", "tests"),
        evaluator_only_changed_paths=(),
    )


def test_exact_reuse_three_states_and_cost_without_outcome_analysis() -> None:
    card = _card("case-0")
    prior: dict[tuple[str, str], dict[str, str]] = {}
    _add_prior(
        prior,
        card=card,
        address="new.py",
        judgment="UNJUDGED",
        source="frozen",
        information_need={"purpose": "purpose", "lexical_query": "query"},
        parent_snapshot_sha="parent",
        semantics=USEFULNESS_SEMANTICS,
    )
    assert _normalize_state("not-useful") == "NOT_USEFUL"
    assert prior[("case-0", "new.py")]["state"] == "UNJUDGED"
    with pytest.raises(ValueError, match="exact"):
        _add_prior(
            prior,
            card=card,
            address="wrong.py",
            judgment="USEFUL",
            source="frozen",
            information_need={"purpose": "different", "lexical_query": "query"},
            parent_snapshot_sha="parent",
            semantics=USEFULNESS_SEMANTICS,
        )
    cards = {f"case-{i}": _card(f"case-{i}") for i in range(24)}
    cases: list[dict[str, object]] = []
    for case_id in cards:
        candidate = {
            "address": "new.py",
            "canonical_category": "no-positive-rank",
            "absent_all_saved_positive_lexical": True,
        }
        arms = {
            direction: {
                "candidates": [candidate]
                if case_id == "case-0" and direction == "outgoing"
                else [],
                "same_volume_lexical_control": {
                    "addresses": ["control.py"]
                    if case_id == "case-0" and direction == "outgoing"
                    else []
                },
            }
            for direction in ("outgoing", "incoming")
        }
        cases.append(
            {
                "case_id": case_id,
                "parent_snapshot_sha": "parent",
                "information_need": {"purpose": "purpose", "lexical_query": "query"},
                "arms": arms,
            }
        )
    result = build_cost(mechanics={"cases": cases}, prior=prior, cards=cards)
    assert result["structural_union"] == {"total": 1, "reused": 1, "new": 0}
    assert result["previously_unjudged_reused_count"] == 1
    assert result["same_volume_control_union"] == {"total": 1, "reused": 0, "new": 1}
    assert result["new_pair_identities"] == []


@pytest.mark.parametrize(
    ("purpose", "query", "snapshot", "prior_address", "semantics"),
    [
        ("other", "query", "parent", "new.py", USEFULNESS_SEMANTICS),
        ("purpose", "other", "parent", "new.py", USEFULNESS_SEMANTICS),
        ("purpose", "query", "other", "new.py", USEFULNESS_SEMANTICS),
        ("purpose", "query", "parent", "other.py", USEFULNESS_SEMANTICS),
        ("purpose", "query", "parent", "new.py", "other-semantics"),
    ],
)
def test_every_exact_reuse_identity_dimension_is_required(
    purpose: str, query: str, snapshot: str, prior_address: str, semantics: str
) -> None:
    assert not prior_judgment_matches(
        card=_card("case"),
        prior_information_need={"purpose": purpose, "lexical_query": query},
        prior_parent_snapshot=snapshot,
        prior_address=prior_address,
        resource_address="new.py",
        prior_usefulness_semantics=semantics,
    )


def test_frozen_candidate_artifact_precedes_cost_and_excludes_heldout() -> None:
    root = Path("experiments/increment_27")
    frozen = build_freeze(root)
    mechanics = read_candidate_artifact(root / "structural_import_candidates.json.gz")
    cost = _read_json(root / "structural_import_judgment_cost.json")
    freeze_payload = cast("dict[str, Any]", frozen["payload"])
    mechanical_cases = cast("list[dict[str, Any]]", mechanics["cases"])
    cost_payload = cast("dict[str, Any]", cost["payload"])
    assert mechanics["content_identity"] == _digest(
        {key: value for key, value in mechanics.items() if key != "content_identity"}
    )
    assert mechanics["freeze_identity"] == frozen["content_identity"]
    assert mechanics["heldout_executed"] is False
    assert mechanics["judgment_artifacts_loaded"] is False
    assert [case["case_id"] for case in mechanical_cases] == freeze_payload[
        "development_case_ids"
    ]
    assert not {case["case_id"] for case in mechanical_cases} & set(
        freeze_payload["heldout_case_ids_sealed"]
    )
    assert cost_payload["candidate_identity"] == mechanics["content_identity"]
    assert cost_payload["labels_by_origin_analyzed"] is False
    assert cost_payload["new_judgments_assigned"] is False


def test_deterministic_serialization(tmp_path: Path) -> None:
    value = {"z": [1, 2], "a": {"b": "text"}}
    assert _digest(value) == _digest({"a": {"b": "text"}, "z": [1, 2]})
    path = tmp_path / "artifact.json"
    write_artifact(path=path, payload=value)
    first = path.read_bytes()
    write_artifact(path=path, payload=value)
    assert path.read_bytes() == first


def test_non_ascii_canonical_json_round_trip_uses_utf8(tmp_path: Path) -> None:
    payload = {"purpose": "Runtime → Evidence", "resource": "café.py"}
    artifact = {"payload": payload, "content_identity": _digest(payload)}
    path = tmp_path / "unicode.json"
    write_artifact(path=path, payload=artifact)
    assert path.read_bytes() == canonical_json_bytes(artifact)
    recovered = _read_json(path)
    assert recovered == artifact
    assert recovered["content_identity"] == _digest(recovered["payload"])


def test_compressed_candidate_is_exact_canonical_original() -> None:
    path = Path("experiments/increment_27/structural_import_candidates.json.gz")
    compressed = path.read_bytes()
    raw = gzip.decompress(compressed)
    assert hashlib.sha256(raw).hexdigest() == RAW_CANDIDATE_SHA256
    assert gzip.compress(raw, compresslevel=GZIP_COMPRESSLEVEL, mtime=0) == compressed
    artifact = read_candidate_artifact(path)
    assert raw == canonical_json_bytes(artifact)
    assert artifact["content_identity"] == _digest(
        {key: value for key, value in artifact.items() if key != "content_identity"}
    )
