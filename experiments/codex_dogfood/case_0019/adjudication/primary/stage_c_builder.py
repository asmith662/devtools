"""Standalone frozen primary adjudication; stdlib only, workspace inputs only.

This replays authored judgments, not an automated semantic reviewer.
Run with python -B stage_c_builder.py verify (read-only except scratch replay).
"""
from __future__ import annotations

import ast
import copy
import gzip
import hashlib
import importlib.util
import itertools
import json
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).absolute().parent
INPUT_HASHES = {
    'README.md': '17c7a5c68d9374381bc000689e415d68b1b79784d7c7a9babda26b985a6c5a29',
    'integrity.json': 'd5aee029ad6d832d94f2787cff448af06bdc64d014db5707c6cc9934b52a8494',
    'manifest.json': 'a082dab178c3dd2e7f7b5683ec1766bbc44c4888ba8534a3d497e6bc4a72eb4a',
    'resources.json.gz': '9cdf7234c3ded1f193a1f64f9f458c98f66aa354c95eadf13845b0649d1f5373',
    'validate_packet.py': '72558691d636a60e77454f691951800177cf807d8dd103c510831b4a7516428a',
}
PAYLOAD_HASH = '874282ee0e339f27717dcd08523526b0ad05e483a433027cb5fd063e1410f596'
FRAME = {
    'repository_id': '5cf96d9e-d6a5-44a6-83d3-1e24f6e00009',
    'snapshot_id': '6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028',
    'corpus_id': 'eb20830bed8817e886f21cae6ceffbb15da7dc1f6ccae8667cf2208a6b659ef6',
}
NAMES = ('stage_c_review.json', 'stage_c_statistics.json', 'STAGE_C_REVIEW.md',
         'stage_c_validation.json', 'stage_c_hashes.json', 'stage_c_method.md',
         'stage_c_builder.py')
CATEGORIES = ('REQUIRED', 'HELPFUL_ONLY', 'UNNECESSARY')
EXCLUDED = (
    'repository checkout', 'Git/history', 'parent directories', 'sibling workspaces',
    'prior Codex session', 'web', 'queries', 'lexical ranks/scores',
    'structural annotations', 'Reference treatment evidence', 'support pairs',
    'predecessor pairs', 'treatment timings', 'graph/PPR/RRF', 'other cohort cases',
    'child implementation', 'child paths', 'child diff',
    'current modern vLLM implementation', 'prior gold', 'confirmation', 'reserve',
)
NEXT = ('Import this clean Astra / High primary byte-for-byte.\n\n'
        'Preserve the frozen task-specification gap.\n\n'
        'Do NOT inspect the historical child implementation.\n\n'
        'Wait until the other independently blinded cohort primaries are complete before\n'
        'any structural-discrimination effectiveness interpretation.\n\nSTOP.')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n').encode()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def no_reparse(path):
    info = path.lstat()
    need(not path.is_symlink() and not getattr(info, 'st_file_attributes', 0) &
         stat.FILE_ATTRIBUTE_REPARSE_POINT, 'Reparse point: ' + str(path))


def authenticate():
    no_reparse(ROOT)
    for name, digest in INPUT_HASHES.items():
        path = ROOT / name
        no_reparse(path)
        need(path.is_file() and sha(path.read_bytes()) == digest, 'Input hash: ' + name)
    raw = gzip.decompress((ROOT / 'resources.json.gz').read_bytes())
    p = json.loads(raw)
    need(sha(raw) == PAYLOAD_HASH and raw == canonical(p), 'Payload hash/codec')
    spec = importlib.util.spec_from_file_location('blind_packet_validator', ROOT / 'validate_packet.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate_payload(p, module.BOUND)
    need(all(p['parent_frame'][k] == v for k, v in FRAME.items()), 'Frame')
    need(p['task_text'] == 'Add vLLM CUDA graph estimate control\n', 'Task')
    need(len(p['resources']) == 222 and len(p['obligations']) == 3, 'Counts')
    return p


def resource(p, n):
    return p['resources'][n-1]


def identity(p, n):
    r = resource(p, n)
    return {'packet_index': n, **{k: v for k, v in r.items() if k != 'content'}}


def span(p, n, lo, hi):
    r = resource(p, n)
    lines = r['content'].splitlines(keepends=True)
    need(1 <= lo <= hi <= len(lines), 'Span bounds')
    start = sum(map(len, lines[:lo-1]))
    quote = ''.join(lines[lo-1:hi])
    end = start + len(quote)
    return {'resource': identity(p, n), 'start_line': lo, 'end_line': hi,
            'start_char': start, 'end_char': end,
            'start_utf8_byte': len(r['content'][:start].encode()),
            'end_utf8_byte': len(r['content'][:end].encode()),
            'quote': quote, 'quote_sha256': sha(quote.encode()),
            'provenance': 'AUTHENTICATED_PARENT_RESOURCE'}


def spans(p, n, ranges):
    return [span(p, n, a, b) for a, b in ranges]


def task_evidence(p, oid, field):
    o = p['obligations'][int(oid[1:])-1]
    text = o[field]
    return {'json_pointer': f'/obligations/{int(oid[1:])-1}/{field}',
            'obligation_identity': o['obligation_identity'], 'start_char': 0,
            'end_char': len(text), 'quote': text,
            'quote_sha256': sha(text.encode()), 'provenance': 'FROZEN_OBLIGATION'}


# Human-authored positive contributions. These are not lexical rules or edit targets.
# Resource numbers refer only to the authenticated, canonical packet order.
HELP = {
    (3, 'O3'): ([(5, 16), (64, 73)], 'The documentation authority and update policy help locate the bounded explanation; a valid explanation does not require this navigation document.'),
    (5, 'O3'): ([(15, 35)], 'The existing pytest configuration informs local validation conventions; the focused semantic checks are already specified by O3.'),
    (19, 'O2'): ([(8, 19), (64, 71)], 'Direct ordered argv and ordinary nonzero results clarify the lower transport boundary; the owned launch baseline is established in the provider source.'),
    (21, 'O2'): ([(26, 58)], 'Direct subprocess creation and cancellation semantics clarify the executor used by the provider; this task need not alter or independently re-prove that executor.'),
    (22, 'O2'): ([(57, 79)], 'The command domain boundary and immediate-child limits inform lifecycle preservation without supplying a CUDA estimation contract.'),
    (25, 'O2'): ([(180, 203)], 'The direct subprocess executor confirms argv forwarding and missing-executable normalization, beyond the owned provider launch evidence needed here.'),
    (28, 'O2'): ([(14, 21), (38, 62)], 'The immutable executable/arguments representation explains how the returned Command retains ordered launch arguments; it is not an additional provider integration fact.'),
    (30, 'O2'): ([(14, 29), (41, 55)], 'Result exit-status and byte diagnostics clarify existing failure handling; the provider source already shows the preservation seam.'),
    (85, 'O1'): ([(16, 23)], 'Existing benchmark persistence records other launch choices. It informs an optional durable retention design, but O1 does not mandate benchmark artifacts.'),
    (85, 'O3'): ([(3, 23)], 'The benchmark boundary and retained offload choices inform limits to document if artifact retention is selected; no new benchmark is required.'),
    (86, 'O1'): ([(41, 79)], 'The immutable serving snapshot extracts public configuration. This is a defensible optional retention extension, not a mandated schema for the new control.'),
    (86, 'O3'): ([(41, 79)], 'Snapshot extraction informs optional retention checks; focused configuration/launch checks can satisfy O3 without changing snapshot scope.'),
    (87, 'O1'): ([(97, 109)], 'The benchmark result captures a snapshot from the server. This identifies an existing consumer of retained configuration, not a required benchmark workflow.'),
    (88, 'O1'): ([(24, 24), (66, 94), (106, 165)], 'Explicit schema serialization and old-schema reconstruction are useful if durable artifacts are extended; their historical defaults cannot determine a future estimation default.'),
    (88, 'O3'): ([(66, 94), (106, 165)], 'The serializer and loader inform optional round-trip/compatibility checks, without making those a mandatory new artifact contract.'),
    (89, 'O2'): ([(2, 6)], 'The explicit provider launch/lifecycle boundary corroborates keeping this change out of Agent and Runtime invocation semantics.'),
    (90, 'O1'): ([(19, 35)], 'Documentation establishes existing explicit provider-specific controls and defaults as integration context; none specifies the future estimation value.'),
    (90, 'O2'): ([(19, 39)], 'The lifecycle description corroborates current Docker, readiness and primary-error behavior; it does not fully specify the exact ordered launch representation.'),
    (90, 'O3'): ([(5, 15), (19, 39)], 'Current package scope and limits materially inform the new bounded explanation, but the task supplies the documentation duty and current tests supply preservation expectations.'),
    (91, 'O2'): ([(5, 37)], 'The error taxonomy and startup diagnostic payload clarify the failures preserved by the provider lifecycle; the required source/test alternatives already establish their uses.'),
    (91, 'O3'): ([(9, 37)], 'Error names and diagnostic shape help write regression assertions; the existing lifecycle tests directly demonstrate their contract.'),
    (92, 'O1'): ([(12, 39)], 'Pinned model-reference validation is current unrelated configuration context, not a future CUDA control value-domain rule.'),
    (92, 'O2'): ([(12, 39)], 'The repository/revision value explains existing model identity forwarded at launch; this task preserves it without changing the reference contract.'),
    (93, 'O3'): ([(46, 100), (119, 154), (210, 342), (345, 399)], 'Production configuration, launch and lifecycle provide additional test oracles; the bounded check/documentation obligation can be supported by the existing regression specification and task criteria.'),
    (190, 'O1'): ([(135, 168)], 'The test shows public server-config snapshot extraction as an optional retention route; it cannot require adding the new control to benchmark artifacts.'),
    (190, 'O3'): ([(135, 168)], 'The snapshot test is a focused example for optional retention coverage, unnecessary for the minimal configuration/launch check contract.'),
    (192, 'O1'): ([(74, 206)], 'Artifact tests establish explicit retained offload choices and historical-schema reconstruction. They inform an optional durable extension without prescribing new defaults.'),
    (192, 'O3'): ([(74, 206)], 'Round-trip, disabled-state and missing-provenance checks are useful optional examples, not mandatory test wording or a required estimation schema.'),
    (195, 'O1'): ([(41, 54), (100, 161), (250, 294)], 'Tests corroborate retained immutable configuration and structural validation; they do not exhaustively define the current field/validation surface or full ordered launch baseline.'),
    (195, 'O2'): ([(164, 247), (297, 407), (410, 1203)], 'Tests independently support lifecycle preservation and several forwarding facts, but cannot replace the complete ordered launch baseline; combining them with that baseline is a nonminimal resource superset.'),
    (210, 'O1'): ([(349, 440)], 'The composition tests demonstrate callers mapping explicit arguments into public configuration. A new CLI spelling or driver change is not mandated.'),
    (210, 'O3'): ([(100, 107), (110, 162), (349, 440)], 'The fake composition boundary and public-configuration checks inform optional caller-level tests. The referenced script is not in the packet and is not needed for the frozen minimum.'),
}

TASK_UNITS = [
    ('T1', ['O1'], 'Expose an explicit caller-selected CUDA graph estimation choice coherently in existing provider configuration.', [('O1', 'requirement'), ('O1', 'satisfaction')]),
    ('T2', ['O1'], 'Validate the choice according to its supported provider contract; that contract remains unspecified.', [('O1', 'satisfaction')]),
    ('T3', ['O1'], 'Retain the configuration choice reproducibly.', [('O1', 'satisfaction')]),
    ('T4', ['O1', 'O2'], 'Omitting the new control preserves parent launch behavior; this does not select a provider default for the new option.', [('O1', 'satisfaction'), ('O2', 'satisfaction')]),
    ('T5', ['O2'], 'Forward the explicit supported choice faithfully through the existing launch representation while preserving unrelated launch options.', [('O2', 'requirement'), ('O2', 'satisfaction')]),
    ('T6', ['O2'], 'Keep ownership/readiness/error semantics unchanged.', [('O2', 'satisfaction')]),
    ('T7', ['O2', 'O3'], 'Bound claims to configuration/launch evidence; no unproven runtime effect or hardware/performance guarantee.', [('O2', 'satisfaction'), ('O3', 'excluded_interpretation')]),
    ('T8', ['O3'], 'Document the supported configuration/launch contract and its limits.', [('O3', 'requirement'), ('O3', 'satisfaction')]),
    ('T9', ['O3'], 'Add focused no-live-service omitted, explicit and invalid control-input/forwarding checks as applicable.', [('O3', 'satisfaction')]),
    ('T10', ['O3'], 'Preserve existing configuration and lifecycle tests.', [('O3', 'satisfaction')]),
]
REPO_UNITS = [
    ('R1', ['O1'], 'Current provider configuration surface: VLLMServingConfig is provider-specific, frozen and slotted, with the shown existing fields, defaults, structural validation and prefetch constraints.',
     [(93, [(46, 100), (119, 154)])],
     'Only the provider definition exhaustively establishes the current configuration surface and its constraints. Example constructions and prose omit parts of that surface.'),
    ('R2', ['O1', 'O2'], 'Current omission baseline and extension seam: the deterministic owned Docker Command contains the exact ordered base arguments and conditional existing offload, WSL2 and remote-code options shown in _build_launch_command.',
     [(93, [(31, 34), (345, 399)])],
     'Tests assert selected presence/absence/counts, not the complete ordered command or placement around the image. Documentation and generic Command resources cannot reconstruct this provider baseline.'),
    ('R3', ['O1'], 'The current reproducible launch configuration is immutable and retained as the public server.config value, sufficient for minimum in-process reproducible retention.',
     [(93, [(46, 68), (168, 187)]), (195, [(100, 132)])],
     'Either the frozen configuration plus retained getter, or the explicit immutability and identity tests, establishes this fact. Benchmark snapshots corroborate consumers but do not establish the server retention contract alone.'),
    ('R4', ['O2'], 'Owned startup returns after model readiness; malformed launch identity and operational failures remain explicit; stop respects exact ownership, and failed-start cleanup preserves the primary failure/cancellation with bounded secondary diagnostics.',
     [(93, [(31, 43), (210, 342), (402, 433), (441, 539), (542, 563)]),
      (195, [(326, 376), (410, 513), (516, 555), (558, 665), (668, 853), (856, 1203)])],
     'The complete source lifecycle or the focused regression expectations separately establish these preservation facts. Overview prose and error classes give only partial corroboration.'),
    ('R5', ['O3'], 'Existing configuration regression expectations cover immutable/hashable defaults, retained config identity, invalid structural input and isolated complete prefetch input.',
     [(195, [(41, 54), (100, 161), (250, 294)])],
     'The actual existing regression expectations are in this test resource. Production behavior is an additional oracle but cannot identify which existing checks must be preserved.'),
    ('R6', ['O3'], 'Existing launch/lifecycle regression expectations use recorded executors and replaced probes to cover default/explicit forwarding, readiness, exact ownership, bounded diagnostics and primary-error/cancellation preservation.',
     [(195, [(57, 97), (164, 247), (297, 1203), (1215, 1255)])],
     'The existing serving regression suite provides the bounded no-live-provider test seam and preservation expectations. Generic command and benchmark tests do not substitute for this suite.'),
]


def build_units(p):
    units = []
    for uid, obs, claim, refs in TASK_UNITS:
        units.append({'id': uid, 'classification': 'TASK_BACKED', 'obligations': obs,
                      'claim': claim, 'task_evidence': [task_evidence(p, *x) for x in refs],
                      'support_alternatives': [{'id': uid+'A0', 'resources': [], 'spans': [],
                                                'inferability': 'EXPLICIT_FROZEN_TASK_CRITERIA'}],
                      'alternatives_rationale': 'No repository fact is required to establish this duty.'})
    for uid, obs, claim, alternatives, rationale in REPO_UNITS:
        units.append({'id': uid, 'classification': 'REPOSITORY_SUPPORTED', 'obligations': obs,
                      'claim': claim, 'task_evidence': [],
                      'support_alternatives': [
                          {'id': uid+'A'+str(i), 'resources': [n], 'spans': spans(p, n, ranges),
                           'inferability': 'DIRECT_CURRENT_SOURCE_OR_REGRESSION_EXPECTATION; NO_FUTURE_PROVIDER_INFERENCE'}
                          for i, (n, ranges) in enumerate(alternatives, 1)],
                      'alternatives_rationale': rationale})
    return units


def families(units):
    result = {}
    for oid in ('O1', 'O2', 'O3'):
        needed = [u for u in units if oid in u['obligations']]
        assignments = []
        for selected in itertools.product(*(u['support_alternatives'] for u in needed)):
            union = sorted({r for alt in selected for r in alt['resources']})
            assignments.append({'resources': union, 'units': [u['id'] for u in needed],
                                'alternatives': {u['id']: a['id'] for u, a in zip(needed, selected)}})
        minimal = [a for a in assignments if not any(set(b['resources']) < set(a['resources']) for b in assignments)]
        grouped = {}
        for a in minimal:
            key = tuple(a['resources'])
            grouped.setdefault(key, []).append(a['alternatives'])
        witnesses = [{'id': oid+'W'+str(i), 'resources': list(key),
                      'semantic_units': [u['id'] for u in needed],
                      'support_assignments': support_assignments,
                      'scope': 'COMPLETE_FROZEN_REPOSITORY_INTEGRATION_PROJECTION',
                      'condition': 'G1 remains open; this is not complete future provider-contract satisfaction.'}
                     for i, (key, support_assignments) in enumerate(sorted(grouped.items()), 1)]
        result[oid] = {'required_units': [u['id'] for u in needed],
                       'minimal_complete_witnesses': witnesses,
                       'dominated_support_assignments': []}
        # Record resource supersets explicitly, without calling them minimal witnesses.
        for selected in itertools.product(*(u['support_alternatives'] for u in needed)):
            union = sorted({r for alt in selected for r in alt['resources']})
            if any(set(w['resources']) < set(union) for w in witnesses):
                result[oid]['dominated_support_assignments'].append({
                    'resources': union, 'alternatives': {u['id']: a['id'] for u, a in zip(needed, selected)},
                    'reason': 'Strict resource superset of a complete witness; alternative evidence is redundant at obligation level.'})
    return result


def scope_description(r):
    """Descriptive source excerpt only; never chooses relevance categories."""
    if not r['content']:
        return 'Empty parent resource.'
    if r['address'].endswith('.py'):
        tree = ast.parse(r['content'])
        doc = ast.get_docstring(tree) or 'Python definitions without a module docstring.'
        return ' '.join(doc.split())
    return next((s.strip('# ').strip() for s in r['content'].splitlines() if s.strip()), 'Empty resource.')


def build_cells(p, units, fs):
    cells = []
    for n, r in enumerate(p['resources'], 1):
        for o in p['obligations']:
            oid = o['id']
            required = any(n in w['resources'] for w in fs[oid]['minimal_complete_witnesses'])
            if required:
                ss = []
                uids = []
                for u in units:
                    if oid not in u['obligations']:
                        continue
                    for a in u['support_alternatives']:
                        if n in a['resources']:
                            ss += a['spans']
                            uids.append(u['id'])
                ss = list({(s['start_line'], s['end_line']): s for s in ss}.values())
                category = 'REQUIRED'
                why = {'O1': 'The exhaustive current configuration surface, retained value and exact omission launch baseline are necessary to integrate the explicit choice without inventing future semantics.',
                       'O2': 'The owned deterministic launch and existing lifecycle establish the forwarding and preservation boundaries required by O2.',
                       'O3': 'The actual existing configuration and lifecycle regression expectations establish what O3 requires preserving and provide the focused no-live-provider check seam.'}[oid]
            elif (n, oid) in HELP:
                ranges, why = HELP[n, oid]
                ss, uids, category = spans(p, n, ranges), [], 'HELPFUL_ONLY'
            else:
                ss, uids, category = [], [], 'UNNECESSARY'
                why = (scope_description(r) + ' Its content does not establish an additional necessary or materially informative '
                       + {'O1': 'fact about the caller-selected estimation configuration or its minimum reproducible retention.',
                          'O2': 'fact about propagation through the owned vLLM launch or the preserved lifecycle boundary.',
                          'O3': 'fact needed for the bounded estimation documentation/checks or the existing serving regression expectations.'}[oid])
            cells.append({'resource': identity(p, n), 'obligation': oid,
                          'obligation_identity': o['obligation_identity'], 'classification': category,
                          'spans': ss, 'rationale': why, 'semantic_units': sorted(set(uids)),
                          'inferability': ('NO_MATERIAL_CONTRIBUTION' if category == 'UNNECESSARY' else
                                          'CURRENT_PARENT_FACTS_ONLY; FUTURE_ESTIMATION_CONTRACT_NOT_INFERABLE'),
                          'provenance': 'AUTHENTICATED_PACKET_ONLY; SAME_PRIMARY_SEMANTIC_JUDGMENT',
                          'unresolved_decision': False})
    return cells


def gap_records(p):
    return [
        {'id': 'G1', 'category': 'TASK_INTERPRETATION_GAP', 'present': True,
         'status': 'PRESERVED_OPEN', 'obligations': ['O1', 'O2', 'O3'],
         'facets': ['provider option spelling', 'value domain', 'provider-version applicability', 'default behavior'],
         'frozen_evidence': p['interpretation_gaps'], 'ambiguities': p['ambiguities'],
         'finding': 'No packet evidence refutes any frozen unspecified facet. Existing offload/pin-memory settings, test image tags and omission branches are current facts, not an estimation contract.',
         'effect': 'Repository integration can be adjudicated completely. Concrete explicit/invalid values, provider encoding, version support and complete future task satisfaction cannot be certified.',
         'resolution': 'Requires an explicit future design/provider-contract decision; no external lookup or guessed choice was used.'},
        {'id': 'G2', 'category': 'TASK_GAP', 'present': False, 'status': 'NONE_IDENTIFIED',
         'obligations': ['O1', 'O2', 'O3'],
         'finding': 'The frozen obligations cover exposure, propagation, preservation, documentation and bounded checks for the one-line task. No separate missing mandatory objective is established. Their detailed acceptance duties come from the freeze, not from the title alone.',
         'ambiguity': 'Reproducible retention does not explicitly mandate durable benchmark artifacts or a new CLI. Minimum retention is the immutable public server configuration; broader retention remains design freedom, not an extra mandatory obligation.'},
        {'id': 'G3', 'category': 'REPOSITORY_INFORMATION_GAP', 'present': False, 'status': 'NONE_FOR_FROZEN_INTEGRATION',
         'obligations': ['O1', 'O2', 'O3'],
         'finding': 'Current configuration, launch and preservation checks are present in the parent packet. The missing future provider contract is G1, not missing repository information.',
         'limitation': 'The composition test refers to a script not retained in this packet. Its absence limits optional CLI-specific conclusions, but no frozen obligation requires that script. No attempt was made to retrieve it.'},
    ]


SELF_REVIEW = [
    ('REQUIRED inflation/under-selection', 'Only sources necessary in a resource-minimal complete integration witness are REQUIRED. Tests as corroboration do not inflate O1/O2; actual regression expectations remain necessary for O3.'),
    ('expected edit target bias', 'No change destinations or child paths were used. Production source is HELPFUL_ONLY for O3; benchmark models/storage remain optional despite plausible edit relevance.'),
    ('future/current fact confusion', 'Existing image tags, booleans, zero defaults and environment/argv options establish only current parent behavior. None determines new estimation semantics.'),
    ('duplicate support', 'R3 and R4 admit both source and test alternatives. Their larger obligation-level resource unions are dominated and removed.'),
    ('missing alternatives', 'Checked documentation, source, serving tests, command primitives, benchmark snapshots/storage/tests and composition tests. No additional complete alternative for R1/R2/R5/R6 is defensible at the stated fact scope.'),
    ('witness supersets', 'Enumerated support products and removed every strict resource superset before forming task combinations.'),
    ('invalid inferability', 'Direct source and test expectations are distinguished from execution proof. No live provider behavior or new option semantics are inferred.'),
    ('overcompound units', 'Self-review split compound task duties into independently assessable exposure, validation, retention, omission, forwarding, lifecycle preservation, claim limits, documentation, focused checks and preservation of existing tests. Six cohesive current-fact units remain separate from those ten duties; cell categories did not change.'),
    ('artificial fragmentation', 'Did not create units for individual argv tokens, constructor fields, invalid examples or test functions. Cohesive preservation facts remain units.'),
    ('task-design ambiguity treated as repository gap', 'G1 remains open with all four facets. G2 and G3 are evaluated separately; optional snapshot/CLI extensions are not imposed as missing mandatory work.'),
]


def build_review(p, reviewed=True):
    units = build_units(p)
    fs = families(units)
    return {'schema': 'stage-c-clean-primary-v1', 'case_id': p['case_id'],
            'task_identity': p['task_identity'], 'task_text': p['task_text'],
            'parent_frame': p['parent_frame'], 'obligations': p['obligations'],
            'authentication': {'initial_exact_five': True, 'initial_no_reparse_points': True,
                               'validator_result': 'PASS; NO ADJUDICATION',
                               'input_sha256': INPUT_HASHES, 'canonical_payload_sha256': PAYLOAD_HASH},
            'reviewer': {'designated_model': 'GPT-6 Astra', 'designated_reasoning': 'High',
                         'primary_count': 1, 'second_reviewer': False, 'reconciliation': False,
                         'host_routing_independently_verified': False,
                         'routing_limitation': 'Designation recorded as requested; no independent host/model-routing evidence is available within the permitted packet.'},
            'blindness': {'access': {k: 'NO' for k in EXCLUDED},
                         'qualification': 'Excluded categories mean external experiment/history evidence. Native parent resource text and immutable identity fields supplied in this packet were read. Locally generated source declarations and line views are reading aids, not supplied structural treatment annotations.'},
            'semantics': {'REQUIRED': 'Necessary in at least one inclusion-minimal complete repository-integration witness for the frozen obligation.',
                          'HELPFUL_ONLY': 'Materially informative but unnecessary in all such minimal witnesses.',
                          'UNNECESSARY': 'No necessary or materially informative contribution to the bounded obligation.',
                          'sufficiency_scope': 'Repository-integration projection only. Every witness is conditional on resolving G1 before claiming a fully specified implementation.',
                          'span_coordinates': 'One-based inclusive lines; zero-based half-open Unicode-character and UTF-8-byte offsets; quotes preserve native line endings.',
                          'unit_policy': 'Separate task-backed duties from current repository facts; no mixed TASK_AND_REPOSITORY_SUPPORTED unit is needed. The mixed class is allowed but has zero units.',
                          'retention_interpretation': 'The minimum is reproducible in-process config retention. Durable benchmark snapshots and caller CLI additions are optional, not silently mandated.'},
            'resource_ledger': [{'resource': identity(p, n), 'content_scope': scope_description(r),
                                 'cells_complete': 3, 'order': n}
                                for n, r in enumerate(p['resources'], 1)],
            'cells': build_cells(p, units, fs), 'semantic_units': units, 'obligation_support': fs,
            'gaps': gap_records(p),
            'task_interpretation_challenge': 'Accepted the frozen three-obligation scope. The terse task title alone would not establish all validation/lifecycle duties, but the authenticated freeze expressly supplies them. No additional mandatory benchmark, CLI, live test or provider default was inferred.',
            'self_review': {'completed': reviewed, 'reviewer': 'SAME_PRIMARY',
                            'checks': [{'check': k, 'result': 'PASS', 'finding': v} for k, v in SELF_REVIEW] if reviewed else []},
            'limitations': ['Semantic necessity is the primary judgment, not proven by deterministic replay.',
                            'All resources were decoded and screened in canonical order using source docstrings/declarations/imports or prose headings; candidate contributions were read as exact native spans. This does not claim every unrelated implementation line was manually read.',
                            'Tests were inspected as parent expectations; no devtools code, repository tests, Docker, GPU or network was executed.',
                            'Full future task satisfaction remains uncertifiable because G1 is intentionally unresolved.'],
            'unresolved_cell_decisions': 0, 'next_step': NEXT}


def intersection(sets):
    return sorted(set.intersection(*(set(s) for s in sets))) if sets else None


def dedup_sets(sets):
    return [list(s) for s in sorted({tuple(sorted(s)) for s in sets})]


def minimal_sets(sets):
    return [s for s in sets if not any(set(t) < set(s) for t in sets)]


def statistics(r):
    by_obligation = {}
    for oid, family in r['obligation_support'].items():
        ws = family['minimal_complete_witnesses']
        by_obligation[oid] = {
            'cell_counts': {c: sum(x['obligation'] == oid and x['classification'] == c for x in r['cells']) for c in CATEGORIES},
            'minimal_complete_witness_count': len(ws),
            'repository_empty_witness_count': sum(not w['resources'] for w in ws),
            'obligation_indispensable_resources': intersection([w['resources'] for w in ws]),
            'obligation_indispensable_semantic_units': intersection([w['semantic_units'] for w in ws]),
            'resource_count_range': [min(len(w['resources']) for w in ws), max(len(w['resources']) for w in ws)],
            'semantic_unit_count_range': [min(len(w['semantic_units']) for w in ws), max(len(w['semantic_units']) for w in ws)],
        }
    products = list(itertools.product(*(r['obligation_support'][o]['minimal_complete_witnesses'] for o in ('O1', 'O2', 'O3'))))
    combos = [{'id': 'C'+str(i), 'witnesses': [w['id'] for w in ws],
               'resource_union': sorted({n for w in ws for n in w['resources']}),
               'semantic_unit_union': sorted({u for w in ws for u in w['semantic_units']})}
              for i, ws in enumerate(products, 1)]
    ru = dedup_sets([c['resource_union'] for c in combos])
    su = dedup_sets([c['semantic_unit_union'] for c in combos])
    return {'schema': 'stage-c-statistics-v1', 'case_id': r['case_id'],
            'scope': 'CONDITIONAL_REPOSITORY_INTEGRATION; G1_REMAINS_OPEN',
            'resources': 222, 'obligations': 3, 'expected_cells': 666,
            'actual_cells': len(r['cells']),
            'duplicates': len(r['cells'])-len({(c['resource']['packet_index'], c['obligation']) for c in r['cells']}),
            'missing': len({(n, o) for n in range(1, 223) for o in ('O1', 'O2', 'O3')} - {(c['resource']['packet_index'], c['obligation']) for c in r['cells']}),
            'unexpected': len({(c['resource']['packet_index'], c['obligation']) for c in r['cells']} - {(n, o) for n in range(1, 223) for o in ('O1', 'O2', 'O3')}),
            'unresolved': sum(c['unresolved_decision'] for c in r['cells']),
            'cell_counts': {c: sum(x['classification'] == c for x in r['cells']) for c in CATEGORIES},
            'positive_resources': sorted({c['resource']['packet_index'] for c in r['cells'] if c['classification'] != 'UNNECESSARY'}),
            'unit_class_counts': {c: sum(u['classification'] == c for u in r['semantic_units']) for c in ('TASK_BACKED', 'REPOSITORY_SUPPORTED', 'TASK_AND_REPOSITORY_SUPPORTED')},
            'by_obligation': by_obligation, 'complete_task_combinations': combos,
            'complete_task_combination_count': len(combos),
            'distinct_sufficient_resource_unions': ru, 'distinct_sufficient_resource_union_count': len(ru),
            'inclusion_minimal_sufficient_resource_unions': minimal_sets(ru),
            'inclusion_minimal_sufficient_resource_union_count': len(minimal_sets(ru)),
            'resource_count_range': [min(map(len, ru)), max(map(len, ru))],
            'sufficient_semantic_unit_unions': su, 'sufficient_semantic_unit_union_count': len(su),
            'semantic_unit_count_range': [min(map(len, su)), max(map(len, su))],
            'task_indispensable_resources': intersection(ru),
            'task_indispensable_units': intersection(su),
            'union_count_convention': 'Distinct unions generated by combinations of minimal complete obligation witnesses, not every arbitrary upward-closed superset.',
            'unconditional_future_task_satisfaction': {
                'certifiable': False, 'reason': 'G1 is unresolved by design.',
                'complete_witness_count_by_obligation': {'O1': 0, 'O2': 0, 'O3': 0},
                'complete_task_combination_count': 0, 'distinct_sufficient_resource_unions': [],
                'inclusion_minimal_sufficient_resource_unions': [], 'sufficient_semantic_unit_unions': [],
                'resource_count_range': None, 'semantic_unit_count_range': None,
                'obligation_indispensable_resources': None, 'obligation_indispensable_semantic_units': None,
                'task_indispensable_resources': None, 'task_indispensable_units': None,
                'null_semantics': 'Undefined over an empty certifiable witness family; no vacuous indispensability assertion.'}}


def validate_span(p, s):
    n = s['resource']['packet_index']
    need(1 <= n <= 222, 'Span resource index')
    need(s == span(p, n, s['start_line'], s['end_line']), 'Positive identity/span/quote/provenance')


def validate_review(p, r, expected):
    need(r['authentication']['input_sha256'] == INPUT_HASHES, 'Authentication')
    need(r['parent_frame'] == p['parent_frame'] and r['obligations'] == p['obligations'], 'Frozen semantics')
    expected_keys = [(n, o) for n in range(1, 223) for o in ('O1', 'O2', 'O3')]
    keys = [(c['resource']['packet_index'], c['obligation']) for c in r['cells']]
    need(keys == expected_keys, 'Ordered complete cells; duplicates/missing/unexpected')
    need(len(r['resource_ledger']) == 222, 'Resource ledger')
    unit_map = {u['id']: u for u in r['semantic_units']}
    need(len(unit_map) == len(r['semantic_units']), 'Duplicate unit')
    for u in r['semantic_units']:
        need(u['classification'] in {'TASK_BACKED', 'REPOSITORY_SUPPORTED', 'TASK_AND_REPOSITORY_SUPPORTED'}, 'Unit class')
        alts = u['support_alternatives']
        need(bool(alts) and len({a['id'] for a in alts}) == len(alts), 'Unit alternatives')
        sets = [a['resources'] for a in alts]
        need(len(dedup_sets(sets)) == len(sets) and minimal_sets(sets) == sets, 'Alternative redundancy')
        for a in alts:
            need(a['resources'] == sorted({s['resource']['packet_index'] for s in a['spans']}), 'Alternative evidence coverage')
            for s in a['spans']:
                validate_span(p, s)
            if u['classification'] == 'TASK_BACKED':
                need(a['resources'] == [] and bool(u['task_evidence']), 'Task-backed support')
            else:
                need(bool(a['resources']), 'Repository-backed empty support')
        for te in u['task_evidence']:
            parts = te['json_pointer'].split('/')
            oid, field = 'O'+str(int(parts[2])+1), parts[3]
            need(te == task_evidence(p, oid, field), 'Task quote')
    for c in r['cells']:
        n, oid = c['resource']['packet_index'], c['obligation']
        need(c['resource'] == identity(p, n), 'Cell native identity')
        need(c['obligation_identity'] == p['obligations'][int(oid[1:])-1]['obligation_identity'], 'Cell obligation identity')
        need(c['classification'] in CATEGORIES and c['unresolved_decision'] is False, 'Cell decision')
        need(bool(c['spans']) == (c['classification'] != 'UNNECESSARY'), 'Positive spans required')
        for s in c['spans']:
            need(s['resource'] == c['resource'], 'Cross-resource cell span')
            validate_span(p, s)
        need(bool(c['rationale']) and bool(c['inferability']) and bool(c['provenance']), 'Decision explanation')
        need(set(c['semantic_units']) <= unit_map.keys(), 'Cell unit reference')
    # Independent exhaustive resource-subset sufficiency check, rather than only
    # repeating the support-product builder. The candidate pool is very small.
    for oid, f in r['obligation_support'].items():
        us = [u for u in r['semantic_units'] if oid in u['obligations']]
        need(f['required_units'] == [u['id'] for u in us], 'Required units')
        pool = sorted({n for u in us for a in u['support_alternatives'] for n in a['resources']})
        sufficient = []
        for mask in range(1 << len(pool)):
            selected = {pool[i] for i in range(len(pool)) if mask & (1 << i)}
            if all(any(set(a['resources']) <= selected for a in u['support_alternatives']) for u in us):
                sufficient.append(sorted(selected))
        minimal = dedup_sets(minimal_sets(sufficient))
        ws = f['minimal_complete_witnesses']
        need(dedup_sets([w['resources'] for w in ws]) == minimal and len(ws) == len(minimal), 'Witness completeness/minimality')
        for w in ws:
            need(w['semantic_units'] == [u['id'] for u in us], 'Witness units')
            for assignment in w['support_assignments']:
                need(set(assignment) == {u['id'] for u in us}, 'Witness support assignment coverage')
                selected = [next((a for a in u['support_alternatives'] if a['id'] == assignment[u['id']]), None) for u in us]
                need(all(a is not None for a in selected), 'Witness alternative reference')
                need(sorted({n for a in selected for n in a['resources']}) == w['resources'], 'Witness resource union')
        required = {n for w in ws for n in w['resources']}
        need(required == {c['resource']['packet_index'] for c in r['cells'] if c['obligation'] == oid and c['classification'] == 'REQUIRED'}, 'REQUIRED/witness equivalence')
    need(r['gaps'] == gap_records(p), 'Gap categories/facets')
    need(all(v == 'NO' for v in r['blindness']['access'].values()) and set(r['blindness']['access']) == set(EXCLUDED), 'Blindness')
    need(r['self_review']['completed'] and len(r['self_review']['checks']) == 10, 'Self-review')
    # Authored primary is authoritative for semantic choices. Exact comparison
    # rejects plausible-looking but unauthorized transformations of that primary.
    need(r == expected, 'Authored primary differs')


def validate_statistics(r, s):
    need(s == statistics(r), 'Statistics/union/intersection arithmetic')
    need((s['resources'], s['obligations'], s['expected_cells'], s['actual_cells']) == (222, 3, 666, 666), 'Completeness counts')
    need(all(s[k] == 0 for k in ('duplicates', 'missing', 'unexpected', 'unresolved')), 'Completeness anomalies')
    for c in s['complete_task_combinations']:
        ws = [w for f in r['obligation_support'].values() for w in f['minimal_complete_witnesses'] if w['id'] in c['witnesses']]
        need(len(ws) == 3, 'Task witness combination')
        need(c['resource_union'] == sorted(set().union(*(set(w['resources']) for w in ws))), 'Task resource union')
        need(c['semantic_unit_union'] == sorted(set().union(*(set(w['semantic_units']) for w in ws))), 'Task unit union')


def mutation_checks(p, r, s):
    tests = []

    def reject(name, kind, mutate):
        changed = copy.deepcopy(r if kind == 'review' else s)
        mutate(changed)
        try:
            if kind == 'review':
                validate_review(p, changed, r)
            else:
                validate_statistics(r, changed)
        except (ValueError, KeyError, IndexError, TypeError, StopIteration):
            tests.append({'mutation': name, 'result': 'REJECTED_AS_REQUIRED'})
        else:
            raise ValueError('Adversarial mutation accepted: ' + name)

    def positive(x):
        return next(c for c in x['cells'] if c['spans'])

    reject('cell_missing', 'review', lambda x: x['cells'].pop())
    reject('cell_duplicate', 'review', lambda x: x['cells'].append(copy.deepcopy(x['cells'][0])))
    reject('cell_unexpected_identity', 'review', lambda x: x['cells'][0]['resource'].__setitem__('packet_index', 223))
    reject('cell_required_inflation', 'review', lambda x: x['cells'][0].__setitem__('classification', 'REQUIRED'))
    reject('positive_native_identity', 'review', lambda x: positive(x)['resource'].__setitem__('content_identity', '0'*64))
    reject('span_offset', 'review', lambda x: positive(x)['spans'][0].__setitem__('start_char', 0))
    reject('span_quote', 'review', lambda x: positive(x)['spans'][0].__setitem__('quote', 'corrupted'))
    reject('inferability_future_contract', 'review', lambda x: positive(x).__setitem__('inferability', 'FUTURE_PROVIDER_DEFAULT_KNOWN'))
    reject('unit_missing', 'review', lambda x: x['semantic_units'].pop())
    reject('unit_claim', 'review', lambda x: x['semantic_units'][0].__setitem__('claim', 'Invented control semantics'))
    reject('alternative_missing', 'review', lambda x: next(u for u in x['semantic_units'] if u['id'] == 'R3')['support_alternatives'].pop())
    reject('alternative_resource', 'review', lambda x: next(u for u in x['semantic_units'] if u['id'] == 'R1')['support_alternatives'][0]['resources'].append(1))
    reject('witness_superset', 'review', lambda x: x['obligation_support']['O1']['minimal_complete_witnesses'][0]['resources'].append(195))
    reject('witness_missing', 'review', lambda x: x['obligation_support']['O3']['minimal_complete_witnesses'].clear())
    reject('union_corruption', 'statistics', lambda x: x['distinct_sufficient_resource_unions'][0].append(1))
    reject('task_combination_corruption', 'statistics', lambda x: x['complete_task_combinations'][0]['witnesses'].pop())
    reject('unit_union_corruption', 'statistics', lambda x: x['sufficient_semantic_unit_unions'][0].pop())
    reject('obligation_indispensability', 'statistics', lambda x: x['by_obligation']['O1']['obligation_indispensable_resources'].clear())
    reject('task_indispensability', 'statistics', lambda x: x['task_indispensable_resources'].append(1))
    reject('unit_indispensability', 'statistics', lambda x: x['task_indispensable_units'].pop())
    reject('gap_silenced', 'review', lambda x: x['gaps'][0].__setitem__('present', False))
    reject('gap_reclassified', 'review', lambda x: x['gaps'][0].__setitem__('category', 'REPOSITORY_INFORMATION_GAP'))
    reject('unconditional_satisfaction_claim', 'statistics', lambda x: x['unconditional_future_task_satisfaction'].__setitem__('certifiable', True))
    reject('input_hash_corruption', 'review', lambda x: x['authentication']['input_sha256'].__setitem__('README.md', '0'*64))
    return tests


METHOD = '''# Stage C method

This is one designated GPT-6 Astra / High primary, followed by one same-primary
self-review. Host routing was not independently verified. No second reviewer,
delegation, reconciliation, external lookup or child comparison was used.

Initial authentication occurred before any file creation: exactly the five
specified regular files, no extras or reparse points, and validate_packet.py
returned PASS; NO ADJUDICATION. All four expected digests, the exact task, all
three frame identities, and the 222-resource/three-obligation boundary matched.
Derived-output verification authenticates those original files separately.

All 222 native resources were decoded and screened in canonical packet order.
Reading aids displayed module docstrings, definitions and imports for Python,
and headings/introductory prose for other resources; candidate support and
boundary evidence were then read as exact numbered source spans. This is not
a claim to manually read every unrelated implementation line. The source text
was never imported or executed. No keyword score, acquisition query, supplied
structural annotation or treatment ranking was used. Resource framing remains
the native whole-resource identity, not a reading-aid excerpt identity.

The authored positive map and unit alternatives are explicit decisions in
stage_c_builder.py. They are not learned from filenames, expected edits, child
paths or diffs. Every other resource-obligation pair has a retained negative
decision with a source-content scope and obligation-specific rationale. The
ordered pre-self-review ledger is .scratch/primary_ledger_before_self_review.json.
The final ledger is stage_c_review.json. Scratch is operational, not a scientific
input or additional source of case evidence.

Necessity is evaluated against the frozen repository-integration projection.
Current source facts and existing regression expectations supply the parent
baseline; frozen task criteria supply the future duties. Provider spelling,
value domain, version applicability and default remain open. These cannot be
derived from existing booleans, CLI flags, environment variables, test image
tags or artifact compatibility defaults. Reproducible retention minimally means
immutable configuration retained by the server. Durable benchmark retention
and a new caller CLI are permissible design choices, not imposed duties.

Ten task-backed units separate independently assessable duties. Six repository
units keep coherent configuration, ordered launch, retention, lifecycle and
regression facts together rather than splitting individual fields or tests.
There are no mixed units because task duties and current evidence were kept
separate. Per-unit support alternatives use exact native spans. Evidence
alternatives for retained config and lifecycle are source or serving tests.
These test alternatives generate supersets when combined with the indispensable
full launch/config source; dominated obligation witnesses are excluded. Generic
command facts and partial prose/tests cannot replace the full provider baseline.

Support products enumerate every alternative for each required semantic unit.
Strict resource supersets are removed. Independent exhaustive subset coverage
checks verify the resulting antichain. Complete task combinations are the
Cartesian product of the minimal obligation witnesses. Distinct unions,
inclusion-minimal unions, ranges and intersections are recomputed. Union counts
refer to these combinations, not all arbitrary upward-closed supersets. Empty
repository supports are used for task units; no entire obligation is repository
empty because each has a parent preservation/integration fact. Full future task
satisfaction has no certifiable witness while G1 remains open; ranges and
indispensability for that empty family are null, not vacuous universal sets.

Self-review covered ten named risks after the initial 666-cell ledger. It split
compound task units into ten independently assessable duties; cell categories
were retained. The final review records the judgments and limitations.

Verification is stdlib-only and uses this workspace. It checks original hashes,
native identities, exact quotes and coordinate systems, all 666 cells, units,
alternatives, witness coverage/minimality, all task arithmetic, gap records,
blindness declarations, canonical bytes and output hashes. It replays authored
judgments; it does not independently prove their semantic truth. Adversarial
mutations cover cells, identities, spans, inferability, units, alternatives,
witnesses, unions, indispensability, gaps and hashes. A separate Python process
emits all seven scientific files into .scratch/replay; verification requires
byte-for-byte equality for every one, including builder and hash manifest.

Commands:
    python -B stage_c_builder.py build
    python -B stage_c_builder.py verify
    python -B stage_c_builder.py handoff

The hash manifest covers the other six scientific files and the expected exact
handoff report bytes. It intentionally cannot include its own recursive hash;
the external verification receipt records the manifest digest. The handoff
command requires completed adjudication/self-review, separate-process replay,
all frozen hashes, original input preservation and blindness attestation before
creating .local. It then copies STAGE_C_REVIEW.md byte-for-byte to
.local/codex-result.md and checks equality. No original input is modified.
'''


def report(r, s):
    c = s['cell_counts']
    lines = [
        'Completed one treatment-blind primary semantic adjudication for case 0019, “Add vLLM CUDA graph estimate control.” Designated reviewer: GPT-6 Astra / High; host routing was not independently verified. No second reviewer or reconciliation was used.',
        '',
        'Authentication passed before any file creation: exactly the five specified regular files, no extras or reparse points, and `PASS; NO ADJUDICATION`. All expected digests, frame identities and counts matched. The original five files remain byte-for-byte preserved.',
        '',
        f'The final ledger contains **222 resources × 3 obligations = 666 cells**: **{c["REQUIRED"]} REQUIRED, {c["HELPFUL_ONLY"]} HELPFUL_ONLY, {c["UNNECESSARY"]} UNNECESSARY**. Duplicates, missing, unexpected and unresolved cell decisions are all **0**. Every positive cell retains native identity/address, obligation, exact spans, rationale, inferability and provenance.',
        '',
        '**The frozen specification gap remains open.** Provider option spelling, value domain, version applicability and default behavior are unspecified. Existing parent defaults, flags and test image tags do not determine those future choices. Repository-integration sufficiency below is conditional; it does not certify a fully specified implementation or provider runtime effects.',
        '',
        '| Obligation | Required / helpful / unnecessary | Minimal repository-integration witness | Indispensable units |',
        '|---|---:|---|---|',
    ]
    for oid in ('O1', 'O2', 'O3'):
        row = s['by_obligation'][oid]
        counts = row['cell_counts']
        addresses = ', '.join('`'+resource_address(r, n)+'`' for n in row['obligation_indispensable_resources'])
        lines.append(f'| {oid} | {counts["REQUIRED"]} / {counts["HELPFUL_ONLY"]} / {counts["UNNECESSARY"]} | {addresses} | '+', '.join(row['obligation_indispensable_semantic_units'])+' |')
    lines += [
        '',
        'There is **1 complete conditional task combination**, **1 distinct sufficient resource union**, and **1 inclusion-minimal sufficient resource union**. The resource-count range is **2–2**. Both task-indispensable resources are `src/devtools/model_serving/vllm.py` and `tests/model_serving/test_vllm.py`.',
        '',
        'There is **1 sufficient semantic-unit union**, with a count range of **16–16**: **10 TASK_BACKED**, **6 REPOSITORY_SUPPORTED**, and **0 TASK_AND_REPOSITORY_SUPPORTED**. All 16 units are task-indispensable within this conditional projection. Task duties and current facts are kept separate.',
        '',
        'T1–T10 cover exposure, contract-appropriate validation, reproducible retention, omission preservation, faithful forwarding, lifecycle preservation, bounded claims, documentation, focused checks, and preservation of existing tests. R1–R6 cover the current configuration surface, complete ordered launch baseline, retained immutable configuration, lifecycle behavior, configuration regressions, and launch/lifecycle regressions.',
        '',
        'R3 and R4 each have two minimal support alternatives: production source or serving tests. The test alternatives produce redundant resource supersets at the obligation level because the full configuration/launch source is already necessary. Those supersets are excluded from minimal witnesses. No complete obligation has a repository-empty witness; individual task-backed units do.',
        '',
        'Minimum reproducible retention is supported by the immutable configuration retained on the server. Benchmark snapshots, artifact schemas and composition tests are helpful for optional extensions; the freeze does not mandate durable benchmark persistence or a new CLI. Generic command primitives and package documentation provide context without replacing the complete provider baseline.',
        '',
        '| Gap category | Finding |',
        '|---|---|',
        '| TASK_INTERPRETATION_GAP | Present and preserved: all four unspecified provider-contract facets. |',
        '| TASK_GAP | No separate omitted mandatory objective identified; broader retention/CLI choices remain design freedom. |',
        '| REPOSITORY_INFORMATION_GAP | None for frozen integration. An absent script referenced by composition tests limits optional CLI conclusions only. |',
        '',
        'For unconditional future task satisfaction, certifiable complete witnesses and task combinations are **0**; sufficient unions are empty, and count ranges/indispensability are **undefined**, not vacuously universal. The open design gap is not an unresolved cell decision.',
        '',
        'The same-primary self-review completed all ten requested checks. It split compound task duties into independently assessable units and retained the cell classifications. All resources were screened in packet order using native content declarations/prose, with detailed span inspection of candidate support. This does not claim manual reading of every unrelated implementation line. Parent tests were evidence only; no devtools import, repository test, live service or network execution occurred.',
        '',
        'Standalone verification **PASS**: original hashes, identities/spans, cells, units, alternatives, witnesses, intersections, unions, arithmetic, gaps and canonical bytes validated. **25 representative adversarial mutations were rejected.** Separate-process replay reproduced all seven scientific files with **exact byte equality**. Hashes are frozen; the manifest excludes its own recursive hash, whose digest is recorded in the verification receipt.',
        '',
        'Scientific outputs: `stage_c_review.json`, `stage_c_statistics.json`, `STAGE_C_REVIEW.md`, `stage_c_validation.json`, `stage_c_hashes.json`, `stage_c_method.md`, and `stage_c_builder.py`. The full cell/span/unit/alternative ledger is in the review JSON. Reverify with `python -B stage_c_builder.py verify`. After all gates passed, this report was copied byte-for-byte to `.local/codex-result.md`.',
        '',
        'Blindness attestation — access:',
        '',
        '| Excluded category | Access |',
        '|---|---|',
    ]
    lines += ['| '+k+' | NO |' for k in EXCLUDED]
    lines += ['', 'These exclusions refer to external evidence; native parent text and identity fields inside the authenticated packet were permitted evidence.', '', NEXT, '']
    return '\n'.join(lines).encode('utf-8')


def resource_address(r, n):
    return r['resource_ledger'][n-1]['resource']['address']


def check_hashes(blobs, manifest):
    need(set(manifest['scientific_sha256']) == set(NAMES)-{'stage_c_hashes.json'}, 'Hash scope')
    for name, digest in manifest['scientific_sha256'].items():
        need(sha(blobs[name]) == digest, 'Scientific hash: '+name)
    need(manifest['original_input_sha256'] == INPUT_HASHES, 'Original hash manifest')
    need(manifest['handoff_report_sha256'] == sha(blobs['STAGE_C_REVIEW.md']), 'Handoff hash')


def generate(p):
    r = build_review(p)
    s = statistics(r)
    validate_review(p, r, build_review(p))
    validate_statistics(r, s)
    mutations = mutation_checks(p, r, s)
    # Independently exercise the hash checker with a representative data mutation.
    demo = {name: name.encode() for name in NAMES if name != 'stage_c_hashes.json'}
    demo_manifest = {'scientific_sha256': {k: sha(v) for k, v in demo.items()},
                     'original_input_sha256': INPUT_HASHES,
                     'handoff_report_sha256': sha(demo['STAGE_C_REVIEW.md'])}
    check_hashes(demo, demo_manifest)
    demo['stage_c_review.json'] += b'corruption'
    try:
        check_hashes(demo, demo_manifest)
    except ValueError:
        mutations.append({'mutation': 'scientific_hash_corruption', 'result': 'REJECTED_AS_REQUIRED'})
    else:
        raise ValueError('Hash mutation accepted')
    need(len(mutations) == 25, 'Mutation count')
    validation = {'schema': 'stage-c-validation-v1', 'status': 'PASS',
                  'resources': 222, 'obligations': 3, 'expected_cells': 666, 'actual_cells': 666,
                  'duplicates': 0, 'missing': 0, 'unexpected': 0, 'unresolved': 0,
                  'original_packet_preserved': True, 'native_identity_and_span_checks': 'PASS',
                  'units_and_alternatives': 'PASS', 'independent_subset_witness_check': 'PASS',
                  'intersections_and_task_arithmetic': 'PASS', 'gap_records': 'PASS',
                  'same_primary_self_review': 'PASS', 'blindness_attestation': 'PASS',
                  'adversarial_mutations': mutations,
                  'separate_process_replay': {'required': True, 'exact_bytes_required': list(NAMES),
                                              'observed_receipt': '.scratch/verification_receipt.json',
                                              'note': 'The verify/handoff commands enforce this gate; this deterministic file is not its own execution receipt.'},
                  'semantic_truth_limit': 'Verification replays and protects the primary judgment; no second semantic reviewer is implied.'}
    blobs = {'stage_c_review.json': canonical(r), 'stage_c_statistics.json': canonical(s),
             'STAGE_C_REVIEW.md': report(r, s), 'stage_c_validation.json': canonical(validation),
             'stage_c_method.md': METHOD.encode(), 'stage_c_builder.py': (ROOT/'stage_c_builder.py').read_bytes()}
    manifest = {'schema': 'stage-c-hashes-v1', 'original_input_sha256': INPUT_HASHES,
                'canonical_payload_sha256': PAYLOAD_HASH,
                'scientific_sha256': {k: sha(v) for k, v in sorted(blobs.items())},
                'handoff_report_sha256': sha(blobs['STAGE_C_REVIEW.md']),
                'self_hash_policy': 'This manifest excludes itself; its exact digest is recorded in the external verification receipt.',
                'scratch_policy': 'Operational scratch and verification receipt excluded from scientific hashes.'}
    blobs['stage_c_hashes.json'] = canonical(manifest)
    check_hashes(blobs, manifest)
    return blobs


def inside(path):
    path = path.absolute()
    need(path == ROOT or ROOT in path.parents, 'Destination outside workspace')
    current = path
    while current != ROOT:
        if current.exists():
            no_reparse(current)
        current = current.parent
    no_reparse(ROOT)
    return path


def write_outputs(destination, blobs):
    destination = inside(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        target = destination/name
        if target.exists():
            no_reparse(target)
        if target == ROOT/'stage_c_builder.py':
            need(target.read_bytes() == blobs[name], 'Builder changed')
        else:
            target.write_bytes(blobs[name])


def verify():
    p = authenticate()
    expected = generate(p)
    actual = {}
    for name in NAMES:
        path = ROOT/name
        no_reparse(path)
        actual[name] = path.read_bytes()
    check_hashes(actual, json.loads(actual['stage_c_hashes.json']))
    for name in NAMES:
        need(actual[name] == expected[name], 'Exact authored bytes: '+name)
    replay = inside(ROOT/'.scratch'/'replay')
    child = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'stage_c_builder.py'),
                            'emit', str(replay)], cwd=ROOT, capture_output=True, text=True, check=False)
    need(child.returncode == 0, 'Separate-process replay failed: '+child.stderr)
    for name in NAMES:
        need((replay/name).read_bytes() == actual[name], 'Separate-process byte mismatch: '+name)
    authenticate()
    receipt = {'status': 'PASS', 'separate_process_exit_code': child.returncode,
               'exact_byte_matches': {name: True for name in NAMES},
               'scientific_sha256_including_manifest': {name: sha(actual[name]) for name in NAMES},
               'original_packet_preserved': True, 'adjudication_complete': True,
               'self_review_complete': True, 'blindness_attested': True,
               'hashes_frozen': True, 'task_interpretation_gap_preserved': True,
               'local_absent_at_this_verification': not (ROOT/'.local').exists()}
    (ROOT/'.scratch'/'verification_receipt.json').write_bytes(canonical(receipt))
    return receipt


def main():
    need(len(sys.argv) >= 2, 'Use build, verify, emit, or handoff')
    action = sys.argv[1]
    if action in {'build', 'emit'}:
        if action == 'build':
            need(not (ROOT/'.local').exists(), '.local must not exist before handoff')
        p = authenticate()
        blobs = generate(p)
        target = ROOT if action == 'build' else Path(sys.argv[2])
        if action == 'emit':
            need(inside(target) == ROOT/'.scratch'/'replay', 'Only the workspace scratch replay destination is allowed')
        write_outputs(target, blobs)
        print('PASS: deterministic scientific outputs emitted; no handoff created')
    elif action == 'verify':
        receipt = verify()
        print(json.dumps(receipt, indent=2))
    elif action == 'handoff':
        need(not (ROOT/'.local').exists(), 'Initial handoff requires .local absent')
        receipt = verify()
        need(receipt['status'] == 'PASS' and receipt['local_absent_at_this_verification'], 'Handoff gates')
        path = inside(ROOT/'.local')
        path.mkdir()
        report_bytes = (ROOT/'STAGE_C_REVIEW.md').read_bytes()
        (path/'codex-result.md').write_bytes(report_bytes)
        need((path/'codex-result.md').read_bytes() == report_bytes, 'Handoff bytes')
        authenticate()
        handoff = {'status': 'PASS', 'all_gates_passed_before_local_creation': True,
                   'report_sha256': sha(report_bytes), 'exact_report_copy': True,
                   'hash_manifest_sha256': sha((ROOT/'stage_c_hashes.json').read_bytes())}
        (ROOT/'.scratch'/'handoff_receipt.json').write_bytes(canonical(handoff))
        print(json.dumps(handoff, indent=2))
    else:
        raise ValueError('Unknown action')


if __name__ == '__main__':
    main()
