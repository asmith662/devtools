# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Demonstrate intrinsic canonical paths without introducing RI role facts."""

from pathlib import PurePosixPath

from devtools.context.repository.resource import RepositoryResourceAddress


def test_canonical_address_answers_resource_path_questions() -> None:
    address = RepositoryResourceAddress("tests/package/test_example.py")
    path = PurePosixPath(address.value)
    assert address.parts == ("tests", "package", "test_example.py")
    assert path.name == address.parts[-1] == "test_example.py"
    assert path.suffix == ".py"
    assert path.parent == PurePosixPath("tests/package")
    assert len(address.parts) - 1 == 2  # edges from repository root to parent
    assert path.is_relative_to("tests")
    assert not path.is_relative_to("test")
    assert address == RepositoryResourceAddress("tests/package/test_example.py")
    assert address != RepositoryResourceAddress("other/test_example.py")
    assert not hasattr(address, "role")


def test_root_resource_and_suffix_semantics_are_stdlib_values() -> None:
    address = RepositoryResourceAddress("archive.tar.gz")
    path = PurePosixPath(address.value)
    assert path.parent == PurePosixPath(".")
    assert len(address.parts) - 1 == 0
    assert path.suffix == ".gz"
    assert path.suffixes == [".tar", ".gz"]
    assert PurePosixPath(".config").suffix == ""
