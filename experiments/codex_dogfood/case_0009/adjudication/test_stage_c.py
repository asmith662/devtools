"""Isolated structural, evidence, negative-case and deterministic replay checks."""
import ast
import copy
import json
from pathlib import Path

import pytest
import stage_c

from build_judgments import build
from stage_c import ROOT, canonical, load_packet, sha, statistics, validate, write_new


def test_exact_packet_and_complete_frame():
    manifest, resources = load_packet()
    judgment = json.loads(build()['judgments.json'])
    validate(judgment, manifest, resources)
    assert len(resources) == 531
    assert len(judgment['obligations']) == 9
    assert len(judgment['cells']) == 4779
    assert all(value == 'NO' for value in judgment['blindness_attestation'].values())
    assert judgment['task_gap']['status'] == judgment['repository_gap']['status'] == 'NONE'


def test_exact_replay_and_serialization():
    first = build()
    assert first == build()
    for name, data in first.items():
        assert (ROOT / name).read_bytes() == data
    judgments = json.loads(first['judgments.json'])
    assert canonical(judgments) == first['judgments.json']
    assert sha(first['judgments.json']) in first['judgments.sha256'].decode()
    assert json.loads(first['gold_statistics.json']) == statistics(judgments)


@pytest.mark.parametrize('change', ['missing', 'duplicate', 'foreign', 'content', 'qualification', 'label', 'excerpt', 'alternative', 'forbidden'])
def test_corrupt_gold_is_rejected(change):
    manifest, resources = load_packet()
    judgment = copy.deepcopy(json.loads(build()['judgments.json']))
    if change == 'missing':
        judgment['cells'].pop()
    elif change == 'duplicate':
        judgment['cells'][0] = judgment['cells'][1]
    elif change == 'foreign':
        judgment['cells'][0]['obligation'] = 'foreign'
    elif change == 'content':
        judgment['cells'][0]['resource']['content_identity'] = '0' * 64
    elif change == 'qualification':
        judgment['cells'][0]['frame'] = {}
    elif change == 'label':
        cell = next(c for c in judgment['cells'] if c['label'] == 'REQUIRED')
        cell['label'] = 'UNNECESSARY'
    elif change == 'excerpt':
        judgment['obligations'][0]['acceptable_alternatives'][0]['witnesses'][0]['supports'][0]['span']['excerpt'] += 'corruption'
    elif change == 'alternative':
        judgment['obligations'][0]['acceptable_alternatives'][0]['witnesses'].pop()
    else:
        judgment['score'] = 1
    with pytest.raises(ValueError):
        validate(judgment, manifest, resources)


def test_overwrite_refuses_before_any_write():
    before = (ROOT / 'judgments.json').read_bytes()
    with pytest.raises(FileExistsError):
        write_new({'judgments.json': b'invalid', 'gold_statistics.json': b'invalid'})
    assert (ROOT / 'judgments.json').read_bytes() == before


def test_bad_seal_stops_before_decompression(monkeypatch):
    monkeypatch.setattr(stage_c, 'PINNED', {**stage_c.PINNED, 'manifest.json': '0' * 64})
    def forbidden_decompression(_):
        raise AssertionError('Decompressed before file seals passed')
    monkeypatch.setattr(stage_c.gzip, 'decompress', forbidden_decompression)
    with pytest.raises(ValueError, match='Input digest mismatch'):
        load_packet()


def test_frozen_obligation_cannot_be_rewritten():
    manifest, resources = load_packet()
    judgment = json.loads(build()['judgments.json'])
    judgment['obligations'][0]['frozen_definition']['predicate'] = 'different task'
    with pytest.raises(ValueError, match='Frozen obligation altered'):
        validate(judgment, manifest, resources)


def test_helpers_are_self_contained_and_parse():
    allowed = {'argparse', 'ast', 'copy', 'gzip', 'hashlib', 'itertools', 'json',
               'collections', 'pathlib', 'pytest', 'stage_c', 'build_judgments'}
    for name in ('stage_c.py', 'build_judgments.py', 'test_stage_c.py'):
        tree = ast.parse((ROOT / name).read_text(encoding='utf-8'), filename=name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(alias.name.split('.')[0] in allowed for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                assert node.module.split('.')[0] in allowed


def test_sufficient_alternatives_and_unit_statistics():
    judgment = json.loads(build()['judgments.json'])
    result = statistics(judgment)
    assert result['cross_obligation_combination_count'] == 2
    assert result['acceptable_alternative_count'] == 10
    assert result['inherent_discovery_units'] == 0
    assert result['inferable_units'] == len(judgment['information_units'])
    assert sum(result['label_counts'].values()) == 4779
    assert result['label_counts']['UNRESOLVED'] == 0
    assert result['minimum_sufficient_unique_resource_union'] <= result['maximum_sufficient_unique_resource_union']
