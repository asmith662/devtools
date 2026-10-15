# Copyright (c) 2026
# ruff: noqa: T201, E402, INP001, C901, PLR0912, PLR0915, E501 -- repository-owned metadata-only local usage CLI
"""Observe local usage, never account-wide subscription quota or scientific authority."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from devtools.agents.integrations.codex.errors import CodexOutputError
from devtools.agents.integrations.codex.sessions import read_exec_usage
from devtools.core.time import Timestamp
from devtools.models.interaction.usage import ModelUsage
from devtools.observability.usage import Attribution, Purpose, UsageWindow, report
from devtools.observability.usage.ingestion import from_capture, from_session
from devtools.observability.usage.models import UsageObservation
from devtools.observability.usage.storage import load, save, writer
from experiments.orchestration.storage import binary
from experiments.orchestration.storage import load as read_json
from experiments.orchestration.storage import save as save_metadata

if TYPE_CHECKING:
    from devtools.observability.usage.report import UsageReport

LEDGER = ROOT / ".local/usage/ledger.json"
WORKERS = Path("C:/ExperimentWorkers")


def backfill(at: Timestamp, *, codex_home: Path | None = None) -> dict[str, Any]:
    """Backfill identifiable metadata; no prompt-based purpose classification."""
    start = UsageWindow.rolling(at).start
    home = codex_home or Path.home() / ".codex"
    original = load(LEDGER)
    projected_sources = {"LOCAL_CODEX_EXEC_METADATA", "DEVTOOLS_LOCAL_CAPTURE"}
    observations = [r for r in original if r.source not in projected_sources]
    files: list[Path] = []
    for folder in (home / "sessions", home / "archived_sessions"):
        if folder.exists():
            files.extend(
                p
                for p in folder.rglob("*.jsonl")
                if p.stat().st_mtime >= start.value.timestamp()
            )
    workers = WORKERS
    if workers.exists():
        files.extend(
            p
            for p in workers.rglob("rollout-*.jsonl")
            if p.stat().st_mtime >= start.value.timestamp()
        )
    local = ROOT / ".local"
    failures = []
    for path in sorted(files):
        try:
            observations.extend(from_session(path))
        except (ValueError, OSError, KeyError) as error:
            failures.append(
                {"source": "LOCAL_CODEX_METADATA", "failure": type(error).__name__},
            )
    # Native engineering receipts contain normalized usage and no semantic text.
    engineering = ROOT / "experiments/orchestration/engineering/host_disclosure"
    for name in ("minimal", "capacity", "output"):
        path = engineering / (name + "-receipt.json")
        value = read_json(path)
        capture = value["measurement"]
        observations.append(
            from_capture(
                capture,
                timestamp=Timestamp.from_isoformat(value["timestamp"]),
                source="DEVTOOLS_ENGINEERING",
                source_digest=value["measurement"]["original_capture_sha256"],
                attribution=Attribution(
                    "devtools",
                    Purpose.EXPERIMENT_ENGINEERING,
                    "semantic-runtime-engineering",
                    stage=name,
                ),
            ),
        )
    # Historical adopted branch metadata is original consumption, not a new use.
    # Timestamp comes from session metadata where available, never file-copy mtime.
    timestamps: dict[str, Timestamp] = {}
    for row in observations:
        if row.thread_id and row.timestamp:
            timestamps[row.thread_id] = min(
                timestamps.get(row.thread_id, row.timestamp),
                row.timestamp,
                key=lambda t: t.value,
            )
    old = "b6cd4408b4dbc86a50c335f4a364898ff3b45c123becb7b6865c34208d3e1982"
    seals = ROOT / "experiments/orchestration/engineering/adopted_branches" / old
    for case in ("0022", "0023"):
        seal = read_json(seals / case / "seal.json")
        capture = seal["original_usage"]
        thread = capture["measurement"]["backend_thread_id"]["value"]
        # Existing worker captures retain authoritative launch UTC independently
        # of semantic messages. Missing launch evidence stays temporally UNKNOWN.
        timestamp = timestamps.get(thread)
        roots = [
            ROOT / ".local/experiment-runs" / old,
            WORKERS / old,
        ]
        for base in roots:
            if timestamp is not None:
                break
            for launch in base.glob(
                f"**/{case}/B/grounding-operation/worker/process/child.json",
            ):
                raw = binary(launch)
                match = re.search(rb'"launch_utc"\s*:\s*"([^"]+)"', raw)
                if match:
                    timestamp = Timestamp.from_isoformat(match[1].decode())
                    break
        observations.append(
            from_capture(
                capture,
                timestamp=timestamp,
                source="DEVTOOLS_ORIGINAL_BRANCH",
                source_digest=seal["original_usage"]["original_capture_sha256"],
                attribution=Attribution("devtools", Purpose.SCIENCE, old, case, "B"),
            ),
        )
    smoke = read_json(engineering / "smoke-receipt.json")
    trusted_threads = {r.thread_id for r in observations if r.thread_id} | {
        v["semantic_receipt"]["thread_id"] for v in smoke["paths"].values()
    }
    restored = [
        r
        for r in original
        if r.source in projected_sources and r.thread_id in trusted_threads
    ]
    observations.extend(restored)
    excluded_prior = sum(
        r.source in projected_sources and r.thread_id not in trusted_threads
        for r in original
    )
    unverified_stream_records = 0
    # Normalized files are metadata-only; source provenance is still required.
    for path in sorted(local.rglob("invocation-measurement.json")):
        value = read_json(path)
        if value.get("schema") != "semantic-invocation-measurement-v1":
            continue
        thread = value["measurement"]["backend_thread_id"]["value"]
        if (
            thread not in trusted_threads
            and path
            != local
            / "astra-capacity-failure-01/capture/invocation/invocation-measurement.json"
        ):
            continue
        timestamp = timestamps.get(thread)
        child = path.parent / "process/child.json"
        if child.exists():
            match = re.search(rb'"launch_utc"\s*:\s*"([^"]+)"', binary(child))
            if match:
                timestamp = Timestamp.from_isoformat(match[1].decode())
        observations.append(
            from_capture(
                value,
                timestamp=timestamp,
                source="DEVTOOLS_LOCAL_CAPTURE"
                if thread in trusted_threads
                else "DEVTOOLS_ENGINEERING_CONFIG_FAILURE",
                source_digest=hashlib.sha256(binary(path)).hexdigest(),
                attribution=Attribution("devtools", Purpose.EXPERIMENT_ENGINEERING),
            ),
        )
    failure = (
        ROOT
        / ".local/experiment-runs"
        / old
        / "logs/0022/C-semantic/process/child.json"
    )
    if failure.exists():
        raw = binary(failure)
        match = re.search(rb'"launch_utc"\s*:\s*"([^"]+)"', raw)
        observations.append(
            UsageObservation(
                timestamp=Timestamp.from_isoformat(match[1].decode())
                if match
                else None,
                backend="Codex",
                provider="OpenAI",
                model="gpt-6-astra",
                reasoning_effort="High",
                execution_profile="SEMANTIC_WORKER",
                invocation_id=old + "/0022/C",
                thread_id=None,
                turn_id=None,
                response_id=None,
                usage=ModelUsage(),
                source="DEVTOOLS_REJECTED_TURN",
                source_digest=hashlib.sha256(raw).hexdigest(),
                attribution=Attribution("devtools", Purpose.SCIENCE, old, "0022", "C"),
                completed=False,
                validated=False,
                accepted=False,
                failure_class="TRANSPORT_CHARACTER_LIMIT",
            ),
        )
    for folder in (local, workers):
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("stdout.log")):
            if path.stat().st_mtime < start.value.timestamp():
                continue
            try:
                records = read_exec_usage(path)
            except (ValueError, OSError, TypeError, CodexOutputError) as error:
                failures.append(
                    {
                        "source": "LOCAL_CODEX_EXEC_METADATA",
                        "failure": type(error).__name__,
                    },
                )
                continue
            child = path.parent / "child.json"
            timestamp = None
            if child.exists():
                match = re.search(rb'"launch_utc"\s*:\s*"([^"]+)"', binary(child))
                if match:
                    timestamp = Timestamp.from_isoformat(match[1].decode())
            for record in records:
                if not record.thread_id or record.thread_id not in trusted_threads:
                    unverified_stream_records += 1
                    continue
                observations.append(
                    UsageObservation(
                        timestamp=timestamp,
                        backend="Codex",
                        provider="OpenAI",
                        model="UNKNOWN",
                        reasoning_effort="UNKNOWN",
                        execution_profile="UNKNOWN",
                        invocation_id=None,
                        thread_id=record.thread_id,
                        turn_id=record.turn_id,
                        response_id=None,
                        usage=record.counts,
                        source="LOCAL_CODEX_EXEC_METADATA",
                        source_digest=hashlib.sha256(
                            (
                                record.thread_id + str(record.turn_id) + record.raw_json
                            ).encode(),
                        ).hexdigest(),
                        completed=True,
                    ),
                )
    for item in smoke["paths"].values():
        meta = item["semantic_receipt"]
        times = [
            r.timestamp
            for r in observations
            if r.thread_id == meta["thread_id"] and r.timestamp is not None
        ]
        child = Path(item["logs"]) / "process/child.json"
        if child.exists():
            match = re.search(rb'"launch_utc"\s*:\s*"([^"]+)"', binary(child))
            if match:
                times.append(Timestamp.from_isoformat(match[1].decode()))
        usage = meta["usage"]
        observations.append(
            UsageObservation(
                timestamp=min(times, key=lambda t: t.value) if times else None,
                backend="Codex",
                provider="OpenAI",
                model="gpt-6-luna",
                reasoning_effort=smoke["reasoning"],
                execution_profile="SEMANTIC_WORKER",
                invocation_id=meta["invocation"],
                thread_id=meta["thread_id"],
                turn_id=None,
                response_id=None,
                usage=ModelUsage(
                    input_tokens=usage.get("input_tokens"),
                    cached_input_tokens=usage.get("cached_input_tokens"),
                    cache_write_tokens=usage.get("cache_write_input_tokens"),
                    output_tokens=usage.get("output_tokens"),
                    reasoning_tokens=usage.get("reasoning_output_tokens"),
                ),
                source="DEVTOOLS_LUNA_ENGINEERING",
                source_digest=hashlib.sha256(
                    json.dumps(usage, sort_keys=True).encode()
                    + meta["thread_id"].encode(),
                ).hexdigest(),
                attribution=Attribution(
                    "devtools",
                    Purpose.EXPERIMENT_ENGINEERING,
                    "semantic-runtime-engineering",
                ),
                completed=True,
                validated=True,
                accepted=True,
            ),
        )
    with writer(LEDGER):
        archive = LEDGER.parent / "ledger-before-authenticated-import-01.json"
        if excluded_prior and not archive.exists():
            save(archive, original)
        # Import provenance correction is explicit and archived, never a
        # window-dependent deletion of authenticated historical consumption.
        current = load(LEDGER)
        additions = tuple(
            r
            for r in current
            if r.source not in projected_sources or r.thread_id in trusted_threads
        )
        save(LEDGER, (*additions, *observations))
    result = {
        "observed_at": str(at),
        "coverage": "PARTIAL",
        "local_session_files": len(files),
        "metadata_import_failures": failures,
        "unverified_native_records_not_counted": unverified_stream_records,
        "prior_provisional_rows_archived_and_excluded": excluded_prior,
        "stored_observations": len(load(LEDGER)),
        "ledger": str(LEDGER),
    }
    save_metadata(ROOT / ".local/usage/backfill.json", result)
    return result


def render(value: UsageReport) -> str:
    """Render concise known categories and coverage without dumping identifiers."""
    lines = [
        str(value["coverage"]),
        f"{value['window']['start']} .. {value['window']['end']} ({value['window']['timezone']})",
        f"Fresh turns {value['fresh_invocations']} | adopted uses {value['adopted_dependencies']} | accepted {value['accepted']} rejected {value['rejected']} failed {value['failed']} | missing usage {value['missing_usage_invocations']} conflicts {value['conflicting_invocations_excluded']}",
    ]
    lines.append(
        "Reported tokens "
        + " | ".join(
            f"{k}={v:,}"
            + (
                f" + UNKNOWN({value['unknown_category_observations'][k]})"
                if value["unknown_category_observations"][k]
                else ""
            )
            for k, v in value["tokens"].items()
        ),
    )
    lines.extend(
        f"{group['dimension']}={group['value']}: {group['fresh_invocations']} turns, {group['tokens']['input_tokens']:,} reported input"
        for group in value["groups"]
    )
    return "\n".join(lines)


def main() -> None:
    """Provide one-line ingest/report commands; no model operation exists."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("ingest", "report"))
    parser.add_argument("--rolling-days", type=int, default=7)
    parser.add_argument("--calendar-week", action="store_true")
    parser.add_argument("--previous-week", action="store_true")
    parser.add_argument("--timezone", default="America/New_York")
    parser.add_argument("--week-start", type=int, default=0)
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--at")
    parser.add_argument("--experiment")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    at = Timestamp.from_isoformat(args.at) if args.at else Timestamp.now()
    if args.command == "ingest":
        print(json.dumps(backfill(at), indent=2))
        return
    if args.refresh:
        backfill(at)
    if args.start or args.end:
        if not (args.start and args.end):
            parser.error("Both --start and --end are required (include UTC offset)")
        window = UsageWindow(
            Timestamp.from_isoformat(args.start),
            Timestamp.from_isoformat(args.end),
            args.timezone,
        )
    elif args.calendar_week or args.previous_week:
        window = UsageWindow.calendar_week(
            at,
            args.timezone,
            previous=args.previous_week,
            week_start=args.week_start,
        )
    else:
        window = UsageWindow.rolling(at, args.rolling_days, args.timezone)
    value = report(load(LEDGER), window, experiment=args.experiment)
    print(json.dumps(value, indent=2) if args.json else render(value))


if __name__ == "__main__":
    main()
