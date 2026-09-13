# Copyright (c) 2026
"""Exceptions for the :mod:`devtools.core.paths` domain."""


class PathError(Exception):
    """Base exception for path-domain failures."""


class PathParsingError(PathError):
    """Raised when a path representation cannot be parsed."""


class PathResolutionError(PathError):
    """Raised when a path cannot be resolved according to path policy."""
