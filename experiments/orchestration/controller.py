# Copyright (c) 2026
# ruff: noqa: ANN401, E501, PLR0913, PLR0917, C901, PLR0912, PLR0915, ASYNC109, ASYNC240, TRY300, BLE001, SIM117 -- fixed experiment lifecycle, no general workflow DSL
"""Execute approved cohorts with immutable claims and serialized publication."""

from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
from contextlib import nullcontext
from pathlib import Path
from typing import Any

from devtools.agents.integrations.codex.parsing import parse_codex_turn_output
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from experiments.codex_dogfood.case_0009.artifacts import (
    digest,
    json_bytes,
)
from experiments.orchestration.cache import PreparationCache
from experiments.orchestration.isolation import (
    PRIMARY,
    candidate,
    preserve_packet,
    semantic_outputs,
    semantic_receipt,
    sterile,
)
from experiments.orchestration.lease import writer
from experiments.orchestration.model import (
    RunPlan,
    StageState,
    validation_tier,
)
from experiments.orchestration.publication import Repository
from experiments.orchestration.storage import (
    binary,
    bundle,
    exclusive,
    load,
    materialize,
    no_links,
    require,
    safe,
    save,
)
from experiments.orchestration.workers import codex
from experiments.orchestration.workers.process import invoke

PACKAGE = Path(__file__).resolve().parent


def expand(arguments: list[str], bindings: dict[str, str]) -> list[str]:
    """Replace named controller tokens while preserving literal JSON braces."""
    token = re.compile(r"\{(" + "|".join(map(re.escape, bindings)) + r")\}")
    return [
        token.sub(lambda match: bindings[match.group(1)], argument)
        for argument in arguments
    ]


def implementation() -> dict[str, str]:
    """Content-address controller code, without importing semantic experiment state."""
    return {
        p.relative_to(PACKAGE).as_posix(): digest(binary(p))
        for p in sorted(PACKAGE.rglob("*.py"))
        if "tests" not in p.parts and "runs" not in p.parts
    }


class Controller:
    """Run one immutable approved fixed Stage A/packet/B/C/import/D lifecycle."""

    def __init__(self, repository: Repository, plan: RunPlan, work_root: Path) -> None:
        """Bind distinct canonical and isolated computation roots."""
        no_links(work_root)
        work_root = resolve_path(work_root).value
        self.repository, self._plan, self.work_root = repository, plan, work_root
        self._run_id = plan.identity(implementation())
        require(
            not work_root.is_relative_to(repository.root),
            "Worker root must be outside canonical worktree",
        )
        no_links(work_root)
        require(
            all(not (p / ".git").exists() for p in (work_root, *work_root.parents)),
            "Worker root may not be inside a checkout",
        )
        self.prefix = self.value["publication"]["root"] + "/" + self.run_id
        self.science = safe(repository.root, self.prefix)
        self.operational = repository.root / ".local/experiment-runs" / self.run_id
        self.cache = PreparationCache(repository.root / ".local/experiment-cache")
        self.slots = asyncio.Semaphore(self.value["concurrency"]["workers"])
        self.branch_slots = {
            "B": asyncio.Semaphore(self.value["concurrency"]["cases"]),
            "C": asyncio.Semaphore(self.value["concurrency"]["semantic"]),
        }
        self.blocked = False
        self.started = time.perf_counter()
        self._state: dict[str, Any] = {
            "run_id": self.run_id,
            "status": "QUEUED",
            "stages": {},
            "publications": {},
            "automatic_scientific_retries": 0,
        }
        self.thread_ids: set[str] = set()
        self.approved_head = repository.expected_head

    @property
    def plan(self) -> RunPlan:
        """Expose the frozen approved plan without an assignment seam."""
        return self._plan

    @property
    def value(self) -> dict[str, Any]:
        """Return copies; a caller cannot change in-flight scientific configuration."""
        return self._plan.value

    @property
    def run_id(self) -> str:
        """Expose immutable identity rather than a caller-adjustable attempt."""
        return self._run_id

    @property
    def state(self) -> dict[str, Any]:
        """Return a deep operational snapshot without exposing controller internals."""
        return dict(json.loads(json.dumps(self._state)))

    @classmethod
    async def from_plan(
        cls,
        root: Path,
        plan_address: str,
        work_root: Path,
    ) -> Controller:
        """Authenticate committed approval/plan/Stage A and pinned adapter sources."""
        plan_path = safe(root, plan_address)
        repo = Repository(root, push=False)
        head = (await repo.git("rev-parse", "HEAD")).decode().strip()
        raw = await repo.git("show", head + ":" + plan_address)
        require(
            raw == binary(plan_path),
            "Run plan differs from committed bytes",
        )
        plan = RunPlan.parse(json.loads(raw))
        value = plan.value
        require(
            value["controller_implementation"] == implementation(),
            "Approved controller implementation differs",
        )
        repo.remote, repo.push_enabled = (
            value["publication"]["remote"],
            value["publication"]["push"],
        )
        await repo.authenticate(head)
        controller = cls(repo, plan, work_root)
        controller.approved_head = head
        await controller.authenticate_approved_inputs(head)
        return controller

    async def authenticate_approved_inputs(self, head: str) -> None:
        """Authenticate approval, reachable Stage A and exact frozen adapter sources."""
        repo, root, value = self.repository, self.repository.root, self.value
        approval = json.loads(await repo.git("show", head + ":" + value["approval"]))
        require(
            approval
            == {
                "approved": True,
                "stage_a_checkpoint": value["stage_a"]["checkpoint"],
                "plan_sha256": digest(self.plan.canonical),
            },
            "Explicit committed approval required",
        )
        await repo.git(
            "merge-base",
            "--is-ancestor",
            value["stage_a"]["checkpoint"],
            head,
        )
        for name in ("protocol", "integrity"):
            artifact = value["stage_a"][name]
            content = await repo.git(
                "show",
                value["stage_a"]["checkpoint"] + ":" + artifact["path"],
            )
            require(
                digest(content) == artifact["sha256"],
                "Stage A artifact digest differs",
            )
        for address, sha in value["implementation"].items():
            committed = await repo.git("show", head + ":" + address)
            require(
                digest(committed) == sha and binary(safe(root, address)) == committed,
                "Adapter implementation changed",
            )

    def progress(self, case: str, stage: str, status: str, **fields: Any) -> None:
        """Persist reconstructible status and operational progress without authority."""
        self._state["stages"][case + "/" + stage] = {"status": status, **fields}
        update = {
            "timestamp": str(Timestamp.now()),
            "elapsed_seconds": time.perf_counter() - self.started,
            "run_id": self.run_id,
            "case": case,
            "stage": stage,
            "worker_type": "SEMANTIC" if stage == "C" else "MECHANICAL",
            "model": self.value["semantic"]["model"] if stage == "C" else None,
            "reasoning": self.value["semantic"]["reasoning"] if stage == "C" else None,
            "completed": sum(
                v["status"] == "COMPLETE"
                and key.rsplit("/", 1)[1]
                in {"prepare", "packet", "B", "C", "import", "D"}
                for key, v in self._state["stages"].items()
            ),
            "total": len(self.plan.cases) * 5 + 1,
            "status": status,
            **fields,
        }
        save(self.operational / "progress.json", update)
        save(self.operational / "state.json", self._state)
        self.operational.mkdir(parents=True, exist_ok=True)
        with (self.operational / "progress.log").open("ab") as stream:
            stream.write((json.dumps(update, sort_keys=True) + "\n").encode())

    def stage_root(self, case: str, stage: str) -> Path:
        """Resolve only owned isolated worker directories."""
        return safe(self.work_root, self.run_id + "/" + case + "/" + stage)

    def journal(self, case: str, stage: str, event: str) -> Path:
        """Locate immutable controller claims outside non-authoritative .local."""
        return safe(
            self.science,
            "journal/" + case + "/" + stage + "/" + event + ".json",
        )

    def arguments(self, name: str, workspace: Path, case: str, stage: str) -> list[str]:
        """Expand only fixed controller bindings into frozen direct argv."""
        frame = next((c.frame for c in self.plan.cases if c.identity == case), {})
        bindings = {
            "workspace": str(workspace),
            "case": case,
            "stage": stage,
            "frame": json.dumps(frame),
            "run_id": self.run_id,
            "python": sys.executable,
            "repository": str(self.repository.root),
            "packet_commit": self._state["publications"].get("PACKET", ""),
            "stage_b_commit": self._state["publications"].get("B", ""),
            "gold_commit": self._state["publications"].get("C", ""),
        }
        return expand(self.value["commands"][name], bindings)

    def environment(self) -> dict[str, str]:
        """Inherit only frozen named environment values; never log credentials."""
        names = self.value["semantic"]["environment_allowlist"]
        require(
            all(n not in {"PYTHONPATH", "PYTHONSTARTUP", "CODEX_HOME"} for n in names),
            "Environment may not inject repository or prior Codex sessions",
        )
        return {name: os.environ[name] for name in names if name in os.environ}

    async def process(
        self,
        argv: list[str],
        workspace: Path,
        case: str,
        stage: str,
        timeout: str = "worker",
        environment: Any = None,
    ) -> Any:
        """Own one process lifecycle with persisted PID/exit/logs; no retry."""
        logs = self.operational / "logs" / case / stage
        logs.mkdir(parents=True, exist_ok=True)
        invocation_logs = logs / f"{len(tuple(logs.iterdir())):06}"
        operation = asyncio.create_task(
            invoke(
                argv,
                workspace,
                self.environment() if environment is None else environment,
                self.value["timeouts"][timeout],
                self.value["timeouts"]["grace"],
                invocation_logs,
            ),
        )
        try:
            while not operation.done():
                await asyncio.wait({operation}, timeout=1)
                if not operation.done():
                    try:
                        fields = (
                            load(workspace / "progress.json")
                            if (workspace / "progress.json").exists()
                            else {}
                        )
                        if not isinstance(fields, dict):
                            fields = {}
                    except (ValueError, OSError):
                        fields = {}
                    self.progress(
                        case,
                        stage,
                        "RUNNING",
                        operation_progress={
                            k: fields[k]
                            for k in ("operation", "current", "total")
                            if k in fields
                        },
                        heartbeat=True,
                    )
            result = await operation
        except BaseException:
            operation.cancel()
            await asyncio.gather(operation, return_exceptions=True)
            raise
        if stage not in {"prepare", "packet", "B", "C", "import", "D"}:
            self.progress(
                case,
                stage,
                "PROCESS_FAILED"
                if result.failed or result.stdout_truncated
                else "PROCESS_RETURNED",
                exit_code=result.exit_code,
                duration_seconds=result.duration.total_seconds,
            )
        require(
            not result.failed and not result.stdout_truncated,
            "Worker failed/timed out/truncated; no retry",
        )
        return result

    async def validate(self, name: str, workspace: Path, case: str, stage: str) -> Any:
        """Run the frozen deterministic validator, never a semantic reviewer."""
        result = await self.process(
            self.arguments(name, workspace, case, stage),
            workspace,
            case,
            stage + "-validate",
            "validation",
        )
        receipt = json.loads(result.stdout.decode().splitlines()[-1])
        require(receipt["status"] == "PASS", "Validator rejected candidate")
        return receipt

    async def worker(
        self,
        case: Any,
        stage: str,
        inputs: dict[str, bytes],
    ) -> Any:
        """Contain pre-entry failures while letting entered independent siblings finish."""
        try:
            return await self._worker(case, stage, inputs)
        except (ValueError, OSError, KeyError) as error:
            self.blocked = True
            self.progress(
                case.identity,
                stage,
                "BLOCKED_BEFORE_ENTRY",
                error=str(error),
            )
            return None

    async def _worker(
        self,
        case: Any,
        stage: str,
        inputs: dict[str, bytes],
    ) -> Any:
        """Claim once, preserve failed identities, and quarantine surviving siblings."""
        case_id = case.identity
        returned = self.journal(case_id, stage, "RETURNED")
        if returned.exists():
            receipt = load(returned)
            require(
                receipt["run_id"] == self.run_id
                and receipt["case"] == case_id
                and receipt["stage"] == stage
                and receipt["frame"] == case.frame
                and receipt["inputs_sha256"]
                == digest(json_bytes({n: digest(v) for n, v in inputs.items()})),
                "Completed receipt input identity differs",
            )
            files = self.completed_files(receipt)
            if stage == "C":
                if Path(receipt["workspace"]).exists():
                    preserve_packet(Path(receipt["workspace"]), inputs)
                semantic_receipt(receipt["validation"], self.value["semantic"])
                semantic_outputs(files)
            self.progress(case_id, stage, StageState.COMPLETE, resumed=True)
            return receipt, files
        require(
            not self.journal(case_id, stage, "ENTERED").exists(),
            "Entered/unreturned attempt dead; resume refused",
        )
        self.progress(case_id, stage, StageState.QUEUED)
        semaphore = self.branch_slots.get(stage, self.slots)
        async with semaphore:
            async with self.slots if semaphore is not self.slots else nullcontext():
                if self.blocked:
                    self.progress(
                        case_id,
                        stage,
                        StageState.QUEUED,
                        reason="Sibling failure; not launched",
                    )
                    return None
                root = self.stage_root(case_id, stage)
                if root.exists():
                    require(
                        {p.name for p in root.iterdir()} == set(inputs)
                        and all(
                            (root / n).read_bytes() == raw for n, raw in inputs.items()
                        ),
                        "Never-entered workspace not provably pristine",
                    )
                elif stage == "C":
                    sterile(root, inputs)
                else:
                    materialize(root, inputs)
                if stage == "C":
                    await self.validate("packet_validate", root, case_id, "C-packet")
                    config = self.value["semantic"]
                    if config["kind"] == "codex":
                        version = await self.process(
                            [codex.argv(config, root)[0], "--version"],
                            root,
                            case_id,
                            "C-version",
                            "validation",
                        )
                        require(
                            version.stdout.decode().strip()
                            == "codex-cli " + config["cli_version"],
                            "Codex CLI version differs; no reviewer entered",
                        )
                    preserve_packet(root, inputs)
                    require(
                        {p.name for p in root.iterdir()} == set(inputs),
                        "Packet validator changed sterile allowlist before reviewer entry",
                    )
                if self.blocked:
                    self.progress(
                        case_id,
                        stage,
                        "QUEUED",
                        reason="Sibling failure before scientific entry",
                    )
                    return None
                binding = {
                    "run_id": self.run_id,
                    "case": case_id,
                    "stage": stage,
                    "frame": case.frame,
                    "inputs_sha256": digest(
                        json_bytes({n: digest(v) for n, v in inputs.items()}),
                    ),
                    "workspace": str(root),
                }
                exclusive(self.journal(case_id, stage, "ENTERED"), binding)
                started = time.perf_counter()
                self.progress(case_id, stage, StageState.RUNNING)
                try:
                    if stage == "C":
                        config = self.value["semantic"]
                        if config["kind"] == "codex":
                            env = self.environment()
                            auth_root = self.stage_root(case_id, "auth")
                            materialize(
                                auth_root,
                                {"auth.json": Path(config["auth_file"]).read_bytes()}
                                if config.get("auth_file")
                                else {},
                            )
                            env["CODEX_HOME"] = str(auth_root)
                            result = await self.process(
                                codex.argv(config, root),
                                root,
                                case_id,
                                stage,
                                environment=env,
                            )
                            thread = parse_codex_turn_output(result.stdout).thread_id
                            require(
                                thread not in self.thread_ids,
                                "Reviewer conversation reused across cases",
                            )
                            self.thread_ids.add(thread)
                        else:
                            await self.process(
                                expand(
                                    config["argv"],
                                    {
                                        "workspace": str(root),
                                        "case": case_id,
                                        "frame": json.dumps(case.frame),
                                        "python": sys.executable,
                                        "repository": str(self.repository.root),
                                    },
                                ),
                                root,
                                case_id,
                                stage,
                            )
                        preserve_packet(root, inputs)
                        require(
                            all((root / n).is_file() for n in PRIMARY),
                            "Missing primary scientific artifacts",
                        )
                        validation = await self.validate(
                            "C_validate",
                            root,
                            case_id,
                            stage,
                        )
                        semantic_receipt(validation, config)
                        preserve_packet(root, inputs)
                        files = {n: (root / n).read_bytes() for n in PRIMARY}
                        semantic_outputs(files)
                        save(
                            self.operational / "archives" / (case_id + ".json"),
                            {
                                "workspace": str(root),
                                "status": "RETAINED_AFTER_TERMINATION",
                                "packet_sha256": {
                                    n: digest(v) for n, v in inputs.items()
                                },
                                "primary_sha256": {
                                    n: digest(v) for n, v in files.items()
                                },
                            },
                        )
                    else:
                        await self.process(
                            self.arguments(stage, root, case_id, stage),
                            root,
                            case_id,
                            stage,
                        )
                        validation = await self.validate(
                            stage + "_validate",
                            root,
                            case_id,
                            stage,
                        )
                        _, files = candidate(root, case_id, case.frame, stage)
                        if stage == "B":
                            require(
                                validation["mode"] == "SEALED"
                                and validation["native_archives_decoded"]
                                == validation["deep_correspondence_executions"]
                                == 0
                                and validation["completion_proof_sha256"]
                                == digest(files["completion_proof.json"]),
                                "Normal completion proof required",
                            )
                        if stage == "import":
                            require(
                                validation["semantic_transformation"] == "NONE"
                                and all(
                                    files["primary/" + n] == inputs["primary/" + n]
                                    for n in PRIMARY
                                ),
                                "Import changed primary scientific bytes",
                            )
                    receipt = {
                        **binding,
                        "files": {n: digest(raw) for n, raw in files.items()},
                        "validation": validation,
                    }
                    exclusive(returned, receipt)
                    self.progress(
                        case_id,
                        stage,
                        StageState.QUARANTINED if self.blocked else StageState.COMPLETE,
                        duration_seconds=time.perf_counter() - started,
                    )
                    return receipt, files
                except BaseException as error:
                    self.blocked = True
                    exclusive(
                        self.journal(case_id, stage, "FAILED"),
                        {
                            **binding,
                            "error": type(error).__name__,
                            "state": "DEAD; NO AUTOMATIC RETRY",
                        },
                    )
                    self.progress(
                        case_id,
                        stage,
                        StageState.DEAD,
                        duration_seconds=time.perf_counter() - started,
                        error=str(error),
                    )
                    return None

    async def input_files(self, case: Any) -> dict[str, bytes]:
        """Disclose only committed Stage A files explicitly authorized for this case."""
        specification = json.loads(case.inputs_json)
        files = {}
        for item in specification:
            raw = await self.repository.git(
                "show",
                self.value["stage_a"]["checkpoint"] + ":" + item["path"],
            )
            require(digest(raw) == item["sha256"], "Stage A case input hash differs")
            files[item["name"]] = raw
        return files

    async def checkpoint_validation(
        self,
        boundary: str,
        paths: tuple[str, ...],
    ) -> None:
        """Run focused checkpoints or final full validation under explicit policy."""
        tier = validation_tier(boundary, paths)
        commands = list(self.value["validation"][tier])
        if tier == "final":
            commands += [
                ["uv", "run", "python", "scripts/validate_development.py"],
                [
                    "uv",
                    "run",
                    "ruff",
                    "check",
                    "src",
                    "tests",
                    "experiments/orchestration",
                ],
                [
                    "uv",
                    "run",
                    "ruff",
                    "format",
                    "--check",
                    "experiments/orchestration",
                    *(
                        p
                        for p in paths
                        if p.startswith("src/devtools/") and p.endswith(".py")
                    ),
                ],
                [
                    "uv",
                    "run",
                    "mypy",
                    "src",
                    "tests",
                    "experiments/orchestration",
                    "--exclude",
                    "tests/experiments/",
                ],
            ]
        for index, argv in enumerate(commands):
            result = await self.process(
                expand(
                    argv,
                    {"repository": str(self.repository.root), "python": sys.executable},
                ),
                self.repository.root,
                "cohort",
                boundary + "-" + tier + "-" + str(index),
                "validation",
            )
            require(not result.failed, "Checkpoint validation failed")

    async def publish(self, boundary: str, results: Any) -> None:
        """Serialize candidate publication in original case order, never completion order."""
        marker = safe(self.science, "publications/" + boundary + ".json")
        if marker.exists():
            committed = await self.publication_identity(boundary)
            self._state["publications"][boundary] = committed
            return
        files = {
            boundary + "/" + case.identity + "/" + name: raw
            for case, result in zip(self.plan.cases, results, strict=True)
            for name, raw in result[1].items()
        }
        if boundary == "PACKET":
            for case in self.plan.cases:
                receipt = load(self.journal(case.identity, "prepare", "RETURNED"))
                files.update(
                    {
                        "PREPARATION/" + case.identity + "/" + n: raw
                        for n, raw in self.completed_files(receipt).items()
                    },
                )
        commit = await self.repository.commit(
            boundary,
            self.prefix,
            files,
            self.value["publication"]["subjects"][boundary],
            self.checkpoint_validation,
        )
        self._state["publications"][boundary] = commit
        self.progress("cohort", boundary + "-publication", "COMPLETE", commit=commit)

    async def run(self, *, resume: bool = False) -> dict[str, Any]:
        """Hold the exact worktree writer lease through the fixed cohort lifecycle."""
        with writer(self.repository.root):
            return await self._run(resume=resume)

    async def _run(self, *, resume: bool = False) -> dict[str, Any]:
        """Execute fixed branches, stopping all new dependent work on failure."""
        require(
            self.value["controller_implementation"] == implementation(),
            "Approved controller implementation differs",
        )
        context = self.science / "run.json"
        if resume:
            saved = load(context)
            self.approved_head = saved["approval_checkpoint"]
            expected = self.approved_head
            for boundary in ("PACKET", "B", "C", "D"):
                marker = safe(self.science, "publications/" + boundary + ".json")
                if marker.exists():
                    expected = await self.publication_identity(boundary)
            await self.repository.authenticate(expected, self.prefix)
        else:
            require(
                self.approved_head,
                "Use authenticated from_plan API before execution",
            )
            await self.repository.authenticate(self.approved_head, self.prefix)
        await self.authenticate_approved_inputs(self.approved_head)
        if resume:
            require(
                load(context)
                == {
                    "run_id": self.run_id,
                    "plan": self.value,
                    "implementation": implementation(),
                    "approval_checkpoint": self.approved_head,
                },
                "Durable run identity changed",
            )
            for failed in self.science.glob("journal/*/*/FAILED.json"):
                require(
                    not failed.exists(),
                    "Failed attempt dead; resume requires maintainer decision",
                )
        else:
            require(
                not context.exists(),
                "Run identity already exists; use explicit resume",
            )
            exclusive(
                context,
                {
                    "run_id": self.run_id,
                    "plan": self.value,
                    "implementation": implementation(),
                    "approval_checkpoint": self.approved_head,
                },
            )
        self.blocked = False
        self._state["status"] = "RUNNING"
        save(self.operational / "locator.json", {"prefix": self.prefix})
        try:
            initial_inputs = await asyncio.gather(
                *(self.input_files(case) for case in self.plan.cases),
            )
            prepared = await asyncio.gather(
                *(
                    self.prepare(case, inputs)
                    for case, inputs in zip(
                        self.plan.cases,
                        initial_inputs,
                        strict=True,
                    )
                ),
            )
            require(not self.blocked and all(prepared), "Preparation failed")
            packets = await asyncio.gather(
                *(
                    self.worker(case, "packet", p[1])
                    for case, p in zip(self.plan.cases, prepared, strict=True)
                ),
            )
            require(not self.blocked and all(packets), "Packet freeze failed")
            await self.publish("PACKET", packets)
            tasks = [
                self.worker(
                    case,
                    stage,
                    prepared[i][1] if stage == "B" else packets[i][1],
                )
                for i, case in enumerate(self.plan.cases)
                for stage in ("B", "C")
            ]
            branches = await asyncio.gather(*tasks)
            if self.blocked:
                for case, stage, returned in zip(
                    (case for case in self.plan.cases for _ in ("B", "C")),
                    (stage for _ in self.plan.cases for stage in ("B", "C")),
                    branches,
                    strict=True,
                ):
                    if returned is not None:
                        self.progress(
                            case.identity,
                            stage,
                            StageState.QUARANTINED,
                            reason="Sibling failure; publication prohibited",
                        )
            require(
                not self.blocked and all(branches),
                "Scientific worker failure; surviving results quarantined; Stage D blocked",
            )
            treatment = branches[0::2]
            semantic = branches[1::2]
            await self.publish("B", treatment)
            imports = await asyncio.gather(
                *(
                    self.worker(
                        case,
                        "import",
                        {
                            **{"primary/" + n: raw for n, raw in s[1].items()},
                            **{"packet/" + n: raw for n, raw in p[1].items()},
                        },
                    )
                    for case, s, p in zip(
                        self.plan.cases,
                        semantic,
                        packets,
                        strict=True,
                    )
                ),
            )
            require(
                not self.blocked and all(imports),
                "Gold import failed; Stage D blocked",
            )
            await self.publish("C", imports)
            # One cohort analysis consumes only published/captured case bytes and commits.
            case = self.plan.cases[0]
            joined_inputs = {
                stage + "/" + c.identity + "/" + n: raw
                for stage, results in (("B", treatment), ("C", imports))
                for c, result in zip(self.plan.cases, results, strict=True)
                for n, raw in result[1].items()
            }
            result = await self.worker(case, "D", joined_inputs)
            require(result is not None and not self.blocked, "Stage D failed")
            # Cohort artifacts use one owner, not synthetic duplicate case results.
            marker = safe(self.science, "publications/D.json")
            if not marker.exists():
                commit = await self.repository.commit(
                    "D",
                    self.prefix,
                    {
                        **{"D/" + n: raw for n, raw in result[1].items()},
                        "D/controller_summary.json": json_bytes(self.final_summary()),
                    },
                    self.value["publication"]["subjects"]["D"],
                    self.checkpoint_validation,
                )
                self._state["publications"]["D"] = commit
            else:
                self._state["publications"]["D"] = await self.publication_identity("D")
            self._state["status"] = "COMPLETE; MAINTAINER_REVIEW_READY"
        except (ValueError, OSError, KeyError) as error:
            self._state["status"] = "BLOCKED; MAINTAINER_DECISION_REQUIRED"
            self._state["failure_boundary"] = str(error)
        self.progress("cohort", "run", self._state["status"])
        return self.state

    def final_summary(self) -> dict[str, Any]:
        """Bind deterministic final identities without operational timestamps."""
        return {
            "run_id": self.run_id,
            "controller_implementation": implementation(),
            "approval_checkpoint": self.approved_head,
            "scientific_retry_count": 0,
            "case_order": [c.identity for c in self.plan.cases],
            "operation_hashes": {
                p.relative_to(self.science).as_posix(): digest(binary(p))
                for p in sorted(self.science.glob("journal/*/*/RETURNED.json"))
            },
            "prior_publications": dict(self._state["publications"]),
            "human_boundary": "MAINTAINER_RESULT_REVIEW",
        }

    async def publication_identity(self, boundary: str) -> str:
        """Require a committed receipt and exact committed artifact bytes."""
        marker = safe(self.science, "publications/" + boundary + ".json")
        address = marker.relative_to(self.repository.root).as_posix()
        commit = (
            (await self.repository.git("log", "-1", "--format=%H", "--", address))
            .decode()
            .strip()
        )
        require(commit, "Uncommitted publication ambiguous; resume refused")
        raw = await self.repository.git("show", commit + ":" + address)
        require(
            raw == binary(marker),
            "Publication receipt differs from committed bytes",
        )
        receipt = json.loads(raw)
        require(
            receipt["boundary"] == boundary
            and (await self.repository.git("rev-parse", commit + "^")).decode().strip()
            == receipt["parent_head"],
            "Publication parent identity differs",
        )
        for name, sha in json.loads(raw)["sha256"].items():
            artifact = safe(self.science, name)
            committed = await self.repository.git(
                "show",
                commit + ":" + artifact.relative_to(self.repository.root).as_posix(),
            )
            require(
                digest(committed) == sha and binary(artifact) == committed,
                "Published artifact changed",
            )
        return commit

    async def verify(self) -> dict[str, Any]:
        """Verify committed scientific boundaries, never .local handoff authority."""
        result = self.status()
        await self.repository.git("diff", "--exit-code", "HEAD", "--", self.prefix)
        for boundary in result["publications"]:
            await self.publication_identity(boundary)
        for case in self.plan.cases:
            for stage in ("prepare", "packet", "B", "C", "import"):
                path = self.journal(case.identity, stage, "RETURNED")
                if path.exists():
                    receipt = load(path)
                    require(
                        receipt["case"] == case.identity
                        and receipt["frame"] == case.frame
                        and receipt["stage"] == stage
                        and receipt["run_id"] == self.run_id,
                        "Operation receipt identity differs",
                    )
        if "D" in result["publications"]:
            summary = load(self.science / "D/controller_summary.json")
            require(
                summary["operation_hashes"]
                == {
                    p.relative_to(self.science).as_posix(): digest(binary(p))
                    for p in sorted(self.science.glob("journal/*/*/RETURNED.json"))
                },
                "Final operation journal integrity differs",
            )
            result["status"] = "COMPLETE; MAINTAINER_REVIEW_READY"
        result["verification"] = "PASS"
        return result

    async def prepare(self, case: Any, inputs: dict[str, bytes]) -> Any:
        """Reuse pure immutable preparation only after fresh exact adapter validation."""
        config = self.value["cache"]
        if (
            not config["enabled"]
            or self.journal(case.identity, "prepare", "ENTERED").exists()
        ):
            return await self.worker(case, "prepare", inputs)
        binding = {
            "schema": "immutable-preparation-v1",
            "parent_tree": case.frame["parent_tree"],
            "repository_id": case.frame["repository_id"],
            "observation_semantics": config["observation_semantics"],
            "implementation": self.value["implementation"],
            "configuration": {
                "inputs": {n: digest(v) for n, v in inputs.items()},
                "frame": case.frame,
                "parameters": config["configuration"],
            },
            "surfaces": config["surfaces"],
        }
        started = time.perf_counter()
        status, files = self.cache.get(binding)
        root = self.stage_root(case.identity, "prepare")
        if files is not None:
            try:
                require(
                    not (set(inputs) & set(files)),
                    "Cache overlaps immutable input ownership",
                )
                materialize(root, {**inputs, **files})
                save(
                    root / "candidate.json",
                    {
                        "schema": "experiment-candidate-v1",
                        "case": case.identity,
                        "frame": case.frame,
                        "stage": "prepare",
                        "files": {n: digest(raw) for n, raw in files.items()},
                    },
                )
                async with self.slots:
                    validation = await self.validate(
                        "prepare_validate",
                        root,
                        case.identity,
                        "prepare",
                    )
                receipt = {
                    "run_id": self.run_id,
                    "case": case.identity,
                    "stage": "prepare",
                    "frame": case.frame,
                    "inputs_sha256": digest(
                        json_bytes({n: digest(v) for n, v in inputs.items()}),
                    ),
                    "workspace": str(root),
                    "files": {n: digest(v) for n, v in files.items()},
                    "validation": validation,
                    "cache_binding": binding,
                }
                exclusive(
                    self.journal(case.identity, "prepare", "ENTERED"),
                    {
                        k: v
                        for k, v in receipt.items()
                        if k not in {"files", "validation"}
                    },
                )
                exclusive(self.journal(case.identity, "prepare", "RETURNED"), receipt)
                self.progress(
                    case.identity,
                    "prepare",
                    "COMPLETE",
                    cache_status=status,
                    cache_key=self.cache.key(binding),
                    bytes=sum(map(len, files.values())),
                    elapsed_seconds=time.perf_counter() - started,
                    producing_implementation=binding["implementation"],
                )
                return receipt, files
            except (ValueError, OSError, KeyError):
                status = "CACHE_REJECTED"
                if root.exists():
                    backup = self.stage_root(case.identity, "prepare-cache-rejected")
                    require(not backup.exists(), "Cache rejection staging conflict")
                    root.rename(backup)
        self.progress(
            case.identity,
            "prepare",
            status,
            cache_key=self.cache.key(binding),
        )
        result = await self.worker(case, "prepare", inputs)
        if result:
            try:
                self.cache.put(binding, result[1])
            except (ValueError, OSError) as error:
                self.progress(
                    case.identity,
                    "cache-write",
                    "CACHE_REJECTED",
                    error=str(error),
                )
            self.progress(
                case.identity,
                "prepare",
                "COMPLETE",
                cache_status="RECOMPUTED",
                prior_cache_status=status,
                cache_key=self.cache.key(binding),
                bytes=sum(map(len, result[1].values())),
                elapsed_seconds=time.perf_counter() - started,
                producing_implementation=binding["implementation"],
            )
        return result

    def status(self) -> dict[str, Any]:
        """Reconstruct from immutable scientific receipts, not mutable .local authority."""
        require(
            load(self.science / "run.json")["run_id"] == self.run_id,
            "Run identity missing",
        )
        result: dict[str, Any] = {
            "run_id": self.run_id,
            "stages": {},
            "publications": {},
        }
        for receipt in self.science.glob("journal/*/*/ENTERED.json"):
            value = load(receipt)
            returned = receipt.with_name("RETURNED.json")
            failed = receipt.with_name("FAILED.json")
            state = (
                "DEAD"
                if failed.exists()
                else "COMPLETE"
                if returned.exists()
                else "ENTERED; RECOVERY_REQUIRES_PROOF"
            )
            if returned.exists():
                completed = load(returned)
                self.completed_files(completed)
            result["stages"][value["case"] + "/" + value["stage"]] = state
        for receipt in (self.science / "publications").glob("*.json"):
            result["publications"][receipt.stem] = load(receipt)
        result["status"] = (
            "COMPLETE_CANDIDATE; COMMITTED_VERIFICATION_REQUIRED"
            if "D" in result["publications"]
            else "BLOCKED"
            if any(v.startswith("DEAD") for v in result["stages"].values())
            else "ACTIVE_OR_INTERRUPTED; SEE_OPERATIONAL_HEARTBEAT"
            if any(v.startswith("ENTERED") for v in result["stages"].values())
            else "INCOMPLETE; SAFE_QUEUED_WORK_MAY_RESUME"
        )
        try:
            if (self.operational / "state.json").exists():
                result["operational_non_authoritative"] = load(
                    self.operational / "state.json",
                )
                if (self.operational / "progress.json").exists():
                    result["latest_progress_non_authoritative"] = load(
                        self.operational / "progress.json",
                    )
        except (ValueError, OSError):
            result["operational_non_authoritative"] = "UNAVAILABLE_OR_CORRUPT"
        return result

    def completed_files(self, receipt: Any) -> dict[str, bytes]:
        """Use published bytes after a checkpoint; staging is never permanent authority."""
        stage, case = receipt["stage"], receipt["case"]
        boundary, address = {
            "prepare": ("PACKET", "PREPARATION/" + case),
            "packet": ("PACKET", "PACKET/" + case),
            "B": ("B", "B/" + case),
            "C": ("C", "C/" + case + "/primary"),
            "import": ("C", "C/" + case),
            "D": ("D", "D"),
        }[stage]
        marker = self.science / "publications" / (boundary + ".json")
        root = Path(receipt["workspace"])
        require(receipt["files"], "Completed scientific output list missing")
        if marker.exists():
            prefix = address + "/"
            published = {
                n[len(prefix) :]: sha
                for n, sha in load(marker)["sha256"].items()
                if n.startswith(prefix)
            }
            if stage == "D":
                published.pop("controller_summary.json", None)
            require(
                published == receipt["files"],
                "Completed receipt/published output set differs",
            )
            root = safe(self.science, address)
        return bundle(root, receipt["files"])
