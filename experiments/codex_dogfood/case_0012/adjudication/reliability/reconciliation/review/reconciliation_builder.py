"""Deterministic Case 0012 reconciliation. Uses only sealed local packet inputs.

No embedded repository source is imported or executed. Build refuses overwrites.
Verify reconstructs the scientific artifacts in memory and compares exact bytes.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import itertools
import json
import re
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).absolute().parent
EXPECTED_ROOT = r"C:\Users\recoveryadmin\CodexSterile\case_0012_gold_reconciliation_34b81cc26248"
INPUT_HASHES = {
    "README.md": "68b12b7db474e2846b240cf78f75c9f57347b6665beeea5373b663848e644797",
    "manifest.json": "408c7e83c6e8455afb817767ad6b2b7848d699a73344d4c99e3ed42fe7056cd0",
    "packet.json.gz": "34b81cc262487fb8bc2a6a6bf795622575a15b8f7542f8cc6862cc4ebcb56522",
    "validate_packet.py": "f3968f8607aec79fd77e4c4e17def7bb71a0e4d9d7fc0c62ec3c548d294b442a",
    "integrity.json": "c8d9e602021a7667c3b0e066cf336caa76d52a24e47dc3936e00765d5c2da64a",
}
PAYLOAD_HASH = "c63885421eb93fc456ca136a1c54bd5a69ce99c6e1f92c473f1503ca28fe2e44"
OUTPUTS = ("reconciliation.json", "RECONCILIATION_REVIEW.md", "reconciliation_method.md", "reconciliation_validation.json", "reconciliation_hashes.json")
DECISIONS = {"REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "RECONCILED", "UNRESOLVED"}


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_packet():
    require(str(ROOT).casefold() == EXPECTED_ROOT.casefold(), "workspace identity")
    for name, digest in INPUT_HASHES.items():
        path = ROOT / name
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and not path.is_symlink() and not getattr(info, "st_file_attributes", 0) & 1024, "input link")
        require(sha(path.read_bytes()) == digest, "original packet bytes: " + name)
    require(not getattr(ROOT.lstat(), "st_file_attributes", 0) & 1024, "workspace reparse")
    raw = gzip.decompress((ROOT / "packet.json.gz").read_bytes())
    packet = json.loads(raw)
    require(raw == canonical(packet) and sha(raw) == PAYLOAD_HASH, "payload identity")
    manifest = json.loads((ROOT / "manifest.json").read_bytes())
    require(manifest["archive_sha256"] == INPUT_HASHES["packet.json.gz"], "archive scope")
    require(manifest["canonical_payload_sha256"] == PAYLOAD_HASH, "canonical scope")
    require(manifest["reviewer_whitelist"] == sorted(INPUT_HASHES), "initial whitelist metadata")
    require([q["identity"] for q in packet["propositions"]] == manifest["proposition_identities"], "packet roster")
    require(dict(Counter(q["type"] for q in packet["propositions"])) == manifest["proposition_counts"], "packet type counts")
    for q in packet["propositions"]:
        require(sha(canonical({k:v for k,v in q.items() if k != "identity"})) == q["identity"], "proposition digest")
    for r in packet["resources"]:
        require(sha(r["text"].encode()) == r["text_sha256"], "resource seal")
    return packet


P = load_packet()
RES = {r["address"]:r for r in P["resources"]}
OBS = {o["key"]:o for o in P["obligations"]}
F = "src/devtools/context/python/function/declarations.py"
C = "src/devtools/context/python/classes/declarations.py"
CD = "src/devtools/context/python/classes/docs/overview.md"
S = "src/devtools/context/python/modules/selection.py"
SD = "src/devtools/context/python/modules/docs/overview.md"
V = "src/devtools/context/python/classes/containment.py"
PLAN = "src/devtools/context/planning/plan.py"
MAT = "src/devtools/context/planning/materialization.py"
REN = "src/devtools/context/planning/rendering.py"
RESOURCE = "src/devtools/context/repository/resource.py"
SNAP = "src/devtools/context/repository/snapshot.py"
CFG = "pyproject.toml"
VALID = "docs/development/validation.md"
PDOC = "src/devtools/context/planning/docs/overview.md"
ARCH = "docs/architecture.md"
PIN = "src/devtools/context/planning/__init__.py"
OUT = "src/devtools/context/__init__.py"


def evidence(address, start=0, end=None):
    text = P["task_text"] if address is None else RES[address]["text"]
    end = len(text) if end is None else end
    return {"origin":"TASK" if address is None else "RESOURCE", "address":address,
            "content_identity":None if address is None else RES[address]["content_identity"],
            "document_identity":None if address is None else RES[address]["document_identity"],
            "text_sha256":sha(text.encode()), "coordinate_system":"Unicode code points; zero-based; half-open",
            "start":start, "end":end, "text":text[start:end]}


def section(address, start, end=None):
    text = RES[address]["text"]
    a = text.index(start)
    b = len(text) if end is None else text.index(end, a + len(start))
    return evidence(address, a, b)


def task(ob):
    return [evidence(None, x["start"], x["end"]) for x in OBS[ob]["task_basis"]]


def unique(values):
    return [v for _,v in sorted({sha(canonical(v)):v for v in values}.items())]


def walk_spans(value):
    if isinstance(value, dict):
        if {"origin","start","end","text"} <= value.keys():
            yield evidence(value.get("address") if value["origin"] != "TASK" else None, value["start"], value["end"])
        else:
            for child in value.values():
                yield from walk_spans(child)
    elif isinstance(value,list):
        for child in value:
            yield from walk_spans(child)


UNITS = {}


def unit(key, claim, obligations, bundles, reason, mode="DIRECT", granularity="ATOMIC"):
    supports = []
    for bundle in bundles:
        spans = unique(bundle)
        supports.append({"mode":mode if any(e["origin"] == "RESOURCE" for e in spans) else "TASK",
                         "resources":sorted({e["address"] for e in spans if e["origin"] == "RESOURCE"}),
                         "evidence":spans,
                         "inference":reason})
    UNITS[key] = {"id":key,"claim":claim,"obligations":sorted(obligations.split()),
                  "necessity_rationale":reason,"granularity":granularity,"supports":supports}


def tu(key, claim, obligations, task_ob=None, reason=None):
    unit(key,claim,obligations,[task(task_ob or obligations.split()[0])],reason or "The task prescribes this future behavior; this does not assert that it is implemented.")


def define_units():
    tu("source.admitted","Admit caller-selected direct function/class declarations and direct methods only under a validated native class parent.","source",reason="The task fixes positive source scope; admission still requires the native contracts below.")
    tu("source.exclusions","Source identity must not be interpreted as runtime attribute, imported-facade, inherited-method or semantic resolution.","source documentation","source")
    selector = [evidence(S)]
    selector_doc = [section(SD,"## Exact source declaration selection", "Localization's [direct import dependency adapter]")]
    unit("source.selection","The selector accepts one retained module, exact identifier and CLASS/FUNCTION kind, and retains both native analyses plus all matching direct declarations, including repeated/decorated declarations; parse failure propagates without successful coverage.","source integrity",[selector,selector_doc],"Neither the selected function name nor the future scope specifies its current input/result and failure contract.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("integrity.module","Selection requires matching module repository, snapshot and retained resource state before canonical derivation.","integrity",[selector,selector_doc],"Current module admission is a repository fact, also documented explicitly; either account supplies the same required check.")
    f_identity = [section(F,"class PythonModuleResourceDependency:","class PythonFunctionDeclarationCoverage:")]
    unit("native.function","Function knowledge separates derivation, snapshot-local structural subject and addressed source occurrence; its subject binds parser definition, content-bearing resource dependency and declaration ordinal, rather than name alone.","source integrity materialization",[f_identity],"Native identity/provenance must be validated and preserved using the actual function value contract.",granularity="LEGITIMATELY_COLLECTIVE")
    class_code = [section(C,"class PythonClassMethodDerivationDefinition:","class PythonExcludedClassMethodSyntaxKind"),section(C,"def derive_python_class_method_declarations(","def analyze_python_class_method_resources(")]
    class_doc = [section(CD,"## Identity, provenance, and containment","## Bounded direct-base resolution")]
    unit("native.class","A direct module-body class has distinct knowledge, derivation and structural subject identities bound to parser definition, snapshot, exact resource dependency and direct-class ordinal, with an addressed source occurrence.","source integrity materialization",[class_code,class_doc],"The implementation and its package account are substitutable evidence of this bounded identity relationship.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("native.method","A native direct method retains its own occurrence and canonical containing_class; its subject binds that class subject and per-class ordinal. Lexical parent and occurrence resource are different relationships.","source integrity materialization",[class_code,class_doc],"The native parent relationship is needed to admit methods without runtime resolution; a particular containment view is not an additional necessary fact.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("integrity.canonical","Compare supplied declarations, and a supplied method's parent and parent link, with canonical native values from the retained content under compatible derivation semantics before admission.","integrity",[class_code + task("integrity"),class_doc + task("integrity")],"Canonical derivation plus equality/membership is an admissible implementation inference. Frozen or structurally stamped caller values alone cannot authenticate name/range. The function and selector units complement this method-specific check.",mode="BOUNDED_INFERENCE")
    tu("choices.explicit","Add source choices alongside the existing qualified-reference and whole-resource choices, preserving compatibility and caller selection without automatic retrieval.","choices")
    unit("choices.protocol","Each choice supplies purpose, repository_id, snapshot_id, representation, identity and materialize(snapshot) returning MaterializedDisclosureItem through PlannedDisclosure.","choices exports",[[section(PLAN,"class PlannedDisclosure(Protocol):","class DisclosurePlan:")]],"The existing participation seam is necessary to integrate a new option and preserve dependency direction.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("choices.value","DisclosurePlan is frozen and retains purpose, frame, ordered disclosures and optional preceding_plan_identity.","choices",[[section(PLAN,"@dataclass(frozen=True, slots=True)","    def __post_init__")]],"The future immutability instruction does not specify the current value shape.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("choices.admission","Plan construction rejects blank purpose, empty choices, incompatible purpose/repository/snapshot and duplicate choice identities.","choices",[[section(PLAN,"    def __post_init__","    @property")]],"These existing admission checks must survive integration.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("choices.identity","The length-framed plan digest binds purpose, repository/snapshot, optional lineage and every ordered representation/choice identity pair.","choices",[[section(PLAN,"    @property\n    def identity", "def plan_disclosures("),section(PLAN,"def _digest(")]],"Native deterministic identity and ordered lineage are not supplied in full by the task.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("resource.value","RepositoryResourceOccurrence is a frozen addressed value with independent content_identity, exact content string, encoding and byte_size.","integrity materialization",[[section(RESOURCE,"class ContentIdentity:","def _validate_sha256")]],"Validation and owner provenance need this actual retained-resource representation, not just the task's instruction to retain content.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("integrity.lookup","RepositorySnapshot.resource_at returns the retained occurrence at the exact address or raises ValueError when absent, with no acquisition.","integrity",[[section(SNAP,"    def resource_at(")]],"The task names the lookup but does not specify its existing absence behavior.")
    tu("integrity.required","Reject foreign/stale frame or content, missing resources, unsupported scope and mismatched returned identity before publication, without reacquiring files.","integrity")
    materialize = section(MAT,"def materialize_disclosure_plan(")
    aligned = section(MAT,"class ContextDisclosure:","    @property")
    unit("integrity.plan_frame","Common materialization checks plan repository/snapshot against the supplied snapshot before realizing choices.","integrity",[[materialize]],"A valid individual declaration cannot compensate for an incompatible plan frame.")
    unit("integrity.returned","Every returned item must match its planned option_identity and representation; ContextDisclosure enforces positional alignment.","integrity",[[materialize,aligned]],"This existing equality boundary is stronger than merely requesting a correctly labeled new item.")
    unit("integrity.publication","The common function returns ContextDisclosure only after every option succeeds; no successful partial disclosure is returned.","integrity",[[materialize,aligned]],"Control flow and final alignment jointly establish all-or-fail publication; sampled tests alone do not prove this complete boundary.",mode="BOUNDED_INFERENCE")
    unit("materialization.carrier","MaterializedDisclosureItem carries option_identity, representation, owner resource-address/content-identity tuples, text and native_provenance; ContextDisclosure retains the originating plan.","materialization",[[section(MAT,"class MaterializedDisclosureItem:","    def __post_init__")]],"The new representation must fit the actual native carrier rather than inventing fields from the task.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("materialization.alignment","ContextDisclosure requires exactly one matching item at every ordered choice position.","materialization",[[aligned]],"Cardinality and position alignment are a result invariant distinct from carrier shape.")
    unit("materialization.order","Common materialization invokes each choice and appends its item in caller plan order.","materialization",[[materialize]],"Mixed representations must preserve this existing realization behavior.")
    unit("materialization.coordinates","Native ranges use one-based lines, zero-based UTF-8 byte columns and exclusive ends, anchored by snapshot and resource address.","materialization",[[section(F,"class PythonSourceRange:","class PythonModuleResourceDependency:")]],"These native coordinates are necessary to interpret exact spans; source-extractor code is a useful implementation example, not a distinct mandatory fact.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("materialization.decorators","Native declaration spans start at def/async def/class and exclude preceding decorators; decorated declarations remain valid native source facts.","materialization",[[section(F,"def derive_python_function_declarations(","def analyze_python_function_declaration_resources("),section(C,"def _occurrence(","def _range_values(")],class_doc],"The existing range is narrower than the requested representation. Preserve native provenance and explicitly account for a decorator-inclusive segment; do not silently relabel the old range.",mode="BOUNDED_INFERENCE")
    tu("materialization.exact","Materialize the exact selected source, preserving decorators, UTF-8 boundaries and CRLF/non-ASCII bytes.","materialization")
    tu("materialization.provenance","Retain native derivation, source-range and owner-resource provenance in the disclosure.","materialization")
    tu("materialization.no_expansion","Do not implicitly expand a declaration choice to its whole owner.","materialization")
    tu("materialization.no_sufficiency","Exact source disclosure must not imply information sufficiency.","materialization")
    unit("assembly.render","Common rendering retains ContextDisclosure and emits purpose, plan/snapshot identities, item count and each ordered item's ordinal, representation, option identity and text.","assembly",[[section(REN,"class RenderedContextDisclosure:","def assemble_context_disclosure_model_request(")]],"Rendering compatibility depends on the actual metadata and ordered presentation, not just task-first policy.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("assembly.framing","Common assembly preserves task text before rendered Context using its existing section markers and UTF-8 byte-length framing.","assembly",[[section(REN,"def assemble_context_disclosure_model_request(")]],"This existing framing contract is absent from the future task's abstract preservation instruction.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("assembly.copy","The assembler uses dataclasses.replace with a new Prompt retaining the original role, thereby preserving all non-prompt request fields and the original request.","assembly",[[section(REN,"def assemble_context_disclosure_model_request(")]],"The observed replacement mechanism supports all-field preservation including tools without separately requiring the ModelRequest field inventory.",mode="BOUNDED_INFERENCE")
    tu("assembly.preserve","Preserve the original request, role, settings, conversation, provider settings and tools except the copied prompt.","assembly")
    tu("assembly.no_budget","Introduce no new budget or truncation policy.","assembly")
    tu("exports.planning_target","Expose the new explicit choice through the common planning public API.","exports")
    tu("exports.outer_target","Expose the new explicit choice through the outer Context facade.","exports")
    tu("exports.direction","Keep language-specific behavior out of common assembly and introduce no Retrieval dependency.","exports")
    unit("exports.planning_structure","The common planning boundary uses explicit imports and __all__ to expose its choices and realization APIs.","exports",[[evidence(PIN)]],"This is an existing exposure contract to extend compatibly, not a consequence of being a likely edit target.")
    unit("exports.outer_structure","The outer Context facade explicitly imports planning APIs and qualified-reference choices and re-exports them through __all__.","exports",[[section(OUT,"from devtools.context.planning import (","from devtools.context.python import ("),section(OUT,"__all__ = [")]],"The second boundary has its own concrete re-export contract; the task supplies the destination but not this structure. Existing facade Retrieval imports do not authorize adding a Retrieval dependency to common assembly.")
    test_claims = {
        "function":"Test direct function source choices.","class":"Test direct class source choices.",
        "method":"Test direct methods admitted through validated native class-parent containment.",
        "decorated":"Test decorated declarations without substituting runtime bindings.",
        "repeated":"Test repeated declarations as distinct native identities.",
        "order":"Test mixed-plan caller order.","exact":"Test exact source including decorator/UTF-8/CRLF/non-ASCII fidelity.",
        "provenance":"Test native derivation, range and owner provenance.",
        "rejection":"Test stale, foreign and missing-resource rejection.",
        "scope_identity":"Test unsupported supplied scope and mismatched returned identity rejection before publication.",
        "old_choices":"Regression-test preserved qualified-reference and whole-resource choices.",
        "request":"Regression-test copied requests, unchanged original/role and all non-prompt fields including tools.",
    }
    for k,v in test_claims.items():
        extra = task("tests") + (task("integrity") if k == "scope_identity" else task("materialization") if k in {"exact","provenance"} else task("assembly") if k == "request" else task("source") if k == "method" else [])
        unit("tests."+k,v,"tests",[extra],"The focused test requirement is interpreted with the feature contract it must validate; it does not require adopting a particular existing fixture.",mode="BOUNDED_INFERENCE")
    unit("config.pytest","Tests use pytest under tests/ with strict configuration and markers, retaining the configured opt-in marker.","tests validation",[[section(CFG,"[tool.pytest.ini_options]","[tool.coverage.run]")]],"The task requires tests and configuration preservation but does not supply the existing framework and settings.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("config.coverage","Retain devtools branch coverage, term-missing output, 100% thresholds, configured source, show_missing=true and skip_covered=false.","tests validation",[[section(CFG,"[tool.pytest.ini_options]","[tool.ruff]")]],"The live configured gate is necessary under the frozen test-conventions and validation criteria; this shared fact is counted once across obligations.",granularity="LEGITIMATELY_COLLECTIVE")
    tu("docs.package_target","Update src/devtools/context/planning/docs/overview.md.","documentation")
    tu("docs.architecture_target","Update docs/architecture.md.","documentation")
    tu("docs.content","Explain source identity versus runtime binding, explicit representation admission, supported/deferred scope and compatibility, without automatic relevance/readiness claims.","documentation")
    unit("docs.package_baseline","The package overview enumerates two implemented choices and describes the protocol as permitting its two current consumers; extend that inventory while preserving explicit selection and provenance.","documentation",[[section(PDOC,"DisclosurePlan binds purpose", "The caller may construct")]],"An accurate update must correct these concrete current claims. The task supplies neither their wording nor their implemented-status qualification.")
    unit("docs.architecture_baseline","Architecture separates native referents from representations and Localization from Context admission, and limits implemented planning to caller-directed reference/whole-resource choices; extend the implemented inventory without promoting general planning.","documentation",[[section(ARCH,"## Accepted Context and disclosure semantics", "## Accepted Evaluation responsibility")]],"These status/ownership claims constrain the requested architecture edit; the filename alone would not make this resource required.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("validation.profile","The documented protected command runs tests/ excluding tests/experiments/ before collection, leaves pytest options intact and propagates pytest exit status.","validation",[[section(VALID,"## Protected development test profile","This profile validates development behavior.")]],"The task names a protected profile but its exact scope and invocation require repository evidence.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("validation.boundary","Ordinary development validation does not validate confirmation judgments/outcomes; separate authorization is needed and the experiment-tree exclusion must not be removed to obtain a pass.","validation",[[section(VALID,"This profile validates development behavior.","## Other quality gates")]],"This is a validation/admissibility boundary, not a new feature or a reason to access excluded data.")
    unit("validation.mypy","Strict mypy uses Python 3.12, covers src/tests/experiments and retains explicit package bases with src on mypy_path.","validation",[[section(CFG,"[tool.mypy]")]],"The exact configured strict type-check scope is existing repository information.",granularity="LEGITIMATELY_COLLECTIVE")
    unit("validation.gates","Run documented separate Ruff lint/format, mypy, worktree whitespace and staged-index whitespace gates; the protected entry runs tests only.","validation",[[section(VALID,"## Other quality gates")]],"The invocation contract is necessary. Memorizing every Ruff selected/ignored rule adds no independent required fact when running the configured tool unchanged.",granularity="LEGITIMATELY_COLLECTIVE")


define_units()


def minimal_sets(sets):
    sets = sorted({tuple(sorted(s)) for s in sets}, key=lambda s:(len(s),s))
    kept = []
    for s in sets:
        if not any(set(k) <= set(s) for k in kept):
            kept.append(s)
    return sorted(kept)


def witnesses(ob):
    units = [u for u in UNITS.values() if ob in u["obligations"]]
    candidates = [()]
    for u in units:
        candidates = minimal_sets(set(c)|set(s["resources"]) for c in candidates for s in u["supports"])
    result=[]
    for members in candidates:
        assignments={u["id"]:[i for i,s in enumerate(u["supports"]) if set(s["resources"]) <= set(members)] for u in units}
        require(all(assignments.values()), "incomplete witness")
        removal={r:[u["id"] for u in units if not any(set(s["resources"]) <= (set(members)-{r}) for s in u["supports"])] for r in members}
        require(all(removal.values()),"redundant member")
        result.append({"resources":list(members),"required_unit_ids":[u["id"] for u in units],
                       "support_assignment_options":assignments,"removal_witnesses":removal,
                       "member_semantics":"ALL","alternative_semantics":"ANY"})
    return result


WITNESSES = {ob:witnesses(ob) for ob in OBS}


def indispensable(ob):
    alternatives = WITNESSES[ob]
    return sorted(set.intersection(*(set(a["resources"]) for a in alternatives)))


def global_structure():
    sets=[()]
    for ob in OBS:
        sets=minimal_sets(set(s)|set(a["resources"]) for s in sets for a in WITNESSES[ob])
    return {"sufficient_resource_unions":[list(s) for s in sets],
            "resource_range":[min(map(len,sets)),max(map(len,sets))],
            "task_indispensable_resources":sorted(set.intersection(*(set(s) for s in sets))),
            "task_only_sufficient":False,
            "scope":"Complete evidence structures for the supplied obligation frame; disagreement reconciliation only, not an already materialized reviewed gold target.",
            "derivation":"Choose ANY complete alternative for EACH mandatory obligation; union with cross-obligation reuse; discard strict supersets."}


# Explicit decisions for every disputed REQUIRED cell. No candidate position is a truth source.
REQUIRED_CELLS = {
    5:("HELPFUL_ONLY","Canonical native analysis and exact parent/method membership establish the needed admission facts. The containment view additionally checks supplied aggregate structure but is not mandatory; requiring it alongside canonical declarations would add a removable witness member."),
    21:("REQUIRED","The native class/method model establishes actual parent, ordinal, derivation and occurrence relationships needed for validation. Its package account can substitute for these semantic facts; either resource can be necessary in a complete alternative."),
    22:("REQUIRED","The frozen tests criterion includes repository test conventions. The task gives a coverage matrix but does not identify pytest's configured strictness and production coverage gate. The configuration supplies these facts; they are reused by validation."),
    24:("REQUIRED","Retained resource equality and owner provenance require the actual immutable occurrence fields and address/content distinction. The named lookup alone does not establish the returned value contract."),
    41:("HELPFUL_ONLY","The task fully prescribes the new assembly dependency restriction. The current renderer corroborates it; protocol participation and the two real export surfaces establish the required export seam without this additional resource. Its rendering contract is necessary under assembly."),
    61:("HELPFUL_ONLY","Tests demonstrate stale state and returned-item failures, but do not establish every common control-flow/publication invariant or both constructor mismatch branches. They are not a complete substitute for the common materializer's implementation."),
    67:("HELPFUL_ONLY","The class model or its package contract already establishes the canonical direct parent and bounded method analysis. Calling the convenience navigation view is not prescribed by the task and is not a separate semantic prerequisite."),
    71:("REQUIRED","The task identifies the outer facade as a destination; the existing explicit import and __all__ structure supplies the current compatibility/exposure contract. Preserve and extend that second boundary."),
    73:("REQUIRED","Exact source and owner provenance need the retained content field and independent addressed content identity. These are existing value semantics, not supplied by the task's desired representation."),
    81:("REQUIRED","The source-selection section specifies matching retained module state, both analyses, exact matches and failure boundaries. It substitutes for selection.py at the semantic level, so it belongs to a complete minimal integrity alternative; it is not required together with that implementation."),
    89:("REQUIRED","The actual PlannedDisclosure structural contract supplies the existing seam for language-specific participation without moving parsing into common assembly. The task's dependency prohibition does not provide that protocol."),
    93:("HELPFUL_ONLY","Preserving the existing qualified-reference adapter through the unchanged structural protocol does not require reproducing its delegation internals. Its concrete two-owner provenance is useful regression context, while protocol compatibility is learned from the common seam."),
    102:("HELPFUL_ONLY","The task preserves explicit whole-resource behavior and forbids implicit expansion; the common protocol supplies integration. This existing consumer illustrates those constraints but adds no necessary fact for the new option's admission."),
    107:("REQUIRED","The architecture contains concrete implemented-choice inventory and future/current ownership distinctions that the requested update must extend accurately. These claims must be learned from its text; being a named edit target alone would not suffice."),
    123:("REQUIRED","The package text supplies the native snapshot/content/parser/ordinal identity and canonical containing_class semantics. It is an alternative to the class declaration implementation for these semantic facts, not additional mandatory corroboration."),
    136:("HELPFUL_ONLY","The extractor demonstrates safe byte slicing and malformed-range rejection. Necessary coordinates come from the already-required native function contract and exactness from the task; the specific extraction algorithm is not a further required semantic input."),
    142:("REQUIRED","Validation needs the actual function subject, dependency, derivation and support fields. Desired stale/foreign rejection cannot stand in for that current identity contract."),
    144:("REQUIRED","The overview's two-consumer and implemented-choice claims are concrete baselines that must be revised coherently. The task prescribes the new content but does not state these old claims."),
    145:("REQUIRED","The current planning imports and __all__ determine its explicit public exposure mechanism. The task supplies a destination, not that compatibility contract."),
}

# Each rationale identifies the concrete contribution independently of candidate wording.
HELPFUL_REASON = {
 1:"Coverage and support mutation cases are useful negative-test patterns for caller-supplied native values.",
 3:"The preserved adapter is a concrete protocol participant useful for mixed-plan regression setup.",
 4:"The subject/occurrence distinction explains why a source declaration and its derived knowledge have separate identities.",
 6:"Canonical-substrate guidance corroborates dependency ownership; it supplies no extra export surface.",
 7:"The existing qualified-reference materializer illustrates rechecking caller-supplied membership and retained dependencies.",
 8:"Class tests concretely demonstrate bounded direct methods, exclusions and keyword-start ranges.",
 9:"Function prose explains retained-source extraction and UTF-8 spans, useful context for exact materialization.",
 10:"The real ordered-plan protocol provides a concrete example for the documentation's compatibility wording.",
 11:"The common assembler identifies concrete task-first and copied-request assertions for new regression tests.",
 12:"The frozen Prompt content/role pair clarifies what request-preservation assertions compare.",
 13:"Architecture's distinction between a subject and its occurrence contextualizes source-range/owner provenance.",
 17:"The actual source selector illustrates the source-versus-binding distinction the documentation must explain.",
 18:"The conservative binding lookup is a concrete contrast to preserving decorated and repeated source declarations.",
 19:"The planning/assembly separation corroborates why realization cannot silently change selected information.",
 25:"Architecture corroborates native subject/provenance distinctions but lacks the complete concrete native identity contract.",
 26:"Architecture corroborates ownership and current planning scope; exact export mechanisms have narrower evidence.",
 27:"Subjecthood and derivation prose gives useful terminology for documenting source identities.",
 28:"Function-package prose supplies compatibility context, with terminology that must be checked against current code.",
 29:"Grounding shows canonical analysis followed by native-parent membership, a relevant admission-test pattern.",
 30:"The immutable ordered plan explains the order that materialization must realize; materializer code supplies the actual realization contract.",
 32:"Existing function request tests include tools and unchanged original fields, useful regression patterns for common assembly.",
 35:"The implemented backlog contract corroborates profile exclusion, coverage retention and exit-code propagation.",
 36:"The taxonomy distinguishes selected plans, realized disclosures and model requests, contextualizing assembly ownership.",
 37:"The occurrence fields help construct retained content and provenance fixtures.",
 40:"Older rendering tests show CRLF, non-ASCII and repeated-source order assertions transferable to new cases.",
 42:"Qualified-reference stale/redirected dependency tests illustrate compatibility risks for preserved choices.",
 44:"The overview corroborates task-first copying and ordered realized items, without specifying every exact rendering detail.",
 45:"Module interpretation exposes retained module state useful for constructing selector inputs.",
 46:"Materialized item and result guards provide the result side of the option protocol and useful integration context.",
 51:"Class/method tests demonstrate keyword-start spans and native parent provenance relevant to decorator-preserving extraction.",
 52:"The selector's documented repeated/decorated and failure semantics help choose test fixtures.",
 54:"The taxonomy corroborates distinct planning and assembly ownership without specifying public exports.",
 55:"The renderer supplies concrete examples of compatibility and task-before-Context copying for documentation.",
 56:"Function identities and native range construction help write accurate source/provenance explanations.",
 57:"The interaction overview corroborates request immutability and ownership; generic replacement already preserves all fields.",
 58:"Containment mutation tests show how declared support and ordinals constrain native function ownership.",
 59:"Reference documentation makes the existing binding-based choice's scope explicit, useful compatibility context.",
 62:"The package overview summarizes frame checking and aligned realized items as integrity context.",
 64:"Reference materialization tests provide stale/redirected source examples applicable to provenance preservation.",
 65:"The initializer locates public planning values and gives useful integration context; exports has the distinct current exposure obligation.",
 66:"Malformed-range and CRLF/non-ASCII examples are directly useful to validate exact extraction.",
 70:"The selector provides canonical native declarations and analyses for new test setup.",
 72:"Function code provides exact native subjects, ranges and derivations for meaningful fixtures.",
 74:"Selection tests cover native identity preservation across decorators and repeated names and reject foreign inputs.",
 75:"Generic option dispatch corroborates that common planning need not parse Python or resolve bindings.",
 76:"The preserved reference materializer is an exact extraction and dependency-validation example, without licensing binding resolution for direct source choices.",
 77:"The whole-resource consumer provides a compatibility fixture and an example of retained-resource equality checks.",
 78:"Decorated versus binding selection tests give concrete examples for scope documentation.",
 79:"Containment code illustrates supplied-analysis checks and direct parent navigation for negative fixtures.",
 84:"Module interpretation helps construct caller-selected retained modules without discovery or acquisition.",
 86:"Reference scope gives a concrete comparison with source identity, especially imported or decorated bindings.",
 87:"Reference tests demonstrate rejection of stale target/source and redirected support, useful integrity corroboration.",
 88:"The overview corroborates generic participation and current consumers but does not supply the explicit public export lists.",
 90:"Architecture's realized-versus-planned distinction corroborates faithful materialization and no implicit sufficiency.",
 92:"Class code supplies concrete parent/source identity examples useful in documentation.",
 95:"Existing rendering tests demonstrate exact-source and caller-order assertions for repeated declarations.",
 97:"Malformed byte-range tests corroborate rejection rather than inaccurate source publication.",
 99:"ModelRequest tests corroborate immutable role/settings/continuation behavior; the common replacement mechanism already establishes preservation.",
 100:"Function containment tests show stale/inconsistent support mutations useful for validation design.",
 103:"The overview corroborates one realized item per choice and native provenance, but lacks all concrete carrier and coordinate details.",
 104:"Native class tests illustrate exclusions and class-parent linkage against which supplied values can be checked.",
 105:"The plan implementation gives testable duplicate/purpose/frame/order invariants for integration fixtures.",
 106:"The snapshot lookup supplies a convenient missing-resource fixture and establishes retained rather than reacquired state.",
 109:"Reference documentation helps distinguish source subjects from static binding-resolution products.",
 110:"The ModelRequest field inventory confirms that tools and provider settings are fields to preserve in regression assertions.",
 112:"The operating guide's documentation-impact instruction corroborates updating behavior claims and preserving architecture status.",
 113:"Common result guards identify meaningful returned-identity and incomplete-disclosure regression cases.",
 114:"Function-package prose corroborates membership, retained dependencies and UTF-8 range checks, but is not a complete substitute for native identity contracts.",
 115:"Plan construction rejects incompatible choices, useful context alongside the later publication-time frame check.",
 116:"The architecture describes native source subjects and parent containment, corroborating narrower native contracts.",
 119:"Function containment navigation exposes occurrence owners, useful provenance context without a new source fact.",
 120:"Function documentation describes copying and task-first assembly, corroborating the common assembly pattern.",
 121:"The existing extractor gives concrete byte-boundary, reversed-range and line-boundary cases for new tests.",
 125:"The identity/derivation architecture explains why frame and content applicability differ from a bare name or location.",
 126:"Retained exact-address lookup contextualizes source selection, with its mandatory lookup behavior established under integrity.",
 128:"The extractor demonstrates rejection of invalid UTF-8/range boundaries before returning exact text.",
 129:"The older assembler supplies a useful all-fields-copy regression pattern.",
 130:"The function containment builder is an example of testing supplied analysis consistency without rereading files.",
 131:"Native class/method derivation provides valid and excluded source forms for focused fixtures.",
 132:"The taxonomy's native-subject and explicit-representation distinction contextualizes direct source admission.",
 135:"The class overview supplies bounded direct-parent and decorator-range examples useful for test design.",
 137:"The resource value explains retained owner representation useful to source fixture construction.",
 138:"Architecture corroborates the separation of realized disclosure from consumer-specific model presentation.",
 139:"Repeated-name and UTF-8-column tests corroborate exact range and identity preservation.",
 140:"Repeated declarations with distinct subjects and UTF-8 ranges are concrete source-contract corroboration.",
 143:"Observation explains how the retained independent content identity is constructed; integrity compares retained values and need not reacquire or recompute them.",
 147:"The roadmap's implemented checkpoint corroborates the existing two-choice inventory; the requested package and architecture texts supply the actual documentation baselines.",
}


NONCELL = {
 2:(["tests.old_choices","tests.request"],"OVERCOMPOUND","Existing-choice regression and copied-request regression can fail independently. Split the combined claim into those two coverage units; neither changes the required behavior."),
 14:(["source.admitted","source.exclusions","docs.content"],"PARTIAL_OVERLAP","Positive source scope and forbidden runtime resolution are task-backed. Documentation additionally requires representation admission, compatibility and no relevance/readiness claims; a source-scope sentence alone does not cover those editorial requirements."),
 16:([],"NOT_NECESSARY","Run the configured Ruff commands, but no independent necessary unit requires memorizing py312, 88 columns or individual selected/ignored rule names. These are useful configuration details, not missing task facts needed in addition to the configured invocation."),
 20:(["docs.package_target","docs.architecture_target","docs.package_baseline","docs.architecture_baseline"],"COMPLEMENTARY","Destinations are task-backed. Concrete two-consumer/implemented-inventory claims and current/future ownership distinctions are repository-backed baselines that must be learned for accurate edits. Neither position alone states both roles."),
 23:(["assembly.framing","assembly.copy","assembly.preserve"],"PARTIAL_OVERLAP","Both descriptions share copied-request semantics; byte-length framing is a distinct current contract and must not disappear. The task supplies preservation targets, while common code supplies framing and the all-field-copy mechanism."),
 31:(["resource.value"],"NECESSARY","The retained immutable value and its independent address/content fields are real repository contracts. A desired exact representation does not establish them. Keep one shared unit for integrity and materialization."),
 33:(["choices.explicit","choices.value","choices.protocol","choices.admission","choices.identity"],"PARTIAL_OVERLAP","Retain task-backed compatibility and the actual immutable/protocol/admission/identity contracts. Existing consumer internals are useful examples but need not be promoted into required units when the common seam and old consumers remain intact."),
 34:(["tests.order","tests.exact","tests.provenance"],"OVERCOMPOUND","Ordering, exact source bytes and native provenance can fail independently. Represent their coverage separately; decorator/encoding cases exercise exactness rather than creating arbitrary implementation units."),
 43:(["integrity.plan_frame","integrity.returned","integrity.publication"],"OVERCOMPOUND","Frame admission, returned identity/representation alignment and successful whole-disclosure publication are distinct guards. They share one source without becoming one indivisible fact."),
 63:(["choices.value","choices.identity"],"PARTIAL_OVERLAP","Both identify the ordered digest inputs. The frozen value shape and the digest relation are distinct; retain the explicit length framing and lineage without duplicating equivalent identity claims."),
 69:(["integrity.plan_frame","integrity.returned","integrity.publication"],"EQUIVALENT_AFTER_SPLIT","The compound and split accounts cover the same control-flow/result boundaries. Use three units with shared implementation evidence; do not count repeated statements as extra information."),
 80:(["native.method","integrity.canonical"],"PARTIAL_OVERLAP","The necessary fact is canonical direct parent/method membership in retained native analysis. The view's aggregate consistency checks do not authenticate arbitrary names/ranges. Canonical replay/equality can satisfy admission without requiring this particular view; its limitations remain explicit."),
 82:(["config.pytest","config.coverage","validation.mypy"],"OVERCOMPOUND","Test collection/marker configuration, coverage gate and type-check scope are separate configured contracts. Preserve their exact values with separate units; do not infer them from task wording."),
 83:(["materialization.exact","materialization.provenance","materialization.coordinates","materialization.decorators","materialization.order","materialization.no_expansion","materialization.no_sufficiency"],"PARTIAL_OVERLAP","Desired exactness and non-expansion are task-backed; existing byte coordinates, keyword-start ranges and common order are repository-backed. The existing extractor algorithm is a helpful way to implement exactness, not an independently mandatory information unit."),
 85:(["source.selection","integrity.module"],"PARTIAL_OVERLAP","Keep exact kind/name, both native analyses, repeated/decorated results and propagated parse failure. Separate the module-frame/resource admission check from the selector result contract. Code and package documentation are semantic alternatives."),
 94:(["integrity.required","integrity.canonical","integrity.module","integrity.returned","integrity.publication"],"COMPLEMENTARY","The task prescribes the rejection policy. Current canonical admission, selector checks and common publication guards establish how existing values and boundaries constrain implementation. Do not replace repository truth with the desired policy or mandate every optional aggregate-view check."),
 96:(["tests.function","tests.class","tests.method","tests.decorated","tests.repeated"],"OVERCOMPOUND","Function, class, validated-parent method, decorated and repeated cases expose independent failures. Use separate coverage units without treating each fixture permutation as a new obligation."),
 98:(["materialization.carrier","materialization.alignment","materialization.order"],"OVERCOMPOUND","Carrier fields, result positional/cardinality alignment and materialization iteration order are distinct facts. Both supplied wordings overlap but hide at least one of those boundaries in a compound sentence."),
 101:(["exports.planning_target","exports.outer_target","exports.planning_structure","exports.outer_structure"],"COMPLEMENTARY","Future exposure destinations are task-backed. Explicit current imports and __all__ at two boundaries are existing compatibility contracts and require repository evidence; preserve both levels rather than treating a named API as proof of its structure."),
 117:(["validation.profile","validation.boundary"],"PARTIAL_OVERLAP","Keep the protected selection/invocation contract and the separate authorization/exclusion boundary as distinct facts. The longer profile statement does not make the explicit authorization requirement disappear."),
 122:(["assembly.preserve","assembly.copy","assembly.no_budget"],"PARTIAL_OVERLAP","The task fully supplies the preservation target and no-budget policy. Current replace-based copying is a separate repository mechanism reused from the assembly decision; no new request-field inventory unit is needed."),
 133:(["tests.rejection","tests.scope_identity"],"BROADER_REQUIRED","Stale/foreign/missing are explicitly enumerated, while unsupported-scope and returned-identity rejection are also mandatory feature guards. Focused tests must exercise those guards before publication. Keep the inference explicit rather than misquoting the test sentence as enumerating them."),
 141:(["config.pytest","config.coverage"],"NECESSARY","The frozen tests obligation includes existing conventions. The task does not establish pytest strictness or the configured 100% branch gate. Reuse the same configuration units under validation rather than either omitting them or counting them twice."),
 146:(["exports.direction","choices.protocol"],"PARTIAL_OVERLAP","The desired no-Retrieval/no-language-specific-assembly boundary is supplied by the task. The actual structural protocol is necessary existing integration information. The renderer confirms the restriction but adds no independent required exports unit."),
}


WITNESS_RATIONALES = {
 "validation":"The development contract plus current configuration covers invocation/exclusion, strict testing/coverage, mypy and separate gates. Exact Ruff rule enumeration is not an additional necessary unit. The script corroborates the documented behavior and is not added merely because the task names it.",
 "tests":"The task supplies coverage categories, but the frozen criterion also requires the current repository testing conventions. Configuration is therefore necessary. Existing test files supply replaceable examples; the empty resource witness omits the framework/gate facts.",
 "source":"Require selector semantics, native function identity and native class/method identity. Selector implementation or its exact package account can substitute; class implementation or its package account can substitute. The view is redundant when canonical parent/method semantics are already established.",
 "integrity":"Combine native selector/function/class-method contracts with retained occurrence/lookup and common publication guards. Native declarations cannot be omitted in favor of generic future rejection wording. Class/selector documentation can substitute for their stated native facts. Tests are not a complete alternative for all common guards.",
 "assembly":"Common rendering.py supplies exact framing, metadata/order and generic replacement. The task supplies no-budget and preservation targets. Older assemblers, request fields and tests corroborate but do not add necessary members.",
 "materialization":"Combine native function/class-method provenance and coordinates with retained owner values and the common carrier/order contract. The task supplies exactness; native keyword-start ranges require an explicit decorator-inclusive segment. The old extractor is a removable implementation example.",
 "exports":"Future destinations and exclusions are task-backed, but the two existing explicit import/__all__ boundaries and actual structural participation seam are necessary repository facts. Common rendering is corroboration for this obligation and remains required for assembly.",
 "choices":"The task supplies explicit coexistence and compatibility; plan.py supplies value shape, admission, identity and protocol. Existing adapters can remain preserved through that seam, so their internal realization details are not additional required members.",
 "documentation":"The task supplies destinations and future content. Both named documents also contain concrete implemented-choice/current-future baseline claims that an accurate update must reconcile. Their necessity follows from those claims, not from likely editing alone.",
}


def unit_evidence(ids):
    return unique(e for key in ids for s in UNITS[key]["supports"] for e in s["evidence"])


def make_decisions():
    result=[]
    cell_ids={i for i,q in enumerate(P["propositions"]) if q["type"] == "DISPUTED_CELL_LABEL"}
    require(cell_ids == set(HELPFUL_REASON),"explicit helpful-cell coverage")
    require({i for i,q in enumerate(P["propositions"]) if q["type"] == "DISPUTED_REQUIRED_NECESSITY"} == set(REQUIRED_CELLS),"explicit required-cell coverage")
    for i,q in enumerate(P["propositions"]):
        ob=q["obligations"][0]
        te=unique(e for o in q["obligations"] for e in task(o))
        ev=[]
        if q["type"] in {"DISPUTED_CELL_LABEL","DISPUTED_REQUIRED_NECESSITY"}:
            address=q["resource_addresses"][0]
            if i in REQUIRED_CELLS:
                decision,rationale=REQUIRED_CELLS[i]
            else:
                decision="HELPFUL_ONLY"
                rationale=HELPFUL_REASON[i]+" This materially aids interpretation or implementation, but the reconciled required facts have complete support without this additional resource for this obligation."
            ids=[u["id"] for u in UNITS.values() if ob in u["obligations"] and any(address in s["resources"] for s in u["supports"])]
            is_member=any(address in a["resources"] for a in WITNESSES[ob])
            require((decision == "REQUIRED") == is_member,"cell/witness consistency: "+str(i))
            # Exact local corroboration from candidates, rechecked against sealed resources.
            ev=[e for e in walk_spans(q["positions"]) if e["origin"] == "RESOURCE" and e["address"] == address]
            if not ev:
                ev=[evidence(address)]
            ev+=unit_evidence(ids)
            judgment={"label":decision,"obligation":ob,"resource_address":address,
                      "necessary_unit_ids":ids if decision == "REQUIRED" else [],
                      "required_in_any_minimal_alternative":is_member}
        elif q["type"] == "ALTERNATIVE_WITNESS_SUFFICIENCY":
            decision="RECONCILED"; rationale=WITNESS_RATIONALES[ob]
            ids=[u["id"] for u in UNITS.values() if ob in u["obligations"]]
            judgment={"complete_alternatives":WITNESSES[ob],"indispensable_resources":indispensable(ob)}
            ev=unit_evidence(ids)
        elif q["type"] == "OBLIGATION_INDISPENSABILITY":
            decision="RECONCILED"; rationale="Derived from the reconciled necessary units and complete minimal alternatives, not candidate arithmetic. "+WITNESS_RATIONALES[ob]
            ids=[u["id"] for u in UNITS.values() if ob in u["obligations"]]
            judgment={"indispensable_resources":indispensable(ob),"indispensable_unit_ids":ids,"deduplicated":True}
            ev=unit_evidence(ids)
        elif q["type"] == "TASK_SUFFICIENCY_INDISPENSABILITY":
            decision="RECONCILED"; rationale="Derive sufficiency only after native contracts, task prescriptions and per-obligation alternatives are reconciled. Cross-obligation reuse prevents counting the same configuration/protocol/native facts twice; eliminate strict resource supersets."
            judgment=global_structure(); ev=unit_evidence(list(UNITS))
        elif q["type"] == "LIMITATION_ADMISSIBILITY":
            decision="RECONCILED"
            if i == 49:
                statement="Native subject/derivation identity includes parser implementation/runtime and grammar/analysis definition. Canonical equality must use compatible derivation semantics; identical content alone is insufficient."
                rationale="This is a real identity compatibility constraint, corroborated by both native definition digests. It is not a missing-evidence gap and requires no runtime execution here."
            elif i == 118:
                statement="Containment validates supplied structural frame/dependency/coverage/ordinal/parent consistency without reparsing. It does not authenticate every caller-supplied name/range; canonical retained-source replay and membership/equality can provide that check."
                rationale="The builder's checks omit arbitrary name/range rederivation; the canonical selector and method-grounding example supply an admissible stronger admission path. This limits what containment alone proves, not the feasibility of the task."
            else:
                raise ValueError("unknown limitation")
            judgment={"classification":"IMPLEMENTATION_AND_INFERENCE_CONSTRAINT","statement":statement,"blocks_complete_judgment":False,"duplicate_of":None}
            ev=list(walk_spans(q["positions"]))
        else:
            require(i in NONCELL,"missing semantic decision")
            ids,relation,rationale=NONCELL[i]; decision="RECONCILED"
            judgment={"relation":relation,"necessary_unit_ids":ids,"replacement_claims":[UNITS[u]["claim"] for u in ids]}
            if q["type"] == "GRANULARITY":
                judgment["granularity"]=relation
            ev=unit_evidence(ids)
            if not ev:
                ev=list(walk_spans(q["positions"]))
        all_ev=unique(te+ev)
        d={"proposition_identity":q["identity"],"type":q["type"],"obligations":q["obligations"],
           "neutral_question":q["neutral_question"],"decision":decision,"final_reconciled_judgment":judgment,
           "rationale":rationale,"task_evidence":[e for e in all_ev if e["origin"] == "TASK"],
           "repository_evidence":[e for e in all_ev if e["origin"] == "RESOURCE"],
           "ambiguity":{"state":"RESOLVED","reason":"Supplied task and repository evidence support this bounded judgment; implementation choices are not missing semantic evidence."},
           "provenance":{"packet_archive_sha256":INPUT_HASHES["packet.json.gz"],"canonical_payload_sha256":PAYLOAD_HASH,
                         "candidate_position_sha256":[sha(canonical(x)) for x in q["positions"]],
                         "basis":"Independent task/repository adjudication; candidate positions are interpretations, not authority."}}
        d["decision_sha256"]=sha(canonical(d))
        result.append(d)
    return result


BLINDNESS_CATEGORIES = ["repository checkout","Git/history","parent directory","sibling workspaces","PRIMARY adjudication","independent C-R adjudication","source reviewer identities","model identities","chronology","Stage B","retrieval queries","analyzed terms","hint inventories","routes","rankings","scores","arms","acquisition costs","U2 outcome information","confirmation data","reserve data","external web information","prior Codex-session content"]


def document():
    decisions=make_decisions()
    doc={"schema":"case-0012-reconciliation-v1","case":P["case"],"task_identity":P["task_identity"],
         "packet_identity":{"archive_sha256":INPUT_HASHES["packet.json.gz"],"canonical_payload_sha256":PAYLOAD_HASH,"initial_file_sha256":INPUT_HASHES},
         "scope":"Resolve only the 148 anonymized propositions; no feature implementation, reviewer agreement measurement or experimental outcome judgment.",
         "decision_vocabulary":sorted(DECISIONS),
         "evidence_rules":{"coordinates":"Unicode code points; zero-based; half-open","unit_support":"ALL evidence/resources within a support; ANY complete support alternative","obligation_witness":"ALL members; ANY complete alternative","required":"Necessary member of at least one complete minimal alternative, not necessarily every alternative","helpful_only":"Material corroboration/context/example, removable from every complete minimal alternative","unnecessary":"No material contribution","task":"Authoritative future prescription; not proof of current repository behavior"},
         "semantic_units":list(UNITS.values()),"witnesses_by_obligation":WITNESSES,
         "task_sufficiency":global_structure(),"decisions":decisions,
         "counts":{"propositions":len(decisions),"by_type":dict(sorted(Counter(d["type"] for d in decisions).items())),"by_decision":dict(sorted(Counter(d["decision"] for d in decisions).items())),"unresolved":0},
         "blindness_attestation":{"access":{k:"NO" for k in BLINDNESS_CATEGORIES},
                                  "scope":"No excluded external/source-treatment information was sought or used. Inert repository vocabulary within the permitted packet is not external experimental access. No prior session content was consulted.","clean_treatment_blind":True}}
    return doc


METHOD = """# Case 0012 reconciliation method

This reconciliation uses only the five initially whitelisted files. The standalone
validator was run successfully before any output existed. The archive, canonical
payload, manifest and integrity digest scopes were independently checked; all five
initial file hashes are pinned in the builder. Embedded repository source is inert
text and is never executed or imported. The future development validation commands
are evidence about that task and were not run in this sterile workspace.

The packet supplies no output filename/schema or adjudication-decision enum beyond
the resource labels. The local schema therefore uses REQUIRED, HELPFUL_ONLY and
UNNECESSARY for cells; RECONCILED for explicit structural decisions; UNRESOLVED is
reserved for genuine missing/ambiguous semantic evidence. No unresolved decision
was necessary. Candidate order is not a source identity. Provenance retains only
the packet/proposition identities and hashes of anonymized candidate bytes.

Determine necessary information first. A task prescription authorizes future
behavior; it does not establish a current identity, value, API or compatibility
contract. Current export import/__all__ structures and documentation inventory/status
claims matter because their behavior/claims must be extended compatibly, not merely
because their files are named. Existing adapters, extractor code and test fixtures
are helpful where the common protocol, native coordinates and task fully supply
the needed facts. The configured test framework and gates remain repository facts.

Units separate independently falsifiable boundaries while keeping one value/schema
relationship collective where its fields jointly identify the contract. Multiple
obligations reuse the same unit. ALL members of a unit support are complementary;
ANY complete support may replace another. Witnesses enumerate exact minimal sets
covering every unit for an obligation, with per-member removal counterexamples.
Global sufficiency unions one witness per obligation and eliminates strict
supersets. Indispensability is intersection, calculated only after reconciliation.
Empty witnesses are supported by the representation but rejected here for tests,
exports and documentation because each has a necessary current repository fact.

Native keyword-start spans exclude decorators. Exact representation must explicitly
account for decorator-inclusive ranges without rewriting native provenance. Native
subjects bind parser definition/runtime as well as retained content. Containment
consistency is weaker than canonical replay/equality for caller-constructed values.
These are constraints, not evidence gaps or reasons to access external information.

Build: python -B reconciliation_builder.py build
Verify: python -B reconciliation_builder.py verify

Build preflights all output names and refuses any existing target, even identical
bytes. Verify reconstructs JSON, Markdown, method, validation and hash manifest in
memory, checks exact byte equality, validates support bounds/identities and repeats
adversarial mutations. A separate Python process performs final verification.
The mutation suite checks content-address seals as well as roster/schema/reference
invariants, including mutations with recomputed decision hashes. The hash manifest
seals the builder and four generated scientific outputs. Its payload_sha256 seals
the manifest body excluding that field; its physical hash is reported separately
to avoid recursive self-hashing. Hashes detect alteration, not semantic correctness
or malicious coordinated replacement of the entire trusted packet and builder.

Every decision is exposed in the deterministic Markdown review, including exact
task/repository spans and final unit/witness structures. All 148 propositions have
exactly one decision; no agreed-cell relabeling or extra proposition is invented.
The reconciled unit/witness account supports these disagreements and must be joined
with agreed source judgments to materialize the reviewed target in the next step.

The operational .local/codex-result.md is created only after adjudication, scientific
validation, hashes and blindness attestation are complete. It is excluded from all
scientific evidence and digest scopes. No source identity, ordering or reliability
assumption participates in a decision.
"""


def markdown(doc):
    lines=["# Case 0012 reconciliation review","",f"Resolved {len(doc['decisions'])} propositions; unresolved: 0.","",
           "Only supplied task and inert repository evidence were used. No feature implementation or reviewer-agreement measurement was performed.","",
           "## Counts","","```json",canonical(doc["counts"]).decode().rstrip(),"```","",
           "## Reconciled semantic structure","",
           "Each unit below retains its exact supports in reconciliation.json. Decision sections expose all cited evidence. ALL members of a support/witness are joint; ANY complete alternative substitutes.",""]
    for u in doc["semantic_units"]:
        lines += [f"- **{u['id']}** ({', '.join(u['obligations'])}; {u['granularity']}): {u['claim']} {u['necessity_rationale']}"]
    lines += ["","## Witnesses and task sufficiency","","```json",canonical({"witnesses":doc["witnesses_by_obligation"],"task_sufficiency":doc["task_sufficiency"]}).decode().rstrip(),"```",""]
    for d in doc["decisions"]:
        lines += [f"## {d['proposition_identity']}","",f"**{d['type']} — {d['decision']}**", "",d["neutral_question"],"",d["rationale"],"",
                  "Final judgment:","","```json",canonical(d["final_reconciled_judgment"]).decode().rstrip(),"```","",
                  "Ambiguity: RESOLVED.","",f"Decision SHA-256: `{d['decision_sha256']}`","",
                  "Anonymized candidate-byte hashes: "+", ".join('`'+x+'`' for x in d["provenance"]["candidate_position_sha256"])+".",""]
        for kind in ("task_evidence","repository_evidence"):
            lines += ["Exact "+kind.replace("_"," ")+":",""]
            for e in d[kind]:
                name="TASK" if e["origin"] == "TASK" else e["address"]
                lines += [f"{name} [{e['start']}, {e['end']}) — content identity: {e['content_identity'] or 'task'}; text SHA-256: {e['text_sha256']}","","````text",e["text"].rstrip("\n"),"````",""]
    lines += ["## Blindness attestation","","All categories below are NO. Confirmation and reserve information were not accessed.",""]
    lines += [f"- {k}: {v}" for k,v in doc["blindness_attestation"]["access"].items()]
    lines += ["","## Validation and next step","","See reconciliation_validation.json for checks and reconciliation_hashes.json for scientific artifact hashes. The hash manifest's physical SHA-256 is reported in the final operational report.","",
              "Import this reconciliation into the devtools repository without modification.","",
              "Materialize one reviewed Case 0012 gold target from agreed source judgments plus these reconciled disagreement decisions.","",
              "Validate the complete reviewed cells, semantic units, witnesses, alternatives, sufficiency and gaps.","",
              "Then and only then join reviewed gold to frozen Stage B and perform Stage D.","","STOP.",""]
    return "\n".join(lines).encode("utf-8")


def validate_span(e):
    require(e["origin"] in {"TASK","RESOURCE"},"evidence origin")
    if e["origin"] == "TASK":
        require(e["address"] is None and e["content_identity"] is None and e["document_identity"] is None,"task identity")
        text=P["task_text"]
    else:
        require(e["address"] in RES,"unknown evidence resource")
        r=RES[e["address"]]
        require(e["content_identity"] == r["content_identity"] and e["document_identity"] == r["document_identity"],"altered evidence identity")
        text=r["text"]
    require(type(e["start"]) is int and type(e["end"]) is int and 0 <= e["start"] < e["end"] <= len(text),"invalid support bounds")
    require(e["coordinate_system"] == "Unicode code points; zero-based; half-open","coordinate system")
    require(text[e["start"]:e["end"]] == e["text"] and sha(text.encode()) == e["text_sha256"],"support-span identity")


def validate_document(doc, compare=True):
    require(doc["case"] == P["case"] and doc["task_identity"] == P["task_identity"],"case/task identity")
    require(doc["packet_identity"] == document()["packet_identity"],"exact packet identity")
    roster=[q["identity"] for q in P["propositions"]]
    ids=[d["proposition_identity"] for d in doc["decisions"]]
    require(len(ids) == len(set(ids)),"duplicate decision")
    require(set(ids) == set(roster) and len(ids) == 148,"exact decision inventory")
    require(ids == roster,"deterministic decision order")
    for d,q in zip(doc["decisions"],P["propositions"],strict=True):
        require(d["type"] == q["type"] and d["obligations"] == q["obligations"],"proposition context")
        require(d["decision"] in DECISIONS,"invalid decision")
        for e in d["task_evidence"]+d["repository_evidence"]:
            validate_span(e)
        require(bool(d["task_evidence"]),"missing task evidence")
        require(d["decision_sha256"] == sha(canonical({k:v for k,v in d.items() if k != "decision_sha256"})),"altered judgment seal")
        require(d["provenance"]["candidate_position_sha256"] == [sha(canonical(x)) for x in q["positions"]],"candidate provenance")
        # Scan only adjudication prose, not permitted inert code/API vocabulary or the attestation checklist.
        prose=canonical({"rationale":d["rationale"],"judgment":d["final_reconciled_judgment"],"provenance":d["provenance"]}).decode()
        require(not re.search(r"\bPRIMARY\b|\bC-R\b|\bC_R\b|GPT-6|source[_ -]?reviewer|treatment[_ -]?arm|HIGH_RELIABILITY|SEVERE_ARCHITECTURE",prose,re.I),"source identity leakage")
    for u in doc["semantic_units"]:
        for s in u["supports"]:
            require(set(s["resources"]) <= set(RES),"unit resource identity")
            for e in s["evidence"]:
                validate_span(e)
            require(s["resources"] == sorted({e["address"] for e in s["evidence"] if e["origin"] == "RESOURCE"}),"unit support resources")
    for ob,alts in doc["witnesses_by_obligation"].items():
        require(ob in OBS and alts,"obligation alternatives")
        for a in alts:
            require(set(a["resources"]) <= set(RES),"witness resource identity")
            require(a["member_semantics"] == "ALL" and a["alternative_semantics"] == "ANY","witness logic")
    if compare:
        require(canonical(doc) == canonical(document()),"deterministic semantic reconstruction")


def hash_manifest(files):
    body={"schema":"case-0012-reconciliation-hashes-v1","algorithm":"SHA-256","files":{n:sha(b) for n,b in sorted(files.items())},
          "scope":"Physical builder and four generated scientific outputs. This manifest seals its canonical body separately. Operational .local handoff excluded."}
    return dict(body,payload_sha256=sha(canonical(body)))


def validate_hashes(h, files):
    require(h["payload_sha256"] == sha(canonical({k:v for k,v in h.items() if k != "payload_sha256"})),"tampered manifest seal")
    require(set(h["files"]) == set(files),"hash manifest scope")
    for n,b in files.items():
        require(h["files"][n] == sha(b),"artifact hash: "+n)


def refuse_existing(paths):
    require(not any(p.exists() or p.is_symlink() for p in paths),"overwrite refused")


def mutation_checks(doc):
    results={}
    def reject(name, change, reseal=False):
        altered=copy.deepcopy(doc)
        change(altered)
        if reseal:
            for d in altered["decisions"]:
                d["decision_sha256"]=sha(canonical({k:v for k,v in d.items() if k != "decision_sha256"}))
        try:
            validate_document(altered)
        except (ValueError,KeyError,TypeError):
            results[name]="REJECTED"
        else:
            raise ValueError("mutation accepted: "+name)
    reject("missing_decision",lambda d:d["decisions"].pop())
    reject("duplicate_decision",lambda d:d["decisions"].append(copy.deepcopy(d["decisions"][0])))
    reject("unknown_proposition",lambda d:d["decisions"][0].update(proposition_identity="0"*64),True)
    reject("invalid_decision",lambda d:d["decisions"][0].update(decision="AGREE_BY_MAJORITY"),True)
    reject("altered_evidence_identity",lambda d:d["decisions"][0]["repository_evidence"][0].update(content_identity="0"*64),True)
    reject("unknown_evidence_resource",lambda d:d["decisions"][0]["repository_evidence"][0].update(address="unknown/resource.py"),True)
    reject("invalid_support_span",lambda d:d["decisions"][0]["repository_evidence"][0].update(start=-1),True)
    reject("wrong_span_text",lambda d:d["decisions"][0]["repository_evidence"][0].update(text="altered"),True)
    reject("altered_judgment_without_hash_update",lambda d:d["decisions"][0]["final_reconciled_judgment"].update(altered=True))
    reject("altered_judgment_with_hash_update",lambda d:d["decisions"][0]["final_reconciled_judgment"].update(altered=True),True)
    reject("prohibited_identity_leakage",lambda d:d["decisions"][0].update(rationale="PRIMARY is authoritative"),True)
    reject("packet_identity_tamper",lambda d:d["packet_identity"].update(canonical_payload_sha256="0"*64),True)
    fake_files={"reconciliation.json":canonical(doc)}
    h=hash_manifest(fake_files)
    h["files"]["reconciliation.json"]="0"*64
    for name,reseal in (("tampered_hashes",False),("tampered_hashes_resealed",True)):
        if reseal:
            h["payload_sha256"]=sha(canonical({k:v for k,v in h.items() if k != "payload_sha256"}))
        try:
            validate_hashes(h,fake_files)
        except ValueError:
            results[name]="REJECTED"
        else:
            raise ValueError("hash mutation accepted")
    try:
        refuse_existing([ROOT/"reconciliation_builder.py"])
    except ValueError:
        results["existing_output_overwrite"]="REJECTED"
    else:
        raise ValueError("overwrite test failed")
    return dict(sorted(results.items()))


def construct():
    doc=document()
    validate_document(doc)
    mutations=mutation_checks(doc)
    validation={"schema":"case-0012-reconciliation-validation-v1","status":"PASS",
                "initial_validator":"PASS; NO RECONCILIATION (run before outputs)",
                "initial_whitelist":sorted(INPUT_HASHES),"initial_directories":[],"initial_links_or_reparse_points":[],
                "checks":{"exact_packet_identity":"PASS","exact_proposition_inventory":"148 unique, 148 expected",
                          "decision_vocabulary":"PASS","resource_identities":"PASS","support_spans":"PASS",
                          "anonymous_provenance":"PASS","deterministic_json_reconstruction":"PASS",
                          "deterministic_markdown":"PASS","witness_minimality_and_completeness":"PASS",
                          "cell_witness_consistency":"PASS","input_byte_preservation":"PASS",
                          "output_hashes":"PASS on verify","overwrite_refusal":"PASS"},
                "adversarial_checks":mutations,"counts":doc["counts"],"original_file_sha256":INPUT_HASHES,
                "replay_contract":"A separate python -B process reconstructs all generated scientific bytes and compares them to disk; no replay output directory is created.",
                "blindness":doc["blindness_attestation"],"unresolved":0}
    files={"reconciliation.json":canonical(doc),"RECONCILIATION_REVIEW.md":markdown(doc),
           "reconciliation_method.md":METHOD.encode(),"reconciliation_validation.json":canonical(validation)}
    h=hash_manifest(dict(files,**{"reconciliation_builder.py":(ROOT/"reconciliation_builder.py").read_bytes()}))
    files["reconciliation_hashes.json"]=canonical(h)
    return files


def verify():
    load_packet()
    files=construct()
    for n,b in files.items():
        require((ROOT/n).read_bytes() == b,"separate-process exact byte replay: "+n)
    doc=json.loads((ROOT/"reconciliation.json").read_bytes())
    validate_document(doc)
    h=json.loads((ROOT/"reconciliation_hashes.json").read_bytes())
    scope={n:(ROOT/n).read_bytes() for n in h["files"]}
    validate_hashes(h,scope)
    return {"status":"PASS","separate_process_exact_byte_equality":True,
            "scientific_sha256":{n:sha((ROOT/n).read_bytes()) for n in ("reconciliation_builder.py",)+OUTPUTS},
            "counts":doc["counts"],"task_sufficiency":doc["task_sufficiency"],
            "adversarial_rejections":len(mutation_checks(doc)),"original_bytes_preserved":True}


def main():
    mode=sys.argv[1] if len(sys.argv)>1 else "verify"
    if mode == "build":
        refuse_existing([ROOT/n for n in OUTPUTS])
        require(not (ROOT/".local").exists(),"premature operational handoff")
        files=construct()
        for n,b in files.items():
            with (ROOT/n).open("xb") as stream:
                stream.write(b)
        child=subprocess.run([sys.executable,"-B",str(ROOT/"reconciliation_builder.py"),"verify"],cwd=ROOT,capture_output=True)
        require(child.returncode == 0,"separate process verification failed: "+child.stderr.decode(errors="replace"))
        sys.stdout.buffer.write(child.stdout)
    elif mode == "verify":
        sys.stdout.buffer.write(canonical(verify()))
    else:
        raise ValueError("mode must be build or verify")


if __name__ == "__main__":
    main()
