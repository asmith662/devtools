# Copyright (c) 2026
# ruff: noqa: D103
"""Exercise positive multi-label observations and the immutable read surface."""

from dataclasses import fields, replace
from pathlib import Path

import pytest

from devtools.context.localization.roles import (
    RepositoryRoleEvidenceInputs,
    RepositoryRoleKind,
    RepositoryRoleSupport,
    ResourceRoleEvidence,
    RoleSupportKind,
    derive_repository_role_evidence,
)
from devtools.context.python.mirrored_paths import (
    derive_python_mirrored_path_correspondences,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    derive_python_immediate_package_memberships,
    interpret_python_module_resources,
)
from devtools.context.repository.resource import RepositoryResourceAddress
from tests.context.localization.roles.helpers import snapshot

_R = RepositoryRoleKind
_K = RoleSupportKind
_A = RepositoryResourceAddress


def test_intrinsic_conventions_are_multi_label_and_not_exclusion(
    tmp_path: Path,
) -> None:
    observed = snapshot(
        tmp_path,
        {
            "tests/pkg/__init__.py": "",
            "docs/notes.MD": "",
            "README.rst": "",
            "nested/readme.txt": "",
            "pyproject.toml": "",
            "src/code.py": "",
            "docs/plain.txt": "",
            "opaque.bin": "",
            "testsish/test_thing.py": "",
            "test_thing.py": "",
            "code.PY": "",
            "scripts/validate_development.py": "",
        },
    )
    view = derive_repository_role_evidence(observed)
    assert {item.role for item in view.for_resource(_A("tests/pkg/__init__.py"))} == {
        _R.PYTHON_CODE,
        _R.TEST,
        _R.PACKAGE_SURFACE,
    }
    assert {
        item.kind for item in view.supports_for(_A("docs/notes.MD"), _R.DOCUMENTATION)
    } == {
        _K.MARKDOWN_SUFFIX_CONVENTION,
        _K.DOCUMENTATION_DIRECTORY_CONVENTION,
    }
    assert (
        view.supports_for(_A("README.rst"), _R.DOCUMENTATION)[0].kind
        == _K.README_NAME_CONVENTION
    )
    assert view.supports_for(_A("nested/readme.txt"), _R.DOCUMENTATION)
    assert view.supports_for(_A("pyproject.toml"), _R.PROJECT_CONFIGURATION)
    assert not view.for_resource(_A("opaque.bin"))
    assert not view.for_resource(_A("code.PY"))
    assert not view.supports_for(_A("test_thing.py"), _R.TEST)
    assert not view.supports_for(_A("testsish/test_thing.py"), _R.TEST)
    assert len(view.resources) == len(observed.resources)
    assert all(item.role is _R.TEST for item in view.for_role(_R.TEST))
    assert not view.for_role(_R.BUILD_CONFIGURATION)
    with pytest.raises(ValueError, match="outside the retained frame"):
        view.for_resource(_A("missing.py"))
    with pytest.raises(ValueError, match="outside the retained frame"):
        view.supports_for(_A("missing.py"), _R.TEST)
    assert not {"score", "probability", "confidence", "resolved", "excluded"} & {
        item.name
        for model in (ResourceRoleEvidence, RepositoryRoleSupport)
        for item in fields(model)
    }
    assert "VALIDATION" not in _R.__members__
    assert "IMPLEMENTATION" not in _R.__members__
    assert view == derive_repository_role_evidence(
        replace(observed, resources=tuple(reversed(observed.resources))),
    )
    assert len({item.identity for item in view.evidence}) == len(view.evidence)
    assert all(
        item.repository_id == observed.repository_id and item.snapshot_id == observed.id
        for item in view.evidence
    )


def test_native_structural_supports_and_duplicate_input_normalization(
    tmp_path: Path,
) -> None:
    observed = snapshot(
        tmp_path,
        {
            "src/devtools/__init__.py": "__all__ = compute_dynamic_exports()",
            "src/devtools/a.py": "",
            "tests/test_a.py": "",
            "notes.txt": "",
        },
    )
    addresses = tuple(item.address for item in observed.resources)
    modules = interpret_python_module_resources(
        observed,
        module_root=PythonModuleRoot("src"),
        resource_addresses=addresses,
    )
    memberships = derive_python_immediate_package_memberships(
        observed,
        interpretation_analysis=modules,
    )
    mirrors = derive_python_mirrored_path_correspondences(observed)
    inputs = RepositoryRoleEvidenceInputs(
        modules=(modules,),
        memberships=(memberships,),
        mirrors=(mirrors,),
    )
    view = derive_repository_role_evidence(observed, inputs=inputs)
    assert {
        item.kind
        for item in view.supports_for(
            _A("src/devtools/__init__.py"),
            _R.PACKAGE_SURFACE,
        )
    } == {
        _K.INITIALIZER_NAME_CONVENTION,
        _K.PACKAGE_INTERPRETATION,
        _K.PACKAGE_MEMBERSHIP,
    }
    assert {
        item.kind for item in view.supports_for(_A("tests/test_a.py"), _R.TEST)
    } == {
        _K.TEST_DIRECTORY_CONVENTION,
        _K.MIRRORED_TEST_PATH,
    }
    assert {
        item.kind for item in view.supports_for(_A("src/devtools/a.py"), _R.PYTHON_CODE)
    } == {
        _K.PYTHON_SUFFIX_CONVENTION,
        _K.MODULE_INTERPRETATION,
    }
    assert view.supports_for(_A("src/devtools/a.py"), _R.PACKAGE_MEMBER)[
        0
    ].native_identities == (memberships.memberships[0].identity,)
    assert not view.supports_for(_A("src/devtools/a.py"), _R.TEST)
    assert not view.for_resource(_A("notes.txt"))
    duplicated = replace(
        inputs,
        modules=(modules, modules),
        memberships=(memberships, memberships),
        mirrors=(mirrors, mirrors),
    )
    assert view == derive_repository_role_evidence(observed, inputs=duplicated)
    reordered = replace(
        modules,
        interpretations=tuple(reversed(modules.interpretations)),
        exclusions=tuple(reversed(modules.exclusions)),
    )
    assert view == derive_repository_role_evidence(
        observed,
        inputs=replace(inputs, modules=(reordered,)),
    )
    assert (
        view.derivation_identity
        != derive_repository_role_evidence(observed).derivation_identity
    )
    assert all(
        len({support.identity for support in item.supports}) == len(item.supports)
        for item in view.evidence
    )


def test_empty_and_duplicate_resource_frames(tmp_path: Path) -> None:
    observed = snapshot(tmp_path, {})
    empty = derive_repository_role_evidence(observed)
    assert not empty.resources
    assert not empty.evidence
    assert not empty.limitations
    single = snapshot(tmp_path, {"a.py": ""})
    with pytest.raises(ValueError, match="repeats a resource address"):
        derive_repository_role_evidence(replace(single, resources=single.resources * 2))
