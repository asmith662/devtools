# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, C901, COM812, E501, EM101, EM102, INP001, PLR0912, PLR0915, S101, T201, TRY003
"""Freeze Case 0006 treatment; never acquire, route, ground or generate."""

from __future__ import annotations

import asyncio
import gzip
import hashlib
import io
import json
import pickle
import sys
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory

from treatment import TASK, treatment

from devtools.context.localization.generation import ProjectionKind
from devtools.context.localization.grounding import (
    AnchorGroundingRequest,
    PythonDirectDeclarationKind,
    PythonDirectDeclarationLocator,
    PythonModuleLocator,
    ResourceAddressLocator,
)
from devtools.context.localization.identity import (
    LocalizationAnchorIdentity,
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    TaskProvenance,
)
from devtools.context.localization.lexical import (
    LocalizationLexicalAcquisitionRequest,
    ObligationLexicalQuery,
)
from devtools.context.localization.obligation import (
    LocalizationObligation,
    RequirementStatus,
    SatisfactionCriterion,
)
from devtools.context.localization.roles import derive_repository_role_evidence
from devtools.context.localization.roles.models import (
    RepositoryRoleEvidenceInputs,
    RepositoryRoleKind,
)
from devtools.context.localization.routing import ObligationRolePreference
from devtools.context.localization.task import (
    LocalizationAnchor,
    LocalizationTaskInterpretation,
)
from devtools.context.python.mirrored_paths import (
    derive_python_mirrored_path_correspondences,
)
from devtools.context.python.modules import (
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
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.index import (
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import FileFormat, TextFile, read, write

CASE = Path(__file__).resolve().parent
ROOT = CASE.parents[2]
START = "492229e0e0d4661cf5287c26d18c6488a80fe8ce"
REPOSITORY = Repository(RepositoryId.parse("d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"))


def sha(content: bytes) -> str:
    """Identify exact retained bytes."""
    return hashlib.sha256(content).hexdigest()


def binary(path: Path) -> bytes:
    """Use bounded canonical reads at the native archive boundary."""
    if path.suffix == ".gz":
        # Native compressed archive boundary: canonical filesystem currently
        # supplies neither a binary reading codec nor a binary writing codec.
        with path.open("rb") as source:
            content = source.read((64 << 20) + 1)
        if len(content) > 64 << 20:
            raise ValueError("Native archive exceeds the explicit 64 MiB bound.")
        return content
    result = read(resolve_path(path), file_format=FileFormat.TEXT, max_bytes=64 << 20)
    assert isinstance(result, TextFile)
    return result.content.encode("utf-8")


def json_bytes(value: object) -> bytes:
    """Serialize protocol JSON deterministically."""
    return (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode()


def postings(index) -> tuple:
    """Compare native postings without repeatedly comparing whole documents."""
    documents = {id(item) for item in index.corpus_statistics.document_statistics}
    result = []
    for term in index.term_postings:
        values = []
        for posting in term.postings:
            if id(posting.document_statistics) not in documents:
                raise ValueError(
                    "Posting does not reference native document statistics."
                )
            values.append(
                (
                    posting.document_statistics.analysis.document.id,
                    posting.term_frequency,
                )
            )
        result.append((term.normalized_term, tuple(values)))
    return tuple(result)


def put_text(path: Path, content: str) -> None:
    """Reuse canonical atomic text writes with overwrite refusal."""
    path.parent.mkdir(parents=True, exist_ok=True)
    write(TextFile(resolve_path(path), content), overwrite=False)


def eligible(path: str) -> bool:
    """Apply the outcome-independent frozen selection without opening blobs."""
    explicit = {
        "README.md",
        "AGENTS.md",
        "pyproject.toml",
        "scripts/validate_development.py",
    }
    if path in explicit:
        return True
    parts = path.split("/")
    return (
        parts[0] in {"src", "docs", "tests"}
        and Path(path).suffix in {".py", ".md", ".toml", ".yaml", ".yml"}
        and path != "docs/implementation_ledger.md"
        and not path.startswith("tests/experiments/")
        and not any(
            part in {"__pycache__", ".pytest_cache", ".ruff_cache"} for part in parts
        )
    )


async def git(*args: str) -> bytes:
    """Use managed commands only; reject incomplete retained output."""
    result = await CommandExecutor(
        output_policy=CommandOutputPolicy(max_stdout_bytes=32 << 20),
    ).execute(Command("git").args(*args).cwd(resolve_path(ROOT)))
    if result.failed or result.stdout_truncated:
        raise ValueError(f"Incomplete Git command: {args[:2]}")
    return result.stdout


def task_inputs(treatment: dict) -> tuple:
    """Construct production caller contracts without acquisition or routing."""
    task_id = LocalizationTaskIdentity(treatment["task_identity"])
    provenance = TaskProvenance(
        sha(treatment["task_full_prompt"].encode()),
        explanation="Frozen caller-authored task interpretation.",
    )
    anchors = tuple(
        LocalizationAnchor(
            LocalizationAnchorIdentity(task_id, item["identity"]),
            item["text"],
            provenance,
        )
        for item in treatment["anchors"]
    )
    obligations = tuple(
        LocalizationObligation(
            LocalizationObligationIdentity(task_id, item["identity"]),
            item["predicate"],
            tuple(
                LocalizationAnchorIdentity(task_id, anchor)
                for anchor in item["anchors"]
            ),
            provenance,
            RequirementStatus(item["requirement"]),
            SatisfactionCriterion(**item["satisfaction"]),
            (),
            item["applicability_condition"],
        )
        for item in treatment["obligations"]
    )
    queries = tuple(
        ObligationLexicalQuery(
            LocalizationQueryIdentity(task_id, item["identity"]),
            LocalizationObligationIdentity(task_id, item["obligation"]),
            item["text"],
        )
        for item in treatment["obligation_queries"]
    )
    preferences = tuple(
        ObligationRolePreference(
            query.identity,
            query.obligation,
            tuple(RepositoryRoleKind[role] for role in item["preferred_roles"]),
        )
        for query, item in zip(queries, treatment["obligation_queries"], strict=True)
    )
    return (
        LocalizationTaskInterpretation(task_id, provenance, anchors, obligations),
        queries,
        preferences,
    )


def role_view(snapshot):
    """Apply frozen static RI recipe and retain grounding/mirror inputs."""
    modules = tuple(
        interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot(root),
            resource_addresses=tuple(
                resource.address
                for resource in snapshot.resources
                if resource.address.value.startswith(root + "/")
                and resource.address.value.endswith(".py")
            ),
        )
        for root in ("src", "tests")
    )
    memberships = tuple(
        derive_python_immediate_package_memberships(
            snapshot, interpretation_analysis=analysis
        )
        for analysis in modules
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=tuple(
            item for analysis in modules for item in analysis.interpretations
        ),
    )
    declarations = analyze_python_project_configuration(
        snapshot, address=RepositoryResourceAddress("pyproject.toml")
    )
    targets = resolve_python_project_configuration(
        snapshot,
        declarations,
        universe=universe,
        frame=PythonConfigurationFrame(PythonModuleRoot("."), PythonModuleRoot(".")),
    )
    mirrors = derive_python_mirrored_path_correspondences(snapshot)
    inputs = RepositoryRoleEvidenceInputs(
        modules,
        memberships,
        (mirrors,),
        (declarations,),
        (targets,),
    )
    return (
        derive_repository_role_evidence(snapshot, inputs=inputs),
        universe,
        modules,
        mirrors,
    )


def grounding_requests(treatment_data: dict, task, snapshot) -> dict:
    """Construct typed requests without invoking the grounding resolver."""
    requests = {}
    for item in treatment_data["grounding_requests"]:
        locator_data = item["locator"]
        if item["locator_kind"] == "PYTHON_DECLARATION":
            locator = PythonDirectDeclarationLocator(
                PythonModuleLocator(locator_data["module"]),
                locator_data["name"],
                PythonDirectDeclarationKind[locator_data["declaration_kind"]],
            )
        elif item["locator_kind"] == "RESOURCE_ADDRESS":
            locator = ResourceAddressLocator(
                RepositoryResourceAddress(locator_data["address"])
            )
        else:
            raise ValueError("Unsupported frozen locator family.")
        value = AnchorGroundingRequest(
            task.identity,
            LocalizationAnchorIdentity(task.identity, item["anchor"]),
            snapshot.repository_id,
            snapshot.id,
            locator,
            TaskProvenance(
                sha(treatment_data["task_full_prompt"].encode()),
                explanation=item["interpretation_provenance"]["explanation"],
            ),
        )
        if item["identity"] in requests:
            raise ValueError("Duplicate grounding request identity.")
        requests[item["identity"]] = value
    return requests


def validate_intent(treatment_data: dict, task, queries, preferences) -> None:
    """Check treatment references and exact vocabulary, never outcomes."""
    if treatment_data != treatment() or treatment_data["task_full_prompt"] != TASK:
        raise ValueError("Caller treatment differs from authored exact task.")
    if treatment_data["global_lane"]["query_text"] != TASK:
        raise ValueError("Global query differs from exact task.")
    anchors = {item.identity.value for item in task.anchors}
    obligations = {item.identity.value for item in task.obligations}
    if len(anchors) != len(task.anchors) or len(obligations) != len(task.obligations):
        raise ValueError("Duplicate task identities.")
    if {query.obligation.value for query in queries} != obligations:
        raise ValueError("Queries do not cover the obligation frame exactly.")
    if len(queries) != len(preferences) or len(queries) != len(obligations):
        raise ValueError("Query/preference cardinality differs.")
    request_ids = {item["identity"] for item in treatment_data["grounding_requests"]}
    if len(request_ids) != len(treatment_data["grounding_requests"]):
        raise ValueError("Grounding request identity repeats.")
    if any(
        item["anchor"] not in anchors for item in treatment_data["grounding_requests"]
    ):
        raise ValueError("Unknown grounding anchor.")
    recipe_ids = set()
    for recipe in treatment_data["generation_recipes"]:
        obligation = recipe["obligation"]
        identity = (obligation, recipe["identity"])
        if obligation not in obligations or identity in recipe_ids:
            raise ValueError("Unknown or repeated hypothesis recipe.")
        recipe_ids.add(identity)
        keys = [member["identity"] for member in recipe["members"]]
        if not keys or len(set(keys)) != len(keys):
            raise ValueError("Invalid complementary member identities.")
        for member in recipe["members"]:
            if member["grounding_request"] not in request_ids:
                raise ValueError("Recipe has unknown grounding request.")
            if member["projection"] not in ProjectionKind.__members__:
                raise ValueError("Recipe has unsupported projection.")
            grounding = next(
                item
                for item in treatment_data["grounding_requests"]
                if item["identity"] == member["grounding_request"]
            )
            owning = next(
                item
                for item in treatment_data["obligations"]
                if item["identity"] == obligation
            )
            if grounding["anchor"] not in owning["anchors"]:
                raise ValueError("Recipe anchor is not linked to its obligation.")
    without = {item["identity"] for item in treatment_data["obligations"]} - {
        item[0] for item in recipe_ids
    }
    if without != set(treatment_data["no_recipe_obligations"]):
        raise ValueError("No-recipe obligations are incompletely explained.")


async def freeze() -> None:
    """Retain committed corpus and static production inputs exactly once."""
    if any(
        (CASE / name).exists()
        for name in ("pre_retrieval.json", "inputs.pkl.gz", "integrity.json")
    ):
        raise FileExistsError("Frozen Stage A already exists; never overwrite it.")
    if (await git("rev-parse", "HEAD")).decode().strip() != START:
        raise ValueError("Starting commit changed.")
    treatment_data = json.loads(binary(CASE / "treatment.json"))
    task, queries, preferences = task_inputs(treatment_data)
    validate_intent(treatment_data, task, queries, preferences)
    addresses = tuple(
        path
        for path in (await git("ls-tree", "-r", "--name-only", START))
        .decode()
        .splitlines()
        if eligible(path)
    )
    # Export ONLY selected blobs: no historical case outcomes are read.
    archive = await git("archive", "--format=tar", START, "--", *addresses)
    with TemporaryDirectory(prefix="case0006-") as temporary:
        exported = Path(temporary)
        blob_digests = {}
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            for member in bundle.getmembers():
                if not member.isfile():
                    continue
                if member.name not in addresses:
                    raise ValueError("Export contains an ineligible blob.")
                stream = bundle.extractfile(member)
                assert stream is not None
                content = stream.read()
                blob_digests[member.name] = sha(content)
                put_text(exported / member.name, content.decode("utf-8"))
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
                discovery=discovery, selected_addresses=selected
            ),
            snapshot=snapshot,
        )
        statistics = calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=represent_repository_text_corpus(corpus=corpus)
            )
        )
        index = build_repository_text_lexical_inverted_index(
            corpus_statistics=statistics
        )
        roles, module_universe, module_analyses, mirrors = role_view(snapshot)
        groundings = grounding_requests(treatment_data, task, snapshot)
        request = LocalizationLexicalAcquisitionRequest(
            task,
            treatment_data["purpose"],
            treatment_data["task_full_prompt"],
            queries,
            snapshot,
            index,
            len(addresses),
        )
        native = {
            "request": request,
            "role_evidence": roles,
            "preferences": preferences,
            "module_universe": module_universe,
            "module_analyses": module_analyses,
            "mirrored_paths": mirrors,
            "grounding_requests": groundings,
            "generation_recipe_specs": treatment_data["generation_recipes"],
        }
        payload = gzip.compress(
            pickle.dumps(native, protocol=pickle.HIGHEST_PROTOCOL), mtime=0
        )
        # Pickle/gzip is an explicit experiment binary boundary. The canonical
        # filesystem writer currently has no binary codec; exclusive creation
        # preserves refusal rather than introducing a framework codec here.
        with (CASE / "inputs.pkl.gz").open("xb") as output:
            output.write(payload)
        manifest = dict(treatment_data)
        manifest.update(
            {
                "task_sha256": sha(request.full_task_query.encode()),
                "repository_id": str(snapshot.repository_id),
                "snapshot_id": str(snapshot.id),
                "eligible_corpus_id": str(corpus.id),
                "eligible_index_identity": {
                    "corpus": str(corpus.id),
                    "semantics": index.INDEX_SEMANTICS,
                    "binding": "Exact native index graph retained in digest-bound inputs archive; no parallel production index ID exists.",
                },
                "frame_resource_count": len(addresses),
                "eligible_resources": [
                    {
                        "address": resource.address.value,
                        "content_identity": resource.content_identity.value,
                        "git_blob_sha256": blob_digests[resource.address.value],
                    }
                    for resource in snapshot.resources
                ],
                "bm25": {
                    "k1": request.settings.k1,
                    "b": request.settings.b,
                    "filename_weight": 0.25,
                    "maximum_results": len(addresses),
                    "behavior": "Native content plus filename; distinct casefolded Unicode words; positive scores only; ties retain corpus lexical address order.",
                    "index_semantics": index.INDEX_SEMANTICS,
                },
                "role_derivation": {
                    "semantics": roles.SEMANTICS,
                    "identity": roles.derivation_identity,
                    "retained": "Full native role view and canonical RI inputs in inputs.pkl.gz; no hand-authored assignments.",
                    "implementation_binding": "Every eligible src/devtools Python blob hash below binds transitive production implementation; Stage B must verify committed and current normalized bytes before loading/execution.",
                },
                "grounding_inputs": {
                    "request_count": len(groundings),
                    "module_universe_identity": module_universe.identity,
                    "module_roots": ["src", "tests"],
                    "retained": "Typed unexecuted requests, exact native module universe/analyses and snapshot in inputs.pkl.gz.",
                },
                "generation_inputs": {
                    "recipe_count": len(treatment_data["generation_recipes"]),
                    "mirror_semantics": mirrors.derivation.DEFINITION_SEMANTICS,
                    "mirror_derivation_identity": mirrors.derivation.identity,
                    "retained": "Caller specifications and native mirrored-path analysis in inputs.pkl.gz; no projection executed.",
                },
                "implementation_sha256": {
                    resource.address.value: sha(
                        resource.content.replace("\r\n", "\n").encode()
                    )
                    for resource in snapshot.resources
                    if resource.address.value.startswith("src/devtools/")
                    and resource.address.value.endswith(".py")
                },
                "inputs_sha256": sha(payload),
                "python_version": sys.version,
                "observation_bounds": {
                    "resource_count": 10000,
                    "traversal_entries": 20000,
                    "resource_bytes": 1 << 20,
                },
            }
        )
        put_text(CASE / "pre_retrieval.json", json_bytes(manifest).decode())
    integrity = {
        name: sha(
            binary(CASE / name).replace(b"\r\n", b"\n")
            if name.endswith((".py", ".md", ".json"))
            else binary(CASE / name)
        )
        for name in (
            "treatment.json",
            "pre_retrieval.json",
            "inputs.pkl.gz",
            "freeze.py",
            "treatment.py",
            "README.md",
        )
    }
    put_text(CASE / "integrity.json", json_bytes(integrity).decode())
    validate()


def validate() -> dict:
    """Check identities/digests and native static consistency, never query."""
    integrity = json.loads(binary(CASE / "integrity.json"))
    for name, expected in integrity.items():
        data = binary(CASE / name)
        if name.endswith((".py", ".md", ".json")):
            data = data.replace(b"\r\n", b"\n")
        if sha(data) != expected:
            raise ValueError(f"Frozen artifact changed: {name}")
    protocol = json.loads(binary(CASE / "pre_retrieval.json"))
    if binary(CASE / "pre_retrieval.json").replace(b"\r\n", b"\n") != json_bytes(
        protocol
    ):
        raise ValueError("Manifest serialization is not deterministic.")
    if sha(binary(CASE / "inputs.pkl.gz")) != protocol["inputs_sha256"]:
        raise ValueError("Native input digest differs.")
    treatment_data = json.loads(binary(CASE / "treatment.json"))
    if any(protocol[key] != value for key, value in treatment_data.items()):
        raise ValueError("Manifest treatment differs.")
    native = pickle.loads(gzip.decompress(binary(CASE / "inputs.pkl.gz")))  # noqa: S301
    request, roles, preferences = (
        native["request"],
        native["role_evidence"],
        native["preferences"],
    )
    task, queries, expected_preferences = task_inputs(treatment_data)
    validate_intent(treatment_data, task, queries, expected_preferences)
    if (request.task, request.obligation_queries, preferences) != (
        task,
        queries,
        expected_preferences,
    ):
        raise ValueError("Task/query/preference correspondence differs.")
    if len({query.identity for query in queries}) != len(queries) or {
        query.obligation for query in queries
    } != {obligation.identity for obligation in task.obligations}:
        raise ValueError("Query/obligation coverage differs.")
    for path, expected_digest in protocol["implementation_sha256"].items():
        if sha(binary(ROOT / path).replace(b"\r\n", b"\n")) != expected_digest:
            raise ValueError(f"Production implementation changed: {path}")
    if (
        request.full_task_query != protocol["global_lane"]["query_text"]
        or request.full_task_query != protocol["task_full_prompt"]
        or sha(request.full_task_query.encode()) != protocol["task_sha256"]
    ):
        raise ValueError("Exact global task differs.")
    corpus = (
        request.index.corpus_statistics.collection_analysis.document_collection.corpus
    )
    rebuilt = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=represent_repository_text_corpus(corpus=corpus)
            )
        )
    )
    if rebuilt.corpus_statistics != request.index.corpus_statistics or postings(
        rebuilt
    ) != postings(request.index):
        raise ValueError("Static lexical index reproduction differs.")
    resources = request.snapshot.resources
    observed = tuple(item.address.value for item in resources)
    expected = tuple(item["address"] for item in protocol["eligible_resources"])
    if (
        observed != expected
        or len(set(observed)) != len(observed)
        or len(observed) != protocol["frame_resource_count"]
        or corpus.resources != resources
        or roles.resources != resources
    ):
        raise ValueError("Eligible identity coverage differs.")
    if (
        str(request.snapshot.repository_id) != protocol["repository_id"]
        or str(request.snapshot.id) != protocol["snapshot_id"]
        or str(corpus.id) != protocol["eligible_corpus_id"]
        or roles.repository_id != request.snapshot.repository_id
        or roles.snapshot_id != request.snapshot.id
    ):
        raise ValueError("Repository/snapshot/corpus binding differs.")
    expected_groundings = grounding_requests(treatment_data, task, request.snapshot)
    if (
        native["grounding_requests"] != expected_groundings
        or native["generation_recipe_specs"] != treatment_data["generation_recipes"]
    ):
        raise ValueError("Frozen grounding/recipe specification differs.")
    rebuilt_roles, universe, modules, mirrors = role_view(request.snapshot)
    if (
        native["module_universe"] != universe
        or native["module_analyses"] != modules
        or native["mirrored_paths"] != mirrors
        or protocol["grounding_inputs"]["module_universe_identity"] != universe.identity
        or protocol["generation_inputs"]["mirror_semantics"]
        != mirrors.derivation.DEFINITION_SEMANTICS
        or protocol["generation_inputs"]["mirror_derivation_identity"]
        != mirrors.derivation.identity
        or protocol["grounding_inputs"]["request_count"] != len(expected_groundings)
        or protocol["generation_inputs"]["recipe_count"]
        != len(treatment_data["generation_recipes"])
    ):
        raise ValueError("Native grounding/generation inputs differ.")
    if (
        request.maximum_results != len(resources)
        or request.settings.k1 != protocol["bm25"]["k1"]
        or request.settings.b != protocol["bm25"]["b"]
    ):
        raise ValueError("Lexical settings differ.")
    for resource, frozen in zip(resources, protocol["eligible_resources"], strict=True):
        if (
            resource.content_identity.value != frozen["content_identity"]
            or sha(resource.content.encode()) != frozen["git_blob_sha256"]
        ):
            raise ValueError("Retained resource content differs.")
    if (
        rebuilt_roles != roles
        or roles.derivation_identity != protocol["role_derivation"]["identity"]
    ):
        raise ValueError("Static role reproduction differs.")
    if any(protocol["firewall"].values()):
        raise ValueError("Stage A firewall is not intact.")
    if any(
        (CASE / name).exists()
        for name in (
            "capture.pkl.gz",
            "retrieval.json",
            "routing.json",
            "grounding.json",
            "generation.json",
            "analysis.json",
            "adjudication",
        )
    ):
        raise ValueError("Later-stage output exists.")
    return {
        "resources": len(resources),
        "obligations": len(task.obligations),
        "queries": len(queries),
        "preferences": len(preferences),
        "grounding_requests": len(expected_groundings),
        "generation_recipes": len(treatment_data["generation_recipes"]),
        "retrieval_executed": False,
        "routing_executed": False,
        "grounding_executed": False,
        "generation_executed": False,
    }


if __name__ == "__main__":
    if sys.argv[1:] == ["--author"]:
        put_text(CASE / "treatment.json", json_bytes(treatment()).decode())
    elif sys.argv[1:] == ["--freeze"]:
        asyncio.run(freeze())
    elif sys.argv[1:] == ["--validate"]:
        print(json.dumps(validate(), sort_keys=True))
    else:
        raise SystemExit(
            "Use --author once, --freeze once or --validate; no Stage B execution exists here."
        )
