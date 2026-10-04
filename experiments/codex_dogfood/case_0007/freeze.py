# Copyright (c) 2026
# ruff: noqa: E501, PLR0915, PLR2004, PT018, S101, T201
"""Prepare and validate native Stage A inputs; never execute the treatment.

Git is used through managed Commands for a bounded tracked-address inventory.
Canonical Repository observation, corpus/index construction and Python RI own
native truth. Case-local framing is research composition, not a new framework
discovery policy or production persistence API.
"""

from __future__ import annotations

import argparse
import asyncio
import gzip
import hashlib
import json
import pickle
import platform
import re
import sys
from pathlib import Path
from typing import Any

from devtools.context.localization import LocalizationLexicalAcquisitionRequest
from devtools.context.localization.association.references import (
    PythonReferenceProjectionRequest,
    PythonReferenceSourceInput,
    validate_reference_frame,
)
from devtools.context.localization.roles import (
    RepositoryRoleEvidenceInputs,
    derive_repository_role_evidence,
)
from devtools.context.python import derive_python_mirrored_path_correspondences
from devtools.context.python.classes import derive_python_class_method_declarations
from devtools.context.python.function import derive_python_function_declarations
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    derive_python_immediate_package_memberships,
    interpret_python_module_resources,
)
from devtools.context.python.project_configuration import (
    analyze_python_project_configuration,
)
from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.filename import (
    build_repository_text_filename_lexical_index,
)
from devtools.context.retrieval.lexical.index import (
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from experiments.codex_dogfood.case_0007 import treatment as t
from experiments.codex_dogfood.case_0007.frame import TrackedFrameDiscovery

ROOT = Path(__file__).resolve().parents[3]
CASE = Path(__file__).resolve().parent
AUTHORING_SURFACES = (
    "AGENTS.md",
    "docs/documentation_map.md",
    "docs/architecture/taxonomy.md",
    "docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md",
    "docs/backlog/overview.md",
    "docs/backlog/metadata.md",
    "docs/backlog/epics/B-0002-coding-context-substrate.md",
    "src/devtools/context/localization/docs/overview.md",
    "src/devtools/context/python/docs/overview.md",
    "src/devtools/context/python/modules/docs/overview.md",
    "src/devtools/context/python/references/docs/overview.md",
    "src/devtools/context/python/__init__.py",
    "src/devtools/context/python/modules/__init__.py",
    "src/devtools/context/python/imports/__init__.py",
    "src/devtools/context/python/function/__init__.py",
    "src/devtools/context/python/classes/__init__.py",
    "src/devtools/context/python/references/declarations/__init__.py",
)
OPERATIONS = (
    "lexical_acquisition",
    "routing",
    "exact_grounding",
    "owner_generation",
    "mirror_generation",
    "reference_generation",
    "adjudication",
    "development_implementation",
    "historical_gold_use",
    "confirmation_access",
)
MECHANICAL_SURFACES = (
    "experiments/codex_dogfood/capture.py",
    "experiments/codex_dogfood/case_0004/capture.py",
    "src/devtools/context/localization/__init__.py",
    "src/devtools/context/localization/task.py",
    "src/devtools/context/localization/obligation.py",
    "src/devtools/context/localization/lexical.py",
    "src/devtools/context/localization/grounding/contract.py",
    "src/devtools/context/localization/grounding/resolve.py",
    "src/devtools/context/localization/generation/__init__.py",
    "src/devtools/context/localization/generation/contract.py",
    "src/devtools/context/localization/association/references.py",
    "src/devtools/context/localization/roles/__init__.py",
    "src/devtools/context/localization/roles/models.py",
    "src/devtools/context/localization/roles/derivation.py",
    "src/devtools/context/localization/roles/inputs.py",
    "src/devtools/context/localization/routing/__init__.py",
    "src/devtools/context/localization/routing/models.py",
    "src/devtools/context/python/modules/interpretation.py",
    "src/devtools/context/python/modules/membership.py",
    "src/devtools/context/python/mirrored_paths.py",
    "src/devtools/context/python/references/declarations/analysis.py",
    "src/devtools/context/python/function/declarations.py",
    "src/devtools/context/python/classes/declarations.py",
    "src/devtools/context/python/project_configuration/__init__.py",
    "src/devtools/context/python/project_configuration/declarations.py",
    "src/devtools/context/repository/observation.py",
    "src/devtools/context/repository/corpus.py",
    "src/devtools/context/repository/discovery.py",
    "src/devtools/context/repository/document.py",
    "src/devtools/context/repository/identity.py",
    "src/devtools/context/repository/resource.py",
    "src/devtools/context/repository/snapshot.py",
    "src/devtools/context/retrieval/lexical/analysis.py",
    "src/devtools/context/retrieval/lexical/statistics.py",
    "src/devtools/context/retrieval/lexical/index.py",
    "src/devtools/context/retrieval/lexical/bm25.py",
    "src/devtools/context/retrieval/lexical/filename.py",
    "src/devtools/resources/commands/__init__.py",
    "src/devtools/resources/commands/docs/overview.md",
    "src/devtools/resources/commands/models/command.py",
    "src/devtools/resources/commands/models/result.py",
    "src/devtools/resources/commands/execution.py",
)
ARTIFACTS = (
    "README.md",
    "treatment.py",
    "freeze.py",
    "frame.py",
    "test_freeze.py",
    "__init__.py",
    "treatment.json",
    "pre_retrieval.json",
    "inputs.pkl.gz",
)
STAGE_B_OUTPUTS = (
    "capture.pkl.gz",
    "retrieval.json",
    "routing.json",
    "grounding.json",
    "generation.json",
    "stage_b",
    "adjudication",
)


def sha(content: bytes) -> str:
    """Hash exact artifact bytes."""
    return hashlib.sha256(content).hexdigest()


def text_bytes(path: Path) -> bytes:
    """Use canonical LF for implementation and textual artifact identities."""
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").encode("utf-8")


def write_json(path: Path, value: object) -> None:
    """Write case metadata with canonical deterministic JSON representation."""
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


async def git(*arguments: str) -> str:
    """Read Git metadata with explicit finite output/time limits."""
    executor = CommandExecutor(
        output_policy=CommandOutputPolicy(max_stdout_bytes=4_000_000),
    )
    result = await executor.execute(
        Command("git")
        .args(*arguments)
        .cwd(resolve_path(ROOT))
        .with_timeout(Duration.seconds(30)),
    )
    if result.failed or result.stdout_truncated or result.stderr_truncated:
        msg = "Required bounded Git metadata acquisition did not complete."
        raise ValueError(msg)
    return result.stdout.decode("utf-8")


def eligible(address: str) -> bool:
    """Select ordinary tracked textual resources without task-result inspection."""
    parts = address.split("/")
    if any(
        part.casefold()
        in {
            "experiments",
            "confirmation",
            "adjudication",
            "__pycache__",
            ".local",
            ".git",
            ".venv",
        }
        for part in parts
    ):
        return False
    if (
        address.startswith(("docs/research/", "docs/reports/"))
        or address == "docs/implementation_ledger.md"
    ):
        return False
    if address in {
        "README.md",
        "AGENTS.md",
        "pyproject.toml",
        "uv.lock",
        ".gitignore",
        ".gitattributes",
        ".python-version",
    }:
        return True
    if address == "scripts/validate_development.py":
        return True
    return parts[0] in {"src", "tests", "docs"} and Path(address).suffix.lower() in {
        ".py",
        ".md",
        ".toml",
        ".json",
        ".yaml",
        ".yml",
        ".ini",
        ".cfg",
        ".txt",
        ".rst",
    }


def treatment_json() -> dict[str, Any]:
    """Serialize all authored semantics without targets or production results."""
    return {
        "case": t.CASE,
        "status": t.STATUS,
        "task_identity": t.TASK_ID.value,
        "task": t.TASK,
        "purpose": t.PURPOSE,
        "provenance": {
            "source_identity": t.PROVENANCE.source_identity,
            "explanation": t.PROVENANCE.explanation,
        },
        "anchors": [{"identity": key, "text": text} for key, text in t.ANCHORS.items()],
        "obligations": [
            {
                "identity": key,
                "predicate": row[0],
                "anchors": row[1],
                "requirement": "mandatory",
                "applicability_condition": None,
                "satisfaction": {"name": row[2], "statement": row[3]},
                "witness_alternatives": [],
                "query_identity": f"q-{key}",
                "query": row[4],
                "preferred_roles": row[5],
            }
            for key, row in t.OBLIGATIONS.items()
        ],
        "global_query": t.TASK,
        "global_routed": False,
        "groundings": [
            {
                "identity": key,
                "anchor": row[0],
                "locator_kind": "PYTHON_MODULE"
                if row[1] == "MODULE"
                else "PYTHON_DECLARATION",
                "declaration_kind": None if row[1] == "MODULE" else row[1],
                "module": row[2],
                "name": row[3],
                "module_kind": "PACKAGE" if row[1] == "MODULE" else None,
            }
            for key, row in t.GROUNDINGS.items()
        ],
        "deliberately_ungrounded_anchors": [
            key
            for key in t.ANCHORS
            if key not in {row[0] for row in t.GROUNDINGS.values()}
        ],
        "recipe_specifications": t.recipe_specs(),
        "no_recipe_obligations": {
            "explicit-exposure": "New exposure/__all__ truth has no existing exact native locator or allowed projection; no fabricated relation.",
            "documentation": "Documentation authority is not an owner, mirror or Reference relation.",
            "validation": "Protected validation policy is not an allowed declaration-owner, mirror or Reference relation.",
        },
        "reference_bounds": {
            "max_results": t.REFERENCE_MAX_RESULTS,
            "result_rationale": "Shared budget of at most sixteen unresolved children per family bounds human review; no target fanout was inspected. Complete overflow abstains, never truncates.",
            "work_limit": t.REFERENCE_WORK_LIMIT,
            "work_unit": "distinct supplied source analyses authorized for replay/enumeration",
            "work_rationale": "Shared finite 4096-analysis budget permits a broad ordinary checkout frame; validate frame count fits before freeze without examining any seed's referencers.",
        },
        "authoring_surfaces": AUTHORING_SURFACES,
        "mechanical_inspection_surfaces": MECHANICAL_SURFACES,
        "historical_firewall": "No Case 0006 treatment/results/gold or historical Reference gold inspected. Aggregate motivation supplied by the user only.",
        "no_treatment_repair": True,
    }


async def freeze() -> None:
    """Create one pre-execution archive, refusing to overwrite frozen native state."""
    if (CASE / "inputs.pkl.gz").exists():
        msg = "Stage A native archive exists; refusing a second freeze."
        raise FileExistsError(msg)
    if (await git("rev-parse", "HEAD")).strip() != t.STARTING_HEAD or (
        await git("branch", "--show-current")
    ).strip() != "main":
        msg = "Stage A requires the expected main checkpoint."
        raise ValueError(msg)
    tracked = tuple(sorted((await git("ls-files")).splitlines()))
    addresses = tuple(
        RepositoryResourceAddress(item) for item in tracked if eligible(item)
    )
    for address in addresses:
        path = ROOT / address.value
        if not path.is_file() or path.is_symlink() or path.is_junction():
            msg = f"Eligible tracked address is not a regular file: {address}."
            raise ValueError(msg)
    repository = Repository(RepositoryId.parse("fe2c8984-a021-4342-9e31-404a6cf07707"))
    snapshot = observe_repository_resources(
        repository=repository,
        root=resolve_path(ROOT),
        addresses=addresses,
        maximum_resource_bytes=4_000_000,
    )
    discovery = TrackedFrameDiscovery(
        repository.id,
        resolve_path(ROOT),
        20_000,
        20_000,
        len(tracked),
        addresses,
    )
    if len(tracked) > discovery.maximum_traversal_entry_count:
        msg = "Tracked metadata inventory exceeds declared work budget."
        raise ValueError(msg)
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=addresses,
    )
    corpus = realize_repository_text_corpus(definition=definition, snapshot=snapshot)
    documents = represent_repository_text_corpus(corpus=corpus)
    analysis = analyze_repository_text_document_collection(
        document_collection=documents,
    )
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analysis,
    )
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)
    filename_index = build_repository_text_filename_lexical_index(
        document_collection=documents,
    )
    python_addresses = tuple(
        item.address
        for item in snapshot.resources
        if item.address.value.endswith(".py")
    )
    # Only src is an import root. Tests remain Reference sources, not installed modules.
    modules = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=python_addresses,
    )
    universe = define_python_module_interpretation_universe(
        repository_id=repository.id,
        interpretations=modules.interpretations,
    )
    memberships = derive_python_immediate_package_memberships(
        snapshot,
        interpretation_analysis=modules,
    )
    mirrors = derive_python_mirrored_path_correspondences(snapshot)
    configurations = analyze_python_project_configuration(
        snapshot,
        address=RepositoryResourceAddress("pyproject.toml"),
    )
    roles = derive_repository_role_evidence(
        snapshot,
        inputs=RepositoryRoleEvidenceInputs(
            modules=(modules,),
            memberships=(memberships,),
            mirrors=(mirrors,),
            configurations=(configurations,),
        ),
    )
    functions, classes, references = [], [], []
    for address in python_addresses:
        # No target-relative filtering, inverse lookup, grounding or projection here.
        functions.append(
            derive_python_function_declarations(snapshot, resource_address=address),
        )
        classes.append(
            derive_python_class_method_declarations(snapshot, resource_address=address),
        )
        source_interpretations = tuple(
            item
            for item in universe.interpretations
            if item.resource.address == address
        )
        native = derive_python_declaration_references(
            snapshot,
            resource_address=address,
            module_universe=universe,
            source_interpretations=source_interpretations,
        )
        references.append(PythonReferenceSourceInput(native, source_interpretations))
    if len(references) > t.REFERENCE_WORK_LIMIT:
        msg = "Frozen complete Reference frame does not fit prospective work budget."
        raise ValueError(msg)
    reference_request = PythonReferenceProjectionRequest(
        universe,
        tuple(references),
        t.REFERENCE_WORK_LIMIT,
    )
    queries, preferences = t.lexical_inputs()
    request = LocalizationLexicalAcquisitionRequest(
        t.interpretation(),
        t.PURPOSE,
        t.TASK,
        queries,
        snapshot,
        index,
        len(addresses),
    )
    inputs = {
        "lexical_request": request,
        "filename_index": filename_index,
        "roles": roles,
        "role_preferences": preferences,
        "modules": modules,
        "module_universe": universe,
        "memberships": memberships,
        "mirrors": mirrors,
        "configuration": configurations,
        "functions": tuple(functions),
        "classes": tuple(classes),
        "reference_request": reference_request,
        "grounding_requests": t.grounding_requests(snapshot),
        "recipe_specifications": t.recipe_specs(),
    }
    payload = gzip.compress(pickle.dumps(inputs, protocol=5), mtime=0)
    (CASE / "inputs.pkl.gz").write_bytes(payload)
    write_json(CASE / "treatment.json", treatment_json())
    implementation = {
        item: sha(text_bytes(ROOT / item))
        for item in tracked
        if item.startswith("src/") and item.endswith(".py")
    }
    manifest = {
        "case": t.CASE,
        "status": t.STATUS,
        "starting_head": t.STARTING_HEAD,
        "starting_subject": "Add direct-reference witness generation",
        "task_sha256": sha(t.TASK.encode()),
        "inputs_archive_sha256": sha(payload),
        "repository_id": str(repository.id),
        "snapshot_id": str(snapshot.id),
        "corpus_id": str(corpus.id),
        "frame_resource_count": len(addresses),
        "tracked_inventory_count": len(tracked),
        "inclusion_policy": "eligible() in freeze.py; tracked src, ordinary tests, authoritative docs, selected root files and protected validation entry point; textual suffixes only.",
        "exclusion_policy": "experiments/confirmation/adjudication/cache/local/untracked/binary/generated; historical research/reports/implementation ledger excluded from textual frame.",
        "snapshot_resources": [
            {
                "address": str(item.address),
                "content_identity": str(item.content_identity),
                "byte_size": item.byte_size,
            }
            for item in snapshot.resources
        ],
        "bm25": {
            "k1": request.settings.k1,
            "b": request.settings.b,
            "filename_weight": 0.25,
            "maximum_results": request.maximum_results,
            "tokenization": "Unicode regex \\w+ spans, casefold; no identifier splitting; distinct query terms scored",
            "tie": "corpus document order",
            "content": "whole-resource exact text",
            "filename": "final filename stem, independent BM25",
        },
        "routing_policy": "current two-tier preferred-role-supported then complete escape; native order within each; no removal; global unrouted",
        "native_frames": {
            "module_count": len(universe.interpretations),
            "module_universe_identity": universe.identity,
            "function_analysis_count": len(functions),
            "class_method_analysis_count": len(classes),
            "reference_source_analysis_count": len(reference_request.sources),
            "reference_coverage": "all eligible .py resources; native non-exhaustive semantic coverage retained; no source omitted",
            "reference_sources": [
                {
                    "address": str(
                        item.analysis.derivation.dependency.resource.address,
                    ),
                    "content_identity": str(
                        item.analysis.derivation.dependency.resource.content_identity,
                    ),
                    "analysis_identity": item.analysis.derivation.identity,
                    "source_interpretation_identities": [
                        module.identity for module in item.source_interpretations
                    ],
                }
                for item in reference_request.sources
            ],
            "mirrors_identity": mirrors.derivation.identity,
            "role_derivation_identity": roles.derivation_identity,
        },
        "implementation_sha256": implementation,
        "runtime": {
            "python": sys.version,
            "implementation": sys.implementation.name,
            "platform": platform.platform(),
            "uv_lock_sha256": sha(text_bytes(ROOT / "uv.lock")),
            "pyproject_sha256": sha(text_bytes(ROOT / "pyproject.toml")),
        },
        "operation_executed": dict.fromkeys(OPERATIONS, False),
        "native_preparation": "Observation, corpus/index, role evidence and query-independent Python module/declaration/membership/mirror/configuration/Reference RI preparation only; none is a treatment projection.",
    }
    write_json(CASE / "pre_retrieval.json", manifest)
    seal()
    validate()


def seal() -> None:
    """Seal Stage A artifacts only; never alter treatment/native inputs."""
    write_json(
        CASE / "integrity.json",
        {
            "schema": "case-0007-stage-a-integrity-v1",
            "files": {
                name: sha((CASE / name).read_bytes())
                if name.endswith(".gz")
                else sha(text_bytes(CASE / name))
                for name in ARTIFACTS
            },
        },
    )


def validate_specs(specs: list[dict[str, Any]], requests: dict) -> None:
    """Reject malformed specifications without evaluating native locators."""
    identities = set()
    obligations = t.OBLIGATIONS
    for spec in specs:
        identity = (spec["obligation"], spec["identity"])
        if (
            identity in identities
            or spec["obligation"] not in obligations
            or not spec["members"]
        ):
            msg = "Recipe identity, obligation or member shape is invalid."
            raise ValueError(msg)
        identities.add(identity)
        keys = set()
        branches = 0
        for member in spec["members"]:
            if (
                member["key"] in keys
                or member["grounding_request"] not in requests
                or not member["reason"]
            ):
                msg = "Recipe member key, request or reason is invalid."
                raise ValueError(msg)
            keys.add(member["key"])
            if member["multiplicity"] == "branching":
                branches += 1
                if (
                    member["operator"] != "REFERENCING_RESOURCE"
                    or member["max_results"] <= 0
                    or member["work_limit"] != t.REFERENCE_WORK_LIMIT
                ):
                    msg = "Branch relation or bounds are invalid."
                    raise ValueError(msg)
                if t.GROUNDINGS[member["grounding_request"]][1] == "MODULE":
                    msg = "Reference branch requires an explicit declaration locator."
                    raise ValueError(msg)
            elif member["multiplicity"] != "fixed" or member["operator"] not in {
                "OWNER_RESOURCE",
                "MIRRORED_RESOURCE",
            }:
                msg = "Fixed member relation is invalid."
                raise ValueError(msg)
        if branches > 1 or spec["identity_kind"] != (
            "family" if branches else "caller-hypothesis"
        ):
            msg = "Recipe multiplicity or family identity is invalid."
            raise ValueError(msg)


def validate() -> dict:  # noqa: C901
    """Check archive integrity and frame/bindings; execute no treatment operation."""
    integrity = json.loads((CASE / "integrity.json").read_text(encoding="utf-8"))
    if set(integrity["files"]) != set(ARTIFACTS):
        msg = "Integrity artifact set differs from the frozen schema."
        raise ValueError(msg)
    for name, expected in integrity["files"].items():
        content = (
            (CASE / name).read_bytes()
            if name.endswith(".gz")
            else text_bytes(CASE / name)
        )
        if sha(content) != expected:
            msg = f"Stage A integrity mismatch: {name}."
            raise ValueError(msg)
    manifest = json.loads((CASE / "pre_retrieval.json").read_text(encoding="utf-8"))
    frozen = json.loads((CASE / "treatment.json").read_text(encoding="utf-8"))
    if (
        frozen != json.loads(json.dumps(treatment_json()))
        or manifest["status"] != t.STATUS
        or manifest["starting_head"] != t.STARTING_HEAD
    ):
        msg = "Authored treatment or starting state differs from frozen metadata."
        raise ValueError(msg)
    payload = (CASE / "inputs.pkl.gz").read_bytes()
    if sha(payload) != manifest["inputs_archive_sha256"]:
        msg = "Native archive digest differs from the pre-execution manifest."
        raise ValueError(msg)
    inputs = pickle.loads(gzip.decompress(payload))  # noqa: S301
    request = inputs["lexical_request"]
    snapshot = request.snapshot
    corpus = (
        request.index.corpus_statistics.collection_analysis.document_collection.corpus
    )
    queries, preferences = t.lexical_inputs()
    assert (
        request.task == t.interpretation()
        and request.full_task_query == t.TASK
        and request.purpose == t.PURPOSE
    )
    assert (
        request.obligation_queries == queries
        and inputs["role_preferences"] == preferences
    )
    assert (
        request.maximum_results
        == len(snapshot.resources)
        == manifest["frame_resource_count"]
    )
    assert corpus.resources == snapshot.resources
    assert (
        str(snapshot.repository_id) == manifest["repository_id"]
        and str(snapshot.id) == manifest["snapshot_id"]
        and str(corpus.id) == manifest["corpus_id"]
    )
    assert inputs["grounding_requests"] == t.grounding_requests(snapshot)
    assert inputs["recipe_specifications"] == t.recipe_specs()
    assert inputs["reference_request"].module_universe == inputs["module_universe"]
    assert inputs["reference_request"].work_limit == t.REFERENCE_WORK_LIMIT
    assert len(inputs["reference_request"].sources) <= t.REFERENCE_WORK_LIMIT
    validate_reference_frame(inputs["reference_request"], snapshot)
    validate_specs(inputs["recipe_specifications"], inputs["grounding_requests"])
    assert inputs["roles"].resources == snapshot.resources
    assert inputs["roles"].snapshot_id == snapshot.id
    assert len(queries) == len(preferences) == len(request.task.obligations)
    assert set(manifest["operation_executed"]) == set(OPERATIONS) and not any(
        manifest["operation_executed"].values(),
    )
    assert all(not (CASE / name).exists() for name in STAGE_B_OUTPUTS)
    assert manifest["task_sha256"] == sha(t.TASK.encode())
    assert request.settings.k1 == manifest["bm25"]["k1"] == 1.2
    assert request.settings.b == manifest["bm25"]["b"] == 0.75
    identities = [
        {
            "address": str(item.address),
            "content_identity": str(item.content_identity),
            "byte_size": item.byte_size,
        }
        for item in snapshot.resources
    ]
    assert identities == manifest["snapshot_resources"]
    python_addresses = {
        item.address
        for item in snapshot.resources
        if item.address.value.endswith(".py")
    }
    assert {
        item.analysis.derivation.dependency.resource.address
        for item in inputs["reference_request"].sources
    } == python_addresses
    assert len(inputs["functions"]) == len(inputs["classes"]) == len(python_addresses)
    for analyses in (inputs["functions"], inputs["classes"]):
        assert {
            item.derivation.dependency.resource.address for item in analyses
        } == python_addresses
        for item in analyses:
            dependency = item.derivation.dependency
            assert dependency.snapshot_id == snapshot.id
            assert dependency.repository_id == snapshot.repository_id
            assert dependency.resource == snapshot.resource_at(
                dependency.resource.address,
            )
    assert inputs["modules"].snapshot_id == snapshot.id
    assert inputs["modules"].repository_id == snapshot.repository_id
    assert (
        inputs["modules"].interpretations == inputs["module_universe"].interpretations
    )
    assert (
        inputs["mirrors"].derivation.identity
        == manifest["native_frames"]["mirrors_identity"]
    )
    assert (
        inputs["roles"].derivation_identity
        == manifest["native_frames"]["role_derivation_identity"]
    )
    # Role input validation canonicalizes presentation order independently of the
    # Reference universe's retained original order. Compare native facts/scope.
    (role_module,) = inputs["roles"].inputs.modules
    assert role_module.repository_id == snapshot.repository_id
    assert role_module.snapshot_id == snapshot.id
    assert role_module.module_root == inputs["modules"].module_root
    assert set(role_module.interpretations) == set(inputs["modules"].interpretations)
    assert set(role_module.exclusions) == set(inputs["modules"].exclusions)
    (role_membership,) = inputs["roles"].inputs.memberships
    assert (
        role_membership.derivation.identity == inputs["memberships"].derivation.identity
    )
    assert set(role_membership.memberships) == set(inputs["memberships"].memberships)
    assert set(role_membership.assessments) == set(inputs["memberships"].assessments)
    assert role_membership.coverage == inputs["memberships"].coverage
    assert inputs["roles"].inputs.mirrors == (inputs["mirrors"],)
    assert inputs["roles"].inputs.configurations == (inputs["configuration"],)
    assert (
        len(inputs["reference_request"].sources)
        == manifest["native_frames"]["reference_source_analysis_count"]
    )
    reference_rows = [
        {
            "address": str(item.analysis.derivation.dependency.resource.address),
            "content_identity": str(
                item.analysis.derivation.dependency.resource.content_identity,
            ),
            "analysis_identity": item.analysis.derivation.identity,
            "source_interpretation_identities": [
                module.identity for module in item.source_interpretations
            ],
        }
        for item in inputs["reference_request"].sources
    ]
    assert reference_rows == manifest["native_frames"]["reference_sources"]
    assert (
        inputs["module_universe"].identity
        == manifest["native_frames"]["module_universe_identity"]
    )
    assert (
        len(inputs["module_universe"].interpretations)
        == manifest["native_frames"]["module_count"]
    )
    for link in re.findall(
        r"\]\(([^)#]+)(?:#[^)]*)?\)",
        (CASE / "README.md").read_text(encoding="utf-8"),
    ):
        assert (CASE / link).is_file()
    for path, expected in manifest["implementation_sha256"].items():
        assert sha(text_bytes(ROOT / path)) == expected
    for path in AUTHORING_SURFACES:
        assert path in {item.address.value for item in snapshot.resources}
    summary = {
        "case": t.CASE,
        "stage": "A only",
        "resources": len(snapshot.resources),
        "grounding_requests": len(inputs["grounding_requests"]),
        "recipe_specifications": len(inputs["recipe_specifications"]),
        "reference_analyses": len(inputs["reference_request"].sources),
        "treatment_operations_executed": False,
    }
    print(json.dumps(summary, sort_keys=True))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("freeze", "validate", "seal"))
    arguments = parser.parse_args()
    if arguments.mode == "freeze":
        asyncio.run(freeze())
    elif arguments.mode == "seal":
        seal()
    else:
        validate()
