# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, E501, EM101, TRY003, T201, PLC0415 -- bounded one-attempt capture CLI
"""Execute once; replay/finalization use only immutable returned native values."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import platform
import sys
import time
import traceback
import unicodedata
from functools import partial
from pathlib import Path
from typing import Any

from devtools.context.localization.grounding.resolve import ground_task_anchor
from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    TaskProvenance,
)
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal, exclusive
from experiments.codex_dogfood.case_0012.stage_b.execute import index_for
from experiments.codex_dogfood.case_0013 import freeze, protocol
from experiments.codex_dogfood.case_0013.stage_b import native
from experiments.codex_dogfood.case_0013.stage_b.authenticate import (
    STAGE_A,
    authenticate,
)
from experiments.exact_hint_routing import routing
from experiments.exact_hint_routing.serialization import project
from experiments.mechanism_routing.composition import compose
from experiments.mechanism_routing.policy import Arm

PACKAGE = Path(__file__).resolve().parent
CAPTURE = PACKAGE / "attempts/case-0013-stage-b-1"
EXECUTION = "case-0013-stage-b-1"


def source_hashes() -> dict[str, str]:
    """Seal this producer/reporting plus every actually reused capture substrate."""
    reused = ROOT / "experiments/codex_dogfood/case_0012/stage_b"
    files = {
        *PACKAGE.glob("*.py"),
        PACKAGE / "README.md",
        PACKAGE / ".gitattributes",
        PACKAGE / "pytest.ini",
        *(
            reused / n
            for n in (
                "durability.py",
                "graph.py",
                "canonical.py",
                "execute.py",
                "reporting.py",
            )
        ),
    }
    return {p.relative_to(ROOT).as_posix(): digest(binary(p)) for p in sorted(files)}


def run_schedule(j: Journal, image: dict[str, Any], t: dict[str, Any]) -> None:
    """Invoke each frozen operation once and capture independent arm resolutions."""
    metadata = image["metadata"]
    s = j.call(
        "frame:resources",
        {"snapshot": metadata["snapshot_id"]},
        lambda: native.snapshot(image),
    )
    universe = j.call(
        "frame:modules",
        {"universe": metadata["module_universe_identity"]},
        lambda: native.modules(s, metadata),
    )
    addresses = j.call(
        "frame:declarations",
        {"addresses": metadata["declaration_resource_universe"]},
        lambda: tuple(
            RepositoryResourceAddress(a)
            for a in metadata["declaration_resource_universe"]
        ),
    )
    frame = j.call(
        "frame:assembly",
        {"frame": metadata["frame_identity"]},
        lambda: native.assemble(s, universe, addresses, metadata),
    )
    index = j.call(
        "index-build", {"frame": frame.identity}, lambda: index_for(frame, metadata)
    )
    lexical = {}
    for key, text in [
        ("global", t["global_safety_query"]["text"]),
        *[(o["key"], o["query"]) for o in t["obligations"]],
    ]:
        lexical[key] = j.call(
            "lexical:" + key,
            {"query": text, "maximum_results": len(s.resources)},
            partial(
                retrieve_repository_text_documents_by_bm25,
                query=analyze_repository_text_lexical_query(text=text),
                index=index,
                maximum_results=len(s.resources),
            ),
        )
    j.call("arm:A", {"lanes": list(lexical)}, lambda: lexical)
    bases = j.call(
        "purposes:shared",
        {"task": t["task_identity"], "purposes": len(t["acquisition_intents"])},
        lambda: native.purposes(t),
    )
    original_ground = ground_task_anchor
    active_route = [""]
    subcalls: dict[str, int] = {}

    def observed_ground(**kwargs: Any) -> Any:
        key = active_route[0]
        subcalls[key] = subcalls.get(key, 0) + 1
        return j.call(
            f"ground:{key}:{subcalls[key]}",
            project(kwargs["request"]),
            lambda: original_ground(**kwargs),
        )

    setattr(routing, "ground_task_anchor", observed_ground)  # noqa: B010 -- instrument native boundary
    hint_keys = {h["identity"]["value"]: h["key"] for h in t["hint_inventory"]}
    try:
        for arm in (Arm.B, Arm.C):

            def capture_arm(arm: Arm = arm) -> dict[str, Any]:
                plan = j.call(
                    "policy:" + arm.name,
                    {"arm": arm.value, "task": t["task_identity"]},
                    lambda: native.policy(arm, bases, t),
                )
                results = []
                for d in plan:
                    if d.request is None:
                        continue
                    request = d.request
                    h = hint_keys[request.hint.identity.value]
                    active_route[0] = arm.name + ":" + h
                    result = j.call(
                        "route:" + active_route[0],
                        {
                            "arm": arm.name,
                            "request": project(request),
                            "request_identity": request.identity,
                        },
                        partial(routing.resolve, frame, request),
                    )
                    results.append(result)
                views = {}
                for o in t["obligations"]:
                    key = o["key"]
                    lane = LocalizationObligationIdentity(protocol.TASK_ID, key)
                    lane_plan = tuple(
                        d for d in plan if d.basis.need.obligation == lane
                    )
                    lane_results = tuple(
                        r for r in results if r.request.association.lane == lane
                    )
                    views[key] = j.call(
                        f"present:{arm.name}:{key}",
                        {"arm": arm.name, "obligation": o["identity"]},
                        partial(
                            compose,
                            frame,
                            lane,
                            lexical[key],
                            lexical["global"],
                            lane_plan,
                            lane_results,
                            TaskProvenance(
                                protocol.TASK_ID.value,
                                explanation=f"Arm {arm.name} frozen construction",
                            ),
                        ),
                    )
                return {"policy": plan, "resolutions": tuple(results), "views": views}

            j.call(
                "arm:" + arm.name,
                {
                    "arm": arm.value,
                    "requests": [
                        r["identity"] for r in t["exact_route_requests"][arm.name]
                    ],
                },
                capture_arm,
            )
    finally:
        setattr(routing, "ground_task_anchor", original_ground)  # noqa: B010
    j.complete()


async def execute() -> dict[str, Any]:
    """Authenticate before exclusive claim; no resume or implicit retry."""
    if CAPTURE.exists():
        raise FileExistsError("Attempt already exists; native retry refused")
    authentication = await authenticate()
    if (await git("rev-parse", "HEAD")).decode().strip() != STAGE_A or (
        await git("rev-parse", "origin/main")
    ).decode().strip() != STAGE_A:
        raise ValueError("Unexpected capture parent")
    if (
        (await git("branch", "--show-current")).decode().strip() != "main"
        or (await git("diff", "--name-only")).strip()
        or (await git("diff", "--cached", "--name-only")).strip()
    ):
        raise ValueError("Expected clean tracked main/index before execution")
    t = read_json(freeze.CASE / "treatment.json")
    image = json.loads(gzip.decompress(binary(freeze.CASE / "inputs.json.gz")))
    metadata = authentication["frame"]
    marker = {
        "case": "case-0013",
        "execution": EXECUTION,
        "stage_a_commit": STAGE_A,
        "stage_a_integrity_sha256": digest(binary(freeze.CASE / "integrity.json")),
        "stage_a_trace_sha256": digest(binary(freeze.CASE / "trace.json")),
        "treatment_sha256": digest(binary(freeze.CASE / "treatment.json")),
        "frame": {
            k: metadata[k]
            for k in ("repository_id", "snapshot_id", "corpus_id", "frame_identity")
        },
        "implementation_sha256": {
            **read_json(freeze.CASE / "pre_execution.json")["implementation_sha256"],
            **source_hashes(),
        },
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "unicode": unicodedata.unidata_version,
        },
        "starting_invocation_counts": {
            "index_builds": 0,
            "queries": 0,
            "exact_routes": 0,
            "specialized_mechanisms": 0,
            "treatments": 0,
        },
        "scope": "TASK-ROLE-CONDITIONED EXACT-ROUTE ADMISSION",
    }
    j = Journal.start(CAPTURE, marker)
    j.context({"metadata": metadata, "treatment": t, "image": image})
    try:
        run_schedule(j, image, t)
    except BaseException as error:
        if not (CAPTURE / "capture_failure.json").exists():
            exclusive(
                CAPTURE / "capture_failure.json",
                {
                    "execution": EXECUTION,
                    "error_type": type(error).__qualname__,
                    "error": str(error),
                    "traceback": traceback.format_exc(),
                    "boundary": "NO NATIVE RETRY; entered/returned records authoritative; only complete returned schedule may finalize",
                    "gold": "ABSENT",
                    "effectiveness": "UNKNOWN",
                    "u3_outcome": "NOT_SELECTED",
                },
            )
        raise
    return finalize()


def outputs(j: Journal) -> dict[str, bytes]:
    """Derive mechanical artifacts solely from captured returns."""
    from experiments.codex_dogfood.case_0013.stage_b.reporting import (
        artifacts,
    )

    j.ready()
    if j.state["state"] != "NATIVE_CAPTURE_COMPLETE":
        raise ValueError("Incomplete native capture; no authoritative publication")
    return artifacts(j.state)


def finalize() -> dict[str, Any]:
    """Finish publication without invoking any native treatment operation."""
    started = time.perf_counter_ns()
    j = Journal.load(CAPTURE)
    result = outputs(j)
    for name, raw in result.items():
        destination = CAPTURE / name
        if destination.exists():
            if binary(destination) != raw:
                raise ValueError("Existing output differs; overwrite refused")
        elif name.endswith(".gz"):
            put_binary(destination, raw)
        else:
            put_text(destination, raw.decode())
    if not (CAPTURE / "publication_cost.json").exists():
        exclusive(
            CAPTURE / "publication_cost.json",
            {
                "elapsed_ns": time.perf_counter_ns() - started,
                "scope": "First read-only finalization and publication, descriptive; excluded from mechanism and charged treatment costs",
            },
        )
    sealed = {
        p.relative_to(CAPTURE).as_posix(): digest(binary(p))
        for p in CAPTURE.rglob("*")
        if p.is_file() and p.name != "integrity.json"
    }
    seal = {
        "schema": "case-0013-stage-b-integrity-v1",
        "sha256": sealed,
        "scope": "canonical UTF-8 LF text; exact gzip; journal immutable native graph; no operational .local",
    }
    if (CAPTURE / "integrity.json").exists():
        if read_json(CAPTURE / "integrity.json") != seal:
            raise ValueError("Final integrity differs")
    else:
        put_text(CAPTURE / "integrity.json", json_bytes(seal).decode())
    return verify()


def verify() -> dict[str, Any]:
    """Authenticate and reconstruct without retrieval, resolution or presentation."""
    seal = read_json(CAPTURE / "integrity.json")
    actual = {
        p.relative_to(CAPTURE).as_posix()
        for p in CAPTURE.rglob("*")
        if p.is_file() and p.name != "integrity.json"
    }
    if actual != set(seal["sha256"]) or any(
        digest(binary(CAPTURE / p)) != h for p, h in seal["sha256"].items()
    ):
        raise ValueError("Capture digest/coverage differs")
    j = Journal.load(CAPTURE)
    if (CAPTURE / "capture_failure.json").exists():
        raise ValueError("Failed attempt is not authoritative")
    if j.state["marker"]["stage_a_integrity_sha256"] != digest(
        binary(freeze.CASE / "integrity.json")
    ):
        raise ValueError("Stage A binding differs")
    for p, h in j.state["marker"]["implementation_sha256"].items():
        if digest(binary(ROOT / p)) != h:
            raise ValueError("Captured implementation differs")
    for name, raw in outputs(j).items():
        if binary(CAPTURE / name) != raw:
            raise ValueError("Deterministic captured replay differs: " + name)
    return read_json(CAPTURE / "summary.json")


def main() -> None:
    """Keep execute distinct from immutable-return-only finalization and verification."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("execute", "finalize", "verify"))
    operation = parser.parse_args().operation
    result = (
        asyncio.run(execute())
        if operation == "execute"
        else finalize()
        if operation == "finalize"
        else verify()
    )
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "stage_b",
                    "execution",
                    "counts",
                    "gold",
                    "effectiveness",
                    "u3_outcome",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
