"""Select from catalog records without modifying their order or ownership."""

from .policy import eligible
from .versions import version_order


def choose_release(records, *, project, platform, include_previews=False):
    candidates = (
        row
        for row in records
        if eligible(
            row, project=project, platform=platform, include_previews=include_previews
        )
    )
    return max(candidates, key=lambda row: version_order(row.version), default=None)
