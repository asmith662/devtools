"""Deterministic independent Case 0011 adjudication; no repository imports."""
from __future__ import annotations

import itertools
from pathlib import Path

from stage_c import (ATTESTATIONS, FRAME, INPUTS, OBLIGATIONS, PAYLOAD_SHA256,
                     canonical, compute_statistics, load_packet, require,
                     sha256, validate_judgments)

P = 'src/devtools/context/planning/'
F = 'src/devtools/context/python/function/'
M = 'src/devtools/models/interaction/'
T = 'tests/context/planning/test_plan.py'
A = 'docs/architecture.md'
ADR = 'docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md'
TAX = 'docs/architecture/taxonomy.md'
DOC = P + 'docs/overview.md'

# Each witness is complete for its unit. Ranges within one witness are ALL required.
# Different witnesses of a unit are genuine interchangeable source accounts.
# Unit-level choices expand to explicit, indivisible obligation alternatives below.
UNIT_SPECS = [
 ('U01', 'Common Context Planning owns explicit plan realization followed by rendering and copied assembly, independently of acquisition.',
  [(DOC, [(3, 8), (43, 59)]), (A, [(633, 645)])]),
 ('U02', 'Assembly presents already realized information; capacity is a ceiling and must not silently re-plan, truncate semantics, or promote automatic selection.',
  [(ADR, [(193, 218), (278, 300)]), (TAX, [(775, 788), (823, 842)]),
   (A, [(1057, 1076), (1082, 1098)])]),
 ('U03', 'The common implementation imports ModelRequest and Prompt and the common disclosure type; its rendering/assembly module is the current assembly owner.',
  [(P+'rendering.py', [(6, 20), (45, 50)])]),
 ('U04', 'The Python qualified-reference adapter depends on common materialization and invokes its existing specific materializer/renderer, retaining the one-way adapter boundary.',
  [(F+'planned_reference.py', [(9, 15), (57, 78)])]),
 ('U05', 'Common rendered Context includes its header, purpose, plan and snapshot identities, item count, and ordered item headings/identities followed by unchanged item.text; joining performs no newline normalization.',
  [(P+'rendering.py', [(23, 42)])]),
 ('U06', 'Existing assembly counts context.text encoded as UTF-8 separately from task text, embeds each unchanged string with the existing LF framing, and replaces only Prompt while retaining its role.',
  [(P+'rendering.py', [(45, 70)])]),
 ('U07', 'The frozen common assembly signature accepts a RenderedContextDisclosure and has no capacity argument or admission check; existing calls assemble all of context.text.',
  [(P+'rendering.py', [(45, 70)])]),
 ('U08', 'Existing common invalid plan/disclosure admission uses descriptive local messages and the ValueError family.',
  [(P+'materialization.py', [(20, 21), (43, 51)]),
   (P+'plan.py', [(66, 86)])]),
 ('U09', 'At least one established optional numeric admission precedent is needed: either request output-token validation using ValueError or nonnegative usage validation using TypeError/ValueError. Each admits None, rejects bool/non-int values and provides descriptive local errors. The precedent domain range must not override the task ceiling range.',
  [(M+'models.py', [(12, 18)]), (M+'usage.py', [(15, 29)])]),
 ('U10', 'ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools, including typed admission and unique Tool names.',
  [(M+'models.py', [(98, 138)])]),
 ('U11', 'Prompt is a frozen dataclass with exactly content and role; copied assembly must retain role while changing content.',
  [(M+'prompt.py', [(7, 12)])]),
 ('U12', 'DisclosurePlan is immutable and binds purpose, repository and snapshot, ordered disclosures and optional lineage; it rejects blank purpose, empty choices, mismatched frames/purpose and duplicate choices.',
  [(P+'plan.py', [(52, 86)])]),
 ('U13', 'The plan identity binds purpose, snapshot, repository, preceding-plan lineage and each representation/option identity in disclosure order through length-framed UTF-8 hashing.',
  [(P+'plan.py', [(88, 102), (122, 128)])]),
 ('U14', 'MaterializedDisclosureItem retains option identity, representation, addresses, content identities, text and native_provenance; immutable ContextDisclosure requires one matching item per ordered plan choice.',
  [(P+'materialization.py', [(24, 51)])]),
 ('U15', 'The realized disclosure identity binds its plan, item identities/representations, addresses, content identities and exact text in order.',
  [(P+'materialization.py', [(53, 70)])]),
 ('U16', 'Common materialization verifies repository/snapshot agreement, calls each chosen option in order, verifies its returned identity and representation, and publishes ContextDisclosure only after every item succeeds.',
  [(P+'materialization.py', [(73, 92)])]),
 ('U17', 'Whole-resource materialization rejects stale/foreign, missing or different occurrences, emits the exact retained content with its own headings/separators and byte count, and preserves occurrence provenance and content identity.',
  [(P+'resource.py', [(50, 86)])]),
 ('U18', 'The qualified-reference plan option binds purpose/repository/snapshot and option identity from native support and passes both source/target addresses, content identities, rendered text and native materialized provenance into the common item.',
  [(F+'planned_reference.py', [(29, 78)])]),
 ('U19', 'Qualified-reference admission verifies purpose, analysis/fact membership and supported resolution route; materialization rechecks membership, source repository/snapshot/address and retained source content.',
  [(F+'qualified_reference.py', [(95, 157)])]),
 ('U20', 'Qualified-reference materialization verifies target snapshot, resource/dependency identity, retained target occurrence, qualified-resolution support and declaration-analysis membership before extracting exact source and target spans.',
  [(F+'qualified_reference.py', [(159, 227)])]),
 ('U21', 'Existing exact source extraction translates recorded UTF-8 byte columns, retains original newline bytes, rejects invalid ranges and partial character boundaries, and performs no source rewriting.',
  [(F+'materialization.py', [(104, 152)])]),
 ('U22', 'The planning public package explicitly imports and lists disclosure, rendering and copied-assembly symbols in __all__. The optional argument belongs to that already exported assembly API.',
  [(P+'__init__.py', [(4, 38)])]),
 ('U23', 'The umbrella Context public package reexports the common plan/disclosure/renderer/assembler through explicit imports and __all__ entries.',
  [('src/devtools/context/__init__.py', [(4, 17), (130, 130), (132, 133), (137, 137), (168, 168), (206, 206), (211, 211), (217, 217), (224, 224), (229, 229), (231, 231)])]),
 ('U24', 'The common planning tests create snapshots by writing exact UTF-8 bytes and observing explicitly addressed resources, and build qualified options using the real production analysis pipeline.',
  [(T, [(49, 86)])]),
 ('U25', 'Common mixed-plan tests cover order-sensitive/lineage identities, retained source after filesystem deletion, CRLF/non-ASCII exact text, provenance identity, render order and copied request semantics.',
  [(T, [(89, 185)])]),
 ('U26', 'Common plan tests exercise invalid purpose, empty choices, mismatched purpose/snapshot and duplicate choice rejection with pytest.raises and message fragments.',
  [(T, [(208, 238)])]),
 ('U27', 'Common tests preserve the snapshot identity while replacing resource state to exercise changed-content checks, and separately cover stale snapshots and missing resources.',
  [(T, [(241, 275)])]),
 ('U28', 'Common tests use an incompatible option and direct immutable disclosure construction to exercise item identity/representation and plan cardinality validation.',
  [(T, [(278, 337)])]),
 ('U29', 'Existing adjacent assembly tests pair exact CRLF/non-ASCII rendered source with a fully populated request and assert unchanged task, role, settings, continuation, provider settings and tools.',
  [('tests/context/python/function/test_request_assembly.py', [(70, 124)]),
   ('tests/context/python/function/test_qualified_reference.py', [(104, 165)])]),
 ('U30', 'Existing model-boundary numeric tests parametrize bool, strings, floats and negative values, test None separately, and use ValueError or the existing TypeError/ValueError family as appropriate to the existing control.',
  [('tests/models/interaction/test_models.py', [(31, 48), (281, 288)])]),
 ('U31', 'Existing byte-limit tests accept an exact byte boundary, reject a lower ceiling and negative value, and test explicit None as unlimited.',
  [('tests/resources/filesystem/test_reading.py', [(157, 179)])]),
 ('U32', 'The central architecture documents the implemented common plan/materialization foundation and distinguishes its bounded caller-selected choices from broader accepted assembly/planning semantics.',
  [(A, [(633, 645), (1050, 1076)])]),
 ('U33', 'The package overview describes exact materialization, native provenance, copied assembly and the two supported choices; current capacity discussion selects no token budget or universal cost function.',
  [(DOC, [(35, 68)])]),
 ('U34', 'The documentation map identifies central architecture/taxonomy authority, the common planning package, and the package-first update workflow with conditional map/ADR updates and historical preservation.',
  [('docs/documentation_map.md', [(3, 11), (292, 298), (418, 424)])]),
 ('U35', 'The governing taxonomy distinguishes immutable plans, realized disclosure and ModelRequest, identifies current qualified/whole-resource forms, and prohibits semantic strengthening in materialization/assembly.',
  [(TAX, [(775, 788), (823, 842)])]),
 ('U36', 'The operating guide requires a documentation-impact check for each source change, updates to behavior claims, and architecture updates only for actual architectural changes while preserving historical records.',
  [('AGENTS.md', [(220, 226)])]),
 ('U37', 'The protected executable passes tests/ and --ignore=tests/experiments/ to pytest and propagates its exit code; the operational entry point is scripts/validate_development.py.',
  [('scripts/validate_development.py', [(14, 27)])]),
 ('U38', 'Project pytest uses strict configuration/markers and devtools branch coverage with a 100 percent gate; that existing configuration must remain active in future protected development validation.',
  [('pyproject.toml', [(34, 55)])]),
 ('U39', 'Project style/type checks use Python 3.12, Ruff ALL with declared exceptions and 88-column formatting, and strict mypy across src/tests/experiments with explicit package bases and src path.',
  [('pyproject.toml', [(57, 78)])]),
 ('U40', 'The validation documentation specifies separate uv Ruff lint/format, mypy and diff whitespace gates, including staged diff checking when applicable.',
  [('docs/development/validation.md', [(31, 44)])]),
 ('U41', 'Protected validation is invoked through uv run python scripts/validate_development.py, keeps project coverage/configuration, and excludes the experiment tree before collection; excluded validation requires separate explicit authorization.',
  [('docs/development/validation.md', [(5, 16), (21, 29)])]),
 ('U42', 'After a substantial development task the operating guide requires an ephemeral .local/codex-result.md containing the substantive completion report; it must not become the sole durable decision/evidence location.',
  [('AGENTS.md', [(245, 251)])]),
]

OBLIGATION_UNITS = {
 'ownership': ['U01', 'U02', 'U03', 'U04'],
 'bytes': ['U05', 'U06'],
 'ceiling': ['U07', 'U08', 'U09'],
 'request': ['U06', 'U10', 'U11'],
 'frame': ['U05'] + [f'U{i:02}' for i in range(12, 22)],
 'exports': ['U22', 'U23'],
 'tests': [f'U{i:02}' for i in range(24, 32)],
 'documentation': ['U02'] + [f'U{i:02}' for i in range(32, 37)],
 'validation': [f'U{i:02}' for i in range(37, 42)],
}

APPLICABILITY = {
 'ownership': 'The task explicitly assigns capacity checking to common Context Planning and prohibits a language-adapter or Retrieval dependency; common ownership and an adapter already exist.',
 'bytes': 'The task expressly counts exact rendered UTF-8 Context, including internal headings/separators, and preserves newline behavior; the common renderer and assembler already implement those presentations.',
 'ceiling': 'The requested new optional nonnegative integer control needs existing local numeric/error conventions and the current unbounded assembly boundary. Its new acceptance rules come from the task.',
 'request': 'The task requires copied assembly preserving original task, role and every request field; current immutable request and Prompt values provide those semantics.',
 'frame': 'The task explicitly preserves plan/disclosure order, native provenance and repository/snapshot/content checks across both supported choices; all those contracts already exist.',
 'exports': 'The task calls for public export conventions; the common assembly is already exported at both planning and umbrella Context boundaries.',
 'tests': 'The task expressly requests focused boundary, Unicode/newline, invalid-frame and copied-request tests; applicable current fixtures and assertions exist.',
 'documentation': 'The task expressly requests governing architecture and package documentation updates; the current architecture, taxonomy, package docs and update policies define the relevant claims.',
 'validation': 'The task expressly requires protected development validation with existing tooling configuration; the executable, protected profile docs and project configuration exist.',
}

# Explicit auxiliary examples, selected by their actual inspected contents.
# These do not establish another complete witness alternative for that obligation.
HELPFUL = {
 'ownership': {P+'plan.py', P+'materialization.py', P+'resource.py', P+'__init__.py',
               'docs/documentation_map.md', 'AGENTS.md'},
 'bytes': {P+'resource.py', P+'materialization.py', DOC, A, ADR, TAX, T,
           F+'qualified_reference.py', F+'materialization.py',
           'tests/context/python/function/test_rendering.py',
           'tests/context/python/function/test_materialization.py',
           'tests/context/python/function/test_request_assembly.py',
           'tests/context/python/function/test_qualified_reference.py'},
 'ceiling': {'src/devtools/resources/filesystem/reading.py',
             'tests/resources/filesystem/test_reading.py',
             'tests/models/interaction/test_models.py', T, DOC, ADR, TAX, A,
             'src/devtools/models/benchmarks/runner.py'},
 'request': {T, DOC, A, F+'request_assembly.py', F+'qualified_reference.py',
             'src/devtools/models/interaction/__init__.py',
             'tests/context/python/function/test_request_assembly.py',
             'tests/context/python/function/test_qualified_reference.py',
             'tests/models/interaction/test_models.py'},
 'frame': {T, DOC, A, ADR, TAX, 'src/devtools/context/repository/resource.py',
           'src/devtools/context/repository/snapshot.py',
           'src/devtools/context/repository/observation.py',
           'tests/context/python/function/test_qualified_reference.py',
           'tests/context/python/function/test_materialization.py'},
 'exports': {P+'rendering.py', DOC, A,
             'src/devtools/context/python/function/__init__.py', T,
             'src/devtools/models/interaction/__init__.py'},
 'tests': {P+'rendering.py', P+'plan.py', P+'materialization.py', P+'resource.py',
           F+'planned_reference.py', F+'qualified_reference.py', M+'models.py',
           M+'usage.py', M+'prompt.py', 'pyproject.toml',
           'tests/context/python/function/test_rendering.py',
           'tests/context/python/function/test_materialization.py',
           'tests/context/repository/test_observation.py'},
 'documentation': {P+'rendering.py', P+'plan.py', P+'materialization.py',
                   P+'resource.py', F+'planned_reference.py',
                   'README.md', 'src/devtools/context/python/function/docs/overview.md'},
 'validation': {'AGENTS.md', 'tests/scripts/test_validate_development.py',
                'docs/backlog/items/B-0047-protected-development-validation-profile.md'},
}


def make_support(resource, unit_id, evidence_id, ranges):
    content = resource['content']
    lines = content.splitlines(keepends=True)
    spans = []
    for lo, hi in ranges:
        require(1 <= lo <= hi <= len(lines), 'Adjudicated source range')
        start = sum(len(line) for line in lines[:lo-1])
        end = sum(len(line) for line in lines[:hi])
        excerpt = content[start:end]
        spans.append({'start_line': lo, 'end_line': hi,
                      'line_convention': 'Python str.splitlines(keepends=True), one-based inclusive',
                      'start_character': start, 'end_character': end,
                      'start_utf8_byte': len(content[:start].encode('utf-8')),
                      'end_utf8_byte': len(content[:end].encode('utf-8')),
                      'excerpt': excerpt, 'excerpt_sha256': sha256(excerpt.encode('utf-8'))})
    return {'evidence_id': evidence_id, 'unit_id': unit_id,
            'resource_address': resource['address'],
            'resource_identity': {k: FRAME[k] for k in ('repository_id', 'snapshot_id')} |
                                 {'address': resource['address']},
            'content_identity': resource['content_identity'],
            'source_sha256': sha256(content.encode('utf-8')), 'spans': spans,
            'span_semantics': 'ALL spans are complementary support for this unit witness.'}


def build(manifest, archive):
    resources = {r['address']: r for r in archive['resources']}
    units, support, witnesses = [], [], {}
    for unit_id, statement, sources in UNIT_SPECS:
        witnesses[unit_id] = []
        for index, (address, ranges) in enumerate(sources, 1):
            evidence_id = f'{unit_id}.S{index}'
            witnesses[unit_id].append(evidence_id)
            support.append(make_support(resources[address], unit_id, evidence_id, ranges))
        units.append({'unit_id': unit_id, 'statement': statement,
                      'necessity': 'REQUIRED',
                      'scope': 'SUPPLEMENTAL_TASK_GAP' if unit_id == 'U42' else 'FROZEN_OBLIGATIONS',
                      'inferability': 'INFERABLE_AT_START',
                      'inferability_reason': 'Established by ordinary inspection of already frozen source, tests or governing documentation; no future execution result is needed.',
                      'inherent_discovery_prerequisites': [],
                      'inspection_dependencies': [],
                      'acceptable_unit_witnesses': witnesses[unit_id]})
    evidence = {e['evidence_id']: e for e in support}
    obligation_judgments, cells = [], []
    for obligation_id in OBLIGATIONS:
        ids = OBLIGATION_UNITS[obligation_id]
        alternatives = []
        for index, members in enumerate(itertools.product(*(witnesses[u] for u in ids)), 1):
            alternatives.append({'alternative_id': f'{obligation_id}.A{index:02}',
                                 'all_evidence_ids': list(members),
                                 'all_resource_addresses': sorted({evidence[e]['resource_address'] for e in members}),
                                 'all_required_unit_ids': list(ids),
                                 'acceptance_reason': 'Every listed unit has a complete existing source account; ALL members are complementary. This is a source witness choice, not a future implementation decision.'})
        obligation_judgments.append({'obligation_id': obligation_id,
                                     'applicability': 'APPLICABLE',
                                     'applicability_reason': APPLICABILITY[obligation_id],
                                     'required_unit_ids': ids,
                                     'acceptable_alternatives': alternatives,
                                     'alternative_semantics': 'ANY one complete alternative suffices; ALL its members are required together.',
                                     'inherent_discovery_prerequisites': []})
        necessary = {r for a in alternatives for r in a['all_resource_addresses']}
        for address in sorted(resources):
            matching = sorted({evidence[e]['unit_id'] for a in alternatives
                               for e in a['all_evidence_ids']
                               if evidence[e]['resource_address'] == address})
            if address in necessary:
                label, reason = 'REQUIRED', 'Contributes necessary unit information to at least one complete acceptable alternative.'
            elif address in HELPFUL[obligation_id]:
                label, reason = 'HELPFUL_ONLY', 'Inspected adjacent contract, policy or example aids application; it contributes no necessary unit to a complete alternative for this obligation.'
            else:
                label, reason = 'UNNECESSARY', 'The frozen content contributes no necessary witness unit or selected supporting example for this bounded obligation; other domains and unrelated operations do not establish its required contract.'
            cells.append({'obligation_id': obligation_id, 'resource_address': address,
                          'content_identity': resources[address]['content_identity'],
                          'label': label, 'reason': reason,
                          'required_unit_ids': matching,
                          'complete_alternative_ids': [a['alternative_id'] for a in alternatives
                                                       if address in a['all_resource_addresses']]})
    return {
        'schema': 'case-0011-independent-stage-c-gold-v1',
        'frame': FRAME, 'input_sha256': INPUTS, 'payload_sha256': PAYLOAD_SHA256,
        'task_sha256': INPUTS['task.txt'], 'frozen_obligations': manifest['obligations'],
        'obligation_judgments': obligation_judgments,
        'required_units': units, 'source_support': support, 'cells': cells,
        'resource_frame': [{k: r[k] for k in ('address', 'content_identity', 'byte_size', 'encoding')}
                           for r in sorted(archive['resources'], key=lambda r: r['address'])],
        'task_gaps': [{
            'gap_id': 'G01',
            'statement': 'Mandatory substantial-task completion handoff information is absent from the nine frozen satisfaction criteria.',
            'applicability_reason': 'Implementing the requested behavior, focused tests, documentation and protected validation is a substantial development task under the frozen operating guide.',
            'missing_obligation_scope': 'The nine criteria cover assembly ownership/bytes/limits/preservation/frames/exports/tests/docs/validation, but none requires the local completion-report destination and lifetime.',
            'supplemental_required_unit_ids': ['U42'], 'all_evidence_ids': ['U42.S1'],
            'frozen_obligations_modified': False,
            'handling': 'Retain as a separately supported task gap; do not add an obligation or relabel the frozen matrix on its behalf.'}],
        'repository_information_gaps': [],
        'repository_gap_review': 'No necessary existing repository contract is absent from this packet. Future limit code, future focused tests and future validation outcomes are work products, not repository-information gaps.',
        'task_interpretation_gaps': [
            {'gap_id': 'I01', 'statement': 'The task names an already materialized ContextDisclosure as caller input; the frozen exported assembler accepts RenderedContextDisclosure.',
             'evidence_ids': ['U07.S1', 'U14.S1'],
             'disposition': 'Record the mismatch. Required semantics count the exact common renderer output; the frozen task does not select the future signature or compatibility design.'},
            {'gap_id': 'I02', 'statement': 'The current common plan prohibits zero choices and the renderer always emits nonempty headings, so no ordinary valid common disclosure renders zero bytes.',
             'evidence_ids': ['U12.S1', 'U05.S1'],
             'disposition': 'The task zero-ceiling rule is a generic admission rule; do not invent an empty plan, truncation or zero-header representation to make it reachable.'},
            {'gap_id': 'I03', 'statement': 'The task specifies invalid ceilings and oversize rejection but no exact new argument name, exception class or message; existing optional numeric controls show more than one error convention.',
             'evidence_ids': ['U09.S1', 'U09.S2', 'U08.S1'],
             'disposition': 'Keep both existing numeric precedents as acceptable source accounts. The task supplies nonnegative/None/equality/oversize semantics; the future API choice is not missing repository evidence.'},
            {'gap_id': 'I04', 'statement': 'Native disclosure provenance lives in disclosure/rendered values; ModelRequest has no disclosure-provenance field.',
             'evidence_ids': ['U14.S1', 'U10.S1', 'U03.S1'],
             'disposition': 'Preserve the caller disclosure and its native values under copied assembly. Do not infer a requirement to add a new ModelRequest field.'},
        ],
        'blindness_attestations': {key: 'NO' for key in ATTESTATIONS},
        'review_method': {
            'resource_coverage': 'Every frozen resource identity and content binding participates in every obligation cell; bounded source inspection followed the common API, direct adapters/consumers, tests and governing policies.',
            'necessity_rule': 'REQUIRED iff necessary source evidence participates in at least one explicitly complete alternative. General topical overlap does not establish necessity.',
            'source_closure': 'The frozen common assembler occurs only in its definition, two public exports, package overview and common planning tests; no additional frozen production consumer was found.',
            'task_rule_boundary': 'New numeric range, equality, rejection-before-copy and no-truncation rules originate in the task. Existing source units establish integration/preservation/convention facts, not future behavior.',
            'discovery': 'All necessary existing facts can be inspected at task start. Following imports and documentation links is ordinary source inspection, not an inherent discovery prerequisite.',
            'uncertainty': 'No frozen cell remains unresolved. API interpretation gaps are explicit and do not disguise future implementation outcomes as missing repository information.',
        },
    }


def main():
    targets = ('judgments.json', 'gold_statistics.json', 'judgments.sha256')
    # Refuse the entire write before touching any target, including partial releases.
    for name in targets:
        if Path(name).exists():
            raise FileExistsError('Refusing to overwrite existing Stage C output: ' + name)
    manifest, archive = load_packet()
    judgments = build(manifest, archive)
    validate_judgments(judgments, manifest, archive)
    statistics = compute_statistics(judgments)
    blobs = {'judgments.json': canonical(judgments),
             'gold_statistics.json': canonical(statistics)}
    blobs['judgments.sha256'] = (sha256(blobs['judgments.json']) +
                                '  judgments.json\n').encode('ascii')
    for name in targets:
        with Path(name).open('xb') as stream:
            stream.write(blobs[name])
    print('Built 531 resources x 9 obligations = 4779 cells.')


if __name__ == '__main__':
    main()
