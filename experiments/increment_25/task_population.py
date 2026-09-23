# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, PLR0911, PLR2004, S311
"""Freeze historical maintenance tasks without running retrieval mechanisms.

This module consumes only Git commit and change metadata.  It deliberately does
not import lexical retrieval or Python Repository Intelligence packages.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import subprocess
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from pathlib import Path

CUTOFF_COMMIT = "f624234d84b81217c9db13ae6875437dcd22dc39"
FREEZE_CHECKPOINT = "dc0ba53182d5d90a9db1b0783f73446c412d5850"
RANDOM_SEED = 25025
DEVELOPMENT_SIZE = 8
CONFIRMATION_SIZE = 16
RELEVANT_PREFIXES = ("src/devtools/", "tests/")
SCHEMA = "devtools-increment-25-task-population-freeze-v1"

_MECHANISM_PATTERN = re.compile(
    r"\b(?:retrieval|ranking|lexical|bm25|import[ -]?(?:relation|resolution)|"
    r"structural(?:[ -](?:expansion|retrieval))?|purpose[ -]relative)\b",
    re.IGNORECASE,
)
_EXTERNAL_STATE_PATTERN = re.compile(
    r"\b(?:qwen|llama(?:\.cpp)?|vllm|hugging[ -]?face|model[ -]?serving|cuda|gguf)\b",
    re.IGNORECASE,
)
_REORGANIZATION_PATTERN = re.compile(
    r"\b(?:reorgani[sz]\w*|rename|move|architecture backlog|establish twelve-domain)\b",
    re.IGNORECASE,
)
_ARCHITECTURE_ONLY_PATTERN = re.compile(
    r"\b(?:reconcile|document|establish)\b.*\b(?:architecture|research|taxonomy|backlog|evaluation)\b",
    re.IGNORECASE,
)
_OPAQUE_SUBJECT_PATTERN = re.compile(
    r"^(?:wip|misc(?:ellaneous)?|updates?|changes?|fix|update|implemented?)\s*$",
    re.IGNORECASE,
)
_BOOKKEEPING_ID = re.compile(r"\bB-\d{4}\b", re.IGNORECASE)
_SUBJECTIVE_EXCLUSIONS = {
    "243fac616131e0f8d31f2f515920dd7d6f79ef86": "subject 'implemented runtime' does not state a reconstructible maintenance purpose",
    "2f66a64e8fa9c534ec0a0700f95c6dfa6aaa6498": "subject 'Filesystems' is only a domain label",
    "37972492fcec1918453173903d06918257eb6e4a": "subject 'ReadRepositoryFileTool' is an identifier without a stated task",
    "4e279045455aa83df78f721cd073900468affb29": "subject 'message history' is only a domain label",
    "891fc354c8e17854d8a1540c4e465743100c26bb": "subject 'paths' is only a domain label",
    "8c69e4e5b2a9724ee32be68cc33897682afb5a28": "subject 'implemented session' does not state a reconstructible maintenance purpose",
    "944b8c0533d4fbf786044adf766a9e6231370807": "subject 'agents and codex wrapper' is only a domain label",
    "9c42bd9b3da3f468bb7bbf0b8235596187dc64c3": "subject 'added persistence' does not state a reconstructible maintenance purpose",
    "a7342e0b7c7792c9eca783a15a7dd2c452c8b5fa": "subject 'Filesystems' is only a domain label",
    "c0fabcb195e20d6775d1b16ef2116bee287c1f": "subject 'added evidence' does not state a reconstructible maintenance purpose",
}


@dataclass(frozen=True, slots=True)
class CommitMetadata:
    """Git-only historical record, independent of any retrieval result."""

    sha: str
    parent_sha: str | None
    parents: tuple[str, ...]
    subject: str
    body: str
    changed_paths: tuple[str, ...]
    path_categories: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PopulationRecord:
    """One enumerated historical commit and its auditable disposition."""

    commit: CommitMetadata
    disposition: str
    exclusion_reason: str | None
    exclusion_kind: str | None
    task_evidence: str


@dataclass(frozen=True, slots=True)
class TaskCard:
    """A task-first InformationNeed configuration with evaluator-only path data."""

    case_id: str
    source_commit_sha: str
    parent_snapshot_sha: str
    original_subject: str
    original_body: str
    information_need_purpose: str
    lexical_query: str
    maintenance_category: str
    repository_domain: str
    corpus_source_roots: tuple[str, ...]
    evaluator_only_changed_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FrozenSplit:
    """One deterministic development/confirmation/reserve assignment."""

    development_case_ids: tuple[str, ...]
    confirmation_case_ids: tuple[str, ...]
    reserve_case_ids: tuple[str, ...]


def path_categories(paths: Iterable[str]) -> tuple[str, ...]:
    """Classify change paths mechanically without interpreting their contents."""
    categories: set[str] = set()
    for path in paths:
        if path.startswith("src/devtools/"):
            categories.add("source")
        elif path.startswith("tests/"):
            categories.add("test")
        elif path.startswith("docs/"):
            categories.add("documentation")
        elif path.startswith("experiments/"):
            categories.add("experiment")
        elif path.startswith("scripts/"):
            categories.add("script")
        else:
            categories.add("other")
    return tuple(sorted(categories))


def classify_commit(commit: CommitMetadata) -> PopulationRecord:
    """Apply the frozen, outcome-blind population rules to one commit."""
    evidence = _task_evidence(commit)
    if len(commit.parents) != 1:
        return _excluded(commit, "merge-commit", "mechanical", evidence)
    if commit.parent_sha is None:
        return _excluded(commit, "missing-parent", "mechanical", evidence)
    if not any(path.startswith(RELEVANT_PREFIXES) for path in commit.changed_paths):
        reason = (
            "documentation-only"
            if commit.path_categories == ("documentation",)
            else "no-source-or-test-touch"
        )
        return _excluded(commit, reason, "mechanical", evidence)
    if _MECHANISM_PATTERN.search(evidence):
        return _excluded(
            commit, "prior-retrieval-or-structural-experiment", "mechanical", evidence
        )
    if any(
        path.startswith(
            ("src/devtools/context/retrieval/", "src/devtools/context/python/imports/")
        )
        for path in commit.changed_paths
    ):
        return _excluded(
            commit, "prior-retrieval-or-structural-experiment", "mechanical", evidence
        )
    if _EXTERNAL_STATE_PATTERN.search(evidence):
        return _excluded(
            commit, "requires-external-model-or-service-state", "mechanical", evidence
        )
    if _REORGANIZATION_PATTERN.search(evidence):
        return _excluded(
            commit, "repository-reorganization-only", "mechanical", evidence
        )
    if _ARCHITECTURE_ONLY_PATTERN.search(evidence):
        return _excluded(
            commit, "architecture-reconciliation-only", "mechanical", evidence
        )
    if _OPAQUE_SUBJECT_PATTERN.fullmatch(commit.subject.strip()):
        return _excluded(commit, "insufficient-task-evidence", "judgment", evidence)
    if subjective_reason := _SUBJECTIVE_EXCLUSIONS.get(commit.sha):
        return _excluded(commit, subjective_reason, "judgment", evidence)
    return PopulationRecord(commit, "eligible", None, None, evidence)


def enumerate_population(
    commits: Iterable[CommitMetadata],
) -> tuple[PopulationRecord, ...]:
    """Classify a cutoff-validated commit population in SHA order."""
    unique = {commit.sha: commit for commit in commits}
    return tuple(classify_commit(unique[sha]) for sha in sorted(unique))


def task_card(record: PopulationRecord) -> TaskCard:
    """Make an eligible task card exclusively from preserved task-message evidence."""
    if record.disposition != "eligible":
        msg = "Only eligible population records may become task cards."
        raise ValueError(msg)
    commit = record.commit
    wording = _normalized_task_wording(commit.subject, commit.body)
    return TaskCard(
        case_id=f"i25-{commit.sha[:12]}",
        source_commit_sha=commit.sha,
        parent_snapshot_sha=commit.parent_sha or "",
        original_subject=commit.subject,
        original_body=commit.body,
        information_need_purpose=f"Address the historical maintenance task: {wording}",
        lexical_query=wording,
        maintenance_category=_maintenance_category(commit.subject, commit.body),
        repository_domain=_repository_domain(commit.changed_paths),
        corpus_source_roots=("src", "tests"),
        evaluator_only_changed_paths=commit.changed_paths,
    )


def sample_cards(cards: Iterable[TaskCard], *, seed: int = RANDOM_SEED) -> FrozenSplit:
    """Use one fixed seeded permutation; never downsize a population below 24."""
    ordered = sorted(cards, key=lambda card: card.case_id)
    if len(ordered) < DEVELOPMENT_SIZE + CONFIRMATION_SIZE:
        msg = "Fewer than 24 eligible tasks; review is required before sampling."
        raise ValueError(msg)
    selected = list(ordered)
    random.Random(seed).shuffle(selected)
    development = tuple(card.case_id for card in selected[:DEVELOPMENT_SIZE])
    confirmation = tuple(
        card.case_id
        for card in selected[DEVELOPMENT_SIZE : DEVELOPMENT_SIZE + CONFIRMATION_SIZE]
    )
    reserve = tuple(
        card.case_id for card in selected[DEVELOPMENT_SIZE + CONFIRMATION_SIZE :]
    )
    return FrozenSplit(development, confirmation, reserve)


def build_freeze(
    *, commits: Iterable[CommitMetadata], checkpoint: str
) -> dict[str, object]:
    """Build the complete sealed freeze payload; it has no candidate-result fields."""
    if checkpoint != FREEZE_CHECKPOINT:
        msg = "The task population must be frozen from the declared Increment-25 checkpoint."
        raise ValueError(msg)
    population = enumerate_population(commits)
    cards = tuple(
        task_card(record) for record in population if record.disposition == "eligible"
    )
    split = sample_cards(cards)
    payload: dict[str, object] = {
        "protocol": {
            "identity": "increment-25-lexically-seeded-structural-expansion-task-freeze-v1",
            "statement": "This freeze supports lexically seeded structural expansion, not structural retrieval independent of lexical retrieval.",
            "cutoff_exclusive": CUTOFF_COMMIT,
            "checkpoint": checkpoint,
            "sampling_seed": RANDOM_SEED,
            "development_size": DEVELOPMENT_SIZE,
            "confirmation_size": CONFIRMATION_SIZE,
            "candidate_outcomes_generated": False,
            "usefulness_judgments_made": False,
            "confirmation_status": "sealed",
            "population_inclusion": "commits preceding the exclusive imported-member implementation cutoff, with a locally available single parent and at least one src/devtools/ or tests/ path",
            "exclusion_rules": {
                "mechanical": [
                    "merge commits and missing parents",
                    "documentation-only or no source/test touch",
                    "prior retrieval/ranking/lexical/import-relation/structural/purpose-relative work",
                    "external model/service state",
                    "repository reorganization only",
                    "architecture reconciliation only",
                ],
                "judgment": "The listed commit-message-only decisions have insufficient task evidence; each preserves exact message evidence and rationale.",
            },
        },
        "category_definitions": _category_definitions(),
        "population": [asdict(record) for record in population],
        "task_cards": [asdict(card) for card in cards],
        "split": asdict(split),
    }
    return {"schema": SCHEMA, "content_identity": _digest(payload), "payload": payload}


def validate_freeze(envelope: dict[str, object]) -> bool:
    """Validate identity and the intentional absence of prohibited result data."""
    if envelope.get("schema") != SCHEMA or not isinstance(
        envelope.get("payload"), dict
    ):
        return False
    payload = envelope["payload"]
    if envelope.get("content_identity") != _digest(payload):
        return False
    prohibited = {
        "bm25",
        "lexical_results",
        "structural_results",
        "candidate_sets",
        "usefulness_labels",
        "metrics",
    }
    return not (_all_mapping_keys(payload) & prohibited)


def collect_git_population(repository_root: Path) -> tuple[CommitMetadata, ...]:
    """Read all non-merge and merge historical records before the exclusive cutoff."""
    shas = _git_lines(repository_root, "rev-list", "--topo-order", f"{CUTOFF_COMMIT}^")
    return tuple(_git_commit(repository_root, sha) for sha in shas)


def _git_commit(repository_root: Path, sha: str) -> CommitMetadata:
    raw = _git(repository_root, "show", "-s", "--format=%H%x1f%P%x1f%s%x1f%b", sha)
    parts = raw.split("\x1f", maxsplit=3)
    if len(parts) != 4:
        msg = f"Could not parse Git metadata for {sha}."
        raise RuntimeError(msg)
    _, parents_raw, subject, body = parts
    parents = tuple(parents_raw.split())
    paths = _changed_paths(repository_root, sha)
    return CommitMetadata(
        sha=sha,
        parent_sha=parents[0] if len(parents) == 1 else None,
        parents=parents,
        subject=subject.strip(),
        body=body.strip(),
        changed_paths=paths,
        path_categories=path_categories(paths),
    )


def _changed_paths(repository_root: Path, sha: str) -> tuple[str, ...]:
    rows = _git_lines(
        repository_root, "diff-tree", "--no-commit-id", "--name-status", "-r", sha
    )
    paths: list[str] = []
    for row in rows:
        fields = row.split("\t")
        if len(fields) >= 2:
            paths.extend(fields[1:])
    return tuple(sorted(set(paths)))


def _git_lines(repository_root: Path, *arguments: str) -> tuple[str, ...]:
    return tuple(
        line for line in _git(repository_root, *arguments).splitlines() if line
    )


def _git(repository_root: Path, *arguments: str) -> str:
    completed = subprocess.run(  # noqa: S603
        ("git", *arguments),  # noqa: S607
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _excluded(
    commit: CommitMetadata, reason: str, kind: str, evidence: str
) -> PopulationRecord:
    return PopulationRecord(commit, "excluded", reason, kind, evidence)


def _task_evidence(commit: CommitMetadata) -> str:
    return "\n\n".join(value for value in (commit.subject, commit.body) if value)


def _normalized_task_wording(subject: str, body: str) -> str:
    source = subject if subject.strip() else body
    normalized = _BOOKKEEPING_ID.sub("", source)
    normalized = re.sub(
        r"^(?:implemented?|add|fix|update|support|enable)\s*[-:]?\s*",
        "",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(r"\s+", " ", normalized).strip(" -:.")
    return normalized or subject.strip()


def _maintenance_category(subject: str, body: str) -> str:
    evidence = "\n\n".join(value for value in (subject, body) if value)
    lowered = evidence.lower()
    if any(token in lowered for token in ("fix", "bug", "failure", "error")):
        return "defect-fix"
    if any(
        token in lowered for token in ("test", "acceptance", "evaluate", "validation")
    ):
        return "test-verification"
    if any(token in lowered for token in ("tool", "script", "ci", "workflow")):
        return "tooling-infrastructure"
    if any(token in lowered for token in ("refactor", "maintain", "cleanup")):
        return "refactor-maintenance"
    return "feature-capability"


def _repository_domain(paths: Sequence[str]) -> str:
    domains: set[str] = set()
    for path in paths:
        if path.startswith("src/devtools/"):
            pieces = path.split("/")
            if len(pieces) > 2:
                domains.add(pieces[2])
        elif path.startswith("tests/"):
            pieces = path.split("/")
            if len(pieces) > 1:
                domains.add(pieces[1])
    return next(iter(domains)) if len(domains) == 1 else "cross-domain"


def _category_definitions() -> dict[str, str]:
    return {
        "defect-fix": "Task evidence contains fix, bug, failure, or error.",
        "feature-capability": "Default for intelligible maintenance tasks not matched by another category.",
        "refactor-maintenance": "Task evidence contains refactor, maintain, or cleanup.",
        "test-verification": "Task evidence contains test, acceptance, evaluate, or validation.",
        "tooling-infrastructure": "Task evidence contains tool, script, CI, or workflow.",
    }


def _all_mapping_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = {str(key) for key in value}
        for item in value.values():
            keys.update(_all_mapping_keys(item))
        return keys
    if isinstance(value, list):
        return (
            set().union(*(_all_mapping_keys(item) for item in value))
            if value
            else set()
        )
    return set()


def _digest(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
