# Copyright (c) 2026
"""Explicit supplied-population roles, never inferred from working Context."""

from enum import Enum


class PopulationScope(Enum):
    """Retain the declared PopulationScope scientific values and invariants."""

    FULL_DESCRIPTIVE = "full_descriptive"
    DESCRIPTIVE_SUBSET = "descriptive_subset"
    TRAINING = "training"
    VALIDATION = "validation"
    TEST = "test"
