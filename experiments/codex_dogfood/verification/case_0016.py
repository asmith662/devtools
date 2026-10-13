# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, COM812, D102, D107, PLC0415, PLR2004 -- bounded adapter
"""Optimized Case 0016 authentication/replay; sealed scientific code stays intact."""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from types import FunctionType, SimpleNamespace
from typing import Any, cast

from devtools.core.time import Timestamp
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes, read_json
from experiments.codex_dogfood.case_0016 import freeze
from experiments.codex_dogfood.case_0016.adjudication.reviewed import (
    materialize as gold,
)
from experiments.codex_dogfood.case_0016.stage_b import authenticate as stage_a
from experiments.codex_dogfood.case_0016.stage_b import reporting as stage_b
from experiments.codex_dogfood.case_0016.stage_d import analysis, authentication
from experiments.performance.retrieval.benchmark import publish
from experiments.task_conditioned_graph import ranking, view

from .audit import sealed_files
from .bindings import bind, module_bindings
from .completion import AuthenticatedCompletion
from .completion import authenticate as authenticate_completion
from .journal import journal_type
from .native import NativeMemo
from .rows import build
from .spans import SourceSpans


@dataclass(frozen=True)
class AuthenticatedInputs:
    """Invocation-owned inputs; consumers must treat retained values as read-only.

    Nested historical dictionaries retain their original representation for exact
    output compatibility. They are not exported as a mutable shared/global cache.
    """

    data: Any
    primary: Any
    journal: Any
    completion: AuthenticatedCompletion | None = None


class Invocation:
    """One authentication owner, one expected-result owner, no persisted trust."""

    def __init__(self) -> None:
        self.memo, self.spans = NativeMemo(), SourceSpans()
        self.times: dict[str, int] = {}
        self.counts: dict[str, int] = {}
        self.started = time.perf_counter_ns()
        self.bundle: AuthenticatedInputs | None = None
        self.progress_path: Path | None = None
        self.last_progress = self.started
        self.memo.on_envelope = self.progress

    def progress(self, *, force: bool = False) -> None:
        now = time.perf_counter_ns()
        if self.progress_path is not None and (
            force or now - self.last_progress >= 5_000_000_000
        ):
            publish(
                self.progress_path,
                {
                    "timestamp": Timestamp.now().isoformat(),
                    "elapsed_ns": now - self.started,
                    "timings_ns": self.times,
                    "counts": self.counts,
                    "canonical_envelopes_started": self.memo.envelopes,
                    "shared_blocks_authenticated": self.memo.blocks_checked,
                    "native_nodes_checked": self.memo.nodes_checked,
                },
            )
            self.last_progress = now

    def phase(self, name: str, invoke: Any) -> Any:
        start = time.perf_counter_ns()
        sys.stdout.write(f"{Timestamp.now().isoformat()} {name} START\n")
        sys.stdout.flush()
        self.progress(force=True)
        result = invoke()
        self.times[name] = time.perf_counter_ns() - start
        sys.stdout.write(
            f"{Timestamp.now().isoformat()} {name} {self.times[name] / 1e9:.3f}s\n"
        )
        sys.stdout.flush()
        self.progress(force=True)
        return result

    def counted(self, name: str, invoke: Any) -> Any:
        self.counts[name] = self.counts.get(name, 0) + 1
        return self.phase(name, invoke)

    def reviewed(self) -> Any:
        primary = self.counted("primary_authentication", self.authenticate_primary)
        facade = module_bindings(gold, {})
        facade.authenticate = lambda: primary
        facade.construct_gold = bind(
            gold.construct_gold, {"authenticate": facade.authenticate}
        )
        expected_gold = facade.construct_gold()
        statistics = primary[2].statistics(primary[0])

        def validate(value: Any) -> Any:
            gold.require(value == expected_gold, "Exact unchanged reviewed projection")
            return statistics

        facade.validate = validate
        facade.outputs = bind(
            gold.outputs,
            {"construct_gold": lambda: expected_gold, "validate": validate},
        )
        files = self.counted("reviewed_gold_authentication", facade.outputs)
        for name, raw in files.items():
            gold.require(
                (gold.ROOT / name).read_bytes() == raw,
                "Reviewed reconstruction: " + name,
            )
        replay = {
            "status": "PASS",
            "sha256": {n: gold.sha(b) for n, b in files.items()},
            "statistics": statistics,
        }
        facade.outputs = lambda: files
        facade.verify = lambda: replay
        self.primary = primary
        return facade

    def authenticate_primary(self) -> Any:
        """Instrument only the fresh invocation-owned sealed primary module."""

        def specification(name: str, path: Any) -> Any:
            spec = importlib.util.spec_from_file_location(name, path)
            gold.require(
                spec is not None and spec.loader is not None, "Sealed validator loader"
            )
            if spec is None or spec.loader is None:
                raise ValueError("Sealed validator loader")
            module = importlib.util.module_from_spec(spec)

            def execute(target: Any) -> None:
                if spec.loader is None:
                    raise ValueError("Sealed validator loader")
                spec.loader.exec_module(target)
                adversarial = target.adversarial

                def checks(*args: Any, **kwargs: Any) -> Any:
                    self.counts["primary_adversarial_bundle"] = (
                        self.counts.get("primary_adversarial_bundle", 0) + 1
                    )
                    return adversarial(*args, **kwargs)

                original = target.bundle
                bundled = FunctionType(
                    original.__code__,
                    {**original.__globals__, "adversarial": checks},
                    original.__name__,
                    original.__defaults__,
                    original.__closure__,
                )

                def bundle(*args: Any, **kwargs: Any) -> Any:
                    self.counts["primary_bundle_executions"] = (
                        self.counts.get("primary_bundle_executions", 0) + 1
                    )
                    return bundled(*args, **kwargs)

                target.bundle = bundle

            return SimpleNamespace(
                module=module, loader=SimpleNamespace(exec_module=execute)
            )

        adapter = SimpleNamespace(
            util=SimpleNamespace(
                spec_from_file_location=specification,
                module_from_spec=lambda spec: spec.module,
            )
        )
        return bind(gold.authenticate, {"importlib": adapter})()

    def captured_bytes(self) -> None:
        capture = stage_a.CAPTURE
        gold.require(
            gold.sha((capture / "integrity.json").read_bytes()) == authentication.SEAL,
            "Authoritative capture seal",
        )
        seal = read_json(capture / "integrity.json")
        actual = {
            p.relative_to(capture).as_posix()
            for p in capture.rglob("*")
            if p.is_file() and p.name != "integrity.json"
        }
        gold.require(actual == set(seal["sha256"]), "Capture missing/extra files")
        for name, expected in seal["sha256"].items():
            gold.require(
                gold.sha((capture / name).read_bytes()) == expected,
                "Physical attempt-2 bytes: " + name,
            )

    def native(self) -> Any:
        self.phase("capture_byte_authentication", self.captured_bytes)
        return self.counted(
            "journal_native_authentication",
            lambda: journal_type(self.memo).load(stage_a.CAPTURE),
        )

    def probe(self, *, profile: bool = False) -> Any:
        """Bound a selected shared-state correspondence phase, not a full verifier."""
        import cProfile
        import io
        import pstats

        from experiments.codex_dogfood.case_0012.stage_b.durability import unpack
        from experiments.performance.retrieval.workload import native_inputs

        self.phase("capture_byte_authentication", self.captured_bytes)
        values = self.phase("shared_native_decode", native_inputs)
        records = {
            read_json(p)["operation"]["identity"]: p
            for p in (stage_a.CAPTURE / "operations").glob("*.returned.json")
        }
        selected: tuple[str, ...] = (
            "frame:prepare",
            "lexical:index",
            "query:Q1:A",
            "query:Q1:B",
            "query:Q2:A",
            "query:Q2:B",
            "ri:references:tests/observability/evidence/test_terminal.py",
        )
        if profile:
            selected = selected[:3]
        profiler = cProfile.Profile()
        for identity in selected:
            raw = self.phase(
                "unpack:" + identity,
                lambda identity=identity: unpack(
                    read_json(records[identity])["canonical"]
                ),
            )
            passed = self.phase(
                "correspond:" + identity,
                lambda identity=identity, raw=raw: (
                    profiler.runcall(self.memo.corresponds, values[identity], raw)
                    if profile and identity == "query:Q1:A"
                    else self.memo.corresponds(values[identity], raw)
                ),
            )
            gold.require(passed, "Probe native correspondence: " + identity)
        stream = io.StringIO()
        if profile:
            pstats.Stats(profiler, stream=stream).sort_stats("cumtime").print_stats(25)
        return {
            "status": "PASS",
            "timings_ns": self.times,
            "shared_blocks": self.memo.blocks_checked,
            "profile": stream.getvalue(),
        }

    def replay(self, journal: Any) -> Any:
        services = self.memo.services() | {
            "_extract_source_segment": self.spans.extract
        }
        graph = module_bindings(view, services, lookups=True)
        graph.build_reference_view = build(view.build_reference_view, services)
        graph.require_view = bind(
            view.require_view, {"build_reference_view": graph.build_reference_view}
        )
        checked_views: dict[int, Any] = {}

        def require_view(snapshot: Any, retained: Any) -> None:
            if id(retained) not in checked_views:
                graph.require_view(snapshot, retained)
                checked_views[id(retained)] = retained
            elif retained.snapshot != snapshot:
                raise ValueError("Reference view frame/provenance/weight mismatch")

        rank = module_bindings(
            ranking, services | {"require_view": require_view}, lookups=True
        )
        reporting = module_bindings(
            stage_b,
            services
            | {
                "require_view": require_view,
                "require_ranking": rank.require_ranking,
                "Journal": SimpleNamespace(load=lambda _: journal),
            },
            lookups=True,
        )
        return self.counted(
            "stage_b_reconstruction", lambda: reporting.verify(stage_a.CAPTURE)
        )

    def checkpoints(self, facade: Any) -> Any:
        """Authenticate historical checkpoints using the one reviewed projection."""
        original: Any = None

        async def authenticate_original() -> Any:
            nonlocal original
            if original is None:
                original = await freeze.authenticate_original()
            return original

        frozen = module_bindings(
            freeze, {"authenticate_original": authenticate_original}
        )
        amended = module_bindings(stage_a, {"freeze": frozen})
        inputs = module_bindings(authentication, {"m": facade, "a": amended})
        provenance = self.phase(
            "checkpoint_authentication", lambda: asyncio.run(inputs.checkpoints())
        )
        return inputs, provenance

    def authenticate(self) -> AuthenticatedInputs:
        """Authenticate normal downstream proof without decoding native archives."""
        if self.bundle is not None:
            if self.bundle.completion is None:
                raise ValueError("Use a fresh invocation when switching proof levels")
            return self.bundle
        start = time.perf_counter_ns()
        self.phase("sealed_historical_audit", sealed_files)
        facade = self.reviewed()
        inputs, provenance = self.checkpoints(facade)
        completion = self.counted(
            "capture_completion_proof_authentication",
            lambda: authenticate_completion(stage_a.CAPTURE),
        )
        self.times.update(dict(completion.timings))
        data = self.phase(
            "canonical_scientific_loading_indexing",
            lambda: inputs.read_inputs(provenance),
        )
        self.counts.update(
            native_archives_decoded=0,
            deep_correspondence_executions=0,
            completion_envelopes=completion.envelopes,
        )
        self.bundle = AuthenticatedInputs(data, self.primary, None, completion)
        self.times["stage_d_input_authentication_total"] = (
            time.perf_counter_ns() - start
        )
        return self.bundle

    def authenticate_deep(self) -> AuthenticatedInputs:
        """Explicit forensic replay; expensive native/algebra proof is re-executed."""
        if self.bundle is not None:
            if self.bundle.journal is None:
                raise ValueError("Use a fresh invocation when switching proof levels")
            return self.bundle
        start = time.perf_counter_ns()
        self.phase("sealed_historical_audit", sealed_files)
        facade = self.reviewed()
        original: Any = None

        async def authenticate_original() -> Any:
            nonlocal original
            if original is None:
                original = await freeze.authenticate_original()
            return original

        frozen = module_bindings(
            freeze, {"authenticate_original": authenticate_original}
        )
        amended = module_bindings(stage_a, {"freeze": frozen})
        inputs = module_bindings(authentication, {"m": facade, "a": amended})
        provenance = self.phase(
            "checkpoint_authentication", lambda: asyncio.run(inputs.checkpoints())
        )
        journal = self.native()
        self.replay(journal)
        data = self.phase("stage_d_read_inputs", lambda: inputs.read_inputs(provenance))
        self.bundle = AuthenticatedInputs(data, self.primary, journal)
        self.times["stage_d_input_authentication_total"] = (
            time.perf_counter_ns() - start
        )
        return self.bundle

    def construction_probe(self) -> Any:
        """Isolate artifact construction without claiming journal authentication."""
        from experiments.codex_dogfood.case_0012.stage_b.durability import Journal
        from experiments.performance.retrieval.workload import native_inputs

        self.phase("capture_byte_authentication", self.captured_bytes)
        values = self.phase("shared_native_decode", native_inputs)
        journal = Journal(
            stage_a.CAPTURE,
            {
                "marker": read_json(stage_a.CAPTURE / "execution_started.json"),
                "operations": read_json(stage_a.CAPTURE / "trace.json")["operations"],
                "values": values,
                "active": [],
                "state": "NATIVE_CAPTURE_COMPLETE",
            },
        )
        journal.pickler = None
        journal.events = 928
        journal.chain = read_json(stage_a.CAPTURE / "execution_completed.json")[
            "journal_chain_sha256"
        ]
        self.replay(journal)
        return {
            "status": "PASS",
            "scope": "ISOLATED_CONSTRUCTION_NOT_JOURNAL_AUTHENTICATION",
            "timings_ns": self.times,
            "counts": self.counts,
        }

    def expected(self, bundle: AuthenticatedInputs) -> dict[str, bytes]:
        """Historical construction, including every semantic/adversarial check, once."""
        from experiments.codex_dogfood.case_0016.stage_d import (
            metrics,
            reporting,
            validation,
        )

        def analyze(data: Any) -> Any:
            return self.counted("metrics_construction", lambda: metrics.analyze(data))

        def enrich(data: Any, result: Any) -> Any:
            return self.counted(
                "reporting_enrichment", lambda: reporting.enrich(data, result)
            )

        def validate(data: Any, result: Any) -> Any:
            start = time.perf_counter_ns()
            try:
                return validation.validate(data, result)
            finally:
                self.counts["stage_d_semantic_validation"] = (
                    self.counts.get("stage_d_semantic_validation", 0) + 1
                )
                self.times["stage_d_validation"] = (
                    self.times.get("stage_d_validation", 0)
                    + time.perf_counter_ns()
                    - start
                )

        def markdown(data: Any, result: Any) -> bytes:
            return cast(
                "bytes",
                self.counted(
                    "markdown_rendering", lambda: reporting.markdown(data, result)
                ),
            )

        expected = bind(
            analysis.expected,
            {
                "metrics": SimpleNamespace(analyze=analyze),
                "reporting": SimpleNamespace(enrich=enrich, markdown=markdown),
                "validation": SimpleNamespace(validate=validate),
            },
        )
        start = time.perf_counter_ns()
        files = expected(bundle.data)
        self.times["expected_artifacts_total"] = time.perf_counter_ns() - start
        self.times["artifact_encoding_hashing"] = self.times[
            "expected_artifacts_total"
        ] - sum(
            self.times[n]
            for n in (
                "metrics_construction",
                "reporting_enrichment",
                "stage_d_validation",
                "markdown_rendering",
            )
        )
        return cast("dict[str, bytes]", files)

    def verify(self, *, deep: bool = False) -> Any:
        bundle = self.authenticate_deep() if deep else self.authenticate()
        files = self.expected(bundle)
        start = time.perf_counter_ns()
        for name, raw in files.items():
            gold.require(
                (analysis.PACKAGE / name).read_bytes() == raw,
                "Stage D deterministic replay: " + name,
            )
        self.times["committed_byte_comparison"] = time.perf_counter_ns() - start
        self.times["complete_optimized_verify"] = time.perf_counter_ns() - self.started
        return {
            "status": "PASS",
            "verification_level": "DEEP_FORENSIC_REPLAY"
            if deep
            else "SEALED_DOWNSTREAM",
            "capture_time_deep_proof": "REEXECUTED" if deep else "AUTHENTICATED",
            "outcome": json.loads(files["analysis.json"])["outcome"],
            "sha256": {n: digest(raw) for n, raw in files.items()},
            "timings_ns": self.times,
            "counts": self.counts,
        }


def main() -> None:
    """Run an optimized verifier or an independently bounded target phase."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "phase",
        choices=(
            "native",
            "gold",
            "probe",
            "probe-profile",
            "construction",
            "verify",
            "deep",
        ),
    )
    parser.add_argument("--progress", type=Path)
    args = parser.parse_args()
    selected = args.phase
    invocation = Invocation()
    invocation.progress_path = args.progress
    if selected == "construction":
        result = invocation.construction_probe()
    elif selected in ("probe", "probe-profile"):
        result = invocation.probe(profile=selected == "probe-profile")
    elif selected == "native":
        journal = invocation.native()
        result = {
            "operations": len(journal.state["operations"]),
            "events": journal.events,
            "timings_ns": invocation.times,
            "counts": invocation.counts,
        }
    elif selected == "gold":
        invocation.reviewed()
        result = {"timings_ns": invocation.times, "counts": invocation.counts}
    else:
        result = invocation.verify(deep=selected == "deep")
    sys.stdout.write(json_bytes(result).decode())


if __name__ == "__main__":
    main()
