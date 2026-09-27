# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR0913, PLR2004, TRY003
"""Outcome-blind exact mirrored source/test path candidates."""

from __future__ import annotations

import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from devtools.context.repository.resource import RepositoryResourceAddress
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
from experiments.increment_30.mechanics import _verified_json

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from experiments.increment_25.development import SnapshotCorpus

ROOT = Path(__file__).resolve().parent
FREEZE_NAME = "mirrored_test_paths_freeze.json"
CANDIDATES_NAME = "mirrored_test_paths_candidates.json"
METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")


def build_freeze(root: Path = ROOT) -> dict[str, Any]:
    """Bind the development-only sources and exact path rule before outcomes."""
    i27 = root.parent / "increment_27"
    sources = {
        "task_population": root.parent / "increment_25" / "task_population_freeze.json",
        "development": i27 / "experiment_freeze.json",
        "lexical": i27 / "lexical_comparison_rankings.json",
        "imports": i27 / IMPORT_NAME,
        "references_calls": root.parent
        / "increment_29"
        / "references_calls_candidates.json",
        "containment": root.parent
        / "increment_30"
        / "package_containment_candidates.json",
    }
    imports = read_candidate_artifact(sources["imports"])
    references = _verified_json(sources["references_calls"])
    containment = _verified_json(sources["containment"])
    development = _verified_json(sources["development"])["payload"]
    cases = [str(case["case_id"]) for case in imports["cases"]]
    sealed = [
        str(case["case_id"])
        for case in development["increment_27_confirmation"]["cards"]
    ]
    suspended = development["preserved_suspended_increment_26_confirmation"]
    if (
        len(cases) != 24
        or len(set(cases)) != 24
        or len(sealed) != 14
        or set(cases) & set(sealed)
        or cases != [row["case_id"] for row in references["cases"]]
        or cases != [row["case_id"] for row in containment["cases"]]
        or imports["judgment_artifacts_loaded"]
        or references["judgments_loaded"]
        or containment["judgments_loaded"]
        or any(
            (
                imports["heldout_executed"],
                references["heldout_executed"],
                containment["heldout_executed"],
            )
        )
    ):
        raise ValueError(
            "Saved candidate sources differ from development-only population."
        )
    payload = {
        "development_case_ids": cases,
        "heldout_case_ids_sealed": sealed,
        "suspended_increment_26_confirmation": suspended,
        "source_sha256": {name: sha256_file(path) for name, path in sources.items()},
        "source_content_identities": {
            name: (_verified_json(path) if name != "imports" else imports)[
                "content_identity"
            ]
            for name, path in sources.items()
            if name != "task_population"
        },
        "relation": "both observed paths in one parent snapshot: src/devtools/<relative-directory>/<stem>.py and tests/<relative-directory>/test_<stem>.py",
        "excluded": "initializer paths, unmatched paths, all canonical top-five seeds",
        "directions": ["source_to_test", "test_to_source"],
        "seeds": "saved first five positive canonical resource results per case",
        "candidate_unit": "InformationNeed, parent snapshot, resource address; retain every path support",
        "changed_paths_used": False,
        "ranking": None,
        "judgments_loaded": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i31-mirrored-test-path-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_protocol(root: Path = ROOT) -> dict[str, Any]:
    """Persist the outcome-independent protocol."""
    artifact = build_freeze(root)
    path = root / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing mirrored-test protocol differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def derive_mirrors(
    snapshot: SnapshotCorpus,
) -> tuple[list[dict[str, str]], dict[str, int]]:
    """Match only exact observed resource addresses; do not parse test semantics."""
    addresses = {str(address): address for address in snapshot.addresses}
    source = [
        address
        for address in snapshot.addresses
        if address.parts[:2] == ("src", "devtools") and str(address).endswith(".py")
    ]
    tests = [
        address
        for address in snapshot.addresses
        if address.parts[0] == "tests" and str(address).endswith(".py")
    ]
    relations: list[dict[str, str]] = []
    excluded_initializers = sum(
        address.parts[-1] == "__init__.py" for address in [*source, *tests]
    )
    matched_tests: set[str] = set()
    eligible_source = [
        address for address in source if address.parts[-1] != "__init__.py"
    ]
    eligible_tests = [
        address
        for address in tests
        if address.parts[-1].startswith("test_")
        and address.parts[-1] != "test___init__.py"
    ]
    for address in eligible_source:
        test = RepositoryResourceAddress(
            "/".join(("tests", *address.parts[2:-1], f"test_{address.parts[-1]}"))
        )
        if str(test) not in addresses:
            continue
        relations.append(
            {
                "snapshot_id": str(snapshot.snapshot.id),
                "source_address": str(address),
                "test_address": str(test),
                "source_content_identity": str(
                    snapshot.snapshot.resource_at(address).content_identity
                ),
                "test_content_identity": str(
                    snapshot.snapshot.resource_at(test).content_identity
                ),
                "rule": "exact-mirrored-test-path-v1",
            }
        )
        matched_tests.add(str(test))
    relations.sort(key=lambda row: (row["source_address"], row["test_address"]))
    return relations, {
        "source_resources_examined": len(source),
        "test_resources_examined": len(tests),
        "excluded_initializers": excluded_initializers,
        "unmatched_source_resources": len(eligible_source) - len(relations),
        "unmatched_named_test_resources": len(eligible_tests) - len(matched_tests),
        "exact_mirrored_pairs": len(relations),
    }


def project_case(
    *,
    original: Mapping[str, Any],
    relations: Sequence[Mapping[str, str]],
    lexical: Mapping[str, Any],
    references: Mapping[str, Any],
    containment: Mapping[str, Any],
    diagnostics: Mapping[str, int],
) -> dict[str, Any]:
    """Project one mirror edge in either direction, preserving all supports."""
    seeds = list(original["seeds"])
    if len(seeds) != 5 or [row["canonical_rank"] for row in seeds] != [1, 2, 3, 4, 5]:
        raise ValueError(
            "Canonical seeds differ from saved first five positive results."
        )
    seed_addresses = {str(row["address"]) for row in seeds}
    imports = {
        str(row["address"])
        for arm in original["arms"].values()
        for row in arm["candidates"]
    }
    calls = {str(row["address"]) for row in references["candidates"]}
    packages = {str(row["address"]) for row in containment["candidates"]}
    ranks = {
        method: {
            str(row["address"]): int(row["rank"]) for row in lexical["rankings"][method]
        }
        for method in METHODS
    }
    supports: dict[str, list[dict[str, str]]] = defaultdict(list)
    fanout: dict[str, int] = {}
    for seed in seeds:
        address = str(seed["address"])
        local: set[str] = set()
        for relation in relations:
            for direction, endpoint, candidate in (
                (
                    "source_to_test",
                    relation["source_address"],
                    relation["test_address"],
                ),
                (
                    "test_to_source",
                    relation["test_address"],
                    relation["source_address"],
                ),
            ):
                if address != endpoint or candidate in seed_addresses:
                    continue
                supports[str(candidate)].append(
                    {"seed_address": address, "direction": direction, **relation}
                )
                local.add(str(candidate))
        fanout[address] = len(local)
    candidates = []
    for address, evidence in sorted(supports.items()):
        method_ranks = {method: ranks[method].get(address) for method in METHODS}
        absent_lexical = all(rank is None for rank in method_ranks.values())
        candidates.append(
            {
                "address": address,
                "directions": sorted({row["direction"] for row in evidence}),
                "saved_positive_method_ranks": method_ranks,
                "canonical_top_five": address in seed_addresses,
                "absent_all_saved_positive_lexical": absent_lexical,
                "existing_import_candidate": address in imports,
                "existing_references_calls_candidate": address in calls,
                "existing_containment_candidate": address in packages,
                "absent_existing_evidence_union": absent_lexical
                and address not in imports
                and address not in calls
                and address not in packages,
                "support_count": len(evidence),
                "supports": evidence,
            }
        )
    return {
        "case_id": original["case_id"],
        "parent_snapshot_sha": original["parent_snapshot_sha"],
        "information_need": original["information_need"],
        "snapshot_id": original["snapshot_id"],
        "corpus_id": original["corpus_id"],
        "seed_addresses": [row["address"] for row in seeds],
        "seed_fanout": fanout,
        "relation_count": len(relations),
        "candidate_count": len(candidates),
        "analysis_diagnostics": dict(diagnostics),
        "candidates": candidates,
    }


def summarize(cases: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Summarize only outcome-free reach and cost."""
    rows = [row for case in cases for row in case["candidates"]]
    counts: Counter[str] = Counter()
    for row in rows:
        for direction in row["directions"]:
            counts[f"{direction}_pairs"] += 1
        for method, rank in row["saved_positive_method_ranks"].items():
            if rank is None:
                counts[f"absent_{method}_positive"] += 1
        if row["canonical_top_five"]:
            counts["canonical_top_five"] += 1
        for field in (
            "absent_all_saved_positive_lexical",
            "existing_import_candidate",
            "existing_references_calls_candidate",
            "existing_containment_candidate",
            "absent_existing_evidence_union",
        ):
            if row[field]:
                counts[field] += 1
    return {
        "development_cases": len(cases),
        "cases_with_additions": sum(case["candidate_count"] > 0 for case in cases),
        "source_resources_examined": sum(
            case["analysis_diagnostics"]["source_resources_examined"] for case in cases
        ),
        "test_resources_examined": sum(
            case["analysis_diagnostics"]["test_resources_examined"] for case in cases
        ),
        "exact_mirrored_pairs": sum(case["relation_count"] for case in cases),
        "unmatched_source_resources": sum(
            case["analysis_diagnostics"]["unmatched_source_resources"] for case in cases
        ),
        "unmatched_named_test_resources": sum(
            case["analysis_diagnostics"]["unmatched_named_test_resources"]
            for case in cases
        ),
        "excluded_initializers": sum(
            case["analysis_diagnostics"]["excluded_initializers"] for case in cases
        ),
        "candidate_pairs": len(rows),
        "distinct_candidate_addresses": len({row["address"] for row in rows}),
        "retained_supports": sum(row["support_count"] for row in rows),
        "max_case_fanout": max((case["candidate_count"] for case in cases), default=0),
        "max_seed_fanout": max(
            (value for case in cases for value in case["seed_fanout"].values()),
            default=0,
        ),
        "case_fanout": {
            str(case["case_id"]): case["candidate_count"] for case in cases
        },
        "counts": dict(sorted(counts.items())),
    }


def run_mechanics(*, repository_root: Path, root: Path = ROOT) -> dict[str, Any]:
    """Observe only development parents and persist candidates before judgments."""
    frozen = build_freeze(root)
    if _read_json(root / FREEZE_NAME) != frozen:
        raise ValueError("Mirrored-test protocol must be frozen before mechanics.")
    imports = read_candidate_artifact(root.parent / "increment_27" / IMPORT_NAME)
    lexical = _verified_json(
        root.parent / "increment_27" / "lexical_comparison_rankings.json"
    )
    references = _verified_json(
        root.parent / "increment_29" / "references_calls_candidates.json"
    )
    containment = _verified_json(
        root.parent / "increment_30" / "package_containment_candidates.json"
    )
    population = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_25" / "task_population_freeze.json"),
    )
    allowed = list(frozen["payload"]["development_case_ids"])
    cards = {
        str(row["case_id"]): _task_card(row)
        for row in population["payload"]["task_cards"]
        if row["case_id"] in allowed
    }
    if len(cards) != 24 or [row["case_id"] for row in lexical["cases"]] != allowed:
        raise ValueError("Development cards or rankings differ from frozen population.")
    cases = []
    for original, ranking, ref_case, package_case in zip(
        imports["cases"],
        lexical["cases"],
        references["cases"],
        containment["cases"],
        strict=True,
    ):
        case_id = str(original["case_id"])
        card = cards[case_id]
        if any(
            row["case_id"] != case_id
            or row["parent_snapshot_sha"] != card.parent_snapshot_sha
            for row in (original, ranking, ref_case, package_case)
        ) or original["information_need"] != {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
        }:
            raise ValueError("Source case/snapshot/InformationNeed identity differs.")
        with tempfile.TemporaryDirectory(
            prefix=f"devtools-i31-mirror-{case_id}-"
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
            if (
                len(corpus.addresses) != original["corpus_resource_count"]
                or str(corpus.snapshot.id) != original["snapshot_id"]
            ):
                raise ValueError(
                    "Historical parent corpus differs from frozen evidence."
                )
            relations, diagnostics = derive_mirrors(corpus)
            cases.append(
                project_case(
                    original=original,
                    relations=relations,
                    lexical=ranking,
                    references=ref_case,
                    containment=package_case,
                    diagnostics=diagnostics,
                )
            )
    if [case["case_id"] for case in cases] != allowed or set(allowed) & set(
        frozen["payload"]["heldout_case_ids_sealed"]
    ):
        raise ValueError("Mirrored-test mechanics escaped development.")
    artifact: dict[str, Any] = {
        "schema": "devtools-i31-mirrored-test-path-candidates-v1",
        "freeze_identity": frozen["content_identity"],
        "judgments_loaded": False,
        "heldout_executed": False,
        "cases": cases,
        "summary": summarize(cases),
    }
    artifact["content_identity"] = _digest(artifact)
    path = root / CANDIDATES_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing mirrored-test candidate evidence differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    freeze_protocol()
    run_mechanics(repository_root=ROOT.parents[1])
