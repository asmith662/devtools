# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, C901, PLR0911, PLR0912, PLR0915, PLR2004 -- exact authenticated block boundary
"""Skip authenticated immutable closures while checking each local alias binding.

Exact byte digests are retained for each proven ordinal relocation. A new
relocation checks the complete non-reference byte skeleton and every reference.
No node-boundary scan or JSON decode is needed inside an authenticated closure.
"""

from __future__ import annotations

import importlib
import json
import re
import time
from dataclasses import is_dataclass
from hashlib import sha256
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import json_bytes

from .fields import FieldChecks
from .references import render, surface, template


class Blocks:
    """Immutable native closure certificates, never shared between invocations."""

    def __init__(self, memo: Any) -> None:
        """Own all certificate and dense-ordinal indices for this invocation."""
        self.memo = memo
        self.blocks: dict[int, list[Any]] = {}
        self.refs = re.compile(rb'"ref": ([0-9]+)')
        self.numpy: Any = None
        try:
            self.numpy = importlib.import_module("numpy")
        except ImportError:
            self.numpy = None
        self.hits = 0
        self.alias_bindings = 0
        self.times: dict[str, int] = {}
        self.events: list[dict[str, Any]] = []
        self.registry: dict[int, tuple[Any, int]] = {}
        self.ordinal_bytes: Any = None
        self.field_checks = FieldChecks()

    def decimals(self, maximum: int) -> Any:
        """Cache exact integer encoding, never input authentication or trust."""
        existing = 0 if self.ordinal_bytes is None else len(self.ordinal_bytes)
        if maximum >= existing:
            size = max(1024, 1 << maximum.bit_length())
            new = (
                self.numpy.arange(existing, size, dtype=self.numpy.int64)
                .astype(f"S{len(str(size))}")
                .tolist()
            )
            old = [] if self.ordinal_bytes is None else self.ordinal_bytes.tolist()
            self.ordinal_bytes = self.numpy.asarray(old + new, dtype=object)
        return self.ordinal_bytes

    def index(self, item: Any) -> int:
        """Assign a dense lookup key; this is never proof of correspondence."""
        key = id(item)
        if key not in self.registry:
            self.registry[key] = (item, len(self.registry))
        return self.registry[key][1]

    def numbers(self, raw: bytes) -> Any:
        """Parse complete reference digits, without fixed-width truncation."""
        if self.numpy is None:
            values = self.refs.findall(raw)
            return tuple(map(int, values))
        return surface(self.numpy, raw, normalized=False)[0]

    def digits(self, values: Any) -> int:
        """Compute exact decimal lengths used by historical canonical references."""
        if self.numpy is None:
            return sum(len(str(v)) for v in values)
        return int(
            len(values)
            + self.numpy.searchsorted(
                [10**i for i in range(1, 19)], values, side="right"
            ).sum()
        )

    def authenticate(self, root: Any, raw: bytes) -> bool:
        """Check one return envelope and every field/alias it binds."""
        tail = raw.rfind(b'\n  "root":')
        if tail < 0:
            return False
        graph = self.memo.parse(b"{" + raw[tail:])
        if (
            set(graph) != {"root", "schema"}
            or graph["schema"] != "case-0012-native-graph-v1"
        ):
            return False
        cursor = len(b'{\n  "nodes": [\n')
        if not raw.startswith(b'{\n  "nodes": ['):
            return False
        bulk = None
        if (len(self.memo.unique_nodes) < 10000 and len(raw) > 5_000_000) or (
            type(root).__name__ == "PythonDeclarationReferenceAnalysis"
            and len(raw) > 100000
        ):
            bulk = json.loads(raw)["nodes"]
            self.memo.json_decodes += 1
        seen: dict[int, int] = {}
        assigned = (
            self.numpy.full(
                max(1_000_000, 2 * len(self.registry)), -1, dtype=self.numpy.int64
            )
            if self.numpy is not None
            else None
        )
        objects: list[Any] = []
        mutable: list[int] = []
        tail_bulk: Any = None
        tail_first = 0
        body_end = raw.rfind(b"\n  ],", 0, tail)

        def previous(item: Any) -> int | None:
            if assigned is None:
                return seen.get(id(item))
            hit = self.registry.get(id(item))
            if hit is None or hit[1] >= len(assigned):
                return None
            value = int(assigned[hit[1]])
            return value if value >= 0 else None

        def record(item: Any, ordinal: int) -> None:
            nonlocal assigned
            if assigned is None:
                seen[id(item)] = ordinal
            else:
                index = self.index(item)
                if index >= len(assigned):
                    assigned = self.numpy.pad(
                        assigned, (0, len(assigned)), constant_values=-1
                    )
                assigned[index] = ordinal

        def certificate(item: Any, first: int, start: int) -> None:
            count = len(objects) - first
            minimum = (
                1024
                if isinstance(item, tuple)
                or "retrieval.lexical" in type(item).__module__
                else 64
            )
            if count < minimum or (mutable and mutable[-1] >= first):
                return
            selected = isinstance(item, tuple) or type(item).__name__ in {
                "PythonModuleInterpretationUniverse",
                "ReferenceView",
            }
            if count > 2048 and not selected:
                return
            # A different surrounding alias layout is handled by the existing
            # child certificates. Do not rebuild a complete closure certificate
            # merely because an ancestor was visited in another envelope.
            if id(item) in self.blocks:
                return
            began = time.perf_counter_ns()
            block = raw[start:cursor]
            refs = self.numbers(block)
            if self.numpy is not None and len(refs):
                self.decimals(int(refs.max()))
            foreign = {
                int(v): objects[int(v)]
                for v in set(map(int, refs))
                if not first <= int(v) < first + count
            }
            positions: Any
            if self.numpy is not None:
                external = (refs < first) | (refs >= first + count)
                external_values = self.numpy.array(
                    list(foreign), dtype=self.numpy.int64
                )
                order = self.numpy.argsort(external_values)
                external_values = external_values[order]
                foreign = {int(v): foreign[int(v)] for v in external_values}
                positions = (
                    external,
                    self.numpy.searchsorted(external_values, refs[external]),
                )
            else:
                positions = {
                    v: tuple(i for i, r in enumerate(refs) if r == v) for v in foreign
                }
            members = tuple(objects[first:])
            member_indices = (
                self.numpy.asarray(
                    [self.index(o) for o in members], dtype=self.numpy.int64
                )
                if self.numpy is not None
                else None
            )
            foreign_indices = (
                self.numpy.asarray(
                    [self.index(o) for o in foreign.values()], dtype=self.numpy.int64
                )
                if self.numpy is not None
                else None
            )
            self.blocks.setdefault(id(item), []).append(
                (
                    members,
                    {id(o) for o in members},
                    first,
                    refs,
                    foreign,
                    positions,
                    len(block),
                    self.digits(refs),
                    sha256(self.refs.sub(b'"ref": @', block)).digest(),
                    {},
                    member_indices,
                    foreign_indices,
                    template(self.numpy, block) if self.numpy is not None else None,
                )
            )
            original_bound: Any = (
                self.numpy.asarray(list(foreign), dtype=self.numpy.int64)
                if self.numpy is not None
                else tuple(foreign)
            )
            signature = (
                sha256(original_bound.tobytes()).digest()
                if self.numpy is not None
                else original_bound
            )
            self.blocks[id(item)][-1][9][(first, signature)] = (
                sha256(block).digest(),
                len(block),
            )
            self.times["certificate"] = (
                self.times.get("certificate", 0) + time.perf_counter_ns() - began
            )

        def visit(item: Any, expected: Any) -> bool:
            nonlocal cursor, tail_bulk, tail_first
            if item is None or type(item) in (bool, int, float, str):
                return type(item) is type(expected) and (
                    item.hex() == expected.hex()
                    if isinstance(item, float)
                    else item == expected
                )
            if (
                type(expected) is not dict
                or set(expected) != {"ref"}
                or type(expected["ref"]) is not int
            ):
                return False
            old = previous(item)
            if old is not None:
                return bool(expected == {"ref": old})
            ordinal = len(objects)
            if expected != {"ref": ordinal}:
                return False
            if ordinal:
                if raw[cursor : cursor + 2] != b",\n":
                    return False
                cursor += 2
            start = cursor
            for retained in self.blocks.get(id(item), ()):
                began = time.perf_counter_ns()
                (
                    members,
                    member_ids,
                    first,
                    refs,
                    foreign,
                    positions,
                    length,
                    digit_count,
                    skeleton,
                    variants,
                    member_indices,
                    foreign_indices,
                    compiled,
                ) = retained
                bound: Any
                signature: Any
                if assigned is None:
                    if not member_ids.isdisjoint(seen):
                        continue
                    bound = tuple(seen.get(id(value), -1) for value in foreign.values())
                    if -1 in bound:
                        continue
                    signature = bound
                else:
                    if self.numpy.any(assigned[member_indices] >= 0):
                        continue
                    bound = assigned[foreign_indices]
                    if self.numpy.any(bound < 0):
                        continue
                    signature = sha256(bound.tobytes()).digest()
                variant_key = (ordinal, signature)
                if variant_key in variants:
                    exact, size = variants[variant_key]
                    block = raw[start : start + size]
                    passed = sha256(block).digest() == exact
                else:
                    vector_start = time.perf_counter_ns()
                    needed: Any = (
                        refs.copy()
                        if self.numpy is not None
                        else [r + ordinal - first for r in refs]
                    )
                    if self.numpy is not None:
                        needed += ordinal - first
                    if self.numpy is not None:
                        needed[positions[0]] = self.numpy.asarray(
                            bound, dtype=self.numpy.int64
                        )[positions[1]]
                    else:
                        for v, target in zip(foreign, bound, strict=True):
                            for pos in positions[v]:
                                needed[pos] = target
                    size = length + self.digits(needed) - digit_count
                    block = raw[start : start + size]
                    vector_ns = time.perf_counter_ns() - vector_start
                    number_start = time.perf_counter_ns()
                    if self.numpy is not None:
                        expected_block = render(
                            self.numpy,
                            compiled[0],
                            compiled[1],
                            needed,
                            self.decimals(int(needed.max()) if len(needed) else 0),
                        )
                        same_refs = expected_block == block
                        actual_skeleton = skeleton if same_refs else None
                        actual = needed
                    else:
                        actual = self.numbers(block)
                        actual_skeleton = sha256(
                            self.refs.sub(b'"ref": @', block)
                        ).digest()
                    number_ns = time.perf_counter_ns() - number_start
                    same_refs = (
                        bool(self.numpy.array_equal(actual, needed))
                        if self.numpy is not None
                        else tuple(actual) == tuple(needed)
                    )
                    passed = same_refs and actual_skeleton == skeleton
                    if passed:
                        variants[variant_key] = (sha256(block).digest(), size)
                    self.events.append(
                        {
                            "type": type(item).__name__,
                            "bytes": size,
                            "members": len(members),
                            "foreign": len(foreign),
                            "vector_ns": vector_ns,
                            "numbers_ns": number_ns,
                            "passed": bool(passed),
                            "lookup_ns": time.perf_counter_ns() - began,
                        }
                    )
                if passed:
                    if assigned is None:
                        seen.update((id(o), ordinal + i) for i, o in enumerate(members))
                    else:
                        assigned[member_indices] = self.numpy.arange(
                            ordinal, ordinal + len(members)
                        )
                    objects.extend(members)
                    cursor += size
                    self.hits += 1
                    self.alias_bindings += len(members)
                    return True
            end = raw.find(b"\n    }", cursor)
            if end < 0 or raw[cursor : cursor + 5] != b"    {":
                return False
            cursor = end + 6
            record(item, ordinal)
            objects.append(item)
            self.memo.recursive_visits += 1
            self.memo.unique_nodes[id(item)] = item
            if isinstance(item, (dict, list)) or (
                is_dataclass(item)
                and not vars(type(item))["__dataclass_params__"].frozen
            ):
                mutable.append(ordinal)
            if bulk is not None:
                node = bulk[ordinal]
            else:
                if (
                    tail_bulk is None
                    and ordinal > 10000
                    and 0 < body_end - start < 8_000_000
                ):
                    tail_bulk = json.loads(b"[" + raw[start:body_end] + b"]")
                    tail_first = ordinal
                    self.memo.json_decodes += 1
                node = (
                    tail_bulk[ordinal - tail_first]
                    if tail_bulk is not None
                    else self.memo.parse(raw[start:cursor])
                )
            value: Any
            checker = self.field_checks.checker(item)
            kind, value = (
                ("fields", None) if checker is not None else self.memo.description(item)
            )
            key = "items" if kind == "mapping" else kind
            if (
                set(node) != {"type", key}
                or node["type"] != type(item).__module__ + "." + type(item).__qualname__
            ):
                return False
            actual = node[key]
            if kind == "fields":
                passed = bool(checker(item, actual, visit))
            elif kind == "mapping":
                passed = len(actual) == len(value) and all(
                    len(pair) == 2 and visit(k, pair[0]) and visit(v, pair[1])
                    for (k, v), pair in zip(value, actual, strict=True)
                )
            elif kind == "items":
                passed = len(actual) == len(value) and all(
                    visit(v, e) for v, e in zip(value, actual, strict=True)
                )
            else:
                passed = json_bytes(value) == json_bytes(actual)
            if passed and kind in {"fields", "items"}:
                immutable = isinstance(item, tuple) or (
                    kind == "fields" and vars(type(item))["__dataclass_params__"].frozen
                )
                if immutable:
                    certificate(item, ordinal, start)
            return bool(passed)

        passed = visit(root, graph["root"])
        if not objects:
            return passed and raw[:tail] == b'{\n  "nodes": [],'
        self.memo.nodes_checked += len(objects)
        return bool(passed and raw[cursor:tail] == b"\n  ],")
