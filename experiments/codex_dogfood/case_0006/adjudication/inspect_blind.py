"""Exact text inspection of the two authorized blind inputs only."""

import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def resources():
    return json.loads(gzip.decompress((ROOT / "blind_resources.json.gz").read_bytes()))[
        "resources"
    ]


if __name__ == "__main__":
    for resource in resources():
        selections = [item.partition(":") for item in sys.argv[1:]]
        selected = next(
            (parts for parts in selections if parts[0] == resource["address"]), None
        )
        if selected is not None:
            bounds = selected[2].split("-") if selected[2] else []
            start, end = map(int, bounds) if bounds else (1, 1000000)
            print("RESOURCE", resource["address"], resource["content_identity"])
            for number, line in enumerate(resource["content"].splitlines(), 1):
                if start <= number <= end:
                    print(f"{number}: {line}")
