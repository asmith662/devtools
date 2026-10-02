# Copyright (c) 2026
"""Bounded exact dotted-name lookup without root precedence."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )


def lookup_python_modules(
    universe: PythonModuleInterpretationUniverse,
    dotted_name: str,
) -> tuple[PythonModuleInterpretation, ...]:
    """Retain every exact name match in supplied universe order."""
    return tuple(
        item for item in universe.interpretations if item.dotted_name == dotted_name
    )
