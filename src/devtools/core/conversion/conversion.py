# Copyright (c) 2026
"""Explicit callable-based value conversion."""

from __future__ import annotations

from collections.abc import Callable, Iterable

from devtools.core.conversion.errors import ConversionError

type Converter[SourceT, TargetT] = Callable[[SourceT], TargetT]


def convert[SourceT, TargetT](
    value: SourceT,
    converter: Converter[SourceT, TargetT],
) -> TargetT:
    """Convert one value through an explicit caller-supplied callable.

    :param value: Source value to convert.
    :param converter: Callable that converts the source value.
    :returns: Converter result, unchanged.
    :raises ConversionError: If the converter raises an ordinary exception.
    """
    try:
        return converter(value)
    except ConversionError:
        raise
    except Exception as error:
        raise ConversionError(type(value)) from error


def convert_all[SourceT, TargetT](
    values: Iterable[SourceT],
    converter: Converter[SourceT, TargetT],
) -> tuple[TargetT, ...]:
    """Convert every value in source order with fail-fast semantics.

    :param values: Source values to convert.
    :param converter: Callable that converts each source value.
    :returns: Immutable converted results in source order.
    :raises ConversionError: If a conversion fails, including its source index.
    """
    results: list[TargetT] = []

    for index, value in enumerate(values):
        try:
            results.append(convert(value, converter))
        except ConversionError as error:
            raise ConversionError(type(value), index=index) from error

    return tuple(results)
