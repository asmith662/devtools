# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, PLR2004 -- concrete bounded worker composition
"""Read-only Qwen Tools over the existing admitted RI/Context source index.

No independent index, semantic identity, command capability or edit authority is
defined here. One host-selected corpus is retained, drift checked and refreshed
only after a host-admitted edit. Tool results are data, never instructions.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING, Any, cast

from apps.qwen.model_tool_composition import normalize_tool_descriptor
from devtools.context import (
    Repository,
    RepositoryResourceAddress,
    materialize_disclosure_plan,
    observe_repository_resources,
    plan_disclosures,
)
from devtools.context.planning import SourceSearchDisclosureOption
from devtools.context.python.modules.interpretation import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.retrieval import (
    build_source_search_index,
    search_repository_source,
)
from devtools.core.paths import resolve_path
from devtools.tools import ToolDescriptor, ToolRunner

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.tasks import CodingTask
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.source import RepositorySourceUnit, SourceSearchMode
    from devtools.models.interaction import ModelToolCall, ModelToolDefinition


CONTEXT_TOOL_NAMES = (
    "search_source",
    "lookup_symbol",
    "read_source",
    "expand_source",
    "source_relationships",
)


def _schema(name: str, properties: dict[str, Any]) -> ToolDescriptor:
    return ToolDescriptor(
        name,
        {
            "search_source": (
                "Search the admitted corpus; returns versioned source units."
            ),
            "lookup_symbol": (
                "Exact qualified Python source-view name lookup; retains all matches."
            ),
            "read_source": (
                "Read an exact character range from a known path and version; "
                "bounded, possibly truncated."
            ),
            "expand_source": (
                "Expand a known unit to its parent symbol, class or file; "
                "returns metadata for optional reading."
            ),
            "source_relationships": (
                "Inspect bounded static outgoing Python references/calls in a "
                "versioned file. Not exhaustive runtime analysis."
            ),
        }[name],
        json.dumps(
            {
                "type": "object",
                "properties": properties,
                "required": list(properties),
                "additionalProperties": False,
            }
        ),
    )


_TEXT = {"type": "string", "minLength": 1, "maxLength": 512}
_DEFINITIONS = (
    _schema(
        "search_source",
        {
            "query": _TEXT,
            "mode": {"type": "string", "enum": ["file", "symbol", "window", "mixed"]},
        },
    ),
    _schema("lookup_symbol", {"name": _TEXT}),
    _schema(
        "read_source",
        {
            "path": _TEXT,
            "version": _TEXT,
            "start": {"type": "integer", "minimum": 0},
            "end": {"type": "integer", "minimum": 0},
        },
    ),
    _schema(
        "expand_source",
        {
            "unit": _TEXT,
            "to": {"type": "string", "enum": ["file", "class", "symbol"]},
        },
    ),
    _schema("source_relationships", {"path": _TEXT, "version": _TEXT}),
)


def context_tool_definitions() -> tuple[ModelToolDefinition, ...]:
    """Use the existing Tool disclosure composition for this fixed Tool surface."""
    return tuple(normalize_tool_descriptor(d) for d in _DEFINITIONS)


class ContextTools:
    """Concrete task-scoped Tool implementation, dispatched through ToolRunner."""

    name = "qwen_repository_context"
    description = "Read-only RI/Context acquisition within the admitted task corpus."

    def __init__(self, root: Path, task: CodingTask) -> None:
        """Observe only explicitly admitted sources; discovery discloses no extras."""
        self.root = resolve_path(root).value
        self.task = task
        self.repository = Repository.new()
        self.addresses = tuple(
            RepositoryResourceAddress(p)
            for p in (task.source, *task.tests, *task.read_paths)
        )
        # Existing metadata discovery, not content acquisition. Only the selected
        # <=32 resources enter the existing source index. Failure is fail-closed.
        self.discovery = discover_repository_resource_addresses(
            repository=self.repository,
            root=resolve_path(self.root),
            maximum_resource_count=32,
            maximum_traversal_entry_count=512,
            requested_addresses=self.addresses,
        )
        self.snapshot = self._observe()
        self._index()

    @property
    def definitions(self) -> tuple[ModelToolDefinition, ...]:
        """Disclose the existing ToolDescriptor projection, never executable writes."""
        return context_tool_definitions()

    def _observe(self) -> RepositorySnapshot:
        for address in self.addresses:
            candidate = self.root / address.value
            for path in (candidate, *candidate.parents):
                if path == self.root:
                    break
                if path.is_symlink() or path.is_junction():
                    raise ValueError("Context path aliases are not admitted")
        return observe_repository_resources(
            repository=self.repository,
            root=resolve_path(self.root),
            addresses=self.addresses,
            maximum_resource_bytes=131072,
        )

    def _index(self) -> None:
        corpus = realize_repository_text_corpus(
            definition=define_repository_text_corpus(
                discovery=self.discovery,
                selected_addresses=self.addresses,
            ),
            snapshot=self.snapshot,
        )
        self.index = build_source_search_index(
            self.snapshot,
            corpus=corpus,
            window_lines=40,
            overlap_lines=10,
        )

    def check_current(self) -> None:
        """Refuse stale source before every invocation and Tool dispatch."""
        if self._observe() != self.snapshot:
            raise ValueError("SOURCE_DRIFT: admitted Context changed")

    def accept_source(self, updated: str) -> None:
        """Refresh only the exact host-admitted edit; unrelated drift still refuses."""
        current = self._observe()
        for resource in current.resources:
            previous = self.snapshot.resource_at(resource.address)
            expected = (
                updated
                if resource.address.value == self.task.source
                else previous.content
            )
            if resource.content != expected:
                raise ValueError("SOURCE_DRIFT after admitted edit")
        self.snapshot = current
        self._index()

    def validate(self, arguments: tuple[str, dict[str, Any]]) -> None:
        """Validate keys/types/enums; schema disclosure grants no authority."""
        name, values = arguments
        descriptor = next((d for d in _DEFINITIONS if d.name == name), None)
        if descriptor is None or not isinstance(values, dict):
            raise ValueError("Unknown or malformed Context Tool")
        properties = json.loads(descriptor.input_schema_json)["properties"]
        if set(values) != set(properties):
            raise ValueError("Context Tool requires exact argument keys")
        for key, spec in properties.items():
            value = values[key]
            if spec["type"] == "string":
                if not isinstance(value, str) or not value or len(value) > 512:
                    raise ValueError("Context Tool requires bounded nonempty text")
            elif type(value) is not int or value < 0:
                raise ValueError("Source offsets must be nonnegative integers")
            if "enum" in spec and value not in spec["enum"]:
                raise ValueError("Unsupported Context Tool selection")
        self.check_current()

    async def dispatch(self, call: ModelToolCall) -> dict[str, Any]:
        """Materialize native arguments and execute exactly once via ToolRunner."""
        values = json.loads(call.arguments_json)
        result = await ToolRunner().execute(self, (call.name, values))
        result = {
            "repository": str(self.repository.id),
            "snapshot": str(self.snapshot.id),
            "revision": self.task.baseline_revision,
            "discovery_semantics": self.discovery.semantics,
            "uncertainty": (
                "bounded admitted-corpus observation; not runtime or sufficiency proof"
            ),
            **result,
        }
        if len(json.dumps(result, ensure_ascii=False).encode()) > 12000:
            raise ValueError("Context response byte budget exceeded")
        return result

    def _metadata(self, unit: RepositorySourceUnit) -> dict[str, Any]:
        return {
            "path": unit.resource.address.value,
            "version": str(unit.resource.content_identity),
            "repository": str(unit.repository_id),
            "revision": self.task.baseline_revision,
            "snapshot": str(unit.snapshot_id),
            "unit": str(unit.id),
            "kind": unit.kind,
            "qualified_name": unit.qualified_name,
            "span": [unit.start, unit.end],
            "lines": [unit.start_line, unit.end_line],
            "semantic_declaration": unit.declaration.identity
            if unit.declaration
            else None,
        }

    async def execute(self, arguments: tuple[str, dict[str, Any]]) -> dict[str, Any]:
        """Project existing search, source units, expansion and relationship facts."""
        name, values = arguments
        if name == "search_source":
            result = search_repository_source(
                self.index,
                query=values["query"],
                mode=cast("SourceSearchMode", values["mode"]),
                maximum_results=9,
            )
            rows = [dict(self._metadata(h.unit), rank=h.rank) for h in result.hits]
            return {
                "matches": rows[:8],
                "truncated": len(rows) > 8,
                "scope": "host-admitted corpus only; rank is not sufficiency",
            }
        if name == "lookup_symbol":
            rows = [
                self._metadata(u)
                for u in self.index.views[1].units
                if u.kind == "symbol" and u.qualified_name == values["name"]
            ]
            return {
                "matches": rows[:8],
                "truncated": len(rows) > 8,
                "scope": "exact qualified source-view name; not runtime binding",
            }
        if name == "expand_source":
            units = {str(u.id): u for view in self.index.views for u in view.units}
            if values["unit"] not in units:
                raise ValueError("Unknown or stale source unit")
            selected = units[values["unit"]]
            if values["to"] == "symbol":
                if selected.parent_symbol_id is None:
                    raise ValueError("Source unit has no parent symbol")
                unit = units[str(selected.parent_symbol_id)]
            else:
                unit = self.index.expand(selected, to=values["to"])
            return {**self._metadata(unit), "truncated": False}
        # ResourceAddress performs canonical-path admission before lookup.
        address = RepositoryResourceAddress(values["path"])
        resource = self.snapshot.resource_at(address)
        if values["version"] != str(resource.content_identity):
            raise ValueError("SOURCE_VERSION_MISMATCH")
        if name == "source_relationships":
            return {
                "path": str(address),
                "version": str(resource.content_identity),
                **self._relationships(address),
            }
        return self._read(values)

    def _read(self, values: dict[str, Any]) -> dict[str, Any]:
        unit = next(
            u
            for u in self.index.views[0].units
            if u.resource.address.value == values["path"]
        )
        start, end = values["start"], values["end"]
        if not 0 <= start < end <= len(unit.text):
            raise ValueError("Read range must be a nonempty exact source span")
        # Existing Context materialization authenticates the unit and snapshot.
        materialize_disclosure_plan(
            plan=plan_disclosures(
                purpose=self.task.objective,
                snapshot=self.snapshot,
                disclosures=(SourceSearchDisclosureOption(self.task.objective, unit),),
            ),
            snapshot=self.snapshot,
        )
        text = unit.text[start:end].encode()[:4096].decode(errors="ignore")
        return {
            "path": str(unit.resource.address),
            "version": str(unit.resource.content_identity),
            "parent": self._metadata(unit),
            "representation": "exact-character-range",
            "text": text,
            "requested_span": [start, end],
            "span": [start, start + len(text)],
            "truncated": start + len(text) < end,
            "bytes": len(text.encode()),
            "uncertainty": "exact retained source; no runtime interpretation",
        }

    def _relationships(self, address: RepositoryResourceAddress) -> dict[str, Any]:
        interpretations = tuple(
            i
            for root in ("src", ".")
            for i in interpret_python_module_resources(
                self.snapshot,
                module_root=PythonModuleRoot(root),
                resource_addresses=tuple(
                    a
                    for a in self.addresses
                    if a.value.startswith("src/") == (root == "src")
                ),
            ).interpretations
        )
        try:
            analysis = derive_python_declaration_references(
                self.snapshot,
                resource_address=address,
                module_universe=define_python_module_interpretation_universe(
                    repository_id=self.repository.id,
                    interpretations=interpretations,
                ),
                source_interpretations=tuple(
                    i for i in interpretations if i.resource.address == address
                ),
            )
        except SyntaxError:
            return {
                "status": "UNPARSEABLE_PYTHON",
                "references": [],
                "truncated": False,
            }
        rows = [
            {
                "identity": r.identity,
                "from": asdict(r.occurrence.source_range),
                "target_path": str(r.target_resource.address),
                "target_version": str(r.target_resource.content_identity),
                "target_declaration": r.target_declaration.identity,
                "target_span": asdict(r.target_declaration.support.source_range),
                "direct_call": r.direct_call,
                "route": r.route.value,
            }
            for r in analysis.references
        ]
        return {
            "path": str(address),
            "snapshot": str(self.snapshot.id),
            "derivation": analysis.derivation.identity,
            "references": rows[:8],
            "truncated": len(rows) > 8,
            "assessed": analysis.coverage.assessed_count,
            "resolved": analysis.coverage.reference_count,
            "uncertainty": (
                "bounded static outgoing relationships; unresolved is not absence"
            ),
        }
