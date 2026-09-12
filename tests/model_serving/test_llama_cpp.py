# ruff: noqa: ARG001, C901, COM812, CPY001, D103, EM101, FBT003, PLR2004, PT011, PT018, SLF001, TC003
"""Tests for the bounded concrete llama.cpp Docker lifecycle."""

from __future__ import annotations

import asyncio
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from devtools.commands import Command, CommandExecutor, CommandResult
from devtools.model_serving import llama_cpp
from devtools.model_serving.errors import (
    LlamaCppCapabilityError,
    LlamaCppInspectionError,
    LlamaCppLaunchError,
    LlamaCppOwnershipError,
    LlamaCppStartupError,
    LlamaCppStopError,
    ServingReadinessTimeoutError,
)
from devtools.paths import ResolvedPath
from devtools.time import Duration, Timestamp

_ID = "a" * 64


def _result(
    command: Command,
    code: int = 0,
    out: bytes = b"",
    err: bytes = b"",
) -> CommandResult:
    return CommandResult(command, code, out, err, Duration.seconds(0))


def _config(tmp_path: Path, **changes: object) -> llama_cpp.LlamaCppServingConfig:
    model = tmp_path / "model.gguf"
    model.touch(exist_ok=True)
    values: dict[str, object] = {
        "model": llama_cpp.GGUFModel(ResolvedPath(model)),
        "image": "ghcr.io/ggml-org/llama.cpp:server-cuda",
        "host_port": 8081,
        "served_model_name": "local-model",
        "context_size": 4096,
        "gpu_layers": "all",
    }
    values.update(changes)
    return llama_cpp.LlamaCppServingConfig(**values)  # type: ignore[arg-type]


class _Executor(CommandExecutor):
    def __init__(self, results: list[CommandResult | BaseException]) -> None:
        self.commands: list[Command] = []
        self.results = results

    async def execute(self, command: Command) -> CommandResult:
        self.commands.append(command)
        value = self.results.pop(0)
        if isinstance(value, BaseException):
            raise value
        return value


def test_values_and_config_validate(tmp_path: Path) -> None:
    config = _config(tmp_path)
    assert config.flash_attention == "auto" and config.cache_type_k == "f16"
    assert config.parallel_sequences == 1 and hash(config)
    assert config.n_cpu_ffn == 0
    with pytest.raises(FrozenInstanceError):
        config.host_port = 1  # type: ignore[misc]
    for field, value in [
        ("image", "image"),
        ("host_port", 0),
        ("served_model_name", " "),
        ("context_size", 0),
        ("gpu_layers", -1),
        ("gpu_layers", "bad"),
        ("parallel_sequences", 0),
        ("n_cpu_ffn", -1),
        ("flash_attention", "invalid"),
        ("cache_type_k", "invalid"),
        ("cache_type_v", "invalid"),
    ]:
        with pytest.raises(ValueError):
            _config(tmp_path, **{field: value})
    with pytest.raises(ValueError, match="gguf"):
        llama_cpp.GGUFModel(ResolvedPath(tmp_path / "model.bin"))
    with pytest.raises(TypeError, match="integer"):
        _config(tmp_path, n_cpu_ffn=True)


def test_launch_argv_is_exact_and_safe(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        gpu_layers=12,
        flash_attention="on",
        cache_type_k="q8_0",
        cache_type_v="q4_0",
        parallel_sequences=2,
    )
    command = llama_cpp._build_launch_command(config, "devtools-llama-cpp-test")
    assert command.executable == "docker" and command.arguments.count("--model") == 1
    assert "--gpus" in command.arguments and "all" in command.arguments
    assert f"127.0.0.1:{config.host_port}:8080" in command.arguments
    assert (
        f"type=bind,src={config.model.path.value.resolve()},dst=/models/model.gguf,readonly"
        in command.arguments
    )
    assert (
        "/models/model.gguf" in command.arguments and config.image in command.arguments
    )
    for option, value in {
        "--alias": "local-model",
        "--ctx-size": "4096",
        "--n-gpu-layers": "12",
        "--flash-attn": "on",
        "--cache-type-k": "q8_0",
        "--cache-type-v": "q4_0",
        "--parallel": "2",
    }.items():
        assert command.arguments.count(option) == 1
        assert command.arguments[command.arguments.index(option) + 1] == value
    assert "--rm" not in command.arguments and "--hf-repo" not in command.arguments
    assert "--n-cpu-ffn" not in command.arguments

    cpu_ffn_command = llama_cpp._build_launch_command(
        _config(tmp_path, n_cpu_ffn=4),
        "devtools-llama-cpp-test",
    )
    assert cpu_ffn_command.arguments.count("--n-cpu-ffn") == 1
    assert (
        cpu_ffn_command.arguments[cpu_ffn_command.arguments.index("--n-cpu-ffn") + 1]
        == "4"
    )

    persistent_command = llama_cpp._build_launch_command(
        config,
        "devtools-qwen38-llama-cpp",
        managed=False,
        labels=(("devtools.qwen.persistent-service", "qwen38-llama-cpp"),),
    )
    assert "devtools.model_serving.managed=true" not in persistent_command.arguments
    assert "devtools.qwen.persistent-service=qwen38-llama-cpp" in (
        persistent_command.arguments
    )


def test_launch_argv_mounts_snapshot_backing_file_with_gguf_target(
    tmp_path: Path,
) -> None:
    """A snapshot link mounts its resolved bytes without losing the GGUF name."""
    blob = tmp_path / "blobs" / ("a" * 64)
    blob.parent.mkdir()
    blob.write_bytes(b"GGUF")
    snapshot = tmp_path / "snapshots" / "model.gguf"
    snapshot.parent.mkdir()
    snapshot.symlink_to(blob)
    config = _config(
        tmp_path,
        model=llama_cpp.GGUFModel(ResolvedPath(snapshot)),
    )

    command = llama_cpp._build_launch_command(config, "devtools-llama-cpp-test")

    assert (
        f"type=bind,src={blob.resolve()},dst=/models/model.gguf,readonly"
        in command.arguments
    )
    assert (
        f"type=bind,src={snapshot.parent},dst=/models,readonly"
        not in command.arguments
    )
    assert (
        command.arguments[command.arguments.index("--model") + 1]
        == "/models/model.gguf"
    )


def test_n_cpu_ffn_preflight_uses_exact_image_before_model_launch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A required new option is checked in-image before a serving run exists."""
    config = _config(tmp_path, n_cpu_ffn=4)
    command = Command("docker")
    executor = _Executor(
        [
            _result(command, err=b"Usage: llama-server --n-cpu-ffn N\n"),
            _result(command, out=f"{_ID}\n".encode()),
        ],
    )

    async def ready(
        _self: llama_cpp.LlamaCppServer,
        *,
        readiness_timeout: Duration,
    ) -> None:
        assert readiness_timeout == llama_cpp.DEFAULT_READINESS_TIMEOUT

    monkeypatch.setattr(llama_cpp.LlamaCppServer, "wait_ready", ready)
    asyncio.run(llama_cpp.LlamaCppServer.start(config=config, executor=executor))

    assert executor.commands[0].arguments == ("run", "--rm", config.image, "--help")
    assert executor.commands[1].arguments[0:2] == ("run", "--detach")


def test_n_cpu_ffn_preflight_rejects_unsupported_image_before_launch(
    tmp_path: Path,
) -> None:
    """An unsupported image cannot create a serving container by accident."""
    config = _config(tmp_path, n_cpu_ffn=4)
    command = Command("docker")
    executor = _Executor([_result(command, out=b"Usage: llama-server --parallel N\\n")])

    with pytest.raises(LlamaCppCapabilityError, match="does not advertise"):
        asyncio.run(llama_cpp.LlamaCppServer.start(config=config, executor=executor))

    assert [item.arguments for item in executor.commands] == [
        ("run", "--rm", config.image, "--help"),
    ]


def test_n_cpu_ffn_preflight_reports_failed_inspection_without_option_claim(
    tmp_path: Path,
) -> None:
    """A Docker/help failure does not prove the image lacks the option."""
    config = _config(tmp_path, n_cpu_ffn=4)
    command = Command("docker")
    executor = _Executor([_result(command, 1, err=b"image unavailable")])

    with pytest.raises(LlamaCppCapabilityError, match="Could not establish") as raised:
        asyncio.run(llama_cpp.LlamaCppServer.start(config=config, executor=executor))

    assert "does not advertise" not in str(raised.value)
    assert "image unavailable" in str(raised.value)
    assert [item.arguments for item in executor.commands] == [
        ("run", "--rm", config.image, "--help"),
    ]


def test_n_cpu_ffn_option_match_is_exact() -> None:
    """Similar option names cannot satisfy the selective-placement preflight."""
    assert llama_cpp._advertises_n_cpu_ffn("  --n-cpu-ffn N")
    assert not llama_cpp._advertises_n_cpu_ffn("--n-cpu-ffn-other N")


def test_id_parser_and_inspection_are_strict() -> None:
    command = Command("docker")
    assert (
        llama_cpp._parse_container_id(_result(command, out=f"{_ID}\n".encode())) == _ID
    )
    for output in (b"", b"x\n" + _ID.encode(), b"a" * 63):
        with pytest.raises(LlamaCppLaunchError):
            llama_cpp._parse_container_id(_result(command, out=output))
    assert llama_cpp._is_exact_container_not_found(
        _result(command, 1, err=f"Error: No such object: {_ID}".encode()),
        _ID,
    )
    assert not llama_cpp._is_exact_container_not_found(
        _result(command, 1, err=b"Error: No such object: other"),
        _ID,
    )


def test_start_ready_and_no_success_logs(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        return _result(
            command,
            out=(
                f"{_ID}\n".encode() if command.arguments[0] == "run" else b"true|true\n"
            ),
        )

    executor.execute = execute  # type: ignore[method-assign]

    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(llama_cpp, "_probe_ready", ready)
    server = asyncio.run(
        llama_cpp.LlamaCppServer.start(
            config=_config(tmp_path),
            executor=executor,
            readiness_timeout=Duration.seconds(1),
        ),
    )
    assert server.container_id == _ID and server.endpoint == "http://127.0.0.1:8081"
    assert all(command.arguments[0] != "logs" for command in executor.commands)


def test_start_exit_logs_cleanup_and_cancellation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    command = Command("docker")
    executor = _Executor(
        [
            _result(command, out=f"{_ID}\n".encode()),
            _result(command, out=b"false|true\n"),
            _result(command, out=b"tail"),
            _result(command, out=b"false|true\n"),
            _result(command),
        ],
    )
    with pytest.raises(LlamaCppStartupError, match="tail"):
        asyncio.run(
            llama_cpp.LlamaCppServer.start(config=_config(tmp_path), executor=executor),
        )
    server = llama_cpp.LlamaCppServer(
        config=_config(tmp_path),
        container_id=_ID,
        container_name="x",
        executor=_Executor([]),
        started_at=Timestamp.now(),
    )
    primary = asyncio.CancelledError()

    async def fail(_self: llama_cpp.LlamaCppServer) -> None:
        raise RuntimeError("cleanup")

    monkeypatch.setattr(llama_cpp.LlamaCppServer, "stop", fail)
    asyncio.run(server._stop_after_unsuccessful_start(primary))
    assert primary.__notes__ and "cleanup" in primary.__notes__[0]


def test_timeout_status_and_stop_boundaries(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config = _config(tmp_path)
    server = llama_cpp.LlamaCppServer(
        config=config,
        container_id=_ID,
        container_name="x",
        executor=_Executor([]),
        started_at=Timestamp.now(),
    )

    async def absent(*_: object) -> None:
        return None

    monkeypatch.setattr(llama_cpp, "_inspect_container", absent)
    assert asyncio.run(server.status()) == llama_cpp.LlamaCppServerStatus(False, False)
    asyncio.run(server.stop())

    async def owned(*_: object) -> llama_cpp._ContainerInspection:
        return llama_cpp._ContainerInspection(True, "false")

    monkeypatch.setattr(llama_cpp, "_inspect_container", owned)
    with pytest.raises(LlamaCppOwnershipError):
        asyncio.run(server.stop())
    with pytest.raises(ValueError):
        asyncio.run(server.wait_ready(readiness_timeout=Duration.seconds(0)))


def test_readiness_loading_timeout_and_http(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    async def loading(
        _self: llama_cpp.LlamaCppServer,
    ) -> llama_cpp.LlamaCppServerStatus:
        return llama_cpp.LlamaCppServerStatus(True, False)

    server = llama_cpp.LlamaCppServer(
        config=_config(tmp_path),
        container_id=_ID,
        container_name="x",
        executor=_Executor([]),
        started_at=Timestamp.now(),
    )
    monkeypatch.setattr(llama_cpp.LlamaCppServer, "status", loading)
    with pytest.raises(ServingReadinessTimeoutError):
        asyncio.run(server.wait_ready(readiness_timeout=Duration.seconds(0.001)))

    async def get(_: str, __: str) -> tuple[int, str]:
        return 503, ""

    monkeypatch.setattr(llama_cpp, "_http_get", get)
    assert not asyncio.run(llama_cpp._probe_ready("http://host"))

    async def good(_: str, __: str) -> tuple[int, str]:
        return 200, ""

    monkeypatch.setattr(llama_cpp, "_http_get", good)
    assert asyncio.run(llama_cpp._probe_ready("http://host"))
    monkeypatch.undo()
    assert asyncio.run(llama_cpp._http_get("relative", "/health")) == (0, "")


def test_remaining_failure_boundaries(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Exercise bounded failures without Docker or network access."""
    config = _config(tmp_path)
    server = llama_cpp.LlamaCppServer(
        config=config,
        container_id=_ID,
        container_name="x",
        executor=_Executor([]),
        started_at=Timestamp.now(),
    )
    assert server.started_at
    missing = llama_cpp.LlamaCppServingConfig(
        model=llama_cpp.GGUFModel(ResolvedPath(tmp_path / "missing.gguf")),
        image=config.image,
        host_port=config.host_port,
        served_model_name=config.served_model_name,
        context_size=config.context_size,
        gpu_layers=config.gpu_layers,
    )
    with pytest.raises(ValueError, match="existing"):
        asyncio.run(
            llama_cpp.LlamaCppServer.start(config=missing, executor=_Executor([]))
        )
    directory = tmp_path / "directory.gguf"
    directory.mkdir()
    directory_config = llama_cpp.LlamaCppServingConfig(
        model=llama_cpp.GGUFModel(ResolvedPath(directory)),
        image=config.image,
        host_port=config.host_port,
        served_model_name=config.served_model_name,
        context_size=config.context_size,
        gpu_layers=config.gpu_layers,
    )
    with pytest.raises(ValueError, match="existing"):
        asyncio.run(
            llama_cpp.LlamaCppServer.start(
                config=directory_config,
                executor=_Executor([]),
            )
        )
    command = Command("docker")
    with pytest.raises(LlamaCppLaunchError, match="exit code"):
        asyncio.run(
            llama_cpp.LlamaCppServer.start(
                config=config, executor=_Executor([_result(command, 1, err=b"bad")])
            )
        )
    assert llama_cpp._diagnostic_text(b"x" * 5000) == "x" * 4096
    assert "bad" in llama_cpp._launch_error_message(_result(command, 1, err=b"bad"))

    async def failed(_: Command) -> CommandResult:
        return _result(command, 1, err=b"daemon")

    with pytest.raises(LlamaCppInspectionError, match="daemon"):
        asyncio.run(
            llama_cpp._inspect_container(
                _Executor([_result(command, 1, err=b"daemon")]), _ID
            )
        )
    for output in (b"", b"maybe|true\n", b"true|true\nfalse|true\n"):
        with pytest.raises(LlamaCppInspectionError):
            asyncio.run(
                llama_cpp._inspect_container(
                    _Executor([_result(command, out=output)]), _ID
                )
            )

    async def stopped(*_: object) -> llama_cpp._ContainerInspection:
        return llama_cpp._ContainerInspection(False, "true")

    monkeypatch.setattr(llama_cpp, "_inspect_container", stopped)

    async def bad_remove(_executor: _Executor, _: Command) -> CommandResult:
        return _result(command, 1, err=b"cannot remove")

    monkeypatch.setattr(_Executor, "execute", bad_remove)
    with pytest.raises(LlamaCppStopError, match="cannot remove"):
        asyncio.run(server.stop())
    assert "cannot" in llama_cpp._stop_error_message(
        "remove", _result(command, 1, err=b"cannot"), _ID
    )

    class Reader:
        async def read(self) -> bytes:
            return b"not http"

    class Writer:
        def write(self, _: bytes) -> None:
            pass

        async def drain(self) -> None:
            pass

        def close(self) -> None:
            pass

        async def wait_closed(self) -> None:
            pass

    async def connection(_: str, __: int) -> tuple[Reader, Writer]:
        return Reader(), Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    assert asyncio.run(llama_cpp._http_get("http://host", "/health")) == (0, "")


def test_uncovered_operational_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Exercise remaining exact-ID, diagnostics, stop, and HTTP branches."""
    command = Command("docker")
    config = _config(tmp_path)
    server = llama_cpp.LlamaCppServer(
        config=config,
        container_id=_ID,
        container_name="x",
        executor=_Executor([]),
        started_at=Timestamp.now(),
    )
    assert server.config is config
    assert str(LlamaCppStartupError("plain", provider_log_tail=None)) == "plain"
    assert (
        asyncio.run(
            llama_cpp._inspect_container(
                _Executor(
                    [_result(command, 1, err=f"Error: No such object: {_ID}".encode())]
                ),
                _ID,
            )
        )
        is None
    )
    with pytest.raises(LlamaCppInspectionError, match="Docker could"):
        asyncio.run(llama_cpp._inspect_container(_Executor([_result(command, 1)]), _ID))
    assert (
        asyncio.run(llama_cpp._provider_log_tail(_Executor([_result(command, 1)]), _ID))
        is None
    )
    assert (
        asyncio.run(llama_cpp._provider_log_tail(_Executor([RuntimeError()]), _ID))
        is None
    )
    executor = _Executor([])
    server = llama_cpp.LlamaCppServer(
        config=config,
        container_id=_ID,
        container_name="x",
        executor=executor,
        started_at=Timestamp.now(),
    )

    async def running(*_: object) -> llama_cpp._ContainerInspection:
        return llama_cpp._ContainerInspection(True, "true")

    async def commands(_executor: _Executor, docker_command: Command) -> CommandResult:
        _executor.commands.append(docker_command)
        return _result(docker_command)

    monkeypatch.setattr(llama_cpp, "_inspect_container", running)
    monkeypatch.setattr(_Executor, "execute", commands)
    asyncio.run(server.stop())
    assert [item.arguments[0] for item in executor.commands] == ["stop", "rm"]

    async def failed_stop(
        _executor: _Executor, docker_command: Command
    ) -> CommandResult:
        return _result(docker_command, 1, err=b"stop failed")

    monkeypatch.setattr(_Executor, "execute", failed_stop)
    with pytest.raises(LlamaCppStopError, match="stop failed"):
        asyncio.run(server.stop())

    async def refused(*_: object) -> tuple[object, object]:
        raise OSError

    monkeypatch.setattr(asyncio, "open_connection", refused)
    assert asyncio.run(llama_cpp._http_get("http://host", "/health")) == (0, "")

    class ValidReader:
        async def read(self) -> bytes:
            return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nready"

    class ValidWriter:
        def write(self, _: bytes) -> None:
            pass

        async def drain(self) -> None:
            pass

        def close(self) -> None:
            pass

        async def wait_closed(self) -> None:
            pass

    async def accepted(_: str, __: int) -> tuple[ValidReader, ValidWriter]:
        return ValidReader(), ValidWriter()

    monkeypatch.setattr(asyncio, "open_connection", accepted)
    assert asyncio.run(llama_cpp._http_get("http://host", "/health")) == (200, "ready")

    class InvalidReader:
        async def read(self) -> bytes:
            return b"HTTP/1.1 nope OK\r\n\r\n"

    async def invalid(_: str, __: int) -> tuple[InvalidReader, ValidWriter]:
        return InvalidReader(), ValidWriter()

    monkeypatch.setattr(asyncio, "open_connection", invalid)
    assert asyncio.run(llama_cpp._http_get("http://host", "/health")) == (0, "")

    class EmptyHeaderReader:
        async def read(self) -> bytes:
            return b"\r\n\r\n"

    async def empty_header(_: str, __: int) -> tuple[EmptyHeaderReader, ValidWriter]:
        return EmptyHeaderReader(), ValidWriter()

    monkeypatch.setattr(asyncio, "open_connection", empty_header)
    assert asyncio.run(llama_cpp._http_get("http://host", "/health")) == (0, "")


def test_start_preserves_timeout_and_cancellation_through_cleanup(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Start preserves primary timeout/cancellation while attempting cleanup once."""
    command = Command("docker")
    primary_timeout = ServingReadinessTimeoutError("timeout")
    calls: list[str] = []

    async def wait_timeout(
        _self: llama_cpp.LlamaCppServer,
        *,
        readiness_timeout: Duration,
    ) -> None:
        raise primary_timeout

    async def clean_stop(_self: llama_cpp.LlamaCppServer) -> None:
        calls.append("stop")

    monkeypatch.setattr(llama_cpp.LlamaCppServer, "wait_ready", wait_timeout)
    monkeypatch.setattr(llama_cpp.LlamaCppServer, "stop", clean_stop)
    with pytest.raises(ServingReadinessTimeoutError) as raised:
        asyncio.run(
            llama_cpp.LlamaCppServer.start(
                config=_config(tmp_path),
                executor=_Executor([_result(command, out=f"{_ID}\n".encode())]),
            ),
        )
    assert raised.value is primary_timeout
    assert getattr(raised.value, "__notes__", None) is None
    assert calls == ["stop"]

    primary_cancelled = asyncio.CancelledError()
    cleanup_error = RuntimeError("x" * 10_000)
    calls.clear()

    async def wait_cancelled(
        _self: llama_cpp.LlamaCppServer,
        *,
        readiness_timeout: Duration,
    ) -> None:
        raise primary_cancelled

    async def failed_stop(_self: llama_cpp.LlamaCppServer) -> None:
        calls.append("stop")
        raise cleanup_error

    monkeypatch.setattr(llama_cpp.LlamaCppServer, "wait_ready", wait_cancelled)
    monkeypatch.setattr(llama_cpp.LlamaCppServer, "stop", failed_stop)
    with pytest.raises(asyncio.CancelledError) as cancelled:
        asyncio.run(
            llama_cpp.LlamaCppServer.start(
                config=_config(tmp_path),
                executor=_Executor([_result(command, out=f"{_ID}\n".encode())]),
            ),
        )
    assert cancelled.value is primary_cancelled
    assert calls == ["stop"]
    assert cancelled.value.__notes__ is not None
    assert len(cancelled.value.__notes__[0].encode("utf-8")) <= 4_096


def test_start_retains_primary_when_owned_remove_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A real owned remove failure remains supplemental to readiness failure."""
    primary = ServingReadinessTimeoutError("timeout")
    command = Command("docker")
    executor = _Executor(
        [
            _result(command, out=f"{_ID}\n".encode()),
            _result(command, out=b"false|true\n"),
            _result(command, 1, err=b"cannot remove"),
        ],
    )

    async def fail_ready(
        _self: llama_cpp.LlamaCppServer,
        *,
        readiness_timeout: Duration,
    ) -> None:
        raise primary

    monkeypatch.setattr(llama_cpp.LlamaCppServer, "wait_ready", fail_ready)
    with pytest.raises(ServingReadinessTimeoutError) as raised:
        asyncio.run(
            llama_cpp.LlamaCppServer.start(
                config=_config(tmp_path),
                executor=executor,
            ),
        )

    assert raised.value is primary
    assert primary.__notes__ is not None
    assert len(primary.__notes__) == 1
    assert "Owned llama.cpp container cleanup also failed" in primary.__notes__[0]
    assert "cannot remove" in primary.__notes__[0]
    assert len(primary.__notes__[0].encode("utf-8")) <= 4_096
    assert [item.arguments for item in executor.commands] == [
        executor.commands[0].arguments,
        (
            "inspect",
            "--format",
            (
                "{{.State.Running}}|"
                '{{index .Config.Labels "devtools.model_serving.managed"}}'
            ),
            _ID,
        ),
        ("rm", _ID),
    ]
