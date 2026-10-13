# Copyright (c) 2026
# ruff: noqa: D103, S101, COM812, PLR2004 -- synthetic prospective rule fixtures
"""Design/evidence/ordinal tests; no selected-frame acquisition or gold.

The only Reference derivations below use an isolated three-file synthetic
snapshot. A ranks are constructed fixture inputs, never obtained by BM25.
"""

from __future__ import annotations

import asyncio
import io
import json
import tarfile
from dataclasses import replace
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references import (
    PythonDeclarationReferenceKnowledge,
    derive_python_declaration_references,
)
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.context.retrieval.lexical.analysis import (
    RepositoryTextLexicalCollectionAnalysis,
    RepositoryTextLexicalDocumentAnalysis,
)
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Match,
    RepositoryTextLexicalBm25RetrievalResult,
    RepositoryTextLexicalBm25Settings,
    RepositoryTextLexicalQuery,
)
from devtools.context.retrieval.lexical.index import RepositoryTextLexicalInvertedIndex
from devtools.context.retrieval.lexical.statistics import (
    RepositoryTextLexicalCorpusStatistics,
    RepositoryTextLexicalDocumentStatistics,
)
from devtools.core.paths import resolve_path
from experiments.codex_dogfood.case_0009.artifacts import (
    digest,
    git,
    json_bytes,
    put_text,
)
from experiments.structural_discrimination import freeze
from experiments.structural_discrimination.cases import CASES
from experiments.structural_discrimination.decision import (
    Label,
    case_category,
    classify_pair,
)
from experiments.structural_discrimination.evidence import annotate, prepare_references
from experiments.structural_discrimination.frames import public_cards
from experiments.structural_discrimination.protocol import PROTOCOL

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.repository.snapshot import RepositorySnapshot
    from experiments.structural_discrimination.evidence import AnnotatedLexicalSurface

type NativeFixture = tuple[
    RepositorySnapshot,
    tuple[PythonDeclarationReferenceKnowledge, ...],
    RepositoryTextLexicalBm25RetrievalResult,
]


@pytest.fixture
def native_fixture(
    tmp_path: Path,
) -> tuple[
    RepositorySnapshot,
    tuple[PythonDeclarationReferenceKnowledge, ...],
    RepositoryTextLexicalBm25RetrievalResult,
]:
    texts = {
        "source.py": (
            "from target import f\ndef local():\n    pass\nlocal()\nf()\nf()\n"
        ),
        "target.py": "def f():\n    pass\n",
        "other.md": "independent synthetic predecessor\n",
    }
    for address, text in texts.items():
        put_text(tmp_path / address, text)
    repository = Repository(RepositoryId.parse("00000000-0000-4000-8000-000000000031"))
    snapshot = observe_repository_resources(
        repository=repository,
        root=resolve_path(tmp_path),
        addresses=tuple(RepositoryResourceAddress(p) for p in texts),
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
    analysis = derive_python_declaration_references(
        snapshot,
        resource_address=RepositoryResourceAddress("source.py"),
        module_universe=universe,
        source_interpretations=tuple(
            i
            for i in universe.interpretations
            if str(i.resource.address) == "source.py"
        ),
    )
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=resolve_path(tmp_path),
        maximum_resource_count=10,
        maximum_traversal_entry_count=20,
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=tuple(r.address for r in snapshot.resources),
        ),
        snapshot=snapshot,
    )
    collection = represent_repository_text_corpus(corpus=corpus)
    analyses = tuple(
        RepositoryTextLexicalDocumentAnalysis(d, ()) for d in collection.documents
    )
    statistics = tuple(
        RepositoryTextLexicalDocumentStatistics(a, 0, ()) for a in analyses
    )
    corpus_statistics = RepositoryTextLexicalCorpusStatistics(
        RepositoryTextLexicalCollectionAnalysis(collection, analyses),
        statistics,
        (),
        len(statistics),
        0.0,
    )
    index = RepositoryTextLexicalInvertedIndex(corpus_statistics, ())
    by_address = {str(s.analysis.document.resource.address): s for s in statistics}
    # Artificial native-shaped order, explicitly no lexical query/scoring call.
    matches = tuple(
        RepositoryTextLexicalBm25Match(by_address[p], float(3 - rank), ())
        for rank, p in enumerate(("source.py", "other.md", "target.py"))
    )
    lexical = RepositoryTextLexicalBm25RetrievalResult(
        RepositoryTextLexicalQuery("synthetic", ()),
        index,
        RepositoryTextLexicalBm25Settings(),
        3,
        matches,
    )
    return snapshot, analysis.references, lexical


def scoped_annotation(
    native_fixture: NativeFixture,
) -> AnnotatedLexicalSurface:
    snapshot, references, lexical = native_fixture
    task = LocalizationTaskIdentity("synthetic-task")
    return annotate(
        prepare_references(snapshot, references),
        obligation=LocalizationObligationIdentity(task, "O1"),
        query=LocalizationQueryIdentity(task, "Q1"),
        purpose="synthetic need",
        lexical_result=lexical,
    )


def test_support_pair_native_identity_and_no_reorder(
    native_fixture: NativeFixture,
) -> None:
    surface = scoped_annotation(native_fixture)
    assert surface.lexical_result is native_fixture[2]
    assert len(surface.annotations) == 1
    target = surface.annotations[0]
    assert str(target.resource.address) == "target.py"
    assert target.a_rank == 3
    assert str(target.predecessor.address) == "other.md"
    assert target.best_source_rank == 1
    assert target.distinct_source_count == 1
    assert target.occurrence_count == 2
    assert all(
        s.direction == "reference-to-definition"
        for source in target.sources
        for s in source.supports
    )


def test_unsupported_rank1_self_and_ablation(native_fixture: NativeFixture) -> None:
    snapshot, references, lexical = native_fixture
    prepared = prepare_references(snapshot, references)
    assert prepared.self_reference_count == 1
    original = scoped_annotation(native_fixture)
    task = original.obligation.task
    ablated = annotate(
        prepare_references(snapshot, ()),
        obligation=original.obligation,
        query=original.query,
        purpose=original.purpose,
        lexical_result=lexical,
    )
    assert not ablated.annotations
    assert ablated.lexical_result is lexical
    reversed_lexical = replace(lexical, matches=tuple(reversed(lexical.matches)))
    reversed_surface = annotate(
        prepared,
        obligation=LocalizationObligationIdentity(task, "O1"),
        query=LocalizationQueryIdentity(task, "Q1"),
        purpose="same scope",
        lexical_result=reversed_lexical,
    )
    assert not reversed_surface.annotations


def test_native_duplicate_and_input_order_invariance(
    native_fixture: NativeFixture,
) -> None:
    snapshot, references, _ = native_fixture
    assert prepare_references(snapshot, references) == prepare_references(
        snapshot, tuple(reversed(references)) + references
    )


def test_graph_only_target_not_admitted(native_fixture: NativeFixture) -> None:
    snapshot, references, lexical = native_fixture
    surface = scoped_annotation(
        (snapshot, references, replace(lexical, matches=lexical.matches[:2]))
    )
    assert not surface.annotations
    assert len(surface.lexical_result.matches) == 2


def test_native_stale_conflicting_and_type_reject(
    native_fixture: NativeFixture,
) -> None:
    snapshot, references, _ = native_fixture
    fact = next(f for f in references if str(f.target_resource.address) == "target.py")
    stale = replace(
        fact,
        occurrence=replace(fact.occurrence, snapshot_id=RepositorySnapshotId("0" * 64)),
    )
    with pytest.raises(ValueError, match="snapshot"):
        prepare_references(snapshot, (stale,))
    with pytest.raises(ValueError, match="Conflicting"):
        prepare_references(
            snapshot, (fact, replace(fact, direct_call=not fact.direct_call))
        )
    with pytest.raises(TypeError, match="Only positive"):
        prepare_references(
            snapshot, (cast("PythonDeclarationReferenceKnowledge", object()),)
        )


def test_foreign_task_or_match_reject(native_fixture: NativeFixture) -> None:
    snapshot, references, lexical = native_fixture
    task = LocalizationTaskIdentity("synthetic-task")
    with pytest.raises(ValueError, match="scope"):
        annotate(
            prepare_references(snapshot, references),
            obligation=LocalizationObligationIdentity(task, "O1"),
            query=LocalizationQueryIdentity(LocalizationTaskIdentity("foreign"), "Q1"),
            purpose="need",
            lexical_result=lexical,
        )
    changed = replace(
        lexical.matches[0],
        document_statistics=replace(
            lexical.matches[0].document_statistics, document_length=99
        ),
    )
    with pytest.raises(ValueError, match="foreign"):
        scoped_annotation(
            (
                snapshot,
                references,
                replace(lexical, matches=(changed, *lexical.matches[1:])),
            )
        )


@pytest.mark.parametrize("target", list(Label))
@pytest.mark.parametrize("predecessor", list(Label))
def test_all_ordinal_label_pairs(target: Label, predecessor: Label) -> None:
    result = classify_pair(target, predecessor)
    order = (Label.REQUIRED, Label.HELPFUL_ONLY, Label.UNNECESSARY)
    expected = (
        "NEUTRAL"
        if target == predecessor
        else "BENEFICIAL"
        if order.index(target) < order.index(predecessor)
        else "HARMFUL"
    )
    assert result.direction == expected
    assert result.strong_beneficial == (
        target is Label.REQUIRED and predecessor is Label.UNNECESSARY
    )
    assert result.strong_harmful == (
        target is Label.UNNECESSARY and predecessor is Label.REQUIRED
    )


@pytest.mark.parametrize(
    ("beneficial", "harmful", "category"),
    [
        (0, 0, "NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL"),
        (1, 0, "STRUCTURAL_DISCRIMINATION_SIGNAL"),
        (0, 1, "STRUCTURAL_DISCRIMINATION_CONTRADICTED"),
        (1, 1, "MIXED_STRUCTURAL_DISCRIMINATION_SIGNAL"),
    ],
)
def test_case_categories(beneficial: int, harmful: int, category: str) -> None:
    assert case_category(beneficial, harmful) == category


def test_invalid_count_or_label_rejects() -> None:
    for n in (-1, True):
        with pytest.raises(ValueError, match="nonnegative"):
            case_category(n, 0)
    with pytest.raises(TypeError, match="Unknown"):
        classify_pair(cast("Label", "UNRESOLVED"), Label.REQUIRED)


def test_public_cohort_and_shared_contract() -> None:
    cards = asyncio.run(public_cards())
    assert [c["case_id"] for c in cards] == [
        CASES[c]["population_case"] for c in sorted(CASES)
    ]
    assert (
        cards[0]["task_source"]["task_sha256"]
        == "d1f9e3c61d35d350e0859e2fb02595d46a8baf8e6323aed736497f1ea2ed7d43"
    )
    assert PROTOCOL["annotation"]["rank_change"] is False
    assert PROTOCOL["references"]["pagerank"] is False
    assert PROTOCOL["eligibility"]["graph_only_admission"] is False
    assert not any(freeze.NO_EXECUTION.values())


def test_blind_spec_allowlist() -> None:
    record = {
        "case_id": "synthetic",
        "task_identity": "synthetic",
        "task_text": "synthetic",
        "parent_frame": {},
        "interpretation_gaps": [],
        "ambiguities": [],
        "obligations": [
            {
                "id": "O1",
                "requirement": "r",
                "satisfaction": "s",
                "excluded_interpretation": "e",
                "obligation_identity": {},
                "query": "hidden",
                "need": "hidden",
            }
        ],
    }
    blind = freeze.blind_record(record)
    raw = json_bytes(blind)
    assert b"hidden" not in raw
    assert b"query" not in raw
    assert b"authoring_basis" not in raw


def test_partial_freeze_overwrite_refusal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "existing.json").write_bytes(b"existing")

    async def expected() -> dict[str, bytes]:
        return {"existing.json": b"new"}

    monkeypatch.setattr(freeze, "ROOT", tmp_path)
    monkeypatch.setattr(freeze, "expected", expected)
    with pytest.raises(FileExistsError, match="overwrite"):
        asyncio.run(freeze.build())
    assert (tmp_path / "existing.json").read_bytes() == b"existing"


def test_stage_a_exact_rebuild_and_access_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Observe real allowed parents only; forbid treatment and holdout access."""
    from pathlib import Path  # noqa: PLC0415 -- instrument actual filesystem boundary

    from experiments.structural_discrimination import frames  # noqa: PLC0415

    cards = asyncio.run(public_cards())
    parents = {c["frame"]["parent_commit"] for c in cards}
    original_open = Path.open
    original_git = git
    operations: list[tuple[str, ...]] = []

    def guarded_open(path: Path, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401 -- text/binary Path.open instrumentation
        if any(
            part.casefold() in {"holdout", "adjudication", "confirmation", "reserve"}
            for part in path.parts
        ):
            message = "Forbidden scientific input opened"
            raise AssertionError(message)
        return original_open(path, *args, **kwargs)

    async def guarded_git(*args: str) -> bytes:
        operations.append(args)
        if "diff" in args or "log" in args or "cat-file" in args:
            message = "Child/history inspection is forbidden"
            raise AssertionError(message)
        if args[0] == "show":
            assert args[1] in {
                frames.START + ":" + frames.POPULATION + "population_freeze.json",
                frames.START + ":" + frames.POPULATION + "selection_provenance.json",
            }
        if args[0] in {"rev-parse", "ls-tree"}:
            candidate = args[1] if args[0] == "rev-parse" else args[-1]
            assert candidate.removesuffix("^{tree}") in parents
        if "archive" in args:
            assert args[args.index("--format=tar") + 1] in parents
        return await original_git(*args)

    def forbidden(*_args: object, **_kwargs: object) -> None:
        message = "Stage A attempted treatment computation"
        raise AssertionError(message)

    monkeypatch.setattr(Path, "open", guarded_open)
    monkeypatch.setattr(frames, "git", guarded_git)
    monkeypatch.setattr(
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_bm25",
        forbidden,
    )
    monkeypatch.setattr(
        "devtools.context.python.references.derive_python_declaration_references",
        forbidden,
    )
    first = asyncio.run(freeze.expected())
    second = asyncio.run(freeze.expected())
    assert first == second
    cohort = json.loads(first[freeze.PREFIX + "cohort.json"])
    assert [r["case_id"] for r in cohort["cases"]] == [
        "case-0017",
        "case-0018",
        "case-0019",
    ]
    assert not any(cohort["no_execution"].values())
    for record in cohort["cases"]:
        assert (
            record["shared_protocol_sha256"]
            == cohort["cases"][0]["shared_protocol_sha256"]
        )
        assert "child_commit" not in record["public_task_card"]["frame"]
    assert operations
    assert_case_mutations_rejected(first)


def assert_case_mutations_rejected(first: dict[str, bytes]) -> None:
    """Mutate actual reconstructed prospective bindings, never fixture gold."""
    name = "experiments/codex_dogfood/case_0017/protocol.json"
    for field in (
        "parent_commit",
        "task_text",
        "query",
        "source_hash",
        "child_commit",
        "changed_paths",
        "diff",
        "shared_protocol",
    ):
        altered = dict(first)
        value = json.loads(first[name])
        if field == "parent_commit":
            value["public_task_card"]["frame"][field] = "0" * 40
        elif field == "query":
            value["obligations"][0][field] += " unauthorized.py"
        elif field == "source_hash":
            basis = value["authoring_basis_sha256"]
            basis[next(iter(basis))] = "0" * 64
        else:
            value[field] = "unauthorized"
        altered[name] = json_bytes(value)
        with pytest.raises(ValueError, match="bytes differ"):
            freeze.compare(first, altered)


@pytest.mark.parametrize("changed", [False, True])
def test_external_publication_binds_implementation(
    *, changed: bool, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A committed seal also authenticates source bytes, not merely its own PASS."""
    source = b"exact evaluator source\n"
    seal_name = freeze.PREFIX + "integrity.json"
    seal = json_bytes({"implementation": {"source.py": digest(source)}})
    files = {seal_name: seal}
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        for name, raw in {
            seal_name: seal,
            "source.py": b"altered" if changed else source,
        }.items():
            member = tarfile.TarInfo(name)
            member.size = len(raw)
            archive.addfile(member, io.BytesIO(raw))

    async def captured_git(*args: str) -> bytes:
        if args[0] == "show":
            assert args[1] == "authoritative:" + seal_name
            return seal
        assert "archive" in args
        return stream.getvalue()

    monkeypatch.setattr(freeze, "git", captured_git)
    if changed:
        with pytest.raises(ValueError, match="implementation bytes"):
            asyncio.run(freeze.authenticate_publication("authoritative", files))
    else:
        asyncio.run(freeze.authenticate_publication("authoritative", files))
