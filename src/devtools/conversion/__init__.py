# Copyright (c) 2026
"""Explicit callable-based typed conversion."""

from devtools.conversion.conversion import Converter, convert, convert_all
from devtools.conversion.errors import ConversionError

__all__ = [
    "ConversionError",
    "Converter",
    "convert",
    "convert_all",
]
