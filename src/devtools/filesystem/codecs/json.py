# Copyright (c) 2026
"""JSON representation codec."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import TYPE_CHECKING

from devtools.filesystem.errors import (
    FileFormatError,
    TextDecodingError,
    TextEncodingError,
)
from devtools.filesystem.models import (
    JsonFile,
    JsonListFile,
    JsonObjectFile,
    JsonScalarFile,
)
from devtools.filesystem.models.json import freeze_json, thaw_json

if TYPE_CHECKING:
    from devtools.filesystem.models.json import JsonValue
    from devtools.paths import ResolvedPath


class JsonCodec:
    """Convert JSON source representations and immutable JSON file models."""

    def decode(
        self,
        path: ResolvedPath,
        content: bytes,
        *,
        encoding: str = "utf-8",
    ) -> JsonFile:
        """Decode and parse JSON bytes without accessing the filesystem.

        :param path: Source path represented by the resulting model.
        :param content: Raw JSON bytes.
        :param encoding: Encoding used for byte decoding.
        :returns: Concrete immutable JSON file model.
        :raises TextDecodingError: If the bytes cannot be decoded.
        """
        try:
            source = content.decode(encoding)
        except (UnicodeDecodeError, LookupError) as error:
            msg = f"Unable to decode {path} using encoding {encoding!r}."
            raise TextDecodingError(msg) from error

        return self.parse(
            path,
            source,
            encoding=encoding,
            byte_size=len(content),
        )

    def parse(
        self,
        path: ResolvedPath,
        content: str,
        *,
        encoding: str = "utf-8",
        byte_size: int | None = None,
    ) -> JsonFile:
        """Parse JSON source text into a concrete immutable model.

        :param path: Source path represented by the resulting model.
        :param content: Decoded JSON source text.
        :param encoding: Encoding metadata for the source text.
        :param byte_size: Source byte size, derived from the encoding when omitted.
        :returns: Concrete immutable JSON file model.
        :raises FileFormatError: If the source is not valid strict JSON.
        :raises TextEncodingError: If byte-size derivation cannot encode content.
        """
        source_size = byte_size

        if source_size is None:
            try:
                source_size = len(content.encode(encoding))
            except (UnicodeEncodeError, LookupError) as error:
                msg = f"Unable to encode JSON source using {encoding!r}."
                raise TextEncodingError(msg) from error

        try:
            parsed = json.loads(
                content,
                parse_constant=_reject_nonstandard_constant,
            )
        except (json.JSONDecodeError, ValueError) as error:
            msg = _format_parse_error(error)
            raise FileFormatError(msg) from error

        value = freeze_json(parsed)

        if isinstance(value, Mapping):
            return JsonObjectFile(
                path,
                content,
                encoding=encoding,
                byte_size=source_size,
                value=value,
            )

        if isinstance(value, tuple):
            return JsonListFile(
                path,
                content,
                encoding=encoding,
                byte_size=source_size,
                value=value,
            )

        if isinstance(value, str | int | float | bool) or value is None:
            return JsonScalarFile(
                path,
                content,
                encoding=encoding,
                byte_size=source_size,
                value=value,
            )

        msg = f"Unsupported frozen JSON root type: {type(value).__name__}."
        raise FileFormatError(msg)

    def serialize(
        self,
        file: JsonFile,
        *,
        indent: int | None = 2,
        ensure_ascii: bool = False,
        sort_keys: bool = False,
        trailing_newline: bool = True,
    ) -> str:
        """Serialize a model's current structured value into JSON text.

        :param file: Immutable JSON file model.
        :param indent: Indentation width, or ``None`` for compact output.
        :param ensure_ascii: Whether non-ASCII characters should be escaped.
        :param sort_keys: Whether object keys should be sorted.
        :param trailing_newline: Whether to append a final newline.
        :returns: JSON representation of the current structured value.
        :raises FileFormatError: If the file does not have a concrete JSON root.
        """
        value = _get_value(file)
        separators = (",", ":") if indent is None else None
        try:
            serialized = json.dumps(
                thaw_json(value),
                indent=indent,
                ensure_ascii=ensure_ascii,
                sort_keys=sort_keys,
                separators=separators,
                allow_nan=False,
            )
        except ValueError as error:
            msg = "JSON model value cannot be serialized as strict JSON."
            raise FileFormatError(msg) from error

        return f"{serialized}\n" if trailing_newline else serialized

    def encode(
        self,
        file: JsonFile,
        *,
        encoding: str | None = None,
    ) -> bytes:
        """Serialize and encode a JSON model without writing to disk.

        :param file: Immutable JSON file model.
        :param encoding: Output encoding, defaulting to the model encoding.
        :returns: Encoded JSON representation of the current structured value.
        :raises TextEncodingError: If the serialized text cannot be encoded.
        """
        target_encoding = file.encoding if encoding is None else encoding
        serialized = self.serialize(file)

        try:
            return serialized.encode(target_encoding)
        except (UnicodeEncodeError, LookupError) as error:
            msg = f"Unable to encode JSON using {target_encoding!r}."
            raise TextEncodingError(msg) from error


def _reject_nonstandard_constant(value: str) -> None:
    """Reject non-standard JSON constants accepted by Python's parser."""
    msg = f"Invalid JSON constant: {value}."
    raise ValueError(msg)


def _format_parse_error(error: json.JSONDecodeError | ValueError) -> str:
    """Create a useful filesystem-domain JSON parse error message."""
    if isinstance(error, json.JSONDecodeError):
        return (
            f"Invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}."
        )

    return str(error)


def _get_value(file: JsonFile) -> JsonValue:
    """Return the structured value from a concrete JSON file model."""
    if isinstance(file, JsonObjectFile | JsonListFile | JsonScalarFile):
        return file.value

    msg = "JsonCodec requires a concrete JSON root model."
    raise FileFormatError(msg)
