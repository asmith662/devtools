# Copyright (c) 2026
# ruff: noqa: COM812, E402, E501, S301
"""Separate pre-retrieval freeze and unchanged production ranking capture."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import pickle
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from devtools.context.python.imports.declarations import (
    derive_python_import_declarations,
)
from devtools.context.python.imports.relations import (
    PythonResolvedModuleImportRelation,
    derive_python_resolved_module_import_relations,
)
from devtools.context.python.imports.resolution import resolve_python_import_declaration
from devtools.context.python.modules.interpretation import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.retrieval.fusion import fuse_lexical_repository_map_rankings
from devtools.context.retrieval.graph import rank_python_repository_resources
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    analyze_repository_text_lexical_query,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.repository_map import (
    build_repository_map_view,
    calculate_repository_map_importance,
    rank_repository_map,
)
from devtools.core.paths import ResolvedPath
from experiments.codex_dogfood.capture import CodexDogfoodCase
from experiments.typed_graph_baseline.evaluate import VIEWS, _derive_views

HERE = Path(__file__).parent
HEAD = "0bcb2caaf7ae4b6a776bd9505efa1dc87e8325a5"
TASK = "Investigate and implement production Repository Intelligence for deterministic Python-project configuration relationships actually declared in this repository. Derive bounded configuration declarations and repository-resolvable resource or module targets from retained snapshot content, including project README, package selection and tool resource/module selectors where static evidence supports them. Preserve identity, provenance, bounded coverage, ambiguity and unresolved assessments. Do not invent entry-point relationships when no entry points are declared; distinguish syntax and declared selection from actual tooling or runtime behavior. Reuse existing repository resource and Python module identities and resolution semantics. Integrate focused tests and package, architecture, documentation-map, roadmap and backlog documentation. Do not modify Retrieval ranking, graph projection, fusion or Context policy. Validate using a protected development profile excluding sealed confirmation material, then retain a coherent checkpoint without pushing."
NEED = "Python project configuration declarations, pyproject TOML, retained repository snapshots, resource and module resolution, identity provenance coverage, RI tests and architecture."


def _write(name: str, payload: object) -> None:
    (HERE / name).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _dump(name: str, payload: object) -> None:
    (HERE / name).write_bytes(gzip.compress(pickle.dumps(payload, protocol=5), mtime=0))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_handoff() -> None:
    """Render frozen experiment top-ten suggestions and deduplicated rank notes."""
    frozen = json.loads((HERE / "pre_retrieval.json").read_text(encoding="utf-8"))
    captured = json.loads((HERE / "retrieval.json").read_text(encoding="utf-8"))
    if captured["freeze_sha256"] != _sha(HERE / "pre_retrieval.json"):
        initial_path = HERE / "initial_pre_retrieval.json"
        if not initial_path.exists() or captured["freeze_sha256"] != _sha(initial_path):
            msg = "Handoff retrieval and task freeze differ."
            raise ValueError(msg)
        initial = json.loads(initial_path.read_text(encoding="utf-8"))
        initial["bm25"]["filename_weight"] = 0.25
        initial["pre_capture_metadata_correction"] = frozen[
            "pre_capture_metadata_correction"
        ]
        if initial != frozen or not (HERE / "freeze_correction.json").exists():
            msg = "Handoff metadata correction exceeds the retained weight typo."
            raise ValueError(msg)
    lines = [
        "# Development task",
        frozen["task_full_prompt"],
        "# Advisory retrieval suggestions",
        "These ranked suggestions are not guaranteed complete. Search and open any repository resource needed, including unlisted resources. Recover from missing evidence. This experiment presentation is not production Selection.",
    ]
    if captured["freeze_sha256"] != _sha(HERE / "pre_retrieval.json"):
        lines.append(
            "Protocol note: a handwritten filename-weight typo in the captured manifest was corrected transparently; unchanged production BM25 used its canonical 0.25 default throughout. See retained freeze_correction.json."
        )
    notes: dict[str, list[str]] = {}
    for arm, results in captured["arms"].items():
        for channel, order in results["rankings"].items():
            lines.append(f"## {arm}: {channel}")
            lines.extend(
                f"{rank}. {address}" for rank, address in enumerate(order[:10], 1)
            )
            for rank, address in enumerate(order[:10], 1):
                notes.setdefault(address, []).append(f"{arm}/{channel} {rank}")
    lines.append("# Deduplicated suggestion notes (native ranks)")
    lines.extend(
        f"{address}: {', '.join(ranks)}" for address, ranks in sorted(notes.items())
    )
    (HERE / "handoff.txt").write_text("\n\n".join(lines) + "\n", encoding="utf-8")


def _eligible(path: Path) -> bool:
    name = path.as_posix()
    if name == "docs/implementation_ledger.md" or "__pycache__" in path.parts:
        return False
    if name in {
        "README.md",
        "AGENTS.md",
        "pyproject.toml",
        "experiments/codex_dogfood/__init__.py",
        "experiments/codex_dogfood/capture.py",
        "tests/experiments/test_codex_dogfood_capture.py",
    }:
        return True
    return path.suffix.lower() in {".py", ".md", ".toml", ".yaml", ".yml"} and (
        name.startswith(("src/", "docs/"))
        or (name.startswith("tests/") and not name.startswith("tests/experiments/"))
    )


def freeze() -> None:
    """Observe selected content and current RI before any query ranking."""
    if (HERE / "pre_retrieval.json").exists():
        msg = "Case freeze already exists; never overwrite it."
        raise ValueError(msg)
    export = Path(tempfile.mkdtemp(prefix="devtools-case3-snapshot-"))
    paths = [
        ROOT / name
        for name in (
            "AGENTS.md",
            "README.md",
            "pyproject.toml",
            "experiments/codex_dogfood/__init__.py",
            "experiments/codex_dogfood/capture.py",
            "tests/experiments/test_codex_dogfood_capture.py",
        )
    ]
    paths += [
        path
        for prefix in ("src", "docs", "tests")
        for path in (ROOT / prefix).rglob("*")
        if path.is_file() and _eligible(path.relative_to(ROOT))
    ]
    for source in sorted(set(paths)):
        if source.exists():
            target = export / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    repository = Repository(RepositoryId.parse("d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"))
    start = time.perf_counter()
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=ResolvedPath(export),
        maximum_resource_count=10000,
        maximum_traversal_entry_count=20000,
    )
    snapshot = observe_repository_resources(
        repository=repository,
        root=ResolvedPath(export),
        addresses=discovery.addresses,
        maximum_resource_bytes=1048576,
    )
    definition = define_repository_text_corpus(
        discovery=discovery, selected_addresses=discovery.addresses
    )
    corpus = realize_repository_text_corpus(definition=definition, snapshot=snapshot)
    documents = represent_repository_text_corpus(corpus=corpus)
    index = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=documents
            )
        )
    )
    addresses = tuple(
        item.address
        for item in snapshot.resources
        if item.address.value.endswith(".py")
    )
    interpretations = tuple(
        item
        for prefix in ("src", ".")
        for item in interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot(prefix),
            resource_addresses=tuple(
                address
                for address in addresses
                if address.value.startswith("src/") == (prefix == "src")
            ),
        ).interpretations
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id, interpretations=interpretations
    )
    imports: list[PythonResolvedModuleImportRelation] = []
    for address in addresses:
        analysis = derive_python_import_declarations(snapshot, resource_address=address)
        source_interpretations = tuple(
            item for item in interpretations if item.resource.address == address
        )
        resolutions = tuple(
            resolve_python_import_declaration(
                analysis,
                declaration,
                target_universe=universe,
                source_interpretations=source_interpretations,
            )
            for declaration in analysis.declarations
        )
        imports.extend(
            derive_python_resolved_module_import_relations(
                analysis,
                resolutions=resolutions,
                source_interpretations=source_interpretations,
            ).relations
        )
    case = CodexDogfoodCase(
        snapshot=snapshot,
        index=index,
        full_prompt=TASK,
        short_information_need=NEED,
        seed_origins=(),
        imports=tuple(imports),
        references=(),
        memberships=(),
    )
    core = _derive_views(case)[VIEWS[2]]
    view = build_repository_map_view(snapshot, core=core)
    _dump("inputs.pkl.gz", (case, core, view))
    _write(
        "pre_retrieval.json",
        {
            "schema": "codex-prospective-multichannel-freeze-v1",
            "starting_head": HEAD,
            "task_full_prompt": TASK,
            "short_information_need": NEED,
            "snapshot_id": str(snapshot.id),
            "eligible_corpus_id": str(corpus.id),
            "snapshot_resources": [
                [str(item.address), str(item.content_identity)]
                for item in snapshot.resources
            ],
            "eligible_frame": "all src/docs and production tests with text suffix py/md/toml/yaml/yml; excludes ledger, tests/experiments except capture test; adds capture protocol pair and root README/AGENTS/pyproject; no sealed artifacts",
            "inputs_archive_sha256": _sha(HERE / "inputs.pkl.gz"),
            "bm25": {
                "k1": 1.2,
                "b": 0.75,
                "maximum_results": len(snapshot.resources),
                "filename_weight": 0.25,
            },
            "typed_ppr": {
                "view": "typed-core-v1",
                "damping": 0.85,
                "tolerance": 1e-10,
                "maximum_iterations": 200,
                "personalization": "positive resource BM25 reciprocal ranks k60",
                "aggregation": "maximum node mass per resource",
            },
            "repository_map": {
                "importance": "uniform resource global PageRank",
                "damping": 0.85,
                "tolerance": 1e-10,
                "maximum_iterations": 200,
                "symbol_bm25": {"k1": 1.2, "b": 0.75},
                "symbol_rrf_k": 60,
                "aggregation": "maximum winning symbol",
                "lexical_abstention": True,
            },
            "fusion": {
                "channels": ["BM25", "repository_map"],
                "equal_weights": True,
                "k": 60,
            },
            "ri": {
                "graph_nodes": len(core.nodes),
                "graph_edges": len(core.edges),
                "map_nodes": len(view.dependencies.nodes),
                "map_edges": len(view.dependencies.edges),
                "symbols": len(view.symbols),
                "fact_ids": sorted(
                    {
                        support.fact.identity
                        for edge in core.edges
                        for support in edge.contributions
                    }
                ),
                "inputs": "retained imports, direct declarations, generalized references, direct bases; containment; typed-core excludes memberships/mirrors",
            },
            "implementation_sha256": {
                path.relative_to(ROOT).as_posix(): hashlib.sha256(
                    path.read_text(encoding="utf-8").encode()
                ).hexdigest()
                for path in sorted(
                    (ROOT / "src/devtools/context/retrieval").rglob("*.py")
                )
            },
            "handoff_rule": "top10 of each of eight labeled arms, deduplicated resource notes with native ranks; suggestions only, not Selection or sufficiency; free search/open outside list",
            "measurements": [
                "required count",
                "recall@5/10/20/50/100",
                "last required rank",
                "helpful/unnecessary before coverage",
                "missing required",
                "structural rescues",
                "promotions/displacements with provenance",
                "candidate volume",
                "construction and ranking runtime",
                "agent searches/opens/recovery",
                "task and validation outcome",
            ],
            "construction_seconds": time.perf_counter() - start,
            "snapshot_export": str(export),
            "validation_boundary": "explicit protected profile, 22 retained confirmation/audit test node exclusions and seven bounded benchmark cwd cases; no default pytest",
            "confirmation_accessed": False,
        },
    )


def capture() -> None:
    """Rank the immutable archive without reading labels or mutable source."""
    frozen = json.loads((HERE / "pre_retrieval.json").read_text(encoding="utf-8"))
    if (
        _sha(HERE / "inputs.pkl.gz") != frozen["inputs_archive_sha256"]
        or (HERE / "retrieval.json").exists()
    ):
        msg = "Input mismatch or capture already exists."
        raise ValueError(msg)
    case, core, view = pickle.loads(
        gzip.decompress((HERE / "inputs.pkl.gz").read_bytes())
    )
    start = time.perf_counter()
    importance = calculate_repository_map_importance(case.snapshot, view=view)
    construction = time.perf_counter() - start
    native: dict[str, object] = {}
    results: dict[str, Any] = {}
    handoff = [
        "# Development task",
        TASK,
        "# Advisory retrieval suggestions",
        "These ranked suggestions are not guaranteed complete. Search and open any repository resource needed. Recover from missing evidence. This experiment presentation is not production Selection.",
    ]
    for arm in ("full_prompt", "short_information_need"):
        text = getattr(case, arm)
        query = analyze_repository_text_lexical_query(text=text)
        timings = {}
        start = time.perf_counter()
        lexical = retrieve_repository_text_documents_by_bm25(
            query=query,
            index=case.index,
            maximum_results=len(case.snapshot.resources),
            settings=case.lexical_settings,
        )
        timings["bm25"] = time.perf_counter() - start
        start = time.perf_counter()
        ppr = rank_python_repository_resources(
            case.snapshot, purpose=text, lexical_result=lexical, graph_view=core
        )
        timings["typed_ppr"] = time.perf_counter() - start
        start = time.perf_counter()
        ranked = rank_repository_map(
            case.snapshot, purpose=text, query=query, importance=importance
        )
        timings["repository_map"] = time.perf_counter() - start
        start = time.perf_counter()
        fusion = fuse_lexical_repository_map_rankings(
            case.snapshot, purpose=text, lexical_result=lexical, map_result=ranked
        )
        timings["bm25_map_rrf"] = time.perf_counter() - start
        native[arm] = (lexical, ppr, ranked, fusion)
        orders = {
            "bm25": [
                str(item.document_statistics.analysis.document.resource.address)
                for item in lexical.matches
            ],
            "typed_ppr": [str(item.resource_address) for item in ppr.resources],
            "repository_map": [str(item.resource_address) for item in ranked.resources],
            "bm25_map_rrf": [str(item.resource_address) for item in fusion.resources],
        }
        results[arm] = {
            "rankings": orders,
            "runtime_seconds": timings,
            "bm25_scores": {
                str(
                    item.document_statistics.analysis.document.resource.address
                ): item.score
                for item in lexical.matches
            },
            "ppr_provenance": {
                str(item.resource_address): {
                    "winner": item.winning_node.identity,
                    "supports": [
                        {
                            "source": support.source.identity,
                            "family": support.contribution.family,
                            "fact": support.contribution.fact.identity,
                            "flow": support.flow,
                        }
                        for support in item.incoming_supports
                    ],
                }
                for item in ppr.resources
            },
            "map_provenance": {
                str(item.resource_address): {
                    "symbol": item.winning_symbol.symbol.qualified_name,
                    "subject": item.winning_symbol.symbol.declaration.subject.identity,
                    "importance": item.winning_symbol.importance,
                    "importance_rank": item.winning_symbol.importance_rank,
                    "lexical_rank": item.winning_symbol.lexical_rank,
                    "supports": [
                        {
                            "source": support.source.identity,
                            "family": support.contribution.family,
                            "fact": support.contribution.fact.identity,
                            "flow": support.flow,
                        }
                        for support in item.winning_symbol.incoming_supports
                    ],
                }
                for item in ranked.resources
            },
            "ranked_symbols": len(ranked.symbols),
            "ppr_iterations": ppr.iterations,
            "ppr_converged": ppr.converged,
        }
        for channel, order in orders.items():
            handoff.append(f"## {arm}: {channel}")
            handoff.extend(
                f"{rank}. {address}" for rank, address in enumerate(order[:10], 1)
            )
    _dump("capture.pkl.gz", (importance, native))
    _write(
        "retrieval.json",
        {
            "freeze_sha256": _sha(HERE / "pre_retrieval.json"),
            "snapshot_id": str(case.snapshot.id),
            "global_importance_seconds": construction,
            "global_iterations": importance.iterations,
            "global_converged": importance.converged,
            "arms": results,
            "native_capture_sha256": _sha(HERE / "capture.pkl.gz"),
            "confirmation_accessed": False,
        },
    )
    (HERE / "handoff.txt").write_text("\n\n".join(handoff) + "\n", encoding="utf-8")
    render_handoff()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("freeze", "capture", "handoff"))
    args = parser.parse_args()
    if args.phase == "freeze":
        freeze()
    elif args.phase == "capture":
        capture()
    else:
        render_handoff()
