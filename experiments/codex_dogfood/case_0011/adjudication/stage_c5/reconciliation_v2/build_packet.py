"""Build only from the frozen blinded v1 packet; never load source adjudications."""

from __future__ import annotations

import gzip
import importlib.util
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def validator(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("bounded_packet_validator", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def payloads() -> dict[str, bytes]:
    v = validator(ROOT / "packet/validate_packet.py")
    old = ROOT.parent / "reconciliation/packet"
    validator(old / "validate_packet.py").validate(old)
    packet = v.load(gzip.decompress((old / "packet.json.gz").read_bytes()))
    packet["schema"] = "case-0011-neutral-c5-reconciliation-v2"
    packet["bindings"]["reliability_comparison_sha256"] = v.sha(
        (ROOT.parent / "reliability/c5_reliability_comparison.json").read_bytes()
    )
    packet["rules"] += [
        "Resolve only the 110 supplied propositions.",
        "Do not derive the final 576-pair mapping.",
        "Do not assign labels to omitted pairs.",
        "Do not assume omitted pairs are DOES_NOT_COVER.",
        "Do not reconstruct source adjudications.",
        "Do not calculate final full-frame unit/need/alternative counts.",
    ]
    raw = v.canonical(packet)
    archive = gzip.compress(raw, mtime=0)
    manifest = {
        "schema": "case-0011-neutral-c5-manifest-v2",
        "packet_identity": v.sha(raw),
        "archive_sha256": v.sha(archive),
        "canonical_payload_sha256": v.sha(raw),
        "bindings": packet["bindings"],
        "proposition_counts": v.COUNTS,
        "proposition_identities": [p["identity"] for p in packet["propositions"]],
        "semantic_propositions_sha256": v.sha(v.canonical(packet["propositions"])),
        "output_scope": "BOUNDED_110_PROPOSITION_DECISIONS_ONLY",
        "absent_pair_default": None,
    }
    files = {
        name: (ROOT / "packet" / name).read_bytes()
        for name in v.FILES - {"packet.json.gz", "manifest.json", "integrity.json"}
    }
    files["packet.json.gz"] = archive
    files["manifest.json"] = v.canonical(manifest)
    files["integrity.json"] = v.canonical(
        {
            "schema": "case-0011-neutral-c5-integrity-v2",
            "archive_sha256": v.sha(archive),
            "canonical_payload_sha256": v.sha(raw),
            "manifest_sha256": v.sha(files["manifest.json"]),
            "files": {name: v.sha(value) for name, value in sorted(files.items())},
        }
    )
    return files


def write(target: Path) -> dict[str, str]:
    assert not target.exists(), "OVERWRITE_REFUSED"
    files = payloads()
    target.mkdir(parents=True)
    for name, raw in files.items():
        with (target / name).open("xb") as stream:
            stream.write(raw)
    return {
        name: validator(ROOT / "packet/validate_packet.py").sha(raw)
        for name, raw in files.items()
    }


if __name__ == "__main__":
    import sys

    write(Path(sys.argv[1]))
