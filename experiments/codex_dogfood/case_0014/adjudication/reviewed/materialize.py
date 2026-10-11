"""Publish sealed Astra semantics unchanged inside an exact frame envelope.

Physical byte I/O is an explicit immutable import/serialization boundary: the
older text helper normalizes newlines and cannot authenticate physical bytes.
No scientific retrieval, semantic reviewer, or reconciliation is invoked.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, E501, COM812, EM101, TRY003
import argparse
import gzip
import importlib.util
import json
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ADJ = ROOT.parent
CASE = ADJ.parent
PACKET = CASE / "stage_c/packet"
STERILE = Path(r"C:\Users\recoveryadmin\CodexSterile\case_0014_stage_c_59a7f62ecc1e")
HASHES = {
    "STAGE_C_REVIEW.md": "628f2f1b86627c33f76807dd3875c7fd49b7dc7fb307f85a808e873de1dd4a4f",
    "stage_c_builder.py": "5f0e25a082118ee37651adc64d0d57228eaf0e7d7496d53f9798997c6762ddeb",
    "stage_c_hashes.json": "910ca60da636f3d888708a4709b95c2ca68969fb16f14a1c3f361d0249865a16",
    "stage_c_method.md": "e2a76a8feef89f0f5207333d4d3feaa67bb67c5b427f84b7844edb37703a713b",
    "stage_c_review.json": "cee15c825f70eee62162cf772f66597dfbfa6f51ef6567780ea161b08a7b59ea",
    "stage_c_statistics.json": "cb42c54dfde3cf88e492c3e40e3fe1f946b0eedeee5e172799d56ae4ffbbcefa",
    "stage_c_validation.json": "019cc61f46284e898615e911c64bd0e2c20c1356ad942c5e87d892163c7e920a",
}
BLIND = {
    "Git/history",
    "analyzed terms",
    "classification lexicon",
    "confirmation data",
    "contributions",
    "costs/timings",
    "decision rule",
    "gates",
    "inversions",
    "parent directory",
    "prior Codex-session content",
    "prior R1.7 interpretation",
    "prior gold",
    "prior semantic adjudication",
    "ranking metrics",
    "rankings",
    "repository checkout",
    "reserve data",
    "retrieval queries",
    "scores",
    "sibling workspaces",
    "term roles",
    "treatment arms",
    "treatment results",
    "web",
    "weights/multipliers",
}


def encoded(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode()


def sha(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_bytes())


def require(value: Any, message: str) -> None:
    if not value:
        raise ValueError(message)


def authenticate() -> tuple[Any, Any, Any]:
    primary = ADJ / "primary"
    for name, expected in HASHES.items():
        require(
            sha((primary / name).read_bytes()) == expected, "Sealed primary: " + name
        )
    manifest = load(primary / "stage_c_hashes.json")
    for name, expected in manifest["original_sha256"].items():
        require(sha((PACKET / name).read_bytes()) == expected, "Sealed packet: " + name)
    raw = gzip.decompress((PACKET / "resources.json.gz").read_bytes())
    require(
        sha(raw) == manifest["packet_digest_scopes"]["canonical_payload_sha256"],
        "Canonical payload",
    )
    payload = json.loads(raw)
    review = load(primary / "stage_c_review.json")
    require(
        set(review["blindness_attestation"]) == BLIND
        and set(review["blindness_attestation"].values()) == {"NO"},
        "Complete blindness attestation",
    )
    require(
        review["model"] == "GPT-6 Astra"
        and review["reasoning"] == "High"
        and review["no_second_reviewer"] is True,
        "Primary reviewer identity",
    )
    require(not review["unresolved_judgments"], "Unresolved primary gold")
    spec = importlib.util.spec_from_file_location(
        "case0014_primary_invariants", primary / "stage_c_builder.py"
    )
    require(spec is not None and spec.loader is not None, "Primary validator loader")
    assert spec is not None  # noqa: S101
    assert spec.loader is not None  # noqa: S101
    module: Any = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.packet(PACKET)
    module.validate_review(review, payload, module.seed())
    require(
        module.statistics(review) == load(primary / "stage_c_statistics.json"),
        "Primary statistics replay",
    )
    require(
        module.markdown(review, module.statistics(review))
        == (primary / "STAGE_C_REVIEW.md").read_bytes(),
        "Primary Markdown replay",
    )
    return review, payload, module


def construct_gold() -> Any:
    review, payload, _ = authenticate()
    frame = load(CASE / "frame.json")
    native = json.loads(gzip.decompress((CASE / "resources.json.gz").read_bytes()))
    require(
        payload["eligible_resources"]
        == [{k: r[k] for k in payload["eligible_resources"][0]} for r in native],
        "Exact semantic resource frame",
    )
    require(
        review["resource_frame"]
        == [{k: r[k] for k in review["resource_frame"][0]} for r in frame["resources"]],
        "Exact gold/native metadata frame",
    )
    design = load(CASE / "protocol.json")
    require(
        review["case"] == design["case"]
        and review["task_identity"] == design["task_identity"]
        and review["task_text"] == design["task_text"],
        "Exact case/task binding",
    )
    return {
        "schema": "case-0014-reviewed-gold-v1",
        "primary": review,
        "frame": {k: frame[k] for k in ("repository_id", "snapshot_id", "corpus_id")},
        "resource_bindings": review["resource_frame"],
        "provenance": {
            "source": "PRIMARY_ASTRA_HIGH",
            "semantic_transformation": "NONE",
            "primary_sha256": HASHES,
            "MODEL": "GPT-6 Astra",
            "REASONING": "High",
            "treatment_blind": True,
            "automatic_second_reviewer": False,
            "projection": "Full unchanged primary object; exact frame bindings only. No reconciliation or semantic modification.",
        },
    }


def validate(gold: Any) -> Any:
    source, payload, module = authenticate()
    module.validate_review(gold["primary"], payload, module.seed())
    require(
        gold["primary"] == source and gold == construct_gold(),
        "Exact reviewed projection identity",
    )
    return module.statistics(gold["primary"])


def markdown(gold: Any, stats: Any) -> bytes:
    review = gold["primary"]
    lines = [
        "# Case 0014 reviewed development gold",
        "",
        "Provenance: PRIMARY_ASTRA_HIGH; semantic_transformation = NONE. One primary review; no reconciliation or second reviewer.",
        "",
        (ADJ / "primary/STAGE_C_REVIEW.md").read_bytes().decode(),
    ]
    for name, value in [
        ("Reviewed statistics", stats),
        (
            "Exact frame and provenance",
            {"frame": gold["frame"], "provenance": gold["provenance"]},
        ),
        (
            "Complete positive cells and exact spans",
            [c for c in review["cells"] if c["label"] != "UNNECESSARY"],
        ),
        (
            "All semantic units and exact support alternatives/spans",
            review["semantic_units"],
        ),
        ("All witnesses and obligation intersections", review["obligation_semantics"]),
        ("All gaps", review["gaps"]),
        ("All limitations", review["limitations"]),
        ("Preserved design freedom", review["ambiguities"]),
    ]:
        lines += [
            "## " + name,
            "",
            "```json",
            encoded(value).decode().rstrip(),
            "```",
            "",
        ]
    lines += [
        "All 18,900 combinations, 2,850 sufficient resource unions, 126 inclusion-minimal union identities and the sufficient unit union are owned by reviewed_gold.json: primary.task_sufficiency. Their structures are unchanged from the sealed primary.",
        "",
    ]
    return ("\n".join(lines).rstrip() + "\n").encode()


def write_new(files: dict[Path, bytes]) -> None:
    if any(path.exists() for path in files):
        raise FileExistsError("Refusing to overwrite reviewed artifacts")
    for path, raw in files.items():
        with path.open("xb") as stream:
            stream.write(raw)


def outputs() -> dict[str, bytes]:
    gold = construct_gold()
    stats = validate(gold)
    _, payload, module = authenticate()
    mutations = module.adversarial(gold["primary"], payload, module.seed())
    files = {
        "reviewed_gold.json": encoded(gold),
        "reviewed_statistics.json": encoded(stats),
        "REVIEWED_GOLD.md": markdown(gold, stats),
        "reviewed_validation.json": encoded(
            {
                "status": "PASS",
                "statistics": stats,
                "semantic_transformation": "NONE",
                "primary_validation": load(ADJ / "primary/stage_c_validation.json"),
                "mutation_rejections": mutations,
                "checks": [
                    "exact sealed primary and packet bytes/replay",
                    "complete blindness",
                    "case/task/obligation/frame binding",
                    "all Cartesian cells",
                    "exact labels/spans/units/classes/alternatives",
                    "witness completeness/deletion minimality/exhaustive enumeration",
                    "task combinations/unions/inclusion minimality",
                    "obligation/task intersections",
                    "gaps/limitations/ambiguities unchanged",
                    "statistics/JSON/Markdown/hash replay",
                    "overwrite refusal and tamper rejection",
                ],
            }
        ),
    }
    files["reviewed_hashes.json"] = encoded(
        {
            "schema": "case-0014-reviewed-hashes-v1",
            "sha256": {n: sha(b) for n, b in files.items()},
            "materializer_sha256": sha(Path(__file__).read_bytes()),
            "import_metadata_sha256": sha((ADJ / "IMPORT.json").read_bytes()),
            "excluded": [".local", "self hash to avoid cycle"],
        }
    )
    return files


def verify() -> Any:
    files = outputs()
    for name, raw in files.items():
        require((ROOT / name).read_bytes() == raw, "Reviewed reconstruction: " + name)
    return {
        "status": "PASS",
        "sha256": {n: sha(b) for n, b in files.items()},
        "statistics": load(ROOT / "reviewed_statistics.json"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    if parser.parse_args().mode == "build":
        write_new({ROOT / n: raw for n, raw in outputs().items()})
    sys.stdout.write(encoded(verify()).decode())


if __name__ == "__main__":
    main()
