# Copyright (c) 2026
"""Case-local tracked-frame provenance with a portable native archive identity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from devtools.context.repository.discovery import RepositoryResourceDiscovery


@dataclass(frozen=True, slots=True)
class TrackedFrameDiscovery(RepositoryResourceDiscovery):
    """Qualify an explicit Git inventory without claiming recursive discovery."""

    DISCOVERY_SEMANTICS: ClassVar[str] = (
        "case-0007-bounded-git-tracked-regular-file-inventory-v1"
    )
