"""Verify the frozen Case0002 and observed discovery without invoking a model."""

import argparse
import asyncio
import hashlib
import json
import sys
from pathlib import Path

from devtools.context.repository.resource import ContentIdentity
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify(case, evidence):
    frozen = read(case / "freeze.json")
    copy = dict(frozen)
    expected = copy.pop("task_digest")
    assert (
        hashlib.sha256(
            json.dumps(copy, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        == expected
    )
    for name, value in frozen["files"].items():
        assert hashlib.sha256((case / name).read_bytes()).hexdigest() == value, name
    worker = read(evidence / "worker-result.json")
    outcome = read(evidence / "outcome.json")
    assert outcome["task_digest"] == expected
    assert frozen["required_source_witnesses"] is None
    assert len(frozen["available_resources"]) == 18 and len(frozen["editable"]) == 11
    prompt = read(evidence / "initial-prompt.json")["content"]
    assert "releasevault/versions.py" not in prompt
    requests = worker["requests"]
    assert (
        len(requests) == outcome["model_requests"] == outcome["inference_entries"] == 5
    )
    assert all(
        r["inference_entered"] and r["outcome"] == "normalized-response"
        for r in requests
    )
    assert (
        outcome["worker_accepted"]
        and outcome["completed"]
        and outcome["candidate_validated"]
    )
    assert (
        outcome["disposition"] == "validated"
        and outcome["focused_exit"] == outcome["heldout_exit"] == 0
    )
    assert (
        outcome["restored_git_status"] == ""
        and worker["result"]["custody"]["restored"] is True
    )
    assert all(
        effect["acknowledged"] for effect in worker["result"]["progress"]["effects"]
    )
    by_id = {
        call["provider_call_id"]: (r["number"], call)
        for r in requests
        for call in r["response"]["tool_calls"]
    }
    assert len(by_id) == sum(len(r["response"]["tool_calls"]) for r in requests) == 11
    assert set(t["name"] for t in requests[0]["request"]["tools"]) == set(
        frozen["tools"]
    )
    assert all("oracle.py" not in str(r["request"]) for r in requests)
    trace = []
    source_reads = []
    search_candidates = []
    for event in worker["acquisitions"]:
        number, call = by_id[event["call_id"]]
        consumed = []
        for later in requests:
            for message in later["request"]["prompt"]["messages"]:
                if (
                    message["role"] == "tool"
                    and message["tool_call_id"] == event["call_id"]
                ):
                    assert json.loads(message["content"]) == event["result"]
                    assert later["number"] > number
                    consumed.append(later["number"])
        assert consumed
        if event["kind"] == "source":
            args = json.loads(call["arguments_json"])
            text = (case / "fixture" / args["path"]).read_text(encoding="utf-8")
            result = event["result"]
            assert result["text"] == text[args["start"] : args["end"]]
            assert result["span"] == [args["start"], args["end"]]
            assert result["version"] == str(ContentIdentity.from_text(text))
            assert result["snapshot"] == frozen["snapshot_id"] and not result["partial"]
            source_reads.append(
                dict(
                    path=args["path"],
                    span=result["span"],
                    requested_in=number,
                    consumed_by=consumed,
                    call_id=event["call_id"],
                )
            )
        else:
            assert event["result"]["source_acquired"] is False
            assert "text" not in json.dumps(event["result"])
            if event["kind"] == "retrieval":
                search_candidates = event["result"]["hits"]
                assert len(search_candidates) == 6
                assert search_candidates[0]["path"] == "releasevault/versions.py"
        trace.append(
            dict(
                kind=event["kind"],
                call_id=event["call_id"],
                requested_in=number,
                consumed_by=consumed,
            )
        )
    assert len(source_reads) == 8
    assert [event["kind"] for event in worker["acquisitions"]].count("inventory") == 1
    assert [event["kind"] for event in worker["acquisitions"]].count("retrieval") == 1
    assert (
        len(worker["applied"])
        == outcome["applied_batches"]
        == outcome["proposals"]
        == 1
    )
    change = worker["applied"][0][0]
    path = change["address"]["value"]
    assert path == "releasevault/versions.py"
    old = json.loads(worker["proposals"][0]["calls"][0]["arguments_json"])["old_text"]
    before = (case / "fixture" / path).read_text(encoding="utf-8")
    assert before.count(old) == 1
    start = before.index(old)
    assert any(
        r["path"] == path and r["span"][0] <= start and start + len(old) <= r["span"][1]
        for r in source_reads
    )
    hashes = read(evidence / "candidate-hashes.json")
    changed = []
    for name, value in hashes.items():
        candidate = evidence / "candidate" / name
        assert hashlib.sha256(candidate.read_bytes()).hexdigest() == value
        if candidate.read_bytes() != (case / "fixture" / name).read_bytes():
            changed.append(name)
    assert changed == [path]
    assert (evidence / "candidate" / path).read_text(encoding="utf-8") == change[
        "after"
    ]
    assert (
        len(worker["procedures"]) == 1
        and worker["procedures"][0]["trigger"] == "deterministic-host-validation"
    )
    assert worker["procedures"][0]["report"]["status"] == "passed"
    assert not any(
        call["name"] in {"validate_candidate", "inspect_and_validate_change"}
        for _, call in by_id.values()
    )
    records = {r["label"]: r for r in outcome["command_records"]}
    assert "Ran 7 tests" in records["final-focused"]["stderr"] and records[
        "final-focused"
    ]["stderr"].rstrip().endswith("OK")
    assert "Ran 10 tests" in records["final-heldout"]["stderr"] and records[
        "final-heldout"
    ]["stderr"].rstrip().endswith("OK")
    usages = [r["response"]["usage"] for r in requests]
    assert all(
        r["measured_input_tokens"] == u["input_tokens"]
        for r, u in zip(requests, usages, strict=True)
    )
    return dict(
        task_digest=expected,
        requests=5,
        edits=1,
        resources_available=18,
        editable_resources=11,
        search_candidates=search_candidates,
        source_reads=source_reads,
        disclosure_trace=trace,
        edited=[path],
        focused_tests=7,
        heldout_tests=10,
        model_requested_checks=False,
        host_validation=True,
        live_repair=False,
        input_tokens=sum(u["input_tokens"] for u in usages),
        output_tokens=sum(u["output_tokens"] for u in usages),
        total_tokens=sum(u["total_tokens"] for u in usages),
        worker_seconds=outcome["seconds"],
        command_observations=len(outcome["command_observations"]),
        restored=True,
        discovery_qualification="The version read was requested in the search batch, before seeing its hits; later requests contain search metadata and earlier source. Presence in input is not proof of internal reasoning.",
    )


async def grade(case):
    root = case / "evidence/candidate"
    records = []
    for name, argv in [
        ("focused", ("acceptance.py",)),
        ("heldout", (str(case / "oracle.py"), str(root))),
    ]:
        result = await CommandExecutor().execute(
            Command(sys.executable)
            .args("-B", *argv)
            .cwd(resolve_path(root))
            .with_timeout(Duration.seconds(30))
        )
        assert result.exit_code == 0, result.stderr.decode(errors="replace")
        records.append(
            dict(
                name=name,
                exit_code=result.exit_code,
                seconds=result.duration.total_seconds,
            )
        )
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grade", action="store_true")
    args = parser.parse_args()
    case = Path(__file__).resolve().parent
    result = verify(case, case / "evidence")
    if args.grade:
        result["regrade"] = asyncio.run(grade(case))
        verify(case, case / "evidence")
    print(json.dumps(result, indent=2))
