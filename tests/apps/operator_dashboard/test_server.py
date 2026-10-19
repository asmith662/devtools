# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- isolated local HTTP/evidence fixtures
"""Current data, archived turn association and read-only local security."""

from __future__ import annotations

import hashlib
import json
from http.client import HTTPConnection
from threading import Thread
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

import pytest

from apps.operator_dashboard import server as module
from apps.operator_dashboard.details import DISPLAY_LIMIT, confined, display
from apps.operator_dashboard.server import DashboardServer
from scripts.backlog.intake import Intake

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


def put(path: Path, value: object) -> None:
    """Write synthetic host-owned fixture data only."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def run(root: Path, name: str, *, turns: int, scripted: bool = False) -> None:
    """Represent the known record contracts without invoking a model."""
    folder = root / name
    stages = []
    for number in range(1, turns + 1):
        passed = turns == 2 and number == 2
        validation = {
            key: {
                "exit_code": 0 if passed else 1,
                "argv": ["fixture-python", key],
                "stdout": "PASS" if passed else "FAILED assertion",
                "stderr": "",
            }
            for key in ("tests", "oracle")
        }
        stages.append(
            {
                "number": number,
                "disposition": "ACCEPTED" if passed else "TESTS_FAILED",
                "proposal_id": f"call-{number}",
                "proposal_valid": True,
                "source_before": f"source-{number}",
                "source_after": f"source-{number + 1}",
                "validation": validation,
            }
        )
        turn = folder / f"turn-{number:02d}"
        put(
            turn / "request.json",
            {
                "prompt": {
                    "content": f'Task\nHOST FEEDBACK:\n{{"turn":{number}}}\nCONTEXT'
                },
                "settings": {"maximum_output_tokens": 4096},
            },
        )
        put(
            turn / "response.json",
            {
                "content": "exact response <script>alert(1)</script>",
                "tool_calls": [
                    {
                        "name": "propose_edit",
                        "provider_call_id": f"call-{number}",
                        "arguments_json": (
                            '{"path":"src/example.py",'
                            '"old_text":"old","new_text":"new"}'
                        ),
                    }
                ],
            },
        )
        (turn / "proposal.patch").write_text(
            "--- a/src/example.py\n+++ b/src/example.py\n-old\n+new\n", encoding="utf-8"
        )
    put(
        folder / "result.json",
        {
            "schema": "qwen-coding-loop-v2",
            "task_name": "markdown" if turns == 2 else "python-source-segments",
            "task_definition": {"objective": "Fixture task objective"},
            "disposition": "ACCEPTED" if turns == 2 else "REPAIR_BUDGET_EXHAUSTED",
            "turns": stages,
            "usage_totals": {},
            "provenance": {"mode": "SCRIPTED_HOST_TEST_ONLY"}
            if scripted
            else {"model": "fixture-local", "profile": {"context_size": 32768}},
        },
    )


@pytest.fixture
def api(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[DashboardServer]:
    """Serve real production routes against isolated records, never real authority."""
    (tmp_path / "docs/backlog/items").mkdir(parents=True)
    (tmp_path / "docs/backlog/overview.md").write_text("# Backlog", encoding="utf-8")
    (tmp_path / "docs/backlog/items/B-0001-example.md").write_text(
        "# B-0001 Example\n- status: SUPERSEDED\n- split_children: B-0002\n"
        "\n## Split record\nActual recorded split reason.\n",
        encoding="utf-8",
    )
    (tmp_path / "docs/backlog/items/B-0002-example.md").write_text(
        "# B-0002 Example\n- status: DEFERRED\n", encoding="utf-8"
    )

    async def identity(*_args: object) -> str:
        return "fixture-head"

    monkeypatch.setattr(module, "git", identity)
    worker_root = tmp_path / "workers"
    run(worker_root, "markdown-run", turns=2)
    run(worker_root, "python-run", turns=3)
    run(worker_root, "scripted", turns=2, scripted=True)
    http = DashboardServer(tmp_path, (worker_root,), raw=True, port=0)
    thread = Thread(target=http.serve_forever)
    thread.start()
    try:
        yield http
    finally:
        http.shutdown()
        thread.join()
        http.server_close()


def request(
    api: DashboardServer,
    path: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
) -> tuple[int, Any]:
    """Exercise actual TCP request routing and serialized projections."""
    connection = HTTPConnection("127.0.0.1", api.server_port, timeout=5)
    connection.request(method, path, headers=headers or {})
    response = connection.getresponse()
    body = response.read()
    connection.close()
    return response.status, json.loads(body) if body and response.getheader(
        "Content-Type", ""
    ).startswith("application/json") else body


def test_fresh_records_and_real_vs_scripted(api: DashboardServer) -> None:
    """New source records appear through the same running API without a build."""
    status, overview = request(api, "/api/overview")
    assert status == 200
    assert len(overview["workers"]) == 3
    assert overview["proposals"] == []
    intake = Intake(api.root, coordinator=api.root)
    identity = intake.capture(
        {
            "kind": "investigation",
            "title": "New fixture discovery",
            "summary": "Summary",
            "benefit": "Benefit",
            "uncertainty": "Unknown",
            "discovery": {"kind": "human", "reference": "fixture"},
            "parent": None,
            "resources": [],
            "evidence": ["fixture"],
            "dependencies": [],
        }
    )
    run(api.worker_roots[0], "added-after-refresh", turns=2)
    _, refreshed = request(api, "/api/overview")
    assert len(refreshed["workers"]) == 4
    assert refreshed["proposals"][0]["id"] == identity
    assert request(api, f"/api/proposals/{identity}")[1]["state"] == "PENDING_REVIEW"
    assert {r["evidence_class"] for r in refreshed["workers"]} == {
        "LOCAL_MODEL_RECEIPT",
        "SCRIPTED_HOST_TEST_ONLY",
    }


def test_turns_feedback_missing_capture_and_unchanged_sources(
    api: DashboardServer,
) -> None:
    """Associate exact requests, Tool calls, failures and accepted repair by turn."""
    before = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in api.root.rglob("*")
        if p.is_file()
    }
    _, index = request(api, "/api/overview")
    for row in index["workers"]:
        _, detail = request(api, "/api/runs/" + row["key"])
        expected = 3 if row["id"] == "python-run" else 2
        assert len(detail["turns"]) == expected
        assert detail["turns"][0]["stage"]["disposition"] == "TESTS_FAILED"
        assert detail["turns"][-1]["stage"]["disposition"] == (
            "TESTS_FAILED" if expected == 3 else "ACCEPTED"
        )
        for turn in detail["turns"]:
            assert turn["proposal_correlation"] == "MATCH"
            assert turn["tools"][0]["name"] == "propose_edit"
            assert json.loads(turn["feedback"]["text"])["turn"] == turn["number"]
            assert "exact response <script>" in turn["response_text"]["text"]
    assert all(
        hashlib.sha256(p.read_bytes()).hexdigest() == d for p, d in before.items()
    )
    row = index["workers"][0]
    folder = api.worker_roots[0] / row["id"]
    (folder / "turn-01/response.json").unlink()
    _, detail = request(api, "/api/runs/" + row["key"])
    assert detail["turns"][0]["response_text"]["availability"] == "NOT_CAPTURED"
    api.raw = False
    _, detail = request(api, "/api/runs/" + row["key"])
    assert detail["turns"][0]["request_text"]["availability"] == "NOT_DISCLOSED"


def test_backlog_security_and_bounds(api: DashboardServer) -> None:
    """No inferred reasons, arbitrary file reads, cross-origin requests or writes."""
    detail = request(api, "/api/backlog/B-0001")[1]
    assert "Actual recorded split reason" in detail["rationale"][0]
    assert detail["metadata"]["split_children"] == "B-0002"
    assert "NOT_RECORDED" in request(api, "/api/backlog/B-0002")[1]["rationale"][0]
    for path in ("/../AGENTS.md", "/api/runs/%2e%2e", "/api/overview?root=elsewhere"):
        assert request(api, path)[0] == 400
    assert request(api, "/api/runs/not-a-valid-id")[0] == 404
    assert request(api, "/api/proposals/invalid")[0] == 404
    assert request(api, "/api/overview", method="POST")[0] == 405
    assert (
        request(api, "/api/overview", headers={"Origin": "https://untrusted.example"})[
            0
        ]
        == 403
    )
    assert (
        request(api, "/api/overview", headers={"Host": "untrusted.example"})[0] == 403
    )
    assert (
        request(api, "/api/overview", headers={"Sec-Fetch-Site": "cross-site"})[0]
        == 403
    )
    assert request(api, "/data.json")[0] == 404
    assert request(api, "/api/overview", method="HEAD")[1] == b""
    bounded = display("a" * (DISPLAY_LIMIT + 100))
    assert bounded["truncated"]
    assert len(bounded["text"]) == DISPLAY_LIMIT
    with pytest.raises(ValueError, match="escapes"):
        confined(api.root, api.root / "../outside")


def test_multiple_roots_keep_run_identity_and_bound_responses(
    api: DashboardServer,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Same directory label in different roots never invents a shared session."""
    other = api.root / "other-workers"
    run(other, "markdown-run", turns=2)
    api.worker_roots = (*api.worker_roots, other)
    _, index = request(api, "/api/overview")
    rows = [w for w in index["workers"] if w["id"] == "markdown-run"]
    assert len(rows) == 2
    assert rows[0]["key"] != rows[1]["key"]
    for row in rows:
        assert request(api, "/api/runs/" + row["key"])[0] == 200
    monkeypatch.setattr(module, "MAX_RESPONSE", 100)
    assert request(api, "/api/overview")[0] == 503


def test_cancelled_observation_does_not_retry_response() -> None:
    """Closing a view may abort its read without causing another send or effect."""
    handler = module.Handler.__new__(module.Handler)
    handler.request_version = "HTTP/1.1"
    handler.command = "GET"
    handler.requestline = "GET /api/overview HTTP/1.1"
    output = Mock()
    output.write.side_effect = ConnectionAbortedError
    handler.wfile = output
    handler._send(200, b"read-only", "text/plain")  # noqa: SLF001
    assert output.write.call_count == 1
