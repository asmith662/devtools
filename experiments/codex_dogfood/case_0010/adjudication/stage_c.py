"""Isolated, standard-library-only verification of the frozen Stage C packet."""
from __future__ import annotations

import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import re

INPUT_HASHES = {
    'FRESH_STAGE_C_INSTRUCTIONS.md': 'db70636523d5c78b4f0a7a421448937d14e5e815fc36867cd969a8048d128e30',
    'README.md': '39befead5d4b3fa96e4c786c451da166071294dbf91dd3d685754cdd5fdcb381',
    'manifest.json': '32567908921086274586caba62f277d8168801ce36a28cf62f5169716b8dfc1e',
    'resources.json.gz': 'f3f2d88383f09233d6de33820732b20c3b2e62262f3b0170878313c0edcc3373',
    'integrity.json': '8cbfaa427856ee0ca1c10f46b8acf8ecc7718bcad221fd873975d1e2c5aed2b2',
}
PAYLOAD_HASH = '101a722662773a047c0f1641d7940ebdddcee247e43babde2e9573720c17c297'
FRAME = {
    'repository_id': '5cf96d9e-d6a5-44a6-83d3-1e24f6e00009',
    'snapshot_id': '3728b26c92d4a3e20e8860b226d843d8dcf35d454b1e6f0951a92f728f90f032',
    'corpus_id': '3eb6d9cb1b253e56ae6f6b7a8c898ec5417371b5f305cca2ee6efe6d571d1e70',
}
OUTPUTS = {'judgments.json', 'gold_statistics.json', 'judgments.sha256', 'METHOD.md',
           'build_judgments.py', 'stage_c.py', 'test_stage_c.py', 'stage_c_pytest.ini'}
CACHES = {'__pycache__', '.pytest_cache', '.stage_c_test_tmp'}
LABELS = {'REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY', 'UNRESOLVED'}
FORBIDDEN_FIELDS = {
    'arm', 'arms', 'k1', 'b', 'filename_weight', 'rank', 'ranks', 'score', 'scores',
    'challenger_identity', 'treatment_membership', 'parameter_outcome',
    'completion_delta', 'treatment_cost', 'effectiveness_conclusion',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def semantic_content_identity(text):
    digest = hashlib.sha256()
    for value in ('decoded-utf8-text-sha256-v1', text):
        data = value.encode('utf-8')
        digest.update(len(data).to_bytes(8, 'big'))
        digest.update(data)
    return digest.hexdigest()


def check_workspace(root, initial=False):
    """Inspect only descendants, without following links or reparse points."""
    allowed = set(INPUT_HASHES) if initial else set(INPUT_HASHES) | OUTPUTS | CACHES
    def walk(directory):
        for path in sorted(directory.iterdir(), key=lambda p: p.name):
            info = path.lstat()
            require(not path.is_symlink() and not (getattr(info, 'st_file_attributes', 0) & 0x400),
                    f'Link or reparse point: {path.name}')
            relative = path.relative_to(root)
            require(relative.parts[0] in allowed, f'Unexpected workspace entry: {relative}')
            require('.git' not in relative.parts, 'Git entry forbidden')
            if path.is_dir():
                require(relative.parts[0] in CACHES and not initial, 'Preexisting directory forbidden')
                walk(path)
    walk(root)
    require(set(INPUT_HASHES) <= {p.name for p in root.iterdir()}, 'Missing input')


def load_packet(root):
    for name, expected in INPUT_HASHES.items():
        require(sha((root / name).read_bytes()) == expected, f'Input digest failed: {name}')
    integrity = json.loads((root / 'integrity.json').read_bytes())
    require(integrity['schema'] == 'case-0010-blind-integrity-v1', 'Integrity schema')
    require(integrity['sha256'] == {k: v for k, v in INPUT_HASHES.items() if k != 'integrity.json'},
            'Integrity file bindings')
    manifest = json.loads((root / 'manifest.json').read_bytes())
    for value in (integrity, manifest):
        require(value['archive_sha256'] == INPUT_HASHES['resources.json.gz'], 'Archive binding')
        require(value['canonical_payload_sha256'] == PAYLOAD_HASH, 'Payload binding')
    require(integrity['manifest_sha256'] == INPUT_HASHES['manifest.json'], 'Manifest binding')
    raw = gzip.decompress((root / 'resources.json.gz').read_bytes())
    require(sha(raw) == PAYLOAD_HASH, 'Payload digest')
    payload = json.loads(raw)
    verify_packet(manifest, payload)
    return manifest, payload


def verify_packet(manifest, payload):
    require(manifest['case_identity'] == 'case-0010', 'Case binding')
    require(manifest['task_identity'] == 'case-0010-line-range-disclosure', 'Task binding')
    require(manifest['schema'] == 'case-0010-blind-task-v1', 'Manifest schema')
    for key, value in FRAME.items():
        require(manifest[key] == payload[key] == value, f'Frame binding: {key}')
    resources = payload['resources']
    require(len(resources) == manifest['resource_count'] == 531, 'Resource frame count')
    require(len({r['address'] for r in resources}) == 531, 'Duplicate expected resource identity')
    require(len(manifest['obligations']) == manifest['obligation_count'] == 10, 'Obligation count')
    require(len({o['identity'] for o in manifest['obligations']}) == 10, 'Duplicate obligation')
    require(manifest['expected_cell_count'] == 5310, 'Cell count')
    for resource in resources:
        require(resource['encoding'] == 'utf-8', 'Resource encoding')
        require(resource['byte_size'] == len(resource['content'].encode('utf-8')), 'Resource size')
        require(resource['content_identity'] == semantic_content_identity(resource['content']),
                f'Content identity: {resource["address"]}')


def reject_forbidden_fields(value):
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = re.sub(r'[^a-z0-9]+', '_', key.lower()).strip('_')
            require(normalized not in FORBIDDEN_FIELDS, f'Forbidden field: {key}')
            reject_forbidden_fields(child)
    elif isinstance(value, list):
        for child in value:
            reject_forbidden_fields(child)


def coverage(manifest, payload, cells):
    expected = {(o['identity'], r['address']) for o in manifest['obligations']
                for r in payload['resources']}
    observed = [(c['obligation_id'], c['resource_address']) for c in cells]
    require(len(observed) == len(set(observed)), 'Duplicate observed cell identity')
    require(set(observed) == expected, 'Missing or unexpected cells')
    require(all(c['label'] in LABELS for c in cells), 'Invalid label')
    return {'resources': 531, 'obligations': 10, 'cells': 5310,
            'duplicate_expected_resource_identities': 0,
            'duplicate_observed_resource_identities': 0,
            'duplicate_cells': 0, 'missing_resources': 0, 'unexpected_resources': 0,
            'missing_cells': 0, 'unexpected_cells': 0}


def verify_judgments(manifest, payload, gold):
    reject_forbidden_fields(gold)
    require(all(gold[k] == v for k, v in FRAME.items()), 'Gold frame binding')
    require(gold['task'] == manifest['task'], 'Task text changed')
    coverage(manifest, payload, gold['cells'])
    by_address = {r['address']: r for r in payload['resources']}
    require(gold['resource_frame'] == [
        {'address': r['address'], 'content_identity': r['content_identity']}
        for r in sorted(payload['resources'], key=lambda r: r['address'])], 'Gold resource frame')
    units = {u['identity']: u for u in gold['information_units']}
    require(len(units) == len(gold['information_units']), 'Duplicate unit')
    supports = {}
    for unit in units.values():
        require(unit['inferability'] in {'INFERABLE_AT_START', 'INHERENT_DISCOVERY_REQUIRED'},
                'Inferability value')
        require(unit['supports'], 'Unsupported unit')
        for support in unit['supports']:
            require(support['identity'] not in supports, 'Duplicate support')
            supports[support['identity']] = (unit['identity'], support)
            resource = by_address[support['resource_identity']['address']]
            require(support['resource_identity'] == {
                'repository_id': FRAME['repository_id'], 'snapshot_id': FRAME['snapshot_id'],
                'address': resource['address']}, 'Support occurrence frame')
            require(support['content_identity'] == resource['content_identity'], 'Support content identity')
            start, end = support['character_start'], support['character_end_exclusive']
            require(0 <= start < end <= len(resource['content']), 'Support bounds')
            require(resource['content'][start:end] == support['excerpt'], 'Support excerpt')
            require(sha(support['excerpt'].encode('utf-8')) == support['excerpt_sha256'], 'Support digest')
            require(sha(resource['content'].encode('utf-8')) == support['resource_utf8_sha256'],
                    'Resource support digest')
            require(support['start_line'] == resource['content'][:start].count('\n') + 1,
                    'Support line start')
            require(support['end_line'] == resource['content'][:end-1].count('\n') + 1,
                    'Support line end')
    obligations = {o['identity']: o for o in gold['obligations']}
    require(set(obligations) == {o['identity'] for o in manifest['obligations']}, 'Obligation frame')
    required = {}
    linked = collections.defaultdict(set)
    for frozen in manifest['obligations']:
        obligation = obligations[frozen['identity']]
        require(obligation['frozen_obligation'] == frozen, 'Frozen obligation changed')
        require(obligation['applicability']['result'] == 'APPLICABLE', 'Unsupported applicability')
        require(obligation['applicability']['frozen_condition'] is None, 'Invented applicability clause')
        required_units = set(obligation['required_unit_ids'])
        require(required_units <= units.keys() and required_units, 'Required unit membership')
        require(obligation['acceptable_alternatives'], 'No sufficient alternative')
        required[obligation['identity']] = set()
        for alternative in obligation['acceptable_alternatives']:
            members = alternative['all_of']
            require({m['unit_id'] for m in members} == required_units, 'Incomplete alternative')
            require(len(members) == len(required_units), 'Duplicate alternative unit')
            addresses = set()
            for member in members:
                require(member['support_ids'], 'Empty witness')
                for sid in member['support_ids']:
                    require(sid in supports and supports[sid][0] == member['unit_id'], 'Wrong unit support')
                    address = supports[sid][1]['resource_identity']['address']
                    addresses.add(address)
                    linked[(obligation['identity'], address)].add(member['unit_id'])
            require(sorted(addresses) == alternative['resource_addresses'], 'Alternative resource set')
            required[obligation['identity']].update(addresses)
    for cell in gold['cells']:
        key = cell['obligation_id'], cell['resource_address']
        needed = cell['resource_address'] in required[cell['obligation_id']]
        require((cell['label'] == 'REQUIRED') == needed, 'Label differs from witness necessity')
        require(cell['required_unit_ids'] == sorted(linked[key]), 'Cell unit linkage')
        require(bool(cell['reason']), 'Missing cell rationale')
        require(cell['content_identity'] == by_address[cell['resource_address']]['content_identity'],
                'Cell content identity')
    require(all(v == 'NO' for v in gold['blindness_attestation'].values()), 'Blindness failed')
    require(gold['task_gap']['result'] == gold['repository_information_gap']['result'] == 'NONE',
            'Gap review changed')


def statistics(manifest, payload, gold):
    verify_judgments(manifest, payload, gold)
    choices = [o['acceptable_alternatives'] for o in gold['obligations']
               if o['applicability']['result'] == 'APPLICABLE']
    unions = []
    for combination in itertools.product(*choices):
        union = sorted({a for alternative in combination for a in alternative['resource_addresses']})
        unions.append({'alternative_ids': [a['identity'] for a in combination],
                       'resource_addresses': union, 'unique_resource_count': len(union)})
    smallest = min(u['unique_resource_count'] for u in unions)
    largest = max(u['unique_resource_count'] for u in unions)
    labels = collections.Counter(c['label'] for c in gold['cells'])
    inference = collections.Counter(u['inferability'] for u in gold['information_units'])
    result = {
        'schema': 'case-0010-stage-c-statistics-v1', **FRAME,
        'coverage': coverage(manifest, payload, gold['cells']),
        'applicable_obligations': len(choices),
        'cell_labels': {label: labels[label] for label in sorted(LABELS)},
        'distinct_required_information_units': len(gold['information_units']),
        'obligation_relative_required_unit_judgments': sum(len(o['required_unit_ids']) for o in gold['obligations']),
        'unique_required_resources_across_all_alternatives': len({c['resource_address'] for c in gold['cells'] if c['label'] == 'REQUIRED'}),
        'acceptable_alternative_count': sum(len(c) for c in choices),
        'valid_cross_obligation_combinations': len(unions),
        'minimum_sufficient_unique_resource_union': smallest,
        'maximum_sufficient_unique_resource_union': largest,
        'number_of_minimum_combinations': sum(u['unique_resource_count'] == smallest for u in unions),
        'inferability': {key: inference[key] for key in ['INFERABLE_AT_START', 'INHERENT_DISCOVERY_REQUIRED']},
        'exact_computation': 'Exhaustive deterministic Cartesian product of complete alternatives; no approximation.',
        'combinations': unions,
    }
    reject_forbidden_fields(result)
    return result


def write_outputs(root, artifacts):
    require(all(name in OUTPUTS for name in artifacts), 'Unapproved output name')
    require(not any((root / name).exists() for name in artifacts), 'Overwrite refusal: output exists')
    for name in sorted(artifacts):
        with (root / name).open('xb') as stream:
            stream.write(artifacts[name])
