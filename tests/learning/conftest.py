# Copyright (c) 2026
"""Collect authenticated Python execution inside the real contained worker."""

from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

import coverage
import pytest

from devtools.tools.learning import ManagedLearningWorker
from devtools.tools.learning import execution as worker_execution

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Mapping

    from devtools.core.time import Duration
    from devtools.learning.integrations.local.operations import LearningPublication
    from devtools.learning.investigation.classification.contracts import (
        ExecutionAuthorization,
    )
    from devtools.learning.investigation.plans import LearningPlan


_ENTRY = (
    "runpy.run_module('devtools.learning.integrations.local.worker',"
    "run_name='__main__')"
)
_MEASUREMENT = """
import atexit,coverage,hashlib
measurement_nonce=NONCE
measurement_root=pathlib.Path.cwd()
measurement_packet=(measurement_root/'request.json').read_bytes()
measurement_plan=json.loads(measurement_packet)['grant']['plan_identity']
measurement_file=measurement_root/('.coverage-'+measurement_nonce)
measurement=coverage.Coverage(data_file=str(measurement_file),branch=True,
    source=['devtools'],config_file=False)
measurement.start()
def retain_test_coverage():
    measurement.stop()
    measurement.save()
    sources={name:hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest()
        for name in measurement.get_data().measured_files()}
    receipt=dict(nonce=measurement_nonce,operation_identity=measurement_plan,
        packet_sha256=hashlib.sha256(measurement_packet).hexdigest(),
        executable_sha256=hashlib.sha256(pathlib.Path(sys.executable).read_bytes()).hexdigest(),
        data_sha256=hashlib.sha256(measurement_file.read_bytes()).hexdigest(),
        sources=sources)
    (measurement_root/('.coverage-'+measurement_nonce+'.json')).write_text(
        json.dumps(receipt),encoding='utf-8')
atexit.register(retain_test_coverage)
"""


def _digest(path: Path) -> str:
    """Hash an actual selected interpreter or source file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _collect(
    root: Path,
    parent: coverage.Coverage,
    expected: Mapping[str, str],
    *,
    packet_name: str = "request.json",
    completed: bool = False,
) -> None:
    """Combine only fresh nonce-, packet-, interpreter- and source-bound data."""
    name = ".coverage-" + expected["nonce"]
    receipt = root / (name + ".json")
    if not receipt.exists():
        # Refused/mocked operations and killed workers have no completed capture.
        assert not completed, "completed numerical process did not retain coverage"
        return
    actual = json.loads(receipt.read_bytes())
    for key, value in expected.items():
        assert actual[key] == value, key
    assert (
        actual["packet_sha256"]
        == hashlib.sha256((root / packet_name).read_bytes()).hexdigest()
    )
    data_path = root / name
    assert actual["data_sha256"] == hashlib.sha256(data_path.read_bytes()).hexdigest()
    source_root = worker_execution.__file__
    assert source_root is not None
    framework = Path(source_root).resolve().parents[2]
    for source, digest in actual["sources"].items():
        path = Path(source).resolve()
        assert path.is_relative_to(framework)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    data = coverage.CoverageData(basename=str(data_path))
    data.read()
    assert data.has_arcs()
    assert set(data.measured_files()) == set(actual["sources"])
    parent.get_data().update(data)


@pytest.fixture(autouse=True)
def native_coverage(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Keep tracing test-only, within Job1, with files in its owned operation."""
    parent = coverage.Coverage.current()
    if parent is None:
        yield
        return
    bootstrap = vars(worker_execution)["_BOOTSTRAP"]
    assert bootstrap.count(_ENTRY) == 1
    nonce = uuid4().hex
    injected = _MEASUREMENT.replace("NONCE", repr(nonce))
    monkeypatch.setattr(
        worker_execution,
        "_BOOTSTRAP",
        bootstrap.replace(_ENTRY, injected + _ENTRY),
    )
    execute = ManagedLearningWorker.execute

    async def measured(
        self: ManagedLearningWorker,
        plan: LearningPlan,
        grant: ExecutionAuthorization,
        root: Path,
        **options: Duration,
    ) -> LearningPublication:
        expected = {
            "nonce": nonce,
            "operation_identity": plan.identity,
            "executable_sha256": await asyncio.to_thread(
                _digest,
                self.executable.value,
            ),
        }
        completed = False
        try:
            result = await execute(self, plan, grant, root, **options)
            completed = True
            return result
        finally:
            await asyncio.to_thread(
                _collect,
                root,
                parent,
                expected,
                completed=completed,
            )

    monkeypatch.setattr(ManagedLearningWorker, "execute", measured)
    yield


@pytest.fixture
def control_coverage(
    tmp_path: Path,
) -> Callable[[Path, Path], tuple[str, Callable[[], None]]]:
    """Measure the existing authored control script under the same Job1 custody."""
    parent = coverage.Coverage.current()

    def prepare(program: Path, executable: Path) -> tuple[str, Callable[[], None]]:
        if parent is None:
            return "", lambda: None
        nonce = uuid4().hex
        identity = _digest(program)
        packet = {
            "schema": "test-process-coverage-v1",
            "coverage_identity": identity,
            "program_sha256": identity,
            "argv": [str(program), str(tmp_path / "science")],
        }
        packet_name = ".coverage-request.json"
        (tmp_path / packet_name).write_text(json.dumps(packet), encoding="utf-8")
        expected = {
            "nonce": nonce,
            "operation_identity": identity,
            "executable_sha256": _digest(executable),
        }
        control = (
            _MEASUREMENT.replace("'request.json'", repr(packet_name))
            .replace(
                "measurement_plan=json.loads(measurement_packet)['grant']['plan_identity']",
                "measurement_control=json.loads(measurement_packet)\n"
                "measurement_plan=measurement_control['coverage_identity']\n"
                "measurement_program=pathlib.Path(sys.argv[0])\n"
                "assert hashlib.sha256(measurement_program.read_bytes()).hexdigest()=="
                "measurement_control['program_sha256']\n"
                "assert list(sys.argv)==measurement_control['argv']",
            )
            .replace(
                "    measurement.stop()",
                "    assert hashlib.sha256("
                "measurement_program.read_bytes()).hexdigest()=="
                "measurement_control['program_sha256']\n    measurement.stop()",
            )
        )

        def finish() -> None:
            _collect(
                tmp_path,
                parent,
                expected,
                packet_name=packet_name,
                completed=True,
            )

        return control.replace("NONCE", repr(nonce)), finish

    return prepare
