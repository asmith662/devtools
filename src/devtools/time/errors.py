# Copyright (c) 2026
"""Exceptions for the :mod:`devtools.time` domain."""


class TimeError(Exception):
    """Base exception for time-domain failures."""


class TimestampParsingError(TimeError):
    """Raised when a timestamp representation cannot be parsed."""
