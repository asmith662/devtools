# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, PLR2004 -- fixed experiment task definitions
"""Host-selected configuration for the existing bounded coding loop.

These are two concrete development obligations, not a task/plugin registry or
framework Task abstraction. No model-originated commands/config are accepted.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

from apps.qwen.development_task import ACCEPTANCE, SOURCE, TESTS
from apps.qwen.source_segment_acceptance import ACCEPTANCE as SEGMENT_ACCEPTANCE
from devtools.context import RepositoryResourceAddress

if TYPE_CHECKING:
    from devtools.context.retrieval.source import SourceSearchMode


@dataclass(frozen=True, slots=True)
class CodingTask:
    """One host-owned one-file objective, admitted Context, checks and bounds."""

    name: str
    objective: str
    source: str
    tests: tuple[str, ...]
    baseline_revision: str
    baseline_hashes: tuple[tuple[str, str], ...]
    context: tuple[tuple[str, str, SourceSearchMode, str], ...]
    oracle: str
    maximum_calls: int = 3
    output_tokens: int = 4096
    wall_seconds: int = 900
    call_seconds: int = 300
    context_mode: str = "prepared"
    read_paths: tuple[str, ...] = ()
    quality_checks: bool = False

    def __post_init__(self) -> None:  # noqa: C901, PLR0912 -- narrow configuration admission
        """Validate scope and prevent configured bounds exceeding host limits."""
        if type(self.quality_checks) is not bool:
            raise ValueError("quality_checks must be a host-selected boolean")
        paths = (self.source, *self.tests, *self.read_paths)
        if self.context_mode not in {"prepared", "on-demand"}:
            raise ValueError("Unknown Context acquisition mode")
        if not isinstance(self.read_paths, tuple) or len(paths) > 32:
            raise ValueError("Task requires a bounded tuple of read paths")
        if (
            not self.name.strip()
            or not self.objective.strip()
            or len(self.baseline_revision) != 40
            or any(c not in "0123456789abcdef" for c in self.baseline_revision)
        ):
            raise ValueError("Task requires an objective and exact Git revision")
        for _, digest in self.baseline_hashes:
            if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                raise ValueError("Task requires exact SHA-256 input identities")
        for path in paths:
            address = RepositoryResourceAddress(path)
            if not path.endswith(".py") or address.parts[0] not in {"src", "tests"}:
                raise ValueError("Task requires repository Python source/test paths")
        if (
            not self.source.startswith("src/devtools/")
            or not self.tests
            or any(not p.startswith("tests/") for p in self.tests)
            or len(set(paths)) != len(paths)
            or len(self.baseline_hashes) != len(paths)
            or len(self.context) != len(paths)
            or set(dict(self.baseline_hashes)) != set(paths)
            or {p for p, _, _, _ in self.context} != set(paths)
        ):
            raise ValueError("Task source, tests, hashes and Context must agree")
        for _, query, mode, expansion in self.context:
            if mode not in {"file", "symbol", "window", "mixed"} or expansion not in {
                "file",
                "class",
                "none",
            }:
                raise ValueError("Unsupported task source-search choice")
            if not query.strip():
                raise ValueError("Task requires explicit nonempty retrieval queries")
        for value, bound in (
            (self.maximum_calls, 10 if self.context_mode == "on-demand" else 3),
            (self.output_tokens, 4096),
            (self.wall_seconds, 900),
            (self.call_seconds, 300),
        ):
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or not 1 <= value <= bound
            ):
                raise ValueError("Task exceeds the bounded local worker limits")

    @property
    def oracle_sha256(self) -> str:
        """Identify exact host-only acceptance code."""
        return hashlib.sha256(self.oracle.encode()).hexdigest()

    @property
    def definition_sha256(self) -> str:
        """Bind the complete host definition, including all checks and bounds."""
        value = asdict(self)
        if not self.quality_checks:
            del value["quality_checks"]
        # Existing assignment-v1 receipts predate these optional fields. Their
        # exact definition hashes remain valid only for legacy prepared mode.
        if self.context_mode == "prepared" and not self.read_paths:
            del value["context_mode"], value["read_paths"]
        return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

    @property
    def prompt(self) -> str:
        """Combine the objective with the same host-controlled proposal boundary."""
        if self.context_mode == "on-demand":
            return (
                self.objective
                + (
                    " Host acceptance includes Ruff and formatting; "
                    "repair their diagnostics. "
                    if self.quality_checks
                    else ""
                )
                + " Only edit "
                + self.source
                + ". "
                "Investigate with native read-only Context Tools as needed. "
                "Propose one contiguous replacement using native propose_edit. "
                "The host applies and tests it; you have no write, shell or Git "
                "authority. Do not claim tests ran. Read results identify exact "
                "source version hashes. After failure revise current source using the "
                "correlated Tool result. At most 3 edit proposals, 8 Context "
                f"actions and {self.maximum_calls} total model calls are permitted."
            )
        return (
            self.objective + " Only edit " + self.source + ". "
            "Use exactly one native propose_edit call for a contiguous replacement. "
            "The host applies and tests it; you have no write, shell or Git authority. "
            "Do not claim tests ran. Context below is CURRENT source state. "
            "After failure, revise current source using correlated host feedback. "
            f"At most {self.maximum_calls} proposals are permitted."
        )


MARKDOWN = CodingTask(
    "markdown-fences",
    "Repair Markdown fence closing: non-whitespace text after matching fence "
    "markers must not expose fenced headings. Preserve backtick/tilde, longer "
    "closers, trailing spaces/tabs, matching-marker/minimum-length behavior and APIs.",
    SOURCE,
    (TESTS,),
    "d9a118315450b1e3df8bc00b6bbc29798845877b",
    (
        (SOURCE, "b01a8fdac51f3d5485275898b45d43cd643efac736b1e275b8a18fc205fd6195"),
        (TESTS, "92e5f321000054d18f30775387b24f65a1b2635fb02e15e2ea01643abdb4b7a9"),
    ),
    (
        (SOURCE, "MarkdownFile fence headings", "symbol", "file"),
        (TESTS, "markdown headings fenced code", "file", "file"),
    ),
    ACCEPTANCE,
)
_SOURCE = "src/devtools/context/python/function/materialization.py"
_TESTS = "tests/context/python/function/test_materialization.py"
SOURCE_SEGMENTS = CodingTask(
    "python-source-segments",
    "Fix exact Python function source materialization for valid AST source ranges "
    "when Unicode/ASCII non-newline separators occur inside strings or comments. "
    "Preserve original source bytes, UTF-8 byte-column semantics, LF/CRLF/CR "
    "line endings, sync/async functions and existing invalid-range rejection. "
    "Do not change identities, public APIs or unrelated behavior.",
    _SOURCE,
    (_TESTS,),
    "11225000d7c1e728fa1313f92a0c54214b75a426",
    (
        (_SOURCE, "b67c8cb67598a59d4b9250e8086065b79d6a7a11040511f6e3d565a220d11fa6"),
        (_TESTS, "7ac458ae2c86aa07326c184f5892f0c0542dc19f59aa961fb45fbbf8aa4c143c"),
    ),
    (
        (_SOURCE, "extract source segment UTF8 byte offset", "symbol", "file"),
        (_TESTS, "materializes source utf8 range", "file", "file"),
    ),
    SEGMENT_ACCEPTANCE,
)
TASK_NAMES = (MARKDOWN.name, SOURCE_SEGMENTS.name)


def select_task(name: str) -> CodingTask:
    """Select one maintained host definition, never model-generated task data."""
    for task in (MARKDOWN, SOURCE_SEGMENTS):
        if task.name == name:
            return task
    raise ValueError("Unknown coding task: " + name)
