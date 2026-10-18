# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, TRY301, PLR2004, T201 -- bounded consumer composition
"""Concrete Markdown coding worker: retrieved Context, proposal, tests and repair.

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
from experiments.qwen.development_task import (
    ACCEPTANCE,
    SOURCE,
    TESTS,
    _hash,
    _save,
    _structured_edit_definition,
    _structured_edit_patch_from_calls,
    _timed_command,
    apply_markdown_patch,
)
from experiments.qwen.patch_proposal_worker import PatchProposalError, _read_text

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.retrieval.source import SourceSearchMode
    from devtools.models.interaction import ModelInteraction


TASK = (
    "Repair Markdown fence closing: a matching closing fence followed by "
    "non-whitespace text must not prematurely expose fenced headings. Preserve "
    "backtick/tilde markers, longer closers, trailing spaces/tabs, minimum length, "
    "public APIs and unrelated behavior. Only edit " + SOURCE + ". "
    "Use exactly one native propose_edit call for a contiguous replacement. "
    "The host applies and tests it; you have no write, shell or Git authority. "
    "Do not claim to have run tests. Context below is the CURRENT source state, "
    "not the original state. If tests fail, revise that current state using the "
    "correlated host feedback. At most three proposals are permitted."
)
BASELINE_HASHES = {
    SOURCE: "b01a8fdac51f3d5485275898b45d43cd643efac736b1e275b8a18fc205fd6195",
    TESTS: "92e5f321000054d18f30775387b24f65a1b2635fb02e15e2ea01643abdb4b7a9",
}
ORACLE_HASH = "373b20627f04d364b5624abbab4699e560d464b96993e9fa28097cc11e0be12b"


def acquire_context(
    root: Path, repository: Repository, *, mode: SourceSearchMode = "symbol"
) -> tuple[str, list[dict[str, Any]]]:
    """Search the two explicitly admitted resources and disclose exact expansions.

    The source's module constants and imports are required surrounding Context;
    expand a ranked symbol to its file. Tests are a separately selected file.
    No repository-wide disclosure or automatic sufficiency claim is made.
    """
    addresses = tuple(RepositoryResourceAddress(path) for path in (SOURCE, TESTS))
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
    for path, query, view in (
        (SOURCE, "MarkdownFile fence headings", mode),
        (TESTS, "markdown headings fenced code", "file"),
    ):
        result = search_repository_source(
            index, query=query, mode=view, maximum_results=100
        )
        hit = next(
            (hit for hit in result.hits if hit.unit.resource.address.value == path),
            None,
        )
        if hit is None:
            raise ValueError("Required task resource not retrieved: " + path)
        unit = index.expand(hit.unit, to="file")
        choices.append(SourceSearchDisclosureOption(TASK, unit))
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
    plan = plan_disclosures(purpose=TASK, snapshot=snapshot, disclosures=tuple(choices))
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


def _prepare_workspace(root: Path, folder: Path) -> Path:
    """Copy supported source and focused tests, never Git or scientific evidence."""
    for path, digest in BASELINE_HASHES.items():
        if _hash(root / path) != digest:
            raise ValueError("Frozen task baseline changed: " + path)
    if hashlib.sha256(ACCEPTANCE.encode()).hexdigest() != ORACLE_HASH:
        raise ValueError("Frozen oracle changed")
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
    target = workspace / TESTS
    target.parent.mkdir(parents=True)
    shutil.copyfile(root / TESTS, target)
    # No inherited pytest configuration, parent conftest, or editable-install
    # imports. The exact local source is asserted before either validation.
    prelude = (
        "import sys\nfrom pathlib import Path\n"
        f"sys.path.insert(0, {str(workspace / 'src')!r})\n"
        "import devtools.resources.filesystem.models.markdown.file as module\n"
        f"assert Path(module.__file__).resolve() == Path({str(workspace / SOURCE)!r})\n"
    )
    write(TextFile(resolve_path(folder / "oracle-runner.py"), prelude + ACCEPTANCE))
    test_arguments = [
        str(target),
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
            + (f"import pytest\nraise SystemExit(pytest.main({test_arguments!r}))\n"),
        )
    )
    write(TextFile(resolve_path(workspace / "pytest.ini"), "[pytest]\n"))
    return workspace


async def _turns(
    workspace: Path,
    folder: Path,
    interaction: ModelInteraction,
    report: dict[str, Any],
    *,
    maximum_calls: int,
) -> None:
    repository = Repository.new()
    feedback: dict[str, Any] = {"disposition": "INITIAL_PROPOSAL"}
    for number in range(1, maximum_calls + 1):
        turn = folder / f"turn-{number:02d}"
        turn.mkdir()
        context, resources = acquire_context(workspace, repository)
        prompt = TASK + "\nHOST FEEDBACK:\n" + json.dumps(feedback) + "\n" + context
        if len(prompt.encode()) > 60000:
            raise ValueError("Bounded Context byte allowance exceeded")
        request = ModelRequest(
            prompt=Prompt(prompt, role="user"),
            settings=ModelSettings(maximum_output_tokens=4096, thinking_enabled=False),
            tools=(_structured_edit_definition(),),
        )
        source_hash = _hash(workspace / SOURCE)
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
        async with asyncio.timeout(300):
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
        if _hash(workspace / SOURCE) != source_hash:
            raise PatchProposalError("Source changed while proposal pending")
        call, patch, updated = _structured_edit_patch_from_calls(
            workspace,
            _read_text(resolve_path(workspace / SOURCE)).content,
            response.tool_calls,
        )
        stage["proposal_valid"] = True
        stage["proposal_id"] = call.provider_call_id
        stage["phase"] = "PATCH_APPLICATION"
        _save(turn / "stage.json", stage, overwrite=True)
        await apply_markdown_patch(workspace, turn, patch)
        if _read_text(resolve_path(workspace / SOURCE)).content != updated:
            raise PatchProposalError("Applied source differs from admitted proposal")
        stage["source_after"] = _hash(workspace / SOURCE)
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
            "validation": {
                key: {field: value[field][-6000:] for field in ("stdout", "stderr")}
                for key, value in validation.items()
                if key != "accepted"
            },
        }
    report["disposition"] = "REPAIR_BUDGET_EXHAUSTED"


async def run_coding_task(  # noqa: C901 -- bounded task stages and conservative cleanup
    root: Path,
    folder: Path,
    interaction: ModelInteraction,
    *,
    maximum_calls: int = 3,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run one bounded engineering task; preserve evidence and discard all edits.

    The caller must obtain local execution authorization before providing a live
    interaction. Reusing an output directory is refused before any invocation.
    """
    if not 1 <= maximum_calls <= 3:
        raise ValueError("Model call bound must be between one and three")
    folder = resolve_path(folder).value
    folder.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    report: dict[str, Any] = {
        "schema": "qwen-markdown-coding-loop-v1",
        "started_at": str(Timestamp.now()),
        "accepted": False,
        "disposition": "PREPARING",
        "turns": [],
        "limits": {
            "model_calls": maximum_calls,
            "output_tokens": 4096,
            "wall_seconds": 900,
            "per_call_seconds": 300,
        },
        "baseline": BASELINE_HASHES,
        "oracle_sha256": ORACLE_HASH,
        "coordination_usage": "UNKNOWN",
        "provenance": provenance,
    }
    workspace: Path | None = None
    try:
        async with asyncio.timeout(900):
            workspace = _prepare_workspace(root, folder)
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
                    "task": TASK,
                    "tool": asdict(_structured_edit_definition()),
                    "settings": asdict(ModelSettings(4096, thinking_enabled=False)),
                },
            )
            await _turns(
                workspace, folder, interaction, report, maximum_calls=maximum_calls
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
            if (workspace / SOURCE).exists():
                current = _read_text(resolve_path(workspace / SOURCE))
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
                _hash(root / path) == digest for path, digest in BASELINE_HASHES.items()
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
