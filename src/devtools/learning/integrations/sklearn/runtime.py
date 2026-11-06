# Copyright (c) 2026
"""Observed numerical binary identity for the explicitly qualified first profile."""

from __future__ import annotations

import hashlib
import importlib
import importlib.metadata
import platform
import sqlite3
import struct
import sys
from pathlib import Path

from devtools.core.paths import resolve_path
from devtools.resources.filesystem import BinaryFile, FileFormat, read

VERSIONS = {
    "numpy": "2.5.3",
    "scipy": "1.18.1",
    "scikit-learn": "1.9.1",
    "threadpoolctl": "3.7.0",
}


def observe_runtime() -> dict[str, object]:
    """Record actual loaded libraries and thread limits; version names alone do not qualify."""
    versions = {name: importlib.metadata.version(name) for name in VERSIONS}
    if (
        versions != VERSIONS
        or sys.platform != "win32"
        or sys.implementation.name != "cpython"
        or platform.python_version() != "3.12.13"
    ):
        msg = "the first numerical profile requires its qualified Windows CPython 3.12.13 stack"
        raise ValueError(
            msg,
        )
    origins = {}
    for name in (
        "numpy",
        "scipy",
        "sklearn",
        "scipy.linalg",
        "sklearn.svm",
        "sklearn.neighbors",
    ):
        module = importlib.import_module(name)
        origins[name] = str(module.__file__)
    control = importlib.import_module("threadpoolctl")
    pools = control.threadpool_info()
    if not pools or any(p["num_threads"] != 1 for p in pools):
        msg = "one native thread is required before numerical fitting"
        raise ValueError(msg)
    for pool in pools:
        binary = read(
            resolve_path(Path(pool["filepath"])),
            file_format=FileFormat.BINARY,
            max_bytes=128 << 20,
        )
        if not isinstance(binary, BinaryFile):
            msg = "native binary bytes required"
            raise TypeError(msg)
        pool["sha256"] = hashlib.sha256(binary.content).hexdigest()
    executable = read(
        resolve_path(Path(sys.executable)),
        file_format=FileFormat.BINARY,
        max_bytes=16 << 20,
    )
    if not isinstance(executable, BinaryFile):
        msg = "interpreter binary bytes required"
        raise TypeError(msg)
    return {
        "python": platform.python_version(),
        "implementation": sys.implementation.name,
        "abi": sys.implementation.cache_tag,
        "pointer_bits": struct.calcsize("P") * 8,
        "executable": sys.executable,
        "executable_sha256": hashlib.sha256(executable.content).hexdigest(),
        "sqlite": sqlite3.sqlite_version,
        "versions": versions,
        "origins": origins,
        "native_pools": pools,
    }
