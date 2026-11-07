# Copyright (c) 2026
"""Explicit Windows API report faults, supplementing real contained-process tests."""

from __future__ import annotations

import ctypes
import time
from ctypes import wintypes
from functools import partial
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.resources.commands import _windows_job as module
from devtools.resources.commands._windows_job import WindowsJob, _Extended

if TYPE_CHECKING:
    from collections.abc import Callable


_EXTENDED_INFORMATION = 9


class _Function:
    """Expose ctypes-compatible signature attributes and an explicit report."""

    def __init__(self, report: Callable[[tuple[object, ...]], int]) -> None:
        self.report = report
        self.argtypes: object = None
        self.restype: object = None

    def __call__(self, *args: object) -> int:
        """Return a unit-control report without operating on a real process."""
        return self.report(args)


def _query_report(args: tuple[object, ...], fault: str) -> None:
    """Report extended limits or cleanup membership for the selected control."""
    if args[1] == _EXTENDED_INFORMATION:
        limits = ctypes.cast(
            cast("Any", args[2]),
            ctypes.POINTER(_Extended),
        ).contents
        limits.basic.flags, limits.basic.active = (
            0x2008,
            2 if fault == "limits" else 1,
        )
    elif fault == "cleanup":
        ctypes.cast(cast("Any", args[2]), ctypes.POINTER(wintypes.DWORD))[10] = 1


def _driver(monkeypatch: pytest.MonkeyPatch, fault: str) -> list[str]:
    """Simulate only driver reports; no handle or process is created by this driver."""
    calls: list[str] = []

    def report(name: str, args: tuple[object, ...]) -> int:
        calls.append(name)
        if name == "CreateJobObjectW":
            return 0 if fault == "create" else 123
        if name == "GetHandleInformation":
            ctypes.cast(
                cast("Any", args[1]),
                ctypes.POINTER(wintypes.DWORD),
            ).contents.value = 1 if fault == "inherit" else 0
        if name == "QueryInformationJobObject":
            _query_report(args, fault)
        if name == "GetProcessId":
            return 999 if fault == "identity" else 456
        if name == "IsProcessInJob":
            ctypes.cast(
                cast("Any", args[2]),
                ctypes.POINTER(wintypes.BOOL),
            ).contents.value = fault != "assigned"
        if name == "NtResumeProcess" and fault == "resume":
            return -1
        return 1

    names = (
        "CreateJobObjectW",
        "SetInformationJobObject",
        "QueryInformationJobObject",
        "AssignProcessToJobObject",
        "GetProcessId",
        "GetHandleInformation",
        "IsProcessInJob",
        "CloseHandle",
        "TerminateJobObject",
        "NtResumeProcess",
    )
    driver = SimpleNamespace(
        **{name: _Function(partial(report, name)) for name in names},
    )
    monkeypatch.setattr(ctypes, "WinDLL", lambda *_args, **_kwargs: driver)
    monkeypatch.setattr(time, "sleep", lambda _: None)
    return calls


@pytest.mark.parametrize("fault", ["create", "inherit", "limits"])
def test_job_setup_refuses_unverifiable_driver_reports(
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """Never create a producer after invalid one-process or handle-custody reports."""
    calls = _driver(monkeypatch, fault)
    with pytest.raises(OSError, match=r"WinError|custody|limits"):
        WindowsJob()
    assert "NtResumeProcess" not in calls
    if fault != "create":
        assert calls[-1] == "CloseHandle"


@pytest.mark.parametrize("fault", ["identity", "assigned", "resume"])
def test_job_assignment_refusal_never_retries_or_resumes_before_custody(
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """Only simulated handles are used; real assignment has separate positive tests."""
    calls = _driver(monkeypatch, fault)
    job = WindowsJob()
    try:
        with pytest.raises(OSError, match=r"PID|custody|resume"):
            job.assign_and_resume(321, 456)
    finally:
        job.close()
    if fault in {"identity", "assigned"}:
        assert "NtResumeProcess" not in calls
    else:
        assert calls.index("AssignProcessToJobObject") < calls.index("NtResumeProcess")


def test_job_uncertain_cleanup_still_closes_its_sole_handle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A reported nonempty Job remains uncertain after the bounded polling limit."""
    calls = _driver(monkeypatch, "cleanup")
    job = WindowsJob()
    with pytest.raises(OSError, match="did not confirm an empty Job"):
        job.close()
    assert calls[-1] == "CloseHandle"
    before = tuple(calls)
    job.close()
    assert tuple(calls) == before


def test_nonwindows_report_refuses_before_any_native_job_creation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Refuse a simulated unsupported platform before native entry."""
    monkeypatch.setattr(module, "os", SimpleNamespace(name="posix"))
    with pytest.raises(OSError, match="Windows Job profile"):
        WindowsJob()
