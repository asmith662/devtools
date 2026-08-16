# Copyright (c) 2026
"""Persistence-domain errors."""


class PersistenceError(Exception):
    """Base error for persistence-domain failures."""


class PersistenceFormatError(PersistenceError):
    """Raised when persisted data does not match a supported format."""


class PersistenceVersionError(PersistenceFormatError):
    """Raised when persisted data uses an unsupported version."""


class PersistenceConflictError(PersistenceError):
    """Raised when immutable persisted semantic identities conflict."""
