# Copyright (c) 2026
"""Immutable reproducibility identity for a serving profile."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServingProfileFingerprint:
    """Identify one stable, behaviorally relevant serving profile snapshot."""

    value: str

    def __post_init__(self) -> None:
        """Reject ambiguous fingerprints."""
        if not self.value.strip() or self.value != self.value.strip():
            msg = (
                "Serving profile fingerprint must be nonblank without "
                "surrounding whitespace."
            )
            raise ValueError(msg)

    def __str__(self) -> str:
        """Return the canonical fingerprint text."""
        return self.value


@dataclass(frozen=True, slots=True)
class ServingProfileIdentity:
    """Describe the model environment that reproducibly served an interaction.

    Operational endpoint, container, readiness, and lifetime data intentionally
    do not belong here.
    """

    fingerprint: ServingProfileFingerprint
    provider: str
    served_model_alias: str
    context_capacity: int
    model_repository: str | None = None
    model_revision: str | None = None
    artifact_filename: str | None = None
    artifact_hash: str | None = None
    quantization: str | None = None
    server_build: str | None = None
    template_reasoning_defaults: str | None = None

    def __post_init__(self) -> None:
        """Validate only immutable identity/provenance facts."""
        for value, label in (
            (self.provider, "Provider"),
            (self.served_model_alias, "Served model alias"),
        ):
            if not value.strip() or value != value.strip():
                msg = f"{label} must be nonblank without surrounding whitespace."
                raise ValueError(msg)
        if isinstance(self.context_capacity, bool) or self.context_capacity <= 0:
            msg = "Serving profile context capacity must be a positive integer."
            raise ValueError(msg)
