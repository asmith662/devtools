"""Independent semantic decisions and deterministic frozen-content witnesses."""
from __future__ import annotations

from pathlib import Path
import sys

import stage_c as sc

P = 'src/devtools/context/planning/'
R = 'src/devtools/context/repository/'
F = 'src/devtools/context/python/function/'
T = 'tests/context/'
A = 'docs/architecture.md'
OV = P + 'docs/overview.md'


class Adjudication:
    def __init__(self, payload):
        self.resources = {r['address']: r for r in payload['resources']}
        self.units = {}

    def unit(self, identity, statement, witnesses):
        """Each supplied span is an independently addressable support record."""
        supports = []
        for ordinal, (address, beginning, ending) in enumerate(witnesses, 1):
            resource = self.resources[address]
            content = resource['content']
            start = content.index(beginning) if beginning else 0
            end = content.index(ending, start + len(beginning)) if ending else len(content)
            excerpt = content[start:end]
            supports.append({
                'identity': f'{identity}.support-{ordinal}',
                'resource_identity': {'repository_id': sc.FRAME['repository_id'],
                                      'snapshot_id': sc.FRAME['snapshot_id'], 'address': address},
                'content_identity': resource['content_identity'],
                'character_start': start, 'character_end_exclusive': end,
                'start_line': content[:start].count('\n') + 1,
                'end_line': content[:end-1].count('\n') + 1,
                'excerpt': excerpt, 'excerpt_sha256': sc.sha(excerpt.encode('utf-8')),
                'resource_utf8_sha256': sc.sha(content.encode('utf-8')),
            })
        self.units[identity] = {
            'identity': identity, 'statement': statement, 'supports': supports,
            'inferability': 'INFERABLE_AT_START', 'inherent_discovery_prerequisites': [],
            'inferability_reason': 'Exact existing contract is available by ordinary inspection of the frozen content.',
        }

    def alternative(self, identity, assignments, explanation):
        members = []
        addresses = set()
        for unit_id, ordinals in sorted(assignments.items()):
            selected = [self.units[unit_id]['supports'][i-1] for i in ordinals]
            addresses.update(s['resource_identity']['address'] for s in selected)
            members.append({'unit_id': unit_id, 'support_ids': [s['identity'] for s in selected]})
        return {'identity': identity, 'all_of': members,
                'resource_addresses': sorted(addresses), 'explanation': explanation}


def decisions(payload):
    d = Adjudication(payload)
    u = d.unit
    # Ownership: two independently adequate current documentation witnesses.
    u('planning-owner', 'The capability belongs to devtools.context.planning, the production owner of explicit DisclosurePlan and ContextDisclosure.', [
        (OV, 'The devtools.context.planning package owns', '~~~text'),
        (A, 'The first common Context Planning foundation', 'Filesystem Resources remain'),
        ('docs/documentation_map.md', 'The [Context Planning package]', 'The adjacent `context.python.imports`'),
    ])
    u('planning-boundary', 'Caller-directed choice and materialization are Context responsibilities; retrieval, automatic planning, sufficiency and agent recovery are outside this increment.', [
        (OV, 'A caller supplies a purpose', '~~~text'),
        (A, 'The first common Context Planning foundation', 'Filesystem Resources remain'),
        ('docs/documentation_map.md', 'The [Context Planning package]', 'The adjacent `context.python.imports`'),
    ])
    u('adapter-direction', 'The Python-specific choice adapts to the common materialized item; the common Planning facade depends on its own plan/resource/materialization/rendering modules, preserving the Python-to-Planning dependency direction.', [
        (F+'planned_reference.py', 'from devtools.context.planning.materialization', 'if TYPE_CHECKING:'),
        (P+'__init__.py', 'from devtools.context.planning.materialization', '__all__ ='),
    ])
    # Exact retained source and existing range mechanism, not a future option.
    u('retained-occurrence', 'RepositoryResourceOccurrence retains the exact addressed content string, independent content identity, encoding and original byte size.', [
        (R+'resource.py', 'class RepositoryResourceOccurrence:', 'def _validate_sha256'),
    ])
    u('observation-text', 'Observation reads canonical TEXT through the filesystem substrate and retains its content, encoding and byte size; materialization consumes the resulting snapshot rather than reopening a path.', [
        (R+'observation.py', '    file = cast(', 'def _semantic_digest'),
    ])
    u('decode-preservation', 'The text codec decodes raw bytes directly, preserving source newline characters; invalid or unknown encodings fail rather than normalizing source.', [
        ('src/devtools/resources/filesystem/codecs/text.py', '    def decode(', '    def encode('),
    ])
    u('python-range-coordinates', 'Existing Python source coordinates have one-based lines, zero-based UTF-8 byte columns and an exclusive end; this local parser convention is not a universal whole-line representation.', [
        (F+'declarations.py', 'class PythonSourceRange:', 'class PythonModuleResourceDependency:'),
    ])
    u('exact-extraction', 'Existing bounded extraction keeps newline terminators in split lines, translates range coordinates to absolute byte offsets, slices exact UTF-8 bytes and rejects cuts inside a character.', [
        (F+'materialization.py', 'def _extract_source_segment(', 'def _absolute_byte_offset('),
    ])
    u('extraction-bounds', 'Existing extraction rejects reversed ranges, lines outside retained content, invalid byte columns and invalid UTF-8 boundaries; line offsets account for actual retained terminators.', [
        (F+'materialization.py', 'def _extract_source_segment(', 'def _semantic_digest('),
    ])
    # Deterministic semantic identity and ordered lineage.
    u('digest-framing', 'Planning deterministic identities SHA-256 hash the UTF-8 values with an eight-byte big-endian length prefix for every value.', [
        (P+'plan.py', 'def _digest(', None),
    ])
    u('choice-binding', 'The existing whole-resource choice binds representation, purpose, snapshot, repository, occurrence address and exact content identity.', [
        (P+'resource.py', '    def identity(', '    def materialize('),
    ])
    u('plan-binding', 'DisclosurePlan identity binds purpose, snapshot, repository, optional preceding-plan identity and every representation/option identity in choice order.', [
        (P+'plan.py', '    def identity(', 'def plan_disclosures('),
    ])
    u('plan-invariants', 'Plans require a nonblank purpose and at least one choice, reject incompatible purpose/repository/snapshot choices and reject repeated identical choice identities.', [
        (P+'plan.py', '    def __post_init__(', '    @property'),
    ])
    u('content-identity-semantics', 'Content identity is independent of address and uses the decoded-UTF-8-text semantic domain with length-framed exact decoded text; observation snapshot identity binds repository and canonical address/content pairs.', [
        (R+'resource.py', 'class ContentIdentity:', 'class RepositoryResourceOccurrence:'),
        (R+'observation.py', '_CONTENT_IDENTITY_SEMANTICS =', 'class RepositoryObservationError'),
        (R+'observation.py', '    snapshot_id = RepositorySnapshotId(', 'def _observe_resource('),
        (R+'observation.py', '    content_identity = ContentIdentity(', None),
    ])
    # Defensive validation at each implemented boundary.
    u('snapshot-lookup', 'A snapshot carries repository and snapshot identity and retained occurrences; exact-address lookup fails when the selected address is absent.', [
        (R+'snapshot.py', 'class RepositorySnapshot:', None),
    ])
    u('plan-frame-recheck', 'Plan materialization rechecks repository and snapshot together before invoking any option; a mismatch is an observable DisclosureMaterializationError.', [
        (P+'materialization.py', 'def materialize_disclosure_plan(', '    items: list['),
    ])
    u('occurrence-recheck', 'Whole-resource materialization rejects a foreign repository or snapshot, missing selected address and an unequal retained occurrence even when the supplied snapshot ID is unchanged.', [
        (P+'resource.py', '    def materialize(', '        text ='),
    ])
    u('choice-interface', 'Concrete planned options expose purpose, repository, snapshot, representation and deterministic identity plus materialize(snapshot) returning a MaterializedDisclosureItem.', [
        (P+'plan.py', 'class PlannedDisclosure(Protocol):', 'class DisclosurePlan:'),
    ])
    u('materialized-item', 'MaterializedDisclosureItem keeps option identity, representation, exact resource addresses and content identities, rendered text and native provenance as distinct fields.', [
        (P+'materialization.py', 'class MaterializedDisclosureItem:', 'class ContextDisclosure:'),
    ])
    u('realization-alignment', 'A ContextDisclosure has exactly one item per ordered choice and checks both option identity and representation; the materialization loop rechecks each returned item.', [
        (P+'materialization.py', 'class ContextDisclosure:', '    @property'),
        (P+'materialization.py', '    items: list[', None),
    ])
    u('realization-identity', 'Realized disclosure identity binds its plan and ordered item identities, representations, addresses, content identities and exact realized text.', [
        (P+'materialization.py', '    def identity(', 'def materialize_disclosure_plan('),
    ])
    u('retained-native-materialization', 'Whole-resource realization uses retained source, explicit source delimiters, source UTF-8 byte length, address/content metadata and the observed occurrence as native provenance.', [
        (P+'resource.py', '        text =', 'def choose_whole_resource_disclosure('),
    ])
    u('python-native-adaptation', 'The existing Python option delegates its native materialization/rendering and returns both source and target addresses/content identities with the materialized Python value as native provenance.', [
        (F+'planned_reference.py', '    def materialize(', 'def choose_python_qualified_reference_disclosure('),
    ])
    # Rendering and copied model input.
    u('render-order', 'Common rendering preserves materialized order, exact item text and option/representation identity, and retains the ContextDisclosure behind the rendered text.', [
        (P+'rendering.py', 'class RenderedContextDisclosure:', 'def assemble_context_disclosure_model_request('),
    ])
    u('request-copy', 'Assembly places unchanged task text before unchanged rendered Context with explicit delimiters and UTF-8 lengths, then replaces only Prompt while preserving its role and all other ModelRequest fields.', [
        (P+'rendering.py', 'def assemble_context_disclosure_model_request(', None),
    ])
    # Public API shape is established by actual export lists.
    u('planning-facade', 'The public Planning facade exports concrete option/value classes and caller-facing choose/plan/materialize/render/assemble functions through imports and __all__.', [
        (P+'__init__.py', '', None),
    ])
    u('context-facade', 'The public devtools.context facade re-exports common Planning choices, values and functions; additions must follow the corresponding Planning and Context facade convention.', [
        ('src/devtools/context/__init__.py', 'from devtools.context.planning import', 'from devtools.context.python import'),
        ('src/devtools/context/__init__.py', '__all__ =', '    "PythonFunctionAnalysisCandidateResource",'),
        ('src/devtools/context/__init__.py', '    "WholeResourceDisclosureOption",', '    "analyze_python_function_declaration_resources",'),
        ('src/devtools/context/__init__.py', '    "choose_whole_resource_disclosure",', '    "define_repository_text_corpus",'),
    ])
    # Current tests establish concrete invariants, not hypothetical future tests.
    u('test-mixed-plan', 'The mixed-plan fixture establishes deterministic identity, order and lineage changes, retained CRLF/non-ASCII source after deletion, native provenance, rendering order and copied request settings.', [
        (T+'planning/test_plan.py', 'def _snapshot(', 'def test_same_resource_reference_uses_same_plan_boundary('),
    ])
    u('test-plan-rejection', 'Planning tests reject blank/empty/mixed/duplicate choices, stale or missing occurrences and materialized identity/representation or item-count mismatches.', [
        (T+'planning/test_plan.py', 'def test_plan_rejects_mixed_or_duplicate_choices(', None),
    ])
    u('test-utf8-extraction', 'Existing exact-source fixtures require faithful CRLF and non-ASCII multi-line source and UTF-8 byte-column extraction for a non-ASCII single-line declaration.', [
        (T+'python/function/test_materialization.py', 'def _snapshot(', 'def test_rejects_mismatched_snapshot_and_resource_state('),
    ])
    u('test-range-rejection', 'Current source-materialization tests reject stale snapshot/address state, reversed/out-of-content coordinates and UTF-8 character-boundary cuts.', [
        (T+'python/function/test_materialization.py', 'def test_rejects_mismatched_snapshot_and_resource_state(', 'def test_zero_disclosure_materializes_without_resolving_snapshot_source('),
    ])
    u('test-no-reacquisition', 'Current source-materialization tests prohibit filesystem reacquisition, parsing, derivation and retrieval while consuming retained snapshot state.', [
        (T+'python/function/test_materialization.py', 'def test_materialization_does_not_reacquire_parse_derive_or_retrieve(', 'def test_multi_resource_range_is_applied_only_to_its_addressed_resource('),
    ])
    # Narrow authoritative documentation, including explicit behavior claims to update.
    u('package-description', 'The Planning overview documents its implemented representation set, common protocol, purpose/order/lineage, faithful materialization and rendering/assembly boundaries; the new representation belongs in this package contract.', [
        (OV, 'DisclosurePlan binds purpose', 'The caller may construct a later plan'),
    ])
    u('architecture-description', 'The current architecture explicitly enumerates qualified-reference and whole-resource options and the immutable plan/materialization boundary; its supported-form account must describe the new representation.', [
        (A, 'The first common Context Planning foundation', 'Filesystem Resources remain'),
        (A, 'The implemented DisclosurePlan is intentionally narrower', 'Every disclosure stage preserves'),
    ])
    u('taxonomy-description', 'The governing taxonomy distinguishes planned decision, realized disclosure and ModelRequest and explicitly describes the current qualified-reference/whole-resource implementation; preserve this distinction when describing the new form.', [
        ('docs/architecture/taxonomy.md', 'A ContextDisclosure is an identifiable', 'The accepted, unimplemented planning direction'),
    ])
    u('documentation-impact', 'Documentation authority and workflow require exact API behavior in package docs, current system semantics in architecture, and map/architecture updates when navigation or cross-package ownership changes; historical records are not rewritten as current truth.', [
        ('docs/documentation_map.md', '## Update workflow', '## Repository-map retrieval navigation'),
        ('docs/documentation_map.md', '- [Central architecture]', '- [Retrieval foundation]'),
    ])
    # Protected development validation is recorded, never executed here.
    u('protected-profile', 'The authorized future development command is uv run python scripts/validate_development.py; it excludes tests/experiments before collection, preserves project strict/branch/full-production-coverage configuration and propagates pytest failure.', [
        ('docs/development/validation.md', '## Protected development test profile', '## Other quality gates'),
    ])
    u('validation-entrypoint', 'The existing script selects tests/ and --ignore=tests/experiments without replacing project settings, and returns pytest.main exit status.', [
        ('scripts/validate_development.py', 'def pytest_arguments(', None),
    ])
    u('validation-configuration', 'Project tests use strict config/markers and branch coverage with a 100% production gate; Ruff targets Python 3.12 with ALL checks, and mypy is strict over the configured trees.', [
        ('pyproject.toml', '[tool.pytest.ini_options]', None),
    ])
    u('separate-quality-gates', 'Protected testing is followed by the separately documented Ruff lint/format, mypy and diff checks; confirmation validation needs separate authorization and the experiment exclusion must remain.', [
        ('docs/development/validation.md', '## Other quality gates', None),
        ('docs/development/validation.md', 'This profile validates development behavior.', '## Other quality gates'),
    ])

    def one(name, unit_ids):
        return d.alternative(name+'.existing-contracts',
                             {i: list(range(1, len(d.units[i]['supports'])+1)) for i in unit_ids},
                             'All listed units and their selected source supports are complementary; this is one complete existing-contract witness, not future implementation evidence.')

    alternatives = {
        'ownership': [d.alternative('ownership.package-contract', {
            'planning-owner': [1], 'planning-boundary': [1], 'adapter-direction': [1,2]},
            'The package overview supplies explicit owner and boundary; source imports establish the actual adapter direction.'),
            d.alternative('ownership.current-architecture', {
            'planning-owner': [2], 'planning-boundary': [2], 'adapter-direction': [1,2]},
            'The current architecture independently states the same implemented owner and responsibility boundary; source imports establish the adapter direction.')],
        'range': [one('range', ['retained-occurrence','observation-text','decode-preservation',
                               'python-range-coordinates','exact-extraction','extraction-bounds'])],
        'identity': [one('identity', ['digest-framing','choice-binding','plan-binding',
                                     'plan-invariants','content-identity-semantics'])],
        'frame': [one('frame', ['plan-invariants','snapshot-lookup','plan-frame-recheck',
                               'occurrence-recheck','retained-occurrence'])],
        'materialization': [one('materialization', ['choice-interface','materialized-item',
            'realization-alignment','realization-identity','retained-native-materialization',
            'python-native-adaptation','occurrence-recheck'])],
        'assembly': [one('assembly', ['render-order','request-copy'])],
        'package': [one('package', ['planning-facade','context-facade','planning-owner','adapter-direction'])],
        'tests': [one('tests', ['test-mixed-plan','test-plan-rejection','test-utf8-extraction',
                               'test-range-rejection','test-no-reacquisition'])],
        'documentation': [one('documentation', ['package-description','architecture-description',
                            'taxonomy-description','documentation-impact'])],
        'validation': [one('validation', ['protected-profile','validation-entrypoint',
                                         'validation-configuration','separate-quality-gates'])],
    }
    alternatives['ownership'].append(d.alternative('ownership.documentation-map', {
        'planning-owner': [3], 'planning-boundary': [3], 'adapter-direction': [1,2]},
        'The current documentation map independently names the Planning package and bounded responsibilities; source imports establish the adapter direction.'))
    # For package ownership, the package-local owner support is enough. The alternative
    # does not require the architecture excerpt again just because it also supports it.
    alternatives['package'] = [d.alternative('package.public-facades', {
        'planning-facade': [1], 'context-facade': [1,2,3,4], 'planning-owner': [1],
        'adapter-direction': [1,2]}, 'Both actual public facades, package owner and the one-way Python adapter are complementary API/boundary evidence.')]
    for suffix, ordinal in [('current-architecture', 2), ('documentation-map', 3)]:
        alternatives['package'].append(d.alternative('package.'+suffix, {
            'planning-facade': [1], 'context-facade': [1,2,3,4],
            'planning-owner': [ordinal], 'adapter-direction': [1,2]},
            'The same actual facade and adapter witnesses, with an independently adequate current owner documentation witness.'))
    return d, alternatives


def helpful_decisions():
    """Individually bounded useful context that is not needed by a sufficient witness."""
    adr = 'docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md'
    return {
        'ownership': {
            adr: 'Accepted rationale for the same Context/materialization ownership, already fully specified by current owner documentation and imports.',
            'docs/architecture/taxonomy.md': 'Context/ModelRequest semantic vocabulary supplements the narrow current ownership contract.',
            'AGENTS.md': 'General substrate-reuse rules reinforce the owner but do not supply a missing capability boundary.',
            P+'plan.py': 'Shows the caller-directed protocol; owner and dependency information already have complete witnesses.',
        },
        'range': {
            'src/devtools/resources/filesystem/models/text.py': 'Logical lines deliberately omit separators; useful caution when choosing a faithful extractor, not an exact retained-source extraction witness.',
            'src/devtools/resources/filesystem/models/markdown/section.py': 'Has inclusive bounds but normalizes Markdown section content; it is not an acceptable exact-source disclosure extractor.',
            'src/devtools/resources/filesystem/models/markdown/file.py': 'Illustrates normalized section slicing and why it cannot substitute for exact retained text.',
            P+'resource.py': 'Example whole-resource text realization; exact retained-source and bounded extraction units already have their witnesses.',
            T+'python/function/test_materialization.py': 'Concrete CRLF/non-ASCII and invalid-coordinate examples supplement source contracts.',
            T+'repository/test_observation.py': 'Tests confirm exact observed CRLF text and distinct address/content identity.',
            F+'qualified_reference.py': 'A second consumer uses the existing extractor without defining new whole-line semantics.',
        },
        'identity': {
            R+'identity.py': 'Nominal repository wrapper details supplement the choice bindings; this task creates no new repository identity kind.',
            R+'snapshot.py': 'Wrapper and lookup shape supplement the existing identity derivation and binding contracts.',
            R+'document.py': 'Another versioned length-framed address/content representation; unnecessary for the explicit-choice identity.',
            P+'materialization.py': 'Downstream realization identity is judged separately and does not define choice/plan identity.',
            T+'planning/test_plan.py': 'Examples confirm plan order and lineage changes; source defines the exact identity.',
            T+'repository/test_observation.py': 'Repository/occurrence/content identity examples supplement exact identity source.',
            OV: 'Narrative identity summary adds context to the exact source algorithm.',
        },
        'frame': {
            F+'qualified_reference.py': 'Python-specific source/target dependency checks exemplify stronger native fact validation, unnecessary for a resource-only choice.',
            T+'planning/test_plan.py': 'Current common-plan stale/missing rejection examples supplement source checks.',
            T+'python/function/test_qualified_reference.py': 'Python fact and target-frame rejection examples are adjacent contracts, not resource-only frame machinery.',
            R+'observation.py': 'Observation creates a valid retained frame but new disclosure must not perform acquisition.',
        },
        'materialization': {
            OV: 'Narrative account reinforces source item/provenance contracts.',
            F+'qualified_reference.py': 'Full native Python implementation remains delegated and unchanged; its adapter is the necessary common-item integration witness.',
            adr: 'Accepted materialization rationale is already preserved in current concrete contracts.',
            R+'snapshot.py': 'Retained lookup context; the necessary defensive check and item contract are explicit in the chosen source witness.',
        },
        'assembly': {
            P+'materialization.py': 'Defines the upstream item/order account; rendering directly exposes all fields consumed by assembly.',
            'src/devtools/models/interaction/models.py': 'Enumerates current ModelRequest fields; dataclass replacement already copies every non-prompt field without needing to enumerate them.',
            'src/devtools/models/interaction/prompt.py': 'Prompt role/content type context, unnecessary to understand the existing copy implementation.',
            T+'planning/test_plan.py': 'Concrete order/copy assertions supplement the rendering source.',
            F+'request_assembly.py': 'Older Python-specific copied request assembly provides a parallel example, not the common assembly owner.',
            T+'python/function/test_request_assembly.py': 'Older dedicated assembly test examples are adjacent, not the common-plan assembly contract.',
            adr: 'Architectural assembly rationale supplements exact current rendering.',
        },
        'package': {
            'AGENTS.md': 'General cohesive package/substrate rules support the exact existing facade pattern.',
            F+'__init__.py': 'Shows the separate Python facade; the new language-independent resource choice belongs in Planning and Context facades.',
            R+'__init__.py': 'Source identity exports are available but no new Repository API is needed.',
            A: 'Current package ownership summary supplements explicit local owner and public imports.',
        },
        'tests': {
            T+'python/function/test_qualified_reference.py': 'Useful expanded Python-native regression cases; the common-plan mixed fixture already establishes coexistence and preserved native adaptation.',
            T+'repository/test_observation.py': 'Useful acquisition/identity fixtures; the common-plan and exact-source fixtures already establish retained source/frame behavior needed here.',
            T+'python/function/test_rendering.py': 'Older native rendering examples supplement the common-plan deterministic rendering test.',
            T+'python/function/test_request_assembly.py': 'Older native request-copy tests supplement common-plan copied assembly assertions.',
            'tests/scripts/test_validate_development.py': 'Operational validation tests are separate from disclosure/range/frame/assembly regression contracts.',
        },
        'documentation': {
            adr: 'Decision rationale supplies useful semantic-strength context; no accepted cross-package decision changes for an additional explicit representation.',
            'AGENTS.md': 'General documentation-impact rule is useful; documentation authority/workflow already have exact map support.',
            F+'docs/overview.md': 'Python-specific option documentation is useful context; its behavior does not change with the generic resource choice.',
        },
        'validation': {
            'AGENTS.md': 'Operating guide repeats the protected command and prohibition on routine confirmation/live checks; the canonical validation document is sufficient.',
            'tests/scripts/test_validate_development.py': 'Confirms entry-point selection/exit propagation; exact current script and config already establish the contract.',
            'docs/backlog/items/B-0047-protected-development-validation-profile.md': 'Background pressure for the adopted profile, not an additional current validation authority.',
        },
    }


def build(manifest, payload):
    d, alternatives = decisions(payload)
    helpful = helpful_decisions()
    obligations = []
    cells = []
    for frozen in manifest['obligations']:
        oid = frozen['identity']
        selected = alternatives[oid]
        linkage = {}
        for alternative in selected:
            for member in alternative['all_of']:
                unit = d.units[member['unit_id']]
                by_id = {s['identity']: s for s in unit['supports']}
                for sid in member['support_ids']:
                    address = by_id[sid]['resource_identity']['address']
                    linkage.setdefault(address, set()).add(member['unit_id'])
        required_units = sorted({m['unit_id'] for a in selected for m in a['all_of']})
        obligations.append({
            'identity': oid, 'frozen_obligation': frozen,
            'applicability': {'result': 'APPLICABLE', 'frozen_condition': None,
                'reason': 'The frozen requirement is mandatory with no conditional applicability field. Its predicate addresses behavior or completion work expressly requested in the frozen task.'},
            'required_unit_ids': required_units, 'acceptable_alternatives': selected,
            'interpretation_gap': 'NONE', 'repository_information_gap': 'NONE',
            'necessity_rule': 'A resource is REQUIRED exactly when selected support for a required unit belongs to at least one complete acceptable alternative for this obligation.',
        })
        for resource in sorted(payload['resources'], key=lambda r: r['address']):
            address = resource['address']
            units = sorted(linkage.get(address, set()))
            if units:
                label = 'REQUIRED'
                reason = 'Exact support for required information units in a complete alternative: ' + ', '.join(units) + '.'
            elif address in helpful[oid]:
                label = 'HELPFUL_ONLY'
                reason = helpful[oid][address]
            else:
                label = 'UNNECESSARY'
                reason = ('Frozen content supplies no additional information required by this predicate or its sufficient witnesses. '
                          'Other domains, acquisition mechanisms, language analyses, historical records and general neighboring tests do not become necessary for this explicit representation increment.')
            cells.append({'obligation_id': oid, 'resource_address': address,
                          'content_identity': resource['content_identity'], 'label': label,
                          'required_unit_ids': units, 'reason': reason})
    obligations.sort(key=lambda o: o['identity'])
    cells.sort(key=lambda c: (c['obligation_id'], c['resource_address']))
    attestation = {key: 'NO' for key in [
        'parent/sibling filesystem accessed', 'repository checkout accessed', 'Git history accessed',
        'treatment results accessed', 'arm identities accessed', 'parameter configurations accessed',
        'development sensitivity outcomes accessed', 'confirmation accessed', 'Stage D performed',
        'Arm A results accessed', 'challenger results accessed', 'treatment ranks accessed',
        'treatment scores accessed', 'treatment comparison accessed', 'treatment costs accessed',
        'analyzer diagnostics accessed', 'historical/provisional gold accessed',
        'confirmation/reserve accessed', 'effectiveness analysis performed',
    ]}
    gold = {
        'schema': 'case-0010-independent-stage-c-v1', **sc.FRAME,
        'case_identity': manifest['case_identity'], 'task_identity': manifest['task_identity'],
        'task': manifest['task'], 'input_sha256': sc.INPUT_HASHES,
        'canonical_payload_sha256': sc.PAYLOAD_HASH,
        'resource_identity_convention': 'Canonical native address qualified by the frozen repository and snapshot; content identity is retained independently. The sealed archive defines the expected resource frame.',
        'resource_frame': [{'address': r['address'], 'content_identity': r['content_identity']}
                           for r in sorted(payload['resources'], key=lambda r: r['address'])],
        'obligations': obligations, 'information_units': [d.units[k] for k in sorted(d.units)],
        'cells': cells,
        'task_gap': {'result': 'NONE', 'reason': 'The ten predicates jointly cover owner, retained range source, deterministic identity/lineage, frame rejection, native materialization/provenance, copied assembly, exports, focused tests, governing docs and protected validation. Caller-directed inclusive bounds and exclusions constrain those obligations rather than adding a separate information need.'},
        'repository_information_gap': {'result': 'NONE', 'reason': 'Current contracts provide sufficient existing information. Empty-line, non-ASCII, final-line and invalid-inclusive-bound behavior are future feature acceptance work specified by the task, not missing existing evidence. No future implementation result or future validation outcome is a repository witness.'},
        'task_interpretation': {
            'range_distinction': 'Task requests inclusive one-based whole lines. Existing Python half-open byte-column ranges establish exact-source preservation and defensive extraction, without imposing Python parsing or byte columns on the new caller choice.',
            'unavailable_text': 'Absence of a selected occurrence in retained snapshot state is a failure. Observation admits decoded text; the new option must not reacquire unavailable source.',
            'scope': 'Extend the existing explicit representation boundary. Do not add automatic selection, a representation registry, agent execution or Localization satisfaction machinery.',
            'design_discretion': 'Exact new type/function names, representation discriminator and invalid-bound exception wording remain implementation choices under existing conventions; their absence is not an information gap.',
        },
        'blindness_attestation': attestation,
    }
    stats = sc.statistics(manifest, payload, gold)
    return gold, stats


def artifacts(manifest, payload):
    gold, stats = build(manifest, payload)
    judgment_bytes = sc.canonical(gold)
    return {'judgments.json': judgment_bytes, 'gold_statistics.json': sc.canonical(stats),
            'judgments.sha256': (sc.sha(judgment_bytes) + '  judgments.json\n').encode('ascii')}


def main():
    root = Path(__file__).absolute().parent
    sc.check_workspace(root)
    manifest, payload = sc.load_packet(root)
    result = artifacts(manifest, payload)
    sc.write_outputs(root, result)
    print('Created deterministic Stage C gold; no input changed.')


if __name__ == '__main__':
    main()
