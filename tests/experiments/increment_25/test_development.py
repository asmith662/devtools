# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, PT018, S607, SLF001
"""Tests for Increment-25 development-only candidate generation."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import cast

import pytest

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.increment_25 import development
from experiments.increment_25.development import (
    DevelopmentBoundaryError,
    SnapshotCorpus,
    generate_case,
    load_frozen_development,
)
from experiments.increment_25.run_development import parse_arguments
from experiments.increment_25.task_population import TaskCard

_FREEZE = Path("experiments/increment_25/task_population_freeze.json")


def _card(*, lexical_query: str = "needle") -> TaskCard:
    return TaskCard(
        case_id="development-case",
        source_commit_sha="b" * 40,
        parent_snapshot_sha="a" * 40,
        original_subject="Needle task",
        original_body="",
        information_need_purpose="Find the needle implementation",
        lexical_query=lexical_query,
        maintenance_category="feature-capability",
        repository_domain="context",
        corpus_source_roots=("src", "tests"),
        evaluator_only_changed_paths=("src/post_change.py",),
    )


def _corpus(tmp_path: Path, resources: dict[str, str]) -> SnapshotCorpus:
    for address, content in resources.items():
        target = tmp_path / address
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return development._build_snapshot_corpus(
        snapshot_root=tmp_path,
        source_roots=("src", "tests"),
    )


def test_freeze_exposes_exact_development_partition_only() -> None:
    frozen = load_frozen_development(_FREEZE)

    assert len(frozen.cards) == 8
    assert tuple(card.case_id for card in frozen.cards) == frozen.development_case_ids
    assert all(frozen.require_case(item) for item in frozen.development_case_ids)


def test_confirmation_reserve_and_unknown_execution_are_rejected() -> None:
    frozen = load_frozen_development(_FREEZE)

    with pytest.raises(DevelopmentBoundaryError, match="Confirmation case is sealed"):
        frozen.require_case(next(iter(frozen.confirmation_case_ids)))
    with pytest.raises(DevelopmentBoundaryError, match="Reserve case"):
        frozen.require_case(next(iter(frozen.reserve_case_ids)))
    with pytest.raises(DevelopmentBoundaryError, match="not in"):
        frozen.require_case("not-frozen")


def test_development_cli_has_no_partition_selection() -> None:
    parsed = parse_arguments(
        [
            "--candidate-output",
            "candidate.json",
            "--judgment-output",
            "judgment.json",
        ],
    )
    assert vars(parsed).keys() == {
        "repository_root",
        "freeze",
        "candidate_output",
        "judgment_output",
    }


def test_git_materialization_uses_requested_parent_not_task_or_head(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    subprocess.run(("git", "init", "-q"), cwd=repository, check=True)
    subprocess.run(
        ("git", "config", "user.email", "test@example.invalid"),
        cwd=repository,
        check=True,
    )
    subprocess.run(("git", "config", "user.name", "Test"), cwd=repository, check=True)
    source = repository / "src" / "value.py"
    source.parent.mkdir()
    source.write_text("PARENT = True\n", encoding="utf-8")
    subprocess.run(("git", "add", "src/value.py"), cwd=repository, check=True)
    subprocess.run(("git", "commit", "-qm", "parent"), cwd=repository, check=True)
    parent = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    source.write_text("TASK = True\n", encoding="utf-8")
    subprocess.run(("git", "commit", "-qam", "task"), cwd=repository, check=True)
    source.write_text("WORKTREE = True\n", encoding="utf-8")

    destination = tmp_path / "snapshot"
    destination.mkdir()
    development._materialize_git_snapshot(
        repository_root=repository,
        snapshot_sha=parent,
        source_roots=("src", "tests"),
        destination=destination,
    )

    assert (destination / "src" / "value.py").read_text(
        encoding="utf-8",
    ) == "PARENT = True\n"
    assert source.read_text(encoding="utf-8") == "WORKTREE = True\n"


def test_structural_expansion_is_outgoing_resolved_one_hop_and_deduplicated(
    tmp_path: Path,
) -> None:
    corpus = _corpus(
        tmp_path,
        {
            "src/consumer.py": (
                "from pkg import f\n"
                "from pkg import f as again\n"
                "from missing import nope\n"
                "from pkg import absent\n"
                "from dupe import item\n"
                "import os\n"
            ),
            "src/pkg/__init__.py": "from .impl import f\n",
            "src/pkg/impl.py": "from deeper import g\ndef f():\n    pass\n",
            "src/deeper/__init__.py": "from .impl import g\n",
            "src/deeper/impl.py": "def g():\n    pass\n",
            "src/dupe.py": "",
            "src/dupe/__init__.py": "",
        },
    )
    consumer = RepositoryResourceAddress("src/consumer.py")
    resolutions, diagnostics = development._resolve_seed_imported_members(
        snapshot=corpus.snapshot,
        addresses=corpus.addresses,
        source_roots=("src", "tests"),
        seed=(consumer,),
    )
    additions, provenance = development._structural_additions(
        resolutions=resolutions,
        seed=(consumer,),
    )

    assert additions == (RepositoryResourceAddress("src/pkg/impl.py"),)
    assert len(provenance[additions[0]]) == 2
    assert RepositoryResourceAddress("src/deeper/impl.py") not in additions
    counts = cast("dict[str, int]", diagnostics[0]["counts"])
    assert counts == {
        "relevant_imported_member_observations_considered": 6,
        "resolved": 2,
        "unresolved_in_universe": 2,
        "ambiguous": 1,
        "unsupported": 1,
        "resolved_targets_already_in_seed": 0,
        "distinct_structural_additions": 1,
    }


def test_seed_target_is_excluded_but_diagnostic_is_preserved(tmp_path: Path) -> None:
    corpus = _corpus(
        tmp_path,
        {
            "src/consumer.py": "from pkg import f\n",
            "src/pkg/__init__.py": "from .impl import f\n",
            "src/pkg/impl.py": "def f():\n    pass\n",
        },
    )
    seed = (
        RepositoryResourceAddress("src/consumer.py"),
        RepositoryResourceAddress("src/pkg/impl.py"),
    )
    resolutions, diagnostics = development._resolve_seed_imported_members(
        snapshot=corpus.snapshot,
        addresses=corpus.addresses,
        source_roots=("src", "tests"),
        seed=seed,
    )
    additions, _ = development._structural_additions(resolutions=resolutions, seed=seed)

    assert additions == ()
    counts = cast("dict[str, int]", diagnostics[0]["counts"])
    assert counts["resolved_targets_already_in_seed"] == 1


def test_generate_case_uses_canonical_lexical_seed_and_matched_control(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    resources = {f"src/d{index}.py": "needle\n" for index in range(1, 8)}
    resources["src/z.py"] = "no positive score here\n"
    corpus = _corpus(tmp_path, resources)
    canonical = retrieve_repository_text_documents_by_bm25
    calls = 0

    def spy(**kwargs: object) -> object:
        nonlocal calls
        calls += 1
        return canonical(**kwargs)  # type: ignore[arg-type]

    def no_resolutions(**_kwargs: object) -> tuple[tuple[()], list[dict[str, object]]]:
        return (), []

    structural = (
        RepositoryResourceAddress("src/d7.py"),
        RepositoryResourceAddress("src/z.py"),
    )
    provenance: dict[RepositoryResourceAddress, list[dict[str, object]]] = {
        address: [] for address in structural
    }

    def fake_additions(**_kwargs: object) -> object:
        return structural, provenance

    monkeypatch.setattr(development, "retrieve_repository_text_documents_by_bm25", spy)
    monkeypatch.setattr(development, "_resolve_seed_imported_members", no_resolutions)
    monkeypatch.setattr(development, "_structural_additions", fake_additions)

    case = generate_case(card=_card(), corpus=corpus)

    assert calls == 1
    assert case["shared_lexical_seed"] == [f"src/d{index}.py" for index in range(1, 6)]
    assert case["matched_lexical_additions"] == ["src/d6.py", "src/d7.py"]
    assert case["overlap"] == {
        "intersection": ["src/d7.py"],
        "structural_only": ["src/z.py"],
        "lexical_only": ["src/d6.py"],
    }
    additions = cast("list[dict[str, object]]", case["structural_additions"])
    assert additions[0]["positive_lexical_rank"] == 7
    assert additions[1]["positive_lexical_rank"] is None
    assert additions[1]["has_positive_lexical_rank"] is False
    assert cast("dict[str, object]", case["capacity"])["m"] == 2


def test_lexical_exhaustion_is_explicit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    corpus = _corpus(
        tmp_path,
        {f"src/d{index}.py": "needle\n" for index in range(1, 7)}
        | {"src/z.py": "other\n"},
    )
    additions = (
        RepositoryResourceAddress("src/z.py"),
        RepositoryResourceAddress("src/a.py"),
    )
    monkeypatch.setattr(
        development, "_resolve_seed_imported_members", lambda **_kwargs: ((), []),
    )
    monkeypatch.setattr(
        development,
        "_structural_additions",
        lambda **_kwargs: (additions, {item: [] for item in additions}),
    )

    case = generate_case(card=_card(), corpus=corpus)
    capacity = cast("dict[str, object]", case["capacity"])
    assert capacity == {
        "m": 2,
        "actual_lexical_control_additions": 1,
        "lexical_exhausted": True,
    }


def test_frozen_query_is_consumed_unchanged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    corpus = _corpus(tmp_path, {"src/value.py": "# exact frozen query\n"})
    seen: list[str] = []
    canonical = analyze_repository_text_lexical_query

    def spy(*, text: str) -> object:
        seen.append(text)
        return canonical(text=text)

    monkeypatch.setattr(development, "analyze_repository_text_lexical_query", spy)
    generate_case(card=_card(lexical_query="Exact FROZEN query"), corpus=corpus)
    assert seen == ["Exact FROZEN query"]


def test_blinded_judgment_contains_neutral_parent_content_only(tmp_path: Path) -> None:
    corpus = _corpus(tmp_path, {"src/a.py": "parent a\n", "src/b.py": "parent b\n"})
    case: dict[str, object] = {
        "structural_additions": [{"address": "src/b.py", "supports": ["secret"]}],
        "matched_lexical_additions": ["src/a.py", "src/b.py"],
    }
    blinded = development._judgment_case(
        card=_card(), case=case, snapshot=corpus.snapshot,
    )
    serialized = json.dumps(blinded, sort_keys=True)

    assert [
        item["address"] for item in cast("list[dict[str, str]]", blinded["resources"])
    ] == ["src/a.py", "src/b.py"]
    assert "parent a" in serialized and "parent b" in serialized
    for hidden in (
        "origin",
        "supports",
        "structural",
        "matched",
        "changed_paths",
        "post_change",
        "lexical_rank",
        "useful",
    ):
        assert hidden not in serialized.lower()


def test_artifact_guards_reject_labels_and_blinding_leaks() -> None:
    frozen = load_frozen_development(_FREEZE)
    contaminated: dict[str, object] = {
        "cases": [
            {"case_id": item, "usefulness": "forbidden"}
            for item in frozen.development_case_ids
        ],
    }
    with pytest.raises(RuntimeError, match="adjudication"):
        development._assert_candidate_artifact(contaminated, frozen=frozen)
    with pytest.raises(RuntimeError, match="leaks"):
        development._assert_judgment_artifact({"changed_paths": []})


def test_case_generation_is_deterministic(tmp_path: Path) -> None:
    corpus = _corpus(
        tmp_path, {f"src/d{index}.py": "needle\n" for index in range(1, 7)},
    )
    first = generate_case(card=_card(), corpus=corpus)
    second = generate_case(card=_card(), corpus=corpus)
    assert first == second
