# Copyright (c) 2026
# ruff: noqa: COM812, D103, E501
"""Semantic invariants for the sealed, Git-metadata-only task freeze."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from experiments.increment_25 import task_population as population


def _commit(
    sha: str,
    *,
    subject: str = "Fix bounded observation failure",
    body: str = "",
    paths: tuple[str, ...] = ("src/devtools/core/value.py",),
    parents: tuple[str, ...] = ("parent",),
) -> population.CommitMetadata:
    return population.CommitMetadata(
        sha=sha,
        parent_sha=parents[0] if len(parents) == 1 else None,
        parents=parents,
        subject=subject,
        body=body,
        changed_paths=paths,
        path_categories=population.path_categories(paths),
    )


def _eligible_cards(count: int = 24) -> tuple[population.TaskCard, ...]:
    return tuple(
        population.task_card(
            population.classify_commit(_commit(f"{index:012x}{index:028x}"))
        )
        for index in range(count)
    )


def test_merge_parent_and_relevant_touch_rules_are_explicit() -> None:
    assert (
        population.classify_commit(_commit("1", parents=("a", "b"))).exclusion_reason
        == "merge-commit"
    )
    assert (
        population.classify_commit(_commit("2", parents=())).exclusion_reason
        == "merge-commit"
    )
    assert (
        population.classify_commit(_commit("3", paths=("README.md",))).exclusion_reason
        == "no-source-or-test-touch"
    )


def test_documentation_only_and_prior_mechanism_history_are_excluded() -> None:
    documentation = _commit("4", paths=("docs/architecture.md",))
    prior = _commit("5", subject="Evaluate structural repository expansion")
    imports = _commit("6", paths=("src/devtools/context/python/imports/relations.py",))
    assert (
        population.classify_commit(documentation).exclusion_reason
        == "documentation-only"
    )
    assert (
        population.classify_commit(prior).exclusion_reason
        == "prior-retrieval-or-structural-experiment"
    )
    assert (
        population.classify_commit(imports).exclusion_reason
        == "prior-retrieval-or-structural-experiment"
    )


def test_subjective_exclusions_preserve_exact_message_evidence() -> None:
    commit = _commit("2f66a64e8fa9c534ec0a0700f95c6dfa6aaa6498", subject="Filesystems")
    record = population.classify_commit(commit)
    assert record.exclusion_kind == "judgment"
    assert record.task_evidence == "Filesystems"
    assert record.exclusion_reason is not None


def test_task_card_uses_only_message_evidence_and_keeps_paths_evaluator_only() -> None:
    commit = _commit(
        "7",
        subject="Fix bounded observation failure",
        body="Preserve the bounded behavior.",
        paths=("src/devtools/secret/answer.py",),
    )
    card = population.task_card(population.classify_commit(commit))
    rendered_card = (
        json.dumps(
            {
                key: value
                for key, value in card.__dict__.items()
                if key != "evaluator_only_changed_paths"
            }
        )
        if hasattr(card, "__dict__")
        else json.dumps(
            {"purpose": card.information_need_purpose, "query": card.lexical_query}
        )
    )
    assert "secret/answer.py" not in rendered_card
    assert card.evaluator_only_changed_paths == ("src/devtools/secret/answer.py",)
    assert "bounded observation failure" in card.lexical_query


def test_population_and_sampling_ignore_input_order() -> None:
    commits = tuple(_commit(f"{index:012x}{index:028x}") for index in range(24))
    first = population.enumerate_population(commits)
    second = population.enumerate_population(reversed(commits))
    assert first == second
    cards = tuple(population.task_card(record) for record in first)
    assert population.sample_cards(cards) == population.sample_cards(reversed(cards))


def test_fixed_seed_split_is_disjoint_complete_and_exact_when_population_is_large_enough() -> (
    None
):
    cards = _eligible_cards()
    split = population.sample_cards(cards)
    assert len(split.development_case_ids) == population.DEVELOPMENT_SIZE
    assert len(split.confirmation_case_ids) == population.CONFIRMATION_SIZE
    assert not split.reserve_case_ids
    assert set(split.development_case_ids).isdisjoint(split.confirmation_case_ids)
    assert {*split.development_case_ids, *split.confirmation_case_ids} == {
        card.case_id for card in cards
    }


def test_reserve_is_subset_of_eligible_without_duplicates() -> None:
    cards = _eligible_cards(27)
    split = population.sample_cards(cards)
    assigned = (
        *split.development_case_ids,
        *split.confirmation_case_ids,
        *split.reserve_case_ids,
    )
    assert len(assigned) == len(set(assigned))
    assert set(assigned) == {card.case_id for card in cards}


def test_sampling_never_silently_downsizes() -> None:
    with pytest.raises(ValueError, match="Fewer than 24"):
        population.sample_cards(_eligible_cards(23))


def test_collect_uses_the_exclusive_cutoff(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls: list[tuple[str, ...]] = []

    def fake_lines(_root: Path, *arguments: str) -> tuple[str, ...]:
        calls.append(arguments)
        return ()

    monkeypatch.setattr(population, "_git_lines", fake_lines)
    assert population.collect_git_population(tmp_path) == ()
    assert calls == [("rev-list", "--topo-order", f"{population.CUTOFF_COMMIT}^")]


def test_freeze_has_no_candidate_or_judgment_fields() -> None:
    envelope = population.build_freeze(
        commits=(_commit(f"{index:012x}{index:028x}") for index in range(24)),
        checkpoint=population.FREEZE_CHECKPOINT,
    )
    assert population.validate_freeze(envelope)
    assert population.validate_freeze(envelope)
    envelope["payload"]["lexical_results"] = []  # type: ignore[index]
    assert not population.validate_freeze(envelope)


def test_committed_freeze_is_valid_and_sealed() -> None:
    path = Path("experiments/increment_25/task_population_freeze.json")
    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert population.validate_freeze(envelope)
    protocol = envelope["payload"]["protocol"]
    assert protocol["candidate_outcomes_generated"] is False
    assert protocol["usefulness_judgments_made"] is False
    assert protocol["confirmation_status"] == "sealed"
