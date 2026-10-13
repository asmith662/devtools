# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, E501 -- bounded scientific capture codec
"""Native journal composition and mechanically frozen scientific operations."""

from __future__ import annotations

import inspect
import json
import sys
import time
from collections import Counter
from pathlib import Path
from types import FunctionType
from typing import Any

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
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.index import (
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    json_bytes,
)
from experiments.codex_dogfood.case_0012.stage_b.durability import (
    Journal as HistoricalJournal,
)
from experiments.codex_dogfood.case_0016.stage_b.durability import (
    Journal as SafeJournal,
)
from experiments.codex_dogfood.verification.native import NativeMemo
from experiments.structural_discrimination.evidence import annotate

STAGE_A = "48d896b16a992887236285b50e54b159c7c0bb1b"
CASES = ("0017", "0018", "0019")
PACKAGE = Path(__file__).resolve().parent


def case_root(case: str) -> Path:
    """Resolve only the three prospective case destinations."""
    if case not in CASES:
        raise ValueError("Case outside frozen cohort")
    return ROOT / f"experiments/codex_dogfood/case_{case}"


def capture_root(case: str) -> Path:
    """One fresh attempt; never resumes or selects a retry."""
    return case_root(case) / "stage_b" / "attempts" / f"case-{case}-stage-b-1"


def source_hashes() -> dict[str, str]:
    """Bind unchanged Stage A dependencies and exact new capture implementation."""
    prior = json.loads(binary(PACKAGE.parent / "integrity.json"))["implementation"]
    extra = {
        *PACKAGE.glob("*.py"),
        PACKAGE / "README.md",
        PACKAGE / ".gitattributes",
        *(ROOT / "experiments/codex_dogfood/case_0012/stage_b").glob("*.py"),
        *(ROOT / "experiments/codex_dogfood/case_0015/stage_b").glob("*.py"),
        ROOT / "experiments/codex_dogfood/case_0016/stage_b/durability.py",
        ROOT / "experiments/bm25f/fields.py",
    }
    return {
        **prior,
        **{p.relative_to(ROOT).as_posix(): digest(binary(p)) for p in sorted(extra)},
    }


class Journal(SafeJournal):
    """Same journal semantics; exact graph encoding with local immutable templates."""

    def __init__(self, root: Path, state: dict[str, Any]) -> None:
        """Bind the codec to this one producing invocation."""
        super().__init__(root, state)
        memo = NativeMemo()

        def encode(value: Any) -> bytes:
            return value if isinstance(value, bytes) else json_bytes(value)

        original = HistoricalJournal.call
        self.native_call = FunctionType(
            original.__code__,
            {
                **original.__globals__,
                "describe": memo.encoding.encode,
                "json_bytes": encode,
            },
            original.__name__,
            original.__defaults__,
            original.__closure__,
        )

    def call(self, identity: str, inputs: object, invoke: Any) -> Any:
        """Preserve failure stop and the unchanged authoritative event owner."""
        if self.state["active"]:
            raise ValueError("Unreturned scientific boundary; STOP/no retry")
        return self.native_call(self, identity, inputs, invoke)


def schedule(case: str, rows: Any) -> dict[str, Any]:
    """Freeze the complete address-derived schedule before any scientific entry."""
    operations = (
        "frame:prepare",
        "lexical:fields",
        "lexical:index",
        "ri:module-universe",
        *(
            "ri:references:" + r["address"]
            for r in rows
            if r["address"].endswith(".py")
        ),
        "references:prepare",
        *(
            f"query:Q{i}:{step}"
            for i in range(1, 4)
            for step in ("A", "annotation", "pairs", "validate")
        ),
        "annotation:ablation",
        "capture:validate",
    )
    return {
        "schema": "direct-discrimination-schedule-v1",
        "execution": f"case-{case}-stage-b-1",
        "stage_a_checkpoint": STAGE_A,
        "operations": list(operations),
    }


def universe(snapshot: Any) -> Any:
    """Exact frozen src/. native interpretation union, without root preference."""
    interpretations: list[Any] = []
    for root, prefix in (("src", "src/"), (".", "")):
        addresses = tuple(
            r.address
            for r in snapshot.resources
            if str(r.address).endswith(".py")
            and (
                str(r.address).startswith(prefix)
                if prefix
                else not str(r.address).startswith("src/")
            )
        )
        interpreted = interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot(root),
            resource_addresses=addresses,
        )
        interpretations.extend(interpreted.interpretations)
    return define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=tuple(interpretations),
    )


def index(fields: Any) -> Any:
    """Build native content statistics/index, preserving canonical filename query behavior."""
    return build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=fields.content,
        ),
    )


def acquire(query: str, retained_index: Any, count: int) -> Any:
    """One analysis/acquisition; timing excludes every publication operation."""
    started = time.perf_counter_ns()
    result = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text=query),
        index=retained_index,
        maximum_results=count,
    )
    return {"result": result, "online_ns": time.perf_counter_ns() - started}


def annotation(prepared: Any, lexical: Any, design: Any, obligation: Any) -> Any:
    """Observe the existing projection/construction boundary without changing code."""
    if sys.gettrace() is not None:
        raise ValueError("Existing trace prevents exact timing observation")
    lines, first = inspect.getsourcelines(annotate)
    boundary = first + next(
        i for i, line in enumerate(lines) if line.strip() == "annotations = []"
    )
    split = []

    def observe(frame: Any, event: str, _argument: Any) -> Any:
        if frame.f_code is not annotate.__code__:
            return None
        if event == "line" and frame.f_lineno == boundary:
            split.append(time.perf_counter_ns())
        return observe

    task = LocalizationTaskIdentity(design["task_identity"])
    started = time.perf_counter_ns()
    sys.settrace(observe)
    try:
        result = annotate(
            prepared,
            obligation=LocalizationObligationIdentity(task, obligation["id"]),
            query=LocalizationQueryIdentity(
                task,
                obligation["query_identity"]["value"],
            ),
            purpose=obligation["need"],
            lexical_result=lexical,
        )
    finally:
        sys.settrace(None)
    ended = time.perf_counter_ns()
    if len(split) != 1:
        raise ValueError("Frozen annotation timing boundary differs")
    return {
        "result": result,
        "support_projection_ns": split[0] - started,
        "annotation_construction_ns": ended - split[0],
        "online_ns": ended - started,
    }


def identity(resource: Any, document: Any, rank: int) -> dict[str, Any]:
    """Exact resource/document/content scope, never filenames alone."""
    return {
        "address": str(resource.address),
        "content_identity": str(resource.content_identity),
        "document_identity": str(document),
        "a_rank": rank,
    }


def pairs(surface: Any) -> dict[str, Any]:
    """One explicit pair projection; the original ranking is never mutated."""
    started = time.perf_counter_ns()
    result = tuple(
        {
            "obligation": surface.obligation.value,
            "query": surface.query.value,
            "target": identity(t.resource, t.document_id, t.a_rank),
            "predecessor": identity(
                t.predecessor,
                t.predecessor_document_id,
                t.a_rank - 1,
            ),
        }
        for t in surface.annotations
        if t.a_rank > 1
    )
    return {"result": result, "online_ns": time.perf_counter_ns() - started}


def validate_surface(prepared: Any, surface: Any, pair_result: Any) -> dict[str, Any]:  # noqa: C901 -- complete exact support boundary
    """Check complete eligible support and original predecessor without rerunning treatment."""
    documents = tuple(
        m.document_statistics.analysis.document for m in surface.lexical_result.matches
    )
    positions = {d.resource.address: i for i, d in enumerate(documents, 1)}
    expected = {
        (f.occurrence.resource_address, f.target_resource.address, f.identity)
        for f in prepared.facts
        if f.occurrence.resource_address in positions
        and f.target_resource.address in positions
        and positions[f.occurrence.resource_address]
        < positions[f.target_resource.address]
    }
    actual = set()
    if surface.snapshot is not prepared.snapshot:
        raise ValueError("Foreign annotation snapshot")
    if [t.a_rank for t in surface.annotations] != sorted(
        t.a_rank for t in surface.annotations
    ):
        raise ValueError("Target order differs")
    for target in surface.annotations:
        rank = positions[target.resource.address]
        if (
            target.a_rank != rank
            or rank <= 1
            or documents[rank - 1].resource is not target.resource
            or documents[rank - 2].resource is not target.predecessor
            or documents[rank - 1].id != target.document_id
            or documents[rank - 2].id != target.predecessor_document_id
        ):
            raise ValueError("Target/predecessor binding differs")
        if [s.a_rank for s in target.sources] != sorted(
            s.a_rank for s in target.sources
        ):
            raise ValueError("Source order differs")
        for source in target.sources:
            if (
                source.a_rank != positions[source.resource.address]
                or source.a_rank >= rank
                or documents[source.a_rank - 1].resource is not source.resource
                or documents[source.a_rank - 1].id != source.document_id
            ):
                raise ValueError("Source eligibility differs")
            ids = [s.fact.identity for s in source.supports]
            if ids != sorted(set(ids)):
                raise ValueError("Occurrence order/duplicates differ")
            for support in source.supports:
                fact = support.fact
                if (
                    support.direction != "reference-to-definition"
                    or support.seed_resource != source.resource.address
                ):
                    raise ValueError("Native support direction differs")
                actual.add(
                    (source.resource.address, target.resource.address, fact.identity),
                )
    if actual != expected:
        raise ValueError("Reference evidence completeness differs")
    expected_pairs = tuple(
        {
            "obligation": surface.obligation.value,
            "query": surface.query.value,
            "target": identity(t.resource, t.document_id, t.a_rank),
            "predecessor": identity(
                t.predecessor,
                t.predecessor_document_id,
                t.a_rank - 1,
            ),
        }
        for t in surface.annotations
    )
    if pair_result != expected_pairs:
        raise ValueError("Local pairs differ")
    return {
        "status": "PASS",
        "supported_targets": len(surface.annotations),
        "qualifying_occurrences": len(actual),
        "support_source_target_pairs": sum(len(t.sources) for t in surface.annotations),
        "local_pairs": len(pair_result),
    }


def validate_references(frame: Any, analyses: Any, prepared: Any) -> dict[str, Any]:
    """Complete source coverage and positive/negative assessment accounting."""
    addresses = [
        str(r.address)
        for r in frame.snapshot.resources
        if str(r.address).endswith(".py")
    ]
    if list(analyses) != addresses:
        raise ValueError("RI source coverage/order differs")
    outcomes: Counter[str] = Counter()
    references = []
    for address, analysis in analyses.items():
        if str(analysis.derivation.dependency.resource.address) != address:
            raise ValueError("RI derivation source differs")
        if analysis.coverage.assessed_count != len(
            analysis.assessments,
        ) or analysis.coverage.reference_count != len(analysis.references):
            raise ValueError("RI coverage differs")
        positives = tuple(
            a.reference for a in analysis.assessments if a.reference is not None
        )
        if positives != analysis.references:
            raise ValueError("RI positive assessment correspondence differs")
        for assessment in analysis.assessments:
            if (
                assessment.occurrence.snapshot_id != frame.snapshot.id
                or str(assessment.occurrence.resource_address) != address
            ):
                raise ValueError("RI assessment frame differs")
            outcomes[assessment.outcome.value] += 1
        references.extend(analysis.references)
    if {f.identity for f in references} != {f.identity for f in prepared.facts}:
        raise ValueError("Prepared Reference coverage differs")
    return {
        "resources_derived": len(analyses),
        "assessments": sum(outcomes.values()),
        "outcomes": dict(sorted(outcomes.items())),
        "positive_references": len(prepared.facts),
        "self_references": prepared.self_reference_count,
        "cross_resource_references": sum(
            f.occurrence.resource_address != f.target_resource.address
            for f in prepared.facts
        ),
        "direct_cross_resource_pairs": len(
            {
                (str(f.occurrence.resource_address), str(f.target_resource.address))
                for f in prepared.facts
                if f.occurrence.resource_address != f.target_resource.address
            },
        ),
    }
