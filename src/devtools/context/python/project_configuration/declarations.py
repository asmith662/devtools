# Copyright (c) 2026
"""Parse bounded Python-project declarations from exact retained TOML content."""

from __future__ import annotations

import tomllib
from dataclasses import replace
from typing import TYPE_CHECKING

from devtools.context.python.project_configuration.models import (
    PythonConfigurationDeclaration,
    PythonConfigurationDeclarationAnalysis,
    PythonConfigurationSelector,
    digest,
)
from devtools.context.python.project_configuration.settings import analyze_settings

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import RepositorySnapshot


def analyze_python_project_configuration(
    snapshot: RepositorySnapshot,
    *,
    address: RepositoryResourceAddress,
) -> PythonConfigurationDeclarationAnalysis:
    """Observe declarations using tomllib, with key/item anchors and bounded coverage.

    Unsupported value forms are assessed, not interpreted. Malformed TOML,
    including duplicate keys, produces no declarations or absence claims.
    """
    resource = snapshot.resource_at(address)
    derivation = digest(
        "python-project-config-tomllib-declarations-v2",
        str(snapshot.repository_id),
        str(snapshot.id),
        address.value,
        resource.content_identity.value,
        resource.content,
    )
    declarations: list[PythonConfigurationDeclaration] = []
    absent: list[PythonConfigurationSelector] = []
    parse_error = None
    settings = None
    try:
        data = tomllib.loads(resource.content)
    except tomllib.TOMLDecodeError:
        parse_error = "malformed-toml"
    else:
        settings = analyze_settings(data, derivation)
        for selector in PythonConfigurationSelector:
            key = tuple(selector.value.split("."))
            value = _at(data, key)
            if value is None:
                absent.append(selector)
                continue
            declarations.extend(
                _selector_declarations(derivation, key, selector, value),
            )
        dynamic = _at(data, ("project", "dynamic"))
        if isinstance(dynamic, list) and "readme" in dynamic:
            declarations = [
                replace(item, unsupported_reason="dynamic-readme")
                if item.selector == PythonConfigurationSelector.README
                else item
                for item in declarations
            ]
            declarations.extend(
                PythonConfigurationDeclaration(
                    derivation,
                    ("project", "dynamic"),
                    ordinal,
                    PythonConfigurationSelector.README,
                    "readme",
                    "dynamic-readme",
                )
                for ordinal, item in enumerate(dynamic)
                if item == "readme"
            )
            absent = [
                item for item in absent if item != PythonConfigurationSelector.README
            ]
    return PythonConfigurationDeclarationAnalysis(
        snapshot.repository_id,
        snapshot.id,
        resource,
        derivation,
        tuple(declarations),
        tuple(absent),
        parse_error,
        settings,
    )


def _at(data: object, key: tuple[str, ...]) -> object:
    for part in key:
        if not isinstance(data, dict):
            return None
        data = data.get(part)
    return data


def _selector_declarations(
    derivation: str,
    key: tuple[str, ...],
    selector: PythonConfigurationSelector,
    value: object,
) -> tuple[PythonConfigurationDeclaration, ...]:
    items: list[tuple[int | None, object]]
    if selector == PythonConfigurationSelector.README:
        items = [(None, value)]
    elif isinstance(value, list):
        items = list(enumerate(value))
    else:
        items = [(None, value)]
    declarations = []
    for ordinal, item in items:
        reason = None
        if not isinstance(item, str):
            reason = "unsupported-value-form"
        elif selector != PythonConfigurationSelector.README and ordinal is None:
            reason = "expected-array"
        declarations.append(
            PythonConfigurationDeclaration(
                derivation,
                key,
                ordinal,
                selector,
                item if isinstance(item, str) else None,
                reason,
            ),
        )
    return tuple(declarations)
