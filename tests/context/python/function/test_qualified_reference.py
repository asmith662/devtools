# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Tests for explicit qualified-reference Context and exact source realization."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.python.function import (
    MaterializedPythonQualifiedReferenceContext,
    PythonFunctionSourceMaterializationError,
    PythonQualifiedReferenceDisclosureError,
    assemble_python_qualified_reference_model_request,
    disclose_python_qualified_reference,
    materialize_python_qualified_reference_source,
    render_python_qualified_reference_context,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references import (
    PythonFunctionReferenceAnalysis,
    PythonFunctionReferenceKnowledge,
    derive_python_function_references,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import RepositorySnapshot
from devtools.core.paths import ResolvedPath
from devtools.models.interaction import (
    ConversationRef,
    InteractionSource,
    ModelRequest,
    ModelSettings,
    ModelToolDefinition,
    Prompt,
    ProviderRequestSettings,
)


def _snapshot(tmp_path: Path, resources: dict[str, str]) -> RepositorySnapshot:
    for name, content in resources.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode("utf-8"))
    return observe_repository_resources(
        repository=Repository(
            RepositoryId.parse("00000000-0000-4000-8000-000000000031"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(name) for name in resources),
        maximum_resource_bytes=1024 * 1024,
    )


def _analysis(
    snapshot: RepositorySnapshot,
    source: str = "consumer.py",
) -> PythonFunctionReferenceAnalysis:
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot("."),
            resource_addresses=tuple(item.address for item in snapshot.resources),
        ).interpretations,
    )
    return derive_python_function_references(
        snapshot,
        resource_address=RepositoryResourceAddress(source),
        module_universe=universe,
    )


def _materialized(
    snapshot: RepositorySnapshot,
    analysis: PythonFunctionReferenceAnalysis,
    reference: PythonFunctionReferenceKnowledge,
) -> MaterializedPythonQualifiedReferenceContext:
    disclosure = disclose_python_qualified_reference(
        purpose="Understand this established reference.",
        analysis=analysis,
        reference=reference,
    )
    return materialize_python_qualified_reference_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )


def test_cross_resource_call_exact_source_and_request(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\r\nlabel = 'π'; f()\r\n",
            "target.py": "def f():\r\n    return 'π'\r\n",
        },
    )
    analysis = _analysis(snapshot)
    reference = analysis.references[0]
    materialized = _materialized(snapshot, analysis, reference)
    assert materialized.reference_name_text == "f"
    assert materialized.target_declaration_text == "def f():\r\n    return 'π'"
    assert reference.occurrence.source_range.start_column_utf8 == 14
    assert materialized.snapshot_id == snapshot.id
    assert (
        materialized.identity == _materialized(snapshot, analysis, reference).identity
    )
    rendered = render_python_qualified_reference_context(materialized)
    assert "Purpose: Understand this established reference." in rendered.text
    assert "qualified-name-load-references-direct-python-function" in rendered.text
    assert "ast.Call.func; no runtime invocation is asserted" in rendered.text
    assert "Reference analysis is non-exhaustive" in rendered.text
    assert "Source resource pointer: consumer.py" in rendered.text
    assert "Target resource pointer: target.py" in rendered.text
    assert "--- exact Reference Name begins ---\nf\n" in rendered.text
    assert "--- exact target declaration begins ---\ndef f():\r\n" in rendered.text
    assert str(reference.identity) in rendered.text
    assert str(snapshot.id) in rendered.text
    assert str(materialized.source_content_identity) in rendered.text
    assert str(materialized.target_content_identity) in rendered.text
    settings = ModelSettings(maximum_output_tokens=128, thinking_enabled=False)
    conversation = ConversationRef(InteractionSource("test-model"), "thread-1")
    provider = ProviderRequestSettings("test-model")
    tools = (
        ModelToolDefinition(
            name="inspect",
            description="Inspect one value.",
            input_schema_json='{"type":"object"}',
        ),
    )
    task_request = ModelRequest(
        Prompt("Inspect the binding.", "system"),
        settings=settings,
        conversation=conversation,
        provider_settings=provider,
        tools=tools,
    )
    assembled = assemble_python_qualified_reference_model_request(
        task_request=task_request,
        context=rendered,
    )
    assert task_request.prompt.content == "Inspect the binding."
    assert assembled.prompt.role == "system"
    assert assembled.settings is settings
    assert assembled.conversation is conversation
    assert assembled.provider_settings is provider
    assert assembled.tools is tools
    assert assembled.prompt.content.startswith("Task/instruction UTF-8 byte length:")
    assert "Inspect the binding." in assembled.prompt.content
    assert rendered.text in assembled.prompt.content
    assert replace(assembled, prompt=task_request.prompt) == task_request


def test_same_resource_non_call_reference_and_exact_target(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"consumer.py": "from consumer import f as g\ndef f():\n    pass\nvalue = g\n"},
    )
    analysis = _analysis(snapshot)
    assert len(analysis.references) == 1
    reference = analysis.references[0]
    assert not reference.direct_call
    materialized = _materialized(snapshot, analysis, reference)
    assert materialized.reference_name_text == "g"
    assert materialized.target_declaration_text == "def f():\n    pass"
    assert materialized.source_content_identity == materialized.target_content_identity
    rendered = render_python_qualified_reference_context(materialized)
    assert "without the direct-call syntax tag" in rendered.text
    assert "Source resource pointer: consumer.py" in rendered.text
    assert "Target resource pointer: consumer.py" in rendered.text


def test_duplicate_names_preserve_exact_qualified_target(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    return 'chosen'\n",
            "other.py": "def f():\n    return 'not chosen'\n",
        },
    )
    analysis = _analysis(snapshot)
    materialized = _materialized(snapshot, analysis, analysis.references[0])
    assert "'chosen'" in materialized.target_declaration_text
    assert "not chosen" not in materialized.target_declaration_text


def test_one_facade_target_support_is_preserved(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import exported as local\nlocal()\n",
            "package/__init__.py": "from .impl import f as exported\n",
            "package/impl.py": "def f():\n    return 1\n",
        },
    )
    analysis = _analysis(snapshot)
    materialized = _materialized(snapshot, analysis, analysis.references[0])
    assert materialized.reference_name_text == "local"
    assert materialized.target_declaration_text == "def f():\n    return 1"
    rendered = render_python_qualified_reference_context(materialized)
    assert "Resolution path: one-facade" in rendered.text
    assert "Target resource pointer: package/impl.py" in rendered.text


def test_stale_source_or_target_content_is_rejected(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\n",
        },
    )
    analysis = _analysis(snapshot)
    disclosure = disclose_python_qualified_reference(
        purpose="Inspect binding",
        analysis=analysis,
        reference=analysis.references[0],
    )
    newer = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n# change\n",
            "target.py": "def f():\n    return 1\n",
        },
    )
    with pytest.raises(PythonQualifiedReferenceDisclosureError, match="snapshot"):
        materialize_python_qualified_reference_source(
            disclosure=disclosure,
            snapshot=newer,
        )
    for stale_address, message in (
        ("consumer.py", "source content"),
        ("target.py", "Target declaration"),
    ):
        stale = replace(
            snapshot,
            resources=tuple(
                newer.resource_at(item.address)
                if item.address == RepositoryResourceAddress(stale_address)
                else item
                for item in snapshot.resources
            ),
        )
        with pytest.raises(PythonQualifiedReferenceDisclosureError, match=message):
            materialize_python_qualified_reference_source(
                disclosure=disclosure,
                snapshot=stale,
            )


def test_redirected_or_missing_resources_are_rejected(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\n",
            "other.py": "def f():\n    pass\n",
        },
    )
    analysis = _analysis(snapshot)
    fact = analysis.references[0]
    other = RepositoryResourceAddress("other.py")
    redirected_source = replace(
        fact,
        occurrence=replace(fact.occurrence, resource_address=other),
    )
    redirected_target = replace(
        fact,
        target_declaration=replace(
            fact.target_declaration,
            support=replace(fact.target_declaration.support, resource_address=other),
        ),
    )
    for changed, message in (
        (redirected_source, "source dependency"),
        (redirected_target, "Target declaration resource"),
    ):
        altered_analysis = replace(analysis, references=(changed,))
        disclosure = disclose_python_qualified_reference(
            purpose="Inspect binding",
            analysis=altered_analysis,
            reference=changed,
        )
        with pytest.raises(PythonQualifiedReferenceDisclosureError, match=message):
            materialize_python_qualified_reference_source(
                disclosure=disclosure,
                snapshot=snapshot,
            )
    disclosure = disclose_python_qualified_reference(
        purpose="Inspect binding",
        analysis=analysis,
        reference=fact,
    )
    for missing, message in (
        ("consumer.py", "source resource is missing"),
        ("target.py", "target resource is missing"),
    ):
        reduced = replace(
            snapshot,
            resources=tuple(
                item
                for item in snapshot.resources
                if item.address != RepositoryResourceAddress(missing)
            ),
        )
        with pytest.raises(PythonQualifiedReferenceDisclosureError, match=message):
            materialize_python_qualified_reference_source(
                disclosure=disclosure,
                snapshot=reduced,
            )


def test_fact_membership_derivation_and_ranges_are_checked(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\n",
        },
    )
    analysis = _analysis(snapshot)
    fact = analysis.references[0]
    with pytest.raises(PythonQualifiedReferenceDisclosureError, match="purpose"):
        disclose_python_qualified_reference(
            purpose="  ",
            analysis=analysis,
            reference=fact,
        )
    for altered_analysis, altered_fact in (
        (replace(analysis, references=()), fact),
        (analysis, replace(fact, derivation_identity="wrong")),
        (
            replace(
                analysis,
                coverage=replace(analysis.coverage, derivation_identity="wrong"),
            ),
            fact,
        ),
    ):
        with pytest.raises(PythonQualifiedReferenceDisclosureError, match="analysis"):
            disclose_python_qualified_reference(
                purpose="Inspect binding",
                analysis=altered_analysis,
                reference=altered_fact,
            )
    invalid_source = replace(
        fact,
        occurrence=replace(
            fact.occurrence,
            source_range=replace(fact.occurrence.source_range, start_column_utf8=99),
        ),
    )
    invalid_target = replace(
        fact,
        target_declaration=replace(
            fact.target_declaration,
            support=replace(
                fact.target_declaration.support,
                source_range=replace(
                    fact.target_declaration.support.source_range,
                    end_column_utf8=99,
                ),
            ),
        ),
    )
    for changed in (invalid_source, invalid_target):
        changed_analysis = replace(analysis, references=(changed,))
        with pytest.raises(PythonFunctionSourceMaterializationError):
            _materialized(snapshot, changed_analysis, changed)


def test_target_from_another_snapshot_is_rejected(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\n",
        },
    )
    analysis = _analysis(snapshot)
    fact = analysis.references[0]
    newer = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n# changed\n",
            "target.py": "def f():\n    pass\n",
        },
    )
    for changed_target in (
        replace(
            fact.target_declaration,
            support=replace(fact.target_declaration.support, snapshot_id=newer.id),
        ),
        replace(
            fact.target_declaration,
            subject=replace(fact.target_declaration.subject, snapshot_id=newer.id),
        ),
    ):
        changed = replace(fact, target_declaration=changed_target)
        with pytest.raises(PythonQualifiedReferenceDisclosureError, match="snapshot"):
            _materialized(snapshot, replace(analysis, references=(changed,)), changed)


def test_qualified_target_support_must_match_snapshot(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\n",
            "other.py": "def f():\n    pass\n",
        },
    )
    analysis = _analysis(snapshot)
    fact = analysis.references[0]
    facade = fact.member_resolution.facade
    assert facade is not None
    changed_facade = replace(
        facade,
        resource=snapshot.resource_at(RepositoryResourceAddress("other.py")),
    )
    changed = replace(
        fact,
        member_resolution=replace(
            fact.member_resolution,
            facade=changed_facade,
        ),
    )
    with pytest.raises(PythonQualifiedReferenceDisclosureError, match="support"):
        _materialized(snapshot, replace(analysis, references=(changed,)), changed)

    facade_snapshot = _snapshot(
        tmp_path / "facade",
        {
            "consumer.py": "from package import exported as local\nlocal()\n",
            "package/__init__.py": "from .impl import f as exported\n",
            "package/impl.py": "def f():\n    pass\n",
        },
    )
    facade_analysis = _analysis(facade_snapshot)
    facade_fact = facade_analysis.references[0]
    target_analysis = facade_fact.member_resolution.target_function_analysis
    assert target_analysis is not None
    changed = replace(
        facade_fact,
        member_resolution=replace(
            facade_fact.member_resolution,
            target_function_analysis=replace(target_analysis, declarations=()),
        ),
    )
    with pytest.raises(PythonQualifiedReferenceDisclosureError, match="analysis"):
        _materialized(
            facade_snapshot,
            replace(facade_analysis, references=(changed,)),
            changed,
        )


def test_materialization_does_not_reacquire_files(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\n",
        },
    )
    analysis = _analysis(snapshot)
    (tmp_path / "consumer.py").unlink()
    (tmp_path / "target.py").unlink()
    materialized = _materialized(snapshot, analysis, analysis.references[0])
    assert materialized.reference_name_text == "f"
    assert materialized.target_declaration_text == "def f():\n    pass"
