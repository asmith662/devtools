# Copyright (c) 2026
# ruff: noqa: B009, C901, COM812, E501, EM101, PLR0911, PLR0912, PLR0915, PLR2004, TRY003
"""Outcome-blind imported-binding use in saved lexical seed windows."""

from __future__ import annotations

import ast
import hashlib
from collections import Counter
from pathlib import Path
from typing import Any, cast

from experiments.increment_25.development import _git, write_artifact
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import (
    MECHANICS_NAME,
    _digest,
    read_candidate_artifact,
)
from experiments.increment_27.window_unit import source_windows

ROOT27 = Path(__file__).resolve().parents[1] / "increment_27"
FREEZE_NAME = "import_use_freeze.json"
EVIDENCE_NAME = "import_use_evidence.json"
STATES = ("SUPPORTED", "NO_QUALIFYING_OCCURRENCE", "INDETERMINATE")


def build_freeze(root: Path = ROOT27) -> dict[str, Any]:
    """Bind the fixed population, inputs, and conservative source semantics."""
    candidates = read_candidate_artifact(root / MECHANICS_NAME)
    structural = cast("dict[str, Any]", _read_json(root / "structural_import_freeze.json"))
    windows = cast("dict[str, Any]", _read_json(root / "window_resource_rankings.json"))
    cases = cast("list[dict[str, Any]]", candidates["cases"])
    ids = [str(case["case_id"]) for case in cases]
    allowed = structural["payload"]["development_case_ids"]
    if len(ids) != 24 or ids != allowed or [case["case_id"] for case in windows["cases"]] != ids:
        raise ValueError("Increment 28 requires the exact saved development population.")
    outgoing = sum(len(case["arms"]["outgoing"]["candidates"]) for case in cases)
    union = sum(
        len({row["address"] for arm in case["arms"].values() for row in arm["candidates"]})
        for case in cases
    )
    if (outgoing, union) != (99, 109):
        raise ValueError("Existing structural candidate identities changed.")
    payload = {
        "development_case_ids": ids,
        "heldout_case_ids_sealed": structural["payload"]["heldout_case_ids_sealed"],
        "candidate_identity": candidates["content_identity"],
        "window_identity": windows["content_identity"],
        "source_sha256": {
            MECHANICS_NAME: sha256_file(root / MECHANICS_NAME),
            "window_resource_rankings.json": sha256_file(root / "window_resource_rankings.json"),
            "structural_import_freeze.json": sha256_file(root / "structural_import_freeze.json"),
        },
        "candidate_population": {"union_pairs": 109, "outgoing_pairs": 99},
        "proposition": "A source-grounded read of the specifically imported local binding in the seed's saved winning query-scored window qualifies one existing outgoing direct-import support; it creates no candidates.",
        "scope": "Direct module-body import declarations already grounded by uniquely resolved module-import relations. AST Name Load reads at module level and in function/async-function/lambda bodies with no local or enclosing-function competing binding. Class and comprehension scopes and function/variable annotation expressions are indeterminate for relevant reads. Import declarations are never reads.",
        "forms": {
            "import package": "local first dotted component; dotted target requires an Attribute chain with the full dotted target prefix",
            "import package as alias": "local alias names the requested module; alias read qualifies",
            "from package import name": "local imported name; its read qualifies for the resolved module-portion candidate",
            "from package import name as alias": "local alias; its read qualifies for the resolved module-portion candidate",
            "star_import": "indeterminate",
        },
        "competition": "Any additional module-scope binding of the local name (including pattern capture), named-expression assignment to that name, wildcard import, global/nonlocal declaration naming it anywhere in the source, dynamic exec/globals/locals call, or relevant read in an unsupported scope makes unsupported absence indeterminate. A verified qualifying read can establish support only when module binding is unique and its function scope chain is unshadowed.",
        "window": "Use saved positive winning window identity and half-open Unicode character bounds. An AST read occurrence must fit wholly inside; partial overlap is indeterminate. AST UTF-8 byte columns are mapped to Unicode character offsets against exact parent-snapshot source; saved text, hash, and window identity are verified before use.",
        "aggregation": "Classify every outgoing support first. Candidate has any-supported when at least one support is SUPPORTED; retain all support identities, counts, seed identities, incoming membership and strict saved-lexical escape membership. No weighted score.",
        "outcome_join_before_checkpoint": False,
        "new_candidates": 0,
    }
    return {"schema": "devtools-i28-import-use-freeze-v1", "content_identity": _digest(payload), "payload": payload}


def freeze(root: Path = ROOT27) -> dict[str, Any]:
    """Persist the semantics and population identity before deriving evidence."""
    artifact = build_freeze(root)
    path = root.parent / "increment_28" / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Increment 28 import-use freeze differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def _binding_name(node: ast.alias, *, from_import: bool) -> str | None:
    if node.name == "*":
        return None
    return node.asname or (node.name if from_import else node.name.split(".")[0])


def _bindings(node: ast.AST) -> tuple[Counter[str], bool, set[str]]:
    """Collect bindings in one lexical scope, excluding nested scope bodies."""
    names: Counter[str] = Counter()
    wildcard = False
    directives: set[str] = set()

    def visit(current: ast.AST) -> None:
        nonlocal wildcard
        if isinstance(current, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            names[current.name] += 1
            return
        if isinstance(current, ast.Lambda | ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp):
            return
        if isinstance(current, ast.Import | ast.ImportFrom):
            for alias in current.names:
                name = _binding_name(alias, from_import=isinstance(current, ast.ImportFrom))
                if name is None:
                    wildcard = True
                else:
                    names[name] += 1
            return
        if isinstance(current, ast.Name) and isinstance(current.ctx, ast.Store | ast.Del):
            names[current.id] += 1
        if isinstance(current, ast.ExceptHandler) and current.name:
            names[current.name] += 1
        if isinstance(current, ast.MatchAs | ast.MatchStar) and current.name:
            names[current.name] += 1
        if isinstance(current, ast.MatchMapping) and current.rest:
            names[current.rest] += 1
        if isinstance(current, ast.Global | ast.Nonlocal):
            directives.update(current.names)
        for child in ast.iter_child_nodes(current):
            visit(child)

    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda):
        args = node.args
        for arg in (*args.posonlyargs, *args.args, *args.kwonlyargs):
            names[arg.arg] += 1
        if args.vararg:
            names[args.vararg.arg] += 1
        if args.kwarg:
            names[args.kwarg.arg] += 1
        body = node.body if not isinstance(node, ast.Lambda) else [node.body]
        for child in body:
            visit(child)
    elif isinstance(node, ast.ClassDef):
        for child in node.body:
            visit(child)
    else:
        visit(node)
    return names, wildcard, directives


def _span(content: str, node: ast.AST) -> tuple[int, int, list[int]]:
    """Map Python AST UTF-8 byte columns into source Unicode character offsets."""
    lines = content.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))

    def offset(line: int, column: int) -> int:
        raw = lines[line - 1].encode("utf-8")[:column]
        return starts[line - 1] + len(raw.decode("utf-8"))

    lineno = int(getattr(node, "lineno"))
    col_offset = int(getattr(node, "col_offset"))
    end_lineno = int(getattr(node, "end_lineno"))
    end_col_offset = int(getattr(node, "end_col_offset"))
    start = offset(lineno, col_offset)
    end = offset(end_lineno, end_col_offset)
    return start, end, [lineno, col_offset, end_lineno, end_col_offset]


def _declaration(tree: ast.Module, resolution: dict[str, Any], path: dict[str, Any]) -> tuple[ast.Import | ast.ImportFrom, ast.alias] | None:
    ordinal = 0
    for node in tree.body:
        if not isinstance(node, ast.Import | ast.ImportFrom):
            continue
        span = [node.lineno, node.col_offset, node.end_lineno, node.end_col_offset]
        for alias in node.names:
            if ordinal == path["declaration_ordinal"] and span == path["import_source_span"]:
                module = alias.name if isinstance(node, ast.Import) else node.module
                imported = None if isinstance(node, ast.Import) else alias.name
                if module == resolution["module_text"] and imported == resolution["imported_name"] and alias.asname == resolution["local_alias"]:
                    return node, alias
                return None
            ordinal += 1
    return None


def _qualified_read(
    *, content: str, tree: ast.Module, resolution: dict[str, Any], path: dict[str, Any], window: dict[str, Any]
) -> dict[str, Any]:
    matched = _declaration(tree, resolution, path)
    if matched is None:
        return {"state": "INDETERMINATE", "reason": "declaration-mismatch", "occurrences": []}
    declaration, alias = matched
    local = _binding_name(alias, from_import=isinstance(declaration, ast.ImportFrom))
    if local is None:
        return {"state": "INDETERMINATE", "reason": "star-import", "local_binding": None, "occurrences": []}
    module_bindings, wildcard, _ = _bindings(tree)
    if module_bindings[local] != 1 or wildcard or any(
        (isinstance(node, ast.NamedExpr) and isinstance(node.target, ast.Name) and node.target.id == local)
        or (isinstance(node, ast.Global | ast.Nonlocal) and local in node.names)
        for node in ast.walk(tree)
    ):
        return {"state": "INDETERMINATE", "reason": "competing-module-binding-or-star-import", "local_binding": local, "occurrences": []}
    if any(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"exec", "globals", "locals"}
        for node in ast.walk(tree)
    ):
        return {"state": "INDETERMINATE", "reason": "dynamic-namespace-call", "local_binding": local, "occurrences": []}
    supported: list[dict[str, Any]] = []
    uncertain: list[dict[str, Any]] = []
    requested = str(resolution["requested_module"])

    def visit(node: ast.AST, scopes: tuple[tuple[str, Counter[str], set[str]], ...], parents: tuple[ast.AST, ...]) -> None:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            for outer in (*node.decorator_list, *node.args.defaults, *(value for value in node.args.kw_defaults if value is not None)):
                visit(outer, scopes, (*parents, node))
            annotations = [
                arg.annotation
                for arg in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs, node.args.vararg, node.args.kwarg)
                if arg is not None and arg.annotation is not None
            ]
            if node.returns is not None:
                annotations.append(node.returns)
            for annotation in annotations:
                visit(annotation, (*scopes, ("annotation", Counter(), set())), (*parents, node))
            for type_param in node.type_params:
                visit(type_param, (*scopes, ("annotation", Counter(), set())), (*parents, node))
            binds, _star, directives = _bindings(node)
            for child in node.body:
                visit(child, (*scopes, ("function", binds, directives)), (*parents, node))
            return
        if isinstance(node, ast.Lambda):
            for outer in (*node.args.defaults, *(value for value in node.args.kw_defaults if value is not None)):
                visit(outer, scopes, (*parents, node))
            binds, _star, directives = _bindings(node)
            for arg in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs, node.args.vararg, node.args.kwarg):
                if arg is not None and arg.annotation is not None:
                    visit(arg.annotation, (*scopes, ("annotation", Counter(), set())), (*parents, node))
            visit(node.body, (*scopes, ("function", binds, directives)), (*parents, node))
            return
        if isinstance(node, ast.AnnAssign):
            visit(node.target, scopes, (*parents, node))
            visit(node.annotation, (*scopes, ("annotation", Counter(), set())), (*parents, node))
            if node.value is not None:
                visit(node.value, scopes, (*parents, node))
            return
        if isinstance(node, ast.ClassDef):
            for outer in (*node.decorator_list, *node.bases, *(item.value for item in node.keywords)):
                visit(outer, scopes, (*parents, node))
            binds, _star, directives = _bindings(node)
            for child in node.body:
                visit(child, (*scopes, ("class", binds, directives)), (*parents, node))
            return
        if isinstance(node, ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp):
            for subnode in ast.iter_child_nodes(node):
                visit(subnode, (*scopes, ("comprehension", Counter(), set())), (*parents, node))
            return
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id == local:
            use_node: ast.AST = node
            if isinstance(declaration, ast.Import) and alias.asname is None:
                components = requested.split(".")
                if components[0] != local:
                    uncertain.append({"reason": "import-root-target-mismatch"})
                    return
                current: ast.AST = node
                chain: list[str] = []
                for ancestor in reversed(parents):
                    if not isinstance(ancestor, ast.Attribute) or ancestor.value is not current:
                        break
                    chain.append(ancestor.attr)
                    current = ancestor
                    if len(chain) == len(components) - 1:
                        break
                if chain[: len(components) - 1] != components[1:]:
                    return
                use_node = current
            try:
                start, end, span = _span(content, use_node)
            except (IndexError, UnicodeDecodeError, TypeError, ValueError):
                uncertain.append({"reason": "source-offset-mapping"})
                return
            lo, hi = int(window["char_start"]), int(window["char_end"])
            if end <= lo or start >= hi:
                return
            occurrence = {"span_utf8": span, "char_span": [start, end], "text": content[start:end]}
            if start < lo or end > hi:
                uncertain.append({**occurrence, "reason": "partial-window-overlap"})
            elif any(kind != "function" or binds[local] or local in directives for kind, binds, directives in scopes):
                uncertain.append({**occurrence, "reason": "unsupported-or-shadowed-scope"})
            else:
                supported.append(occurrence)
            return
        for subnode in ast.iter_child_nodes(node):
            visit(subnode, scopes, (*parents, node))

    visit(tree, (), ())
    if supported:
        return {"state": "SUPPORTED", "reason": None, "local_binding": local, "occurrences": sorted(supported, key=lambda row: row["char_span"]), "uncertain_occurrences": uncertain}
    if uncertain:
        return {"state": "INDETERMINATE", "reason": "uncertain-relevant-occurrence", "local_binding": local, "occurrences": uncertain}
    return {"state": "NO_QUALIFYING_OCCURRENCE", "reason": None, "local_binding": local, "occurrences": []}


def _verified_seed_source(repository_root: Path, snapshot_sha: str, address: str, window: dict[str, Any]) -> tuple[str, ast.Module]:
    content = _git(repository_root, "show", f"{snapshot_sha}:{address}").decode("utf-8")
    lo, hi = int(window["char_start"]), int(window["char_end"])
    selected = content[lo:hi]
    if selected != window["text"] or hashlib.sha256(selected.encode("utf-8")).hexdigest() != window["text_sha256"]:
        raise ValueError("Saved window differs from exact parent-snapshot source.")
    matching = [item for item in source_windows(content=content, address=address, parent_snapshot_sha=snapshot_sha) if item.ordinal == window["ordinal"]]
    if len(matching) != 1 or matching[0].identity != window["identity"] or (matching[0].char_start, matching[0].char_end) != (lo, hi):
        raise ValueError("Saved winning window identity or bounds differ.")
    return content, ast.parse(content, filename=address)


def derive_evidence(*, repository_root: Path, root: Path = ROOT27) -> dict[str, Any]:
    """Derive fixed-support evidence without loading usefulness artifacts."""
    frozen = _read_json(root.parent / "increment_28" / FREEZE_NAME)
    if frozen != build_freeze(root):
        raise ValueError("Import-use semantics must be frozen before derivation.")
    candidates = read_candidate_artifact(root / MECHANICS_NAME)
    windows = cast("dict[str, Any]", _read_json(root / "window_resource_rankings.json"))
    window_cases = {row["case_id"]: row for row in windows["cases"]}
    result_cases: list[dict[str, Any]] = []
    total_states: Counter[str] = Counter()
    for case in candidates["cases"]:
        case_id = str(case["case_id"])
        window_case = window_cases[case_id]
        if case["parent_snapshot_sha"] != window_case["parent_snapshot_sha"] or case["corpus_id"] != window_case["corpus_id"]:
            raise ValueError("Candidate and window historical corpus differ.")
        window_rows = {row["address"]: row for row in window_case["positive_resource_ordering"]}
        seeds = {row["address"]: row for row in case["seeds"]}
        needed_sources = {
            path["seed_address"]
            for candidate in case["arms"]["outgoing"]["candidates"]
            for path in candidate["paths"]
        }
        sources: dict[str, tuple[str, ast.Module]] = {}
        for address, seed in seeds.items():
            row = window_rows.get(address)
            if row is None or row["winning_window"] is None or seed["canonical_rank"] > 5:
                raise ValueError("Saved canonical seed lacks positive winning window.")
            if address in needed_sources:
                sources[address] = _verified_seed_source(repository_root, case["parent_snapshot_sha"], address, row["winning_window"])
        resolutions = {row["resolution_identity"]: row for source in case["relation_derivation"]["sources"] for row in source.get("resolutions", [])}
        incoming = {row["address"] for row in case["arms"]["incoming"]["candidates"]}
        outgoing = case["arms"]["outgoing"]["candidates"]
        candidate_rows: list[dict[str, Any]] = []
        for candidate in outgoing:
            supports: list[dict[str, Any]] = []
            for path in candidate["paths"]:
                seed_address = str(path["seed_address"])
                if path["source_resource"] != seed_address or path["target_resource"] != candidate["address"] or path["resolution_outcome"] != "resolved":
                    raise ValueError("Outgoing support differs from fixed candidate identity.")
                resolution = resolutions[path["resolution_identity"]]
                window = window_rows[seed_address]["winning_window"]
                content, tree = sources[seed_address]
                classified = _qualified_read(content=content, tree=tree, resolution=resolution, path=path, window=window)
                total_states[classified["state"]] += 1
                supports.append({
                    "case_id": case_id, "parent_snapshot_sha": case["parent_snapshot_sha"],
                    "seed_address": seed_address, "seed_canonical_rank": path["seed_rank"],
                    "window_identity": window["identity"], "window_char_span": [window["char_start"], window["char_end"]],
                    "declaration_derivation_identity": path["declaration_derivation_identity"],
                    "declaration_ordinal": path["declaration_ordinal"], "import_source_span": path["import_source_span"],
                    "resolution_identity": path["resolution_identity"], "relation_identity": path["relation_identity"],
                    "candidate_address": candidate["address"], "imported_module": resolution["requested_module"],
                    "imported_name": resolution["imported_name"], "local_alias": resolution["local_alias"],
                    **classified,
                })
            counts = Counter(row["state"] for row in supports)
            candidate_rows.append({
                "case_id": case_id, "address": candidate["address"], "outgoing": True, "incoming": candidate["address"] in incoming,
                "absent_all_saved_positive_lexical": candidate["absent_all_saved_positive_lexical"],
                "existing_support_count": candidate["support_count"],
                "existing_best_seed_rank": min(path["seed_rank"] for path in candidate["paths"]),
                "distinct_supporting_seeds": sorted({path["seed_address"] for path in candidate["paths"]}),
                "supported_seed_addresses": sorted({row["seed_address"] for row in supports if row["state"] == "SUPPORTED"}),
                "state_counts": {state: counts[state] for state in STATES},
                "any_supported": counts["SUPPORTED"] > 0,
                "supports": supports,
            })
        incoming_only = sorted(incoming - {row["address"] for row in outgoing})
        result_cases.append({"case_id": case_id, "parent_snapshot_sha": case["parent_snapshot_sha"], "outgoing": candidate_rows, "incoming_only_addresses": incoming_only})
    if sum(len(case["outgoing"]) for case in result_cases) != 99 or sum(len(case["incoming_only_addresses"]) for case in result_cases) != 10 or sum(total_states.values()) != 499:
        raise ValueError("Evidence did not preserve the 109-pair fixed candidate union.")
    rows = [row for case in result_cases for row in case["outgoing"]]
    hard = [row for row in rows if row["absent_all_saved_positive_lexical"]]

    def summary(values: list[dict[str, Any]]) -> dict[str, Any]:
        counts = Counter(state for row in values for state, n in row["state_counts"].items() for _ in range(n))
        selected = {(row["case_id"], row["address"]) for row in values}
        return {
            "candidate_pairs": len(values), "support_count": sum(row["existing_support_count"] for row in values),
            "support_states": {state: counts[state] for state in STATES},
            "candidate_any_supported": sum(row["any_supported"] for row in values),
            "candidate_only_no_occurrence": sum(row["state_counts"]["NO_QUALIFYING_OCCURRENCE"] == row["existing_support_count"] for row in values),
            "candidate_any_indeterminate": sum(row["state_counts"]["INDETERMINATE"] > 0 for row in values),
            "cases_with_supported": len({case["case_id"] for case in result_cases for row in case["outgoing"] if (case["case_id"], row["address"]) in selected and row["any_supported"]}),
        }

    artifact: dict[str, Any] = {
        "schema": "devtools-i28-import-use-evidence-v1", "freeze_identity": frozen["content_identity"],
        "candidate_identity": candidates["content_identity"], "window_identity": windows["content_identity"],
        "cases": result_cases, "summary": {"outgoing": summary(rows), "outgoing_all_lexical_escape": summary(hard), "incoming_only_pairs": 10, "fixed_union_pairs": 109},
        "usefulness_outcomes_loaded": False, "new_candidate_resources": 0, "heldout_executed": False,
    }
    artifact["content_identity"] = _digest(artifact)
    return artifact


def write_evidence(*, repository_root: Path, root: Path = ROOT27) -> dict[str, Any]:
    """Persist the source-grounded evidence without opening judgments."""
    artifact = derive_evidence(repository_root=repository_root, root=root)
    path = root.parent / "increment_28" / EVIDENCE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Increment 28 evidence differs from existing artifact.")
    write_artifact(path=path, payload=artifact)
    return artifact
