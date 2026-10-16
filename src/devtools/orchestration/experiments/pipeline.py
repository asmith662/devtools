# Copyright (c) 2026
# ruff: noqa: EM101, TRY301, BLE001, COM812 -- bounded preparation outcomes carry evidence
"""Concrete non-executing experiment preparation through target-owned contracts."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, cast

from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Timestamp
from devtools.orchestration.experiments import receipts
from devtools.orchestration.experiments.target import PROGRAM
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import FileFormat, TextFile, read


class PreparationError(ValueError):
    """Carry a bounded preparation outcome, never execution authority."""

    def __init__(self, disposition: str, evidence: dict[str, Any]) -> None:
        """Retain stage diagnostics for durable inspection."""
        self.disposition, self.evidence = disposition, evidence
        super().__init__(str(evidence))


class ExperimentExecutionPipeline:
    """Prepare one prospective plan; no approval or scientific dispatch methods."""

    version = "1"

    def __init__(self, target: Path, receipt_root: Path, python: Path) -> None:
        """Require explicit target/environment and separate pipeline receipt storage."""
        self.target = resolve_path(target, base_directory=Path.cwd()).value
        self.receipt_root = resolve_path(receipt_root, base_directory=Path.cwd()).value
        self.python = resolve_path(python, base_directory=Path.cwd()).value
        if self.receipt_root.is_relative_to(self.target):
            message = "Preparation receipts must be outside the target checkout"
            raise ValueError(message)
        self.executor = CommandExecutor(
            output_policy=CommandOutputPolicy(max_stdout_bytes=16 << 20),
        )

    async def _git(self, *args: str) -> str:
        result = await self.executor.execute(
            Command("git").args(*args).cwd(resolve_path(self.target)),
        )
        if result.failed or result.stdout_truncated:
            raise PreparationError(
                "PLAN_INVALID_OR_INCOMPATIBLE",
                {
                    "error": result.stderr.decode(errors="replace"),
                },
            )
        return result.stdout.decode().strip()

    async def _stage(
        self,
        name: str,
        address: str,
        head: str,
        sha256: str,
    ) -> dict[str, Any]:
        result = await self.executor.execute(
            Command(str(self.python))
            .args("-B", "-c", PROGRAM, name, address, head, sha256)
            .cwd(resolve_path(self.target))
            .with_timeout(Duration.seconds(300)),
        )
        if result.stdout_truncated or result.stderr_truncated:
            raise PreparationError(
                "EVIDENCE_UNAVAILABLE",
                {"error": "Target output truncated"},
            )
        try:
            evidence = dict(json.loads(result.stdout))
        except (ValueError, TypeError) as error:
            raise PreparationError(
                "EVIDENCE_UNAVAILABLE",
                {
                    "error": "Target returned no structured evidence",
                    "stderr": result.stderr.decode(errors="replace"),
                },
            ) from error
        if result.failed:
            message = str(evidence.get("error", "Target check failed"))
            disposition = (
                "STARTUP_PREFLIGHT_FAILED"
                if "preflight" in message or "startup" in message
                else "BUDGET_REJECTED"
                if "BUDGET_BLOCKED" in message
                else "EVIDENCE_UNAVAILABLE"
                if name == "usage"
                else "BUDGET_UNAVAILABLE"
                if name == "budget"
                else "PLAN_INVALID_OR_INCOMPATIBLE"
            )
            raise PreparationError(disposition, evidence)
        return evidence

    async def prepare(self, plan: Path) -> dict[str, Any]:
        """Observe readiness once and persist terminal/interrupted stage receipts."""
        attempt = str(receipts.PreparationId.new())
        folder = self.receipt_root / attempt
        folder.mkdir(parents=True)  # Exclusive allocation; never reuse an attempt.
        started = str(Timestamp.now())
        result: dict[str, Any] = {
            "pipeline": "ExperimentExecutionPipeline",
            "version": self.version,
            "attempt": attempt,
            "started": started,
            "target": str(self.target),
            "python": str(self.python),
            "plan": str(plan),
            "plan_sha256": None,
            "target_head": None,
            "execution_authorized": "NO",
            "scientific_dispatches": 0,
            "approval": "SEPARATE_EXPLICIT_MAINTAINER_DECISION_REQUIRED",
            "stages": [],
            "report": str(folder / "result.json"),
        }
        receipts.store(folder / "start.json", result)
        active = "identity"
        begin = time.perf_counter()
        stage_started = started
        try:
            resolved = resolve_path(plan, base_directory=self.target).value
            address = resolved.relative_to(self.target).as_posix()
            # UTF-8 text decoding preserves exact bytes, including CRLF and BOM.
            file = cast(
                "TextFile",
                read(resolve_path(resolved), file_format=FileFormat.TEXT),
            )
            result.update(
                plan=address,
                plan_sha256=hashlib.sha256(
                    file.content.encode(file.encoding)
                ).hexdigest(),
            )
            head = await self._git("rev-parse", "HEAD")
            result["target_head"] = head
            result["target_git_directory"] = await self._git(
                "rev-parse",
                "--absolute-git-dir",
            )
            for active in ("validation", "usage", "budget"):
                begin = time.perf_counter()
                stage_started = str(Timestamp.now())
                evidence = await self._stage(
                    active,
                    address,
                    head,
                    result["plan_sha256"],
                )
                stage = {
                    "name": active,
                    "started": stage_started,
                    "finished": str(Timestamp.now()),
                    "elapsed_seconds": time.perf_counter() - begin,
                    "disposition": evidence.get("status", "INDETERMINATE"),
                    "evidence": evidence,
                }
                receipts.store(folder / (active + ".json"), stage)
                result["stages"].append(
                    {"name": active, "sha256": receipts.digest(stage)},
                )
                result[active] = evidence
            if await self._git("rev-parse", "HEAD") != head:
                raise PreparationError(
                    "PLAN_INVALID_OR_INCOMPATIBLE",
                    {"error": "Target HEAD changed"},
                )
            budget = result["budget"]["status"]
            result["disposition"] = (
                "EVIDENCE_UNAVAILABLE"
                if result["usage"]["status"] == "UNAVAILABLE"
                else "BUDGET_UNAVAILABLE"
                if budget != "BUDGET_CHECK_PASS"
                else "READY_FOR_APPROVAL"
            )
        except asyncio.CancelledError:
            result.update(disposition="INTERRUPTED", interrupted_stage=active)
            raise
        except PreparationError as error:
            result.update(
                disposition=error.disposition,
                failed_stage=active,
                error=error.evidence,
            )
        except Exception as error:
            result.update(
                disposition="PREPARATION_FAILED",
                failed_stage=active,
                error=str(error),
            )
        finally:
            if not any(stage["name"] == active for stage in result["stages"]):
                stage = {
                    "name": active,
                    "started": stage_started,
                    "finished": str(Timestamp.now()),
                    "elapsed_seconds": time.perf_counter() - begin,
                    "disposition": result["disposition"],
                    "evidence": result.get("error"),
                }
                receipts.store(folder / (active + ".json"), stage)
                result["stages"].append(
                    {"name": active, "sha256": receipts.digest(stage)},
                )
            result["finished"] = str(Timestamp.now())
            receipts.store(folder / "result.json", result)
        return result


def target_python(target: Path) -> Path:
    """Infer the checkout's own conventional environment, never the caller's."""
    return (
        target / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    )


def summary(result: dict[str, Any]) -> str:
    """Render human readiness, coverage and authority without manual run IDs."""
    validation = result.get("validation", {})
    baseline = result.get("usage", {})
    observed = baseline.get("observation") or {}
    inventory = validation.get("usage_budget", {})
    preflight = validation.get("worker_entrypoint_preflight", {})
    economics = validation.get("economics", {})
    models = validation.get("models", {})
    return "\n".join(
        [
            f"{result['disposition']}: {validation.get('name', result['plan'])}",
            f"Plan: {result['plan']} ({result['plan_sha256']})",
            f"Target: {result['target']} @ {result['target_head']}",
            f"Readiness: {validation.get('status', 'UNRESOLVED')}",
            "Startup preflight: " + str(preflight.get("status", "UNRESOLVED")),
            "Maximum fresh calls: " + str(inventory.get("fresh_call_limit", "UNKNOWN")),
            "Model call inventory: "
            + json.dumps(inventory.get("model_call_limits", {})),
            "Scientific purpose: " + str(validation.get("name", "UNRESOLVED")),
            "Semantic model/reasoning: "
            + json.dumps(
                {
                    "model": models.get("model_id", models.get("model")),
                    "reasoning": models.get("reasoning"),
                }
            ),
            "Forecast model/reasoning inventory: "
            + json.dumps(
                sorted(
                    {
                        (
                            str(call.get("model", "UNKNOWN")),
                            str(call.get("reasoning_effort", "UNKNOWN")),
                        )
                        for call in economics.get("calls", [])
                    }
                )
            ),
            "Adopted B branches (cases): "
            + json.dumps(sorted(validation.get("adopted_branches", {}))),
            "Economics forecast: "
            + json.dumps(
                {
                    "schema": economics.get("schema"),
                    "fresh_calls": economics.get("fresh_calls"),
                    "input_range": economics.get("input_range", "UNKNOWN"),
                    "output_range": economics.get("output_range", "UNKNOWN"),
                    "confidence": economics.get("confidence", "UNKNOWN"),
                    "provenance": economics.get("provenance", "AUTHENTICATED_PLAN"),
                    "details": "See validation evidence in report",
                }
            ),
            "Usage baseline (partial local, NOT account-wide): "
            + json.dumps(
                {
                    "status": baseline.get("status", "UNRESOLVED"),
                    "fresh_invocations": observed.get("fresh_invocations"),
                    "tokens": observed.get("tokens"),
                    "unknown_categories": observed.get("unknown_category_observations"),
                },
            ),
            "Budget disposition: "
            + json.dumps(
                {
                    "status": result.get("budget", {}).get("status", "UNRESOLVED"),
                    "reason": result.get("budget", {}).get("reason"),
                }
            ),
            (
                f"Approval: {result['approval']}; "
                "AUTHORIZED=NO; EXECUTED=NO; ACCEPTED=UNASSESSED"
            ),
            "Diagnostics: " + json.dumps(result.get("error")),
            f"Durable preparation report: {result['report']}",
        ],
    )
