# Copyright (c) 2026
"""Tests for the experiment-owned filename and full-path lexical comparison."""

from __future__ import annotations

import json
from pathlib import Path

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments import address_lexical as experiment

_EXPECTED_CASE_COUNT = 13


def test_filename_terms_preserve_stem_and_exclude_extension_scoring() -> None:
    """Filename lexicalization uses the baseline rule only over a stem."""
    address = RepositoryResourceAddress("src/Request_Assembly.py")
    document = experiment.address_document(address=address, variant="filename")

    assert document.extension == ".py"
    assert [item.normalized_term for item in document.observations] == [
        "request_assembly",
    ]
    assert all(item.normalized_term != "py" for item in document.observations)


def test_full_path_terms_include_generic_directories_but_not_extension() -> None:
    """Full-path lexicalization distinguishes directories from the filename."""
    address = RepositoryResourceAddress("src/devtools/context/bm25.py")
    observations = experiment.full_path_observations(address=address)

    assert [(item.normalized_term, item.source) for item in observations] == [
        ("src", "directory"),
        ("devtools", "directory"),
        ("context", "directory"),
        ("bm25", "filename"),
    ]
    assert "py" not in {item.normalized_term for item in observations}


def test_controlled_cases_isolate_filename_directory_and_extension_effects() -> None:
    """Address evidence helps its intended field without extension leakage."""
    cases = experiment.controlled_cases()

    filename_baseline, filename, filename_path = cases["filename-only"]
    assert filename_baseline.hit_at_k is False
    assert filename.hit_at_k is True
    assert filename_path.hit_at_k is True

    directory_baseline, directory_filename, directory_path = cases["directory-only"]
    assert directory_baseline.hit_at_k is False
    assert directory_filename.hit_at_k is False
    assert directory_path.hit_at_k is True

    extension_baseline, extension_filename, extension_path = cases["shared-extension"]
    assert extension_baseline.matches == ()
    assert extension_filename.matches == ()
    assert extension_path.matches == ()


def test_controlled_address_evidence_exposes_content_distractor_limits() -> None:
    """Address terms need not outweigh a strong content distractor."""
    cases = experiment.controlled_cases()
    _baseline, filename, _path = cases["filename-distractor"]
    _baseline, _filename, path = cases["directory-distractor"]

    assert filename.relevant_ranks == (
        (RepositoryResourceAddress("src/target-guide.md"), 2),
    )
    assert path.relevant_ranks == ((RepositoryResourceAddress("context/opaque.md"), 2),)


def test_filename_weight_fixtures_exercise_conservative_and_distractor_behavior() -> (
    None
):
    """A small declared weight sweep makes regression pressure inspectable."""
    cases = experiment.controlled_filename_weight_cases(weights=(0.0, 0.25, 1.0))

    filename_only = dict(cases["filename-only"])
    assert filename_only[0.0].matches == ()
    assert filename_only[0.25].relevant_ranks == (
        (RepositoryResourceAddress("src/guide.md"), 1),
    )

    strong_content = dict(cases["strong-content-filename-coincidence"])
    assert strong_content[0.0].relevant_ranks == (
        (RepositoryResourceAddress("src/target.md"), 1),
    )
    assert strong_content[1.0].relevant_ranks == (
        (RepositoryResourceAddress("src/target.md"), 1),
    )

    test_distractor = dict(cases["test-source-filename-distractor"])
    assert test_distractor[1.0].relevant_ranks == (
        (RepositoryResourceAddress("src/rendering.py"), 2),
    )


def test_weight_calibration_preserves_content_baseline_at_zero_weight() -> None:
    """Zero filename weight leaves native production BM25 ranks unchanged."""
    baseline_run, evaluations_by_weight = experiment.run_filename_weight_calibration(
        repository_root=Path.cwd(),
        weights=(0.0, 0.25),
    )
    zero_weight_evaluations = dict(evaluations_by_weight)[0.0]
    payload = experiment.filename_weight_report_payload(
        baseline_run=baseline_run,
        evaluations_by_weight=evaluations_by_weight,
    )

    assert [item.relevant_ranks for item in zero_weight_evaluations] == [
        tuple(
            (item.address, item.rank) for item in baseline.retrieved_relevant_resources
        )
        for baseline in baseline_run.evaluations
    ]
    assert payload["schema"] == "devtools-filename-weight-bm25-calibration-v1"
    configuration = payload["configuration"]
    weights = payload["weights"]
    assert isinstance(configuration, dict)
    assert isinstance(weights, list)
    assert configuration["weights"] == [0.0, 0.25]


def test_real_repository_comparison_is_paired_and_writes_only_selected_report(
    tmp_path: Path,
) -> None:
    """All variants share one production benchmark realization and case set."""
    baseline_run, comparisons = experiment.run_comparison(repository_root=Path.cwd())
    payload = experiment.report_payload(
        baseline_run=baseline_run,
        comparisons=comparisons,
    )
    report_path = tmp_path / "address-comparison.json"
    experiment.write_report(path=report_path, payload=payload)

    persisted = json.loads(report_path.read_text(encoding="utf-8"))
    assert len(comparisons) == _EXPECTED_CASE_COUNT
    assert [item.name for item in comparisons] == [
        item.name for item in baseline_run.cases
    ]
    assert persisted["schema"] == "devtools-address-lexical-bm25-comparison-v1"
    assert persisted["identified_state"]["corpus_id"] == str(baseline_run.corpus.id)
    assert persisted["configuration"]["bm25"] == {"k1": 1.2, "b": 0.75}
    assert "content_bm25_score" in persisted["configuration"]["combination"]
