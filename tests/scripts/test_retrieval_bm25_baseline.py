# Copyright (c) 2026
# ruff: noqa: INP001
"""Tests for the bounded real-repository content-only BM25 benchmark script."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from devtools.context.repository.discovery import RepositoryResourceDiscovery
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import ResolvedPath

_DRIVER_PATH = Path("scripts/retrieval_bm25_baseline.py")
_REPOSITORY_ID = RepositoryId.parse("00000000-0000-4000-8000-000000000009")
_EXPECTED_CASE_COUNT = 13
_EXPECTED_RESULT_BOUND = 5
_REPORT_SCHEMA = "devtools-content-only-bm25-repository-benchmark-v1"

if TYPE_CHECKING:
    from types import ModuleType


@pytest.fixture
def driver() -> ModuleType:
    """Load the tracked script without promoting scripts to a library package."""
    specification = importlib.util.spec_from_file_location(
        "test_retrieval_bm25_baseline",
        _DRIVER_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def _discovery(*addresses: str) -> RepositoryResourceDiscovery:
    """Build one metadata-only discovery fixture for eligibility testing."""
    return RepositoryResourceDiscovery(
        repository_id=_REPOSITORY_ID,
        root=ResolvedPath(Path.cwd()),
        maximum_resource_count=20,
        maximum_traversal_entry_count=20,
        examined_entry_count=len(addresses),
        addresses=tuple(RepositoryResourceAddress(address) for address in addresses),
    )


@pytest.fixture
def benchmark_repository(driver: ModuleType, tmp_path: Path) -> Path:
    """Copy the manually judged resources into a small real filesystem fixture."""
    for case in driver.benchmark_cases():
        for address in case.relevant_resource_addresses:
            source = Path.cwd() / address.value
            destination = tmp_path / address.value
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                source.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
    return tmp_path


def test_selection_is_heterogeneous_and_uses_only_explicit_operational_rules(
    driver: ModuleType,
) -> None:
    """Selection includes configured text suffixes without classifying their content."""
    discovery = _discovery(
        ".venv/library.py",
        "assets/image.bin",
        "docs/guide.md",
        "pyproject.toml",
        "settings/config.yaml",
        "settings/config.yml",
        "settings/config.json",
        "src/feature.py",
        "scripts/retrieval_bm25_baseline.py",
    )

    selected = driver.select_benchmark_addresses(discovery=discovery)

    assert tuple(str(address) for address in selected) == (
        "docs/guide.md",
        "pyproject.toml",
        "settings/config.yaml",
        "settings/config.yml",
        "src/feature.py",
    )


def test_benchmark_reuses_the_production_pipeline_and_is_deterministic(
    driver: ModuleType,
    benchmark_repository: Path,
) -> None:
    """The real checkout produces explicit, rerunnable case and ranking evidence."""
    first = driver.run_benchmark(repository_root=benchmark_repository)
    second = driver.run_benchmark(repository_root=benchmark_repository)

    assert first.corpus.id == second.corpus.id
    assert (
        first.summary.evaluation_k,
        first.summary.hit_rate_at_k,
        first.summary.mean_recall_at_k,
        first.summary.mean_reciprocal_rank,
    ) == (
        second.summary.evaluation_k,
        second.summary.hit_rate_at_k,
        second.summary.mean_recall_at_k,
        second.summary.mean_reciprocal_rank,
    )
    assert tuple(
        tuple(
            match.document_statistics.analysis.document.resource.address
            for match in evaluation.retrieval_result.matches
        )
        for evaluation in first.evaluations
    ) == tuple(
        tuple(
            match.document_statistics.analysis.document.resource.address
            for match in evaluation.retrieval_result.matches
        )
        for evaluation in second.evaluations
    )
    assert len(first.cases) == _EXPECTED_CASE_COUNT
    assert len(first.documents.documents) == len(first.definition.selected_addresses)
    assert first.summary.evaluation_k == _EXPECTED_RESULT_BOUND
    assert all(
        len(evaluation.retrieval_result.matches) <= _EXPECTED_RESULT_BOUND
        for evaluation in first.evaluations
    )
    selected_addresses = set(first.definition.selected_addresses)
    assert all(
        address in selected_addresses
        for case in first.cases
        for address in case.relevant_resource_addresses
    )
    assert any(address.value.endswith(".py") for address in selected_addresses)
    assert any(address.value.endswith(".md") for address in selected_addresses)
    assert RepositoryResourceAddress("pyproject.toml") in selected_addresses


def test_report_payload_retains_native_case_evidence_and_writes_only_on_request(
    driver: ModuleType,
    benchmark_repository: Path,
    tmp_path: Path,
) -> None:
    """A caller-selected artifact preserves ground truth, rankings, and aggregates."""
    run = driver.run_benchmark(repository_root=benchmark_repository)
    payload = driver.report_payload(run=run)
    report_path = tmp_path / "baseline.json"

    driver.write_report(path=report_path, payload=payload)

    persisted = json.loads(report_path.read_text(encoding="utf-8"))
    assert persisted["schema"] == _REPORT_SCHEMA
    assert persisted["membership"]["selected_addresses"] == [
        str(address) for address in run.definition.selected_addresses
    ]
    assert len(persisted["cases"]) == len(run.cases)
    assert persisted["cases"][0]["designated_relevant_resources"] == [
        str(address) for address in run.cases[0].relevant_resource_addresses
    ]
    assert persisted["aggregate"]["mean_reciprocal_rank"] == (
        run.summary.mean_reciprocal_rank
    )
