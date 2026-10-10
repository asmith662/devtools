"""Deterministic PRIMARY adjudication builder; Python standard library only."""
from __future__ import annotations

import ast
import collections
import gzip
import hashlib
import itertools
import json
import re
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_ROOT = Path('C:/Users/recoveryadmin/CodexSterile/case_0012_stage_c_2cbc95afb120')
ORIGINALS = ['README.md', 'integrity.json', 'manifest.json', 'resources.json.gz', 'validate_packet.py']
EXPECTED = {
    'archive_sha256': '2cbc95afb120c920ed8d919e37a187f8fe0eec4618eff28eb25203d108599fe3',
    'canonical_payload_sha256': 'c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce',
    'manifest_sha256': '15c886a8af33bf2ba12c2a92e82ec3a33789a605064bded6f17ae4b603d579cf',
    'integrity_sha256': '89947624937675a94d6228e3c6fc6c206bc929600b4f21faf2f5cf22bf78a6f9',
}
OUTPUTS = ['stage_c_review.json', 'stage_c_statistics.json', 'STAGE_C_REVIEW.md',
           'stage_c_validation.json', 'stage_c_hashes.json', 'stage_c_method.md']
LABELS = ['REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY', 'UNRESOLVED']
KEYS = ['source', 'choices', 'integrity', 'materialization', 'assembly', 'exports', 'tests', 'documentation', 'validation']

def raw_json(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n').encode('utf-8')

def sha(value):
    return hashlib.sha256(value).hexdigest()

def native_digest(*values):
    h = hashlib.sha256()
    for value in values:
        encoded = value.encode('utf-8')
        h.update(len(encoded).to_bytes(8, 'big'))
        h.update(encoded)
    return h.hexdigest()

def packet():
    assert ROOT == EXPECTED_ROOT and Path.cwd() == ROOT
    assert not ROOT.is_symlink() and not (getattr(ROOT.stat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    raw = {name: (ROOT / name).read_bytes() for name in ORIGINALS}
    integrity = json.loads(raw['integrity.json'])
    manifest = json.loads(raw['manifest.json'])
    expanded = gzip.decompress(raw['resources.json.gz'])
    p = json.loads(expanded)
    assert raw_json(p) == expanded
    actual = dict(archive_sha256=sha(raw['resources.json.gz']), canonical_payload_sha256=sha(expanded),
                  manifest_sha256=sha(raw['manifest.json']), integrity_sha256=sha(raw['integrity.json']))
    assert actual == EXPECTED
    for name, digest in integrity['sha256'].items():
        assert sha(raw[name]) == digest
    assert p['case'] == manifest['case'] == 'case-0012'
    assert p['task_identity'] == manifest['task_identity'] == 'case-0012-direct-source-disclosure'
    assert p['frame'] == manifest['frame']
    assert set(p) == {'case', 'task_identity', 'task_text', 'obligations', 'resources', 'frame'}
    assert [o['key'] for o in p['obligations']] == KEYS
    assert len(p['resources']) == 531 and len(p['obligations']) == 9
    assert len({r['address'] for r in p['resources']}) == 531
    for o in p['obligations']:
        assert set(o) == {'identity', 'key', 'statement', 'criterion', 'applicability', 'task_basis'}
        for b in o['task_basis']:
            assert p['task_text'][b['start']:b['end']] == b['text']
    for r in p['resources']:
        assert set(r) == {'address', 'content_identity', 'text', 'encoding', 'byte_size', 'document_identity'}
        assert len(r['text'].encode('utf-8')) == r['byte_size']
        assert native_digest('decoded-utf8-text-sha256-v1', r['text']) == r['content_identity']
        assert native_digest('whole-resource-exact-text-v1', p['frame']['repository_id'], r['address'], r['content_identity']) == r['document_identity']
    assert len({r['document_identity'] for r in p['resources']}) == 531
    frame_values = [v for r in sorted(p['resources'], key=lambda r: r['address']) for v in (r['address'], r['content_identity'])]
    assert native_digest('explicit-required-text-resources-sha256-v1', p['frame']['repository_id'], *frame_values) == p['frame']['snapshot_id']
    return p, {name: sha(raw[name]) for name in ORIGINALS}

P, ORIGINAL_HASHES = packet()
RS = P['resources']
OS = {o['key']: o for o in P['obligations']}
PROVENANCE = {'canonical_payload_sha256': EXPECTED['canonical_payload_sha256'], 'frame': P['frame'],
              'authorship': 'PRIMARY treatment-blind semantic adjudication in this session'}

def span(i, begin=None, end=None):
    r = RS[i]
    t = r['text']
    s = t.index(begin) if begin is not None else 0
    e = t.index(end, s + len(begin)) if end is not None else len(t)
    assert 0 <= s < e <= len(t)
    return {'kind': 'resource', 'address': r['address'], 'document_identity': r['document_identity'],
            'content_identity': r['content_identity'], 'start': s, 'end': e, 'text': t[s:e],
            'coordinate_system': 'zero-based Unicode character offsets; half-open', 'provenance': PROVENANCE}

def symbol(i, name):
    t = RS[i]['text']
    nodes = [n for n in ast.walk(ast.parse(t)) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == name]
    assert len(nodes) == 1, (i, name)
    n = nodes[0]
    lines = t.splitlines(keepends=True)
    first = min([n.lineno] + [d.lineno for d in n.decorator_list])
    start = sum(map(len, lines[:first - 1]))
    end = sum(map(len, lines[:n.end_lineno]))
    evidence = span(i)
    evidence.update(start=start, end=end, text=t[start:end])
    return evidence

def task_span(text):
    t = P['task_text']
    s = t.index(text)
    return {'kind': 'task', 'task_identity': P['task_identity'], 'start': s, 'end': s + len(text),
            'text': text, 'coordinate_system': 'zero-based Unicode character offsets; half-open', 'provenance': PROVENANCE}

UNITS = []

def unit(key, local, statement, scope, why, options, task_text=None, inferability=None):
    uid = f'{key}.{local}'
    support = []
    for n, evidence in enumerate(options, 1):
        support.append({'identity': f'{uid}.support-{n:02}', 'resources': sorted({e['address'] for e in evidence if e['kind'] == 'resource'}),
                        'evidence': evidence, 'mode': 'INFERABLE' if inferability else 'DIRECT',
                        'inferability_rationale': inferability or 'The cited retained text states or implements this fact directly.'})
    if task_text:
        # Task evidence is an admissible foundation, not a repository resource.
        evidence = [task_span(task_text)]
        support.append({'identity': f'{uid}.support-task', 'resources': [], 'evidence': evidence,
                        'mode': 'DIRECT', 'inferability_rationale': 'The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.'})
    assert support
    UNITS.append({'identity': uid, 'obligation': OS[key]['identity'], 'statement': statement, 'semantic_scope': scope,
                  'why_necessary': why, 'supports': support, 'provenance': PROVENANCE,
                  'granularity_audit': 'One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.'})

# Source scope, selection and native subject/containment contracts.
unit('source', 'selector', 'Exact kind/name selection in one retained interpreted module returns all native direct class or sync/async function declarations, including decorated and repeated declarations, without binding resolution.',
     'Canonical direct-source selector contract', 'The task expressly requires reusing this selector and retaining source identities rather than runtime bindings.',
     [[symbol(158, 'select_python_module_source_declarations'), symbol(158, 'PythonModuleSourceDeclarationSelection')],
      [span(154, '## Exact source declaration selection', "Localization's")]])
unit('source', 'function-identity', 'A direct function is native knowledge with derivation identity, structural subject bound to snapshot/definition/resource dependency/ordinal, and a source occurrence; its name alone is not identity.',
     'Direct module-body function identity and provenance', 'Caller choices and repeated declarations need the actual native identity and support contract.',
     [[symbol(136, 'PythonFunctionSubject'), symbol(136, 'PythonFunctionDeclarationKnowledge'), symbol(136, 'PythonModuleResourceDependency')]])
unit('source', 'class-method-identity', 'A direct module class has a native structural subject; a direct sync/async method has a distinct subject bound to its containing class and per-class ordinal, plus one native containing_class link.',
     'Class and direct-method subject/parent contract', 'A method choice must retain its exact native parent rather than infer runtime ownership or use a bare name.',
     [[symbol(130, 'PythonClassSubject'), symbol(130, 'PythonMethodSubject'), symbol(130, 'PythonMethodDeclarationKnowledge')],
      [span(131, '## Identity, provenance, and containment', '## Bounded direct-base resolution')]])
unit('source', 'containment', 'The native class/method containment builder validates supplied analyses against retained state, then navigates direct methods and their established lexical class parent; unselected declarations fail.',
     'Native method containment admission and navigation', 'The task restricts method support to validated native class-parent containment.',
     [[symbol(129, 'build_python_class_method_containment_view'), symbol(129, 'PythonClassMethodContainmentView')],
      [span(131, '`PythonMethodDeclarationKnowledge.containing_class`', 'Successful coverage')]])
unit('source', 'excluded-resolution', 'Source disclosure must not resolve runtime attributes, imported facades, inherited methods, or semantic targets.',
     'Explicit negative feature scope', 'The task makes these boundaries mandatory.', [],
     'without runtime attribute, imported-facade, inherited-method or semantic resolution.')

# Explicit integration contracts and existing choices.
unit('choices', 'plan', 'The immutable plan binds nonblank purpose, repository/snapshot, ordered nonempty choices and optional lineage; mixed applicability and duplicate identical choices fail, and identity includes choice order.',
     'One purpose/frame/order plan invariant', 'The new choice must preserve the actual existing plan contract.',
     [[symbol(123, 'DisclosurePlan'), symbol(123, 'plan_disclosures')]])
unit('choices', 'admission', 'Each admitted concrete choice provides purpose, frame, representation, deterministic identity and materialize(snapshot) returning a common item through PlannedDisclosure.',
     'Common concrete-choice participation protocol', 'The new option needs the existing semantic admission seam.', [[symbol(123, 'PlannedDisclosure')]])
unit('choices', 'whole-compatibility', 'WholeResourceDisclosureOption is an explicit coarse retained-resource choice with resource/frame identity, validated snapshot materialization, and common item provenance; it remains distinct from declaration disclosure.',
     'Existing whole-resource choice boundary', 'Compatibility must preserve the coarse choice without turning it into an implicit fallback.',
     [[symbol(125, 'WholeResourceDisclosureOption'), symbol(125, 'choose_whole_resource_disclosure')]])
unit('choices', 'reference-compatibility', 'The existing qualified-reference option adapts its purpose/frame/identity and delegates to its validated Python materializer/renderer before returning a common item with both owner addresses/content identities and native provenance.',
     'Existing qualified-reference common-plan adapter', 'Compatibility includes this native delegation boundary rather than replacing it with new source-choice resolution.',
     [[symbol(140, 'PythonQualifiedReferenceDisclosureOption'), symbol(140, 'choose_python_qualified_reference_disclosure')]])
unit('choices', 'caller-selection', 'Choice integration remains caller-selected and performs no automatic retrieval or selection.',
     'Explicit feature admission policy', 'The feature explicitly forbids automatic choice.', [], 'without automatic retrieval or selection.')

# Retained-frame integrity and publication.
unit('integrity', 'lookup', 'resource_at(address) returns the retained occurrence at that exact address and raises ValueError for an absent address, without file acquisition.',
     'Retained snapshot lookup contract', 'The task expressly binds every resource validation to this method.', [[symbol(181, 'resource_at')]])
unit('integrity', 'selection-frame', 'Canonical direct-source selection checks module repository, snapshot and exact resource equality against resource_at before deriving declarations from retained content.',
     'Module/frame/content validation before source selection', 'Foreign/stale module inputs must not become disclosure support.',
     [[symbol(158, 'select_python_module_source_declarations')], [span(154, '## Exact source declaration selection', 'Direct decorated')]])
unit('integrity', 'method-frame', 'Validated class/method containment checks exact retained resource equality, coverage, derivation, subject ordinals, support frame/address and method parent consistency.',
     'Native class-parent validation details', 'The task requires validating supplied method and parent support, not accepting nominal names.',
     [[symbol(129, 'build_python_class_method_containment_view')]])
unit('integrity', 'canonical-membership', 'Supplied declaration identity/scope must agree with canonical native declarations reproduced from retained content; structurally stamped containment alone does not prove source-range/name authenticity.',
     'Native declaration authenticity at admission', 'The task requires rejecting unsupported scope and mismatched native declaration identity.',
     [[symbol(158, 'select_python_module_source_declarations'), symbol(129, 'build_python_class_method_containment_view')]],
     inferability='The selector reproduces canonical facts from retained content. The containment validator checks provenance fields but does not reparse or compare every range/name; full canonical membership/equality is the necessary admission check inferred from the task and these mechanisms. No existing source-choice implementation is claimed.')
unit('integrity', 'publication', 'Common materialization checks plan frame and each returned option identity/representation before returning ContextDisclosure; incomplete or mismatched materialization cannot publish a disclosure.',
     'Atomic ordered publication boundary', 'The task requires all rejection checks before disclosure publication.',
     [[symbol(122, 'materialize_disclosure_plan'), symbol(122, 'ContextDisclosure')],
      [symbol(383, 'test_materialization_rejects_an_option_that_changes_its_plan'), symbol(383, 'test_realized_context_rejects_items_outside_the_plan'), symbol(383, 'test_whole_resource_rejects_stale_or_missing_state')]])

# Exact materialization and provenance are distinct necessary facts.
unit('materialization', 'coordinates', 'Native source ranges use one-based lines, zero-based UTF-8 byte columns and exclusive ends.',
     'Python occurrence coordinate semantics', 'Exact source extraction cannot interpret UTF-8 columns as character offsets.',
     [[symbol(136, 'PythonSourceRange')], [span(131, 'Every class and method retains', 'AST declaration spans')]])
unit('materialization', 'extraction', 'The existing source extractor computes retained UTF-8 absolute offsets with line endings intact, rejects reversed/out-of-bounds ranges and invalid UTF-8 boundaries, and decodes only the exact selected byte segment.',
     'Exact source segment algorithm and failure boundaries', 'CRLF/non-ASCII fidelity and invalid-range rejection require the actual byte-boundary semantics.',
     [[symbol(139, '_extract_source_segment'), symbol(139, '_absolute_byte_offset')]])
unit('materialization', 'decorator-boundary', 'Existing native declaration ranges begin at class/def/async def and exclude preceding decorators; decorator-preserving disclosure therefore needs an explicit faithful extension or additional source-range provenance.',
     'Native range versus decorator-inclusive requested representation', 'The task requires decorators, and a literal existing-range slice would omit them.',
     [[span(131, 'AST declaration spans begin', '```text')],
      [symbol(136, 'derive_python_function_declarations'), symbol(130, '_occurrence'), symbol(130, 'derive_python_class_method_declarations')]],
     inferability='The native range starts at the declaration AST node. Its stated exclusion and task decorator requirement imply additional explicitly accounted representation work; no undocumented decorator-inclusive native range is assumed.')
unit('materialization', 'item-provenance', 'A common materialized item carries option identity, representation, owner addresses/content identities, text and native provenance, while ContextDisclosure retains the plan and aligned items.',
     'Realized declaration representation and supporting provenance carrier', 'The task places native derivation/range/owner support inside ContextDisclosure through the existing item carrier.',
     [[symbol(122, 'MaterializedDisclosureItem'), symbol(122, 'ContextDisclosure')]])
unit('materialization', 'mixed-order', 'Common materialization appends exactly one item per planned choice in caller order, without implicit owner expansion or re-selection.',
     'Mixed-plan exact realization order', 'New declarations must coexist faithfully with old representations.',
     [[symbol(122, 'materialize_disclosure_plan')], [symbol(383, 'test_mixed_plan_preserves_purpose_sources_and_request')]])
unit('materialization', 'bounded-meaning', 'Exact source realization must not infer sufficiency or implicitly expand to the whole owner resource.',
     'Source-choice representation fidelity', 'These are mandatory feature boundaries rather than additional implementation facts.', [],
     'without inferring sufficiency or expanding to whole owners implicitly.')

unit('assembly', 'rendering', 'The common renderer consumes realized items in plan order, adds common metadata and item text, and retains the exact ContextDisclosure.',
     'Current common rendering behavior', 'The new choice must preserve common presentation compatibility.', [[symbol(124, 'render_context_disclosure'), symbol(124, 'RenderedContextDisclosure')]])
unit('assembly', 'request-copy', 'The common assembler places unchanged task text before rendered Context and uses dataclass replacement to create a new prompt with the original role, retaining every other request field including tools.',
     'Pure copied-request assembly', 'The task explicitly requires original request, role, settings, conversation, provider settings and tools preservation.',
     [[symbol(124, 'assemble_context_disclosure_model_request')]],
     inferability='The code explicitly reuses the original prompt role and calls replace(task_request, prompt=...). The task supplies the required field inventory; replacing only prompt retains other fields, including tools. The original immutable request is not mutated.')
unit('assembly', 'no-budget', 'The feature introduces no new budget or truncation policy.', 'Assembly policy boundary', 'This is a mandatory preservation constraint.', [], 'introduce no new budget or truncation policy.')

unit('exports', 'planning-surface', 'The common planning initializer explicitly imports its public choices and realization APIs and lists them in __all__; this is the new choice exposure seam.',
     'Common planning public API surface', 'Actual current export structure is needed to extend both public boundaries compatibly.', [[span(120)]])
unit('exports', 'outer-surface', 'The outer Context facade re-exports common planning values/functions and qualified-reference choices through explicit imports and __all__.',
     'Outer Context public API surface', 'The task requires adding exposure at this second distinct boundary.',
     [[span(83, 'from devtools.context.planning import', 'from devtools.context.python import'), span(83, '__all__ =')]])
unit('exports', 'option-ownership', 'Language-specific choices participate through the common PlannedDisclosure protocol; its contract does not require common planning to parse Python or depend on Retrieval.',
     'Dependency ownership through concrete-choice protocol', 'Permitted direction requires the existing structural participation seam.', [[symbol(123, 'PlannedDisclosure')]],
     inferability='The protocol accepts frame/representation values and a materialize method rather than Python declarations or retrieval values. The explicit task dependency prohibition therefore fits a Python-owned concrete adapter, with public exposure through the common API.')
unit('exports', 'assembly-ownership', 'Common rendering/request assembly depends on realized common disclosure and ModelRequest/Prompt, with no Retrieval calls or Python-specific parsing/resolution.',
     'Common assembly dependency boundary', 'The task forbids moving language-specific logic into common assembly.', [[span(124)]])

for local, statement, excerpt in [
    ('direct-choices', 'Tests must exercise direct function, class and validated direct-method choices.', 'direct function/class/method choices'),
    ('decorated-repeated', 'Tests must exercise decorated and repeated native declarations without runtime-binding substitution.', 'decorated and repeated declarations'),
    ('mixed-fidelity', 'Tests must exercise mixed-plan ordering and exact selected source/provenance, including the task-mandated UTF-8, CRLF and decorator fidelity.', 'mixed-plan ordering and exact source/provenance'),
    ('rejection', 'Tests must exercise stale, foreign and missing-resource rejection.', 'stale/foreign/missing-resource rejection'),
    ('existing-choices', 'Regression tests must preserve existing qualified-reference and whole-resource choices.', 'unchanged existing choices'),
    ('request-preservation', 'Regression tests must preserve copied requests and the original request, role and all non-prompt fields.', 'copied-request preservation.')]:
    unit('tests', local, statement, 'Mandatory test coverage category', 'This category is expressly required by the feature task; existing test examples are replaceable.', [], excerpt)

unit('documentation', 'package-baseline', 'The package overview currently describes only qualified-reference and whole-resource choices and says the common protocol permits its two current consumers, while preserving caller direction and native provenance.',
     'Package documentation claims that must evolve with the feature', 'Updating the package accurately requires identifying these concrete implemented-scope claims, not merely its filename.',
     [[span(121, 'DisclosurePlan binds', 'The caller may construct')]])
unit('documentation', 'architecture-baseline', 'The architecture separates native referents from capacity-consuming representations and Localization resolution from Context admission, while identifying the implemented plan as narrower than general planning with only reference and whole-resource forms.',
     'Cross-package architectural status claims to preserve/update', 'The architecture update must preserve ownership/status distinctions and accurately extend its current representation inventory.',
     [[span(2, '## Accepted Context and disclosure semantics', 'Every disclosure stage preserves')]])
unit('documentation', 'scope-claims', 'Documentation must distinguish source identities from runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.',
     'Mandatory content of both requested documentation updates', 'The feature task fixes these claims and exclusions.', [],
     'to explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.')

unit('validation', 'protected-profile', 'The documented protected development entry runs tests/ while excluding tests/experiments/ before collection, preserves pytest configuration and returns pytest failure status; confirmation is outside ordinary development validation.',
     'Protected test selection and invocation boundary', 'The task requires this documented protected profile, not outcome-dependent selection.',
     [[span(60, '## Protected development test profile', '## Other quality gates')],
      [symbol(65, 'pytest_arguments'), symbol(65, 'main'), span(0, 'The canonical protected development test profile', 'For read-only audits:')]])
unit('validation', 'pytest-coverage', 'Actual pytest settings select tests with strict config/markers and devtools branch coverage at a 100% threshold; coverage run/report settings also retain branch/source and fail_under=100.',
     'Actual protected configuration to preserve', 'The task specifically requires retaining pyproject test/coverage settings, and only the concrete config fixes its exact values.',
     [[span(64, '[tool.pytest.ini_options]', '[tool.ruff]')]])
unit('validation', 'static-config', 'Actual static configuration selects Ruff py312, 88 columns, ALL lint with D203/D213 and test S101 exceptions, and strict mypy for Python 3.12 over src/tests/experiments with explicit package bases and src path.',
     'Existing lint/format/type configuration', 'Running the required lint/format and strict type profile must preserve the actual configured scope and settings.',
     [[span(64, '[tool.ruff]')]])
unit('validation', 'quality-commands', 'The documented separate gates are uv run ruff check ., uv run ruff format --check, uv run mypy, git diff --check, and git diff --cached --check for the staged/index view.',
     'Documented complete static and whitespace command contract', 'The task explicitly requires the documented profile and both whitespace views.', [[span(60, '## Other quality gates')]])

HELPFUL = []
def helpful(key, i, evidence, rationale):
    assert all(e['address'] == RS[i]['address'] for e in evidence)
    HELPFUL.append({'obligation': OS[key]['identity'], 'address': RS[i]['address'], 'evidence': evidence, 'rationale': rationale})

# Useful evidence remains optional when it does not supply a unique required fact.
helpful('source', 153, [symbol(153, 'lookup_python_module_declaration')], 'The competing binding-oriented API illustrates why decorated/repeated source selection must not use unique runtime-like binding policy; the canonical selector already establishes the needed boundary.')
helpful('source', 138, [span(138, '## Direct declaration containment', '## Context disclosure')], 'Explains intrinsic function ownership and source-versus-binding scope; native identity schema and selector already supply the required facts.')
helpful('source', 135, [symbol(135, 'build_python_function_declaration_containment_view')], 'A validated function-ownership navigation example is useful, but direct function selection already carries native owner support and the task only mandates the native method-parent route.')
helpful('source', 155, [symbol(155, 'PythonModuleInterpretation')], 'Defines the retained module interpretation input. The needed frame/resource fields are already exposed by the selector and task; no new root discovery is required.')
helpful('source', 409, [symbol(409, 'test_plain_and_decorated_native_identity'), symbol(409, 'test_exact_kind_scope_and_repeated_declarations')], 'Concrete cases corroborate decorated and repeated native source identities; they do not replace the full selected native function subject schema.')
helpful('choices', 121, [span(121, 'DisclosurePlan binds', 'Implemented choices:')], 'Summarizes the common plan and materialization contracts, but does not replace the exact admission protocol/invariants and old adapters.')
helpful('choices', 138, [span(138, 'choose_python_qualified_reference_disclosure now')], 'Corroborates unchanged qualified-reference adaptation without independently providing the complete common item contract.')
helpful('choices', 141, [symbol(141, 'disclose_python_qualified_reference'), symbol(141, 'materialize_python_qualified_reference_source')], 'Underlying reference implementation adds useful rejection details. The adapter delegates unchanged, so re-establishing its entire resolver is not necessary for adding the direct-source choice.')
helpful('integrity', 135, [symbol(135, 'build_python_function_declaration_containment_view')], 'Useful provenance checks for supplied function analyses; canonical selector membership and native dependency facts already establish the mandatory validation strategy.')
helpful('integrity', 125, [symbol(125, 'WholeResourceDisclosureOption')], 'Provides a retained-resource validation pattern; resource_at and native selector/containment already establish required facts.')
helpful('integrity', 141, [symbol(141, 'materialize_python_qualified_reference_source')], 'Corroborates validation before exact extraction; imported-reference route is preserved rather than required for new direct-source admission.')
helpful('materialization', 140, [symbol(140, 'PythonQualifiedReferenceDisclosureOption')], 'Concrete common-item native provenance example; the common carrier and native source contracts suffice.')
helpful('materialization', 125, [symbol(125, 'WholeResourceDisclosureOption')], 'Shows exact retained CRLF-bearing whole-resource realization; this is a different representation and cannot be necessary for exact declaration extraction.')
helpful('materialization', 383, [symbol(383, 'test_mixed_plan_preserves_purpose_sources_and_request')], 'Existing mixed-plan CRLF/non-ASCII regression is useful; the common item/publication carrier already entails caller order in every complete alternative, so this duplicate order evidence is optional.')
helpful('assembly', 255, [symbol(255, 'ModelRequest')], 'Corroborates the typed field inventory and immutability. The task names preserved fields and the common replace-only-prompt implementation preserves all of them.')
helpful('assembly', 257, [symbol(257, 'Prompt')], 'Corroborates the immutable content/role value; those fields are directly used in the necessary common assembler.')
helpful('assembly', 143, [symbol(143, 'assemble_python_function_context_model_request')], 'Older language-specific assembly demonstrates the same copy pattern; preserving common assembly requires its own renderer/assembler.')
helpful('assembly', 383, [symbol(383, 'test_mixed_plan_preserves_purpose_sources_and_request')], 'Corroborates original request, role and settings preservation but does not supply a complete common rendering contract.')
helpful('exports', 122, [symbol(122, 'materialize_disclosure_plan')], 'Shows generic option dispatch as a dependency ownership example. The public surfaces, protocol, and common assembly already supply the required seams.')
helpful('exports', 140, [symbol(140, 'PythonQualifiedReferenceDisclosureOption')], 'Provides an existing Python-owned adapter pattern; no redesign of this adapter is required.')
helpful('documentation', 131, [span(131, '## Identity, provenance, and containment', '## Bounded direct-base resolution')], 'Supplies supported/deferred Python source scope to explain in the requested documents; those semantic units are established independently under source/materialization and the task fixes the required claims.')
helpful('documentation', 154, [span(154, '## Exact source declaration selection', "Localization's")], 'Useful wording for source versus binding semantics; the package/architecture baseline claims and task requirements determine this documentation obligation.')
helpful('documentation', 61, [span(61, 'The [Context Planning package', 'The adjacent `context.python.imports`')], 'The map provides navigation/context; it is not a requested update and does not supply a unique mandatory documentation fact.')
helpful('validation', 65, [symbol(65, 'pytest_arguments'), symbol(65, 'main')], 'Confirms actual protected selection and failure propagation. The required documented commands already entail the full profile in docs/development/validation.md, making the script redundant in minimal alternatives.')
helpful('validation', 0, [span(0, 'The canonical protected development test profile', 'For read-only audits:')], 'Corroborates protected selection/confirmation separation, but the documented commands already cover these facts. Repository operating prose is evidence here, not an instruction to access Git.')
helpful('validation', 524, [symbol(524, 'test_profile_selects_tests_and_excludes_experiment_tests_before_collection'), symbol(524, 'test_profile_propagates_pytest_failure_code')], 'Corroborates the protected entry behavior; existing tests are not required evidence for preserving a documented/configured validation profile.')

for key, i, names, reason in [
    ('tests', 383, ['test_mixed_plan_preserves_purpose_sources_and_request', 'test_materialization_rejects_an_option_that_changes_its_plan'], 'Reusable mixed-plan, rejection and copied-request regression examples; the mandatory test categories are fully fixed by the task.'),
    ('tests', 409, ['test_plain_and_decorated_native_identity', 'test_exact_kind_scope_and_repeated_declarations', 'test_selection_rejects_invalid_and_foreign_inputs'], 'Native source-selector fixture and decorated/repeated/foreign cases; a useful test convention rather than necessary evidence.'),
    ('tests', 387, ['test_direct_classes_methods_exclusions_and_existing_function_contract', 'test_containment_rejects_inconsistent_native_facts'], 'Direct class/method containment regression examples; equivalent focused cases can be written from native contracts.'),
    ('tests', 393, ['test_multiple_same_name_direct_declarations_have_distinct_subjects', 'test_source_range_uses_utf8_byte_columns'], 'Repeated subject and UTF-8 occurrence examples; no requirement to reuse these exact tests.'),
    ('tests', 395, ['test_materializes_duplicate_sync_and_async_exact_multiline_source', 'test_rejects_source_ranges_that_cannot_be_faithfully_applied'], 'CRLF/non-ASCII and invalid-range cases corroborate the task test matrix without becoming mandatory repository witnesses.'),
    ('tests', 396, ['test_cross_resource_call_exact_source_and_request', 'test_stale_source_or_target_content_is_rejected'], 'Preserved qualified-reference path regression examples; the task requires behavior preservation, not reading every existing test.'),
    ('tests', 398, ['test_assembles_real_context_after_distinct_unchanged_task'], 'Copied-request regression example from an older Python path; common source and task semantics support a new equivalent test.'),
    ('tests', 473, ['test_model_request_is_immutable_and_separates_input_from_settings', 'test_prompt_is_an_immutable_model_input_without_conversation_identity'], 'Request-value immutability examples; no unique new-choice test requirement originates here.'),
]:
    helpful(key, i, [symbol(i, n) for n in names], reason)

for key in ['choices', 'assembly', 'exports', 'documentation']:
    helpful(key, 6, [span(6, '### Planning versus model-input assembly', '### InformationNeed decomposition')], 'Accepted architectural distinction between selection and assembly is useful background; the task and concrete common contracts already establish the necessary bounded change.')
for key in ['choices', 'materialization', 'documentation']:
    helpful(key, 10, [span(10, '### Context disclosure and assembly', '### Resource')], 'Taxonomy corroborates immutable plan/disclosure and semantic-strength boundaries; it is not necessary merely because it is broad architectural background.')

helpful('choices', 383, [symbol(383, 'test_mixed_plan_preserves_purpose_sources_and_request'), symbol(383, 'test_plan_rejects_mixed_or_duplicate_choices')], 'Regresses existing plan order and old choices, but does not replace the complete choice identity/admission contract.')
helpful('source', 99, [symbol(99, '_ground_declaration'), symbol(99, '_ground_method')], 'An existing consumer demonstrates canonical selector reuse and method-parent containment, without becoming necessary for Context implementation or introducing a Localization dependency.')
helpful('integrity', 99, [symbol(99, '_ground_method')], 'Corroborates canonical parent membership checking after retained-source derivation. The canonical native selector and containment mechanisms already establish the needed strategy.')
helpful('integrity', 179, [symbol(179, '_observe_resource'), symbol(179, '_semantic_digest')], 'Explains the native length-framed content identity of retained resources. The task requires comparison to retained occurrences rather than recomputing observation or reacquiring files, so observation is optional background.')
helpful('choices', 2, [span(2, 'The first common Context Planning foundation now', 'Filesystem Resources remain')], 'Corroborates the bounded explicit plan and two old representations; the concrete protocol/options provide complete necessary contracts.')
helpful('documentation', 63, [span(63, 'The current Context checkpoint establishes', '[Codex dogfood Case 0001]')], 'Corroborates the implemented representation inventory in a continuity document; no roadmap update is required and the requested package/architecture claims suffice.')
helpful('tests', 64, [span(64, '[tool.pytest.ini_options]', '[tool.ruff]')], 'Confirms the configured pytest/strict-marker/coverage convention used to add tests. The mandatory semantic test matrix comes from the task; exact configuration preservation is required separately under validation.')

def split_unit(identity, parts):
    original = next(u for u in UNITS if u['identity'] == identity)
    pos = UNITS.index(original)
    replacement = []
    for local, statement, scope, why in parts:
        u = json.loads(json.dumps(original))
        u['identity'] = identity.split('.')[0] + '.' + local
        u.update(statement=statement, semantic_scope=scope, why_necessary=why,
                 granularity_audit=f'Split from {identity}: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.')
        for n, support in enumerate(u['supports'], 1):
            support['identity'] = f"{u['identity']}.support-{n:02}"
        replacement.append(u)
    UNITS[pos:pos + 1] = replacement

split_unit('choices.plan', [
    ('plan-value', 'The plan is an immutable value retaining purpose, repository/snapshot identities, ordered disclosures and optional preceding-plan lineage.', 'Plan value shape and immutability', 'New concrete choices must participate in this existing immutable value.'),
    ('plan-admission', 'Plan construction rejects blank purpose, empty choices, mixed purpose/repository/snapshot applicability and repeated identical choice identities.', 'Plan admission invariant', 'Integration must preserve actual admissibility rather than silently weaken validation.'),
    ('plan-identity', 'Plan identity is a deterministic length-framed digest of purpose, frame, optional lineage and ordered representation/choice identities.', 'Plan deterministic identity and order', 'Choice/order changes must retain their effect on the existing identity contract.'),
])
split_unit('source.class-method-identity', [
    ('class-identity', 'A direct module-body class has a native structural subject bound to snapshot, parser/definition, exact observed resource dependency and direct-class ordinal.', 'Native class subject identity', 'Repeated same-name classes must remain independently selectable native subjects.'),
    ('method-identity', 'A direct sync/async method has native knowledge/support and a subject bound to its containing class subject and per-class ordinal; containing_class is its canonical lexical-parent link.', 'Native direct-method identity and parent', 'Method support cannot substitute a name or runtime owner for its native lexical parent.'),
])
split_unit('tests.decorated-repeated', [
    ('decorated', 'Tests must exercise decorated native declarations without runtime-binding substitution.', 'Decorated direct-source test coverage', 'Decorator support is expressly required and can fail independently of repeated-name handling.'),
    ('repeated', 'Tests must exercise repeated native declarations as distinct source identities.', 'Repeated declaration test coverage', 'Repeated source identities are expressly required and can fail independently of decorators.'),
])
split_unit('tests.mixed-fidelity', [
    ('mixed-order', 'Tests must exercise caller ordering in mixed declaration/reference/whole-resource plans.', 'Mixed-plan order test coverage', 'Ordering can fail independently of exact source/provenance preservation.'),
    ('exact-fidelity', 'Tests must exercise exact selected source and native provenance, including mandatory UTF-8, CRLF and decorator fidelity.', 'Exact source/provenance test coverage', 'The requested source representation must be verified with its native support, not only its position.'),
])
split_unit('validation.static-config', [
    ('ruff-config', 'Actual Ruff settings select py312, 88 columns, ALL lint with D203/D213 ignored and S101 ignored for tests.', 'Preserved lint/format configuration', 'The requested static checks must retain actual configured lint/format semantics.'),
    ('mypy-config', 'Actual mypy configuration is strict Python 3.12 over src/tests/experiments with explicit package bases and src path.', 'Preserved strict type-checking configuration', 'Strict mypy has a separate scope/configuration from Ruff and protected pytest.'),
])
split_unit('integrity.publication', [
    ('plan-frame', 'Common materialization rejects a supplied snapshot with repository/snapshot identity different from its plan before realizing choices.', 'Plan frame admission before materialization', 'A valid native declaration does not make a foreign or stale overall plan applicable.'),
    ('returned-identity', 'Common materialization and ContextDisclosure alignment require every returned item option identity/representation to equal its planned choice.', 'Returned item identity/representation integrity', 'The task explicitly requires rejecting mismatched returned identity before publication.'),
    ('publication', 'A failed or incomplete materialization must not return a successfully published ContextDisclosure; every aligned ordered item must be realized first.', 'Complete disclosure publication boundary', 'Publication must follow all required validation and successful realization, rather than exposing a partial disclosure.'),
])
split_unit('validation.pytest-coverage', [
    ('pytest-config', 'Actual pytest settings select tests with strict configuration and strict marker checks, retaining the live_codex opt-in marker declaration.', 'Actual test-selection/admission configuration', 'The task requires preserving the concrete test settings in pyproject.toml.'),
    ('coverage-config', 'Actual pytest/coverage settings retain devtools branch coverage, term-missing reporting, a 100% fail threshold, configured source, show_missing=true and skip_covered=false.', 'Actual production coverage configuration', 'The task requires retaining coverage settings independently of test selection and strict marker admission.'),
])
split_unit('tests.direct-choices', [
    ('function-choice', 'Focused tests must exercise direct native function source disclosure choices.', 'Direct function choice test coverage', 'Function support is a separately required positive feature behavior.'),
    ('class-choice', 'Focused tests must exercise direct native class source disclosure choices.', 'Direct class choice test coverage', 'Class support can fail independently of function support.'),
    ('method-choice', 'Focused tests must exercise direct native method source choices admitted through validated native class-parent containment.', 'Direct method choice test coverage', 'Method admission has a distinct mandatory parent/containment boundary.'),
])

next(u for u in UNITS if u['identity'] == 'choices.plan-identity')['supports'][0]['evidence'].append(symbol(123, '_digest'))
next(u for u in UNITS if u['identity'] == 'tests.exact-fidelity')['supports'][0]['evidence'].append(task_span('preserve UTF-8 boundaries, decorators, CRLF/non-ASCII bytes'))
next(u for u in UNITS if u['identity'] == 'tests.request-preservation')['supports'][0]['evidence'].append(task_span('original request, prompt role, settings, conversation, provider settings and tools remain unchanged except the copied prompt'))

METHOD = '''# PRIMARY blind Stage C method

Evidence was limited to the five initially present packet files in the verified
flat sterile workspace. The supplied validator ran as `python -B validate_packet.py`
before any output creation. Original compressed, canonical payload, manifest,
integrity and individual packet-file digest scopes were verified and retained.
Native content/document/snapshot identities were also reproduced using their
frozen length-framed semantic SHA-256 formulas, distinct from raw file hashes.
Repository resources are frozen text evidence; none was imported or executed as
repository code. No repository checkout, Git, parent/sibling file or web access
was used. Source-head metadata was retained only as supplied frame provenance.

The exact task, nine obligations, criteria, applicability and task-basis spans
were reconstructed unchanged. The task interpretation audit precedes resource
labeling and partitions all substantive clauses. All obligations are applicable.
The frame remains all 531 addressed, content/document-qualified resources.
Every one of the 4,779 obligation/resource cells retains a rationale.

All retained texts were processed for content scope; Python module docstrings,
native declarations and relevant bodies, and Markdown headings/relevant sections
were inspected. Domain-scoped negative judgments use actual content summaries,
not lexical proximity. Relevant interfaces, native identity/range/containment,
materializers, public facades, configuration and documentation claims were read
directly. Existing regression examples were inspected as optional evidence.

REQUIRED means membership in at least one complete minimal evidence alternative
for a necessary semantic unit. It does not mean every positive resource is
simultaneously necessary. HELPFUL_ONLY corroborates or illustrates a contract
without belonging to a minimal alternative. UNNECESSARY supplies no needed or
specifically useful fact for that obligation within the bounded change.
UNRESOLVED is reserved for genuinely undecidable cells; none remains here.
Task-backed requirements may have no required repository-resource member. The
mandatory test matrix is such a case: no particular old test is necessary solely
because tests are requested. Required does not mean that future implementation
has already satisfied the feature.

Units describe semantic facts independently of answer locations. Source identity,
native membership, choice admission, exact byte extraction and actual export/
configuration/documentation claims are distinct. Granularity was audited and
separable identity/admission/configuration/test facts were split. Evidence spans
use zero-based Unicode character offsets with exclusive ends; original task and
resource text is preserved. These adjudication offsets are different from the
Python native one-based-line/zero-based-UTF-8-byte source range contract.

Each unit has directly established or explicitly justified inferable support
options. An obligation alternative jointly covers ALL its units and resources;
ANY complete alternative substitutes for another. Resource supersets are pruned
within obligations; equivalent minimal support assignments are retained as
separate proof variants inside one alternative. Cartesian products across
applicable obligations yield complete task combinations. Distinct resource/unit
unions and indispensable intersections are calculated separately. Task unions
may be supersets of another task union due to cross-obligation reuse; they are
retained faithfully and are not asserted to be globally irredundant.

The internal self-review challenged necessity inflation, broad documents, named
edit targets, tests, duplicate evidence, overcompound units, unsupported inference
and redundant alternatives. Native decorators are a representation boundary:
existing ranges exclude their preceding lines, so implementing their requested
preservation requires explicit additional provenance. This is recorded as an
implementation-constraining limitation rather than an impossible task or a
missing repository fact. Broad future architecture prose does not override
concrete bounded implementation status. Unknown final public API names and
repeat-selection cardinality remain bounded design choices, without automatic
selection or stronger claims.

The standalone standard-library builder constructs the complete review, derives
statistics, enumerates alternatives/combinations, verifies spans and all binding
invariants, and reconstructs human-readable Markdown. A second process independently
reconstructs every byte and compares fingerprints before publication, then reads
and verifies the actual outputs. Mutation challenges test validator rejection.
Exclusive file creation and an independently invoked overwrite-refusal check
protect existing artifacts. The original packet hashes are rechecked throughout.

Scientific hashes cover the complete review, statistics, human review, validation,
method and builder. The hash index excludes its own bytes to avoid a circular
digest; its physical SHA-256 is reported in the terminal/handoff report. The
operational .local handoff is created only after scientific validation, replay,
original-file preservation, hash freezing and complete access attestation. It is
excluded from evidence, task semantics and scientific digest scopes.
'''

def synopsis(r):
    t = r['text']
    if r['address'].endswith('.py'):
        tree = ast.parse(t)
        desc = (ast.get_docstring(tree) or 'Module without a module docstring.').replace('\n', ' ')
        subjects = [n.name for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))]
        return {'content_scope': desc, 'top_level_subjects': subjects}
    headings = [line for line in t.splitlines() if line.startswith('#')]
    if r['address'].endswith('.toml'):
        headings = [line for line in t.splitlines() if line.startswith('[')]
    return {'content_scope': ' / '.join(headings) or 'Retained configuration/text.', 'top_level_subjects': []}

def minimal_alternatives(units):
    by_resources = collections.defaultdict(list)
    for selection in itertools.product(*(u['supports'] for u in units)):
        resources = tuple(sorted({r for s in selection for r in s['resources']}))
        assignment = [{'unit': u['identity'], 'support': s['identity']} for u, s in zip(units, selection)]
        by_resources[resources].append(assignment)
    kept = [rs for rs in by_resources if not any(set(other) < set(rs) for other in by_resources)]
    key = units[0]['obligation'].split('/')[-1]
    alternatives = []
    for n, resources in enumerate(sorted(kept), 1):
        alternatives.append({'identity': f'{key}.alternative-{n:02}', 'obligation': units[0]['obligation'],
            'required_units': [u['identity'] for u in units], 'required_resources': list(resources),
            'proof_variants': by_resources[resources], 'rationale_for_completeness': 'Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.',
            'rationale_for_minimality': 'No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.',
            'inferability_assumptions': sorted({s['inferability_rationale'] for u in units for s in u['supports'] if s['mode'] == 'INFERABLE' and any(s['identity'] == a['support'] for variant in by_resources[resources] for a in variant)}),
            'provenance': PROVENANCE})
    return alternatives

def mathematics(review):
    alternatives = review['alternatives']
    groups = [[a for a in alternatives if a['obligation'] == o['identity']] for o in review['obligations'] if o['assessment']['status'] == 'APPLICABLE']
    combos = []
    if all(groups):
        for n, selection in enumerate(itertools.product(*groups), 1):
            combos.append({'identity': f'task-combination-{n:04}', 'alternatives': [a['identity'] for a in selection],
                'resources': sorted({r for a in selection for r in a['required_resources']}),
                'units': sorted({u for a in selection for u in a['required_units']})})
    resource_unions = sorted({tuple(c['resources']) for c in combos})
    unit_unions = sorted({tuple(c['units']) for c in combos})
    def intersect(sets):
        return sorted(set.intersection(*(set(s) for s in sets))) if sets else []
    per_obligation = {}
    for o in review['obligations']:
        group = [a for a in alternatives if a['obligation'] == o['identity']]
        per_obligation[o['key']] = {'resources': intersect([a['required_resources'] for a in group]), 'units': intersect([a['required_units'] for a in group])}
    return {'complete_task_combinations': combos, 'distinct_sufficient_resource_unions': [list(s) for s in resource_unions],
            'distinct_sufficient_unit_unions': [list(s) for s in unit_unions],
            'minimum_sufficient_resource_count': min(map(len, resource_unions)) if resource_unions else None,
            'maximum_sufficient_resource_count': max(map(len, resource_unions)) if resource_unions else None,
            'minimum_sufficient_unit_count': min(map(len, unit_unions)) if unit_unions else None,
            'maximum_sufficient_unit_count': max(map(len, unit_unions)) if unit_unions else None,
            'obligation_indispensable': per_obligation,
            'task_indispensable_resources': intersect([c['resources'] for c in combos]),
            'task_indispensable_units': intersect([c['units'] for c in combos])}

def audit():
    definitions = [
        (0, ['source', 'choices'], ['Add caller-selected direct Python source-declaration disclosure choices to common Context Planning', 'alongside existing qualified-reference and whole-resource choices', 'without automatic retrieval or selection.']),
        (1, ['source'], ['Reuse function `devtools.context.python.modules.selection.select_python_module_source_declarations` for direct function and class source identities', 'support a direct method only through its validated native class parent and containment', 'without runtime attribute, imported-facade, inherited-method or semantic resolution.']),
        (2, ['choices'], ['Integrate the choices with class `devtools.context.planning.plan.DisclosurePlan` and module `devtools.context.planning`', 'retaining immutable purpose/frame/ordered-choice contracts and compatibility with existing choices.']),
        (3, ['integrity'], ['Validate every supplied native declaration and resource against the retained snapshot through method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at`', 'reject foreign or stale frame/content', 'missing resource', 'unsupported declaration scope', 'mismatched returned identity before publishing the disclosure', 'without reacquiring files.']),
        (4, ['materialization'], ['Materialize the exact declaration source segment with native derivation, source-range and owner-resource provenance in class `ContextDisclosure`', 'preserve UTF-8 boundaries', 'decorators', 'CRLF/non-ASCII bytes', 'caller order in mixed plans', 'without inferring sufficiency or expanding to whole owners implicitly.']),
        (5, ['assembly'], ['Preserve common rendering and copied request assembly with class `ModelRequest`', 'original request', 'prompt role', 'settings', 'conversation', 'provider settings and tools remain unchanged except the copied prompt', 'keep task text before Context', 'introduce no new budget or truncation policy.']),
        (6, ['exports'], ['Expose the new explicit choice through the common planning public API and outer Context facade', 'keeping dependency direction', 'avoiding a Retrieval dependency or language-specific logic in common assembly.']),
        (7, ['tests'], ['Add focused tests for direct function/class/method choices', 'decorated and repeated declarations', 'mixed-plan ordering and exact source/provenance', 'stale/foreign/missing-resource rejection', 'unchanged existing choices', 'copied-request preservation.']),
        (8, ['documentation'], ['Update file `src/devtools/context/planning/docs/overview.md` and file `docs/architecture.md`', 'to explain source identity versus runtime bindings', 'explicit representation admission', 'supported/deferred scope and compatibility', 'without claiming automatic relevance or readiness.']),
        (9, ['validation'], ['Validate with file `scripts/validate_development.py`', 'preserve file `pyproject.toml` test/coverage settings', 'run the documented protected development profile', 'Ruff lint/format', 'strict mypy', 'both worktree/index whitespace checks.']),
    ]
    lines = P['task_text'].splitlines(keepends=True)
    result = []
    offset = 0
    for n, keys, clauses in definitions:
        line = lines[n]
        for k, clause in enumerate(clauses, 1):
            s = offset + line.index(clause)
            result.append({'identity': f'task-clause-{n + 1:02}-{k:02}', 'classification': 'COVERED',
                'obligations': [OS[key]['identity'] for key in keys],
                'evidence': {'kind': 'task', 'task_identity': P['task_identity'], 'start': s, 'end': s + len(clause), 'text': clause, 'provenance': PROVENANCE},
                'rationale': 'The cited frozen obligation statement and criterion cover this mandatory feature clause without extending unrelated obligations.'})
        offset += len(line)
    return result

ATTESTATION_ITEMS = ['repository_checkout', 'Git_history', 'parent_or_sibling_workspace_files', 'retrieval_queries', 'rankings', 'scores', 'hint_or_routing_artifacts', 'experiment_arms', 'treatment_results', 'acquisition_costs', 'prior_gold', 'confirmation_or_reserve_data', 'external_web_information']

def make_review():
    obligation_records = []
    for o in P['obligations']:
        obligation_records.append({**o, 'assessment': {'status': 'APPLICABLE', 'rationale': 'This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.',
            'inferability_at_task_start': 'The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.'}})
    alternatives = []
    for key in KEYS:
        alternatives.extend(minimal_alternatives([u for u in UNITS if u['obligation'] == OS[key]['identity']]))
    required = collections.defaultdict(set)
    for a in alternatives:
        required[a['obligation']].update(a['required_resources'])
    resource_records = [{k: v for k, v in r.items() if k != 'text'} | synopsis(r) for r in RS]
    cells = []
    for o in obligation_records:
        oid = o['identity']
        for r in resource_records:
            address = r['address']
            support_options = [s for u in UNITS if u['obligation'] == oid for s in u['supports'] if address in s['resources']]
            extra = [h for h in HELPFUL if h['obligation'] == oid and h['address'] == address]
            if address in required[oid]:
                label = 'REQUIRED'
                used = [a for a in alternatives if a['obligation'] == oid and address in a['required_resources']]
                bindings = sorted({binding['unit'] for a in used for variant in a['proof_variants'] for binding in variant
                    if any(s['identity'] == binding['support'] and address in s['resources'] for u in UNITS for s in u['supports'])})
                evidence = [e for a in used for variant in a['proof_variants'] for b in variant for u in UNITS if u['identity'] == b['unit'] for s in u['supports'] if s['identity'] == b['support'] for e in s['evidence'] if e['kind'] == 'resource' and e['address'] == address]
                rationale = 'Establishes necessary unit(s) ' + ', '.join(bindings) + '. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.'
            elif extra or support_options:
                label = 'HELPFUL_ONLY'
                bindings = []
                evidence = [e for h in extra for e in h['evidence']] + [e for s in support_options for e in s['evidence'] if e['kind'] == 'resource' and e['address'] == address]
                rationale = ' '.join(h['rationale'] for h in extra) or 'Supports a duplicated fact, but other jointly necessary members already supply that fact in every minimal alternative; requiring it would add a redundant member.'
            else:
                label = 'UNNECESSARY'
                bindings = []
                evidence = []
                rationale = f"Content scope: {r['content_scope']}. This resource supplies no required or specifically useful contract fact for {o['statement']} in the bounded direct-source change. Unrelated domain behavior, retrieval/resolution mechanisms, general test adjacency and merely mentioning a concept do not establish necessity."
            unique = {(e['address'], e['start'], e['end']): e for e in evidence}
            cells.append({'obligation': oid, 'address': address, 'document_identity': r['document_identity'], 'content_identity': r['content_identity'],
                'label': label, 'rationale': rationale, 'required_units': bindings, 'evidence': [unique[k] for k in sorted(unique)],
                'inferability_rationale': 'Necessary-unit support modes and assumptions are retained in the referenced units; this cell does not assert stronger facts.' if label == 'REQUIRED' else 'No necessity inference is made.',
                'provenance': PROVENANCE})
    limitations = [
        {'identity': 'limitation.decorator-range', 'kind': 'INTERPRETATION_LIMITATION', 'impact': 'CONSTRAINS_IMPLEMENTATION', 'blocks_judgment': False,
         'statement': 'Native spans exclude decorator lines; the task requires preserving decorators. Existing extraction alone is insufficient. The new representation needs explicit decorator-inclusive support/range accounting or an authorized native-range extension without runtime evaluation.',
         'evidence': [task_span('preserve UTF-8 boundaries, decorators, CRLF/non-ASCII bytes'), span(131, 'AST declaration spans begin', '```text')],
         'rationale': 'These facts bound the implementation rather than prove it impossible. The frozen source contains the ranges and retained text needed to define a faithful extension; no absent repository fact or inferred runtime semantics is required.', 'provenance': PROVENANCE},
        {'identity': 'limitation.explicit-cardinality', 'kind': 'INTERPRETATION_LIMITATION', 'impact': 'CONSTRAINS_IMPLEMENTATION', 'blocks_judgment': False,
         'statement': 'The task fixes caller-selected native identities and repeated-declaration preservation, but does not select final new option names or whether a factory offers one explicit declaration or a caller-approved tuple of native matches.',
         'evidence': [task_span('Add caller-selected direct Python source-declaration disclosure choices'), symbol(158, 'PythonModuleSourceDeclarationSelection'), symbol(123, 'DisclosurePlan')],
         'rationale': 'Both explicit per-declaration choice and explicit caller selection of a multi-match group are defensible if native identity, order and no automatic selection/owner expansion remain intact. This is not an unresolved resource label or an invented behavior requirement.', 'provenance': PROVENANCE},
        {'identity': 'limitation.architecture-status', 'kind': 'INTERPRETATION_LIMITATION', 'impact': 'NOTEWORTHY', 'blocks_judgment': False,
         'statement': 'Broad architecture/ADR prose still describes general assembly/materializer mechanisms as future, while concrete source and narrower implemented-status paragraphs establish the existing common boundary.',
         'evidence': [span(2, 'The implemented DisclosurePlan is intentionally narrower', 'Every disclosure stage preserves'), span(2, 'Concrete coverage, fidelity', 'The breadth gate'), span(6, '## Status and implementation boundary'), symbol(124, 'assemble_context_disclosure_model_request')],
         'rationale': 'Preserve the distinction between bounded implemented functions and general future infrastructure; documentation of the feature must not promote broad automatic planning/readiness. This constrains claims, not the repository fact judgment.', 'provenance': PROVENANCE},
        {'identity': 'limitation.definition-replay', 'kind': 'INTERPRETATION_LIMITATION', 'impact': 'CONSTRAINS_IMPLEMENTATION', 'blocks_judgment': False,
         'statement': 'Native subject/derivation identity binds parser implementation/runtime version and grammar. Canonical native comparison must use compatible derivation-definition semantics rather than assuming only content controls identity.',
         'evidence': [symbol(136, 'PythonFunctionDeclarationDerivationDefinition'), symbol(130, 'PythonClassMethodDerivationDefinition')],
         'rationale': 'The native definitions directly bound reproducibility. No external runtime reproduction is required for this semantic adjudication.', 'provenance': PROVENANCE},
    ]
    review = {'schema': 'case-0012-primary-stage-c-review-v1', 'case': P['case'], 'task_identity': P['task_identity'], 'task_text': P['task_text'],
        'frame': P['frame'], 'packet_digests': EXPECTED, 'packet_original_file_hashes': ORIGINAL_HASHES,
        'initial_boundary_validation': {'workspace': str(EXPECTED_ROOT), 'exact_initial_files': sorted(ORIGINALS), 'no_subdirectories': True,
          'no_git': True, 'no_local': True, 'no_symlinks_junctions_or_reparse_points': True, 'supplied_validator_command': 'python -B validate_packet.py', 'supplied_validator_status': 'VERIFIED; NO ADJUDICATION'},
        'label_vocabulary': LABELS, 'label_semantics': {'REQUIRED': 'Member of at least one complete minimal alternative supporting necessary units; not necessarily indispensable.', 'HELPFUL_ONLY': 'Specifically useful or corroborating evidence, excluded from minimal alternatives.', 'UNNECESSARY': 'No needed or specifically useful fact for this obligation within the feature scope.', 'UNRESOLVED': 'Genuinely undecidable obligation-relative resource judgment.'},
        'obligations': obligation_records, 'task_interpretation_audit': audit(), 'task_interpretation_gaps': [],
        'resources': resource_records, 'cells': cells, 'required_information_units': UNITS, 'alternatives': alternatives,
        'task_gap': {'status': 'NONE', 'blocks_judgment': False, 'evidence': [task_span(P['task_text'])],
                     'rationale': 'The task requests future software behavior, not an already completed implementation. All mandatory source, integration, integrity, representation, assembly, public API, test, documentation and development-profile semantics can be established/design-bounded from the task and frozen native contracts. Operational handoff/reliability work is outside feature semantics.'},
        'repository_information_gap': {'status': 'NONE', 'blocks_judgment': False, 'evidence_unit_ids': [u['identity'] for u in UNITS],
                     'rationale': 'Every necessary unit has complete retained support alternatives. No unavailable checkout file, external runtime binding, confirmation artifact or proposed API name is needed to judge these obligations.'},
        'interpretation_limitations': limitations, 'unresolved_judgments': [],
        'ambiguity_records': [{'identity': 'ambiguity.new-choice-cardinality', 'limitation': 'limitation.explicit-cardinality', 'status': 'PRESERVED', 'blocks_judgment': False,
             'interpretations': ['One caller-selected native declaration per new choice.', 'A caller explicitly approves an ordered group of native selection matches.'],
             'rationale': 'The task leaves new API shape open; neither interpretation permits automatic selection, merging repeated identities, or implicit whole-owner expansion.'}],
        'self_review': {'status': 'COMPLETED_AND_REVISED', 'kind': 'Internal review of the same PRIMARY adjudication',
            'findings': ['Broad architectural background retained as helpful unless a specific mandatory baseline fact is supplied.',
              'Named script retained helpful because documented gates already supply its selection contract; filenames alone do not establish necessity.',
              'Existing tests retained helpful for test obligation. Task-backed test categories need zero repository witnesses.',
              'Whole-resource test alternative removed: it did not establish the full old choice identity schema.',
              'Separable plan identity/admission, class/method identities, Ruff/mypy and decorator/repetition/order/fidelity test units split.',
              'Redundant support members pruned at obligation level; cross-obligation reuse retained in distinct task unions.',
              'Containment provenance checks do not authenticate all source facts; canonical membership inference explicitly retained.',
              'Decorator exclusion, API cardinality and derivation-definition boundaries preserved as limitations without fabricated gaps.']},
        'blind_access_attestation': {key: 'NO' for key in ATTESTATION_ITEMS},
        'attestation_scope_note': 'NO denotes access to excluded artifacts/information, not natural vocabulary, frame provenance or historical references occurring inside original frozen repository text. No such references were used to infer the present adjudication.',
        'provenance': PROVENANCE}
    review['witness_structure'] = mathematics(review)
    return review

def statistics(review):
    w = review['witness_structure']
    counts = {label: sum(c['label'] == label for c in review['cells']) for label in LABELS}
    by_obligation = {}
    for o in review['obligations']:
        oid = o['identity']
        by_obligation[o['key']] = {
            'applicability': o['assessment']['status'],
            'cell_counts': {label: sum(c['label'] == label and c['obligation'] == oid for c in review['cells']) for label in LABELS},
            'required_unit_count': sum(u['obligation'] == oid for u in review['required_information_units']),
            'alternative_count': sum(a['obligation'] == oid for a in review['alternatives']),
            'required_resource_union': sorted({c['address'] for c in review['cells'] if c['obligation'] == oid and c['label'] == 'REQUIRED'}),
            'indispensable': w['obligation_indispensable'][o['key']],
        }
    return {'schema': 'case-0012-primary-stage-c-statistics-v1', 'case': review['case'], 'task_identity': review['task_identity'],
        'resource_count': len(review['resources']), 'obligation_count': len(review['obligations']), 'cell_count': len(review['cells']),
        'cell_counts': counts, 'by_obligation': by_obligation,
        'required_unit_count': len(review['required_information_units']),
        'required_resource_union': sorted({c['address'] for c in review['cells'] if c['label'] == 'REQUIRED'}),
        'complete_task_combination_count': len(w['complete_task_combinations']),
        'distinct_sufficient_resource_union_count': len(w['distinct_sufficient_resource_unions']),
        'distinct_sufficient_unit_union_count': len(w['distinct_sufficient_unit_unions']),
        **{key: w[key] for key in ['minimum_sufficient_resource_count', 'maximum_sufficient_resource_count', 'minimum_sufficient_unit_count',
             'maximum_sufficient_unit_count', 'task_indispensable_resources', 'task_indispensable_units']},
        'task_clause_count': len(review['task_interpretation_audit']), 'uncovered_task_clause_count': sum(c['classification'] != 'COVERED' for c in review['task_interpretation_audit']),
        'task_interpretation_gap_count': len(review['task_interpretation_gaps']), 'task_gap': review['task_gap']['status'],
        'repository_information_gap': review['repository_information_gap']['status'], 'interpretation_limitation_count': len(review['interpretation_limitations']),
        'unresolved_judgment_count': len(review['unresolved_judgments']), 'ambiguity_record_count': len(review['ambiguity_records'])}

def validate_evidence(evidence):
    assert evidence['provenance'] == PROVENANCE
    if evidence['kind'] == 'task':
        assert evidence['task_identity'] == P['task_identity']
        t = P['task_text']
    else:
        assert evidence['kind'] == 'resource'
        r = next(r for r in RS if r['address'] == evidence['address'])
        assert evidence['document_identity'] == r['document_identity'] and evidence['content_identity'] == r['content_identity']
        t = r['text']
    assert 0 <= evidence['start'] < evidence['end'] <= len(t)
    assert t[evidence['start']:evidence['end']] == evidence['text']

def validate(review):
    assert review['case'] == P['case'] and review['task_identity'] == P['task_identity'] and review['task_text'] == P['task_text']
    assert review['frame'] == P['frame'] and review['packet_digests'] == EXPECTED
    assert review['packet_original_file_hashes'] == ORIGINAL_HASHES
    assert len(review['obligations']) == 9
    for actual, frozen in zip(review['obligations'], P['obligations'], strict=True):
        assert {k: actual[k] for k in frozen} == frozen
        assert actual['assessment']['status'] in {'APPLICABLE', 'NOT_APPLICABLE', 'UNRESOLVED'}
        assert actual['assessment']['rationale']
    expected_resource = {r['address']: {k: v for k, v in r.items() if k != 'text'} for r in RS}
    assert len(review['resources']) == 531
    actual_resource = {r['address']: {k: r[k] for k in expected_resource[r['address']]} for r in review['resources']}
    assert actual_resource == expected_resource and len(actual_resource) == len(review['resources'])
    oids = {o['identity'] for o in review['obligations']}
    rids = set(expected_resource)
    expected_pairs = set(itertools.product(oids, rids))
    cells = review['cells']
    assert len(cells) == 4779
    pairs = {(c['obligation'], c['address']) for c in cells}
    assert len(pairs) == len(cells) and pairs == expected_pairs
    assert review['label_vocabulary'] == LABELS
    units = review['required_information_units']
    unit_map = {u['identity']: u for u in units}
    assert len(unit_map) == len(units)
    support_map = {}
    for u in units:
        assert u['obligation'] in oids and u['supports'] and u['statement'] and u['why_necessary'] and u['semantic_scope'] and u['granularity_audit']
        assert u['provenance'] == PROVENANCE
        for s in u['supports']:
            assert s['identity'] not in support_map and s['evidence'] and s['mode'] in {'DIRECT', 'INFERABLE'} and s['inferability_rationale']
            support_map[s['identity']] = (u['identity'], s)
            assert set(s['resources']) <= rids and len(s['resources']) == len(set(s['resources']))
            assert set(s['resources']) == {e['address'] for e in s['evidence'] if e['kind'] == 'resource'}
            for e in s['evidence']:
                validate_evidence(e)
    alternatives = review['alternatives']
    alternative_map = {a['identity']: a for a in alternatives}
    assert len(alternative_map) == len(alternatives)
    required_pairs = set()
    for a in alternatives:
        oid = a['obligation']
        assert oid in oids and a['provenance'] == PROVENANCE
        expected_units = {u['identity'] for u in units if u['obligation'] == oid}
        assert set(a['required_units']) == expected_units and len(a['required_units']) == len(expected_units)
        assert set(a['required_resources']) <= rids and len(a['required_resources']) == len(set(a['required_resources']))
        assert a['proof_variants'] and a['rationale_for_completeness'] and a['rationale_for_minimality']
        required_pairs.update((oid, r) for r in a['required_resources'])
        for variant in a['proof_variants']:
            assert {b['unit'] for b in variant} == expected_units and len(variant) == len(expected_units)
            actual_rs = set()
            for b in variant:
                assert b['unit'] in unit_map and unit_map[b['unit']]['obligation'] == oid
                unit_id, s = support_map[b['support']]
                assert unit_id == b['unit']
                actual_rs.update(s['resources'])
            assert actual_rs == set(a['required_resources'])
    # Independently propagate support states instead of repeating the builder's
    # Cartesian-product implementation. This detects missing or redundant alts.
    for oid in oids:
        states = {frozenset()}
        for u in (u for u in units if u['obligation'] == oid):
            states = {state | frozenset(s['resources']) for state in states for s in u['supports']}
            states = {state for state in states if not any(other < state for other in states)}
        expected = {tuple(sorted(state)) for state in states}
        actual = [tuple(a['required_resources']) for a in alternatives if a['obligation'] == oid]
        assert len(actual) == len(set(actual)) and set(actual) == expected
    for c in cells:
        r = expected_resource[c['address']]
        assert c['document_identity'] == r['document_identity'] and c['content_identity'] == r['content_identity']
        assert c['label'] in LABELS and c['rationale'] and c['inferability_rationale'] and c['provenance'] == PROVENANCE
        assert (c['label'] == 'REQUIRED') == ((c['obligation'], c['address']) in required_pairs)
        assert c['evidence'] or c['label'] in {'UNNECESSARY', 'UNRESOLVED'}
        for e in c['evidence']:
            validate_evidence(e)
            assert e['kind'] == 'resource' and e['address'] == c['address']
        for uid in c['required_units']:
            assert uid in unit_map and unit_map[uid]['obligation'] == c['obligation']
            assert any(c['address'] in s['resources'] for s in unit_map[uid]['supports'])
        if c['label'] == 'REQUIRED':
            assert c['required_units']
    assert review['witness_structure'] == mathematics(review)
    # Also reconstruct task combinations by iterative extension, independently.
    states = [([], set(), set())]
    for o in review['obligations']:
        if o['assessment']['status'] == 'APPLICABLE':
            states = [(ids + [a['identity']], rs | set(a['required_resources']), us | set(a['required_units']))
                      for ids, rs, us in states for a in alternatives if a['obligation'] == o['identity']]
    actual_combos = review['witness_structure']['complete_task_combinations']
    assert len(states) == len(actual_combos)
    for (ids, rs, us), c in zip(states, actual_combos, strict=True):
        assert ids == c['alternatives'] and sorted(rs) == c['resources'] and sorted(us) == c['units']
    clause_ids = set()
    covered_chars = set()
    for c in review['task_interpretation_audit']:
        assert c['identity'] not in clause_ids
        clause_ids.add(c['identity'])
        assert c['classification'] in {'COVERED', 'NOT_COVERED'}
        assert set(c['obligations']) <= oids and c['rationale']
        validate_evidence(c['evidence'])
        covered_chars.update(range(c['evidence']['start'], c['evidence']['end']))
    leftover = ''.join(char for i, char in enumerate(P['task_text']) if i not in covered_chars)
    assert not re.sub(r'[\s,;.:]', '', re.sub(r'\band\b', '', leftover)), leftover
    for group in ['task_interpretation_gaps', 'interpretation_limitations', 'unresolved_judgments']:
        records = review[group]
        assert len({x['identity'] for x in records}) == len(records)
        for item in records:
            assert item['statement'] and item['rationale'] and isinstance(item['blocks_judgment'], bool)
            assert item['impact'] in {'BLOCKS_JUDGMENT', 'CONSTRAINS_IMPLEMENTATION', 'NOTEWORTHY'}
            for e in item['evidence']:
                validate_evidence(e)
    for name in ['task_gap', 'repository_information_gap']:
        item = review[name]
        assert item['status'] in {'NONE', 'PRESENT', 'UNRESOLVED'} and isinstance(item['blocks_judgment'], bool) and item['rationale']
        for e in item.get('evidence', []):
            validate_evidence(e)
        assert set(item.get('evidence_unit_ids', [])) <= set(unit_map)
    for a in review['ambiguity_records']:
        assert len(a['interpretations']) >= 2 and a['status'] == 'PRESERVED' and a['rationale']
        assert a['limitation'] in {x['identity'] for x in review['interpretation_limitations']}
    assert review['blind_access_attestation'] == {key: 'NO' for key in ATTESTATION_ITEMS}
    return statistics(review)

def mutation_challenges(review):
    import copy
    challenges = []
    def challenge(name, mutate):
        changed = copy.deepcopy(review)
        mutate(changed)
        try:
            validate(changed)
        except (AssertionError, KeyError, StopIteration, ValueError):
            challenges.append({'name': name, 'result': 'REJECTED_AS_REQUIRED'})
        else:
            raise AssertionError('Validator accepted corrupt review: ' + name)
    challenge('task_binding', lambda r: r.update(task_identity='foreign-task'))
    challenge('obligation_statement', lambda r: r['obligations'][0].update(statement='altered'))
    challenge('resource_frame_missing', lambda r: r['resources'].pop())
    challenge('duplicate_qualified_cell', lambda r: r['cells'].__setitem__(0, r['cells'][1]))
    challenge('invalid_label', lambda r: r['cells'][0].update(label='NOT_A_LABEL'))
    challenge('support_identity', lambda r: r['required_information_units'][0]['supports'][0]['evidence'][0].update(content_identity='foreign'))
    challenge('support_bounds', lambda r: r['required_information_units'][0]['supports'][0]['evidence'][0].update(end=100000000))
    challenge('duplicate_unit', lambda r: r['required_information_units'].append(r['required_information_units'][0]))
    challenge('unsupported_unit', lambda r: r['required_information_units'][0].update(supports=[]))
    challenge('alternative_obligation', lambda r: r['alternatives'][0].update(obligation='foreign'))
    challenge('missing_alternative_member', lambda r: r['alternatives'][0]['required_resources'].append('absent-resource'))
    challenge('missing_complete_alternative', lambda r: r['alternatives'].pop(0))
    challenge('combination_mathematics', lambda r: r['witness_structure']['complete_task_combinations'][0]['resources'].pop())
    challenge('indispensable_intersection', lambda r: r['witness_structure']['task_indispensable_resources'].append('absent-resource'))
    challenge('limitation_structure', lambda r: r['interpretation_limitations'][0].update(impact='INVALID'))
    return challenges

def markdown(review, stats):
    # Deduplicated exact evidence is presented once and linked from every judgment.
    evidence_map = {}
    def evidence_key(e):
        return (e['kind'], e.get('address', e.get('task_identity')), e['start'], e['end'])
    def register(e):
        evidence_map[evidence_key(e)] = e
    for u in review['required_information_units']:
        for s in u['supports']:
            for e in s['evidence']:
                register(e)
    for c in review['cells']:
        for e in c['evidence']:
            register(e)
    for item in review['interpretation_limitations'] + review['task_interpretation_audit']:
        es = item['evidence'] if isinstance(item['evidence'], list) else [item['evidence']]
        for e in es:
            register(e)
    keys = sorted(evidence_map)
    ids = {key: f'evidence-{n:04}' for n, key in enumerate(keys, 1)}
    def refs(es):
        return ', '.join(f"[{ids[evidence_key(e)]}](#{ids[evidence_key(e)]})" for e in es)
    def dump(value):
        return '```json\n' + raw_json(value).decode() + '```\n'
    out = ['# PRIMARY blind Stage C adjudication\n', f"Case: `{review['case']}`; task: `{review['task_identity']}`.\n",
        'This adjudication establishes task/repository truth from the frozen packet. It does not claim the future feature is already implemented.\n',
        '## Exact task\n', '```text\n' + review['task_text'] + '```\n',
        '## Boundary and packet digests\n', dump(review['initial_boundary_validation']), dump(review['packet_digests']),
        '## Obligations and applicability\n']
    for o in review['obligations']:
        out.extend([f"### {o['key']}\n", f"Identity: `{o['identity']}`\n", f"Statement: {o['statement']}\n", f"Criterion: {o['criterion']}\n",
            f"Frozen applicability: {o['applicability']}\n", dump(o['assessment']), 'Exact task basis/provenance:\n', dump(o['task_basis'])])
    out.append('## Task-interpretation audit\n')
    out.append(f"{len(review['task_interpretation_audit'])} substantive clauses covered; no TASK_INTERPRETATION_GAP.\n")
    for c in review['task_interpretation_audit']:
        out.append(f"- **{c['identity']} — {c['classification']}**: {c['evidence']['text']}\n  Obligations: {', '.join(c['obligations'])}. {refs([c['evidence']])}\n")
    out.extend(['\n## Cell counts and required-resource union\n', dump({'cell_count': stats['cell_count'], 'cell_counts': stats['cell_counts']}), dump(stats['by_obligation']),
        'The required-resource union is a union of acceptable alternatives, not a requirement to read all resources together.\n', dump(stats['required_resource_union']),
        '## All positive resources by obligation\n'])
    for o in review['obligations']:
        out.append(f"### {o['key']}\n")
        for c in review['cells']:
            if c['obligation'] == o['identity'] and c['label'] in {'REQUIRED', 'HELPFUL_ONLY'}:
                out.extend([f"- **{c['label']} — `{c['address']}`**\n  Document: `{c['document_identity']}`; content: `{c['content_identity']}`.\n  {c['rationale']}\n  Units: {', '.join(c['required_units']) or 'none required'}. Evidence: {refs(c['evidence'])}\n"])
        out.append('\n')
    out.append('## Every required semantic information unit\n')
    for u in review['required_information_units']:
        out.extend([f"### {u['identity']}\n", f"Obligation: `{u['obligation']}`\n", f"**{u['statement']}**\n", f"Scope: {u['semantic_scope']}\n", f"Necessary because: {u['why_necessary']}\n", f"Granularity: {u['granularity_audit']}\n"])
        for s in u['supports']:
            out.append(f"- `{s['identity']}` — {s['mode']}; jointly required resources: {', '.join(s['resources']) or '(none; task evidence)'}.\n  {s['inferability_rationale']}\n  Exact evidence: {refs(s['evidence'])}\n")
        out.append('\n')
    out.append('## Acceptable ALL-of alternatives\n')
    out.append('ANY complete alternative may substitute for another for its obligation. Each proof variant covers ALL required units with ALL listed resource members. Proof variants are substitutable, not cumulative.\n')
    for a in review['alternatives']:
        out.extend([f"### {a['identity']}\n", dump(a)])
    out.extend(['## Complete task combinations and sufficient unions\n', dump(review['witness_structure']),
        '## Task and repository-information gaps\n', dump(review['task_gap']), dump(review['repository_information_gap']),
        '## Limitations and preserved ambiguities\n'])
    for item in review['interpretation_limitations']:
        out.extend([f"### {item['identity']}\n", f"{item['impact']}; blocks judgment: {item['blocks_judgment']}.\n", item['statement'] + '\n', item['rationale'] + '\n', refs(item['evidence']) + '\n'])
    out.extend([dump(review['ambiguity_records']), '## Unresolved judgments\n', dump(review['unresolved_judgments']),
        '## Internal PRIMARY self-review\n', dump(review['self_review']), '## Blind access attestation\n', dump(review['blind_access_attestation']), review['attestation_scope_note'] + '\n',
        '## Exact evidence registry\n', 'Offsets below are Unicode character offsets within the original frozen text, half-open. Native Python source coordinates remain separate.\n'])
    for key in keys:
        e = evidence_map[key]
        eid = ids[key]
        metadata = {k: v for k, v in e.items() if k != 'text'}
        longest = max([len(m.group()) for m in re.finditer(r'`+', e['text'])] or [0])
        fence = '`' * max(3, longest + 1)
        out.extend([f'<a id="{eid}"></a>\n', f'### {eid}\n', dump(metadata), fence + 'text\n' + e['text'] + ('\n' if not e['text'].endswith('\n') else '') + fence + '\n'])
    return '\n'.join(out).encode('utf-8')

def validation_record(review, challenges):
    return {'schema': 'case-0012-primary-stage-c-validation-v1', 'status': 'PASS', 'case': review['case'], 'task_identity': review['task_identity'],
        'validated_cell_count': len(review['cells']), 'packet_originals_unchanged': True,
        'checks': {key: 'PASS' for key in ['exact_case_task_binding', 'exact_obligation_set', 'exact_resource_frame', 'complete_unique_qualified_cells',
           'valid_labels', 'native_content_document_snapshot_identity_scopes', 'exact_support_identities_and_spans', 'unique_supported_units', 'valid_complete_minimal_alternatives',
           'independent_support_state_reconstruction', 'complete_combination_mathematics', 'distinct_unions_and_indispensable_intersections',
           'task_clause_coverage', 'gap_limitation_ambiguity_structure', 'statistics_from_review', 'markdown_from_review',
           'independent_process_byte_reconstruction', 'scientific_output_hashes', 'overwrite_refusal', 'complete_blind_attestation']},
        'mutation_challenges': challenges,
        'replay_command': 'python -B stage_c_builder.py --verify',
        'overwrite_policy': 'Refuse if any scientific output already exists; verify/replay mode never overwrites.',
        'hash_index_scope': 'All scientific outputs except the hash index itself, plus builder. Hash-index physical digest is reported separately. Operational handoff excluded.'}

def reconstructed():
    review = make_review()
    stats = validate(review)
    challenges = mutation_challenges(review)
    validation = validation_record(review, challenges)
    files = {'stage_c_review.json': raw_json(review), 'stage_c_statistics.json': raw_json(stats),
             'STAGE_C_REVIEW.md': markdown(review, stats), 'stage_c_validation.json': raw_json(validation), 'stage_c_method.md': METHOD.encode('utf-8')}
    files['stage_c_hashes.json'] = raw_json({'schema': 'case-0012-primary-stage-c-hashes-v1', 'case': P['case'], 'task_identity': P['task_identity'],
        'algorithm': 'SHA-256', 'packet_originals': ORIGINAL_HASHES,
        'scientific_outputs': {name: sha(data) for name, data in files.items()} | {'stage_c_builder.py': sha(Path(__file__).read_bytes())},
        'excluded': {'stage_c_hashes.json': 'Self-reference excluded to avoid circular hashing; physical digest reported in terminal/handoff.',
                     '.local/codex-result.md': 'Operational handoff, not scientific evidence or an output hash member.'}})
    return files

def assert_workspace_members(allow_handoff=False):
    allowed = set(ORIGINALS + OUTPUTS + ['stage_c_builder.py'])
    actual = set()
    for item in ROOT.iterdir():
        assert not item.is_symlink() and not (getattr(item.stat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)
        if item.name == '.local' and allow_handoff:
            assert item.is_dir()
            members = list(item.iterdir())
            assert len(members) == 1 and members[0].name == 'codex-result.md' and members[0].is_file() and not members[0].is_symlink()
            assert not (getattr(members[0].stat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)
            continue
        assert item.is_file()
        actual.add(item.name)
    assert actual <= allowed

def refuse_overwrite():
    present = [name for name in OUTPUTS if (ROOT / name).exists()]
    if present:
        raise FileExistsError('OVERWRITE REFUSED: ' + ', '.join(present))

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else '--build'
    if mode == '--build':
        refuse_overwrite()
        assert not (ROOT / '.local').exists()
        assert_workspace_members()
        files = reconstructed()
        local_fingerprints = {name: sha(data) for name, data in files.items()}
        child = subprocess.run([sys.executable, '-B', str(Path(__file__)), '--fingerprints'], cwd=ROOT, capture_output=True, check=True)
        assert json.loads(child.stdout) == local_fingerprints
        for name in OUTPUTS:
            with (ROOT / name).open('xb') as f:
                f.write(files[name])
        verify = subprocess.run([sys.executable, '-B', str(Path(__file__)), '--verify'], cwd=ROOT, capture_output=True, check=True)
        receipt = json.loads(verify.stdout)
        assert receipt['status'] == 'PASS'
        refused = subprocess.run([sys.executable, '-B', str(Path(__file__)), '--build'], cwd=ROOT, capture_output=True)
        assert refused.returncode != 0 and b'OVERWRITE REFUSED' in refused.stderr
        assert packet()[1] == ORIGINAL_HASHES
        print(json.dumps(receipt, indent=2))
    elif mode == '--fingerprints':
        assert_workspace_members()
        print(json.dumps({name: sha(data) for name, data in reconstructed().items()}, sort_keys=True))
    elif mode == '--verify':
        assert_workspace_members(allow_handoff=True)
        files = reconstructed()
        for name, data in files.items():
            assert (ROOT / name).read_bytes() == data, name
        saved = json.loads((ROOT / 'stage_c_review.json').read_bytes())
        saved_stats = json.loads((ROOT / 'stage_c_statistics.json').read_bytes())
        assert validate(saved) == saved_stats
        assert markdown(saved, saved_stats) == (ROOT / 'STAGE_C_REVIEW.md').read_bytes()
        hashes = json.loads((ROOT / 'stage_c_hashes.json').read_bytes())
        for name, digest in hashes['scientific_outputs'].items():
            assert sha((ROOT / name).read_bytes()) == digest
        try:
            refuse_overwrite()
        except FileExistsError:
            pass
        else:
            raise AssertionError('Overwrite refusal failed')
        assert packet()[1] == ORIGINAL_HASHES
        print(json.dumps({'status': 'PASS', 'deterministic_byte_equality': True, 'originals_unchanged': True,
                          'scientific_output_sha256': {name: sha(data) for name, data in files.items()} | {'stage_c_builder.py': sha(Path(__file__).read_bytes())}}, indent=2))
    else:
        raise ValueError('Unknown mode')

if __name__ == '__main__':
    main()
