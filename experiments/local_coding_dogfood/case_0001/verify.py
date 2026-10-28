"""Verify frozen inputs and captured actual effects without running a model."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
from pathlib import Path

from devtools.context.repository.resource import ContentIdentity


def verify(case: Path, evidence: Path) -> dict:
    frozen = json.loads((case / "freeze.json").read_text(encoding="utf-8"))
    payload = dict(frozen)
    expected = payload.pop("task_digest")
    assert (
        hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        == expected
    )
    for name, expected_hash in frozen["files"].items():
        assert (
            hashlib.sha256((case / name).read_bytes()).hexdigest() == expected_hash
        ), name
    outcome = json.loads((evidence / "outcome.json").read_text(encoding="utf-8"))
    worker = json.loads((evidence / "worker-result.json").read_text(encoding="utf-8"))
    assert outcome["task_digest"] == expected
    assert outcome["inference_entries"] == outcome["model_requests"] == 2
    assert outcome["applied_batches"] == outcome["proposals"] == 1
    assert outcome["tool_actions"] == 3
    assert outcome["worker_accepted"] and outcome["worker_completed"]
    assert outcome["worker_disposition"] == "validated"
    assert outcome["heldout_exit"] == outcome["focused_exit"] == 0
    assert outcome["restored_git_status"] == ""
    first, second = worker["requests"]
    assert {t["name"] for t in first["request"]["tools"]} == {
        "read_source",
        "replace_source",
        "validate_candidate",
        "inspect_and_validate_change",
    }
    calls = first["response"]["tool_calls"]
    assert [c["name"] for c in calls] == ["read_source"] * 3
    feedback = {
        m["tool_call_id"]: m
        for m in second["request"]["prompt"]["messages"]
        if m["role"] == "tool"
    }
    assert set(feedback) == {c["provider_call_id"] for c in calls}
    for call in calls:
        args = json.loads(call["arguments_json"])
        source = (case / "fixture" / args["path"]).read_text(encoding="utf-8")
        result = json.loads(feedback[call["provider_call_id"]]["content"])
        assert result["text"] == source
        assert result["span"] == [0, len(source)]
        assert result["snapshot"] == frozen["snapshot_id"]
        assert result["version"] == str(ContentIdentity.from_text(source))
        assert not result["partial"]
    assert [c["name"] for c in second["response"]["tool_calls"]] == ["replace_source"]
    assert not any(
        c["name"] == "inspect_and_validate_change"
        for r in worker["requests"]
        for c in r["response"]["tool_calls"]
    )
    assert len(outcome["procedures"]) == 1
    assert outcome["procedures"][0]["trigger"] == "deterministic-host-validation"
    assert outcome["procedures"][0]["report"]["status"] == "passed"
    records = {r["label"]: r for r in outcome["command_records"]}
    assert "Ran 8 tests" in records["final-heldout"]["stderr"]
    assert "Ran 5 tests" in records["final-focused"]["stderr"]
    assert records["final-heldout"]["stderr"].rstrip().endswith("OK")
    assert records["final-focused"]["stderr"].rstrip().endswith("OK")
    candidate = json.loads((evidence / "candidate-hashes.json").read_text())
    for name, expected_hash in candidate.items():
        assert (
            hashlib.sha256((evidence / "candidate" / name).read_bytes()).hexdigest()
            == expected_hash
        )
    assert (
        hashlib.sha256((evidence / "candidate/acceptance.py").read_bytes()).hexdigest()
        == frozen["files"]["fixture/acceptance.py"]
    )
    for path in ("events.py", "keys.py", "reports.py", "__init__.py"):
        assert (evidence / "candidate/stockroom" / path).read_bytes() == (
            case / "fixture/stockroom" / path
        ).read_bytes()
    after = worker["applied"][0][0]["after"]
    assert (evidence / "candidate/stockroom/projection.py").read_text(
        encoding="utf-8"
    ) == after
    assert worker["result"]["custody"]["restored"] is True
    assert all(e["acknowledged"] for e in worker["result"]["progress"]["effects"])
    usages = [r["response"]["usage"] for r in worker["requests"]]
    assert [r["measured_input_tokens"] for r in worker["requests"]] == [
        u["input_tokens"] for u in usages
    ]
    return dict(
        task_digest=expected,
        real_inference_calls=2,
        focused_tests=5,
        heldout_tests=8,
        input_tokens=sum(u["input_tokens"] for u in usages),
        output_tokens=sum(u["output_tokens"] for u in usages),
        total_tokens=sum(u["total_tokens"] for u in usages),
        worker_seconds=outcome["seconds"],
        command_observations=len(outcome["command_observations"]),
        model_selected_procedure=False,
        host_procedure=True,
        restored=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--grade",
        action="store_true",
        help="Rerun only frozen candidate oracles; never inference",
    )
    args = parser.parse_args()
    case = Path(__file__).resolve().parent
    summary = verify(case, case / "evidence")
    if args.grade:
        from devtools.core.paths import resolve_path
        from devtools.core.time import Duration
        from devtools.resources.commands import Command, CommandExecutor

        async def grade():
            root = case / "evidence/candidate"
            for name, argv in [
                ("focused", ("acceptance.py",)),
                ("heldout", (str(case / "heldout.py"), str(root))),
            ]:
                result = await CommandExecutor().execute(
                    Command(sys.executable)
                    .args("-B", *argv)
                    .cwd(resolve_path(root))
                    .with_timeout(Duration.seconds(30))
                )
                assert result.exit_code == 0, result.stderr.decode(errors="replace")
                summary[name + "_regrade_exit"] = result.exit_code
                summary[name + "_regrade_seconds"] = result.duration.total_seconds
            verify(case, case / "evidence")

        asyncio.run(grade())
    print(json.dumps(summary, indent=2))
