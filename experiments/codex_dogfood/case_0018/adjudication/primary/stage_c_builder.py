"""Deterministic, packet-only serialization of one primary semantic adjudication.

This program encodes human semantic decisions; it does not discover relevance.
Only the five authenticated packet files and this builder are scientific inputs.
Use python -B stage_c_builder.py --build for separate-process replay and freeze.
"""
from __future__ import annotations

import argparse
import ast
import copy
import gzip
import hashlib
import itertools
import json
import runpy
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINAL_HASHES = {
    'README.md': 'ef6241e6971553a124fd5abde64c5aa0a9611ab7a9495316ffaf52023f953de8',
    'integrity.json': '6f3955479aa6fbb4ae80189256f0a49160ad592cfd9089201cd222556ba726f1',
    'manifest.json': '6381d26ed9c406c6a28aa243bf5346c65e5fbe74c3a59e14f99fb4f2007bea85',
    'resources.json.gz': 'ef761a2d124b26181889580719baf8cc082897be6b7fce9fb86b69cbf4f1c831',
    'validate_packet.py': '0d74cc32d2522aa336fea568130b270802c03844975567deece2fe0d835acfe6',
}
PAYLOAD_HASH = '66aa4b49ee362d786e4c879db318f9c94d56e2d960743a983653d11c77e72b4f'
FRAME = {
    'repository_id': '5cf96d9e-d6a5-44a6-83d3-1e24f6e00009',
    'snapshot_id': 'bf0f8d2a30e2be56053a2098a4800ad3d43a70c41707b618ad36c197b6b6b827',
    'corpus_id': '7ce2a9e4a048fcb3d1a4e8c625be8c951a84dc0c5cac70809c6427a8bb50eb33',
}
OBS = ('O1', 'O2', 'O3')
SELF_REVIEW = {
    'status': 'COMPLETE',
    'reviewer': 'same designated primary',
    'passes': 1,
    'second_reviewer': False,
    'reconciliation': False,
    'checks': [
        'Rechecked the original task against all frozen satisfaction/exclusion clauses; preserved three typed gaps and no unjustified fourth obligation.',
        'Reviewed every positive cell, exact support span, alternative and minimal witness; challenged whether a fact was truly necessary or only an implementation detail.',
        'Rechecked all 382 content-screening records against negative cells; all 350 resources unnecessary across every obligation had no targeted import/relationship hits, and their content subjects fell outside the bounded capability.',
        'Challenged package proximity, ordinary import use sites, facade/edit-destination bias, generic design analogies and historical implementation leakage.',
        'Checked unique positive module resolution, relative/nonpositive behavior, alias multiplicity, collision versus repeated-entry handling and foreign/stale state qualification.',
        'Confirmed tests can substitute for supported behavioral facts but do not prove unseen runtime behavior; no tests or resource code were executed.',
        'Checked source occurrence provenance versus semantic identity and rejected universal invalidation merely because a snapshot changed.',
        'Recomputed and inspected all final labels, obligation witnesses, complete task combinations, unit/resource unions and indispensability after the correction.',
        'Reviewed completeness, exact spans, independent powerset validation and all 21 adversarial rejection results before final publication.',
    ],
    'corrections': [
        'Narrowed U6 from exact universe hash/order implementation to repository/membership admission and repeated-entry rejection; added resolver tests as an alternative. Opaque identity can be retained without reproducing its hash algorithm.',
        'This changes R057/O3, R280/O2 and R280/O3 from HELPFUL_ONLY to REQUIRED through newly available minimal witnesses. R092 ceases to be individually indispensable; R089 remains the sole resource indispensable for each obligation and the task under the declared information model.',
    ],
}


def canonical(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n').encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe(path):
    require(path.resolve().is_relative_to(ROOT), 'Path leaves sterile workspace')
    for member in (path, *path.parents):
        if member.exists():
            require(not member.is_symlink() and not (
                getattr(member.lstat(), 'st_file_attributes', 0)
                & stat.FILE_ATTRIBUTE_REPARSE_POINT
            ), 'Reparse point')
        if member == ROOT:
            break
    return path


def authenticate():
    for name, digest in ORIGINAL_HASHES.items():
        require(sha(safe(ROOT / name).read_bytes()) == digest, 'Original packet changed: ' + name)
    raw = gzip.decompress((ROOT / 'resources.json.gz').read_bytes())
    require(sha(raw) == PAYLOAD_HASH, 'Payload hash')
    packet = json.loads(raw)
    validator = runpy.run_path(str(ROOT / 'validate_packet.py'), run_name='packet_authentication_only')
    validator['validate_payload'](packet, validator['BOUND'])
    require(raw == canonical(packet), 'Canonical payload')
    require(packet['case_id'] == 'case-0018', 'Case')
    require(packet['task_text'] == 'Implement qualified repository import relations\n', 'Task')
    require(all(packet['parent_frame'][k] == v for k, v in FRAME.items()), 'Frame')
    require(len(packet['resources']) == 382 and len(packet['obligations']) == 3, 'Counts')
    return packet


def minimal(sets):
    ordered = sorted(set(frozenset(s) for s in sets), key=lambda s: (len(s), tuple(sorted(s))))
    result = []
    for candidate in ordered:
        if not any(other <= candidate for other in result):
            result.append(candidate)
    return [sorted(s) for s in result]


def combine(alternatives):
    current = [[]]
    for choices in alternatives:
        current = minimal(set(left) | set(right) for left in current for right in choices)
    return current


def resource_id(number):
    return f'R{number:03d}'


class Decisions:
    def __init__(self, packet):
        self.packet = packet
        self.evidence = {}
        self.units = []
        self.help = {}

    def span(self, number, lo, hi):
        key = f'E{number:03d}_{lo:04d}_{hi:04d}'
        if key not in self.evidence:
            r = self.packet['resources'][number - 1]
            lines = r['content'].splitlines(keepends=True)
            require(1 <= lo <= hi <= len(lines), 'Span bounds')
            start = sum(map(len, lines[:lo - 1]))
            end = sum(map(len, lines[:hi]))
            quote = r['content'][start:end]
            self.evidence[key] = {
                'id': key, 'resource_id': resource_id(number),
                'address': r['address'], 'document_identity': r['document_identity'],
                'content_identity': r['content_identity'],
                'start_line_1based': lo, 'end_line_1based_inclusive': hi,
                'start_character_0based': start, 'end_character_0based_exclusive': end,
                'quote': quote, 'quote_utf8_sha256': sha(quote.encode('utf-8')),
            }
        return key

    def unit(self, uid, statement, rationale, alternatives, task=False):
        supports = []
        for i, alternative in enumerate(alternatives, 1):
            evidence = [self.span(*entry) for entry in alternative]
            supports.append({
                'id': f'{uid}.A{i}',
                'resources': sorted({self.evidence[e]['resource_id'] for e in evidence}),
                'evidence': sorted(evidence),
                'task_span': {'start_character_0based': 0, 'end_character_0based_exclusive': len(self.packet['task_text'].rstrip('\n')),
                              'quote': self.packet['task_text'].rstrip('\n')} if task else None,
            })
        self.units.append({
            'id': uid, 'statement': statement,
            'classification': 'TASK_BACKED' if task else 'REPOSITORY_SUPPORTED',
            'necessity_rationale': rationale,
            'minimal_support_alternatives': supports,
        })

    def helpful(self, number, obligations, spans, rationale):
        for ob in obligations:
            self.help[(resource_id(number), ob)] = {
                'evidence': sorted(self.span(number, lo, hi) for lo, hi in spans),
                'rationale': rationale,
            }


def semantic_decisions(packet):
    d = Decisions(packet)
    d.unit('T0', 'Implement qualified repository import relations.',
           'The original task supplies the goal; no repository resource is required to learn this sentence.',
           [[]], task=True)
    d.unit('U1', 'The existing direct-module-body import analysis retains exact source resource, repository/snapshot correlation, source coordinates, content-derived derivation identity, and a distinct ordinal for each syntactic alias.',
           'Relation provenance and occurrence accounting must compose with the actual declaration contract, including repeated aliases sharing a statement span. Names or target addresses alone cannot replace this information.',
           [[(89, 23, 68), (89, 75, 129)]])
    d.unit('U2', 'The established resolver consumes an analysis/declaration and explicit target universe; a unique matching eligible module portion is resolved. Imported members are not resolved as submodules.',
           'A positive relation must follow established bounded resolution, rather than guessing a file or resolving the imported member.',
           [[(90, 75, 92), (90, 121, 141), (90, 168, 185)],
            [(278, 67, 147)]])
    d.unit('U3', 'The established import outcome vocabulary distinguishes resolved, unresolved-in-universe, ambiguous and unsupported; these are bounded outcomes, not runtime dependency truth.',
           'Preserving qualification requires knowing which nonpositive meanings the parent actually establishes.',
           [[(90, 26, 53), (90, 82, 86), (90, 99, 141)],
            [(278, 110, 147), (278, 236, 293)],
            [(3, 450, 456)], [(10, 347, 352)], [(57, 156, 158)]])
    d.unit('U4', 'Relative module resolution uses an explicit source interpretation and distinguishes missing/ambiguous source and traversal beyond its package; repository/source mismatches are rejected.',
           'Both relative positive relations and qualified nonpositive outcomes must preserve these parent rules; choosing a convenient source root changes import truth.',
           [[(90, 87, 108), (90, 144, 185)],
            [(278, 150, 301), (278, 352, 363)]])
    d.unit('U5', 'Module meaning is an explicit-root interpretation of selected observed resources, with ordinary/package roles and dotted names. Colliding names remain distinct without root precedence.',
           'A relation target is an interpreted observed resource, not a dotted-name-to-path guess. The root and role qualify the mapping.',
           [[(92, 52, 101), (92, 156, 198), (92, 211, 243)],
            [(280, 39, 110), (280, 165, 198)],
            [(3, 436, 448)], [(10, 335, 345)], [(57, 147, 155)]])
    d.unit('U6', 'The established module universe is repository-scoped; foreign repositories and repeated interpretation entries are rejected rather than being made into additional valid matches.',
           'Duplicate/frame accounting must preserve parent universe admission rather than silently treating repeated or foreign inputs as positive evidence. A relation can retain opaque parent identities; reproducing the exact sorted-identity hash algorithm is not mandatory.',
           [[(92, 118, 153)], [(278, 366, 403)]])
    d.unit('U7', 'Applicability follows semantic dependencies; snapshot provenance and semantic identity are distinct. A changed snapshot need not invalidate unchanged applicable knowledge, while changed consumed content or resolution state can matter.',
           'Stale/changed-frame handling must not silently rebind provenance or impose universal snapshot invalidation.',
           [[(3, 155, 185), (3, 216, 232)],
            [(5, 386, 443)],
            [(8, 389, 409), (8, 442, 460)],
            [(10, 18, 45), (10, 103, 109)],
            [(89, 23, 68), (89, 88, 93), (90, 57, 72), (92, 77, 101), (92, 118, 153)],
            [(89, 23, 68), (89, 88, 93), (90, 57, 72), (280, 126, 162)]])
    d.unit('U8', 'Repository relationship knowledge has qualified derived semantics distinct from derivation dependencies, graph infrastructure and purpose-relative retrieval/Context. A generic graph or retrieval mechanism is not required to add a bounded relation family.',
           'This resolves the repository meaning of qualified relations without silently enlarging the task to graph storage, ranking or recursive closure.',
           [[(3, 134, 153), (3, 195, 214), (3, 244, 254), (3, 506, 516)],
            [(5, 786, 844), (5, 890, 894)],
            [(8, 400, 434), (8, 558, 574)],
            [(10, 18, 60), (10, 116, 134), (10, 335, 352)]])

    d.helpful(1, ['O3'], [(30, 39), (55, 59), (210, 230)],
              'Repository operating policy supports reuse, documentation-impact assessment and deterministic validation; it does not prescribe a relation API or supply an indispensable import contract.')
    d.helpful(2, ['O3'], [(24, 48)],
              'Project posture helps explain deterministic knowledge versus retrieval and avoiding premature generalization; it adds no missing import-specific contract.')
    d.helpful(6, ['O1', 'O3'], [(100, 107), (136, 147)],
              'Clarifies that import/graph proximity used by retrieval is purpose-relative evidence; useful boundary context, not a necessary relation-construction input.')
    d.helpful(7, ['O3'], [(63, 86)],
              'Clarifies downstream disclosure coverage and relationship use; it does not select this capability\'s representation or integration API.')
    d.helpful(57, ['O3'], [(27, 38), (147, 158)],
              'Identifies current documentation claims and their authority; useful documentation-impact evidence, not a mandatory edit destination.')
    d.helpful(59, OBS, [(67, 81)],
              'Records the bounded progression from declarations/module interpretation to resolution and distinguishes relations still to be added. Its earlier no-resolution wording is qualified by the subsequent resolver paragraph.')
    d.helpful(60, ['O3'], [(18, 35), (40, 70)],
              'Supplies concrete deterministic tooling and branch-coverage configuration; these aid implementation validation but do not establish relation semantics.')
    d.helpful(78, ['O3'], [(4, 10), (48, 71), (104, 150)],
              'The aggregate Context facade demonstrates existing public export style; a new relation need not be re-exported from this specific file.')
    d.helpful(82, OBS, [(95, 143), (225, 238)],
              'Function derivation identity and ordered aggregation are concrete reusable design precedents; function subject semantics are not import relation truth.')
    d.helpful(84, ['O2', 'O3'], [(68, 101)],
              'Shows exact snapshot/resource checks before applying source coordinates. This materialization policy is an analogy, not authority for rejecting every cross-snapshot import result.')
    d.helpful(87, ['O2', 'O3'], [(94, 125)],
              'Shows deterministic first-match grouping that preserves all declaration support, a possible duplicate-accounting pattern without imposing its retrieval policy on relations.')
    d.helpful(88, ['O3'], [(4, 30)],
              'Existing import exports aid public API integration; the task does not make this expected edit location necessary evidence.')
    d.helpful(91, ['O3'], [(4, 26)],
              'Existing module exports aid canonical primitive reuse; facade names alone do not establish their semantics.')
    d.helpful(92, ['O2', 'O3'], [(118, 153)],
              'The implementation additionally retains supplied interpretation order and hashes sorted identities. Useful identity detail does not mandate reproducing the parent hash or selecting that order for new relation output.')
    d.helpful(94, ['O3'], [(22, 36)],
              'Identifies canonical public repository value imports for integration; other inspected contracts already expose the relevant types.')
    d.helpful(98, OBS, [(11, 41)],
              'Explains the concrete nominal repository identity wrapper and parsing API, useful provenance background without requiring a new identity scheme.')
    d.helpful(99, ['O3'], [(65, 123)],
              'Provides a bounded observation fixture construction path; relation construction can consume already established analyses and interpretations.')
    d.helpful(100, OBS, [(49, 72)],
              'Gives the concrete resource/content field shape for endpoint provenance; import analysis and interpretation contracts already retain these objects.')
    d.helpful(101, OBS, [(34, 61)],
              'Explains supplied snapshot/resource lookup and failure behavior, helpful for optional validation against explicit state without making one new helper signature mandatory.')
    d.helpful(268, ['O2', 'O3'], [(83, 120)],
              'Tests independent analysis/occurrence retention with duplicate names; useful testing precedent but not an import contract.')
    d.helpful(271, ['O2', 'O3'], [(132, 153)],
              'Provides changed-snapshot and mismatched-resource adversarial fixture patterns for exact source materialization, not a universal import freshness rule.')
    d.helpful(274, ['O2', 'O3'], [(133, 168)],
              'Tests deduplication that retains all original support, useful for duplicate-relation test design without mandating endpoint grouping.')
    d.helpful(277, OBS, [(29, 45), (48, 65)],
              'Concrete import syntax, alias ordering, shared occurrence, nested exclusion, parse failure and explicit selection examples complement U1 but omit its full identity/provenance contract.')
    d.helpful(280, ['O2', 'O3'], [(113, 162), (165, 198)],
              'Module tests demonstrate content dependence, unchanged identity across unrelated snapshot changes, root collisions and duplicate selection rejection. They complement, rather than replace, universe admission evidence.')
    d.helpful(286, OBS, [(92, 106), (153, 182)],
              'Concrete repository/content/address identity tests aid changed-frame test design; endpoint correlation can be obtained from the import/module contracts already required.')
    return d


REQUIRED_UNITS = {
    'O1': ['T0', 'U1', 'U2', 'U4', 'U5', 'U7', 'U8'],
    'O2': ['T0', 'U1', 'U3', 'U4', 'U6', 'U7'],
    'O3': ['T0', 'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8'],
}

GAPS = [
    {'id': 'G1', 'type': 'TASK_INTERPRETATION_GAP', 'obligations': list(OBS),
     'status': 'RESOLVED_WITH_EXPLICIT_QUALIFICATION',
     'description': 'The one-sentence task does not explicitly specify Python, unique-positive module resolution, relative-import rules, provenance fields, duplicate accounting or a testing/documentation matrix. Frozen O1-O3 select a reasonable repository-grounded interpretation; they are not verbatim task entailments.',
     'effect': 'Evaluate all three frozen obligations, but classify their detailed grounding as mixed task/repository support. No extra mandatory obligation was identified.'},
    {'id': 'G2', 'type': 'TASK_GAP', 'obligations': list(OBS),
     'status': 'OPEN_DESIGN_FREEDOM_NOT_UNRESOLVED_CELL',
     'description': 'New type/helper names, exact representation, grouping/order policy for repeated input resolutions, facade destination, and whether malformed/stale/foreign inputs raise or produce a retained nonpositive report are not selected.',
     'effect': 'Require no unsupported positive and inspectable provenance/accounting under an explicit bounded contract. Do not require a child-specific API, a universal stale enum, or a particular file edit.'},
    {'id': 'G3', 'type': 'REPOSITORY_INFORMATION_GAP', 'obligations': ['O1', 'O2', 'O3'],
     'status': 'BOUNDED_LIMITATION_NO_BLOCKING_SUPPORT_GAP',
     'description': 'The parent has declaration, interpretation and resolution primitives, not the requested relation capability or a universal applicability checker. Its resolver does not validate arbitrary fabricated results against a new supplied snapshot. Runtime importability, namespace packages and external-versus-missing truth are outside its information boundary.',
     'effect': 'Absence of the future relation is expected development work, not evidence from a missing historical implementation. No mandatory information unit lacks an in-packet support alternative.'},
]

LIMITATIONS = [
    'Exhaustiveness means all 382 retained packet resources and all three frozen obligations, not resources outside the packet or every possible future implementation.',
    'Minimality is inclusion-minimal information support at the declared semantic-unit granularity, not minimum file count, cheapest disclosure, or a theorem about all imaginable programs.',
    'Tests are alternative behavioral-contract evidence for U2/U4; they were inspected, not executed, and do not prove arbitrary runtime correctness.',
    'Exact source spans are 1-based inclusive line ranges plus 0-based half-open Unicode code-point offsets in native decoded text. They are not AST UTF-8 byte columns.',
    'All resources received content-derived screening and full-text semantic searches; detailed bodies were read for positive and near-positive evidence. This is not a claim that every unrelated method body was read line by line.',
    'Host routing to requested GPT-6 Astra / High was not independently verified. No model selection or provider introspection was performed.',
    'Packet source_head/source_tree and native parent discussions of earlier lexical benchmarks were encountered as supplied data; no history or treatment metadata was obtained, and those numbers did not determine judgments.',
    'Deterministic validation proves framing, completeness and consistency with encoded decisions, not semantic correctness by itself. There is exactly one human-facing primary model judgment and one same-reviewer self-review.',
]

BLINDNESS = {
    'designation': 'sole clean treatment-blind primary',
    'requested_model': 'GPT-6 Astra', 'requested_reasoning': 'High',
    'host_routing_independently_verified': False,
    'evidence_scope': 'five original packet files inside the sterile workspace only',
    'outside_workspace_evidence_accessed': [],
    'excluded_external_categories_accessed': [],
    'repository_checkout_accessed': False, 'git_or_history_accessed': False,
    'historical_child_accessed': False, 'changed_paths_or_child_diff_accessed': False,
    'other_case_or_prior_session_accessed': False, 'web_accessed': False,
    'acquisition_queries_needs_ranks_scores_accessed': False,
    'structural_annotations_or_reference_treatment_accessed': False,
    'evaluator_implementation_accessed': False,
    'confirmation_or_reserve_accessed': False,
    'second_reviewer': False, 'reconciliation': False,
    'native_packet_metadata_encountered': ['parent_frame.source_head', 'parent_frame.source_tree'],
    'native_repository_content_caveat': 'Earlier benchmark prose/numbers and ordinary query/ranking code are unchanged parent content, not external treatment evidence; no effectiveness inference uses them.',
    'packet_validator_used': 'validate_packet.py authenticates inputs only; it supplies no adjudication or evaluator gold.',
    'tools_used': 'Local PowerShell/Python standard-library inspection and authored deterministic builders; no resource source code executed.',
    'initial_exact_five_check': 'PASS; no .git, .local, extras, directories, symlinks, junctions or reparse points.',
    'initial_validator_result': 'PASS; NO ADJUDICATION',
}


def subject(resource):
    if resource['address'].endswith('.py'):
        doc = ast.get_docstring(ast.parse(resource['content'])) or 'Python module without a descriptive module docstring'
        return doc.splitlines()[0]
    return next((s.lstrip('# ').strip() for s in resource['content'].splitlines() if s.startswith('#')), 'Project build and validation configuration')


def intersection(sets):
    return sorted(set.intersection(*(set(s) for s in sets))) if sets else []


def make_review(packet):
    d = semantic_decisions(packet)
    units = {u['id']: u for u in d.units}
    witnesses = {}
    for ob in OBS:
        choices = [[a['resources'] for a in units[uid]['minimal_support_alternatives']] for uid in REQUIRED_UNITS[ob]]
        witnesses[ob] = combine(choices)
    obligation_results = []
    for frozen in packet['obligations']:
        ob = frozen['id']
        detailed = []
        for i, resources in enumerate(witnesses[ob], 1):
            proofs = {uid: [a['id'] for a in units[uid]['minimal_support_alternatives']
                            if set(a['resources']) <= set(resources)] for uid in REQUIRED_UNITS[ob]}
            detailed.append({'id': f'{ob}.W{i:03d}', 'resources': resources,
                             'units': REQUIRED_UNITS[ob], 'all_available_support_alternatives': proofs})
        obligation_results.append({
            **frozen, 'classification': 'MIXED',
            'task_backed_component': 'Adding qualified repository import relations is the explicit task goal.',
            'repository_supported_component': 'Python/module boundaries, current contracts, identity/applicability and integration constraints come from retained parent evidence.',
            'normative_scope': 'Frozen satisfaction/exclusions retained; not asserted to be literal task wording.',
            'required_units': REQUIRED_UNITS[ob],
            'minimal_complete_unit_witnesses': [REQUIRED_UNITS[ob]],
            'all_minimal_complete_resource_witnesses': detailed,
            'indispensable_resources': intersection(witnesses[ob]),
            'indispensable_units': REQUIRED_UNITS[ob],
            'task_only_complete_witness': False,
            'blocking_information_gap': False,
        })
    cells = []
    resources = []
    for number, native in enumerate(packet['resources'], 1):
        rid = resource_id(number)
        resources.append({k: v for k, v in native.items() if k != 'content'} | {
            'id': rid, 'content_subject': subject(native),
            'screening': 'Content-derived subject/definitions/headings and complete-content semantic search; positive/near-positive spans inspected.',
        })
        for ob in OBS:
            in_witnesses = [w['id'] for o in obligation_results if o['id'] == ob
                            for w in o['all_minimal_complete_resource_witnesses'] if rid in w['resources']]
            supplied_units, evidence = [], set()
            for uid in REQUIRED_UNITS[ob]:
                for alt in units[uid]['minimal_support_alternatives']:
                    if rid in alt['resources']:
                        supplied_units.append(uid)
                        evidence.update(e for e in alt['evidence'] if d.evidence[e]['resource_id'] == rid)
            help_record = d.help.get((rid, ob))
            if help_record:
                evidence.update(help_record['evidence'])
            if in_witnesses:
                label = 'REQUIRED'
                rationale = ('Contributes necessary information ' + ', '.join(sorted(set(supplied_units))) +
                             ' in at least one minimal complete ' + ob + ' witness. Necessity is informational; individual indispensability is assessed separately.')
            elif supplied_units or help_record:
                label = 'HELPFUL_ONLY'
                rationale = help_record['rationale'] if help_record else (
                    'Supports ' + ', '.join(sorted(set(supplied_units))) +
                    ', but that contribution is redundant in every minimal complete ' + ob +
                    ' witness. Corroboration is useful without making this resource required.')
            else:
                label = 'UNNECESSARY'
                target = {'O1': 'positive import-module relation and endpoint provenance',
                          'O2': 'bounded import dispositions, applicability and duplicate accounting',
                          'O3': 'import/module integration, bounded documentation and behavior validation'}[ob]
                rationale = ('Content concerns: ' + subject(native) + ' It supplies no necessary unit or specific implementation aid for ' +
                             target + '. General coding patterns, ordinary import use sites and package proximity do not establish necessity.')
            cells.append({
                'resource_id': rid, 'address': native['address'],
                'document_identity': native['document_identity'], 'content_identity': native['content_identity'],
                'obligation_id': ob, 'obligation_identity': {'task': packet['task_identity'], 'value': ob},
                'judgment': label, 'rationale': rationale,
                'supported_required_units': sorted(set(supplied_units)),
                'positive_evidence': sorted(evidence),
                'minimal_witness_membership': in_witnesses,
                'indispensable_for_obligation': rid in intersection(witnesses[ob]),
                'decision_status': 'RESOLVED',
            })
    combinations = []
    witness_lists = [o['all_minimal_complete_resource_witnesses'] for o in obligation_results]
    for i, items in enumerate(itertools.product(*witness_lists), 1):
        combinations.append({
            'id': f'TC{i:04d}', 'obligation_witnesses': [w['id'] for w in items],
            'resource_union': sorted(set().union(*(set(w['resources']) for w in items))),
            'unit_union': sorted(set().union(*(set(w['units']) for w in items))),
        })
    task_minimal = minimal(c['resource_union'] for c in combinations)
    distinct_unions = sorted({tuple(c['resource_union']) for c in combinations}, key=lambda s: (len(s), s))
    return {
        'schema': 'stage-c-clean-primary-semantic-review-v1',
        'case_id': packet['case_id'], 'task_identity': packet['task_identity'],
        'task_text': packet['task_text'], 'parent_frame': packet['parent_frame'],
        'original_packet_sha256': ORIGINAL_HASHES, 'canonical_payload_sha256': PAYLOAD_HASH,
        'definitions': {
            'REQUIRED': 'Occurs in at least one inclusion-minimal complete information witness for this obligation.',
            'HELPFUL_ONLY': 'Concrete useful partial/redundant support or implementation/validation context, but no membership in a minimal complete witness.',
            'UNNECESSARY': 'No necessary information or concrete obligation-specific aid found in this retained resource.',
            'indispensability': 'Intersection of every minimal complete witness; differs from REQUIRED.',
            'minimal_support': 'All adjudicated resource alternatives for the exact stated unit; each alternative is conjunctive, alternatives disjunctive. Evidence spans jointly explain that support.',
            'scope_of_exhaustiveness': 'All alternatives judged in this retained frame under the explicitly declared semantic granularity, not unconstrained future program synthesis.',
        },
        'resources': resources, 'obligations': obligation_results,
        'semantic_units': d.units, 'evidence_spans': sorted(d.evidence.values(), key=lambda e: e['id']),
        'semantic_compositions': [
            {'id': 'M' + ob[1:], 'classification': 'MIXED', 'obligation_id': ob,
             'premise_units': REQUIRED_UNITS[ob],
             'inference': 'The task goal plus these descriptive parent contracts supports the frozen desired behavior; the repository alone does not issue this development task.'}
            for ob in OBS
        ],
        'cells': cells,
        'task_analysis': {
            'task_backed_goal_repository_witnesses': [[]],
            'task_backed_goal_units': ['T0'],
            'task_empty_witness_scope': 'The task sentence alone supplies T0. The empty repository witness does not discharge any complete frozen obligation.',
            'all_complete_obligation_witness_combinations': combinations,
            'all_distinct_sufficient_resource_unions': [list(s) for s in distinct_unions],
            'all_minimal_sufficient_resource_unions': task_minimal,
            'all_minimal_sufficient_unit_unions': [sorted(units)],
            'indispensable_resources': intersection(task_minimal),
            'indispensable_units': sorted(units),
            'sufficiency_closure': 'Every superset within the retained frame of a listed minimal sufficient resource union is information-sufficient; no unlisted proper subset is sufficient under these units.',
        },
        'frozen_interpretation_gaps': packet['interpretation_gaps'],
        'frozen_ambiguities': packet['ambiguities'],
        'interpretation_completeness_challenge': 'O1-O3 cover the capability, qualification and integration/validation. No fourth mandatory requirement is justified. Test-case categories and exact provenance prescriptions are the frozen repository-informed interpretation, not all literal requirements of the task sentence.',
        'gaps': GAPS, 'limitations': LIMITATIONS,
        'unresolved_decisions': [], 'blindness_attestation': BLINDNESS,
        'same_reviewer_self_review': SELF_REVIEW,
    }


def brute_witnesses(unit_ids, units):
    """Independent powerset coverage check, not the incremental union builder."""
    alternatives = [[set(a['resources']) for a in units[u]['minimal_support_alternatives']] for u in unit_ids]
    candidates = sorted(set().union(*(a for choices in alternatives for a in choices)))
    found = []
    for size in range(len(candidates) + 1):
        for choice in itertools.combinations(candidates, size):
            chosen = set(choice)
            if any(set(previous) <= chosen for previous in found):
                continue
            if all(any(a <= chosen for a in choices) for choices in alternatives):
                found.append(list(choice))
    return found


def validate_review(review, packet):
    require(review['parent_frame'] == packet['parent_frame'], 'Review frame')
    require(review['task_text'] == packet['task_text'] and review['task_identity'] == packet['task_identity'], 'Review task')
    resources = {r['id']: r for r in review['resources']}
    expected_ids = {resource_id(i) for i in range(1, 383)}
    require(len(review['resources']) == 382 and set(resources) == expected_ids, 'Resource inventory')
    for i, native in enumerate(packet['resources'], 1):
        retained = resources[resource_id(i)]
        require(all(retained[k] == v for k, v in native.items() if k != 'content'), 'Native identity mismatch')
    require([o['id'] for o in review['obligations']] == list(OBS), 'Obligation inventory')
    for original, ob in zip(packet['obligations'], review['obligations'], strict=True):
        require(all(ob[k] == v for k, v in original.items()), 'Frozen obligation changed')
    expected_pairs = {(rid, ob) for rid in expected_ids for ob in OBS}
    pairs = [(c['resource_id'], c['obligation_id']) for c in review['cells']]
    require(len(pairs) == 1146 and len(set(pairs)) == 1146, 'Duplicate/missing cells')
    require(set(pairs) == expected_pairs, 'Unexpected/missing cells')
    require(not review['unresolved_decisions'], 'Unresolved decisions')
    evidence = {e['id']: e for e in review['evidence_spans']}
    require(len(evidence) == len(review['evidence_spans']), 'Duplicate evidence')
    for e in evidence.values():
        require(e['resource_id'] in resources, 'Foreign evidence resource')
        native = packet['resources'][int(e['resource_id'][1:]) - 1]
        require(all(e[k] == native[k] for k in ('address', 'document_identity', 'content_identity')), 'Evidence identity')
        start, end = e['start_character_0based'], e['end_character_0based_exclusive']
        require(0 <= start < end <= len(native['content']), 'Evidence offset')
        require(native['content'][start:end] == e['quote'], 'Exact quote mismatch')
        lines = native['content'].splitlines(keepends=True)
        lo, hi = e['start_line_1based'], e['end_line_1based_inclusive']
        require(1 <= lo <= hi <= len(lines), 'Line bounds')
        require(start == sum(map(len, lines[:lo - 1])) and end == sum(map(len, lines[:hi])), 'Line/offset mismatch')
        require(e['quote_utf8_sha256'] == sha(e['quote'].encode('utf-8')), 'Quote hash')
    units = {u['id']: u for u in review['semantic_units']}
    require(len(units) == 9 and set(units) == {'T0', *(f'U{i}' for i in range(1, 9))}, 'Unit inventory')
    for u in units.values():
        choices = u['minimal_support_alternatives']
        require(bool(choices), 'Unsupported unit')
        sets = [a['resources'] for a in choices]
        require(len(sets) == len({tuple(s) for s in sets}), 'Duplicate support alternative')
        require({tuple(s) for s in sets} == {tuple(s) for s in minimal(sets)}, 'Nonminimal support alternative')
        for a in choices:
            require(set(a['resources']) <= expected_ids, 'Foreign alternative')
            require(set(a['evidence']) <= evidence.keys(), 'Missing alternative evidence')
            require(set(a['resources']) == {evidence[e]['resource_id'] for e in a['evidence']}, 'Alternative evidence coverage')
            if a['task_span'] is not None:
                t = a['task_span']
                require(packet['task_text'][t['start_character_0based']:t['end_character_0based_exclusive']] == t['quote'], 'Task quote')
            else:
                require(bool(a['resources']), 'Invented empty repository support')
    obligation_witnesses = {}
    for ob in review['obligations']:
        expected = brute_witnesses(ob['required_units'], units)
        actual = [w['resources'] for w in ob['all_minimal_complete_resource_witnesses']]
        require(actual == expected, 'Missing/nonminimal complete witness: ' + ob['id'])
        require(ob['indispensable_resources'] == intersection(expected), 'Obligation indispensability')
        require(ob['minimal_complete_unit_witnesses'] == [REQUIRED_UNITS[ob['id']]], 'Unit witness')
        obligation_witnesses[ob['id']] = ob['all_minimal_complete_resource_witnesses']
        for w in ob['all_minimal_complete_resource_witnesses']:
            for uid in ob['required_units']:
                available = [a['id'] for a in units[uid]['minimal_support_alternatives'] if set(a['resources']) <= set(w['resources'])]
                require(w['all_available_support_alternatives'][uid] == available, 'Witness support proof')
    for c in review['cells']:
        rid, ob = c['resource_id'], c['obligation_id']
        r = resources[rid]
        require(all(c[k] == r[k] for k in ('address', 'document_identity', 'content_identity')), 'Cell native identity')
        require(c['obligation_identity'] == {'task': packet['task_identity'], 'value': ob}, 'Cell obligation identity')
        require(c['judgment'] in {'REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY'}, 'Invalid judgment')
        require(c['decision_status'] == 'RESOLVED' and bool(c['rationale'].strip()), 'Unresolved/empty rationale')
        memberships = [w['id'] for w in obligation_witnesses[ob] if rid in w['resources']]
        require(c['minimal_witness_membership'] == memberships, 'Cell witness membership')
        require((c['judgment'] == 'REQUIRED') == bool(memberships), 'Necessity label inconsistent')
        require(bool(c['positive_evidence']) == (c['judgment'] != 'UNNECESSARY'), 'Positive span completeness')
        for e in c['positive_evidence']:
            require(e in evidence and evidence[e]['resource_id'] == rid, 'Cell span ownership')
    task = review['task_analysis']
    expected_combinations = list(itertools.product(*(obligation_witnesses[ob] for ob in OBS)))
    require(len(task['all_complete_obligation_witness_combinations']) == len(expected_combinations), 'Missing task combinations')
    for actual, combination in zip(task['all_complete_obligation_witness_combinations'], expected_combinations, strict=True):
        require(actual['obligation_witnesses'] == [w['id'] for w in combination], 'Task combination identity')
        require(actual['resource_union'] == sorted(set().union(*(set(w['resources']) for w in combination))), 'Task resource union')
        require(actual['unit_union'] == sorted(set().union(*(set(w['units']) for w in combination))), 'Task unit union')
    task_expected = brute_witnesses(sorted(units), units)
    require(task['all_minimal_sufficient_resource_unions'] == task_expected, 'Task minimal unions')
    require(task['indispensable_resources'] == intersection(task_expected), 'Task indispensability')
    require(task['all_minimal_sufficient_unit_unions'] == [sorted(units)], 'Task unit unions')
    require(task['task_backed_goal_repository_witnesses'] == [[]], 'Task-empty witness lost')
    # Exact semantic specification comparison also detects edits to rationale or
    # support alternatives that structural tests cannot independently adjudicate.
    require(review == make_review(packet), 'Encoded primary semantic decision differs')
    return {'status': 'PASS', 'expected_cells': 1146, 'actual_cells': len(pairs),
            'duplicates': 0, 'missing': 0, 'unexpected': 0, 'unresolved': 0,
            'native_identities': 'PASS', 'positive_spans': 'PASS',
            'support_alternative_antichains': 'PASS',
            'all_minimal_witnesses_independent_powerset_check': 'PASS',
            'indispensability_and_all_task_combinations': 'PASS',
            'encoded_primary_decisions': 'PASS'}


def statistics(review):
    cells = review['cells']
    labels = ['REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY']
    global_counts = Counter(c['judgment'] for c in cells)
    per_ob = {ob: {label: sum(c['obligation_id'] == ob and c['judgment'] == label for c in cells)
                   for label in labels} for ob in OBS}
    return {
        'case_id': review['case_id'], 'resources': 382, 'mandatory_obligations': 3,
        'complete_cells': 1146, 'duplicates': 0, 'missing': 0, 'unexpected': 0, 'unresolved': 0,
        'cell_counts': {label: global_counts[label] for label in labels}, 'per_obligation': per_ob,
        'unique_resources_by_any_cell_label': {label: len({c['resource_id'] for c in cells if c['judgment'] == label}) for label in labels},
        'resources_with_all_cells_unnecessary': sum(all(c['judgment'] == 'UNNECESSARY' for c in cells if c['resource_id'] == r['id']) for r in review['resources']),
        'base_semantic_units': len(review['semantic_units']),
        'base_unit_classifications': dict(Counter(u['classification'] for u in review['semantic_units'])),
        'mixed_semantic_compositions': len(review['semantic_compositions']),
        'positive_evidence_spans': len(review['evidence_spans']),
        'support_alternative_counts': {u['id']: len(u['minimal_support_alternatives']) for u in review['semantic_units']},
        'minimal_complete_witness_counts': {o['id']: len(o['all_minimal_complete_resource_witnesses']) for o in review['obligations']},
        'obligation_indispensable_resources': {o['id']: o['indispensable_resources'] for o in review['obligations']},
        'task_combination_count': len(review['task_analysis']['all_complete_obligation_witness_combinations']),
        'distinct_sufficient_resource_union_count': len(review['task_analysis']['all_distinct_sufficient_resource_unions']),
        'minimal_sufficient_resource_union_count': len(review['task_analysis']['all_minimal_sufficient_resource_unions']),
        'task_indispensable_resources': review['task_analysis']['indispensable_resources'],
        'task_indispensable_units': review['task_analysis']['indispensable_units'],
        'gap_counts': dict(Counter(g['type'] for g in review['gaps'])),
        'effectiveness_interpretation': 'DEFERRED; no cross-cohort or structural-discrimination conclusion',
    }


def adversarial_mutations(review, packet):
    cases = []
    def trial(name, change):
        mutant = copy.deepcopy(review)
        change(mutant)
        try:
            validate_review(mutant, packet)
        except (ValueError, KeyError, IndexError, TypeError) as error:
            cases.append({'mutation': name, 'result': 'REJECTED', 'detector': str(error)})
        else:
            raise ValueError('Mutation escaped: ' + name)
    trial('delete one cell', lambda r: r['cells'].pop())
    trial('duplicate a cell replacing another', lambda r: r['cells'].__setitem__(1, copy.deepcopy(r['cells'][0])))
    trial('foreign resource cell', lambda r: r['cells'][0].__setitem__('resource_id', 'R999'))
    trial('foreign obligation cell', lambda r: r['cells'][0].__setitem__('obligation_id', 'O4'))
    trial('unresolved decision', lambda r: r['cells'][0].__setitem__('decision_status', 'UNRESOLVED'))
    trial('wrong snapshot frame', lambda r: r['parent_frame'].__setitem__('snapshot_id', '0' * 64))
    trial('wrong native content identity', lambda r: r['cells'][0].__setitem__('content_identity', '0' * 64))
    trial('changed frozen obligation', lambda r: r['obligations'][0].__setitem__('requirement', 'Resolve runtime dependencies'))
    trial('fabricated positive quote', lambda r: r['evidence_spans'][0].__setitem__('quote', 'invented'))
    trial('off-by-one exact span', lambda r: r['evidence_spans'][0].__setitem__('start_character_0based', r['evidence_spans'][0]['start_character_0based'] + 1))
    trial('promote unrelated resource by proximity', lambda r: next(c for c in r['cells'] if c['resource_id'] == 'R093' and c['obligation_id'] == 'O1').__setitem__('judgment', 'REQUIRED'))
    trial('drop alternative support', lambda r: r['semantic_units'][2]['minimal_support_alternatives'].pop())
    trial('invent task-empty support for repository unit', lambda r: r['semantic_units'][1]['minimal_support_alternatives'][0].update(resources=[], evidence=[]))
    trial('omit a minimal witness', lambda r: r['obligations'][0]['all_minimal_complete_resource_witnesses'].pop())
    trial('inflate a minimal witness', lambda r: r['obligations'][0]['all_minimal_complete_resource_witnesses'][0]['resources'].append('R093'))
    trial('invent obligation indispensability', lambda r: r['obligations'][0]['indispensable_resources'].append('R093'))
    trial('omit task witness combination', lambda r: r['task_analysis']['all_complete_obligation_witness_combinations'].pop())
    trial('corrupt sufficient union', lambda r: r['task_analysis']['all_minimal_sufficient_resource_unions'][0].append('R093'))
    trial('invent task indispensability', lambda r: r['task_analysis']['indispensable_resources'].append('R093'))
    trial('remove task-empty goal witness', lambda r: r['task_analysis'].__setitem__('task_backed_goal_repository_witnesses', []))
    trial('forge routing verification', lambda r: r['blindness_attestation'].__setitem__('host_routing_independently_verified', True))
    return cases


METHOD = '''# Stage C primary method

The five original packet files were authenticated before any output existed. The initial validator returned PASS; NO ADJUDICATION, and all expected digests, identities and counts matched. After outputs exist, the builder authenticates those five files separately; it does not weaken or edit the original exact-five validator.

The reviewer used only the sterile packet. Native resource source code was not executed. Content-derived module docstrings, declarations/test names, Markdown headings and full-content searches screened every retained resource; detailed inspection established exact positive and near-positive evidence. Negative judgments are explicit cells with resource-specific content subjects, not an unreviewed directory exclusion. Generic import statements in consumers, likely edits, direct/indirect package proximity and historical developer behavior are not relevance gold.

T0 is the task-backed goal and has an empty repository support witness. U1-U8 describe current parent contracts. M1-M3 are mixed task/repository inferences for the frozen obligations. Frozen satisfaction criteria are retained without pretending the one-sentence task literally stated all their details. TASK_INTERPRETATION_GAP, TASK_GAP and REPOSITORY_INFORMATION_GAP records preserve specification freedom and epistemic limits. No unsupported capability or child API was invented to close a gap.

An information unit is a coherent semantic contract, not a token or an entire file by default. Each listed support alternative is a minimal conjunctive resource set; alternatives are disjunctive. All positive evidence has exact native text, half-open Unicode character offsets, inclusive line coordinates, document/content identity and quote hash. Task evidence is kept separately from repository evidence.

For an obligation, a resource set is complete when it contains at least one support alternative for every required unit. Enumerate all alternatives, union their resources and remove proper supersets. REQUIRED is membership in at least one resulting minimal complete witness. HELPFUL_ONLY is useful partial/redundant support or a concrete integration/test aid outside that witness union. UNNECESSARY supplies neither. Indispensable resources are the intersection of all minimal witnesses, not all REQUIRED resources. Unit indispensability is relative to the declared non-substitutable contract decomposition. No claim is made that every future implementation must read these literal files.

Task sufficiency enumerates the Cartesian product of all obligation witnesses, retains every complete combination and its resource/unit unions, and separately records distinct and inclusion-minimal sufficient unions. All supersets of minimal unions within this fixed frame are represented by an explicit monotone closure rule. The task-backed empty witness supplies only the task goal, not a complete frozen obligation.

The builder serializes the primary's explicit semantic choices. It does not perform a second semantic adjudication. An independent powerset coverage routine checks complete witness enumeration and minimality. Validation checks all 1,146 cells, exact identities/spans, alternatives, provenance, unit coverage, indispensability and task unions. Representative in-memory adversarial mutations must be rejected. The original packet is never mutated for testing. Equality against the encoded primary additionally detects arbitrary changes to judgments/rationales; that check is tamper/consistency detection, not independent proof of semantic truth.

One same-reviewer self-review challenges grounding, redundant alternatives, boundary cases, edit/proximity bias, stale-versus-changed state and every label. No second reviewer or reconciliation participates. The final build computes outputs in memory, invokes the same builder in a separate Python process in .scratch/replay, compares every scientific output byte-for-byte, and only then writes final root outputs. The child process is deterministic replay, not another reviewer. Checks use standard-library tooling, no repository checkout, package installation, history, web or external evidence.

stage_c_hashes.json freezes the five original files, builder and five generated scientific report/data files. The hashes sidecar excludes itself to avoid self-reference; the final .local/codex-result.md is a byte-identical mirror of STAGE_C_REVIEW.md and has the same hash. Scratch files are operational ledger/replay artifacts, not scientific inputs. No timestamp or absolute host path enters generated scientific outputs. .local is created only after adjudication, self-review, validation, replay, hash freeze and original-packet preservation checks pass.

Replay: `python -B stage_c_builder.py --build`. Verification without rewriting scientific output: `python -B stage_c_builder.py --verify`. The builder and packet are sufficient to reconstruct the scientific outputs; .scratch is not needed as input. Files must remain inside this sterile workspace. The initial exact-five validator is intentionally not rerun against an output-populated root.

Requested designation is GPT-6 Astra / High. Host routing is not independently verified. Scientific validity remains conditional on the disclosed single-reviewer semantic judgments and the frozen interpretation. No structural-discrimination effectiveness conclusion is drawn before other independently blinded cohort primaries are available.
'''


def markdown(review, stats):
    lines = ['# Case 0018 — treatment-blind primary semantic adjudication', '',
             'Task: **Implement qualified repository import relations**.', '',
             'Designated reviewer: **GPT-6 Astra / High**, sole primary. Host routing was not independently verified. No second reviewer or reconciliation.', '',
             'Authentication: **PASS; NO ADJUDICATION** before any file creation. The initial root contained exactly the five authorized regular files and no reparse points or extra entries. Original packet bytes are preserved.', '',
             '**1,146 / 1,146 cells resolved**: duplicates 0; missing 0; unexpected 0; unresolved 0.', '',
             '| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY | Minimal witnesses |',
             '|---|---:|---:|---:|---:|']
    for ob in OBS:
        c = stats['per_obligation'][ob]
        lines.append(f"| {ob} | {c['REQUIRED']} | {c['HELPFUL_ONLY']} | {c['UNNECESSARY']} | {stats['minimal_complete_witness_counts'][ob]} |")
    lines += ['', f"Total cells: {stats['cell_counts']}. Resources unnecessary for all obligations: {stats['resources_with_all_cells_unnecessary']}.", '',
              'REQUIRED means membership in at least one minimal complete information witness; it does not mean every solution needs that particular resource. HELPFUL_ONLY is concrete assistance or redundant support. Indispensability is reported separately.', '',
              '## Interpretation and findings', '',
              'The parent already has direct import declarations, explicit-root module interpretations and qualified bounded resolution. It explicitly does not yet establish repository dependency relations. The requested capability can compose those facts into directed source-to-target relations without asserting runtime imports, imported-member binding, root precedence, reverse edges or external dependency truth.', '',
              'The original task sentence supplies the goal. Detailed O1-O3 prescriptions are the frozen repository-informed interpretation. Documentation/exposure and test categories are evaluated as frozen criteria; no particular new API name, implementation file or facade edit is mandatory.', '',
              'Source provenance and semantic identity must remain distinct. Repeated aliases can share a source span while retaining different ordinals. Universes reject repeated interpretation identities but preserve colliding dotted names. Universe identity ignores supplied order. Unrelated snapshot changes do not automatically make semantic knowledge stale; incompatible consumed state must not silently become a positive relation.', '',
              '## Frozen obligations', '']
    for o in review['obligations']:
        lines += [f"- **{o['id']} — {o['requirement']}** {o['satisfaction']} Excluded: {o['excluded_interpretation']} Classification: MIXED."]
    lines += ['', '## Semantic units and all minimal support alternatives', '',
              'Alternative brackets are conjunctive resource sets; “or” separates alternatives. Exact quotations, native identities and all support-span links are in stage_c_review.json. T0 requires no repository disclosure.', '']
    for u in review['semantic_units']:
        alternatives = ' or '.join('[' + ', '.join(a['resources']) + ']' for a in u['minimal_support_alternatives'])
        lines += [f"- **{u['id']} ({u['classification']})**: {u['statement']} Supports: {alternatives}. {u['necessity_rationale']}"]
    lines += ['', 'M1-M3 are the mixed compositions of T0 and repository units for O1-O3; they are not additional independent evidence.', '', '## Every minimal complete witness and indispensability', '']
    for o in review['obligations']:
        lines += [f"**{o['id']}**. Required unit witness: {', '.join(o['required_units'])}. Indispensable resources: {', '.join(o['indispensable_resources']) or 'none'}.", '']
        for w in o['all_minimal_complete_resource_witnesses']:
            lines.append(f"- {w['id']}: {', '.join(w['resources'])}")
        lines.append('')
    task = review['task_analysis']
    lines += [f"Task-level complete combinations: **{stats['task_combination_count']}**; distinct sufficient resource unions: **{stats['distinct_sufficient_resource_union_count']}**; minimal sufficient unions: **{stats['minimal_sufficient_resource_union_count']}**.", '',
              f"Task indispensable resources: **{', '.join(task['indispensable_resources'])}**. Task indispensable base units: {', '.join(task['indispensable_units'])}.", '',
              'All task-minimal resource unions:', '']
    lines.extend('- ' + ', '.join(s) for s in task['all_minimal_sufficient_resource_unions'])
    lines += ['', 'The empty resource witness supports T0 only. No full frozen obligation has an empty resource witness. Every complete combination and its unit/resource union is enumerated in the JSON and in the appendix below.', '', '## Gaps, ambiguity and limitations', '']
    for g in review['gaps']:
        lines += [f"- **{g['type']} ({g['id']})**: {g['description']} {g['effect']} Status: {g['status']}."]
    lines += ['', 'Frozen ambiguities: ' + ' '.join(review['frozen_ambiguities']), '']
    lines.extend('- ' + value for value in LIMITATIONS)
    lines += ['', '## Same-reviewer self-review', '',
              f"Status: {SELF_REVIEW['status']}; passes: {SELF_REVIEW['passes']}. No second reviewer or reconciliation.", '']
    lines.extend('- ' + value for value in SELF_REVIEW['checks'])
    lines.extend('- Correction: ' + value for value in SELF_REVIEW['corrections'])
    lines += ['', '## Deterministic validation and preservation', '',
              'The final build requires exact native frame/identity and cell coverage checks, exact span/quote checks, independent powerset witness enumeration, task-combination/union checks, representative adversarial rejection, separate-process exact byte replay, frozen hashes and post-write original-packet hash checks. See stage_c_validation.json and stage_c_hashes.json for the machine-readable results.', '',
              'Scientific outputs: stage_c_review.json; stage_c_statistics.json; STAGE_C_REVIEW.md; stage_c_validation.json; stage_c_hashes.json; stage_c_method.md; stage_c_builder.py. The persistent .scratch ledger records the work. .local/codex-result.md is created only after all final gates pass and contains this same complete report byte-for-byte.', '',
              'Original SHA-256 hashes:', '']
    lines.extend(f'- {name}: `{digest}`' for name, digest in sorted(ORIGINAL_HASHES.items()))
    lines += ['', f'Canonical payload SHA-256: `{PAYLOAD_HASH}`.', '',
              'Frame:', '']
    lines.extend(f'- {key}: `{value}`' for key, value in FRAME.items())
    lines += ['', '## Full blindness attestation', '',
              'Only the five original files in this sterile workspace supplied evidence. No repository checkout, Git/history, parent/sibling directory, prior session, other case, acquisition queries/needs/ranks/scores, structural annotations, Reference treatment pairs/counts/timings, evaluator implementation, historical child implementation, changed paths/diff, prior gold, confirmation, reserve, web or external-provider answers were accessed. No delegated reviewer or reconciliation was used.', '',
              'The authenticated packet itself exposed source_head/source_tree values and unchanged natural repository text about earlier benchmarks. Those were not used to access history or infer treatment effectiveness. The packet validator authenticates data only. Standard-library execution and deterministic child-process replay are tooling, not outside evidence or additional reviewers. Requested model/reasoning is recorded; host routing was not independently verified.', '',
              '## Complete cell ledger', '',
              'Each resource appears below with all three judgments. Native identities, rationales and exact evidence are also retained in machine-readable form. R = REQUIRED; H = HELPFUL_ONLY; U = UNNECESSARY.', '',
              '| Resource | Native address | O1 | O2 | O3 |', '|---|---|---|---|---|']
    for r in review['resources']:
        row = [c for c in review['cells'] if c['resource_id'] == r['id']]
        lines.append('| ' + r['id'] + ' | `' + r['address'] + '` | ' + ' | '.join({'REQUIRED': 'R', 'HELPFUL_ONLY': 'H', 'UNNECESSARY': 'U'}[c['judgment']] for c in row) + ' |')
    lines += ['', '## Cell rationales and exact positive-span references', '']
    for c in review['cells']:
        lines.append(f"- {c['resource_id']} × {c['obligation_id']} — **{c['judgment']}**. {c['rationale']} Evidence: {', '.join(c['positive_evidence']) or 'none'}. Obligation-indispensable: {str(c['indispensable_for_obligation']).lower()}.")
    lines += ['', '## Exact positive spans', '', 'Text is copied from the authenticated native resource, with original Unicode content preserved.', '']
    for e in review['evidence_spans']:
        lines += [f"**{e['id']}** — {e['resource_id']} `{e['address']}` lines {e['start_line_1based']}-{e['end_line_1based_inclusive']}; characters [{e['start_character_0based']}, {e['end_character_0based_exclusive']}); quote SHA-256 `{e['quote_utf8_sha256']}`.", '',
                  '````text', e['quote'].rstrip('\n'), '````', '']
    lines += ['## Every complete task combination', '',
              'All combinations share unit union: ' + ', '.join(task['indispensable_units']) + '.', '',
              '| Combination | Obligation witnesses | Sufficient resource union |', '|---|---|---|']
    for c in task['all_complete_obligation_witness_combinations']:
        lines.append(f"| {c['id']} | {', '.join(c['obligation_witnesses'])} | {', '.join(c['resource_union'])} |")
    lines += ['', '## Every distinct sufficient resource union', '']
    lines.extend('- ' + ', '.join(s) for s in task['all_distinct_sufficient_resource_unions'])
    lines += ['', '## Final next step', '',
              'Import this clean Astra / High primary byte-for-byte.', '',
              'Do NOT inspect the historical child.', '',
              'Wait for the other independently blinded cohort primaries before any structural-discrimination effectiveness interpretation.', '', 'STOP.', '']
    return '\n'.join(lines).encode('utf-8')


def artifacts(packet):
    review = make_review(packet)
    checks = validate_review(review, packet)
    mutations = adversarial_mutations(review, packet)
    stats = statistics(review)
    validation = {
        'schema': 'stage-c-clean-primary-validation-v1', 'case_id': packet['case_id'],
        'status': 'PASS' if SELF_REVIEW['status'] == 'COMPLETE' else 'DRAFT_NOT_FINAL',
        'adjudication_completeness': checks,
        'adversarial_mutations': mutations,
        'adversarial_mutations_rejected': len(mutations),
        'scientific_validation_limit': 'Deterministic consistency/tamper checks are not a second semantic reviewer.',
        'same_reviewer_self_review': SELF_REVIEW,
        'original_packet_preservation': {'status': 'PASS', 'sha256': ORIGINAL_HASHES},
        'separate_process_exact_replay': {
            'status': 'PASS' if SELF_REVIEW['status'] == 'COMPLETE' else 'NOT_FINAL',
            'method': 'The --build controller publishes root outputs only after separate-process reconstruction equals every scientific byte, including a copy of this builder.',
            'comparison': '7 scientific files; no normalization or semantic transformation',
            'publication_scope': 'PASS is a final-root publication assertion; scratch --emit files are candidates until the controller completes the comparison.',
        },
        'hash_freeze': 'stage_c_hashes.json; excludes itself and byte-identical report mirror',
        'local_report_gate': 'Creation is permitted only after --build exits successfully and --verify passes with self-review COMPLETE.',
    }
    outputs = {
        'stage_c_review.json': canonical(review),
        'stage_c_statistics.json': canonical(stats),
        'STAGE_C_REVIEW.md': markdown(review, stats),
        'stage_c_method.md': METHOD.encode('utf-8'),
        'stage_c_validation.json': canonical(validation),
    }
    outputs['stage_c_hashes.json'] = canonical({
        'schema': 'stage-c-clean-primary-hashes-v1',
        'algorithm': 'SHA-256 over exact bytes',
        'original_packet': ORIGINAL_HASHES,
        'canonical_payload_sha256': PAYLOAD_HASH,
        'scientific_files': {name: sha(raw) for name, raw in sorted(outputs.items())} |
                            {'stage_c_builder.py': sha((ROOT / 'stage_c_builder.py').read_bytes())},
        'exclusions': {'stage_c_hashes.json': 'self-reference avoided', '.scratch': 'non-scientific operational artifacts',
                       '.local/codex-result.md': 'must equal STAGE_C_REVIEW.md byte-for-byte'},
    })
    return outputs


def write_outputs(directory, outputs, copy_builder=False):
    safe(directory).mkdir(parents=True, exist_ok=True)
    for name, raw in outputs.items():
        safe(directory / name).write_bytes(raw)
    if copy_builder:
        safe(directory / 'stage_c_builder.py').write_bytes((ROOT / 'stage_c_builder.py').read_bytes())


def verify_existing(packet, outputs):
    for name, raw in outputs.items():
        require(safe(ROOT / name).read_bytes() == raw, 'Scientific byte mismatch: ' + name)
    frozen = json.loads((ROOT / 'stage_c_hashes.json').read_bytes())
    for name, digest in frozen['scientific_files'].items():
        require(sha(safe(ROOT / name).read_bytes()) == digest, 'Frozen scientific hash: ' + name)
    authenticate()
    mirror = ROOT / '.local' / 'codex-result.md'
    if mirror.exists():
        require(safe(mirror).read_bytes() == outputs['STAGE_C_REVIEW.md'], 'Final report mirror changed')


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--build', action='store_true')
    mode.add_argument('--verify', action='store_true')
    mode.add_argument('--emit', type=str)
    args = parser.parse_args()
    packet = authenticate()
    outputs = artifacts(packet)
    if args.emit:
        directory = safe(ROOT / args.emit)
        require(directory.is_relative_to(ROOT / '.scratch'), 'Emit destination must be scratch')
        write_outputs(directory, outputs, copy_builder=True)
        authenticate()
        print('EMIT PASS: deterministic scientific candidate bytes')
    elif args.verify:
        require(SELF_REVIEW['status'] == 'COMPLETE', 'Self-review incomplete')
        verify_existing(packet, outputs)
        print('VERIFY PASS: 1146 cells; original packet and frozen scientific bytes intact')
    else:
        require(SELF_REVIEW['status'] == 'COMPLETE' and SELF_REVIEW['passes'] == 1, 'Exactly one completed same-reviewer pass required')
        replay = safe(ROOT / '.scratch' / 'replay')
        child = subprocess.run([sys.executable, '-B', str(ROOT / 'stage_c_builder.py'), '--emit', '.scratch/replay'],
                               cwd=ROOT, capture_output=True, check=False)
        require(child.returncode == 0, 'Separate-process replay failed: ' + child.stderr.decode('utf-8', errors='replace'))
        for name, raw in outputs.items():
            require((replay / name).read_bytes() == raw, 'Separate-process byte mismatch: ' + name)
        require((replay / 'stage_c_builder.py').read_bytes() == (ROOT / 'stage_c_builder.py').read_bytes(), 'Builder replay byte mismatch')
        authenticate()
        write_outputs(ROOT, outputs)
        verify_existing(packet, outputs)
        safe(ROOT / '.scratch' / 'replay_receipt.json').write_bytes(canonical({
            'status': 'PASS', 'separate_process_exit_code': child.returncode,
            'files_compared': sorted([*outputs, 'stage_c_builder.py']),
            'all_exact_bytes_equal': True, 'packet_preservation_after_publication': 'PASS',
            'scientific_hash_manifest_sha256': sha(outputs['stage_c_hashes.json']),
        }))
        print('BUILD PASS: adjudication, self-review, validation, 21 mutations, separate-process exact replay, hash freeze, packet preservation')


if __name__ == '__main__':
    main()
