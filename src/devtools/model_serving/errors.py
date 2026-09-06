# Copyright (c) 2026
"""Errors specific to experimental vLLM serving lifecycle operations."""


class ModelServingError(Exception):
    """Base error for model-serving failures that add domain meaning."""


class VLLMLaunchError(ModelServingError):
    """Raised when Docker rejects an attempted vLLM container launch."""


class VLLMInspectionError(ModelServingError):
    """Raised when Docker cannot establish an owned container's state."""


class ServingReadinessTimeoutError(ModelServingError):
    """Raised when a launched provider never becomes ready in time."""


class VLLMOwnershipError(ModelServingError):
    """Raised when a retained container is not owned by this server handle."""


class VLLMStopError(ModelServingError):
    """Raised when Docker cannot stop an owned vLLM container."""
