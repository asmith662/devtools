# Copyright (c) 2026
"""System primitives for developer tooling."""

from devtools.core.system.detection import get_operating_system
from devtools.core.system.models import OperatingSystem

__all__ = [
    "OperatingSystem",
    "get_operating_system",
]
