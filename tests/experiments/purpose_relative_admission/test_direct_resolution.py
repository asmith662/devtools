# Copyright (c) 2026
# ruff: noqa: ARG001, D103, E501, I001
# mypy: disable-error-code="attr-defined"
"""Direct controls bypass heterogeneous relationship admission."""

from types import SimpleNamespace

import pytest

from experiments.purpose_relative_admission.direct_resolution import run_exact_name_direct_resolution_control


def test_direct_control_uses_exact_path_and_is_not_k5_applicable(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def retrieve(*, declarations: object, query: object) -> object:
        calls.append(query.declared_name)
        return object()

    def select(_retrieval: object) -> object:
        return SimpleNamespace(resource_addresses=("first.py", "second.py"))

    monkeypatch.setattr("experiments.purpose_relative_admission.direct_resolution.retrieve_python_functions_by_exact_name", retrieve)
    monkeypatch.setattr("experiments.purpose_relative_admission.direct_resolution.select_python_function_resources_from_exact_name_retrieval", select)

    result = run_exact_name_direct_resolution_control(declared_name="target", declarations=())

    assert calls == ["target"]
    assert result.resource_addresses == ("first.py", "second.py")
    assert not result.applicable_to_heterogeneous_k5_metrics
