# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, D102, D107, C901, PLR0911, PLR0912, PLR0915, PLR2004, COM812 -- full graph boundary
"""Native/canonical graph correspondence after exact capture-byte authentication.

Canonical bytes must first match an authoritative seal. This permits comparing
their decoded graph directly, without re-encoding hundreds of MB per return.
Every field, native type, primitive, traversal ordinal and alias is checked.
Object identity indexes retained objects; it never establishes correspondence.
"""

from __future__ import annotations

import inspect
import json
import re
from dataclasses import fields, is_dataclass
from enum import Enum
from hashlib import sha256
from pathlib import PurePath
from typing import Any

from devtools.core.identity import Identity
from experiments.codex_dogfood.case_0012.stage_b.canonical import NativeEncoder

from .bindings import bind
from .blocks import Blocks
from .encoding import GraphEncoding


class NativeMemo:
    """Read-only retained state and pure derived values, owned by one invocation."""

    def __init__(self) -> None:
        self.shallow: dict[int, tuple[Any, str, Any]] = {}
        self.type_fields: dict[type[Any], Any] = {}
        self.encoder = NativeEncoder()
        self.identities: dict[int, tuple[Any, Any]] = {}
        self.getters: dict[Any, Any] = {}
        self.resources: dict[int, tuple[Any, dict[Any, Any]]] = {}
        self.nodes_checked = 0
        self.blocks: dict[int, list[Any]] = {}
        self.blocks_checked = 0
        self.envelopes = 0
        self.parsed: dict[bytes, Any] = {}
        self.json_decodes = 0
        self.parse_hits = 0
        self.unique_nodes: dict[int, Any] = {}
        self.recursive_visits = 0
        self.on_envelope: Any = lambda: None
        self.state_indices: dict[int, Any] = {}
        self.pair_indices: dict[int, Any] = {}
        self.member_indices: dict[int, Any] = {}
        self.encoding = GraphEncoding(self)
        self.certificates = Blocks(self)
        self.archives: Any = None

    def parse(self, raw: bytes) -> Any:
        """Decode an exactly content-bound canonical fragment once locally."""
        key = sha256(raw).digest()
        if key in self.parsed:
            self.parse_hits += 1
            return self.parsed[key]
        result = json.loads(raw)
        self.json_decodes += 1
        self.parsed[key] = result
        return result

    def services(self) -> dict[str, Any]:
        return {
            "_memo_identity": self.identity,
            "_memo_resource": self.resource,
            "_memo_state": self.state,
            "_memo_pair": self.pair,
            "_memo_member": self.member,
        }

    def state(self, ranking: Any, address: Any) -> Any:
        if id(ranking) not in self.state_indices:
            self.state_indices[id(ranking)] = (
                ranking,
                {s.address: s.stationary_mass for s in ranking.states},
            )
        index = self.state_indices[id(ranking)][1]
        if address not in index:
            raise StopIteration
        return index[address]

    def pair(self, view: Any, source: str, target: str) -> Any:
        if id(view) not in self.pair_indices:
            self.pair_indices[id(view)] = (
                view,
                {(str(e.source), str(e.target)): e for e in view.edges},
            )
        index = self.pair_indices[id(view)][1]
        if (source, target) not in index:
            raise StopIteration
        return index[source, target]

    def member(self, members: Any, address: str) -> Any:
        if id(members) not in self.member_indices:
            self.member_indices[id(members)] = (members, {str(r): r for r in members})
        index = self.member_indices[id(members)][1]
        if address not in index:
            raise StopIteration
        return index[address]

    def resource(self, snapshot: Any, address: Any) -> Any:
        hit = self.resources.get(id(snapshot))
        if hit is None:
            index = {r.address: r for r in snapshot.resources}
            if len(index) != len(snapshot.resources):
                raise ValueError("Duplicate retained resource address")
            hit = (snapshot, index)
            self.resources[id(snapshot)] = hit
        if address in hit[1]:
            return hit[1][address]
        # Preserve the native missing-address exception and message.
        return snapshot.resource_at(address)

    def identity(self, value: Any) -> Any:
        hit = self.identities.get(id(value))
        if hit is not None and hit[0] is value:
            return hit[1]
        descriptor = inspect.getattr_static(type(value), "identity", None)
        if isinstance(descriptor, property) and descriptor.fget is not None:
            getter = self.getters.get(descriptor.fget)
            if getter is None:
                getter = bind(descriptor.fget, self.services(), lookups=True)
                self.getters[descriptor.fget] = getter
            result = getter(value)
        else:
            result = value.identity
        # Only immutable native values are eligible; mutable objects are reread.
        if is_dataclass(value) and vars(type(value))["__dataclass_params__"].frozen:
            self.identities[id(value)] = (value, result)
        return result

    def description(self, item: Any) -> tuple[str, Any]:
        hit = self.shallow.get(id(item))
        if hit is not None and hit[0] is item:
            return hit[1], hit[2]
        if isinstance(item, dict):
            return "mapping", tuple(item.items())
        if isinstance(item, (tuple, list)):
            return "items", item
        if isinstance(item, (Identity, PurePath, Enum)):
            kind, value = "value", self.encoder.default(item)
        elif is_dataclass(item) and not isinstance(item, type):
            names = self.type_fields.get(type(item))
            if names is None:
                names = tuple(f.name for f in fields(item))
                self.type_fields[type(item)] = names
            kind, value = (
                "fields",
                {name: getattr(item, name) for name in names}.items(),
            )
        else:
            kind, value = "value", self.encoder.default(item)
        if isinstance(item, (Identity, PurePath, Enum)) or (
            is_dataclass(item) and vars(type(item))["__dataclass_params__"].frozen
        ):
            self.shallow[id(item)] = (item, kind, value)
        return kind, value

    def corresponds(self, native: Any, canonical: bytes) -> bool:
        """Compare regenerated exact bytes using unique native node projections."""
        self.envelopes += 1
        self.on_envelope()
        before = self.certificates.hits
        passed = self.certificates.authenticate(native, canonical)
        self.blocks_checked += self.certificates.hits - before
        return passed

    def legacy_corresponds(self, native: Any, canonical: bytes) -> bool:
        """Check authenticated canonical fields against the actual native return."""
        self.envelopes += 1
        self.on_envelope()
        tail = canonical.rfind(b'\n  "root":')
        if tail < 0:
            return False
        graph = self.parse(b"{" + canonical[tail:])
        if (
            set(graph) != {"schema", "root"}
            or graph["schema"] != "case-0012-native-graph-v1"
        ):
            return False
        seen: dict[int, int] = {}
        objects: list[Any] = []
        mutable_ordinals: list[int] = []
        starts = [m.start() + 1 for m in re.finditer(rb"\n    \{\n", canonical)]
        ends = [m.end() for m in re.finditer(rb"\n    \}", canonical)]
        if len(starts) != len(ends):
            return False
        bulk_nodes = None

        def block_surface(first: int, count: int) -> tuple[str, tuple[int, ...]]:
            raw = canonical[starts[first] : ends[first + count - 1]]
            pattern = rb'"ref": (\d+)'
            references = tuple(int(m[1]) for m in re.finditer(pattern, raw))
            skeleton = sha256(re.sub(pattern, b'"ref": @', raw)).hexdigest()
            return skeleton, references

        def remember(item: Any, ordinal: int, *, minimum: int = 64) -> None:
            count = len(objects) - ordinal
            if count < minimum or (
                mutable_ordinals and mutable_ordinals[-1] >= ordinal
            ):
                return
            skeleton, refs = block_surface(ordinal, count)
            normalized = tuple(
                r - ordinal if ordinal <= r < ordinal + count else (objects[r], r)
                for r in refs
            )
            self.blocks.setdefault(id(item), []).append(
                (
                    tuple(objects[ordinal:]),
                    skeleton,
                    normalized,
                    ordinal,
                    sha256(
                        canonical[starts[ordinal] : ends[ordinal + count - 1]]
                    ).hexdigest(),
                )
            )

        def visit(item: Any, expected: Any) -> bool:
            if item is None or type(item) in (bool, int, float, str):
                if type(item) is not type(expected):
                    return False
                return bool(
                    item.hex() == expected.hex()
                    if isinstance(item, float)
                    else item == expected
                )
            previous = seen.get(id(item))
            if previous is not None:
                return bool(expected == {"ref": previous})
            ordinal = len(seen)
            if expected != {"ref": ordinal} or ordinal >= len(starts):
                return False
            for retained in self.blocks.get(id(item), ()):
                members, skeleton, references, original_ordinal, exact_digest = retained
                count = len(members)
                if ordinal + count > len(starts) or any(id(o) in seen for o in members):
                    continue
                raw = canonical[starts[ordinal] : ends[ordinal + count - 1]]
                if (
                    ordinal == original_ordinal
                    and sha256(raw).hexdigest() == exact_digest
                ):
                    foreign = (r for r in references if not isinstance(r, int))
                    if all(seen.get(id(r[0]), -1) == r[1] for r in foreign):
                        seen.update((id(o), ordinal + i) for i, o in enumerate(members))
                        objects.extend(members)
                        self.blocks_checked += 1
                        return True
                current_skeleton, current_references = block_surface(ordinal, count)
                if current_skeleton != skeleton or len(current_references) != len(
                    references
                ):
                    continue
                # Internal refs are relative ordinals; outside aliases bind to
                # actual already-authenticated native objects, not filenames.
                wanted = tuple(
                    ordinal + r if isinstance(r, int) else seen.get(id(r[0]), -1)
                    for r in references
                )
                if current_references == wanted:
                    seen.update((id(o), ordinal + i) for i, o in enumerate(members))
                    objects.extend(members)
                    self.blocks_checked += 1
                    return True
            seen[id(item)] = ordinal
            objects.append(item)
            self.recursive_visits += 1
            self.unique_nodes[id(item)] = item
            if isinstance(item, (dict, list)):
                mutable_ordinals.append(ordinal)
            node = (
                bulk_nodes[ordinal]
                if bulk_nodes is not None
                else self.parse(canonical[starts[ordinal] : ends[ordinal]])
            )
            native_type = type(item).__module__ + "." + type(item).__qualname__
            if node.get("type") != native_type:
                return False
            kind, value = self.description(item)
            key = "items" if kind == "mapping" else kind
            if set(node) != {"type", key}:
                return False
            actual = node[key]
            if kind == "fields":
                passed = set(actual) == {k for k, _ in value} and all(
                    visit(v, actual[k]) for k, v in value
                )
                if (
                    passed
                    and not (mutable_ordinals and mutable_ordinals[-1] >= ordinal)
                    and vars(type(item))["__dataclass_params__"].frozen
                ):
                    remember(
                        item,
                        ordinal,
                        minimum=2
                        if type(item).__name__ == "RepositoryTextLexicalTermPostings"
                        else 64,
                    )
                return passed
            if kind == "mapping":
                return len(value) == len(actual) and all(
                    len(pair) == 2 and visit(k, pair[0]) and visit(v, pair[1])
                    for (k, v), pair in zip(value, actual, strict=True)
                )
            if kind == "items":
                passed = len(value) == len(actual) and all(
                    visit(v, other) for v, other in zip(value, actual, strict=True)
                )
                if passed and isinstance(item, tuple) and len(item) >= 32:
                    remember(item, ordinal)
                return passed
            return bool(value == actual)

        passed = visit(native, graph["root"]) and len(seen) == len(starts)
        self.nodes_checked += len(seen)
        return passed
