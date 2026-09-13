# Copyright (c) 2026
"""Tests for public operating-system detection."""

import pytest

from devtools.core.system import OperatingSystem, get_operating_system


@pytest.mark.parametrize(
    ("platform_name", "expected"),
    [
        ("Windows", OperatingSystem.WINDOWS),
        ("Linux", OperatingSystem.LINUX),
        ("Darwin", OperatingSystem.MACOS),
        ("windows", OperatingSystem.OTHER),
        ("Plan9", OperatingSystem.OTHER),
    ],
)
def test_get_operating_system_uses_platform_family(
    monkeypatch: pytest.MonkeyPatch,
    platform_name: str,
    expected: OperatingSystem,
) -> None:
    """Detection maps platform responses without depending on the host."""
    monkeypatch.setattr(
        "devtools.core.system.detection.platform.system",
        lambda: platform_name,
    )

    assert get_operating_system() is expected
