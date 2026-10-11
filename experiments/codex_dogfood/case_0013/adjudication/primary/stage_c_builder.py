"""Standalone sealed-packet adjudication builder. No repository imports or access.

The declarations below are this reviewer's scientific judgments. The algorithms
only expand, validate and publish them; they do not decide semantic necessity.
"""
from __future__ import annotations

import argparse
import ast
import copy
import gzip
import hashlib
import itertools
import json
import math
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).absolute().parent
CASE = 'case-0013'
TASK = 'case-0013-context-disclosure-manifest'
INPUT_HASHES = {
    'README.md': '66b119b890f3019c0cc50982b26385fb63a54c87b4c5f2a88b3446b0a0da8578',
    'integrity.json': '683a0d244b3c166821db046d107b2b5cdd00e1d2753d1b924c9ca2054df60f16',
    'manifest.json': '9653a664db91faa1c41ade168e2da528d3601b809d08386d9c13cc96a24bb0f4',
    'resources.json.gz': '7d501a60f1107e1d7e5de17d37ad61732e7d173b8d3554975d516586002d9558',
    'validate_packet.py': '35e60aeb0df29a9462cac19c5acba152f3b9e08832e0e53375144b9bdb8917c2',
}
PAYLOAD_HASH = '1305f78b76f482750807bb376c820515990683d13b8d107be9725729b7a8ece6'
KEYS = ['structure', 'integrity', 'manifest', 'projection', 'compatibility', 'exports', 'tests', 'documentation', 'validation']
LABELS = ['REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY']
CLASSES = ['TASK_BACKED', 'REPOSITORY_SUPPORTED', 'TASK_AND_REPOSITORY_SUPPORTED']
OUTPUTS = ['stage_c_review.json', 'stage_c_statistics.json', 'STAGE_C_REVIEW.md', 'stage_c_validation.json', 'stage_c_hashes.json', 'stage_c_method.md']


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n').encode('utf-8')


def packet():
    for name, digest in INPUT_HASHES.items():
        path = ROOT / name
        require(not path.is_symlink() and not (getattr(path.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT), 'Input reparse point')
        require(sha(path.read_bytes()) == digest, 'Sealed input bytes differ: ' + name)
    raw = gzip.decompress((ROOT / 'resources.json.gz').read_bytes())
    require(sha(raw) == PAYLOAD_HASH, 'Canonical payload hash differs')
    p = json.loads(raw)
    require(canonical(p) == raw, 'Noncanonical input payload')
    require(set(p) == {'case', 'task_identity', 'task_text', 'obligations', 'resources'}, 'Packet metadata allowlist')
    require(p['case'] == CASE and p['task_identity'] == TASK, 'Case/task binding')
    require(len(p['resources']) == 531 and len(p['obligations']) == 9, 'Packet frame')
    require([o['key'] for o in p['obligations']] == KEYS, 'Obligation identities/order')
    require(len({r['address'] for r in p['resources']}) == 531, 'Resource identities')
    for r in p['resources']:
        require(set(r) == {'address', 'content_identity', 'text', 'encoding', 'byte_size'}, 'Resource metadata allowlist')
        h = hashlib.sha256()
        for v in ('decoded-utf8-text-sha256-v1', r['text']):
            b = v.encode('utf-8'); h.update(len(b).to_bytes(8, 'big')); h.update(b)
        require(h.hexdigest() == r['content_identity'] and len(r['text'].encode('utf-8')) == r['byte_size'] and r['encoding'] == 'utf-8', 'Resource content identity')
    for o in p['obligations']:
        require(set(o) == {'identity', 'key', 'statement', 'criterion', 'applicability', 'task_basis'}, 'Obligation metadata allowlist')
        require(o['identity'] == TASK + '/' + o['key'], 'Obligation binding')
        for b in o['task_basis']:
            require(p['task_text'][b['start']:b['end']] == b['text'], 'Task basis')
    return p


def rid(i):
    return f'R{i:03d}'


def task_span(p, line):
    lines = p['task_text'].splitlines(keepends=True)
    start = sum(map(len, lines[:line - 1]))
    text = lines[line - 1]
    return {'source': 'TASK', 'start': start, 'end': start + len(text), 'text': text, 'line_start': line, 'line_end': line}


def span(p, index, start_line=1, end_line=None):
    r = p['resources'][index]
    lines = r['text'].splitlines(keepends=True)
    end_line = len(lines) if end_line is None else end_line
    require(1 <= start_line <= end_line <= len(lines), 'Authored span range')
    a = sum(map(len, lines[:start_line - 1])); b = sum(map(len, lines[:end_line]))
    return {'source': rid(index), 'address': r['address'], 'content_identity': r['content_identity'], 'start': a, 'end': b, 'line_start': start_line, 'line_end': end_line, 'text': r['text'][a:b]}


def node_span(p, index, name):
    t = p['resources'][index]['text']
    n = next(n for n in ast.walk(ast.parse(t)) if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
    start = min([n.lineno] + [d.lineno for d in getattr(n, 'decorator_list', [])])
    return span(p, index, start, n.end_lineno)


def support(p, specs, mode='DIRECT', inference='The exact retained declarations establish the stated interface and behavior. No execution result is inferred.'):
    evidence = []
    for spec in specs:
        if isinstance(spec, int): evidence.append(span(p, spec))
        elif isinstance(spec[1], str): evidence.append(node_span(p, spec[0], spec[1]))
        else: evidence.append(span(p, *spec))
    return {'resources': sorted({s['source'] for s in evidence}), 'mode': mode, 'evidence': evidence, 'inferability_rationale': inference}


def units(p):
    out = []
    def t(n, obs, statement, lines, reason):
        out.append({'identity': f'T{n:02d}', 'obligations': obs.split(), 'statement': statement, 'evidence_class': 'TASK_BACKED', 'task_evidence': [task_span(p, i) for i in lines], 'support_alternatives': [], 'necessity_rationale': reason, 'inferability_assumptions': 'A desired future behavior is prescribed here; this unit asserts no existing implementation.', 'provenance': 'Independent primary semantic judgment grounded in exact original task text.'})
    def r(n, obs, statement, alternatives, reason):
        out.append({'identity': f'S{n:02d}', 'obligations': obs.split(), 'statement': statement, 'evidence_class': 'REPOSITORY_SUPPORTED', 'task_evidence': [], 'support_alternatives': alternatives, 'necessity_rationale': reason, 'inferability_assumptions': 'Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.', 'provenance': 'Independent primary semantic judgment over frozen eligible resource contents.'})
    t(1, 'structure manifest', 'Build a deterministic inspectable in-memory description of an already materialized disclosure.', [1], 'Defines the object being described and its lifecycle boundary.')
    t(2, 'structure manifest', 'Preserve exact plan identity, caller purpose and repository/snapshot applicability.', [2], 'Changing these would describe a different decision or frame.')
    t(3, 'structure manifest', 'Preserve ordered choices, representation names, option identities and one item per choice.', [2], 'Defines item correspondence and order fidelity.')
    t(4, 'integrity', 'Reject foreign repository and stale snapshot frames before publishing a manifest.', [3], 'Applicability failures cannot be presented as an authenticated manifest.')
    t(5, 'integrity', 'Reject missing resources, content-identity mismatch and misaligned address/content pairs before publication.', [3], 'An ordered support pair must authenticate as that exact addressed occurrence.')
    t(6, 'integrity manifest', 'Use retained snapshot resource_at; do not reacquire source, rematerialize choices or silently substitute evidence.', [3], 'The requested operation describes an existing realization against retained state.')
    t(7, 'manifest', 'Add ContextDisclosureManifest and describe_context_disclosure in the new common planning manifest.py destination.', [4], 'The new public operation and destination are explicitly prescribed, without asserting their prior existence.')
    t(8, 'structure manifest projection', 'Retain every item and every repeated support occurrence in plan order, correlating exact address/content identity pairs.', [4, 5], 'Set conversion or independent ordering of support arrays would lose the requested account.')
    t(9, 'manifest projection', 'Count exact UTF-8 text bytes without normalizing non-ASCII text or line endings.', [4, 7], 'Byte counts must describe the retained text, including non-ASCII and CRLF cases.')
    t(10, 'structure manifest projection', 'Retain original native provenance as native values; do not serialize arbitrary provenance objects.', [4], 'Opaque native values must survive the in-memory operation without a fabricated universal schema.')
    t(11, 'projection', 'Provide deterministic JSON-compatible fields with stable explicit identities and exact ordered support records.', [5], 'Presentation must remain inspectable and deterministic independently of arbitrary object repr output.')
    t(12, 'projection', 'Distinguish the sum of item text byte counts from bytes of unique supporting resources.', [5], 'Item representation text and distinct retained source occurrences are different accounting domains.')
    t(13, 'projection documentation', 'The projection is derived presentation, not a durable wire schema, new repository fact, source-export authority, budget policy or sufficiency claim.', [5], 'Bounds the semantic strength and persistence meaning of the result.')
    t(14, 'compatibility', 'Preserve existing rendering and copied ModelRequest assembly.', [6], 'The added inspection operation must leave existing consumer-visible behavior intact.')
    t(15, 'exports', 'Expose the manifest operation through the common planning and outer Context public facades.', [6], 'Both specified public entry boundaries must expose the operation.')
    t(16, 'exports', 'Keep the common operation independent of the excluded selection subsystem and retain Python-specific provenance ownership.', [6], 'The new feature must respect the explicitly prescribed dependency direction.')
    t(17, 'tests', 'Add tests/context/planning/test_manifest.py exercising mixed existing whole-resource and qualified-reference choices.', [7], 'The tests must cover both existing representations in one disclosure.')
    t(18, 'tests', 'Cover duplicate support and order independently of identical-choice duplication.', [7], 'Support multiplicity is an explicit fidelity requirement.')
    t(19, 'tests', 'Cover non-ASCII and CRLF byte fidelity, exact native provenance, deterministic projection and every requested rejection case.', [7], 'These are explicit observable feature acceptance cases.')
    t(20, 'tests', 'Retain existing planning, rendering and copied-request regression coverage.', [7], 'Adding focused coverage must preserve the established regression boundary.')
    t(21, 'documentation', 'Update the existing planning overview with fidelity, applicability, byte accounting and non-persistence scope.', [8], 'The task specifies the document and required future content; its current wording is contextual rather than an additional fact needed to restate these requirements.')
    t(22, 'documentation', 'Explain why a complete manifest establishes neither task completeness nor model comprehension.', [8], 'A complete account of supplied material cannot certify adequacy or consumer understanding.')
    t(23, 'documentation', 'Explain why the manifest does not authorize disclosure or implement automatic Context planning.', [8], 'The documentation must separate inspection from authority and autonomous selection.')
    t(24, 'structure manifest documentation', 'Keep caller-directed selection distinct from relevance, sufficiency, persistent Evidence and model-input assembly.', [1], 'The inspection feature must not acquire these independent responsibilities.')
    t(25, 'validation', 'Inspect current test, coverage and strict typing constraints; run the protected development profile and separate Ruff, format, strict mypy and both worktree/index diff checks without weakening configuration or crossing the stated restricted/live boundaries.', [9], 'Defines required future validation, not a demand to execute repository checks during this adjudication.')

    r(1, 'structure integrity manifest projection tests', 'A materialized item exposes option_identity, representation, resource_addresses, content_identities, text and opaque object-valued native_provenance; the two support tuples are separate fields.', [support(p, [(122, 'MaterializedDisclosureItem')])], 'The manifest must read the actual materialized interface and validate aligned pairs; the task does not supply the current field layout.')
    r(2, 'structure integrity manifest projection tests', 'ContextDisclosure retains plan and ordered items, rejects cardinality/option/representation disagreement, and materialize_disclosure_plan checks frame and realizes each option once in order.', [support(p, [(122, 'ContextDisclosure'), (122, 'materialize_disclosure_plan')])], 'Defines the existing realization boundary to consume and preserve. It does not itself authenticate each support tuple.')
    r(3, 'structure manifest projection tests', 'The existing plan surface provides purpose, repository_id, snapshot_id, ordered disclosures and identity; these are available on the retained plan without recomputing a new plan.', [support(p, [(123, 'DisclosurePlan')]), support(p, [(122, 'materialize_disclosure_plan'), (122, 'ContextDisclosure'), (124, 'render_context_disclosure')], 'INFERABLE', 'Materialization reads repository_id, snapshot_id and disclosures; rendering reads purpose and identity. Together these establish the same required plan surface; neither alone does.')], 'The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.')
    r(4, 'integrity manifest projection tests', 'RepositorySnapshot exposes id, repository_id and retained resources; resource_at returns the occurrence at exact address equality and raises ValueError when missing.', [support(p, [(181, 'RepositorySnapshot')])], 'Authentication must use the actual retained lookup and failure contract, not a guessed lookup or filesystem read.')
    r(5, 'integrity manifest projection tests', 'The retained occurrence surface exposes address, content_identity and exact content text; the current identity/address presentation is string-compatible.', [support(p, [(180, 'RepositoryResourceAddress'), (180, 'ContentIdentity'), (180, 'RepositoryResourceOccurrence')]), support(p, [(125, 'WholeResourceDisclosureOption')], 'INFERABLE', 'The existing consumer reads and formats address/content_identity/content from resource_at output, establishing the needed surface without needing every occurrence constructor field.'), support(p, [(141, 'materialize_python_qualified_reference_source'), (141, 'render_python_qualified_reference_context')], 'INFERABLE', 'The existing consumer reads retained content and content identities and presents source/target addresses and identities as strings. Its occurrence equality checks bind these values to the addressed retained resources.')], 'Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).')
    r(6, 'compatibility', 'The current common renderer emits its fixed header and purpose/plan/snapshot/item fields, then each item option/representation/text in enumeration order, retaining the original disclosure.', [support(p, [(124, 'RenderedContextDisclosure'), (124, 'render_context_disclosure')])], 'Exact current output compatibility cannot be established solely from a future instruction to leave it unchanged.')
    r(7, 'compatibility', 'The common request assembler preserves unchanged task text before unchanged context, reports both UTF-8 lengths and replaces only Prompt content while retaining its role and every other ModelRequest field.', [support(p, [(124, 'assemble_context_disclosure_model_request')])], 'The exact existing common assembly uses dataclasses.replace; that preserves fields including tools without needing a second complete ModelRequest implementation description.')
    r(8, 'exports', 'The common planning facade uses explicit imports from its owned modules and an explicit __all__ containing its public planning operations and values.', [support(p, [120])], 'Adding a coherent public export needs the actual public enumeration and module ownership, not merely the future destination name.')
    r(9, 'exports', 'The outer Context facade imports common planning names from the planning package and separately exposes them in its explicit __all__; Python function APIs have a separate import owner.', [support(p, [(83, 1, 75), (83, 128, 242)])], 'Both outer import binding and explicit public list must be maintained while preserving ownership.')
    r(10, 'tests', 'The existing whole-resource choice is created for a purpose, snapshot and resource address, materializes retained source into one common item, and carries the retained resource as native provenance.', [support(p, [(125, 'WholeResourceDisclosureOption'), (125, 'choose_whole_resource_disclosure')]), support(p, [(383, 'test_mixed_plan_preserves_purpose_sources_and_request')], 'INFERABLE', 'The executable example supplies the public constructor call, common materialization and an identity assertion for whole.resource provenance.')], 'Mixed-choice tests need the existing representation contract rather than inventing a future substitute option.')
    r(11, 'tests', 'The existing qualified-reference option accepts an explicit purpose plus native analysis/reference, participates in a common plan, and produces ordered source/target support, which may repeat one address.', [support(p, [(140, 'PythonQualifiedReferenceDisclosureOption'), (140, 'choose_python_qualified_reference_disclosure')]), support(p, [(383, '_reference_option'), (383, 'test_mixed_plan_preserves_purpose_sources_and_request'), (383, 'test_same_resource_reference_uses_same_plan_boundary')], 'INFERABLE', 'The fixture and tests establish the same public option integration and ordered support contract, including repeated same-resource support. No stronger Python meaning or provenance serializer is inferred.')], 'Tests must cover real existing option semantics; knowing the new test filename is insufficient. Detailed parser internals and fixture construction recipes are implementation conveniences.')
    r(12, 'validation', 'Current project settings enable strict pytest config/markers, devtools branch coverage with a 100% threshold, Ruff ALL with stated exceptions and Python 3.12/88-column formatting, and strict mypy over src/tests/experiments with explicit package bases and src path.', [support(p, [(64, 35, 78)])], 'The task asks to inspect actual configuration; these repository-specific values cannot be inferred from the desired phrase strict typing.')
    r(13, 'validation', 'The protected development profile runs tests/ while excluding tests/experiments/ before recursive collection, keeps project options and coverage, and is invoked through scripts/validate_development.py.', [support(p, [(60, 3, 29)]), support(p, [65]), support(p, [(57, 33, 42)]), support(p, [(0, 228, 240)], 'INFERABLE', 'The operating guide gives the command, exclusion before collection and preserved branch gate; the configured project contract supplies the remaining current settings.')], 'The task names a protected profile but does not define its implementation or command. Equivalent direct documentation and executable contracts are alternatives.')
    r(14, 'manifest projection tests', 'Addressed resource occurrence and content identity are distinct: equal text at two different addresses remains two resource occurrences; unique supporting-resource bytes must preserve that distinction.', [support(p, [(180, 'ContentIdentity'), (180, 'RepositoryResourceOccurrence')]), support(p, [(179, 'observe_repository_resources'), (179, '_observe_resource')], 'INFERABLE', 'Content identity is computed only from decoded text, while snapshot membership separately stores each requested address; equal content therefore does not collapse addressed occurrences.'), support(p, [(424, 'test_equal_content_at_distinct_addresses_preserves_distinct_occurrences'), (424, 'test_equal_content_at_two_addresses_retains_distinct_multi_occurrences')])], 'A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.')
    # Granularity self-review: independently testable requirements remain distinct
    # even when they share the same exact task paragraph or repository resource.
    def split_unit(identity, replacements):
        original = next(u for u in out if u['identity'] == identity)
        original['statement'] = replacements[0][1]
        original['necessity_rationale'] = replacements[0][2]
        for new_id, statement, reason in replacements[1:]:
            new = copy.deepcopy(original)
            new.update(identity=new_id, statement=statement, necessity_rationale=reason)
            out.append(new)
    split_unit('T16', [
        ('T16', 'Keep the new common operation independent of the task-excluded selection subsystem.', 'The common manifest must obey the explicitly prescribed dependency boundary.'),
        ('T26', 'Retain Python-specific provenance ownership rather than relocating it into common planning.', 'Preserving an opaque native object does not authorize moving its language-specific semantics.'),
    ])
    split_unit('T19', [
        ('T19', 'Test exact non-ASCII and CRLF byte accounting.', 'UTF-8 length and line-ending fidelity need acceptance coverage.'),
        ('T27', 'Test exact native provenance preservation.', 'Value/object fidelity is distinct from equivalent rendered text.'),
        ('T28', 'Test deterministic JSON-compatible projection.', 'Repeated presentation of unchanged inputs must remain equal and JSON compatible.'),
        ('T29', 'Test every requested authentication rejection case.', 'Each foreign, stale, missing, content-mismatched and misaligned case must fail before publication.'),
    ])
    split_unit('T25', [
        ('T25', 'Inspect the existing pyproject.toml test, coverage and strict typing constraints.', 'The task requires current configured facts rather than assumed defaults.'),
        ('T30', 'Run the protected development validation profile.', 'The future implementation must pass the designated ordinary test boundary.'),
        ('T31', 'Run Ruff, formatting, strict mypy and worktree/index diff checks.', 'The future implementation must pass the separate static and change-integrity gates.'),
        ('T32', 'Do not weaken configuration or run the task-excluded restricted, live-model or Docker validation.', 'The desired validation process has explicit preservation and execution boundaries.'),
    ])
    split_unit('S02', [
        ('S02', 'ContextDisclosure retains plan and ordered items and rejects cardinality/option/representation disagreement; it does not check support-tuple alignment.', 'The manifest consumes the existing disclosure interface and must not presume stronger constructor validation.'),
        ('S15', 'materialize_disclosure_plan checks repository/snapshot applicability, materializes each planned choice once in order, and rejects changed option identity or representation.', 'Establishes the existing realization operation that inspection must preserve without invoking again.'),
    ])
    # Only structure and manifest need preservation of the materialization operation;
    # other obligations use the materialized interface, not its implementation.
    next(u for u in out if u['identity'] == 'S15')['obligations'] = ['structure', 'manifest']
    split_unit('S12', [
        ('S12', 'Current pytest configuration enables strict config/markers and devtools branch coverage with a 100% threshold.', 'The configured test/coverage gate must remain intact.'),
        ('S16', 'Current Ruff configuration targets Python 3.12, an 88-column line length and ALL rules with D203/D213 and test S101 exceptions.', 'Static and formatting checks must use the actual configured policy.'),
        ('S17', 'Current mypy is strict for Python 3.12, covers src/tests/experiments, and uses explicit package bases and src on mypy_path.', 'The future change must satisfy the existing strict type-checking scope.'),
    ])
    return sorted(out, key=lambda u: (u['identity'][0] != 'T', u['identity']))


def minimal_sets(sets):
    unique = sorted(set(frozenset(s) for s in sets), key=lambda s: (len(s), sorted(s)))
    result = []
    for s in unique:
        if not any(t <= s for t in result): result.append(s)
    return result


def witnesses(us, key):
    needed = [u for u in us if key in u['obligations']]
    covers = [frozenset()]
    for u in needed:
        if u['evidence_class'] == 'TASK_BACKED': continue
        covers = minimal_sets(a | frozenset(b['resources']) for a in covers for b in u['support_alternatives'])
    result = []
    for ordinal, resources in enumerate(covers, 1):
        result.append({'identity': key + ':W' + str(ordinal), 'obligation': TASK + '/' + key, 'units': sorted(u['identity'] for u in needed), 'resources': sorted(resources), 'unit_support': {u['identity']: [i + 1 for i, a in enumerate(u['support_alternatives']) if set(a['resources']) <= resources] for u in needed if u['evidence_class'] != 'TASK_BACKED'}})
    return result


def intersection(values):
    values = [set(x) for x in values]
    return sorted(set.intersection(*values)) if values else []


def task_math(obs):
    # Explicit combinations retain witness choices; unions account for evidence reuse.
    combos = []
    resource_unions = set(); unit_unions = set()
    for ws in itertools.product(*(o['witnesses'] for o in obs)):
        combos.append([w['identity'] for w in ws])
        resource_unions.add(tuple(sorted(set().union(*(set(w['resources']) for w in ws)))))
        unit_unions.add(tuple(sorted(set().union(*(set(w['units']) for w in ws)))))
    ru = [list(v) for v in sorted(resource_unions, key=lambda x: (len(x), x))]
    uu = [list(v) for v in sorted(unit_unions, key=lambda x: (len(x), x))]
    return {'combination_order': KEYS, 'complete_combinations': combos, 'combination_count': len(combos), 'sufficient_resource_unions': ru, 'sufficient_unit_unions': uu, 'minimum_resource_count': min(map(len, ru)), 'maximum_resource_count': max(map(len, ru)), 'minimum_unit_count': min(map(len, uu)), 'maximum_unit_count': max(map(len, uu)), 'indispensable_resources': intersection(ru), 'indispensable_units': intersection(uu), 'globally_inclusion_minimal_resource_unions': [sorted(v) for v in minimal_sets(ru)], 'union_semantics': 'All complete obligation-witness combinations are retained, including combinations whose shared task union contains a globally removable resource. Obligation minimality and global inclusion minimality are distinct; the latter is also reported separately.'}


def synopsis(r):
    t = r['text']
    if r['address'].endswith('.py'):
        tree = ast.parse(t)
        return {'description': (ast.get_docstring(tree) or 'Package marker').replace('\n', ' '), 'declarations': [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef))]}
    return {'description': next((v.lstrip('# ').strip() for v in t.splitlines() if v.strip()), 'Empty resource'), 'sections': [v for v in t.splitlines() if v.startswith('#')]}


# Helpful evidence is explicitly authored, never selected by filename similarity.
# Each tuple is resource, affected obligations, precise lines (or entire bounded file), rationale.
HELPFUL = [
 (0, 'structure manifest projection exports documentation', 185, 214, 'Broader ownership and persistence distinctions corroborate the task boundary; they do not define the new operation.'),
 (2, 'structure integrity manifest projection compatibility exports documentation', 621, 645, 'Architecture summarizes the two current representations and their realization boundary but does not supply all exact current interfaces.'),
 (4, 'integrity projection documentation', 57, 78, 'Broader repository/snapshot identity semantics provide context beyond the precise retained lookup contract.'),
 (6, 'structure integrity manifest projection compatibility documentation', 209, 270, 'Disclosure and assembly architecture corroborates scope and semantic-strength limits already prescribed by the task.'),
 (10, 'structure manifest projection exports documentation', 798, 823, 'Taxonomy corroborates caller-directed planning and limits on sufficiency and comprehension.'),
 (12, 'structure manifest documentation', 145, 163, 'Backlog context motivates planning boundaries; it is not an exact current API contract.'),
 (28, 'projection documentation', 1, None, 'Disclosure minimization pressure supplies optional context; no policy engine is requested.'),
 (37, 'projection documentation', 1, None, 'Serialization boundary discussion corroborates the distinction between runtime values and durable representations.'),
 (57, 'tests', 29, 40, 'Describes the ordinary development test boundary useful for retaining regression checks.'),
 (60, 'tests', 3, 27, 'The profile documents a convenient way to retain all ordinary regression checks.'),
 (61, 'structure manifest exports documentation', 324, 330, 'Documentation navigation summarizes package ownership but does not define an additional necessary feature contract.'),
 (63, 'structure manifest documentation', 462, 469, 'Current checkpoint corroborates the two supported representations; no additional implementation decision follows.'),
 (64, 'tests', 35, 78, 'Test/static configuration guides implementation quality; its necessity is assigned to the separate validation obligation.'),
 (65, 'tests', 1, None, 'Existing profile is a convenient regression invocation, separate from the new test semantics.'),
 (83, 'structure manifest tests', 3, 18, 'Public imports corroborate current common names; they do not replace the owning value contracts.'),
 (120, 'structure manifest tests', 1, None, 'Public facade corroborates current common APIs and convenient imports.'),
 (121, 'structure integrity manifest projection compatibility exports tests documentation', 1, 66, 'Package prose describes existing boundaries and is useful editing context; new documentation requirements are already task-backed and precise implementation fields need their current contracts.'),
 (123, 'integrity tests', 53, 103, 'Plan constraints provide defensive test examples and corroborate frame checking; no new plan is constructed by the manifest operation.'),
 (124, 'manifest projection tests', 23, 42, 'Shows the separate existing presentation; useful for keeping inspection independent of rendered output.'),
 (125, 'structure manifest projection tests', 27, 86, 'Concrete whole-resource behavior illustrates representation text and native provenance; a generic manifest consumes the common interface.'),
 (133, 'exports tests', 1, None, 'Python facade gives convenient option imports; common planning exports do not require editing this separate facade.'),
 (138, 'structure manifest exports tests documentation', 53, 86, 'Python-specific prose supplies bounded representation context without defining the generic manifest.'),
 (139, 'manifest projection tests', 98, 154, 'Exact source extraction illustrates byte-column and line-ending fidelity; the manifest consumes already realized text and does not re-extract it.'),
 (140, 'structure integrity manifest projection exports tests', 28, 94, 'Python adapter illustrates source/target support and opaque native values. Its internals remain owned by Python; the generic feature need not inspect those internals.'),
 (141, 'structure integrity manifest projection compatibility tests documentation', 125, 233, 'Qualified-reference validation and materialization provide examples; the manifest authenticates already-materialized common support without repeating semantic derivation.'),
 (142, 'compatibility tests', 1, None, 'Separate Python renderer is regression context; it does not establish exact common renderer output.'),
 (143, 'compatibility tests', 1, None, 'Separate Python assembler corroborates copying semantics but is not proof of the common function body.'),
 (155, 'tests', 173, 252, 'Native module-universe construction is useful fixture setup, not a distinct feature acceptance fact.'),
 (168, 'tests', 40, 160, 'Native analysis construction is useful fixture setup; parser implementation is not a manifest requirement.'),
 (174, 'integrity manifest tests', 1, None, 'Repository facade offers convenient access to retained native types.'),
 (178, 'integrity projection tests', 1, None, 'Nominal repository wrapper implementation corroborates identity presentation and supplies fixture constructors.'),
 (179, 'structure integrity manifest projection tests documentation', 1, 119, 'Observation gives bounded-frame context and fixture setup; inspection must not acquire another observation.'),
 (180, 'structure integrity manifest projection tests', 12, 71, 'Native address and identity validation is useful context for malformed fixtures.'),
 (181, 'structure', 34, 61, 'Snapshot storage corroborates applicability; structural preservation can retain the existing plan without independently authenticating support.'),
 (254, 'compatibility tests', 1, None, 'ModelInteraction documentation explains request context but is unnecessary to establish replace-only-Prompt behavior.'),
 (255, 'compatibility tests', 107, 138, 'The request field list corroborates what dataclasses.replace preserves; no request schema changes are requested.'),
 (257, 'compatibility tests', 1, None, 'Prompt field declaration corroborates role/content copying.'),
 (276, 'projection documentation', 1, None, 'Persistent Evidence ownership provides broader context, already excluded by the task.'),
 (383, 'structure integrity manifest projection compatibility tests', 88, 205, 'Existing mixed and same-resource cases demonstrate faithful order, native preservation and unchanged request behavior. Examples do not establish every negative or exact-output contract.'),
 (391, 'compatibility tests', 65, 127, 'Older full pipeline supplies optional regression context across exact source and request assembly.'),
 (395, 'manifest projection tests', 66, 164, 'Older source-materialization tests illustrate exact bytes and rejection; future inspection must not repeat materialization.'),
 (396, 'integrity manifest projection compatibility tests', 104, 218, 'Qualified-reference tests offer source/target and request fixtures and native behavior examples.'),
 (397, 'compatibility tests', 59, 101, 'Existing Python rendering assertions are useful regression examples, separate from the common renderer body.'),
 (398, 'compatibility tests', 70, 134, 'Existing Python copied-request tests illustrate preservation but do not define the common operation.'),
 (424, 'integrity manifest projection tests documentation', 109, 184, 'Observation tests corroborate exact bytes and resource/content identity distinctions.'),
 (524, 'tests validation', 17, 68, 'Profile tests corroborate the command and exclusion but do not assert the complete argument list; they cannot independently establish that no configuration override is supplied.'),
]


def build_review(p):
    us = units(p)
    obs = []
    for o in p['obligations']:
        ws = witnesses(us, o['key'])
        obs.append({**o, 'applicability_decision': 'APPLICABLE', 'applicability_rationale': 'Explicit mandatory task clause; no task-supported exception applies.', 'required_units': sorted(u['identity'] for u in us if o['key'] in u['obligations']), 'witnesses': ws, 'indispensable_resources': intersection(w['resources'] for w in ws), 'indispensable_units': intersection(w['units'] for w in ws)})
    positives = {}
    for o in obs:
        for resource in set().union(*(set(w['resources']) for w in o['witnesses'])):
            related = [u for u in us if o['key'] in u['obligations'] and any(resource in a['resources'] and any(set(a['resources']) <= set(w['resources']) for w in o['witnesses']) for a in u['support_alternatives'])]
            evidence = []
            for u in related:
                for a in u['support_alternatives']:
                    if resource in a['resources']:
                        evidence.extend(s for s in a['evidence'] if s['source'] == resource)
            evidence = list({(s['source'], s['start'], s['end']): s for s in evidence}.values())
            positives[(resource, o['key'])] = {'label': 'REQUIRED', 'units': [u['identity'] for u in related], 'support_evidence': evidence, 'rationale': 'Necessary in at least one complete minimal witness for ' + o['key'] + ': ' + ' '.join(u['necessity_rationale'] for u in related), 'inferability_rationale': 'Use only the complete direct/inferable support alternatives attached to these units. Alternative resources are substitutes; complementary members must be combined. A resource is not indispensable merely because it is REQUIRED.'}
    for i, keys, a, b, why in HELPFUL:
        for key in keys.split():
            if (rid(i), key) not in positives:
                positives[(rid(i), key)] = {'label': 'HELPFUL_ONLY', 'units': [], 'support_evidence': [span(p, i, a, b)], 'rationale': why, 'inferability_rationale': 'Corroboration or implementation convenience only; no complete minimal witness needs this resource for this obligation.'}
    resources = [{'identity': rid(i), **{k: r[k] for k in ('address', 'content_identity', 'encoding', 'byte_size')}, 'content_review': synopsis(r)} for i, r in enumerate(p['resources'])]
    cells = []
    for r in resources:
        for key in KEYS:
            judgment = positives.get((r['identity'], key), {'label': 'UNNECESSARY', 'units': [], 'support_evidence': [], 'rationale': 'The resource concerns ' + r['content_review']['description'] + '. It supplies no additional material contract needed for ' + key + ' under the exact task and the enumerated necessary semantic units.', 'inferability_rationale': 'No required fact or complete support alternative is established by this resource for this obligation. Shared terminology, general utility and transitive package membership do not establish necessity.'})
            cells.append({'identity': CASE + ':' + r['identity'] + ':' + key, 'resource': r['identity'], 'address': r['address'], 'content_identity': r['content_identity'], 'obligation': TASK + '/' + key, **judgment, 'provenance': 'Original eligible resource text; single primary semantic adjudication. All 531 resources are included in the Cartesian frame.'})
    clauses = []
    coverage = {1: ['structure', 'manifest', 'documentation'], 2: ['structure'], 3: ['integrity'], 4: ['structure', 'manifest'], 5: ['projection'], 6: ['compatibility', 'exports'], 7: ['tests'], 8: ['documentation'], 9: ['validation']}
    for line in range(1, 11):
        clauses.append({'identity': 'C' + str(line).zfill(2), 'task_evidence': task_span(p, line), 'classification': 'ADEQUATELY_REPRESENTED' if line < 10 else 'OPERATIONAL_SCIENTIFIC_INSTRUCTION', 'obligations': coverage.get(line, []), 'rationale': 'All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.' if line < 10 else 'The final paragraph governs the original experimental operation, not mandatory software feature semantics. It neither cancels the nine prospective feature obligations nor instructs this reviewer to implement software.'})
    # Each semicolon/sentence-level requirement is audited separately, while retaining exact text.
    subclauses = []
    for c in clauses[:9]:
        text = c['task_evidence']['text']; base = c['task_evidence']['start']; cursor = 0
        import re
        for match in re.finditer(r'.+?(?:; |\. (?=[A-Z])|\n|$)', text):
            v = match.group(); a = base + match.start(); b = base + match.end()
            if not v.strip(): continue
            subclauses.append({'identity': c['identity'] + '.' + str(sum(s['parent'] == c['identity'] for s in subclauses) + 1), 'parent': c['identity'], 'task_evidence': {'source': 'TASK', 'start': a, 'end': b, 'text': p['task_text'][a:b]}, 'classification': 'ADEQUATELY_REPRESENTED', 'obligations': c['obligations'], 'rationale': c['rationale']})
    limitations = [
        {'identity': 'L01', 'category': 'FUTURE_DESIGN_CHOICE', 'statement': 'The task fixes two new names and required information, but does not fix constructor signatures, helper value types, projection method name, key spelling, or a new digest algorithm. Multiple faithful designs remain valid.', 'evidence': [task_span(p, 4), task_span(p, 5)], 'blocks_complete_adjudication': False},
        {'identity': 'L02', 'category': 'OPAQUE_NATIVE_VALUE', 'statement': 'native_provenance is typed object. Preserve the original value in memory. A JSON-compatible projection must expose selected stable fields rather than promise serialization of arbitrary native objects or infer a universal provenance schema.', 'evidence': [node_span(p, 122, 'MaterializedDisclosureItem'), task_span(p, 4), task_span(p, 5)], 'blocks_complete_adjudication': False},
        {'identity': 'L03', 'category': 'BOUNDED_AUTHENTICATION', 'statement': 'resource_at authenticates addressed membership in the supplied retained snapshot, not filesystem freshness or full semantic truth of opaque provenance. The task forbids reacquisition/rematerialization and does not require recomputing all snapshot/content digests.', 'evidence': [node_span(p, 181, 'RepositorySnapshot'), span(p, 179, 1, 7), task_span(p, 3)], 'blocks_complete_adjudication': False},
        {'identity': 'L04', 'category': 'SUPPORT_CARDINALITY', 'statement': 'Item address/content tuples are not length-checked by the existing ContextDisclosure constructor. Future manifest validation must reject misalignment; repeated support can occur even though a DisclosurePlan rejects identical option identities. The task does not expressly settle whether a zero-support custom option must be rejected.', 'evidence': [node_span(p, 122, 'ContextDisclosure'), node_span(p, 123, 'DisclosurePlan'), node_span(p, 383, 'test_same_resource_reference_uses_same_plan_boundary'), task_span(p, 3)], 'blocks_complete_adjudication': False},
        {'identity': 'L05', 'category': 'BYTE_ACCOUNTING', 'statement': 'Materialized item text includes representation headers and framing, not just raw source. Unique resource totals concern addressed retained source occurrences, not unique hashes or a sum over repeated support records. Either address or address/content pair is a valid unique key within one authenticated frame.', 'evidence': [node_span(p, 125, 'WholeResourceDisclosureOption'), node_span(p, 424, 'test_equal_content_at_two_addresses_retains_distinct_multi_occurrences'), task_span(p, 5)], 'blocks_complete_adjudication': False},
        {'identity': 'L06', 'category': 'BOUNDED_NATIVE_MEANING', 'statement': 'A qualified-reference native value and its direct-call flag retain bounded source meaning; preserving provenance cannot strengthen that into execution or exhaustive semantic coverage.', 'evidence': [node_span(p, 141, 'render_python_qualified_reference_context')], 'blocks_complete_adjudication': False},
        {'identity': 'L07', 'category': 'VALIDATION_ENVIRONMENT', 'statement': 'The frozen frame establishes validation configuration and the protected command; successful future checks and host environment readiness are not established by this adjudication. No repository validation was executed.', 'evidence': [task_span(p, 9), span(p, 64, 35, 78), span(p, 65)], 'blocks_complete_adjudication': False},
    ]
    corrections = [
        'Split compound test acceptance, validation process/configuration and materialization units into independently inspectable facts; final granularity is 32 task-backed and 17 repository-supported units.',
        'Separated future manifest names and test destination from existing repository facts; absence of future files is not a gap.',
        'Removed package overview and broad architecture prose from necessary witnesses when the task already supplies the documentation/scope requirement.',
        'Represented plan-surface evidence from complementary materialization/rendering consumers as an alternative to the plan declaration; retained current-field evidence rather than substituting future task prose.',
        'Kept mixed-choice tests as a defensible alternative source for existing option contracts. Removed exact rendering and assembly bodies as required test-obligation units: retaining existing regression coverage does not require rewriting those assertions. Their current bodies remain necessary to the separate compatibility obligation.',
        'Kept profile documentation, implementation, operating guide and backlog implemented-contract prose as alternatives; demoted profile tests to corroboration because they do not assert the entire argument list. Retained pyproject for precise settings.',
        'Split resource surface from addressed-resource versus content identity. Removed observation-constructor evidence as a standalone proof of every occurrence read attribute, and removed plan constructor examples as a standalone proof of every plan read attribute. Retained these as corroboration where appropriate.',
        'Excluded internal digest reimplementation, source extraction and Python parser internals from necessary units; the manifest consumes retained values.',
        'Removed redundant resource supersets from each obligation witness; computed shared task unions without equating the full REQUIRED union with simultaneous necessity.',
    ]
    return {'schema': 'case-0013-independent-semantic-review-v1', 'case': CASE, 'task_identity': TASK, 'task_text': p['task_text'], 'reviewer': {'model': 'GPT-6 Astra', 'reasoning': 'High', 'review_count': 1, 'basis': 'User-designated primary adjudication; no second reviewer.'}, 'input_hashes': INPUT_HASHES, 'canonical_payload_sha256': PAYLOAD_HASH, 'label_vocabulary': {'REQUIRED': 'Necessary in at least one complete minimal acceptable evidence witness for the obligation.', 'HELPFUL_ONLY': 'Material corroboration, context or implementation convenience, without necessity in a minimal witness.', 'UNNECESSARY': 'No material information required for this obligation.'}, 'applicability_vocabulary': {'APPLICABLE': 'Mandatory without a task-supported exception', 'NOT_APPLICABLE': 'Requires exact task-supported rationale; unused'}, 'task_interpretation_audit': {'clauses': clauses, 'substantive_subclauses': subclauses, 'mandatory_clause_coverage': 'COMPLETE', 'operational_clause_excluded_from_feature_model': 'C10', 'gap': None}, 'resources': resources, 'obligations': obs, 'semantic_units': us, 'cells': cells, 'task_sufficiency': task_math(obs), 'gaps': [{'category': k, 'present': False, 'evidence': [], 'rationale': why, 'blocks_complete_adjudication': False} for k, why in [('TASK_INTERPRETATION_GAP', 'All nine substantive task paragraphs are covered by frozen statements, criteria and exact task basis. The tenth paragraph is operational.'), ('TASK_GAP', 'The task and eligible contracts establish required feature decisions; remaining API design choices permit multiple valid implementations.'), ('REPOSITORY_INFORMATION_GAP', 'Necessary current interfaces, ownership and configured validation contracts have complete eligible support. Future destinations need no prior implementation.')]], 'limitations': limitations, 'unresolved_ambiguity': [{'identity': 'A01', 'limitation': 'L01', 'status': 'BOUNDED_IMPLEMENTATION_CHOICE', 'blocking': False}, {'identity': 'A02', 'limitation': 'L04', 'status': 'ZERO_SUPPORT_CUSTOM_OPTION_UNSPECIFIED', 'blocking': False}], 'unresolved_cell_judgments': [], 'self_review': {'completed': True, 'changes': corrections, 'audited': ['REQUIRED inflation', 'REQUIRED under-selection', 'destination necessity', 'edit target necessity', 'broad prose necessity', 'test necessity', 'validation necessity', 'future/current distinction', 'task-backed facts', 'duplicates', 'missing alternatives', 'redundant witness members', 'witness completeness', 'valid substitutions', 'unit granularity', 'inferability', 'resource union versus necessity', 'implementation choice versus gap']}, 'blindness_attestation': {k: 'NO' for k in ['repository_checkout', 'Git_history', 'parent_directory', 'sibling_workspaces', 'retrieval_queries', 'analyzed_terms', 'acquisition_purposes_intents', 'routing_roles', 'hint_metadata_outside_original_task_text', 'hint_associations', 'locators', 'mechanisms', 'route_decisions', 'experiment_arms', 'route_outcomes', 'ranks', 'scores', 'score_contributions', 'treatment_costs_timings', 'experiment_decision_rules', 'prior_gold', 'prior_adjudication', 'confirmation_data', 'reserve_data', 'external_web_information', 'prior_Codex_session_content']}, 'blindness_scope': 'NO denotes access to excluded external or packet-metadata information. Original task/resource text remains legitimate semantic evidence, including natural names and historical prose. No code from the retained repository was imported or executed.'}


def statistics(r):
    m = r['task_sufficiency']
    counts = Counter(c['label'] for c in r['cells'])
    required = sorted({c['resource'] for c in r['cells'] if c['label'] == 'REQUIRED'})
    classes = Counter(u['evidence_class'] for u in r['semantic_units'])
    return {'schema': 'case-0013-semantic-statistics-v1', 'case': r['case'], 'task_identity': r['task_identity'], 'resource_count': len(r['resources']), 'obligation_count': len(r['obligations']), 'applicable_obligation_count': sum(o['applicability_decision'] == 'APPLICABLE' for o in r['obligations']), 'cell_count': len(r['cells']), 'labels': {k: counts[k] for k in LABELS}, 'labels_by_obligation': {o['key']: {l: sum(c['obligation'] == o['identity'] and c['label'] == l for c in r['cells']) for l in LABELS} for o in r['obligations']}, 'required_resource_union': required, 'required_resource_count': len(required), 'semantic_unit_count': len(r['semantic_units']), 'evidence_classes': {k: classes[k] for k in CLASSES}, 'witness_counts': {o['key']: len(o['witnesses']) for o in r['obligations']}, 'complete_task_combination_count': m['combination_count'], 'distinct_sufficient_resource_union_count': len(m['sufficient_resource_unions']), 'distinct_sufficient_unit_union_count': len(m['sufficient_unit_unions']), **{k: m[k] for k in ['minimum_resource_count', 'maximum_resource_count', 'minimum_unit_count', 'maximum_unit_count', 'indispensable_resources', 'indispensable_units']}, 'obligation_indispensability': {o['key']: {'resources': o['indispensable_resources'], 'units': o['indispensable_units']} for o in r['obligations']}, 'globally_minimal_resource_union_count': len(m['globally_inclusion_minimal_resource_unions']), 'task_clause_count': len(r['task_interpretation_audit']['clauses']), 'substantive_subclause_count': len(r['task_interpretation_audit']['substantive_subclauses']), 'gap_counts': {g['category']: int(g['present']) for g in r['gaps']}, 'limitation_count': len(r['limitations']), 'bounded_ambiguity_count': len(r['unresolved_ambiguity']), 'unresolved_cell_count': len(r['unresolved_cell_judgments'])}


def check_span(s, p):
    if s['source'] == 'TASK':
        t = p['task_text']
    else:
        require(s['source'].startswith('R') and s['source'][1:].isdigit(), 'Invalid support resource')
        i = int(s['source'][1:])
        require(0 <= i < 531 and rid(i) == s['source'], 'Invalid support resource identity')
        rr = p['resources'][i]; t = rr['text']
        require(s.get('address') == rr['address'] and s.get('content_identity') == rr['content_identity'], 'Support content binding')
    require(type(s['start']) is int and type(s['end']) is int and 0 <= s['start'] < s['end'] <= len(t), 'Invalid span offsets')
    require(t[s['start']:s['end']] == s['text'], 'Invalid support span text')
    if 'line_start' in s:
        require(t[:s['start']].count('\n') + 1 == s['line_start'], 'Invalid support start line')
        require(t[:s['end']].count('\n') + (0 if t[s['end'] - 1] == '\n' else 1) == s['line_end'], 'Invalid support end line')


def validate_review(r, p, frozen=None):
    require(r['case'] == CASE and r['task_identity'] == TASK and r['task_text'] == p['task_text'], 'Exact case/task binding')
    require(r['input_hashes'] == INPUT_HASHES and r['canonical_payload_sha256'] == PAYLOAD_HASH, 'Input authentication binding')
    rr = r['resources']; require(len(rr) == 531, 'Exact 531-resource frame')
    for i, resource in enumerate(rr):
        require(resource['identity'] == rid(i), 'Resource frame identity')
        for k in ('address', 'content_identity', 'encoding', 'byte_size'):
            require(resource[k] == p['resources'][i][k], 'Resource frame binding')
    valid_resources = {x['identity'] for x in rr}
    obs = r['obligations']; require(len(obs) == 9, 'Exact obligation frame')
    for o, original in zip(obs, p['obligations'], strict=True):
        for k, v in original.items(): require(o[k] == v, 'Exact obligation contract')
        require(o['applicability_decision'] == 'APPLICABLE', 'Mandatory applicability')
        for s in o['task_basis']: require(p['task_text'][s['start']:s['end']] == s['text'], 'Task basis binding')
    expected_pairs = {(rid(i), TASK + '/' + k) for i in range(531) for k in KEYS}
    cells = r['cells']; require(len(cells) == 4779, 'Complete cell count')
    pairs = [(c['resource'], c['obligation']) for c in cells]
    require(len(set(pairs)) == len(pairs), 'Duplicate cell')
    require(set(pairs) == expected_pairs, 'Missing/altered cell frame')
    uu = r['semantic_units']; uid = {u['identity']: u for u in uu}
    require(len(uid) == len(uu), 'Unique semantic-unit identities')
    for u in uu:
        require(u['evidence_class'] in CLASSES, 'Evidence classification')
        require(u['statement'] and u['necessity_rationale'] and u['inferability_assumptions'] and u['provenance'], 'Semantic-unit required fields')
        require(u['obligations'] and set(u['obligations']) <= set(KEYS), 'Unit obligation membership')
        for s in u['task_evidence']: check_span(s, p)
        if u['evidence_class'] == 'TASK_BACKED':
            require(u['task_evidence'] and not u['support_alternatives'], 'Task-backed evidence')
        else:
            require(u['support_alternatives'], 'Repository unit evidence')
        if u['evidence_class'] == 'REPOSITORY_SUPPORTED': require(not u['task_evidence'], 'Repository evidence classification')
        if u['evidence_class'] == 'TASK_AND_REPOSITORY_SUPPORTED': require(u['task_evidence'], 'Mixed evidence classification')
        for a in u['support_alternatives']:
            require(a['mode'] in {'DIRECT', 'INFERABLE'} and a['inferability_rationale'], 'Support inferability')
            require(a['resources'] and len(a['resources']) == len(set(a['resources'])) and set(a['resources']) <= valid_resources, 'Support resource membership')
            require(set(a['resources']) == {s['source'] for s in a['evidence']}, 'Support evidence/resource correspondence')
            for s in a['evidence']: check_span(s, p)
        require(len(minimal_sets(a['resources'] for a in u['support_alternatives'])) == len(u['support_alternatives']), 'Redundant unit support alternatives')
    for c in cells:
        require(c['identity'] == CASE + ':' + c['resource'] + ':' + c['obligation'].split('/')[-1], 'Altered cell identity')
        resource = rr[int(c['resource'][1:])]
        require(c['address'] == resource['address'] and c['content_identity'] == resource['content_identity'], 'Cell resource identity')
        require(c['label'] in LABELS, 'Invalid label')
        require(set(c['units']) <= set(uid), 'Invalid semantic-unit membership')
        require(c['rationale'] and c['inferability_rationale'] and c['provenance'], 'Cell explanation')
        if c['label'] != 'UNNECESSARY': require(c['support_evidence'], 'Positive support evidence')
        for s in c['support_evidence']:
            check_span(s, p); require(s['source'] == c['resource'], 'Cell span owner')
    for o in obs:
        key = o['key']; expected_units = sorted(u['identity'] for u in uu if key in u['obligations'])
        require(o['required_units'] == expected_units, 'Obligation required units')
        require(o['witnesses'] == witnesses(uu, key), 'Invalid/incomplete/nonminimal witness membership')
        for w in o['witnesses']:
            require(set(w['units']) <= set(uid) and set(w['resources']) <= valid_resources, 'Witness reference integrity')
            # Independent deletion check: every resource is necessary for this cover.
            def covers(rs):
                return all(u['evidence_class'] == 'TASK_BACKED' or any(set(a['resources']) <= rs for a in u['support_alternatives']) for u in uu if key in u['obligations'])
            require(covers(set(w['resources'])), 'Witness completeness')
            require(all(not covers(set(w['resources']) - {v}) for v in w['resources']), 'Witness deletion minimality')
        require(o['indispensable_resources'] == intersection(w['resources'] for w in o['witnesses']), 'Invalid obligation resource intersection')
        require(o['indispensable_units'] == intersection(w['units'] for w in o['witnesses']), 'Invalid obligation unit intersection')
        required = set().union(*(set(w['resources']) for w in o['witnesses']))
        require(required == {c['resource'] for c in cells if c['obligation'] == o['identity'] and c['label'] == 'REQUIRED'}, 'REQUIRED/witness consistency')
    require(r['task_sufficiency'] == task_math(obs), 'Invalid task combinations/unions/intersections')
    require(r['task_sufficiency']['combination_count'] == math.prod(len(o['witnesses']) for o in obs), 'Cartesian product arithmetic')
    for c in r['task_interpretation_audit']['clauses'] + r['task_interpretation_audit']['substantive_subclauses']:
        check_span(c['task_evidence'], p)
        require(set(c['obligations']) <= set(KEYS), 'Clause obligation coverage')
    require({g['category'] for g in r['gaps']} == {'TASK_INTERPRETATION_GAP', 'TASK_GAP', 'REPOSITORY_INFORMATION_GAP'}, 'Gap categories')
    for g in r['gaps']:
        require(type(g['present']) is bool and type(g['blocks_complete_adjudication']) is bool and isinstance(g['evidence'], list) and g['rationale'], 'Gap schema')
        if g['present']: require(g['evidence'], 'Genuine gap evidence')
        for s in g['evidence']: check_span(s, p)
    for l in r['limitations']:
        require(l['identity'] and l['category'] and l['statement'] and l['evidence'] and type(l['blocks_complete_adjudication']) is bool, 'Limitation schema')
        for s in l['evidence']: check_span(s, p)
    require(all(v == 'NO' for v in r['blindness_attestation'].values()), 'Clean primary blindness')
    if frozen is not None:
        require(r == frozen, 'Scientific judgment differs from authored frozen declarations')


def markdown(r, st):
    # All source text in quoted evidence remains original semantic input.
    # Generated prose does not discuss excluded experimental information.
    lines = ['Case 0013 — primary semantic adjudication', '', 'MODEL = GPT-6 Astra; REASONING = High. One adjudication with internal self-review.', '', 'Exact original task (quoted evidence)', '', '~~~~text', r['task_text'].rstrip(), '~~~~', '', 'Task interpretation and applicability', '']
    for c in r['task_interpretation_audit']['clauses']:
        lines += [f"- {c['identity']}: {c['classification']}; obligations: {', '.join(c['obligations']) or 'none (operational)'}. {c['rationale']}"]
    lines += ['', 'Substantive clause audit', '']
    for c in r['task_interpretation_audit']['substantive_subclauses']:
        lines += [f"- {c['identity']} [{c['classification']} → {', '.join(c['obligations'])}]: {c['task_evidence']['text'].strip()}"]
    lines += ['', 'All nine obligations are APPLICABLE. No exception is asserted.', '', 'Complete label counts', '', '| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY | Witnesses |', '|---|---:|---:|---:|---:|']
    for o in r['obligations']:
        v = st['labels_by_obligation'][o['key']]
        lines += [f"| {o['key']} | {v['REQUIRED']} | {v['HELPFUL_ONLY']} | {v['UNNECESSARY']} | {len(o['witnesses'])} |"]
    lines += [f"| TOTAL | {st['labels']['REQUIRED']} | {st['labels']['HELPFUL_ONLY']} | {st['labels']['UNNECESSARY']} | |", '', f"Frame: 531 × 9 = {st['cell_count']} cells. Full identities, explanations and all negative judgments are in stage_c_review.json.", '', 'Complete REQUIRED resource union', '']
    lookup = {v['identity']: v for v in r['resources']}
    for id in st['required_resource_union']:
        v = lookup[id]; lines += [f"- {id}: `{v['address']}`; content identity `{v['content_identity']}`"]
    lines += ['', f"Union size: {st['required_resource_count']}. This is the union over alternatives, not simultaneous necessity.", '', 'Positive cells by obligation', '']
    for o in r['obligations']:
        lines += [o['key'], '', o['statement'], '', 'Satisfaction criterion: ' + o['criterion'], '']
        for c in r['cells']:
            if c['obligation'] == o['identity'] and c['label'] != 'UNNECESSARY':
                lines += [f"- {c['resource']} `{c['address']}` — {c['label']}; units {', '.join(c['units']) or 'corroboration only'}. {c['rationale']}"]
        lines += ['']
    lines += ['Complete semantic-unit inventory', '', f"{st['semantic_unit_count']} units: {st['evidence_classes']['TASK_BACKED']} task-backed; {st['evidence_classes']['REPOSITORY_SUPPORTED']} repository-supported; {st['evidence_classes']['TASK_AND_REPOSITORY_SUPPORTED']} mixed.", '']
    for u in r['semantic_units']:
        lines += [f"{u['identity']} — {u['evidence_class']} — {', '.join(u['obligations'])}", '', u['statement'], '', 'Necessity: ' + u['necessity_rationale'], '', 'Assumptions: ' + u['inferability_assumptions'], '']
        for s in u['task_evidence']: lines += [f"Task [{s['start']}:{s['end']}]."]
        for n, a in enumerate(u['support_alternatives'], 1):
            lines += [f"Alternative {n}: ALL({', '.join(a['resources'])}); {a['mode']}. {a['inferability_rationale']}"]
        lines += ['']
    lines += ['Complete minimal obligation witnesses', '', 'All listed units and resources within a witness are jointly required. Any listed witness for that obligation substitutes for another. Unit evidence alternatives that use already-required resources do not create duplicate resource witnesses.', '']
    for o in r['obligations']:
        lines += [o['key'], '', 'Required units: ' + ', '.join(o['required_units']), '']
        for w in o['witnesses']: lines += [f"- {w['identity']}: ALL(resources: {', '.join(w['resources']) or 'empty'}; units: {', '.join(w['units'])})."]
        lines += ['', 'Obligation-indispensable resources: ' + (', '.join(o['indispensable_resources']) or 'none'), '', 'Obligation-indispensable units: ' + ', '.join(o['indispensable_units']), '']
    m = r['task_sufficiency']
    lines += ['Complete task combinations', '', 'The exact finite product below denotes every complete combination, without imposing an order of resource use. Every tuple is additionally enumerated in the JSON complete_combinations array.', '', ' × '.join('{' + ', '.join(w['identity'] for w in o['witnesses']) + '}' for o in r['obligations']), '', f"Count: {m['combination_count']} = " + ' × '.join(str(len(o['witnesses'])) for o in r['obligations']) + '.', '', 'Distinct sufficient repository-resource unions', '', f"{len(m['sufficient_resource_unions'])} distinct unions; resource-count range {m['minimum_resource_count']}–{m['maximum_resource_count']}. Complete inventory follows.", '']
    for i, v in enumerate(m['sufficient_resource_unions'], 1): lines += [f"- RU{i:04d} ({len(v)}): {', '.join(v)}"]
    lines += ['', 'Distinct sufficient semantic-unit unions', '', f"{len(m['sufficient_unit_unions'])} distinct unions; unit-count range {m['minimum_unit_count']}–{m['maximum_unit_count']}.", '']
    for i, v in enumerate(m['sufficient_unit_unions'], 1): lines += [f"- UU{i:04d}: {', '.join(v)}"]
    lines += ['', 'Task-indispensable resources: ' + ', '.join(m['indispensable_resources']), '', 'Task-indispensable units: ' + ', '.join(m['indispensable_units']), '', 'Globally inclusion-minimal resource unions', '', m['union_semantics'], '']
    for i, v in enumerate(m['globally_inclusion_minimal_resource_unions'], 1): lines += [f"- GM{i:03d}: {', '.join(v)}"]
    lines += ['', 'Gaps, limitations and ambiguity', '']
    for g in r['gaps']: lines += [f"- {g['category']}: {'PRESENT' if g['present'] else 'NONE'}. {g['rationale']}"]
    for l in r['limitations']: lines += [f"- {l['identity']} ({l['category']}): {l['statement']} Blocking: {l['blocks_complete_adjudication']}."]
    for a in r['unresolved_ambiguity']: lines += [f"- {a['identity']}: {a['status']}; see {a['limitation']}; blocking: {a['blocking']}."]
    lines += ['', 'Unresolved cell judgments: none.', '', 'Internal self-review corrections', '']
    lines += ['- ' + c for c in r['self_review']['changes']]
    lines += ['', 'Exact support-span catalogue', '', 'Offsets are half-open Unicode character offsets in the sealed decoded task/resource text. Line numbers are one-based. Repeated uses of one exact span share this catalogue entry; JSON retains spans at each relevant judgment. Original quoted evidence may contain natural repository terminology.', '']
    collected = {}
    def collect(obj):
        if isinstance(obj, dict):
            if {'source', 'start', 'end', 'text'} <= set(obj): collected[(obj['source'], obj['start'], obj['end'])] = obj
            for value in obj.values(): collect(value)
        elif isinstance(obj, list):
            for value in obj: collect(value)
    collect(r['semantic_units']); collect(r['cells']); collect(r['limitations']); collect(r['task_interpretation_audit'])
    for key, s in sorted(collected.items()):
        lines += [f"{s['source']} {s.get('address', 'original task')} [{s['start']}:{s['end']}]" + (f" lines {s['line_start']}–{s['line_end']}" if 'line_start' in s else ''), '', '~~~~text', s['text'].rstrip('\n'), '~~~~', '']
    lines += ['Authentication and method', '', 'The initial five-file whitelist and packet validator passed before output creation. The four declared digest scopes were checked. All original packet bytes are sealed by exact hashes. The builder performs deterministic reconstruction, invariant checks, independent-process byte comparison and adversarial rejection tests. The output hash manifest authenticates scientific files; its own digest is supplied by the operational final report.', '', 'All requested excluded-access categories are NO; confirmation and reserve access are NO. The machine review retains the category-by-category attestation. Original task/resource text is legitimate evidence. No repository checkout or external source was used.', '']
    return ('\n'.join(lines) + '\n').encode('utf-8')


METHOD = '''Case 0013 primary semantic adjudication method

One user-designated GPT-6 Astra / High review with an internal self-review.
Only the original five sealed workspace files supplied semantic evidence.
The initial exact whitelist and python -B validate_packet.py passed before
the builder was created. The builder contains authored scientific judgments;
its cover algorithm does not discover or select semantic judgments.

The complete payload was decoded and integrity-checked. Every native resource
was included in content/structure inspection and the complete Cartesian cell
frame. Existing interfaces, source consumers, tests and documentation were
examined for necessary facts and support alternatives. Source structure and
whole-frame text scans assisted inspection; filenames were not a necessity
rule. Topic summaries retained per resource explain the negative judgments.
Source text is evidence, never instructions to execute that repository.

The task is a prospective feature specification. Task-backed units state future
requirements. Repository-supported units state necessary current contracts.
New files and API names have no invented current resource. The final original
task paragraph is an operational instruction, outside the feature model.

Resources use stable adjudication identifiers R000–R530, each bound to its exact
packet address and native content identity. Support offsets are half-open
Unicode character indices; the packet byte size remains UTF-8 byte size.
Every positive cell retains exact evidence and necessity/inferability rationale.
The same exact evidence may support several obligations without being counted
more than once in a sufficient task resource union.

Each semantic unit has direct or inferable minimal support alternatives.
Corroboration remains HELPFUL_ONLY. Minimal resource covers are computed by
conjoining all required units and pruning strictly redundant resource supersets.
Each resulting witness contains its necessary units plus a minimal resource
cover. Task-backed units require no repository resource. A witness is minimal
relative to the independently authored necessary information model, not a claim
that software implementation needs a complete transitive dependency cookbook.

The complete task combination array is the Cartesian product of obligation
witnesses in the declared obligation order. Sufficient resource/unit unions are
deduplicated from that array. Every obligation witness is minimal, while some
task unions can contain globally redundant resources due to different evidence
choices for shared facts. The review reports both all such sufficient unions
and the globally inclusion-minimal subset, without silently discarding valid
combinations. Indispensability is the appropriate intersection, not the union
of positive labels. The human report uses a lossless finite-product expression
for the complete combination family and prints every distinct sufficient union.

The internal challenge checks temporal mistakes, necessary-versus-convenient
evidence, substitutions, completeness, redundancy and unit granularity. Its
recorded revisions are changes within this one review, not another reviewer.
Bounded API design choices and native semantic limitations remain explicit.

Reproduction (standard library only, Python 3.12 or later):
  python -B -X utf8 stage_c_builder.py --verify

Initial publication only, refusing any pre-existing output:
  python -B -X utf8 stage_c_builder.py --build

The builder reads only its local source and the five packet inputs plus named
scientific outputs during verification. It imports no repository code, accesses
no parent or sibling files, and starts only its own separate Python process for
deterministic byte comparison. No network or repository command is used.
The hash manifest includes the builder and all other scientific artifacts;
its own exact hash is reported separately to avoid a self-hash cycle.
The optional later .local handoff is never scientific input or hashed evidence.
'''


def check_hashes(files, hashes):
    require(hashes['schema'] == 'case-0013-scientific-hashes-v1', 'Hash schema')
    require(set(hashes['sha256']) == set(files), 'Scientific hash scope')
    for name, raw in files.items(): require(sha(raw) == hashes['sha256'][name], 'Tampered scientific hash: ' + name)


def refuse_overwrite(names=OUTPUTS):
    require(all(not (ROOT / name).exists() for name in names), 'Overwrite refusal: a named output already exists')


def adversarial_tests(r, p):
    cases = []
    def mutate(name, change):
        value = copy.deepcopy(r); change(value)
        try: validate_review(value, p, frozen=r)
        except (ValueError, KeyError, IndexError, TypeError, StopIteration): cases.append({'name': name, 'result': 'REJECTED'})
        else: raise ValueError('Mutation accepted: ' + name)
    mutate('altered_cell_identity', lambda v: v['cells'][0].__setitem__('identity', 'changed'))
    mutate('missing_cell', lambda v: v['cells'].pop())
    mutate('duplicate_cell', lambda v: v['cells'].__setitem__(1, copy.deepcopy(v['cells'][0])))
    mutate('invalid_label', lambda v: v['cells'][0].__setitem__('label', 'LIKELY'))
    mutate('invalid_resource_identity', lambda v: v['cells'][0].__setitem__('resource', 'R999'))
    mutate('invalid_support_span', lambda v: next(c for c in v['cells'] if c['support_evidence'])['support_evidence'][0].__setitem__('text', 'not the sealed text'))
    mutate('invalid_semantic_unit_membership', lambda v: v['cells'][0].__setitem__('units', ['S999']))
    mutate('invalid_witness_membership', lambda v: v['obligations'][0]['witnesses'][0]['resources'].append('R999'))
    mutate('incomplete_witness', lambda v: v['obligations'][0]['witnesses'][0]['resources'].pop())
    mutate('redundant_witness_member', lambda v: v['obligations'][0]['witnesses'][0]['resources'].append('R001'))
    mutate('invalid_task_combination', lambda v: v['task_sufficiency']['complete_combinations'][0].__setitem__(0, 'structure:W999'))
    mutate('invalid_sufficient_union', lambda v: v['task_sufficiency']['sufficient_resource_unions'][0].append('R999'))
    mutate('invalid_sufficient_unit_union', lambda v: v['task_sufficiency']['sufficient_unit_unions'][0].append('S999'))
    mutate('invalid_task_indispensability', lambda v: v['task_sufficiency']['indispensable_resources'].append('R001'))
    mutate('invalid_obligation_indispensability', lambda v: v['obligations'][0]['indispensable_units'].append('S999'))
    mutate('altered_task_binding', lambda v: v.__setitem__('task_identity', 'another-task'))
    mutate('invalid_support_classification', lambda v: v['semantic_units'][0].__setitem__('evidence_class', 'ASSUMED'))
    mutate('altered_obligation_criterion', lambda v: v['obligations'][0].__setitem__('criterion', 'changed'))
    hashes = {'schema': 'case-0013-scientific-hashes-v1', 'sha256': {'scientific.json': '0' * 64}}
    try: check_hashes({'scientific.json': canonical(r)}, hashes)
    except ValueError: cases.append({'name': 'tampered_scientific_hash', 'result': 'REJECTED'})
    else: raise ValueError('Tampered hash accepted')
    try: refuse_overwrite(['README.md'])
    except ValueError: cases.append({'name': 'overwrite_refusal', 'result': 'REJECTED'})
    else: raise ValueError('Existing file accepted for overwrite')
    return cases


def artifacts(p):
    r = build_review(p); validate_review(r, p)
    st = statistics(r)
    tests = adversarial_tests(r, p)
    validation = {'schema': 'case-0013-semantic-validation-v1', 'status': 'PASS', 'initial_whitelist': {'status': 'PASS', 'exact_files': sorted(INPUT_HASHES), 'no_subdirectories_links_junctions_reparse_points': True, 'performed_before_output_creation': True}, 'initial_validator_result': 'PASS; NO ADJUDICATION', 'packet_digest_scopes': {'archive_sha256': INPUT_HASHES['resources.json.gz'], 'canonical_payload_sha256': PAYLOAD_HASH, 'manifest_sha256': INPUT_HASHES['manifest.json'], 'integrity_sha256': INPUT_HASHES['integrity.json']}, 'sealed_input_hashes': INPUT_HASHES, 'checks': ['exact case/task/obligation binding', 'exact 531-resource frame', '4779 unique complete qualified cells', 'label vocabulary', 'resource identities and native content identities', 'exact support text/offset/line spans', 'unique semantic-unit identities', 'evidence classification and support alternatives', 'unit/obligation memberships', 'witness completeness and resource-deletion minimality', 'REQUIRED/witness correspondence', 'Cartesian task combinations', 'resource and unit unions', 'obligation and task intersections', 'gap and limitation schemas', 'deterministic statistics', 'deterministic Markdown', 'scientific output hashes', 'overwrite refusal'], 'adversarial_tests': tests, 'adversarial_test_count': len(tests), 'deterministic_replay': {'mode': 'Separate python -B process rebuilds all publication bytes in memory; publisher/verify compares the complete length-framed artifact byte stream directly for exact equality, in addition to artifact SHA-256 authentication.', 'status': 'PASS', 'no_timestamp_or_environment_dependent_fields': True}, 'original_packet_preservation': 'PASS: all five sealed input byte hashes match', 'blindness': 'PASS: every excluded-access category is NO', 'scope': 'Structural invariants and exact evidence are mechanically validated; semantic judgments are the single primary reviewer decisions retained in the builder and review.'}
    files = {'stage_c_review.json': canonical(r), 'stage_c_statistics.json': canonical(st), 'STAGE_C_REVIEW.md': markdown(r, st), 'stage_c_validation.json': canonical(validation), 'stage_c_method.md': METHOD.encode('utf-8')}
    hashed = {**files, 'stage_c_builder.py': (ROOT / 'stage_c_builder.py').read_bytes()}
    hashes = {'schema': 'case-0013-scientific-hashes-v1', 'case': CASE, 'task_identity': TASK, 'algorithm': 'SHA-256', 'sha256': {name: sha(raw) for name, raw in sorted(hashed.items())}, 'excluded': ['stage_c_hashes.json (its digest is reported separately to avoid self-reference)', '.local/codex-result.md (operational handoff only)']}
    check_hashes(hashed, hashes)
    files['stage_c_hashes.json'] = canonical(hashes)
    return files


def independent_replay(files):
    result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(ROOT / 'stage_c_builder.py'), '--replay-bytes'], cwd=ROOT, check=True, capture_output=True)
    require(result.stdout == replay_bytes(files), 'Separate-process exact byte identity')


def replay_bytes(files):
    # Length framing makes the direct byte comparison unambiguous even if an
    # artifact contains another filename or arbitrary embedded source text.
    result = bytearray()
    for name, raw in sorted(files.items()):
        encoded = name.encode('utf-8')
        result.extend(len(encoded).to_bytes(8, 'big')); result.extend(encoded)
        result.extend(len(raw).to_bytes(8, 'big')); result.extend(raw)
    return bytes(result)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--build', action='store_true')
    mode.add_argument('--verify', action='store_true')
    mode.add_argument('--fingerprint', action='store_true', help=argparse.SUPPRESS)
    mode.add_argument('--replay-bytes', action='store_true', help=argparse.SUPPRESS)
    args = ap.parse_args()
    p = packet()
    if args.build: refuse_overwrite()
    files = artifacts(p)
    if args.fingerprint:
        sys.stdout.buffer.write(canonical({name: sha(raw) for name, raw in sorted(files.items())})); return
    if args.replay_bytes:
        sys.stdout.buffer.write(replay_bytes(files)); return
    independent_replay(files)
    if args.build:
        require(not (ROOT / '.local').exists(), 'Operational handoff must not precede scientific publication')
        for name, raw in files.items():
            with (ROOT / name).open('xb') as f: f.write(raw)
    else:
        for name, raw in files.items(): require((ROOT / name).read_bytes() == raw, 'Deterministic reconstruction differs: ' + name)
        actual = json.loads((ROOT / 'stage_c_review.json').read_bytes())
        validate_review(actual, p, frozen=build_review(p))
        check_hashes({name: (ROOT / name).read_bytes() for name in json.loads((ROOT / 'stage_c_hashes.json').read_bytes())['sha256']}, json.loads((ROOT / 'stage_c_hashes.json').read_bytes()))
        refusal = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(ROOT / 'stage_c_builder.py'), '--build'], cwd=ROOT, capture_output=True)
        require(refusal.returncode != 0 and b'Overwrite refusal' in refusal.stderr, 'Actual publication overwrite refusal')
    packet()
    sys.stdout.buffer.write(canonical({'status': 'PASS', 'operation': 'build' if args.build else 'verify', 'separate_process_replay': 'PASS', 'original_packet_bytes': 'PRESERVED', 'scientific_sha256': {**{name: sha(raw) for name, raw in sorted(files.items())}, 'stage_c_builder.py': sha((ROOT / 'stage_c_builder.py').read_bytes())}}))


if __name__ == '__main__':
    main()
