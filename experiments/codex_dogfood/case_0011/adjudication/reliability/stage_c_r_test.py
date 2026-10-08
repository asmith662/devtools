"""Isolated Stage C-R tests. No packet code is imported or executed."""
import copy
import importlib.util
import itertools
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location('stage_c_r_builder',ROOT/'stage_c_r_build.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def test_exact_input_bindings_and_frame():
    manifest, resources, hashes = b.packet()
    assert len(resources)==531 and len(manifest['obligations'])==9
    assert set(hashes)==set(b.INPUTS)


def test_full_coverage_and_exact_frozen_obligations():
    review=b.adjudicate()
    manifest,resources,_=b.packet()
    b.validate_review(review,resources)
    assert [o['frozen_obligation'] for o in review['obligations']]==manifest['obligations']
    assert len(review['cells'])==4779


def test_byte_identical_review_statistics_and_method_replay():
    first=b.build(); second=b.build()
    assert first==second
    assert all((ROOT/n).read_bytes()==v for n,v in first.items())


def test_overwrite_refusal_changes_nothing():
    before={n:(ROOT/n).read_bytes() for n in b.GENERATED+b.INPUTS}
    with pytest.raises(FileExistsError):b.write_new(b.build())
    assert before=={n:(ROOT/n).read_bytes() for n in before}


@pytest.mark.parametrize('corruption',['missing','duplicate','support','label','identity','alternative'])
def test_detects_corrupt_review(corruption):
    review=copy.deepcopy(b.adjudicate()); _,resources,_=b.packet()
    if corruption=='missing':review['cells'].pop()
    elif corruption=='duplicate':review['cells'][-1]=review['cells'][0]
    elif corruption=='support':review['required_information_units'][0]['supports'][0]['excerpt']+='x'
    elif corruption=='label':
        next(c for c in review['cells'] if c['label']=='REQUIRED')['label']='HELPFUL_ONLY'
    elif corruption=='identity':review['resources'][0]['content_identity']='0'*64
    elif corruption=='alternative':review['obligations'][0]['alternatives_any'][0]['all_resources']=[]
    with pytest.raises(AssertionError):b.validate_review(review,resources)


def test_alternative_statistics_independently():
    review=b.adjudicate(); stats=b.statistics(review)
    unit_paths={u['id']:u['resource']['address'] for u in review['required_information_units']}
    choices=[o['alternatives_any'] for o in review['obligations']]
    combos=list(itertools.product(*choices)); unions=[]; unit_unions=[]
    for combo in combos:
        us={u for a in combo for u in a['all_units']}
        unit_unions.append(us);unions.append(frozenset(unit_paths[u] for u in us))
    assert stats['complete_cross_obligation_combinations']==len(combos)
    assert stats['distinct_sufficient_resource_unions']==len(set(unions))
    assert stats['minimum_sufficient_union']==min(map(len,unions))
    assert stats['maximum_sufficient_union']==max(map(len,unions))
    assert set(stats['task_indispensable']['resources'])==set.intersection(*(set(s) for s in unions))
    assert set(stats['task_indispensable']['units'])==set.intersection(*unit_unions)
    assert sum(stats['label_counts'].values())==4779


def test_required_labels_exactly_match_witness_membership():
    review=b.adjudicate()
    for unit in review['required_information_units']:
        assert unit['inferability']=='INFERABLE_AT_START'
        expected=[]
        for o in review['obligations']:
            for a in o['alternatives_any']:
                if unit['id'] in a['all_units']:
                    expected.append({'obligation':o['frozen_obligation']['identity'],'alternative':a['id']})
        assert unit['witness_memberships']==expected
    assert set(review['blindness_attestations'].values())=={'NO'}


def test_output_canonicalization_only():
    # Frozen payload bytes are never compared against a reserialization.
    for name in b.GENERATED[:2]:
        raw=(ROOT/name).read_bytes()
        assert b.canonical(json.loads(raw))==raw


def test_workspace_output_whitelist():
    assert set(b.workspace_check())<=b.WHITELIST
