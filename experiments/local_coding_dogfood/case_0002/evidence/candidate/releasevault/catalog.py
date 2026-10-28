"""Public client API over a retained catalog snapshot."""

from .cache import CatalogSnapshot
from .display import ordered_versions
from .manifest import decode_manifest
from .selection import choose_release


class Catalog:
    def __init__(self, records):
        self.snapshot = CatalogSnapshot(tuple(records))

    @classmethod
    def from_manifest(cls, text):
        return cls(decode_manifest(text))

    def choose(self, project, platform, *, include_previews=False):
        return choose_release(
            self.snapshot.records,
            project=project,
            platform=platform,
            include_previews=include_previews,
        )

    def versions(self, project):
        return ordered_versions(
            row for row in self.snapshot.records if row.project == project
        )
