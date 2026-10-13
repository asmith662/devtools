# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003 -- bounded Stage A artifact codec
"""Authenticate public cards and observe only allowed historical parent trees.

Never imports the population builder: its administration replay opens holdouts.
No retrieval, lexical analysis, module interpretation or Reference derivation.
"""

from __future__ import annotations

import hashlib
import io
import json
import tarfile
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import ROOT, digest, git
from experiments.codex_dogfood.case_0015.freeze import eligible, frame

START = "8d2420bbbb873834c9bd0511cee1e193ce34ff6d"
POPULATION = "experiments/development_population/extension_01/historical/"
POPULATION_SHA = "062d56eb131c97e0dcac62f77cd503de0a83ff80b54d1900d36fc3c3e56286c4"
SELECTION_SHA = "f8001402319c3a9ed6c9d09553d5453d13a0bc2e636aebdea54ebc6c329f3942"
SEED = "55a91301a1249ecaf0513c0e8d1340a27a02ed12b78aabc3fa71773f39020637"
POPULATION_COUNT = 15


async def public_cards() -> list[Any]:
    """Authenticate the two public freeze sources and return first three cards."""
    await git("merge-base", "--is-ancestor", START, "HEAD")
    sources = {}
    for name, sha in (
        ("population_freeze.json", POPULATION_SHA),
        ("selection_provenance.json", SELECTION_SHA),
    ):
        raw = await git("show", START + ":" + POPULATION + name)
        if digest(raw) != sha or (ROOT / POPULATION / name).read_bytes() != raw:
            raise ValueError("Public population source differs")
        sources[name] = json.loads(raw)
    population = sources["population_freeze.json"]
    selection = sources["selection_provenance.json"]
    cards: list[Any] = population["selected_development_tasks"]
    if len(cards) != POPULATION_COUNT or selection["seed_sha256"] != SEED:
        raise ValueError("Population membership/seed differs")
    chosen = cards[:3]
    for position, card in enumerate(chosen, 1):
        if (
            card["case_id"] != f"historical-development-{position:03}"
            or card["selection_position"] != position
            or digest(card["task_text"].encode()) != card["task_source"]["task_sha256"]
        ):
            raise ValueError("Public task identity/order differs")
    return chosen


def parent_objects(listed: bytes) -> dict[str, str]:
    """Select broad regular parent blobs before content acquisition."""
    objects = {}
    for entry in listed.split(b"\0"):
        if not entry:
            continue
        metadata, raw_address = entry.split(b"\t", 1)
        address = raw_address.decode("utf8")
        if not eligible(address):
            continue
        mode, kind, oid = metadata.decode().split()
        if kind != "blob" or mode not in {"100644", "100755"}:
            raise ValueError("Eligible parent entry is not a regular blob")
        objects[address] = oid
    return objects


async def parent_blobs(card: Any) -> tuple[dict[str, bytes], dict[str, str]]:
    """Archive eligible parent blobs and authenticate every extracted Git blob."""
    parent = card["frame"]["parent_commit"]
    tree = (await git("rev-parse", parent + "^{tree}")).decode().strip()
    if tree != card["frame"]["parent_tree"]:
        raise ValueError("Parent tree differs")
    objects = parent_objects(await git("ls-tree", "-r", "-z", parent))
    archive = await git(
        "-c",
        "core.autocrlf=false",
        "archive",
        "--format=tar",
        parent,
        "--",
        *sorted(objects),
    )
    blobs = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            if member.isdir():
                continue
            stream = bundle.extractfile(member)
            if not member.isfile() or member.name not in objects or stream is None:
                raise ValueError("Unexpected parent archive entry")
            raw = stream.read()
            # Git SHA-1 object identity is the repository's existing object format.
            header = f"blob {len(raw)}\0".encode()
            oid = hashlib.sha1(header + raw, usedforsecurity=False).hexdigest()
            if oid != objects[member.name] or member.name in blobs:
                raise ValueError("Extracted parent bytes differ from Git blob")
            blobs[member.name] = raw
    if set(blobs) != set(objects):
        raise ValueError("Incomplete parent archive")
    return dict(sorted(blobs.items())), dict(sorted(objects.items()))


async def observe(card: Any) -> tuple[Any, Any]:
    """Use the established native observation/corpus adapter, never treatment."""
    blobs, objects = await parent_blobs(card)
    metadata, resources = frame(blobs)
    if any(r["content"] != blobs[r["address"]].decode("utf8") for r in resources):
        raise ValueError("Native observation altered parent text")
    metadata["source_head"] = card["frame"]["parent_commit"]
    metadata["source_tree"] = card["frame"]["parent_tree"]
    metadata["python_resource_count"] = sum(
        r["address"].endswith(".py") for r in resources
    )
    for collection in (resources, metadata["resources"]):
        for row in collection:
            row["git_blob_oid"] = objects[row["address"]]
    return metadata, resources
