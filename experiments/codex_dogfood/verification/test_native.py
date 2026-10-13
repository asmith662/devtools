# Copyright (c) 2026
# ruff: noqa: S101, S311, D103, COM812 -- deterministic codec fixtures
"""Decode-once, alias relocation, native type and exact historical codec checks."""

from __future__ import annotations

import base64
import copy
import importlib
import random
import re
from dataclasses import dataclass
from hashlib import sha256

import pytest

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.case_0012.stage_b.durability import pack
from experiments.codex_dogfood.case_0012.stage_b.graph import describe

from .archive import decoder
from .encoding import GraphEncoding
from .journal import ArchiveMemo
from .native import NativeMemo
from .references import render, surface, template


def test_reference_scanner_exact_regex() -> None:
    numpy = importlib.import_module("numpy")
    random_source = random.Random(16)
    for size in (0, 1, 5, 50, 1000):
        raw = b",".join(
            b'{"ref": ' + str(random_source.randrange(10000000)).encode() + b"}"
            for _ in range(size)
        )
        expected = tuple(map(int, re.findall(rb'"ref": ([0-9]+)', raw)))
        values, actual = surface(numpy, raw, normalized=True)
        assert tuple(map(int, values)) == expected
        assert actual == sha256(re.sub(rb'"ref": ([0-9]+)', b'"ref": @', raw)).digest()
    raw = b" " * (1024 * 1024 - 3) + b'{"ref": 12345}'
    values, actual = surface(numpy, raw, normalized=True)
    assert tuple(map(int, values)) == (12345,)
    assert actual == sha256(re.sub(rb'"ref": ([0-9]+)', b'"ref": @', raw)).digest()


def test_reference_template_exact_relocation() -> None:
    numpy = importlib.import_module("numpy")
    raw = b'{"ref": 9}, {"ref": 123}, "value": "@email", {"ref": 0}'
    base, slots = template(numpy, raw)
    expected = b'{"ref": 1000}, {"ref": 4}, "value": "@email", {"ref": 9}'
    assert (
        render(numpy, base, slots, numpy.asarray([1000, 4, 9], dtype=numpy.int64))
        == expected
    )
    assert (
        render(numpy, base, slots, numpy.asarray([9, 123, 0], dtype=numpy.int64)) == raw
    )


@dataclass(frozen=True)
class Retained:
    """Immutable retained fixture whose child aliases remain visible."""

    children: tuple[object, ...]


def test_parse_once_and_new_invocation() -> None:
    raw = b'{"type":"fixture","value":1}'
    memo = NativeMemo()
    assert memo.parse(raw) is memo.parse(bytes(bytearray(raw)))
    assert memo.json_decodes == 1
    fresh = NativeMemo()
    assert fresh.json_decodes == 0
    assert fresh.parse(raw) == memo.parse(raw)
    assert fresh.json_decodes == 1


def test_archive_once_and_exact_digest_binding() -> None:
    memo = ArchiveMemo()
    block = pack(b"native archive" * 100)
    assert memo.unpack(block) == memo.unpack(copy.deepcopy(block))
    assert memo.decompressions == 1
    assert memo.hits == 1
    with pytest.raises(ValueError, match="archive digest differs"):
        memo.unpack(block | {"sha256": "0" * 64})
    altered = dict(block)
    altered["gzip_b85"] = "0" + altered["gzip_b85"][1:]
    with pytest.raises((ValueError, OSError)):
        memo.unpack(altered)
    fresh = ArchiveMemo()
    assert fresh.unpack(block) == memo.unpack(block)
    assert fresh.decompressions == 1


def test_base85_exact_historical_codec() -> None:
    decode = decoder()
    random_source = random.Random(16)
    for size in (*range(50), 4096, 100001):
        value = random_source.randbytes(size)
        encoded = base64.b85encode(value)
        assert decode(encoded) == base64.b85decode(encoded) == value
    for value in (b" ", b"~~~~~", b"abc\xff", b"zzzzz"):
        try:
            expected = base64.b85decode(value)
        except ValueError:
            with pytest.raises(ValueError, match="base85"):
                decode(value)
        else:
            assert decode(value) == expected


def test_alias_relocation_type_fields_order_and_unique_closure() -> None:
    shared = Retained(tuple((i, str(i)) for i in range(1200)))
    memo = NativeMemo()
    assert memo.corresponds(shared, json_bytes(describe(shared)))
    first = memo.recursive_visits
    assert memo.corresponds(
        ("offset", shared, shared), json_bytes(describe(("offset", shared, shared)))
    )
    assert memo.recursive_visits - first == 1
    assert memo.blocks_checked > 0
    for name in ("alias", "type", "field", "order"):
        value = describe((shared, shared))
        if name == "alias":
            value["nodes"][0]["items"][1] = {"ref": 2}
        elif name == "type":
            value["nodes"][1]["type"] = "untrusted.Other"
        elif name == "field":
            value["nodes"][-1]["items"][0] = 999
        else:
            value["nodes"][-1]["items"].reverse()
        assert not memo.corresponds((shared, shared), json_bytes(value))


def test_native_description_template_exact_bytes() -> None:
    shared = Retained(tuple((i, str(i)) for i in range(80)))
    memo = NativeMemo()
    encoder = GraphEncoding(memo)
    for value in (
        shared,
        (shared, shared),
        {"ordered": shared, "again": shared},
        -0.0,
        None,
    ):
        assert encoder.encode(value) == json_bytes(describe(value))
    mutable = [1, 2]
    assert encoder.encode(mutable) == json_bytes(describe(mutable))
    mutable[0] = 3
    assert encoder.encode(mutable) == json_bytes(describe(mutable))
