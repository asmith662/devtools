# Copyright (c) 2026
# ruff: noqa: E501, EM101, FBT001, INP001, PLR2004, PT011, PT018, SLF001, TRY003
"""Tests for the Qwen-specific persistent llama.cpp service command."""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from devtools.commands import Command, CommandResult
from devtools.model_serving.huggingface import AcquiredGGUF
from devtools.paths import ResolvedPath
from devtools.time import Duration

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import ModuleType


_SCRIPT_DIRECTORY = Path("scripts/model_benchmarks").resolve()
_SERVICE_PATH = _SCRIPT_DIRECTORY / "qwen38_llama_cpp_service.py"
_ID = "a" * 64


@pytest.fixture
def service() -> Iterator[ModuleType]:
    """Load the tracked operational script without making scripts a package."""
    sys.path.insert(0, str(_SCRIPT_DIRECTORY))
    specification = importlib.util.spec_from_file_location(
        "test_qwen38_llama_cpp_service",
        _SERVICE_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    try:
        specification.loader.exec_module(module)
        yield module
    finally:
        sys.path.remove(str(_SCRIPT_DIRECTORY))
        sys.modules.pop(specification.name, None)


def _result(
    command: Command,
    code: int = 0,
    out: bytes = b"",
    err: bytes = b"",
) -> CommandResult:
    return CommandResult(command, code, out, err, Duration.seconds(0))


class _Executor:
    def __init__(self, values: list[CommandResult]) -> None:
        self.commands: list[Command] = []
        self._values = values

    async def execute(self, command: Command) -> CommandResult:
        self.commands.append(command)
        return self._values.pop(0)


def _inspection(
    service: ModuleType,
    *,
    running: bool,
    fingerprint: str | None = None,
    service_label: str | None = None,
    port: int | str = 8080,
) -> bytes:
    return (
        f"{_ID}|{str(running).lower()}|"
        f"{service_label if service_label is not None else service._SERVICE_VALUE}|"
        f"{fingerprint if fingerprint is not None else service.profile_fingerprint()}|{port}\n"
    ).encode()


def _absent(service: ModuleType) -> CommandResult:
    return _result(
        Command("docker"),
        1,
        err=f"Error: No such object: {service._CONTAINER_NAME}".encode(),
    )


def _acquired(service: ModuleType, tmp_path: Path) -> AcquiredGGUF:
    semantic = tmp_path / service.QWEN38_27B_UD_IQ4_XS.model.filename
    semantic.write_bytes(b"GGUF")
    return AcquiredGGUF(
        service.QWEN38_27B_UD_IQ4_XS.model,
        ResolvedPath(tmp_path),
        ResolvedPath(semantic),
    )


def _patch_acquisition_and_port(
    monkeypatch: pytest.MonkeyPatch,
    service: ModuleType,
    acquired: AcquiredGGUF,
) -> None:
    async def acquire(**_kwargs: object) -> AcquiredGGUF:
        return acquired

    monkeypatch.setattr(service, "acquire_huggingface_gguf", acquire)
    monkeypatch.setattr(service, "_assert_host_port_available", lambda _port: None)


def test_profile_fingerprint_and_configuration_are_canonical(
    service: ModuleType,
    tmp_path: Path,
) -> None:
    """The command derives all provider flags from the tracked Qwen profile."""
    profile = service.QWEN38_27B_UD_IQ4_XS
    assert service.profile_fingerprint() == service.profile_fingerprint()
    config = service._serving_config(ResolvedPath(tmp_path / profile.model.filename), 8080)
    assert config.model.path.value.name == profile.model.filename
    assert config.image == profile.image_build_identity
    assert config.context_size == 32_768 and config.n_cpu_ffn == 0
    assert config.gpu_layers == "all" and config.flash_attention == "on"
    assert config.cache_type_k == config.cache_type_v == "q4_0"
    assert config.parallel_sequences == 1


def test_inspection_classifies_required_states(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Status distinguishes absence, ownership, readiness, and drift."""
    fingerprint = service.profile_fingerprint()

    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", ready)
    cases = [
        (_absent(service), service.PersistentQwenServiceState.ABSENT),
        (
            _result(Command("docker"), out=_inspection(service, running=False)),
            service.PersistentQwenServiceState.STOPPED,
        ),
        (
            _result(Command("docker"), out=_inspection(service, running=True)),
            service.PersistentQwenServiceState.READY,
        ),
        (
            _result(
                Command("docker"),
                out=_inspection(service, running=True, service_label="foreign"),
            ),
            service.PersistentQwenServiceState.CONFLICT,
        ),
        (
            _result(
                Command("docker"),
            out=_inspection(service, running=True, fingerprint="b" * 64),
            ),
            service.PersistentQwenServiceState.PROFILE_MISMATCH,
        ),
    ]
    for result, expected in cases:
        status = asyncio.run(
            service.inspect_service(
                executor=_Executor([result]),
                expected_fingerprint=fingerprint,
            ),
        )
        assert status.state is expected


def test_inspection_reports_loading_and_requested_port_mismatch(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Running health and start-port compatibility remain distinct facts."""
    async def loading(_: str) -> bool:
        return False

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", loading)
    loading_status = asyncio.run(
        service.inspect_service(
            executor=_Executor([_result(Command("docker"), out=_inspection(service, running=True))]),
            expected_fingerprint=service.profile_fingerprint(),
        ),
    )
    assert loading_status.state is service.PersistentQwenServiceState.RUNNING_LOADING
    assert loading_status.container_running and not loading_status.model_ready

    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", ready)
    port_status = asyncio.run(
        service.inspect_service(
            executor=_Executor([_result(Command("docker"), out=_inspection(service, running=True))]),
            expected_fingerprint=service.profile_fingerprint(),
            requested_port=8123,
        ),
    )
    assert port_status.state is service.PersistentQwenServiceState.PORT_MISMATCH


@pytest.mark.parametrize(
    "fingerprint",
    [
        pytest.param("<no value>", id="missing"),
        pytest.param("", id="empty"),
        pytest.param("stale", id="arbitrary-text"),
        pytest.param("a" * 63, id="short"),
        pytest.param("a" * 65, id="long"),
        pytest.param("g" + "a" * 63, id="nonhex"),
    ],
)
def test_malformed_fingerprint_is_conflict_without_lifecycle_authority(
    service: ModuleType,
    fingerprint: str,
) -> None:
    """Incomplete fingerprint metadata never grants stop or recreate authority."""
    inspection = _result(
        Command("docker"),
        out=_inspection(service, running=False, fingerprint=fingerprint),
    )
    status = asyncio.run(
        service.inspect_service(
            executor=_Executor([inspection]),
            expected_fingerprint=service.profile_fingerprint(),
        ),
    )
    assert status.state is service.PersistentQwenServiceState.CONFLICT

    start_executor = _Executor([inspection])
    with pytest.raises(service.PersistentQwenServiceError, match="foreign"):
        asyncio.run(
            service.start_service(
                cache_root=ResolvedPath(Path.cwd()),
                host_port=8080,
                readiness_timeout=Duration.seconds(1),
                executor=start_executor,
            ),
        )
    assert len(start_executor.commands) == 1

    stop_executor = _Executor([inspection])
    with pytest.raises(service.PersistentQwenServiceError, match="foreign"):
        asyncio.run(service.stop_service(executor=stop_executor))
    assert len(stop_executor.commands) == 1


@pytest.mark.parametrize(
    "port",
    [
        pytest.param("<no value>", id="missing"),
        pytest.param("", id="empty"),
        pytest.param("bad", id="nonnumeric"),
        pytest.param("0", id="zero"),
        pytest.param("65536", id="out-of-range"),
    ],
)
def test_malformed_port_is_conflict_without_lifecycle_authority(
    service: ModuleType,
    port: str,
) -> None:
    """Malformed port metadata is not a stale owned-service port selection."""
    inspection = _result(Command("docker"), out=_inspection(service, running=False, port=port))
    status = asyncio.run(
        service.inspect_service(
            executor=_Executor([inspection]),
            expected_fingerprint=service.profile_fingerprint(),
        ),
    )
    assert status.state is service.PersistentQwenServiceState.CONFLICT

    start_executor = _Executor([inspection])
    with pytest.raises(service.PersistentQwenServiceError, match="foreign"):
        asyncio.run(
            service.start_service(
                cache_root=ResolvedPath(Path.cwd()),
                host_port=8080,
                readiness_timeout=Duration.seconds(1),
                executor=start_executor,
            ),
        )
    assert len(start_executor.commands) == 1

    stop_executor = _Executor([inspection])
    with pytest.raises(service.PersistentQwenServiceError, match="foreign"):
        asyncio.run(service.stop_service(executor=stop_executor))
    assert len(stop_executor.commands) == 1


def test_start_absent_acquires_semantic_artifact_launches_and_waits(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """An absent service is created from selected profile and semantic GGUF path."""
    acquired = _acquired(service, tmp_path)
    _patch_acquisition_and_port(monkeypatch, service, acquired)

    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", ready)
    executor = _Executor(
        [
            _absent(service),
            _result(Command("docker"), out=f"{_ID}\n".encode()),
            _result(Command("docker"), out=_inspection(service, running=True)),
        ],
    )

    status = asyncio.run(
        service.start_service(
            cache_root=ResolvedPath(tmp_path),
            host_port=8080,
            readiness_timeout=Duration.seconds(1),
            executor=executor,
        ),
    )

    launch = executor.commands[1]
    assert status.state is service.PersistentQwenServiceState.READY
    assert launch.arguments[0:4] == ("run", "--detach", "--name", service._CONTAINER_NAME)
    assert service.QWEN38_27B_UD_IQ4_XS.image_build_identity in launch.arguments
    assert "--n-cpu-ffn" not in launch.arguments
    assert "127.0.0.1:8080:8080" in launch.arguments
    assert f"devtools.qwen.persistent-service={service._SERVICE_VALUE}" in launch.arguments
    assert f"devtools.qwen.profile-sha256={service.profile_fingerprint()}" in launch.arguments
    assert "devtools.qwen.host-port=8080" in launch.arguments
    assert f"/models/{acquired.path.value.name}" in launch.arguments
    assert "--restart" not in launch.arguments


def test_start_ready_is_idempotent_without_model_acquisition(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A matching ready service remains running and no new Docker run occurs."""
    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", ready)
    executor = _Executor([_result(Command("docker"), out=_inspection(service, running=True))])

    status = asyncio.run(
        service.start_service(
            cache_root=ResolvedPath(Path.cwd()),
            host_port=8080,
            readiness_timeout=Duration.seconds(1),
            executor=executor,
        ),
    )

    assert status.state is service.PersistentQwenServiceState.READY
    assert len(executor.commands) == 1


def test_start_waits_for_matching_loading_service(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A matching loading service is waited for rather than recreated."""
    ready_values = iter((False, True))

    async def readiness(_: str) -> bool:
        return next(ready_values)

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", readiness)

    async def immediate_sleep(_: float) -> None:
        return None

    monkeypatch.setattr(service.asyncio, "sleep", immediate_sleep)
    executor = _Executor(
        [
            _result(Command("docker"), out=_inspection(service, running=True)),
            _result(Command("docker"), out=_inspection(service, running=True)),
        ],
    )

    status = asyncio.run(
        service.start_service(
            cache_root=ResolvedPath(Path.cwd()),
            host_port=8080,
            readiness_timeout=Duration.seconds(1),
            executor=executor,
        ),
    )
    assert status.state is service.PersistentQwenServiceState.READY
    assert all(command.arguments[0] == "inspect" for command in executor.commands)


@pytest.mark.parametrize("running", [False, True])
def test_start_refuses_foreign_same_name_container(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    running: bool,
) -> None:
    """Name collisions never grant lifecycle authority over foreign containers."""
    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", ready)
    executor = _Executor(
        [
            _result(
                Command("docker"),
                out=_inspection(service, running=running, service_label="foreign"),
            ),
        ],
    )
    with pytest.raises(service.PersistentQwenServiceError, match="foreign"):
        asyncio.run(
            service.start_service(
                cache_root=ResolvedPath(Path.cwd()),
                host_port=8080,
                readiness_timeout=Duration.seconds(1),
                executor=executor,
            ),
        )
    assert len(executor.commands) == 1


@pytest.mark.parametrize("running", [False, True])
def test_start_handles_stale_profile_by_running_state(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    running: bool,
) -> None:
    """Running stale services require an explicit stop; stopped ones are recreated."""
    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", ready)
    stale = _result(Command("docker"), out=_inspection(service, running=running, fingerprint="b" * 64))
    if running:
        executor = _Executor([stale])
        with pytest.raises(service.PersistentQwenServiceError, match="stop it explicitly"):
            asyncio.run(
                service.start_service(
                    cache_root=ResolvedPath(tmp_path),
                    host_port=8080,
                    readiness_timeout=Duration.seconds(1),
                    executor=executor,
                ),
            )
        assert len(executor.commands) == 1
        return

    acquired = _acquired(service, tmp_path)
    _patch_acquisition_and_port(monkeypatch, service, acquired)
    executor = _Executor(
        [
            stale,
            _result(Command("docker")),
            _result(Command("docker"), out=f"{_ID}\n".encode()),
            _result(Command("docker"), out=_inspection(service, running=True)),
        ],
    )
    status = asyncio.run(
        service.start_service(
            cache_root=ResolvedPath(tmp_path),
            host_port=8080,
            readiness_timeout=Duration.seconds(1),
            executor=executor,
        ),
    )
    assert status.state is service.PersistentQwenServiceState.READY
    assert [command.arguments[0] for command in executor.commands] == [
        "inspect",
        "rm",
        "run",
        "inspect",
    ]


def test_start_recreates_stopped_service_and_reports_port_conflict(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Stopped services are disposable while occupied ports fail before launch."""
    acquired = _acquired(service, tmp_path)
    _patch_acquisition_and_port(monkeypatch, service, acquired)

    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", ready)
    executor = _Executor(
        [
            _result(Command("docker"), out=_inspection(service, running=False)),
            _result(Command("docker")),
            _result(Command("docker"), out=f"{_ID}\n".encode()),
            _result(Command("docker"), out=_inspection(service, running=True)),
        ],
    )
    assert asyncio.run(
        service.start_service(
            cache_root=ResolvedPath(tmp_path),
            host_port=8080,
            readiness_timeout=Duration.seconds(1),
            executor=executor,
        ),
    ).state is service.PersistentQwenServiceState.READY

    def occupied(_: int) -> None:
        raise service.PersistentQwenServiceError("port occupied")

    monkeypatch.setattr(service, "_assert_host_port_available", occupied)
    with pytest.raises(service.PersistentQwenServiceError, match="occupied"):
        asyncio.run(
            service.start_service(
                cache_root=ResolvedPath(tmp_path),
                host_port=8080,
                readiness_timeout=Duration.seconds(1),
                executor=_Executor([_absent(service)]),
            ),
        )


def test_start_refuses_running_service_with_different_requested_port(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A running service is never silently replaced just to change its port."""
    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", ready)
    executor = _Executor(
        [_result(Command("docker"), out=_inspection(service, running=True))],
    )
    with pytest.raises(service.PersistentQwenServiceError, match="stop it explicitly"):
        asyncio.run(
            service.start_service(
                cache_root=ResolvedPath(Path.cwd()),
                host_port=8123,
                readiness_timeout=Duration.seconds(1),
                executor=executor,
            ),
        )
    assert len(executor.commands) == 1


def test_readiness_timeout_is_reported_without_generation(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A loading service reaches the bounded readiness failure deterministically."""
    async def loading(**_kwargs: object) -> object:
        return service._status(
            service.PersistentQwenServiceState.RUNNING_LOADING,
            expected_fingerprint=service.profile_fingerprint(),
            host_port=8080,
            container_running=True,
        )

    monkeypatch.setattr(service, "inspect_service", loading)
    with pytest.raises(service.PersistentQwenServiceError, match="did not become ready"):
        asyncio.run(
            service._wait_ready(
                executor=_Executor([]),
                expected_fingerprint=service.profile_fingerprint(),
                host_port=8080,
                readiness_timeout=Duration.seconds(0.001),
            ),
        )


def test_stop_is_safe_for_absent_owned_and_foreign_services(
    service: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Stop removes only explicitly labeled persistent-Qwen containers."""
    async def ready(_: str) -> bool:
        return True

    monkeypatch.setattr(service.llama_cpp, "_probe_ready", ready)
    absent = asyncio.run(service.stop_service(executor=_Executor([_absent(service)])))
    assert absent.state is service.PersistentQwenServiceState.ABSENT

    owned_executor = _Executor(
        [
            _result(Command("docker"), out=_inspection(service, running=True)),
            _result(Command("docker")),
            _result(Command("docker")),
        ],
    )
    assert (
        asyncio.run(service.stop_service(executor=owned_executor)).state
        is service.PersistentQwenServiceState.ABSENT
    )
    assert [command.arguments[0] for command in owned_executor.commands] == ["inspect", "stop", "rm"]

    stale_stopped_executor = _Executor(
        [
            _result(
                Command("docker"),
                out=_inspection(service, running=False, fingerprint="b" * 64),
            ),
            _result(Command("docker")),
        ],
    )
    assert (
        asyncio.run(service.stop_service(executor=stale_stopped_executor)).state
        is service.PersistentQwenServiceState.ABSENT
    )
    assert [command.arguments[0] for command in stale_stopped_executor.commands] == [
        "inspect",
        "rm",
    ]

    foreign_executor = _Executor(
        [
            _result(Command("docker"), out=_inspection(service, running=True, service_label="foreign")),
        ],
    )
    with pytest.raises(service.PersistentQwenServiceError, match="foreign"):
        asyncio.run(service.stop_service(executor=foreign_executor))
    assert len(foreign_executor.commands) == 1


def test_parser_and_helpers_validate_operational_inputs(service: ModuleType) -> None:
    """CLI and strict Docker projections reject malformed local operations."""
    parsed = service.parse_arguments(["start", "--cache-root", "cache", "--port", "8123"])
    assert parsed.command == "start" and parsed.port == 8123
    assert service.parse_arguments(["status"]).command == "status"
    with pytest.raises(ValueError):
        service._validate_start_inputs(0, Duration.seconds(1))
    with pytest.raises(ValueError):
        service._validate_start_inputs(8080, Duration.seconds(0))
    with pytest.raises(service.PersistentQwenServiceError):
        service._parse_inspection(b"not-an-inspection\n")
    assert service._parse_port_label("8080") == 8080
    assert service._parse_port_label("bad") is None
    assert service._is_valid_profile_fingerprint("a" * 64)
    assert service._is_valid_profile_fingerprint("A" * 64)
    assert not service._is_valid_profile_fingerprint("stale")
    assert not service._is_valid_profile_fingerprint("g" + "a" * 63)
