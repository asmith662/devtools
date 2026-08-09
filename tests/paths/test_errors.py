# Copyright (c) 2026
"""Tests for public path-domain error types."""

from devtools.paths import PathError, PathParsingError, PathResolutionError


def test_path_errors_share_the_domain_base_type() -> None:
    """Specific path errors remain catchable as path-domain failures."""
    assert issubclass(PathParsingError, PathError)
    assert issubclass(PathResolutionError, PathError)
    assert issubclass(PathError, Exception)
