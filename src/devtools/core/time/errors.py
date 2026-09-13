# Copyright (c) 2026
"""Exceptions for the :mod:`devtools.core.time` domain."""


class TimeError(Exception):
    """Base exception for time-domain failures."""


class TimestampParsingError(TimeError):
    """Raised when a timestamp representation cannot be parsed."""
