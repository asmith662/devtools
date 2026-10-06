"""Self-contained blind packet validation, canonical serialization and statistics."""
import gzip
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PINNED = {
    'FRESH_STAGE_C_INSTRUCTIONS.md': '2a76e05b6f8e131f702888f72f497cf75141c0cf03e1e80fd38c050929924835',
    'RECOVERY.md': 'bc54af501a280222e4366fdbf7f2b3d6e16827cefc575349d00988d9afcbd043',
    'manifest.json': 'a68bf46bec7e7875e9321986864bbe3cb12cec80ecc167992d770610f48ae932',
    'integrity.json': 'edce2e60cea2e5dee279ad60aa9d97b9ac3fd95514167f242a8f87d78e8e9849',
    'resources.json.gz': 'c23e0908d664e9c81149dec54a81aeeff3ef25fa9624c342cfac9bda44be5b37',
    'README.md': 'f0e7b7019cc436c066d7e82dad5cf9668c4301bbbf6cce0e1394b5e12954622d',
}
PAYLOAD = '29e09439ad7812b96f7a10ccb40e34548e842a56ab9e90306fcac8a299349c99'
INPUTS = set(PINNED) | {'RECOVERY.md', 'FRESH_STAGE_C_INSTRUCTIONS.md'}
OUTPUTS = {'judgments.json', 'gold_statistics.json', 'judgments.sha256', 'METHOD.md',
           'build_judgments.py', 'stage_c.py', 'test_stage_c.py', 'stage_c_pytest.ini'}
LABELS = {'REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY', 'UNRESOLVED'}
FORBIDDEN = {'arm', 'arm_identity', 'rank', 'score', 'rank_delta', 'analyzer_term',
             'treatment_membership', 'gain_loss', 'gain_loss_classification',
             'treatment_cost', 'effectiveness_conclusions'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def load_packet():
    unexpected = {p.name for p in ROOT.iterdir()} - INPUTS - OUTPUTS
    if unexpected:
        raise ValueError(f'Unexpected workspace entries: {sorted(unexpected)}')
    for name, digest in PINNED.items():
        if sha((ROOT / name).read_bytes()) != digest:
            raise ValueError(f'Input digest mismatch: {name}')
    seal = json.loads((ROOT / 'integrity.json').read_bytes())
    if seal['sha256'] != {k: PINNED[k] for k in ('README.md', 'manifest.json', 'resources.json.gz')}:
        raise ValueError('Integrity seal mismatch')
    manifest = json.loads((ROOT / 'manifest.json').read_bytes())
    archive = (ROOT / 'resources.json.gz').read_bytes()
    if archive[4:8] != bytes(4):
        raise ValueError('Nonzero gzip mtime')
    payload = gzip.decompress(archive)
    if sha(payload) != PAYLOAD or manifest['resources_payload_sha256'] != PAYLOAD:
        raise ValueError('Payload digest mismatch')
    if manifest['resources_archive_sha256'] != PINNED['resources.json.gz']:
        raise ValueError('Archive manifest mismatch')
    resources = json.loads(payload)['resources']
    if len(resources) != manifest['resource_count'] or len(resources) != 531:
        raise ValueError('Resource count mismatch')
    if len({r['address'] for r in resources}) != len(resources):
        raise ValueError('Duplicate resource identity')
    if len(manifest['obligations']) != 9 or manifest['obligation_count'] != 9:
        raise ValueError('Obligation count mismatch')
    if len({o['identity'] for o in manifest['obligations']}) != 9:
        raise ValueError('Duplicate obligation identity')
    if manifest['expected_cell_count'] != 531 * 9:
        raise ValueError('Cell count mismatch')
    return manifest, resources


def qualification(manifest):
    return {k: manifest[k] for k in ('case_identity', 'task_identity', 'repository_id',
                                    'snapshot_id', 'corpus_id')}


def resource_identity(resource):
    return {k: resource[k] for k in ('address', 'content_identity')}


def statistics(judgments):
    counts = Counter(c['label'] for c in judgments['cells'])
    obligations = judgments['obligations']
    combinations = []
    choices = [o['acceptable_alternatives'] for o in obligations if o['applicable']]
    for selected in itertools.product(*choices):
        union = sorted({w['resource']['address'] for alt in selected for w in alt['witnesses']})
        combinations.append({'alternatives': [a['identity'] for a in selected],
                             'resources': union, 'unique_resource_count': len(union)})
    sizes = [c['unique_resource_count'] for c in combinations]
    infer = Counter(u['inferability'] for u in judgments['information_units'])
    return {
        'frame': judgments['frame'], 'resource_count': len(judgments['resources']),
        'obligation_count': len(obligations), 'qualified_cell_count': len(judgments['cells']),
        'applicable_obligations': sum(o['applicable'] for o in obligations),
        'label_counts': {label: counts[label] for label in sorted(LABELS)},
        'distinct_required_information_units': len(judgments['information_units']),
        'obligation_relative_required_unit_judgments': sum(len(o['required_units']) for o in obligations),
        'unique_required_resources': len({c['resource']['address'] for c in judgments['cells'] if c['label'] == 'REQUIRED'}),
        'acceptable_alternative_count': sum(len(o['acceptable_alternatives']) for o in obligations),
        'cross_obligation_combination_count': len(combinations),
        'cross_obligation_combinations': combinations,
        'minimum_sufficient_unique_resource_union': min(sizes),
        'maximum_sufficient_unique_resource_union': max(sizes),
        'minimum_sufficient_combination_count': sizes.count(min(sizes)),
        'inferable_units': infer['INFERABLE_AT_START'],
        'inherent_discovery_units': infer['INHERENT_DISCOVERY_REQUIRED'],
        'identity_coverage': {'duplicate': 0, 'missing': 0, 'unexpected': 0},
    }


def validate(judgments, manifest, resources):
    if judgments['frame'] != qualification(manifest):
        raise ValueError('Incorrect qualification')
    expected_resources = sorted([resource_identity(r) for r in resources], key=lambda r: r['address'])
    if judgments['resources'] != expected_resources:
        raise ValueError('Resource frame mismatch')
    expected_obligations = {o['identity'] for o in manifest['obligations']}
    observed = [o['identity'] for o in judgments['obligations']]
    if len(observed) != len(set(observed)) or set(observed) != expected_obligations:
        raise ValueError('Obligation frame mismatch')
    expected = {(o, r['address'], r['content_identity']) for o in expected_obligations for r in resources}
    actual = [(c['obligation'], c['resource']['address'], c['resource']['content_identity']) for c in judgments['cells']]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError('Cell coverage mismatch')
    if len(actual) != manifest['expected_cell_count']:
        raise ValueError('Cell count mismatch')
    by_address = {r['address']: r for r in resources}
    units = {u['identity']: u for u in judgments['information_units']}
    if len(units) != len(judgments['information_units']):
        raise ValueError('Duplicate unit')
    used_units = set()
    required_pairs = set()
    frozen = {o['identity']: o for o in manifest['obligations']}
    for obligation in judgments['obligations']:
        if obligation['frozen_definition'] != frozen[obligation['identity']]:
            raise ValueError('Frozen obligation altered')
        if not isinstance(obligation['applicable'], bool):
            raise ValueError('Applicability must be explicit')
        used_units.update(obligation['required_units'])
        if not obligation['acceptable_alternatives']:
            raise ValueError('No sufficient alternative')
        alternative_sets = set()
        for alternative in obligation['acceptable_alternatives']:
            covered = set()
            addresses = []
            for witness in alternative['witnesses']:
                resource = by_address[witness['resource']['address']]
                if witness['resource'] != resource_identity(resource):
                    raise ValueError('Wrong witness content identity')
                addresses.append(resource['address'])
                required_pairs.add((obligation['identity'], resource['address']))
                for support in witness['supports']:
                    covered.add(support['unit'])
                    if support['unit'] not in units:
                        raise ValueError('Unknown unit')
                    span = support['span']
                    lines = resource['content'].splitlines(keepends=True)
                    if not 1 <= span['start_line'] <= span['end_line'] <= len(lines):
                        raise ValueError('Invalid source line bounds')
                    excerpt = ''.join(lines[span['start_line'] - 1:span['end_line']])
                    if not excerpt or excerpt != span['excerpt']:
                        raise ValueError('Inexact source excerpt')
            if len(addresses) != len(set(addresses)):
                raise ValueError('Duplicate witness')
            signature = tuple(sorted(addresses))
            if signature in alternative_sets:
                raise ValueError('Equivalent duplicate alternative')
            alternative_sets.add(signature)
            if covered != set(obligation['required_units']):
                raise ValueError('Incomplete alternative unit coverage')
    if used_units != set(units):
        raise ValueError('Unused or absent unit')
    for cell in judgments['cells']:
        if cell['label'] not in LABELS:
            raise ValueError('Invalid label')
        required = (cell['obligation'], cell['resource']['address']) in required_pairs
        if (cell['label'] == 'REQUIRED') != required:
            raise ValueError('Required cell lacks necessary alternative witness')
        if cell['frame'] != judgments['frame']:
            raise ValueError('Unqualified cell')
    def check_keys(value):
        if isinstance(value, dict):
            if set(value) & FORBIDDEN:
                raise ValueError('Forbidden field')
            for child in value.values():
                check_keys(child)
        elif isinstance(value, list):
            for child in value:
                check_keys(child)
    check_keys(judgments)


def write_new(artifacts):
    if any((ROOT / name).exists() for name in artifacts):
        raise FileExistsError('Refusing to overwrite any frozen output')
    for name, data in artifacts.items():
        with (ROOT / name).open('xb') as stream:
            stream.write(data)
