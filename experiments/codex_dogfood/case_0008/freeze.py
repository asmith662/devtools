# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, C901, E501, EM101, EM102, INP001, PLR0912, PLR0915, S101, T201, TRY003
"""Freeze/verify Case 0008 native inputs without any task-relative execution."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import hashlib
import importlib
import importlib.metadata
import io
import json
import pickle
import sys
import tarfile
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Never

if TYPE_CHECKING:
    from collections.abc import Callable

from devtools.context.localization import (
    LocalizationAnchor,
    LocalizationAnchorIdentity,
    LocalizationLexicalAcquisitionRequest,
    LocalizationObligation,
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    LocalizationTaskInterpretation,
    ObligationLexicalQuery,
    RequirementStatus,
    SatisfactionCriterion,
    TaskProvenance,
)
from devtools.context.localization.association import (
    PythonImportDependencyProjectionRequest,
    PythonImportDependencySourceInput,
    PythonReferenceProjectionRequest,
    PythonReferenceSourceInput,
)
from devtools.context.localization.association.imports import (
    validate_import_dependency_frame,
)
from devtools.context.localization.association.references import (
    validate_reference_frame,
)
from devtools.context.localization.generation import ProjectionKind
from devtools.context.localization.grounding import (
    AnchorGroundingRequest,
    PythonDirectDeclarationKind,
    PythonDirectDeclarationLocator,
    PythonModuleLocator,
)
from devtools.context.localization.roles import (
    RepositoryRoleEvidenceInputs,
    RepositoryRoleKind,
    derive_repository_role_evidence,
)
from devtools.context.localization.routing import ObligationRolePreference
from devtools.context.python.classes import derive_python_class_method_declarations
from devtools.context.python.function.declarations import (
    derive_python_function_declarations,
)
from devtools.context.python.imports import (
    derive_python_import_declarations,
    resolve_python_import_declaration,
)
from devtools.context.python.mirrored_paths import (
    derive_python_mirrored_path_correspondences,
)
from devtools.context.python.modules import (
    PythonModuleKind,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    derive_python_immediate_package_memberships,
    interpret_python_module_resources,
)
from devtools.context.python.project_configuration import (
    PythonConfigurationFrame,
    analyze_python_project_configuration,
    resolve_python_project_configuration,
)
from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import FileFormat, TextFile, read, write

CASE = Path(__file__).resolve().parent
ROOT = CASE.parents[2]
START = "6a121f4b2f3391565df36f1ab2c0975e303cb2c5"
REPOSITORY = Repository(RepositoryId.parse("fe2c8984-a021-4342-9e31-404a6cf07707"))
TASK = (
    "Implement the first production unresolved-frontier and bounded acquisition-request capability for Localization. "
    "The capability should let an incomplete Localization assessment represent exactly what repository observation or evidence is still missing for an applicable obligation, "
    "preserve task, obligation, repository/snapshot, candidate-hypothesis and native evidence provenance, "
    "distinguish unresolved evidence from accepted witness support and from justified non-applicability, "
    "and express bounded follow-up acquisition requests without selecting Retrieval algorithms or claiming that requested evidence will satisfy the obligation. "
    "Integrate coherently with the existing task interpretation, anchor grounding, candidate witness association, witness generation, accepted witness alternatives, "
    "LocalizationAssessment and readiness contracts; preserve deterministic identity and replay validation; "
    "expose enough structure for future autonomous orchestration to request additional repository evidence without moving orchestration policy into Localization; "
    "add rigorous tests and authoritative architecture/development documentation; preserve package/API conventions where applicable; and pass protected development validation. "
    "Do not implement automatic hypothesis resolution, candidate elimination, numeric confidence, learned ranking, autonomous acquisition execution, Context Planning admission, or agent retry policy."
)
STATUS = "FROZEN BEFORE RETRIEVAL, ROUTING, GROUNDING, STRUCTURAL GENERATION AND ADJUDICATION"
ARTIFACTS = (
    "treatment.json",
    "README.md",
    "freeze.py",
    "test_freeze.py",
    "pre_execution.json",
    "inputs.pkl.gz",
)
FORBIDDEN_OUTPUTS = (
    "execution_started.json",
    "stage_b_raw.pkl.gz",
    "capture.pkl.gz",
    "retrieval.json",
    "routing.json",
    "grounding.json",
    "generation.json",
    "stage_b_integrity.json",
    "analysis.json",
    "adjudication",
)
FORBIDDEN_OPERATIONS = frozenset(
    {
        "acquire_localization_lexical_evidence",
        "retrieve_repository_text_documents_by_bm25",
        "retrieve_repository_text_documents_by_content_bm25",
        "analyze_repository_text_lexical_query",
        "route_localization_lexical_evidence",
        "ground_task_anchor",
        "build_anchor_grounding_view",
        "generate_witness_hypotheses",
        "project_referencing_resources",
        "project_direct_import_dependencies",
        "owner_resource",
        "validate_structural_support",
        "assess_localization_readiness",
        "build_candidate_witness_view",
        "select_python_module_source_declarations",
        "_project",
    },
)


def sha(content: bytes) -> str:
    """Digest frozen artifact bytes."""
    return hashlib.sha256(content).hexdigest()


def binary(path: Path) -> bytes:
    """Read bounded text through the substrate or the explicit binary boundary."""
    if path.suffix == ".gz":
        with path.open("rb") as stream:
            content = stream.read((128 << 20) + 1)
        if len(content) > 128 << 20:
            raise ValueError("Native archive exceeds the 128 MiB compressed bound.")
        return content
    value = read(resolve_path(path), file_format=FileFormat.TEXT, max_bytes=128 << 20)
    assert isinstance(value, TextFile)
    return value.content.replace("\r\n", "\n").encode()


def json_bytes(value: object) -> bytes:
    """Encode stable, newline-terminated JSON."""
    return (
        json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode()


def put_text(path: Path, content: str) -> None:
    """Use canonical atomic text writes with refusal to overwrite."""
    path.parent.mkdir(parents=True, exist_ok=True)
    write(TextFile(resolve_path(path), content), overwrite=False)


async def git(*args: str) -> bytes:
    """Read bounded committed metadata/content through managed commands."""
    result = await CommandExecutor(
        output_policy=CommandOutputPolicy(max_stdout_bytes=64 << 20),
    ).execute(
        Command("git").args(*args).cwd(resolve_path(ROOT)),
    )
    if result.failed or result.stdout_truncated:
        raise ValueError(f"Incomplete Git command: {args[:2]}")
    return result.stdout


def eligible(path: str) -> bool:
    """Select a broad textual frame using only outcome-independent addresses."""
    if path in {
        "README.md",
        "AGENTS.md",
        "pyproject.toml",
        "scripts/validate_development.py",
    }:
        return True
    parts = path.split("/")
    return (
        parts[0] in {"src", "tests", "docs"}
        and Path(path).suffix in {".py", ".md", ".toml", ".yaml", ".yml"}
        and path != "docs/implementation_ledger.md"
        and not path.startswith(
            ("tests/experiments/", "docs/research/", "docs/reports/"),
        )
        and not any(
            part in {"__pycache__", ".pytest_cache", ".ruff_cache"}
            or "confirmation" in part.lower()
            for part in parts
        )
    )


@contextmanager
def stage_a_guard():
    """Tripwire every loaded production alias for prohibited treatment calls."""
    # Load adapter modules solely to expose their function aliases to the guard.
    for name in (
        "devtools.context.localization.generation.references",
        "devtools.context.localization.generation.imports",
        "devtools.context.localization.routing.derive",
    ):
        importlib.import_module(name)
    attempts = dict.fromkeys(sorted(FORBIDDEN_OPERATIONS), 0)
    originals = []

    def blocked(name: str) -> Callable[..., Never]:
        def fail(*_args: object, **_kwargs: object) -> Never:
            attempts[name] += 1
            raise RuntimeError(f"Stage A forbids treatment operation: {name}")

        return fail

    for module_name, module in tuple(sys.modules.items()):
        if module is None or not module_name.startswith("devtools.context."):
            continue
        for attribute, value in tuple(vars(module).items()):
            name = getattr(value, "__name__", None)
            if callable(value) and name in FORBIDDEN_OPERATIONS:
                originals.append((module, attribute, value))
                setattr(module, attribute, blocked(name))
    try:
        yield attempts
    finally:
        for module, attribute, value in originals:
            setattr(module, attribute, value)


def contracts(treatment: dict):
    """Construct task/query/preferences and typed locators, never resolve them."""
    if treatment["task_full_prompt"] != TASK or treatment["status"] != STATUS:
        raise ValueError("Exact frozen task or Stage A status differs.")
    identity = LocalizationTaskIdentity(treatment["task_identity"])
    anchors = {
        item["id"]: LocalizationAnchorIdentity(identity, item["id"])
        for item in treatment["anchors"]
    }
    obligations = {
        item["id"]: LocalizationObligationIdentity(identity, item["id"])
        for item in treatment["obligations"]
    }
    if len(anchors) != len(treatment["anchors"]) or len(obligations) != len(
        treatment["obligations"],
    ):
        raise ValueError("Duplicate task identities.")
    if any(item["witness_alternatives"] for item in treatment["obligations"]):
        raise ValueError("Stage A must not populate accepted gold witnesses.")
    task = LocalizationTaskInterpretation(
        identity,
        TaskProvenance("case_0008-exact-user-task"),
        tuple(
            LocalizationAnchor(
                anchors[item["id"]],
                item["text"],
                TaskProvenance(item["provenance"]),
            )
            for item in treatment["anchors"]
        ),
        tuple(
            LocalizationObligation(
                obligations[item["id"]],
                item["predicate"],
                tuple(anchors[key] for key in item["anchors"]),
                TaskProvenance(item["provenance"]),
                RequirementStatus[item["requirement"]],
                SatisfactionCriterion(**item["satisfaction"]),
                (),
                item["applicability_condition"],
            )
            for item in treatment["obligations"]
        ),
    )
    query_ids = {
        item["id"]: LocalizationQueryIdentity(identity, item["id"])
        for item in treatment["queries"]
    }
    queries = tuple(
        ObligationLexicalQuery(
            query_ids[item["id"]],
            obligations[item["obligation"]],
            item["text"],
        )
        for item in treatment["queries"]
    )
    preferences = tuple(
        ObligationRolePreference(
            query_ids[item["query"]],
            obligations[item["obligation"]],
            tuple(RepositoryRoleKind[role] for role in item["roles"]),
        )
        for item in treatment["role_preferences"]
    )
    if (
        len(query_ids) != len(queries)
        or {item.query for item in preferences} != set(query_ids.values())
        or len(preferences) != len(queries)
    ):
        raise ValueError("Query/preference identity coverage differs.")
    if {item["obligation"] for item in treatment["queries"]} | set(
        treatment["deliberate_no_query_obligations"],
    ) != set(obligations):
        raise ValueError("Obligation query coverage differs.")
    if any(
        pref.obligation != query.obligation
        for pref, query in zip(preferences, queries, strict=True)
    ):
        raise ValueError("Role preference obligation differs.")
    locators = {}
    for spec in treatment["grounding_specs"]:
        locator = spec["locator"]
        module = PythonModuleLocator(
            locator["module"],
            PythonModuleKind[locator["module_kind"]]
            if locator["kind"] == "module"
            else None,
        )
        if locator["kind"] == "module":
            typed = module
        elif locator["kind"] == "direct-declaration":
            typed = PythonDirectDeclarationLocator(
                module,
                locator["name"],
                PythonDirectDeclarationKind[locator["declaration_kind"]],
            )
        else:
            raise ValueError("Unsupported locator syntax.")
        if spec["id"] in locators or spec["anchor"] not in anchors:
            raise ValueError("Grounding spec identity/anchor differs.")
        locators[spec["id"]] = typed
    if set(treatment["ungrounded_anchors"]) != set(anchors) - {
        item["anchor"] for item in treatment["grounding_specs"]
    }:
        raise ValueError("Ungrounded anchor accounting differs.")
    specs = {item["id"]: item for item in treatment["grounding_specs"]}
    recipe_ids = set()
    for recipe in treatment["recipes"]:
        key = (recipe["obligation"], recipe["id"])
        if (
            key in recipe_ids
            or recipe["obligation"] not in obligations
            or not recipe["members"]
        ):
            raise ValueError("Recipe identity/obligation differs.")
        recipe_ids.add(key)
        names = [member["key"] for member in recipe["members"]]
        if len(names) != len(set(names)):
            raise ValueError("Recipe repeats a member key.")
        branching = 0
        for member in recipe["members"]:
            op = ProjectionKind[member["projection"]]
            spec = specs[member["grounding"]]
            obligation = next(
                item
                for item in treatment["obligations"]
                if item["id"] == recipe["obligation"]
            )
            if spec["anchor"] not in obligation["anchors"]:
                raise ValueError("Recipe grounding anchor is not linked to obligation.")
            is_branch = member["multiplicity"] == "branching"
            if member["multiplicity"] not in {"fixed", "branching"}:
                raise ValueError("Unsupported member multiplicity.")
            required_branch = op in {
                ProjectionKind.REFERENCING_RESOURCE,
                ProjectionKind.DIRECT_IMPORT_DEPENDENCY_RESOURCE,
            }
            if is_branch != required_branch:
                raise ValueError(
                    "Projection requires its prescribed member multiplicity.",
                )
            if (
                op is ProjectionKind.REFERENCING_RESOURCE
                and spec["locator"]["kind"] != "direct-declaration"
            ):
                raise ValueError("Reference requires native declaration locator.")
            if (
                not member["reason"].strip()
                or (
                    is_branch
                    and member["max_results"]
                    != treatment["bounds"]["branch_max_results"]
                )
                or (not is_branch and member["max_results"] is not None)
            ):
                raise ValueError("Member reason/result bound differs.")
            branching += int(is_branch)
        if (
            branching > 1
            or (recipe["kind"] == "family") != bool(branching)
            or recipe["kind"] not in {"fixed", "family"}
        ):
            raise ValueError("Invalid fixed/branching recipe shape.")
    if treatment["bounds"]["branch_max_results"] < 1:
        raise ValueError("Result bound must be positive.")
    if set(treatment["operators"]) != {item.name for item in ProjectionKind}:
        raise ValueError("Operator identity coverage differs.")
    if set(treatment["no_recipe_obligations"]) != set(obligations) - {
        item["obligation"] for item in treatment["recipes"]
    }:
        raise ValueError("No-recipe obligation coverage differs.")
    return task, queries, preferences, locators


def prepare_native(snapshot, corpus, treatment: dict):
    """Build only query-independent RI/index inputs and unexecuted requests."""
    task, queries, preferences, locators = contracts(treatment)
    module_analyses = tuple(
        interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot(root),
            resource_addresses=tuple(
                item.address
                for item in snapshot.resources
                if item.address.value.startswith(prefix)
                and item.address.value.endswith(".py")
            ),
        )
        for root, prefix in (("src", "src/"), (".", "tests/"), (".", "scripts/"))
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=tuple(
            item for analysis in module_analyses for item in analysis.interpretations
        ),
    )
    memberships = tuple(
        derive_python_immediate_package_memberships(
            snapshot,
            interpretation_analysis=item,
        )
        for item in module_analyses
    )
    mirrors = derive_python_mirrored_path_correspondences(snapshot)
    declarations = analyze_python_project_configuration(
        snapshot,
        address=RepositoryResourceAddress("pyproject.toml"),
    )
    targets = resolve_python_project_configuration(
        snapshot,
        declarations,
        universe=universe,
        frame=PythonConfigurationFrame(PythonModuleRoot("."), PythonModuleRoot(".")),
    )
    roles = derive_repository_role_evidence(
        snapshot,
        inputs=RepositoryRoleEvidenceInputs(
            module_analyses,
            memberships,
            (mirrors,),
            (declarations,),
            (targets,),
        ),
    )
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analyze_repository_text_document_collection(
            document_collection=represent_repository_text_corpus(corpus=corpus),
        ),
    )
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)
    reference_sources = []
    import_sources = []
    declaration_inputs = []
    for module in universe.interpretations:
        reference_sources.append(
            PythonReferenceSourceInput(
                derive_python_declaration_references(
                    snapshot,
                    resource_address=module.resource.address,
                    module_universe=universe,
                    source_interpretations=(module,),
                ),
                (module,),
            ),
        )
        imports = derive_python_import_declarations(
            snapshot,
            resource_address=module.resource.address,
        )
        import_sources.append(
            PythonImportDependencySourceInput(
                module,
                imports,
                tuple(
                    resolve_python_import_declaration(
                        imports,
                        declaration,
                        target_universe=universe,
                        source_interpretations=(module,),
                    )
                    for declaration in imports.declarations
                ),
            ),
        )
        declaration_inputs.append(
            (
                module,
                derive_python_function_declarations(
                    snapshot,
                    resource_address=module.resource.address,
                ),
                derive_python_class_method_declarations(
                    snapshot,
                    resource_address=module.resource.address,
                ),
            ),
        )
    # Authorize the complete supplied domain without examining any seed's fanout.
    references = PythonReferenceProjectionRequest(
        universe,
        tuple(reference_sources),
        len(reference_sources),
    )
    imports = PythonImportDependencyProjectionRequest(
        universe,
        tuple(import_sources),
        len(import_sources),
    )
    requests = tuple(
        (
            spec["id"],
            AnchorGroundingRequest(
                task.identity,
                next(
                    item.identity
                    for item in task.anchors
                    if item.identity.value == spec["anchor"]
                ),
                snapshot.repository_id,
                snapshot.id,
                locators[spec["id"]],
                TaskProvenance(spec["provenance"]),
            ),
        )
        for spec in treatment["grounding_specs"]
    )
    return {
        "request": LocalizationLexicalAcquisitionRequest(
            task,
            treatment["purpose"],
            TASK,
            queries,
            snapshot,
            index,
            len(snapshot.resources),
        ),
        "corpus": corpus,
        "role_evidence": roles,
        "preferences": preferences,
        "module_analyses": module_analyses,
        "module_universe": universe,
        "declaration_inputs": tuple(declaration_inputs),
        "mirrors": mirrors,
        "python_references": references,
        "python_import_dependencies": imports,
        "grounding_requests": requests,
        "recipe_specs": treatment["recipes"],
    }


async def freeze() -> dict:
    """Create a single immutable Stage A checkpoint from selected committed blobs."""
    if any(
        (CASE / name).exists()
        for name in ("pre_execution.json", "inputs.pkl.gz", "integrity.json")
    ):
        raise FileExistsError("Stage A already frozen; never overwrite.")
    if (await git("rev-parse", "HEAD")).decode().strip() != START or (
        await git("branch", "--show-current")
    ).decode().strip() != "main":
        raise ValueError("Expected starting main/HEAD differs.")
    if await git("diff", "HEAD", "--name-only"):
        raise ValueError("Tracked worktree/index is not clean.")
    tree = (await git("ls-tree", "-r", "--name-only", START)).decode().splitlines()
    used = {
        path.split("/")[2]
        for path in tree
        if path.startswith("experiments/codex_dogfood/case_")
    }
    next_case = next(
        f"case_{index:04d}"
        for index in range(1, 10000)
        if f"case_{index:04d}" not in used
    )
    if next_case != CASE.name:
        raise ValueError("Case identifier is not the next unused committed identifier.")
    treatment = json.loads(binary(CASE / "treatment.json"))
    contracts(treatment)
    addresses = tuple(sorted(path for path in tree if eligible(path)))
    archive = await git("archive", "--format=tar", START, "--", *addresses)
    blobs = {}
    with stage_a_guard() as calls, TemporaryDirectory(prefix="case0008-") as temporary:
        exported = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            for member in bundle.getmembers():
                if not member.isfile():
                    continue
                if member.name not in addresses:
                    raise ValueError("Unexpected exported blob.")
                stream = bundle.extractfile(member)
                assert stream is not None
                content = stream.read()
                blobs[member.name] = sha(content)
                put_text(exported / member.name, content.decode())
        if set(blobs) != set(addresses):
            raise ValueError("Committed export identity coverage differs.")
        discovery = discover_repository_resource_addresses(
            repository=REPOSITORY,
            root=resolve_path(exported),
            maximum_resource_count=10000,
            maximum_traversal_entry_count=20000,
        )
        selected = tuple(RepositoryResourceAddress(address) for address in addresses)
        snapshot = observe_repository_resources(
            repository=REPOSITORY,
            root=resolve_path(exported),
            addresses=selected,
            maximum_resource_bytes=1 << 20,
        )
        corpus = realize_repository_text_corpus(
            definition=define_repository_text_corpus(
                discovery=discovery,
                selected_addresses=selected,
            ),
            snapshot=snapshot,
        )
        native = prepare_native(snapshot, corpus, treatment)
        if any(calls.values()):
            raise ValueError("A prohibited operation was attempted.")
        native["runtime"] = {
            "python_version": sys.version,
            "pickle_protocol": pickle.HIGHEST_PROTOCOL,
            "uv_lock": await git("show", f"{START}:uv.lock"),
            "pyproject": await git("show", f"{START}:pyproject.toml"),
            "packages": {
                name: importlib.metadata.version(name)
                for name in ("devtools", "pytest", "ruff", "mypy")
            },
        }
        payload = gzip.compress(
            pickle.dumps(native, protocol=pickle.HIGHEST_PROTOCOL),
            mtime=0,
        )
        # Canonical filesystem has no binary archive codec. Exclusive creation
        # at this experiment-only pickle/gzip boundary preserves refusal.
        with (CASE / "inputs.pkl.gz").open("xb") as output:
            output.write(payload)
        request = native["request"]
        manifest = {
            "schema": "case-0008-pre-execution-v1",
            "case": CASE.name,
            "status": STATUS,
            "starting_head": START,
            "treatment_sha256": sha(binary(CASE / "treatment.json")),
            "task_sha256": sha(TASK.encode()),
            "repository_id": str(snapshot.repository_id),
            "snapshot_id": str(snapshot.id),
            "corpus_id": str(corpus.id),
            "resource_count": len(addresses),
            "resources": [
                {
                    "address": item.address.value,
                    "content_identity": item.content_identity.value,
                    "git_blob_sha256": blobs[item.address.value],
                }
                for item in snapshot.resources
            ],
            "inputs_sha256": sha(payload),
            "implementation_sha256": {
                item.address.value: sha(item.content.replace("\r\n", "\n").encode())
                for item in snapshot.resources
                if item.address.value.startswith("src/devtools/")
                and item.address.value.endswith(".py")
            },
            "runtime": {
                "python_version": sys.version,
                "pickle_protocol": pickle.HIGHEST_PROTOCOL,
                "uv_lock_sha256": sha(native["runtime"]["uv_lock"]),
                "pyproject_sha256": sha(native["runtime"]["pyproject"]),
                "packages": native["runtime"]["packages"],
            },
            "bm25": {
                "k1": request.settings.k1,
                "b": request.settings.b,
                "filename_weight": 0.25,
                "maximum_results": len(addresses),
                "index_semantics": request.index.INDEX_SEMANTICS,
            },
            "routing": {
                "policy": "preferred positive role OR; native order within preferred/escape; global lane unchanged",
                "role_semantics": native["role_evidence"].SEMANTICS,
                "role_derivation_identity": native["role_evidence"].derivation_identity,
            },
            "mirror_frame": {
                "snapshot_id": str(snapshot.id),
                "resource_count": len(addresses),
                "scope": "all selected observed resources; native exact mirrored-path convention",
            },
            "reference_frame": {
                "source_analysis_count": len(native["python_references"].sources),
                "work_limit": native["python_references"].work_limit,
                "source_resources": [
                    item.analysis.derivation.dependency.resource.address.value
                    for item in native["python_references"].sources
                ],
                "coverage": "native bounded non-exhaustive declaration References; no task seed queried",
            },
            "import_frame": {
                "source_analysis_count": len(
                    native["python_import_dependencies"].sources,
                ),
                "work_limit": native["python_import_dependencies"].work_limit,
                "source_resources": [
                    {
                        "module_identity": item.module.identity,
                        "address": item.module.resource.address.value,
                        "content_identity": item.module.resource.content_identity.value,
                        "analysis_identity": item.analysis.derivation_identity,
                    }
                    for item in native["python_import_dependencies"].sources
                ],
                "coverage": "exhaustive direct Module.body import declarations and all canonical module resolutions in explicit universe; no task seed projected",
            },
            "module_frame": {
                "roots": [item.module_root.value for item in native["module_analyses"]],
                "scope": "src under src; tests and protected script under repository root; exact selected resources only",
                "universe_identity": native["module_universe"].identity,
                "interpretation_count": len(native["module_universe"].interpretations),
                "declaration_input_count": len(native["declaration_inputs"]),
            },
            "counts": {
                "anchors": len(treatment["anchors"]),
                "obligations": len(treatment["obligations"]),
                "lexical_lanes": 1 + len(treatment["queries"]),
                "routed_lanes": len(treatment["queries"]),
                "grounding_requests": len(native["grounding_requests"]),
                "recipe_specs": len(treatment["recipes"]),
                "expected_judgment_cells": len(addresses)
                * len(treatment["obligations"]),
            },
            "observation_bounds": {
                "resources": 10000,
                "traversal_entries": 20000,
                "resource_bytes": 1 << 20,
            },
            "forbidden_operation_attempts": calls,
            "stage_b_outputs": "ABSENT",
        }
        put_text(CASE / "pre_execution.json", json_bytes(manifest).decode())
    integrity = {
        "schema": "case-0008-integrity-v1",
        "normalization": "UTF-8 text LF; compressed binary exact",
        "sha256": {name: sha(binary(CASE / name)) for name in ARTIFACTS},
    }
    put_text(CASE / "integrity.json", json_bytes(integrity).decode())
    return validate()


def validate(*, allow_stage_b: bool = False) -> dict:
    """Read-only verification of exact frozen correspondence; never run treatment."""
    if not allow_stage_b and any((CASE / name).exists() for name in FORBIDDEN_OUTPUTS):
        raise ValueError("Stage B/later output exists in this Stage A checkpoint.")
    integrity = json.loads(binary(CASE / "integrity.json"))
    if set(integrity["sha256"]) != set(ARTIFACTS):
        raise ValueError("Frozen artifact identity coverage differs.")
    for name, digest in integrity["sha256"].items():
        if sha(binary(CASE / name)) != digest:
            raise ValueError(f"Frozen artifact digest differs: {name}")
    treatment = json.loads(binary(CASE / "treatment.json"))
    manifest = json.loads(binary(CASE / "pre_execution.json"))
    if (
        manifest["schema"] != "case-0008-pre-execution-v1"
        or manifest["case"] != CASE.name
        or manifest["starting_head"] != START
        or manifest["status"] != STATUS
        or manifest["task_sha256"] != sha(TASK.encode())
    ):
        raise ValueError("Pre-execution identity/status differs.")
    with stage_a_guard() as calls:
        task, queries, preferences, locators = contracts(treatment)
        compressed = binary(CASE / "inputs.pkl.gz")
        if (
            sha(compressed) != manifest["inputs_sha256"]
            or sha(binary(CASE / "treatment.json")) != manifest["treatment_sha256"]
        ):
            raise ValueError("Archive/treatment binding differs.")
        # Only load digest-checked repository-owned pickle at this local boundary.
        native = pickle.loads(gzip.decompress(compressed))  # noqa: S301
        request = native["request"]
        snapshot = request.snapshot
        if (
            request.task != task
            or request.obligation_queries != queries
            or native["preferences"] != preferences
            or request.purpose != treatment["purpose"]
            or request.full_task_query != TASK
            or native["recipe_specs"] != treatment["recipes"]
        ):
            raise ValueError(
                "Native task/query/preference/spec correspondence differs.",
            )
        if (
            str(snapshot.repository_id),
            str(snapshot.id),
            str(native["corpus"].id),
        ) != (
            manifest["repository_id"],
            manifest["snapshot_id"],
            manifest["corpus_id"],
        ):
            raise ValueError("Repository/snapshot/corpus identity differs.")
        resources = snapshot.resources
        expected_counts = {
            "anchors": len(task.anchors),
            "obligations": len(task.obligations),
            "lexical_lanes": 1 + len(queries),
            "routed_lanes": len(preferences),
            "grounding_requests": len(locators),
            "recipe_specs": len(treatment["recipes"]),
            "expected_judgment_cells": len(resources) * len(task.obligations),
        }
        if manifest["counts"] != expected_counts:
            raise ValueError("Frozen interpretation/count correspondence differs.")
        if manifest["bm25"] != {
            "k1": request.settings.k1,
            "b": request.settings.b,
            "filename_weight": 0.25,
            "maximum_results": len(resources),
            "index_semantics": request.index.INDEX_SEMANTICS,
        } or (request.settings.k1, request.settings.b) != (1.2, 0.75):
            raise ValueError("Frozen BM25 settings differ.")
        if (
            len(resources) != manifest["resource_count"]
            or request.maximum_results != len(resources)
            or len({item.address for item in resources}) != len(resources)
            or native["corpus"].resources != resources
            or native["role_evidence"].resources != resources
        ):
            raise ValueError("Frozen eligible resource coverage differs.")
        if len(native["declaration_inputs"]) != len(
            native["module_universe"].interpretations,
        ):
            raise ValueError("Frozen declaration input coverage differs.")
        for resource, row in zip(resources, manifest["resources"], strict=True):
            if (
                resource.address.value != row["address"]
                or resource.content_identity.value != row["content_identity"]
                or sha(resource.content.encode()) != row["git_blob_sha256"]
                or not eligible(resource.address.value)
            ):
                raise ValueError("Frozen resource identity/content differs.")
        for name, digest in manifest["implementation_sha256"].items():
            if sha(binary(ROOT / name)) != digest:
                raise ValueError(f"Production implementation drift: {name}")
        for key in ("uv_lock", "pyproject"):
            if sha(native["runtime"][key]) != manifest["runtime"][key + "_sha256"]:
                raise ValueError("Frozen runtime configuration digest differs.")
        if (
            native["runtime"]["python_version"] != sys.version
            or native["runtime"]["packages"]
            != {
                name: importlib.metadata.version(name)
                for name in native["runtime"]["packages"]
            }
            or native["runtime"]["packages"] != manifest["runtime"]["packages"]
        ):
            raise ValueError("Runtime implementation/version correspondence differs.")
        references = native["python_references"]
        imports = native["python_import_dependencies"]
        validate_reference_frame(references, snapshot)
        validate_import_dependency_frame(imports, snapshot)
        if (
            references.module_universe != native["module_universe"]
            or imports.module_universe != native["module_universe"]
            or len(references.sources) != references.work_limit
            or len(imports.sources) != imports.work_limit
            or len(references.sources)
            != manifest["reference_frame"]["source_analysis_count"]
            or len(imports.sources) != manifest["import_frame"]["source_analysis_count"]
        ):
            raise ValueError("Native relation input frame/bounds differs.")
        if [
            (key, value.locator) for key, value in native["grounding_requests"]
        ] != list(locators.items()):
            raise ValueError("Unexecuted grounding request correspondence differs.")
        if any(
            value.repository_id != snapshot.repository_id
            or value.snapshot_id != snapshot.id
            or value.task != task.identity
            for _, value in native["grounding_requests"]
        ):
            raise ValueError("Grounding request frame differs.")
        if any(calls.values()) or any(
            manifest["forbidden_operation_attempts"].values(),
        ):
            raise ValueError("Prohibited operation attempted.")
    return {
        "case": CASE.name,
        **manifest["counts"],
        "resources": len(resources),
        "reference_sources": len(references.sources),
        "import_sources": len(imports.sources),
        "treatment_operations": "NOT EXECUTED",
        "inputs_sha256": manifest["inputs_sha256"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("freeze", "verify"))
    parser.add_argument(
        "--allow-stage-b",
        action="store_true",
        help="Read-only frozen-input verification during later Stage B recovery.",
    )
    arguments = parser.parse_args()
    if arguments.command == "freeze" and arguments.allow_stage_b:
        parser.error("--allow-stage-b is valid only for read-only verify")
    print(
        json.dumps(
            asyncio.run(freeze())
            if arguments.command == "freeze"
            else validate(allow_stage_b=arguments.allow_stage_b),
            indent=2,
        ),
    )
