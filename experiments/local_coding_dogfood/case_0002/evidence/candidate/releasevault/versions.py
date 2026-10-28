"""Strict catalog version syntax and shared ordering values."""

import re
from dataclasses import dataclass

_VERSION = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)


@dataclass(frozen=True)
class VersionParts:
    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...]
    build: tuple[str, ...]


def parse_version(text: str) -> VersionParts:
    match = _VERSION.fullmatch(text)
    if match is None:
        raise ValueError("catalog versions require strict major.minor.patch syntax")
    major, minor, patch, preview, build = match.groups()
    identifiers = tuple(preview.split(".")) if preview else ()
    if any(
        part.isdecimal() and len(part) > 1 and part.startswith("0")
        for part in identifiers
    ):
        raise ValueError("numeric prerelease identifiers cannot have leading zeroes")
    return VersionParts(
        int(major),
        int(minor),
        int(patch),
        identifiers,
        tuple(build.split(".")) if build else (),
    )


def _identifier_key(identifier: str):
    # Numeric identifiers rank below nonnumeric and compare numerically;
    # other identifiers compare lexically (ASCII).
    if identifier.isdigit():
        return (0, int(identifier), "")
    return (1, 0, identifier)


def version_order(text: str) -> tuple:
    """Return a sortable ordering key for one accepted catalog version."""
    parts = parse_version(text)
    # A stable release ranks above any prerelease at the same core, so an
    # empty prerelease sequence maps to a higher rank than a non-empty one.
    # Build metadata is ignored for precedence.
    if parts.prerelease:
        pre_rank = 0
    else:
        pre_rank = 1
    return (
        parts.major,
        parts.minor,
        parts.patch,
        pre_rank,
        tuple(_identifier_key(identifier) for identifier in parts.prerelease),
    )
