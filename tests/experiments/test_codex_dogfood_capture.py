# Copyright (c) 2026
# ruff: noqa: D103
"""Advisory capture of production retrieval without Selection or Codex execution."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
)
from devtools.context.retrieval.composition import LexicalStructuralResourceInventory
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.codex_dogfood.capture import (
    CodexDogfoodAgentObservation,
    CodexDogfoodCase,
    CodexDogfoodLexicalInventory,
    capture_codex_dogfood_retrieval,
    render_codex_dogfood_orientation,
)
from tests.context.retrieval.test_composition import _lexical
from tests.context.retrieval.test_structural import _facts


def _case(tmp_path: Path) -> CodexDogfoodCase:
    snapshot, relation, references, membership = _facts(tmp_path)
    lexical = _lexical(tmp_path, snapshot)
    return CodexDogfoodCase(
        snapshot=snapshot,
        index=lexical.index,
        full_prompt="Please update target and validate its consumer call",
        short_information_need="Locate target implementation",
        seed_origins=((RepositoryResourceAddress("consumer.py"), "named in task"),),
        imports=(relation,),
        references=references,
        memberships=(membership,),
    )


def test_capture_preserves_comparable_query_arms_and_all_native_supports(
    tmp_path: Path,
) -> None:
    case = _case(tmp_path)
    capture = capture_codex_dogfood_retrieval(case)
    full = capture.full_prompt_inventory
    short = capture.short_need_inventory
    assert isinstance(full, LexicalStructuralResourceInventory)
    assert isinstance(short, LexicalStructuralResourceInventory)
    assert full.lexical_result.query.text == case.full_prompt
    assert short.lexical_result.query.text == case.short_information_need
    assert full.lexical_result.index is short.lexical_result.index is case.index
    assert full.lexical_result.settings == short.lexical_result.settings
    assert full.lexical_result.maximum_results == short.lexical_result.maximum_results
    assert full.lexical_result.maximum_results == case.lexical_work_bound
    assert full.structural_result is short.structural_result
    assert full.purpose == short.purpose == case.short_information_need
    assert full.structural_result.request.seed_resources == (
        RepositoryResourceAddress("consumer.py"),
    )
    supports = tuple(
        support
        for entry in full.resources
        for support in entry.structural_supports
    )
    assert any(support.fact is case.imports[0] for support in supports)
    assert any(
        support.fact is reference
        for support in supports
        for reference in case.references
    )
    assert capture.orientation_addresses == tuple(
        sorted(
            {
                entry.resource.address
                for result in (full, short)
                for entry in result.resources
            },
            key=str,
        ),
    )
    assert capture == capture_codex_dogfood_retrieval(case)
    orientation = render_codex_dogfood_orientation(capture)
    assert "not a sufficiency claim" in orientation
    assert "Search and open any additional" in orientation
    assert "full-prompt lexical rank" in orientation
    assert "short-need lexical rank" in orientation
    assert "RI " in orientation


def test_zero_seed_capture_keeps_both_native_lexical_arms(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = replace(_case(tmp_path), seed_origins=())

    def forbid_structural(*_args: object, **_kwargs: object) -> None:
        msg = "Zero-seed capture must not invoke structural retrieval or composition."
        raise AssertionError(msg)

    monkeypatch.setattr(
        "experiments.codex_dogfood.capture.retrieve_python_direct_structural_resources",
        forbid_structural,
    )
    monkeypatch.setattr(
        "experiments.codex_dogfood.capture.compose_lexical_structural_resource_evidence",
        forbid_structural,
    )
    capture = capture_codex_dogfood_retrieval(case)
    full = capture.full_prompt_inventory
    short = capture.short_need_inventory
    assert isinstance(full, CodexDogfoodLexicalInventory)
    assert isinstance(short, CodexDogfoodLexicalInventory)
    for inventory, query in (
        (full, case.full_prompt),
        (short, case.short_information_need),
    ):
        assert inventory.snapshot_id == case.snapshot.id
        assert inventory.purpose == case.short_information_need
        assert inventory.lexical_result == retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=query),
            index=case.index,
            maximum_results=case.lexical_work_bound,
            settings=case.lexical_settings,
        )
        assert inventory.lexical_result.index is case.index
        assert inventory.lexical_result.settings is case.lexical_settings
        assert tuple(entry.resource.address for entry in inventory.resources) == tuple(
            sorted((entry.resource.address for entry in inventory.resources), key=str),
        )
        assert all(
            entry.lexical_match
            is inventory.lexical_result.matches[entry.lexical_rank - 1]
            for entry in inventory.resources
        )
    assert capture.orientation_addresses == tuple(
        sorted(
            {
                entry.resource.address
                for result in (full, short)
                for entry in result.resources
            },
            key=str,
        ),
    )
    orientation = render_codex_dogfood_orientation(capture)
    assert "full-prompt lexical rank" in orientation
    assert "short-need lexical rank" in orientation
    assert "RI " not in orientation


def test_capture_rejects_stale_lexical_observation(tmp_path: Path) -> None:
    case = _case(tmp_path)
    assert all(
        match.document_statistics.analysis.document.resource.address
        != RepositoryResourceAddress("unrelated.py")
        for query in (case.full_prompt, case.short_information_need)
        for match in retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=query),
            index=case.index,
            maximum_results=case.lexical_work_bound,
            settings=case.lexical_settings,
        ).matches
    )
    unmatched = next(
        resource for resource in case.snapshot.resources
        if resource.address == RepositoryResourceAddress("unrelated.py")
    )
    changed = replace(
        unmatched,
        content_identity=ContentIdentity("0" * 64),
    )
    stale = replace(
        case.snapshot,
        resources=tuple(
            changed if resource is unmatched else resource
            for resource in case.snapshot.resources
        ),
    )
    for seeds in (case.seed_origins, ()):
        with pytest.raises(ValueError, match="differs from the supplied snapshot"):
            capture_codex_dogfood_retrieval(
                replace(
                    case,
                    snapshot=stale,
                    seed_origins=seeds,
                    imports=(),
                    references=(),
                    memberships=(),
                ),
            )


def test_case_keeps_observation_separate(tmp_path: Path) -> None:
    case = _case(tmp_path)
    with pytest.raises(ValueError, match="origin"):
        replace(case, seed_origins=((RepositoryResourceAddress("consumer.py"), ""),))
    observed = CodexDogfoodAgentObservation(
        searches=("rg target src",),
        opened_resources=(RepositoryResourceAddress("consumer.py"),),
        modified_resources=(),
        validation_resources=(),
        task_success=None,
        validation_success=None,
        observation_source="manual Codex transcript review; incomplete file reads",
    )
    assert observed.bytes_read is None
    assert observed.opened_resources != observed.modified_resources
    assert not hasattr(observed, "required_resources")
