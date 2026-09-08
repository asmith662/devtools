# Copyright (c) 2026
"""Tests for concrete experimental vLLM serving lifecycle behavior."""

from __future__ import annotations

import asyncio
from dataclasses import FrozenInstanceError
from typing import TYPE_CHECKING

import pytest

from devtools.commands import Command, CommandNotFoundError, CommandResult
from devtools.model_serving import vllm
from devtools.model_serving.errors import (
    ServingReadinessTimeoutError,
    VLLMInspectionError,
    VLLMLaunchError,
    VLLMOwnershipError,
    VLLMStartupError,
    VLLMStopError,
)
from devtools.model_serving.huggingface import HuggingFaceModelRef
from devtools.model_serving.vllm import VLLMServer, VLLMServingConfig
from devtools.paths import ResolvedPath
from devtools.time import Duration

if TYPE_CHECKING:
    from pathlib import Path


_VALID_CONTAINER_ID = "a" * 64
_PREFETCH_OPTIONS = (
    "--offload-backend",
    "--offload-group-size",
    "--offload-num-in-group",
    "--offload-prefetch-step",
)
_WSL2_PIN_MEMORY_ENVIRONMENT = "VLLM_WSL2_ENABLE_PIN_MEMORY=1"
_CUDAGRAPH_MEMORY_ESTIMATE_ENVIRONMENT = "VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=0"
_COMBINED_ENVIRONMENT_OPTION_COUNT = 2


def _config(tmp_path: Path, **changes: object) -> VLLMServingConfig:
    """Create a compact valid vLLM configuration."""
    values: dict[str, object] = {
        "model": HuggingFaceModelRef("Qwen/Qwen3-8B", "a" * 40),
        "image": "vllm/vllm-openai:v0.26.0",
        "cache_root": ResolvedPath(tmp_path / "cache"),
        "host_port": 8123,
        "served_model_name": "qwen-local",
        "max_model_len": 2048,
        "gpu_memory_utilization": 0.8,
        "max_num_seqs": 1,
    }
    values.update(changes)
    return VLLMServingConfig(**values)  # type: ignore[arg-type]


def _result(
    command: Command,
    *,
    exit_code: int = 0,
    stdout: bytes = b"",
    stderr: bytes = b"diagnostic",
) -> CommandResult:
    """Create a compact ordinary command result."""
    return CommandResult(command, exit_code, stdout, stderr, Duration.seconds(0))


def _not_found_result(command: Command) -> CommandResult:
    """Create Docker's exact absent-container inspection result."""
    return _result(
        command,
        exit_code=1,
        stderr=f"Error: No such object: {_VALID_CONTAINER_ID}".encode(),
    )


def _assert_no_prefetch_arguments(command: Command) -> None:
    """Require that a historical command has no prefetch provider flags."""
    assert all(option not in command.arguments for option in _PREFETCH_OPTIONS)


class _Executor:
    """Record commands and return queued results or errors."""

    def __init__(self, responses: list[CommandResult | BaseException]) -> None:
        """Initialize queued execution behavior."""
        self.commands: list[Command] = []
        self._responses = responses

    async def execute(self, command: Command) -> CommandResult:
        """Record one command and apply the next planned outcome."""
        self.commands.append(command)
        response = self._responses.pop(0)
        if isinstance(response, BaseException):
            raise response

        return response


def test_config_is_immutable_hashable_and_preserves_defaults(tmp_path: Path) -> None:
    """A vLLM launch profile is an immutable reproducible value."""
    config = _config(tmp_path)

    assert config.trust_remote_code is False
    assert config.cpu_offload_gb == 0.0
    assert config.offload_backend is None
    assert config.offload_group_size == 0
    assert config.offload_num_in_group == 0
    assert config.offload_prefetch_step == 0
    assert config.wsl2_enable_pin_memory is False
    assert config.estimate_cudagraph_memory is True
    assert config == _config(tmp_path)
    assert hash(config) == hash(_config(tmp_path))

    with pytest.raises(FrozenInstanceError):
        config.host_port = 9000  # type: ignore[misc]


def test_server_exposes_config_and_start_facts(tmp_path: Path) -> None:
    """Live handles expose only their immutable launch and operational facts."""
    config = _config(tmp_path)
    started_at = __import__("devtools.time", fromlist=["Timestamp"]).Timestamp.now()
    server = VLLMServer(
        config=config,
        container_id=_VALID_CONTAINER_ID,
        container_name="devtools-vllm-test",
        executor=_Executor([]),  # type: ignore[arg-type]
        started_at=started_at,
    )

    assert server.config is config
    assert server.container_id == _VALID_CONTAINER_ID
    assert server.started_at is started_at


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("image", "vllm/vllm-openai", "image"),
        ("host_port", 0, "port"),
        ("host_port", 65_536, "port"),
        ("served_model_name", " ", "name"),
        ("max_model_len", 0, "length"),
        ("gpu_memory_utilization", 0.0, "utilization"),
        ("gpu_memory_utilization", 1.1, "utilization"),
        ("max_num_seqs", 0, "sequences"),
        ("cpu_offload_gb", -0.1, "offload"),
        ("cpu_offload_gb", float("nan"), "offload"),
        ("cpu_offload_gb", float("inf"), "offload"),
        ("offload_backend", "uva", "backend"),
        ("offload_group_size", 1, "require"),
    ],
)
def test_config_rejects_invalid_structural_values(
    tmp_path: Path,
    field: str,
    value: object,
    match: str,
) -> None:
    """Only explicit and structurally usable launch values are accepted."""
    with pytest.raises(ValueError, match=match):
        _config(tmp_path, **{field: value})


def test_start_builds_deterministic_owned_docker_launch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Launch uses Docker argv, explicit configuration, and an ownership label."""
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")

        return _result(command, stdout=b"true|true\n")

    executor.execute = execute  # type: ignore[method-assign]

    async def ready(_endpoint: str, _model: str) -> bool:
        return True

    monkeypatch.setattr("devtools.model_serving.vllm._probe_model_ready", ready)
    config = _config(tmp_path)
    server = asyncio.run(
        VLLMServer.start(
            config=config,
            executor=executor,  # type: ignore[arg-type]
            readiness_timeout=Duration.seconds(1),
        ),
    )

    command = executor.commands[0]
    assert command.executable == "docker"
    assert "--detach" in command.arguments
    assert "--rm" not in command.arguments
    assert "--gpus" in command.arguments
    assert "all" in command.arguments
    assert "--ipc" in command.arguments
    assert "host" in command.arguments
    assert "devtools.model_serving.managed=true" in command.arguments
    assert f"127.0.0.1:{config.host_port}:8000" in command.arguments
    expected_mount = f"type=bind,src={config.cache_root},dst=/root/.cache/huggingface"
    assert expected_mount in command.arguments
    assert config.image in command.arguments
    assert config.model.repository in command.arguments
    assert config.model.revision in command.arguments
    assert config.served_model_name in command.arguments
    assert str(config.max_model_len) in command.arguments
    assert str(config.gpu_memory_utilization) in command.arguments
    assert str(config.max_num_seqs) in command.arguments
    assert "--cpu-offload-gb" not in command.arguments
    _assert_no_prefetch_arguments(command)
    assert _WSL2_PIN_MEMORY_ENVIRONMENT not in command.arguments
    assert _CUDAGRAPH_MEMORY_ESTIMATE_ENVIRONMENT not in command.arguments
    assert "--trust-remote-code" not in command.arguments
    assert server.container_id == _VALID_CONTAINER_ID
    assert server.endpoint == "http://127.0.0.1:8123"
    assert server.cache_root == config.cache_root
    assert config.cache_root.value.is_dir()
    assert all(command.arguments[0] != "logs" for command in executor.commands)


def test_launch_adds_exact_positive_cpu_weight_offload(tmp_path: Path) -> None:
    """Positive model-weight offload is one explicit vLLM launch option."""
    config = _config(tmp_path, cpu_offload_gb=2.0)

    command = vllm._build_launch_command(config, "devtools-vllm-test")  # noqa: SLF001

    assert command.arguments.count("--cpu-offload-gb") == 1
    option = command.arguments.index("--cpu-offload-gb")
    assert command.arguments[option + 1] == "2.0"
    _assert_no_prefetch_arguments(command)
    assert _WSL2_PIN_MEMORY_ENVIRONMENT not in command.arguments
    assert _CUDAGRAPH_MEMORY_ESTIMATE_ENVIRONMENT not in command.arguments


def test_launch_adds_exact_wsl2_pinned_memory_environment(tmp_path: Path) -> None:
    """The opt-in applies only as one explicit Docker container environment."""
    command = vllm._build_launch_command(  # noqa: SLF001
        _config(tmp_path, wsl2_enable_pin_memory=True),
        "devtools-vllm-test",
    )

    assert command.arguments.count("--env") == 1
    option = command.arguments.index("--env")
    assert command.arguments[option + 1] == _WSL2_PIN_MEMORY_ENVIRONMENT
    assert "--cpu-offload-gb" not in command.arguments
    _assert_no_prefetch_arguments(command)
    assert _CUDAGRAPH_MEMORY_ESTIMATE_ENVIRONMENT not in command.arguments


def test_launch_adds_exact_disabled_cudagraph_memory_estimate_environment(
    tmp_path: Path,
) -> None:
    """Disabling estimate application is one explicit container-local opt-in."""
    command = vllm._build_launch_command(  # noqa: SLF001
        _config(tmp_path, estimate_cudagraph_memory=False),
        "devtools-vllm-test",
    )

    assert command.arguments.count("--env") == 1
    option = command.arguments.index("--env")
    assert command.arguments[option + 1] == _CUDAGRAPH_MEMORY_ESTIMATE_ENVIRONMENT
    assert _WSL2_PIN_MEMORY_ENVIRONMENT not in command.arguments
    assert "--cpu-offload-gb" not in command.arguments
    _assert_no_prefetch_arguments(command)


def test_prefetch_offload_requires_complete_isolated_configuration(
    tmp_path: Path,
) -> None:
    """Prefetch is explicit and cannot accidentally combine with UVA offload."""
    config = _config(
        tmp_path,
        offload_backend="prefetch",
        offload_group_size=24,
        offload_num_in_group=5,
        offload_prefetch_step=1,
    )

    assert config.offload_backend == "prefetch"

    with pytest.raises(ValueError, match="UVA"):
        _config(
            tmp_path,
            cpu_offload_gb=2.0,
            offload_backend="prefetch",
            offload_group_size=24,
            offload_num_in_group=5,
            offload_prefetch_step=1,
        )
    with pytest.raises(ValueError, match="count"):
        _config(
            tmp_path,
            offload_backend="prefetch",
            offload_group_size=4,
            offload_num_in_group=5,
            offload_prefetch_step=1,
        )
    with pytest.raises(ValueError, match="group size"):
        _config(
            tmp_path,
            offload_backend="prefetch",
            offload_num_in_group=1,
            offload_prefetch_step=1,
        )
    with pytest.raises(ValueError, match="step"):
        _config(
            tmp_path,
            offload_backend="prefetch",
            offload_group_size=24,
            offload_num_in_group=5,
        )


def test_launch_adds_exact_prefetch_offload_arguments(tmp_path: Path) -> None:
    """Prefetch settings map once and only once to vLLM's provider argv."""
    command = vllm._build_launch_command(  # noqa: SLF001
        _config(
            tmp_path,
            offload_backend="prefetch",
            offload_group_size=24,
            offload_num_in_group=5,
            offload_prefetch_step=1,
            wsl2_enable_pin_memory=True,
            estimate_cudagraph_memory=False,
        ),
        "devtools-vllm-test",
    )

    assert "--cpu-offload-gb" not in command.arguments
    expected = {
        "--offload-backend": "prefetch",
        "--offload-group-size": "24",
        "--offload-num-in-group": "5",
        "--offload-prefetch-step": "1",
    }
    for option, value in expected.items():
        assert command.arguments.count(option) == 1
        assert command.arguments[command.arguments.index(option) + 1] == value
    assert command.arguments.count("--env") == _COMBINED_ENVIRONMENT_OPTION_COUNT
    environment_values = {
        command.arguments[index + 1]
        for index, argument in enumerate(command.arguments)
        if argument == "--env"
    }
    assert environment_values == {
        _WSL2_PIN_MEMORY_ENVIRONMENT,
        _CUDAGRAPH_MEMORY_ESTIMATE_ENVIRONMENT,
    }


def test_start_preserves_default_readiness_timeout(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Callers that omit the policy retain the historical ten-minute wait."""
    executor = _Executor([])
    observed: list[Duration] = []

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")

    async def ready(_self: VLLMServer, *, readiness_timeout: Duration) -> None:
        observed.append(readiness_timeout)

    executor.execute = execute  # type: ignore[method-assign]
    monkeypatch.setattr(VLLMServer, "wait_ready", ready)

    asyncio.run(VLLMServer.start(config=_config(tmp_path), executor=executor))  # type: ignore[arg-type]

    assert observed == [vllm.DEFAULT_READINESS_TIMEOUT]


def test_start_forwards_custom_readiness_timeout(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A caller-selected wait policy reaches readiness unchanged."""
    executor = _Executor([])
    observed: list[Duration] = []
    custom_timeout = Duration.seconds(37)

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")

    async def ready(_self: VLLMServer, *, readiness_timeout: Duration) -> None:
        observed.append(readiness_timeout)

    executor.execute = execute  # type: ignore[method-assign]
    monkeypatch.setattr(VLLMServer, "wait_ready", ready)

    asyncio.run(
        VLLMServer.start(
            config=_config(tmp_path),
            executor=executor,  # type: ignore[arg-type]
            readiness_timeout=custom_timeout,
        ),
    )

    assert observed == [custom_timeout]


def test_launch_honors_explicit_remote_code_opt_in(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Remote code is enabled only by a recorded explicit configuration choice."""
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")

        return _result(command, stdout=b"true|true\n")

    executor.execute = execute  # type: ignore[method-assign]

    async def ready(_endpoint: str, _model: str) -> bool:
        return True

    monkeypatch.setattr("devtools.model_serving.vllm._probe_model_ready", ready)
    asyncio.run(
        VLLMServer.start(
            config=_config(tmp_path, trust_remote_code=True),
            executor=executor,  # type: ignore[arg-type]
            readiness_timeout=Duration.seconds(1),
        ),
    )

    assert "--trust-remote-code" in executor.commands[0].arguments


def test_nonzero_docker_launch_raises_bounded_serving_error(tmp_path: Path) -> None:
    """A normal nonzero Docker result gains vLLM launch semantics."""
    command = Command("docker", ("run",))
    executor = _Executor([_result(command, exit_code=125)])

    with pytest.raises(VLLMLaunchError, match="exit code 125"):
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )


def test_missing_docker_error_propagates_unchanged(tmp_path: Path) -> None:
    """Command-domain missing-executable errors retain their native meaning."""
    executor = _Executor([CommandNotFoundError("docker not found")])

    with pytest.raises(CommandNotFoundError, match="not found"):
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )


def test_success_without_container_id_is_rejected(tmp_path: Path) -> None:
    """Docker success without detached identity cannot establish ownership."""
    executor = _Executor([_result(Command("docker", ("run",)))])

    with pytest.raises(VLLMLaunchError, match="exactly one valid"):
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )


def test_start_rejects_multiline_container_id_before_readiness(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Malformed detached output cannot establish a server or enter readiness."""
    commands: list[Command] = []

    async def execute(command: Command) -> CommandResult:
        commands.append(command)
        if command.arguments[0] == "run":
            return _result(
                command,
                stdout=b"noise\n" + _VALID_CONTAINER_ID.encode() + b"\n",
            )

        return _result(command, stdout=b"true|true\n")

    async def unexpected_probe(_endpoint: str, _model: str) -> bool:
        msg = "Readiness probe must not run after malformed launch output"
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.model_serving.vllm._probe_model_ready",
        unexpected_probe,
    )
    executor = _Executor([])
    executor.execute = execute  # type: ignore[method-assign]

    with pytest.raises(VLLMLaunchError, match="exactly one valid"):
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )

    assert [command.arguments[0] for command in commands] == ["run"]


@pytest.mark.parametrize(
    "stdout",
    [
        b" ",
        b"not-a-container-id",
        b"abc123 extra",
        b"a" * 63,
        b"a" * 65,
        b"noise\n" + b"a" * 64,
        b"a" * 64 + b"\nsecond-line",
    ],
)
def test_container_id_parser_rejects_malformed_docker_launch_output(
    stdout: bytes,
) -> None:
    """Successful detached launch output must be exactly one Docker full ID."""
    with pytest.raises(VLLMLaunchError, match="exactly one valid"):
        vllm._parse_container_id(_result(Command("docker"), stdout=stdout))  # noqa: SLF001


def test_container_id_parser_accepts_one_full_id_with_trailing_newline() -> None:
    """Normal Docker detached output contains one full ID and a line ending."""
    result = _result(Command("docker"), stdout=_VALID_CONTAINER_ID.encode() + b"\n")

    assert vllm._parse_container_id(result) == _VALID_CONTAINER_ID  # noqa: SLF001


def test_readiness_timeout_stops_owned_container(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A failed promise of readiness does not leak the just-launched container."""
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"true|true\n")

        return _result(command)

    executor.execute = execute  # type: ignore[method-assign]

    async def not_ready(_endpoint: str, _model: str) -> bool:
        return False

    monkeypatch.setattr("devtools.model_serving.vllm._probe_model_ready", not_ready)

    with pytest.raises(ServingReadinessTimeoutError, match=r"0\.01 seconds"):
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
                readiness_timeout=Duration.seconds(0.01),
            ),
        )

    assert [command.arguments[0] for command in executor.commands] == [
        "run",
        "inspect",
        "inspect",
        "stop",
        "rm",
    ]
    assert executor.commands[-1].arguments[-1] == _VALID_CONTAINER_ID


def test_wait_ready_rejects_nonpositive_timeout(tmp_path: Path) -> None:
    """Readiness waiting requires a caller-supplied positive allowance."""
    server = VLLMServer(
        config=_config(tmp_path),
        container_id=_VALID_CONTAINER_ID,
        container_name="devtools-vllm-test",
        executor=_Executor([]),  # type: ignore[arg-type]
        started_at=__import__("devtools.time", fromlist=["Timestamp"]).Timestamp.now(),
    )

    with pytest.raises(ValueError, match="positive"):
        asyncio.run(server.wait_ready(readiness_timeout=Duration.seconds(0)))


def test_cancellation_during_readiness_stops_owned_container(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Cancellation preserves its identity while attempting exact owned cleanup."""
    executor = _Executor([])
    inspected = asyncio.Event()

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            inspected.set()
            return _result(command, stdout=b"true|true\n")

        return _result(command)

    executor.execute = execute  # type: ignore[method-assign]

    async def not_ready(_endpoint: str, _model: str) -> bool:
        return False

    monkeypatch.setattr("devtools.model_serving.vllm._probe_model_ready", not_ready)

    async def run() -> None:
        task = asyncio.create_task(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )
        await inspected.wait()
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(run())

    assert [command.arguments[0] for command in executor.commands[-2:]] == [
        "stop",
        "rm",
    ]


def test_cancellation_preserves_identity_when_removal_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A cleanup-removal failure becomes a note on the same cancellation."""
    primary = asyncio.CancelledError("primary cancellation")
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"false|true\n")
        return _result(command, exit_code=1, stderr=b"cannot remove after cancel")

    async def cancelled_wait(
        _server: VLLMServer,
        *,
        readiness_timeout: Duration,
    ) -> None:
        del readiness_timeout
        raise primary

    executor.execute = execute  # type: ignore[method-assign]
    monkeypatch.setattr(VLLMServer, "wait_ready", cancelled_wait)

    with pytest.raises(asyncio.CancelledError) as raised:
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )

    assert raised.value is primary
    assert primary.__notes__ == [
        (
            "Owned vLLM container cleanup also failed: "
            "Docker could not remove owned vLLM container "
            f"'{_VALID_CONTAINER_ID}'. cannot remove after cancel"
        ),
    ]
    assert [command.arguments[0] for command in executor.commands] == [
        "run",
        "inspect",
        "rm",
    ]


def test_readiness_timeout_preserves_primary_when_removal_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A removal failure is noted without replacing an elapsed timeout."""
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"true|true\n")
        if command.arguments[0] == "stop":
            return _result(command)
        return _result(command, exit_code=1, stderr=b"cannot remove after timeout")

    async def not_ready(_endpoint: str, _model: str) -> bool:
        return False

    executor.execute = execute  # type: ignore[method-assign]
    monkeypatch.setattr("devtools.model_serving.vllm._probe_model_ready", not_ready)

    with pytest.raises(ServingReadinessTimeoutError) as raised:
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
                readiness_timeout=Duration.seconds(0.01),
            ),
        )

    assert raised.value.__notes__ == [
        (
            "Owned vLLM container cleanup also failed: "
            "Docker could not remove owned vLLM container "
            f"'{_VALID_CONTAINER_ID}'. cannot remove after timeout"
        ),
    ]
    assert executor.commands[-1].arguments == ("rm", _VALID_CONTAINER_ID)


def test_early_container_exit_preserves_bounded_provider_log_tail(
    tmp_path: Path,
) -> None:
    """An early exit retains the newest bounded exact-container provider logs."""
    executor = _Executor([])
    provider_stdout = b"\xff" * (vllm._PROVIDER_LOG_TAIL_BYTES + 10)  # noqa: SLF001
    provider_stderr = b"CUDA out of memory"

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"false|true\n")
        if command.arguments[0] == "logs":
            return _result(command, stdout=provider_stdout, stderr=provider_stderr)
        return _result(command)

    executor.execute = execute  # type: ignore[method-assign]

    with pytest.raises(VLLMStartupError, match="stopped") as raised:
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )

    assert raised.value.provider_log_tail is not None
    assert raised.value.provider_log_tail.endswith("CUDA out of memory")
    assert len(raised.value.provider_log_tail.encode()) <= vllm._PROVIDER_LOG_TAIL_BYTES  # noqa: SLF001
    assert not getattr(raised.value, "__notes__", [])
    assert [command.arguments[0] for command in executor.commands] == [
        "run",
        "inspect",
        "logs",
        "inspect",
        "rm",
    ]
    assert executor.commands[2].arguments[-1] == _VALID_CONTAINER_ID


def test_early_container_exit_preserves_startup_error_when_removal_fails(
    tmp_path: Path,
) -> None:
    """A failed removal is noted without replacing the provider-exit error."""
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"false|true\n")
        if command.arguments[0] == "logs":
            return _result(command, stdout=b"CUDA out of memory", stderr=b"")
        return _result(command, exit_code=1, stderr=b"cannot remove owned container")

    executor.execute = execute  # type: ignore[method-assign]

    with pytest.raises(VLLMStartupError, match="stopped") as raised:
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )

    assert raised.value.provider_log_tail == "CUDA out of memory"
    assert raised.value.__notes__ == [
        (
            "Owned vLLM container cleanup also failed: "
            "Docker could not remove owned vLLM container "
            f"'{_VALID_CONTAINER_ID}'. cannot remove owned container"
        ),
    ]
    assert [command.arguments[0] for command in executor.commands] == [
        "run",
        "inspect",
        "logs",
        "inspect",
        "rm",
    ]


def test_early_container_exit_preserves_startup_error_when_logs_fail(
    tmp_path: Path,
) -> None:
    """A secondary Docker-log failure cannot replace the primary startup error."""
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"false|true\n")
        if command.arguments[0] == "logs":
            return _result(command, exit_code=1, stderr=b"logs unavailable")
        return _result(command)

    executor.execute = execute  # type: ignore[method-assign]

    with pytest.raises(VLLMStartupError, match="stopped") as raised:
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )

    assert raised.value.provider_log_tail is None
    assert executor.commands[-1].arguments == ("rm", _VALID_CONTAINER_ID)


def test_early_container_exit_preserves_startup_error_when_log_command_raises(
    tmp_path: Path,
) -> None:
    """An operational log-command error remains secondary to startup failure."""
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"false|true\n")
        if command.arguments[0] == "logs":
            msg = "docker logs unavailable"
            raise RuntimeError(msg)
        return _result(command)

    executor.execute = execute  # type: ignore[method-assign]

    with pytest.raises(VLLMStartupError, match="stopped") as raised:
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )

    assert raised.value.provider_log_tail is None
    assert executor.commands[-1].arguments == ("rm", _VALID_CONTAINER_ID)


def test_status_distinguishes_running_ready_and_stopped(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Status keeps exact-container liveness separate from endpoint readiness."""
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        return _result(command, stdout=b"true|true\n")

    executor.execute = execute  # type: ignore[method-assign]

    async def ready(_endpoint: str, _model: str) -> bool:
        return True

    monkeypatch.setattr("devtools.model_serving.vllm._probe_model_ready", ready)
    server = VLLMServer(
        config=_config(tmp_path),
        container_id=_VALID_CONTAINER_ID,
        container_name="devtools-vllm-test",
        executor=executor,  # type: ignore[arg-type]
        started_at=__import__("devtools.time", fromlist=["Timestamp"]).Timestamp.now(),
    )

    assert asyncio.run(server.status()).container_running is True
    assert asyncio.run(server.status()).model_ready is True

    async def stopped(command: Command) -> CommandResult:
        return _result(command, stdout=b"false|true\n")

    executor.execute = stopped  # type: ignore[method-assign]
    status = asyncio.run(server.status())
    assert status.container_running is False
    assert status.model_ready is False

    async def missing(command: Command) -> CommandResult:
        return _not_found_result(command)

    executor.execute = missing  # type: ignore[method-assign]
    assert asyncio.run(server.status()).container_running is False


def test_stop_requires_ownership_and_is_idempotent(tmp_path: Path) -> None:
    """Stop uses retained exact ID and refuses unlabeled containers."""
    config = _config(tmp_path)
    server: VLLMServer

    async def wrong_label(command: Command) -> CommandResult:
        return _result(command, stdout=b"true|\n")

    executor = _Executor([])
    executor.execute = wrong_label  # type: ignore[method-assign]
    server = VLLMServer(
        config=config,
        container_id=_VALID_CONTAINER_ID,
        container_name="devtools-vllm-test",
        executor=executor,  # type: ignore[arg-type]
        started_at=__import__("devtools.time", fromlist=["Timestamp"]).Timestamp.now(),
    )

    with pytest.raises(VLLMOwnershipError):
        asyncio.run(server.stop())

    commands: list[Command] = []

    async def missing(command: Command) -> CommandResult:
        commands.append(command)
        return _not_found_result(command)

    executor.execute = missing  # type: ignore[method-assign]
    asyncio.run(server.stop())

    assert commands[0].arguments[-1] == _VALID_CONTAINER_ID
    assert len(commands) == 1


def test_inspection_operational_failure_surfaces_without_http_or_stop(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Unknown Docker state is not silently converted to a stopped server."""
    commands: list[Command] = []

    async def execute(command: Command) -> CommandResult:
        commands.append(command)
        return _result(command, exit_code=1, stderr=b"Cannot connect to daemon")

    async def unexpected_probe(_endpoint: str, _model: str) -> bool:
        msg = "HTTP probe must not run after inspect failure"
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.model_serving.vllm._probe_model_ready",
        unexpected_probe,
    )
    executor = _Executor([])
    executor.execute = execute  # type: ignore[method-assign]
    server = VLLMServer(
        config=_config(tmp_path),
        container_id=_VALID_CONTAINER_ID,
        container_name="devtools-vllm-test",
        executor=executor,  # type: ignore[arg-type]
        started_at=__import__("devtools.time", fromlist=["Timestamp"]).Timestamp.now(),
    )

    with pytest.raises(VLLMInspectionError, match="Cannot connect"):
        asyncio.run(server.status())

    with pytest.raises(VLLMInspectionError, match="Cannot connect"):
        asyncio.run(server.stop())

    assert [command.arguments[0] for command in commands] == ["inspect", "inspect"]


def test_different_container_not_found_does_not_establish_absence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A missing-object diagnostic must name this handle's exact container."""
    different_container_id = "b" * 64

    async def execute(command: Command) -> CommandResult:
        return _result(
            command,
            exit_code=1,
            stderr=(f"Error: No such object: {different_container_id}").encode(),
        )

    async def unexpected_probe(_endpoint: str, _model: str) -> bool:
        msg = "HTTP probe must not run after inspect failure"
        raise AssertionError(msg)

    monkeypatch.setattr(
        "devtools.model_serving.vllm._probe_model_ready",
        unexpected_probe,
    )
    executor = _Executor([])
    executor.execute = execute  # type: ignore[method-assign]
    server = VLLMServer(
        config=_config(tmp_path),
        container_id=_VALID_CONTAINER_ID,
        container_name="devtools-vllm-test",
        executor=executor,  # type: ignore[arg-type]
        started_at=__import__("devtools.time", fromlist=["Timestamp"]).Timestamp.now(),
    )

    with pytest.raises(VLLMInspectionError, match="No such object"):
        asyncio.run(server.status())


def test_startup_cleanup_preserves_primary_failure_when_inspection_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Timeout remains authoritative when secondary owned cleanup is uncertain."""
    executor = _Executor([])
    inspection_count = 0

    async def execute(command: Command) -> CommandResult:
        nonlocal inspection_count
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            inspection_count += 1
            if inspection_count == 1:
                return _result(command, stdout=b"true|true\n")
            return _result(command, exit_code=1, stderr=b"Cannot connect to daemon")
        msg = "Unsafe docker stop must not run"
        raise AssertionError(msg)

    async def not_ready(_endpoint: str, _model: str) -> bool:
        return False

    executor.execute = execute  # type: ignore[method-assign]
    monkeypatch.setattr("devtools.model_serving.vllm._probe_model_ready", not_ready)

    with pytest.raises(ServingReadinessTimeoutError):
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
                readiness_timeout=Duration.seconds(0.01),
            ),
        )


def test_startup_cleanup_preserves_cancelled_error_identity(
    tmp_path: Path,
) -> None:
    """Secondary inspect failure never replaces the original cancellation object."""
    primary = asyncio.CancelledError("primary")
    executor = _Executor([])

    async def execute(command: Command) -> CommandResult:
        if command.arguments[0] == "run":
            return _result(command, stdout=_VALID_CONTAINER_ID.encode() + b"\n")
        if command.arguments[0] == "inspect":
            inspections = [
                item for item in executor.commands if item.arguments[0] == "inspect"
            ]
            if len(inspections) == 1:
                raise primary
            return _result(command, exit_code=1, stderr=b"Cannot connect to daemon")
        msg = "Unsafe docker stop must not run"
        raise AssertionError(msg)

    original_execute = execute

    async def recording_execute(command: Command) -> CommandResult:
        executor.commands.append(command)
        return await original_execute(command)

    executor.execute = recording_execute  # type: ignore[method-assign]

    with pytest.raises(asyncio.CancelledError) as raised:
        asyncio.run(
            VLLMServer.start(
                config=_config(tmp_path),
                executor=executor,  # type: ignore[arg-type]
            ),
        )

    assert raised.value is primary


def test_stop_handles_owned_stopped_and_docker_stop_failure(tmp_path: Path) -> None:
    """An owned stopped container is harmless, while failed stop is explicit."""
    executor = _Executor([])
    commands: list[Command] = []

    async def stopped(command: Command) -> CommandResult:
        commands.append(command)
        return _result(command, stdout=b"false|true\n")

    executor.execute = stopped  # type: ignore[method-assign]
    server = VLLMServer(
        config=_config(tmp_path),
        container_id=_VALID_CONTAINER_ID,
        container_name="devtools-vllm-test",
        executor=executor,  # type: ignore[arg-type]
        started_at=__import__("devtools.time", fromlist=["Timestamp"]).Timestamp.now(),
    )
    asyncio.run(server.stop())
    assert [command.arguments[0] for command in commands] == ["inspect", "rm"]

    async def failed_stop(command: Command) -> CommandResult:
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"true|true\n")
        return _result(command, exit_code=1, stdout=b"cannot stop")

    executor.execute = failed_stop  # type: ignore[method-assign]
    with pytest.raises(VLLMStopError, match="diagnostic"):
        asyncio.run(server.stop())

    async def failed_stop_without_diagnostic(command: Command) -> CommandResult:
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"true|true\n")
        return CommandResult(command, 1, b"", b"", Duration.seconds(0))

    executor.execute = failed_stop_without_diagnostic  # type: ignore[method-assign]
    with pytest.raises(VLLMStopError, match=_VALID_CONTAINER_ID):
        asyncio.run(server.stop())

    async def failed_removal(command: Command) -> CommandResult:
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"false|true\n")
        return _result(command, exit_code=1, stdout=b"cannot remove", stderr=b"")

    executor.execute = failed_removal  # type: ignore[method-assign]
    with pytest.raises(VLLMStopError, match="cannot remove"):
        asyncio.run(server.stop())

    async def failed_removal_without_diagnostic(command: Command) -> CommandResult:
        if command.arguments[0] == "inspect":
            return _result(command, stdout=b"false|true\n")
        return CommandResult(command, 1, b"", b"", Duration.seconds(0))

    executor.execute = failed_removal_without_diagnostic  # type: ignore[method-assign]
    with pytest.raises(VLLMStopError, match=_VALID_CONTAINER_ID):
        asyncio.run(server.stop())


def test_failed_start_cleanup_notes_secondary_cleanup_error(
    tmp_path: Path,
) -> None:
    """Cleanup never replaces the primary lifecycle failure."""
    primary = VLLMStartupError("primary", provider_log_tail=None)
    server = VLLMServer(
        config=_config(tmp_path),
        container_id=_VALID_CONTAINER_ID,
        container_name="devtools-vllm-test",
        executor=_Executor([RuntimeError()]),  # type: ignore[arg-type]
        started_at=__import__("devtools.time", fromlist=["Timestamp"]).Timestamp.now(),
    )

    asyncio.run(server._stop_after_unsuccessful_start(primary))  # noqa: SLF001

    assert primary.__notes__ == [
        "Owned vLLM container cleanup also failed: RuntimeError",
    ]


def test_internal_parsing_and_diagnostics_cover_invalid_docker_output() -> None:
    """Malformed operational output remains safely non-running or bounded."""
    command = Command("docker")
    malformed = _result(command, stdout=b"not-an-inspection")
    with pytest.raises(VLLMInspectionError):
        vllm._parse_inspection(malformed)  # noqa: SLF001
    multiline = _result(command, stdout=b"true|true\nfalse|true\n")
    with pytest.raises(VLLMInspectionError, match="single state"):
        vllm._parse_inspection(multiline)  # noqa: SLF001
    assert vllm._diagnostic_text(b"x" * 5_000) == "x" * 4_096  # noqa: SLF001
    assert vllm._launch_error_message(_result(command, exit_code=1)) == (  # noqa: SLF001
        "Docker rejected vLLM launch with exit code 1. diagnostic"
    )
    stdout_only = CommandResult(command, 1, b"stdout", b"", Duration.seconds(0))
    assert vllm._launch_error_message(stdout_only).endswith("stdout")  # noqa: SLF001


def test_probe_model_ready_interprets_only_matching_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Readiness requires both health and the configured served model identity."""
    responses = [
        (503, ""),
        (200, ""),
        (503, ""),
        (200, ""),
        (200, "not json"),
        (200, ""),
        (200, "{}"),
        (200, ""),
        (200, '{"data": [{"id": "other"}]}'),
        (200, ""),
        (200, '{"data": [{"id": "wanted"}]}'),
    ]

    async def get(_endpoint: str, _path: str) -> tuple[int, str]:
        return responses.pop(0)

    monkeypatch.setattr("devtools.model_serving.vllm._http_get", get)
    assert asyncio.run(vllm._probe_model_ready("http://host", "wanted")) is False  # noqa: SLF001
    assert asyncio.run(vllm._probe_model_ready("http://host", "wanted")) is False  # noqa: SLF001
    assert asyncio.run(vllm._probe_model_ready("http://host", "wanted")) is False  # noqa: SLF001
    assert asyncio.run(vllm._probe_model_ready("http://host", "wanted")) is False  # noqa: SLF001
    assert asyncio.run(vllm._probe_model_ready("http://host", "wanted")) is False  # noqa: SLF001
    assert asyncio.run(vllm._probe_model_ready("http://host", "wanted")) is True  # noqa: SLF001


def test_http_get_handles_unusable_or_refused_endpoints() -> None:
    """Provider-local probing treats malformed or unavailable endpoints as down."""
    assert asyncio.run(vllm._http_get("relative", "/health")) == (0, "")  # noqa: SLF001
    assert asyncio.run(vllm._http_get("http://127.0.0.1:1", "/health")) == (  # noqa: SLF001
        0,
        "",
    )


def test_http_get_parses_and_rejects_malformed_provider_responses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The provider-local probe accepts only minimally valid HTTP responses."""
    responses = [
        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{}",
        b"not-http",
        b"HTTP/1.1\r\n\r\n",
        b"HTTP/1.1 nope\r\n\r\n",
    ]

    class Reader:
        """Return one planned wire response."""

        async def read(self, _size: int) -> bytes:
            """Return planned bytes."""
            return responses.pop(0)

    class Writer:
        """Record the minimal connection-close behavior."""

        def write(self, _data: bytes) -> None:
            """Accept request bytes."""

        async def drain(self) -> None:
            """Model a successful drain."""

        def close(self) -> None:
            """Model connection closure."""

        async def wait_closed(self) -> None:
            """Model successful close completion."""

    async def connection(_host: str, _port: int) -> tuple[Reader, Writer]:
        return Reader(), Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)
    assert asyncio.run(vllm._http_get("http://host", "/health")) == (200, "{}")  # noqa: SLF001
    assert asyncio.run(vllm._http_get("http://host", "/health")) == (0, "")  # noqa: SLF001
    assert asyncio.run(vllm._http_get("http://host", "/health")) == (0, "")  # noqa: SLF001
    assert asyncio.run(vllm._http_get("http://host", "/health")) == (0, "")  # noqa: SLF001
