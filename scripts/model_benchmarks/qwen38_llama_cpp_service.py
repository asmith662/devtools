# Copyright (c) 2026
# ruff: noqa: E501, EM101, EM102, I001, INP001, PLR0913, PLR2004, SLF001, T201, TRY003
"""Operate the one persistent local Qwen3.8 llama.cpp development service."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import socket
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.commands import Command, CommandExecutor
from devtools.model_serving import llama_cpp
from devtools.model_serving.huggingface import acquire_huggingface_gguf
from devtools.model_serving.llama_cpp import GGUFModel, LlamaCppServingConfig
from devtools.paths import ResolvedPath, resolve_path
from devtools.time import Duration

from qwen38_llama_cpp_profile import QWEN38_27B_UD_IQ4_XS

if TYPE_CHECKING:
    from collections.abc import Sequence
    from devtools.commands import CommandExecutor as CommandExecutorType


_CONTAINER_NAME = "devtools-qwen38-llama-cpp"
_SERVICE_LABEL = "devtools.qwen.persistent-service"
_SERVICE_VALUE = "qwen38-llama-cpp"
_FINGERPRINT_LABEL = "devtools.qwen.profile-sha256"
_PORT_LABEL = "devtools.qwen.host-port"
_DEFAULT_HOST_PORT = 8080
_SERVED_MODEL_NAME = "qwen38-local"
_POLL_INTERVAL_SECONDS = 0.25
_CONTAINER_ID_LENGTH = 64
_PROFILE_FINGERPRINT_LENGTH = 64


class PersistentQwenServiceState(StrEnum):
    """Describe the bounded persistent Qwen service state."""

    ABSENT = "ABSENT"
    STOPPED = "STOPPED"
    RUNNING_LOADING = "RUNNING_LOADING"
    READY = "READY"
    CONFLICT = "CONFLICT"
    PROFILE_MISMATCH = "PROFILE_MISMATCH"
    PORT_MISMATCH = "PORT_MISMATCH"


@dataclass(frozen=True, slots=True)
class PersistentQwenServiceStatus:
    """Retain inspection facts for the one persistent Qwen service."""

    state: PersistentQwenServiceState
    endpoint: str
    served_model_name: str
    expected_fingerprint: str
    observed_fingerprint: str | None
    container_id: str | None
    container_name: str = _CONTAINER_NAME
    profile_matches: bool | None = None
    container_running: bool = False
    model_ready: bool = False


class PersistentQwenServiceError(RuntimeError):
    """Report an actionable failure in this Qwen-specific service command."""


def parse_arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the explicit start, status, and stop operational commands."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("start", help="Start the persistent Qwen service.")
    start.add_argument(
        "--cache-root",
        required=True,
        help="Visible local Hugging Face cache root for the pinned GGUF.",
    )
    start.add_argument("--port", default=_DEFAULT_HOST_PORT, type=int)
    start.add_argument(
        "--readiness-timeout-seconds",
        default=llama_cpp.DEFAULT_READINESS_TIMEOUT.total_seconds,
        type=float,
    )
    commands.add_parser("status", help="Inspect the persistent Qwen service.")
    commands.add_parser("stop", help="Stop and remove the persistent Qwen service.")
    return parser.parse_args(arguments)


def profile_fingerprint() -> str:
    """Return a stable operational identity for selected serving inputs."""
    profile = QWEN38_27B_UD_IQ4_XS
    payload = {
        "cache_type_k": profile.cache_type_k,
        "cache_type_v": profile.cache_type_v,
        "context_size": profile.context_size,
        "flash_attention": profile.flash_attention,
        "gpu_layers": profile.gpu_layers,
        "image": profile.image_build_identity,
        "model_artifact": profile.model.filename,
        "model_repository": profile.model.repository,
        "model_revision": profile.model.revision,
        "n_cpu_ffn": profile.n_cpu_ffn,
        "parallel_sequences": profile.parallel_sequences,
        "served_model_name": _SERVED_MODEL_NAME,
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


async def inspect_service(
    *,
    executor: CommandExecutorType,
    expected_fingerprint: str,
    requested_port: int | None = None,
) -> PersistentQwenServiceStatus:
    """Inspect only the stable named persistent Qwen service."""
    result = await executor.execute(_inspect_command())
    if result.failed:
        if _is_exact_not_found(result.stderr, _CONTAINER_NAME):
            return _status(
                PersistentQwenServiceState.ABSENT,
                expected_fingerprint=expected_fingerprint,
                host_port=requested_port or _DEFAULT_HOST_PORT,
            )
        raise PersistentQwenServiceError(
            _diagnostic(result.stderr or result.stdout)
            or "Docker could not inspect the persistent Qwen service.",
        )

    inspection = _parse_inspection(result.stdout)
    host_port = inspection.host_port
    if (
        inspection.service_label != _SERVICE_VALUE
        or not _is_valid_profile_fingerprint(inspection.fingerprint)
        or host_port is None
    ):
        return _status(
            PersistentQwenServiceState.CONFLICT,
            expected_fingerprint=expected_fingerprint,
            observed_fingerprint=inspection.fingerprint,
            container_id=inspection.container_id,
            host_port=requested_port or _DEFAULT_HOST_PORT,
        )

    profile_matches = inspection.fingerprint == expected_fingerprint
    ready = await llama_cpp._probe_ready(_endpoint(host_port)) if inspection.running else False
    if not profile_matches:
        state = PersistentQwenServiceState.PROFILE_MISMATCH
    elif requested_port is not None and host_port != requested_port:
        state = PersistentQwenServiceState.PORT_MISMATCH
    elif not inspection.running:
        state = PersistentQwenServiceState.STOPPED
    elif ready:
        state = PersistentQwenServiceState.READY
    else:
        state = PersistentQwenServiceState.RUNNING_LOADING

    return _status(
        state,
        expected_fingerprint=expected_fingerprint,
        observed_fingerprint=inspection.fingerprint,
        container_id=inspection.container_id,
        host_port=host_port,
        profile_matches=profile_matches,
        container_running=inspection.running,
        model_ready=ready,
    )


async def start_service(
    *,
    cache_root: ResolvedPath,
    host_port: int,
    readiness_timeout: Duration,
    executor: CommandExecutorType,
) -> PersistentQwenServiceStatus:
    """Idempotently start the one persistent Qwen development service."""
    _validate_start_inputs(host_port, readiness_timeout)
    fingerprint = profile_fingerprint()
    current = await inspect_service(
        executor=executor,
        expected_fingerprint=fingerprint,
        requested_port=host_port,
    )
    if current.state is PersistentQwenServiceState.READY:
        return current
    if current.state is PersistentQwenServiceState.RUNNING_LOADING:
        return await _wait_ready(
            executor=executor,
            expected_fingerprint=fingerprint,
            host_port=host_port,
            readiness_timeout=readiness_timeout,
        )
    if current.state is PersistentQwenServiceState.CONFLICT:
        raise PersistentQwenServiceError(
            f"Persistent Qwen container name {_CONTAINER_NAME!r} is occupied by a foreign container.",
        )
    if current.state in {
        PersistentQwenServiceState.PROFILE_MISMATCH,
        PersistentQwenServiceState.PORT_MISMATCH,
    } and current.container_running:
        raise PersistentQwenServiceError(
            "Persistent Qwen service is running with incompatible selected inputs; "
            "stop it explicitly before starting the requested service.",
        )
    if current.state in {
        PersistentQwenServiceState.STOPPED,
        PersistentQwenServiceState.PROFILE_MISMATCH,
        PersistentQwenServiceState.PORT_MISMATCH,
    }:
        await _remove_known_container(executor, current.container_id)

    _assert_host_port_available(host_port)
    acquired = await acquire_huggingface_gguf(
        model=QWEN38_27B_UD_IQ4_XS.model,
        cache_root=cache_root,
    )
    config = _serving_config(acquired.path, host_port)
    await llama_cpp._preflight_required_features(config, executor)
    launch = await executor.execute(
        llama_cpp._build_launch_command(
            config,
            _CONTAINER_NAME,
            managed=False,
            labels=(
                (_SERVICE_LABEL, _SERVICE_VALUE),
                (_FINGERPRINT_LABEL, fingerprint),
                (_PORT_LABEL, str(host_port)),
            ),
        ),
    )
    if launch.failed:
        raise PersistentQwenServiceError(
            "Docker rejected persistent Qwen launch. "
            f"{_diagnostic(launch.stderr or launch.stdout)}".strip(),
        )
    llama_cpp._parse_container_id(launch)
    return await _wait_ready(
        executor=executor,
        expected_fingerprint=fingerprint,
        host_port=host_port,
        readiness_timeout=readiness_timeout,
    )


async def stop_service(
    *,
    executor: CommandExecutorType,
) -> PersistentQwenServiceStatus:
    """Stop and remove only the independently verified persistent Qwen service."""
    fingerprint = profile_fingerprint()
    current = await inspect_service(executor=executor, expected_fingerprint=fingerprint)
    if current.state is PersistentQwenServiceState.ABSENT:
        return current
    if current.state is PersistentQwenServiceState.CONFLICT:
        raise PersistentQwenServiceError(
            f"Refusing to stop foreign container named {_CONTAINER_NAME!r}.",
        )
    if current.container_id is None:
        raise PersistentQwenServiceError("Persistent Qwen inspection lacked a container ID.")
    if current.container_running:
        stopped = await executor.execute(Command("docker", ("stop", current.container_id)))
        if stopped.failed:
            raise PersistentQwenServiceError(
                f"Docker could not stop persistent Qwen service. {_diagnostic(stopped.stderr or stopped.stdout)}".strip(),
            )
    await _remove_known_container(executor, current.container_id)
    return _status(
        PersistentQwenServiceState.ABSENT,
        expected_fingerprint=fingerprint,
        host_port=_DEFAULT_HOST_PORT,
    )


async def _wait_ready(
    *,
    executor: CommandExecutorType,
    expected_fingerprint: str,
    host_port: int,
    readiness_timeout: Duration,
) -> PersistentQwenServiceStatus:
    """Wait only for the expected named Qwen service to report ready."""
    try:
        async with asyncio.timeout(readiness_timeout.total_seconds):
            while True:
                status = await inspect_service(
                    executor=executor,
                    expected_fingerprint=expected_fingerprint,
                    requested_port=host_port,
                )
                if status.state is PersistentQwenServiceState.READY:
                    return status
                if status.state is not PersistentQwenServiceState.RUNNING_LOADING:
                    raise PersistentQwenServiceError(
                        f"Persistent Qwen service became {status.state} while waiting for readiness.",
                    )
                await asyncio.sleep(_POLL_INTERVAL_SECONDS)
    except TimeoutError as error:
        raise PersistentQwenServiceError(
            "Persistent Qwen service did not become ready within the configured timeout.",
        ) from error


def _serving_config(model_path: ResolvedPath, host_port: int) -> LlamaCppServingConfig:
    """Map the one selected Qwen profile into existing llama.cpp configuration."""
    profile = QWEN38_27B_UD_IQ4_XS
    image = profile.image_build_identity
    if image is None:
        raise PersistentQwenServiceError("Selected Qwen profile lacks a pinned image.")
    return LlamaCppServingConfig(
        model=GGUFModel(model_path),
        image=image,
        host_port=host_port,
        served_model_name=_SERVED_MODEL_NAME,
        context_size=profile.context_size,
        gpu_layers=profile.gpu_layers,
        flash_attention=profile.flash_attention,
        cache_type_k=profile.cache_type_k,
        cache_type_v=profile.cache_type_v,
        parallel_sequences=profile.parallel_sequences,
        n_cpu_ffn=profile.n_cpu_ffn,
    )


def _validate_start_inputs(host_port: int, readiness_timeout: Duration) -> None:
    """Reject invalid local operating inputs before any Docker action."""
    if not 1 <= host_port <= 65_535:
        raise ValueError("Persistent Qwen host port must be between 1 and 65535.")
    if readiness_timeout.total_seconds <= 0:
        raise ValueError("Persistent Qwen readiness timeout must be positive.")


def _assert_host_port_available(host_port: int) -> None:
    """Fail early when the selected loopback port is already occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        try:
            probe.bind(("127.0.0.1", host_port))
        except OSError as error:
            raise PersistentQwenServiceError(
                f"Persistent Qwen host port {host_port} is already in use.",
            ) from error


@dataclass(frozen=True, slots=True)
class _Inspection:
    container_id: str
    running: bool
    service_label: str
    fingerprint: str
    host_port: int | None


def _inspect_command() -> Command:
    """Build the exact Docker projection required for this one service."""
    return Command(
        "docker",
        (
            "inspect",
            "--format",
            (
                '{{.Id}}|{{.State.Running}}|'
                f'{{{{index .Config.Labels "{_SERVICE_LABEL}"}}}}|'
                f'{{{{index .Config.Labels "{_FINGERPRINT_LABEL}"}}}}|'
                f'{{{{index .Config.Labels "{_PORT_LABEL}"}}}}'
            ),
            _CONTAINER_NAME,
        ),
    )


def _parse_inspection(output: bytes) -> _Inspection:
    """Parse one strict Docker inspect projection for the named service."""
    lines = output.decode(errors="replace").splitlines()
    if len(lines) != 1:
        raise PersistentQwenServiceError("Docker inspection was not one state projection.")
    parts = lines[0].split("|")
    if len(parts) != 5:
        raise PersistentQwenServiceError("Docker inspection had an invalid service projection.")
    container_id, running, service_label, fingerprint, port_text = parts
    if len(container_id) != _CONTAINER_ID_LENGTH or any(
        character not in "0123456789abcdefABCDEF" for character in container_id
    ):
        raise PersistentQwenServiceError("Docker inspection returned an invalid container ID.")
    if running.casefold() not in {"true", "false"}:
        raise PersistentQwenServiceError("Docker inspection returned an invalid running state.")
    host_port = _parse_port_label(port_text)
    return _Inspection(
        container_id=container_id,
        running=running.casefold() == "true",
        service_label=service_label,
        fingerprint=fingerprint,
        host_port=host_port,
    )


def _parse_port_label(value: str) -> int | None:
    """Parse the service-owned port label without inferring external state."""
    if not value:
        return None
    try:
        port = int(value)
    except ValueError:
        return None
    return port if 1 <= port <= 65_535 else None


def _is_valid_profile_fingerprint(value: str) -> bool:
    """Recognize only the SHA-256 label format owned by this service."""
    return len(value) == _PROFILE_FINGERPRINT_LENGTH and all(
        character in "0123456789abcdefABCDEF" for character in value
    )


async def _remove_known_container(
    executor: CommandExecutorType,
    container_id: str | None,
) -> None:
    """Remove one previously inspected owned persistent service container."""
    if container_id is None:
        raise PersistentQwenServiceError("Persistent Qwen inspection lacked a container ID.")
    removed = await executor.execute(Command("docker", ("rm", container_id)))
    if removed.failed and not _is_exact_not_found(removed.stderr, container_id):
        raise PersistentQwenServiceError(
            f"Docker could not remove persistent Qwen service. {_diagnostic(removed.stderr or removed.stdout)}".strip(),
        )


def _status(
    state: PersistentQwenServiceState,
    *,
    expected_fingerprint: str,
    host_port: int,
    observed_fingerprint: str | None = None,
    container_id: str | None = None,
    profile_matches: bool | None = None,
    container_running: bool = False,
    model_ready: bool = False,
) -> PersistentQwenServiceStatus:
    """Construct one status value without inventing a general service model."""
    return PersistentQwenServiceStatus(
        state=state,
        endpoint=_endpoint(host_port),
        served_model_name=_SERVED_MODEL_NAME,
        expected_fingerprint=expected_fingerprint,
        observed_fingerprint=observed_fingerprint,
        container_id=container_id,
        profile_matches=profile_matches,
        container_running=container_running,
        model_ready=model_ready,
    )


def _endpoint(host_port: int) -> str:
    """Return the loopback endpoint exposed by this local development service."""
    return f"http://127.0.0.1:{host_port}"


def _is_exact_not_found(stderr: bytes, target: str) -> bool:
    """Recognize only Docker's exact missing-container diagnostic."""
    return (
        stderr.decode(errors="replace").strip().casefold()
        == f"error: no such object: {target}".casefold()
    )


def _diagnostic(data: bytes) -> str:
    """Retain a bounded actionable Docker diagnostic."""
    return data[:4096].decode(errors="replace").strip()


def _print_status(status: PersistentQwenServiceStatus) -> None:
    """Print stable operator-facing facts without exposing secrets."""
    print(f"state: {status.state}")
    print(f"endpoint: {status.endpoint}")
    print(f"served model: {status.served_model_name}")
    print(f"container name: {status.container_name}")
    print(f"container id: {status.container_id or 'none'}")
    print(f"expected profile fingerprint: {status.expected_fingerprint}")
    print(f"observed profile fingerprint: {status.observed_fingerprint or 'none'}")
    print(f"profile matches: {status.profile_matches}")
    print(f"container running: {status.container_running}")
    print(f"model ready: {status.model_ready}")


async def run(arguments: argparse.Namespace) -> PersistentQwenServiceStatus:
    """Dispatch one explicit persistent Qwen lifecycle command."""
    executor = CommandExecutor()
    if arguments.command == "start":
        cache_root = resolve_path(arguments.cache_root, base_directory=Path.cwd())
        status = await start_service(
            cache_root=cache_root,
            host_port=arguments.port,
            readiness_timeout=Duration.seconds(arguments.readiness_timeout_seconds),
            executor=executor,
        )
    elif arguments.command == "status":
        status = await inspect_service(
            executor=executor,
            expected_fingerprint=profile_fingerprint(),
        )
    else:
        status = await stop_service(executor=executor)
    _print_status(status)
    return status


def main(arguments: Sequence[str] | None = None) -> None:
    """Run one Qwen-specific persistent lifecycle operation."""
    asyncio.run(run(parse_arguments(arguments)))


if __name__ == "__main__":
    main()
