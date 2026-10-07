"""Self-contained frozen-packet and blind Stage C artifact validation."""
from __future__ import annotations

import gzip
import hashlib
import itertools
import json
import os
from pathlib import Path
import stat

INPUTS = {
    'resources.json.gz': 'd8cf340e1b892553944a773d2d2dc309a02ddbd28aa122fa13e9906047d3cc2a',
    'manifest.json': '561adee989446481819e582a88ce6598db7f6e545d9bc5875788c0541be58036',
    'integrity.json': 'e757fd33c8354a359df7c702015721bb80c315546100b5c1a741f1b1924636ab',
    'task.txt': '37b23f717a8c35ecf390c3169aff24bd7c39f271afc9208fb7d9e780f91239d1',
    'README.md': '03d304956ac4ed24de735bf17b2f58c4498af60bb3d28ff6a1ad5e8e70504bc3',
    'FRESH_STAGE_C_INSTRUCTIONS.md': '4267532dfe5136f8adc8df4d84b264a3e12f01e613f33573b8986856d450a9ba',
}
PAYLOAD_SHA256 = 'c242ecb757375be95d5452ef178bd5cf95a6ac7113fa60f99db496af86701ed4'
FRAME = {
    'case_identity': 'case-0011',
    'task_identity': 'case-0011-context-utf8-ceiling',
    'repository_id': '5cf96d9e-d6a5-44a6-83d3-1e24f6e00009',
    'snapshot_id': '981d67d6678d538776f2e400d79156b6e92fed048ee9af57b5a3a0a6e5f4cd17',
    'corpus_id': '1e9d78ac0f6c2ca788c161649450bc70f953ea084b97b5f403344655f78721e4',
}
OBLIGATIONS = ('ownership', 'bytes', 'ceiling', 'request', 'frame', 'exports',
               'tests', 'documentation', 'validation')
OUTPUTS = ('judgments.json', 'gold_statistics.json', 'judgments.sha256',
           'METHOD.md', 'build_judgments.py', 'stage_c.py', 'test_stage_c.py',
           'stage_c_pytest.ini')
LABELS = ('REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY', 'UNRESOLVED')
ATTESTATIONS = (
    'parent_sibling_filesystem_accessed', 'repository_checkout_accessed',
    'git_history_accessed', 'information_needs_accessed', 'query_strings_accessed',
    'treatment_results_accessed', 'arm_identities_accessed', 'ranks_scores_accessed',
    'confirmation_accessed', 'stage_c_5_performed', 'stage_d_performed',
)
FORBIDDEN_KEYS = {
    'information_need', 'information_needs', 'query', 'queries', 'query_strings',
    'arm', 'arms', 'arm_identity', 'rank', 'ranks', 'score', 'scores',
    'analyzer_terms', 'treatment_result', 'treatment_results', 'candidate_overlap',
    'treatment_cost', 'acquisition_cost', 'query_count', 'effectiveness_conclusion',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def semantic_digest(*values):
    digest = hashlib.sha256()
    for value in values:
        data = value.encode('utf-8')
        digest.update(len(data).to_bytes(8, 'big'))
        digest.update(data)
    return digest.hexdigest()


def canonical(data):
    """Output serialization only; never used to validate packet payload layout."""
    return (json.dumps(data, ensure_ascii=False, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def check_workspace(initial=False):
    """Enumerate only cwd; lstat every entry before descending; no cache allowed."""
    allowed = set(INPUTS) if initial else set(INPUTS) | set(OUTPUTS)
    found = []
    root_info = Path.cwd().lstat()
    require(not stat.S_ISLNK(root_info.st_mode), 'Workspace root symlink')
    require(not (getattr(root_info, 'st_file_attributes', 0) & 0x400), 'Workspace root reparse point')
    def visit(directory, prefix=''):
        for entry in sorted(os.scandir(directory), key=lambda item: item.name):
            name = prefix + entry.name
            info = entry.stat(follow_symlinks=False)
            require(not stat.S_ISLNK(info.st_mode), 'Symlink: ' + name)
            require(not (getattr(info, 'st_file_attributes', 0) & 0x400),
                    'Reparse point: ' + name)
            found.append(name)
            if stat.S_ISDIR(info.st_mode):
                visit(entry.path, name + '/')
    visit(Path.cwd())
    require(set(found) <= allowed, 'Unexpected workspace entries: ' +
            repr(sorted(set(found) - allowed)))
    require(set(INPUTS) <= set(found), 'Missing authorized inputs')
    return sorted(found)


def load_packet():
    check_workspace()
    blobs = {name: Path(name).read_bytes() for name in INPUTS}
    for name, digest in INPUTS.items():
        require(sha256(blobs[name]) == digest, 'Input digest mismatch: ' + name)
    integrity = json.loads(blobs['integrity.json'])
    require(integrity['schema'] == 'case-0011-blind-integrity-v1', 'Integrity schema')
    require(integrity['sha256'] == {k: v for k, v in INPUTS.items()
                                  if k != 'integrity.json'}, 'Integrity bindings')
    require(integrity['archive_sha256'] == INPUTS['resources.json.gz'], 'Archive binding')
    require(integrity['manifest_sha256'] == INPUTS['manifest.json'], 'Manifest binding')
    require(integrity['canonical_payload_sha256'] == PAYLOAD_SHA256, 'Payload binding')
    raw = gzip.decompress(blobs['resources.json.gz'])
    require(sha256(raw) == PAYLOAD_SHA256, 'Raw decompressed payload digest')
    archive = json.loads(raw)
    manifest = json.loads(blobs['manifest.json'])
    require(manifest['schema'] == 'case-0011-blind-task-v1', 'Manifest schema')
    for key, value in FRAME.items():
        require(manifest[key] == value, 'Manifest identity: ' + key)
        if key in ('repository_id', 'snapshot_id', 'corpus_id'):
            require(archive[key] == value, 'Archive identity: ' + key)
    require(manifest['archive_sha256'] == INPUTS['resources.json.gz'], 'Manifest archive')
    require(manifest['canonical_payload_sha256'] == PAYLOAD_SHA256, 'Manifest payload')
    require(blobs['task.txt'] == manifest['task'].encode('utf-8'), 'Exact task text')
    require(manifest['task_sha256'] == INPUTS['task.txt'], 'Task identity binding')
    require(manifest['resource_count'] == len(archive['resources']) == 531, 'Resources')
    require(manifest['obligation_count'] == len(manifest['obligations']) == 9, 'Obligations')
    require(manifest['expected_cell_count'] == 531 * 9 == 4779, 'Cell frame')
    require(tuple(o['identity'] for o in manifest['obligations']) == OBLIGATIONS,
            'Obligation identities')
    for obligation in manifest['obligations']:
        require(obligation['applicability_condition'] is None, 'Applicability frame')
        require(obligation['requirement'] == 'mandatory', 'Authored requirement frame')
        for basis in obligation['task_basis']:
            require(manifest['task'][basis['start']:basis['end']] == basis['text'],
                    'Obligation task support')
            require(manifest['task'][:basis['start']].count('\n') + 1 == basis['line'],
                    'Obligation task support line')
    # The manifest's exact hash binds definitions, satisfaction criteria and provenance.
    # Native identity semantics are taken from the frozen observation/corpus sources.
    resources = archive['resources']
    require(len({r['address'] for r in resources}) == 531, 'Duplicate resource identity')
    for resource in resources:
        require(set(resource) == {'address', 'byte_size', 'content',
                                  'content_identity', 'encoding'}, 'Resource schema')
        data = resource['content'].encode(resource['encoding'])
        require(len(data) == resource['byte_size'], 'Resource byte-size frame')
        require(semantic_digest('decoded-utf8-text-sha256-v1', resource['content']) ==
                resource['content_identity'], 'Native content identity')
    values = [FRAME['repository_id']] + [value for r in resources
                                        for value in (r['address'], r['content_identity'])]
    require(semantic_digest('explicit-required-text-resources-sha256-v1', *values) ==
            FRAME['snapshot_id'], 'Native snapshot frame')
    require(semantic_digest('selected-observed-utf8-resource-occurrences-sha256-v1',
                            *values) == FRAME['corpus_id'], 'Native corpus frame')
    return manifest, archive


def reject_leakage(value):
    """Reject excluded data fields; exact authorized source text is not altered."""
    if isinstance(value, dict):
        require(not (set(value) & FORBIDDEN_KEYS), 'Excluded data field')
        for child in value.values():
            reject_leakage(child)
    elif isinstance(value, list):
        for child in value:
            reject_leakage(child)


def validate_judgments(judgments, manifest, archive):
    reject_leakage(judgments)
    require(judgments['frame'] == FRAME, 'Gold identity frame')
    require(judgments['frozen_obligations'] == manifest['obligations'], 'Frozen definitions')
    require(judgments['input_sha256'] == INPUTS, 'Gold input bindings')
    require(judgments['payload_sha256'] == PAYLOAD_SHA256, 'Gold payload binding')
    resources = {r['address']: r for r in archive['resources']}
    require(judgments['resource_frame'] == [{k: r[k] for k in ('address', 'content_identity', 'byte_size', 'encoding')} for r in sorted(archive['resources'], key=lambda r: r['address'])], 'Gold complete resource frame')
    expected = {(o, r) for o in OBLIGATIONS for r in resources}
    cells = judgments['cells']
    actual = [(c['obligation_id'], c['resource_address']) for c in cells]
    require(len(actual) == len(set(actual)) == 4779, 'Duplicate or missing cells')
    require(set(actual) == expected, 'Missing/unexpected cells')
    require(all(c['label'] in LABELS for c in cells), 'Label vocabulary')
    units = {u['unit_id']: u for u in judgments['required_units']}
    require(len(units) == len(judgments['required_units']), 'Duplicate unit')
    evidence = {e['evidence_id']: e for e in judgments['source_support']}
    require(len(evidence) == len(judgments['source_support']), 'Duplicate evidence')
    for e in evidence.values():
        require(e['unit_id'] in units, 'Evidence unit linkage')
        r = resources[e['resource_address']]
        require(e['resource_identity'] == {k: FRAME[k] for k in
                ('repository_id', 'snapshot_id')} | {'address': r['address']},
                'Support resource identity')
        require(e['content_identity'] == r['content_identity'], 'Support content frame')
        require(e['source_sha256'] == sha256(r['content'].encode('utf-8')), 'Source digest')
        for span in e['spans']:
            excerpt = r['content'][span['start_character']:span['end_character']]
            require(excerpt == span['excerpt'], 'Exact source excerpt')
            require(sha256(excerpt.encode('utf-8')) == span['excerpt_sha256'], 'Excerpt digest')
            require(len(r['content'][:span['start_character']].encode('utf-8')) ==
                    span['start_utf8_byte'], 'Support byte start')
            require(len(r['content'][:span['end_character']].encode('utf-8')) ==
                    span['end_utf8_byte'], 'Support byte end')
            lines = r['content'].splitlines(keepends=True)
            require(''.join(lines[span['start_line']-1:span['end_line']]) == excerpt,
                    'Support line range')
    used = set()
    require([o['obligation_id'] for o in judgments['obligation_judgments']] ==
            list(OBLIGATIONS), 'Obligation judgment coverage')
    for o in judgments['obligation_judgments']:
        required = set(o['required_unit_ids'])
        require(o['applicability'] == 'APPLICABLE', 'Applicability decision')
        require(bool(o['applicability_reason']), 'Applicability rationale')
        necessary_resources = set()
        for alternative in o['acceptable_alternatives']:
            ids = alternative['all_evidence_ids']
            require(len(ids) == len(set(ids)), 'Duplicate alternative member')
            require({evidence[i]['unit_id'] for i in ids} == required,
                    'Incomplete/extra alternative units')
            require(alternative['all_required_unit_ids'] == o['required_unit_ids'], 'Alternative unit declaration')
            for i in ids:
                require(i in units[evidence[i]['unit_id']]['acceptable_unit_witnesses'], 'Unaccepted unit witness')
            used.update(ids)
            necessary_resources.update(evidence[i]['resource_address'] for i in ids)
            require(alternative['all_resource_addresses'] ==
                    sorted({evidence[i]['resource_address'] for i in ids}),
                    'Alternative resource membership')
        required_cells = {c['resource_address'] for c in cells
                          if c['obligation_id'] == o['obligation_id'] and
                          c['label'] == 'REQUIRED'}
        require(necessary_resources == required_cells, 'Obligation resource necessity')
        for cell in (c for c in cells if c['obligation_id'] == o['obligation_id']):
            require(cell['content_identity'] == resources[cell['resource_address']]['content_identity'],
                    'Cell content binding')
            members = [evidence[i] for a in o['acceptable_alternatives']
                       for i in a['all_evidence_ids']
                       if evidence[i]['resource_address'] == cell['resource_address']]
            require(cell['required_unit_ids'] == sorted({e['unit_id'] for e in members}),
                    'Cell unit linkage')
    for gap in judgments['task_gaps']:
        for i in gap['all_evidence_ids']:
            used.add(i)
            require(evidence[i]['unit_id'] in gap['supplemental_required_unit_ids'],
                    'Gap support linkage')
    require(used == set(evidence), 'Orphan source support')
    require({evidence[i]['unit_id'] for i in used} == set(units), 'Unsupported required unit')
    require(all(u['inferability'] in ('INFERABLE_AT_START', 'INHERENT_DISCOVERY_REQUIRED')
                for u in units.values()), 'Inferability classification')
    require(judgments['blindness_attestations'] == {key: 'NO' for key in ATTESTATIONS},
            'Blindness attestation')
    return True


def compute_statistics(judgments):
    cells = judgments['cells']
    by_label = {label: sum(c['label'] == label for c in cells) for label in LABELS}
    obligations = judgments['obligation_judgments']
    choices = [o['acceptable_alternatives'] for o in obligations
               if o['applicability'] == 'APPLICABLE']
    combinations = []
    for selected in itertools.product(*choices):
        union = sorted({r for a in selected for r in a['all_resource_addresses']})
        combinations.append({'alternative_ids': [a['alternative_id'] for a in selected],
                             'unique_resource_count': len(union),
                             'resource_union': union})
    minimum = min(c['unique_resource_count'] for c in combinations)
    maximum = max(c['unique_resource_count'] for c in combinations)
    frozen_units = {u for o in obligations for u in o['required_unit_ids']}
    supplemental = {u for g in judgments['task_gaps'] for u in g['supplemental_required_unit_ids']}
    required_resources = sorted({c['resource_address'] for c in cells if c['label'] == 'REQUIRED'})
    units = judgments['required_units']
    result = {
        'schema': 'case-0011-stage-c-statistics-v1', 'frame': FRAME,
        'coverage': {'resources': 531, 'expected_resources': 531,
                     'obligations': len(obligations), 'expected_obligations': 9,
                     'cells': len(cells), 'expected_cells': 4779,
                     'duplicate': 0, 'missing': 0, 'unexpected': 0},
        'applicable_obligations': sum(o['applicability'] == 'APPLICABLE' for o in obligations),
        'cell_labels': by_label,
        'distinct_required_information_units': len(units),
        'distinct_frozen_obligation_required_units': len(frozen_units),
        'supplemental_task_gap_required_units': len(supplemental),
        'obligation_relative_required_unit_judgments': sum(len(o['required_unit_ids']) for o in obligations),
        'unique_required_resources': len(required_resources),
        'required_resource_addresses': required_resources,
        'acceptable_alternatives': sum(len(a) for a in choices),
        'alternatives_per_obligation': {o['obligation_id']: len(o['acceptable_alternatives'])
                                       for o in obligations},
        'valid_complete_cross_obligation_combinations': len(combinations),
        'distinct_sufficient_unions': len({tuple(c['resource_union']) for c in combinations}),
        'minimum_sufficient_unique_resource_union': minimum,
        'maximum_sufficient_unique_resource_union': maximum,
        'number_of_minimum_combinations': sum(c['unique_resource_count'] == minimum for c in combinations),
        'minimum_unions': sorted([list(x) for x in {tuple(c['resource_union']) for c in combinations
                                                  if c['unique_resource_count'] == minimum}]),
        'maximum_unions': sorted([list(x) for x in {tuple(c['resource_union']) for c in combinations
                                                  if c['unique_resource_count'] == maximum}]),
        'complete_combinations': combinations,
        'inferability': {kind: sum(u['inferability'] == kind for u in units) for kind in
                        ('INFERABLE_AT_START', 'INHERENT_DISCOVERY_REQUIRED')},
        'frozen_unit_inferability': {kind: sum(u['unit_id'] in frozen_units and u['inferability'] == kind
                                             for u in units) for kind in
                                    ('INFERABLE_AT_START', 'INHERENT_DISCOVERY_REQUIRED')},
        'task_gaps': len(judgments['task_gaps']),
        'repository_information_gaps': len(judgments['repository_information_gaps']),
        'task_interpretation_gaps': len(judgments['task_interpretation_gaps']),
        'union_scope': 'Frozen obligations only; supplemental task-gap resource union is reported separately.',
        'supplemental_task_gap_resources': sorted({e['resource_address'] for e in judgments['source_support']
                                                 if e['unit_id'] in supplemental}),
    }
    reject_leakage(result)
    return result


def validate_release():
    manifest, archive = load_packet()
    from build_judgments import build
    judgments = json.loads(Path('judgments.json').read_bytes())
    validate_judgments(judgments, manifest, archive)
    rebuilt = build(manifest, archive)
    require(canonical(rebuilt) == Path('judgments.json').read_bytes(), 'Judgment replay')
    statistics = compute_statistics(judgments)
    require(canonical(statistics) == Path('gold_statistics.json').read_bytes(), 'Statistics replay')
    require(Path('judgments.sha256').read_bytes() ==
            (sha256(canonical(judgments)) + '  judgments.json\n').encode('ascii'), 'Judgment checksum')
    require(set(check_workspace()) == set(INPUTS) | set(OUTPUTS), 'Release file coverage')
    return statistics


if __name__ == '__main__':
    result = validate_release()
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('complete_combinations', 'minimum_unions', 'maximum_unions',
                      'required_resource_addresses')}, sort_keys=True, indent=2))
    print('OUTPUT SHA-256')
    for name in OUTPUTS:
        print(sha256(Path(name).read_bytes()), name)
