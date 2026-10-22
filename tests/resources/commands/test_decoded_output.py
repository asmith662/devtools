# Copyright (c) 2026
# ruff: noqa: COM812 -- maintained test formatting convention
"""Independent regression coverage for Qwen's explicit decoded output views."""

from dataclasses import asdict

import pytest

from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandResult


@pytest.mark.parametrize("method", ["stdout_text", "stderr_text"])
def test_decode_views_preserve_original_result(method: str) -> None:
    """Views decode native bytes without altering metadata or retained output."""
    result = CommandResult(
        Command("python"),
        1,
        b"caf\xc3\xa9",
        b"caf\xc3\xa9",
        Duration.seconds(1),
        stdout_truncated=True,
        stderr_truncated=True,
        events_dropped=3,
    )
    before = asdict(result)
    assert getattr(result, method)() == "café"
    assert getattr(result, method)(encoding="latin-1") == b"caf\xc3\xa9".decode(
        "latin-1"
    )
    assert asdict(result) == before


@pytest.mark.parametrize("method", ["stdout_text", "stderr_text"])
def test_decode_views_keep_native_codec_error_contract(method: str) -> None:
    """Strict errors, alternate policies and unknown codecs remain native."""
    result = CommandResult(Command("python"), 0, b"\xff", b"\xff", Duration.seconds(0))
    decode = getattr(result, method)
    with pytest.raises(UnicodeDecodeError):
        decode()
    with pytest.raises(LookupError):
        decode(encoding="does-not-exist")
    assert decode(errors="replace") == "\ufffd"
    assert decode(errors="ignore") == ""
    with pytest.raises(TypeError):
        decode("utf-8")
