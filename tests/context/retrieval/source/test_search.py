# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- explicit fixture spans and source-window bounds
"""Deterministic source-search acceptance; no models or scientific fixtures."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, cast

import pytest

from devtools.context.planning import (
    DisclosureMaterializationError,
    SourceSearchDisclosureOption,
    materialize_disclosure_plan,
    plan_disclosures,
)
from devtools.context.python.classes.declarations import (
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    derive_python_function_declarations,
)
from devtools.context.python.function.materialization import _extract_source_segment
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval import (
    build_source_search_index,
    search_repository_source,
)
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    analyze_repository_text_lexical_query,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.core.paths import resolve_path

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.retrieval.source import SourceSearchIndex, SourceSearchMode


def _index(tmp_path: Path, files: dict[str, str]) -> SourceSearchIndex:
    for name, text in files.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode())
    repository = Repository.new()
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=resolve_path(tmp_path),
        maximum_resource_count=30,
        maximum_traversal_entry_count=60,
    )
    snapshot = observe_repository_resources(
        repository=repository,
        root=resolve_path(tmp_path),
        addresses=discovery.addresses,
        maximum_resource_bytes=100_000,
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery, selected_addresses=discovery.addresses
        ),
        snapshot=snapshot,
    )
    return build_source_search_index(
        snapshot, corpus=corpus, window_lines=5, overlap_lines=2
    )


@pytest.fixture
def index(tmp_path: Path) -> SourceSearchIndex:
    """Retain multiple native and nested syntax subjects plus non-symbol source."""
    return _index(
        tmp_path,
        {
            "large.py": (
                "# é prefix\n@decorator\nclass Café:\n"
                '    class Nested:\n        @trace(\n            "é"\n        )\n'
                '        async def fetch(self):\n            return "resilient é"\n'
                '    @memo\n    def lookup(self):\n        return "resilient lookup"\n'
                "def outer():\n    async def inner():\n"
                '        return "resilient inner"\n    return inner\n'
                'async def remote():\n    return "remote"\n'
                "def long_function():\n"
                + "".join(f"    value_{i} = {i}\n" for i in range(40))
                + '    return "resilient transport budget"\n'
                + "# unrelated file content\n" * 40
                + 'outside = "resilient outside"\n'
            ).replace("\n", "\r\n"),
            "broken.py": "def broken(:\n    resilient\n",
            "notes.txt": "resilient notes\n",
            "plain.py": 'value = "resilient"\n',
            "empty.py": "",
        },
    )


def test_recursive_symbols_decorators_exact_spans_and_native_identity(
    index: SourceSearchIndex,
) -> None:
    """Syntax views reuse native RI identities and qualify nested syntax."""
    symbols = {
        item.qualified_name: item
        for item in index.views[1].units
        if item.kind == "symbol"
    }
    assert set(symbols) == {
        "Café",
        "Café.Nested",
        "Café.Nested.fetch",
        "Café.lookup",
        "outer",
        "outer.inner",
        "remote",
        "long_function",
    }
    method = symbols["Café.Nested.fetch"]
    assert method.symbol_kind == "async-method"
    assert method.text.startswith("@trace(")
    assert method.text.endswith('return "resilient é"')
    assert method.start_line == 5
    assert method.end_line == 9
    assert method.declaration is None
    assert symbols["Café.Nested"].declaration is None
    assert symbols["outer.inner"].symbol_kind == "async-function"
    assert method.parent_symbol_id == symbols["Café.Nested"].id
    resource = method.resource
    functions = derive_python_function_declarations(
        index.snapshot, resource_address=resource.address
    )
    classes = derive_python_class_method_declarations(
        index.snapshot, resource_address=resource.address
    )
    native = {item.subject.identity for item in functions.declarations}
    native.update(item.subject.identity for item in classes.classes)
    native.update(item.subject.identity for item in classes.methods)
    assert {
        item.declaration.subject.identity
        for item in symbols.values()
        if item.declaration
    } == native
    for unit in symbols.values():
        assert unit.occurrence is not None
        assert (
            _extract_source_segment(resource.content, unit.occurrence.source_range)
            == unit.text
        )
        assert resource.content[unit.start : unit.end] == unit.text
        assert unit.snapshot_id == index.snapshot.id
        assert unit.repository_id == index.snapshot.repository_id
    assert symbols["Café"].text.startswith("@decorator\r\nclass Café:")
    assert index.expand(method, to="class") == symbols["Café.Nested"]
    assert index.expand(symbols["Café.Nested"], to="class") == symbols["Café.Nested"]
    assert index.expand(method).text == resource.content


def test_windows_cover_exact_source_and_long_functions_without_tail_duplicates(
    index: SourceSearchIndex,
) -> None:
    """Bounded overlapping windows preserve non-definition text and every character."""
    for file in index.views[0].units:
        units = [
            unit for unit in index.views[2].units if unit.resource == file.resource
        ]
        if not file.text:
            assert units == []
            assert file.start_line == file.end_line == 1
            continue
        covered: set[int] = set()
        spans = []
        for unit in units:
            assert 0 < len(unit.text.splitlines()) <= 5
            assert unit.text == file.text[unit.start : unit.end]
            covered.update(range(unit.start, unit.end))
            spans.append((unit.start, unit.end))
        assert covered == set(range(len(file.text)))
        assert len(set(spans)) == len(spans)
        assert not any(
            a <= c and d <= b for a, b in spans for c, d in spans if (a, b) != (c, d)
        )
    outside = search_repository_source(index, query="outside", mode="window")
    assert any("outside =" in hit.unit.text for hit in outside.hits)
    result = search_repository_source(index, query="transport budget", mode="window")
    long_function = next(
        unit for unit in index.views[1].units if unit.qualified_name == "long_function"
    )
    assert len(result.hits[0].unit.text) < len(long_function.text)
    assert "transport budget" in result.hits[0].unit.text
    assert any(
        index.expand(unit, to="class").symbol_kind == "class"
        for unit in index.views[2].units
        if str(unit.resource.address) == "large.py" and unit.start_line == 7
    )


def test_file_ranking_is_canonical_and_modes_keep_native_populations(
    index: SourceSearchIndex,
) -> None:
    """Whole-file scores/order are unchanged; mixed never adds native BM25 scores."""
    corpus = index.views[
        0
    ].lexical_index.corpus_statistics.collection_analysis.document_collection.corpus
    original = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=represent_repository_text_corpus(corpus=corpus)
            ),
        )
    )
    canonical = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text="resilient"),
        index=original,
        maximum_results=30,
    )
    result = search_repository_source(index, query="resilient", maximum_results=30)
    assert [(hit.unit.id, hit.unit.text, hit.score) for hit in result.hits] == [
        (
            match.document_statistics.analysis.document.id,
            match.document_statistics.analysis.document.text,
            match.score,
        )
        for match in canonical.matches
    ]
    for mode in ("file", "symbol", "window", "mixed"):
        selected: SourceSearchMode = mode
        result = search_repository_source(
            index, query="resilient", mode=selected, maximum_results=1000
        )
        assert result == search_repository_source(
            index, query="resilient", mode=selected, maximum_results=1000
        )
        assert [hit.rank for hit in result.hits] == list(range(1, len(result.hits) + 1))
        if mode == "mixed":
            presented = [
                (item.view, item.rank) for hit in result.hits for item in hit.evidence
            ]
            expected = [
                (kind, rank)
                for kind, native in zip(
                    ("file", "symbol", "window"), result.native_results, strict=True
                )
                for rank in range(1, len(native.matches) + 1)
            ]
            assert sorted(presented) == sorted(expected)
            for hit in result.hits:
                best = {
                    item.view: min(e.rank for e in hit.evidence if e.view == item.view)
                    for item in hit.evidence
                    if not (item.view == "symbol" and item.unit.kind == "file")
                }
                assert hit.score == pytest.approx(
                    sum(1 / (60 + rank) for rank in best.values())
                )
            assert any(len(hit.evidence) > 1 for hit in result.hits)
            assert len(result.hits) < len(presented)
    assert search_repository_source(index, query="doesnotexist").hits == ()


def test_fallbacks_and_representations_are_not_semantic_subjects(
    index: SourceSearchIndex,
) -> None:
    """Unsupported and malformed sources remain searchable through explicit fallback."""
    assert dict(index.views[1].fallbacks) == {
        RepositoryResourceAddress("broken.py"): "invalid-python",
        RepositoryResourceAddress("notes.txt"): "unsupported-language",
        RepositoryResourceAddress("plain.py"): "no-python-declarations",
        RepositoryResourceAddress("empty.py"): "no-python-declarations",
    }
    result = search_repository_source(index, query="broken", mode="symbol")
    assert result.hits[0].unit.kind == "file"
    assert result.hits[0].evidence[0].view == "symbol"
    assert result.hits[0].unit.declaration is None


def test_mixed_file_fallback_retains_provenance_without_a_duplicate_symbol_vote(
    tmp_path: Path,
) -> None:
    """Three native origins over two actual views contribute only two ranks."""
    index = _index(tmp_path, {"notes.txt": "resilient"})
    result = search_repository_source(index, query="resilient", mode="mixed")
    assert len(result.hits) == 1
    assert {item.view for item in result.hits[0].evidence} == {
        "file",
        "symbol",
        "window",
    }
    assert result.hits[0].score == pytest.approx(2 / 61)


def test_explicit_context_disclosure_and_snapshot_incompatibility(
    index: SourceSearchIndex,
) -> None:
    """Callers choose exact retained Context independently of search ranks."""
    method = next(
        unit for unit in index.views[1].units if unit.qualified_name == "Café.lookup"
    )
    parent = index.expand(method, to="class")
    option = SourceSearchDisclosureOption("inspect cache", parent)
    plan = plan_disclosures(
        purpose="inspect cache", snapshot=index.snapshot, disclosures=(option,)
    )
    materialized = materialize_disclosure_plan(plan=plan, snapshot=index.snapshot)
    assert parent.text in materialized.items[0].text
    assert str(parent.resource.address) in materialized.items[0].text
    assert materialized.items[0].native_provenance is parent
    assert option.repository_id == index.snapshot.repository_id
    with pytest.raises(DisclosureMaterializationError, match="incompatible"):
        SourceSearchDisclosureOption("", parent).materialize(index.snapshot)
    foreign = replace(index.snapshot, repository_id=Repository.new().id)
    with pytest.raises(DisclosureMaterializationError, match="incompatible"):
        option.materialize(foreign)
    with pytest.raises(DisclosureMaterializationError, match="missing"):
        option.materialize(replace(index.snapshot, resources=()))
    resource = replace(parent.resource, content="different")
    with pytest.raises(DisclosureMaterializationError, match="changed"):
        option.materialize(replace(index.snapshot, resources=(resource,)))


def test_invalid_bounds_modes_expansion_and_snapshot_binding(
    index: SourceSearchIndex, tmp_path: Path
) -> None:
    """Invalid options and cross-state source reuse fail explicitly."""
    corpus = index.views[
        0
    ].lexical_index.corpus_statistics.collection_analysis.document_collection.corpus
    for size, overlap in ((0, 0), (2, 2), (2, -1)):
        with pytest.raises(ValueError, match="Window"):
            build_source_search_index(
                index.snapshot, corpus=corpus, window_lines=size, overlap_lines=overlap
            )
    with pytest.raises(ValueError, match="another repository"):
        build_source_search_index(
            replace(index.snapshot, repository_id=Repository.new().id), corpus=corpus
        )
    with pytest.raises(ValueError, match="absent"):
        build_source_search_index(replace(index.snapshot, resources=()), corpus=corpus)
    first = index.views[0].units[0]
    with pytest.raises(ValueError, match="differs"):
        build_source_search_index(
            replace(
                index.snapshot,
                resources=(replace(first.resource, content="different"),),
            ),
            corpus=corpus,
        )
    with pytest.raises(ValueError, match="mode"):
        search_repository_source(
            index, query="anything", mode=cast("SourceSearchMode", "invalid")
        )
    with pytest.raises(ValueError, match="positive"):
        search_repository_source(index, query="anything", maximum_results=0)
    with pytest.raises(ValueError, match="target"):
        index.expand(first, to="module")
    with pytest.raises(ValueError, match="enclosing class"):
        index.expand(first, to="class")
    with pytest.raises(ValueError, match="span"):
        replace(first, start=-1)
    with pytest.raises(ValueError, match="span"):
        replace(first, kind="window", end=0)
    other = _index(tmp_path / "other", {"large.py": "def fresh():\n    pass\n"})
    with pytest.raises(ValueError, match="belong"):
        index.expand(other.views[0].units[0])
    assert other.snapshot.id != index.snapshot.id
    assert other.views[1].units[0].id not in {unit.id for unit in index.views[1].units}


@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"])
def test_line_coordinates_preserve_newlines_and_final_unterminated_line(
    tmp_path: Path, newline: str
) -> None:
    """Ordinary and bare-CR Python retain exact source and coordinate lineage."""
    content = newline.join(
        ("# prefix", "class Owner:", "    def method(self):", '        return "é"')
    )
    index = _index(tmp_path, {"source.py": content})
    method = next(
        unit for unit in index.views[1].units if unit.qualified_name == "Owner.method"
    )
    assert method.text == newline.join(("def method(self):", '        return "é"'))
    assert method.start_line == 3
    assert method.end_line == 4
    assert index.views[2].units[0].text == content
    assert index.views[2].units[0].end_line == 4


@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"])
def test_parenthesized_decorators_include_opening_tokens(
    tmp_path: Path, newline: str
) -> None:
    """AST expressions omit opening decorator parentheses; source views must not."""
    content = newline.join(
        (
            "@(",
            "    decorate",
            ")",
            "class Owner:",
            "    @(",
            "        staticmethod",
            "    )",
            "    @another",
            "    async def method():",
            '        return "é"',
        )
    )
    index = _index(tmp_path, {"decorated.py": content})
    owner, method = index.views[1].units
    assert owner.text == content
    assert owner.start_line == 1
    assert method.start_line == 5
    assert method.text.startswith("@(" + newline)
    assert method.occurrence is not None
    assert method.occurrence.source_range.start_line == 5
    assert method.declaration is not None
    assert method.declaration.support.source_range.start_line == 9
