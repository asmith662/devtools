# Copyright (c) 2026
"""Exceptions for the :mod:`devtools.paths` domain."""

from __future__ import annotations


class PathError(Exception):
    """Base exception for all path-domain errors.

    Consumers that wish to handle all path-related failures should catch this
    exception rather than individual subclasses.
    """


class PathResolutionError(PathError):
    """Raised when a path cannot be resolved according to path policy.

    Examples include:

    * A relative path supplied without an explicit base directory.
    * A relative base directory.
    * Invalid input that prevents deterministic path resolution.
    """


class InvalidPathFormatError(PathError):
    """Raised when an external path representation cannot be parsed.

    This exception is raised by parsing operations when the supplied
    representation does not conform to the expected syntax.
    """


class InvalidPythonPathError(InvalidPathFormatError):
    """Raised when a Python module path is syntactically invalid.

    Examples include::

        foo..bar
        foo.
        .foo
        foo-bar
    """