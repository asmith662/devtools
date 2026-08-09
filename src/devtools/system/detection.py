# Copyright (c) 2026
"""System detection helpers."""

import platform

from devtools.system.models import OperatingSystem


def get_operating_system() -> OperatingSystem:
    """Return the current operating-system family.

    :returns: Detected operating-system family.
    """
    system = platform.system()

    if system == "Windows":
        return OperatingSystem.WINDOWS

    if system == "Linux":
        return OperatingSystem.LINUX

    if system == "Darwin":
        return OperatingSystem.MACOS

    return OperatingSystem.OTHER
