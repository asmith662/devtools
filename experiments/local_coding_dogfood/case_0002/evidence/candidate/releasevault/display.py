"""Version display ordering shares catalog version semantics."""

from .versions import parse_version, version_order


def ordered_versions(records):
    valid = []
    for row in records:
        try:
            parse_version(row.version)
        except ValueError:
            continue
        valid.append(row.version)
    return tuple(sorted(valid, key=version_order))
