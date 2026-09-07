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


class VLLMStartupError(ModelServingError):
    """Raised when an owned vLLM container exits before model readiness."""

    def __init__(self, message: str, *, provider_log_tail: str | None) -> None:
        """Initialize a bounded startup failure diagnostic."""
        self.provider_log_tail = provider_log_tail
        if provider_log_tail:
            message = f"{message}\n\nProvider log tail:\n{provider_log_tail}"
        super().__init__(message)


class VLLMOwnershipError(ModelServingError):
    """Raised when a retained container is not owned by this server handle."""


class VLLMStopError(ModelServingError):
    """Raised when Docker cannot stop an owned vLLM container."""
