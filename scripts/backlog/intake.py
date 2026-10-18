# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812, PLR2004 -- bounded administrative contracts
"""Pending proposals and host-reviewed publication into the existing backlog.

This is repository tooling, not a framework work lifecycle or authority service.
The host supplies authorization separately from untrusted proposal/review data.
"""

from __future__ import annotations

import hashlib
import json
import re
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from devtools.core.identity import Identity
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.resources.filesystem import FileFormat, TextFile, read, write
from devtools.resources.filesystem.errors import FilesystemError

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from pathlib import Path

DOMAINS = (
    "core",
    "resources",
    "models",
    "agents",
    "context",
    "tools",
    "execution",
    "orchestration",
    "governance",
    "observability",
    "persistence",
    "evaluation",
    "documentation",
    "experiments",
)
FIELDS = {
    "kind",
    "title",
    "summary",
    "discovery",
    "parent",
    "resources",
    "evidence",
    "benefit",
    "uncertainty",
    "dependencies",
}


@dataclass(frozen=True)
class ProposalId:
    """Host-owned proposal identity, distinct from a canonical B-number."""

    value: Identity

    @classmethod
    def parse(cls, text: str) -> ProposalId:
        """Validate a storage/lookup identity before constructing any path."""
        return cls(Identity.parse(text))

    def __str__(self) -> str:
        """Render the stable proposal identity."""
        return str(self.value)


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def _text(value: object, *, single_line: bool = False) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 8000:
        raise ValueError("Expected nonempty bounded text")
    if single_line and any(char in value for char in "\r\n|"):
        raise ValueError("Expected one line without table delimiters")
    return value


def _validate(payload: dict[str, Any]) -> None:  # noqa: C901 -- closed input schema
    if set(payload) != FIELDS:
        raise ValueError("Proposal fields differ from backlog-proposal-v1")
    if not isinstance(payload["kind"], str) or payload["kind"] not in {
        "bug",
        "enhancement",
        "refactor",
        "investigation",
    }:
        raise ValueError("Unknown proposal kind")
    for field in ("title", "summary", "benefit", "uncertainty"):
        _text(payload[field], single_line=field == "title")
    if len(payload["title"]) > 160:
        raise ValueError("Proposal title is too long")
    discovery = payload["discovery"]
    if not isinstance(discovery, dict) or set(discovery) != {"kind", "reference"}:
        raise ValueError("Discovery requires kind and original reference")
    if discovery["kind"] not in {"human", "tool", "agent", "research"}:
        raise ValueError("Unknown discovery source")
    _text(discovery["reference"], single_line=True)
    if payload["parent"] is not None:
        _text(payload["parent"], single_line=True)
    for field in ("resources", "evidence", "dependencies"):
        values = payload[field]
        if not isinstance(values, list) or len(values) > 100:
            raise ValueError("Expected bounded reference lists")
        for value in values:
            _text(value, single_line=True)
    if not payload["evidence"]:
        raise ValueError("At least one evidence reference is required")
    if len(json.dumps(payload).encode()) > 65536:
        raise ValueError("Serialized proposal exceeds the 64 KiB intake allowance")


def _read(path: Path) -> str:
    file = read(resolve_path(path), file_format=FileFormat.TEXT, max_bytes=1 << 20)
    if not isinstance(file, TextFile):
        raise TypeError("Expected text from the TEXT codec")
    return file.content


def load_json(path: Path) -> dict[str, Any]:
    """Read bounded JSON through the canonical filesystem substrate."""
    value = json.loads(_read(path))
    if not isinstance(value, dict):
        raise TypeError("Expected a JSON object")
    return value


class Intake:
    """Administer one checkout's docs/backlog with immutable proposal/review files."""

    def __init__(self, root: Path) -> None:
        """Select an explicit repository; no branch or active task is changed."""
        self.root = resolve_path(root).value
        self.backlog = self._path("docs/backlog")
        self.proposals = self._path("docs/backlog/proposals")
        if not (self.backlog / "overview.md").is_file():
            raise ValueError("Canonical backlog overview is required")

    def _path(self, relative: str) -> Path:
        path = resolve_path(relative, base_directory=self.root).value
        if not path.is_relative_to(self.root):
            raise ValueError("Backlog path escapes selected repository")
        return path

    @contextmanager
    def _writer(self) -> Iterator[None]:
        # Same exclusive-directory pattern as the usage ledger. That ledger's
        # domain-specific writer is not a general locking API to import here.
        self.proposals.mkdir(exist_ok=True)
        lease = self._path("docs/backlog/proposals/.writer")
        lease.mkdir()
        try:
            yield
        finally:
            lease.rmdir()

    def _save(self, path: Path, value: object) -> None:
        text = json.dumps(value, indent=2) + "\n"
        if len(text.encode()) > 1 << 20:
            raise ValueError("Intake record exceeds the bounded reader allowance")
        write(
            TextFile(resolve_path(path), text),
            overwrite=False,
        )

    def capture(self, payload: dict[str, Any]) -> str:
        """Capture untrusted discovery only; return its host-assigned identity."""
        _validate(payload)
        identity = str(ProposalId(Identity.new()))
        with self._writer():
            folder = self._path("docs/backlog/proposals/" + identity)
            folder.mkdir()
            self._save(
                folder / "proposal.json",
                {
                    "schema": "backlog-proposal-v1",
                    "id": identity,
                    "created_at": str(Timestamp.now()),
                    "payload": payload,
                    "payload_sha256": _digest(payload),
                },
            )
        return identity

    def get(self, identity: str) -> dict[str, Any]:
        """Validate identity, original payload and ordered review hash chain."""
        identity = str(ProposalId.parse(identity))
        folder = self._path("docs/backlog/proposals/" + identity)
        proposal = load_json(folder / "proposal.json")
        if set(proposal) != {"schema", "id", "created_at", "payload", "payload_sha256"}:
            raise ValueError("Incomplete proposal envelope")
        Timestamp.from_isoformat(proposal["created_at"])
        if proposal["schema"] != "backlog-proposal-v1" or proposal["id"] != identity:
            raise ValueError("Proposal identity/schema mismatch")
        _validate(proposal["payload"])
        if _digest(proposal["payload"]) != proposal["payload_sha256"]:
            raise ValueError("Proposal payload digest mismatch")
        history = []
        previous = None
        for sequence, path in enumerate(sorted(folder.glob("review-*.json")), 1):
            review = load_json(path)
            if set(review) != {
                "schema",
                "proposal",
                "proposal_sha256",
                "previous",
                "at",
                "decision",
                "reviewer",
                "decision_reference",
                "rationale",
                "duplicates",
                "duplicate_disposition",
                "scope",
                "publication",
                "sha256",
            }:
                raise ValueError("Incomplete review envelope")
            Timestamp.from_isoformat(review["at"])
            digest = review.pop("sha256")
            if (
                path.name != f"review-{sequence:04d}.json"
                or review["previous"] != previous
                or review["proposal_sha256"] != _digest(proposal)
                or review["proposal"] != identity
                or review["schema"] != "backlog-review-v1"
                or review["decision"]
                not in {"ADVISORY", "APPROVED", "DEFERRED", "REJECTED"}
                or digest != _digest(review)
            ):
                raise ValueError("Review chain is incomplete or invalid")
            previous = digest
            history.append({**review, "sha256": digest})
        decisions = [v for v in history if v["decision"] != "ADVISORY"]
        state = decisions[-1]["decision"] if decisions else "PENDING_REVIEW"
        return {"proposal": proposal, "history": history, "state": state}

    def queue(self) -> dict[str, Any]:
        """List every proposal; malformed/incomplete records stay visible as errors."""
        entries = []
        errors = []
        for folder in sorted(self.proposals.glob("*")):
            if not folder.is_dir() or folder.name.startswith("."):
                continue
            try:
                record = self.get(folder.name)
                entries.append(
                    {
                        "id": folder.name,
                        "title": record["proposal"]["payload"]["title"],
                        "state": record["state"],
                    }
                )
            except (ValueError, KeyError, TypeError, OSError, FilesystemError) as error:
                errors.append({"path": str(folder), "error": str(error)})
        return {"proposals": entries, "errors": errors}

    def duplicates(self, identity: str) -> list[dict[str, str]]:
        """Surface title-token overlap or shared affected resource; never auto-merge."""
        payload = self.get(identity)["proposal"]["payload"]
        words = set(re.findall(r"[a-z0-9]+", payload["title"].lower()))
        matches = []
        for entry in self.queue()["proposals"]:
            if entry["id"] == identity:
                continue
            other = self.get(entry["id"])["proposal"]["payload"]
            tokens = set(re.findall(r"[a-z0-9]+", other["title"].lower()))
            if len(words & tokens) / max(1, len(words | tokens)) >= 0.5 or set(
                payload["resources"]
            ) & set(other["resources"]):
                matches.append(
                    {
                        "reference": entry["id"],
                        "reason": "title overlap or shared resource",
                    }
                )
        for path in sorted(self.backlog.glob("*/*.md")):
            if path.parent.name not in {"items", "epics"}:
                continue
            text = _read(path)
            title = text.split("\n", 1)[0]
            tokens = set(re.findall(r"[a-z0-9]+", title.lower()))
            if len(words & tokens) / max(1, len(words | tokens)) >= 0.5 or any(
                resource in text for resource in payload["resources"]
            ):
                matches.append(
                    {
                        "reference": path.relative_to(self.root).as_posix(),
                        "reason": "title overlap or shared resource",
                    }
                )
        return matches

    def review(  # noqa: PLR0913 -- explicit closed review fields, separate host check
        self,
        identity: str,
        *,
        decision: str,
        reviewer: str,
        reference: str,
        rationale: str,
        duplicate_disposition: str,
        domain: str | None = None,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> dict[str, Any]:
        """Record advice or an exact host-authorized backlog-only decision.

        The callback belongs to the trusted host, never proposal/model data. Its
        input includes the complete proposal, decision and publication bytes.
        Default-deny applies to all non-advisory decisions.
        """
        if decision not in {"ADVISORY", "APPROVED", "DEFERRED", "REJECTED"}:
            raise ValueError("Unknown review decision")
        identity = str(ProposalId.parse(identity))
        for value in (reviewer, reference, rationale, duplicate_disposition):
            _text(value)
        with self._writer():
            record = self.get(identity)
            if record["state"] in {"APPROVED", "REJECTED"}:
                raise ValueError("Terminal review requires a new related proposal")
            if self.queue()["errors"]:
                raise ValueError("Reconcile malformed intake records before review")
            history = record["history"]
            review = {
                "schema": "backlog-review-v1",
                "proposal": identity,
                "proposal_sha256": _digest(record["proposal"]),
                "previous": history[-1]["sha256"] if history else None,
                "at": str(Timestamp.now()),
                "decision": decision,
                "reviewer": reviewer,
                "decision_reference": reference,
                "rationale": rationale,
                "duplicates": self.duplicates(identity),
                "duplicate_disposition": duplicate_disposition,
                "scope": "canonical-backlog-only; no execution authority",
                "publication": self._publication(
                    record["proposal"], domain, len(history) + 1
                )
                if decision == "APPROVED"
                else None,
            }
            if decision != "ADVISORY" and (
                authorize is None
                or not authorize({**review, "proposed_work": record["proposal"]})
            ):
                raise PermissionError("Host authorization required for review decision")
            result = {**review, "sha256": _digest(review)}
            self._save(
                self._path(
                    f"docs/backlog/proposals/{identity}/"
                    f"review-{len(history) + 1:04d}.json"
                ),
                result,
            )
        return result

    def _publication(
        self, proposal: dict[str, Any], domain: str | None, review_sequence: int
    ) -> dict[str, str]:
        if domain not in DOMAINS:
            raise ValueError("Approval requires a canonical primary domain")
        ids = [
            int(p.name[2:6])
            for p in self.backlog.glob("*/*.md")
            if re.match(r"B-\d{4}-", p.name)
        ]
        for entry in self.queue()["proposals"]:
            for review in self.get(entry["id"])["history"]:
                if review["publication"]:
                    ids.extend([int(review["publication"]["id"][2:])])
        number = max(ids, default=0) + 1
        if number > 9999:
            raise ValueError("Canonical B-number range exhausted")
        identity = f"B-{number:04d}"
        payload = proposal["payload"]
        slug = re.sub(r"[^a-z0-9]+", "-", payload["title"].lower()).strip("-") or "work"
        path = f"items/{identity}-{slug}.md"
        kind = "INVESTIGATION" if payload["kind"] == "investigation" else "STORY"
        text = (
            f"# {identity} — {payload['title']}\n\n- type: {kind}\n"
            "- status: BACKLOG\n- decision_maturity: DISCOVERED\n"
            f"- primary_domain: {domain}\n"
            "- supporting_domains: unknown\n- evidence_basis: REPOSITORY\n"
            "- hard_dependencies: unknown\n- pressure_dependencies: unknown\n"
            "- operational_dependencies: unknown\n"
            "- validation_level: NONE\n- execution_authorization: NONE\n"
            f"- proposal: ../proposals/{proposal['id']}/proposal.json\n"
            f"- intake_review: ../proposals/{proposal['id']}/"
            f"review-{review_sequence:04d}.json\n\n"
        )
        for heading, body in (
            ("Problem / value", payload["summary"]),
            ("Proposed benefit", payload["benefit"]),
            ("Uncertainty / unresolved semantics", payload["uncertainty"]),
            (
                "Discovery / parent",
                str(payload["discovery"]) + "\n" + str(payload["parent"]),
            ),
            ("Evidence", "\n".join(payload["evidence"])),
            ("Affected resources", "\n".join(payload["resources"])),
            ("Possible dependencies", "\n".join(payload["dependencies"]) or "unknown"),
            (
                "Consumers / invariants / risks",
                "unknown; preserve existing behavior and authority boundaries",
            ),
            (
                "Promotion / validation expectations",
                (
                    "Backlog inclusion only. Scope, priority, dependencies "
                    "and acceptance require deliberate review before implementation."
                ),
            ),
        ):
            text += f"## {heading}\n\n{body}\n\n"
        row = f"| [{identity}]({path}) | {payload['title']} | BACKLOG | {domain} |"
        return {"id": identity, "path": path, "text": text, "row": row}

    def promote(
        self,
        identity: str,
        *,
        authorize: Callable[[dict[str, Any]], bool] | None = None,
    ) -> str:
        """Publish only approved exact bytes; safely reconcile partial publication.

        Item then index writes are individually atomic, not one transaction.
        Repetition verifies existing bytes and completes only the missing write.
        Conflicting content is never overwritten. Authority is checked each time.
        """
        identity = str(ProposalId.parse(identity))
        with self._writer():
            record = self.get(identity)
            if record["state"] != "APPROVED":
                raise PermissionError("Only host-approved proposals may be promoted")
            review = record["history"][-1]
            if authorize is None or not authorize(
                {**review, "proposed_work": record["proposal"]}
            ):
                raise PermissionError(
                    "Host authorization required for backlog publication"
                )
            publication = review["publication"]
            path = self._path("docs/backlog/" + publication["path"])
            if path.exists():
                if _read(path) != publication["text"]:
                    raise ValueError(
                        "Conflicting backlog item; manual reconciliation required"
                    )
            else:
                write(
                    TextFile(resolve_path(path), publication["text"]), overwrite=False
                )
            overview = self._path("docs/backlog/overview.md")
            text = _read(overview)
            if publication["row"] not in text.splitlines():
                if f"[{publication['id']}]" in text:
                    raise ValueError(
                        "Conflicting backlog index; manual reconciliation required"
                    )
                lines = text.splitlines(keepends=True)
                anchors = [
                    n
                    for n, line in enumerate(lines)
                    if re.match(r"\| \[B-\d{4}\]", line)
                ]
                if not anchors:
                    raise ValueError("Canonical backlog index table is missing")
                anchor = anchors[-1]
                newline = "\r\n" if lines[anchor].endswith("\r\n") else "\n"
                lines.insert(anchor + 1, publication["row"] + newline)
                write(TextFile(resolve_path(overview), "".join(lines)))
            return str(publication["id"])
