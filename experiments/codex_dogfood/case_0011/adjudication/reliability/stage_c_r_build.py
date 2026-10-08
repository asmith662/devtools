"""Self-contained independent Case 0011 Stage C-R adjudication and replay.

Reads only explicitly named files in this workspace. Never imports packet code.
"""
from __future__ import annotations

import argparse
import ast
import collections
import gzip
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).absolute().parent
INPUTS = ('task.txt', 'manifest.json', 'resources.json.gz', 'README.md',
          'FRESH_STAGE_C_INSTRUCTIONS.md', 'integrity.json', 'STAGE_C_R_INSTRUCTIONS.md')
GENERATED = ('stage_c_r_review.json', 'stage_c_r_statistics.json', 'stage_c_r_method.md')
SUPPORT = ('stage_c_r_build.py', 'stage_c_r_test.py', 'stage_c_r_pytest.ini')
SEALED = ('stage_c_r_validation.json', 'stage_c_r_sha256.json')
WHITELIST = set(INPUTS + GENERATED + SUPPORT + SEALED)
EXPECTED = {
    'resources.json.gz': 'd8cf340e1b892553944a773d2d2dc309a02ddbd28aa12213e9906047d3cc2a',
    'manifest.json': '561adee989446481819e582a88ce6598db7f6e545d9bc5875788c0541be58036',
    'integrity.json': 'e757fd33c8354a359df7c702015721bb80c315546100b5c1a741f1b1924636ab',
}
# Exact archive binding, written separately to make transcription explicit.
EXPECTED['resources.json.gz'] = 'd8cf340e1b892553944a773d2d2dc309a02ddbd28aa122fa13e9906047d3cc2a'
PAYLOAD_DIGEST = 'c242ecb757375be95d5452ef178bd5cf95a6ac7113fa60f99db496af86701ed4'
FRAME = {
    'case_identity': 'case-0011',
    'task_identity': 'case-0011-context-utf8-ceiling',
    'repository_id': '5cf96d9e-d6a5-44a6-83d3-1e24f6e00009',
    'snapshot_id': '981d67d6678d538776f2e400d79156b6e92fed048ee9af57b5a3a0a6e5f4cd17',
    'corpus_id': '1e9d78ac0f6c2ca788c161649450bc70f953ea084b97b5f403344655f78721e4',
}
OBLIGATIONS = ('ownership', 'bytes', 'ceiling', 'request', 'frame', 'exports',
               'tests', 'documentation', 'validation')
ATTESTATIONS = {name: 'NO' for name in (
    'parent/sibling filesystem accessed', 'repository checkout accessed',
    'Git history accessed', 'primary Stage C gold accessed',
    'prior adjudication statistics accessed', 'information needs accessed',
    'queries accessed', 'treatment results accessed', 'arm identities accessed',
    'ranks/scores accessed', 'confirmation accessed', 'Stage C.5 performed',
    'Stage D performed')}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    """Output-only canonicalization; never applied as an input acceptance rule."""
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def workspace_check():
    observed = []
    def walk(folder):
        for entry in os.scandir(folder):
            stat = entry.stat(follow_symlinks=False)
            assert not entry.is_symlink(), 'Link rejected'
            assert not (getattr(stat, 'st_file_attributes', 0) & 1024), 'Reparse point rejected'
            relative = str(Path(entry.path).relative_to(ROOT))
            observed.append(relative)
            if entry.is_dir(follow_symlinks=False):
                raise AssertionError('Unexpected directory: ' + relative)
    walk(ROOT)
    assert set(observed) <= WHITELIST, 'Unexpected workspace entries'
    assert set(INPUTS) <= set(observed)
    return sorted(observed)


def packet():
    workspace_check()
    raw = {name: (ROOT / name).read_bytes() for name in INPUTS}
    for name, expected in EXPECTED.items():
        assert digest(raw[name]) == expected, name
    integrity = json.loads(raw['integrity.json'])
    for name, expected in integrity['sha256'].items():
        assert name in INPUTS and digest(raw[name]) == expected, name
    manifest = json.loads(raw['manifest.json'])
    assert integrity['manifest_sha256'] == digest(raw['manifest.json'])
    assert manifest['archive_sha256'] == integrity['archive_sha256'] == digest(raw['resources.json.gz'])
    payload_bytes = gzip.decompress(raw['resources.json.gz'])
    assert digest(payload_bytes) == PAYLOAD_DIGEST == manifest['canonical_payload_sha256'] == integrity['canonical_payload_sha256']
    payload = json.loads(payload_bytes)
    assert manifest['task'] == raw['task.txt'].decode('utf-8')
    assert digest(raw['task.txt']) == manifest['task_sha256']
    for key, expected in FRAME.items():
        assert manifest[key] == expected
        if key in payload:
            assert payload[key] == expected
    assert tuple(o['identity'] for o in manifest['obligations']) == OBLIGATIONS
    assert manifest['resource_count'] == len(payload['resources']) == 531
    assert manifest['obligation_count'] == len(manifest['obligations']) == 9
    assert manifest['expected_cell_count'] == 531 * 9 == 4779
    resources = {r['address']: r for r in payload['resources']}
    assert len(resources) == 531
    for r in resources.values():
        assert set(r) == {'address', 'byte_size', 'content', 'content_identity', 'encoding'}
        assert r['encoding'] == 'utf-8'
        assert len(r['content_identity']) == 64
    # Task provenance uses frozen character offsets, not reformatted text.
    for o in manifest['obligations']:
        assert o['applicability_condition'] is None
        assert o['requirement'] == 'mandatory'
        for basis in o['task_basis']:
            assert manifest['task'][basis['start']:basis['end']] == basis['text']
            assert manifest['task'][:basis['start']].count('\n') + 1 == basis['line']
    return manifest, resources, {name: digest(data) for name, data in sorted(raw.items())}


P = 'src/devtools/context/planning/'
M = 'src/devtools/models/interaction/'
T = 'tests/context/planning/test_plan.py'
A = 'docs/architecture.md'
D = P + 'docs/overview.md'
Q = 'src/devtools/context/python/function/'
N = 'tests/models/interaction/test_models.py'
V = 'docs/development/validation.md'


def adjudicate():
    manifest, resources, bindings = packet()
    units = []
    def unit(uid, path, spans, statement, necessity):
        content = resources[path]['content']
        lines = content.splitlines(keepends=True)
        supports = []
        for first, last in spans:
            excerpt = ''.join(lines[first-1:last])
            start = len(''.join(lines[:first-1]))
            supports.append({'first_line': first, 'last_line': last,
                             'start_character': start, 'end_character': start + len(excerpt),
                             'excerpt': excerpt, 'excerpt_sha256': digest(excerpt.encode('utf-8'))})
        units.append({'id': uid, 'statement': statement,
                      'resource': identity(resources[path]),
                      'content_sha256': digest(content.encode('utf-8')),
                      'supports': supports, 'necessity_rationale': necessity,
                      'inferability': 'INFERABLE_AT_START',
                      'inherent_discovery_prerequisites': [],
                      'manual_review': {
                          'exact_information': statement,
                          'required_not_merely_helpful': necessity,
                          'granularity': 'Only the cited contract or implementation slice is a unit; the containing file is not a semantic unit.',
                          'relationship': 'Complementary within each named alternative; competing alternatives are explicitly separate.',
                          'start_inferability': 'Ordinary inspection of frozen repository contents suffices.',
                          'evidence_scope': 'Blind packet only.'}})

    unit('O1', A, [(633,645)],
         'Common Context Planning owns ordered caller-directed plans, faithful materialization, then rendering and copied request assembly; it is not an automatic planner or retrieval operation.',
         'Establishes the existing common owner and the boundary the added check must preserve.')
    unit('O2', D, [(3,8),(43,59)],
         'The planning package owns explicit plans, materialization, rendering and copied assembly, with whole-resource and qualified-reference choices and no automatic selection.',
         'An alternative package contract establishes the same concrete ownership boundary as O1.')
    unit('O3', P+'rendering.py', [(6,12)],
         'Common rendering uses dataclass replacement and ModelRequest/Prompt, with ContextDisclosure as a type-only dependency and no language adapter or Retrieval import.',
         'Identifies the actual dependency seam where byte admission can be added without reversing dependency direction.')
    unit('B1', P+'rendering.py', [(27,42)],
         'Rendered Context contains its purpose, plan and snapshot identities, item count, ordered item headings, option identities and exact item.text; joining inserts only the explicit separators.',
         'The byte count must cover this complete rendered string, not only source text or character count, and preserve item newlines.')
    unit('B2', P+'rendering.py', [(51,65)],
         'Assembly separately encodes task_text and context.text as UTF-8, reports their byte lengths, and places context.text unchanged inside an outer task/Context envelope.',
         'Locates the existing Context counting boundary and distinguishes it from task bytes and outer envelope separators.')
    unit('C1', M+'models.py', [(12,18)],
         'The optional numeric request validator returns for None, rejects bool and non-int using ValueError, and rejects values below its positive domain.',
         'Provides the closest request-side optional integer/error convention; the new nonnegative domain and equality rule come from the task, not this positive-token precedent.')
    unit('C2', N, [(31,48)],
         'Numeric request tests accept positive integers and None and expect ValueError for zero, negatives, bool, string and float.',
         'An executable specification is an alternative witness to C1 for the request numeric validation convention; zero acceptance must deliberately differ for the new ceiling.')
    unit('C3', P+'rendering.py', [(45,50),(67,70)],
         'The existing common assembly entry point is keyword-only, consumes RenderedContextDisclosure, and constructs the copied request only at the final dataclasses.replace call.',
         'A rejecting limit must be admitted before the construction point while retaining the unlimited call path.')
    unit('R1', P+'rendering.py', [(67,70)],
         'Assembly replaces only prompt and explicitly retains the caller Prompt role.',
         'This is the copy mechanism preserving all other request fields rather than manually reconstructing a subset.')
    unit('R2', M+'models.py', [(98,106)],
         'ModelRequest is frozen and contains prompt, settings, conversation, provider_settings and tools.',
         'Defines the complete current request field inventory, including tools, for preservation and failure assertions.')
    unit('F1', P+'plan.py', [(60,86)],
         'DisclosurePlan carries repository/snapshot identities and ordered disclosures; construction rejects blank purpose, empty choices, mixed purposes or frames, and duplicate choices.',
         'These existing plan admission constraints must survive addition of a byte limit; zero capacity does not authorize empty plans.')
    unit('F2', P+'materialization.py', [(24,51)],
         'Immutable materialized items retain text, resource and content identities and native provenance; ContextDisclosure aligns item count, order, option identity and representation with its plan.',
         'Defines exactly which ordered native values must remain unchanged on success and rejection.')
    unit('F3', P+'materialization.py', [(79,92)],
         'Materialization rejects a foreign repository or snapshot, realizes each ordered option, and rejects option identity/representation drift before publishing a disclosure.',
         'Locates the existing common frame validation; byte checking cannot bypass or substitute for it.')
    unit('F4', P+'resource.py', [(50,65),(79,86)],
         'Whole-resource realization rejects foreign, missing or unequal retained occurrences and retains the observed resource as native provenance with its content identity.',
         'Establishes whole-resource stale/content protection and the native identity contract to preserve.')
    unit('F5', Q+'planned_reference.py', [(57,78)],
         'The qualified-reference plan adapter delegates to the existing validated materializer, retains its rendered text, both source/target identities and the native materialized value.',
         'Establishes how the second existing representation participates without importing it into common capacity code.')
    unit('F6', Q+'qualified_reference.py', [(142,180)],
         'Qualified-reference materialization checks source repository/snapshot/address and retained content, target snapshot and dependency identity, and equality with retained target support.',
         'Defines the exact source/target frame protections named by the frozen obligation, which cannot be replaced by byte admission.')
    unit('F7', Q+'qualified_reference.py', [(181,212)],
         'Qualified-reference target module interpretation and any retained declaration analysis must match the target resource and repository/snapshot frame.',
         'Complements the source/target checks: preservation includes native resolution support, not just matching file text.')
    unit('E1', P+'__init__.py', [(15,19),(25,38)],
         'The planning package imports and lists the common renderer, rendered value and assembler in __all__.',
         'The optional argument belongs on this existing public assembler; any new public helper must follow this explicit export convention.')
    unit('E2', 'src/devtools/context/__init__.py', [(4,17),(211,211),(224,224),(229,231)],
         'The outer Context facade re-exports the common planning assembler and its companion planning/materialization/rendering functions.',
         'Establishes the second public surface whose existing callable must continue exposing the added optional argument.')
    unit('T1', T, [(49,61)],
         'Planning tests create exact UTF-8 files with write_bytes and observe an explicit resource collection into a snapshot.',
         'Provides the local fixture convention for exercising real non-ASCII and newline behavior without accidental text-mode normalization.')
    unit('T2', T, [(89,108),(136,163)],
         'The mixed-plan test uses CRLF and non-ASCII text in qualified-reference and whole-resource options and asserts exact source, provenance and rendered order.',
         'Provides the existing focused regression pattern for both supported representations and their exact-text contract.')
    unit('T3', T, [(164,185)],
         'The common assembly test asserts unchanged task, role, shared settings/continuation/provider values, ordered Context placement and replacement equivalence.',
         'Provides the actual common-assembly preservation assertions to extend for bounded success and failure; R2 identifies the additional tools field.')
    unit('T4', T, [(241,263),(321,337)],
         'Planning tests exercise changed snapshots, stale content under a retained snapshot identity, missing resources and mismatched realized items using replace and pytest.raises.',
         'Provides the existing frame-invalidating fixture pattern needed for focused stale/foreign regressions.')
    unit('D1', A, [(3,10),(633,645)],
         'Architecture.md is the canonical cross-package overview and describes the current caller-directed planning, realization and assembly boundary.',
         'The explicit architecture documentation update requires knowing this current implemented claim and its authority.')
    unit('D2', D, [(43,68)],
         'Package documentation describes exact materialization, appended Context, the two concrete choices, and no selected token-budget field or universal cost function.',
         'The bounded byte feature must be documented here without falsely promoting automatic planning or a token budget.')
    unit('D3', D, [(76,78)],
         'The package currently says plan_disclosures remains caller-directed and does not establish representation coverage/capacity.',
         'The documentation update must distinguish a new assembly byte check from unchanged plan-level capacity/coverage claims.')
    unit('V1', V, [(5,24)],
         'The protected command is uv run python scripts/validate_development.py; it excludes tests/experiments before collection and preserves project pytest configuration, branch coverage and the 100 percent gate.',
         'Establishes the exact protected development invocation and its required collection/configuration boundary.')
    unit('V2', 'AGENTS.md', [(228,239)],
         'Operating rules name the protected uv script command, require the experiment-tree exclusion and configured coverage gate, and require separate static checks.',
         'Together with V3 this is an alternative operating-rule plus implementation witness for the protected test contract.')
    unit('V3', 'scripts/validate_development.py', [(14,27)],
         'The protected script constructs tests and --ignore=tests/experiments arguments, invokes pytest.main and returns its exit code.',
         'Complements V2 with implemented selection and failure propagation rather than relying solely on the prose validation contract.')
    unit('V4', V, [(31,44)],
         'Protected tests do not run static gates; separate Ruff lint, Ruff format, mypy and diff checks are documented.',
         'The task asks for established tooling configuration and protected validation, which includes knowing the separate quality gates. These commands are evidence only, not executed in this adjudication.')
    unit('V5', 'pyproject.toml', [(34,78)],
         'Project settings enforce strict pytest configuration/markers, production branch coverage at 100 percent, Ruff ALL with documented exceptions and Python 3.12, and strict mypy over src/tests/experiments with src import base.',
         'Defines current concrete test/type/style settings; generic tool names cannot establish these constraints.')

    alternatives = {
        'ownership': [('owner-architecture', ['O1','O3']), ('owner-package', ['O2','O3'])],
        'bytes': [('rendered-text', ['B1','B2'])],
        'ceiling': [('numeric-source', ['C1','C3']), ('numeric-tests', ['C2','C3'])],
        'request': [('copy-contract', ['B2','R1','R2'])],
        'frame': [('native-frame-contract', ['F1','F2','F3','F4','F5','F6','F7'])],
        'exports': [('both-public-facades', ['E1','E2'])],
        'tests': [('focused-regressions', ['T1','T2','T3','T4','C2'])],
        'documentation': [('current-claims', ['D1','D2','D3'])],
        'validation': [('documented-profile', ['V1','V4','V5']),
                       ('operating-rule-and-script', ['V2','V3','V4','V5'])],
    }
    explanations = {
        'ownership': 'Task lines 1 and 7 explicitly locate common capacity ownership; current common assembly is implemented.',
        'bytes': 'Task line 3 explicitly requires exact UTF-8 rendered-text accounting and existing newline preservation.',
        'ceiling': 'Task lines 2, 4 and 5 explicitly require optional admission, nonnegative integers, bool rejection, equality and rejection without reduction.',
        'request': 'Task lines 1, 3 and 6 explicitly require copied-request, task and all-field preservation.',
        'frame': 'Task lines 2, 6 and 7 explicitly preserve materialized plan provenance, ordering, frames and both representations.',
        'exports': 'Task line 8 explicitly requires public export conventions, and two facades already expose this assembler.',
        'tests': 'Task line 8 explicitly requires focused tests; current common fixtures and numeric-request tests provide usable conventions.',
        'documentation': 'Task line 9 explicitly requires governing architecture and package documentation updates.',
        'validation': 'Task line 9 explicitly requires protected development validation with established tool configuration.',
    }
    helpful = {
        'ownership': [P+'__init__.py', P+'plan.py', Q+'planned_reference.py', 'docs/architecture/taxonomy.md', 'docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md'],
        'bytes': [D, T, P+'resource.py', Q+'rendering.py', Q+'request_assembly.py', 'tests/context/python/function/test_rendering.py', 'tests/context/python/function/test_request_assembly.py'],
        'ceiling': [P+'materialization.py', P+'plan.py', M+'usage.py', 'src/devtools/resources/filesystem/reading.py', 'tests/resources/filesystem/test_reading.py', T],
        'request': [M+'prompt.py', M+'docs/overview.md', T, N, Q+'request_assembly.py', 'tests/context/python/function/test_request_assembly.py'],
        'frame': [D, T, P+'rendering.py', 'src/devtools/context/repository/snapshot.py', 'src/devtools/context/repository/resource.py', 'src/devtools/context/repository/observation.py', Q+'materialization.py', 'tests/context/python/function/test_qualified_reference.py', 'tests/context/python/function/test_materialization.py'],
        'exports': [D, T, 'AGENTS.md'],
        'tests': [P+'rendering.py', P+'materialization.py', P+'resource.py', M+'models.py', 'tests/context/python/function/test_request_assembly.py', 'tests/context/python/function/test_rendering.py', 'tests/context/python/function/test_qualified_reference.py', 'tests/context/repository/test_observation.py', 'tests/resources/filesystem/test_reading.py'],
        'documentation': ['AGENTS.md', 'docs/documentation_map.md', 'docs/architecture/taxonomy.md', 'docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md', P+'rendering.py', T],
        'validation': ['tests/scripts/test_validate_development.py', 'docs/backlog/items/B-0047-protected-development-validation-profile.md'],
    }
    by_id = {u['id']: u for u in units}
    judgments = []
    for obligation in manifest['obligations']:
        oid = obligation['identity']
        alts = [{'id': name, 'all_units': ids,
                 'all_resources': sorted({by_id[u]['resource']['address'] for u in ids})}
                for name, ids in alternatives[oid]]
        judgments.append({'frozen_obligation': obligation, 'applicability': 'APPLICABLE',
                          'applicability_rationale': explanations[oid],
                          'alternatives_any': alts, 'repository_information_gap': 'NONE',
                          'inherent_discovery_prerequisites': []})
    for u in units:
        u['witness_memberships'] = [{'obligation': oid, 'alternative': name}
                                    for oid in OBLIGATIONS for name, ids in alternatives[oid]
                                    if u['id'] in ids]
        u['owning_obligations'] = sorted({m['obligation'] for m in u['witness_memberships']})
    cells = []
    for oid in OBLIGATIONS:
        for path, resource in sorted(resources.items()):
            ids = sorted({u for _, members in alternatives[oid] for u in members
                          if by_id[u]['resource']['address'] == path})
            label = 'REQUIRED' if ids else 'HELPFUL_ONLY' if path in helpful[oid] else 'UNNECESSARY'
            reason = ('Necessary supporting units in at least one complete named alternative.' if ids else
                      'Corroboration, analogous behavior or local navigation; no additional mandatory fact is needed from this resource.' if label == 'HELPFUL_ONLY' else
                      'No necessary or materially useful obligation-specific information beyond the identified contract witnesses; content belongs to another concern or is package scaffolding.')
            cells.append({'obligation': oid, 'resource': identity(resource), 'label': label,
                          'required_units': ids, 'rationale': reason})
    limitations = [
        {'id': 'L1', 'statement': 'Task names ContextDisclosure as input, but the existing assembler accepts RenderedContextDisclosure. The sound bounded interpretation is to retain materialization and rendering before common assembly, or add a compatible wrapper; changing the public input type is not compelled.', 'units': ['C3','F2'], 'task_lines': [1,2]},
        {'id': 'L2', 'statement': 'Rendered Context headings/separators are distinct from the outer assembly envelope. This review interprets the ceiling as len(context.text.encode("utf-8")), matching the existing Context byte-length field. The task wording does not explicitly resolve whether outer envelope markers count; no existing byte-ceiling contract settles that alternative.', 'units': ['B1','B2'], 'task_lines': [3]},
        {'id': 'L3', 'statement': 'Zero is a valid ceiling, but valid plans are nonempty and canonical rendering always emits headings. No canonical valid disclosure currently renders to zero bytes. The task does not authorize weakening plan invariants to manufacture a zero-byte example.', 'units': ['F1','B1'], 'task_lines': [5]},
        {'id': 'L4', 'statement': 'Foreign/stale checks occur during planning and materialization. Assembly has no fresh snapshot argument and cannot discover later filesystem changes. Preserve existing checks; do not interpret the task as requiring new current-state validation at assembly.', 'units': ['C3','F3','F4','F6'], 'task_lines': [2,6,8]},
        {'id': 'L5', 'statement': 'Existing numeric errors are not uniform: request maximum-output validation uses ValueError for invalid types, while ModelUsage uses TypeError for non-integers and ValueError for negatives. This review prefers the request-side precedent; the task does not prescribe a new exception class or message.', 'units': ['C1','C2'], 'additional_support': support(resources[M+'usage.py'],22,29), 'task_lines': [4,8]},
    ]
    review = {
        'schema': 'case-0011-stage-c-r-independent-review-v1',
        'adjudication': 'Independent reliability adjudication',
        'frame': FRAME, 'frozen_manifest': manifest, 'input_sha256': bindings,
        'initial_sterility': {'preexisting_files': sorted(INPUTS), 'unexpected_preexisting_files': 0,
                             'git_absent': True, 'symlinks_absent': True, 'reparse_points_absent': True,
                             'treatment_outputs_absent': True, 'prior_gold_absent': True},
        'resources': [identity(r) for _,r in sorted(resources.items())],
        'obligations': judgments, 'required_information_units': units,
        'cells': cells, 'task_gap': 'NONE', 'supplemental_task_gap_units': [],
        'task_gap_rationale': 'All affirmative requirements are represented by the nine obligations. The final task line constrains scope rather than adding a new repository-information requirement; common ownership, faithful realization and pure copying cover those exclusions. Operating rules do not add an unrepresented semantic feature requirement.',
        'task_interpretation_limitations': limitations,
        'repository_information_gap': 'NONE',
        'repository_gap_rationale': 'The existing API, representations, validation precedents, test patterns, exports, documentation and tooling are available. New code, new boundary tests and their future outcomes are implementation work, not missing existing information.',
        'inherent_discovery_prerequisites': [],
        'protocol_limitations': ['STAGE_C_R_INSTRUCTIONS.md specifies neither exact output filenames nor a machine-readable output schema. Explicit stage_c_r names and this versioned schema are local choices, not purported protocol requirements.'],
        'blindness_attestations': ATTESTATIONS,
    }
    validate_review(review, resources)
    return review


def identity(resource):
    return {**{k: FRAME[k] for k in ('repository_id','snapshot_id','corpus_id')},
            **{k: resource[k] for k in ('address','content_identity')}}


def support(resource, first, last):
    lines = resource['content'].splitlines(keepends=True)
    excerpt = ''.join(lines[first-1:last])
    return {'resource': identity(resource), 'first_line': first, 'last_line': last,
            'excerpt': excerpt, 'excerpt_sha256': digest(excerpt.encode('utf-8'))}


def validate_review(review, resources):
    units = {u['id']: u for u in review['required_information_units']}
    assert len(units) == len(review['required_information_units'])
    assert review['resources'] == [identity(r) for _,r in sorted(resources.items())]
    assert [o['frozen_obligation']['identity'] for o in review['obligations']] == list(OBLIGATIONS)
    for u in units.values():
        r = resources[u['resource']['address']]
        assert u['resource'] == identity(r)
        assert u['content_sha256'] == digest(r['content'].encode('utf-8'))
        assert u['witness_memberships']
        for s in u['supports']:
            assert r['content'][s['start_character']:s['end_character']] == s['excerpt']
            assert ''.join(r['content'].splitlines(keepends=True)[s['first_line']-1:s['last_line']]) == s['excerpt']
            assert digest(s['excerpt'].encode('utf-8')) == s['excerpt_sha256']
    for limitation in review['task_interpretation_limitations']:
        if 'additional_support' in limitation:
            s = limitation['additional_support']; r = resources[s['resource']['address']]
            assert s == support(r,s['first_line'],s['last_line'])
    expected = {(o,p) for o in OBLIGATIONS for p in resources}
    observed = [(c['obligation'],c['resource']['address']) for c in review['cells']]
    assert len(observed) == len(set(observed)) == 4779
    assert set(observed) == expected
    for o in review['obligations']:
        oid = o['frozen_obligation']['identity']
        assert o['alternatives_any']
        required = set()
        for alt in o['alternatives_any']:
            assert len(alt['all_units']) == len(set(alt['all_units']))
            assert set(alt['all_units']) <= units.keys()
            assert alt['all_resources'] == sorted({units[u]['resource']['address'] for u in alt['all_units']})
            required.update(alt['all_units'])
        for cell in (c for c in review['cells'] if c['obligation'] == oid):
            assert cell['resource'] == identity(resources[cell['resource']['address']])
            wanted = sorted(u for u in required if units[u]['resource'] == cell['resource'])
            assert cell['required_units'] == wanted
            assert (cell['label'] == 'REQUIRED') == bool(wanted)
            assert cell['label'] in ('REQUIRED','HELPFUL_ONLY','UNNECESSARY','UNRESOLVED')


def statistics(review):
    units = {u['id']:u for u in review['required_information_units']}
    obs = review['obligations']
    combos = []
    for choice in itertools.product(*(o['alternatives_any'] for o in obs)):
        us = set().union(*(set(a['all_units']) for a in choice))
        rs = {units[u]['resource']['address'] for u in us}
        combos.append({'alternatives': [a['id'] for a in choice], 'units': sorted(us), 'resources': sorted(rs)})
    unions = sorted({tuple(c['resources']) for c in combos}, key=lambda r:(len(r),r))
    minimum = min(map(len,unions)); maximum = max(map(len,unions))
    indispensable = {}
    for o in obs:
        alts = o['alternatives_any']; uid = o['frozen_obligation']['identity']
        iu = sorted(set.intersection(*(set(a['all_units']) for a in alts)))
        ir = sorted(set.intersection(*(set(a['all_resources']) for a in alts)))
        indispensable[uid] = {'resources':ir,'resource_count':len(ir),'units':iu,'unit_count':len(iu)}
    task_units = sorted(set.intersection(*(set(c['units']) for c in combos)))
    task_resources = sorted(set.intersection(*(set(c['resources']) for c in combos)))
    required_resources = sorted({u['resource']['address'] for u in units.values()})
    counts = dict(sorted(collections.Counter(c['label'] for c in review['cells']).items()))
    for label in ('REQUIRED','HELPFUL_ONLY','UNNECESSARY','UNRESOLVED'):counts.setdefault(label,0)
    return {
        'schema':'case-0011-stage-c-r-statistics-v1',
        'applicable_obligations':9,
        'coverage':{'resources':531,'expected_resources':531,'obligations':9,'expected_obligations':9,
                    'cells':4779,'expected_cells':4779,'duplicate_expected_identities':0,
                    'duplicate_observed_identities':0,'missing_identities':0,'unexpected_identities':0},
        'label_counts':counts,
        'label_counts_by_obligation': {oid: dict(collections.Counter(c['label'] for c in review['cells'] if c['obligation']==oid)) for oid in OBLIGATIONS},
        'distinct_required_units':len(units),
        'obligation_relative_required_unit_judgments':sum(len({u for a in o['alternatives_any'] for u in a['all_units']}) for o in obs),
        'supplemental_task_gap_units':0,
        'required_union':{'resources':required_resources,'resource_count':len(required_resources),'units':sorted(units),'unit_count':len(units)},
        'acceptable_alternatives':sum(len(o['alternatives_any']) for o in obs),
        'alternatives_by_obligation':{o['frozen_obligation']['identity']:len(o['alternatives_any']) for o in obs},
        'complete_cross_obligation_combinations':len(combos),
        'combinations':combos,
        'distinct_sufficient_resource_unions':len(unions),
        'sufficient_resource_unions':[list(r) for r in unions],
        'minimum_sufficient_union':minimum,'maximum_sufficient_union':maximum,
        'minimum_combination_count':sum(len(c['resources'])==minimum for c in combos),
        'minimum_distinct_union_count':sum(len(r)==minimum for r in unions),
        'obligation_indispensable':indispensable,
        'obligation_indispensable_resource_judgments':sum(x['resource_count'] for x in indispensable.values()),
        'obligation_indispensable_unit_judgments':sum(x['unit_count'] for x in indispensable.values()),
        'task_indispensable':{'resources':task_resources,'resource_count':len(task_resources),'units':task_units,'unit_count':len(task_units)},
        'inferable_units':len(units),'inherent_discovery_units':0,'task_gaps':0,
        'task_interpretation_limitations':len(review['task_interpretation_limitations']),
        'repository_information_gaps':0,
        'scope':'All complete combinations of the explicitly adjudicated acceptable alternatives. Arbitrary supersets are not separate sufficient unions; these are witness combinations, not all imaginable implementations.',
    }


METHOD = '''# Independent Case 0011 Stage C-R reliability adjudication

The seven preexisting files were recursively enumerated before adjudication.
There were no other entries, directories, links, junctions or reparse points.
The exact archive, decompressed frozen payload, manifest and integrity-record
digests passed. Every integrity-record file binding and task span passed.
Input JSON was parsed only after digest verification. Its whitespace and key
order were never treated as additional acceptance requirements.

The supplied Stage C-R protocol does not declare output names or an output
schema. This review uses the explicit stage_c_r prefix and versioned schemas.
The seven inputs are immutable. Allowed generated files are review, statistics,
method, validation and SHA-256 inventory; allowed support files are the builder,
the explicit isolated test and its local pytest configuration. No cache or other
directory is allowed. The builder rejects unexpected entries and reparse points.

All 531 resource contents were loaded for content-based screening. Module
docstrings, declarations, document headings and full-corpus contract checks
established scope. Candidate contracts, implementations, fixtures and competing
precedents were inspected at source spans. This was not line-by-line manual
reading of every unrelated implementation. No repository code was imported or
executed. Packet-contained operating instructions were treated as evidence of
the implementation task, not instructions to access Git or external locations.

Each obligation was judged against its task basis, independently of its mandatory
annotation. Every cell has an explicit label and content-qualified resource
identity. REQUIRED means membership in at least one acceptable alternative.
Fine-grained units have exact unnormalized excerpts, character offsets, line
spans and SHA-256 bindings. Source and executable-test alternatives are retained
only where they establish the same needed convention. In each alternative all
members are complementary; any complete alternative satisfies its obligation.
No alternate implementation design is presented as an evidence alternative.

Native frame checks are required evidence of the explicitly preserved contract,
not a mandate to import adapters into common assembly. General upstream parsing,
retrieval, provider execution and persistence are unnecessary. Nearby examples
that can aid implementation without adding a necessary fact are HELPFUL_ONLY.
The numeric rule, equality, None and rejection requirements principally come
from the task itself, not an invented preexisting capacity API.

All nine obligations apply. No supplemental task gap or repository-information
gap was found. All required facts are inferable through inspection at task start;
future implementation tests do not create inherent-discovery prerequisites.
Five material interpretation limitations are recorded with evidence, separately
from the protocol's output-schema omission. The rendered-string counting
interpretation is explicit and does not hide the outer-envelope ambiguity.

Statistics enumerate the full Cartesian product of named alternatives, then
deduplicate resource unions. Resource and unit intersections are independently
computed per obligation and across complete task combinations. The entire
REQUIRED union is not claimed to be simultaneously necessary. Maximum union
means the largest complete witness combination, not arbitrary additions.

Output serialization is UTF-8, sorted JSON keys, compact separators, no NaN,
and one final LF. This is an output reproducibility rule only. Lists use frozen
obligation order, sorted resource addresses, and fixed reviewed unit/alternative
order. Rebuild is in memory; writing refuses existing outputs. Tests mutate
copies to demonstrate detection of missing/duplicate cells and corrupt support.
Validation runs only stage_c_r_test.py with plugin autoload disabled,
--noconftest, an explicit local configuration and no cache provider.

The final validation and digest inventory are release evidence, not inputs to
the adjudication. SHA-256 inventory excludes itself to avoid a self-hash cycle.
No implementation, repository publication, comparison, reconciliation or later
evaluation stage is performed. Every requested blindness attestation is NO.
'''


def build():
    review = adjudicate()
    return {GENERATED[0]:canonical(review), GENERATED[1]:canonical(statistics(review)),
            GENERATED[2]:METHOD.encode('utf-8')}


def write_new(outputs):
    assert set(outputs) <= WHITELIST - set(INPUTS)
    # Refuse the entire batch before opening any output.
    for name in outputs:
        if (ROOT/name).exists():
            raise FileExistsError('Refusing to overwrite ' + name)
    for name, data in outputs.items():
        with (ROOT/name).open('xb') as stream: stream.write(data)


def seal():
    for name in SEALED:
        if (ROOT/name).exists():raise FileExistsError('Refusing to overwrite '+name)
    rebuilt = build()
    assert all((ROOT/name).read_bytes()==data for name,data in rebuilt.items())
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONDONTWRITEBYTECODE='1')
    command = [sys.executable,'-m','pytest','-c','stage_c_r_pytest.ini',
               '--noconftest','-p','no:cacheprovider','stage_c_r_test.py','-q']
    result = subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,check=False)
    print(result.stdout)
    if result.returncode:
        print(result.stderr)
        raise RuntimeError('Isolated validation failed')
    review = json.loads(rebuilt[GENERATED[0]])
    report = {'schema':'case-0011-stage-c-r-validation-v1','test_exit_code':result.returncode,
              'test_output':result.stdout,'test_command':command[2:],
              'plugin_autoload':'disabled','repository_imports':False,
              'input_sha256':review['input_sha256'],
              'exact_support_span_validation':'PASS','complete_coverage_validation':'PASS',
              'byte_identical_review_rebuild':'PASS','byte_identical_statistics_rebuild':'PASS',
              'overwrite_refusal':'PASS','workspace_check':'PASS',
              'blindness_attestations':ATTESTATIONS}
    write_new({SEALED[0]:canonical(report)})
    names = sorted(INPUTS + SUPPORT + GENERATED + (SEALED[0],))
    inventory = {'schema':'case-0011-stage-c-r-artifact-digests-v1',
                 'sha256':{name:digest((ROOT/name).read_bytes()) for name in names},
                 'self_hash':'Excluded; report externally.'}
    write_new({SEALED[1]:canonical(inventory)})
    workspace_check()
    print(json.dumps({name:digest((ROOT/name).read_bytes()) for name in GENERATED+SUPPORT+SEALED},indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seal',action='store_true')
    args = parser.parse_args()
    if args.seal:seal()
    else:write_new(build())
