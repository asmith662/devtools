"""Build only the neutral reconciliation packet, never reconciled decisions."""

from __future__ import annotations

import argparse
import gzip
from collections import Counter
from pathlib import Path
from typing import Any

from compare_c5 import ROOT, build, digest, encode, exclusive, load, neutral_packet
from validate_packet import FILES, check_payload, validate

INSTRUCTIONS = """# Treatment-blind C.5 semantic reconciliation packet

Validate first: python -B validate_packet.py. Verify all integrity/manifest hashes,
the archive and payload digests, bindings and exact workspace whitelist. Stop on
failure or unexpected files. Use only these five regular files; do not seek Git,
a repository checkout, another adjudication, source locations or external data.
The operational .local/codex-result.md handoff is excluded from evidence and hashes.

The packet preserves the frozen task, obligations, InformationNeed meanings,
required-unit meanings and ALL-complementary / ANY-alternative memberships.
Opaque identities have no quality or chronological rank. Position numbers are
assigned separately per proposition by canonical claim digest, with no global
reviewer numbering. No source mapping is supplied.

For every two-position dispute choose ACCEPT_POSITION_1, ACCEPT_POSITION_2,
REPLACE_WITH_RECONCILED_JUDGMENT or UNRESOLVED, with an explicit semantic rationale.
PAIR_LABEL decisions must state sought and established facts, and why a complete
answer would or would not establish the complete unit. DIRECT_RATIONALE items
require confirmation of the shared label and its defensible semantic rationale.
UNIT_STATUS and NEED_CLASSIFICATION decisions must follow reconciled mappings,
without mechanically inventing MISFORMULATED or AMBIGUOUS judgments.

Single-position granularity and collective audits are unconfirmed propositions.
For granularity choose ATOMIC_FOR_NEED_MAPPING, COLLECTIVELY_COVERABLE,
OVERCOMPOUND_FOR_PAIRWISE_MAPPING or AMBIGUOUS_GRANULARITY, with rationale.
For every proposed collective set explicitly judge complete sufficiency and
minimality; explain why removing each member loses a necessary fact. Replace or
leave unresolved unsupported sets. Do not treat structural validation as proof
of semantic truth. Never change frozen units or needs in this review.

Keep strict direct unit coverage separate from GRANULARITY_AWARE_COVERED, a
secondary diagnostic (direct or a confirmed complete collective set). Every
member of an alternative must be covered; never combine members across different
alternatives. Preserve the frozen U1 every-required-unit direct rule separately.

No majority voting. No automatic preference for more direct coverage. No
automatic preference for smaller or broader need sets. Preserve uncertainty.
Do not seek acquisition data, query strings, analyzer outputs, retrieval outputs,
answer resources, ranks, scores, costs, treatment arms, model identities,
confirmation or effectiveness outcomes. Do not perform Stage D. This packet
contains no reconciliation result; any later review must freeze its own results.
"""


def payloads() -> tuple[dict[str, bytes], dict[str, Any]]:
    d = load()
    comparison = build(d)
    packet, audit = neutral_packet(d, comparison)
    check_payload(packet)
    payload = encode(packet)
    archive = gzip.compress(payload, mtime=0)
    manifest = {
        "schema": "case-0011-neutral-c5-manifest-v1",
        "archive_sha256": digest(archive),
        "canonical_payload_sha256": digest(payload),
        "bindings": packet["bindings"],
        "proposition_counts": dict(
            sorted(Counter(p["kind"] for p in packet["propositions"]).items())
        ),
        "proposition_identities": [p["identity"] for p in packet["propositions"]],
    }
    files = {
        "packet.json.gz": archive,
        "manifest.json": encode(manifest),
        "INSTRUCTIONS.md": INSTRUCTIONS.encode(),
        "validate_packet.py": (ROOT / "validate_packet.py").read_bytes(),
    }
    integrity = {
        "schema": "case-0011-neutral-c5-integrity-v1",
        "archive_sha256": digest(archive),
        "canonical_payload_sha256": digest(payload),
        "manifest_sha256": digest(files["manifest.json"]),
        "files": {n: digest(v) for n, v in sorted(files.items())},
    }
    files["integrity.json"] = encode(integrity)
    assert set(files) == FILES
    return files, audit


def write(root: Path) -> dict[str, Any]:
    files, _ = payloads()
    assert not root.exists(), "OVERWRITE_REFUSED"
    root.mkdir(parents=True)
    for name, raw in files.items():
        exclusive(root / name, raw)
    return validate(root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(encode(write(args.output)).decode())
