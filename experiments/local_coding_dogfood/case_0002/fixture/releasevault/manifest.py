"""Catalog interchange; published record order is retained."""

import json
from dataclasses import asdict

from .models import Artifact


def decode_manifest(text):
    rows = json.loads(text)
    if not isinstance(rows, list):
        raise ValueError("manifest must contain an array")
    return tuple(Artifact(**row) for row in rows)


def encode_manifest(records):
    return json.dumps([asdict(row) for row in records], ensure_ascii=False)
