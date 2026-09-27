# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, PLR0912, PLR0915, PLR2004, TRY003
"""Outcome-blind, source-grounded references to direct Python functions."""

from __future__ import annotations

import ast
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from devtools.context.python.function.declarations import (
    PythonModuleParseError,
    derive_python_function_declarations,
)
from devtools.context.python.imports.declarations import (
    PythonImportParseError,
    derive_python_import_declarations,
)
from devtools.context.python.imports.members import (
    PythonFacadeCompetingBindingKind,
    PythonImportedMemberResolutionOutcome,
    PythonImportedMemberUnsupportedReason,
    resolve_python_imported_member,
)
from devtools.context.python.imports.resolution import (
    PythonImportResolutionOutcome,
    resolve_python_import_declaration,
)
from experiments.increment_25.development import (
    _build_snapshot_corpus,
    _materialize_git_snapshot,
    _task_card,
    write_artifact,
)
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import (
    MECHANICS_NAME as IMPORT_CANDIDATES_NAME,
)
from experiments.increment_27.structural_imports.mechanics import (
    _digest,
    _module_universe,
    read_candidate_artifact,
)
from experiments.increment_28.import_use import _qualified_read

if TYPE_CHECKING:
    from collections.abc import Mapping

    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationKnowledge,
    )
    from devtools.context.python.imports.declarations import (
        PythonImportDeclarationAnalysis,
    )
    from devtools.context.python.imports.members import PythonImportedMemberResolution
    from devtools.context.python.imports.resolution import PythonImportResolution
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )
    from experiments.increment_25.development import SnapshotCorpus

ROOT = Path(__file__).resolve().parent
ROOT27 = ROOT.parent / "increment_27"
FREEZE_NAME = "references_calls_freeze.json"
CANDIDATES_NAME = "references_calls_candidates.json"
METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")
DIRECTIONS = ("forward", "reverse")


def build_freeze(root: Path = ROOT) -> dict[str, Any]:
    """Bind one bounded reference/call meaning without loading judgments."""
    i27 = root.parent / "increment_27"
    population = cast("dict[str, Any]", _read_json(i27 / "experiment_freeze.json"))
    structural = cast(
        "dict[str, Any]", _read_json(i27 / "structural_import_freeze.json")
    )
    saved = read_candidate_artifact(i27 / IMPORT_CANDIDATES_NAME)
    development = [str(row["case_id"]) for row in saved["cases"]]
    heldout = list(structural["payload"]["heldout_case_ids_sealed"])
    suspended = list(
        structural["payload"]["suspended_increment_26_case_ids_not_executed"]
    )
    if (
        len(development) != 24
        or len(set(development)) != 24
        or len(heldout) != 14
        or len(suspended) != 16
        or set(development) & set(heldout)
        or development != structural["payload"]["development_case_ids"]
        or population["payload"]["increment_27_confirmation"]["case_ids"] != heldout
    ):
        raise ValueError("References/Calls population differs from frozen development.")
    source_names = (
        "experiment_freeze.json",
        "structural_import_freeze.json",
        IMPORT_CANDIDATES_NAME,
        "canonical_positive_lexical_rankings.json",
        "lexical_comparison_rankings.json",
    )
    payload = {
        "development_case_ids": development,
        "heldout_case_ids_sealed": heldout,
        "suspended_increment_26_confirmation_not_executed": suspended,
        "source_sha256": {name: sha256_file(i27 / name) for name in source_names}
        | {
            "increment_25/task_population_freeze.json": sha256_file(
                root.parent / "increment_25" / "task_population_freeze.json"
            )
        },
        "source_content_identities": {
            "increment_27_structural_candidates": saved["content_identity"],
            "increment_27_population": population["content_identity"],
        },
        "seeds": "saved first five positive canonical resource results per case",
        "target": "exactly one direct module-body PythonFunctionSubject",
        "binding": "one unambiguous direct module-body ImportFrom alias, qualified by the unchanged Increment-28 AST Name-load checker over the whole parent-snapshot source",
        "resolution": "unique module-portion resolution and a unique direct function declaration, or the existing single-facade imported-member RESOLVED result; competing/unsupported cases do not establish a reference",
        "reference": "source-grounded ast.Name Load statically refers to the resolved direct function under the bounded binding rules",
        "direct_call": "the same qualified ast.Name is exactly ast.Call.func; call is also a reference",
        "projection": "forward from referencing seed resource to defining resource; reverse from a seed defining resource to referencing resource; exclude all seed resources; deduplicate case/snapshot/resource while retaining all supports",
        "candidate_unit": "parent-snapshot resource",
        "candidate_rank": None,
        "candidate_cap": None,
        "new_judgments_during_mechanics": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i29-references-calls-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_protocol(root: Path = ROOT) -> dict[str, Any]:
    """Persist the exact pre-outcome protocol before source analysis."""
    artifact = build_freeze(root)
    path = root / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing References/Calls freeze differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def _direct_function_target(
    *,
    resolution: PythonImportResolution,
    member: PythonImportedMemberResolution,
    functions: Mapping[str, tuple[PythonFunctionDeclarationKnowledge, ...]],
) -> PythonFunctionDeclarationKnowledge | None:
    """Accept only the one direct function binding qualified by member analysis."""
    if (
        resolution.outcome is not PythonImportResolutionOutcome.RESOLVED
        or member.unsupported_reason
        is not PythonImportedMemberUnsupportedReason.COMPETING_FACADE_BINDING
        or member.facade is None
        or member.facade_bindings
        or len(member.competing_facade_bindings) != 1
        or member.competing_facade_bindings[0].kind
        is not PythonFacadeCompetingBindingKind.FUNCTION
    ):
        return None
    target = str(member.facade.resource.address)
    matches = tuple(
        item
        for item in functions.get(target, ())
        if item.declared_name == resolution.declaration.imported_name
    )
    if len(matches) != 1:
        return None
    direct = matches[0].support.source_range
    competitor = member.competing_facade_bindings[0].support
    if (
        direct.start_line,
        direct.start_column_utf8,
        direct.end_line,
        direct.end_column_utf8,
    ) != (
        competitor.start_line,
        competitor.start_column_utf8,
        competitor.end_line,
        competitor.end_column_utf8,
    ):
        return None
    return matches[0]


def _call_spans(tree: ast.Module) -> set[tuple[int, int, int, int]]:
    """Find only Name nodes in the direct callee position."""
    return {
        (
            node.func.lineno,
            node.func.col_offset,
            cast("int", node.func.end_lineno),
            cast("int", node.func.end_col_offset),
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }


def _source_occurrences(
    *,
    corpus: SnapshotCorpus,
    universe: PythonModuleInterpretationUniverse,
    by_address: Mapping[str, list[PythonModuleInterpretation]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Derive bounded cross-resource facts once; retain qualification counts."""
    functions: dict[str, tuple[PythonFunctionDeclarationKnowledge, ...]] = {}
    counts: Counter[str] = Counter()
    failures: list[dict[str, str]] = []
    for address in corpus.addresses:
        if not str(address).endswith(".py"):
            continue
        counts["python_resources"] += 1
        try:
            function_analysis = derive_python_function_declarations(
                corpus.snapshot, resource_address=address
            )
        except PythonModuleParseError as error:
            counts["function_parse_failed"] += 1
            failures.append(
                {
                    "address": str(address),
                    "kind": "function-parse",
                    "reason": str(error),
                }
            )
            continue
        functions[str(address)] = function_analysis.declarations
        counts["direct_function_declarations"] += len(function_analysis.declarations)
    occurrences: list[dict[str, Any]] = []
    for address in corpus.addresses:
        source = str(address)
        if source not in functions:
            continue
        try:
            import_analysis: PythonImportDeclarationAnalysis = (
                derive_python_import_declarations(
                    corpus.snapshot, resource_address=address
                )
            )
        except PythonImportParseError as error:
            counts["import_parse_failed"] += 1
            failures.append(
                {"address": source, "kind": "import-parse", "reason": str(error)}
            )
            continue
        tree = ast.parse(corpus.snapshot.resource_at(address).content, filename=source)
        source_content = import_analysis.resource.content
        calls = _call_spans(tree)
        interpretations = by_address.get(source, [])
        for declaration in import_analysis.declarations:
            counts["import_aliases_examined"] += 1
            if declaration.imported_name in (None, "*"):
                counts["unsupported_not_named_import"] += 1
                continue
            resolution = resolve_python_import_declaration(
                import_analysis,
                declaration,
                target_universe=universe,
                source_interpretations=interpretations,
            )
            if resolution.outcome is not PythonImportResolutionOutcome.RESOLVED:
                counts[f"module_resolution_{resolution.outcome.value}"] += 1
                continue
            member = resolve_python_imported_member(
                corpus.snapshot,
                import_analysis,
                declaration,
                module_universe=universe,
                source_interpretations=interpretations,
            )
            target: PythonFunctionDeclarationKnowledge | None = None
            mode: str | None = None
            if member.outcome is PythonImportedMemberResolutionOutcome.RESOLVED:
                target = (
                    member.target_declarations[0]
                    if len(member.target_declarations) == 1
                    else None
                )
                mode = "single-facade"
            else:
                target = _direct_function_target(
                    resolution=resolution, member=member, functions=functions
                )
                if target is not None:
                    mode = "direct-module"
            if target is None or mode is None:
                counts[f"member_resolution_{member.outcome.value}"] += 1
                if member.unsupported_reason is not None:
                    counts[f"member_unsupported_{member.unsupported_reason.value}"] += 1
                continue
            support = declaration.support
            qualified = _qualified_read(
                content=source_content,
                tree=tree,
                resolution={
                    "module_text": declaration.module,
                    "imported_name": declaration.imported_name,
                    "local_alias": declaration.local_alias,
                    "requested_module": resolution.requested_module,
                },
                path={
                    "declaration_ordinal": declaration.declaration_ordinal,
                    "import_source_span": [
                        support.start_line,
                        support.start_column_utf8,
                        support.end_line,
                        support.end_column_utf8,
                    ],
                },
                window={"char_start": 0, "char_end": len(source_content)},
            )
            counts[f"binding_{qualified['state'].lower()}"] += 1
            if qualified["state"] == "INDETERMINATE":
                counts[f"binding_indeterminate_{qualified['reason']}"] += 1
            counts["binding_uncertain_occurrences"] += len(
                qualified.get("uncertain_occurrences", ())
            )
            if qualified["state"] != "SUPPORTED":
                continue
            target_resource = str(target.support.resource_address)
            for use in qualified["occurrences"]:
                span = cast("list[int]", use["span_utf8"])
                direct_call = tuple(span) in calls
                occurrence = {
                    "source_resource": source,
                    "target_resource": target_resource,
                    "snapshot_id": str(corpus.snapshot.id),
                    "source_span_utf8": span,
                    "import_declaration_derivation_identity": declaration.derivation_identity,
                    "import_declaration_ordinal": declaration.declaration_ordinal,
                    "import_source_span_utf8": [
                        support.start_line,
                        support.start_column_utf8,
                        support.end_line,
                        support.end_column_utf8,
                    ],
                    "local_binding": qualified["local_binding"],
                    "module_resolution_identity": resolution.identity,
                    "module_resolution_outcome": resolution.outcome.value,
                    "member_resolution_identity": member.identity,
                    "member_resolution_outcome": member.outcome.value,
                    "resolution_path": mode,
                    "target_declaration_identity": target.identity,
                    "target_subject_identity": target.subject.identity,
                    "reference": True,
                    "direct_call": direct_call,
                }
                occurrences.append(occurrence)
                counts["reference_occurrences"] += 1
                if direct_call:
                    counts["direct_call_occurrences"] += 1
    occurrences.sort(
        key=lambda row: (
            row["source_resource"],
            row["source_span_utf8"],
            row["target_subject_identity"],
            row["import_declaration_ordinal"],
        )
    )
    return occurrences, {"counts": dict(sorted(counts.items())), "failures": failures}


def project_case(
    *,
    case: Mapping[str, Any],
    occurrences: list[dict[str, Any]],
    lexical: Mapping[str, Any],
    import_case: Mapping[str, Any],
    diagnostics: Mapping[str, Any],
) -> dict[str, Any]:
    """Project two directions from unchanged seeds and retain every support."""
    seeds = list(case["seeds"])
    seed_addresses = {str(seed["address"]) for seed in seeds}
    if len(seeds) != 5 or [seed["canonical_rank"] for seed in seeds] != [1, 2, 3, 4, 5]:
        raise ValueError("References/Calls seeds differ from canonical top five.")
    import_addresses = {
        str(row["address"])
        for arm in import_case["arms"].values()
        for row in arm["candidates"]
    }
    ranks = {
        method: {
            str(row["address"]): int(row["rank"]) for row in lexical["rankings"][method]
        }
        for method in METHODS
    }
    by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seed_fanout: dict[str, dict[str, int]] = {}
    for seed in seeds:
        seed_address = str(seed["address"])
        forward: set[str] = set()
        reverse: set[str] = set()
        for occurrence in occurrences:
            for direction, endpoint, candidate in (
                (
                    "forward",
                    occurrence["source_resource"],
                    occurrence["target_resource"],
                ),
                (
                    "reverse",
                    occurrence["target_resource"],
                    occurrence["source_resource"],
                ),
            ):
                if endpoint != seed_address or candidate in seed_addresses:
                    continue
                by_candidate[candidate].append(
                    {"direction": direction, "seed_address": seed_address, **occurrence}
                )
                (forward if direction == "forward" else reverse).add(candidate)
        seed_fanout[seed_address] = {"forward": len(forward), "reverse": len(reverse)}
    candidates = []
    for address, supports in sorted(by_candidate.items()):
        method_ranks = {method: ranks[method].get(address) for method in METHODS}
        candidates.append(
            {
                "address": address,
                "reference": True,
                "direct_call": any(row["direct_call"] for row in supports),
                "directions": sorted({row["direction"] for row in supports}),
                "saved_positive_method_ranks": method_ranks,
                "canonical_positive_rank": method_ranks["canonical"],
                "canonical_top_five": address in seed_addresses,
                "absent_all_saved_positive_lexical": all(
                    rank is None for rank in method_ranks.values()
                ),
                "existing_import_candidate": address in import_addresses,
                "support_count": len(supports),
                "supports": supports,
            }
        )
    return {
        "case_id": case["case_id"],
        "parent_snapshot_sha": case["parent_snapshot_sha"],
        "information_need": case["information_need"],
        "snapshot_id": case["snapshot_id"],
        "corpus_id": case["corpus_id"],
        "seed_addresses": [seed["address"] for seed in seeds],
        "seed_fanout": seed_fanout,
        "occurrence_count": len(occurrences),
        "candidate_count": len(candidates),
        "analysis_diagnostics": diagnostics,
        "candidates": candidates,
    }


def _summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [row for case in cases for row in case["candidates"]]
    counter: Counter[str] = Counter()
    for row in rows:
        counter["reference_pairs"] += 1
        if row["direct_call"]:
            counter["call_tagged_pairs"] += 1
        else:
            counter["reference_without_call_pairs"] += 1
        for direction in row["directions"]:
            counter[f"{direction}_pairs"] += 1
        if row["canonical_positive_rank"] is None:
            counter["no_positive_canonical_rank"] += 1
        elif row["canonical_positive_rank"] > 5:
            counter["canonical_rank_gt_five"] += 1
        if row["absent_all_saved_positive_lexical"]:
            counter["absent_all_saved_positive_lexical"] += 1
        if not row["existing_import_candidate"]:
            counter["absent_existing_import_candidates"] += 1
        if (
            row["absent_all_saved_positive_lexical"]
            and not row["existing_import_candidate"]
        ):
            counter["absent_lexical_and_import"] += 1
    return {
        "development_cases": len(cases),
        "candidate_pairs": len(rows),
        "unique_candidate_addresses": len({row["address"] for row in rows}),
        "counts": dict(sorted(counter.items())),
        "case_fanout": {case["case_id"]: case["candidate_count"] for case in cases},
        "reference_occurrences": sum(
            case["analysis_diagnostics"]["counts"].get("reference_occurrences", 0)
            for case in cases
        ),
        "direct_call_occurrences": sum(
            case["analysis_diagnostics"]["counts"].get("direct_call_occurrences", 0)
            for case in cases
        ),
    }


def run_mechanics(*, repository_root: Path, root: Path = ROOT) -> dict[str, Any]:
    """Run exactly the frozen development mechanics without opening outcomes."""
    i27 = root.parent / "increment_27"
    frozen = build_freeze(root)
    if _read_json(root / FREEZE_NAME) != frozen:
        raise ValueError("References/Calls protocol must be frozen first.")
    saved = read_candidate_artifact(i27 / IMPORT_CANDIDATES_NAME)
    lexical = cast(
        "dict[str, Any]", _read_json(i27 / "lexical_comparison_rankings.json")
    )
    task_population = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_25" / "task_population_freeze.json"),
    )
    cards = {
        str(row["case_id"]): _task_card(row)
        for row in task_population["payload"]["task_cards"]
        if row["case_id"] in frozen["payload"]["development_case_ids"]
    }
    if (
        len(cards) != 24
        or [row["case_id"] for row in lexical["cases"]]
        != frozen["payload"]["development_case_ids"]
    ):
        raise ValueError("Saved lexical/case population differs from freeze.")
    cases: list[dict[str, Any]] = []
    for original, ranking in zip(saved["cases"], lexical["cases"], strict=True):
        case_id = str(original["case_id"])
        card = cards[case_id]
        if (
            case_id != ranking["case_id"]
            or card.parent_snapshot_sha != original["parent_snapshot_sha"]
            or card.lexical_query != original["information_need"]["lexical_query"]
            or card.information_need_purpose != original["information_need"]["purpose"]
        ):
            raise ValueError("Frozen InformationNeed or parent snapshot differs.")
        with tempfile.TemporaryDirectory(prefix=f"devtools-i29-ref-{case_id}-") as raw:
            location = Path(raw)
            _materialize_git_snapshot(
                repository_root=repository_root,
                snapshot_sha=card.parent_snapshot_sha,
                source_roots=card.corpus_source_roots,
                destination=location,
            )
            corpus = _build_snapshot_corpus(
                snapshot_root=location, source_roots=card.corpus_source_roots
            )
            if len(corpus.addresses) != original["corpus_resource_count"]:
                raise ValueError("Historical corpus size differs from saved evidence.")
            universe, by_address = _module_universe(corpus, card.corpus_source_roots)
            occurrences, diagnostics = _source_occurrences(
                corpus=corpus, universe=universe, by_address=by_address
            )
            cases.append(
                project_case(
                    case=original,
                    occurrences=occurrences,
                    lexical=ranking,
                    import_case=original,
                    diagnostics=diagnostics,
                )
            )
    if len(cases) != 24 or {row["case_id"] for row in cases} & set(
        frozen["payload"]["heldout_case_ids_sealed"]
    ):
        raise ValueError("References/Calls mechanics escaped development.")
    artifact: dict[str, Any] = {
        "schema": "devtools-i29-references-calls-candidates-v1",
        "freeze_identity": frozen["content_identity"],
        "heldout_executed": False,
        "judgments_loaded": False,
        "cases": cases,
        "summary": _summary(cases),
    }
    artifact["content_identity"] = _digest(
        {key: value for key, value in artifact.items() if key != "content_identity"}
    )
    path = root / CANDIDATES_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing References/Calls candidate evidence differs.")
    write_artifact(path=path, payload=artifact)
    return artifact
