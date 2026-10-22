# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, PLR2004 -- concrete bounded worker composition

"""Read-only Qwen Tools over the existing admitted RI/Context source index.

No independent index, semantic identity, command capability or edit authority is
defined here. One host-selected corpus is retained, drift checked and refreshed
only after a host-admitted edit. Tool results are data, never instructions.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import TYPE_CHECKING, Any, cast

from apps.qwen.api_contracts import inspect_contract
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
    "inspect_source",
    "search_source",
    "lookup_symbol",
    "read_source",
    "expand_source",
    "source_relationships",
    "inspect_api",
    "inspect_new_source",
)


class ContextRequestError(ValueError):
    """A bounded read-request mistake, distinct from authority or source drift."""

    def __init__(self, code: str, detail: str) -> None:
        """Retain the invalid-input diagnostic for correlated native feedback."""
        super().__init__(detail)
        self.code = code


def _schema(name: str, properties: dict[str, Any]) -> ToolDescriptor:
    return ToolDescriptor(
        name,
        {
            "inspect_source": (
                "Read a known authorized file by path and start character offset "
                "(use 0 initially). Host resolves the exact current version. "
                "Returns <=4096 bytes, edit_ref and continuation_start. Prefer "
                "this for known paths; no version hashes or unit IDs needed."
            ),
            "search_source": (
                "Search the admitted corpus; returns versioned source units."
            ),
            "lookup_symbol": (
                "Exact qualified Python source-view name lookup; retains all matches."
            ),
            "read_source": (
                "Read an exact character range. FIRST obtain the exact version "
                "from search_source or lookup_symbol; never guess or use CURRENT. "
                "Bounded, possibly truncated."
            ),
            "expand_source": (
                "Expand a known unit to its parent symbol, class or file; "
                "returns metadata for optional reading. Use the exact unit ID "
                "from search_source/lookup_symbol; a file path is not a unit ID."
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
            "version": {
                **_TEXT,
                "description": (
                    "Exact version from a prior search/lookup result. "
                    "CURRENT is not a valid version."
                ),
            },
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


def context_tool_definitions(
    api_targets: tuple[str, ...] = (),
    new_paths: tuple[str, ...] = (),
    *,
    direct_reads: bool = False,
) -> tuple[ModelToolDefinition, ...]:
    """Use the existing Tool disclosure composition for this fixed Tool surface."""
    descriptors: tuple[ToolDescriptor, ...] = _DEFINITIONS
    if direct_reads:
        descriptors = (
            *(d for d in descriptors if d.name != "read_source"),
            _schema(
                "inspect_source",
                {"path": _TEXT, "start": {"type": "integer", "minimum": 0}},
            ),
        )
    if new_paths and not direct_reads:
        descriptors += (
            ToolDescriptor(
                "inspect_new_source",
                "Verify an explicitly authorized new file is absent; returns the "
                "exact absence version required for creation. No write occurs.",
                json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "enum": list(new_paths)}
                        },
                        "required": ["path"],
                        "additionalProperties": False,
                    }
                ),
            ),
        )
    if api_targets:
        descriptors += (
            ToolDescriptor(
                "inspect_api",
                (
                    "Inspect an actual host-allowlisted installed Python API "
                    "signature/docstring/version. Never executes the API or imports "
                    "a model-selected module. Verify keywords before editing."
                ),
                json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "target": {"type": "string", "enum": list(api_targets)}
                        },
                        "required": ["target"],
                        "additionalProperties": False,
                    }
                ),
            ),
        )
    return tuple(normalize_tool_descriptor(d) for d in descriptors)


class ContextTools:
    """Concrete task-scoped Tool implementation, dispatched through ToolRunner."""

    name = "qwen_repository_context"
    description = "Read-only RI/Context acquisition within the admitted task corpus."

    def __init__(
        self, root: Path, task: CodingTask, *, direct_reads: bool = False
    ) -> None:
        """Observe only explicitly admitted sources; discovery discloses no extras."""
        self.root = resolve_path(root).value
        self.task = task
        self.direct_reads = direct_reads
        self.repository = Repository.new()
        self.addresses = tuple(
            RepositoryResourceAddress(p)
            for p in (*task.existing_sources, *task.tests, *task.read_paths)
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
        self.observations: list[dict[str, Any]] = []
        self.api_observations: dict[str, dict[str, Any]] = {}
        self.absent_observations: dict[str, str] = {}
        self.edit_references: dict[str, dict[str, Any]] = {}

    def reference(self, observation: dict[str, Any]) -> dict[str, Any]:
        """Name an actual source observation locally; never replace its RI identity."""
        if (
            observation.get("path") not in self.task.sources
            or "text" not in observation
        ):
            return observation
        record = {k: v for k, v in observation.items() if k != "edit_ref"}
        for key, saved in self.edit_references.items():
            if saved == record:
                return {**observation, "edit_ref": key}
        key = f"R{len(self.edit_references) + 1}"
        self.edit_references[key] = record
        return {**observation, "edit_ref": key}

    @property
    def definitions(self) -> tuple[ModelToolDefinition, ...]:
        """Disclose the existing ToolDescriptor projection, never executable writes."""
        return context_tool_definitions(
            self.task.api_targets, self.task.new_paths, direct_reads=self.direct_reads
        )

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
        for path in self.task.new_paths:
            if (self.root / path).exists() and RepositoryResourceAddress(
                path
            ) not in self.addresses:
                raise ValueError("SOURCE_DRIFT: unadmitted new source")
        if self._observe() != self.snapshot:
            raise ValueError("SOURCE_DRIFT: admitted Context changed")

    def accept_source(  # noqa: C901 -- exact verified interval refresh, not fuzzy matching
        self,
        updated: str,
        *,
        replaced_span: tuple[int, int] | None = None,
        edit_call_id: str | None = None,
    ) -> None:
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
        old_resource = self.snapshot.resource_at(
            RepositoryResourceAddress(self.task.source)
        )
        new_resource = current.resource_at(RepositoryResourceAddress(self.task.source))
        retained = [o for o in self.observations if o["path"] != self.task.source]
        if replaced_span is not None:
            start, end = replaced_span
            if not 0 <= start <= end <= len(old_resource.content):
                raise ValueError("Invalid admitted replacement span")
            delta = len(updated) - len(old_resource.content)
            for observation in self.observations:
                if observation["path"] != self.task.source:
                    continue
                left, right = observation["span"]
                if old_resource.content[left:right] != observation["text"]:
                    raise ValueError(
                        "Observed source does not match admitted coordinates"
                    )
                for first, last, shift in (
                    (left, min(right, start), 0),
                    (max(left, end), right, delta),
                ):
                    if first >= last:
                        continue
                    text = old_resource.content[first:last]
                    if updated[first + shift : last + shift] != text:
                        raise ValueError("Unchanged source refresh verification failed")
                    retained.append(
                        {
                            "path": self.task.source,
                            "version": str(new_resource.content_identity),
                            "span": [first + shift, last + shift],
                            "text": text,
                            "derived_from": {
                                "observation_call_id": observation.get(
                                    "observation_call_id"
                                ),
                                "version": observation["version"],
                                "span": observation["span"],
                                "admitted_edit_call_id": edit_call_id,
                            },
                        }
                    )
        self.snapshot = current
        self._index()
        self.observations = retained

    def accept_transaction(  # noqa: C901 -- exact interval reconciliation
        self,
        updates: dict[str, str],
        edits: list[dict[str, Any]],
        *,
        call_id: str | None,
    ) -> None:
        """Reconcile one admitted transaction and retain only verified source."""
        created = [
            RepositoryResourceAddress(p)
            for p in updates
            if RepositoryResourceAddress(p) not in self.addresses
        ]
        if created:
            self.addresses += tuple(created)
            self.discovery = discover_repository_resource_addresses(
                repository=self.repository,
                root=resolve_path(self.root),
                maximum_resource_count=32,
                maximum_traversal_entry_count=512,
                requested_addresses=self.addresses,
            )
        current = self._observe()
        for resource in current.resources:
            previous = (
                None
                if resource.address in created
                else self.snapshot.resource_at(resource.address)
            )
            if resource.content != updates.get(
                resource.address.value, previous.content if previous else ""
            ):
                raise ValueError("SOURCE_DRIFT after transaction")
        retained = [o for o in self.observations if o["path"] not in updates]
        for path, updated in updates.items():
            address = RepositoryResourceAddress(path)
            old = None if address in created else self.snapshot.resource_at(address)
            new = current.resource_at(address)
            changes = sorted(
                (e for e in edits if e["path"] == path), key=lambda e: e["start"]
            )
            for observation in self.observations:
                if observation["path"] != path:
                    continue
                left, right = observation["span"]
                if old is None or old.content[left:right] != observation["text"]:
                    raise ValueError("Observed coordinates changed")
                segments = [(left, right)]
                for edit in changes:
                    segments = [
                        (a, b)
                        for first, last in segments
                        for a, b in (
                            (first, min(last, edit["start"])),
                            (max(first, edit["end"]), last),
                        )
                        if a < b
                    ]
                for first, last in segments:
                    shift = sum(
                        e["new_length"] - (e["end"] - e["start"])
                        for e in changes
                        if e["end"] <= first
                    )
                    if old is None:
                        raise ValueError("Cannot refresh an absent observation")
                    text = old.content[first:last]
                    if updated[first + shift : last + shift] != text:
                        raise ValueError(
                            "Unchanged transaction region failed verification"
                        )
                    retained.append(
                        {
                            "path": path,
                            "version": str(new.content_identity),
                            "span": [first + shift, last + shift],
                            "text": text,
                            "derived_from": {
                                "observation_call_id": observation.get(
                                    "observation_call_id"
                                ),
                                "version": observation["version"],
                                "span": observation["span"],
                                "admitted_edit_call_id": call_id,
                            },
                        }
                    )
            shift = 0
            for edit in changes:
                first = edit["start"] + shift
                last = first + edit["new_length"]
                retained.append(
                    {
                        "path": path,
                        "version": str(new.content_identity),
                        "span": [first, last],
                        "text": updated[first:last],
                        "observation_call_id": call_id,
                    }
                )
                shift += edit["new_length"] - (edit["end"] - edit["start"])
        self.snapshot = current
        self._index()
        self.observations = retained

    def validate(self, arguments: tuple[str, dict[str, Any]]) -> None:
        """Validate keys/types/enums; schema disclosure grants no authority."""
        name, values = arguments
        descriptor = next((d for d in self.definitions if d.name == name), None)
        if descriptor is None:
            if name in CONTEXT_TOOL_NAMES:
                raise ContextRequestError(
                    "SOURCE_OPERATION_UNAVAILABLE", "Use a disclosed Context operation"
                )
            raise ValueError("Unknown or malformed Context Tool")
        if not isinstance(values, dict):
            raise ContextRequestError(
                "SOURCE_ARGUMENTS_REFUSED", "Arguments must be a JSON object"
            )
        properties = json.loads(descriptor.input_schema_json)["properties"]
        if set(values) != set(properties):
            raise ContextRequestError(
                "SOURCE_ARGUMENTS_REFUSED",
                "Required argument keys: " + ", ".join(properties),
            )
        for key, spec in properties.items():
            value = values[key]
            if spec["type"] == "string":
                if not isinstance(value, str) or not value or len(value) > 512:
                    raise ContextRequestError(
                        "SOURCE_ARGUMENTS_REFUSED",
                        f"Argument {key} requires nonempty text (<=512 characters)",
                    )
            elif type(value) is not int or value < 0:
                raise ContextRequestError(
                    "SOURCE_ARGUMENTS_REFUSED",
                    f"Argument {key} must be a nonnegative integer character offset",
                )
            if "enum" in spec and value not in spec["enum"]:
                raise ContextRequestError(
                    "SOURCE_ARGUMENTS_REFUSED",
                    f"Argument {key} must be one of {spec['enum']}",
                )
        self.check_current()

    async def dispatch(self, call: ModelToolCall) -> dict[str, Any]:
        """Materialize native arguments and execute exactly once via ToolRunner."""
        values = json.loads(call.arguments_json)
        result = await ToolRunner().execute(self, (call.name, values))
        if "text" in result:
            result["observation_call_id"] = call.provider_call_id
        result = {
            "operation": call.name,
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
        return self.reference(result)

    def refusal(
        self, call: ModelToolCall, error: ContextRequestError
    ) -> dict[str, Any]:
        """Explain a safe mistake without reading source or relaxing admission."""
        self.check_current()
        descriptor = next((d for d in self.definitions if d.name == call.name), None)
        return {
            "status": "REFUSED",
            "error": error.code,
            "operation": call.name,
            "diagnostic": str(error),
            "arguments_schema": json.loads(descriptor.input_schema_json)
            if descriptor
            else None,
            "instruction": (
                "No source was read or changed. This dispatch consumed one action. "
                "Use inspect_source(path, start=0) for a known admitted path; "
                "continue at continuation_start when truncated. "
                if self.direct_reads
                else "No source was read or changed. This consumed one action. "
                "Use read_source with the exact returned version and valid range. "
            )
            + "Search unknown paths/names with search_source. Expand only actual "
            "unit IDs from search/lookup; paths are not unit IDs. A missing parent "
            "can be expanded to file instead. Never guess versions or identities.",
        }

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

    async def execute(self, arguments: tuple[str, dict[str, Any]]) -> dict[str, Any]:  # noqa: C901, PLR0911, PLR0912 -- fixed source/API operations
        """Project existing search, source units, expansion and relationship facts."""
        name, values = arguments
        if name == "inspect_source":
            path = values["path"]
            if path in self.task.new_paths and not (self.root / path).exists():
                return await self.execute(("inspect_new_source", {"path": path}))
            address = RepositoryResourceAddress(path)
            if address not in self.addresses:
                raise ValueError("Unauthorized source read")
            resource = self.snapshot.resource_at(address)
            return self._read(
                {
                    "path": path,
                    "version": str(resource.content_identity),
                    "start": values["start"],
                    "end": len(resource.content),
                }
            )
        if name == "inspect_new_source":
            path = values["path"]
            raw = self.root / path
            if (
                resolve_path(raw).value != raw
                or not raw.parent.is_dir()
                or raw.exists()
                or raw.is_symlink()
            ):
                raise ValueError(
                    "New source must be absent under an existing unaliased parent"
                )
            version = hashlib.sha256(
                (self.task.baseline_revision + ":ABSENT:" + path).encode()
            ).hexdigest()
            self.absent_observations[path] = version
            return {
                "path": path,
                "version": version,
                "status": "ABSENT",
                "text": "",
                "source_length": 0,
                "scope": "Only this exact host-authorized new file may be proposed; "
                "no source exists.",
            }
        if name == "inspect_api":
            observation = inspect_contract(values["target"], self.task.api_targets)
            self.api_observations[observation["observation_id"]] = observation
            return observation
        if name == "search_source":
            result = search_repository_source(
                self.index,
                query=values["query"],
                mode=cast("SourceSearchMode", values["mode"]),
                maximum_results=9,
            )
            rows = [dict(self._metadata(h.unit), rank=h.rank) for h in result.hits]
            return {
                "query": values["query"],
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
                "name": values["name"],
                "matches": rows[:8],
                "truncated": len(rows) > 8,
                "scope": "exact qualified source-view name; not runtime binding",
                "status": "RETURNED" if rows else "NOT_FOUND",
                "instruction": (
                    "Use search_source to discover names; no match is not proof "
                    "of absence outside the admitted corpus."
                ),
            }
        if name == "expand_source":
            units = {str(u.id): u for view in self.index.views for u in view.units}
            if values["unit"] not in units:
                raise ContextRequestError(
                    "SOURCE_UNIT_MISMATCH", "Unknown or stale source unit"
                )
            selected = units[values["unit"]]
            if values["to"] == "symbol":
                if selected.parent_symbol_id is None:
                    raise ContextRequestError(
                        "SOURCE_PARENT_NOT_FOUND", "Source unit has no parent symbol"
                    )
                unit = units[str(selected.parent_symbol_id)]
            else:
                try:
                    unit = self.index.expand(selected, to=values["to"])
                except ValueError as error:
                    if str(error) != "Source unit has no enclosing class.":
                        raise
                    raise ContextRequestError(
                        "SOURCE_PARENT_NOT_FOUND", str(error)
                    ) from error
            return {**self._metadata(unit), "truncated": False}
        # ResourceAddress performs canonical-path admission before lookup.
        address = RepositoryResourceAddress(values["path"])
        resource = self.snapshot.resource_at(address)
        if values["version"] != str(resource.content_identity):
            raise ContextRequestError(
                "SOURCE_VERSION_MISMATCH", "SOURCE_VERSION_MISMATCH"
            )
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
        if not (
            0 <= start < end <= len(unit.text) or start == end == len(unit.text) == 0
        ):
            return {
                "status": "REFUSED",
                "error": "SOURCE_RANGE_OUT_OF_BOUNDS",
                "path": values["path"],
                "version": values["version"],
                "source_length": len(unit.text),
                "valid_range": [0, len(unit.text)],
                "coordinate_convention": "half-open Unicode character offsets",
                "requested_span": [start, end],
                "instruction": (
                    "Use start < end within valid_range; read <=4096 bytes at a time."
                ),
            }
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
        result = {
            "path": str(unit.resource.address),
            "version": str(unit.resource.content_identity),
            "source_length": len(unit.text),
            "valid_range": [0, len(unit.text)],
            "coordinate_convention": "half-open Unicode character offsets",
            "continuation_start": start + len(text),
            "parent": self._metadata(unit),
            "representation": "exact-character-range",
            "text": text,
            "requested_span": [start, end],
            "span": [start, start + len(text)],
            "truncated": start + len(text) < end,
            "bytes": len(text.encode()),
            "uncertainty": "exact retained source; no runtime interpretation",
        }
        self.observations.append(result)
        return result

    def observed(self, old_text: str, *, path: str | None = None) -> bool:
        """Require exact logical text in a union of current observed source spans."""
        return self.observed_matches(old_text, path=path) > 0

    def observed_matches(self, old_text: str, *, path: str | None = None) -> int:
        """Count overlapping matches only within current disclosed source unions."""
        version = str(
            self.snapshot.resource_at(
                RepositoryResourceAddress(path or self.task.source)
            ).content_identity
        )
        regions = sorted(
            (o["span"][0], o["text"])
            for o in self.observations
            if o["path"] == (path or self.task.source) and o["version"] == version
        )
        merged: list[tuple[int, str]] = []
        for start, text in regions:
            if merged and start <= merged[-1][0] + len(merged[-1][1]):
                previous, content = merged[-1]
                merged[-1] = (
                    previous,
                    content + text[max(0, previous + len(content) - start) :],
                )
            else:
                merged.append((start, text))
        needle = old_text.replace("\r\n", "\n")
        if not needle:
            return 0
        matches = 0
        for _, text in merged:
            logical = text.replace("\r\n", "\n")
            offset = 0
            while (found := logical.find(needle, offset)) >= 0:
                matches += 1
                offset = found + 1
        return matches

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
