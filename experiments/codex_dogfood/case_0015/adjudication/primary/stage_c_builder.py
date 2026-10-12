"""Standalone deterministic Case 0015 review validator and artifact builder.

Only local sealed packet/scientific files are read. No repository package imports,
external data, environment discovery, network operations, or semantic reviewer.
Python 3.12+ standard library only. Run with -B to avoid bytecode artifacts.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import importlib.util
import itertools
import json
import stat
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).absolute().parent
INPUTS = {
    'README.md': 'd7fd2e1fc656a35b30cca813200998c77852dacad07e8eb13d082d6205fbe618',
    'manifest.json': '6a3a0dbd7eb8eaffeacafb47edf86decd50665e9cb25d0b9a32b8208c19e12ad',
    'integrity.json': '5b5dc7e6ff3c797f8f56dd7fd90e5083a33471dfd80bfdfc3201e30ac9a4febc',
    'resources.json.gz': 'a2445d3fe86bda2d5d2eb6264bbb0578cbd8772bb8db658cc79bc32001b77741',
    'validate_packet.py': '71c95c20175fee971583fc25a65e46bcfe39442b126d02ded23c7c28943f1209',
}
PAYLOAD_SHA = '5f90696d95d5514253454612a0301a4f08f48223bea2818069f4cfe856a0e859'
SEMANTIC_COMMITMENT = '5600a7c294e7d3a5b6dab07795ff7da3b027b3282af5b1b1ab9b1cfce05077e5'
OBS = tuple(f'O{i}' for i in range(1, 7))
LABELS = ('REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY')
CLASSES = ('TASK_BACKED', 'REPOSITORY_SUPPORTED', 'TASK_AND_REPOSITORY_SUPPORTED')
DERIVED = ('witnesses', 'obligation_indispensability', 'task_combinations',
           'sufficient_resource_unions', 'inclusion_minimal_resource_unions',
           'sufficient_unit_unions', 'task_indispensable_resources',
           'task_indispensable_units')
BASE = ('stage_c_review.json', 'stage_c_method.md', 'stage_c_builder.py')
GENERATED = ('stage_c_statistics.json', 'STAGE_C_REVIEW.md', 'stage_c_validation.json')
HASH_FILE = 'stage_c_hashes.json'


def canonical(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n').encode('utf-8')


def sha(value):
    return hashlib.sha256(value).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local(name):
    require('/' not in name and '\\' not in name and name not in ('', '.', '..'), 'nonlocal name')
    path = ROOT / name
    for p in (ROOT, path):
        if p.exists():
            require(not p.is_symlink() and not (getattr(p.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT), 'reparse point')
    return path


def packet():
    raw = {name: local(name).read_bytes() for name in INPUTS}
    require({name: sha(data) for name, data in raw.items()} == INPUTS, 'sealed original packet changed')
    payload_bytes = gzip.decompress(raw['resources.json.gz'])
    require(sha(payload_bytes) == PAYLOAD_SHA, 'canonical payload binding')
    p = json.loads(payload_bytes)
    require(canonical(p) == payload_bytes, 'noncanonical payload')
    # Reuse only the authenticated, local, stdlib-only payload authenticator.
    spec = importlib.util.spec_from_file_location('sealed_packet_validator', local('validate_packet.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate_payload(p)
    return p


def minimal_sets(values):
    ordered = sorted(set(map(frozenset, values)), key=lambda x: (len(x), tuple(sorted(x))))
    result = []
    for item in ordered:
        if not any(old <= item for old in result):
            result.append(item)
    return result


def intersection(values):
    items = list(values)
    return sorted(set.intersection(*(set(x) for x in items))) if items else []


def algebra(review):
    units = review['semantic_units']
    witnesses = {}
    for obligation in OBS:
        required = [u for u in units if obligation in u['obligations']]
        covers = [frozenset()]
        for unit in required:
            if unit['evidence_class'] == 'TASK_BACKED':
                continue
            covers = minimal_sets(old | frozenset(a['resources']) for old in covers for a in unit['alternatives'])
        witnesses[obligation] = []
        for index, resources in enumerate(covers, 1):
            witnesses[obligation].append({
                'id': f'{obligation}.W{index}', 'units': sorted(u['id'] for u in required),
                'resources': sorted(resources),
                'unit_support': {u['id']: [a['id'] for a in u['alternatives'] if set(a['resources']) <= resources] for u in required if u['evidence_class'] != 'TASK_BACKED'},
                'minimality_rationale': 'Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.',
            })
    indispensable = {o: {'resources': intersection(w['resources'] for w in ws), 'units': intersection(w['units'] for w in ws)} for o, ws in witnesses.items()}
    combinations = []
    for index, choice in enumerate(itertools.product(*(witnesses[o] for o in OBS)), 1):
        combinations.append({'id': f'TC{index:03d}', 'witnesses': [w['id'] for w in choice],
                             'resources': sorted(set().union(*(set(w['resources']) for w in choice))),
                             'units': sorted(set().union(*(set(w['units']) for w in choice)))})
    def distinct(key):
        return [list(x) for x in sorted({tuple(c[key]) for c in combinations}, key=lambda x: (len(x), x))]
    resource_unions = distinct('resources')
    unit_unions = distinct('units')
    return {
        'witnesses': witnesses, 'obligation_indispensability': indispensable,
        'task_combinations': combinations, 'sufficient_resource_unions': resource_unions,
        'inclusion_minimal_resource_unions': [sorted(x) for x in minimal_sets(resource_unions)],
        'sufficient_unit_unions': unit_unions,
        'task_indispensable_resources': intersection(resource_unions),
        'task_indispensable_units': intersection(unit_unions),
    }


def semantic_projection(review):
    return {key: value for key, value in review.items() if key not in DERIVED}


def validate_review(review, p, check_commitment=True):
    require(review['schema'] == 'case-0015-primary-semantic-review-v1', 'review schema')
    require((review['case'], review['task_identity'], review['task_text']) == (p['case'], p['task_identity'], p['task_text']), 'case/task binding')
    require(review['obligations'] == p['obligations'], 'six exact obligations')
    require(review['packet_binding']['input_sha256'] == INPUTS, 'input scopes')
    require(review['packet_binding']['canonical_payload_sha256'] == PAYLOAD_SHA, 'payload scope')
    expected_frame = [{k: v for k, v in r.items() if k != 'content'} for r in p['eligible_resources']]
    require(review['resource_frame'] == expected_frame, '515 exact native resources')
    resources = {r['document_identity']: r for r in p['eligible_resources']}
    require(len(resources) == 515 and len(review['obligations']) == 6, 'frame cardinality')
    for field in ('repository_id', 'snapshot_id', 'corpus_id'):
        require(review['packet_binding'][field] == p['eligible_resources'][0][field], 'native frame binding')
    require(review['labels'] == list(LABELS), 'label vocabulary')

    def task_span(s):
        require(type(s['start']) is int and type(s['end']) is int and 0 <= s['start'] < s['end'] <= len(p['task_text']), 'task span range')
        require(p['task_text'][s['start']:s['end']] == s['quote'], 'task span text')

    def source_span(s):
        require(s['resource'] in resources, 'span resource')
        r = resources[s['resource']]
        require(s['address'] == r['address'], 'span address')
        c = r['content']
        require(type(s['start']) is int and type(s['end']) is int and 0 <= s['start'] < s['end'] <= len(c), 'source span range')
        require(c[s['start']:s['end']] == s['quote'], 'source span quote')
        require(c[:s['start']].count('\n') + 1 == s['start_line'], 'start line')
        require(c[:s['end']].count('\n') + (0 if c[s['end']-1] == '\n' else 1) == s['end_line'], 'end line')

    expected_pairs = [(r['document_identity'], o) for r in p['eligible_resources'] for o in OBS]
    actual_pairs = [(c['resource'], c['obligation']) for c in review['cells']]
    require(len(actual_pairs) == 3090, 'cell count')
    require(len(set(actual_pairs)) == 3090, 'duplicate cells')
    require(actual_pairs == expected_pairs, 'cell identity/order/frame')
    for c in review['cells']:
        require(c['label'] in LABELS, 'invalid label')
        require(c['address'] == resources[c['resource']]['address'], 'cell address')
        require(c['semantic_rationale'] and c['inferability_rationale'], 'cell rationale')
        require(c['provenance']['document_identity'] == c['resource'] and c['provenance']['content_identity'] == resources[c['resource']]['content_identity'], 'cell provenance')
        ordinal = c['provenance']['packet_ordinal']
        require(p['eligible_resources'][ordinal]['document_identity'] == c['resource'], 'cell ordinal')
        require(bool(c['support_spans']) == (c['label'] != 'UNNECESSARY'), 'positive span completeness')
        for s in c['support_spans']:
            source_span(s)
            require(s['resource'] == c['resource'], 'foreign cell support')
    require(review['unresolved_cells'] == [], 'unresolved cells')
    require([x['resource'] for x in review['resource_inspection']] == [r['document_identity'] for r in p['eligible_resources']], 'inspection ledger')
    for record in review['resource_inspection']:
        source_span(record['context_span'])

    units = review['semantic_units']
    require(len({u['id'] for u in units}) == len(units), 'duplicate units')
    alternatives = set()
    for u in units:
        require(u['statement'] and u['necessity_rationale'] and u['inferability_assumptions'], 'unit semantics')
        require(u['evidence_class'] in CLASSES, 'evidence class')
        require(u['obligations'] and len(set(u['obligations'])) == len(u['obligations']) and set(u['obligations']) <= set(OBS), 'unit obligations')
        require(u['task_support'], 'task provenance')
        for s in u['task_support']:
            task_span(s)
        if u['evidence_class'] == 'TASK_BACKED':
            require(not u['alternatives'] and not u['repository_support'], 'task-backed inflation')
        else:
            require(u['alternatives'], 'repository support absent')
            sets = []
            for a in u['alternatives']:
                require(a['id'] not in alternatives, 'duplicate alternative')
                alternatives.add(a['id'])
                require(a['kind'] in ('DIRECT_SUPPORT', 'INFERABLE_SUPPORT'), 'alternative kind')
                require(a['resources'] and len(set(a['resources'])) == len(a['resources']) and set(a['resources']) <= resources.keys(), 'alternative resource')
                require(a['rationale'] and a['inferability_assumptions'], 'alternative semantics')
                for s in a['support_spans']:
                    source_span(s)
                require(set(a['resources']) == {s['resource'] for s in a['support_spans']}, 'alternative support completeness')
                sets.append(frozenset(a['resources']))
            require(len(set(sets)) == len(sets) and len(minimal_sets(sets)) == len(sets), 'redundant unit alternatives')
            for s in u['repository_support']:
                source_span(s)
            require(u['repository_support'] == [s for a in u['alternatives'] for s in a['support_spans']], 'unit support inventory')
    for clause in review['task_audit']:
        require(clause['classification'] in ('ADEQUATELY_REPRESENTED', 'NOT_ADEQUATELY_REPRESENTED'), 'task audit classification')
        task_span(clause['task_support'])
        require(set(clause['units']) <= {u['id'] for u in units}, 'audit unit')
    require({u['id'] for u in units if u['evidence_class'] == 'TASK_BACKED'} <= set().union(*(set(c['units']) for c in review['task_audit'])), 'mandatory task unit audit')

    derived = algebra(review)
    for key in DERIVED:
        require(review[key] == derived[key], 'invalid derived field: ' + key)
    for o in OBS:
        required = set().union(*(set(w['resources']) for w in derived['witnesses'][o]))
        labeled = {c['resource'] for c in review['cells'] if c['obligation'] == o and c['label'] == 'REQUIRED'}
        require(required == labeled, 'REQUIRED/witness mismatch: ' + o)
    require(set(review['gaps']) == {'TASK_INTERPRETATION_GAP', 'TASK_GAP', 'REPOSITORY_INFORMATION_GAP'}, 'gap categories')
    require(all(isinstance(v, list) for v in review['gaps'].values()), 'gap schema')
    for key in ('limitations', 'ambiguities'):
        require(len({v['id'] for v in review[key]}) == len(review[key]), key + ' identities')
        for v in review[key]:
            require(v['statement'] and type(v['blocking']) is bool, key + ' semantics')
            for s in v.get('support', []): source_span(s)
            for s in v.get('task_support', []): task_span(s)
    require(review['self_review']['separate_pass_completed'] is True, 'self-review absent')
    require(review['reviewer_count'] == 1 and review['blindness']['second_reviewer'] is False, 'single reviewer')
    require(all(v == 'NO' for v in review['blindness']['excluded_category_access'].values()), 'blindness attestation')
    if check_commitment:
        require(sha(canonical(semantic_projection(review))) == SEMANTIC_COMMITMENT, 'reviewed semantic commitment changed')
    return derived


def statistics(review):
    by_obligation = {}
    for o in OBS:
        counts = Counter(c['label'] for c in review['cells'] if c['obligation'] == o)
        by_obligation[o] = {label: counts[label] for label in LABELS}
    total = Counter(c['label'] for c in review['cells'])
    required = sorted({c['resource'] for c in review['cells'] if c['label'] == 'REQUIRED'})
    ec = Counter(u['evidence_class'] for u in review['semantic_units'])
    ru = review['sufficient_resource_unions']; uu = review['sufficient_unit_unions']
    return {
        'case': review['case'], 'resources': len(review['resource_frame']), 'obligations': len(OBS),
        'applicability': {o: 'APPLICABLE' for o in OBS},
        'expected_cells': 3090, 'actual_cells': len(review['cells']), 'duplicate_cells': 0,
        'missing_cells': 0, 'unexpected_cells': 0, 'unresolved_cells': len(review['unresolved_cells']),
        'label_counts_by_obligation': by_obligation, 'total_label_counts': {label: total[label] for label in LABELS},
        'required_resource_union': required, 'required_resource_count': len(required),
        'semantic_unit_count': len(review['semantic_units']), 'evidence_class_counts': {c: ec[c] for c in CLASSES},
        'witness_counts': {o: len(review['witnesses'][o]) for o in OBS},
        'total_witness_count': sum(len(w) for w in review['witnesses'].values()),
        'obligation_indispensability': review['obligation_indispensability'],
        'task_combination_count': len(review['task_combinations']),
        'sufficient_resource_union_count': len(ru),
        'inclusion_minimal_resource_union_count': len(review['inclusion_minimal_resource_unions']),
        'minimum_sufficient_resource_count': min(map(len, ru)), 'maximum_sufficient_resource_count': max(map(len, ru)),
        'sufficient_semantic_unit_union_count': len(uu),
        'minimum_sufficient_unit_count': min(map(len, uu)), 'maximum_sufficient_unit_count': max(map(len, uu)),
        'task_indispensable_resources': review['task_indispensable_resources'],
        'task_indispensable_units': review['task_indispensable_units'],
        'gap_counts': {k: len(v) for k, v in review['gaps'].items()},
        'limitation_count': len(review['limitations']), 'ambiguity_count': len(review['ambiguities']),
    }


def markdown(review, stats):
    resources = {r['document_identity']: r['address'] for r in review['resource_frame']}
    def paths(ids): return ', '.join('`' + resources[i] + '`' for i in ids) or '(repository-empty)'
    lines = ['# Case 0015 primary semantic adjudication', '', 'MODEL = GPT-6 Astra; REASONING = High. One adjudicator, followed by one self-review.', '',
             '## Exact original task', '', '```text', review['task_text'].rstrip(), '```', '',
             '## Task-clause audit', '', review['audit_interpretation'], '',
             '| Clause | Requirement | Obligations | Assessment | Task characters |', '|---|---|---|---|---|']
    for c in review['task_audit']:
        s = c['task_support']; lines.append(f"| {c['id']} | {c['requirement']} | {', '.join(c['obligations'])} | {c['classification']} | [{s['start']}, {s['end']}) |")
    lines += ['', '## Frozen obligations and applicability', '']
    for o in review['obligations']:
        lines += [f"- **{o['identity']['value']}: {o['title']}** — mandatory; {o['applicability']}. Satisfaction: {o['satisfaction']}"]
    lines += ['', '## Complete cell accounting', '', '515 resources × 6 obligations = 3,090 cells. No missing, duplicate, unexpected or unresolved cells.', '',
              '| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY |', '|---|---:|---:|---:|']
    for o, counts in stats['label_counts_by_obligation'].items(): lines.append('| ' + o + ' | ' + ' | '.join(str(counts[k]) for k in LABELS) + ' |')
    lines += ['| TOTAL | ' + ' | '.join(str(stats['total_label_counts'][k]) for k in LABELS) + ' |', '',
              'The JSON contains every cell, its native identity, rationale and provenance. REQUIRED means membership in at least one minimal witness; it does not mean membership in every witness.', '',
              '## Positive resources by obligation', '']
    for o in OBS:
        lines += [f'### {o}', '']
        for label in LABELS[:2]:
            lines += [f'**{label}**', '']
            for cell in review['cells']:
                if cell['obligation'] == o and cell['label'] == label:
                    coordinates = '; '.join(f"lines {s['start_line']}–{s['end_line']}, characters [{s['start']}, {s['end']})" for s in cell['support_spans'])
                    lines.append(f"- `{cell['address']}` — {coordinates}. {cell['semantic_rationale']}")
            if not any(c['obligation'] == o and c['label'] == label for c in review['cells']): lines.append('- None.')
            lines.append('')
    lines += ['## Complete REQUIRED-resource union', '', f"{stats['required_resource_count']} distinct resources:", '']
    for r in stats['required_resource_union']: lines.append(f'- `{resources[r]}` — `{r}`')
    lines += ['', '## Semantic-unit inventory and support alternatives', '',
              f"{stats['semantic_unit_count']} units: " + ', '.join(f'{k} = {v}' for k, v in stats['evidence_class_counts'].items()) + '.', '',
              'Coordinates are zero-based half-open Unicode character offsets; line numbers are one-based inclusive. Exact quoted spans and all provenance are retained in the JSON. Each alternative is conjunctive; alternatives substitute for one another.', '']
    for u in review['semantic_units']:
        lines += [f"### {u['id']} — {u['evidence_class']}", '', u['statement'], '',
                  'Obligations: ' + ', '.join(u['obligations']) + '.', '',
                  'Necessity: ' + u['necessity_rationale'], '', 'Inferability: ' + u['inferability_assumptions'], '']
        for s in u['task_support']: lines.append(f"Task support [{s['start']}, {s['end']}): {s['quote'].strip()}")
        for a in u['alternatives']:
            lines += ['', f"**{a['id']} — {a['kind']}**: {paths(a['resources'])}", '', a['rationale'], '']
            for s in a['support_spans']:
                lines += [f"- `{s['address']}` lines {s['start_line']}–{s['end_line']}, characters [{s['start']}, {s['end']})."]
        lines.append('')
    lines += ['## All minimal complete obligation witnesses', '',
              'All listed units and resources within a witness are required together; any complete witness for that obligation substitutes for another. No helpful corroboration is part of a witness.', '']
    for o in OBS:
        lines += [f'### {o} ({len(review["witnesses"][o])} witnesses)', '']
        for w in review['witnesses'][o]:
            lines += [f"- **{w['id']}**: units {', '.join(w['units'])}; resources {paths(w['resources'])}."]
        ind = review['obligation_indispensability'][o]
        lines += ['', 'Indispensable resources: ' + paths(ind['resources']) + '.', '', 'Indispensable units: ' + ', '.join(ind['units']) + '.', '']
    lines += ['## Complete task sufficiency', '',
              f"{stats['task_combination_count']} complete combinations; {stats['sufficient_resource_union_count']} distinct sufficient resource unions; {stats['inclusion_minimal_resource_union_count']} inclusion-minimal resource unions.", '',
              f"Sufficient resource-count range: {stats['minimum_sufficient_resource_count']}–{stats['maximum_sufficient_resource_count']}. Cross-obligation reuse is retained.", '',
              '| Combination | Witness choices |', '|---|---|']
    for c in review['task_combinations']: lines.append(f"| {c['id']} | {', '.join(c['witnesses'])} |")
    lines += ['', '**All distinct sufficient resource unions**', '']
    for n, union in enumerate(review['sufficient_resource_unions'], 1): lines.append(f'{n}. ({len(union)} resources) {paths(union)}')
    lines += ['', '**Inclusion-minimal resource unions**', '']
    for n, union in enumerate(review['inclusion_minimal_resource_unions'], 1): lines.append(f'{n}. ({len(union)} resources) {paths(union)}')
    lines += ['', f"Sufficient semantic-unit unions: {stats['sufficient_semantic_unit_union_count']}; size range {stats['minimum_sufficient_unit_count']}–{stats['maximum_sufficient_unit_count']}.", '']
    for union in review['sufficient_unit_unions']: lines.append('- ' + ', '.join(union))
    lines += ['', 'Task-indispensable resources: ' + paths(review['task_indispensable_resources']) + '.', '',
              'Task-indispensable units: ' + ', '.join(review['task_indispensable_units']) + '.', '', '## Gaps, limitations and ambiguities', '']
    for key, value in review['gaps'].items(): lines.append(f'- {key}: ' + ('None.' if not value else json.dumps(value)))
    lines += ['', '**Nonblocking limitations**', '']
    for v in review['limitations']: lines.append(f"- {v['id']}: {v['statement']}")
    lines += ['', '**Preserved ambiguities**', '']
    for v in review['ambiguities']: lines.append(f"- {v['id']}: {v['statement']} {v['resolution']}")
    lines += ['', 'Unresolved cell decisions: none.', '', '## Separate self-review', '', review['self_review']['granularity_review'], '']
    for change in review['self_review']['changes']: lines.append('- ' + change)
    lines += ['', '## Validation and provenance', '',
              'The standalone builder authenticates all original inputs, exact native identities, every cell/span, semantic commitments, support algebra, all minimal witnesses and task arithmetic. It derives statistics and this Markdown deterministically, exercises adversarial mutations, and verifies scientific byte hashes. Verification runs independently in a separate Python process.', '',
              'All excluded access categories are attested NO in the machine-readable review. One primary adjudicator performed the work and its separate self-review. No second reviewer was used.', '',
              'Scientific artifacts: `stage_c_review.json`, `stage_c_statistics.json`, `STAGE_C_REVIEW.md`, `stage_c_validation.json`, `stage_c_hashes.json`, `stage_c_method.md`, `stage_c_builder.py`.', '',
              'Scratch navigation/ledger state and the local handoff are excluded from scientific evidence and hashes.', '']
    return '\n'.join(lines).encode('utf-8')


def verify_hash_manifest(manifest, expected):
    require(manifest == expected, 'tampered scientific hashes')


def refuse_overwrite(paths):
    require(not any(path.exists() for path in paths), 'overwrite refused')


def adversarial(review, p):
    cases = []
    def trial(name, mutate):
        changed = copy.deepcopy(review)
        mutate(changed)
        try:
            validate_review(changed, p)
        except (ValueError, KeyError, TypeError, IndexError):
            cases.append({'name': name, 'result': 'REJECTED'})
        else:
            raise ValueError('mutation accepted: ' + name)
    trial('altered_cell_identity', lambda r: r['cells'][0].update(obligation='O9'))
    trial('missing_cell', lambda r: r['cells'].pop())
    trial('duplicate_cell', lambda r: r['cells'].__setitem__(1, copy.deepcopy(r['cells'][0])))
    trial('invalid_label', lambda r: r['cells'][0].update(label='MAYBE'))
    trial('invalid_resource', lambda r: r['cells'][0].update(resource='invalid'))
    trial('invalid_support_span', lambda r: next(c for c in r['cells'] if c['support_spans'])['support_spans'][0].update(end=99999999))
    trial('altered_unit', lambda r: r['semantic_units'][0].update(statement='Unreviewed semantic alteration'))
    trial('invalid_evidence_class', lambda r: r['semantic_units'][0].update(evidence_class='GUESSED'))
    trial('invalid_alternative', lambda r: next(u for u in r['semantic_units'] if u['alternatives'])['alternatives'][0].update(resources=['invalid']))
    trial('invalid_witness', lambda r: r['witnesses']['O1'][0]['units'].pop())
    trial('redundant_witness', lambda r: r['witnesses']['O1'].append(copy.deepcopy(r['witnesses']['O1'][0])))
    trial('invalid_task_combination', lambda r: r['task_combinations'][0]['witnesses'].__setitem__(0, 'O1.W999'))
    trial('invalid_sufficient_union', lambda r: r['sufficient_resource_unions'][0].pop())
    trial('invalid_minimal_union', lambda r: r['inclusion_minimal_resource_unions'].append(r['sufficient_resource_unions'][-1]))
    trial('invalid_sufficient_unit_union', lambda r: r['sufficient_unit_unions'][0].pop())
    trial('invalid_indispensability', lambda r: r['task_indispensable_units'].pop())
    trial('altered_gap', lambda r: r['gaps']['TASK_GAP'].append({'statement': 'Unreviewed gap'}))
    trial('altered_limitation', lambda r: r['limitations'][0].update(statement='Unreviewed limitation'))
    try:
        verify_hash_manifest({'sha256': {'stage_c_review.json': '0'*64}}, {'sha256': {'stage_c_review.json': sha(canonical(review))}})
    except ValueError:
        cases.append({'name': 'tampered_hashes', 'result': 'REJECTED'})
    else:
        raise ValueError('hash mutation accepted')
    try:
        refuse_overwrite([local('stage_c_builder.py')])
    except ValueError:
        cases.append({'name': 'overwrite_refusal', 'result': 'REJECTED'})
    else:
        raise ValueError('overwrite accepted')
    return cases


def render(review, p):
    validate_review(review, p)
    stats = statistics(review)
    trials = adversarial(review, p)
    validation = {'schema': 'case-0015-deterministic-validation-v1', 'status': 'PASS',
                  'packet_preservation': 'PASS', 'canonical_payload_sha256': PAYLOAD_SHA,
                  'semantic_commitment_sha256': SEMANTIC_COMMITMENT,
                  'completeness': {k: stats[k] for k in ('resources','obligations','expected_cells','actual_cells','duplicate_cells','missing_cells','unexpected_cells','unresolved_cells')},
                  'checks': ['exact original input bytes', 'exact task and six obligations', 'exact native 515-resource frame', 'complete ordered 3090-cell frame', 'positive identities and exact original spans', 'unique semantic units and evidence classes', 'minimal support alternatives', 'complete minimal witnesses', 'obligation intersections', 'complete task product', 'distinct sufficient resource and unit unions', 'inclusion-minimal resource unions', 'task intersections', 'reviewed gaps and limitations', 'deterministic statistics and Markdown', 'scientific hashes and overwrite refusal'],
                  'adversarial_mutations': trials,
                  'adversarial_rejected': len(trials),
                  'verification_contract': 'The --verify command regenerates each derived artifact in memory and requires exact byte equality against disk, reauthenticates original inputs and checks scientific hashes without writing.'}
    return {'stage_c_statistics.json': canonical(stats), 'STAGE_C_REVIEW.md': markdown(review, stats), 'stage_c_validation.json': canonical(validation)}


def hash_manifest(generated):
    members = {name: local(name).read_bytes() for name in BASE}
    members.update(generated)
    return {'schema': 'case-0015-scientific-hashes-v1', 'algorithm': 'SHA-256',
            'input_sha256': INPUTS, 'canonical_payload_sha256': PAYLOAD_SHA,
            'sha256': {name: sha(data) for name, data in sorted(members.items())},
            'scope': 'Six scientific artifact byte digests; this manifest is externally hashed by the completion report to avoid self-reference. Original packet scopes are separate. Scratch and local handoff are excluded.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--build', action='store_true')
    mode.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    if args.build:
        refuse_overwrite([local(name) for name in (*GENERATED, HASH_FILE)])
    p = packet()
    review_bytes = local('stage_c_review.json').read_bytes()
    review = json.loads(review_bytes)
    require(review_bytes == canonical(review), 'review canonical bytes')
    generated = render(review, p)
    manifest = hash_manifest(generated)
    if args.build:
        for name, data in generated.items():
            with local(name).open('xb') as target: target.write(data)
        with local(HASH_FILE).open('xb') as target: target.write(canonical(manifest))
    else:
        for name, data in generated.items():
            require(local(name).read_bytes() == data, 'replay byte mismatch: ' + name)
        disk_hashes = local(HASH_FILE).read_bytes()
        require(disk_hashes == canonical(json.loads(disk_hashes)), 'hash manifest canonical bytes')
        verify_hash_manifest(json.loads(disk_hashes), manifest)
    # Final original-byte authentication; never rerun the initial directory whitelist.
    require({name: sha(local(name).read_bytes()) for name in INPUTS} == INPUTS, 'final packet preservation')
    print(json.dumps({'status': 'PASS', 'mode': 'build' if args.build else 'verify',
                      'resources': 515, 'cells': len(review['cells']),
                      'semantic_units': len(review['semantic_units']),
                      'adversarial_mutations_rejected': 20,
                      'derived_bytes': 'EXACT', 'original_packet_bytes': 'UNCHANGED',
                      'hash_manifest_sha256': sha(canonical(manifest))}, indent=2))


if __name__ == '__main__':
    main()
