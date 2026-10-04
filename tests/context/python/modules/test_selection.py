# Copyright (c) 2026
# ruff: noqa: D103
"""Exact native source selection must remain independent of bindings."""

import hashlib
from dataclasses import replace

import pytest

from devtools.context.python.modules import (
    PythonModuleInterpretation,
    PythonModuleRoot,
    interpret_python_module_resources,
)
from devtools.context.python.modules.declarations import (
    PythonModuleDeclarationLookupOutcome as BindingOutcome,
)
from devtools.context.python.modules.declarations import (
    lookup_python_module_declaration,
)
from devtools.context.python.modules.selection import (
    PythonSourceDeclarationKind as Kind,
)
from devtools.context.python.modules.selection import (
    select_python_module_source_declarations,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)


def _frame(content: str) -> tuple[RepositorySnapshot, PythonModuleInterpretation]:
    resource = RepositoryResourceOccurrence(
        RepositoryResourceAddress("src/native.py"),
        ContentIdentity(hashlib.sha256(content.encode()).hexdigest()),
        content,
        "utf-8",
        len(content.encode()),
    )
    snapshot = RepositorySnapshot(
        RepositorySnapshotId("a" * 64),
        RepositoryId.parse("00000000-0000-0000-0000-000000000001"),
        (resource,),
    )
    module = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=(resource.address,),
    ).interpretations[0]
    return snapshot, module


@pytest.mark.parametrize(
    ("syntax", "kind"),
    [
        ("class Target: pass", Kind.CLASS),
        ("def Target(): pass", Kind.FUNCTION),
        ("async def Target(): pass", Kind.FUNCTION),
    ],
)
@pytest.mark.parametrize("prefix", ["", "@decorator\n"])
def test_plain_and_decorated_native_identity(
    syntax: str,
    kind: Kind,
    prefix: str,
) -> None:
    snapshot, module = _frame(prefix + syntax + "\n")
    selected = select_python_module_source_declarations(
        snapshot,
        module=module,
        declared_name="Target",
        kind=kind,
    )
    assert len(selected.declarations) == 1
    target = selected.declarations[0]
    assert target in (
        selected.class_analysis.classes
        if kind is Kind.CLASS
        else selected.function_analysis.declarations
    )
    assert target.subject.snapshot_id == snapshot.id
    assert target.support.resource_address == module.resource.address
    assert selected.module is module
    assert selected.kind is kind
    assert selected.declared_name == "Target"
    assert selected == select_python_module_source_declarations(
        snapshot,
        module=module,
        declared_name="Target",
        kind=kind,
    )
    binding = lookup_python_module_declaration(
        snapshot,
        module=module,
        declared_name="Target",
    )
    assert binding.outcome is (
        BindingOutcome.NOT_DECLARATION if prefix else BindingOutcome.RESOLVED
    )


@pytest.mark.parametrize(
    ("content", "kind", "count"),
    [
        ("class Target: pass\nclass Target: pass\n", Kind.CLASS, 2),
        ("def Target(): pass\ndef Target(): pass\n", Kind.FUNCTION, 2),
        ("class Target: pass\ndef Target(): pass\n", Kind.CLASS, 1),
        ("class Target: pass\ndef Target(): pass\n", Kind.FUNCTION, 1),
        ("class Target: pass\n", Kind.FUNCTION, 0),
        ("def Target(): pass\n", Kind.CLASS, 0),
        ("class target: pass\n", Kind.CLASS, 0),
        ("if enabled:\n    class Target: pass\n", Kind.CLASS, 0),
        ("Target = lambda: None\n", Kind.FUNCTION, 0),
        ("@decorator\nclass Target: pass\nTarget = other\nexec(code)\n", Kind.CLASS, 1),
    ],
)
def test_exact_kind_scope_and_repeated_declarations(
    content: str,
    kind: Kind,
    count: int,
) -> None:
    snapshot, module = _frame(content)
    selected = select_python_module_source_declarations(
        snapshot,
        module=module,
        declared_name="Target",
        kind=kind,
    )
    assert len(selected.declarations) == count
    assert len({item.subject.identity for item in selected.declarations}) == count


def test_selection_rejects_invalid_and_foreign_inputs() -> None:
    snapshot, module = _frame("class Target: pass\n")
    with pytest.raises(ValueError, match="identifier"):
        select_python_module_source_declarations(
            snapshot,
            module=module,
            declared_name="a.b",
            kind=Kind.CLASS,
        )
    with pytest.raises(TypeError, match="unsupported kind"):
        select_python_module_source_declarations(
            snapshot,
            module=module,
            declared_name="Target",
            kind="class",  # type: ignore[arg-type]
        )
    for foreign in (
        replace(
            module,
            repository_id=RepositoryId.parse("00000000-0000-0000-0000-000000000002"),
        ),
        replace(module, snapshot_id=RepositorySnapshotId("b" * 64)),
        replace(
            module,
            resource=replace(module.resource, content="class Different: pass\n"),
        ),
    ):
        with pytest.raises(ValueError, match="differs from the supplied snapshot"):
            select_python_module_source_declarations(
                snapshot,
                module=foreign,
                declared_name="Target",
                kind=Kind.CLASS,
            )
