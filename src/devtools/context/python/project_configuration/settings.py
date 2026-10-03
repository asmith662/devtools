# Copyright (c) 2026
"""Recognize bounded project metadata and pytest declarations, not execution."""

from __future__ import annotations

from dataclasses import replace
from typing import cast

from devtools.context.python.project_configuration.models import (
    PythonConfigurationSetting,
    PythonConfigurationSettings,
)

# testpaths and readme retain their existing selector declaration owner.
_STRING_KEYS = (
    ("build-system", "build-backend"),
    ("project", "name"),
    ("project", "version"),
    ("project", "description"),
    ("project", "requires-python"),
)
_ARRAY_KEYS = (
    ("build-system", "requires"),
    ("build-system", "backend-path"),
    ("project", "dependencies"),
    ("project", "dynamic"),
)
_PYTEST_KEYS = tuple(
    ("tool", "pytest", "ini_options", name)
    for name in (
        "python_files",
        "python_classes",
        "python_functions",
        "norecursedirs",
        "addopts",
    )
)
_ENTRY_TABLES = (
    ("project", "scripts"),
    ("project", "gui-scripts"),
    ("project", "entry-points"),
)
_TOOL_TABLES = (
    ("tool", "coverage", "run"),
    ("tool", "coverage", "report"),
    ("tool", "hatch", "build", "targets", "wheel"),
    ("tool", "mypy"),
    ("tool", "pytest", "ini_options"),
    ("tool", "ruff"),
    ("tool", "ruff", "lint"),
)
_MISSING = object()
_NON_TABLE = object()


def analyze_settings(data: object, derivation: str) -> PythonConfigurationSettings:
    """Account for named keys without parsing specifiers, patterns or targets.

    Strings remain strings; string arrays remain ordered tuples including
    duplicates. Unsupported values remain anchored in the retained resource.
    Absence is asserted only when traversal encounters a missing key, never
    when a parent has an unsupported non-table shape.
    """
    declarations: list[PythonConfigurationSetting] = []
    absent: list[tuple[str, ...]] = []
    dynamic = _lookup(data, ("project", "dynamic"))
    for key in sorted((*_STRING_KEYS, *_ARRAY_KEYS, *_PYTEST_KEYS)):
        value = _lookup(data, key)
        if value is _MISSING:
            absent.append(key)
            continue
        setting = _setting(derivation, key, value, allow_array=key not in _STRING_KEYS)
        if key in _ARRAY_KEYS and isinstance(value, str):
            setting = PythonConfigurationSetting(
                derivation,
                key,
                value,
                "expected-string-array",
            )
        declarations.append(setting)
    for key in _ENTRY_TABLES:
        value = _lookup(data, key)
        if value is _MISSING:
            absent.append(key)
        else:
            declarations.extend(_entry_declarations(derivation, key, value))
    for ordinal, declaration in enumerate(declarations):
        if (
            declaration.key[0] == "project"
            and declaration.key[1] != "dynamic"
            and isinstance(dynamic, list)
            and declaration.key[1] in dynamic
        ):
            declarations[ordinal] = replace(
                declaration,
                unsupported_reason="dynamic-project-field",
            )
    return PythonConfigurationSettings(
        tuple(sorted(declarations, key=lambda item: item.key)),
        tuple(sorted(absent)),
        tuple(key for key in _TOOL_TABLES if isinstance(_lookup(data, key), dict)),
    )


def _lookup(data: object, key: tuple[str, ...]) -> object:
    for part in key:
        if not isinstance(data, dict):
            return _NON_TABLE
        table = cast("dict[str, object]", data)
        if part not in table:
            return _MISSING
        data = table[part]
    return data


def _setting(
    derivation: str,
    key: tuple[str, ...],
    value: object,
    *,
    allow_array: bool,
) -> PythonConfigurationSetting:
    retained: str | tuple[str, ...] | None = None
    reason = None
    if isinstance(value, str):
        retained = value
    elif (
        allow_array
        and isinstance(value, list)
        and all(isinstance(item, str) for item in value)
    ):
        retained = tuple(cast("list[str]", value))
    else:
        reason = "non-table-parent" if value is _NON_TABLE else "unsupported-value-form"
    return PythonConfigurationSetting(derivation, key, retained, reason)


def _entry_declarations(
    derivation: str,
    key: tuple[str, ...],
    value: object,
) -> tuple[PythonConfigurationSetting, ...]:
    if not isinstance(value, dict):
        return (PythonConfigurationSetting(derivation, key, None, "expected-table"),)
    table = cast("dict[str, object]", value)
    # An empty declared table is positive presence, not absence or a binding.
    if not table:
        return (PythonConfigurationSetting(derivation, key, (), None),)
    declarations = []
    for name, item in sorted(table.items()):
        anchor = (*key, name)
        if key == ("project", "entry-points"):
            if name in {"console_scripts", "gui_scripts"}:
                declarations.append(
                    PythonConfigurationSetting(
                        derivation,
                        anchor,
                        None,
                        "reserved-entrypoint-group",
                    ),
                )
            else:
                declarations.extend(_entry_declarations(derivation, anchor, item))
        else:
            declarations.append(_setting(derivation, anchor, item, allow_array=False))
    return tuple(declarations)
