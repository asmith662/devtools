"""Eligibility is distinct from ordering eligible releases."""

from .versions import parse_version


def eligible(artifact, *, project, platform, include_previews):
    if not artifact.enabled or artifact.project != project:
        return False
    if artifact.platform.strip().casefold() != platform.strip().casefold():
        return False
    try:
        parts = parse_version(artifact.version)
    except ValueError:
        return False
    return include_previews or not parts.prerelease
