# Copyright (c) 2026
"""Conversion-domain errors."""

from __future__ import annotations


class ConversionError(Exception):
    """Represent a failure from an explicit conversion callable.

    :ivar index: Zero-based source index for a batch failure, if applicable.
    :ivar source_type: Type of the source value passed to the converter.
    """

    def __init__(
        self,
        source_type: type[object],
        *,
        index: int | None = None,
    ) -> None:
        """Initialize conversion failure context.

        :param source_type: Type of the source value passed to the converter.
        :param index: Zero-based source index for a batch failure.
        """
        self.index = index
        self.source_type = source_type

        location = "" if index is None else f" at index {index}"
        super().__init__(
            f"Conversion failed{location} for source type {source_type.__name__}.",
        )
