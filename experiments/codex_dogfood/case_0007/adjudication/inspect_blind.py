# Copyright (c) 2026
# ruff: noqa: INP001, S101, T201
"""Case 0007: inspect only the two authorized frozen inputs."""

import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:  # noqa: C901, PLR0912
    """Enumerate/search frozen data without invoking any repository API."""
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode", choices=["verify", "inventory", "search", "show", "outline", "lines"]
    )
    parser.add_argument("terms", nargs="*")
    args = parser.parse_args()
    manifest_bytes = (HERE / "blind_manifest.json").read_bytes()
    archive_bytes = (HERE / "blind_resources.json.gz").read_bytes()
    manifest = json.loads(manifest_bytes)
    resources = json.loads(gzip.decompress(archive_bytes))
    if args.mode == "verify":
        print("manifest_sha256", hashlib.sha256(manifest_bytes).hexdigest())
        print("archive_sha256", hashlib.sha256(archive_bytes).hexdigest())
        assert (
            hashlib.sha256(archive_bytes).hexdigest()
            == manifest["resource_archive"]["sha256"]
        )
        print("count", len(resources))
        print("first resource", json.dumps(resources[0], ensure_ascii=False)[:6000])
        keys = set()

        def visit(value: object) -> None:
            if isinstance(value, dict):
                keys.update(value)
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(resources)
        print("archive keys", sorted(keys))
    elif args.mode == "inventory":
        for index, resource in enumerate(resources):
            print(index, resource["address"])
    elif args.mode == "show":
        for term in args.terms:
            parts = [int(part) for part in term.split(":")]
            resource = resources[parts[0]]
            print("RESOURCE", term, resource["address"])
            for number, line in enumerate(resource["content"].splitlines(), 1):
                if len(parts) == 1 or parts[1] <= number <= parts[2]:
                    print(f"{number}: {line}")
    elif args.mode == "outline":
        for term in args.terms:
            resource = resources[int(term)]
            print("RESOURCE", term, resource["address"])
            for number, line in enumerate(resource["content"].splitlines(), 1):
                if line.startswith(("def ", "class ", "#", "    def ")):
                    print(f"{number}: {line}")
    elif args.mode == "lines":
        for index, resource in enumerate(resources):
            for number, line in enumerate(resource["content"].splitlines(), 1):
                if any(term.lower() in line.lower() for term in args.terms):
                    print(f"{index} {resource['address']}:{number}: {line}")
    else:
        for index, resource in enumerate(resources):
            text = json.dumps(resource, ensure_ascii=False)
            if any(term.lower() in text.lower() for term in args.terms):
                print(index, resource["address"])


if __name__ == "__main__":
    main()
