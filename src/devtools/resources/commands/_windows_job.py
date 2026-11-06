# Copyright (c) 2026
"""One-process Windows Job custody for explicitly contained managed commands.

The child starts suspended and is assigned before any child instruction runs.
The non-inherited job handle belongs to the executing host. Closing it kills
all job members. This enforces process custody, not file/network authorization.
"""

from __future__ import annotations

import ctypes
import os
import time
from ctypes import wintypes


class _Limits(ctypes.Structure):
    _fields_ = [
        ("process_time", ctypes.c_int64),
        ("job_time", ctypes.c_int64),
        ("flags", wintypes.DWORD),
        ("minimum", ctypes.c_size_t),
        ("maximum", ctypes.c_size_t),
        ("active", wintypes.DWORD),
        ("affinity", ctypes.c_size_t),
        ("priority", wintypes.DWORD),
        ("scheduling", wintypes.DWORD),
    ]


class _IO(ctypes.Structure):
    _fields_ = [("counter" + str(i), ctypes.c_uint64) for i in range(6)]


class _Extended(ctypes.Structure):
    _fields_ = [
        ("basic", _Limits),
        ("io", _IO),
        ("process_memory", ctypes.c_size_t),
        ("job_memory", ctypes.c_size_t),
        ("peak_process", ctypes.c_size_t),
        ("peak_job", ctypes.c_size_t),
    ]


class WindowsJob:
    """Own one kill-on-close, active-process-limit-one Job Object."""

    def __init__(self) -> None:
        """Create and verify custody before creating the suspended producer."""
        if os.name != "nt":
            msg = "Contained commands require the qualified Windows Job profile."
            raise OSError(msg)
        self._kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self._native = ctypes.WinDLL("ntdll")
        self._kernel.CreateJobObjectW.restype = wintypes.HANDLE
        self._kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self._kernel.SetInformationJobObject.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        self._kernel.QueryInformationJobObject.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
            ctypes.c_void_p,
        ]
        self._kernel.AssignProcessToJobObject.argtypes = [
            wintypes.HANDLE,
            wintypes.HANDLE,
        ]
        self._kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        self._kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        self._native.NtResumeProcess.argtypes = [wintypes.HANDLE]
        self._native.NtResumeProcess.restype = ctypes.c_long
        self._handle = self._kernel.CreateJobObjectW(None, None)
        self._check(bool(self._handle))
        try:
            limits = _Extended()
            limits.basic.flags = 0x2000 | 0x8
            limits.basic.active = 1
            self._check(
                bool(
                    self._kernel.SetInformationJobObject(
                        self._handle, 9, ctypes.byref(limits), ctypes.sizeof(limits),
                    ),
                ),
            )
            actual = _Extended()
            self._check(
                bool(
                    self._kernel.QueryInformationJobObject(
                        self._handle,
                        9,
                        ctypes.byref(actual),
                        ctypes.sizeof(actual),
                        None,
                    ),
                ),
            )
            if (
                actual.basic.flags & limits.basic.flags != limits.basic.flags
                or actual.basic.active != 1
            ):
                msg = (
                    "Windows Job limits differ from the requested one-process profile."
                )
                raise OSError(msg)
        except BaseException:
            self.close()
            raise

    @staticmethod
    def _check(ok: bool) -> None:
        if not ok:
            raise ctypes.WinError(ctypes.get_last_error())

    def assign_and_resume(self, process_handle: int) -> None:
        """Enter custody before resuming trusted code; assignment never retries."""
        self._check(
            bool(self._kernel.AssignProcessToJobObject(self._handle, process_handle)),
        )
        if self._native.NtResumeProcess(process_handle) < 0:
            msg = "Cannot resume the contained command."
            raise OSError(msg)

    def close(self) -> None:
        """Release the sole host handle, terminating any remaining member."""
        if self._handle:
            handle, self._handle = self._handle, None
            try:
                self._check(bool(self._kernel.TerminateJobObject(handle, 1)))
                # Query the job-owned active count, never the machine process table.
                for _ in range(100):
                    accounting = (ctypes.c_int64 * 6)()
                    self._check(bool(self._kernel.QueryInformationJobObject(handle, 1, ctypes.byref(accounting), ctypes.sizeof(accounting), None)))
                    if not (wintypes.DWORD * 12).from_buffer(accounting)[10]:
                        return
                    time.sleep(0.01)
                msg = "Contained command cleanup did not confirm an empty Job."
                raise OSError(msg)
            finally:
                self._check(bool(self._kernel.CloseHandle(handle)))
