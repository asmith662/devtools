# Copyright (c) 2026
"""Select exact native source declarations independently of name bindings."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from devtools.context.python.classes.declarations import (
    PythonClassMethodAnalysis,
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationAnalysis,
    derive_python_function_declarations,
)

if TYPE_CHECKING:
    from devtools.context.python.modules.declarations import (
        PythonDirectModuleDeclaration,
    )
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot


class PythonSourceDeclarationKind(Enum):
    """Name only syntax families represented by direct declaration RI."""

    CLASS = "class"
    FUNCTION = "function"


@dataclass(frozen=True, slots=True)
class PythonModuleSourceDeclarationSelection:
    """Retain all exact source matches and their native analysis provenance.

    Declaration subjects are static source identities. This result establishes
    neither post-decoration binding values nor runtime/import object identity.
    """

    module: PythonModuleInterpretation
    declared_name: str
    kind: PythonSourceDeclarationKind
    function_analysis: PythonFunctionDeclarationAnalysis
    class_analysis: PythonClassMethodAnalysis
    declarations: tuple[PythonDirectModuleDeclaration, ...]

    SEMANTICS: ClassVar[str] = "exact-python-module-source-declaration-selection-v1"


def select_python_module_source_declarations(
    snapshot: RepositorySnapshot,
    *,
    module: PythonModuleInterpretation,
    declared_name: str,
    kind: PythonSourceDeclarationKind,
) -> PythonModuleSourceDeclarationSelection:
    """Select direct declarations by exact kind/name in one observed module.

    Consume canonical RI without a parallel parser or binding policy. Repeated
    declarations remain distinct; decorators and other bindings do not erase
    source facts. Native parse failures propagate without successful coverage.
    """
    if not declared_name.isidentifier():
        msg = "Source declaration name must be a Python identifier."
        raise ValueError(msg)
    if not isinstance(kind, PythonSourceDeclarationKind):
        msg = "Source declaration selection has an unsupported kind."
        raise TypeError(msg)
    if (
        module.repository_id != snapshot.repository_id
        or module.snapshot_id != snapshot.id
        or module.resource != snapshot.resource_at(module.resource.address)
    ):
        msg = "Source declaration module differs from the supplied snapshot."
        raise ValueError(msg)
    address = module.resource.address
    functions = derive_python_function_declarations(snapshot, resource_address=address)
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=address,
    )
    declarations: tuple[PythonDirectModuleDeclaration, ...] = (
        classes.classes
        if kind is PythonSourceDeclarationKind.CLASS
        else functions.declarations
    )
    return PythonModuleSourceDeclarationSelection(
        module,
        declared_name,
        kind,
        functions,
        classes,
        tuple(item for item in declarations if item.declared_name == declared_name),
    )
