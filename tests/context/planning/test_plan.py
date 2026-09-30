# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Tests for explicit Context plans and snapshot-faithful mixed disclosure."""

from dataclasses import dataclass, replace
from pathlib import Path

import pytest

from devtools.context.planning import (
    ContextDisclosure,
    DisclosureMaterializationError,
    DisclosurePlan,
    MaterializedDisclosureItem,
    assemble_context_disclosure_model_request,
    choose_whole_resource_disclosure,
    materialize_disclosure_plan,
    plan_disclosures,
    render_context_disclosure,
)
from devtools.context.python.function import (
    PythonQualifiedReferenceDisclosureOption,
    choose_python_qualified_reference_disclosure,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references import derive_python_function_references
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.core.paths import ResolvedPath
from devtools.models.interaction import (
    ConversationRef,
    InteractionSource,
    ModelRequest,
    ModelSettings,
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
            RepositoryId.parse("00000000-0000-4000-8000-000000000041"),
        ),
        root=ResolvedPath(tmp_path),
        addresses=tuple(RepositoryResourceAddress(name) for name in resources),
        maximum_resource_bytes=1024 * 1024,
    )


def _reference_option(
    snapshot: RepositorySnapshot,
    *,
    purpose: str = "Inspect this binding.",
) -> PythonQualifiedReferenceDisclosureOption:
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot("."),
            resource_addresses=tuple(item.address for item in snapshot.resources),
        ).interpretations,
    )
    analysis = derive_python_function_references(
        snapshot,
        resource_address=RepositoryResourceAddress("consumer.py"),
        module_universe=universe,
    )
    return choose_python_qualified_reference_disclosure(
        purpose=purpose,
        analysis=analysis,
        reference=analysis.references[0],
    )


def test_mixed_plan_preserves_purpose_sources_and_request(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\r\nf()\r\n",
            "target.py": "def f():\r\n    return 'π'\r\n",
        },
    )
    purpose = "Inspect this binding."
    reference = _reference_option(snapshot)
    whole = choose_whole_resource_disclosure(
        purpose=purpose,
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    plan = plan_disclosures(
        purpose=purpose,
        snapshot=snapshot,
        disclosures=(reference, whole),
    )
    assert (
        plan.identity
        == plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(reference, whole),
        ).identity
    )
    assert (
        plan.identity
        != plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(whole, reference),
        ).identity
    )
    assert (
        plan.identity
        != plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(reference, whole),
            preceding_plan_identity="prior",
        ).identity
    )
    (tmp_path / "consumer.py").unlink()
    (tmp_path / "target.py").unlink()
    materialized = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
    assert len(materialized.items) == 2
    assert materialized.items[0].option_identity == reference.identity
    assert materialized.items[0].representation == reference.representation
    assert materialized.items[0].resource_addresses == (
        RepositoryResourceAddress("consumer.py"),
        RepositoryResourceAddress("target.py"),
    )
    assert "ast.Call.func; no runtime invocation is asserted" in (
        materialized.items[0].text
    )
    assert "def f():\r\n    return 'π'" in materialized.items[0].text
    assert materialized.items[1].native_provenance is whole.resource
    assert whole.resource.content in materialized.items[1].text
    assert (
        materialized.identity
        == materialize_disclosure_plan(
            plan=plan,
            snapshot=snapshot,
        ).identity
    )
    rendered = render_context_disclosure(materialized)
    assert rendered.disclosure is materialized
    assert rendered.text.index("Disclosure item 1") < rendered.text.index(
        "Disclosure item 2",
    )
    assert purpose in rendered.text
    assert plan.identity in rendered.text
    settings = ModelSettings(maximum_output_tokens=128, thinking_enabled=False)
    continuation = ConversationRef(InteractionSource("test-model"), "thread-1")
    provider = ProviderRequestSettings("test-model")
    task = ModelRequest(
        Prompt("Inspect source.", "system"),
        settings=settings,
        conversation=continuation,
        provider_settings=provider,
    )
    assembled = assemble_context_disclosure_model_request(
        task_request=task,
        context=rendered,
    )
    assert task.prompt.content == "Inspect source."
    assert assembled.prompt.role == "system"
    assert assembled.settings is settings
    assert assembled.conversation is continuation
    assert assembled.provider_settings is provider
    assert assembled.prompt.content.index("Inspect source.") < (
        assembled.prompt.content.index(rendered.text)
    )
    assert replace(assembled, prompt=task.prompt) == task


def test_same_resource_reference_uses_same_plan_boundary(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"consumer.py": "from consumer import f as g\ndef f():\n    pass\nvalue = g\n"},
    )
    option = _reference_option(snapshot)
    plan = plan_disclosures(
        purpose=option.purpose,
        snapshot=snapshot,
        disclosures=(option,),
    )
    realized = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
    assert realized.items[0].resource_addresses == (
        RepositoryResourceAddress("consumer.py"),
        RepositoryResourceAddress("consumer.py"),
    )
    assert "without the direct-call syntax tag" in realized.items[0].text
    assert "def f():\n    pass" in realized.items[0].text


def test_plan_rejects_mixed_or_duplicate_choices(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"target.py": "def f():\n    pass\n"})
    option = choose_whole_resource_disclosure(
        purpose="Inspect target.",
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    with pytest.raises(ValueError, match="purpose"):
        plan_disclosures(purpose=" ", snapshot=snapshot, disclosures=(option,))
    with pytest.raises(ValueError, match="at least one"):
        plan_disclosures(purpose="Inspect target.", snapshot=snapshot, disclosures=())
    with pytest.raises(ValueError, match="incompatible"):
        plan_disclosures(
            purpose="Different purpose.",
            snapshot=snapshot,
            disclosures=(option,),
        )
    with pytest.raises(ValueError, match="incompatible"):
        plan_disclosures(
            purpose=option.purpose,
            snapshot=snapshot,
            disclosures=(
                replace(option, snapshot_id=replace(snapshot.id, value="0" * 64)),
            ),
        )
    with pytest.raises(ValueError, match="repeats"):
        plan_disclosures(
            purpose=option.purpose,
            snapshot=snapshot,
            disclosures=(option, option),
        )


def test_whole_resource_rejects_stale_or_missing_state(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"target.py": "first\r\nline\r\n"})
    option = choose_whole_resource_disclosure(
        purpose="Inspect target.",
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    plan = plan_disclosures(
        purpose=option.purpose,
        snapshot=snapshot,
        disclosures=(option,),
    )
    newer = _snapshot(tmp_path, {"target.py": "changed\r\nline\r\n"})
    with pytest.raises(DisclosureMaterializationError, match="snapshot"):
        materialize_disclosure_plan(plan=plan, snapshot=newer)
    with pytest.raises(DisclosureMaterializationError, match="another snapshot"):
        option.materialize(newer)
    stale = replace(snapshot, resources=newer.resources)
    with pytest.raises(DisclosureMaterializationError, match="differs"):
        materialize_disclosure_plan(plan=plan, snapshot=stale)
    missing = replace(snapshot, resources=())
    with pytest.raises(DisclosureMaterializationError, match="missing"):
        materialize_disclosure_plan(plan=plan, snapshot=missing)
    with pytest.raises(ValueError, match="purpose"):
        choose_whole_resource_disclosure(
            purpose=" ",
            snapshot=snapshot,
            resource_address=RepositoryResourceAddress("target.py"),
        )
    with pytest.raises(ValueError, match="does not contain"):
        choose_whole_resource_disclosure(
            purpose=option.purpose,
            snapshot=snapshot,
            resource_address=RepositoryResourceAddress("absent.py"),
        )


@pytest.mark.parametrize("wrong_value", ["identity", "representation"])
def test_materialization_rejects_an_option_that_changes_its_plan(
    tmp_path: Path,
    wrong_value: str,
) -> None:
    snapshot = _snapshot(tmp_path, {"target.py": "source\n"})
    option = choose_whole_resource_disclosure(
        purpose="Inspect target.",
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )

    @dataclass(frozen=True)
    class IncompatibleOption:
        purpose: str = option.purpose
        snapshot_id: RepositorySnapshotId = option.snapshot_id
        repository_id: RepositoryId = option.repository_id
        representation: str = option.representation

        @property
        def identity(self) -> str:
            return option.identity

        def materialize(
            self,
            current: RepositorySnapshot,
        ) -> MaterializedDisclosureItem:
            item = option.materialize(current)
            if wrong_value == "identity":
                return replace(item, option_identity="changed")
            return replace(item, representation="changed")

    forged = IncompatibleOption()
    plan = DisclosurePlan(
        purpose=option.purpose,
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        disclosures=(forged,),
    )
    with pytest.raises(DisclosureMaterializationError, match="differs"):
        materialize_disclosure_plan(plan=plan, snapshot=snapshot)


def test_realized_context_rejects_items_outside_the_plan(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"target.py": "source\n"})
    option = choose_whole_resource_disclosure(
        purpose="Inspect target.",
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    plan = plan_disclosures(
        purpose=option.purpose,
        snapshot=snapshot,
        disclosures=(option,),
    )
    item = option.materialize(snapshot)
    with pytest.raises(DisclosureMaterializationError, match="do not match"):
        ContextDisclosure(plan, ())
    with pytest.raises(DisclosureMaterializationError, match="do not match"):
        ContextDisclosure(plan, (replace(item, option_identity="other"),))
