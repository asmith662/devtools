# Copyright (c) 2026
"""Explicit callable-based typed conversion."""

from devtools.core.conversion.conversion import Converter, convert, convert_all
from devtools.core.conversion.errors import ConversionError

__all__ = [
    "ConversionError",
    "Converter",
    "convert",
    "convert_all",
]
