# Copyright (c) 2026
# ruff: noqa: ANN401, PLR2004, S311 -- prospectively frozen design-aware sampling, not cryptography
"""Census first; fixed-size obligation-stratified SRS without replacement."""

import hashlib
import math
import random
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import require
from experiments.orchestration.workers import schema
from experiments.source_grounding import contracts
from experiments.source_grounding.discrimination import gold

SEED = "PURPOSE_RELATIVE_SOURCE_GROUNDING-CANDIDATE-DISCRIMINATION-01"
MARGIN = 0.15
OUTPUT_BYTES = 63357


def half_width(population: int, sample: int) -> float:
    """Worst-case binary 95% normal planning margin with finite correction."""
    require(0 < sample <= population, "Finite nonempty sample")
    return (
        0.0
        if sample == population
        else 1.96
        * math.sqrt(0.25 * (population - sample) / ((population - 1) * sample))
    )


def packet(design: Any, rows: Any, units: Any) -> tuple[Any, Any]:
    """Disclose resource contents once and exact relation provenance through keys."""
    by = {r["address"]: r for r in rows}
    addresses = sorted(
        {u[role]["address"] for u in units for role in ("source", "target")},
    )
    keys = {address: f"s{i:04}" for i, address in enumerate(addresses)}
    facts = {f["fact_identity"]: f for u in units for f in u["references"]}
    reference_keys = {identity: f"r{i:04}" for i, identity in enumerate(sorted(facts))}
    declarations = {
        identity: f"d{i:04}"
        for i, identity in enumerate(
            sorted({f["target_declaration_identity"] for f in facts.values()}),
        )
    }
    disclosed = {
        "case": design["case"],
        "task": design["task_text"],
        "obligations": [
            {k: o[k] for k in contracts.BLIND_OBLIGATION} for o in design["obligations"]
        ],
        "resources": [
            {"source_key": keys[a], "address": a, "content": by[a]["content"]}
            for a in addresses
        ],
        "candidates": [
            {
                "candidate_id": f"c{i:04}",
                "obligation_id": u["obligation_id"],
                "source_key": keys[u["source"]["address"]],
                "target_key": keys[u["target"]["address"]],
                "references": [
                    reference_keys[f["fact_identity"]] for f in u["references"]
                ],
            }
            for i, u in enumerate(units)
        ],
        "references": [
            {
                "reference_key": reference_keys[identity],
                "source_key": keys[f["source_address"]],
                "target_key": keys[f["target_address"]],
                "source_range_utf8": f["source_range_utf8"],
                "native_route": f["native_route"],
                "target_declaration_key": declarations[
                    f["target_declaration_identity"]
                ],
            }
            for identity, f in sorted(facts.items())
        ],
    }
    host = {
        "resources": {keys[a]: by[a] for a in addresses},
        "units": {f"c{i:04}": u["identity"] for i, u in enumerate(units)},
        "references": {reference_keys[k]: v for k, v in facts.items()},
        "declarations": {v: k for k, v in declarations.items()},
    }
    return disclosed, host


def design_sample(design: Any, rows: Any, universe: Any) -> Any:
    """Choose n before random selection; packet size cannot bias inclusion.

    The complete census input must fit even if its output does not. Thus every
    possible selected subset fits: no outcome- or resource-size-dependent sample
    size. Output bounds use the census source length/key sizes for every choice.
    """
    all_units = universe["units"]
    require(bool(all_units), "Empty candidate surface cannot support discrimination")
    census, _ = packet(design, rows, all_units)
    raw = gold.render(census)
    require(
        len(raw.decode()) <= 700000 and len(raw) <= 700000,
        "One-call census-input upper bound does not fit; redesign required",
    )
    maximum_source = max(len(r["content"]) for r in census["resources"])
    keys = [r["source_key"] for r in census["resources"]]

    def bound(n: int) -> int:
        return schema.envelope(gold.contract(n, keys, maximum_source)).utf8_bytes

    populations = {
        o["id"]: sum(u["obligation_id"] == o["id"] for u in all_units)
        for o in design["obligations"]
    }
    require(
        all(populations.values()),
        "Every obligation needs a nonempty candidate population",
    )
    counts = {
        o: next(n for n in range(1, size + 1) if half_width(size, n) <= MARGIN)
        for o, size in populations.items()
    }
    require(
        bound(sum(counts.values())) <= OUTPUT_BYTES,
        "Precision target cannot fit one call; redesign required",
    )
    while (
        sum(counts.values()) < len(all_units)
        and bound(sum(counts.values()) + 1) <= OUTPUT_BYTES
    ):
        selected = max(
            (o for o in counts if counts[o] < populations[o]),
            key=lambda o: (half_width(populations[o], counts[o]), o),
        )
        counts[selected] += 1
    chosen = []
    for obligation, count in counts.items():
        population = [u for u in all_units if u["obligation_id"] == obligation]
        seed = int.from_bytes(
            hashlib.sha256((SEED + design["case"] + obligation).encode()).digest(),
        )
        chosen.extend(random.Random(seed).sample(population, count))
    chosen.sort(key=lambda u: hashlib.sha256((SEED + u["identity"]).encode()).digest())
    disclosed, host = packet(design, rows, chosen)
    response = gold.contract(
        len(chosen),
        [r["source_key"] for r in disclosed["resources"]],
        maximum_source,
    )
    rendered = gold.render(disclosed)
    require(
        len(rendered) <= len(raw) and len(rendered.decode()) <= len(raw.decode()),
        "Selected input exceeds census upper bound",
    )
    value = {
        "schema": "candidate-discrimination-stratified-design-v1",
        "case": design["case"],
        "universe_sha256": universe["sha256"],
        "seed": SEED,
        "sampling": "CENSUS"
        if len(chosen) == len(all_units)
        else "OBLIGATION_STRATIFIED_SRSWOR",
        "allocation": {
            o: {
                "N": size,
                "n": counts[o],
                "inclusion_probability": counts[o] / size,
                "weight": size / counts[o],
                "planning_margin_95": half_width(size, counts[o]),
            }
            for o, size in populations.items()
        },
        "selected": [u["identity"] for u in chosen],
        "packet": disclosed,
        "host": host,
        "response_schema": response,
        "input": {
            "sha256": digest(rendered),
            "characters": len(rendered.decode()),
            "utf8_bytes": len(rendered),
            "census_upper_characters": len(raw.decode()),
            "census_upper_bytes": len(raw),
        },
        "output_maximum": schema.envelope(response).__dict__,
        "scientific_calls": 1,
    }
    return {**value, "sha256": digest(json_bytes(value))}
