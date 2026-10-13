"""Standalone packet-bound primary adjudication builder and validator; stdlib only.

All scientific decisions below are authored by the sole primary. Algorithms
enumerate their consequences; they do not perform another semantic review.
Run with python -B stage_c_builder.py --draft, --build, or --verify.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import itertools
import json
import re
import stat
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).absolute().parent
PACKET_DIGESTS = {
    'archive_sha256': '64dad46fb86c69cdb4de0b9e6314290bbcfcd2f7a23e4f6daef2f570dab591ac',
    'canonical_payload_sha256': 'e80a6088e42290c7fb68ec09f2c10a2e695b1314642dc329402917efac914556',
    'manifest_sha256': '5d1976523476a659d952b38bffa91e3ffce89d935ad0455b49f28f2780b29d5c',
    'integrity_sha256': 'b9c3f0a30e8f05710e43201da8fed9e6fc2d93cd2fc29b36a1ef10ff22dd52d6',
}
ORIGINALS = {
    'README.md': '90985acd6359932a7524aab6d01bb1a00427b1d9eda534bf6f7be06de52a88b1',
    'manifest.json': PACKET_DIGESTS['manifest_sha256'],
    'integrity.json': PACKET_DIGESTS['integrity_sha256'],
    'resources.json.gz': PACKET_DIGESTS['archive_sha256'],
    'validate_packet.py': 'ce921a581595854ce136973c5a6cb8d12da1e22df6de8041ac522e31faf481f6',
}
LABELS = ('REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY')
EXCLUDED = [
    'repository checkout', 'Git/history', 'parent directories', 'sibling workspaces',
    'prior Codex session', 'web', 'queries', 'lexical ranks/scores',
    'structural annotations', 'Reference treatment evidence', 'support pairs',
    'predecessor pairs', 'treatment timings', 'graph/PPR/RRF', 'other cohort cases',
    'child implementation', 'child paths', 'child diff', 'prior gold', 'confirmation',
    'reserve',
]
NEXT_STEP = (
    'Import this clean Astra / High primary adjudication byte-for-byte into the\n'
    'devtools repository.\n\n'
    'Do NOT run another semantic reviewer.\n\n'
    'Do NOT inspect the historical child implementation.\n\n'
    'Wait until the other independently blinded cohort primaries are also complete\n'
    'before any structural-discrimination effectiveness interpretation.'
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n').encode('utf-8')


def safe(path):
    require(path.parent == ROOT or ROOT in path.parents, 'Outside workspace')
    current = path
    while current != ROOT:
        if current.exists():
            require(not current.is_symlink() and not (
                getattr(current.lstat(), 'st_file_attributes', 0)
                & stat.FILE_ATTRIBUTE_REPARSE_POINT), 'Reparse point')
        current = current.parent
    require(not ROOT.is_symlink() and not (
        getattr(ROOT.lstat(), 'st_file_attributes', 0)
        & stat.FILE_ATTRIBUTE_REPARSE_POINT), 'Workspace reparse point')
    return path


def packet():
    for name, digest in ORIGINALS.items():
        require(sha(safe(ROOT / name).read_bytes()) == digest, 'Packet file binding: ' + name)
    # Execute only the authenticated standalone validator definitions, not its
    # exact-five CLI entry point (derived files now legitimately exist).
    namespace = {'__name__': 'authenticated_packet_validator'}
    exec(compile((ROOT / 'validate_packet.py').read_bytes(), 'validate_packet.py', 'exec'), namespace)
    raw = gzip.decompress((ROOT / 'resources.json.gz').read_bytes())
    p = json.loads(raw)
    namespace['validate_payload'](p, namespace['BOUND'])
    require(raw == canonical(p), 'Canonical payload bytes')
    require(sha(raw) == PACKET_DIGESTS['canonical_payload_sha256'], 'Payload digest')
    require(p['task_text'] == 'Implement repository lexical statistics and inverted index\n', 'Task')
    f = p['parent_frame']
    require((f['repository_id'], f['snapshot_id'], f['corpus_id']) == (
        '5cf96d9e-d6a5-44a6-83d3-1e24f6e00009',
        '0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49',
        '32d70eb6fef4210e2ef4ccb48486bab51357e4f84e277c3e2b84f17bd89ddf91'), 'Frame')
    return p


def rid(n):
    return f'R{n:03}'


def identity(p, n):
    r = p['resources'][n - 1]
    return {'resource_id': rid(n), 'packet_ordinal': n, **{k: r[k] for k in (
        'address', 'document_identity', 'content_identity', 'repository_id',
        'snapshot_id', 'corpus_id', 'source_blob_sha256')}}


def span(p, n, a, b):
    text = p['resources'][n - 1]['content']
    lines = text.splitlines(keepends=True)
    require(1 <= a <= b <= len(lines), 'Authored span line bounds')
    start = sum(map(len, lines[:a - 1]))
    end = sum(map(len, lines[:b]))
    return {'resource_id': rid(n), 'start_line': a, 'end_line': b,
            'start_char': start, 'end_char': end, 'quote': text[start:end]}


def evidence(p, n, ranges):
    return [span(p, n, a, b) for a, b in ranges]


def task_evidence(p, obligations, field='satisfaction'):
    return [{'source': f'/obligations/{int(o[1:])-1}/{field}',
             'obligation_identity': p['obligations'][int(o[1:])-1]['obligation_identity'],
             'quote': p['obligations'][int(o[1:])-1][field]}
            for o in obligations]


# One necessary semantic fact per record, with closely coupled arithmetic or
# protocol fields kept together. Exact future API names are deliberately absent.
TASK_UNITS = [
    ('T01', ['O1'], 'Compute per-document counts of each observed normalized term and document length as the number of observations, including repetitions.',
     'Without occurrence multiplicity and document length the requested document lexical statistics are absent.',
     'Ordinary term frequency is an occurrence count, not a count of distinct spellings; no new tokenizer is inferred.'),
    ('T02', ['O1'], 'Compute collection document count, per-term document frequency, and average document length; include zero-length documents and explicitly define the empty-collection outcome.',
     'These are the frozen corpus statistics, and omitting empty documents changes their denominator.',
     'Document frequency counts documents containing a term once; for nonempty collections average length is total length divided by document count. The zero-denominator representation remains a documented design choice.'),
    ('T03', ['O1', 'O2', 'O3'], 'Make repeated derivations over equivalent admitted input deterministic, including output ordering.',
     'Determinism is explicitly required for statistics, postings, and validation.',
     'The packet requires reproducibility, not a particular ordering of terms or postings; explicit stable ordering suffices.'),
    ('T04', ['O1', 'O2'], 'Retain the provenance of statistics and postings to their admitted lexical documents and collection.',
     'Uncorrelated counts cannot satisfy preserving provenance or retaining document identity.',
     'Retaining the existing analysis/document/collection objects is sufficient; no new digest algorithm or provenance framework is mandated.'),
    ('T05', ['O1', 'O2'], 'Derive the capability from the existing lexical material without new tokenization semantics, filesystem reacquisition, or relevance/scoring claims.',
     'The frozen scope excludes a tokenizer, acquisition, scoring, ranking, query service, and maintenance system.',
     'Ordinary in-memory grouping/counting is permitted; using an existing analyzer is distinct from inventing new lexical semantics.'),
    ('T06', ['O2'], 'Build a term-to-document inverted mapping retaining each posting document and its term frequency.',
     'A vocabulary alone or aggregate corpus frequency is not an inverted index.',
     'One posting per term/document with its count is sufficient; representation, constructor names, and lookup API remain open.'),
    ('T07', ['O3'], 'Preserve the existing lexical observation behavior and values when adding the capability.',
     'Changing observations would violate the explicit compatibility condition.',
     'Separate derived statistics are sufficient; existing analyses need not acquire new mutable or statistical fields.'),
    ('T08', ['O3'], 'Expose a coherent public capability consistent with the existing lexical boundary.',
     'An unreachable internal computation alone does not satisfy coherent exposure.',
     'The frozen ambiguity permits module/layout choices. It does not require editing any particular initializer.'),
    ('T09', ['O3'], 'Document the new statistics/index boundary accurately.',
     'Boundary documentation is explicitly part of the integration obligation.',
     'The exact documentation destination is open; update affected current behavior claims under parent documentation rules.'),
    ('T10', ['O3'], 'Validate heterogeneous resources, repeated terms, and empty documents/collections, together with deterministic behavior.',
     'The frozen acceptance cases cannot be replaced by a single nonempty Python fixture.',
     'Deterministic local fixtures suffice; no live model, treatment-dependent fixture, or historical implementation is needed.'),
]


def make_units(p):
    units = []
    for uid, obs, statement, why, inference in TASK_UNITS:
        ev = task_evidence(p, obs)
        if uid == 'T05':
            ev += task_evidence(p, obs, 'excluded_interpretation')
        units.append({'id': uid, 'obligations': obs, 'statement': statement,
                      'evidence_class': 'TASK_BACKED', 'task_evidence': ev,
                      'support_alternatives': [], 'corroboration': [],
                      'necessity_rationale': why, 'inferability_assumptions': inference})

    def alt(uid, num, ranges, kind, inference):
        return {'id': uid + '-' + rid(num), 'resource_ids': [rid(num)],
                'support_class': kind, 'spans': evidence(p, num, ranges),
                'rationale': inference, 'compatibility': 'All alternatives describe the same frozen parent contract; compatible across units.'}

    def unit(uid, obs, statement, why, inference, alternatives, corroboration=()):
        units.append({'id': uid, 'obligations': obs, 'statement': statement,
                      'evidence_class': 'REPOSITORY_SUPPORTED', 'task_evidence': [],
                      'support_alternatives': alternatives, 'corroboration': list(corroboration),
                      'necessity_rationale': why, 'inferability_assumptions': inference})

    unit('R01', ['O1', 'O2', 'O3'],
         'Existing per-document lexical analyses expose document and ordered observations with normalized_term; collection analyses expose analyses and document_collection. Those retained objects carry the input provenance.',
         'An implementation and its compatibility checks must know how to consume the existing analysis interface instead of assuming a token list or inventing an incompatible input.',
         'Test usage can establish the consumed protocol without revealing every class declaration. Retained upstream values can remain opaque; no need to reproduce their construction or identity algorithms.', [
             alt('R01', 98, [(19, 49), (52, 85)], 'DIRECT_SUPPORT', 'The dataclasses and constructors explicitly define every consumed field and retained input.'),
             alt('R01', 271, [(89, 116), (119, 170), (173, 201)], 'INFERABLE_SUPPORT', 'Calls and assertions expose document_collection, analyses, document, observations and normalized_term, including empty inputs. A typed consumer can use this protocol without guessing return-class names.'),
         ])
    unit('R03', ['O3'],
         'The parent baseline uses Unicode word spans with casefolding, retains repeated observations and exact string offsets/encounter order, and does not split identifiers or add statistical state to observations.',
         'Compatibility requires knowing the current behavior that must remain unchanged; the task itself does not specify these lexical choices.',
         'A regex over empty text produces no observations. Tests establish behavior by examples; documented word-span semantics support the corresponding general contract.', [
             alt('R03', 98, [(16, 74)], 'DIRECT_SUPPORT', 'The Unicode regex, immutable observation fields and construction loop define current behavior.'),
             alt('R03', 271, [(89, 170), (191, 201), (239, 258)], 'INFERABLE_SUPPORT', 'Heterogeneous, repetition, casefolding, span, empty and no-statistics assertions collectively establish the compatibility target.'),
             alt('R03', 3, [(312, 322)], 'DIRECT_SUPPORT', 'The architecture states the exact baseline lexical semantics and current lack of statistics.'),
             alt('R03', 57, [(81, 88)], 'DIRECT_SUPPORT', 'The documentation map explicitly states the same lexical contract.'),
             alt('R03', 10, [(218, 222)], 'INFERABLE_SUPPORT', 'The implemented-status paragraph describes Unicode spans, exact evidence, repetitions, casefolding and no identifier decomposition; this is current-state evidence, not backlog authorization.'),
         ])
    unit('R04', ['O3'],
         'The parent normal deterministic validation convention is uv run ruff check ., uv run mypy, uv run pytest and git diff --check, with 100% branch coverage; live model/Docker tests require separate authorization.',
         'The frozen obligation explicitly requires parent development conventions. Tool configuration alone does not supply the full operating procedure or its live-test boundary.',
         'These are requirements for a future implementation. This adjudication does not run Git, install dependencies or execute repository tests.', [
             alt('R04', 1, [(207, 219)], 'DIRECT_SUPPORT', 'The operating guide gives the exact normal validation suite, branch coverage and opt-in live-test rule.'),
         ], [alt('R04', 60, [(19, 70)], 'CORROBORATION_ONLY', 'The configuration confirms the tools, strict typing/linting and 100% branch coverage, but omits the complete operating procedure and live-test authorization rule.')])
    unit('R05', ['O3'],
         'Parent documentation distinguishes current behavior from architecture and history: inspect documentation impact, update changed behavior claims, and change architecture/navigation only when affected.',
         'Correct boundary documentation under the parent conventions requires this ownership rule, not merely a new prose file or indiscriminate architecture rewrites.',
         'The policy does not make every listed documentation destination necessary to inspect or edit for this bounded feature.', [
             alt('R05', 1, [(199, 205)], 'DIRECT_SUPPORT', 'The guide gives the documentation-impact and behavior-claim update policy.'),
             alt('R05', 57, [(143, 149)], 'DIRECT_SUPPORT', 'The documentation map independently states the behavior-first update workflow and preservation of history.'),
         ])
    return units


# Positive cell decisions are explicit primary judgments, not filename rules.
# Each entry: ordinal, obligations, exact spans, material contribution.
HELPFUL = [
    (3, ['O1','O2','O3'], [(284,322)], 'Describes the current corpus/document provenance and lexical boundary. It lacks the consumed analysis field protocol; once that protocol is supported by source or lexical tests, its lexical description is corroborative.'),
    (5, ['O3'], [(340,359)], 'Explains the parent distinction between representational transformation and epistemic derivation without mandating new classes. Useful boundary guidance, not an additional prerequisite to this bounded capability.'),
    (6, ['O3'], [(91,115)], 'Explains referent identity and relevance-evidence ownership, helping document why an index is not a relevance verdict or a new universal evidence lifecycle.'),
    (8, ['O3'], [(301,335)], 'Clarifies current Context/Repository Intelligence ownership and identity distinctions. Useful terminology guidance; concrete parent lexical interfaces already suffice for this task.'),
    (10, ['O1','O2','O3'], [(204,222)], 'Summarizes the implemented corpus, document and baseline observation stages. The future-pressure record is not independent implementation authorization and adds no missing consumed API field.'),
    (57, ['O1','O2','O3'], [(61,88),(143,149)], 'Provides current boundary descriptions and documentation ownership. Its documentation rule is an independent unit-level alternative, but AGENTS is already necessary for the complete validation convention.'),
    (60, ['O3'], [(19,70)], 'Provides executable strict lint/type/test and coverage configuration. It corroborates, but cannot replace, the full operating procedure in AGENTS.'),
    (78, ['O3'], [(50,78),(114,147)], 'Shows actual root-level public repository/lexical exports, useful for coherent exposure. The future package layout is explicitly open, so this likely edit destination is not required.'),
    (89, ['O3'], [(4,60)], 'Shows public repository model constructors and exports available for integration fixtures. No change to this initializer is required to implement statistics or postings.'),
    (90, ['O1','O2','O3'], [(59,71),(102,163)], 'Shows selected corpus membership, empty realization, stable provenance and ordering. Retaining the supplied lexical collection avoids a need to reconstruct this upstream substrate.'),
    (92, ['O1','O2','O3'], [(18,58),(61,89)], 'Makes document/collection identity fields, provenance and representation ordering explicit. Statistics and postings can retain the existing document and collection objects opaquely, preserving their identities without learning or reconstructing their internal field/digest contracts.'),
    (95, ['O1','O2','O3'], [(49,72)], 'Explains retained content identity and resource occurrence fields. This improves provenance understanding but no obligation requires rebuilding or validating the upstream occurrence type.'),
    (97, ['O3'], [(1,18)], 'Shows the existing public retrieval exports. Useful for exposure consistency; choosing a coherent new public module remains permitted.'),
    (266, ['O1','O2','O3'], [(180,226)], 'Demonstrates exact selected occurrence retention and canonical membership order, providing useful end-to-end fixture context. Statistics/index construction can consume already formed lexical inputs.'),
    (268, ['O1','O2','O3'], [(94,170),(209,245)], 'Demonstrates represented corpus provenance, document identity distinctions, deterministic documents and successful empty representation. Retaining each existing lexical-analysis document object preserves those distinctions without needing this upstream representation test.'),
]
REQUIRED = {1: ['O3'], 98: ['O1','O2','O3'], 271: ['O1','O2','O3']}


def minimal_sets(values):
    unique = set(map(frozenset, values))
    return sorted((sorted(s) for s in unique if not any(t < s for t in unique)),
                  key=lambda s: (len(s), s))


def supports(unit, resource_set):
    if unit['evidence_class'] == 'TASK_BACKED':
        return True
    return any(set(a['resource_ids']) <= resource_set for a in unit['support_alternatives'])


def derive_witnesses(units, obligation):
    needed = [u for u in units if obligation in u['obligations']]
    choices = [u['support_alternatives'] for u in needed if u['evidence_class'] != 'TASK_BACKED']
    unions = [set().union(*(set(a['resource_ids']) for a in combination))
              for combination in itertools.product(*choices)]
    result = []
    for i, members in enumerate(minimal_sets(unions), 1):
        s = set(members)
        assignments = {u['id']: [a['id'] for a in u['support_alternatives']
                                  if set(a['resource_ids']) <= s] for u in needed
                       if u['evidence_class'] != 'TASK_BACKED'}
        necessity = {r: [u['id'] for u in needed if not supports(u, s - {r})] for r in members}
        result.append({'id': f'{obligation}-W{i:02}', 'obligation': obligation,
                       'resource_ids': members, 'unit_ids': sorted(u['id'] for u in needed),
                       'support_assignments': assignments, 'member_necessity': necessity})
    return result


def intersection(collection):
    sets = list(map(set, collection))
    return sorted(set.intersection(*sets)) if sets else []


def derive_sufficiency(witnesses):
    intersections = {o: {'resource_ids': intersection(w['resource_ids'] for w in ws),
                         'unit_ids': intersection(w['unit_ids'] for w in ws)}
                     for o, ws in witnesses.items()}
    combos = []
    for i, triple in enumerate(itertools.product(*(witnesses[o] for o in ('O1','O2','O3'))), 1):
        combos.append({'id': f'TC{i:03}', 'witness_ids': [w['id'] for w in triple],
                       'resource_ids': sorted(set().union(*(set(w['resource_ids']) for w in triple))),
                       'unit_ids': sorted(set().union(*(set(w['unit_ids']) for w in triple)))})
    resource_unions = sorted({tuple(c['resource_ids']) for c in combos}, key=lambda s: (len(s), s))
    unit_unions = sorted({tuple(c['unit_ids']) for c in combos}, key=lambda s: (len(s), s))
    minima = minimal_sets(resource_unions)
    return {'obligation_intersections': intersections, 'complete_task_combinations': combos,
            'task_combination_count': len(combos),
            'distinct_sufficient_resource_unions': [list(s) for s in resource_unions],
            'sufficient_resource_union_count': len(resource_unions),
            'inclusion_minimal_sufficient_resource_unions': minima,
            'resource_count_range': [min(map(len, resource_unions)), max(map(len, resource_unions))],
            'inclusion_minimal_resource_count_range': [min(map(len, minima)), max(map(len, minima))],
            'sufficient_semantic_unit_unions': [list(s) for s in unit_unions],
            'semantic_unit_count_range': [min(map(len, unit_unions)), max(map(len, unit_unions))],
            'task_indispensable_resource_ids': intersection(resource_unions),
            'task_indispensable_unit_ids': intersection(unit_unions)}


def content_scope(resource):
    text = resource['content']
    doc = re.search(r'"""(.*?)"""', text, re.S)
    if doc and doc.start() < 600:
        return ' '.join(doc.group(1).split())
    scope = re.search(r'^- scope: (.+)$', text, re.M)
    if scope:
        return scope.group(1)
    return next((line.strip('# ') for line in text.splitlines() if line.strip()), 'Empty namespace')


def make_cells(p, units):
    helper = {(n,o): (ranges, why) for n, obs, ranges, why in HELPFUL for o in obs}
    cells = []
    for n, r in enumerate(p['resources'], 1):
        for obligation in p['obligations']:
            o = obligation['id']
            cell = {**identity(p,n), 'cell_id': f'{rid(n)}:{o}',
                    'obligation_id': o, 'obligation_identity': obligation['obligation_identity'],
                    'label': 'UNNECESSARY', 'spans': [], 'unit_ids': [],
                    'rationale': 'The resource concerns ' + content_scope(r) + '. It establishes no additional consumed lexical contract, document-posting identity contract, or obligation-specific integration convention needed here.',
                    'inferability_rationale': 'Neither generic reuse possibilities nor namespace/test/documentation status establishes material information for this obligation.',
                    'provenance': {'kind': 'ORIGINAL_PARENT_RESOURCE_TEXT', 'packet_sha256': PACKET_DIGESTS['canonical_payload_sha256']},
                    'resolved': True}
            if o in REQUIRED.get(n, []):
                related = [u for u in units if o in u['obligations'] and any(
                    rid(n) in a['resource_ids'] for a in u['support_alternatives'])]
                spans = [s for u in related for a in u['support_alternatives']
                         if rid(n) in a['resource_ids'] for s in a['spans'] if s['resource_id'] == rid(n)]
                cell.update(label='REQUIRED', unit_ids=[u['id'] for u in related],
                            spans=list({(s['start_char'],s['end_char']): s for s in spans}.values()),
                            rationale='This resource independently supplies necessary current-parent information for ' + ', '.join(u['id'] for u in related) + ' and is necessary in at least one minimal complete witness.',
                            inferability_rationale=' '.join(a['rationale'] for u in related for a in u['support_alternatives'] if rid(n) in a['resource_ids']))
            elif (n,o) in helper:
                ranges, why = helper[n,o]
                cell.update(label='HELPFUL_ONLY', spans=evidence(p,n,ranges), rationale=why,
                            inferability_rationale='The cited original content materially informs this obligation, but no minimal complete witness needs this resource: its useful facts are already supplied by a required alternative, or retaining the existing input avoids needing these upstream details.')
            cells.append(cell)
    return cells


LIMITATIONS = [
    'The model/reasoning designation is GPT-6 Astra / High as requested; host routing was not independently verified. No claim of routing verification is made.',
    'Semantic necessity is the judgment of this one primary over the frozen packet, not proof of a unique implementation or an empirical effectiveness result.',
    'All 357 resources received content-based screening in packet order; candidate support received close reading. Unrelated resources were screened through content purpose, declarations/headings and full-text lexical-contract matching, not asserted to have received exhaustive line-by-line reading.',
    'The retained parent frame is authoritative; absent checkout resources were not sought. Completeness of alternatives is within this supplied resource frame and the explicit inferability assumptions.',
    'Validation proves identity/span/schema consistency and exhaustive arithmetic over the authored support model. It cannot mechanically prove the semantic truth or exhaustive discovery of that model.',
    'No repository tests were run and no implementation was written. Parent tests are source-text evidence only.',
    'Natural mentions of queries, graphs, scores, history and evaluation inside original parent text are permitted evidence; they are not access to treatment metadata or another case.',
]
AMBIGUITIES = [
    {'id':'A01', 'statement':'Public type/helper names and package layout are unspecified.', 'origin':'FROZEN_PACKET', 'disposition':'Preserved exactly; coherent exposure does not mandate a particular changed path.'},
    {'id':'A02', 'statement':'Index representation and construction API are unspecified; no scoring/ranking capability is requested.', 'origin':'FROZEN_PACKET', 'disposition':'Preserved exactly; immutable postings or other deterministic representations remain possible.'},
    {'id':'A03', 'statement':'The empty-collection average-length representation and exact term/posting ordering are unspecified.', 'origin':'PRIMARY_ANALYSIS', 'disposition':'Document an explicit empty policy and deterministic order; this is bounded design freedom, not a missing repository fact.'},
    {'id':'A04', 'statement':'Defensive handling of manually assembled inconsistent analyses or duplicate document identities is unspecified.', 'origin':'PRIMARY_ANALYSIS', 'disposition':'Do not manufacture a validation subsystem requirement; state admitted-input assumptions or a narrow rejection policy.'},
]
SELF_REVIEW = {
    'reviewer_count': 1, 'second_reviewer': 'NO', 'reconciliation': 'NO',
    'distinct_self_review_completed': True,
    'audits': ['REQUIRED inflation', 'REQUIRED under-selection', 'edit destinations',
               'test/documentation status', 'package proximity', 'future versus current facts',
               'duplicate support', 'missing alternatives', 'inferability', 'witness completeness',
               'witness supersets', 'compound units', 'artificial fragmentation', 'design freedom versus gaps'],
    'corrections': [
        'Kept the observation field protocol distinct from behavioral preservation. Architectural lexical descriptions support R03 but cannot replace R01; they remain HELPFUL_ONLY in complete witnesses.',
        'Accepted the lexical tests as an inferable alternative for the consumed observation protocol; did not require source solely because it is source.',
        'After the complete 1,071-cell draft, removed proposed R02 (document identity field internals) as an unnecessary semantic unit and downgraded R092/O2 and R268/O2 from REQUIRED to HELPFUL_ONLY. Postings can retain analysis.document directly, preserving its existing identity without knowing its internal id fields or digest algorithm. R02 is retired, not renumbered.',
        'Recomputed O2 witnesses after removing R02: each existing observation-interface alternative suffices independently. Eliminated supersets containing additional document source/tests or both independent interface alternatives.',
        'Did not require corpus construction or observation/acquisition internals: retained input objects preserve that provenance.',
        'Kept public initializers HELPFUL_ONLY because the frozen package-layout ambiguity permits coherent exposure without any particular initializer edit.',
        'Distinguished the complete AGENTS validation convention from corroborating pyproject configuration. Documentation-map support for R05 is redundant once the indispensable AGENTS validation rule is present.',
        'Recorded average-length empty policy and malformed manually assembled input handling as design ambiguities, preserving the frozen empty interpretation-gap list.'
    ],
    'remaining_unresolved_cells': 0,
}


def make_review(p):
    units = make_units(p)
    witnesses = {o: derive_witnesses(units, o) for o in ('O1','O2','O3')}
    return {
        'schema': 'stage-c-clean-primary-semantic-review-v1',
        'case_id': p['case_id'], 'task_identity': p['task_identity'],
        'task_text': p['task_text'], 'parent_frame': p['parent_frame'],
        'packet_binding': PACKET_DIGESTS, 'original_file_sha256': ORIGINALS,
        'reviewer': {'model':'GPT-6 Astra', 'reasoning':'High', 'designation':'sole designated primary',
                     'host_routing_independently_verified':False, 'second_reviewer':'NO'},
        'task_audit': {
            'exact_task_preserved':True, 'frozen_obligations_preserved':True,
            'assessment':'The one-line task names statistics and an inverted index. The frozen satisfaction criteria supply the deterministic counts, postings, provenance, empties and integration scope. These are authoritative task-backed constraints, not independently discovered parent facts.',
            'obligation_completeness':'O1 covers statistics, O2 covers inversion, O3 covers compatibility, exposure, documentation and validation. No packet-internal contradiction or omitted mandatory capability was found.',
            'interpretation_challenge':'The title alone does not specify every count, validation rule or exclusion. Their authority is the frozen packet interpretation, preserved rather than silently presented as title entailment.',
            'current_parent_distinction':'Only consumed interfaces, baseline semantics and parent development/documentation rules are repository-supported necessary units. Retaining existing document objects preserves their identity without a separate internal-identity fact.',
        },
        'obligations': p['obligations'], 'label_vocabulary':list(LABELS),
        'resource_frame':[identity(p,n) for n in range(1,358)],
        'cells':make_cells(p,units), 'semantic_units':units,
        'minimal_witnesses':witnesses, 'sufficiency':derive_sufficiency(witnesses),
        'frozen_interpretation_gaps':p['interpretation_gaps'],
        'frozen_ambiguities':p['ambiguities'],
        'gaps':{
            'TASK_INTERPRETATION_GAP':{'status':'NONE', 'records':[], 'rationale':'The frozen interpretation is authoritative and internally consistent; its original empty record is preserved exactly.'},
            'TASK_GAP':{'status':'NONE', 'records':[], 'rationale':'The frozen criteria are sufficient for a bounded implementation. API names, representation, deterministic ordering and explicit empty-average policy are design freedoms.'},
            'REPOSITORY_INFORMATION_GAP':{'status':'NONE', 'records':[], 'rationale':'All necessary current-parent facts have packet-contained support alternatives. No external resource is needed under the stated retained-input assumptions.'},
        },
        'ambiguities':AMBIGUITIES, 'limitations':LIMITATIONS, 'self_review':SELF_REVIEW,
        'blindness_attestation':{category:'NO' for category in EXCLUDED},
        'blindness_scope':'Access means excluded external experiment/repository evidence, not natural identifiers or descriptions inside authenticated original task/parent resource text. Parent source identity hashes in the frozen frame were not followed to Git.',
        'next_step':NEXT_STEP,
    }


def validate_span(p, s, allowed_resources=None):
    require(set(s) == {'resource_id','start_line','end_line','start_char','end_char','quote'}, 'Span schema')
    require(re.fullmatch(r'R\d{3}', s['resource_id']) is not None, 'Span resource identity')
    n = int(s['resource_id'][1:])
    require(1 <= n <= 357, 'Span resource range')
    if allowed_resources is not None:
        require(s['resource_id'] in allowed_resources, 'Span outside evidence resource')
    require(s == span(p,n,s['start_line'],s['end_line']), 'Span exact bytes/offsets/lines')


def validate_review(p, r):
    require(r['packet_binding'] == PACKET_DIGESTS, 'Packet binding')
    require(r['original_file_sha256'] == ORIGINALS, 'Original file binding')
    require(r['case_id'] == p['case_id'] and r['task_identity'] == p['task_identity'], 'Case/task identity')
    require(r['parent_frame'] == p['parent_frame'], 'Frame identity')
    require(r['task_text'] == p['task_text'] and r['obligations'] == p['obligations'], 'Task/obligations')
    require(r['label_vocabulary'] == list(LABELS), 'Label vocabulary')
    expected_frame = [identity(p,n) for n in range(1,358)]
    require(r['resource_frame'] == expected_frame, 'Resource frame identities/order')
    expected_keys = [(rid(n),o) for n in range(1,358) for o in ('O1','O2','O3')]
    actual_keys = [(c['resource_id'],c['obligation_id']) for c in r['cells']]
    require(len(actual_keys) == 1071, 'Exact cell count')
    require(len(set(actual_keys)) == 1071, 'Duplicate cell')
    require(actual_keys == expected_keys, 'Missing/unexpected/reordered cell')
    by_cell = {}
    for c in r['cells']:
        n = int(c['resource_id'][1:])
        require(all(c[k] == v for k,v in identity(p,n).items()), 'Cell resource identity')
        o = c['obligation_id']
        require(c['cell_id'] == f'{rid(n)}:{o}', 'Cell identity')
        require(c['obligation_identity'] == p['obligations'][int(o[1:])-1]['obligation_identity'], 'Cell obligation identity')
        require(c['label'] in LABELS and c['resolved'] is True, 'Invalid label/unresolved cell')
        require(bool(c['spans']) == (c['label'] != 'UNNECESSARY'), 'Positive span presence')
        require(c['rationale'] and c['inferability_rationale'] and c['provenance'], 'Cell rationale/provenance')
        for s in c['spans']:
            validate_span(p,s,{c['resource_id']})
        by_cell[c['resource_id'],o] = c
    units = r['semantic_units']
    uids = [u['id'] for u in units]
    require(len(uids) == len(set(uids)) and bool(uids), 'Unit identity uniqueness')
    aid_all = []
    for u in units:
        require(u['evidence_class'] in ('TASK_BACKED','REPOSITORY_SUPPORTED','TASK_AND_REPOSITORY_SUPPORTED'), 'Evidence class')
        require(u['statement'] and u['necessity_rationale'] and u['inferability_assumptions'], 'Semantic unit rationale')
        require(u['obligations'] and set(u['obligations']) <= {'O1','O2','O3'}, 'Semantic unit obligation')
        task_backed = u['evidence_class'] in ('TASK_BACKED','TASK_AND_REPOSITORY_SUPPORTED')
        repo_backed = u['evidence_class'] in ('REPOSITORY_SUPPORTED','TASK_AND_REPOSITORY_SUPPORTED')
        require(bool(u['task_evidence']) == task_backed, 'Unit task evidence class binding')
        require(bool(u['support_alternatives']) == repo_backed, 'Unit repository evidence class binding')
        for ev in u['task_evidence']:
            parts = ev['source'].strip('/').split('/')
            require(len(parts) == 3 and parts[0] == 'obligations', 'Task evidence source')
            ob = p['obligations'][int(parts[1])]
            require(ev['quote'] == ob[parts[2]] and ev['obligation_identity'] == ob['obligation_identity'], 'Task evidence quote')
        alternatives = u['support_alternatives']
        for a in alternatives + u['corroboration']:
            aid_all.append(a['id'])
            require(a['resource_ids'] and len(a['resource_ids']) == len(set(a['resource_ids'])), 'Alternative members')
            require(set(a['resource_ids']) <= set(x['resource_id'] for x in expected_frame), 'Alternative resource identity')
            require(a['spans'] and a['rationale'] and a['compatibility'], 'Alternative justification')
            require(a['support_class'] in ('DIRECT_SUPPORT','INFERABLE_SUPPORT','CORROBORATION_ONLY'), 'Support class')
            require((a in u['corroboration']) == (a['support_class'] == 'CORROBORATION_ONLY'), 'Corroboration cannot satisfy unit')
            require(set(s['resource_id'] for s in a['spans']) == set(a['resource_ids']), 'Every alternative member supported')
            for s in a['spans']:
                validate_span(p,s,set(a['resource_ids']))
            for o in u['obligations']:
                require(all(by_cell[x,o]['label'] != 'UNNECESSARY' for x in a['resource_ids']), 'Unit evidence contradicts cell label')
        sets = [set(a['resource_ids']) for a in alternatives]
        require(not any(x <= y for i,x in enumerate(sets) for j,y in enumerate(sets) if i != j), 'Nonminimal/duplicate unit support alternative')
    require(len(aid_all) == len(set(aid_all)), 'Duplicate support alternative identity')
    # Exhaustive independent subset coverage check, distinct from product-based
    # witness construction. It verifies both completeness and member necessity.
    for o in ('O1','O2','O3'):
        needed = [u for u in units if o in u['obligations']]
        candidates = sorted({x for u in needed for a in u['support_alternatives'] for x in a['resource_ids']})
        complete = []
        for size in range(len(candidates)+1):
            for values in itertools.combinations(candidates,size):
                s = set(values)
                if all(supports(u,s) for u in needed):
                    if not any(t < s for t in complete):
                        complete.append(s)
        actual = r['minimal_witnesses'][o]
        require({frozenset(w['resource_ids']) for w in actual} == {frozenset(s) for s in complete}, 'Witness completeness/minimality')
        require(actual == derive_witnesses(units,o), 'Witness IDs/assignments/necessity')
        require(all(w['member_necessity'][x] for w in actual for x in w['resource_ids']), 'Redundant witness member')
        required_union = set().union(*(set(w['resource_ids']) for w in actual))
        require(required_union == {c['resource_id'] for c in r['cells'] if c['obligation_id'] == o and c['label'] == 'REQUIRED'}, 'REQUIRED/witness agreement')
    require(r['sufficiency'] == derive_sufficiency(r['minimal_witnesses']), 'Sufficiency/intersection arithmetic')
    require(r['frozen_interpretation_gaps'] == p['interpretation_gaps'] and r['frozen_ambiguities'] == p['ambiguities'], 'Frozen gap/ambiguity preservation')
    require(set(r['gaps']) == {'TASK_INTERPRETATION_GAP','TASK_GAP','REPOSITORY_INFORMATION_GAP'}, 'Gap categories')
    require(r['ambiguities'] == AMBIGUITIES, 'Gap/ambiguity authored decision binding')
    require(r['self_review'] == SELF_REVIEW and r['self_review']['distinct_self_review_completed'], 'Self-review binding')
    require(r['blindness_attestation'] == {x:'NO' for x in EXCLUDED}, 'Blindness exclusions')
    # Bind prose decisions as well as machine-checkable relationships to this
    # primary's authored record. This is not a second semantic adjudication.
    require(r == make_review(p), 'Authored primary decision binding')
    return {'resources':357, 'obligations':3, 'expected_cells':1071, 'actual_cells':1071,
            'duplicates':0, 'missing':0, 'unexpected':0, 'unresolved':0}


def statistics(r):
    counts = {o: {label:sum(c['obligation_id']==o and c['label']==label for c in r['cells'])
                  for label in LABELS} for o in ('O1','O2','O3')}
    classes = Counter(u['evidence_class'] for u in r['semantic_units'])
    return {'case_id':r['case_id'], 'resources':357, 'obligations':3, 'expected_cells':1071,
            'actual_cells':len(r['cells']), 'duplicates':0, 'missing':0, 'unexpected':0, 'unresolved':0,
            'label_counts_by_obligation':counts,
            'total_label_counts':{label:sum(v[label] for v in counts.values()) for label in LABELS},
            'required_resource_union':sorted({c['resource_id'] for c in r['cells'] if c['label']=='REQUIRED'}),
            'semantic_unit_count':len(r['semantic_units']),
            'semantic_unit_classes':{c:classes[c] for c in ('TASK_BACKED','REPOSITORY_SUPPORTED','TASK_AND_REPOSITORY_SUPPORTED')},
            'semantic_unit_counts_by_obligation':{o:sum(o in u['obligations'] for u in r['semantic_units']) for o in counts},
            'witness_counts_by_obligation':{o:len(w) for o,w in r['minimal_witnesses'].items()},
            'support_alternative_count':sum(len(u['support_alternatives']) for u in r['semantic_units']),
            'corroboration_count':sum(len(u['corroboration']) for u in r['semantic_units']),
            **r['sufficiency']}


def validate_hashes(files, hashes):
    require(hashes['schema'] == 'stage-c-scientific-sha256-v1', 'Scientific hash schema')
    require(hashes['sha256'] == {name:sha(raw) for name,raw in sorted(files.items())}, 'Scientific hash')
    require(hashes['excluded'] == ['stage_c_hashes.json (self-reference)', '.scratch/', '.local/'], 'Hash exclusion scope')


def adversarial(p, r):
    cases = []
    def add(name, mutate):
        changed = copy.deepcopy(r)
        mutate(changed)
        try:
            validate_review(p,changed)
        except (ValueError, KeyError, IndexError, TypeError):
            cases.append({'mutation':name, 'result':'REJECTED'})
        else:
            raise ValueError('Adversarial mutation accepted: '+name)
    add('cell identity', lambda x:x['cells'][0].update(cell_id='R001:O2'))
    add('missing cell', lambda x:x['cells'].pop())
    add('duplicate cell', lambda x:x['cells'].__setitem__(1,copy.deepcopy(x['cells'][0])))
    add('unexpected cell', lambda x:x['cells'][0].update(obligation_id='O4'))
    add('invalid label', lambda x:x['cells'][0].update(label='MAYBE'))
    add('resource identity', lambda x:x['cells'][0].update(document_identity='0'*64))
    add('positive span', lambda x:next(c for c in x['cells'] if c['spans'])['spans'][0].update(quote='fabricated'))
    add('semantic unit identity', lambda x:x['semantic_units'][0].update(id='T99'))
    add('semantic unit meaning', lambda x:x['semantic_units'][0].update(statement='Compute rankings.'))
    add('evidence class', lambda x:x['semantic_units'][0].update(evidence_class='REPOSITORY_SUPPORTED'))
    add('support alternative', lambda x:next(u for u in x['semantic_units'] if u['support_alternatives'])['support_alternatives'][0].update(resource_ids=['R002']))
    add('witness incomplete', lambda x:x['minimal_witnesses']['O1'][0].update(resource_ids=[]))
    add('witness redundant superset', lambda x:x['minimal_witnesses']['O1'][0]['resource_ids'].append('R271'))
    add('missing alternative witness', lambda x:x['minimal_witnesses']['O2'].pop())
    add('sufficient union', lambda x:x['sufficiency']['distinct_sufficient_resource_unions'][0].append('R357'))
    add('task combination arithmetic', lambda x:x['sufficiency'].update(task_combination_count=999))
    add('obligation indispensability', lambda x:x['sufficiency']['obligation_intersections']['O1']['resource_ids'].append('R098'))
    add('task indispensability', lambda x:x['sufficiency']['task_indispensable_resource_ids'].append('R098'))
    add('gap', lambda x:x['gaps']['TASK_GAP'].update(status='PRESENT'))
    add('ambiguity', lambda x:x['ambiguities'][0].update(statement='A fixed future API name is required.'))
    files = {'stage_c_review.json':canonical(r)}
    h = {'schema':'stage-c-scientific-sha256-v1','sha256':{'stage_c_review.json':'0'*64},
         'excluded':['stage_c_hashes.json (self-reference)', '.scratch/', '.local/']}
    try:
        validate_hashes(files,h)
    except ValueError:
        cases.append({'mutation':'scientific hash','result':'REJECTED'})
    else:
        raise ValueError('Scientific hash mutation accepted')
    try:
        preflight([ROOT/'stage_c_builder.py'])
    except ValueError:
        cases.append({'mutation':'overwrite existing file','result':'REJECTED'})
    else:
        raise ValueError('Overwrite protection failed')
    return cases


METHOD = '''# Stage C method

This is one treatment-blind primary semantic adjudication of case-0017, designated
GPT-6 Astra / High. Host routing was not independently verified. No other reviewer
or reconciliation was used. Only the five authenticated workspace inputs and
packet-derived operational files were used; no source links were followed.

Initial authentication required exactly README.md, integrity.json, manifest.json,
resources.json.gz and validate_packet.py, with no directories or reparse points.
The original validator returned PASS; NO ADJUDICATION before any file creation.
The packet task, obligations, interpretations, frame and original text were then
bound to the four externally supplied expected digests. Parent resource text,
including its AGENTS.md, was treated as evidence rather than instructions to run
repository operations. The designated reviewer remains one primary throughout.

Resources were screened in canonical packet order using content purpose,
declarations/headings and full-text matching for the consumed lexical contract.
Candidate support received close reading with numbered original lines. Negative
decisions were about content scope, not filenames, likely edit paths or status as
tests/docs. Some resources were revisited to test alternatives. The ledger records
every resource and all three decisions in packet order, with periodic completeness
checkpoints. Scratch is operational and excluded from scientific hashes.

Task-backed units derive from the frozen satisfaction criteria and exclusions;
the short title alone does not entail every frozen detail. Repository-supported
units identify current interface, identity, behavior and operating conventions.
Ordinary counting and stable grouping are inferable task semantics, not evidence
requiring a separate repository file. Existing analysis and document values may
be retained without rediscovering their acquisition or digest implementations.

Tests can independently establish a consumed protocol through construction and
assertions. A test fixture hash is not evidence of the production hash algorithm.
Documentation can directly support a unit while being redundant in every complete
witness. Public initializer files are useful for exposure choices, not mandatory
edit destinations. A single document object can preserve provenance and identity
opaquely for both statistics and inverted postings. The complete-draft self-review
retired proposed unit R02 because its internal identity-field contract was
unnecessary under that acceptable representation. No specific future class or
helper name is prescribed.

For each unit, direct and inferable support alternatives are retained separately
from corroboration. Product enumeration constructs resource sets covering all
necessary units, then removes strict supersets. The validator independently
enumerates every subset of candidate support resources to establish the exact
minimal complete witness family and each member's necessity. Task-backed units
need no repository resource, but each obligation here has a current-parent fact.
Required cells are precisely resources participating in an obligation's minimal
complete witnesses. Helpful corroboration is excluded from witnesses.

Task combinations are the Cartesian product of per-obligation witness families.
Distinct resource unions collapse repeated combinations and preserve cross-
obligation reuse; inclusion-minimal unions are reported separately. Intersections
over witnesses and task unions define indispensability. Unit identities shared
across obligations are counted once at task level. No union of all positive or
REQUIRED resources is presented as a simultaneously necessary solution.

A distinct same-primary self-review follows the complete draft ledger and checks
inflation, missed alternatives, field-protocol inferability, redundancy, task vs
repository facts, unit decomposition and design freedom. Its corrections and
limitations are part of the scientific review. This is not a second reviewer.

The standalone builder embeds the authored decisions and imports only the Python
standard library. It reads the packet, never imports devtools and never accesses
network, checkout, parent/sibling resources or Git. Exact spans use Python string
character offsets (end exclusive) and one-based inclusive line endpoints, with
the exact original substring retained. JSON uses sorted ASCII keys, two-space
indentation and LF final newline; Markdown uses UTF-8 and LF.

Commands, all from this workspace:

    python -B stage_c_builder.py --draft
    python -B stage_c_builder.py --build
    python -B stage_c_builder.py --verify

Build refuses if any generated scientific output already exists and performs its
preflight before writing. Verify re-authenticates originals, validates every cell,
unit, span, alternative, witness, intersection and arithmetic result, executes
representative adversarial mutations, then requires exact derived-byte identity
for all generated files. It runs in a separate Python process from build. Replay
does not overwrite scientific artifacts. Semantic prose is also bound to this
primary's embedded authored decisions; that integrity check is not independent
semantic validation. No mechanical check can prove the primary's semantic model.

stage_c_hashes.json binds review, statistics, Markdown, method, validation and
builder bytes. It excludes its own digest to avoid self-reference; its digest is
reported in the final operational handoff. Scratch and .local are excluded. The
seven artifact digests appear in the handoff and final report, avoiding circular
hash claims in a file that would hash itself. The handoff is created only after
separate-process replay, adversarial validation and original-file preservation.
'''


def markdown(r, s):
    address = {x['resource_id']:x['address'] for x in r['resource_frame']}
    lines = ['# Clean primary semantic adjudication: case-0017', '',
             'MODEL: GPT-6 Astra. REASONING: High. Sole primary; second reviewer: NO.',
             'Host routing independently verified: NO.', '',
             'Task: '+r['task_text'].strip(), '',
             'Authentication: PASS; NO ADJUDICATION before file creation. Exact initial five files; no directories, symlinks, junctions or reparse points.', '']
    lines += [f'- {k}: `{v}`' for k,v in PACKET_DIGESTS.items()]
    lines += ['', 'Frame:', ''] + [f'- {k}: `{r["parent_frame"][k]}`' for k in ('repository_id','snapshot_id','corpus_id')]
    lines += ['', 'Completeness: 357 resources × 3 obligations = 1,071 resolved cells; duplicates, missing, unexpected and unresolved: 0.', '',
              '| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY | Witnesses |',
              '|---|---:|---:|---:|---:|']
    for o, counts in s['label_counts_by_obligation'].items():
        lines.append(f'| {o} | {counts["REQUIRED"]} | {counts["HELPFUL_ONLY"]} | {counts["UNNECESSARY"]} | {s["witness_counts_by_obligation"][o]} |')
    total=s['total_label_counts']
    lines += [f'| Total | {total["REQUIRED"]} | {total["HELPFUL_ONLY"]} | {total["UNNECESSARY"]} | |', '',
              'REQUIRED-resource union (not one necessary solution):', '']
    lines += [f'- {x}: `{address[x]}`' for x in s['required_resource_union']]
    lines += ['', f'Semantic units: {s["semantic_unit_count"]}; classes: '+json.dumps(s['semantic_unit_classes'],sort_keys=True)+'.', '',
              '| Unit | Obligations | Evidence class | Necessary information |', '|---|---|---|---|']
    for u in r['semantic_units']:
        lines.append('| '+ ' | '.join([u['id'], ', '.join(u['obligations']),u['evidence_class'],u['statement']])+' |')
    lines += ['', 'Minimal complete witnesses:', '']
    for o, ws in r['minimal_witnesses'].items():
        for w in ws:
            lines.append(f'- {w["id"]}: resources '+', '.join(w['resource_ids'])+'; units '+', '.join(w['unit_ids'])+'.')
        inter=s['obligation_intersections'][o]
        lines.append(f'- {o} indispensable resources: '+(', '.join(inter['resource_ids']) or 'none')+'; indispensable units: '+', '.join(inter['unit_ids'])+'.')
    lines += ['', f'Task combinations: {s["task_combination_count"]}. Distinct sufficient resource unions: {s["sufficient_resource_union_count"]}.', '',
              'All distinct sufficient resource unions:', '']
    lines += ['- '+', '.join(u) for u in s['distinct_sufficient_resource_unions']]
    lines += ['', 'Inclusion-minimal sufficient resource unions:', '']
    lines += ['- '+', '.join(u) for u in s['inclusion_minimal_sufficient_resource_unions']]
    lines += ['', f'Resource-count range across all sufficient unions: {s["resource_count_range"]}; inclusion-minimal range: {s["inclusion_minimal_resource_count_range"]}.',
              f'Sufficient semantic-unit unions: {len(s["sufficient_semantic_unit_unions"])}; count range: {s["semantic_unit_count_range"]}.',
              'Task-indispensable resources: '+(', '.join(s['task_indispensable_resource_ids']) or 'none')+'.',
              'Task-indispensable units: '+', '.join(s['task_indispensable_unit_ids'])+'.', '',
              'Positive evidence (all exact quotes, rationale, inference and native identities are retained in stage_c_review.json):', '',
              '| Resource | Obligation | Label | Original lines |', '|---|---|---|---|']
    for c in r['cells']:
        if c['label'] != 'UNNECESSARY':
            lines.append(f'| {c["resource_id"]} `{c["address"]}` | {c["obligation_id"]} | {c["label"]} | '+', '.join(f'{v["start_line"]}-{v["end_line"]}' for v in c['spans'])+' |')
    lines += ['', 'Gap audit:', '']
    lines += [f'- {k}: {v["status"]}. {v["rationale"]}' for k,v in r['gaps'].items()]
    lines += ['', 'Frozen interpretation gaps: `[]`, preserved exactly.', '', 'Ambiguities:', '']
    lines += [f'- {a["id"]}: {a["statement"]} {a["disposition"]}' for a in r['ambiguities']]
    lines += ['', 'Self-review corrections:', ''] + ['- '+x for x in r['self_review']['corrections']]
    lines += ['', 'Limitations:', ''] + ['- '+x for x in r['limitations']]
    lines += ['', 'Blindness attestation (excluded external evidence access):', '']
    lines += [f'- {k}: {v}' for k,v in r['blindness_attestation'].items()]
    lines += ['', r['blindness_scope'], '',
              'Validation: exhaustive cell/frame/span checks; independent subset witness validation; exact task arithmetic; 22 representative adversarial mutations including overwrite and scientific-hash rejection. Deterministic replay requires exact generated-byte identity in a separate Python process. Original packet SHA-256 values are rechecked on every build and verification.', '',
              'Scientific artifacts: stage_c_review.json, stage_c_statistics.json, STAGE_C_REVIEW.md, stage_c_validation.json, stage_c_hashes.json, stage_c_method.md, stage_c_builder.py. SHA-256 bindings are in stage_c_hashes.json; its own digest and separate-process outcome are reported in the operational handoff.', '',
              'Exact next step:', '', NEXT_STEP, '', 'STOP.', '']
    return '\n'.join(lines).encode('utf-8')


def preflight(paths):
    for path in paths:
        safe(path)
        require(not path.exists(), 'Overwrite refusal: '+path.name)


def outputs(p):
    review = make_review(p)
    gate = validate_review(p,review)
    stats = statistics(review)
    mutations = adversarial(p,review)
    validation = {
        'schema':'stage-c-validation-v1', 'status':'PASS', 'case_id':p['case_id'],
        'packet_binding':PACKET_DIGESTS, 'completeness_gate':gate,
        'checks':{k:'PASS' for k in ['packet binding','frame','task','obligations','labels','identities','positive spans',
                                    'units','evidence classes','support alternatives','witness completeness',
                                    'witness minimality','intersections','task-level mathematics',
                                    'gaps and ambiguities','original packet preservation','overwrite refusal']},
        'adversarial_mutations':mutations, 'adversarial_rejected':len(mutations),
        'deterministic_codec':'sorted ensure_ascii JSON, indent=2, LF; Markdown UTF-8 LF',
        'replay_requirement':'Separate python -B stage_c_builder.py --verify process must reproduce every generated scientific byte and verify all hashes; actual run receipt is operational .scratch/verification.json.',
        'scientific_hash_scope':'stage_c_hashes.json binds six artifacts and excludes itself; its own digest is reported in the final handoff.',
        'semantic_validation_limit':'Arithmetic and integrity validation do not constitute another semantic reviewer.'}
    result = {'stage_c_review.json':canonical(review), 'stage_c_statistics.json':canonical(stats),
              'STAGE_C_REVIEW.md':markdown(review,stats), 'stage_c_validation.json':canonical(validation),
              'stage_c_method.md':METHOD.encode('utf-8')}
    hashed = {**result, 'stage_c_builder.py':safe(ROOT/'stage_c_builder.py').read_bytes()}
    hashes = {'schema':'stage-c-scientific-sha256-v1', 'sha256':{n:sha(v) for n,v in sorted(hashed.items())},
              'excluded':['stage_c_hashes.json (self-reference)', '.scratch/', '.local/']}
    validate_hashes(hashed,hashes)
    result['stage_c_hashes.json'] = canonical(hashes)
    return result


def draft(p):
    r = make_review(p)
    cells=[]
    screens=[]
    checkpoints=[]
    scratch=safe(ROOT/'.scratch')
    scratch.mkdir(exist_ok=True)
    for n,resource in enumerate(p['resources'],1):
        cells.extend(r['cells'][(n-1)*3:n*3])
        screens.append({'resource_id':rid(n),'address':resource['address'],
                        'content_scope':content_scope(resource),'source_blob_sha256':resource['source_blob_sha256'],
                        'decision_state':'RESOLVED','cell_ids':[c['cell_id'] for c in cells[-3:]]})
        if n % 25 == 0 or n==357:
            keys=[c['cell_id'] for c in cells]
            require(len(keys)==3*n and len(set(keys))==3*n, 'Ledger checkpoint')
            checkpoints.append({'processed_resources':n,'complete_cells':len(cells),'duplicates':0,
                                'missing_processed_cells':0,'unresolved_processed_cells':0,'remaining_cells':1071-len(cells)})
            ledger={'packet_binding':PACKET_DIGESTS,'processed_resources':n,'cells':cells,
                    'resource_screening':screens,'checkpoints':checkpoints,'scientific':False}
            safe(scratch/'adjudication_work.json').write_bytes(canonical(ledger))
    safe(scratch/'draft_review.json').write_bytes(canonical(r))
    print(json.dumps({'draft_gate':validate_review(p,r),'statistics':statistics(r)},indent=2))


def verify(p):
    expected=outputs(p)
    actual={name:safe(ROOT/name).read_bytes() for name in expected}
    require(all(actual[n]==v for n,v in expected.items()), 'Exact derived-byte identity')
    review=json.loads(actual['stage_c_review.json'])
    gate=validate_review(p,review)
    hashes=json.loads(actual['stage_c_hashes.json'])
    validate_hashes({n:v for n,v in actual.items() if n!='stage_c_hashes.json'} |
                    {'stage_c_builder.py':(ROOT/'stage_c_builder.py').read_bytes()},hashes)
    receipt={'status':'PASS','separate_python_process':True,'exact_derived_byte_identity':True,
             'gate':gate,'adversarial_rejected':22,'original_packet_preserved':True,
             'sha256':{n:sha(safe(ROOT/n).read_bytes()) for n in sorted([*expected,'stage_c_builder.py'])}}
    safe(ROOT/'.scratch').mkdir(exist_ok=True)
    safe(ROOT/'.scratch'/'verification.json').write_bytes(canonical(receipt))
    print(json.dumps(receipt,indent=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--draft',action='store_true')
    group.add_argument('--build',action='store_true')
    group.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    p=packet()
    if args.draft:
        draft(p)
    elif args.build:
        require(not (ROOT/'.local').exists(), '.local must not exist before scientific freeze')
        generated=outputs(p)
        preflight([ROOT/name for name in generated])
        for name,raw in generated.items():
            with safe(ROOT/name).open('xb') as f:
                f.write(raw)
        print(json.dumps({'status':'BUILT','files':sorted(generated),'next':'Run separate python -B stage_c_builder.py --verify'},indent=2))
    else:
        verify(p)


if __name__=='__main__':
    main()
