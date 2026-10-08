"""Case 0011 C.5-R v1: local, frozen semantic decisions and deterministic release.

No discovery outside this directory; no repository imports or external evidence.
The matrix and explanations below are reviewer decisions, not lexical rules.
"""
import collections
import gzip
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).absolute().parent
INPUT_HASHES = {
    'C5_INSTRUCTIONS.md': '728ef0710539c8531e816a334a6ac6baee17ca1f0a3c514c4bb4bc50f76a74a7',
    'C5_R_INSTRUCTIONS.md': '9e03ff5059b56590bde97019010ad9230fc81fc6023fd8fe81a42010939d2852',
    'integrity.json': 'd85c45a838586fead1ba25791a5f6d9c5d69db97b249d2a0ba3f3571695bfd66',
    'manifest.json': 'b39d7b9121d07f5a842bbed40f5a876d828d0fa7a82d3900b05f428a622892f1',
    'packet.json.gz': 'da77c2a3e32129eabd3ffe4331ae2a1caef91cffffbd21b728420a953ad7e6f1',
}
ARTIFACTS = {'c5r_v1.py', 'test_c5r_v1.py', 'c5r_v1_adjudication.json',
             'c5r_v1_validation.json', 'c5r_v1_hashes.json'}
OUTPUT = 'c5r_v1_adjudication.json'
LABELS = {'D': 'DIRECTLY_COVERS', 'P': 'PARTIALLY_COVERS',
          '-': 'DOES_NOT_COVER', 'A': 'AMBIGUOUS'}

# U01..U32 follow the frozen packet order; columns N01..N18 follow need order.
# Every cell was considered, including questions outside the unit's obligation.
MATRIX = [
    '----------D-------',  # U01
    '--------P---------',  # U02
    '----------------PP',  # U03
    '---------------P--',  # U04
    '------PP---P-D----',  # U05
    '-----------D------',  # U06
    '--------PP--------',  # U07
    '--------D---------',  # U08
    '--------------D---',  # U09
    '--------PP--------',  # U10
    '----D--------P----',  # U11
    '----------------PP',  # U12
    '-----PDP----------',  # U13
    '--------PP--------',  # U14
    '-D----------------',  # U15
    'P-P--DP-----------',  # U16
    '--PP--PP----------',  # U17
    '----------------PD',  # U18
    '-----------P------',  # U19
    '----------D-------',  # U20
    '-----PDD----------',  # U21
    '--------D---------',  # U22
    '--------P---D-----',  # U23
    '--------D---------',  # U24
    'DP-------P----P---',  # U25
    '----P--------D----',  # U26
    '--DP-----P--------',  # U27
    '--------PP--------',  # U28
    '-----------------D',  # U29
    '--------PP--------',  # U30
    '----D-------------',  # U31
    '---------P-P------',  # U32
]

NEED_FACTS = [
    'the common contract owning copied assembly and its caller-directed planning role',
    'allowed dependency directions and the separation of common planning from adapters and Retrieval',
    'the complete appended rendered payload, its headings, boundaries and separators',
    'UTF-8 encoding and newline fidelity of rendered text',
    'optional integer admission, invalid-type errors and the applicable nonnegative domain',
    'the assembly input and construction boundary at which full-context rejection can precede request copying',
    'the immutable request field inventory and copying mechanism preserving unrelated fields',
    'preservation of the original task text and Prompt role during appending',
    'repository, snapshot, content and plan/item identity checks binding a disclosure to its plan',
    'ordered item realization and retention of exact text and native provenance',
    'the public import and __all__ boundaries exposing assembly and its companion values',
    'existing exact-text, non-ASCII and newline tests and their text fixtures',
    'existing tests distinguishing foreign/stale frames and retained-content mismatches',
    'existing copied-request preservation tests and invalid-argument test conventions',
    'the governing architecture document and its current capacity versus selection contract',
    'package documentation of rendered Context and copied assembly contracts',
    'the established protected development validation entry point and its scope',
    'established test, type and style tooling configuration',
]

# Direct explanations connect complete answers to complete units; the exact
# frozen statements are also embedded in every generated pair record.
DIRECT = {
    (1,11): 'A complete public-boundary answer identifies the planning imports and __all__ entries for the assembler and the renderer/value through which callers supply it. These are exactly this unit\'s export facts.',
    (5,14): 'The preservation-test question calls for the existing checks of original text, role, other fields and copy equivalence. Explaining the common assembly test completely includes its task-before-Context assertion and replacement-back equality, establishing every listed check.',
    (6,12): 'The exact-text fixture question requires how retained test text is made exact. Writing UTF-8 bytes and observing the addressed resources is the complete fixture mechanism stated here, so explaining that fixture establishes the unit.',
    (8,9): 'The source-side repository/snapshot/content binding is part of the requested frame checks. A complete answer must identify the dependency and occurrence frames, address/presence checks and retained-content equality, which exhaust this unit.',
    (9,15): 'Identifying governing architecture for the capacity change requires identifying its canonical authority and the current planning-to-assembly account being extended. The unit establishes precisely that authority and existing architectural scope.',
    (11,5): 'Explaining applicable optional integer conventions includes the request-side None/type/ValueError precedent and distinguishing its positive token domain from the required nonnegative byte domain. Without that distinction the requested applicability question would be incompletely answered.',
    (13,7): 'An account of preserving every request field needs the full immutable request shape: prompt, settings, conversation, provider_settings and tools. That inventory and frozen-dataclass status establish the whole unit.',
    (15,2): 'A complete dependency-boundary answer identifies the allowed ModelRequest/Prompt imports, the type-only ContextDisclosure dependency and absence of adapter/Retrieval dependencies in rendering and assembly. This establishes the complete import-boundary unit.',
    (16,6): 'Locating the safe rejection boundary requires describing the current keyword-only rendered-disclosure input, lack of a ceiling, whole-context handling and final replace construction. Together these establish where rejection precedes the copied request without dropping items.',
    (18,18): 'The test-configuration question directly seeks strict pytest/marker settings and the production branch-coverage threshold. A complete configuration answer includes all of these enforcement settings.',
    (20,11): 'Exposing common assembly to callers includes the outer Context facade, its explicit imports and __all__ entries for the assembler and companion planning values. Explaining that public boundary establishes the entire unit.',
    (21,7): 'The field-preservation mechanism is replacing only prompt through dataclasses.replace and constructing the new Prompt with the original role. A complete copying answer establishes the exact operation and its role retention.',
    (21,8): 'Explaining how appending preserves the Prompt role requires the new Prompt construction with the original role and its installation in a copied request. The single replace/Prompt operation establishes this whole unit.',
    (22,9): 'The target-side binding question includes support/subject frames, presence, dependency identity and retained support equality. Each is part of the requested complete target frame check, with no independent non-frame clause in this unit.',
    (23,13): 'A complete frame-rejection test answer distinguishes changed snapshots, changed content within a retained snapshot identity and missing resources, including the replacement/raises test idiom. These are exactly the test distinctions in the unit.',
    (24,9): 'Retained target resolution and declaration evidence are content/frame bindings. A complete answer includes matching resource/repository/snapshot identities and declaration membership when analysis exists, exhausting the unit.',
    (25,1): 'Identifying the common assembly owner as a contract requires its pipeline responsibility: caller-directed ordered plans, faithful realization, rendering and copied assembly, with automatic selection/Retrieval outside that ownership. This is a single architectural responsibility statement.',
    (26,14): 'The requested invalid-argument tests include parametrized wrong-type/domain cases, descriptive matching, separate None and valid-integer cases. Interpreting those conventions for this task also requires the explicit zero exception, establishing the whole unit.',
    (27,3): 'An exact appended-payload answer must enumerate the header metadata, ordered headings/identities, unchanged item bodies and precise LF separators without normalization. Omitting any of these would leave the requested exact text unspecified.',
    (29,18): 'The type/style configuration answer requires the Python version, Ruff selection/exceptions/line length, and strict mypy scope and import/package settings. These settings exhaust the complete unit.',
    (31,5): 'ModelUsage supplies the matching optional nonnegative integer admission precedent. A complete account of applicable type/domain error conventions establishes None acceptance, bool/non-int TypeError and negative ValueError for this immutable value.',
}

# Each partial decision explicitly separates established and missing semantics.
PARTIAL = {
    (2,9): ('derivation/coverage and analysis-membership consistency relevant to evidence binding', 'blank-purpose admission, supported target/route restrictions and rechecking directly constructed immutable values'),
    (3,17): ('the documented protected entry point and its development-only scope', 'pre-collection exclusion mechanics, retained pytest/coverage settings and propagation of the pytest exit code'),
    (3,18): ('retained pytest configuration and branch coverage with the 100 percent gate', 'the documented entry-point identity, pre-collection exclusion, exit-code propagation and authorization boundary'),
    (4,16): ('documentation of exact materialization, native provenance, supported disclosure choices and appended copied-request Context', 'the overview\'s explicit distinction of future token budgets/universal costs from current behavior'),
    (5,7): ('preservation of original task, role and unrelated request fields', 'the specific test\'s task-before-Context assertion and replacement-back equality assertion'),
    (5,8): ('unchanged original task and Prompt role during appending', 'the test\'s shared settings/conversation/provider checks, placement assertion and replacement-back equality'),
    (5,12): ('the test\'s unchanged task text and task-before-Context placement', 'Prompt role, shared non-text request values and replacement-back equality'),
    (7,9): ('delegation to validated materialization and retention of source/target addresses and content identities', 'the renderer-to-item text handoff and retention of the native materialized value'),
    (7,10): ('renderer-to-item exact text and native materialized-value retention', 'delegation through frame-validated materialization and both source/target address/content identity bindings'),
    (10,9): ('repository/snapshot rejection, returned identity/representation verification and withholding a disclosure until all items validate', 'ordered realization of the selected choices'),
    (10,10): ('realization of each selected option in order', 'repository/snapshot rejection, returned identity/representation verification and all-success publication'),
    (11,14): ('observable optional integer invalid-type/error conventions used by request tests', 'the existing request validator as the implementation precedent and the explicit positive-token versus nonnegative-byte domain distinction'),
    (12,17): ('the protected entry point running tests only', 'separate uv Ruff lint/format, mypy and working/staged diff checks prescribed by the guide'),
    (12,18): ('the separate lint/format/type and working/staged whitespace-check validation requirements', 'the protected command\'s tests-only scope'),
    (13,6): ('immutability supporting rejection without modifying the caller request', 'the complete prompt/settings/conversation/provider_settings/tools field inventory'),
    (13,8): ('the prompt-bearing request whose Prompt is preserved', 'frozen-dataclass status and the complete inventory of other fields'),
    (14,9): ('plan repository/snapshot identities and rejection of mixed frames', 'blank/heterogeneous purposes, empty or duplicate choices, ordered-choice retention and immutable plan shape'),
    (14,10): ('retention of the ordered choices', 'plan immutability, repository/snapshot identities and blank-purpose, empty-choice, mixed-purpose/frame and duplicate-choice admission'),
    (16,1): ('identification of the common assembly entry point as the assembly contract', 'keyword-only rendered input, absent limit argument, full context handling and final replace timing'),
    (16,3): ('assembly of the entire context.text payload', 'keyword-only rendered input, absent limit argument and final copied-request construction timing'),
    (16,7): ('creation of the copied request at the final replace call', 'keyword-only RenderedContextDisclosure input, no existing limit argument and full-context assembly'),
    (17,3): ('separate task/Context envelope boundaries and unchanged appended payload text', 'the context-only UTF-8 length report and preservation of each embedded string\'s newline bytes'),
    (17,4): ('context-only UTF-8 length accounting and unchanged embedded strings/newline bytes', 'the separate outer task and Context envelope structure'),
    (17,7): ('unchanged original task text in copied assembly', 'separate envelope structure, the context-only byte report and context/newline preservation'),
    (17,8): ('unchanged original task in its separate envelope alongside the Context envelope', 'context-only UTF-8 length reporting and exact preservation of context.text and its newlines'),
    (18,17): ('use of established project coverage settings through the protected entry point', 'strict pytest configuration/markers and the precise production branch-coverage threshold as configuration facts'),
    (19,12): ('identification of a retained qualified option used as a text-test fixture', 'construction through module interpretation and production reference analysis before choosing the reference'),
    (21,6): ('final replacement of a copied request, permitting earlier rejection', 'the Prompt constructor and explicit preservation of the original Prompt role'),
    (23,9): ('snapshot/content/presence rejection distinctions', 'their embodiment in common planning tests with replace and pytest.raises'),
    (25,2): ('independence from Retrieval and adapter-side ownership', 'the common owner\'s ordered caller-directed planning and faithful realization/rendering/assembly pipeline'),
    (25,10): ('ordered plans and faithful realization of selected items', 'common pipeline ownership and separation from Retrieval/automatic selection'),
    (25,15): ('the architectural distinction between common Context capacity and automatic selection', 'the complete ordered plan/realization/rendering/copied-assembly responsibility'),
    (26,5): ('None, invalid bool/string/float/integer and valid-integer admission conventions, including zero for bytes', 'the existing tests\' parametrization, descriptive ValueError matching and separate None test structure'),
    (27,4): ('unchanged text with explicit LF separators and no normalization', 'the full header, purpose, plan/snapshot identity, item-count and ordered option-heading layout'),
    (27,10): ('unchanged item text and item order in rendering', 'the complete metadata headings/identities and explicit LF-only separator construction'),
    (28,9): ('foreign/stale frame, missing-resource and retained-occurrence rejection plus resource/content identity bindings', 'unchanged item content and original-occurrence native provenance retention'),
    (28,10): ('unchanged retained text and original-occurrence native provenance', 'foreign/stale frame, missing-resource and unequal-occurrence rejection and resource/content identity bindings'),
    (30,9): ('address/content/option/representation binding and one matching item per ordered plan choice', 'the immutable item\'s exact text and native_provenance retention'),
    (30,10): ('immutable exact-text/native-provenance retention and one item per ordered choice', 'the complete address/content/option/representation identity schema and matching requirements'),
    (32,10): ('unchanged retained source, native whole-resource provenance and rendered order as preservation contracts', 'the mixed-plan test\'s concrete CRLF and non-ASCII qualified/whole-resource fixtures and their test assertions'),
    (32,12): ('CRLF/non-ASCII mixed-plan fixtures, unchanged source text and rendered item ordering', 'the independent native whole-resource provenance assertion'),
}

# Distinct facts required by each unit, used to state why every negative cell
# asks a different question. No label is inferred from these descriptions.
UNIT_FOCUS = [
    'explicit planning-package import and __all__ declarations',
    'qualified-option admission and re-admission restrictions',
    'protected-command execution mechanics and authorization scope',
    'the planning overview\'s current and future capability claims',
    'the particular assertions in the common copied-assembly test',
    'the retained-snapshot text-fixture construction mechanism',
    'the qualified adapter\'s validated handoff and common-item retention',
    'source-side qualified materialization frame/content checks',
    'the governing architecture document\'s canonical authority and existing pipeline scope',
    'common materialization ordering, admission and atomic publication',
    'the request-side optional integer validator and its domain adaptation',
    'the division between the protected test command and other required validation commands',
    'the immutable ModelRequest schema and complete field inventory',
    'the immutable plan\'s structure and all choice/purpose/frame admission restrictions',
    'the actual allowed imports and forbidden dependency directions of common rendering/assembly',
    'the existing assembly signature and final copied-request construction boundary',
    'task/Context envelopes combined with independent UTF-8 counting and byte fidelity',
    'strict pytest settings and the production branch-coverage gate',
    'production interpretation/reference-analysis construction of a qualified test option',
    'outer Context facade imports and __all__ declarations',
    'the exact replace and role-preserving Prompt construction operation',
    'target-side materialization frame/content checks',
    'specific stale/content/missing-resource test distinctions and assertion idioms',
    'qualified target support/declaration frame and membership checks',
    'common planning\'s caller-directed pipeline ownership and selection boundary',
    'parametrized request numeric tests and their byte-domain adaptation',
    'the complete canonical rendered-disclosure text layout',
    'whole-resource admission coupled with retained text/identity/native provenance',
    'the Python/Ruff/mypy project configuration',
    'the materialized item schema coupled with plan-to-disclosure cardinality and identity binding',
    'the ModelUsage optional integer admission precedent',
    'the mixed-plan text fixtures together with order and native-provenance assertions',
]

COLLECTIVE = {
    7: ([[9,10]], 'Validated source/target identity handoff and the renderer/text/native-value handoff are distinct dimensions of the same adapter bridge. N09 supplies the former and N10 the latter; either alone omits the other.'),
    10: ([[9,10]], 'Frame/identity validation including publication only after all items validate is distinct from realization order. N09 supplies admission and all-success integrity; N10 supplies selected-choice order. Neither alone establishes both.'),
    12: ([[17,18]], 'The protected entry point\'s tests-only scope and the separately configured lint/format/type/whitespace workflow answer different validation questions. N17 supplies the scope and N18 the required separate tooling checks, including applicable staged checking.'),
    17: ([[3,4],[4,8]], 'Envelope placement and context-only UTF-8/newline fidelity are distinct parts of the assembly accounting contract. N03 or N08 supplies the separate unchanged-task/Context envelope boundary; N04 supplies encoding, context-only byte reporting and exact newline fidelity. N07 alone supplies task preservation without the envelope structure. Thus the two listed pairs are the inclusion-minimal sufficient sets.'),
    28: ([[9,10]], 'Whole-resource frame/content rejection and the retained item\'s text/native provenance are separate integrity and representation facts. N09 supplies all admission and identity checks; N10 supplies unchanged content and native occurrence retention.'),
    30: ([[9,10]], 'The item\'s immutable text/native provenance schema and the plan-to-item cardinality/identity binding are distinct representation and binding contracts. N10 supplies immutable ordered text/provenance retention; N09 supplies the complete identity fields and matching requirements.'),
}
OVERCOMPOUND = {
    2: 'The unit joins purpose validity, derivation/analysis membership, target-type/route support, and defensive re-admission of directly constructed values. These are independently searchable admission predicates plus a separate materializer enforcement fact. A single frame-binding need cannot reasonably be required to establish this entire bundle; the frozen needs do not ask for all of its purpose/type/route/re-admission dimensions.',
    3: 'The unit bundles documentation authority, pre-collection exclusion, retained configuration/coverage, exit-code propagation and an authorization boundary. Entry-point discovery and tooling configuration are legitimate distinct needs, but neither nor their union requires all implementation mechanics, especially exit-code propagation. Demanding one direct need for that bundle imposes an invalid pairwise contract.',
    14: 'The unit combines the immutable plan schema and ordering/frame identities with independently searchable purpose validity, nonempty selection, homogeneous purpose/frame and duplicate-choice rules. Frame binding and item retention do not ask for all choice-admission predicates. A single direct frame/item need is an invalid requirement for this bundled schema-and-admission unit.',
}
ATOMIC_REASONS = {
    1: 'One public-package export inventory question can seek this complete boundary.',
    4: 'One question about the planning overview\'s current and future capability claims can seek all clauses; the frozen package-documentation need is narrower.',
    5: 'One question about copied-request preservation assertions can reasonably seek this complete test contract.',
    6: 'One question about retained exact-text fixture construction can seek this complete setup mechanism.',
    8: 'The clauses are coordinated checks for one source-side materialization binding.',
    9: 'Canonical document authority and its relevant current scope form one documentation-location fact.',
    11: 'The validator\'s optional admission/error convention and domain applicability form one validation-precedent question.',
    13: 'Frozen status and fields form one immutable request schema.',
    15: 'Allowed imports and forbidden dependency directions form one common assembly dependency contract.',
    16: 'Input signature, full-payload behavior and final construction boundary form one assembly entry-point contract.',
    18: 'Strict test settings and coverage enforcement form one test-configuration contract.',
    19: 'A single qualified-fixture construction question can seek the complete interpretation/analysis sequence; the frozen text-fixture question does not require the full sequence.',
    20: 'One outer-facade public export inventory can seek all of the declarations.',
    21: 'One copy/Prompt construction operation establishes the complete fact.',
    22: 'The checks jointly describe one target-side materialization binding.',
    23: 'One frame-rejection test-pattern question can seek the complete set of related negative cases and idiom.',
    24: 'The conditional declaration-membership check is part of one target-evidence frame contract.',
    25: 'The ordered pipeline and selection boundary form a single common-planning responsibility contract.',
    26: 'One numeric-validation test-convention question can seek the case matrix, assertion idiom and byte-domain adaptation.',
    27: 'All clauses define one exact rendered payload format.',
    29: 'One established type/style configuration question can reasonably seek these coordinated tool settings.',
    31: 'All clauses define one optional nonnegative integer admission contract.',
    32: 'One question about the mixed-plan preservation regression can seek fixtures and assertions together. The frozen text-boundary question omits its native-provenance assertion, but that omission does not make the coherent regression scenario overcompound.',
}

NEED_REVIEW = {
    1: ('NECESSARY', 'The common ownership contract is uniquely established by this focused ownership question.'),
    2: ('NECESSARY', 'Dependency boundaries are a distinct task constraint, uniquely sought completely here.'),
    3: ('NECESSARY', 'The exact rendered layout requires its full metadata and separator inventory; encoding alone does not supply it.'),
    4: ('PARTIAL_ONLY', 'Encoding/newline fidelity is legitimate and contributes to collective byte coverage, but each applicable unit also includes layout or envelope facts outside this need.'),
    5: ('NECESSARY', 'This well-formed validation question uniquely seeks complete implementation admission precedents, including the distinction between positive tokens and nonnegative bytes.'),
    6: ('NECESSARY', 'The safe rejection boundary uniquely seeks the complete existing assembly input/construction contract.'),
    7: ('NECESSARY', 'The all-field copy question uniquely establishes the complete immutable request schema and also explains the copy operation.'),
    8: ('USEFUL_REDUNDANT', 'This is a usable, focused original-task/role question. Its directly covered Prompt-copy operation is also directly covered by N07. Its extra partial contribution to envelope accounting does not change the frozen redundant label.'),
    9: ('NECESSARY', 'This frame question uniquely covers complete source/target binding checks and contributes to several broader units; it does not ask for every unrelated admission predicate.'),
    10: ('PARTIAL_ONLY', 'The item-order/text/provenance concern is legitimate and collectively useful. The reviewed units add identity/admission, rendering metadata or test-specific facts, so no complete unit is directly established.'),
    11: ('NECESSARY', 'The public-boundary question uniquely seeks the planning and outer-facade export declarations.'),
    12: ('NECESSARY', 'The text-test/fixture question uniquely establishes retained UTF-8 fixture setup. It only partly establishes broader qualified-construction and provenance-assertion tests.'),
    13: ('NECESSARY', 'The rejection-test question uniquely establishes the complete changed-frame versus changed-content and missing-resource test pattern.'),
    14: ('NECESSARY', 'This actionable test question uniquely establishes copied-request assertions and numeric test conventions; its two concerns are explicitly stated and do not prevent acquisition.'),
    15: ('NECESSARY', 'The governing-document question uniquely establishes canonical architecture authority and the current pipeline scope to extend.'),
    16: ('PARTIAL_ONLY', 'The package-documentation question is actionable but does not seek the additional future-token/universal-cost distinction bundled into its matching overview unit.'),
    17: ('PARTIAL_ONLY', 'Protected-entry discovery is actionable and supplies workflow scope. It does not by itself require every command implementation, coverage-setting or separate-tool fact in the reviewed units.'),
    18: ('NECESSARY', 'The configuration question uniquely establishes complete test and type/style configuration units and contributes separate-tool facts to collective workflow coverage.'),
}

BLINDNESS = {k: 'NO' for k in [
    'parent/sibling filesystem accessed', 'repository checkout accessed',
    'Git history accessed', 'primary C.5 outputs accessed', 'primary C.5 statistics accessed',
    'lexical queries accessed', 'analyzed terms accessed', 'retrieval routes accessed',
    'treatment results accessed', 'result resources accessed', 'gold-answer resource paths accessed',
    'ranks/scores accessed', 'acquisition costs accessed', 'arm identities accessed',
    'Stage D outcomes accessed', 'confirmation accessed',
]}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    # This is the OUTPUT convention only; never a packet-input requirement.
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def whitelist():
    actual = set()
    for entry in ROOT.iterdir():
        if entry.name == '.local':
            # Operational handoff is expressly excluded; never traverse it here.
            continue
        assert entry.is_file() and not entry.is_symlink(), entry.name
        actual.add(entry.name)
    assert set(INPUT_HASHES) <= actual
    assert actual <= set(INPUT_HASHES) | ARTIFACTS, sorted(actual - set(INPUT_HASHES) - ARTIFACTS)
    return sorted(actual)


def packet():
    whitelist()
    for name, expected in INPUT_HASHES.items():
        assert sha((ROOT / name).read_bytes()) == expected, name
    integrity = json.loads((ROOT / 'integrity.json').read_bytes())
    manifest = json.loads((ROOT / 'manifest.json').read_bytes())
    for name, expected in integrity['files'].items():
        assert name in INPUT_HASHES and sha((ROOT / name).read_bytes()) == expected
    assert sha((ROOT / 'manifest.json').read_bytes()) == integrity['manifest_sha256']
    archive = (ROOT / 'packet.json.gz').read_bytes()
    assert sha(archive) == integrity['archive_sha256'] == manifest['archive_sha256']
    payload = gzip.decompress(archive)
    assert sha(payload) == integrity['canonical_payload_sha256'] == manifest['canonical_payload_sha256']
    p = json.loads(payload)
    assert p['frame'] == manifest['frame']
    ns = [n['identity'] for n in p['information_needs']]
    us = [u['identity'] for u in p['units']]
    assert len(ns) == len(set(ns)) == manifest['need_count'] == 18
    assert len(us) == len(set(us)) == manifest['required_unit_count'] == 32
    pairs = [(v['need'], v['unit']) for v in p['mapping_frame']]
    assert len(pairs) == len(set(pairs)) == manifest['mapping_count'] == 576
    assert set(pairs) == set(itertools.product(ns, us))
    obs = {o['identity'] for o in p['obligations']}
    assert len(obs) == len(p['obligations']) == 9
    alts = {}
    for group in p['alternatives']:
        assert group['obligation'] in obs
        assert group['alternative_logic'] == 'ANY_COMPLETE_ALTERNATIVE'
        for alt in group['alternatives']:
            assert alt['identity'] not in alts
            assert alt['member_logic'] == 'ALL_COMPLEMENTARY'
            assert len(alt['units']) == len(set(alt['units'])) and set(alt['units']) <= set(us)
            alts[alt['identity']] = (group['obligation'], alt['units'])
    assert len(alts) == 12
    for u in p['units']:
        assert set(u['obligations']) == {o for o, members in alts.values() if u['identity'] in members}
        assert set(u['alternative_membership']) == {a for a, (_, members) in alts.items() if u['identity'] in members}
    for obj in p['information_needs'] + p['obligations']:
        for basis in obj['task_basis']:
            assert p['task'][basis['start']:basis['end']] == basis['text']
            assert p['task'][:basis['start']].count('\n') + 1 == basis['line']
    assert all(n['obligation'] in obs for n in p['information_needs'])
    return p, manifest


def build():
    p, manifest = packet()
    needs, units = p['information_needs'], p['units']
    assert len(MATRIX) == 32 and all(len(row) == 18 for row in MATRIX)
    assert set(''.join(MATRIX)) <= set(LABELS)
    assert set(DIRECT) == {(u,n) for u,row in enumerate(MATRIX,1) for n,c in enumerate(row,1) if c == 'D'}
    assert set(PARTIAL) == {(u,n) for u,row in enumerate(MATRIX,1) for n,c in enumerate(row,1) if c == 'P'}
    pair_decisions = []
    for ni, need in enumerate(needs,1):
        for ui, unit in enumerate(units,1):
            symbol = MATRIX[ui-1][ni-1]
            sought = NEED_FACTS[ni-1]
            record = {'need': need['identity'], 'unit': unit['identity'],
                      'need_statement': need['statement'], 'unit_statement': unit['statement'],
                      'label': LABELS[symbol], 'fact_sought': sought,
                      'fact_established_by_unit': unit['statement']}
            if symbol == 'D':
                record['rationale'] = DIRECT[ui,ni]
            elif symbol == 'P':
                covered, missing = PARTIAL[ui,ni]
                record.update(covered_part=covered, missing_part=missing,
                              rationale=f'The need seeks {sought}. It covers {covered}; it does not require {missing}. Therefore its complete answer does not establish the whole unit.')
            else:
                record['rationale'] = (f'The need seeks {sought}. This unit instead establishes {UNIT_FOCUS[ui-1]}. '
                    'The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. '
                    'No specific constituent of this unit is requested by this need in its frozen task context.')
            pair_decisions.append(record)
    coverage, granularity, collective = [], [], []
    assert set(ATOMIC_REASONS) | set(COLLECTIVE) | set(OVERCOMPOUND) == set(range(1,33))
    assert not (set(ATOMIC_REASONS) & set(COLLECTIVE) or set(ATOMIC_REASONS) & set(OVERCOMPOUND) or set(COLLECTIVE) & set(OVERCOMPOUND))
    for ui, unit in enumerate(units,1):
        row = MATRIX[ui-1]
        status = 'COVERED' if 'D' in row else 'PARTIAL_ONLY' if 'P' in row else 'AMBIGUOUS_ONLY' if 'A' in row else 'UNCOVERED'
        coverage.append({'unit':unit['identity'], 'status':status,
            'direct_needs':[needs[n]['identity'] for n,c in enumerate(row) if c == 'D'],
            'partial_needs':[needs[n]['identity'] for n,c in enumerate(row) if c == 'P'],
            'ambiguous_needs':[needs[n]['identity'] for n,c in enumerate(row) if c == 'A']})
        if ui in COLLECTIVE:
            sets, reason = COLLECTIVE[ui]
            category = 'COLLECTIVELY_COVERABLE'
            collective.append({'unit':unit['identity'], 'status':'MINIMAL_SETS_IDENTIFIED',
                'minimal_need_sets':[[needs[n-1]['identity'] for n in s] for s in sets],
                'rationale':reason,
                'minimality':'Each listed set has two needs. The covered_part/missing_part records show that either singleton omits a distinct necessary facet. No other frozen need supplies the missing facet completely; supersets add no necessary evidence. These are all identified inclusion-minimal sufficient sets.',
                'diagnostic_only':True})
        elif ui in OVERCOMPOUND:
            category, reason = 'OVERCOMPOUND_FOR_PAIRWISE_MAPPING', OVERCOMPOUND[ui]
        else:
            category, reason = 'ATOMIC_FOR_NEED_MAPPING', ATOMIC_REASONS[ui]
        granularity.append({'unit':unit['identity'], 'statement':unit['statement'], 'category':category, 'rationale':reason})
    need_reviews = []
    for ni, need in enumerate(needs,1):
        label, reason = NEED_REVIEW[ni]
        direct = [units[u]['identity'] for u,row in enumerate(MATRIX) if row[ni-1] == 'D']
        unique = [units[u]['identity'] for u,row in enumerate(MATRIX) if row[ni-1] == 'D' and row.count('D') == 1]
        need_reviews.append({'need':need['identity'], 'statement':need['statement'], 'label':label,
            'rationale':reason, 'direct_units':direct, 'uniquely_direct_units':unique,
            'semantic_formulation_review':'Actionable repository information question in the frozen task context; neither misformulation nor unresolvable ambiguity is established. Narrow scope or lack of a whole-unit match is not misformulation.'})
    by_unit = {v['unit']:v for v in coverage}
    collective_units = {v['unit'] for v in collective}
    alternatives = []
    for group in p['alternatives']:
        for alt in group['alternatives']:
            direct = [u for u in alt['units'] if by_unit[u]['status'] == 'COVERED']
            diagnostic = [u for u in alt['units'] if u not in direct and u in collective_units]
            missing = [u for u in alt['units'] if u not in direct + diagnostic]
            status = 'FULLY_DIRECTLY_COVERED' if len(direct) == len(alt['units']) else 'FULLY_COVERED_ONLY_COLLECTIVELY' if not missing else 'INCOMPLETE'
            alternatives.append({'alternative':alt['identity'], 'obligation':group['obligation'],
                'member_logic':alt['member_logic'], 'units':alt['units'], 'status':status,
                'directly_covered_members':direct, 'collectively_covered_members':diagnostic,
                'incomplete_members':missing,
                'rationale':'Every member is required within this alternative. '+
                    ('Every member has a direct need.' if status == 'FULLY_DIRECTLY_COVERED' else
                     'Every member is established, but at least one requires a listed diagnostic collective set.' if status == 'FULLY_COVERED_ONLY_COLLECTIVELY' else
                     'The listed incomplete members lack both a direct need and a defensible complete collective set. Other alternatives cannot fill these gaps inside this alternative.')})
    obligation_audit = []
    for group in p['alternatives']:
        own = [a for a in alternatives if a['obligation'] == group['obligation']]
        obligation_audit.append({'obligation':group['obligation'], 'alternative_logic':group['alternative_logic'],
            'fully_direct_alternatives':[a['alternative'] for a in own if a['status'] == 'FULLY_DIRECTLY_COVERED'],
            'additional_collectively_complete_alternatives':[a['alternative'] for a in own if a['status'] == 'FULLY_COVERED_ONLY_COLLECTIVELY'],
            'rationale':'Any one complete alternative suffices for this obligation; members from different alternatives are never pooled.'})
    count = lambda rows, key: dict(sorted(collections.Counter(r[key] for r in rows).items()))
    return {'schema':'case-0011-c5r-adjudication-v1', 'method_version':'c5r-semantic-review-1.0.0',
        'method':{
            'review':'Independent packet-only human-readable semantic assessment of every Cartesian pair, recorded as an explicit 32-by-18 matrix. The program serializes reviewer decisions and derives audits; it does not classify using terms, similarity, counts or retrieval evidence.',
            'interpretation':'Read each need with its frozen reason and task basis. A complete answer must establish all unit clauses; merely locating a related item is insufficient. Partial coverage requires an identifiable constituent, not shared vocabulary. Tests and implementation contracts are distinguished where a unit requires specific assertions or construction mechanics.',
            'granularity':'Atomic means a coherent focused contract/schema/test scenario could be sought as a whole. Collective means distinct binding, representation or workflow facets have a defensible joint answer in the frozen needs. Overcompound means independently searchable predicates or execution/authorization facts are bundled beyond a defensible single-need evaluation. Complexity or number of clauses alone is insufficient.',
            'uncertainty':'No pair remained semantically indeterminate after review; zero ambiguous labels is a decision, not a forced default. Evidence absent from a question is not imputed to its answer.',
            'input_integrity':'Verify exact archive, decompressed payload and explicitly hashed input bytes. No compact-JSON, whitespace, key-order or input reserialization constraint is imposed.',
            'provenance_digest_limit':'frozen_needs_sha256 and reviewed_gold_sha256 are preserved authenticated manifest declarations. The packet provides neither their original objects nor a digest-construction specification, so they are not recomputed from invented reconstructions.',
            'ordering':'Frozen packet order determines stable N/U display aliases; opaque identities remain authoritative. Output JSON is sorted/indented UTF-8 with one terminal LF.',
            'scientific_scope':'Collective and granularity diagnostics never promote partial pairs, alter the reviewed units, or modify U1. No retrieval, treatment or effectiveness conclusion is made.'},
        'input_sha256':INPUT_HASHES, 'manifest':manifest,
        'frozen_packet':p,
        'display_aliases':{'needs':{f'N{i:02}':n['identity'] for i,n in enumerate(needs,1)},
                           'units':{f'U{i:02}':u['identity'] for i,u in enumerate(units,1)}},
        'pairs':pair_decisions, 'unit_coverage':coverage, 'unit_granularity':granularity,
        'collective_coverage':collective, 'need_classifications':need_reviews,
        'alternative_coverage':alternatives, 'obligation_alternatives':obligation_audit,
        'summary':{'pair_labels':count(pair_decisions,'label'), 'unit_coverage':count(coverage,'status'),
            'need_labels':count(need_reviews,'label'), 'granularity':count(granularity,'category'),
            'alternative_coverage':count(alternatives,'status'),
            'pair_count':len(pair_decisions), 'duplicate_pairs':0, 'missing_pairs':0, 'unexpected_pairs':0,
            'frozen_direct_rule_satisfied':all(v['status']=='COVERED' for v in coverage)},
        'blindness_attestation':BLINDNESS}


def exclusive_write(name, data):
    assert name in ARTIFACTS
    with (ROOT / name).open('xb') as stream:
        stream.write(data)


def release_validation():
    # Refuse a partial overwrite before starting validation.
    assert not (ROOT / 'c5r_v1_validation.json').exists()
    assert not (ROOT / 'c5r_v1_hashes.json').exists()
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONDONTWRITEBYTECODE='1')
    command = [sys.executable, '-B', '-m', 'pytest', str(ROOT / 'test_c5r_v1.py'),
               '--noconftest', '-p', 'no:cacheprovider', '-o', 'addopts=', '-q']
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
    print(result.stdout, end='')
    print(result.stderr, end='')
    assert result.returncode == 0, 'Local validation failed; no release validation emitted'
    assert '12 passed' in result.stdout
    before = (ROOT / OUTPUT).read_bytes()
    assert encode(build()) == before == encode(build())
    replay = subprocess.run([sys.executable, '-B', str(ROOT/'c5r_v1.py'), '--replay'],
                            cwd=ROOT, env=env, capture_output=True, text=True)
    assert replay.returncode == 0 and 'REPLAY_IDENTICAL' in replay.stdout
    refusal = subprocess.run([sys.executable, '-B', str(ROOT/'c5r_v1.py'), '--freeze'],
                             cwd=ROOT, env=env, capture_output=True, text=True)
    assert refusal.returncode == 2 and 'OVERWRITE_REFUSED' in refusal.stdout
    assert (ROOT / OUTPUT).read_bytes() == before
    validation = {'schema':'case-0011-c5r-validation-v1', 'status':'PASS',
        'input_sha256':INPUT_HASHES, 'adjudication_sha256':sha(before),
        'local_tests':{'passed':12, 'failed':0,
            'command':'python -B -m pytest ./test_c5r_v1.py --noconftest -p no:cacheprovider -o addopts= -q',
            'environment':{'PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1','PYTHONDONTWRITEBYTECODE':'1'},
            'repository_imports':False},
        'checks':{k:'PASS' for k in ['exact_input_hashes','declared_archive_and_payload_hashes',
            'packet_manifest_frame_counts_and_memberships','576_unique_pairs','32_granularity_judgments',
            '18_need_classifications','12_alternative_audits','frozen_statement_identity',
            'label_and_rationale_completeness','collective_minimal_sets','coverage_derivation',
            'no_forbidden_fields','scientific_workspace_whitelist','deterministic_replay','overwrite_refusal']},
        'deterministic_replay':'Fresh-process replay and repeated in-process construction exactly equal frozen adjudication bytes; no timestamps or environment-dependent fields.',
        'overwrite_refusal':'Second CLI --freeze exited 2 with OVERWRITE_REFUSED; original adjudication bytes unchanged.',
        'source_provenance_hashes':'Authenticated manifest declarations retained; no invented pre-packet reconstruction or serialization requirement.',
        'scientific_whitelist':sorted(set(INPUT_HASHES)|ARTIFACTS),
        'handoff_exclusion':'.local/codex-result.md is operational and excluded from scientific hashes, evidence and whitelist checks.',
        'blindness_attestation':BLINDNESS}
    exclusive_write('c5r_v1_validation.json', encode(validation))
    hashes = {n:sha((ROOT/n).read_bytes()) for n in sorted((set(INPUT_HASHES)|ARTIFACTS)-{'c5r_v1_hashes.json'})}
    exclusive_write('c5r_v1_hashes.json',encode({'schema':'case-0011-c5r-sha256-v1','sha256':hashes,
        'exclusions':['c5r_v1_hashes.json (its digest is in the operational report)', '.local/codex-result.md (operational handoff)']}))
    assert set(whitelist()) == set(INPUT_HASHES)|ARTIFACTS
    print(json.dumps(build()['summary'], indent=2))
    print('SCIENTIFIC_VALIDATION_COMPLETE')


if __name__ == '__main__':
    if sys.argv[1:] == ['--freeze']:
        try:
            exclusive_write(OUTPUT, encode(build()))
        except FileExistsError:
            print('OVERWRITE_REFUSED')
            sys.exit(2)
        print('FROZEN', sha((ROOT/OUTPUT).read_bytes()))
    elif sys.argv[1:] == ['--replay']:
        assert encode(build()) == (ROOT/OUTPUT).read_bytes()
        print('REPLAY_IDENTICAL')
    elif sys.argv[1:] == ['--validate']:
        release_validation()
    else:
        raise SystemExit('Use --freeze, --replay or --validate')
