# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, EM102, PLR2004, TRY003
"""Outcome-blind, one-edge package/module containment candidates."""

from __future__ import annotations

import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from devtools.context.python.modules import (
    PythonModuleKind,
    PythonModuleRoot,
    interpret_python_module_resources,
)
from experiments.increment_25.development import (
    _build_snapshot_corpus,
    _materialize_git_snapshot,
    _task_card,
    write_artifact,
)
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import (
    MECHANICS_NAME as IMPORT_NAME,
)
from experiments.increment_27.structural_imports.mechanics import (
    _digest,
    read_candidate_artifact,
)
from experiments.increment_29.mechanics import CANDIDATES_NAME as REFERENCES_NAME

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from devtools.context.python.modules import PythonModuleInterpretation
    from experiments.increment_25.development import SnapshotCorpus

ROOT = Path(__file__).resolve().parent
FREEZE_NAME = "package_containment_freeze.json"
CANDIDATES_NAME = "package_containment_candidates.json"
METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")


def _verified_json(path: Path) -> dict[str, Any]:
    value = cast("dict[str, Any]", _read_json(path))
    hashed = (
        value["payload"]
        if "payload" in value
        else {key: item for key, item in value.items() if key != "content_identity"}
    )
    if value.get("content_identity") != _digest(hashed):
        raise ValueError(f"Source content identity differs: {path.name}.")
    return value


def build_freeze(root: Path = ROOT) -> dict[str, Any]:
    """Bind only saved development mechanics, without opening outcomes."""
    i27, i29 = root.parent / "increment_27", root.parent / "increment_29"
    source_paths = {
        "increment_25/task_population_freeze.json": root.parent
        / "increment_25"
        / "task_population_freeze.json",
        "increment_27/experiment_freeze.json": i27 / "experiment_freeze.json",
        "increment_27/structural_import_freeze.json": i27
        / "structural_import_freeze.json",
        f"increment_27/{IMPORT_NAME}": i27 / IMPORT_NAME,
        "increment_27/lexical_comparison_rankings.json": i27
        / "lexical_comparison_rankings.json",
        f"increment_29/{REFERENCES_NAME}": i29 / REFERENCES_NAME,
    }
    import_candidates = read_candidate_artifact(
        source_paths[f"increment_27/{IMPORT_NAME}"]
    )
    references = _verified_json(source_paths[f"increment_29/{REFERENCES_NAME}"])
    structural = _verified_json(
        source_paths["increment_27/structural_import_freeze.json"]
    )
    development = [str(case["case_id"]) for case in import_candidates["cases"]]
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
        or [case["case_id"] for case in references["cases"]] != development
        or references["judgments_loaded"]
        or references["heldout_executed"]
    ):
        raise ValueError("Containment population differs from frozen development.")
    payload = {
        "development_case_ids": development,
        "heldout_case_ids_sealed": heldout,
        "suspended_increment_26_confirmation_not_executed": suspended,
        "source_sha256": {
            name: sha256_file(path) for name, path in source_paths.items()
        },
        "source_content_identities": {
            "structural_import_candidates": import_candidates["content_identity"],
            "references_calls_candidates": references["content_identity"],
        },
        "relation": "one observed child module P.C and exactly one observed package module P in the same snapshot and explicit module root",
        "projection": {
            "child_to_package": "child seed -> immediate parent package resource",
            "package_to_child": "package seed -> each immediate child module resource",
        },
        "seeds": "saved first five positive canonical resources per InformationNeed",
        "candidate_unit": "parent-snapshot resource; exclude every seed; deduplicate by case/snapshot/address while retaining all supports",
        "module_roots": "frozen task-card corpus source roots; no cross-root precedence",
        "recursive_traversal": False,
        "candidate_rank": None,
        "candidate_cap": None,
        "judgments_during_mechanics": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i30-package-containment-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_protocol(root: Path = ROOT) -> dict[str, Any]:
    """Persist the semantics before deriving candidate relationships."""
    artifact = build_freeze(root)
    path = root / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing containment protocol differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def derive_immediate_relations(
    interpretations: Sequence[PythonModuleInterpretation],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Derive only exact one-edge membership; leave missing/ambiguous unresolved."""
    packages: dict[tuple[str, str, str], list[PythonModuleInterpretation]] = (
        defaultdict(list)
    )
    for item in interpretations:
        if item.kind is PythonModuleKind.PACKAGE:
            packages[
                (str(item.snapshot_id), item.module_root.value, item.dotted_name)
            ].append(item)
    relations: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for child in interpretations:
        if "." not in child.dotted_name:
            counts["without_immediate_parent_name"] += 1
            continue
        parent_name = child.dotted_name.rsplit(".", 1)[0]
        parents = packages.get(
            (str(child.snapshot_id), child.module_root.value, parent_name), []
        )
        if not parents:
            counts["missing_observed_immediate_package"] += 1
            continue
        if len(parents) != 1:
            counts["ambiguous_immediate_package"] += 1
            continue
        package = parents[0]
        if package.resource.address == child.resource.address:
            raise ValueError("A package cannot immediately contain itself.")
        relations.append(
            {
                "snapshot_id": str(child.snapshot_id),
                "module_root": child.module_root.value,
                "package_dotted_name": package.dotted_name,
                "child_dotted_name": child.dotted_name,
                "package_address": str(package.resource.address),
                "child_address": str(child.resource.address),
                "package_content_identity": str(package.resource.content_identity),
                "child_content_identity": str(child.resource.content_identity),
                "package_interpretation_identity": package.identity,
                "child_interpretation_identity": child.identity,
                "package_kind": package.kind.value,
                "child_kind": child.kind.value,
            }
        )
        counts["qualified_relations"] += 1
    relations.sort(
        key=lambda row: (
            row["module_root"],
            row["package_address"],
            row["child_address"],
        )
    )
    return relations, dict(sorted(counts.items()))


def _case_relations(
    corpus: SnapshotCorpus, roots: Sequence[str]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    interpretations: list[PythonModuleInterpretation] = []
    excluded: Counter[str] = Counter()
    for root in roots:
        addresses = tuple(
            address for address in corpus.addresses if address.parts[0] == root
        )
        analysis = interpret_python_module_resources(
            corpus.snapshot,
            module_root=PythonModuleRoot(root),
            resource_addresses=addresses,
        )
        interpretations.extend(analysis.interpretations)
        excluded.update(row.reason.value for row in analysis.exclusions)
    relations, statuses = derive_immediate_relations(interpretations)
    return relations, {
        "resources_examined": len(corpus.addresses),
        "interpreted_resources": len(interpretations),
        "interpretation_exclusions": dict(sorted(excluded.items())),
        "relation_statuses": statuses,
    }


def project_case(
    *,
    case: Mapping[str, Any],
    relations: Sequence[Mapping[str, Any]],
    lexical: Mapping[str, Any],
    references: Mapping[str, Any],
    diagnostics: Mapping[str, Any],
) -> dict[str, Any]:
    """Project both one-edge directions without a relevance decision."""
    seeds = list(case["seeds"])
    if len(seeds) != 5 or [seed["canonical_rank"] for seed in seeds] != [1, 2, 3, 4, 5]:
        raise ValueError("Containment seeds differ from saved canonical top five.")
    seed_addresses = {str(seed["address"]) for seed in seeds}
    imports = {
        str(row["address"])
        for arm in case["arms"].values()
        for row in arm["candidates"]
    }
    ref_addresses = {str(row["address"]) for row in references["candidates"]}
    ranks = {
        method: {
            str(row["address"]): int(row["rank"]) for row in lexical["rankings"][method]
        }
        for method in METHODS
    }
    by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seed_fanout: dict[str, dict[str, int]] = {}
    for seed in seeds:
        address = str(seed["address"])
        directions: dict[str, set[str]] = {
            "child_to_package": set(),
            "package_to_child": set(),
        }
        for relation in relations:
            for direction, endpoint, candidate in (
                (
                    "child_to_package",
                    relation["child_address"],
                    relation["package_address"],
                ),
                (
                    "package_to_child",
                    relation["package_address"],
                    relation["child_address"],
                ),
            ):
                if endpoint != address or candidate in seed_addresses:
                    continue
                by_candidate[str(candidate)].append(
                    {"direction": direction, "seed_address": address, **relation}
                )
                directions[direction].add(str(candidate))
        seed_fanout[address] = {
            direction: len(values) for direction, values in directions.items()
        }
    candidates = []
    for address, supports in sorted(by_candidate.items()):
        method_ranks = {method: ranks[method].get(address) for method in METHODS}
        absent_lexical = all(rank is None for rank in method_ranks.values())
        candidates.append(
            {
                "address": address,
                "directions": sorted({row["direction"] for row in supports}),
                "saved_positive_method_ranks": method_ranks,
                "canonical_positive_rank": method_ranks["canonical"],
                "canonical_top_five": address in seed_addresses,
                "absent_all_saved_positive_lexical": absent_lexical,
                "existing_import_candidate": address in imports,
                "existing_references_calls_candidate": address in ref_addresses,
                "absent_existing_evidence_union": absent_lexical
                and address not in imports
                and address not in ref_addresses,
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
        "relation_count": len(relations),
        "candidate_count": len(candidates),
        "analysis_diagnostics": dict(diagnostics),
        "candidates": candidates,
    }


def summarize(cases: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Summarize reach and fan-out, without any usefulness outcomes."""
    rows = [row for case in cases for row in case["candidates"]]
    counts: Counter[str] = Counter()
    for row in rows:
        for direction in row["directions"]:
            counts[f"{direction}_pairs"] += 1
        if row["canonical_positive_rank"] is None:
            counts["no_positive_canonical_rank"] += 1
        elif row["canonical_positive_rank"] > 5:
            counts["canonical_rank_gt_five"] += 1
        if row["absent_all_saved_positive_lexical"]:
            counts["absent_all_saved_positive_lexical"] += 1
        if not row["existing_import_candidate"]:
            counts["absent_import_candidates"] += 1
        if not row["existing_references_calls_candidate"]:
            counts["absent_references_calls_candidates"] += 1
        if row["absent_existing_evidence_union"]:
            counts["absent_existing_evidence_union"] += 1
    return {
        "development_cases": len(cases),
        "cases_with_relations": sum(case["relation_count"] > 0 for case in cases),
        "cases_with_additions": sum(case["candidate_count"] > 0 for case in cases),
        "resources_examined": sum(
            case["analysis_diagnostics"]["resources_examined"] for case in cases
        ),
        "interpreted_resources": sum(
            case["analysis_diagnostics"]["interpreted_resources"] for case in cases
        ),
        "qualified_relations": sum(case["relation_count"] for case in cases),
        "relation_statuses": dict(
            sorted(
                sum(
                    (
                        Counter(case["analysis_diagnostics"]["relation_statuses"])
                        for case in cases
                    ),
                    Counter(),
                ).items()
            )
        ),
        "interpretation_exclusions": dict(
            sorted(
                sum(
                    (
                        Counter(
                            case["analysis_diagnostics"]["interpretation_exclusions"]
                        )
                        for case in cases
                    ),
                    Counter(),
                ).items()
            )
        ),
        "candidate_pairs": len(rows),
        "distinct_candidate_addresses": len({row["address"] for row in rows}),
        "retained_supports": sum(row["support_count"] for row in rows),
        "max_case_fanout": max((case["candidate_count"] for case in cases), default=0),
        "max_seed_fanout": max(
            (
                sum(fanout.values())
                for case in cases
                for fanout in case["seed_fanout"].values()
            ),
            default=0,
        ),
        "case_fanout": {
            str(case["case_id"]): case["candidate_count"] for case in cases
        },
        "seed_fanout": {str(case["case_id"]): case["seed_fanout"] for case in cases},
        "counts": dict(sorted(counts.items())),
    }


def run_mechanics(*, repository_root: Path, root: Path = ROOT) -> dict[str, Any]:
    """Materialize only frozen development parents and derive package membership."""
    frozen = build_freeze(root)
    if _read_json(root / FREEZE_NAME) != frozen:
        raise ValueError("Containment protocol must be frozen before mechanics.")
    i27, i29 = root.parent / "increment_27", root.parent / "increment_29"
    saved = read_candidate_artifact(i27 / IMPORT_NAME)
    lexical = _verified_json(i27 / "lexical_comparison_rankings.json")
    references = _verified_json(i29 / REFERENCES_NAME)
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
        raise ValueError("Saved lexical/case population differs from protocol.")
    cases: list[dict[str, Any]] = []
    for original, ranking, ref_case in zip(
        saved["cases"], lexical["cases"], references["cases"], strict=True
    ):
        case_id = str(original["case_id"])
        card = cards[case_id]
        if (
            case_id != ranking["case_id"]
            or case_id != ref_case["case_id"]
            or card.parent_snapshot_sha != original["parent_snapshot_sha"]
            or card.parent_snapshot_sha != ref_case["parent_snapshot_sha"]
            or card.lexical_query != original["information_need"]["lexical_query"]
            or card.information_need_purpose != original["information_need"]["purpose"]
        ):
            raise ValueError("Frozen case identity differs across saved evidence.")
        with tempfile.TemporaryDirectory(
            prefix=f"devtools-i30-package-{case_id}-"
        ) as raw:
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
                raise ValueError("Historical corpus size differs from frozen evidence.")
            relations, diagnostics = _case_relations(corpus, card.corpus_source_roots)
            cases.append(
                project_case(
                    case=original,
                    relations=relations,
                    lexical=ranking,
                    references=ref_case,
                    diagnostics=diagnostics,
                )
            )
    if len(cases) != 24 or {case["case_id"] for case in cases} & set(
        frozen["payload"]["heldout_case_ids_sealed"]
    ):
        raise ValueError("Containment mechanics escaped development.")
    artifact: dict[str, Any] = {
        "schema": "devtools-i30-package-containment-candidates-v1",
        "freeze_identity": frozen["content_identity"],
        "judgments_loaded": False,
        "heldout_executed": False,
        "cases": cases,
        "summary": summarize(cases),
    }
    artifact["content_identity"] = _digest(artifact)
    path = root / CANDIDATES_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing containment candidate evidence differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    freeze_protocol()
    run_mechanics(repository_root=ROOT.parents[1])
