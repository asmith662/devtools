"""Local validation only; no repository imports, fixtures or conftest files."""
import importlib.util
import json
import os
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('local_c5', ROOT / 'adjudicate_c5_v1.py')
assert spec and spec.loader
c5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c5)


def objects():
    return {name: json.loads(data) for name, data in c5.build().items()}


def test_packet_exact_declared_integrity_and_bindings():
    packet, manifest = c5.load_packet()
    assert packet['frame'] == manifest['frame']
    assert os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] == '1'


def test_cartesian_product():
    packet, _ = c5.load_packet()
    rows = objects()[c5.NAMES[0]]['mappings']
    pairs = [(r['need'], r['unit']) for r in rows]
    expected = {(n['identity'], u['identity']) for n in packet['information_needs'] for u in packet['units']}
    assert len(pairs) == len(set(pairs)) == 576
    assert set(pairs) == expected


def test_labels_and_all_rationales():
    packet, _ = c5.load_packet()
    rows = objects()[c5.NAMES[0]]['mappings']
    for row in rows:
        assert row['label'] in packet['mapping_labels']
        assert row['rationale'].strip()
        assert row['need_fact_sought'].strip() and row['unit_fact_established'].strip()
        if row['label'] == 'DIRECTLY_COVERS':
            assert row['complete_unit_bridge'].strip()
            assert row['counterfactual'].startswith('PASS:')
        if row['label'] == 'PARTIALLY_COVERS':
            assert row['covered_part'].strip() and row['missing_part'].strip()
            assert row['covered_part'] != row['missing_part']
    assert len({(r['need'], r['unit'], r['rationale']) for r in rows}) == 576


def test_unit_derivation_and_precedence():
    data = objects()
    rows = data[c5.NAMES[0]]['mappings']
    units = data[c5.NAMES[1]]['units']
    assert len(units) == len({u['unit'] for u in units}) == 32
    for unit in units:
        own = [r for r in rows if r['unit'] == unit['unit']]
        ds = [r['need'] for r in own if r['label'] == 'DIRECTLY_COVERS']
        ps = [r['need'] for r in own if r['label'] == 'PARTIALLY_COVERS']
        am = [r['need'] for r in own if r['label'] == 'AMBIGUOUS']
        expected = 'COVERED' if ds else 'PARTIAL_ONLY' if ps else 'AMBIGUOUS_ONLY' if am else 'UNCOVERED'
        assert unit['status'] == expected
        assert unit['direct_needs'] == ds and unit['direct_need_count'] == len(ds)
        assert unit['partial_needs'] == ps and unit['ambiguous_needs'] == am


def test_need_classifications_and_reviewer_judgment():
    data = objects()
    units = data[c5.NAMES[1]]['units']
    needs = data[c5.NAMES[2]]['needs']
    assert len(needs) == len({n['need'] for n in needs}) == 18
    for need in needs:
        ds = [u['unit'] for u in units if need['need'] in u['direct_needs']]
        ps = [u['unit'] for u in units if need['need'] in u['partial_needs']]
        uq = [u['unit'] for u in units if u['direct_needs'] == [need['need']]]
        expected = 'NECESSARY' if uq else 'USEFUL_REDUNDANT' if ds else 'PARTIAL_ONLY' if ps else 'UNNECESSARY'
        assert need['direct_units'] == ds and need['partial_units'] == ps and need['unique_units'] == uq
        assert need['classification'] == need['mechanical_support'] == expected
        assert need['reviewer_judgment']['misformulated'] is False
        assert need['reviewer_judgment']['ambiguous'] is False
        assert need['reviewer_judgment']['rationale'].strip()
    assert data[c5.NAMES[2]]['misformulated_reviews'] == []


def test_statistics_and_redundancy():
    packet, _ = c5.load_packet()
    data = objects(); stats = data[c5.NAMES[3]]
    rows = data[c5.NAMES[0]]['mappings']; units = data[c5.NAMES[1]]['units']
    for label in packet['mapping_labels']:
        assert stats['mapping_label_counts'][label] == sum(r['label'] == label for r in rows)
    for status in packet['unit_coverage']:
        assert stats['unit_counts'][status] == sum(u['status'] == status for u in units)
    assert stats['uniquely_covered_units'] == [u['unit'] for u in units if u['direct_need_count'] == 1]
    assert stats['redundantly_covered_units'] == [u['unit'] for u in units if u['direct_need_count'] > 1]
    assert sum(stats['mapping_label_counts'].values()) == 576
    assert sum(stats['unit_counts'].values()) == 32
    assert sum(stats['need_classification_counts'].values()) == 18


def test_obligation_counts_include_cross_pairs():
    packet, _ = c5.load_packet()
    data = objects(); stats = data[c5.NAMES[3]]
    rows = data[c5.NAMES[0]]['mappings']; units = data[c5.NAMES[1]]['units']
    for record in stats['by_obligation']:
        ob = record['obligation']
        own_units = {u['unit'] for u in units if ob in u['obligations']}
        own_needs = {n['identity'] for n in packet['information_needs'] if n['obligation'] == ob}
        assert record['unit_memberships'] == len(own_units)
        for label in packet['mapping_labels']:
            assert record['mapping_counts_by_unit_obligation'][label] == sum(r['label'] == label and r['unit'] in own_units for r in rows)
            assert record['mapping_counts_by_need_obligation'][label] == sum(r['label'] == label and r['need'] in own_needs for r in rows)
        assert sum(record['mapping_counts_by_unit_obligation'].values()) == 18 * len(own_units)
        assert sum(record['mapping_counts_by_need_obligation'].values()) == 32 * len(own_needs)
    assert sum(sum(r['mapping_counts_by_need_obligation'].values()) for r in stats['by_obligation']) == 576


def test_all_alternative_memberships_preserved():
    packet, _ = c5.load_packet(); data = objects()
    units = data[c5.NAMES[1]]['units']
    alternatives = data[c5.NAMES[3]]['by_alternative']
    expected = {a['identity']: (g['obligation'], a) for g in packet['alternatives'] for a in g['alternatives']}
    assert len(alternatives) == len(expected) == 12
    for record in alternatives:
        ob, original = expected[record['alternative']]
        assert record['obligation'] == ob
        assert record['units'] == original['units']
        assert record['member_logic'] == 'ALL_COMPLEMENTARY'
        cs = [u for u in units if u['unit'] in original['units']]
        assert record['all_members_directly_covered'] == all(u['status'] == 'COVERED' for u in cs)
        for status in packet['unit_coverage']:
            assert record['unit_counts'][status] == sum(u['status'] == status for u in cs)


def test_deterministic_replay_matches_frozen_files():
    first = c5.build(); second = c5.build()
    assert first == second
    for name, data in first.items():
        assert (ROOT / name).read_bytes() == data


def test_overwrite_refusal_without_any_modification():
    expected = c5.build()
    inputs_before = {name: (ROOT / name).read_bytes() for name in c5.INPUT_HASHES}
    outputs_before = {name: (ROOT / name).read_bytes() for name in c5.NAMES}
    with pytest.raises(FileExistsError, match='Refusing to overwrite'):
        c5.write_outputs(expected)
    assert inputs_before == {name: (ROOT / name).read_bytes() for name in c5.INPUT_HASHES}
    assert outputs_before == {name: (ROOT / name).read_bytes() for name in c5.NAMES}


def test_digest_manifest():
    data = objects(); record = data[c5.NAMES[6]]
    assert c5.NAMES[6] not in record['scientific_output_sha256']
    for name, expected in record['scientific_output_sha256'].items():
        assert c5.digest((ROOT / name).read_bytes()) == expected
    for name, expected in record['validation_support_sha256'].items():
        assert c5.digest((ROOT / name).read_bytes()) == expected
    assert '.local/codex-result.md' in record['exclusions']


def test_no_forbidden_data_fields():
    forbidden = {'query', 'queries', 'query_string', 'query_strings', 'lexical_query',
                 'analyzed_terms', 'analyzer_terms', 'retrieval_route', 'retrieval_routes',
                 'retrieval_results', 'returned_resources', 'resource_path', 'resource_paths',
                 'expected_resource', 'expected_resources', 'ranks', 'rank', 'scores', 'score',
                 'cost', 'costs', 'acquisition_cost', 'arm', 'arm_id', 'treatment_arm',
                 'treatment_results', 'stage_d', 'stage_d_outcomes', 'confirmation_results'}
    def walk(value):
        if isinstance(value, dict):
            assert not (set(value) & forbidden)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    for value in objects().values():
        walk(value)


def test_blindness_and_method_identity():
    method = objects()[c5.NAMES[4]]
    assert len(method['blindness_attestation']) == 14
    assert set(method['blindness_attestation'].values()) == {'NO'}
    assert method['input_sha256'] == c5.INPUT_HASHES
    assert method['decompressed_payload_sha256'] == c5.PAYLOAD_HASH
    assert method['unit_precedence'] == ['COVERED', 'PARTIAL_ONLY', 'AMBIGUOUS_ONLY', 'UNCOVERED']


def test_scientific_workspace_whitelist_and_no_links():
    expected = set(c5.INPUT_HASHES) | set(c5.NAMES) | {'adjudicate_c5_v1.py', 'test_c5_v1.py'}
    found = set()
    for path in ROOT.rglob('*'):
        info = path.lstat()
        assert not path.is_symlink()
        assert not (getattr(info, 'st_file_attributes', 0) & 0x400)
        assert path.is_file()
        found.add(path.relative_to(ROOT).as_posix())
    assert found == expected


def test_validation_record_requires_all_checks():
    record = objects()[c5.NAMES[5]]
    assert set(record['checks']) == {
        'sterile_preflight', 'exact_packet_input_hashes', 'decompressed_payload_hash',
        'manifest_payload_source_identity_binding', 'pair_coverage_576_of_576',
        'duplicate_pairs_zero', 'missing_pairs_zero', 'unexpected_pairs_zero',
        'all_32_units_accounted_for', 'all_18_needs_classified',
        'direct_rationale_completeness', 'partial_rationale_completeness',
        'unit_coverage_derivation', 'need_classification_consistency',
        'alternative_membership_preservation', 'deterministic_replay',
        'overwrite_refusal', 'no_forbidden_fields', 'blindness_all_no',
        'scientific_workspace_whitelist',
    }
    assert set(record['checks'].values()) == {'PASS'}
