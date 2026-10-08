"""Self-contained local C.5-R checks; no repository or third-party plugins."""
import collections
import gzip
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path

ROOT = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location('local_c5r_v1', ROOT / 'c5r_v1.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def frozen():
    return json.loads((ROOT / review.OUTPUT).read_bytes())


def test_exact_packet_input_hashes():
    for name, digest in review.INPUT_HASHES.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest
    integrity = json.loads((ROOT/'integrity.json').read_bytes())
    manifest = json.loads((ROOT/'manifest.json').read_bytes())
    raw = (ROOT/'packet.json.gz').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == integrity['archive_sha256'] == manifest['archive_sha256']
    assert hashlib.sha256(gzip.decompress(raw)).hexdigest() == integrity['canonical_payload_sha256'] == manifest['canonical_payload_sha256']


def test_packet_manifest_bindings_and_preserved_statements():
    packet, manifest = review.packet()
    result = frozen()
    assert result['frozen_packet'] == packet
    assert result['manifest'] == manifest
    assert result['input_sha256'] == review.INPUT_HASHES
    needs = {n['identity']:n['statement'] for n in packet['information_needs']}
    units = {u['identity']:u['statement'] for u in packet['units']}
    for pair in result['pairs']:
        assert pair['need_statement'] == needs[pair['need']]
        assert pair['unit_statement'] == units[pair['unit']]
        assert pair['fact_established_by_unit'] == units[pair['unit']]


def test_complete_unique_cartesian_pairs():
    result = frozen()
    p = result['frozen_packet']
    expected = set(itertools.product([n['identity'] for n in p['information_needs']],
                                    [u['identity'] for u in p['units']]))
    actual = [(a['need'],a['unit']) for a in result['pairs']]
    assert len(actual) == len(set(actual)) == len(expected) == 576
    assert set(actual) == expected
    assert result['summary']['duplicate_pairs'] == 0
    assert result['summary']['missing_pairs'] == 0
    assert result['summary']['unexpected_pairs'] == 0


def test_labels_and_semantic_rationale_fields():
    result = frozen()
    labels = set(result['frozen_packet']['mapping_labels'])
    for pair in result['pairs']:
        assert pair['label'] in labels
        assert pair['rationale'] and pair['fact_sought'] and pair['fact_established_by_unit']
        if pair['label'] == 'PARTIALLY_COVERS':
            assert pair['covered_part'] and pair['missing_part']
            assert pair['covered_part'] != pair['missing_part']
    assert result['summary']['pair_labels'] == dict(collections.Counter(p['label'] for p in result['pairs']))


def test_complete_granularity():
    result = frozen()
    expected = {u['identity'] for u in result['frozen_packet']['units']}
    actual = result['unit_granularity']
    assert len(actual) == len({u['unit'] for u in actual}) == 32
    assert {u['unit'] for u in actual} == expected
    valid = {'ATOMIC_FOR_NEED_MAPPING','COLLECTIVELY_COVERABLE',
             'OVERCOMPOUND_FOR_PAIRWISE_MAPPING','AMBIGUOUS_GRANULARITY'}
    assert all(u['category'] in valid and u['rationale'] for u in actual)


def test_complete_need_classifications_and_semantic_review():
    result = frozen()
    needs = result['need_classifications']
    assert len(needs) == len({n['need'] for n in needs}) == 18
    assert {n['need'] for n in needs} == {n['identity'] for n in result['frozen_packet']['information_needs']}
    for need in needs:
        assert need['label'] in result['frozen_packet']['need_labels']
        assert need['rationale'] and need['semantic_formulation_review']
        pairs = [p for p in result['pairs'] if p['need'] == need['need']]
        direct = {p['unit'] for p in pairs if p['label'] == 'DIRECTLY_COVERS'}
        assert direct == set(need['direct_units'])
        unique = {u for u in direct if sum(p['unit']==u and p['label']=='DIRECTLY_COVERS' for p in result['pairs']) == 1}
        assert unique == set(need['uniquely_direct_units'])
        if need['label'] == 'NECESSARY':
            assert unique
        elif need['label'] == 'USEFUL_REDUNDANT':
            assert direct and not unique
        elif need['label'] == 'PARTIAL_ONLY':
            assert not direct and any(p['label']=='PARTIALLY_COVERS' for p in pairs)


def test_coverage_derivation():
    result = frozen()
    assert len(result['unit_coverage']) == 32
    for unit in result['unit_coverage']:
        pairs = [p for p in result['pairs'] if p['unit'] == unit['unit']]
        labels = {p['label'] for p in pairs}
        expected = ('COVERED' if 'DIRECTLY_COVERS' in labels else 'PARTIAL_ONLY' if 'PARTIALLY_COVERS' in labels
                    else 'AMBIGUOUS_ONLY' if 'AMBIGUOUS' in labels else 'UNCOVERED')
        assert unit['status'] == expected
        for field,label in [('direct_needs','DIRECTLY_COVERS'),('partial_needs','PARTIALLY_COVERS'),('ambiguous_needs','AMBIGUOUS')]:
            assert set(unit[field]) == {p['need'] for p in pairs if p['label']==label}
    assert result['summary']['frozen_direct_rule_satisfied'] == all(u['status']=='COVERED' for u in result['unit_coverage'])


def test_collective_sets_and_minimality_records():
    result = frozen()
    rows = result['collective_coverage']
    assert {r['unit'] for r in rows} == {u['unit'] for u in result['unit_granularity'] if u['category']=='COLLECTIVELY_COVERABLE'}
    ns = {n['identity'] for n in result['frozen_packet']['information_needs']}
    for row in rows:
        assert row['status']=='MINIMAL_SETS_IDENTIFIED'
        assert row['rationale'] and row['minimality'] and row['diagnostic_only']
        sets = [frozenset(s) for s in row['minimal_need_sets']]
        assert len(sets)==len(set(sets))
        assert all(len(s)==2 and s<=ns for s in sets)
        assert all(not a<b for a in sets for b in sets)
        for s in sets:
            for n in s:
                pair = next(p for p in result['pairs'] if p['need']==n and p['unit']==row['unit'])
                assert pair['label']=='PARTIALLY_COVERS' and pair['missing_part']
    # This verifies the recorded proof structure, not a machine proof of semantics.


def test_all_alternatives_preserve_all_members_and_any_substitution():
    result = frozen()
    frozen_alts = {a['identity']:(g['obligation'],a) for g in result['frozen_packet']['alternatives'] for a in g['alternatives']}
    rows = result['alternative_coverage']
    assert len(rows)==len({r['alternative'] for r in rows})==len(frozen_alts)==12
    assert {r['alternative'] for r in rows}==set(frozen_alts)
    direct = {u['unit'] for u in result['unit_coverage'] if u['status']=='COVERED'}
    collective = {u['unit'] for u in result['collective_coverage']}
    for row in rows:
        obligation, original = frozen_alts[row['alternative']]
        assert row['obligation']==obligation and row['units']==original['units']
        assert row['member_logic']==original['member_logic']=='ALL_COMPLEMENTARY'
        members=set(row['units'])
        assert set(row['directly_covered_members'])==members & direct
        assert set(row['collectively_covered_members'])==(members-direct) & collective
        assert set(row['incomplete_members'])==members-direct-collective
        expected = 'FULLY_DIRECTLY_COVERED' if members<=direct else 'FULLY_COVERED_ONLY_COLLECTIVELY' if members<=direct|collective else 'INCOMPLETE'
        assert row['status']==expected
    assert len(result['obligation_alternatives'])==9
    for group in result['obligation_alternatives']:
        assert group['alternative_logic']=='ANY_COMPLETE_ALTERNATIVE'
        own=[a for a in rows if a['obligation']==group['obligation']]
        assert set(group['fully_direct_alternatives'])=={a['alternative'] for a in own if a['status']=='FULLY_DIRECTLY_COVERED'}
        assert set(group['additional_collectively_complete_alternatives'])=={a['alternative'] for a in own if a['status']=='FULLY_COVERED_ONLY_COLLECTIVELY'}


def test_deterministic_replay():
    original=(ROOT/review.OUTPUT).read_bytes()
    assert review.encode(review.build())==original
    assert review.encode(review.build())==original


def test_overwrite_refusal():
    original=(ROOT/review.OUTPUT).read_bytes()
    try:
        review.exclusive_write(review.OUTPUT,b'never written')
    except FileExistsError:
        pass
    else:
        raise AssertionError('Output overwrite was allowed')
    assert (ROOT/review.OUTPUT).read_bytes()==original


def test_no_forbidden_fields_and_scientific_whitelist():
    assert os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD']=='1'
    assert os.environ['PYTHONDONTWRITEBYTECODE']=='1'
    review.whitelist()
    denied={'lexical_query','lexical_queries','analyzed_terms','analyzer_terms','retrieval_route','retrieval_routes',
            'treatment_results','result_resource','result_resources','gold_answer_resource_path',
            'gold_answer_resource_paths','rank','ranks','score','scores','acquisition_cost',
            'acquisition_costs','arm_identity','arm_id','stage_d_outcomes','confirmation_data',
            'source_path','answer_path','resource_path'}
    def walk(value):
        if isinstance(value,dict):
            assert not denied & set(value)
            for v in value.values(): walk(v)
        elif isinstance(value,list):
            for v in value: walk(v)
    walk(frozen())
    for name in ['c5r_v1_validation.json','c5r_v1_hashes.json']:
        if (ROOT/name).exists(): walk(json.loads((ROOT/name).read_bytes()))
    assert len(frozen()['blindness_attestation'])==16
    assert set(frozen()['blindness_attestation'].values())=={'NO'}
