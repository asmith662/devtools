# Direct Reference RI as a Localization witness-candidate relation

Date: 2026-10-04. Basis: clean `main` at
`bc0f0a879bd7b1e676190d662f5447552ce4237c`
(`Separate declaration grounding from binding semantics`).

## Disposition

**RECOMMEND DEFER** the direct-reference generation operator until the bounded
generation contract explicitly supports one branching member per caller-authored
recipe. The smallest prerequisite is generation multiplicity, including child
hypothesis identity, per-branch outcomes, and visible work/result bounds. Native
Reference RI already supplies qualified exact positive facts; inventing a new
Reference parser or weakening binding resolution is unnecessary.

The eventual relation is worth a prospective Localization test, subject to that
prerequisite. This investigation implements nothing, accepts no new production
behavior, changes no ADR, and freezes no case. It is evidence under the
[research convention](README.md#research-governance), not implementation authority.

## Inspected authority and implemented evidence

The [taxonomy](../architecture/taxonomy.md#repository-intelligence),
[documentation map](../documentation_map.md), and
[B-0002](../backlog/epics/B-0002-coding-context-substrate.md) preserve ownership and
unresolved pressure. The relevant accepted decisions are
[ADR-0002](../architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md#repository-subjects-and-source-occurrences),
[ADR-0003](../architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md#candidates-and-relevance-evidence),
and [ADR-0005](../architecture/decisions/ADR-0005-obligation-driven-repository-localization.md#candidate-competition-and-evidence).
They distinguish repository relationships, purpose-relative evidence, ranking,
candidate explanations, accepted witnesses and readiness. No material conflict
between those authorities and the inspected source was found.

Primary production evidence:

- [Reference model](../../src/devtools/context/python/references/declarations/model.py),
  [analysis](../../src/devtools/context/python/references/declarations/analysis.py),
  [binding checks](../../src/devtools/context/python/references/declarations/bindings.py),
  [resolution](../../src/devtools/context/python/references/declarations/resolution.py),
  and [package contract](../../src/devtools/context/python/references/docs/overview.md).
- [Direct binding lookup](../../src/devtools/context/python/modules/declarations.py),
  [source selection](../../src/devtools/context/python/modules/selection.py),
  [module interpretation](../../src/devtools/context/python/modules/interpretation.py),
  [import resolution](../../src/devtools/context/python/imports/resolution.py), and
  [one-facade member resolution](../../src/devtools/context/python/imports/members.py).
- [Generation values](../../src/devtools/context/localization/generation/contract.py),
  [generation implementation](../../src/devtools/context/localization/generation/generate.py),
  [hypotheses/view](../../src/devtools/context/localization/association/hypothesis.py),
  [structural support](../../src/devtools/context/localization/association/structural.py),
  and [Localization contract](../../src/devtools/context/localization/docs/overview.md#bounded-candidate-witness-generation).
- [Existing resource structural projection](../../src/devtools/context/retrieval/structural.py)
  and [qualified function disclosure validation](../../src/devtools/context/python/function/qualified_reference.py).
- [Reference tests](../../tests/context/python/references/declarations/test_analysis.py),
  [binding tests](../../tests/context/python/references/declarations/test_bindings.py),
  [generation tests](../../tests/context/localization/generation/test_generation.py),
  [association tests](../../tests/context/localization/association/test_hypothesis.py),
  and [imported-member tests](../../tests/context/python/imports/test_members.py).

Tests were inspected, not executed. Historical evidence below informs the
architecture only; experiment code is not the production contract.

## What current Reference RI asserts

The sole active derivation is `derive_python_declaration_references`. It examines
`ast.Name` and outermost `ast.Attribute` load expressions in retained snapshot
source under identified Python 3.12 grammar semantics. Inner parts of a resolved
attribute chain are not independent references. The occurrence span covers the
whole expression, with one-based lines and UTF-8 byte columns.

An assessment retains syntax and an outcome. A positive
`PythonDeclarationReferenceKnowledge` asserts
`bounded-expression-references-python-declaration`: that occurrence targets a
supported native direct function, class, or direct class-body method declaration
under the bounded static resolution contract. It carries the canonical target
subject, declaration knowledge and target resource. This is stronger than a
matching spelling and weaker than runtime object, invocation or dispatch truth.

| Route | Supported target interpretation |
| --- | --- |
| SAME_MODULE | Unique supported direct function/class binding; module-body use before binding is unresolved |
| IMPORTED_MEMBER | Direct named import resolving to a supported direct function/class |
| ONE_FACADE | Existing one-facade imported-function route, with its retained native qualification |
| MODULE_QUALIFIED | Complete statically qualified module member expression targeting a supported direct function/class |
| CLASS_QUALIFIED_METHOD | One direct, unambiguous, undecorated method of a statically identified supported class; lexical parent retained |

Scope/shadowing guards reject unsupported headers, receivers and bindings.
`self.m`, `cls.m`, arbitrary object dispatch, rebound names, ambiguous modules,
wildcards and dynamic namespaces do not become positive facts merely because a
name matches. Direct class/method and module binding guards remain conservative.
The one-facade route has its separate existing declaration-target semantics;
consuming its positive facts must retain that route rather than strengthen it
into a runtime import claim.

`direct_call` is a Boolean specialization of this same fact: the expression
occupies `ast.Call.func`. There is no separate active Call edge to union into
this projection. Both call-tagged and non-call positive References are eligible
in the proposed relation; retain the tag rather than count a Call twice. The
historical function-only classes in `references.analysis` are passive archive
compatibility values, not a second active derivation to include.

Import syntax and resolved module Imports are separate facts. A bare
`from native import Foo` has an alias, not a load-expression Reference to Foo.
A later supported use of Foo may produce a Reference with import support.
Consequently, Reference alone does not expose import-only facades or registration
resources. A base expression may qualify as a load-expression Reference under
the same checks; that fact alone asserts no inheritance relation. Native direct
base, package containment and configuration relations remain separate.

Decorated source declarations can now ground, but that does not relax Reference
binding identity. The direct imported/module-member routes still reject decorated
classes/functions; decorated methods are not resolved as original method targets.
This can yield zero exact Reference facts for a soundly grounded declaration.
The operator must neither bypass that guard nor substitute equal-spelling uses.
In particular, the eight decorated direct classes diagnosed in Case 0006 do not
automatically acquire exact referencers through the grounding correction.

## Exact inverse projection and native support

The desired direction is:

```text
one RESOLVED native declaration grounding
    -> exact equality with Reference.target_subject identity
    -> positive referencing source occurrences
    -> snapshot.resource_at(occurrence.resource_address)
```

This is target-to-source projection. It is distinct from source-to-referenced
target navigation. A class seed does not absorb References whose actual target
is one of its methods through the `containing_class` support link; a method seed
matches the method subject itself. Current facts make inverse lookup deterministic by a finite
scan, but the Reference package exposes no maintained inverse index or dedicated
subject-level inverse query. A request-local grouping suffices; no graph is needed.

The existing Retrieval projection already supports `definition-to-reference`,
but seeds by **resource address** and excludes same-resource relationships. It
would admit references to other declarations in the same defining file. Using
that output directly would broaden an exact declaration seed. Its grouping
pattern is useful evidence, not a replacement semantic owner or adapter to call
unfiltered. Native subject identity must select facts before resource grouping.

The candidate target remains `RepositoryResourceOccurrence` within the explicit
repository/snapshot. Finer native Reference occurrences are support, not extra
candidate resources. Several matching occurrences in one resource give one
candidate with every distinct native supporting fact. Deduplicate repeated
supplied fact identities; retain genuinely distinct occurrences. Occurrence
counts are diagnostics, never independent relevance votes.

A future Python-specific structural support record needs the grounding, grouped
native Reference facts, their native analyses, explicit module universe/source
interpretations, and projection frame/semantics. From those references one can
recover source spans, target declaration/subject/resource, route, Call tag, import
and member resolution, containing class, and derivation identities. Retain those
values; a string such as `reason = reference` is insufficient. The candidate's
resource must equal the analysis source dependency and occurrence owner.

Validate the grounding against the plan, fact membership/derivation/coverage,
repository/snapshot and exact source/target content dependencies, interpretation
universe, target native subject and declaration consistency. Reject altered or
foreign inputs. Existing function-disclosure checks inform these requirements
but only cover a narrower imported-function Context form; do not broaden that
API to validate all References. Any necessary replay must delegate to canonical
RI and account for its work, never implement a Localization parser.

Only exact positive facts generate targets. Unresolved/ambiguous/shadowed/
unsupported assessments supply no identified target and cannot be linked by
spelling, treated as extra candidates, or scored numerically. Retain them as
frame limitations. They do not cancel independently supported positive facts
elsewhere. Zero means no positive match in the supplied frame, never no runtime
referencers. `IS_EXHAUSTIVE` is false.

## Cardinality diagnostic

A bounded architecture diagnostic used only current native production RI at the
starting HEAD. Its finite frame was all 402 current `.py` resources under
`src/devtools` and `tests`, excluding `tests/experiments`; `scripts`, experiments,
external libraries and other resources were outside the frame. The source-root
interpretation was `src`; test resources were interpreted under `.`. All 402
resources had interpretations. The acquisition envelope was 512 resources and
1 MiB per resource, not an operator default or an execution-time guarantee.

| Quantity | Observed value |
| --- | ---: |
| Supported native class/function/method subjects | 2,646 |
| Positive Reference facts / direct Call tags / non-call facts | 3,650 / 3,521 / 129 |
| Subjects with at least one referencing resource | 608 |
| Subjects with zero / one / several referencing resources | 2,038 / 478 / 130 |
| Median / p90 / p95 / maximum fanout among positive subjects | 1 / 2 / 4 / 21 |
| Subjects with referencers outside their declaration resource | 196 |
| Median / p90 / p95 / maximum among those external-positive subjects | 2 / 4 / 7 / 20 |
| Subjects whose positive references were only in their own resource | 412 |
| Failed resource analyses | 0 |

Quantiles use nearest rank `ceil(p * n)` in the ascending positive distribution;
medians use the ordinary sample median. These are distinct-resource counts per
exact native target subject, not occurrence counts or usefulness measurements.
The external-positive distribution is a diagnostic comparison, not a proposed
filter. The complete positive histogram is:

```text
resource count: subject count
1:478  2:70  3:23  4:16  5:4  6:5  7:3  8:4
10:1  12:1  15:1  20:1  21:1
```

| Native category | Subjects | Zero | One | Several | Maximum |
| --- | ---: | ---: | ---: | ---: | ---: |
| Direct class | 482 | 372 | 75 | 35 | 4 |
| Direct function | 1,545 | 1,047 | 403 | 95 | 21 |
| Direct method | 619 | 619 | 0 | 0 | 0 |

Examples of cardinality categories are thus same-resource function use,
small-fanout classes and functions with up to 21 referencing resources. No
individual target name/path is used to choose policy. Zero method reach in this
frame does not contradict supported class-qualified-method fixtures or prove
that methods can never have exact References. Likewise, zero exact facts do not
prove no textual or runtime uses: many decorated, type-checking, header and
receiver forms remain outside the positive resolution surface.

Observed routes were SAME_MODULE 2,255, IMPORTED_MEMBER 744 and ONE_FACADE 651;
no positive MODULE_QUALIFIED or CLASS_QUALIFIED_METHOD occurred in this selected
frame. The native analyses assessed 46,616 load-expression occurrences. Nonpositive
assessments remain limitations, not candidate subjects or negative facts.

Reproduction basis:

- Generate the finite manifest with
  `rg --files src/devtools tests -g '*.py' -g '!tests/experiments/**'`;
  canonicalize separators and sort addresses, reject an oversized manifest.
- Use canonical `observe_repository_resources` (not an independent snapshot
  constructor) with repository diagnostic identity
  `00000000-0000-0000-0000-000000000096`, the stated per-resource bound and manifest.
  The resulting snapshot ID was
  `52566de7a65b12f519dd6f5d5ddf09dac67930e7a1f8da3c641304517dd7046d`.
- Build one module universe from `interpret_python_module_resources` at the two
  roots above. For each resource call canonical function/class/method declaration
  derivation, then `derive_python_declaration_references` with that universe and
  its exact source interpretations. Collect native declaration subject IDs;
  group each positive fact by `target_subject.identity` and distinct occurrence
  resource address. Count an external referencer only when that address differs
  from the native declaration support address. Do not execute analyzed source.
- Count native outcomes/routes/Call tags, deduplicate fact identities and compute
  the tables above. No lexical acquisition, task, obligation, grounding request,
  generation plan, historical gold or Case 0006 input enters the diagnostic.

This is exhaustive enumeration of positive facts returned for this selected
frame, not exhaustive Python Reference interpretation or a repository-wide
runtime graph. The diagnostic is structural inventory, not a replay, performance
benchmark, prospective case, or effectiveness treatment. It supplies no success
threshold. In particular, Option A's 478 singleton subjects include many
same-resource-only uses; 130 subjects have multiple resources and 196 have
external positive reach. Those numbers characterize tradeoffs without deciding
that any target is a witness.

## Current generation invariant and options

`GroundedMemberRecipe` names one grounding, projection, member key and caller
rationale. `WitnessGenerationRecipe` fixes an all-member explanation and a
caller-named obligation-local hypothesis identity. The plan contains explicit
recipes; it does not infer alternatives from relation cardinality.

Each projection admits at most one target. `MemberProjectionAttempt` can retain
several targets/supports, but a multi-target result produces `MULTI_TARGET` and
no hypothesis. `_attempt_recipe` uses each `targets[0]` only after all projections
succeed, rejects duplicate resource conjuncts, and constructs exactly one
hypothesis with the recipe identity. `HypothesisGenerationAttempt.hypothesis`
is singular. Any failed member prevents a partial hypothesis. The no-Cartesian
rule prevents guessed complementary structure, uncontrolled products and silently
manufactured competing alternatives. It does not assert that branching is always
unsound; branching is simply not represented or authorized by the current API.

`CandidateWitnessHypothesis` is an unresolved **all-member explanation** competing
with same-obligation peers. It proposes a whole candidate witness shape, without
asserting sufficiency, acceptance or mandatory coverage. It is more than an
unstructured bag of individually relevant resources. The current view can store
multiple caller-authored hypotheses and cross-obligation participation; it does
not manufacture child identities or validate Reference structural support.

| Option | Assessment |
| --- | --- |
| A: exactly one resource, otherwise abstain | Preserves today's contract and is sound within its limited admission scope. It arbitrarily makes relation usability depend on fanout rather than caller witness shape, losing multi-resource referencer alternatives. A one-target policy is not a relevance discriminator. Not the selected next operator. |
| B: one singleton hypothesis per resource | Honest only when the caller explicitly proposes a singleton referencer as the whole unresolved explanation. The existing association model can represent it, but the generator cannot emit multiple children from one recipe. As an automatic default it loses required complementary owners/contracts. |
| C: one explicit branching member plus fixed members | Smallest useful eventual model. Each target substitutes for one caller-chosen slot; all fixed members remain proposed complements. Supports a singleton family as the zero-fixed-member special case. Requires new bounded multiplicity and identity/outcome contracts before the operator. |
| D: projection view only | Sound staging option if a caller needs raw referencer navigation independently of hypotheses. Current member attempts can retain multi-target diagnostics but cannot validate Reference support or express the required input frame; the association view stores hypotheses, not free projected resources. A new view does not itself solve the desired owner-plus-one-referencer shape, so it is not the selected prerequisite. |

No fifth design is justified. No general resolver/dispatcher or universal
candidate type is needed.

## Minimum prerequisite: one explicit branching slot

The next production request should settle and implement these generation
semantics separately from a new relation:

1. Keep existing recipes and member projections single-target by default. A
   distinct caller-authored branching member declares substitution intent and
   its result bound. At most one such member is allowed in a recipe.
2. For fixed complementary members A and C and branch targets B1...BN, form
   unresolved alternatives `(A, B1, C)` ... `(A, BN, C)`. N alternatives are
   linear in N, with no cross-product or recursion. No member is inferred from
   an obligation, lexical query, role preference or gold witness.
3. Preserve caller recipe-family provenance and deterministic child lineage.
   Reuse existing task/obligation identity conventions; distinguish generated
   child keys from caller literal alternative keys, retain exact native target
   occurrence identity, and detect collisions rather than overwrite. Simple
   unchecked string suffixes and source-order ordinal identities are inadequate.
4. Retain per-branch outcomes and a tuple of generated hypotheses per family.
   A fixed-member failure prevents every child. A branch duplicating a fixed
   resource retains `DUPLICATE_TARGET` and no child for that combination; other
   valid combinations remain separately inspectable. Never silently collapse
   conjuncts or reinterpret a duplicate as support for a smaller witness shape.
5. Define fanout/work abstention and unknown-total/frontier semantics explicitly.
   Keep existing association validation and accepted-witness/readiness boundaries.
   Exercise cardinality with synthetic test projections, not a new production
   operator or a frozen-case replay. No generic plugin dispatcher is necessary.

For example, “owner contract plus one referencing integration” licenses a family
of proposed pairs only when the caller authors that complementarity. Each pair
is still a hypothesis. `(owner, B1, B2, ... BN)` would instead assert all
referencers are proposed complements and is explicitly ruled out as an automatic
interpretation. Conversely, singleton B1/B2 explanations must not be presented
as if they carry the missing owner contract. Branching creates neither truth
that any branch suffices nor a requirement that exactly one branch be accepted.

## Eventual relation contract, bounds and ordering

These are investigation requirements for a later adapter, not accepted APIs:

- **Input:** one current RESOLVED class/function/method native declaration
  grounding, caller-linked obligation/recipe rationale, explicit finite native
  Reference analyses and their universe/source frame, independent work quotas
  and a caller-supplied positive maximum distinct-resource result count.
  Resource/module groundings do not implicitly become declaration seeds.
- **Relation:** all current positive declaration References whose exact target
  native subject equals the seed, with consistent target declaration knowledge.
  Include all supported routes and both Call tags. Imports, inheritance facts,
  exports, containment and other graph edges are not unioned in.
- **Target:** each distinct referencing resource occurrence, including same-owner
  resources if exact positive facts occur there. Do not inherit Retrieval's
  silent self-resource suppression. Duplicate conjunct handling belongs to the
  explicit hypothesis shape, with a visible outcome.
- **Support:** group every distinct matching Reference for a target beside its
  native analysis and grounding/frame. Keep native identities and source spans;
  do not produce a universal repository entity or global relevance identity.
- **Multiplicity:** after the prerequisite, the explicitly marked slot branches
  once over the exact resource set. Structural relation yields targets; lexical,
  role and owning-obligation routing support can attach afterward by exact
  occurrence identity. They never remove referencers or decide branch survival.
- **Result bound:** enumerate the full supplied-frame match set if work permits.
  If N exceeds the declared bound, admit no hypotheses for that family, retain
  N, bound, exact support/frame/semantics and an explicit bound-exceeded outcome.
  No default numerical cap is chosen from this diagnostic or Case 0006.
- **Work bound:** accept finite retained analyses, not an unbounded iterator or
  implicit repository scan. Preflight separate maxima for source analyses,
  occurrence assessments/positive facts, and validation/replay input bytes and
  module-universe resources. Projection scans supplied facts; acquisition,
  parsing and any canonical replay have separately recorded costs. A result cap
  does not bound RI derivation or prove cheap enumeration. There is no maintained
  inverse index today and no need to introduce one for this bounded consumer.
- **Work failure:** if the authorized envelope cannot inspect/validate the whole
  declared frame, abstain without children; report examined work and uncovered
  analysis/source frontier. Total target count remains unknown (or an explicit
  lower bound), not a fabricated exact number. Refusing an oversized finite
  input before scanning is preferable to returning its first few matches.
- **Outcomes:** current ambiguous/unresolved/unsupported grounding outcomes remain
  visible; invalid/foreign frames are rejected. Completed zero positive matches
  yields scoped NO_TARGET. Completed in-bound targets permit unresolved branches.
  Completed overflow yields bound-exceeded abstention; incomplete work yields
  work-limit abstention. Duplicate combinations retain their own failure. All
  retain non-exhaustive native Reference coverage and optional analysis failures.

All exact targets without a cap are reproducible but can be too numerous; this
diagnostic measures cardinality, not a safe default. First-K truncation is
rejected: path, insertion and occurrence order have no relevance meaning. A
typed narrower predicate could be separately caller-selected if justified by a
native proposition (for example, a direct Call syntax restriction), but nothing
here selects one or invents filters. An import-only predicate is another relation.

Native facts are in source-range order within each analysis. Derivation identity
sorts source-interpretation identities; no global relevance order is supplied.
Projection targets and branches should use canonical resource occurrence keys;
supports should use native fact identity/source coordinates. This makes input
permutations reproducible, without source/path order acquiring rank. Cross-obligation
`for_target` and `cross_obligation_targets` already support shared resources; keep
recipe, anchor, branch and obligation provenance separate, even for identical
targets. Do not count repeated cross-obligation support as global agreement.

## Ownership and language boundary

Python RI owns Reference truth. Localization consumes it for a purpose-bearing
candidate relation and caller-shaped hypotheses:

```text
context.python.references -> native qualified facts
                          -> context.localization.generation Python adapter
                          -> association native structural support
                          -> unresolved CandidateWitnessHypothesis
```

Allowed imports go from Localization to Python RI; RI must not import
Localization. A responsibility-focused adapter such as `generation/references.py`
and a narrow Reference support addition in existing `association/structural.py`
fit current ownership. Do not create a parallel RI derivation under Localization,
a top-level package or a family of prefixed flat modules.

The conceptual relation is direct referencing-resource projection, but the
minimum interface consumes `PythonDeclarationReferenceAnalysis` and the existing
native Python declaration types. No language-neutral Reference protocol, abstract
entity or generic graph interface is currently required. A result/support is
task-relative provenance, not a new RI subject or durable schema.

## Empirical motivation and safeguards

The [completed breadth synthesis](repository-retrieval-breadth-production-gate.md#final-evidence-map)
and [Increment 29 summary](../../experiments/increment_29/README.md#completed-development-result)
report 71 Reference/direct-Call candidate additions on 24 historical development
needs, 35 USEFUL, with 198 supports. Eleven additions were outside all five saved
lexical universes and the direct-import union; four were USEFUL. Reverse projection
contributed 35 pairs, 15 USEFUL. Maximum per-case/per-seed additions were 12.
All candidates were call-tagged: non-call value was not isolated. These were
historical function-only, resource-seeded, both-direction experiments, not an
obligation-framed test of this exact-subject inverse operator. They justify
investigation, not production defaults, parameter selection or guaranteed gain.
Only aggregate evidence was used; historical gold paths did not set filters,
bounds, subtypes or recipe shapes.

Graph-1 added 704 novel pairs with two USEFUL in a 128-pair sample and 10,550
novel support paths. Graph-2 added 987 more pairs with zero USEFUL in its separate
128-pair sample, 85,015 novel-support paths and 294,154 complete paths. Unsampled
pairs cannot be called unnecessary. Those findings pressure automatic multi-hop
expansion and path counting; they do not veto exact purpose-selected References.

The eventual operator would require a resolved **subject** seed, caller-selected
inverse relation and branching shape, one hop only, no recursive frontier
execution, visible finite fact/work frame, all-or-abstain result cap, grouped
native support and unresolved hypotheses. It does not consume PPR/RRF, neighbor
counts or generic graph adjacency. These safeguards distinguish it from naive
expansion but do not prove that the resulting surface is useful or small enough.

Case 0006 is used solely through the user-supplied aggregate Stage D diagnosis:
OWNER/MIRRORED counterfactual grounding-fixed coverage remained 12/28 REQUIRED
cells, 15/33 REQUIRED unit judgments, 7/18 unique REQUIRED resources and 2/10
complete obligations; blind gold suggested reference/import connectivity. The
grounding defect is now corrected. No Case 0006 files were opened or its
Retrieval/routing/grounding/generation replayed for this investigation. Reference
and import connectivity remain separate hypotheses, and decorated binding
limitations remain material. No improvement claim follows.

## Prospective evidence needed after the prerequisite

Before any future Case 0007 execution, freeze the natural task, obligations,
native frame, grounded subjects, caller-authored fixed/branching shapes, work
quotas and result caps independently of gold. This investigation freezes none.
Then measure at least:

- Hypotheses and distinct generated resources, total and per obligation;
  reference facts versus resource grouping; duplicate combinations.
- REQUIRED resource cells/unit judgments/resources covered, complete acceptable
  witness-structure coverage, and marginal gain over corrected OWNER/MIRRORED.
- Unique new REQUIRED witnesses and unique unnecessary resources contributed by
  Reference, including overlap across obligations and with existing candidates.
- Exact fanout, bound-exceeded/work-limit abstention, unknown frontiers, frame
  exclusions, native unsupported outcomes and decorated-seed positive reach.
- Candidate surface against global/obligation lexical completion prefixes and
  the independently adjudicated semantically sufficient bound; where comparison
  claims structure adds value, include candidate-volume-matched lexical widening.
- Separate RI acquisition/derivation/validation cost from projection and
  hypothesis construction cost. Count full scans even when no result is admitted.

Encouraging evidence would recover missing complementary integrations and more
complete witness structures with a useful reduction in review surface relative
to lexical completion, without achieving that result through arbitrary truncation.
Poor evidence would mostly duplicate owner/mirror resources, add unnecessary
surface, routinely exceed bounds or fail to reach supported obligation subjects.
No numerical pass threshold is chosen from historical outcomes or this inventory.
Candidate generation still does not accept witnesses, satisfy obligations,
establish readiness, authorize execution or select Context representations.

## Exact next step and task compliance

Request a bounded generation-multiplicity increment implementing the single branching
member contract above, preserving single-target defaults and all-member unresolved
semantics. It must settle child identity and failure/bound diagnostics before any
Reference operator is added. Then separately assess/authorize the narrow Python
Reference adapter and a prospective case; do not freeze Case 0007 automatically.

Production source, production tests, accepted-behavior documentation and ADRs
were not modified. The protected development profile was not run. Only local
diagnostic-helper Ruff/format checks, source-link verification and Git diff checks
apply. Confirmation outcomes were not accessed. This research checkpoint is
committed under repository research convention, without a push.
