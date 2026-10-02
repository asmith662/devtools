"""Exact-path and literal-text inspection confined to the blind archive."""

import argparse
import gzip
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["paths", "read", "search"])
parser.add_argument("terms", nargs="*")
args = parser.parse_args()
data = json.loads(gzip.decompress((ROOT / "blind_resources.json.gz").read_bytes()))
for resource in data["resources"]:
    path = resource["path"]
    if args.mode == "paths" and (not args.terms or any(t in path for t in args.terms)):
        print(path)
    elif args.mode == "read" and path in args.terms:
        print("RESOURCE " + path)
        print(resource["content"])
    elif args.mode == "search":
        for number, line in enumerate(resource["content"].splitlines(), 1):
            if any(t in line for t in args.terms):
                print(f"{path}:{number}: {line}")
