# Copyright (c) 2026
"""Tests for the experiment-owned identifier-aware lexical comparison."""

from __future__ import annotations

import json
from pathlib import Path

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments import retrieval_identifier as experiment

_EXPANDED_IDENTIFIER_LENGTH = 4
_REPOSITORY_DOCUMENT_FREQUENCY = 2
_SECOND_RANK_RECIPROCAL = 0.5
_BENCHMARK_CASE_COUNT = 13


def test_identifier_expansion_preserves_original_and_has_explicit_boundaries() -> None:
    """Identifier expansion preserves baseline evidence before derived components."""
    assert experiment.expand_identifier_terms(
        observed_text="RepositoryTextCorpus",
    ) == ("repositorytextcorpus", "repository", "text", "corpus")
    assert experiment.expand_identifier_terms(
        observed_text="repository_text_corpus",
    ) == ("repository_text_corpus", "repository", "text", "corpus")
    assert experiment.expand_identifier_terms(
        observed_text="parseHTTPResponse",
    ) == ("parsehttpresponse", "parse", "http", "response")
    assert experiment.expand_identifier_terms(
        observed_text="HTTPClient",
    ) == ("httpclient", "http", "client")
    assert experiment.expand_identifier_terms(
        observed_text="version2Parser",
    ) == ("version2parser", "version", "2", "parser")
    assert experiment.expand_identifier_terms(observed_text="BM25") == (
        "bm25",
        "bm",
        "25",
    )
    assert experiment.expand_identifier_terms(observed_text="Qwen3") == (
        "qwen3",
        "qwen",
        "3",
    )
    assert experiment.expand_identifier_terms(observed_text="__init__") == (
        "__init__",
        "init",
    )


def test_query_and_document_expansion_are_symmetric_and_preserve_spans() -> None:
    """The experiment gives no hidden lexicalization advantage to query text."""
    document_observations = experiment.analyze_identifier_text(
        text="RepositoryTextCorpus",
    )
    query_observations = experiment.analyze_identifier_query(
        text="RepositoryTextCorpus",
    )

    assert query_observations == document_observations
    assert [item.normalized_term for item in document_observations] == [
        "repositorytextcorpus",
        "repository",
        "text",
        "corpus",
    ]
    assert [item.origin for item in document_observations] == [
        "original",
        "component",
        "component",
        "component",
    ]
    assert {(item.start, item.end) for item in document_observations} == {(0, 20)}


def test_expansion_changes_only_experimental_term_statistics() -> None:
    """Expanded components change TF, length, and DF while baseline stays exact."""
    documents = (
        experiment.IdentifierExperimentDocument(
            RepositoryResourceAddress("target.py"),
            "RepositoryTextCorpus",
        ),
        experiment.IdentifierExperimentDocument(
            RepositoryResourceAddress("other.md"),
            "repository text",
        ),
    )

    baseline = experiment.build_identifier_index(
        documents=documents,
        identifier_aware=False,
    )
    expanded = experiment.build_identifier_index(
        documents=documents,
        identifier_aware=True,
    )

    assert baseline.document_statistics[0].document_length == 1
    assert (
        expanded.document_statistics[0].document_length == _EXPANDED_IDENTIFIER_LENGTH
    )
    assert dict(expanded.document_statistics[0].term_frequencies)["repository"] == 1
    assert (
        dict(expanded.document_frequency)["repository"]
        == _REPOSITORY_DOCUMENT_FREQUENCY
    )
    assert dict(expanded.document_frequency)["repositorytextcorpus"] == 1


def test_controlled_cases_show_identifier_improvements_and_distractor_limit() -> None:
    """The focused fixtures prove both expansion's benefit and its limitation."""
    cases = {case.name: case for case in experiment.controlled_cases()}

    for name in ("pascal-case", "snake-case", "camel-case", "acronym-and-digits"):
        assert cases[name].baseline.hit_at_k is False
        assert cases[name].experimental.hit_at_k is True
        assert cases[name].newly_recovered == (RepositoryResourceAddress("target.py"),)

    assert cases["prose-only"].baseline.reciprocal_rank == 1.0
    assert cases["prose-only"].experimental.reciprocal_rank == 1.0
    assert cases["lexical-distractor"].baseline.hit_at_k is False
    assert (
        cases["lexical-distractor"].experimental.reciprocal_rank
        == _SECOND_RANK_RECIPROCAL
    )


def test_real_repository_comparison_is_paired_and_report_is_caller_selected(
    tmp_path: Path,
) -> None:
    """Both variants use one observed corpus and preserve every baseline case."""
    baseline_run, comparisons = experiment.run_comparison(repository_root=Path.cwd())
    payload = experiment.report_payload(
        baseline_run=baseline_run,
        comparisons=comparisons,
    )
    report_path = tmp_path / "identifier-comparison.json"
    experiment.write_report(path=report_path, payload=payload)

    persisted = json.loads(report_path.read_text(encoding="utf-8"))
    assert len(comparisons) == _BENCHMARK_CASE_COUNT
    assert [item.name for item in comparisons] == [
        case.name for case in baseline_run.cases
    ]
    assert persisted["schema"] == "devtools-identifier-aware-bm25-comparison-v1"
    assert persisted["identified_state"]["snapshot_id"] == str(baseline_run.snapshot.id)
    assert persisted["constant_configuration"]["bm25"] == {"k1": 1.2, "b": 0.75}
    assert persisted["constant_configuration"]["path_or_package_scoring"] is False
    assert persisted["aggregate"]["baseline"]["hit_rate_at_k"] == (
        baseline_run.summary.hit_rate_at_k
    )
