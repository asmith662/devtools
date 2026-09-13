# Copyright (c) 2026
"""Tests for :class:`devtools.core.system.OperatingSystem`."""

import pytest

from devtools.core.system import OperatingSystem


def test_operating_system_values_are_stable() -> None:
    """Each supported operating-system family has its public string value."""
    assert OperatingSystem.WINDOWS.value == "windows"
    assert OperatingSystem.LINUX.value == "linux"
    assert OperatingSystem.MACOS.value == "macos"
    assert OperatingSystem.OTHER.value == "other"
    assert str(OperatingSystem.WINDOWS) == "windows"


@pytest.mark.parametrize(
    ("operating_system", "is_windows", "is_linux", "is_macos"),
    [
        (OperatingSystem.WINDOWS, True, False, False),
        (OperatingSystem.LINUX, False, True, False),
        (OperatingSystem.MACOS, False, False, True),
        (OperatingSystem.OTHER, False, False, False),
    ],
)
def test_operating_system_convenience_properties(
    operating_system: OperatingSystem,
    *,
    is_windows: bool,
    is_linux: bool,
    is_macos: bool,
) -> None:
    """Convenience properties identify only their matching family."""
    assert operating_system.is_windows is is_windows
    assert operating_system.is_linux is is_linux
    assert operating_system.is_macos is is_macos
