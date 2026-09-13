# Copyright (c) 2026
"""Tests for one-run streamed vLLM benchmark execution."""
# ruff: noqa: PLR2004

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

from devtools.core.paths import ResolvedPath
from devtools.core.time import Duration, Timestamp
from devtools.models.benchmarks import runner
from devtools.models.benchmarks.models import BenchmarkCase
from devtools.models.serving.huggingface import HuggingFaceModelRef
from devtools.models.serving.vllm import VLLMServer, VLLMServingConfig

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


class _Reader:
    """Return planned HTTP response lines and bodies."""

    def __init__(
        self,
        lines: list[bytes],
        body: bytes = b"",
        raw_body: bytes | None = None,
        on_line: Callable[[bytes], None] | None = None,
    ) -> None:
        """Initialize one bounded fake streaming response."""
        self._lines = lines
        self._body = body
        self._raw_body = raw_body
        self._on_line = on_line

    async def readline(self) -> bytes:
        """Return the next response line."""
        if self._lines:
            line = self._lines.pop(0)
            if self._on_line is not None:
                self._on_line(line)
            return line
        if self._raw_body is None:
            return b""
        newline = self._raw_body.find(b"\n")
        if newline < 0:
            line, self._raw_body = self._raw_body, b""
            return line
        line = self._raw_body[: newline + 1]
        self._raw_body = self._raw_body[newline + 1 :]
        return line

    async def read(self, _size: int) -> bytes:
        """Return the bounded error body."""
        if self._raw_body is not None:
            body, self._raw_body = self._raw_body, b""
            return body
        return self._body

    async def readexactly(self, size: int) -> bytes:
        """Return one exact planned body segment or model a truncated socket."""
        body = self._raw_body or b""
        if len(body) < size:
            self._raw_body = b""
            raise asyncio.IncompleteReadError(body, size)
        result = body[:size]
        self._raw_body = body[size:]
        return result


class _Writer:
    """Record one benchmark request without network access."""

    def __init__(self) -> None:
        """Initialize captured request storage."""
        self.request = b""
        self.closed = False

    def write(self, data: bytes) -> None:
        """Capture request bytes."""
        self.request += data

    async def drain(self) -> None:
        """Model a successful socket drain."""

    def close(self) -> None:
        """Record socket closure."""
        self.closed = True

    async def wait_closed(self) -> None:
        """Model successful socket closure."""


class _Stopwatch:
    """Provide deterministic benchmark timing without sleeping."""

    @property
    def elapsed(self) -> Duration:
        """Return first-content elapsed time."""
        return Duration.milliseconds(2)

    def stop(self) -> Duration:
        """Return terminal elapsed time."""
        return Duration.milliseconds(10)


class _TimelineStopwatch:
    """Read an event-driven fake clock for direct TTFT-ordering regressions."""

    def __init__(self, clock: dict[str, int]) -> None:
        """Retain mutable simulated elapsed milliseconds."""
        self._clock = clock

    @property
    def elapsed(self) -> Duration:
        """Return the time established by the just-consumed stream event."""
        return Duration.milliseconds(self._clock["milliseconds"])

    def stop(self) -> Duration:
        """Return the planned terminal time."""
        return Duration.milliseconds(6)


def _server(tmp_path: Path) -> VLLMServer:
    config = VLLMServingConfig(
        model=HuggingFaceModelRef("Qwen/Qwen3-8B", "a" * 40),
        image="vllm/vllm-openai:v0.26.0",
        cache_root=ResolvedPath(tmp_path / "cache"),
        host_port=8123,
        served_model_name="qwen-local",
        max_model_len=2048,
        gpu_memory_utilization=0.8,
        max_num_seqs=1,
    )
    return VLLMServer(
        config=config,
        container_id="a" * 64,
        container_name="devtools-vllm-test",
        executor=object(),  # type: ignore[arg-type]
        started_at=Timestamp.now(),
    )


def _case(**changes: object) -> BenchmarkCase:
    values: dict[str, object] = {
        "name": "ready",
        "prompt": "Reply with exactly: local model ready",
        "max_tokens": 16,
        "expected_response": "hello",
    }
    values.update(changes)
    return BenchmarkCase(**values)  # type: ignore[arg-type]


def _stream_lines(*events: str) -> list[bytes]:
    return [
        b"HTTP/1.1 200 OK\r\n",
        b"Content-Type: text/event-stream\r\n",
        b"\r\n",
        *(f"data: {event}\n".encode() for event in events),
    ]


def _sse_body(*events: str) -> bytes:
    return b"".join(f"data: {event}\n\n".encode() for event in events)


def _chunked_body(*chunks: bytes) -> bytes:
    return (
        b"".join(f"{len(chunk):x}\r\n".encode() + chunk + b"\r\n" for chunk in chunks)
        + b"0\r\n\r\n"
    )


def _chunked_reader(*chunks: bytes) -> _Reader:
    return _Reader(
        [
            b"HTTP/1.1 200 OK\r\n",
            b"Transfer-Encoding: gzip, Chunked\r\n",
            b"Content-Type: text/event-stream\r\n",
            b"\r\n",
        ],
        raw_body=_chunked_body(*chunks),
    )


def test_runner_reconstructs_stream_and_measures_first_content(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Role-only and empty deltas do not become time to first content."""
    writer = _Writer()
    reader = _Reader(
        _stream_lines(
            '{"choices":[{"delta":{"role":"assistant"},"finish_reason":null}]}',
            '{"choices":[{"delta":{"content":""},"finish_reason":null}]}',
            '{"choices":[{"delta":{"content":"hel"},"finish_reason":null}]}',
            '{"choices":[{"delta":{"content":"lo"},"finish_reason":"stop"}]}',
            '{"choices":[],"usage":{"prompt_tokens":8,"completion_tokens":4}}',
            "[DONE]",
        ),
    )

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, writer

    monkeypatch.setattr(asyncio, "open_connection", connection)
    monkeypatch.setattr(runner, "Stopwatch", _Stopwatch)

    result = asyncio.run(
        runner.run_vllm_benchmark(server=_server(tmp_path), case=_case()),
    )

    assert result.response_text == "hello"
    assert result.ttft == Duration.milliseconds(2)
    assert result.total_duration == Duration.milliseconds(10)
    assert result.prompt_tokens == 8
    assert result.completion_tokens == 4
    assert result.completion_tokens_per_second == 400.0
    assert result.finish_reason == "stop"
    assert result.expectation_met is True
    assert b"stream_options" in writer.request
    assert writer.closed is True


def test_runner_records_ttft_only_for_first_nonempty_content_delta(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Role-only, empty, and later content events cannot alter first-token time."""
    clock = {"milliseconds": 0}
    event_times = iter((1, 2, 3, 5, 6))

    def advance(line: bytes) -> None:
        if line.startswith(b"data:"):
            clock["milliseconds"] = next(event_times)

    reader = _Reader(
        _stream_lines(
            '{"choices":[{"delta":{"role":"assistant"}}]}',
            '{"choices":[{"delta":{"content":""}}]}',
            '{"choices":[{"delta":{"content":"first"}}]}',
            '{"choices":[{"delta":{"content":" later"}}]}',
            "[DONE]",
        ),
        on_line=advance,
    )

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    monkeypatch.setattr(runner, "Stopwatch", lambda: _TimelineStopwatch(clock))
    result = asyncio.run(
        runner.run_vllm_benchmark(
            server=_server(tmp_path),
            case=_case(expected_response="first later"),
        ),
    )

    assert result.ttft == Duration.milliseconds(3)
    assert result.total_duration == Duration.milliseconds(6)
    assert result.response_text == "first later"


def test_runner_supports_missing_usage_and_expectation_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Usage is never estimated when the provider does not report it."""
    reader = _Reader(
        _stream_lines(
            '{"choices":[{"delta":{"content":"other"},"finish_reason":"stop"}]}',
            "[DONE]",
        ),
    )

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    monkeypatch.setattr(runner, "Stopwatch", _Stopwatch)
    result = asyncio.run(
        runner.run_vllm_benchmark(server=_server(tmp_path), case=_case()),
    )

    assert result.prompt_tokens is None
    assert result.completion_tokens is None
    assert result.completion_tokens_per_second is None
    assert result.expectation_met is False


def test_runner_decodes_chunked_vllm_stream_before_parsing_sse(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """HTTP chunk sizes never reach the vLLM SSE parser."""
    writer = _Writer()
    reader = _chunked_reader(
        _sse_body('{"choices":[{"delta":{"role":"assistant"}}]}'),
        _sse_body('{"choices":[{"delta":{"content":"hel"}}]}'),
        _sse_body(
            '{"choices":[{"delta":{"content":"lo"},"finish_reason":"stop"}]}',
            '{"choices":[],"usage":{"prompt_tokens":8,"completion_tokens":4}}',
            "[DONE]",
        ),
    )

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, writer

    monkeypatch.setattr(asyncio, "open_connection", connection)
    monkeypatch.setattr(runner, "Stopwatch", _Stopwatch)
    result = asyncio.run(
        runner.run_vllm_benchmark(server=_server(tmp_path), case=_case()),
    )

    assert result.response_text == "hello"
    assert result.completion_tokens_per_second == 400.0
    assert writer.closed is True


def test_runner_parses_an_sse_event_split_across_http_chunks(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """HTTP chunk boundaries never become SSE event boundaries."""
    event = b'data: {"choices":[{"delta":{"content":"hello"}}]}\n\n'
    reader = _chunked_reader(event[:25], event[25:] + b"data: [DONE]\n\n")

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    monkeypatch.setattr(runner, "Stopwatch", _Stopwatch)
    result = asyncio.run(
        runner.run_vllm_benchmark(
            server=_server(tmp_path),
            case=_case(expected_response="hello"),
        ),
    )

    assert result.response_text == "hello"
    assert result.expectation_met is True


def test_runner_parses_multiple_sse_events_inside_one_http_chunk(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """One decoded HTTP chunk can hold several ordered SSE events."""
    reader = _chunked_reader(
        _sse_body(
            '{"choices":[{"delta":{"content":"a"}}]}',
            '{"choices":[{"delta":{"content":"b"}}]}',
            "[DONE]",
        ),
    )

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    monkeypatch.setattr(runner, "Stopwatch", _Stopwatch)
    result = asyncio.run(
        runner.run_vllm_benchmark(
            server=_server(tmp_path),
            case=_case(expected_response="ab"),
        ),
    )

    assert result.response_text == "ab"


@pytest.mark.parametrize(
    ("raw_body", "match"),
    [
        (b"\r\n", "empty chunk size"),
        (b"xyz\r\n", "invalid chunk size"),
        (b"-1\r\n", "invalid chunk size"),
        (b" 1\r\n", "invalid chunk size"),
        (b"5\r\nabc", "within an HTTP chunk"),
        (b"3\r\nabcxx", "invalid chunk terminator"),
        (b"0\r\n\r\n", "before its terminal"),
    ],
)
def test_runner_rejects_malformed_or_incomplete_chunked_framing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    raw_body: bytes,
    match: str,
) -> None:
    """HTTP framing completion remains distinct from SSE protocol completion."""
    reader = _Reader(
        [
            b"HTTP/1.1 200 OK\r\n",
            b"Transfer-Encoding: chunked\r\n",
            b"\r\n",
        ],
        raw_body=raw_body,
    )

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    with pytest.raises(ValueError, match=match):
        asyncio.run(runner.run_vllm_benchmark(server=_server(tmp_path), case=_case()))


@pytest.mark.parametrize(
    ("headers", "match"),
    [
        ([b"bad-header\r\n", b"\r\n"], "invalid HTTP header"),
        ([b": value\r\n", b"\r\n"], "empty HTTP header name"),
    ],
)
def test_runner_rejects_malformed_http_headers(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    headers: list[bytes],
    match: str,
) -> None:
    """Response framing begins only after structurally valid headers."""
    reader = _Reader([b"HTTP/1.1 200 OK\r\n", *headers])

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    with pytest.raises(ValueError, match=match):
        asyncio.run(runner.run_vllm_benchmark(server=_server(tmp_path), case=_case()))


@pytest.mark.parametrize(
    ("raw_body", "match"),
    [
        (b"", "before a chunk size"),
        (b"0\r\n", "before chunked trailers"),
    ],
)
def test_runner_rejects_incomplete_chunked_boundaries(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    raw_body: bytes,
    match: str,
) -> None:
    """Chunked framing cannot silently accept an unfinished HTTP body."""
    reader = _Reader(
        [
            b"HTTP/1.1 200 OK\r\n",
            b"Transfer-Encoding: chunked\r\n",
            b"\r\n",
        ],
        raw_body=raw_body,
    )

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    with pytest.raises(ValueError, match=match):
        asyncio.run(runner.run_vllm_benchmark(server=_server(tmp_path), case=_case()))


def test_runner_consumes_chunked_trailers_and_final_unterminated_sse_line(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """HTTP trailers are framing-only and do not change a valid terminal SSE event."""
    body = b"data: [DONE]"
    reader = _Reader(
        [
            b"HTTP/1.1 200 OK\r\n",
            b"Transfer-Encoding: chunked\r\n",
            b"\r\n",
        ],
        raw_body=(
            f"{len(body):x}\r\n".encode()
            + body
            + b"\r\n0\r\nX-Benchmark: value\r\n\r\n"
        ),
    )

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    monkeypatch.setattr(runner, "Stopwatch", _Stopwatch)
    result = asyncio.run(
        runner.run_vllm_benchmark(
            server=_server(tmp_path),
            case=_case(expected_response=None),
        ),
    )

    assert result.response_text == ""


@pytest.mark.parametrize(
    ("event", "match"),
    [
        ('{"choices":[null]}', "choice"),
        ('{"choices":[{"delta":{},"finish_reason":1}]}', "finish reason"),
        ('{"choices":[{"delta":{"content":1}}]}', "content delta"),
    ],
)
def test_runner_rejects_invalid_stream_event_shapes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    event: str,
    match: str,
) -> None:
    """Provider values with invalid runtime shapes never form a result."""

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return _Reader(_stream_lines(event, "[DONE]")), _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    with pytest.raises(ValueError, match=match):
        asyncio.run(runner.run_vllm_benchmark(server=_server(tmp_path), case=_case()))


def test_runner_ignores_comment_events_and_missing_delta(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Non-content events leave content timing absent rather than fabricated."""
    reader = _Reader(
        [
            b"HTTP/1.1 200 OK\r\n",
            b"\r\n",
            b": comment\n",
            b"event: message\n",
            b'data: {"choices":[{"delta":"unexpected"}]}\n',
            b"data: [DONE]\n",
        ],
    )

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    monkeypatch.setattr(runner, "Stopwatch", _Stopwatch)
    result = asyncio.run(
        runner.run_vllm_benchmark(
            server=_server(tmp_path),
            case=_case(expected_response=None),
        ),
    )

    assert result.response_text == ""
    assert result.ttft is None
    assert result.expectation_met is None


@pytest.mark.parametrize(
    ("lines", "body", "match"),
    [
        ([b"bad\r\n"], b"", "status line"),
        ([b"HTTP/1.1 nope\r\n"], b"", "not an integer"),
        ([b"HTTP/1.1 500 Error\r\n", b"\r\n"], b"server failed", "HTTP 500"),
        (_stream_lines("not-json"), b"", "invalid JSON"),
        (_stream_lines("[]"), b"", "not an object"),
        (
            [b"HTTP/1.1 200 OK\r\n", b"\r\n", b"field: value\n"],
            b"",
            "invalid SSE",
        ),
        (_stream_lines('{"choices":[]}'), b"", "before its terminal"),
    ],
)
def test_runner_rejects_unsuccessful_or_malformed_streams(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    lines: list[bytes],
    body: bytes,
    match: str,
) -> None:
    """One attempted request fails transparently on provider protocol failures."""
    writer = _Writer()

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        return _Reader(lines, body), writer

    monkeypatch.setattr(asyncio, "open_connection", connection)
    with pytest.raises(ValueError, match=match):
        asyncio.run(runner.run_vllm_benchmark(server=_server(tmp_path), case=_case()))
    assert writer.closed is True


def test_runner_preserves_cancellation_identity(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Benchmark cancellation is caller-owned and never converted to a result."""
    primary = asyncio.CancelledError("primary")

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        raise primary

    monkeypatch.setattr(asyncio, "open_connection", connection)
    with pytest.raises(asyncio.CancelledError) as raised:
        asyncio.run(runner.run_vllm_benchmark(server=_server(tmp_path), case=_case()))
    assert raised.value is primary


def test_runner_raises_explicit_timeout(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A benchmark request has one explicit bounded request-timeout policy."""

    async def connection(_host: str, _port: int) -> tuple[_Reader, _Writer]:
        await asyncio.sleep(1)
        return _Reader([]), _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    with pytest.raises(TimeoutError, match="exceeded"):
        asyncio.run(
            runner.run_vllm_benchmark(
                server=_server(tmp_path),
                case=_case(),
                request_timeout=Duration.seconds(0.001),
            ),
        )


def test_stream_helper_rejects_invalid_endpoint_and_usage() -> None:
    """Protocol helpers reject malformed endpoint and usage values directly."""

    async def invalid_endpoint() -> None:
        async for _ in runner._stream_vllm_chat(  # noqa: SLF001
            endpoint="relative",
            model="model",
            case=_case(),
            request_timeout=Duration.seconds(1),
        ):
            pass

    with pytest.raises(ValueError, match="endpoint"):
        asyncio.run(invalid_endpoint())
    assert runner._optional_token_count(None) is None  # noqa: SLF001
    assert runner._optional_token_count(0) == 0  # noqa: SLF001
    with pytest.raises(ValueError, match="token"):
        runner._optional_token_count(value=True)  # noqa: SLF001


def test_throughput_uses_total_duration_and_requires_reported_usage() -> None:
    """Whole-request throughput never fabricates usage or divides by zero."""
    assert (
        runner._completion_throughput(  # noqa: SLF001
            completion_tokens=None,
            total_duration=Duration.seconds(2),
        )
        is None
    )
    assert (
        runner._completion_throughput(  # noqa: SLF001
            completion_tokens=4,
            total_duration=Duration.seconds(2),
        )
        == 2.0
    )
    assert (
        runner._completion_throughput(  # noqa: SLF001
            completion_tokens=1,
            total_duration=Duration.seconds(0),
        )
        is None
    )
