# Copyright (c) 2026
"""Provider-reported termination for one completed model interaction."""

from enum import StrEnum


class ModelTermination(StrEnum):
    """Describe the provider-reported reason one successful response ended."""

    NORMAL_STOP = "normal_stop"
    OUTPUT_LIMIT = "output_limit"
    TOOL_CALL = "tool_call"
