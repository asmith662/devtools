# Copyright (c) 2026
"""Tests for the JSON representation codec."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import TYPE_CHECKING, cast

import pytest

from devtools.core.paths import ResolvedPath
from devtools.resources.filesystem import (
    FileFormatError,
    JsonCodec,
    JsonFile,
    JsonListFile,
    JsonObjectFile,
    JsonScalarFile,
    TextDecodingError,
    TextEncodingError,
)
from devtools.resources.filesystem.codecs import json as json_module

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


def test_decode_preserves_utf8_source_metadata_and_immutable_object(
    tmp_path: Path,
) -> None:
    """UTF-8 decoding preserves source provenance and freezes nested values."""
    codec = JsonCodec()
    source = '{"name":"José","items":[{"active":true}]}'
    encoded = source.encode()

    file = codec.decode(ResolvedPath(tmp_path), encoded)

    assert isinstance(file, JsonObjectFile)
    assert file.content == source
    assert file.encoding == "utf-8"
    assert file.byte_size == len(encoded)
    assert isinstance(file["items"], tuple)
    nested = file["items"][0]
    assert isinstance(nested, Mapping)

    with pytest.raises(TypeError):
        cast("dict[str, object]", nested)["changed"] = True


def test_decode_supports_alternate_encodings_and_rejects_invalid_bytes(
    tmp_path: Path,
) -> None:
    """Decode honors explicit encoding and wraps invalid encoded source bytes."""
    codec = JsonCodec()
    source = '{"city":"München"}'
    utf16 = source.encode("utf-16")

    file = codec.decode(ResolvedPath(tmp_path), utf16, encoding="utf-16")

    assert isinstance(file, JsonObjectFile)
    assert file.content == source
    assert file.encoding == "utf-16"
    assert file.byte_size == len(utf16)

    with pytest.raises(TextDecodingError, match="utf-8"):
        codec.decode(ResolvedPath(tmp_path), b"\xff")


@pytest.mark.parametrize(
    ("source", "model_type", "expected_value"),
    [
        ("{}", JsonObjectFile, {}),
        ("[]", JsonListFile, ()),
        ('"hello"', JsonScalarFile, "hello"),
        ("42", JsonScalarFile, 42),
        ("4.5", JsonScalarFile, 4.5),
        ("true", JsonScalarFile, True),
        ("null", JsonScalarFile, None),
    ],
)
def test_parse_selects_the_correct_concrete_root_model(
    tmp_path: Path,
    source: str,
    model_type: type[JsonFile],
    expected_value: object,
) -> None:
    """JSON root types resolve to their concrete immutable model classes."""
    file = JsonCodec().parse(ResolvedPath(tmp_path), source)

    assert isinstance(file, model_type)
    assert isinstance(file, JsonObjectFile | JsonListFile | JsonScalarFile)
    assert file.value == expected_value


def test_parse_derives_byte_size_and_wraps_parse_and_encoding_errors(
    tmp_path: Path,
) -> None:
    """Parsing derives source size and preserves useful domain-level failures."""
    codec = JsonCodec()
    source = '"é"'
    file = codec.parse(ResolvedPath(tmp_path), source)

    assert file.byte_size == len(source.encode())

    with pytest.raises(FileFormatError, match="line 1, column") as malformed:
        codec.parse(ResolvedPath(tmp_path), "{")

    assert malformed.value.__cause__ is not None

    with pytest.raises(FileFormatError, match="Invalid JSON constant"):
        codec.parse(ResolvedPath(tmp_path), "NaN")

    with pytest.raises(TextEncodingError, match="ascii"):
        codec.parse(ResolvedPath(tmp_path), source, encoding="ascii")


def test_parse_rejects_an_unexpected_frozen_root_type(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A defensive root-type check rejects broken conversion implementations."""
    monkeypatch.setattr(
        "devtools.resources.filesystem.codecs.json.freeze_json",
        lambda _value: object(),
    )

    with pytest.raises(FileFormatError, match="Unsupported frozen JSON root"):
        JsonCodec().parse(ResolvedPath(tmp_path), "{}")


def test_serialize_supports_current_values_and_formatting_policies(
    tmp_path: Path,
) -> None:
    """Serialization thaws current values with explicit formatting controls."""
    codec = JsonCodec()
    file = codec.parse(ResolvedPath(tmp_path), '{"z":["é"],"a":true}')

    pretty = codec.serialize(file, sort_keys=True)
    compact = codec.serialize(file, indent=None, trailing_newline=False)
    ascii_output = codec.serialize(file, ensure_ascii=True, trailing_newline=False)

    assert pretty == '{\n  "a": true,\n  "z": [\n    "é"\n  ]\n}\n'
    assert compact == '{"z":["é"],"a":true}'
    assert "\\u00e9" in ascii_output


def test_serialize_handles_array_scalar_and_defensive_base_models(
    tmp_path: Path,
) -> None:
    """All concrete roots serialize, while incomplete base models are rejected."""
    codec = JsonCodec()
    list_file = codec.parse(ResolvedPath(tmp_path), "[1,2]")
    scalar_file = codec.parse(ResolvedPath(tmp_path), "false")

    assert codec.serialize(list_file, indent=None) == "[1,2]\n"
    assert codec.serialize(scalar_file, indent=None) == "false\n"

    with pytest.raises(FileFormatError, match="concrete JSON root"):
        codec.serialize(JsonFile(ResolvedPath(tmp_path), "{}"))


def test_serialize_rejects_non_finite_float_transformations(tmp_path: Path) -> None:
    """Strict JSON serialization rejects non-finite floats added in memory."""
    codec = JsonCodec()
    file = codec.parse(ResolvedPath(tmp_path), "{}")
    assert isinstance(file, JsonObjectFile)
    updated = file.with_item("not_a_number", float("nan"))

    with pytest.raises(FileFormatError, match="strict JSON"):
        codec.serialize(updated)


def test_encode_uses_model_encoding_and_wraps_encoding_failures(tmp_path: Path) -> None:
    """Encoding defaults to model metadata while allowing an explicit override."""
    codec = JsonCodec()
    file = codec.parse(ResolvedPath(tmp_path), '"é"', encoding="utf-16")

    assert codec.encode(file) == '"é"\n'.encode("utf-16")
    assert codec.encode(file, encoding="utf-8") == b'"\xc3\xa9"\n'

    with pytest.raises(TextEncodingError, match="ascii"):
        codec.encode(file, encoding="ascii")


def test_transformations_preserve_source_provenance_and_serialize_current_state(
    tmp_path: Path,
) -> None:
    """Structured changes leave source provenance intact but affect serialization."""
    codec = JsonCodec()
    original = codec.parse(ResolvedPath(tmp_path), '{"status":"old"}')
    assert isinstance(original, JsonObjectFile)
    updated = original.with_item("status", "new")

    assert updated.content == original.content
    assert updated.value != original.value
    assert (
        codec.serialize(updated, indent=None, trailing_newline=False)
        == '{"status":"new"}'
    )

    original_list = codec.parse(ResolvedPath(tmp_path), "[1]")
    assert isinstance(original_list, JsonListFile)
    updated_list = original_list.appended(2)

    assert updated_list.content == original_list.content
    assert codec.serialize(updated_list, indent=None) == "[1,2]\n"


def test_codec_created_models_retain_source_and_structured_search_and_round_trip(
    tmp_path: Path,
) -> None:
    """Codec output retains model behavior across semantic serialization round trips."""
    codec = JsonCodec()
    original = codec.parse(ResolvedPath(tmp_path), '{"name":"Ada","id":2}')
    assert isinstance(original, JsonObjectFile)

    assert original.search_regex("Ada") is not None
    assert original.find(lambda key, _value: key == "id") == ("id", 2)
    serialized = codec.serialize(original)
    reparsed = codec.parse(ResolvedPath(tmp_path), serialized)

    assert isinstance(reparsed, JsonObjectFile)
    assert reparsed.value == original.value


@pytest.mark.parametrize(
    "content",
    ["1e999", "-1e999", "[0,1e999]", '{"x":[{"n":-1e999}]}'],
)
@pytest.mark.parametrize("operation", ["parse", "decode"])
def test_strict_json_rejects_floating_point_overflow(
    tmp_path: Path,
    content: str,
    operation: str,
) -> None:
    """Valid numeric syntax must not introduce non-finite model values."""
    codec = JsonCodec()
    call: Callable[[], JsonFile] = (
        (lambda: codec.parse(ResolvedPath(tmp_path), content))
        if operation == "parse"
        else (lambda: codec.decode(ResolvedPath(tmp_path), content.encode()))
    )
    with pytest.raises(FileFormatError) as raised:
        call()
    assert isinstance(raised.value.__cause__, ValueError)


@pytest.mark.parametrize(
    "content",
    [
        "1e308",
        "-1e308",
        "1e-999",
        "-0.0",
        "1234567890123456789012345678901234567890",
        '{"s":"1e999","n":1.5}',
    ],
)
def test_strict_json_preserves_finite_numbers_large_integers_and_strings(
    tmp_path: Path,
    content: str,
) -> None:
    """Finite conversion, arbitrary integers, strings and source metadata survive."""
    codec = JsonCodec()
    file = codec.parse(ResolvedPath(tmp_path), content)
    assert file.content == content
    assert file.byte_size == len(content.encode())
    assert isinstance(file, JsonScalarFile | JsonObjectFile | JsonListFile)
    roundtrip = codec.parse(ResolvedPath(tmp_path), codec.serialize(file))
    assert isinstance(roundtrip, JsonScalarFile | JsonObjectFile | JsonListFile)
    assert roundtrip.value == file.value
    assert file.value == json.loads(content)


def test_json_float_conversion_failure_preserves_domain_cause(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An injected lower-level conversion failure retains its exception chain."""

    def conversion_failure(_value: str) -> float:
        message = "Simulated lower-level float overflow"
        raise OverflowError(message)

    monkeypatch.setattr(json_module, "float", conversion_failure, raising=False)
    with pytest.raises(FileFormatError) as raised:
        JsonCodec().parse(ResolvedPath(tmp_path), "1.5")
    assert isinstance(raised.value.__cause__, ValueError)
    assert isinstance(raised.value.__cause__.__cause__, OverflowError)
