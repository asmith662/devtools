"""Immutable source-order snapshots; no release policy is applied here."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogSnapshot:
    records: tuple

    def projects(self):
        return tuple(dict.fromkeys(row.project for row in self.records))
