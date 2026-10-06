# Copyright (c) 2026
# ruff: noqa: COM812, PT011 -- native fixture and grouped boundary rejection

"""Native evidence projections qualify frame identity without semantic inference."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization.grounding.contract import (
    AnchorGrounding,
    AnchorGroundingCandidate,
    AnchorGroundingDisposition,
    AnchorGroundingRequest,
    GroundingResolver,
    ResourceAddressLocator,
)
from devtools.context.localization.identity import (
    LocalizationAnchorIdentity,
    TaskProvenance,
)
from devtools.context.localization.roles import derive_repository_role_evidence
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.context.retrieval.structural import (
    PythonDirectStructuralResourceCandidate,
    PythonDirectStructuralResourceEvidence,
)
from experiments.retrieval_diagnostics.adapters import fields, from_rows
from experiments.retrieval_diagnostics.mechanics import Mechanics
from experiments.retrieval_diagnostics.supports import exact_resource, role, structural
from tests.context.retrieval.lexical._helpers import _collection, _document
from tests.context.retrieval.test_structural import _facts
from tests.experiments.retrieval_diagnostics.helpers import OBLIGATION, capture

if TYPE_CHECKING:
    from pathlib import Path


def test_recomputed_missing_statistics_equal_retained_native_fields() -> None:
    """Only frozen JSON needs deterministic field reconstruction, not new ranking."""
    docs = (("a.py", "CandidateMemberResolution plain"), ("b.py", "plain"))
    collection = _collection(tuple(_document(a, t) for a, t in docs))
    for expanded in (False, True):
        c = capture(docs, "plain", expanded=expanded)
        assert fields(collection, c.configuration) == c.fields
        snapshot = RepositorySnapshot(c.frame.snapshot, c.frame.repository, c.resources)
        r = c.rows[0]
        raw = {
            "address": r.resource.address.value,
            "content_identity": r.resource.content_identity.value,
            "score": r.score,
            "rank": 1,
            "filename_weight": c.configuration.filename_weight,
        }
        for name in ("content", "filename"):
            raw[name + "_terms"] = [
                {
                    "term": t.term,
                    "tf": t.tf,
                    "df": t.df,
                    "length": t.length,
                    "average_length": t.average_length,
                    "idf": t.idf,
                    "contribution": t.contribution,
                }
                for t in r.terms
                if t.field == name
            ]
        for broken in (
            {**raw, "content_identity": "b" * 64},
            {**raw, "filename_weight": 9},
        ):
            with pytest.raises(ValueError):
                from_rows(
                    snapshot,
                    collection,
                    "query",
                    c.query,
                    c.query_terms,
                    [broken],
                    c.configuration,
                    c.fields,
                    complete=False,
                )
        with pytest.raises(ValueError):
            from_rows(
                replace(
                    snapshot, repository_id=_document("a.py", "").repository_id.new()
                ),
                collection,
                "query",
                c.query,
                c.query_terms,
                [],
                c.configuration,
                c.fields,
                complete=False,
            )


def test_native_role_exact_and_structural_references_preserve_qualification(
    tmp_path: Path,
) -> None:
    """Positive support is attached, not promoted to gold relational necessity."""
    c = capture((("a.py", "plain"), ("b.py", "other")))
    resource = c.resources[0]
    snapshot = RepositorySnapshot(c.frame.snapshot, c.frame.repository, c.resources)
    evidence = derive_repository_role_evidence(snapshot).for_resource(resource.address)[
        0
    ]
    ref = role(c, evidence)
    assert ref.identity == evidence.identity
    with pytest.raises(ValueError):
        role(
            c, replace(evidence, snapshot_id=replace(c.frame.snapshot, value="b" * 64))
        )
    task = OBLIGATION.task
    request = AnchorGroundingRequest(
        task,
        LocalizationAnchorIdentity(task, "anchor"),
        c.frame.repository,
        c.frame.snapshot,
        ResourceAddressLocator(resource.address),
        TaskProvenance("test"),
    )
    grounding = AnchorGrounding(
        request,
        AnchorGroundingDisposition.RESOLVED,
        GroundingResolver.SNAPSHOT_RESOURCE_AT,
        (AnchorGroundingCandidate(resource, resource),),
        (resource,),
        None,
        "Exact native lookup",
    )
    exact = exact_resource(c, grounding)
    assert exact[0].kind == "EXACT"
    with pytest.raises(ValueError):
        exact_resource(
            c, replace(grounding, resolver=GroundingResolver.PYTHON_MODULE_LOOKUP)
        )
    outside = _document("outside.py", "plain").resource
    with pytest.raises(ValueError):
        exact_resource(
            c,
            replace(
                grounding, candidates=(AnchorGroundingCandidate(outside, outside),)
            ),
        )
    native_snapshot, relation, _references, _membership = _facts(tmp_path)
    native_resource = native_snapshot.resources[0]
    native_c = replace(
        c,
        frame=replace(
            c.frame,
            repository=native_snapshot.repository_id,
            snapshot=native_snapshot.id,
        ),
        resources=native_snapshot.resources,
    )
    candidate = PythonDirectStructuralResourceCandidate(
        native_snapshot.id,
        native_resource.address,
        (
            PythonDirectStructuralResourceEvidence(
                native_resource.address, "import-to-target", relation
            ),
        ),
    )
    s = structural(native_c, candidate)
    assert s[0].identity == relation.identity
    assert s[0].kind == "STRUCTURAL"
    with pytest.raises(ValueError):
        structural(c, candidate)
    with pytest.raises(ValueError):
        Mechanics(c).overtaker(resource, outside)
