# Copyright (c) 2026
"""System models."""

from enum import StrEnum


class OperatingSystem(StrEnum):
    """Supported operating-system families."""

    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    OTHER = "other"

    @property
    def is_windows(self) -> bool:
        """Return whether this value represents Windows."""
        return self is OperatingSystem.WINDOWS

    @property
    def is_linux(self) -> bool:
        """Return whether this value represents Linux."""
        return self is OperatingSystem.LINUX

    @property
    def is_macos(self) -> bool:
        """Return whether this value represents macOS."""
        return self is OperatingSystem.MACOS
