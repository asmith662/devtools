# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, TRY301, PLR2004, T201 -- bounded consumer composition
"""Bounded configured coding worker: retrieved Context, proposal, tests and repair.

This consumer is deliberately task-local. It exposes no commands or mutations to
the model and does not implement provider conversation or general Agent state.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import shutil
import sys
import time
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from apps.qwen.development_task import (
    _command,
    _hash,
    _save,
    _structured_edit_definition,
    _structured_edit_patch_from_calls,
    _timed_command,
    apply_markdown_patch,
)
from apps.qwen.patch_proposal_worker import PatchProposalError, _read_text
from apps.qwen.tasks import MARKDOWN, CodingTask
from devtools.context import (
    Repository,
    RepositoryResourceAddress,
    materialize_disclosure_plan,
    observe_repository_resources,
    plan_disclosures,
    render_context_disclosure,
)
from devtools.context.planning import SourceSearchDisclosureOption
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.retrieval import (
    build_source_search_index,
    search_repository_source,
)
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.models.interaction import (
    ModelRequest,
    ModelSettings,
    ModelTermination,
    Prompt,
)
from devtools.resources.filesystem import TextFile, write

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.retrieval.source import SourceSearchMode
    from devtools.models.interaction import ModelInteraction


def _validation_feedback(validation: dict[str, Any]) -> dict[str, Any]:
    """Project bounded diagnostics; complete original command logs stay in evidence."""
    projected = {}
    for name in ("oracle", "tests"):
        result = validation[name]
        failures = [
            json.loads(line.removeprefix("QWEN_TEST_FAILURE "))
            for line in result["stderr"].splitlines()
            if line.startswith("QWEN_TEST_FAILURE ")
        ]
        details = {}
        for field in ("stdout", "stderr"):
            text = result[field]
            details[field] = (
                text
                if len(text) <= 2000
                else text[:1000] + "\n[TRUNCATED]\n" + text[-1000:]
            )
            details[field + "_truncated"] = len(text) > 2000
        projected[name] = {
            "exit_code": result["exit_code"],
            "primary_failures": failures[:8],
            "primary_failures_truncated": len(failures) > 8,
            "reporting_failure": "INTERNALERROR" in result["stdout"]
            or "_pytest/" in result["stderr"].replace("\\", "/"),
            **details,
        }
    return projected


def acquire_context(
    root: Path,
    repository: Repository,
    *,
    task: CodingTask = MARKDOWN,
    mode: SourceSearchMode | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    """Search the two explicitly admitted resources and disclose exact expansions.

    The source's module constants and imports are required surrounding Context;
    expand a ranked symbol to its file. Tests are a separately selected file.
    No repository-wide disclosure or automatic sufficiency claim is made.
    """
    addresses = tuple(
        RepositoryResourceAddress(path) for path in (task.source, *task.tests)
    )
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=resolve_path(root),
        maximum_resource_count=5000,
        maximum_traversal_entry_count=10000,
    )
    snapshot = observe_repository_resources(
        repository=repository,
        root=resolve_path(root),
        addresses=addresses,
        maximum_resource_bytes=32768,
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=addresses,
        ),
        snapshot=snapshot,
    )
    index = build_source_search_index(
        snapshot, corpus=corpus, window_lines=40, overlap_lines=10
    )
    choices = []
    details = []
    for path, query, configured_view, expansion in task.context:
        view = mode if path == task.source and mode is not None else configured_view
        result = search_repository_source(
            index, query=query, mode=view, maximum_results=100
        )
        hit = next(
            (hit for hit in result.hits if hit.unit.resource.address.value == path),
            None,
        )
        if hit is None:
            raise ValueError("Required task resource not retrieved: " + path)
        unit = hit.unit if expansion == "none" else index.expand(hit.unit, to=expansion)
        choices.append(SourceSearchDisclosureOption(task.prompt, unit))
        details.append(
            {
                "path": path,
                "query": query,
                "mode": view,
                "selected_kind": hit.unit.kind,
                "selected_unit": str(hit.unit.id),
                "qualified_name": hit.unit.qualified_name,
                "selected_span": [hit.unit.start, hit.unit.end],
                "rank": hit.rank,
                "materialized_kind": unit.kind,
                "unit": str(unit.id),
                "repository": str(unit.repository_id),
                "snapshot": str(snapshot.id),
                "content_identity": str(unit.resource.content_identity),
                "span": [unit.start, unit.end],
                "bytes": len(unit.text.encode()),
                "tokens": None,
            }
        )
    plan = plan_disclosures(
        purpose=task.prompt, snapshot=snapshot, disclosures=tuple(choices)
    )
    return render_context_disclosure(
        materialize_disclosure_plan(
            plan=plan,
            snapshot=snapshot,
        )
    ).text, details


async def validate_workspace(root: Path, folder: Path) -> dict[str, Any]:
    """Execute only host-selected commands with the isolated source on sys.path."""
    oracle = await _timed_command(
        root,
        sys.executable,
        "-I",
        "-B",
        str(folder / "oracle-runner.py"),
    )
    tests = await _timed_command(
        root,
        sys.executable,
        "-I",
        "-B",
        str(folder / "tests-runner.py"),
    )
    return {
        "oracle": oracle,
        "tests": tests,
        "accepted": not oracle["failed"] and not tests["failed"],
    }


async def _authenticate_inputs(root: Path, workspace: Path, task: CodingTask) -> None:
    """Restore only configured immutable inputs when maintained source moved on.

    Git text normalization is reversed only when the resulting LF or CRLF bytes
    match the frozen digest. This never writes into the caller's checkout.
    """
    for path, digest in task.baseline_hashes:
        target = workspace / path
        result = await _command(
            root, "git", "show", task.baseline_revision + ":" + path
        )
        if result["failed"]:
            raise ValueError("Cannot authenticate frozen baseline: " + path)
        text = result["stdout"].replace("\r\n", "\n")
        candidates = (text, text.replace("\n", "\r\n"))
        matched = next(
            (
                value
                for value in candidates
                if hashlib.sha256(value.encode()).hexdigest() == digest
            ),
            None,
        )
        if matched is None:
            raise ValueError("Frozen baseline identity mismatch: " + path)
        if _hash(target) != digest:
            write(TextFile(resolve_path(target), matched))
        if _hash(target) != digest:
            raise ValueError("Materialized baseline identity mismatch: " + path)


def _prepare_workspace(root: Path, folder: Path, task: CodingTask = MARKDOWN) -> Path:
    """Copy supported source and focused tests, never Git or scientific evidence."""
    workspace = folder / "workspace"
    workspace.mkdir()
    shutil.copytree(
        root / "src",
        workspace / "src",
        ignore=shutil.ignore_patterns(
            "__pycache__",
            "*.pyc",
        ),
    )
    for test in task.tests:
        target = workspace / test
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / test, target)
    # No inherited pytest configuration, parent conftest, or editable-install
    # imports. The exact local source is asserted before either validation.
    module_name = task.source.removeprefix("src/").removesuffix(".py").replace("/", ".")
    prelude = (
        "import sys\nfrom pathlib import Path\n"
        f"sys.path.insert(0, {str(workspace / 'src')!r})\n"
        f"import {module_name} as module\n"
        "assert Path(module.__file__).resolve() == "
        f"Path({str(workspace / task.source)!r})\n"
    )
    write(TextFile(resolve_path(folder / "oracle-runner.py"), prelude + task.oracle))
    test_arguments = [
        *(str(workspace / test) for test in task.tests),
        "-c",
        str(workspace / "pytest.ini"),
        f"--confcutdir={workspace}",
        "--no-cov",
        "-q",
    ]
    write(
        TextFile(
            resolve_path(folder / "tests-runner.py"),
            prelude
            + "import json\nimport pytest\n"
            # Capture primary facts before pytest's traceback formatting. Some
            # tests deliberately forbid ast.parse, which formatters also use.
            + "class PrimaryFailures:\n"
            + "    @pytest.hookimpl(hookwrapper=True, tryfirst=True)\n"
            + "    def pytest_runtest_makereport(self, item, call):\n"
            + "        if call.excinfo is not None:\n"
            + "            facts = dict(nodeid=item.nodeid, phase=call.when, "
            + "exception=call.excinfo.type.__name__, "
            + "message=str(call.excinfo.value)[:1000], "
            + "message_truncated=len(str(call.excinfo.value)) > 1000)\n"
            + "            print('QWEN_TEST_FAILURE ' + json.dumps(facts), "
            + "file=sys.stderr, flush=True)\n"
            + "        yield\n"
            + f"arguments = {test_arguments!r}\n"
            + "raise SystemExit(pytest.main(arguments, plugins=[PrimaryFailures()]))\n",
        )
    )
    write(TextFile(resolve_path(workspace / "pytest.ini"), "[pytest]\n"))
    return workspace


async def _turns(  # noqa: PLR0913 -- existing loop collaborators plus task configuration
    workspace: Path,
    folder: Path,
    interaction: ModelInteraction,
    report: dict[str, Any],
    *,
    maximum_calls: int,
    task: CodingTask,
) -> None:
    repository = Repository.new()
    feedback: dict[str, Any] = {"disposition": "INITIAL_PROPOSAL"}
    for number in range(1, maximum_calls + 1):
        turn = folder / f"turn-{number:02d}"
        turn.mkdir()
        context, resources = acquire_context(workspace, repository, task=task)
        prompt = (
            task.prompt + "\nHOST FEEDBACK:\n" + json.dumps(feedback) + "\n" + context
        )
        if len(prompt.encode()) > 60000:
            raise ValueError("Bounded Context byte allowance exceeded")
        request = ModelRequest(
            prompt=Prompt(prompt, role="user"),
            settings=ModelSettings(
                maximum_output_tokens=task.output_tokens, thinking_enabled=False
            ),
            tools=(_structured_edit_definition(source_path=task.source),),
        )
        source_hash = _hash(workspace / task.source)
        stage: dict[str, Any] = {
            "number": number,
            "started_at": str(Timestamp.now()),
            "started_monotonic": time.perf_counter(),
            "source_before": source_hash,
            "context": resources,
            "prompt_bytes": len(prompt.encode()),
            "context_bytes": len(context.encode()),
            "disposition": "DISPATCH_ATTEMPTED",
            "phase": "MODEL_REQUEST",
        }
        report["turns"].append(stage)
        _save(turn / "request.json", asdict(request))
        _save(turn / "stage.json", stage)
        print(
            f"{stage['started_at']} turn {number}/{maximum_calls}: model request; "
            f"Context {stage['context_bytes']} bytes",
            flush=True,
        )
        started = time.perf_counter()
        # No repeat after provider failure, unknown completion, or malformed call.
        async with asyncio.timeout(task.call_seconds):
            response = await interaction.send(request)
        stage.update(
            model_seconds=time.perf_counter() - started,
            usage=asdict(response.usage) if response.usage else None,
            termination=response.termination,
            tool_calls=len(response.tool_calls),
            context_utilization=(
                response.usage.input_tokens / 32768
                if response.usage and response.usage.input_tokens is not None
                else None
            ),
            phase="PROPOSAL_ADMISSION",
        )
        _save(turn / "response.json", asdict(response))
        if response.termination == ModelTermination.OUTPUT_LIMIT:
            raise PatchProposalError("Output limit: no repair dispatch")
        if _hash(workspace / task.source) != source_hash:
            raise PatchProposalError("Source changed while proposal pending")
        call, patch, updated = _structured_edit_patch_from_calls(
            workspace,
            _read_text(resolve_path(workspace / task.source)).content,
            response.tool_calls,
            source_path=task.source,
        )
        stage["proposal_valid"] = True
        stage["proposal_id"] = call.provider_call_id
        stage["phase"] = "PATCH_APPLICATION"
        _save(turn / "stage.json", stage, overwrite=True)
        await apply_markdown_patch(workspace, turn, patch, source_path=task.source)
        if _read_text(resolve_path(workspace / task.source)).content != updated:
            raise PatchProposalError("Applied source differs from admitted proposal")
        stage["source_after"] = _hash(workspace / task.source)
        stage["phase"] = "VALIDATION"
        _save(turn / "stage.json", stage, overwrite=True)
        print(
            f"{Timestamp.now()} turn {number}: edit admitted; focused validation",
            flush=True,
        )
        validation = await validate_workspace(workspace, folder)
        stage.update(
            validation=validation,
            elapsed_seconds=time.perf_counter() - started,
            finished_at=str(Timestamp.now()),
            disposition=("ACCEPTED" if validation["accepted"] else "TESTS_FAILED"),
        )
        _save(turn / "stage.json", stage, overwrite=True)
        print(
            f"{stage['finished_at']} turn {number}: {stage['disposition']}; "
            f"elapsed {stage['elapsed_seconds']:.2f}s",
            flush=True,
        )
        if validation["accepted"]:
            report.update(accepted=True, disposition="ACCEPTED")
            return
        # One latest state, not an ever-growing transcript; full assistant output
        # remains in response.json, with its useful content correlated here.
        feedback = {
            "turn": number,
            "proposal_id": call.provider_call_id,
            "proposal": asdict(call),
            "assistant_content": response.content[:4096],
            "source_after": stage["source_after"],
            "disposition": "EDIT_RETAINED_IN_ISOLATED_WORKSPACE; REVISE_CURRENT_SOURCE",
            "validation": _validation_feedback(validation),
        }
    report["disposition"] = "REPAIR_BUDGET_EXHAUSTED"


async def run_coding_task(  # noqa: C901, PLR0913 -- bounded stages and task configuration
    root: Path,
    folder: Path,
    interaction: ModelInteraction,
    *,
    maximum_calls: int | None = None,
    task: CodingTask = MARKDOWN,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run one bounded engineering task; preserve evidence and discard all edits.

    The caller must obtain local execution authorization before providing a live
    interaction. Reusing an output directory is refused before any invocation.
    """
    maximum_calls = task.maximum_calls if maximum_calls is None else maximum_calls
    if not 1 <= maximum_calls <= task.maximum_calls:
        raise ValueError("Model call bound must be between one and three")
    original_hashes = {path: _hash(root / path) for path, _ in task.baseline_hashes}
    folder = resolve_path(folder).value
    folder.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    report: dict[str, Any] = {
        "schema": "qwen-coding-loop-v2",
        "started_at": str(Timestamp.now()),
        "accepted": False,
        "disposition": "PREPARING",
        "turns": [],
        "limits": {
            "model_calls": maximum_calls,
            "output_tokens": task.output_tokens,
            "wall_seconds": task.wall_seconds,
            "per_call_seconds": task.call_seconds,
        },
        "task_name": task.name,
        "task_definition": asdict(task),
        "task_definition_sha256": task.definition_sha256,
        "baseline": dict(task.baseline_hashes),
        "oracle_sha256": task.oracle_sha256,
        "coordination_usage": "UNKNOWN",
        "provenance": provenance,
    }
    workspace: Path | None = None
    try:
        async with asyncio.timeout(task.wall_seconds):
            workspace = _prepare_workspace(root, folder, task)
            await _authenticate_inputs(root, workspace, task)
            report["baseline_validation"] = await validate_workspace(workspace, folder)
            baseline = report["baseline_validation"]
            if (
                not baseline["oracle"]["failed"]
                or baseline["tests"]["failed"]
                or "AssertionError" not in baseline["oracle"]["stderr"]
            ):
                raise ValueError("Baseline must pass existing tests and fail oracle")
            _save(
                folder / "freeze.json",
                {
                    **report,
                    "task": task.prompt,
                    "tool": asdict(
                        _structured_edit_definition(source_path=task.source)
                    ),
                    "settings": asdict(
                        ModelSettings(task.output_tokens, thinking_enabled=False)
                    ),
                },
            )
            await _turns(
                workspace,
                folder,
                interaction,
                report,
                maximum_calls=maximum_calls,
                task=task,
            )
    except TimeoutError:
        report.update(
            disposition=(
                "TIMEOUT_COMPLETION_UNKNOWN_NO_RETRY"
                if report["turns"] and report["turns"][-1]["phase"] == "MODEL_REQUEST"
                else "HOST_TIMEOUT"
            )
        )
    except Exception as error:  # noqa: BLE001 -- retain terminal failures without redispatch
        phase = report["turns"][-1]["phase"] if report["turns"] else "PREPARATION"
        report.update(
            disposition=phase + "_FAILED", error=f"{type(error).__name__}: {error}"
        )
    finally:
        workspace = folder / "workspace"
        if resolve_path(workspace).value.parent != folder:
            report.update(accepted=False, disposition="CLEANUP_RECONCILIATION_REQUIRED")
        elif workspace.exists():
            if (workspace / task.source).exists():
                current = _read_text(resolve_path(workspace / task.source))
                write(
                    TextFile(resolve_path(folder / "final-source.py"), current.content)
                )
            # Only the workspace created above, never caller or Git worktree paths.
            shutil.rmtree(workspace)
        report.update(
            finished_at=str(Timestamp.now()),
            elapsed_seconds=time.perf_counter() - started,
            workspace_removed=not (folder / "workspace").exists(),
            original_unchanged=all(
                _hash(root / path) == digest for path, digest in original_hashes.items()
            ),
        )
        for stage in report["turns"]:
            if stage["disposition"] == "DISPATCH_ATTEMPTED":
                stage.update(
                    disposition=report["disposition"],
                    finished_at=str(Timestamp.now()),
                    elapsed_seconds=time.perf_counter() - stage["started_monotonic"],
                )
                _save(
                    folder / f"turn-{stage['number']:02d}" / "stage.json",
                    stage,
                    overwrite=True,
                )
        report["repair_cycles"] = max(0, len(report["turns"]) - 1)
        report["model_calls_attempted"] = len(report["turns"])
        report["proposals_admitted"] = sum(
            bool(stage.get("proposal_valid")) for stage in report["turns"]
        )
        report["usage_totals"] = {}
        report["validation_seconds"] = sum(
            result["elapsed_seconds"]
            for validation in (
                report.get("baseline_validation", {}),
                *(stage.get("validation", {}) for stage in report["turns"]),
            )
            for key, result in validation.items()
            if key in {"oracle", "tests"}
        )
        for category in (
            "input_tokens",
            "output_tokens",
            "cached_input_tokens",
            "cache_write_tokens",
            "reasoning_tokens",
        ):
            values = [
                (stage.get("usage") or {}).get(category) for stage in report["turns"]
            ]
            report["usage_totals"][category] = (
                sum(value for value in values if value is not None)
                if values and all(value is not None for value in values)
                else None
            )
        _save(folder / "result.json", report)
    return report
