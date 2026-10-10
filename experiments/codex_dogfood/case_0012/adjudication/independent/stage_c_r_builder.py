"""Case 0012 C-R: frozen semantic decisions and deterministic stdlib-only replay.

Reads only the five supplied packet inputs and explicitly named C-R outputs.
Repository texts are data: none is imported, executed, or followed to disk.
"""
from __future__ import annotations

import ast
import copy
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SEALS = {
    "README.md": "b33c456f8999b4343d6dbe59c311c7866ae681668c9415f4042d8ced231cf7be",
    "manifest.json": "15c886a8af33bf2ba12c2a92e82ec3a33789a605064bded6f17ae4b603d579cf",
    "integrity.json": "89947624937675a94d6228e3c6fc6c206bc929600b4f21faf2f5cf22bf78a6f9",
    "resources.json.gz": "2cbc95afb120c920ed8d919e37a187f8fe0eec4618eff28eb25203d108599fe3",
    "validate_packet.py": "f6d1ec7068ac1a86beabaebf0f76b24df919ba2662ae54c8a40df0e92416a1ca",
}
CASE = "case-0012"
TASK = "case-0012-direct-source-disclosure"
KEYS = ("source", "choices", "integrity", "materialization", "assembly", "exports", "tests", "documentation", "validation")
LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "UNRESOLVED")
OUTPUTS = ("stage_c_r_review.json", "stage_c_r_statistics.json", "STAGE_C_R_REVIEW.md", "stage_c_r_method.md", "stage_c_r_validation.json", "stage_c_r_hashes.json")
BUILDER = "stage_c_r_builder.py"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def jb(obj):
    return (json.dumps(obj, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode("utf-8")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def packet():
    raw = {}
    for name, digest in SEALS.items():
        p = ROOT / name
        require(p.is_file() and not p.is_symlink() and not (getattr(p.stat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT), "input file type")
        raw[name] = p.read_bytes()
        require(sha(raw[name]) == digest, "input seal: " + name)
    manifest = json.loads(raw["manifest.json"])
    integrity = json.loads(raw["integrity.json"])
    payload_bytes = gzip.decompress(raw["resources.json.gz"])
    p = json.loads(payload_bytes)
    require(set(p) == {"case", "task_identity", "task_text", "obligations", "resources", "frame"}, "payload metadata whitelist")
    require(set(p["frame"]) == {"repository_id", "snapshot_id", "corpus_id", "frame_identity", "source_head"}, "frame metadata whitelist")
    require(p["case"] == CASE and p["task_identity"] == TASK, "case/task binding")
    require(manifest["case"] == CASE and manifest["task_identity"] == TASK and manifest["frame"] == p["frame"], "manifest binding")
    require(payload_bytes == jb(p), "canonical payload bytes")
    for key, digest in (("archive_sha256", sha(raw["resources.json.gz"])), ("canonical_payload_sha256", sha(payload_bytes))):
        require(manifest[key] == integrity[key] == digest, "packet digest " + key)
    require(integrity["manifest_sha256"] == sha(raw["manifest.json"]), "manifest digest")
    require(integrity["sha256"] == {n: h for n, h in SEALS.items() if n != "integrity.json"}, "input digest declarations")
    require(len(p["resources"]) == manifest["resources"] == 531, "531-resource frame")
    require(len(p["obligations"]) == manifest["obligations"] == 9, "nine obligations")
    require(tuple(o["key"] for o in p["obligations"]) == KEYS, "exact obligation keys/order")
    require([o["identity"] for o in p["obligations"]] == [TASK + "/" + k for k in KEYS], "exact obligation identities")
    for o in p["obligations"]:
        require(set(o) == {"identity", "key", "statement", "criterion", "applicability", "task_basis"}, "obligation metadata whitelist")
        for s in o["task_basis"]:
            require(p["task_text"][s["start"]:s["end"]] == s["text"], "task provenance")
    for r in p["resources"]:
        require(set(r) == {"address", "content_identity", "text", "encoding", "byte_size", "document_identity"}, "resource metadata whitelist")
        require(r["encoding"] == "utf-8" and len(r["text"].encode("utf-8")) == r["byte_size"], "resource content bounds")
    for key in ("address", "document_identity"):
        require(len({r[key] for r in p["resources"]}) == 531, "duplicate resource " + key)
    return p


class Evidence:
    def __init__(self, p):
        self.p = p
        self.items = []

    def span(self, index, start, end):
        t = self.p["task_text"] if index is None else self.p["resources"][index]["text"]
        require(0 <= start < end <= len(t), "authored support bounds")
        for e in self.items:
            if e["resource_index"] == index and e["start"] == start and e["end"] == end:
                return e["id"]
        r = None if index is None else self.p["resources"][index]
        e = {"id": "E%04d" % (len(self.items) + 1), "origin": "TASK" if r is None else "REPOSITORY",
             "resource_index": index, "resource_identity": None if r is None else r["document_identity"],
             "resource_address": None if r is None else r["address"], "content_identity": None if r is None else r["content_identity"],
             "start": start, "end": end, "text": t[start:end], "coordinate_system": "Unicode code points; zero-based; half-open",
             "start_line": t.count("\n", 0, start) + 1, "end_line": t.count("\n", 0, end - 1) + 1,
             "provenance": "sealed packet task_text" if r is None else "sealed packet resources[%d].text" % index}
        self.items.append(e)
        return e["id"]

    def quote(self, index, text):
        t = self.p["task_text"] if index is None else self.p["resources"][index]["text"]
        require(t.count(text) == 1, "nonunique/missing authored quote: " + str(index) + " " + text[:70])
        return self.span(index, t.index(text), t.index(text) + len(text))

    def section(self, index, heading):
        t = self.p["resources"][index]["text"]
        start = t.index(heading)
        level = len(heading) - len(heading.lstrip("#"))
        end = len(t)
        position = start + len(heading)
        for line in t[position:].splitlines(keepends=True):
            if line.startswith("#") and len(line) - len(line.lstrip("#")) <= level:
                end = position
                break
            position += len(line)
        return self.span(index, start, end)

    def node(self, index, name):
        t = self.p["resources"][index]["text"]
        tree = ast.parse(t)
        parts = name.split(".")
        current = tree
        for part in parts:
            current = next(n for n in current.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == part)
        lines = t.splitlines(keepends=True)
        first = min([current.lineno] + [n.lineno for n in getattr(current, "decorator_list", [])])
        return self.span(index, sum(map(len, lines[:first-1])), sum(map(len, lines[:current.end_lineno])))


def minimal_sets(sets):
    ordered = sorted(set(frozenset(s) for s in sets), key=lambda s: (len(s), sorted(s)))
    out = []
    for s in ordered:
        if not any(t <= s for t in out):
            out.append(s)
    return out


def resource_synopsis(r):
    t = r["text"]
    if r["address"].endswith(".py"):
        tree = ast.parse(t)
        subject = ast.get_docstring(tree) or "Python package/module without a module docstring"
        definitions = [n.name for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))]
        imports = sorted({n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module})
        return {"subject": subject, "top_level_definitions": definitions, "imports": imports, "method": "static AST inventory of the complete sealed text; no execution"}
    return {"subject": t.split("\n\n")[0], "headings": [s for s in t.splitlines() if s.startswith("#")], "method": "decoded complete text and structural document inventory"}


def construct_review(p):
    ev = Evidence(p)
    units = []
    def unit(uid, obligations, statement, necessity, proofs, scope="native repository contract"):
        bundles = []
        for evidence_ids, mode, inference in proofs:
            resources = sorted({ev.items[int(e[1:])-1]["resource_index"] for e in evidence_ids if ev.items[int(e[1:])-1]["resource_index"] is not None})
            bundles.append({"evidence": evidence_ids, "resources": resources, "support_mode": mode, "inferability_rationale": inference})
        units.append({"id": uid, "obligations": obligations.split(), "statement": statement, "scope": scope,
                      "necessity_rationale": necessity, "support_bundles": bundles,
                      "provenance": "independent semantic judgment over sealed task/resource spans", "status": "REQUIRED"})
    def direct(*ids):
        return (list(ids), "DIRECT", "The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.")
    def inferred(ids, why):
        return (ids, "INFERABLE", why)
    task_lines = p["task_text"].splitlines(keepends=True)
    task_evidence = [ev.quote(None, s) for s in task_lines]
    def taskproof(*line_numbers):
        return ([task_evidence[n-1] for n in line_numbers], "TASK_BACKED", "These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.")

    selection_code = ev.node(158, "select_python_module_source_declarations")
    selection_doc = ev.section(154, "## Exact source declaration selection")
    function_subject = ev.node(136, "PythonFunctionSubject")
    function_knowledge = ev.node(136, "PythonFunctionDeclarationKnowledge")
    function_dependency = ev.node(136, "PythonModuleResourceDependency")
    class_subject = ev.node(130, "PythonClassSubject")
    class_knowledge = ev.node(130, "PythonClassDeclarationKnowledge")
    method_subject = ev.node(130, "PythonMethodSubject")
    method_knowledge = ev.node(130, "PythonMethodDeclarationKnowledge")
    class_docs = ev.section(131, "## Identity, provenance, and containment")
    class_derive = ev.node(130, "derive_python_class_method_declarations")
    method_view = ev.node(129, "PythonClassMethodContainmentView")
    method_validate = ev.node(129, "build_python_class_method_containment_view")
    method_consumer = ev.node(99, "_ground_method")
    plan_protocol = ev.node(123, "PlannedDisclosure")
    plan_invariants = ev.node(123, "DisclosurePlan.__post_init__")
    plan_identity = ev.node(123, "DisclosurePlan.identity")
    snapshot_lookup = ev.node(181, "RepositorySnapshot.resource_at")
    resource_value = ev.node(180, "RepositoryResourceOccurrence")
    content_value = ev.node(180, "ContentIdentity")
    materialize = ev.node(122, "materialize_disclosure_plan")
    item = ev.node(122, "MaterializedDisclosureItem")
    context = ev.node(122, "ContextDisclosure")
    coordinates = ev.node(136, "PythonSourceRange")
    occurrence = ev.node(136, "PythonSourceOccurrence")
    function_derive = ev.node(136, "derive_python_function_declarations")
    class_occurrence = ev.node(130, "_occurrence")
    render = ev.node(124, "render_context_disclosure")
    assemble = ev.node(124, "assemble_context_disclosure_model_request")
    pytest_config = ev.quote(64, p["resources"][64]["text"].split("[tool.pytest.ini_options]", 1)[1].split("[tool.ruff]", 1)[0])
    mypy_config = ev.quote(64, '[tool.mypy]\npython_version = "3.12"\nstrict = true\nfiles = ["src", "tests", "experiments"]\nexplicit_package_bases = true\nmypy_path = ["src"]\n')
    profile = ev.section(60, "## Protected development test profile")
    static_checks = ev.section(60, "## Other quality gates")

    unit("U01", "source documentation", "The admitted future source choices are caller-selected direct function/class declarations and direct methods under a validated native class; source identity asserts no runtime attribute, imported-facade, inherited-method, or semantic resolution.", "Defines the mandatory supported/deferred boundary without substituting binding lookup for source selection.", [taskproof(1, 2)], "requested feature scope")
    unit("U02", "source integrity", "Exact module source selection consumes a matching retained module, exact identifier and CLASS/FUNCTION kind, retains both canonical analyses and every matching direct declaration, preserves repeated identities, and propagates native parse failure without successful coverage.", "The mandated selector's actual behavior and available native analyses must be known to reuse it and check supplied identities; the task supplies its name but not this contract.", [direct(selection_code), direct(selection_doc)])
    unit("U03", "source integrity materialization", "Function declaration knowledge retains a derivation identity, a distinct snapshot-local subject bound to resource/content dependency, parser definition and declaration ordinal, and an addressed source occurrence; a name is not the subject identity.", "Necessary to retain/check native function identity and provenance rather than reconstructing an identity from its name.", [direct(function_subject, function_knowledge, function_dependency, occurrence)])
    unit("U04", "source integrity materialization", "A direct class has separate knowledge, subject and derivation identities; its subject is bound to snapshot, exact resource dependency, derivation definition and module-class ordinal, with its own source occurrence.", "Class identity and source provenance must survive selection, validation and materialization, including repeated class names.", [direct(class_subject, class_knowledge), direct(class_docs)])
    unit("U05", "source integrity materialization", "A native direct method has its own source occurrence and a canonical containing_class; its subject additionally binds the parent class subject and ordinal within that class, so occurrence resource and lexical parent are distinct.", "A method cannot be selected/validated or disclosed as an unqualified function or a bare runtime attribute.", [direct(method_subject, method_knowledge), direct(class_docs)])
    unit("U06", "choices", "Each plan participant exposes purpose, repository_id, snapshot_id, representation, identity and materialize(snapshot) returning MaterializedDisclosureItem through PlannedDisclosure.", "These are the existing integration requirements that a new concrete option must implement.", [direct(plan_protocol)])
    unit("U07", "choices", "DisclosurePlan requires a nonblank purpose, a nonempty ordered tuple of choices with equal purpose/repository/snapshot, and distinct option identities.", "Preserving admission invariants requires the existing checks, not merely the task's abstract immutability request.", [direct(plan_invariants)])
    unit("U08", "choices", "The frozen plan identity incorporates purpose, repository and snapshot, preceding-plan identity and every ordered representation/option identity pair.", "Order and lineage must continue to distinguish plans; a new choice must not collapse those native identity inputs.", [direct(plan_identity, ev.node(123, "DisclosurePlan"))])
    unit("U09", "choices", "Add explicit source choices alongside existing qualified-reference and whole-resource choices, retaining immutable purpose/frame/order and compatibility without automatic retrieval or selection.", "States the required compatibility and admission policy; it does not require changing or reverse-engineering preserved adapters.", [taskproof(1, 3)], "requested integration behavior")
    unit("U10", "integrity", "RepositorySnapshot.resource_at(address) returns the retained occurrence whose address equals the requested address, and raises ValueError when none exists.", "The required retained-snapshot lookup and observable missing-resource behavior must be established without assuming a filesystem fallback.", [direct(snapshot_lookup)])
    unit("U11", "integrity materialization", "A retained RepositoryResourceOccurrence is an immutable value carrying address, independent ContentIdentity, exact content string, encoding and byte_size; address and content identity are distinct.", "Native retained content and owner-resource provenance must be checked and emitted using their actual fields, not invented from the task.", [direct(resource_value, content_value)])
    unit("U12", "integrity", "Every supplied declaration/resource must be checked for foreign or stale frame/content, missing resource, unsupported scope and mismatched returned identity before disclosure publication; no files are reacquired.", "These rejection categories and ordering are mandatory future behavior, even where existing helpers supply only part of validation.", [taskproof(4)], "requested validation behavior")
    unit("U13", "integrity", "Canonical class/method analysis from the retained source supplies the parent classes and their direct methods. Requiring the supplied parent and method to equal the corresponding native values and checking the method's containing_class establishes direct source scope without runtime resolution.", "A matching name or resource is insufficient; the parent and method must be connected to the current native analysis. The required information is that native membership/parent relation, not the identity of a particular consumer or containment helper.", [inferred([class_derive, method_knowledge], "The canonical traversal emits module-body classes and only methods directly in each class body, storing the actual containing_class. Equality/membership against these freshly derived native values checks the supplied pair; retained frame/content lookup and publication checks are supplied by the other integrity units."), inferred([selection_code, class_docs], "The selector rederives and retains class_analysis from the matching retained module. The explicit class/method contract establishes native parent-relative identities and direct containment. Membership/equality against that canonical analysis establishes the supplied pair without an additional consumer example."), inferred([selection_doc, class_docs], "The two package contracts jointly establish canonical retained-source analyses, supported direct scope and the canonical containing_class link. Comparing supplied values with those native analysis members is a bounded inference from the documented contracts, not a runtime-binding assumption."), direct(method_consumer), inferred([class_derive, method_view, method_validate], "This is a supported implementation route using the existing validated view. It adds no necessary fact when the same canonical membership/parent information is already established by a complete declaration-analysis support bundle.")])
    unit("U14", "integrity", "Common materialization rejects a foreign plan frame and checks each returned option_identity and representation before appending it; ContextDisclosure is constructed only after all options succeed and itself enforces positional item/choice alignment.", "The existing publication boundary must be preserved so an option cannot publish a mismatched or partial disclosure.", [direct(materialize, context)])
    unit("U15", "materialization", "Each common materialized item carries option identity, representation, resource-address and content-identity tuples, text and native_provenance; ContextDisclosure retains exactly one aligned item per ordered plan choice.", "This is the actual container contract for exact source plus native derivation/range/owner provenance in a mixed plan.", [direct(item, context, materialize)])
    unit("U16", "materialization", "Native source ranges use one-based lines, zero-based UTF-8 byte columns and exclusive ends, anchored by snapshot and resource address.", "Byte-preserving extraction cannot treat native columns as Python character indexes or normalize line endings.", [direct(coordinates, occurrence), inferred([ev.node(139, "_extract_source_segment"), ev.node(139, "_absolute_byte_offset")], "Half-open UTF-8 byte slicing, one-based line indexing and retained line endings establish the same coordinate contract; the addressed occurrence is supplied by U03-U05.")])
    unit("U17", "materialization", "Current native declaration ranges start at def/async def/class and exclude preceding decorator lines; decorated source declarations remain native declarations.", "The decorator requirement cannot be satisfied by assuming that the existing occurrence range already includes its decorators.", [direct(class_docs), inferred([function_derive, class_occurrence], "Both native analyzers use the declaration node's lineno/col_offset. Their code retains declarations without rejecting decorator_list; the class documentation explicitly corroborates the resulting declaration-keyword boundary.")])
    unit("U18", "materialization", "Materialize the selected exact declaration source with derivation/range/owner provenance, preserving decorators, UTF-8 boundaries, CRLF/non-ASCII bytes and mixed caller order; neither expand to whole owners nor claim sufficiency implicitly.", "Defines the future faithful representation independently of any existing function-only materializer; U17 constrains how the requested decorator preservation is implemented.", [taskproof(5)], "requested materialization behavior")
    unit("U19", "assembly", "Common rendering emits disclosure purpose, plan/snapshot identity, item count, then each item's ordinal, representation, option identity and already materialized text in plan order.", "Preserving common rendering requires its actual presentation/ordering contract, not a new language-specific renderer in common assembly.", [direct(render)])
    unit("U20", "assembly", "Common request assembly frames the unchanged task before rendered Context using UTF-8 byte lengths, and dataclasses.replace changes only the Prompt while preserving the original prompt role.", "This is the existing request-copy mechanism whose behavior must survive the new representation.", [direct(assemble)])
    unit("U21", "assembly", "Original request, prompt role, settings, conversation, provider settings and tools are preserved except for the copied prompt; no new budget or truncation policy is introduced.", "The task supplies the preservation target, including tools; current request field names need not be independently rediscovered just to restate that target.", [taskproof(6)], "requested preservation behavior")
    unit("U22", "exports", "Expose the new explicit choice through the common planning public API and the outer Context facade.", "These public destinations are mandatory task-supplied interface locations. An existing initializer is a useful edit reference, but contributes no additional necessary semantic decision.", [taskproof(7)], "requested public exposure")
    unit("U23", "exports", "Keep dependency direction: do not add a Retrieval dependency or language-specific logic in common assembly.", "This is an authoritative constraint on the new design. Existing facade imports are not a requirement to reproduce their implementation form.", [taskproof(7)], "requested ownership boundary")
    unit("U24", "tests", "Focused tests must exercise direct function/class/method choices, decorated declarations and repeated declarations.", "Each family is an explicitly required future test target; repeated native identities must not be replaced by last-binding assumptions.", [taskproof(8)], "requested test coverage")
    unit("U25", "tests", "Focused tests must verify mixed-plan order and exact source/provenance, including the exactness constraints stated for materialization.", "Order and provenance are distinct observable outcomes requiring assertions.", [taskproof(5, 8)], "requested test coverage")
    unit("U26", "tests", "Tests must reject stale, foreign and missing-resource inputs and cover the task's supplied-identity/scope and publication guards.", "Failure behavior must be exercised; new tests can be authored without adopting any existing test fixture.", [taskproof(4, 8)], "requested test coverage")
    unit("U27", "tests", "Regression tests must preserve existing choices and copied-request semantics, including tools and the unchanged original request.", "The task explicitly requires these preserved behaviors to remain testable; existing test files are examples rather than mandatory witnesses.", [taskproof(6, 8)], "requested test coverage")
    unit("U28", "tests", "The repository's test framework is pytest under tests/, with strict configuration/markers and devtools branch coverage including a 100% threshold.", "New tests must participate in the actual configured framework and gate; the task names the settings file but does not provide its contents.", [direct(pytest_config)], "existing test convention")
    unit("U29", "documentation", "Update src/devtools/context/planning/docs/overview.md and docs/architecture.md for the new explicit source-disclosure behavior.", "The two required documentation destinations are supplied by the task; their locations are themselves the necessary fact.", [taskproof(9)], "requested documentation destinations")
    unit("U30", "documentation", "The updated documentation must explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, and make no automatic relevance or readiness claim.", "This future documentation content is fully prescribed by the task and U01; existing prose is context for editing, not an additional mandatory fact.", [taskproof(1, 2, 3, 7, 9)], "requested documentation content")
    unit("U31", "validation", "The documented protected development command is uv run python scripts/validate_development.py; it runs tests/ while excluding tests/experiments/ before recursive collection, uses configured pytest settings unchanged and returns the pytest exit status.", "The documented command and precise isolation/configuration behavior are necessary; merely knowing the script filename does not establish them.", [direct(profile)], "existing protected development contract")
    unit("U32", "validation", "Preserved configuration enables strict pytest configuration/markers, devtools branch coverage, term-missing output and 100% thresholds; strict mypy covers src, tests and experiments with explicit package bases and src on mypy_path.", "These existing settings must be retained. Type-checking an experiments path does not authorize executing excluded experiment tests.", [direct(pytest_config, mypy_config)], "existing protected configuration")
    unit("U33", "validation", "Run separate Ruff lint and format checks, mypy, worktree whitespace and staged-index whitespace checks using the documented commands; the protected entry point runs tests only.", "The task's tool names alone do not supply the complete documented command contract and staged-index distinction.", [direct(static_checks)], "existing documented quality gates")
    unit("U34", "validation", "The protected development profile does not validate confirmation judgments/outcomes; that activity is separately authorized, and the experiment-tree exclusion must not be removed to obtain a pass.", "This is the frozen validation criterion's operational boundary, not a software-feature requirement or a reason to access excluded data.", [direct(profile)], "existing validation isolation boundary")

    # Alternatives are exhaustive inclusion-minimal covers of the independently
    # assessed support bundles. All evidence inside a bundle is complementary.
    alternatives = []
    for key in KEYS:
        relevant = [u for u in units if key in u["obligations"]]
        covers = [frozenset()]
        for u in relevant:
            covers = minimal_sets(a | frozenset(b["resources"]) for a in covers for b in u["support_bundles"])
        for number, resources in enumerate(covers, 1):
            supports = []
            for u in relevant:
                valid = [i for i, b in enumerate(u["support_bundles"]) if set(b["resources"]) <= resources]
                require(valid, "authored alternative coverage")
                supports.append({"unit": u["id"], "support_bundle": valid[0]})
            essential = {}
            for r in sorted(resources):
                essential[str(r)] = [u["id"] for u in relevant if not any(set(b["resources"]) <= resources - {r} for b in u["support_bundles"])]
            alternatives.append({"id": key + "-A%d" % number, "obligation": key, "units": [u["id"] for u in relevant],
                                 "resources": sorted(resources), "task_backed_units": [u["id"] for u in relevant if any(not b["resources"] for b in u["support_bundles"])],
                                 "support_relationships": supports,
                                 "completeness_rationale": "Every required unit for this obligation has a complete supported bundle; task prescriptions are combined with current native contracts only where those contracts are needed.",
                                 "minimality_rationale": "Removing any listed resource leaves the indicated unit(s) unsupported. No superfluous corroboration is included.",
                                 "removal_witnesses": essential,
                                 "inferability_assumptions": "Trust the scoped explicit package contract where it agrees with native code; inferred compositions are confined to each cited support bundle. These are evidence alternatives, not alternate claims that the future feature already exists."})

    helpful = {}
    def help_resource(index, obligations, rationale, evidence):
        for key in obligations.split():
            helpful[(index, key)] = {"rationale": rationale, "evidence": evidence}

    help_resource(0, "exports documentation validation", "The operating guide corroborates package ownership, documentation impact and the protected validation boundary. The needed task constraints and exact commands/settings have complete narrower support; agent-operating instructions are not additional feature obligations.", [ev.section(0, "## Documentation and validation"), ev.section(0, "## Reuse canonical primitives and substrates")])
    help_resource(2, "choices materialization assembly exports documentation", "The current architectural account corroborates the narrow caller-directed plan, provenance-bearing disclosure and separated assembly, while also describing future planning. This context is useful for edits but contributes no additional necessary fact beyond the task and exact implemented contracts.", [ev.section(2, "## Accepted Context and disclosure semantics")])
    architecture_text = p["resources"][2]["text"]
    help_resource(2, "source integrity", "The architectural native-function/class account corroborates distinct subjects, source occurrences, direct scope and class-parent containment. It does not state every concrete identity/dependency field required by the complete native contract and therefore does not substitute for those narrower sources.", [ev.span(2, architecture_text.index("The first bounded derivation consumes one caller-selected resource occurrence"), architecture_text.index("`context.python.imports` separately derives"))])
    help_resource(4, "source integrity materialization documentation", "The architecture explains identity/occurrence and derivation distinctions at a broader level. Native declaration contracts and the task establish the bounded facts needed here without requiring the full architectural framework.", [ev.section(4, "### Repository subjects and source occurrences")])
    help_resource(6, "choices materialization assembly exports documentation", "Planning-versus-assembly guidance corroborates the requested ownership and semantic-strength constraints. It does not supply a missing implemented contract.", [ev.section(6, "### Planning versus model-input assembly")])
    help_resource(10, "source choices materialization assembly exports documentation", "The taxonomy corroborates immutable plan/disclosure distinctions and the absence of automatic sufficiency. The task and narrow native code already establish the necessary feature facts.", [ev.section(10, "### Context disclosure and assembly")])
    help_resource(57, "validation", "The implemented-profile section corroborates protected selection, retained coverage and exit-code propagation; it is redundant with the complete development contract and actual configuration.", [ev.section(57, "## Implemented contract")])
    help_resource(61, "documentation", "The document's authority-and-ownership introduction clarifies the role of current architecture versus taxonomy. The task already supplies the required documentation destinations and update content.", [ev.quote(61, "- [Central architecture](architecture.md) is the canonical current and accepted\n  system-architecture overview: domains, boundaries, dependency direction,\n  cross-domain composition, and whether architecture is implemented/current or\n  accepted but not implemented. It must be understandable without replaying all\n  ADRs.")])
    help_resource(65, "validation", "The script concretely corroborates the documented tests/ exclusion and returned pytest status. Its full semantic command behavior is already stated in the required development contract, so naming this entry point does not make its source additionally necessary.", [ev.node(65, "pytest_arguments"), ev.node(65, "main")])
    help_resource(83, "exports", "The current facade import/export lists are useful edit context. Public destination and required exposure are supplied by the task; preserving unrelated exports does not require treating their entire inventory as new necessary feature information.", [ev.quote(83, p["resources"][83]["text"].split("from devtools.context.python import", 1)[0])])
    help_resource(99, "source integrity tests", "Existing method/declaration grounding is a concrete consumer example of native source selection and validated parent containment. Canonical analysis membership and the native parent link already establish the necessary information in every minimal integrity alternative, so this consumer is corroboration rather than an additional prerequisite.", [method_consumer, ev.node(99, "_ground_declaration")])
    help_resource(120, "choices exports", "The planning initializer shows current public symbols and is useful for adding exports, but the existing option protocol and task-supplied public destinations establish the necessary contracts.", [ev.span(120, 0, len(p["resources"][120]["text"]))])
    help_resource(121, "choices integrity materialization assembly exports documentation", "Package prose corroborates the two current options, immutable ordered plan and copied request. It is useful update context, without replacing the exact current protocol/materialized-item contracts or adding a semantic requirement to the task.", [ev.quote(121, "DisclosurePlan binds purpose, repository and snapshot identities, ordered\nchoices, and optional preceding-plan identity. The plan's deterministic\nidentity changes when purpose, applicability, order, choice, or lineage changes.\nEach concrete choice names an implemented representation and retains its own\nnative support. The common PlannedDisclosure protocol only permits the two\ncurrent consumers to participate in one plan; it is not a generic fact ontology,\nlanguage-independent parser, or materializer registry."), ev.quote(121, "materialize_disclosure_plan rechecks the supplied snapshot and requires each\nmaterialized item to match its planned choice. It fails on stale, missing, or\nincompatible dependencies. A ContextDisclosure retains one item per choice,\nexact content identities and addresses, text, and the native materialized\nprovenance. Rendering preserves plan order and does not infer new facts.\nassemble_context_disclosure_model_request copies a caller's ModelRequest and\nappends already-rendered Context after the unchanged task.")])
    help_resource(122, "choices tests", "The result type and common materialization guards provide implementation and regression-test context for a new protocol participant; their necessity is charged to integrity/materialization rather than to a second invented choice-admission rule.", [item, materialize])
    help_resource(123, "integrity materialization exports tests documentation", "The native immutable plan and protocol corroborate the frame/order and ownership behavior; the obligation's own required units use more specific realization checks or task-prescribed test/documentation targets.", [plan_protocol, plan_invariants])
    help_resource(124, "exports tests documentation", "The common renderer/assembler demonstrates the desired separation and copied-request regression target. Future tests and exports do not require new knowledge of its exact formatting in addition to the assembly obligation.", [render, assemble])
    help_resource(125, "choices integrity materialization tests", "The existing whole-resource option is a useful preserved-compatibility and retained-content validation example. It is not a mandatory template for a new direct-source representation or an implicit whole-owner fallback.", [ev.node(125, "WholeResourceDisclosureOption"), ev.node(125, "choose_whole_resource_disclosure")])
    help_resource(129, "source integrity tests", "The validated view is a useful direct-containment API and test example. Its necessary membership/parent information is already available from the complete canonical declaration contract; validating supplied native identities does not require one particular view implementation in addition to canonical replay/equality.", [method_view, method_validate])
    help_resource(130, "tests documentation", "Native class/method derivation provides examples for test fixtures and precise scope descriptions, without making existing implementation details additional prescribed test/documentation outcomes.", [class_derive, method_knowledge])
    help_resource(131, "tests documentation", "The class/method package explains identities, direct containment and decorator-range limits. It is useful documentation/test context but does not add mandatory future test families or documentation destinations.", [class_docs])
    help_resource(135, "source integrity materialization tests", "The function-containment view provides another validation/navigation example. Canonical selector replay plus exact native membership can satisfy the required checks without requiring this additional aggregate-view mechanism.", [ev.node(135, "build_python_function_declaration_containment_view")])
    help_resource(136, "tests documentation", "The native function model and analyzer help author exact identity/range tests and descriptions; the task prescribes future coverage and other obligations already bind these native facts.", [function_subject, function_derive])
    help_resource(138, "source choices integrity materialization assembly documentation", "Function package prose corroborates direct source versus binding, retained-source extraction and compatibility, but some Reference terminology is narrower than current code. It is not a unique complete native contract for this change.", [ev.section(138, "## Direct declaration containment"), ev.section(138, "## Context disclosure")])
    help_resource(139, "integrity materialization tests", "The UTF-8 extractor is a useful canonical reuse candidate and supports the coordinate fact. Every minimal materialization alternative already needs the native function model, which supplies that coordinate fact; the algorithm's source is therefore not an additional necessary information member.", [ev.node(139, "_extract_source_segment"), ev.node(139, "_absolute_byte_offset")])
    help_resource(140, "choices materialization exports tests", "The qualified-reference adapter is a concrete protocol example and compatibility reference. The new option can preserve it through the existing protocol without modifying or reproducing its internals.", [ev.node(140, "PythonQualifiedReferenceDisclosureOption")])
    help_resource(141, "choices integrity materialization tests", "The preserved qualified-reference path illustrates rechecking native membership and retained dependencies before exact extraction. Direct source declarations must not acquire its imported-reference semantics.", [ev.node(141, "materialize_python_qualified_reference_source")])
    help_resource(143, "assembly tests", "The older function-specific request assembler corroborates the copy-and-task-first pattern. It does not establish the exact common rendering contract, so cannot substitute for the common assembler on its own.", [ev.node(143, "assemble_python_function_context_model_request")])
    help_resource(153, "source documentation", "Binding lookup provides a useful contrast to source selection, retaining conservative decorated/rebound-target behavior. The task and native source selector already establish that this binding path must not be substituted.", [ev.node(153, "lookup_python_module_declaration")])
    help_resource(154, "tests documentation", "The source-selector documentation is useful for test and documentation wording; future test coverage and documentation content are task prescriptions, not proof that new disclosure choices already exist.", [selection_doc])
    help_resource(155, "source integrity tests", "Module interpretation supplies useful fixture-construction and retained-resource context. The task accepts caller-supplied native declarations and the source selector already establishes the admitted module fields; no new module-discovery mechanism is required.", [ev.node(155, "PythonModuleInterpretation"), ev.node(155, "interpret_python_module_resources")])
    help_resource(158, "tests documentation", "The canonical selector is a useful test setup and documentation example. Its API necessity belongs to native source/integrity obligations, not to treating the future test matrix as an existing implementation contract.", [selection_code])
    help_resource(172, "source choices documentation", "The Reference documentation distinguishes bounded binding-based relations from direct source identity and helps explain compatibility. Source disclosure itself does not need Reference resolution.", [ev.span(172, 0, min(len(p["resources"][172]["text"]), 1700))])
    help_resource(180, "source tests", "The immutable retained resource value is useful to construct source fixtures and understand owners. Source identity's native dependency fields and task scope can be established without separately requiring this resource for that obligation.", [resource_value])
    help_resource(181, "source tests", "The snapshot lookup is useful source/test setup context, with its necessary missing-resource contract separately established under integrity.", [snapshot_lookup])
    help_resource(254, "assembly", "The interaction overview corroborates request immutability and model ownership. Task prescriptions plus the common dataclass-copy implementation suffice for preserving all request fields.", [ev.span(254, 0, 1000)])
    help_resource(255, "assembly tests", "ModelRequest's actual immutable field inventory confirms tools/settings/conversation/provider fields. The task authoritatively names the preservation target and common assembly uses replace, so this confirmation is useful but not necessary.", [ev.node(255, "ModelRequest")])
    help_resource(257, "assembly tests", "Prompt is useful confirmation of content/role representation; the task and common assembly already establish the required copying behavior.", [ev.node(257, "Prompt")])
    help_resource(383, "choices integrity materialization assembly tests", "Existing pytest cases provide concrete mixed-order, stale/missing, returned-identity and copied-request examples. New tests can be written from the task and established native contracts; this test file is not required merely because regression tests are requested.", [ev.node(383, "test_mixed_plan_preserves_purpose_sources_and_request"), ev.node(383, "test_materialization_rejects_an_option_that_changes_its_plan")])
    help_resource(387, "source integrity materialization tests", "Class/method tests demonstrate direct scope, native parent and decorator-keyword span boundaries. They corroborate rather than replace the complete native identity and validation contracts.", [ev.node(387, "test_direct_classes_methods_exclusions_and_existing_function_contract")])
    help_resource(390, "source integrity tests", "Function-containment tests illustrate invalid aggregate/declaration support. Reusing this exact aggregate or fixture is not required for new direct choices.", [ev.node(390, "test_rejects_inconsistent_coverage_and_declaration_support")])
    help_resource(393, "source materialization tests", "Tests corroborate repeated native subjects and UTF-8 coordinates but do not supply a complete alternative for every native identity/provenance fact.", [ev.node(393, "test_multiple_same_name_direct_declarations_have_distinct_subjects"), ev.node(393, "test_source_range_uses_utf8_byte_columns")])
    help_resource(395, "integrity materialization tests", "Tests provide CRLF/non-ASCII and malformed-range examples for the existing function-only path; they do not prescribe a new direct-source API or solve decorator-inclusive provenance.", [ev.node(395, "test_materializes_duplicate_sync_and_async_exact_multiline_source"), ev.node(395, "test_rejects_source_ranges_that_cannot_be_faithfully_applied")])
    help_resource(396, "choices integrity materialization tests", "Qualified-reference tests are useful compatibility examples of stale/redirected support and exact target preservation. Direct source disclosure can preserve the existing adapter without requiring these tests as semantic witnesses.", [ev.node(396, "test_stale_source_or_target_content_is_rejected"), ev.node(396, "test_redirected_or_missing_resources_are_rejected")])
    help_resource(397, "assembly tests", "Older function rendering tests illustrate exact source and ordered presentation. They are not a complete proof of the current common renderer's metadata contract.", [ev.node(397, "test_renders_ordered_duplicate_sync_and_async_context_exactly")])
    help_resource(398, "assembly tests", "Older request assembly tests illustrate task-first copying and unchanged request semantics, without requiring that older assembly path in the new common representation.", [ev.node(398, "test_assembles_real_context_after_distinct_unchanged_task")])
    help_resource(409, "source integrity tests documentation", "Selection tests demonstrate decorated/repeated source identity, negative kind/scope cases and foreign inputs. They are useful executable examples, but the complete selector contract also needs retained analyses and parse-failure behavior explicitly established elsewhere.", [ev.node(409, "test_plain_and_decorated_native_identity"), ev.node(409, "test_exact_kind_scope_and_repeated_declarations"), ev.node(409, "test_selection_rejects_invalid_and_foreign_inputs")])
    help_resource(473, "assembly tests", "Request-value tests corroborate immutability, typed settings and Prompt semantics. The task plus common replace-based copying makes these confirmations dispensable to the required preservation information.", [ev.node(473, "test_model_request_is_immutable_and_separates_input_from_settings")])
    help_resource(524, "validation", "Profile tests corroborate pre-collection exclusion and failure-code propagation. They add no missing command or configuration fact beyond the complete documented profile.", [ev.node(524, "test_profile_selects_tests_and_excludes_experiment_tests_before_collection"), ev.node(524, "test_profile_propagates_pytest_failure_code")])

    resources = [{"index": i, **{k: v for k, v in r.items() if k != "text"}, "text_sha256": sha(r["text"].encode("utf-8")), "inspection": resource_synopsis(r)} for i, r in enumerate(p["resources"])]
    cells = []
    for r in resources:
        for key in KEYS:
            alts = [a for a in alternatives if a["obligation"] == key and r["index"] in a["resources"]]
            if alts:
                bindings = sorted({u["id"] for u in units if key in u["obligations"] and any(r["index"] in b["resources"] and any(set(b["resources"]) <= set(a["resources"]) for a in alts) for b in u["support_bundles"])})
                supports = sorted({eid for u in units if u["id"] in bindings for b in u["support_bundles"] for eid in b["evidence"] if ev.items[int(eid[1:])-1]["resource_index"] == r["index"]})
                label = "REQUIRED"
                rationale = "This resource establishes " + ", ".join(bindings) + ". It is an indispensable member within at least one complete minimal alternative (" + ", ".join(a["id"] for a in alts) + "); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information."
                inferability = "Use only the linked support bundles' direct statements or explicit bounded inferences; identity/name or likely edit location alone is not the necessity basis."
            elif (r["index"], key) in helpful:
                h = helpful[(r["index"], key)]
                label, rationale, supports, bindings = "HELPFUL_ONLY", h["rationale"], h["evidence"], []
                inferability = "The cited example or corroboration is dispensable to every minimal complete evidence alternative for this obligation. It is not used to assume future implementation state."
            else:
                label, supports, bindings = "UNNECESSARY", [], []
                subject = r["inspection"]["subject"].replace("\n", " ")
                rationale = "Resource scope: " + subject + ". For " + key + ", this supplies no additional necessary or materially useful contract beyond the task and explicitly supported native units. It neither substitutes for a complete unit support bundle nor introduces a task-required dependency; shared terminology, transitive imports and file roles alone do not establish need."
                inferability = "No task-required fact is inferred from this resource for this obligation; the complete sealed resource identity remains in the fixed Cartesian frame."
            cells.append({"resource_index": r["index"], "resource_identity": r["document_identity"], "resource_address": r["address"], "obligation": key, "obligation_identity": TASK + "/" + key,
                          "label": label, "evidence": supports, "unit_bindings": bindings, "rationale": rationale, "inferability_rationale": inferability,
                          "provenance": "independent sealed-frame semantic adjudication"})

    coverage_obligations = [["source", "choices"], ["source"], ["choices"], ["integrity"], ["materialization"], ["assembly"], ["exports"], ["tests"], ["documentation"], ["validation"]]
    clause_details = [
        ["caller-selected direct Python source choices", "common planning integration alongside qualified-reference/whole-resource choices", "no automatic retrieval or selection"],
        ["reuse the exact named native selector", "direct function/class source identities", "method only through validated native class parent and containment", "exclude runtime attributes, imported facades, inherited methods and semantic resolution"],
        ["integrate DisclosurePlan and common planning module", "retain immutable purpose/frame/ordered-choice contracts", "preserve existing choices"],
        ["validate every supplied native declaration/resource", "use retained RepositorySnapshot.resource_at", "reject foreign/stale frame and content", "reject missing resource", "reject unsupported declaration scope", "reject mismatched returned identity before publishing", "no reacquisition"],
        ["exact declaration source segment in ContextDisclosure", "native derivation/source-range/owner provenance", "UTF-8 boundaries", "decorators", "CRLF and non-ASCII bytes", "mixed caller order", "no sufficiency inference", "no implicit whole-owner expansion"],
        ["preserve common rendering", "copy ModelRequest and leave original unchanged", "preserve role/settings/conversation/provider settings/tools except copied prompt", "task before Context", "no new budget or truncation"],
        ["common planning public API", "outer Context facade", "dependency direction", "no Retrieval dependency", "no language-specific common assembly"],
        ["direct function/class/method tests", "decorated and repeated tests", "mixed order and exact source/provenance tests", "stale/foreign/missing-resource rejection tests", "existing-choice regression", "copied-request preservation regression"],
        ["both exact named documentation destinations", "source identity versus runtime bindings", "explicit representation admission", "supported/deferred scope", "compatibility", "no automatic relevance/readiness claim"],
        ["named validation entry point", "preserve pyproject test/coverage settings", "documented protected development profile", "Ruff lint/format", "strict mypy", "both worktree and index whitespace checks"],
    ]
    audit = [{"id": "C%02d" % (i+1), "task_evidence": task_evidence[i], "exact_text": task_lines[i], "obligations": coverage_obligations[i],
              "requirements": [{"statement": clause, "coverage": "ADEQUATELY_COVERED", "obligations": coverage_obligations[i], "rationale": "The frozen statement/criterion and linked task basis expressly encompass this substantive clause."} for clause in clause_details[i]]} for i in range(10)]

    limitations = [
        {"id": "L01", "category": "native representation boundary", "statement": "Native spans exclude preceding decorators although decorated declarations are selected. The task requires decorator preservation. A compliant implementation must retain the native occurrence/identity and explicitly account for any decorator-inclusive materialized extent, or evolve native range semantics with appropriate provenance; simply slicing the existing occurrence cannot meet that requirement.", "evidence": [task_evidence[4], class_docs, function_derive, class_occurrence], "rationale": "All needed retained source and analyzer behavior are available. The future representation design remains to be made; this is not an unavailable repository fact.", "blocks_complete_adjudication": False},
        {"id": "L02", "category": "bounded caller/API design choice", "statement": "Exact source selection retains repeated same-name declarations. The task does not choose option-constructor names or a cardinality API. Callers may select exact native identities or an explicit ordered set; taking the first/last declaration as a runtime winner would violate the source/selection boundary.", "evidence": [task_evidence[0], task_evidence[1], selection_code, selection_doc], "rationale": "The required semantics are fixed while several explicit API designs remain valid.", "blocks_complete_adjudication": False},
        {"id": "L03", "category": "current documentation mixes implemented and future intent", "statement": "The current package/native code implement a narrow plan, disclosure and assembler, while broad ADR status still describes an unimplemented general planning/assembly direction. Use the precise implemented contract for current behavior and keep broader claims explicitly future-scoped in updates.", "evidence": [plan_protocol, materialize, assemble, ev.section(6, "## Status and implementation boundary"), ev.section(2, "## Accepted Context and disclosure semantics")], "rationale": "The available implementation and current bounded architecture account establish repository truth despite broader status prose; this does not require guessing missing code.", "blocks_complete_adjudication": False},
        {"id": "L04", "category": "existing helper validates only part of a future contract", "statement": "Native containment checks validate frame/dependency/coverage/ordinal/support consistency; they do not by themselves rederive arbitrary caller-constructed names/ranges. Canonical replay and membership/equality, as illustrated by method grounding, can supply that additional admission check before publication.", "evidence": [method_validate, method_consumer, selection_code, task_evidence[3]], "rationale": "No blanket claim is made that a frozen dataclass or containment view authenticates every supplied field. The task can be satisfied from retained source.", "blocks_complete_adjudication": False},
    ]
    blindness_keys = ["repository_checkout", "Git_history_or_commands", "parent_directory", "sibling_workspaces", "PRIMARY_Stage_C_adjudication", "any_prior_gold", "retrieval_queries", "analyzed_terms", "rankings", "scores", "hint_inventories", "routing_artifacts", "treatment_arms", "treatment_results", "acquisition_costs", "reliability_protocol_or_results", "known_disagreement_propositions", "confirmation_data", "reserve_data", "external_web_information", "prior_Codex_session_content"]
    review = {"schema": "case-0012-independent-c-r-review-v1", "case": CASE, "task_identity": TASK, "task_text": p["task_text"], "frame": p["frame"],
              "input_seals": SEALS, "initial_sterility": {"exact_whitelist": sorted(SEALS), "no_subdirectories": True, "no_git_or_local": True, "no_links_junctions_reparse_points": True, "standalone_validator": "VERIFIED; NO ADJUDICATION", "validator_exit_code": 0},
              "obligations": p["obligations"], "applicability": [{"obligation": k, "status": "APPLICABLE", "rationale": "The corresponding task clause is mandatory and unconditional; the frozen applicability statement provides no satisfied exclusion."} for k in KEYS],
              "task_interpretation_audit": audit,
              "interpretation_note": "All 10 task sentences and every listed substantive subclause are covered. The validation criterion's excluded-confirmation boundary is an operational validation restriction, not an added software feature. Packet/operator instructions are not feature semantics.",
              "resources": resources, "cells": cells, "evidence": ev.items, "units": units, "alternatives": alternatives,
              "gap_assessments": [{"kind": k, "status": "NONE", "blocks_complete_adjudication": False, "evidence": task_evidence, "rationale": why} for k, why in [
                  ("TASK_GAP", "Required facts are established by task prescriptions and eligible native contracts. Choosing a new explicit API, decorator representation or new tests/documentation is implementation work, not missing task information."),
                  ("REPOSITORY_INFORMATION_GAP", "The required native selection, identity/containment, snapshot, plan, realization, assembly and protected-validation facts have complete alternatives inside the frozen frame. No unprovided operational experiment is needed."),
                  ("TASK_INTERPRETATION_GAP", "The clause-by-clause audit maps every mandatory feature/validation requirement to the frozen obligations without widening an unrelated obligation.")]],
              "limitations": limitations,
              "ambiguity": {"status": "BOUNDED_DESIGN_AMBIGUITY_ONLY", "limitation_ids": ["L01", "L02", "L03", "L04"], "unresolved_cells": [], "unresolved_units": [], "unresolved_obligations": [], "rationale": "The limitations preserve genuine design/status boundaries but no resource necessity judgment remains unresolved."},
              "self_review": [
                  "Removed tentative necessity based only on named edit locations: existing facade initializers and the two documentation files are helpful context, while their mandatory destinations and future content are task-backed.",
                  "Kept exact source identity and native field/range facts repository-backed; task language about the new behavior was not used to assert that it already exists.",
                  "Did not require old test files merely because new focused/regression tests are requested. Retained actual pytest/coverage configuration as the required test convention; existing tests remain helpful examples.",
                  "Separated function, class and parent-relative method provenance into distinct units, while keeping each coherent native identity basis together.",
                  "Added complete source-code/package-contract alternatives. On a second minimality audit, demoted the grounding consumer and containment-helper implementations: native class/method membership and parent information already support the required validation inference, so adding those examples was redundant. Enumerated minimal covers rather than unioning all positive resources.",
                  "Demoted the existing UTF-8 extraction helper from an additional requirement: it supports a coordinate unit already supplied by the unavoidable function model in every complete materialization alternative.",
                  "Demoted the named validation script's implementation from additional necessity because the complete documented profile supplies its command, scope, configuration retention and exit behavior; actual project settings remain necessary.",
                  "Rejected the tempting assumption that native spans include decorators, and the stronger assumption that a containment validator authenticates arbitrary constructed fields. Recorded bounded limitations and sufficient retained-source validation routes.",
                  "Audited task-only export/documentation alternatives explicitly: these obligations prescribe future destinations and semantics without requiring extra discovery of repository state. Current source contracts are still required for the complete task under other obligations.",
                  "Kept cross-obligation reuse and recomputed indispensability from complete alternative combinations; REQUIRED union membership is not simultaneous task necessity."
              ],
              "blindness_attestation": {k: "NO" for k in blindness_keys},
              "blindness_scope_note": "NO denotes access to excluded external/case-experimental artifacts. Natural identifiers, source code, documentation and test text embedded in the original eligible resources were treated only as repository evidence, as the packet permits. No referenced paths were followed outside the packet. No retrieval/effectiveness analysis was performed.",
              "inspection_method": "Decoded/authenticated all 531 complete retained texts, inspected structural inventories across the frame and read exact bodies/sections for native contracts, relevant consumers, corroborating tests and documentation. All 4,779 cells were retained; semantic unit support, not lexical matches or edit proximity, determines REQUIRED.",
              "granularity_audit": "Units describe semantic contracts or task prescriptions, not reading tasks. Native function/class/method identity facts are separated; plan admission and plan identity, item shape and source coordinates, rendering and request copying are separated. Shared facts retain one unit identity across obligations. Test groups describe separable observable requirements; none is a file-per-unit decomposition."}
    review["combinatorics"] = calculate(review)
    return review


def intersection(sets):
    sets = list(sets)
    return sorted(set.intersection(*(set(s) for s in sets))) if sets else []


def calculate(review):
    by_obligation = {k: [a for a in review["alternatives"] if a["obligation"] == k] for k in KEYS}
    combinations = []
    # An empty resource witness is a real alternative; absence of an alternative
    # is a different state and yields no complete task combinations.
    products = itertools.product(*(by_obligation[k] for k in KEYS))
    for i, chosen in enumerate(products, 1):
        combinations.append({"id": "TC%04d" % i, "alternatives": [a["id"] for a in chosen],
                             "resources": sorted({r for a in chosen for r in a["resources"]}),
                             "units": sorted({u for a in chosen for u in a["units"]})})
    def unions(field, prefix):
        grouped = {}
        for c in combinations:
            grouped.setdefault(tuple(c[field]), []).append(c["id"])
        return [{"id": prefix + "%03d" % (i+1), field: list(values), "combinations": grouped[values]}
                for i, values in enumerate(sorted(grouped, key=lambda s: (len(s), s)))]
    ru, uu = unions("resources", "RU"), unions("units", "UU")
    return {"complete_task_combinations": combinations, "sufficient_resource_unions": ru, "sufficient_unit_unions": uu,
            "complete_task_combination_count": len(combinations), "distinct_sufficient_resource_union_count": len(ru), "distinct_sufficient_unit_union_count": len(uu),
            "minimum_sufficient_resource_count": min((len(c["resources"]) for c in combinations), default=None),
            "maximum_sufficient_resource_count": max((len(c["resources"]) for c in combinations), default=None),
            "minimum_sufficient_unit_count": min((len(c["units"]) for c in combinations), default=None),
            "maximum_sufficient_unit_count": max((len(c["units"]) for c in combinations), default=None),
            "obligation_indispensable": {k: {"resources": intersection(a["resources"] for a in by_obligation[k]), "units": intersection(a["units"] for a in by_obligation[k]), "complete_alternative_exists": bool(by_obligation[k])} for k in KEYS},
            "task_indispensable": {"resources": intersection(c["resources"] for c in combinations), "units": intersection(c["units"] for c in combinations), "complete_combination_exists": bool(combinations)},
            "sufficiency_scope": "Inclusion-minimal complete obligation evidence alternatives, combined by Cartesian product with cross-obligation reuse. Sufficient unions are unions of those complete alternatives, not all arbitrary supersets of adequate evidence. Counts describe necessary information, not implementation execution or measured effectiveness."}


def validate_review(review, p):
    require(review["case"] == p["case"] == CASE and review["task_identity"] == p["task_identity"] == TASK, "case/task identity")
    require(review["task_text"] == p["task_text"] and review["frame"] == p["frame"], "task/frame binding")
    require(review["input_seals"] == SEALS and review["obligations"] == p["obligations"], "obligation/seal binding")
    require(len(review["resources"]) == 531, "resource count")
    resource_map = {r["index"]: r for r in review["resources"]}
    require(set(resource_map) == set(range(531)), "resource index frame")
    for i, native in enumerate(p["resources"]):
        require({k: resource_map[i][k] for k in native if k != "text"} == {k: v for k, v in native.items() if k != "text"}, "resource identity binding")
        require(resource_map[i]["text_sha256"] == sha(native["text"].encode("utf-8")), "resource text digest binding")
    require([a["obligation"] for a in review["applicability"]] == list(KEYS), "applicability frame")
    require(all(a["status"] == "APPLICABLE" and a["rationale"] for a in review["applicability"]), "applicability disposition")
    evidence = {e["id"]: e for e in review["evidence"]}
    require(len(evidence) == len(review["evidence"]), "duplicate evidence identity")
    for e in evidence.values():
        i = e["resource_index"]
        if i is None:
            require(e["origin"] == "TASK" and e["resource_identity"] is None and e["resource_address"] is None and e["content_identity"] is None, "task evidence identity")
            text = p["task_text"]
        else:
            require(i in resource_map and e["origin"] == "REPOSITORY", "support resource identity")
            r = p["resources"][i]
            require((e["resource_identity"], e["resource_address"], e["content_identity"]) == (r["document_identity"], r["address"], r["content_identity"]), "support identity binding")
            text = r["text"]
        require(type(e["start"]) is int and type(e["end"]) is int and 0 <= e["start"] < e["end"] <= len(text), "support span bounds")
        require(text[e["start"]:e["end"]] == e["text"], "exact support span")
        require(e["start_line"] == text.count("\n", 0, e["start"]) + 1 and e["end_line"] == text.count("\n", 0, e["end"] - 1) + 1, "support line bounds")
        require(e["coordinate_system"] == "Unicode code points; zero-based; half-open" and e["provenance"], "support provenance/coordinates")
    units = {u["id"]: u for u in review["units"]}
    require(len(units) == len(review["units"]) and all(units), "unique semantic units")
    for u in units.values():
        require(u["status"] == "REQUIRED" and u["statement"] and u["scope"] and u["necessity_rationale"] and u["provenance"], "unit schema")
        require(u["obligations"] and len(set(u["obligations"])) == len(u["obligations"]) and set(u["obligations"]) <= set(KEYS), "unit obligation membership")
        require(u["support_bundles"], "required unit lacks support")
        for b in u["support_bundles"]:
            require(b["evidence"] and all(e in evidence for e in b["evidence"]), "unit evidence membership")
            expected_resources = sorted({evidence[e]["resource_index"] for e in b["evidence"] if evidence[e]["resource_index"] is not None})
            require(b["resources"] == expected_resources, "unit resource support binding")
            require(b["support_mode"] in {"DIRECT", "INFERABLE", "TASK_BACKED"} and b["inferability_rationale"], "unit inferability")
            require((b["support_mode"] == "TASK_BACKED") == (not b["resources"]), "task/repository support distinction")
    alternatives = {a["id"]: a for a in review["alternatives"]}
    require(len(alternatives) == len(review["alternatives"]), "unique alternatives")
    for a in alternatives.values():
        key = a["obligation"]
        require(key in KEYS and a["id"].startswith(key + "-A"), "alternative obligation")
        required_units = [u["id"] for u in units.values() if key in u["obligations"]]
        require(a["units"] == required_units, "alternative unit membership/completeness")
        require(a["resources"] == sorted(set(a["resources"])) and set(a["resources"]) <= set(resource_map), "alternative resource membership")
        expected_task_units = [uid for uid in required_units if any(not b["resources"] for b in units[uid]["support_bundles"])]
        require(a["task_backed_units"] == expected_task_units, "alternative task-backed membership")
        require([s["unit"] for s in a["support_relationships"]] == required_units, "alternative support completeness")
        for s in a["support_relationships"]:
            require(type(s["support_bundle"]) is int and 0 <= s["support_bundle"] < len(units[s["unit"]]["support_bundles"]), "alternative bundle membership")
            require(set(units[s["unit"]]["support_bundles"][s["support_bundle"]]["resources"]) <= set(a["resources"]), "alternative incomplete support")
        expected_witnesses = {}
        for r in a["resources"]:
            missing = [uid for uid in required_units if not any(set(b["resources"]) <= set(a["resources"]) - {r} for b in units[uid]["support_bundles"])]
            require(missing, "redundant alternative resource")
            expected_witnesses[str(r)] = missing
        require(a["removal_witnesses"] == expected_witnesses, "minimality removal witnesses")
        require(a["completeness_rationale"] and a["minimality_rationale"] and a["inferability_assumptions"], "alternative rationales")
    for key in KEYS:
        covers = [frozenset()]
        for u in units.values():
            if key in u["obligations"]:
                covers = minimal_sets(c | frozenset(b["resources"]) for c in covers for b in u["support_bundles"])
        actual = [frozenset(a["resources"]) for a in alternatives.values() if a["obligation"] == key]
        require(len(actual) == len(set(actual)) and set(actual) == set(covers), "missing/duplicate/nonminimal alternative")
    expected_cells = {(r, key) for r in range(531) for key in KEYS}
    actual_cells = [(c["resource_index"], c["obligation"]) for c in review["cells"]]
    require(len(actual_cells) == 4779 and len(set(actual_cells)) == 4779 and set(actual_cells) == expected_cells, "missing/duplicate/unexpected cell")
    for c in review["cells"]:
        r = resource_map[c["resource_index"]]
        require(c["resource_identity"] == r["document_identity"] and c["resource_address"] == r["address"] and c["obligation_identity"] == TASK + "/" + c["obligation"], "cell identity binding")
        require(c["label"] in LABELS and c["rationale"] and c["inferability_rationale"] and c["provenance"], "cell label/rationale schema")
        member = any(a["obligation"] == c["obligation"] and c["resource_index"] in a["resources"] for a in alternatives.values())
        require((c["label"] == "REQUIRED") == member, "REQUIRED/alternative equivalence")
        require(all(e in evidence and evidence[e]["resource_index"] == c["resource_index"] for e in c["evidence"]), "cell evidence resource binding")
        require(set(c["unit_bindings"]) <= set(units), "cell unit membership")
        if c["label"] in {"REQUIRED", "HELPFUL_ONLY", "UNRESOLVED"}:
            require(c["evidence"], "positive/nontrivial cell evidence")
        if c["label"] == "REQUIRED":
            require(c["unit_bindings"], "required cell unit binding")
            for uid in c["unit_bindings"]:
                require(c["obligation"] in units[uid]["obligations"] and any(c["resource_index"] in b["resources"] for b in units[uid]["support_bundles"]), "required unit/resource relationship")
    require(review["combinatorics"] == calculate(review), "sufficient combinations/unions/intersections")
    require(len(review["task_interpretation_audit"]) == 10, "task clause frame")
    require("".join(c["exact_text"] for c in review["task_interpretation_audit"]) == p["task_text"], "complete exact task audit")
    for c in review["task_interpretation_audit"]:
        require(c["task_evidence"] in evidence and evidence[c["task_evidence"]]["origin"] == "TASK" and evidence[c["task_evidence"]]["text"] == c["exact_text"], "task audit support")
        require(c["requirements"] and set(c["obligations"]) <= set(KEYS), "clause coverage")
        for q in c["requirements"]:
            require(q["statement"] and q["rationale"] and q["coverage"] == "ADEQUATELY_COVERED" and q["obligations"] == c["obligations"], "subclause coverage schema")
    require({g["kind"] for g in review["gap_assessments"]} == {"TASK_GAP", "REPOSITORY_INFORMATION_GAP", "TASK_INTERPRETATION_GAP"}, "gap frame")
    for g in review["gap_assessments"]:
        require(g["status"] == "NONE" and type(g["blocks_complete_adjudication"]) is bool and not g["blocks_complete_adjudication"] and g["rationale"] and all(e in evidence for e in g["evidence"]), "gap schema")
    require(len({l["id"] for l in review["limitations"]}) == len(review["limitations"]), "limitation identity")
    for l in review["limitations"]:
        require(l["category"] and l["statement"] and l["rationale"] and type(l["blocks_complete_adjudication"]) is bool and l["evidence"] and all(e in evidence for e in l["evidence"]), "limitation schema")
    amb = review["ambiguity"]
    require(amb["status"] == "BOUNDED_DESIGN_AMBIGUITY_ONLY" and set(amb["limitation_ids"]) <= {l["id"] for l in review["limitations"]}, "ambiguity schema")
    require(amb["unresolved_cells"] == [c for c in review["cells"] if c["label"] == "UNRESOLVED"] == [] and amb["unresolved_units"] == [] and amb["unresolved_obligations"] == [] and amb["rationale"], "unresolved state")
    require(len(review["blindness_attestation"]) == 21 and set(review["blindness_attestation"].values()) == {"NO"}, "blindness attestation")


def statistics(review):
    counts = {label: sum(c["label"] == label for c in review["cells"]) for label in LABELS}
    per_obligation = {key: {label: sum(c["obligation"] == key and c["label"] == label for c in review["cells"]) for label in LABELS} for key in KEYS}
    required = sorted({c["resource_index"] for c in review["cells"] if c["label"] == "REQUIRED"})
    math = review["combinatorics"]
    return {"schema": "case-0012-independent-c-r-statistics-v1", "case": review["case"], "task_identity": review["task_identity"], "resource_count": len(review["resources"]), "obligation_count": len(review["obligations"]), "applicable_obligation_count": len(KEYS),
            "cell_count": len(review["cells"]), "label_counts": counts, "cell_counts_by_obligation": per_obligation,
            "required_unit_count": len(review["units"]), "required_resource_union": required, "required_resource_union_count": len(required),
            "required_resource_addresses": [review["resources"][i]["address"] for i in required],
            "unit_counts_by_obligation": {k: sum(k in u["obligations"] for u in review["units"]) for k in KEYS},
            "alternative_counts_by_obligation": {k: sum(a["obligation"] == k for a in review["alternatives"]) for k in KEYS},
            "task_clause_count": len(review["task_interpretation_audit"]), "substantive_requirement_count": sum(len(c["requirements"]) for c in review["task_interpretation_audit"]),
            **{k: v for k, v in math.items() if k not in {"complete_task_combinations", "sufficient_resource_unions", "sufficient_unit_unions", "sufficiency_scope"}},
            "gap_counts": {g["kind"]: 0 if g["status"] == "NONE" else 1 for g in review["gap_assessments"]}, "limitation_count": len(review["limitations"]), "unresolved_cell_count": counts["UNRESOLVED"],
            "task_backed_only_obligations": [k for k in KEYS if any(a["obligation"] == k and not a["resources"] for a in review["alternatives"])],
            "task_backed_unit_count": sum(any(not b["resources"] for b in u["support_bundles"]) for u in review["units"])}


def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def rid(i):
    return "R%03d" % i


def render_markdown(review, stats):
    out = ["# Independent C-R semantic adjudication — Case 0012", "", "This is a task/repository-information adjudication over the supplied sealed packet. It does not implement the feature or execute repository validation commands. Scientific resource IDs below are packet-order aliases; exact native identities and addresses remain bound in JSON.", "", "## Packet authentication", "", "Initial workspace: exact five-file whitelist; no directories, .git, .local, symlinks, junctions or reparse points. `python -B validate_packet.py` exited 0 with `VERIFIED; NO ADJUDICATION`. All five original input byte seals are retained in the review and rechecked on replay.", "", "Case: `" + CASE + "`; task: `" + TASK + "`.", "", "| Input | SHA-256 |", "|---|---|"]
    out.extend("| " + n + " | `" + h + "` |" for n, h in sorted(SEALS.items()))
    out.extend(["", "Canonical payload SHA-256: `c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce`.", "", "## Exact task", "", "```text", review["task_text"].rstrip("\n"), "```", "", "## Frozen obligations and applicability", "", "| Obligation | Applicability | Exact statement | Exact satisfaction criterion |", "|---|---|---|---|"])
    for o in review["obligations"]:
        out.append("| " + o["key"] + " | APPLICABLE | " + md_escape(o["statement"]) + " | " + md_escape(o["criterion"]) + " |")
    out.extend(["", "All nine clauses are mandatory and unconditional. The exact frozen applicability text, identities and task-basis offsets are preserved in JSON.", "", "## Task-clause coverage", "", review["interpretation_note"], "", "| Clause | Obligations | Substantive requirements, each adequately covered | Evidence |", "|---|---|---|---|"])
    for c in review["task_interpretation_audit"]:
        out.append("| " + c["id"] + " | " + ", ".join(c["obligations"]) + " | " + md_escape("; ".join(q["statement"] for q in c["requirements"])) + " | " + c["task_evidence"] + " |")
    out.extend(["", "## Complete cell counts", "", "Exactly 531 × 9 = 4,779 cells; no omissions or duplicates. Every cell, including UNNECESSARY cells, has an obligation-relative semantic rationale in JSON.", "", "| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY | UNRESOLVED |", "|---|---:|---:|---:|---:|"])
    for key in KEYS:
        out.append("| " + key + " | " + " | ".join(str(stats["cell_counts_by_obligation"][key][label]) for label in LABELS) + " |")
    out.append("| **Total** | " + " | ".join(str(stats["label_counts"][label]) for label in LABELS) + " |")
    for key in KEYS:
        out.extend(["", "## Positive resources: " + key, "", "| Resource | Label | Address | Units | Exact support | Rationale |", "|---|---|---|---|---|---|"])
        rows = [c for c in review["cells"] if c["obligation"] == key and c["label"] in {"REQUIRED", "HELPFUL_ONLY", "UNRESOLVED"}]
        for c in rows:
            out.append("| " + rid(c["resource_index"]) + " | " + c["label"] + " | " + c["resource_address"] + " | " + ", ".join(c["unit_bindings"]) + " | " + ", ".join(c["evidence"]) + " | " + md_escape(c["rationale"]) + " |")
        if not rows:
            out.append("| — | — | No repository-positive cells | — | — | Task-backed prescription suffices |")
    out.extend(["", "## Complete REQUIRED resource union", "", str(stats["required_resource_union_count"]) + " resources occur in at least one minimal acceptable obligation alternative. This union is not a simultaneous task witness.", "", "| Alias | Address | Native document identity |", "|---|---|---|"])
    for i in stats["required_resource_union"]:
        r = review["resources"][i]
        out.append("| " + rid(i) + " | " + r["address"] + " | `" + r["document_identity"] + "` |")
    out.extend(["", "## Complete semantic-unit inventory", "", review["granularity_audit"], ""])
    for u in review["units"]:
        out.extend(["### " + u["id"] + " — " + ", ".join(u["obligations"]), "", u["statement"], "", "Scope: " + u["scope"] + ". Necessity: " + u["necessity_rationale"], ""])
        for i, b in enumerate(u["support_bundles"]):
            out.append("- Support bundle " + str(i) + " (" + b["support_mode"] + "): " + ", ".join(b["evidence"]) + "; resources: " + (", ".join(rid(r) for r in b["resources"]) or "none; task-backed") + ". " + b["inferability_rationale"])
        out.append("")
    out.extend(["## All minimal acceptable alternatives", "", "ALL members within a row are jointly required; ANY complete row for that obligation suffices. Required units are fixed semantic targets; differing rows substitute complete repository evidence. Empty resource rows rely solely on authoritative task prescriptions. Proof-bundle choices and resource-removal witnesses are retained in JSON.", "", "| Alternative | Obligation | Required resources | Required units | Task-backed units |", "|---|---|---|---|---|"])
    for a in review["alternatives"]:
        out.append("| " + a["id"] + " | " + a["obligation"] + " | " + (", ".join(rid(i) for i in a["resources"]) or "∅") + " | " + ", ".join(a["units"]) + " | " + ", ".join(a["task_backed_units"]) + " |")
    out.extend(["", "## Complete task combinations", "", review["combinatorics"]["sufficiency_scope"], "", "| Combination | Alternatives, one per obligation | Resource union | Unit union |", "|---|---|---|---|"])
    for c in review["combinatorics"]["complete_task_combinations"]:
        out.append("| " + c["id"] + " | " + ", ".join(c["alternatives"]) + " | " + ", ".join(rid(i) for i in c["resources"]) + " | " + ", ".join(c["units"]) + " |")
    out.extend(["", "## Distinct sufficient unions and ranges", "", "Combinations: **%d**. Distinct resource unions: **%d**. Distinct unit unions: **%d**. Sufficient resource count: **%d–%d**. Sufficient unit count: **%d–%d**." % tuple(stats[k] for k in ("complete_task_combination_count", "distinct_sufficient_resource_union_count", "distinct_sufficient_unit_union_count", "minimum_sufficient_resource_count", "maximum_sufficient_resource_count", "minimum_sufficient_unit_count", "maximum_sufficient_unit_count")), "", "| Resource-union ID | Exact members | Combinations |", "|---|---|---|"])
    for u in review["combinatorics"]["sufficient_resource_unions"]:
        out.append("| " + u["id"] + " | " + ", ".join(rid(i) for i in u["resources"]) + " | " + ", ".join(u["combinations"]) + " |")
    out.extend(["", "| Unit-union ID | Exact members | Combinations |", "|---|---|---|"])
    for u in review["combinatorics"]["sufficient_unit_unions"]:
        out.append("| " + u["id"] + " | " + ", ".join(u["units"]) + " | " + ", ".join(u["combinations"]) + " |")
    out.extend(["", "## Indispensability", "", "| Obligation | Resource intersection | Unit intersection |", "|---|---|---|"])
    for key, v in stats["obligation_indispensable"].items():
        out.append("| " + key + " | " + (", ".join(rid(i) for i in v["resources"]) or "∅") + " | " + ", ".join(v["units"]) + " |")
    out.extend(["", "Task-indispensable resources: " + ", ".join(rid(i) for i in stats["task_indispensable"]["resources"]) + ".", "", "Task-indispensable units: " + ", ".join(stats["task_indispensable"]["units"]) + ".", "", "## Gaps", ""])
    for g in review["gap_assessments"]:
        out.append("- " + g["kind"] + ": **" + g["status"] + "**. " + g["rationale"] + " No complete-adjudication block.")
    out.extend(["", "## Interpretation limitations and ambiguity", ""])
    for l in review["limitations"]:
        out.extend(["### " + l["id"] + " — " + l["category"], "", l["statement"], "", l["rationale"] + " Evidence: " + ", ".join(l["evidence"]) + ". Blocks complete adjudication: NO.", ""])
    out.extend(["Ambiguity state: " + review["ambiguity"]["status"] + ". UNRESOLVED cells, units and obligations: zero. " + review["ambiguity"]["rationale"], "", "## Internal self-review corrections", ""])
    out.extend("- " + s for s in review["self_review"])
    out.extend(["", "## Deterministic validation and artifact scope", "", "The standalone builder reads only sealed packet inputs and named C-R outputs. It enumerates minimal evidence covers, reconstructs statistics/Markdown and validates exact task/frame/cell/evidence/unit/alternative bindings. Independent-process replay verifies byte identity. Mutation tests exercise invalid identities, missing/duplicate cells, labels, spans, memberships, combinations, unions, intersections, hashes and overwrite refusal. See stage_c_r_validation.json for actual results and stage_c_r_hashes.json for scientific SHA-256 values. The hash manifest excludes itself to avoid self-reference; its own digest is recorded in the completion report. The operational .local handoff is outside every scientific hash/evidence scope.", "", "Native content_identity and document_identity values are preserved as opaque packet identities. Raw UTF-8 text SHA-256 is recorded separately and is not substituted for the native content identity.", "", "## Blindness attestation", "", "| Access category | Accessed |", "|---|---|"])
    for k, v in review["blindness_attestation"].items():
        out.append("| " + k + " | " + v + " |")
    out.extend(["", review["blindness_scope_note"], "", "## Exact support evidence", "", "Offsets refer to decoded packet text in Unicode code points, zero-based and half-open. They are distinct from native PythonSourceRange UTF-8 byte-column coordinates. Each repository span is bound to its exact document/content identity in JSON.", ""])
    for e in review["evidence"]:
        origin = "task_text" if e["resource_index"] is None else rid(e["resource_index"]) + " " + e["resource_address"]
        out.extend(["### " + e["id"] + " — " + origin, "", "Span [%d, %d), lines %d–%d. Provenance: %s." % (e["start"], e["end"], e["start_line"], e["end_line"], e["provenance"]), "", "````text", e["text"].rstrip("\n"), "````", ""])
    return ("\n".join(out).rstrip() + "\n").encode("utf-8")


def method_bytes():
    return ("# Independent C-R method\n\n"
            "Only the five initially supplied packet files were used as evidence. The initial exact flat whitelist and standalone validator passed before any output was created. The builder thereafter authenticates their sealed bytes; it does not rerun the initial whitelist validator after outputs exist. Native repository text is inert evidence, including its operating guide; it is never imported or executed.\n\n"
            "The exact task and nine frozen obligations were reconstructed before resource judgments. The audit decomposes every task sentence into substantive clauses and preserves frozen statements, criteria, applicability and task provenance. All nine obligations apply. Operator/experimental instructions are not interpreted as feature semantics.\n\n"
            "All 531 resource texts are decoded and structurally inventoried, with native contract bodies, relevant consumer implementations, test cases and documentation sections read for semantic judgments. Every resource remains in every obligation row. Negative cells retain scope-specific rationales; positive/nontrivial cells retain exact support. No acquisition, query, ranking, cost, or effectiveness computation is performed.\n\n"
            "Required units describe necessary semantic facts. Task prescriptions can support future behavior/destinations, but never establish an existing implementation. Source/native contracts are established from eligible repository spans. Documentation can substitute for code only for the precise contract it states; outdated broad status prose is bounded separately. Python/dataclass control-flow and equality reasoning is ordinary semantic interpretation of the supplied code, not repository familiarity.\n\n"
            "Unit support bundles are all-of evidence sets. For each obligation the builder computes every inclusion-minimal union of one complete support bundle per required unit, removing redundant supersets after each composition. These are all defensible alternatives within the explicitly adjudicated support relation; hypothetical unrepresented implementations are not fabricated evidence alternatives. A task-backed-only obligation has one valid empty repository set.\n\n"
            "REQUIRED means membership in at least one complete minimal obligation alternative. HELPFUL_ONLY means precise corroboration, a partial example or edit context that contributes no indispensable member to a complete minimal alternative. UNNECESSARY denotes no additional necessary or materially useful obligation-specific information. UNRESOLVED is available but no final cell needs it. Information sufficiency is distinct from execution and implementation correctness.\n\n"
            "The task combinations choose exactly one alternative per applicable obligation. Resources and semantic units are deduplicated across obligations. Distinct sufficient unions and resource/unit intersections are computed from those combinations; arbitrary extra-resource supersets are outside these sufficiency counts. The REQUIRED resource union is never treated as simultaneous necessity.\n\n"
            "Self-review challenged named-target inflation, tests-as-necessity, redundant code/documentation support, task-versus-repository confusion, missing complete alternatives, decorator ranges, partial native validation, granularity and union/intersection mistakes. Corrections are retained in the review. No prior review or external comparison informed this work.\n\n"
            "Replay is standalone Python stdlib, using -B to avoid bytecode directories. AST parsing inspects text without executing repository modules. The original packet content/document identities remain opaque and authenticated through the sealed payload; raw text SHA-256 has its own explicit field. Evidence spans are zero-based half-open Unicode code-point offsets, with exact substrings and line bounds; native Python source coordinates are separately documented UTF-8 byte offsets.\n\n"
            "Build mode refuses all existing scientific output destinations. Verification reconstructs review, statistics, Markdown, method and validation records in a separate process and compares exact bytes, then authenticates the scientific hash manifest. In-memory adversarial mutations must fail structural/semantic-binding validation. The manifest covers the builder and generated scientific artifacts, excluding itself to avoid circular hashing; its SHA-256 is reported externally. The operational .local/codex-result.md is created only after frozen validation, original-byte preservation and blindness attestation, and is excluded from all scientific scopes.\n").encode("utf-8")


def exclusive_write(name, data):
    require(name in OUTPUTS, "output whitelist")
    with (ROOT / name).open("xb") as f:
        f.write(data)


def check_hashes(manifest):
    require(manifest["schema"] == "case-0012-independent-c-r-hashes-v1", "hash manifest schema")
    require(manifest["input_sha256"] == SEALS, "hash input seals")
    names = set(OUTPUTS) - {"stage_c_r_hashes.json"} | {BUILDER}
    require(set(manifest["scientific_sha256"]) == names, "hash output frame")
    for name, digest in manifest["scientific_sha256"].items():
        require(sha((ROOT / name).read_bytes()) == digest, "scientific hash: " + name)


def mutation_tests(review, p, hashes=None):
    results = []
    def reject(name, mutate):
        changed = copy.deepcopy(review)
        mutate(changed)
        try:
            validate_review(changed, p)
        except (ValueError, KeyError, IndexError, TypeError, StopIteration):
            results.append({"test": name, "result": "REJECTED"})
        else:
            raise ValueError("mutation was accepted: " + name)
    reject("altered_cell_identity", lambda r: r["cells"][0].update(resource_identity="0" * 64))
    reject("missing_cell", lambda r: r["cells"].pop())
    reject("duplicate_cell", lambda r: r["cells"].__setitem__(-1, copy.deepcopy(r["cells"][0])))
    reject("invalid_label", lambda r: r["cells"][0].update(label="USEFUL"))
    reject("out_of_bounds_support_span", lambda r: r["evidence"][0].update(end=10**12))
    reject("in_bounds_altered_support_text", lambda r: r["evidence"][0].update(text="altered"))
    reject("invalid_unit_membership", lambda r: r["alternatives"][0]["units"].append("NONEXISTENT"))
    reject("invalid_alternative_resource_membership", lambda r: r["alternatives"][0]["resources"].append(9999))
    reject("invalid_alternative_obligation_membership", lambda r: r["alternatives"][0].update(obligation="assembly"))
    reject("invalid_sufficient_combination", lambda r: r["combinatorics"]["complete_task_combinations"][0]["alternatives"].pop())
    reject("invalid_sufficient_resource_union", lambda r: r["combinatorics"]["sufficient_resource_unions"][0]["resources"].append(9999))
    reject("invalid_sufficient_unit_union", lambda r: r["combinatorics"]["sufficient_unit_unions"][0]["units"].append("NONEXISTENT"))
    reject("invalid_indispensable_intersection", lambda r: r["combinatorics"]["task_indispensable"]["resources"].append(9999))
    reject("required_unit_without_support", lambda r: r["units"][0].update(support_bundles=[]))
    reject("altered_task_identity", lambda r: r.update(task_identity="other-task"))
    reject("altered_obligation_criterion", lambda r: r["obligations"][0].update(criterion="different"))
    reject("altered_resource_frame", lambda r: r["resources"][0].update(address="other-resource"))
    reject("missing_complete_alternative", lambda r: r["alternatives"].pop(0))
    reject("invalid_gap_schema", lambda r: r["gap_assessments"][0].update(blocks_complete_adjudication="no"))
    reject("invalid_ambiguity_schema", lambda r: r["ambiguity"].update(unresolved_units=["NONEXISTENT"]))
    # Pure-byte checks test deterministic derivative and hash enforcement.
    expected_stats = statistics(review)
    altered_stats = copy.deepcopy(expected_stats)
    altered_stats["cell_count"] -= 1
    markdown = render_markdown(review, expected_stats)
    for name, changed, expected in [("altered_statistics_bytes", jb(altered_stats), jb(expected_stats)), ("altered_markdown_bytes", markdown + b"altered\n", markdown)]:
        try:
            check_reconstructed_bytes(changed, expected, name)
        except ValueError:
            results.append({"test": name, "result": "REJECTED"})
        else:
            raise ValueError("derivative mutation accepted: " + name)
    if hashes is None:
        # The same digest-equality predicate used by check_hashes, before a
        # manifest exists. --verify also mutates and tests the actual manifest.
        require(sha(jb(review)) != "0" * 64, "hash mutation detection")
    else:
        bad = copy.deepcopy(hashes)
        bad["scientific_sha256"]["stage_c_r_review.json"] = "0" * 64
        try:
            check_hashes(bad)
        except ValueError:
            pass
        else:
            raise ValueError("invalid hash accepted")
    results.append({"test": "invalid_scientific_hash", "result": "REJECTED"})
    before = (ROOT / "stage_c_r_review.json").read_bytes()
    try:
        exclusive_write("stage_c_r_review.json", b"must never be written")
    except FileExistsError:
        require((ROOT / "stage_c_r_review.json").read_bytes() == before, "overwrite altered bytes")
    else:
        raise ValueError("overwrite not refused")
    results.append({"test": "scientific_output_overwrite", "result": "REJECTED"})
    return results


def core_products(p):
    review = construct_review(p)
    validate_review(review, p)
    stats = statistics(review)
    return review, {
        "stage_c_r_review.json": jb(review),
        "stage_c_r_statistics.json": jb(stats),
        "STAGE_C_R_REVIEW.md": render_markdown(review, stats),
        "stage_c_r_method.md": method_bytes(),
    }


def compare_core(products):
    for name, expected in products.items():
        check_reconstructed_bytes((ROOT / name).read_bytes(), expected, name)


def check_reconstructed_bytes(actual, expected, name):
    require(actual == expected, "deterministic byte replay: " + name)


def validation_record(review, mutations):
    return {"schema": "case-0012-independent-c-r-validation-v1", "case": CASE, "task_identity": TASK, "status": "PASS",
            "initial_exact_five_file_whitelist": "PASS", "initial_standalone_packet_validator": "PASS; exit 0; VERIFIED; NO ADJUDICATION",
            "packet_input_digests_and_canonical_payload": "PASS", "original_five_input_bytes_preserved": True,
            "resource_count": 531, "obligation_count": 9, "cell_count": 4779,
            "checks": {k: "PASS" for k in ["case_task_frame_binding", "exact_obligation_statements_criteria_applicability_basis", "exact_531_resource_identities", "all_4779_cells_no_missing_no_duplicate", "label_vocabulary", "support_resource_identities", "exact_span_text_bounds_and_line_coordinates", "unique_required_units_with_support_and_inferability", "task_vs_repository_evidence_separation", "alternative_single_obligation_membership", "alternative_completeness_and_resource_removal_minimality", "all_minimal_evidence_alternatives_enumerated", "complete_cartesian_task_combinations", "distinct_sufficient_resource_and_unit_unions", "cross_obligation_reuse", "obligation_and_task_indispensable_intersections", "gap_limitation_and_ambiguity_schemas", "task_clause_coverage", "deterministic_statistics_reconstruction", "deterministic_markdown_reconstruction", "input_byte_preservation", "all_NO_blindness_attestation"]},
            "independent_process_replay": {"invocation": "python -B stage_c_r_builder.py --replay-core", "status": "PASS", "byte_identical": ["stage_c_r_review.json", "stage_c_r_statistics.json", "STAGE_C_R_REVIEW.md", "stage_c_r_method.md"], "reconstruction_destination": "memory in a fresh process; no temporary directories/files"},
            "full_verification_invocation": "python -B stage_c_r_builder.py --verify",
            "scientific_hash_verification": "All scientific artifacts except the non-self-hashing manifest are authenticated by stage_c_r_hashes.json; full --verify checks its exact deterministic bytes and all named digests.",
            "mutation_test_count": len(mutations), "mutation_tests": mutations,
            "scientific_output_overwrite_refused": True,
            "operational_handoff": "Excluded from scientific hashes, evidence, adjudication and gaps; may be created only after full verification and input-byte preservation.",
            "semantic_validation_limit": "Deterministic validation checks the sealed authored judgments, support bindings and exact algebra. It does not claim that arithmetic alone proves a semantic judgment; the independent evidence/rationales and internal critique remain inspectable."}


def verify():
    p = packet()
    review, products = core_products(p)
    compare_core(products)
    manifest = json.loads((ROOT / "stage_c_r_hashes.json").read_bytes())
    check_hashes(manifest)
    mutations = mutation_tests(review, p, manifest)
    require((ROOT / "stage_c_r_validation.json").read_bytes() == jb(validation_record(review, mutations)), "validation record byte replay")
    expected_manifest = {"schema": "case-0012-independent-c-r-hashes-v1", "case": CASE, "task_identity": TASK, "input_sha256": SEALS,
                         "scientific_sha256": {name: sha((ROOT / name).read_bytes()) for name in sorted(set(OUTPUTS) - {"stage_c_r_hashes.json"} | {BUILDER})},
                         "hash_scope": "Exact file bytes. The manifest excludes itself to avoid a circular digest; report its own SHA-256 externally. .local/codex-result.md is operational and excluded."}
    require((ROOT / "stage_c_r_hashes.json").read_bytes() == jb(expected_manifest), "hash manifest byte replay")
    packet()
    return {"status": "PASS", "separate_process_reconstruction": "exact bytes", "core_artifacts": len(products), "scientific_hashes_verified": len(manifest["scientific_sha256"]), "mutation_tests_rejected": len(mutations), "original_inputs_preserved": True,
            "hash_manifest_sha256": sha((ROOT / "stage_c_r_hashes.json").read_bytes()), "statistics": statistics(review)}


def build():
    require(not (ROOT / ".local").exists(), ".local must not exist before scientific freeze")
    require(not any((ROOT / name).exists() for name in OUTPUTS), "refuse to overwrite existing scientific outputs")
    p = packet()
    review, products = core_products(p)
    for name, data in products.items():
        exclusive_write(name, data)
    replay = subprocess.run([sys.executable, "-B", str(ROOT / BUILDER), "--replay-core"], cwd=ROOT, capture_output=True, text=True, check=False)
    require(replay.returncode == 0 and replay.stdout.strip() == "CORE_REPLAY_BYTE_IDENTICAL", "fresh-process core replay: " + replay.stderr)
    mutations = mutation_tests(review, p)
    exclusive_write("stage_c_r_validation.json", jb(validation_record(review, mutations)))
    manifest = {"schema": "case-0012-independent-c-r-hashes-v1", "case": CASE, "task_identity": TASK, "input_sha256": SEALS,
                "scientific_sha256": {name: sha((ROOT / name).read_bytes()) for name in sorted(set(OUTPUTS) - {"stage_c_r_hashes.json"} | {BUILDER})},
                "hash_scope": "Exact file bytes. The manifest excludes itself to avoid a circular digest; report its own SHA-256 externally. .local/codex-result.md is operational and excluded."}
    exclusive_write("stage_c_r_hashes.json", jb(manifest))
    packet()
    final = subprocess.run([sys.executable, "-B", str(ROOT / BUILDER), "--verify"], cwd=ROOT, capture_output=True, text=True, check=False)
    require(final.returncode == 0, "full independent-process verification: " + final.stderr)
    print(final.stdout.strip())


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1:] == ["--build"]:
        build()
    elif sys.argv[1:] == ["--verify"]:
        print(json.dumps(verify(), sort_keys=True, indent=2))
    elif sys.argv[1:] == ["--replay-core"]:
        _, products = core_products(packet())
        compare_core(products)
        print("CORE_REPLAY_BYTE_IDENTICAL")
    elif sys.argv[1:] == ["--inspect"]:
        p = packet()
        review, products = core_products(p)
        print(json.dumps(statistics(review), sort_keys=True, indent=2))
    else:
        raise SystemExit("Use --inspect (no writes), --build (exclusive writes), --verify, or --replay-core.")
