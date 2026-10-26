# Copyright (c) 2026
"""Native-runtime structured model regressions runnable without pytest installed."""

# Native unittest exception assertions intentionally avoid a pytest dependency.
# ruff: noqa: PT027

from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch

from devtools.core.paths import resolve_path
from devtools.resources.filesystem import (
    BinaryFile,
    CsvCodec,
    CsvFile,
    CsvRow,
    JsonCodec,
    JsonListFile,
    JsonObjectFile,
    JsonScalarFile,
    MarkdownFile,
    TextFile,
    read,
)
from devtools.tools import ToolRunner
from devtools.tools.filesystem import ReadRepositoryFileTool

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.resources.filesystem.models.json import JsonValue


class StructuredCompatibilityTests(unittest.TestCase):
    """Exercise actual public models under each already available interpreter."""

    def setUp(self) -> None:
        """Create independent temporary data, never a copy of Devtools source."""
        folder = tempfile.TemporaryDirectory(prefix="devtools-structured-compat-")
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.path = resolve_path(self.root / "model.data")

    def _constructors(
        self,
        *,
        encoding: str = "utf-8",
        byte_size: int = 0,
    ) -> tuple[Callable[[], TextFile], ...]:
        """Return each real affected constructor without deriving expected values."""
        return (
            lambda: JsonObjectFile(
                self.path,
                "{}",
                value={},
                encoding=encoding,
                byte_size=byte_size,
            ),
            lambda: JsonListFile(
                self.path,
                "[]",
                value=(),
                encoding=encoding,
                byte_size=byte_size,
            ),
            lambda: CsvFile(
                self.path,
                "id\n",
                headers=("id",),
                rows=(),
                encoding=encoding,
                byte_size=byte_size,
            ),
        )

    def test_constructors_preserve_metadata(self) -> None:
        """All three current model families construct with inherited metadata."""
        retained_size = 7
        for construct in self._constructors(byte_size=retained_size):
            with self.subTest(constructor=construct):
                file = construct()
                assert file.path == self.path
                assert file.byte_size == retained_size
                assert file.encoding == "utf-8"
                assert not file.truncated

    def test_inherited_validation_refuses_invalid_metadata(self) -> None:
        """Compatibility repair cannot bypass the parent's invariants."""
        for construct in self._constructors(encoding=" "):
            with (
                self.subTest(constructor=construct),
                self.assertRaisesRegex(
                    ValueError,
                    "encoding",
                ),
            ):
                construct()
        for construct in self._constructors(byte_size=-1):
            with (
                self.subTest(constructor=construct),
                self.assertRaisesRegex(
                    ValueError,
                    "negative",
                ),
            ):
                construct()

    def test_inherited_post_init_runs_once(self) -> None:
        """The cooperative parent is called once and still executes its body."""
        original = TextFile.__post_init__
        for construct in self._constructors():
            with (
                self.subTest(constructor=construct),
                patch.object(
                    TextFile,
                    "__post_init__",
                    autospec=True,
                    side_effect=original,
                ) as parent,
            ):
                file = construct()
                parent.assert_called_once_with(file)

    def test_object_and_list_transformations_remain_immutable(self) -> None:
        """Native construction and replacements retain provenance and frozen state."""
        values: dict[str, JsonValue] = {"items": (1,)}
        obj = JsonObjectFile(self.path, '{"items":[1]}', value=values)
        values["items"] = (9,)
        assert obj["items"] == (1,)
        changed = obj.with_item("nested", {"items": [2]})
        assert changed["nested"] == {"items": (2,)}
        assert changed.content == '{"items":[1]}'
        assert "nested" not in obj
        array = JsonListFile(self.path, "[1]", value=(1,))
        changed_array = array.appended({"items": [2]}).with_item(0, [3])
        assert changed_array.value == ((3,), {"items": (2,)})
        assert array.value == (1,)
        assert changed_array.content == "[1]"

    def test_csv_construction_and_replacement_preserve_source(self) -> None:
        """String cells and immutable replacement work on the declared runtime."""
        file = CsvFile(
            self.path,
            "id\n001\n",
            headers=("id",),
            rows=(CsvRow(("id",), ("001",)),),
        )
        changed = file.with_row(0, CsvRow(("id",), ("002",)))
        assert file[0].cells == ("001",)
        assert changed[0].cells == ("002",)
        assert changed.content == "id\n001\n"

    def test_public_codecs_disk_reads_and_toolrunner(self) -> None:
        """Real parsed, read and Tool-returned models use the same constructors."""
        cases = (
            ("object.json", '{"items":[1]}', JsonObjectFile),
            ("array.json", '[{"id":1}]', JsonListFile),
            ("rows.csv", "id\n001\n", CsvFile),
        )
        for name, source, expected_type in cases:
            with self.subTest(name=name):
                path = self.root / name
                path.write_bytes(source.encode("utf-8"))
                file = read(resolve_path(path))
                assert isinstance(file, TextFile)
                assert isinstance(file, expected_type)
                assert file.content == source
                assert file.byte_size == len(source.encode())

                async def exercise(path: Path = path) -> TextFile:
                    result = await ToolRunner().execute(
                        ReadRepositoryFileTool(resolve_path(self.root)),
                        resolve_path(path),
                    )
                    assert isinstance(result, TextFile)
                    return result

                assert asyncio.run(exercise()) == file
        assert JsonCodec().parse(self.path, "{}").content == "{}"
        assert CsvCodec().parse(self.path, "id\n").content == "id\n"

    def test_model_specific_validation_still_runs(self) -> None:
        """Wrong JSON roots and invalid CSV structure still refuse."""
        with self.assertRaisesRegex(TypeError, "object"):
            JsonObjectFile(self.path, "[]", value=())  # type: ignore[arg-type]
        with self.assertRaisesRegex(TypeError, "array"):
            JsonListFile(self.path, "{}", value={})  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "unique"):
            CsvFile(self.path, "id,id\n", headers=("id", "id"), rows=())
        with self.assertRaisesRegex(ValueError, "match"):
            CsvFile(
                self.path,
                "id\nx\n",
                headers=("id",),
                rows=(CsvRow(("other",), ("x",)),),
            )

    def test_unaffected_model_controls(self) -> None:
        """Scalar JSON, text, Markdown and exact bytes remain supported."""
        assert JsonScalarFile(self.path, "null", value=None).value is None
        assert TextFile(self.path, "text").content == "text"
        assert MarkdownFile(self.path, "# title\n").headings[0].text == "title"
        assert BinaryFile(self.path, b"\x00\xff").content == b"\x00\xff"


if __name__ == "__main__":
    unittest.main()
