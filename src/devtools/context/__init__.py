# Copyright (c) 2026
"""Repository intelligence and purpose-relative Context domain."""

from devtools.context.python_declarations import (
    PythonFunctionDeclarationAnalysis,
    PythonFunctionDeclarationAnalysisAggregate,
    PythonFunctionDeclarationCoverage,
    PythonFunctionDeclarationDerivation,
    PythonFunctionDeclarationDerivationDefinition,
    PythonFunctionDeclarationKind,
    PythonFunctionDeclarationKnowledge,
    PythonFunctionSubject,
    PythonModuleParseError,
    PythonModuleResourceDependency,
    PythonSourceOccurrence,
    PythonSourceRange,
    analyze_python_function_declaration_resources,
    derive_python_function_declarations,
)
from devtools.context.python_function_candidates import (
    PythonFunctionAnalysisCandidateResource,
    PythonFunctionAnalysisCandidateSelection,
    PythonFunctionCandidateTokenizationError,
    PythonFunctionNameTokenCandidateEvidence,
    select_python_function_analysis_candidates,
)
from devtools.context.python_function_disclosure import (
    PythonFunctionDeclarationDisclosureItem,
    PythonFunctionExactNameContextDisclosure,
    disclose_python_function_exact_name_retrieval,
)
from devtools.context.python_function_materialization import (
    MaterializedPythonFunctionContext,
    MaterializedPythonFunctionDeclaration,
    PythonFunctionSourceMaterializationError,
    materialize_python_function_disclosure_source,
)
from devtools.context.python_function_rendering import (
    RenderedPythonFunctionContext,
    render_materialized_python_function_context,
)
from devtools.context.python_function_request_assembly import (
    assemble_python_function_context_model_request,
)
from devtools.context.python_function_retrieval import (
    PythonFunctionExactNameQuery,
    PythonFunctionExactNameRelevanceEvidence,
    PythonFunctionExactNameResourceSelection,
    PythonFunctionExactNameRetrievalResult,
    PythonFunctionExactNameSelectedResource,
    retrieve_python_functions_by_exact_name,
    select_python_function_resources_from_exact_name_retrieval,
)
from devtools.context.repository import (
    ContentIdentity,
    Repository,
    RepositoryId,
    RepositoryObservationError,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
    RepositorySnapshot,
    RepositorySnapshotId,
    observe_repository_resource,
    observe_repository_resources,
)
from devtools.context.repository_discovery import (
    RepositoryResourceDiscovery,
    RepositoryResourceDiscoveryError,
    discover_repository_resource_addresses,
)

__all__ = [
    "ContentIdentity",
    "MaterializedPythonFunctionContext",
    "MaterializedPythonFunctionDeclaration",
    "PythonFunctionAnalysisCandidateResource",
    "PythonFunctionAnalysisCandidateSelection",
    "PythonFunctionCandidateTokenizationError",
    "PythonFunctionDeclarationAnalysis",
    "PythonFunctionDeclarationAnalysisAggregate",
    "PythonFunctionDeclarationCoverage",
    "PythonFunctionDeclarationDerivation",
    "PythonFunctionDeclarationDerivationDefinition",
    "PythonFunctionDeclarationDisclosureItem",
    "PythonFunctionDeclarationKind",
    "PythonFunctionDeclarationKnowledge",
    "PythonFunctionExactNameContextDisclosure",
    "PythonFunctionExactNameQuery",
    "PythonFunctionExactNameRelevanceEvidence",
    "PythonFunctionExactNameResourceSelection",
    "PythonFunctionExactNameRetrievalResult",
    "PythonFunctionExactNameSelectedResource",
    "PythonFunctionNameTokenCandidateEvidence",
    "PythonFunctionSourceMaterializationError",
    "PythonFunctionSubject",
    "PythonModuleParseError",
    "PythonModuleResourceDependency",
    "PythonSourceOccurrence",
    "PythonSourceRange",
    "RenderedPythonFunctionContext",
    "Repository",
    "RepositoryId",
    "RepositoryObservationError",
    "RepositoryResourceAddress",
    "RepositoryResourceDiscovery",
    "RepositoryResourceDiscoveryError",
    "RepositoryResourceOccurrence",
    "RepositorySnapshot",
    "RepositorySnapshotId",
    "analyze_python_function_declaration_resources",
    "assemble_python_function_context_model_request",
    "derive_python_function_declarations",
    "disclose_python_function_exact_name_retrieval",
    "discover_repository_resource_addresses",
    "materialize_python_function_disclosure_source",
    "observe_repository_resource",
    "observe_repository_resources",
    "render_materialized_python_function_context",
    "retrieve_python_functions_by_exact_name",
    "select_python_function_analysis_candidates",
    "select_python_function_resources_from_exact_name_retrieval",
]
