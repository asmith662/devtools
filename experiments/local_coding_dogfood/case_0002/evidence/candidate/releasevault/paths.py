"""Safe presentation names for a selected artifact; no download side effects."""

import re


def artifact_filename(artifact):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", artifact.project):
        raise ValueError("unsafe project filename")
    suffix = artifact.platform.strip().casefold()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", suffix):
        raise ValueError("unsafe platform filename")
    return f"{artifact.project}-{artifact.version}-{suffix}.pkg"
