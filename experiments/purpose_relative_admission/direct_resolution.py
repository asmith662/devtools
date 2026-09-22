# Copyright (c) 2026
# ruff: noqa: E501
"""Exact-name controls outside heterogeneous directional-admission metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.python.function.retrieval import (
    PythonFunctionExactNameQuery,
    retrieve_python_functions_by_exact_name,
    select_python_function_resources_from_exact_name_retrieval,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationKnowledge,
    )


@dataclass(frozen=True, slots=True)
class DirectResolutionControlResult:
    """Exact retrieval observation explicitly excluded from K=5 admission metrics."""

    declared_name: str
    resource_addresses: tuple[str, ...]
    applicable_to_heterogeneous_k5_metrics: bool = False


def run_exact_name_direct_resolution_control(
    *,
    declared_name: str,
    declarations: Sequence[PythonFunctionDeclarationKnowledge],
) -> DirectResolutionControlResult:
    """Use only established exact-name retrieval; never invoke relationship admission."""
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=declarations,
        query=PythonFunctionExactNameQuery(declared_name),
    )
    selected = select_python_function_resources_from_exact_name_retrieval(retrieval)
    return DirectResolutionControlResult(
        declared_name=declared_name,
        resource_addresses=tuple(str(address) for address in selected.resource_addresses),
    )
