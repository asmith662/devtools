# Copyright (c) 2026
# ruff: noqa: COM812 -- maintained test formatting convention
"""Independent permanent regression for the Qwen BSD family implementation."""

import pytest

from devtools.core.system import OperatingSystem, get_operating_system


@pytest.mark.parametrize("name", ["FreeBSD", "OpenBSD", "NetBSD", "DragonFly"])
def test_bsd_platform_families(monkeypatch: pytest.MonkeyPatch, name: str) -> None:
    """Supported kernel names share one stable family value."""
    monkeypatch.setattr("devtools.core.system.detection.platform.system", lambda: name)
    detected = get_operating_system()
    assert detected is OperatingSystem.BSD
    assert detected.value == "bsd"
    assert detected.is_bsd
    assert not detected.is_windows
    assert not detected.is_linux
    assert not detected.is_macos


@pytest.mark.parametrize("name", ["freebsd", "FreeBSD14", "BSD", "", "Plan9"])
def test_bsd_recognition_does_not_broaden_unknown_names(
    monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    """Case and exact-name compatibility remain unchanged."""
    monkeypatch.setattr("devtools.core.system.detection.platform.system", lambda: name)
    assert get_operating_system() is OperatingSystem.OTHER
    assert not get_operating_system().is_bsd


def test_bsd_predicate_is_exclusive() -> None:
    """Every non-BSD enum value reports false."""
    assert all(
        value.is_bsd == (value is OperatingSystem.BSD) for value in OperatingSystem
    )
