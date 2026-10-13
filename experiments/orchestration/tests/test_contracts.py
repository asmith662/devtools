# Copyright (c) 2026
# ruff: noqa: S101, D103, PLR2004, PLC0415, ANN401, PT011 -- synthetic contract fixtures
"""Adversarial controller boundaries; every process is a local test executable."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import digest
from experiments.orchestration.controller import Controller, expand
from experiments.orchestration.isolation import candidate, semantic_receipt, sterile
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import (
    binary,
    load,
    materialize,
    no_links,
    safe,
    save,
)
from experiments.orchestration.tests.test_controller import fixture


def test_literal_json_argv() -> None:
    assert expand(["{}", '{"case":"alpha"}', "{case}"], {"case": "beta"}) == [
        "{}",
        '{"case":"alpha"}',
        "beta",
    ]


@pytest.mark.parametrize(
    "address",
    [
        "../escape",
        "a/../../escape",
        "C:/other",
        "a\\other",
        ".git/config",
        "holdout/file",
        "confirmation/file",
        "reserve/file",
        "a//b",
    ],
)
def test_forbidden_addresses(tmp_path: Path, address: str) -> None:
    with pytest.raises(ValueError):
        safe(tmp_path, address)


@pytest.mark.parametrize(
    "field",
    ["repository", "other_cases", "ranks_scores", "prior_gold", "child"],
)
def test_blindness_attestation(field: str) -> None:
    keys = (
        "repository",
        "git_history",
        "parent_siblings",
        "prior_session",
        "web",
        "queries",
        "ranks_scores",
        "annotations",
        "references_treatment",
        "pairs",
        "timings",
        "graph_ppr_rrf",
        "other_cases",
        "child",
        "prior_gold",
        "confirmation_reserve",
    )
    receipt: dict[str, Any] = {
        "status": "PASS",
        "model": "primary",
        "reasoning": "high",
        "second_reviewer": False,
        "reconciliation": False,
        "host_routing_independently_verified": False,
        "blindness": dict.fromkeys(keys, False),
    }
    receipt["blindness"][field] = True
    with pytest.raises(ValueError, match="Blindness"):
        semantic_receipt(receipt, {"model": "primary", "reasoning": "high"})


@pytest.mark.parametrize(
    "fault",
    [
        "nonzero",
        "missing-output",
        "hash",
        "validator",
        "missing-primary",
        "packet-mutation",
        "blindness",
        "forbidden-output",
    ],
)
def test_scientific_failure_is_dead(tmp_path: Path, fault: str) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", fault=fault)
        result = await c.run()
        assert result["status"].startswith("BLOCKED"), result
        assert "D" not in result["publications"]
        assert not c.journal("alpha", "D", "ENTERED").exists()
        failed = list(c.science.glob("journal/*/*/FAILED.json"))
        assert failed
        assert result["automatic_scientific_retries"] == 0
        assert any(v["status"] == "QUARANTINED" for v in result["stages"].values())
        before = {p: binary(p) for p in c.science.glob("journal/*/*/ENTERED.json")}
        with pytest.raises(ValueError, match="Failed attempt dead"):
            await c.run(resume=True)
        assert before == {
            p: binary(p) for p in c.science.glob("journal/*/*/ENTERED.json")
        }

    asyncio.run(run())


@pytest.mark.parametrize("mutation", ["case", "frame", "stage", "files"])
def test_candidate_joins(tmp_path: Path, mutation: str) -> None:
    materialize(tmp_path / "workspace", {"result.json": b"{}\r\n"})
    root = tmp_path / "workspace"
    value: dict[str, Any] = {
        "schema": "experiment-candidate-v1",
        "case": "alpha",
        "frame": {"corpus": "one"},
        "stage": "B",
        "files": {"result.json": digest(b"{}\r\n")},
    }
    assert binary(root / "result.json") == b"{}\r\n"
    value[mutation] = {"result.json": "0" * 64} if mutation == "files" else "foreign"
    save(root / "candidate.json", value)
    with pytest.raises(ValueError):
        candidate(root, "alpha", {"corpus": "one"}, "B")


def test_link_rejected(tmp_path: Path) -> None:
    destination = tmp_path / "destination"
    destination.mkdir()
    link = tmp_path / "link"
    if os.name == "nt":
        import _winapi

        _winapi.CreateJunction(str(destination), str(link))
    else:
        link.symlink_to(destination, target_is_directory=True)
    with pytest.raises(ValueError, match="reparse"):
        no_links(link)
    with pytest.raises(ValueError):
        sterile(link / "child", {"README.md": b"case"})


def test_publication_serialization_and_advancement(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        repo = c.repository
        active = 0
        high_water = 0

        async def validate(_boundary: str, _paths: tuple[str, ...]) -> None:
            nonlocal active, high_water
            active += 1
            high_water = max(high_water, active)
            await asyncio.sleep(0.02)
            active -= 1

        await asyncio.gather(
            *(
                repo.commit(
                    b,
                    "published",
                    {b + ".json": b"{}\n"},
                    "Fixture " + b,
                    validate,
                )
                for b in ("first", "second")
            ),
        )
        assert high_water == 1

        async def advance(_boundary: str, _paths: tuple[str, ...]) -> None:
            await repo.git("commit", "--allow-empty", "-m", "Maintainer change")

        with pytest.raises(ValueError, match="Main changed"):
            await repo.commit(
                "third",
                "published",
                {"third.json": b"{}\n"},
                "Fixture third",
                advance,
            )
        assert (repo.root / "published/third.json").exists()

    asyncio.run(run())


def test_bounded_parallel_independent_branches(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", concurrency=3)
        original = c.process
        active: set[str] = set()
        maxima = 0
        overlap = False
        completed: list[str] = []

        async def tracked(
            argv: list[str],
            workspace: Path,
            case: str,
            stage: str,
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            nonlocal maxima, overlap
            if stage in {"B", "C"}:
                active.add(case + "/" + stage)
                maxima = max(maxima, len(active))
                overlap |= any(x.endswith("/B") for x in active) and any(
                    x.endswith("/C") for x in active
                )
            try:
                return await original(argv, workspace, case, stage, *args, **kwargs)
            finally:
                if stage in {"B", "C"}:
                    active.remove(case + "/" + stage)
                    completed.append(case + "/" + stage)

        monkeypatch.setattr(c, "process", tracked)
        result = await c.run()
        assert result["status"].startswith("COMPLETE"), result
        assert maxima == 3
        assert overlap
        assert sorted(completed) == sorted(
            c.identity + "/" + s for c in c.plan.cases for s in ("B", "C")
        )
        for case in c.plan.cases:
            croot = c.stage_root(case.identity, "C")
            for sibling in (other.identity for other in c.plan.cases if other != case):
                assert sibling.encode() not in binary(croot / "manifest.json")
            assert not (croot / ".git").exists()
        progress = [
            json.loads(line)
            for line in binary(c.operational / "progress.log").splitlines()
        ]
        assert all(
            set(row)
            >= {
                "timestamp",
                "elapsed_seconds",
                "run_id",
                "case",
                "stage",
                "worker_type",
                "completed",
                "total",
                "status",
            }
            for row in progress
        )
        assert (await c.verify())["verification"] == "PASS"
        summary = binary(c.science / "D/controller_summary.json")
        await c.run(resume=True)
        assert binary(c.science / "D/controller_summary.json") == summary

    asyncio.run(run())


def test_final_policy_once(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        calls: list[list[str]] = []

        async def record(argv: list[str], *_args: Any, **_kwargs: Any) -> Any:
            calls.append(argv)

            class Result:
                failed = False

            return Result()

        monkeypatch.setattr(c, "process", record)
        await Controller.checkpoint_validation(c, "PACKET", ("experiments/x.json",))
        assert not any("scripts/validate_development.py" in argv for argv in calls)
        await Controller.checkpoint_validation(c, "D", ())
        assert sum("scripts/validate_development.py" in argv for argv in calls) == 1

    asyncio.run(run())


def test_writer_lease(tmp_path: Path) -> None:
    from experiments.orchestration.lease import writer

    with (
        writer(tmp_path),
        pytest.raises(ValueError, match="writer lease"),
        writer(tmp_path),
    ):
        pytest.fail("Second writer acquired the lease")
    with writer(tmp_path):
        pass


def test_descendant_cleanup(tmp_path: Path) -> None:
    import sys

    from experiments.orchestration.workers.process import invoke

    async def run() -> None:
        result = await invoke(
            [sys.executable, str(Path(__file__).with_name("tree_worker.py"))],
            tmp_path,
            {
                n: os.environ[n]
                for n in ("PATH", "SystemRoot", "TEMP", "TMP")
                if n in os.environ
            },
            0.3,
            0.1,
            tmp_path / "logs",
        )
        assert result.exit_code != 0
        await asyncio.sleep(1.8)
        assert not (tmp_path / "orphan.txt").exists()
        assert load(tmp_path / "logs/exit.json")["exit_code"] != 0

    asyncio.run(run())


def test_cache_validated_hit_and_rejected_recompute(tmp_path: Path) -> None:
    from experiments.orchestration.model import RunPlan
    from experiments.orchestration.tests.test_controller import FixtureController

    async def run() -> None:
        first = await fixture(tmp_path / "repo", tmp_path / "work")
        case = first.plan.cases[0]
        inputs = await first.input_files(case)
        assert await first.prepare(case, inputs)
        value = first.plan.value
        value["attempt"] = 2
        second = FixtureController(
            first.repository,
            RunPlan.parse(value),
            first.work_root,
        )
        assert await second.prepare(case, inputs)
        assert second.state["stages"]["alpha/prepare"]["cache_status"] == "CACHE_HIT"
        assert not (second.operational / "logs/alpha/prepare").exists()
        for path in first.cache.root.glob("*.json"):
            path.write_bytes(b"broken")
        value["attempt"] = 3
        third = FixtureController(
            first.repository,
            RunPlan.parse(value),
            first.work_root,
        )
        assert await third.prepare(case, inputs)
        result = third.state["stages"]["alpha/prepare"]
        assert result["prior_cache_status"] == "CACHE_REJECTED"
        assert result["cache_status"] == "RECOMPUTED"

    asyncio.run(run())


def test_preflight_validator_cannot_leak_into_reviewer_workspace(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        c = await fixture(
            tmp_path / "repo",
            tmp_path / "work",
            fault="packet-preflight-leak",
        )
        result = await c.run()
        assert result["status"].startswith("BLOCKED")
        assert not c.journal("alpha", "C", "ENTERED").exists()
        assert "D" not in result["publications"]
        assert "sterile allowlist" in result["stages"]["alpha/C"]["error"]

    asyncio.run(run())


def test_codex_version_mismatch_before_scientific_review(tmp_path: Path) -> None:
    import sys

    from experiments.codex_dogfood.case_0009.artifacts import json_bytes
    from experiments.orchestration.tests.test_controller import FixtureController

    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        value = c.plan.value
        value["semantic"].update(
            kind="codex",
            model_id="frozen-fixture-model",
            cli_version="0.162.1",
            executable=sys.executable,
        )
        plan = RunPlan.parse(value)
        (c.repository.root / "plan.json").write_bytes(plan.canonical)
        (c.repository.root / "approval.json").write_bytes(
            json_bytes(
                {
                    "approved": True,
                    "stage_a_checkpoint": value["stage_a"]["checkpoint"],
                    "plan_sha256": digest(plan.canonical),
                },
            ),
        )
        await c.repository.git("add", "plan.json", "approval.json")
        await c.repository.git("commit", "-m", "Approve version preflight fixture")
        c = await FixtureController.from_plan(
            c.repository.root,
            "plan.json",
            c.work_root,
        )
        result = await c.run()
        assert result["status"].startswith("BLOCKED")
        assert not list(c.science.glob("journal/*/C/ENTERED.json"))
        assert any(
            "CLI version differs" in value.get("error", "")
            for value in result["stages"].values()
        )

    asyncio.run(run())


def test_temporary_git_push_and_remote_divergence(tmp_path: Path) -> None:
    from experiments.orchestration.publication import Repository

    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        bare = tmp_path / "bare.git"
        bare.mkdir()
        remote = Repository(bare, push=False)
        await remote.git("init", "--bare", "--initial-branch=main")
        await c.repository.git("remote", "add", "origin", str(bare))
        await c.repository.git("push", "-u", "origin", "main")
        c.repository.push_enabled = True
        await c.repository.authenticate(c.approved_head)

        async def validate(_boundary: str, _paths: tuple[str, ...]) -> None:
            return

        published = await c.repository.commit(
            "PACKET",
            "published",
            {"result.json": b"{}\n"},
            "Fixture publication",
            validate,
        )
        assert (
            await remote.git("rev-parse", "refs/heads/main")
        ).decode().strip() == published
        await remote.git("update-ref", "refs/heads/main", c.approved_head)
        with pytest.raises(ValueError, match="Actual remote main differs"):
            await c.repository.authenticate(published)

    asyncio.run(run())


def test_callable_snapshots_cannot_mutate_approved_semantics(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        original = c.plan.canonical
        view = c.value
        view["semantic"]["model"] = "unapproved"
        view["commands"]["B"] = ["unapproved-command"]
        snapshot = c.state
        snapshot["publications"]["B"] = "foreign"
        assert c.plan.canonical == original
        assert c.value["semantic"]["model"] == "fixture-primary"
        assert "B" not in c.state["publications"]
        with pytest.raises(AttributeError):
            c.run_id = "unapproved"  # type: ignore[misc]  # Adversarial API assignment.
        with pytest.raises(AttributeError):
            c.plan = RunPlan.parse(view)  # type: ignore[misc]  # Adversarial assignment.

    asyncio.run(run())


def test_sibling_failure_during_packet_validation_blocks_reviewer_entry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")

        async def packet_validation(*_args: Any) -> dict[str, str]:
            c.blocked = True
            return {"status": "PASS"}

        monkeypatch.setattr(c, "validate", packet_validation)
        result = await c.worker(
            c.plan.cases[0],
            "C",
            {"README.md": b"frozen instructions"},
        )
        assert result is None
        assert not c.journal("alpha", "C", "ENTERED").exists()

    asyncio.run(run())


def test_worker_progress_is_never_scientific_authority(tmp_path: Path) -> None:
    import sys

    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        workspace = tmp_path / "worker"
        workspace.mkdir()
        (workspace / "progress.json").write_bytes(b"partial invalid JSON")
        result = await c.process(
            [sys.executable, "-c", "import time; time.sleep(1.4); print('done')"],
            workspace,
            "alpha",
            "progress-only",
        )
        assert result.exit_code == 0
        assert result.stdout.strip() == b"done"

    asyncio.run(run())


def test_checkout_ancestor_rejected(tmp_path: Path) -> None:
    from experiments.orchestration.tests.test_controller import FixtureController

    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        (tmp_path / "foreign/.git").mkdir(parents=True)
        with pytest.raises(ValueError, match="inside a checkout"):
            FixtureController(c.repository, c.plan, tmp_path / "foreign/workers")

    asyncio.run(run())


def test_commit_race_stops_before_push(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        original = c.repository.git

        async def racing(*args: str) -> bytes:
            if args[:3] == ("commit", "-m", "Fixture race"):
                await original(
                    "commit",
                    "--allow-empty",
                    "--only",
                    "-m",
                    "Maintainer race",
                )
            return await original(*args)

        monkeypatch.setattr(c.repository, "git", racing)

        async def validate(_boundary: str, _paths: tuple[str, ...]) -> None:
            return

        with pytest.raises(ValueError, match="push refused"):
            await c.repository.commit(
                "PACKET",
                "published",
                {"result.json": b"{}\n"},
                "Fixture race",
                validate,
            )
        assert (c.repository.root / "published/result.json").exists()

    asyncio.run(run())


@pytest.mark.parametrize(
    ("path", "bad"),
    [
        (("stage_a", "checkpoint"), "main"),
        (("stage_a", "protocol", "sha256"), "not-a-digest"),
        (("stage_a", "protocol", "path"), "holdout/secret.json"),
        (("approval",), ".local/codex-result.md"),
        (("semantic", "environment_allowlist"), ["PYTHONPATH"]),
        (("validation", "final"), [[""]]),
        (("cache", "enabled"), "yes"),
        (("timeouts", "worker"), float("inf")),
        (("publication", "push"), "yes"),
    ],
)
def test_plan_preflight_rejects_unsafe_or_ambiguous_metadata(
    tmp_path: Path,
    path: tuple[str, ...],
    bad: Any,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        value = c.value
        cursor = value
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = bad
        with pytest.raises(ValueError, match=r"."):
            RunPlan.parse(value)

    asyncio.run(run())


def test_forbidden_plan_address_rejected_before_git_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from experiments.orchestration.publication import Repository

    async def forbidden(*_args: Any) -> bytes:
        pytest.fail("Git was accessed before rejecting a restricted plan path")

    monkeypatch.setattr(Repository, "git", forbidden)

    async def run() -> None:
        with pytest.raises(ValueError, match="Restricted"):
            await Controller.from_plan(
                tmp_path,
                "holdout/protocol.json",
                tmp_path / "workers",
            )

    asyncio.run(run())


def test_publication_preserves_raw_scientific_crlf_and_spaces(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        raw = b"original scientific bytes  \r\n"

        async def validate(_boundary: str, _paths: tuple[str, ...]) -> None:
            return

        commit = await c.repository.commit(
            "PACKET",
            "published",
            {"raw_primary.md": raw},
            "Fixture exact bytes",
            validate,
        )
        assert (
            await c.repository.git("show", commit + ":published/raw_primary.md") == raw
        )
        await c.repository.git("diff", "--check", "HEAD^", "HEAD")
        assert not await c.repository.git("status", "--porcelain=v1")

    asyncio.run(run())
