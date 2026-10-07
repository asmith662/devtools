"""Isolated packet/gold/replay tests; never collect or import repository code."""
import ast
import copy
import json
import os
from pathlib import Path
import sys

import pytest

from build_judgments import build, main
from stage_c import (INPUTS, OUTPUTS, canonical, check_workspace, compute_statistics,
                     load_packet, reject_leakage, sha256, validate_judgments,
                     validate_release)


@pytest.fixture(scope='module')
def packet():
    return load_packet()


@pytest.fixture(scope='module')
def gold():
    return json.loads(Path('judgments.json').read_bytes())


def test_declared_input_integrity_and_full_frame(packet):
    manifest, archive = packet
    assert len(archive['resources']) == 531
    assert len(manifest['obligations']) == 9
    assert manifest['expected_cell_count'] == 4779
    assert manifest['task'].encode('utf-8') == Path('task.txt').read_bytes()
    for name, digest in INPUTS.items():
        assert sha256(Path(name).read_bytes()) == digest


def test_only_whitelisted_regular_files_and_isolated_collection():
    assert set(check_workspace()) == set(INPUTS) | set(OUTPUTS)
    assert os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] == '1'
    assert not any(n == 'devtools' or n.startswith('devtools.') for n in sys.modules)


def test_complete_cell_and_source_support_validation(packet, gold):
    assert validate_judgments(gold, *packet)
    pairs = [(c['obligation_id'], c['resource_address']) for c in gold['cells']]
    assert len(pairs) == len(set(pairs)) == 4779
    assert len({p[1] for p in pairs}) == 531
    assert len({p[0] for p in pairs}) == 9


def test_byte_identical_judgment_rebuild_twice(packet):
    expected = Path('judgments.json').read_bytes()
    assert canonical(build(*packet)) == expected
    assert canonical(build(*packet)) == expected


def test_byte_identical_statistics_rebuild_twice(gold):
    expected = Path('gold_statistics.json').read_bytes()
    assert canonical(compute_statistics(gold)) == expected
    assert canonical(compute_statistics(gold)) == expected


def test_overwrite_refusal_preserves_all_fourteen_files():
    before = {name: Path(name).read_bytes() for name in (*INPUTS, *OUTPUTS)}
    with pytest.raises(FileExistsError, match='Refusing to overwrite'):
        main()
    assert before == {name: Path(name).read_bytes() for name in before}


def test_all_alternatives_are_complete_and_resources_necessary(gold):
    evidence = {e['evidence_id']: e for e in gold['source_support']}
    for obligation in gold['obligation_judgments']:
        assert obligation['applicability'] == 'APPLICABLE'
        necessary = set()
        for alternative in obligation['acceptable_alternatives']:
            ids = alternative['all_evidence_ids']
            assert {evidence[i]['unit_id'] for i in ids} == set(obligation['required_unit_ids'])
            necessary.update(evidence[i]['resource_address'] for i in ids)
        assert necessary == {c['resource_address'] for c in gold['cells']
                             if c['obligation_id'] == obligation['obligation_id']
                             and c['label'] == 'REQUIRED'}


def test_statistics_partition_and_enumerated_unions(gold):
    stats = compute_statistics(gold)
    assert sum(stats['cell_labels'].values()) == 4779
    assert stats['coverage']['duplicate'] == stats['coverage']['missing'] == 0
    assert stats['coverage']['unexpected'] == 0
    combinations = stats['complete_combinations']
    assert len(combinations) == stats['valid_complete_cross_obligation_combinations']
    by_id = {a['alternative_id']: set(a['all_resource_addresses'])
             for o in gold['obligation_judgments'] for a in o['acceptable_alternatives']}
    for combination in combinations:
        union = set().union(*(by_id[i] for i in combination['alternative_ids']))
        assert sorted(union) == combination['resource_union']
        assert len(union) == combination['unique_resource_count']
    sizes = [len(c['resource_union']) for c in combinations]
    assert min(sizes) == stats['minimum_sufficient_unique_resource_union']
    assert max(sizes) == stats['maximum_sufficient_unique_resource_union']
    assert sizes.count(min(sizes)) == stats['number_of_minimum_combinations']


def test_checksum_and_release_replay():
    assert validate_release()['coverage']['cells'] == 4779


@pytest.mark.parametrize('mutation', ['missing_cell', 'duplicate_cell', 'wrong_label',
                                      'wrong_excerpt', 'wrong_digest', 'incomplete_witness',
                                      'foreign_frame', 'leakage'])
def test_rejects_protocol_or_gold_contract_corruption(packet, gold, mutation):
    damaged = copy.deepcopy(gold)
    if mutation == 'missing_cell':
        damaged['cells'].pop()
    elif mutation == 'duplicate_cell':
        damaged['cells'].append(copy.deepcopy(damaged['cells'][0]))
    elif mutation == 'wrong_label':
        damaged['cells'][0]['label'] = 'UNKNOWN'
    elif mutation == 'wrong_excerpt':
        damaged['source_support'][0]['spans'][0]['excerpt'] += 'changed'
    elif mutation == 'wrong_digest':
        damaged['source_support'][0]['spans'][0]['excerpt_sha256'] = '0' * 64
    elif mutation == 'incomplete_witness':
        damaged['obligation_judgments'][0]['acceptable_alternatives'][0]['all_evidence_ids'].pop()
    elif mutation == 'foreign_frame':
        damaged['frame']['repository_id'] = 'foreign'
    else:
        damaged['query'] = 'excluded'
    with pytest.raises(ValueError):
        validate_judgments(damaged, *packet)


def test_rejects_excluded_gold_fields():
    for field in ('information_need', 'query', 'arm', 'rank', 'score', 'analyzer_terms',
                  'treatment_result', 'candidate_overlap', 'treatment_cost',
                  'effectiveness_conclusion'):
        with pytest.raises(ValueError, match='Excluded'):
            reject_leakage({field: None})


def test_no_repository_imports_or_external_adjudication_sources_in_scripts():
    allowed_roots = {'__future__', 'ast', 'copy', 'gzip', 'hashlib', 'itertools',
                     'json', 'os', 'pathlib', 'stat', 'sys', 'pytest',
                     'stage_c', 'build_judgments'}
    for filename in ('build_judgments.py', 'stage_c.py', 'test_stage_c.py'):
        tree = ast.parse(Path(filename).read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(alias.name.split('.')[0] in allowed_roots for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                assert node.module.split('.')[0] in allowed_roots


def test_gaps_and_start_time_inferability_are_separate(gold):
    stats = compute_statistics(gold)
    frozen = {u for o in gold['obligation_judgments'] for u in o['required_unit_ids']}
    for gap in gold['task_gaps']:
        assert not gap['frozen_obligations_modified']
        assert not (set(gap['supplemental_required_unit_ids']) & frozen)
    assert gold['repository_information_gaps'] == []
    assert stats['inferability']['INHERENT_DISCOVERY_REQUIRED'] == 0
    assert sum(stats['inferability'].values()) == len(gold['required_units'])
    assert set(gold['blindness_attestations'].values()) == {'NO'}
