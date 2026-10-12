"""Authenticate immutable physical import bytes against Git blob content."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, D103, COM812
import argparse
import asyncio
import json
import sys

from experiments.codex_dogfood.case_0009.artifacts import ROOT, git
from experiments.codex_dogfood.case_0015.adjudication.reviewed import materialize as m


async def verify(revision: str, *, sterile: bool = False) -> dict[str, str]:
    revision = "" if revision == "INDEX" else revision
    primary = m.ADJ / "primary"
    prefix = primary.relative_to(ROOT).as_posix() + "/"
    result = {}
    for name, expected in m.HASHES.items():
        physical = (primary / name).read_bytes()
        blob = await git("show", revision + ":" + prefix + name)
        if m.sha(physical) != expected or blob != physical:
            raise ValueError("Physical/Git primary byte mismatch: " + name)
        if sterile and (m.STERILE / name).read_bytes() != physical:
            raise ValueError("Sterile/import byte mismatch: " + name)
        result[name] = expected
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "revision", help="INDEX for staged blobs; commit for committed blobs"
    )
    parser.add_argument("--sterile", action="store_true")
    args = parser.parse_args()
    sys.stdout.write(
        json.dumps(asyncio.run(verify(args.revision, sterile=args.sterile)), indent=2)
        + "\n"
    )


if __name__ == "__main__":
    main()
