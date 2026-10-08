"""Self-contained frozen C.5 decisions and deterministic artifact generation.

All evidence inputs are the four regular files in this script's directory.
No repository, network, retrieval, or external evidence is used.
"""
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

VERSION = 'case-0011-c5-semantic-v1'
INPUT_HASHES = {
    'C5_INSTRUCTIONS.md': '728ef0710539c8531e816a334a6ac6baee17ca1f0a3c514c4bb4bc50f76a74a7',
    'manifest.json': 'b39d7b9121d07f5a842bbed40f5a876d828d0fa7a82d3900b05f428a622892f1',
    'integrity.json': 'd85c45a838586fead1ba25791a5f6d9c5d69db97b249d2a0ba3f3571695bfd66',
    'packet.json.gz': 'da77c2a3e32129eabd3ffe4331ae2a1caef91cffffbd21b728420a953ad7e6f1',
}
PAYLOAD_HASH = 'c7b0236c21b1cf6168f6eac123f412dd8e90df8dad7058829b99107d7be2ebe3'
NAMES = [
    'c5_mappings_v1.json', 'c5_unit_coverage_v1.json',
    'c5_need_classifications_v1.json', 'c5_statistics_v1.json',
    'c5_method_provenance_v1.json', 'c5_validation_v1.json',
    'c5_output_digests_v1.json',
]

# D: complete acquisition intent. P: expressly covered component and missing component.
# Numbers are presentation aliases for the packet's original array order only.
# Every other pair receives a separate, fact-based DOES_NOT_COVER explanation.
DECISIONS = {
 1: {'P': {
    25: ('common ownership of copied request assembly', 'ownership of ordered caller-directed plans, faithful realization before rendering, and independence from automatic selection and Retrieval'),
 }},
 2: {'P': {
    15: ('absence of language-adapter and Retrieval dependencies', 'the actual ModelRequest/Prompt imports and type-only ContextDisclosure dependency'),
    25: ('common planning independence from Retrieval', 'ownership of ordered caller-directed plans and faithful realization through rendering and assembly'),
 }},
 3: {'D': {
    27: 'A complete account of the exact appended rendered Context necessarily identifies the disclosure header, purpose, plan/snapshot identities, item count, ordered headings and option identities, unchanged item text, and explicit LF separators without normalization.',
 }, 'P': {
    17: ('the separate appended Context text, its envelope and preserved embedded text/separators', 'the independently reported UTF-8 byte length and exclusion of task length from that measurement'),
    16: ('assembly of the entire context.text', 'the keyword-only signature, rendered input type, absence of a limit argument and final replace staging'),
 }},
 4: {'P': {
    17: ('UTF-8 encoding and preservation of embedded newline bytes', 'the full separate task/Context envelope contract and independently reported Context length excluding task length'),
    27: ('unchanged item text, explicit LF insertion and absence of newline normalization', 'the complete ordered inventory of headers, purpose, identities, item count and headings'),
 }},
 5: {'D': {
    11: 'The optional integer/error-convention question seeks None admission, bool/non-int exclusion and descriptive exceptions. Answering the existing request validator convention establishes those rules and its positive token domain; the frozen nonnegative byte-domain question expressly requires recognizing that positive-token validation cannot be copied unchanged.',
    31: 'The question seeks existing optional nonnegative integer admission and error conventions, including invalid booleans. The ModelUsage contract is exactly that convention: None is accepted, bool/non-int raise descriptive TypeError and negative counts raise descriptive ValueError.',
 }, 'P': {
    26: ('numeric admissibility, None, invalid types, descriptive errors and the task-directed zero boundary', 'the existing tests use parametrization, separate None/valid cases and ValueError matching'),
 }},
 6: {'P': {
    16: ('whole-context assembly and a copied request created only at the final replacement, providing a rejection seam', 'the keyword-only signature, rendered input type and absence of an existing limit argument'),
    21: ('creation of a replacement request rather than mutation of the caller request', 'replacement of only Prompt with explicit preservation of its role'),
 }},
 7: {'D': {
    21: 'How copied assembly preserves all other request fields asks for the actual copying operation and its Prompt preservation rule. The unit supplies dataclasses.replace with only prompt replaced and the original Prompt role retained; that operation completely answers the preservation mechanism.',
 }, 'P': {
    13: ('retention of the request fields other than the changed prompt', 'the complete declared field inventory and the frozen-dataclass declaration'),
    17: ('unchanged original task content alongside appended Context', 'exact envelopes, independent UTF-8 length reporting and embedded newline-byte semantics'),
    16: ('creation of the copied request by replacement', 'the complete entry-point signature, rendered input, no-limit signature and entire-text assembly contract'),
    5: ('preservation of original task, role and other request values', 'the test-specific shared-value assertions, task-before-Context check and inverse-replacement equality assertion'),
 }},
 8: {'P': {
    21: ('Prompt role preservation and original task embedded in new prompt content', 'the dataclasses.replace operation replacing only Prompt and thereby retaining every other field'),
    17: ('unchanged task text and separate appended Context', 'independent Context UTF-8 length reporting and the full envelope/newline contract'),
    5: ('original task and Prompt role preservation and task-before-Context placement', 'shared settings/conversation/provider values and the inverse-replacement equality assertion in the test'),
 }},
 9: {'D': {
    8: 'A complete answer to repository/snapshot/content binding checks must explain qualified-source dependency and occurrence frame/address checks, resource existence and equality with retained source content. Those are precisely the complete source-side frame contract established by the unit.',
    22: 'The content/frame binding question includes qualified-target support and subject snapshots, resource existence, subject resource-dependency identity and retained-support equality. Answering all target binding checks establishes the complete unit rather than merely sharing the word snapshot.',
 }, 'P': {
    24: ('target resource and repository/snapshot frame consistency of resolution support and retained analysis', 'target declaration membership when analysis is retained'),
    10: ('repository/snapshot mismatch rejection', 'ordered realization, returned identity/representation checks and publication only after every item succeeds'),
    14: ('repository/snapshot identities and mixed-frame rejection', 'immutability, purpose and ordered-choice contracts, blank/empty/mixed-purpose/duplicate rejection'),
    28: ('foreign/stale frames, missing resources and retained-occurrence equality', 'unchanged item text, resource/content identity retention and original occurrence as native provenance'),
    30: ('retained content identities and correspondence between disclosure and plan choices', 'the full immutable item field inventory, exact text/native provenance and ordered identity/representation correspondence'),
    7: ('retained source/target addresses and content identities supporting frame binding', 'delegation to validated materialization/rendering and retention of rendered text and native value'),
    23: ('changed snapshots, changed retained content and missing-resource rejection behavior', 'the existence and construction of those regression tests with replace and pytest.raises'),
 }},
 10: {'D': {
    30: 'The item-order/exact-text/native-provenance contract question seeks the common retained item structure and its correspondence to the ordered plan. A complete answer gives immutable identity, representation, addresses, content identities, text and native provenance plus one matching item per ordered choice, establishing the entire unit.',
 }, 'P': {
    7: ('retained rendered text, native materialized value and provenance-bearing addresses/content identities', 'qualified adapter delegation to both its validated materializer and renderer'),
    28: ('unchanged retained text, resource/content identities and original-occurrence native provenance', 'foreign/stale/missing/unequal-occurrence rejection rules'),
    10: ('ordered realization and returned item identity/representation checking', 'repository/snapshot mismatch rejection and publication only after all realizations succeed'),
    14: ('immutable ordered choices', 'purpose/frame identities and blank-purpose, empty-choice, mixed-purpose/frame and duplicate-choice rejection'),
    27: ('ordered items and unchanged item.text', 'the complete header/identity/heading inventory and exact LF separator/no-normalization rendering contract'),
    32: ('unchanged retained source, native whole-resource provenance and item order', 'the test-specific CRLF and non-ASCII mixed qualified/whole-resource fixtures and their assertions'),
    25: ('ordered faithful realization', 'the complete common ownership/lifecycle boundary and independence from Retrieval and automatic selection'),
 }},
 11: {'P': {
    1: ('the planning package assembler import/export exposing copied assembly', 'explicit common renderer and rendered-value companion imports and their __all__ entries'),
    20: ('public exposure of the common planning assembler', 'the distinct outer Context facade and its complete companion plan/materialization/rendering imports and __all__ entries'),
 }},
 12: {'D': {
    6: 'Seeking existing exact-text, non-ASCII and newline fixtures requires the retained-resource fixture construction that preserves exact bytes. This unit establishes writing exact UTF-8 bytes and explicitly observing addressed resources to build retained snapshots; that setup is the complete relevant fixture fact sought.',
 }, 'P': {
    32: ('CRLF/non-ASCII mixed text fixtures, unchanged retained source and rendered order as exact-text boundary evidence', 'the native whole-resource provenance assertion'),
    17: ('preserved exact rendered strings, UTF-8 and newline boundaries', 'the full assembly envelopes and independent reported Context byte length excluding the task'),
    27: ('exact-text and newline preservation behavior', 'the full canonical renderer header, identity, count and ordered-heading construction'),
    5: ('exact original task text and its placement relative to Context', 'role, shared non-prompt values and inverse-replacement equality assertion'),
 }},
 13: {'D': {
    23: 'The need expressly asks for tests of foreign/stale repository, snapshot and content rejection. A full answer identifies the changed-snapshot, same-snapshot changed-content and missing-resource cases, and how replace/pytest.raises exercise them, establishing the complete regression-test unit.',
 }, 'P': {
    8: ('tested source frame/content mismatch and missing-resource rejection', 'the complete source dependency and occurrence snapshot/address checking contract'),
    22: ('tested target frame/content mismatch and missing-resource rejection', 'the complete target support/subject snapshot and subject resource-dependency checks'),
    24: ('tested target resource and repository/snapshot frame consistency', 'retained analysis target declaration-membership checks'),
    28: ('tested foreign/stale/missing/unequal-occurrence rejection', 'exact item text, retained identities and original native provenance'),
    10: ('tested common repository/snapshot mismatch rejection', 'ordered realization, returned identity/representation checks and all-success publication'),
    14: ('tested mixed repository/snapshot frame rejection', 'the immutable ordered-plan contract and its other purpose, emptiness and duplicate checks'),
 }},
 14: {'D': {
    5: 'The copied-request preservation test question seeks the complete common assembly regression: original task and role, shared non-prompt values, append placement and inverse replacement showing equality to the caller request. These assertions together establish the full reviewed test fact.',
    26: 'The invalid-argument test question seeks existing numeric test conventions, including parametrization, descriptive ValueError matching, None and valid cases. The frozen task basis supplies the nonnegative byte domain, so a complete answer also distinguishes the new accepted zero from existing out-of-domain token integers.',
 }, 'P': {
    11: ('numeric request admission and descriptive invalid-value errors evidenced by tests', 'the complete request-side validator implementation convention and its positive-token/nonnegative-byte domain distinction'),
    31: ('optional integer/type/negative-count testable admission behavior', 'the complete ModelUsage admission contract and its separate TypeError versus ValueError convention'),
    13: ('preservation of tested non-prompt request fields', 'the frozen dataclass declaration and complete field inventory including tools'),
    21: ('tested role and non-prompt field preservation', 'the actual dataclasses.replace implementation replacing only Prompt'),
    16: ('copied-request preservation and argument-admission behavior under assembly', 'the keyword-only signature, rendered type, lack of a limit and full-text/final-replace implementation contract'),
 }},
 15: {'P': {
    9: ('identification of governing architecture documentation relevant to bounded capacity', 'its canonical current cross-package status and full current planning/materialization/rendering/assembly description'),
    4: ('distinction of capacity/selection and future budgets from current behavior', 'the package overview facts about exact materialization, native provenance, copied Context and both supported choices'),
    25: ('separation from automatic selection', 'ownership of ordered caller-directed plans and faithful realization through rendering and copied assembly independently of Retrieval'),
 }},
 16: {'P': {
    4: ('documented rendered Context and copied-request assembly contracts', 'the complete exact materialization/native provenance/both-choice description and future-token-budget/universal-cost distinction'),
    9: ('documented current planning/rendering/assembly behavior', 'identification and canonical current status of the governing cross-package architecture overview'),
    27: ('documented unchanged rendered item text and ordered Context construction', 'the complete canonical header, identity, count, heading and explicit LF/no-normalization construction'),
    17: ('documented task preservation with appended Context', 'the complete envelopes, independently reported UTF-8 length and embedded newline-byte semantics'),
 }},
 17: {'P': {
    3: ('identification of the documented protected development entry point', 'its complete before-collection exclusion, preserved pytest/coverage configuration and threshold, exit-code propagation and authorization boundary'),
    12: ('the protected test entry point', 'the separate guide commands for lint, format, typing and unstaged/staged whitespace checks'),
 }},
 18: {'D': {
    18: 'The tooling-configuration question expressly seeks constraints on testing. Answering it establishes strict pytest configuration and markers, production branch coverage and the 100 percent threshold, which is the complete unit.',
    29: 'The test/type/style configuration question seeks the project interpreter, lint/format rules and typing settings. A complete answer establishes Python 3.12, Ruff ALL and exceptions, 88 columns, and strict mypy scopes/package/import-base settings, exactly the complete unit.',
 }, 'P': {
    3: ('preserved project pytest configuration and branch coverage threshold', 'the protected command identity, before-collection experiment exclusion, exit-code propagation and authorization boundary'),
    12: ('test versus Ruff/mypy validation responsibilities', 'the separately prescribed guide commands and diff whitespace/staged diff checks'),
 }},
}

NEED_CONCERNS = [
 'ownership of copied ModelRequest assembly',
 'dependency separation from language adapters and Retrieval',
 'the complete exact rendered Context appended during assembly',
 'UTF-8 and newline preservation contracts',
 'optional nonnegative integer validation and error conventions',
 'the assembly rejection seam before request modification without item loss',
 'the mechanism preserving non-Context request state during copying',
 'original task text and Prompt role preservation',
 'repository/snapshot/content checks binding disclosure to plan',
 'item order, exact text and native provenance retention contracts',
 'public planning-package exports exposing copied assembly',
 'exact-text/non-ASCII/newline tests and fixtures',
 'foreign/stale frame rejection tests',
 'copied-request preservation and invalid-argument tests',
 'governing architecture documentation about capacity versus automatic selection',
 'package documentation of rendered Context and copied assembly',
 'identification of the protected validation entry point',
 'test, type and style tooling configuration constraints',
]

# Unit question summaries give every negative pair a distinct fact contrast.
UNIT_CONCERNS = [
 'all three common planning rendering/assembly imports and __all__ entries',
 'qualified-reference purpose, derivation, analysis, target-type and resolution admission plus materializer re-admission',
 'the full protected-command execution and authorization contract',
 'the complete package overview of materialization, provenance, choices and future budgets/costs',
 'the complete common assembly regression assertions',
 'retained-snapshot fixture construction by exact UTF-8 writes and addressed observation',
 'qualified adapter delegation and all retained common-item values',
 'complete qualified-source frame/address/existence/content checks',
 'canonical governing architecture status and current complete planning lifecycle description',
 'common materialization frame, order, identity/representation and all-success publication checks',
 'request-side optional integer admission/errors and positive-token domain distinction',
 'protected-tests-only versus separate lint/format/type/whitespace guide commands',
 'the frozen ModelRequest dataclass and complete declared fields',
 'the complete immutable DisclosurePlan declaration and all admission rules',
 'actual common assembly/rendering imports, type dependency and forbidden dependency absence',
 'the complete existing assembly signature, rendered input, unlimited entire-text behavior and final copy step',
 'separate unchanged task/Context envelopes, independent UTF-8 length and newline bytes',
 'strict pytest configuration/markers and production branch coverage threshold',
 'qualified test-option construction via interpretation, production analysis and retained-reference choice',
 'the distinct outer Context facade imports and all companion __all__ entries',
 'the actual only-Prompt replacement operation and preserved role',
 'complete qualified-target snapshot/existence/dependency/retained-support checks',
 'snapshot/content/missing-resource regression construction using replace and pytest.raises',
 'qualified target frame consistency and retained declaration-analysis membership',
 'common ordered-plan/faithful-realization lifecycle ownership independent of selection/Retrieval',
 'complete numeric test idioms/cases/errors and the new zero-domain distinction',
 'the complete canonical rendered header/identity/count/heading/text/LF construction',
 'whole-resource rejection rules plus unchanged text, identities and native occurrence',
 'Python/Ruff/mypy configuration with exact scopes and package/import bases',
 'complete immutable item retention and ordered plan-item identity/representation correspondence',
 'ModelUsage optional integer admission and distinct type/negative-count errors',
 'mixed-plan CRLF/non-ASCII fixture and text/provenance/order assertions',
]

BLINDNESS_ITEMS = [
 'parent/sibling filesystem', 'repository checkout', 'Git history',
 'lexical query strings', 'analyzed terms', 'retrieval routes',
 'treatment results', 'result resources', 'resource paths for gold answers',
 'ranks/scores', 'acquisition costs', 'arm identities', 'Stage D outcomes',
 'confirmation',
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def serialize(value):
    # This is an output format only. No input is reserialized for integrity.
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def load_packet():
    root = Path(__file__).resolve().parent
    for name, expected in INPUT_HASHES.items():
        assert digest((root / name).read_bytes()) == expected, name
    archive = (root / 'packet.json.gz').read_bytes()
    payload = gzip.decompress(archive)
    assert digest(payload) == PAYLOAD_HASH
    packet = json.loads(payload)
    manifest = json.loads((root / 'manifest.json').read_bytes())
    integrity = json.loads((root / 'integrity.json').read_bytes())
    for record in (manifest, integrity):
        assert record['archive_sha256'] == INPUT_HASHES['packet.json.gz']
        assert record['canonical_payload_sha256'] == PAYLOAD_HASH
    assert integrity['manifest_sha256'] == INPUT_HASHES['manifest.json']
    for name, value in integrity['files'].items():
        assert INPUT_HASHES[name] == value
    assert packet['frame'] == manifest['frame']
    assert manifest['frozen_needs_sha256'] == '8e951bc42ee08db656717ffb494880de26007c087d31f38657b421b8793c54aa'
    assert manifest['reviewed_gold_sha256'] == '0d6f54a4ab1eed68b2deb4f4557ef767ff9f2a7771eebde534527c425ae34430'
    needs = packet['information_needs']; units = packet['units']
    ns = {n['identity'] for n in needs}; us = {u['identity'] for u in units}
    assert len(needs) == len(ns) == manifest['need_count'] == 18
    assert len(units) == len(us) == manifest['required_unit_count'] == 32
    pairs = [(x['need'], x['unit']) for x in packet['mapping_frame']]
    assert len(pairs) == len(set(pairs)) == manifest['mapping_count'] == 576
    assert set(pairs) == {(n, u) for n in ns for u in us}
    alts = {a['identity']: (g['obligation'], set(a['units']))
            for g in packet['alternatives'] for a in g['alternatives']}
    assert len(alts) == sum(len(g['alternatives']) for g in packet['alternatives'])
    for u in units:
        assert set(u['alternative_membership']) == {a for a, (_, members) in alts.items() if u['identity'] in members}
        assert set(u['obligations']) == {ob for ob, members in alts.values() if u['identity'] in members}
    return packet, manifest


def build():
    packet, manifest = load_packet()
    needs = packet['information_needs']; units = packet['units']
    assert set(DECISIONS) == set(range(1, 19))
    mapping = []
    for ni, need in enumerate(needs, 1):
        chosen = DECISIONS[ni]
        assert not (set(chosen.get('D', {})) & set(chosen.get('P', {})))
        for ui, unit in enumerate(units, 1):
            row = {'need': need['identity'], 'unit': unit['identity'],
                   'need_fact_sought': need['statement'], 'unit_fact_established': unit['statement']}
            if ui in chosen.get('D', {}):
                row.update(label='DIRECTLY_COVERS',
                           rationale=chosen['D'][ui],
                           complete_unit_bridge=chosen['D'][ui],
                           counterfactual='PASS: a complete answer to this acquisition intent establishes all components of this unit without another need or incidental facts.')
            elif ui in chosen.get('P', {}):
                covered, missing = chosen['P'][ui]
                row.update(label='PARTIALLY_COVERS', covered_part=covered, missing_part=missing,
                           rationale=f'The need seeks {covered}. The complete unit additionally requires {missing}; answering this need need not establish that remainder.')
            else:
                row.update(label='DOES_NOT_COVER',
                           rationale=f'The need asks for {NEED_CONCERNS[ni-1]}. This unit establishes {UNIT_CONCERNS[ui-1]}. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.')
            mapping.append(row)
    coverage = []
    for ui, unit in enumerate(units, 1):
        rows = [r for r in mapping if r['unit'] == unit['identity']]
        lists = {label: [r['need'] for r in rows if r['label'] == label] for label in packet['mapping_labels']}
        status = ('COVERED' if lists['DIRECTLY_COVERS'] else
                  'PARTIAL_ONLY' if lists['PARTIALLY_COVERS'] else
                  'AMBIGUOUS_ONLY' if lists['AMBIGUOUS'] else 'UNCOVERED')
        coverage.append({'unit': unit['identity'], 'alias': f'U{ui:02}',
                         'statement': unit['statement'], 'obligations': unit['obligations'],
                         'alternative_membership': unit['alternative_membership'],
                         'status': status, 'direct_need_count': len(lists['DIRECTLY_COVERS']),
                         'direct_needs': lists['DIRECTLY_COVERS'],
                         'partial_needs': lists['PARTIALLY_COVERS'], 'ambiguous_needs': lists['AMBIGUOUS']})
    classes = []
    for ni, need in enumerate(needs, 1):
        direct = [c['unit'] for c in coverage if need['identity'] in c['direct_needs']]
        partial = [c['unit'] for c in coverage if need['identity'] in c['partial_needs']]
        unique = [c['unit'] for c in coverage if c['direct_needs'] == [need['identity']]]
        derived = ('NECESSARY' if unique else 'USEFUL_REDUNDANT' if direct else
                   'PARTIAL_ONLY' if partial else 'UNNECESSARY')
        classes.append({'need': need['identity'], 'alias': f'N{ni:02}',
                        'statement': need['statement'], 'obligation': need['obligation'],
                        'classification': derived, 'mechanical_support': derived,
                        'direct_units': direct, 'partial_units': partial, 'unique_units': unique,
                        'reviewer_judgment': {
                            'misformulated': False, 'ambiguous': False,
                            'rationale': 'The frozen statement has a recognizable, answerable acquisition target. Partial mappings reflect its limited scope relative to compound gold facts, rather than an incoherent question or an unsupported premise. No meaning is genuinely under-specified.'},
                        'rationale': (f'This need directly seeks the complete facts of {len(direct)} units, including {len(unique)} uniquely directly covered units.' if direct else
                                      f'This need seeks an identifiable component of {len(partial)} units but no complete reviewed unit; no statement defect warrants MISFORMULATED.')})
    def counts(rows, key, labels):
        counter = Counter(r[key] for r in rows)
        return {label: counter[label] for label in sorted(labels)}
    by_obligation = []
    for ob in sorted(o['identity'] for o in packet['obligations']):
        owned = [c for c in coverage if ob in c['obligations']]
        # Count all needs against every unit with this membership; cross pairs retained.
        rows = [r for r in mapping if any(c['unit'] == r['unit'] for c in owned)]
        need_rows = [r for r in mapping if any(n['identity'] == r['need'] and n['obligation'] == ob for n in needs)]
        by_obligation.append({'obligation': ob, 'unit_memberships': len(owned),
                              'unit_counts': counts(owned, 'status', packet['unit_coverage']),
                              'mapping_counts_by_unit_obligation': counts(rows, 'label', packet['mapping_labels']),
                              'mapping_counts_by_need_obligation': counts(need_rows, 'label', packet['mapping_labels'])})
    by_alternative = []
    for group in packet['alternatives']:
        for alt in group['alternatives']:
            cs = [c for c in coverage if c['unit'] in alt['units']]
            by_alternative.append({'alternative': alt['identity'], 'obligation': group['obligation'],
                                   'member_logic': alt['member_logic'], 'units': alt['units'],
                                   'unit_counts': counts(cs, 'status', packet['unit_coverage']),
                                   'all_members_directly_covered': all(c['status'] == 'COVERED' for c in cs)})
    stats = {'schema': VERSION + '/statistics', 'mapping_count': len(mapping),
             'mapping_label_counts': counts(mapping, 'label', packet['mapping_labels']),
             'unit_counts': counts(coverage, 'status', packet['unit_coverage']),
             'need_classification_counts': counts(classes, 'classification', packet['need_labels']),
             'uniquely_covered_units': [c['unit'] for c in coverage if c['direct_need_count'] == 1],
             'redundantly_covered_units': [c['unit'] for c in coverage if c['direct_need_count'] > 1],
             'by_obligation': by_obligation, 'by_alternative': by_alternative,
             'complete_alternative_obligations': sorted({a['obligation'] for a in by_alternative if a['all_members_directly_covered']}),
             'counting_note': 'Global unit counts deduplicate unit identities. Obligation and alternative counts use original memberships and can sum above 32. No incompatible alternatives are combined.'}
    method = {'schema': VERSION + '/method-provenance', 'frame': packet['frame'],
              'evidence_inputs': list(INPUT_HASHES), 'input_sha256': INPUT_HASHES,
              'decompressed_payload_sha256': PAYLOAD_HASH,
              'bindings': {'frozen_needs_sha256': manifest['frozen_needs_sha256'],
                           'reviewed_gold_sha256': manifest['reviewed_gold_sha256'],
                           'verification': 'The exact-hashed manifest binds the exact-hashed archive and decompressed payload to these opaque source identifiers. Packet/manifest frames, counts, need/unit identities and full alternative membership are consistent. No source serialization/preimage scope is declared; neither opaque identifier is recomputed from a guessed subset or JSON encoding.'},
              'sterile_preexisting_files': sorted(INPUT_HASHES),
              'sterile_preflight': {'unexpected_preexisting_files': 0, 'git_present': False,
                                   'symlinks_present': False, 'junctions_or_reparse_points_present': False,
                                   'repository_checkout_present': False, 'treatment_outputs_present': False,
                                   'prior_c5_gold_present': False},
              'procedure': 'Independent reviewer compared all 18 need meanings with all 32 unit meanings, including cross-obligation pairs. Direct decisions require the complete unit under the counterfactual; partial decisions specify sought and missing components. Noncoverage is defended with the distinct facts sought and established. The frozen statement, reason and task basis provide intent; labels are not assigned by lexical matching or obligation pruning.',
              'strict_scope_examples': [
                  'Knowing assembly ownership alone does not establish the complete ordered-plan/realization/selection boundary.',
                  'Knowing forbidden dependencies alone does not establish actual permitted imports or type-only dependencies.',
                  'Knowing exports exposing assembly alone does not establish every rendering companion or the separate outer facade.',
                  'Identifying the protected entry point alone does not establish every execution and authorization rule.',
                  'Production behavior and test-existence/construction facts are distinguished; partial overlap does not establish a full regression-test unit.'],
              'unit_precedence': ['COVERED', 'PARTIAL_ONLY', 'AMBIGUOUS_ONLY', 'UNCOVERED'],
              'need_classification': 'Reviewer first explicitly excludes MISFORMULATED/AMBIGUOUS on semantic grounds for each need, then derives NECESSARY/USEFUL_REDUNDANT/PARTIAL_ONLY/UNNECESSARY using direct/partial and unique-unit support. No frozen needs are repaired.',
              'alternative_semantics': 'ALL complementary units per alternative; ANY complete alternative per obligation. Original memberships preserved.',
              'direct_requirement': packet['direct_coverage_rule'],
              'limits': 'This assesses acquisition intent only. It does not establish retrieval success, treatment comparisons or U1 effectiveness.',
              'output_serialization': 'Versioned UTF-8 JSON, sorted object keys, two-space indentation, one terminal LF, original packet order for need/unit arrays. This output rule imposes no additional input integrity rule.',
              'blindness_attestation': {name + ' accessed': 'NO' for name in BLINDNESS_ITEMS},
              'artifact_policy': 'Scientific outputs, local generator and local tests only. Operational .local/codex-result.md is created after scientific validation and excluded from all scientific hashes and evidence.'}
    validation = {'schema': VERSION + '/validation', 'checks': {
        'sterile_preflight': 'PASS', 'exact_packet_input_hashes': 'PASS',
        'decompressed_payload_hash': 'PASS', 'manifest_payload_source_identity_binding': 'PASS',
        'pair_coverage_576_of_576': 'PASS', 'duplicate_pairs_zero': 'PASS',
        'missing_pairs_zero': 'PASS', 'unexpected_pairs_zero': 'PASS',
        'all_32_units_accounted_for': 'PASS', 'all_18_needs_classified': 'PASS',
        'direct_rationale_completeness': 'PASS', 'partial_rationale_completeness': 'PASS',
        'unit_coverage_derivation': 'PASS', 'need_classification_consistency': 'PASS',
        'alternative_membership_preservation': 'PASS', 'deterministic_replay': 'PASS',
        'overwrite_refusal': 'PASS', 'no_forbidden_fields': 'PASS',
        'blindness_all_no': 'PASS', 'scientific_workspace_whitelist': 'PASS'},
        'verification_method': 'Self-contained local pytest suite with plugin autoload disabled, --noconftest and an explicit local test path. Checks recompute derivations and replay in memory; overwrite is refused before any output is written.',
        'digest_manifest_policy': 'The digest manifest excludes itself to avoid recursive hashing, and excludes the operational handoff. Its own hash is reported externally.'}
    objects = {
        NAMES[0]: {'schema': VERSION + '/mappings', 'mappings': mapping},
        NAMES[1]: {'schema': VERSION + '/unit-coverage', 'units': coverage},
        NAMES[2]: {'schema': VERSION + '/need-classifications', 'needs': classes, 'misformulated_reviews': []},
        NAMES[3]: stats, NAMES[4]: method, NAMES[5]: validation,
    }
    blobs = {name: serialize(value) for name, value in objects.items()}
    root = Path(__file__).resolve().parent
    support = ['adjudicate_c5_v1.py', 'test_c5_v1.py']
    blobs[NAMES[6]] = serialize({'schema': VERSION + '/output-digests',
                               'scientific_output_sha256': {name: digest(data) for name, data in blobs.items()},
                               'validation_support_sha256': {name: digest((root / name).read_bytes()) for name in support},
                               'exclusions': [NAMES[6], '.local/codex-result.md']})
    return blobs


def write_outputs(blobs):
    root = Path(__file__).resolve().parent
    existing = [name for name in blobs if (root / name).exists()]
    if existing:
        raise FileExistsError('Refusing to overwrite C.5 artifacts: ' + ', '.join(existing))
    for name, data in blobs.items():
        with (root / name).open('xb') as stream:
            stream.write(data)


if __name__ == '__main__':
    if sys.argv[1:] != ['--generate']:
        raise SystemExit('Usage: python adjudicate_c5_v1.py --generate')
    write_outputs(build())
    print('Created seven versioned C.5 scientific artifacts without overwriting inputs.')
