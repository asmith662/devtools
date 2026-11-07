# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- exercise canonical writer and reader together
"""Payload hashes never collide with WorkCycle's canonical observation seal."""

import base64
import hashlib
from pathlib import Path

from scripts.backlog.native.execution import Capture
from scripts.backlog.work import WorkCycle, _load


def test_http_and_template_payloads_are_canonically_readable(tmp_path: Path) -> None:
    folder = tmp_path / "docs/backlog"
    folder.mkdir(parents=True)
    (folder / "overview.md").write_text("Fixture backlog\n")
    cycle = WorkCycle(tmp_path)
    captures = tmp_path / ".local/capture"
    captures.mkdir(parents=True)
    capture = Capture(cycle.native, captures, 16384)
    raw = b'{"error":"authentic server failure"}\xff'
    prompt = "Tool template π\nexact bytes"
    capture.http_response(1, 500, raw)
    capture.rendered_template(prompt)
    rows = [
        _load(captures / ref["file"], "backlog-native-observation-v1")
        for ref in capture.refs
    ]
    assert base64.b64decode(rows[0]["body_base64"]) == raw
    assert rows[0]["body_sha256"] == hashlib.sha256(raw).hexdigest()
    assert rows[0]["status"] == 500
    assert rows[1]["prompt"] == prompt
    assert rows[1]["prompt_sha256"] == hashlib.sha256(prompt.encode()).hexdigest()
    assert all(
        row["sha256"] == ref["sha256"]
        for row, ref in zip(rows, capture.refs, strict=True)
    )
