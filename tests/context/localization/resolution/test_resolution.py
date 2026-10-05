# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Explicit judgments, exact evidence lineage and downstream witness promotion."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization import (
    Disposition,
    LocalizationAssessment,
    LocalizationEvidenceReference,
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
    SatisfactionCriterion,
    TaskProvenance,
    WitnessSet,
    assess_localization_readiness,
)
from devtools.context.localization.association import (
    CandidateWitnessHypothesis,
    CandidateWitnessMember,
    GeneratedWitnessHypothesisIdentity,
    LexicalMatchSupport,
    WitnessHypothesisFamilyIdentity,
    WitnessHypothesisIdentity,
    build_candidate_witness_view,
)
from devtools.context.localization.generation import (
    WitnessGenerationPlan,
    generate_witness_hypotheses,
)
from devtools.context.localization.grounding import ResourceAddressLocator
from devtools.context.localization.resolution import (
    CandidateHypothesisResolution,
    CandidateMemberResolution,
    PromotedWitnessHypothesis,
    WitnessResolutionView,
    promote_supported_hypothesis,
)
from devtools.context.localization.resolution import (
    HypothesisResolutionDisposition as H,
)
from devtools.context.localization.resolution import (
    MemberResolutionDisposition as M,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import RepositoryResourceAddress as Address
from devtools.context.repository.snapshot import RepositorySnapshotId
from tests.context.localization.association.test_hypothesis import (
    _frame,
    _hypothesis,
    _member,
    _view,
)
from tests.context.localization.generation.test_generation import (
    _frame as _generation_frame,
)
from tests.context.localization.generation.test_generation import (
    _ground,
    _recipe,
)
from tests.context.localization.generation.test_generation import (
    _member as _recipe_member,
)
from tests.context.localization.generation.test_imports import (
    _fixture as _imports_fixture,
)
from tests.context.localization.generation.test_imports import (
    _run as _imports_run,
)
from tests.context.localization.generation.test_references import (
    _fixture as _references_fixture,
)
from tests.context.localization.generation.test_references import (
    _run as _references_run,
)
from tests.context.localization.test_lexical import _execute, _inputs

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.localization.association import CandidateWitnessView


def _decision(
    candidates: CandidateWitnessView,
    hypothesis: CandidateWitnessHypothesis,
    member: CandidateWitnessMember,
    disposition: M = M.SUPPORTED,
) -> CandidateMemberResolution:
    supports = (*member.lexical, *member.roles, *member.routed, *member.structural)
    return CandidateMemberResolution(
        candidates,
        hypothesis,
        member,
        disposition,
        candidates.task.obligations[0].satisfaction,
        "Caller establishes the named criterion, or records an incompatible fact",
        "Explicit inspection of retained native evidence",
        "test-caller",
        TaskProvenance("inspection-decision", explanation="explicit caller judgment"),
        tuple(
            LocalizationEvidenceReference(
                support,
                candidates.snapshot.repository_id,
                candidates.snapshot.id,
            )
            for support in supports
        ),
    )


def test_partial_view_and_explicit_dispositions() -> None:
    frame = _frame()
    first = _hypothesis(
        frame, members=(_member(frame), _member(frame, "docs/alpha.md"))
    )
    second = _hypothesis(frame, key="competitor")
    candidates = _view(frame, second, first)
    empty = WitnessResolutionView(candidates)
    assert empty.hypotheses == empty.completely_supported == empty.unresolved == ()
    assert empty.contradicted == ()
    assert empty.supported_obligations == ()
    assert empty.unrecorded == candidates.hypotheses
    assert empty.for_hypothesis(first.identity) is None
    assert empty.for_member(first.identity, first.members[0].target) is None
    with pytest.raises(ValueError, match="recorded"):
        promote_supported_hypothesis(empty, first.identity)

    supported = _decision(candidates, first, first.members[0])
    partial = WitnessResolutionView(candidates, (supported,))
    resolution = partial.for_hypothesis(first.identity)
    assert resolution is not None
    assert resolution.disposition is H.UNRESOLVED
    assert resolution.unrecorded_members == (first.members[1],)
    assert partial.unrecorded == (second,)
    assert partial.for_member(first.identity, first.members[0].target) is supported
    assert partial.for_obligation(first.identity.obligation) == (resolution,)
    assert supported.task == frame[0].identity
    assert supported.obligation == first.identity.obligation
    assert supported.repository_id == frame[1].repository_id
    assert supported.snapshot_id == frame[1].id

    for disposition, aggregate in (
        (M.SUPPORTED, H.COMPLETELY_SUPPORTED),
        (M.UNRESOLVED, H.UNRESOLVED),
        (M.ABSTAINED, H.UNRESOLVED),
        (M.CONTRADICTED, H.CONTRADICTED),
    ):
        other = _decision(candidates, first, first.members[1], disposition)
        view = WitnessResolutionView(candidates, (other, supported))
        resolved = view.for_hypothesis(first.identity)
        assert resolved is not None
        assert resolved.disposition is aggregate
        assert resolved.unrecorded_members == ()
        assert resolved.members == (supported, other)
        assert view.candidates is candidates
        assert view.for_hypothesis(second.identity) is None
        assert candidates.hypotheses == _view(frame, first, second).hypotheses
        if aggregate is H.COMPLETELY_SUPPORTED:
            assert view.completely_supported == (resolved,)
            assert view.supported_obligations == (first.identity.obligation,)
        else:
            with pytest.raises(ValueError, match="completely supported"):
                promote_supported_hypothesis(view, first.identity)
            assert (
                view.contradicted if aggregate is H.CONTRADICTED else view.unresolved
            ) == (resolved,)

    unresolved = replace(supported, disposition=M.UNRESOLVED, basis=())
    abstained = replace(supported, disposition=M.ABSTAINED, basis=())
    assert unresolved.basis == abstained.basis == ()
    assert unresolved.member is abstained.member is first.members[0]


def test_competition_is_independent_and_order_is_deterministic() -> None:
    frame = _frame()
    first, second = _hypothesis(frame), _hypothesis(frame, key="b")
    candidates = _view(frame, first, second)
    supported = _decision(candidates, first, first.members[0])
    unresolved = _decision(candidates, second, second.members[0], M.UNRESOLVED)
    view = WitnessResolutionView(candidates, (unresolved, supported))
    assert view == WitnessResolutionView(candidates, (supported, unresolved))
    assert len(view.for_obligation(first.identity.obligation)) == 2
    assert len(view.completely_supported) == len(view.unresolved) == 1
    assert len(candidates.hypotheses) == 2
    assert not hasattr(view, "rank")
    assert not hasattr(view, "score")
    assert not hasattr(view, "assessment")
    assert not hasattr(view, "readiness")
    assert not hasattr(view, "acquisition_requests")


def test_foreign_scope_and_same_target_support_substitution() -> None:
    frame = _frame()
    first, second = _hypothesis(frame), _hypothesis(frame, key="competitor")
    candidates = _view(frame, first, second)
    record = _decision(candidates, first, first.members[0])
    assert first.members[0].target == second.members[0].target
    with pytest.raises(ValueError, match="exact attached"):
        replace(record, hypothesis=second, member=second.members[0])
    for obligation in (
        LocalizationObligationIdentity(frame[0].identity, "foreign-obligation"),
        LocalizationObligationIdentity(
            LocalizationTaskIdentity("foreign-task"), "implementation"
        ),
    ):
        foreign = replace(first, identity=WitnessHypothesisIdentity(obligation, "a"))
        invalid = replace(candidates, hypotheses=(foreign,))
        with pytest.raises(ValueError, match="unknown obligation"):
            WitnessResolutionView(invalid)
        with pytest.raises(ValueError, match="criterion"):
            replace(record, candidates=invalid, hypothesis=foreign)


def test_basis_validation_and_record_guards() -> None:
    frame = _frame()
    member = _member(frame, role=True, routed=True)
    hypothesis = _hypothesis(frame, members=(member,))
    candidates = _view(frame, hypothesis)
    record = _decision(candidates, hypothesis, member)
    assert replace(record, basis=tuple(reversed(record.basis))) == record
    assert len(record.basis) > 1
    for disposition in (M.SUPPORTED, M.CONTRADICTED):
        with pytest.raises(ValueError, match="explicit evidence"):
            replace(record, disposition=disposition, basis=())
    with pytest.raises(TypeError, match="explicit disposition"):
        replace(record, disposition="supported")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="claim, reason"):
        replace(record, caller=" ")
    with pytest.raises(ValueError, match="claim, reason"):
        replace(record, claim=" ")
    with pytest.raises(ValueError, match="claim, reason"):
        replace(record, reason=" ")
    with pytest.raises(ValueError, match="criterion"):
        replace(record, criterion=SatisfactionCriterion("other", "other claim"))
    with pytest.raises(ValueError, match="hypothesis is foreign"):
        replace(record, hypothesis=replace(hypothesis))
    with pytest.raises(ValueError, match="member is foreign"):
        replace(record, member=replace(member))
    with pytest.raises(ValueError, match="repeats native"):
        replace(record, basis=(record.basis[0], record.basis[0]))
    foreign_repo = RepositoryId.parse("00000000-0000-4000-8000-000000000002")
    for reference in (
        replace(record.basis[0], repository_id=foreign_repo),
        replace(record.basis[0], snapshot_id=RepositorySnapshotId("b" * 64)),
    ):
        with pytest.raises(ValueError, match="repository/snapshot"):
            replace(record, basis=(reference,))
    forged = replace(record.basis[0], identity=replace(member.lexical[0]))
    with pytest.raises(ValueError, match="exact attached"):
        replace(record, basis=(forged,))
    other = _member(frame, "docs/alpha.md")
    with pytest.raises(ValueError, match="exact attached"):
        replace(record, basis=(replace(record.basis[0], identity=other.lexical[0]),))


def test_view_and_aggregate_frame_guards() -> None:
    frame = _frame()
    first, second = _hypothesis(frame), _hypothesis(frame, key="b")
    candidates = _view(frame, first, second)
    record = _decision(candidates, first, first.members[0])
    with pytest.raises(ValueError, match="nonempty"):
        WitnessResolutionView(replace(candidates, hypotheses=()))
    with pytest.raises(ValueError, match="canonical"):
        WitnessResolutionView(replace(candidates, hypotheses=(second, first)))
    with pytest.raises(ValueError, match="different or stale"):
        WitnessResolutionView(replace(candidates), (record,))
    with pytest.raises(ValueError, match="repeats a member"):
        WitnessResolutionView(candidates, (record, record))
    with pytest.raises(ValueError, match="exact frame"):
        CandidateHypothesisResolution(candidates, first, ())
    with pytest.raises(ValueError, match="exact frame"):
        CandidateHypothesisResolution(replace(candidates), first, (record,))
    with pytest.raises(ValueError, match="exact frame"):
        CandidateHypothesisResolution(candidates, second, (record,))
    with pytest.raises(ValueError, match="repeats a member"):
        CandidateHypothesisResolution(candidates, first, (record, record))
    view = WitnessResolutionView(candidates)
    with pytest.raises(ValueError, match="no such hypothesis"):
        view.for_hypothesis(
            WitnessHypothesisIdentity(first.identity.obligation, "foreign")
        )
    with pytest.raises(ValueError, match="foreign or stale member"):
        view.for_member(first.identity, _member(frame, "docs/alpha.md").target)
    with pytest.raises(ValueError, match="no such admitted family"):
        view.for_family(
            WitnessHypothesisFamilyIdentity(first.identity.obligation, "foreign")
        )

    # Raw association dataclasses cannot bypass the validated view boundary.
    foreign_task = replace(frame[0], provenance=TaskProvenance("different-task-frame"))
    with pytest.raises(ValueError, match="association frame"):
        WitnessResolutionView(replace(candidates, task=foreign_task))
    with pytest.raises(ValueError, match="association frame"):
        WitnessResolutionView(
            replace(
                candidates,
                snapshot=replace(frame[1], id=RepositorySnapshotId("b" * 64)),
            )
        )
    with pytest.raises(ValueError, match="association frame"):
        WitnessResolutionView(
            replace(
                candidates,
                snapshot=replace(
                    frame[1],
                    repository_id=RepositoryId.parse(
                        "00000000-0000-4000-8000-000000000002"
                    ),
                ),
            )
        )
    invalid = replace(
        candidates, task=replace(frame[0], obligations=(frame[0].obligations[1],))
    )
    with pytest.raises(ValueError, match="criterion"):
        replace(record, candidates=invalid)


def test_lexical_only_promotion_and_existing_readiness_flow() -> None:
    task, snapshot, index = _inputs()
    targets = (
        snapshot.resource_at(Address("docs/alpha.md")),
        snapshot.resource_at(Address("src/alpha.py")),
    )
    obligation = replace(
        task.obligations[0], witness_alternatives=(WitnessSet(targets),)
    )
    task = replace(task, obligations=(obligation,))
    acquisition = _execute(
        task,
        snapshot,
        index,
        purpose="generic witnesses",
        full_query="Obligation",
        queries=(),
    )
    members = tuple(
        CandidateWitnessMember(
            target,
            "caller associated native lexical evidence",
            tuple(
                LexicalMatchSupport(None, rank, match)
                for rank, match in enumerate(acquisition.full_task_retrieval.matches, 1)
                if match.document_statistics.analysis.document.resource == target
            ),
        )
        for target in targets
    )
    hypothesis = CandidateWitnessHypothesis(
        WitnessHypothesisIdentity(obligation.identity, "lexical"), members
    )
    candidates = build_candidate_witness_view(
        task=task, snapshot=snapshot, hypotheses=(hypothesis,), acquisition=acquisition
    )
    records = tuple(
        _decision(candidates, hypothesis, member) for member in hypothesis.members
    )
    open_assessment = LocalizationAssessment(
        obligation.identity, snapshot.repository_id, snapshot.id, Disposition.OPEN
    )
    before = assess_localization_readiness(
        task=task,
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        assessments=(open_assessment,),
    )
    view = WitnessResolutionView(candidates, tuple(reversed(records)))
    promotion = promote_supported_hypothesis(view, hypothesis.identity)
    assert promotion.witness_set == obligation.witness_alternatives[0]
    for witness, record in zip(promotion.supported_witnesses, records, strict=True):
        assert witness.target == record.member.target
        assert witness.evidence[:-1] == record.basis
        assert witness.evidence[-1].identity is record
        assert hash(witness.evidence[-1].identity)
    assert (
        assess_localization_readiness(
            task=task,
            repository_id=snapshot.repository_id,
            snapshot_id=snapshot.id,
            assessments=(open_assessment,),
        )
        == before
    )
    assert not before.is_ready
    updated = replace(
        open_assessment,
        disposition=Disposition.RESOLVED,
        supported_witnesses=promotion.supported_witnesses,
    )
    after = assess_localization_readiness(
        task=task,
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        assessments=(updated,),
    )
    assert after.is_ready
    assert open_assessment.disposition is Disposition.OPEN
    # A forged raw frame cannot promote through the public value constructor.
    stale = replace(candidates, acquisition=None)
    stale_records = tuple(replace(record, candidates=stale) for record in records)
    with pytest.raises(ValueError, match="Lexical support requires"):
        PromotedWitnessHypothesis(
            CandidateHypothesisResolution(stale, hypothesis, stale_records)
        )


@pytest.mark.parametrize("channel", ["owner", "reference", "import"])
def test_structural_channels_and_independent_branch_children(
    tmp_path: Path, channel: str
) -> None:
    if channel == "owner":
        task, snapshot = _generation_frame()
        grounding = _ground(
            task, snapshot, ResourceAddressLocator(Address("src/devtools/alpha.py"))
        )
        generated = generate_witness_hypotheses(
            WitnessGenerationPlan(
                task, snapshot, (_recipe(task, _recipe_member(grounding)),)
            )
        )
    elif channel == "reference":
        generated = _references_run(_references_fixture(tmp_path))
    else:
        generated = _imports_run(
            _imports_fixture(tmp_path, "import pkg.target\nimport pkg.other\n")
        )
    candidates = generated.association
    assert len(candidates.hypotheses) >= 1
    hypothesis = candidates.hypotheses[0]
    record = _decision(candidates, hypothesis, hypothesis.members[0])
    view = WitnessResolutionView(candidates, (record,))
    assert view.completely_supported[0].disposition is H.COMPLETELY_SUPPORTED
    assert (
        promote_supported_hypothesis(view, hypothesis.identity)
        .supported_witnesses[0]
        .evidence[0]
        .identity
        is hypothesis.members[0].structural[0]
    )
    if channel != "owner":
        assert len(candidates.hypotheses) > 1
        assert isinstance(hypothesis.identity, GeneratedWitnessHypothesisIdentity)
        family = generated.parent_family(hypothesis.identity)
        assert family is not None
        assert isinstance(family.recipe.identity, WitnessHypothesisFamilyIdentity)
        assert view.for_family(family.recipe.identity) == view.completely_supported
        sibling = candidates.hypotheses[1]
        assert view.for_hypothesis(sibling.identity) is None
        assert sibling in view.unrecorded
        with pytest.raises(ValueError, match="exact attached"):
            replace(record, hypothesis=sibling, member=sibling.members[0])
