# Copyright (c) 2026
"""System primitives for developer tooling."""

from devtools.system.detection import get_operating_system
from devtools.system.models import OperatingSystem

__all__ = [
    "OperatingSystem",
    "get_operating_system",
]
