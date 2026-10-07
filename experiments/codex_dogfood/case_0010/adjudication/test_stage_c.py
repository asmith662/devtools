"""Explicit local Stage C validation; no repository modules or test discovery."""
import copy
import itertools
import json
from pathlib import Path
import tempfile

import pytest

import build_judgments as builder
import stage_c as sc

ROOT = Path(__file__).absolute().parent


@pytest.fixture
def tmp_path():
    """Avoid pytest's convenience links while keeping test writes inside this workspace."""
    base = ROOT / '.stage_c_test_tmp'
    base.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='isolated-', dir=base) as directory:
        yield Path(directory)


@pytest.fixture(scope='module')
def packet():
    return sc.load_packet(ROOT)


@pytest.fixture(scope='module')
def gold(packet):
    return builder.build(*packet)[0]


def test_workspace_has_only_authorized_inputs_outputs_and_new_runtime_caches():
    sc.check_workspace(ROOT)


def test_exact_sealed_input_bindings_and_full_frame(packet):
    manifest, payload = packet
    sc.verify_packet(manifest, payload)
    assert manifest['resource_count'] == len(payload['resources']) == 531
    assert manifest['expected_cell_count'] == 5310
    assert len(manifest['obligations']) == 10


def test_complete_judgment_frame_and_source_support(packet, gold):
    sc.verify_judgments(*packet, gold)
    assert len(gold['cells']) == 5310
    assert all(u['inferability'] == 'INFERABLE_AT_START' for u in gold['information_units'])


def test_deterministic_in_memory_rebuild_and_frozen_output_bytes(packet):
    first = builder.artifacts(*packet)
    second = builder.artifacts(*packet)
    assert first == second
    for name, data in first.items():
        assert (ROOT / name).read_bytes() == data
    digest = first['judgments.sha256'].decode('ascii').split()[0]
    assert digest == sc.sha(first['judgments.json'])
    for name in ['judgments.json', 'gold_statistics.json']:
        assert sc.canonical(json.loads(first[name])) == first[name]


@pytest.mark.parametrize('failure', ['missing', 'duplicate', 'unexpected', 'invalid-label', 'content'])
def test_bad_cell_frames_fail(packet, gold, failure):
    damaged = copy.deepcopy(gold)
    if failure == 'missing':
        damaged['cells'].pop()
    elif failure == 'duplicate':
        damaged['cells'].append(copy.deepcopy(damaged['cells'][0]))
    elif failure == 'unexpected':
        damaged['cells'][0]['resource_address'] = 'not-in-the-sealed-frame'
    elif failure == 'invalid-label':
        damaged['cells'][0]['label'] = 'MAYBE'
    else:
        damaged['cells'][0]['content_identity'] = '0' * 64
    with pytest.raises(ValueError):
        sc.verify_judgments(*packet, damaged)


@pytest.mark.parametrize('field', ['excerpt', 'excerpt_sha256', 'content_identity', 'character_start', 'start_line'])
def test_corrupt_exact_support_fails(packet, gold, field):
    damaged = copy.deepcopy(gold)
    support = damaged['information_units'][0]['supports'][0]
    support[field] = support[field] + 1 if isinstance(support[field], int) else 'corrupt'
    with pytest.raises(ValueError):
        sc.verify_judgments(*packet, damaged)


def test_incomplete_alternative_cannot_manufacture_satisfaction(packet, gold):
    damaged = copy.deepcopy(gold)
    damaged['obligations'][0]['acceptable_alternatives'][0]['all_of'].pop()
    with pytest.raises(ValueError, match='Incomplete alternative'):
        sc.verify_judgments(*packet, damaged)


def test_wrong_unit_linkage_fails(packet, gold):
    damaged = copy.deepcopy(gold)
    member = damaged['obligations'][0]['acceptable_alternatives'][0]['all_of'][0]
    member['support_ids'] = [damaged['information_units'][-1]['supports'][0]['identity']]
    with pytest.raises(ValueError, match='Wrong unit support'):
        sc.verify_judgments(*packet, damaged)


@pytest.mark.parametrize('name', list(sc.INPUT_HASHES))
def test_each_modified_input_is_rejected_before_adjudication(packet, tmp_path, name):
    for original in sc.INPUT_HASHES:
        (tmp_path / original).write_bytes((ROOT / original).read_bytes())
    with (tmp_path / name).open('ab') as stream:
        stream.write(b'corruption')
    with pytest.raises(ValueError, match='Input digest failed'):
        sc.load_packet(tmp_path)


@pytest.mark.parametrize('failure', ['repository', 'snapshot', 'corpus', 'duplicate', 'missing', 'content'])
def test_packet_frame_corruption_rejected(packet, failure):
    manifest, payload = copy.deepcopy(packet)
    if failure in {'repository', 'snapshot', 'corpus'}:
        payload[failure+'_id'] = 'foreign'
    elif failure == 'duplicate':
        payload['resources'][-1] = payload['resources'][0]
    elif failure == 'missing':
        payload['resources'].pop()
    else:
        payload['resources'][0]['content'] += 'corrupt'
    with pytest.raises(ValueError):
        sc.verify_packet(manifest, payload)


def test_exact_exhaustive_sufficient_unions(packet, gold):
    stats = sc.statistics(*packet, gold)
    choices = [o['acceptable_alternatives'] for o in gold['obligations']]
    combinations = list(itertools.product(*choices))
    sizes = [len(set().union(*(set(a['resource_addresses']) for a in combination)))
             for combination in combinations]
    assert len(combinations) == stats['valid_cross_obligation_combinations']
    assert min(sizes) == stats['minimum_sufficient_unique_resource_union']
    assert max(sizes) == stats['maximum_sufficient_unique_resource_union']
    assert sizes.count(min(sizes)) == stats['number_of_minimum_combinations']
    assert sum(stats['cell_labels'].values()) == 5310
    assert all(o['applicability']['result'] == 'APPLICABLE' for o in gold['obligations'])


def test_overwrite_refused_without_partial_writes_or_input_changes(packet, tmp_path):
    outputs = builder.artifacts(*packet)
    sc.write_outputs(tmp_path, outputs)
    original = {name: (tmp_path / name).read_bytes() for name in outputs}
    with pytest.raises(ValueError, match='Overwrite refusal'):
        sc.write_outputs(tmp_path, outputs)
    assert original == {name: (tmp_path / name).read_bytes() for name in outputs}
    partial = tmp_path / 'partial'
    partial.mkdir()
    (partial / 'judgments.json').write_bytes(b'preexisting')
    with pytest.raises(ValueError, match='Overwrite refusal'):
        sc.write_outputs(partial, outputs)
    assert sorted(p.name for p in partial.iterdir()) == ['judgments.json']
    sc.load_packet(ROOT)


@pytest.mark.parametrize('field', sorted(sc.FORBIDDEN_FIELDS))
def test_forbidden_fields_rejected_recursively(field):
    with pytest.raises(ValueError, match='Forbidden field'):
        sc.reject_forbidden_fields({'safe': [{'deep': {field: 'forbidden'}}]})


def test_false_blindness_attestation_rejected(packet, gold):
    damaged = copy.deepcopy(gold)
    damaged['blindness_attestation']['Stage D performed'] = 'YES'
    with pytest.raises(ValueError, match='Blindness failed'):
        sc.verify_judgments(*packet, damaged)


def test_unexpected_workspace_entry_rejected(tmp_path):
    for name in sc.INPUT_HASHES:
        (tmp_path / name).write_bytes((ROOT / name).read_bytes())
    sc.check_workspace(tmp_path, initial=True)
    (tmp_path / 'unexpected.txt').write_bytes(b'unknown')
    with pytest.raises(ValueError, match='Unexpected workspace entry'):
        sc.check_workspace(tmp_path, initial=True)
