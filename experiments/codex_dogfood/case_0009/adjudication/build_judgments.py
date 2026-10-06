"""Independent human-authored information judgments; no repository imports."""
import argparse
from stage_c import (ROOT, PINNED, PAYLOAD, canonical, load_packet, qualification,
                     resource_identity, sha, statistics, validate, write_new)

# Each row defines one semantic information unit, not one filename requirement.
# Resource indices refer exclusively to the sealed archive order. Spans are 1-based inclusive.
UNITS = {
 'member-decisions': ('Explicit caller decision fields and supported/abstained/unresolved/contradicted states.', [(106,28,100)]),
 'complete-support': ('Every complementary member must be recorded SUPPORTED; contradiction remains distinct.', [(106,163,215)]),
 'resolution-view': ('Exact immutable candidate frame, unique member decisions, absent records and independent competitors.', [(108,33,121)]),
 'promotion': ('Explicit promotion rejects partial support, reuses WitnessSet and preserves basis plus member-decision evidence.', [(107,29,75)]),
 'assessment-shape': ('Immutable caller assessment contains obligation/frame/disposition and aggregates distinct witness targets.', [(85,80,114)]),
 'all-any': ('ALL members in a witness set are complementary; ANY complete accepted alternative suffices.', [(103,41,59),(104,324,337),(7,124,129)]),
 'accepted-boundary': ('Accepted alternatives belong to the obligation; promotion cannot silently register an alternative.', [(103,62,94),(107,67,75),(91,360,369)]),
 'independent-competitors': ('Competing hypotheses remain independently queryable, never combined into one alternative.', [(108,112,121),(91,347,358)]),
 'task-frame': ('Task interpretation validates task-local obligation identities, uniqueness and anchor membership.', [(119,33,64)]),
 'candidate-frame': ('Candidate hypotheses require known obligations and exact resource occurrence membership in retained snapshot.', [(87,285,359)]),
 'decision-lineage': ('Resolution requires exact view/hypothesis/member and criterion; basis must be exact attached evidence with matching repository/snapshot.', [(106,65,160)]),
 'snapshot-occurrence': ('An observed resource occurrence carries address and content identity; snapshot lookup returns exact observed occurrence.', [(180,64,72),(181,34,61)]),
 'evidence-frame': ('Assessment evidence references are repository/snapshot qualified; readiness checks every applicability and witness reference.', [(85,37,62),(104,294,321),(104,364,387)]),
 'applicability-values': ('Applicability is separate from disposition and requirement status, including unassessed/applies/does-not-apply.', [(85,18,34)]),
 'deferred-values': ('Deferred discovery names observation and reason plus explicit caller handoff acceptance; only deferred dispositions carry it.', [(85,65,77),(85,106,114)]),
 'conditional-consistency': ('Conditional applicability needs frame evidence; explicit non-applicability forbids supported witnesses and resolved requires applies.', [(104,294,321),(104,340,361)]),
 'deferred-readiness': ('Accepted deferral permits conditional handoff; unaccepted deferral and abstention leave mandatory coverage incomplete.', [(104,253,291)]),
 'readiness-entry': ('Caller supplies assessments to readiness; exact identity coverage and frame checks yield immutable diagnostics without semantic inference.', [(104,107,176)]),
 'readiness-alternative': ('Readiness returns the first complete accepted alternative and rejects inconsistent disposition.', [(104,324,361)]),
 'promotion-no-mutation': ('Promotion produces values without mutating assessment or readiness and leaves candidate support separate from satisfaction.', [(107,29,75),(108,174,183)]),
 'public-assessment-api': ('Localization public imports and __all__ expose assessment, obligation and readiness APIs.', [(84,4,19),(84,27,72)]),
 'public-resolution-api': ('Resolution package publicly exports explicit promotion, resolution views and dispositions.', [(105,4,24)]),
 'dependency-direction': ('Localization may consume native RI/Retrieval but cannot depend on Context Planning, agent loops or experiment code.', [(7,48,64)]),
 'package-conventions': ('Responsibility-focused package/module ownership and mirrored test structure; reusable source excludes experiment composition.', [(0,54,63),(0,151,165)]),
 'project-conventions': ('Python >=3.12, src/devtools wheel package and development dependency groups define package environment.', [(64,1,24)]),
 'support-test': ('Existing tests distinguish complete, partial, abstained, contradicted and unrecorded support; promotion rejects incomplete support.', [(372,117,177)]),
 'competition-test': ('Tests preserve competing hypotheses independently and deterministic order without assessment mutation.', [(372,180,195)]),
 'lineage-test': ('Tests reject foreign task/obligation, stale view, copied member evidence, duplicates and invalid repository/snapshot.', [(372,198,322)]),
 'promotion-readiness-test': ('Existing test proves complementary promotion retains native basis and decision and needs caller assessment to change readiness.', [(372,325,410)]),
 'alternative-test': ('Kernel tests enforce all-member complementarity and any complete alternative.', [(380,310,352)]),
 'conditional-test': ('Kernel tests establish explicit conditional applicability and frame-qualified non-applicability.', [(380,374,425)]),
 'deferral-test': ('Kernel tests distinguish accepted named deferred discovery from unaccepted deferral.', [(380,469,502)]),
 'assessment-frame-test': ('Kernel tests reject duplicate/foreign assessment identities and stale/foreign evidence frames.', [(380,513,560)]),
 'doc-authority': ('Documentation map identifies central architecture authority and behavior-change update workflow.', [(61,3,11),(61,397,403)]),
 'architecture-bridge': ('Central architecture current resolution seam and downstream caller assessment/readiness claims must describe new bridge accurately.', [(2,923,931)]),
 'package-bridge-doc': ('Package overview owns exact resolution/promotion API narrative and caller-created assessment seam.', [(91,304,369)]),
 'continuity-doc': ('Continuity view owns current capability seam from resolution through assessments/readiness.', [(8,119,148)]),
 'validation-invocation': ('Supported command runs tests excluding experiments before collection, preserves gates and exit status; separate static checks are required.', [(60,3,44)]),
 'validation-selection': ('Operational helper selects tests/ with tests/experiments/ ignored and propagates pytest exit code.', [(65,14,27)]),
 'validation-config': ('Project pytest enforces strict config/markers, branch coverage and 100% production coverage; Ruff/mypy scope remains configured.', [(64,34,78)]),
}

# One explicitly sufficient all-of set per obligation, except the two independently
# sufficient source and authoritative semantic documentation routes for alternatives.
SPECS = {
 'bridge': (['member-decisions','complete-support','resolution-view','promotion','assessment-shape'], [[106,108,107,85]], [87,91,372,103,104,105,8,2,10]),
 'alternatives': (['all-any','accepted-boundary','independent-competitors'], [[103,104,107,108],[7,91]], [87,106,85,372,380,2,8,10,363]),
 'frame': (['task-frame','candidate-frame','decision-lineage','snapshot-occurrence','evidence-frame'], [[119,87,106,180,181,85,104]], [101,108,107,91,372,380,363,178,175,239]),
 'applicability': (['applicability-values','deferred-values','conditional-consistency','deferred-readiness'], [[85,104]], [103,91,7,380,8,2,10]),
 'readiness': (['assessment-shape','readiness-entry','readiness-alternative','deferred-readiness','promotion-no-mutation'], [[85,104,107,108]], [119,103,91,372,380,239,8,2,10]),
 'package': (['public-assessment-api','public-resolution-api','dependency-direction','package-conventions','project-conventions'], [[84,105,7,0,64]], [83,86,91,106,107,108,2,10,61,66]),
 'tests': (['support-test','competition-test','lineage-test','promotion-readiness-test','alternative-test','conditional-test','deferral-test','assessment-frame-test'], [[372,380]], [363,365,366,367,368,370,374,379,106,107,108,85,104,103]),
 'documentation': (['doc-authority','architecture-bridge','package-bridge-doc','continuity-doc'], [[61,2,91,8]], [0,7,10,12,63,84,105]),
 'validation': (['validation-invocation','validation-selection','validation-config'], [[60,65,64]], [0,57,524]),
}

RATIONALES = {
 'bridge': 'The task expressly adds a batch conversion from completely supported hypotheses using existing explicit promotion contracts.',
 'alternatives': 'The task requires caller-selected accepted alternatives, complementary members and independent competing hypotheses.',
 'frame': 'The task expressly requires rejection of foreign or stale task/obligation/repository/snapshot provenance.',
 'applicability': 'The batch API must preserve applicability, explicit non-applicability and named deferral as distinct caller decisions even for unconditional bridge execution.',
 'readiness': 'The task requires integrating produced assessments with existing readiness while retaining all input state.',
 'package': 'The new reusable public integration must follow the existing package exports and dependency boundaries.',
 'tests': 'The task explicitly asks focused tests; existing behavioral and fixture contracts are necessary to extend them accurately.',
 'documentation': 'The task expressly requires governing architecture and package updates; the archive identifies their authority and current seam.',
 'validation': 'The task expressly requires protected development validation; locating its scope precedes future execution.',
}


def build():
    manifest, resources = load_packet()
    frame = qualification(manifest)
    obligations = []
    cells = []
    frozen = {o['identity']: o for o in manifest['obligations']}
    for name in sorted(SPECS):
        unit_ids, alternatives, helpful = SPECS[name]
        acceptable = []
        required = set()
        for ordinal, indices in enumerate(alternatives, 1):
            witnesses = []
            for index in sorted(indices, key=lambda i: resources[i]['address']):
                resource = resources[index]
                supports = []
                for unit in sorted(unit_ids):
                    for resource_index, start, end in UNITS[unit][1]:
                        if resource_index == index:
                            lines = resource['content'].splitlines(keepends=True)
                            supports.append({'unit': unit, 'span': {'start_line': start,
                                'end_line': end, 'excerpt': ''.join(lines[start-1:end])}})
                if not supports:
                    raise ValueError('Witness has no required information')
                witnesses.append({'resource': resource_identity(resource), 'supports': supports})
            required.update(indices)
            acceptable.append({'identity': f'{name}:{ordinal}', 'member_semantics': 'ALL',
                               'witnesses': witnesses})
        obligations.append({'identity': name, 'frozen_definition': frozen[name],
            'applicable': True, 'applicability_reason': RATIONALES[name],
            'required_units': sorted(unit_ids), 'alternative_semantics': 'ANY',
            'acceptable_alternatives': acceptable, 'discovery_prerequisites': [],
            'repository_information_gaps': [], 'unresolved_questions': []})
        for index, resource in sorted(enumerate(resources), key=lambda pair: pair[1]['address']):
            label = 'REQUIRED' if index in required else 'HELPFUL_ONLY' if index in helpful else 'UNNECESSARY'
            unit_refs = sorted({s['unit'] for a in acceptable for w in a['witnesses']
                                if w['resource'] == resource_identity(resource) for s in w['supports']})
            reason = ('Contains necessary information in an explicitly sufficient witness alternative.' if label == 'REQUIRED'
                      else 'Provides neighboring implementation, corroboration, navigation or test context; not needed by a sufficient alternative.' if label == 'HELPFUL_ONLY'
                      else 'Contains no additional information needed for this obligation under the frozen task scope.')
            cells.append({'frame': frame, 'obligation': name, 'resource': resource_identity(resource),
                          'label': label, 'required_units': unit_refs, 'reason': reason})
    judgments = {'schema': 'case-0009-independent-stage-c-gold-v1', 'frame': frame,
        'task': manifest['task'], 'input_digests': {**PINNED, 'resources_payload': PAYLOAD},
        'resources': sorted([resource_identity(r) for r in resources], key=lambda r: r['address']),
        'obligations': obligations, 'cells': cells,
        'information_units': [{'identity': name, 'information': UNITS[name][0],
            'inferability': 'INFERABLE_AT_START', 'inferability_reason': 'Existing sealed archive text establishes this contract by ordinary inspection.',
            'discovery_prerequisites': []} for name in sorted(UNITS)],
        'task_gap': {'status': 'NONE', 'reason': 'The nine obligations jointly cover bridge implementation contracts, alternatives, frame integrity, caller decisions, readiness, package constraints, tests, documentation and validation. Boundedness, duplicate rejection and contradiction separation fall within those contracts.'},
        'repository_gap': {'status': 'NONE', 'reason': 'Existing contracts and sources suffice to implement the requested bridge. Future bridge code, new tests and validation outcomes are implementation work, not missing repository evidence.'},
        'blindness_attestation': {name: 'NO' for name in (
            'parent/sibling filesystem accessed', 'repository checkout accessed', 'Git history accessed',
            'previous provisional gold accessed', 'Arm A accessed', 'Arm B accessed',
            'treatment rank/score accessed', 'analyzer diagnostics accessed',
            'confirmation accessed', 'Stage D performed')},
    }
    validate(judgments, manifest, resources)
    data = canonical(judgments)
    return {'judgments.json': data, 'gold_statistics.json': canonical(statistics(judgments)),
            'judgments.sha256': (sha(data) + '  judgments.json\n').encode('ascii')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Rebuild in memory and compare exact bytes')
    args = parser.parse_args()
    artifacts = build()
    if args.check:
        for name, data in artifacts.items():
            if (ROOT / name).read_bytes() != data:
                raise ValueError(f'Replay mismatch: {name}')
        print('Exact deterministic replay verified')
    else:
        write_new(artifacts)
        print('Frozen complete independent Stage C gold')


if __name__ == '__main__':
    main()
