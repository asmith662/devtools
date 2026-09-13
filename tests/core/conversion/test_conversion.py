# Copyright (c) 2026
"""Tests for the generic conversion primitive."""

from __future__ import annotations

import pytest

from devtools.core.conversion import ConversionError, Converter, convert, convert_all


class _UnwrappedFailure(BaseException):
    """Represent a control-flow failure that conversion must not wrap."""


def test_convert_returns_the_converter_result_and_invokes_it_once() -> None:
    """Single conversion delegates exactly once and preserves the result object."""
    source = {"id": "report-17"}
    result = object()
    calls: list[dict[str, str]] = []

    def convert_value(value: dict[str, str]) -> object:
        calls.append(value)
        return result

    converted = convert(source, convert_value)

    assert converted is result
    assert calls == [source]


def test_converter_is_available_from_the_package_root() -> None:
    """The public converter alias describes an explicit callable."""
    converter: Converter[str, str] = str.upper

    assert convert("report", converter) == "REPORT"


def test_convert_wraps_ordinary_failures_with_stable_context() -> None:
    """Ordinary converter errors retain their cause and source type."""
    source = {"id": "report-17"}

    def fail(_value: dict[str, str]) -> None:
        message = "invalid report"
        raise ValueError(message)

    with pytest.raises(ConversionError) as raised:
        convert(source, fail)

    error = raised.value
    assert error.index is None
    assert error.source_type is dict
    assert str(error) == "Conversion failed for source type dict."
    assert "report-17" not in str(error)
    assert isinstance(error.__cause__, ValueError)


def test_convert_preserves_existing_conversion_errors() -> None:
    """An explicit conversion error is not wrapped a second time."""
    expected = ConversionError(str)

    def fail(_value: str) -> str:
        raise expected

    with pytest.raises(ConversionError) as raised:
        convert("source", fail)

    assert raised.value is expected


def test_convert_does_not_wrap_base_exceptions() -> None:
    """Control-flow exceptions propagate without normalization."""

    def fail(_value: str) -> str:
        raise _UnwrappedFailure

    with pytest.raises(_UnwrappedFailure):
        convert("source", fail)


def test_convert_all_returns_an_immutable_ordered_tuple_for_any_iterable() -> None:
    """Batch conversion supports generators while preserving source order."""
    values = (value for value in ("1", "2", "3"))

    assert convert_all(values, int) == (1, 2, 3)
    assert convert_all((), int) == ()


def test_convert_all_fails_fast_and_adds_the_failing_index() -> None:
    """Batch failure has item context and retains the full conversion chain."""
    calls: list[str] = []

    def convert_value(value: str) -> str:
        calls.append(value)
        if value == "bad":
            message = "invalid"
            raise ValueError(message)

        return value.upper()

    with pytest.raises(ConversionError) as raised:
        convert_all(("first", "bad", "never"), convert_value)

    error = raised.value
    assert calls == ["first", "bad"]
    assert error.index == 1
    assert error.source_type is str
    assert str(error) == "Conversion failed at index 1 for source type str."
    assert isinstance(error.__cause__, ConversionError)
    assert isinstance(error.__cause__.__cause__, ValueError)


def test_convert_all_indexes_existing_conversion_errors() -> None:
    """Batch conversion adds position even when a converter raises ConversionError."""
    original = ConversionError(int)

    def fail(_value: int) -> int:
        raise original

    with pytest.raises(ConversionError) as raised:
        convert_all((1,), fail)

    error = raised.value
    assert error.index == 0
    assert error.source_type is int
    assert error.__cause__ is original
