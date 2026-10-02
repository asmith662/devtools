# Obligation-Driven Repository Localization for Autonomous Software-Engineering Agents

## Executive conclusion and the right problem formulation

The central hypothesis is **substantially correct, but incomplete**.

The strongest formulation is not “replace global file ranking with obligation-specific rankings.” That would merely create several rankings instead of one. The more useful abstraction is:

> **Repository localization is a cost-sensitive, partially observed coverage-and-diagnosis problem over task obligations, where retrieval actions acquire evidence, repository semantics constrain candidate hypotheses, and the system stops when mandatory information requirements are either resolved, shown not to apply, deliberately deferred to an unavoidable discovery step, or escalated.**

This combines several established traditions rather than fitting cleanly into one. Classical concept/feature location contributes natural-language-to-code retrieval; probabilistic feature location contributes uncertainty and evidence combination; change-impact analysis and slicing contribute dependency closure; high-recall retrieval contributes iterative search and stopping; active hypothesis testing contributes choosing informative observations; adaptive/interactive set cover contributes the idea of satisfying multiple requirements at minimum cost; and agent planning contributes reasoning about observations that reveal new requirements. citeturn6search50turn5search1turn0search5turn14view8turn14view7

The existing `devtools` evidence is particularly important because it rules out a tempting diagnosis. In the two described dogfood tasks, complete BM25 inventories already contained every independently adjudicated required resource, while full-task prompts reached complete coverage only around ranks 35 and 43; structural retrieval did not rescue lexical misses, and subsequent PPR/typed-graph/repository-map variants did not solve complete selection. The empirical problem, as currently observed, is therefore principally **discrimination and coverage accounting after high-recall candidate generation**, not lack of another broad candidate generator. Those observations are supplied as frozen project context rather than independently verified here because the repository itself was not provided. fileciteturn0file0

That matters architecturally. Improved ranking should remain a component, but **a ranking has no native representation for “all mandatory task aspects are covered.”** A ranker assigns relative preference to items. It does not normally represent that `foo.py` and `__init__.py` compete for one role but complement one another for two different roles; that the test obligation is still unresolved although implementation is localized; that configuration probably does not apply; or that the remaining uncertainty cannot be resolved without running a test. Interactive set-cover research is a useful analogy precisely because it makes the objective “satisfy requirements by acquiring a low-cost set of items under uncertainty,” rather than “sort all items well.” citeturn9search2turn14view7turn14view8

I would therefore use the following conceptual pipeline:

```text
Task
  ↓
Task interpretation
  ├── anchors/entities
  ├── constraints
  ├── validation requirements
  └── localization obligations
          ↓
High-recall candidate evidence
  ├── full-task lexical lane
  ├── obligation-scoped lexical lanes
  ├── deterministic RI relations
  ├── repository-role evidence
  └── graph / structural navigation
          ↓
Localization
  ├── candidate hypotheses
  ├── positive & negative evidence
  ├── competition / complementarity
  ├── applicability decisions
  ├── targeted follow-up actions
  └── sufficiency / abstention
          ↓
Obligation-complete information set
          ↓
Context Planning
  ├── declaration span
  ├── export statement
  ├── test case
  ├── documentation section
  ├── configuration entry
  └── whole resource only when needed
          ↓
Coding agent
```

**The word “obligation” is worth keeping, but it should be qualified as `LocalizationObligation`.** In IR, “subquery,” “facet,” and “information need” are more established, while software engineering uses terms such as feature location, impact set, suspicious entity, and dependency. None carries the needed combination of applicability, satisfaction cardinality, coverage state, and stopping semantics. A subquery says what to search for; an obligation says what must become known before localization can legitimately declare itself sufficient. Modern RAG work already finds value in decomposing complex requests into competing subqueries and deciding sequentially where to spend retrieval effort, but that still lacks the stronger completion semantics required here. citeturn13search17turn5search0

The most important modification to the emerging hypothesis is that **obligations cannot be the only task structure**. The task should separately encode:

| Task construct | Example | Why it should not be collapsed into an obligation |
|---|---|---|
| Anchor/entity | ``Obligation`` | Shared subject of several obligations. |
| Obligation | “Expose `Obligation` publicly” | Something localization must satisfy. |
| Constraint | “Preserve compatibility” | Constrains candidate/edit choices rather than identifying one file. |
| Validation requirement | “Run `pytest …`” | Produces an executable completion condition. |
| Explicit location | `src/foo.py` | Strong evidence/constraint, not itself a work requirement. |
| Conditional requirement | “Register it if registry participation is required” | Must support `NOT_APPLICABLE`, not force retrieval forever. |

This is also the answer to the repeated-concept question. `implement Obligation`, `export Obligation`, `test Obligation`, and `document Obligation` should **not primarily be interpreted as four extra term-frequency votes for the token `Obligation`**. They are four predicate–argument relations around one shared anchor:

```text
IMPLEMENT  → Obligation
EXPORT     → Obligation
TEST       → Obligation
DOCUMENT   → Obligation
```

Term weighting remains useful, and IR literature shows that weighting and query structure materially affect retrieval, but the repeated identifier is more valuable here as evidence of *cross-obligation identity*. Query decomposition research similarly treats distinct subqueries as separate opportunities whose utility evolves as evidence is collected. citeturn13search6turn13search17

This leads to a more precise objective. Let \(O_M\) be mandatory localization obligations, \(U\) repository information units, \(A_o\) the acceptable satisfaction alternatives for obligation \(o\), and \(C(S)\) the cost of acquiring/disclosing selected information \(S\). The practical objective should be **lexicographic**, not a single relevance score:

\[
\text{first maximize } P(\text{all mandatory obligations covered}),
\]

\[
\text{then minimize unresolved mandatory uncertainty},
\]

\[
\text{then minimize acquisition and Context cost},
\]

\[
\text{then add helpful-only information by marginal utility}.
\]

This deliberately treats missing a mandatory resource differently from admitting one extra helpful resource. High-recall review literature reaches a related conclusion: the difficulty is not merely ranking well at the head but knowing when the remaining unseen relevant material is acceptably small, and newer decision-theoretic work argues that stopping should reflect the downstream value and cost of further search rather than a purpose-independent recall threshold. citeturn7search0turn7search11turn14view6

Finally, **do not require exact complete pre-localization in the universal case**. Repository-level work can contain dependencies whose relevance is only exposed by inspecting an implementation, running a validation command, observing an error, or executing a path. Change-impact work explicitly exists because effects propagate through dependencies, and systems such as CodePlan adapt plans using dependency and may-impact analysis rather than presupposing that every edit is knowable from the initial request. citeturn15search0turn0search0turn0search1

The correct boundary is:

> **Frontier-complete localization:** before expensive implementation begins, resolve everything that should be inferable from the task, cached repository facts, inexpensive retrieval, and bounded structural analysis; explicitly identify the remaining uncertainty frontier; permit later exploration only when some necessary fact genuinely depends on newly inspected or executed information.

That gives a principled distinction between **avoidable exploration**—a required test/export/configuration file was already inferable and the localizer simply failed—and **inherent discovery**—for example, only executing the resolved test reveals an undocumented generated artifact or runtime registry. The distinction should itself become an evaluation label.

## What the evidence says about retrieval, structure, graphs, and agent exploration

**Established finding: repository localization is already known to be more than text similarity.** Early concept-location work used latent semantic retrieval to map natural-language concepts into code; later feature-location research combined IR with execution evidence and explicitly framed localization as decision making under uncertainty. Iterative feature location propagated relevance through context instead of treating each artifact independently, and automatic query reformulation used initially retrieved artifacts to improve later searches. These strands strongly support iteration and heterogeneous evidence, but none by itself solves multi-obligation completion. citeturn6search50turn5search1turn5search0turn5search2

**Fault localization is useful but is not the governing abstraction.** Fault localization usually tries to rank program entities by likelihood of containing a fault; IR-based and spectrum-based approaches commonly report measures such as top-\(N\) or mean reciprocal rank. That is valuable for “find the defect,” but an implementation/API/test/docs/configuration task asks for several heterogeneous things that may all be correct and necessary simultaneously. A suspiciousness ranking therefore resembles one evidence channel for an implementation-owner obligation, not the complete architecture. citeturn13search1turn13search2

**Change-impact analysis is closer for closure obligations.** Static and dynamic impact techniques reason about which program components may be affected by a change, and published approaches deliberately trade precision, recall/safety, and analysis cost. This makes them appropriate when an obligation is “find all dependents that must be reconsidered,” but much less appropriate for documentary or governance obligations that are not present in a code dependency graph. citeturn0search5turn0search1turn0search0

**Active high-recall search contributes the strongest stopping analogy.** TREC Total Recall and continuous-active-learning work treat retrieval as an iterative process aimed at finding almost all relevant material; research has consequently developed explicit stopping rules rather than assuming a rank cutoff proves completeness. Recent work continues to treat stopping as a separate estimation/decision problem. This directly argues against interpreting “the next candidate score is low” as sufficient proof that repository localization is complete. citeturn7search0turn7search5turn7search9turn14view6

**Adaptive and interactive set cover provide the strongest abstract mathematical analogy.** Adaptive submodularity studies sequential decisions whose outcomes are uncertain and establishes conditions under which adaptive greedy policies approximate optimal coverage; interactive submodular set cover connects coverage with identification of an unknown hypothesis. These guarantees should **not** be imported wholesale into `devtools`: repository dependencies can introduce complementarity, obligations can be discovered dynamically, and the utility need not be submodular. But the abstraction—low-cost actions that progressively establish coverage—is significantly closer than global file ranking. citeturn14view8turn14view7turn9search0

**Active hypothesis testing contributes the candidate-competition model.** In sequential hypothesis testing and active learning, observations are selected because they discriminate between possible underlying states, sometimes under nonuniform observation cost. That is a useful model for “which of these three modules actually owns this declaration?” Crucially, it should be applied **within an obligation slot**, not by forcing every possibly useful repository file into one probability simplex. citeturn8search11turn8search16

### Repository roles should be evidence, not ontology-by-filename

The distinction requested between conventions is important:

| Convention class | Example | Recommended interpretation |
|---|---|---|
| Near-universal/raw fact | extension, basename, root depth, exact path | Deterministic RI fact. |
| Language/ecosystem convention | `pyproject.toml`, Python package layout | Deterministic identification plus strong role evidence. |
| Tool convention | pytest `testpaths`, `python_files` | Parse configuration into RI; task-relative implication can be strong or sometimes proof-like. |
| Framework convention | framework registries/routes/models | Framework-specific analyzer/evidence; never pretend universal. |
| Repository-specific convention | `foo.py` ↔ `test_foo.py`, custom `checks/` | Derived repository evidence or learned prior. |
| Arbitrary heuristic | “files called `manager.py` are probably important” | Weak evidence only. |

The Python packaging specification makes `pyproject.toml` structured rather than merely conventional: it defines standard `[build-system]`, `[project]`, and `[tool]` namespaces, including entry-point/script metadata. By contrast, `src/` is explicitly an alternative project layout to a flat repository layout, so “implementation must be under `src/`” would be an unsafe hard constraint. citeturn16search3turn16search17turn16search0

Pytest illustrates the same hierarchy particularly well. Its default collection behavior and `testpaths` provide strong test-role evidence, but projects can alter discovery with configuration such as `python_files`, ignore paths, and `conftest.py` behavior. Therefore “search `tests/`” is a useful routing prior, whereas “a file outside `tests/` cannot satisfy a test obligation” is generally false. citeturn16search21turn16search23turn16search33

The recommended implementation is **multi-label `ResourceRoleEvidence`**, not one `FileRole` enum:

```text
resource: tests/unit/test_obligations.py

evidence:
  TEST:
    - path convention: tests/
    - pytest filename pattern: test_*.py
    - configured collection scope: included
    - mirrored source relation: src/devtools/obligations.py
  PYTHON_CODE:
    - extension: .py
```

Raw observations belong in RI. Their implication for a particular obligation belongs in Retrieval or Localization. This preserves the existing distinction between repository truth and task relevance.

### Scope narrowing should be asymmetric

For `find tests for Obligation`, likely test resources should receive dramatically more retrieval attention, but the safe production pattern is:

```text
primary lane:  obligation-scoped test-role candidates
secondary lane: mirrored/structurally connected test candidates
escape lane:   global lexical candidates from the full task/anchor
```

The escape lane matters. The localizer should be allowed to say, “the best candidate is outside the expected role scope, so broaden rather than discard it.” This gives most of the computational gain of hierarchical retrieval without placing recall at the mercy of repository layout assumptions. Agentless independently illustrates the value of hierarchical localization: it moves from files to related classes/functions and then to fine-grained edit locations, rather than placing a full repository directly into the repair prompt. citeturn15search1turn15search3

Recent repository-retrieval benchmarks reinforce the need for multiple routes. Agent Retrieval Bench defines relevance by the *next workflow need* rather than textual similarity and reports different retrieval families winning different task types; its selective-retrieval experiments also expose a calibration problem when systems must decide that no local context is appropriate. SWE-Explore likewise isolates repository exploration and evaluates files and line regions using coverage and efficiency instead of only final repair success. These are recent 2026 results and should be treated as emerging rather than settled evidence, but they align strongly with obligation-conditioned retrieval and explicit abstention. citeturn15search4turn15search7turn15search6

### Positive and negative evidence must be asymmetric too

A candidate can accumulate positive evidence from exact ownership, export resolution, test references, task wording, path role, structural relationships, and lexical matches. But **negative evidence deserves a much higher proof standard than positive evidence** because one erroneous exclusion can destroy complete recall.

IR literature has long supported both positive and negative relevance feedback, but negative feedback is not magical evidence of impossibility; it modifies subsequent search based on observed nonrelevance and can be especially difficult when the initial query is poor. Modern pseudo-relevance-feedback work similarly documents cases where noisy feedback degrades effectiveness. citeturn17search1turn17search6

For `devtools`, use this ladder:

| Evidence | Permitted effect | Example |
|---|---|---|
| Weak negative | Lower ranking only | ordinary `.md` for an implementation-owner obligation |
| Role mismatch | Strong demotion / leave escape lane | implementation module for a test obligation |
| Bounded semantic contradiction | Suppress for one obligation slot | parser proves this file does not own the exact syntactic declaration |
| Deterministic exclusion under explicit configuration | Possibly eliminate for that slot | resource lies outside an authoritative bounded candidate frame |
| Sound impossibility proof | Hard eliminate | wrong resource identity/snapshot; exact required artifact class provably absent under the declared semantic model |

A critical qualification is **“for that obligation slot.”** A Markdown resource excluded from `PYTHON_DECLARATION_OWNER` is not globally irrelevant; it may be the required documentation resource. Likewise, resolving the unique syntactic owner of `Obligation` should suppress alternative owner candidates, but it should not suppress `__init__.py`, its tests, or its documentation because those satisfy complementary obligations.

Graph disconnection should almost never be hard negative evidence. Python permits dynamic behavior, graphs are bounded abstractions, and documentation/configuration/governance edges are often absent. A disconnected graph node may therefore mean “our graph cannot justify a connection,” not “no relevant relationship exists.” Change-impact research itself shows why soundness/precision tradeoffs matter when dependency approximations are used. citeturn0search1turn0search5

### Aider: what its repository map actually does

Aider is especially useful because its documentation and source code make the boundary explicit.

Aider says its repo map contains important classes, functions, signatures, files, and defining lines and is sent to the model as compact repository context. Critically, its documentation says that when more code is needed, **the language model uses the map to decide which specific files it needs to see**. For large repositories, Aider uses a file-dependency graph and graph ranking to choose which portions of the map fit its token budget. citeturn14view0

Its current implementation extracts definitions and references, constructs a directed graph from referencer files to files defining shared identifiers, applies heuristic weight adjustments—including strong boosts involving files already in chat—and runs NetworkX PageRank. It then distributes PageRank through identifier edges to rank definitions and renders as much of the resulting map as will fit the map budget. citeturn14view1turn14view2

So the requested answers are:

| Question | Answer |
|---|---|
| **Does Aider determine the exact set of files required for a task through its graph?** | **No.** Its graph ranks content for a compact map; the model still decides which files need inspection. citeturn14view0turn14view2 |
| **Does it construct a compact repository map that helps the model reason and choose what to inspect?** | **Yes; this is precisely how Aider describes the map.** citeturn14view0 |
| **How are files/symbols ranked?** | Definition/reference tags induce file edges; mention/chat-state heuristics alter weights/personalization; PageRank is computed; rank is redistributed to definitions; map content is truncated to the token budget. citeturn14view1turn14view2 |
| **How much responsibility remains with the model?** | Substantial responsibility: the map helps the LLM decide what additional files to request and ultimately what to change. citeturn14view0 |
| **What does Aider’s graph accomplish that the described `devtools` graphs do not?** | Based on the supplied `devtools` description, the fundamental difference is **not richer semantics**. `devtools` RI is already more explicitly typed. Aider’s distinctive production contribution is the end-to-end integration of graph ranking with a compact, model-facing symbol representation, token budgeting, mention/chat personalization, and interactive file acquisition. This is an architectural inference from Aider’s implementation and the supplied `devtools` description, not evidence that Aider’s graph solves exact localization. citeturn14view0turn14view2 |

That strongly suggests a revised interpretation of your negative PPR results: **PageRank may have been asked to solve the wrong stage.** Graph structure is valuable for owner/export/dependency resolution, change-impact expansion, follow-up navigation, and compact structural explanation even if it is mediocre as the final universal resource ranking.

LocAgent provides complementary modern evidence. It constructs directed heterogeneous repository graphs and lets an LLM agent navigate them through multi-hop reasoning; the reported benefit is better code localization and downstream repair, not a proof that a graph deterministically yields the complete heterogeneous resource set. citeturn14view3

CodePlan goes further in the program-analysis direction: it combines incremental dependency analysis, may-impact analysis, and adaptive planning for repository-wide edits, demonstrating that dependency structure can be most useful for **propagating known changes and sequencing follow-up work**, rather than globally ranking every repository artifact against the original task. citeturn15search0

SWE-agent provides an important negative lesson about dumping retrieval evidence into the coding model. Its ACI documentation reports that a 100-line file viewer worked well and that full-directory string search deliberately returned succinct file matches because displaying more match context confused the model. That is direct evidence for keeping **localization acquisition** separate from **Context disclosure**. citeturn18view0

## Recommended `devtools` architecture and production abstractions

The existing high-level layering should largely survive:

```text
Repository Intelligence
        ↓
Retrieval evidence
        ↓
Localization                 ← NEW FIRST-CLASS RESPONSIBILITY
        ↓
Context Planning
        ↓
Materialization
        ↓
Model request
```

**DECIDE NOW:** introduce **Localization** as a first-class domain.

This is not merely a new name for Retrieval. Retrieval answers questions such as “what repository information provides evidence about X?” Localization owns stateful task-relative judgments such as “which evidence satisfies this obligation?”, “are these candidates competitors?”, “is this obligation unresolved?”, “is registration inapplicable?”, “what follow-up retrieval would resolve the ambiguity?”, and “can we safely stop?” Context Planning should not own those decisions because its responsibility is how established information is represented and disclosed.

The literature offers precedents for each constituent responsibility, but this exact boundary is an architectural proposal tailored to `devtools`. Hierarchical localizers such as Agentless already distinguish localization from repair, while active-retrieval literature distinguishes retrieval actions from stopping decisions. citeturn15search1turn7search0turn14view6

The core production model should be:

```python
TaskModel
  anchors: [...]
  constraints: [...]
  obligations: [...]
  validation_requirements: [...]

LocalizationObligation
  id
  kind
  subject_anchor_ids
  task_source_spans
  requirement: MANDATORY | CONDITIONAL | HELPFUL
  satisfaction_rule
  scope_hints
  dependencies
  status

CandidateAssignment
  obligation_id
  target_id              # resource or finer information unit
  satisfaction_slot
  evidence_ids
  state

LocalizationEvidence
  kind
  polarity
  target_id
  obligation_id
  provenance
  strength
  semantic_scope
  observation

LocalizationResult
  selected_assignments
  unresolved_obligations
  not_applicable_obligations
  deferred_discovery
  eliminated_assignments
  validation_plan
  sufficiency_record
```

The decisive concept is **satisfaction semantics**. Different obligations must not share one universal “relevant file” interpretation:

| Satisfaction form | Example | Candidate relationship |
|---|---|---|
| `ONE_OF` | owner of exact declaration | Candidates mostly compete. |
| `AT_LEAST_ONE` | locate an existing test exemplar | Several can satisfy; one may be enough for understanding. |
| `COMPONENT_COVER` | implementation behavior split across model + adapter | Candidates complement different components. |
| `CLOSURE` | all statically impacted exports/dependents | Candidate set grows until closure condition. |
| `CONDITIONAL` | registration/configuration if the repository uses a registry | Must establish applicability before demanding a file. |
| `VALIDATION` | identify runnable checks proving the change | Resource plus executable command/config evidence may satisfy it. |

This avoids a fundamental probabilistic mistake: **do not normalize all “relevant files” against one another.** Evidence for `src/foo.py` as the implementation owner may reduce belief in another implementation owner because those hypotheses compete. It should not reduce belief in `tests/test_foo.py` because those assignments are complementary.

**Confidence should be explicit, but numeric posterior probabilities should not be production-critical initially.** V1 should represent calibrated *semantics* before calibrated *numbers*:

```text
PROVEN_WITHIN_MODEL
STRONGLY_SUPPORTED
PLAUSIBLE
CONTRADICTED
ELIMINATED
UNKNOWN
```

A score used to order candidates may still exist, but it should be called a **score**, not a probability. Eventually, probabilities can be calibrated separately for obligation kinds and evidence mixtures; until then, a fabricated `0.91 confidence` gives downstream stopping logic unjustified precision. Agent Retrieval Bench's 2026 selective-retrieval results are an especially timely warning: thresholds that worked on counterfactual controls did not straightforwardly solve natural no-gold selective cases. citeturn15search4turn15search7

The following table gives the requested architectural ownership decisions.

| Requested concern | Recommendation | Owner |
|---|---|---|
| Conceptual model | Multi-obligation evidence-driven localization under cost and uncertainty | Localization |
| Major new abstraction | `TaskModel`, `LocalizationObligation`, `CandidateAssignment`, evidence ledger, sufficiency record | Localization |
| Existing RI | Keep its deterministic/provenance-oriented philosophy | RI |
| Existing BM25 | Keep as high-recall baseline and broad fallback | Retrieval |
| Existing structural retrieval | Keep as typed evidence/action source | Retrieval |
| Current PPR/repo-map | Remove status as presumed final selector; reuse as navigation/map evidence | Retrieval + Context |
| Historical experimental code | Reinspect before rebuilding References/Calls/test links/graph expansion/fusion/dogfood machinery | Implementation process |
| New RI facts | Path/file metadata, recognized tool configuration, public export/re-export facts, test-discovery configuration, package entry points, documentation/build metadata where sound | RI |
| Obligations | First-class, source-span-backed, typed, cardinality-aware, applicability-aware | Localization |
| Candidate evidence | Typed positive/negative evidence with native provenance and semantic scope | Retrieval produces; Localization consumes |
| Confidence | Explicit categorical state now; calibrated probabilities later | Localization/Learning |
| Positive/negative interaction | Positive evidence accumulates; negative evidence may demote; proof-strength contradiction alone hard-eliminates | Localization |
| Candidate resolution | Competition within obligation slots; complementarity across slots/components | Localization |
| Repository roles | Multi-label role evidence, never a single hard filename-derived class | RI facts + Retrieval/Localization priors |
| Graphs | Resolve relations, navigate, establish closure, explain, compact—not universal final ranker | RI/ Retrieval/Context |
| Follow-up retrieval | Triggered by unresolved obligation or discriminating ambiguity | Localization |
| Stopping | Sufficiency certificate over obligations, not rank cutoff | Localization |
| Context consumption | Obligation-linked information units, smallest sufficient representation | Context Planning |
| Learning | Later learn uncertain mappings/weights/calibration/policies; retain exact semantics deterministically | Learning |

### New Repository Intelligence worth adding

The highest-value additions are **facts that make later evidence stronger**, not speculative relevance labels.

**DECIDE NOW:** represent exact path, basename, suffix/language, root-relative location, package/source membership, and recognized project metadata as first-class snapshot-bound facts if they are not already. Parse `pyproject.toml` structurally so build system, project metadata, scripts/entry points, and tool configuration can be queried without lexical guessing. The PyPA specification gives these fields standardized semantics. citeturn16search3turn16search17

**DECIDE NOW:** strengthen public-surface facts: syntactic `__all__`, resolvable package re-exports, import/member chains, and bounded “publicly reachable from package surface” relations. Because Python permits dynamic behavior, these must preserve the same bounded-semantics discipline as current RI rather than claiming universal runtime truth.

**DECIDE NOW:** add structured test-discovery/configuration facts for recognized frameworks. For pytest this means configured `testpaths`, file-pattern configuration, package relationships, and known collection exclusions where statically explicit. Treat dynamic `conftest.py` behavior conservatively rather than manufacturing proof. Pytest explicitly permits customization, demonstrating why raw directory conventions alone are insufficient. citeturn16search21turn16search23

**TEST FIRST:** documentation navigation facts, such as MkDocs/Sphinx indexes and explicit references, are likely useful for documentation obligations but should prove value before a large cross-framework abstraction is built.

**TEST FIRST:** generic source-code “registry” semantics. Some Python frameworks encode registration through decorators, calls, dictionaries, metaclasses, plugins, or dynamic import. Prefer framework/plugin analyzers for recurring patterns rather than pretending `registry.py` has universal meaning.

### Retrieval should generate obligation-relative evidence

Keep the full task prompt as a broad lexical query because your existing dogfood found it materially stronger than hand-written short InformationNeeds. Add per-obligation retrieval **alongside**, not instead of, that baseline.

For a task such as:

```text
Add Obligation to the public API,
test it,
document its semantics,
and run repository validation.
```

issue conceptually distinct retrieval operations:

```text
Broad recall:
    full original task

Implementation:
    exact identifier + implementation verbs + symbol ownership

Public API:
    exact identifier + export/re-export/package-surface evidence

Tests:
    exact identifier + test role + mirrored source/test relationships

Documentation:
    exact identifier/domain phrase + documentation-role scope

Configuration/registration:
    exact identifier + registration/config metadata + framework evidence

Validation:
    explicit commands + pyproject/tox/nox/CI/tool configuration
```

Explicit paths, filenames, backticked code identifiers, fully qualified names, and commands should be preserved as anchors. Repeated domain terms across independent clauses should generate shared anchor identity rather than merely larger query term frequency. Aider itself treats mentioned identifiers and files specially in graph personalization, providing one concrete open-source example of distinguishing explicit task mentions from ordinary token frequency. citeturn14view1turn14view2

### Sequential follow-up should be bounded and evidence-directed

Do not build a general autonomous research agent inside Retrieval. Use a small action vocabulary first:

```text
LOOKUP_EXACT_SYMBOL
SEARCH_LEXICAL(scope, query)
LOOKUP_OWNER
FOLLOW_IMPORT_OR_EXPORT
FIND_REFERENCERS
FIND_MIRRORED_TESTS
SEARCH_TEST_SCOPE
SEARCH_DOC_SCOPE
READ_INFORMATION_UNIT
EXPAND_DEPENDENCY_NEIGHBORHOOD
INSPECT_PROJECT_CONFIG
```

The next action is selected only because it can resolve an explicit uncertainty. Examples:

```text
Two plausible owners remain
→ inspect exact declaration ownership.

Implementation resolved, export unresolved
→ traverse import/re-export relationships.

Test obligation has only weak lexical hits
→ query test-role scope + mirrored paths.

Registration applicability unknown
→ inspect project/framework registry evidence.

All mandatory obligations resolved
→ do not issue another search merely because candidates remain.
```

That is much closer to active hypothesis testing and adaptive search than to one-shot ranking. citeturn8search11turn13search17

## Candidate architectures, decisions, and the role of exact pre-localization

The candidate architectures do not have equal status.

| Strategy | Strength | Primary failure mode | Recommendation |
|---|---|---|---|
| **A. Improved global ranking** | Simple, inexpensive, preserves broad recall | Cannot express obligation completeness or competing/complementary roles | **Retain as baseline/candidate generator; reject as governing architecture** |
| **B. Obligation-specific retrieval** | Makes heterogeneous needs explicit; easy to evaluate | Decomposition errors; independent obligations can duplicate work | **Adopt as backbone** |
| **C. Hierarchical localization** | Efficiently exploits test/docs/config/subsystem structure | Hard routing can silently destroy recall | **Adopt with soft routing + global escape lane** |
| **D. Evidence-based hypothesis resolution** | Enables competition, negative evidence, explanation, applicability | Added state/model complexity | **Adopt in deliberately simple form** |
| **E. Sequential active retrieval** | Resolves ambiguity instead of dumping candidates | Extra latency and difficult stopping | **Adopt only for unresolved obligations** |
| **F. Agent-directed exploration** | Handles unexpected/latent semantics | High token cost, variable behavior, difficult evaluation | **Use as bounded escalation** |
| **G. Hybrid** | Covers broad recall, structured selection, and latent discovery | Can become an overengineered planning framework | **Recommended, provided the first version is B+C+D with bounded E; F is fallback and A remains safety net** |

This recommendation is consistent with what public coding systems collectively demonstrate, without claiming they already implement the proposed architecture. Agentless shows hierarchical narrowing; LocAgent demonstrates graph-guided multi-hop localization; SWE-agent demonstrates benefits from constrained exploration interfaces; CodePlan demonstrates dependency-driven adaptive planning; none establishes a general exact pre-task file oracle. citeturn15search3turn14view3turn18view0turn15search0

### DECIDE NOW

**Create the Localization boundary.** The missing responsibility is real, not terminological: something must own obligation states, competing assignments, evidence aggregation, follow-up decisions, and stopping.

**Make obligations first-class but not synonymous with task clauses.** Store task-span provenance and shared anchors so decomposition remains auditable.

**Retain full-prompt BM25 as a recall safety lane.** Your own observations favor it over manually compressed InformationNeeds, and modern repository-retrieval results likewise show no universally dominant retrieval family. citeturn15search4

**Use role-aware soft scoping.** A test query should search likely tests first; it should not pretend test location is universally determined by `tests/`. Python tooling explicitly permits multiple layouts and customized test discovery. citeturn16search0turn16search23

**Make hard elimination proof-carrying.** Every elimination should cite the deterministic fact/invariant and the exact obligation slot it excludes. “Low score” is never sufficient.

**Treat graphs primarily as relationship operators.** Ownership/export navigation, impact closure, neighborhood expansion, candidate confirmation, and compact Context representation are better-supported uses than “global PageRank decides the complete task set.” Aider and LocAgent both use graphs as compact structural aids to subsequent reasoning rather than exact heterogeneous task-completion oracles. citeturn14view0turn14view3

**Carry obligation provenance into Context Planning.** Context should know *why* each disclosure exists.

**Make validation a localization obligation.** A localizer that identifies implementation/tests but cannot tell the agent which repository checks prove success is not task-complete.

### TEST FIRST

**Automatic obligation decomposition.** Start with deterministic extraction of explicit code identifiers, paths, commands, and high-precision verbs plus an explicit fallback `GENERAL_TASK` obligation. Compare rule-based versus model-assisted decomposition prospectively before allowing decomposition errors to control recall.

**Satisfaction-cardinality inference.** `ONE_OF`, `AT_LEAST_ONE`, closure, and component-cover semantics are powerful, but incorrect multiplicity assumptions could prematurely stop search.

**Evidence weighting and categorical thresholds.** Measure whether owner/export/test/path evidence actually discriminates required candidates before tuning elaborate formulas.

**Probabilistic confidence.** Only after prospective labels exist should candidate states be calibrated into probabilities, separately by obligation family.

**Expected-information-gain action selection.** A simple unresolved-first policy may be sufficient. The theoretical active-learning machinery becomes worthwhile only if query-choice cost materially affects outcomes. citeturn14view8turn8search11

**Repository-specific convention learning.** Mirroring and naming patterns can be learned from the repository, but first measure whether deterministic pattern statistics provide enough value.

**Fine-grained Context units beyond code symbols.** Test cases, documentation sections, config keys, and validation-command definitions are promising because contemporary exploration benchmarks find line-level efficiency remains challenging even when file-level localization is strong. citeturn15search6

**History/repository memory.** Recent work reports gains from adding repository memory to graph-guided localization, but this should wait until snapshot-local semantics are well evaluated rather than complicating the first localization kernel. citeturn11search4

### DEFER

**Universal exact pre-localization.** It is not a defensible requirement for all repository tasks.

**Hard path filters based on conventions.** `src/`, `tests/`, `docs/`, `README.md`, and filenames are useful evidence, not universal truths.

**An opaque repository-wide Bayesian model.** The semantics of competition and complementarity need to be correct before numerical inference is worth trusting.

**End-to-end reinforcement learning for retrieval policy.** There is no evidence yet that the current bottleneck requires it.

**Replacing BM25 simply because dense retrieval is newer.** Modern repository-retrieval results show task-dependent winners, while your current evidence says lexical candidate recall is already strong. citeturn15search4

**Global PPR optimization as the next major experiment.** The current evidence and Aider implementation suggest more productive graph roles.

**Trying to infer proprietary IDE internals.** Public evidence should constrain claims; this report makes no undocumented assertions about Cursor or similar systems.

### The principled boundary for exploration

A required resource should be labeled **avoidable exploration** if, at task start, it was recoverable from frozen task text plus available RI, configured retrieval indices, recognized repository/tool conventions, and bounded cheap structural operations.

It is **inherent discovery** if its requirement depends on an observation that did not yet exist—for example:

```text
run test
→ observe plugin-specific failure
→ learn previously unmentioned generated schema must change
```

or:

```text
inspect resolved implementation
→ discover runtime dispatch registry not represented in current RI
→ follow newly observed registry reference
```

The second category should not excuse weak RI forever. If a pattern occurs repeatedly, it becomes a candidate for new Repository Intelligence. In that sense, inherent discovery is **relative to the system's declared semantic capabilities at the frozen snapshot**, not a permanent metaphysical category.

This view is compatible with adaptive planning research: CodePlan discovers and propagates consequences through dependency analysis as work progresses rather than assuming a one-shot static plan suffices. citeturn15search0

## Stopping, Context sufficiency, and evaluation

A single universal confidence threshold should not decide readiness. The localizer should produce a **sufficiency certificate**.

For each mandatory obligation, exactly one of these states must hold:

```text
RESOLVED
    Evidence supports a satisfying assignment under this obligation's rule.

NOT_APPLICABLE
    Evidence supports that the conditional obligation does not apply.

DEFERRED_INHERENT_DISCOVERY
    Further determination requires a named execution/inspection action
    whose prerequisite has only now become known.

ABSTAIN
    The system cannot resolve the obligation safely within policy/budget.
```

`OPEN` is not a stopping state.

A result might therefore look like:

```text
IMPLEMENTATION_OWNER
  RESOLVED → src/devtools/obligations.py::Obligation

PUBLIC_API
  RESOLVED → src/devtools/__init__.py export span

TEST_BEHAVIOR
  RESOLVED → tests/test_obligations.py::test_...

DOCUMENTATION
  RESOLVED → docs/... section

REGISTRATION
  NOT_APPLICABLE
  because: no applicable registry/entry-point mechanism found under
           recognized repository semantics

VALIDATION
  RESOLVED → pytest ... ; ruff ... ; type-check command ...

UNKNOWN_DYNAMIC_INTEGRATION
  DEFERRED_INHERENT_DISCOVERY
  trigger: only if validation reports plugin registration failure
```

This certificate is more defensible than “confidence > 0.85” because it exposes the assumptions under which stopping occurred. Total-recall and TAR literature similarly treats stopping as a distinct estimation/decision task rather than a direct consequence of the retrieval ranker. citeturn7search0turn7search11turn14view6

A follow-up round should trigger when any mandatory obligation is `OPEN` **and** at least one bounded retrieval/inspection action could plausibly discriminate its remaining hypotheses at reasonable cost. Stop when all mandatory obligations have an admissible terminal state and either no unresolved optional information has marginal utility sufficient to justify its cost or the Context budget has been reached.

### Required and helpful Context should be optimized differently

Keep the existing adjudication distinction between `REQUIRED`, `HELPFUL_ONLY`, and `UNNECESSARY`. Do not collapse them into graded relevance.

The preferred policy is:

\[
\text{mandatory completeness} \gg
\text{avoid unnecessary Context} \gg
\text{optional helpful utility}.
\]

A helpful architectural overview can be valuable, but it should not consume budget needed for an unresolved API export. Once all mandatory obligations are satisfied, helpful Context can be admitted by marginal expected utility per token.

This aligns with contemporary repository-exploration evaluation, which increasingly distinguishes core versus optional context and measures context efficiency rather than only file hits. SWE-Explore's released benchmark explicitly uses core/optional regions and ranked line budgets, although its trajectory-derived labels differ from your stronger independent blind-adjudication methodology. citeturn15search6

### Transition from files to information units

Obligation localization provides the natural bridge.

Do not stop at:

```text
TEST → tests/test_obligations.py
```

when RI or targeted inspection can establish:

```text
TEST
  → tests/test_obligations.py
  → TestObligation
  → test_public_semantics
  → lines 88–116
```

Likewise:

```text
PUBLIC_API
  → package/__init__.py
  → import/re-export statement

CONFIGURATION
  → pyproject.toml
  → [project.entry-points."..."]
  → one TOML entry

DOCUMENTATION
  → docs/design.md
  → "Obligations" section
```

Agentless already demonstrates file→element→fine-grained localization, while SWE-Explore's emphasis on line-level efficiency suggests that file-level success can conceal substantial Context waste. citeturn15search3turn15search6

Whole-resource disclosure should therefore become an **explicit representation choice**, not the default consequence of locating a resource.

### Evaluation protocol

Your existing prospective freezing and blinded adjudication are strong foundations. Improve them by adjudicating **obligations and acceptable satisfaction alternatives**, not only resources.

Before running any evaluated localizer, freeze:

1. repository snapshot and eligible frame;
2. complete task text;
3. baseline full-prompt query;
4. localizer implementation/configuration;
5. obligation-generation policy/model/version;
6. role rules and recognized ecosystem/framework analyzers;
7. hard-elimination rules;
8. follow-up-action policy and maximum search budget;
9. Context-unit construction policy;
10. validation obligations.

The adjudicator should remain blind to retrieval provenance and additionally label:

```text
obligation applicability
mandatory / conditional / helpful status
acceptable alternative resource or information-unit sets
required vs helpful-only units
whether each requirement was inferable at task start
or only after a named observation
```

At least difficult `REQUIRED`/`HELPFUL_ONLY` and `INFERABLE`/`INHERENT` decisions should receive independent second adjudication or masked consensus. Recent benchmark work increasingly isolates retrieval/exploration from final patching, but trajectory-derived gold can encode behavior of the agents that generated it; your independent prospective adjudication can therefore be an important complementary design. citeturn15search7turn15search6

Let \(A_o=\{A_{o1},A_{o2},...\}\) be acceptable alternative information-unit sets for obligation \(o\), rather than requiring a single canonical gold file set.

Define obligation satisfaction:

\[
sat(o,S)=
\begin{cases}
1 & \exists A\in A_o : A\subseteq S \\
0 & \text{otherwise}
\end{cases}
\]

and **mandatory obligation coverage**:

\[
OC(S)=\frac{1}{|O_M|}
\sum_{o\in O_M} sat(o,S).
\]

Then **complete obligation coverage** is:

\[
COC(S)=\mathbf{1}[OC(S)=1].
\]

This is superior to fixed Recall@K as the primary metric because it adapts to tasks with different numbers and kinds of required artifacts.

The evaluation suite should report, separately rather than collapsing everything into one score:

| Metric | What it tests |
|---|---|
| **Complete mandatory obligation coverage** | Did localization satisfy the whole task information contract? |
| **Macro obligation recall** | Which obligation classes fail most often? |
| **Required-resource recall** | Compatibility with existing adjudication. |
| **Required information-unit recall** | Whether span-level localization loses needed information. |
| **Required-set complete at handoff** | Direct yes/no pre-coding success. |
| **Selected resource/unit count** | Waste at final handoff. |
| **Selected token/byte cost** | Actual Context burden. |
| **Cover cost** | Cumulative searches/opens/analysis cost until all gold obligations were first covered. |
| **Excess Context ratio** | Additional disclosed cost beyond a minimal accepted gold alternative. |
| **HELPFUL_ONLY admission** | Whether useful optional Context is added after required coverage. |
| **UNNECESSARY admission** | Precision/waste signal. |
| **Retrieval rounds** | Sequential-search overhead. |
| **Searches/file opens avoided** | Agent-work reduction. |
| **Post-handoff exploration** | How many additional resources the coding agent must discover. |
| **Avoidable exploration misses** | Most important diagnostic for localization weakness. |
| **Inherent-discovery count** | Measures irreducible downstream exploration. |
| **False hard eliminations** | Safety metric; required resources must essentially never be proof-eliminated. |
| **Abstention quality** | Does uncertainty produce safe escalation rather than false certainty? |
| **Task success + validation success** | End-to-end consequence. |
| **Wall-clock and compute cost** | Production viability. |

For comparisons across variable-sized tasks, **coverage cost** is particularly useful: how much acquisition effort had been expended at the first point where all required obligations were represented. This resembles the “cover time” perspective studied in ranking/set-cover work. citeturn9search17

Also distinguish three costs:

\[
C_{\text{index}}
,\quad
C_{\text{localize}}
,\quad
C_{\text{context}}.
\]

A 500-file BM25 internal candidate inventory may be almost free if no model sees it; opening 50 files with an LLM is not. Therefore “candidate count” alone is not a sufficient cost measure.

For statistically meaningful comparison, evaluate policies over prospectively held-out real tasks, pair each task across systems, and report task-level distributions and paired bootstrap confidence intervals rather than only averages. Most importantly, **do not tune a rule after examining required resources for the task on which that rule is reported**.

### Efficiency architecture

Repository Intelligence, lexical indexes, symbol maps, file-role observations, and graph projections should remain **snapshot-bound reusable artifacts**. Per-task Localization should mostly manipulate compact IDs and evidence records. Aider's current repo-map implementation similarly caches tag extraction and avoids rescanning unchanged content on every request, illustrating the practical importance of amortizing repository analysis. citeturn14view1

The production cost hierarchy should be approximately:

```text
cheap:
    exact index lookup
    role bitset/filter ordering
    cached lexical search
    cached RI relation lookup

moderate:
    bounded graph traversal
    small source-span materialization
    targeted config/doc parsing

expensive:
    model-based candidate adjudication
    broad file reads
    execution / full test run
    coding-agent exploration
```

The active localizer should spend cheap deterministic evidence before expensive model tokens. Sequential retrieval is acceptable when it performs two or three tiny indexed probes to avoid thirty file disclosures; it is not acceptable if each “round” rebuilds repository semantics.

## Immediate production roadmap

The following increments are deliberately larger than trivial vertical slices but stop short of building a speculative probabilistic planner.

| Increment | Owner and concrete capability | Dependencies and evidence | Falsification and evaluation | What it unlocks |
|---|---|---|---|---|
| **Task model and localization kernel** | **Localization.** Add `TaskModel`, anchors, typed obligations, source-span provenance, requirement/applicability/status fields. Initially support explicit/deterministic extraction plus `GENERAL_TASK` fallback. | Existing task inputs. Query decomposition and iterative localization literature support explicit sub-needs, but automatic decomposition remains uncertain. citeturn13search17turn5search0 | On frozen historical cases, can every adjudicated required category be represented without inventing task meaning? Fail if decomposition itself loses full-task recall. | Makes obligation coverage measurable independently of retrieval. |
| **Role-aware repository facts** | **RI.** Index path/basename/extension/root/package facts; structured `pyproject` metadata; recognized pytest config; export/re-export facts where bounded. | Existing RI/provenance. Python packaging and pytest specifications provide authoritative semantics. citeturn16search3turn16search17turn16search23 | Compare role detection against repository truth. No hard exclusion yet. Fail if semantic model routinely misstates configured scopes. | Enables high-precision role priors and structured config/API obligations. |
| **Obligation-scoped retrieval with recall escape lane** | **Retrieval.** Run full-task BM25 plus per-obligation scoped retrieval, exact-anchor lookup, RI queries; return typed evidence rather than fused rank only. | First two increments; existing lexical/structural channels. Hierarchical Agentless provides external precedent. citeturn15search3 | Compare complete gold coverage of candidate unions against current full-task BM25. Must not reduce required recall; should materially reduce per-obligation candidate depth. | Tests central hypothesis without candidate elimination yet. |
| **Evidence ledger and satisfaction rules** | **Localization.** Introduce candidate assignments, slots, `ONE_OF`/`AT_LEAST_ONE`/`COMPONENT_COVER`/conditional semantics, categorical evidence states. | Obligation model + typed evidence. Active-hypothesis/cover literature motivates competition and coverage. citeturn8search11turn14view7 | Measure complete-obligation coverage and selected-set size. Fail if selection cannot beat per-obligation top-\(k\) without losing recall. | First true small obligation-complete selected set. |
| **Safe negative evidence and proof-carrying elimination** | **Localization + RI.** Define elimination whitelist and explicit contradiction records. All heuristic negatives remain demotions. | Evidence ledger; bounded RI semantics. Negative-feedback literature motivates caution rather than binary inference. citeturn17search1turn17search6 | **Zero required-resource false hard eliminations** on development corpus; separately measure soft-demotion effects. Any recurring hard false negative falsifies the associated rule. | Allows candidate competition to reduce waste safely. |
| **Targeted graph/navigation actions** | **Retrieval/Localization.** Convert graph infrastructure into owner/export/reference/dependency-neighborhood and closure operators; retain repo-map/PPR only as optional evidence. | Existing typed graph machinery. Aider, LocAgent, and CodePlan support relational/navigation roles. citeturn14view0turn14view3turn15search0 | Ablate each graph action against lexical+RI baseline. Fail if it adds latency without resolving obligations or reducing opens. | Makes graph investment directly answer unresolved hypotheses. |
| **Sequential resolver and sufficiency certificate** | **Localization.** Add unresolved-obligation loop, bounded follow-up policy, `NOT_APPLICABLE`, `DEFERRED_INHERENT_DISCOVERY`, `ABSTAIN`, and stopping record. | Previous evidence machinery. Active high-recall search provides stopping precedent. citeturn7search0turn14view6 | Measure extra rounds, coverage gain per round, false stopping, and unnecessary continuing. Fail if most tasks simply run every action. | A real pre-coding localization subsystem rather than static retrieval. |
| **Obligation-linked fine-grained Context** | **Context Planning.** Translate resolved assignments into declaration/test/doc/config spans; whole-file representation remains available. | Localization output + provenance/spans. Agentless/SWE-Explore motivate fine-grained localization. citeturn15search3turn15search6 | Token-matched coding-agent experiment: same or higher task success with fewer disclosed tokens and fewer follow-up opens. | Directly realizes low-waste coding Context. |
| **Calibration and learned policies** | **Learning.** Only after prospective traces: learn obligation classification, role priors, evidence weights, candidate discrimination, information-gain policy, and stopping calibration. | Stable schemas and substantial labeled evaluation corpus. Recent selective-retrieval calibration gaps argue against doing this prematurely. citeturn15search4 | Held-out calibration, false-negative rate, coverage-vs-cost curves; learned component must beat deterministic control. | Allows empirically justified automation rather than handcrafted growth. |

The evaluation/adjudication schema should be implemented **alongside the first increment**, not postponed until the seventh. The roadmap row ordering describes functional capability dependencies, not an excuse to delay prospective measurement.

The experimental directory should be explicitly mined before each relevant increment. Based on the supplied history, the highest-value categories to re-inspect are:

**References/Calls/containment/test correspondence** for evidence constructors; **structural candidate generation and graph expansion** for follow-up action implementations; **heterogeneous evidence composition** for provenance and evidence normalization; **lexical RRF/fusion and dense experiments** as candidate-generation baselines/ablations rather than presumed production winners; and **dogfood capture/adjudication** as the seed of the new prospective evaluation harness. These recommendations are based on the user's inventory; without the actual repository I cannot responsibly claim which specific experimental functions are reusable. fileciteturn0file0

The important implementation principle is: **promote semantics, not experiments wholesale.** If historical code already computes a deterministic test correspondence or reference relation that fits RI's invariants, promote the semantic primitive. If it contains a tuning-dependent fusion heuristic, preserve it as a retrieval experiment until the localization evaluation demonstrates value.

## Strongest immediate experiment and final recommendation

The strongest next experiment is **not another PPR/BM25/dense/fusion comparison**. It should directly test whether obligation decomposition plus evidence resolution can convert an already-high-recall candidate inventory into a much smaller complete handoff set.

Use the next naturally occurring `devtools` development task that was specified **before** localization evaluation and that independently requires several of:

```text
implementation behavior
public API/export
tests
documentation
configuration or registration
repository validation
repository-specific rules
```

A suitable shape is the example already motivating the architecture—adding a new public domain concept such as `Obligation`—but the experiment must not manufacture a registry, documentation file, or test layout merely to make the proposed localizer look good. The task should be accepted because it is real work, then frozen. That is essential to prospective validity.

Run four frozen systems:

| Arm | Purpose |
|---|---|
| **Current full-task BM25** | Existing high-recall control. |
| **Current best production retrieval/fusion configuration** | Fair incumbent architecture. |
| **Obligation retrieval only** | Tests decomposition without hypothesis resolution. |
| **Localization prototype** | Obligation retrieval + role priors + evidence ledger + candidate competition + bounded follow-up; no learned tuning. |

The experiment should have two distinct phases.

**Offline localization phase.** Each system must produce its final selected resources/information units without gold labels. Log every candidate query, structural operation, elimination, inspected span, token/byte cost, and stopping reason.

**Controlled coding phase.** Give the same fixed coding-agent configuration the localized Context from each condition. Permit normal subsequent search so that systems are not artificially prevented from solving the task, but log every subsequent search/file open. This turns downstream exploration into a measurement rather than an escape hatch. SWE-agent's results on carefully bounded exploration interfaces and Agent Retrieval Bench's seed-context experiments both support measuring what happens *after* initial context rather than assuming initial retrieval quality automatically implies repair quality. citeturn18view0turn15search4

Before any required-resource outcomes are examined, freeze:

```text
repository snapshot
eligible resource frame
original task prompt
retrieval/index versions
obligation extraction rules
obligation kinds
role-evidence rules
global escape-lane policy
candidate evidence strengths
satisfaction rules
hard-elimination whitelist
maximum follow-up rounds
follow-up action vocabulary
Context disclosure rules
coding-agent model/prompt/tools
validation commands
success criteria
```

Do **not** tune after seeing the adjudication.

After outputs are frozen, independent adjudicators—blind to retrieval provenance and experimental arm—should first derive/confirm the task obligations and then label acceptable required, helpful-only, unnecessary, and alternative satisfaction units. They should additionally answer:

> Could this requirement reasonably have been localized from information available before coding, or did it depend on a later observation?

That single label makes the experiment much more informative than conventional file Recall@K.

**Strong success** means all of the following:

- every mandatory inferable-at-start obligation is covered at handoff;
- zero required candidate is hard-eliminated;
- the localization arm discloses materially less Context and/or requires materially fewer candidate inspections than the incumbent complete-coverage depth;
- the coding agent performs fewer avoidable post-handoff searches/opens;
- validation/task success is no worse than the best control.

Given your observed rank-35/rank-43 baselines, a particularly compelling outcome would be complete coverage with a selected set near the adjudicated required set rather than with tens of ranked candidates. The exact acceptable ratio should be preregistered from engineering cost requirements, not invented after seeing the result. fileciteturn0file0

**Partial success** is any of:

- complete coverage with little waste reduction: obligations help accountability but not discrimination;
- substantial waste reduction while one obligation remains correctly `ABSTAIN`/deferred and is cheaply resolved downstream;
- improved per-obligation depth but no advantage from candidate competition;
- role scoping works but sequential follow-up adds little.

Those outcomes identify which parts of the hypothesis are useful instead of treating the architecture as all-or-nothing.

**Failure** includes:

- an inferable-at-start mandatory obligation is omitted at handoff;
- a hard-elimination rule removes a required candidate;
- obligation decomposition causes lower complete coverage than full-task BM25;
- scoped retrieval repeatedly misses atypically placed resources that the global baseline finds;
- sequential localization uses comparable or more tokens/file reads than simply letting the coding agent explore;
- task/validation success decreases despite apparently better localization.

**Evidence that the architecture itself should change** would be stronger than one failed rule. For example, across a prospective fixed-policy cohort, if most required resources become knowable only after semantic execution, the architecture should shift more responsibility toward dynamic analysis and agent exploration. If obligation decomposition repeatedly fragments strongly interacting information and increases cost, a subsystem/plan-centered representation may be superior. If role priors routinely hide unconventional resources, routing should become weaker. If evidence resolution adds no selection benefit beyond a learned/global reranker while preserving equal recall, then a distinct Localization domain may be unnecessary.

For that reason, the single next task should be the **first member of a preregistered prospective cohort**, ideally with policy frozen for several heterogeneous real tasks before architectural tuning. One task can falsify unsafe behavior—especially false elimination—but cannot establish general superiority.

The final decision matrix is therefore:

| Status | Decision |
|---|---|
| **DECIDE NOW** | Repository localization is not adequately modeled as one global relevance ranking. |
| **DECIDE NOW** | Introduce a first-class `Localization` responsibility between Retrieval and Context Planning. |
| **DECIDE NOW** | Represent task anchors separately from typed `LocalizationObligation`s. |
| **DECIDE NOW** | Preserve full-task lexical retrieval as a high-recall global safety lane. |
| **DECIDE NOW** | Add obligation-specific retrieval and soft repository-role scopes. |
| **DECIDE NOW** | Represent candidate assignments and evidence explicitly with provenance. |
| **DECIDE NOW** | Model competition only inside appropriate obligation slots; model complementarity explicitly. |
| **DECIDE NOW** | Hard elimination requires proof-strength, obligation-scoped evidence. |
| **DECIDE NOW** | Reposition graphs toward relation resolution, dependency closure, navigation, and compact Context. |
| **DECIDE NOW** | Stop using a sufficiency certificate over mandatory obligations, including validation and applicability. |
| **DECIDE NOW** | Carry obligation identity into fine-grained Context Planning. |
| **DECIDE NOW** | Evaluate complete obligation coverage and acquisition/disclosure cost, not fixed Recall@K alone. |
| **TEST FIRST** | Automatic/LLM task decomposition. |
| **TEST FIRST** | Cardinality inference and obligation interaction rules. |
| **TEST FIRST** | Numeric confidence/calibration. |
| **TEST FIRST** | Learned resource-role priors and repository-specific conventions. |
| **TEST FIRST** | Information-gain-based sequential action policies. |
| **TEST FIRST** | PPR/repo-map signals as targeted evidence after an obligation is known. |
| **TEST FIRST** | History/repository-memory features. |
| **DEFER** | Universal exact pre-localization guarantees. |
| **DEFER** | Hard conventional-directory filtering. |
| **DEFER** | An opaque global probabilistic graphical model. |
| **DEFER** | End-to-end learned or RL localization before prospective traces exist. |
| **DEFER** | Replacing deterministic RI semantics with learned approximations. |
| **DEFER** | Treating dense retrieval, graph ranking, or any single retriever as the architecture. |

The strongest practical architecture is therefore **a hybrid, but not a generic “throw every method together” hybrid**. It has a specific division of labor:

> **BM25 and other retrievers generate evidence; deterministic Repository Intelligence establishes what can be known soundly; repository roles route attention without closing the world; Localization converts task requirements into obligation-specific competing and complementary hypotheses; negative evidence is allowed to eliminate only when it carries a bounded proof; graphs answer relational questions rather than pretending centrality equals task completeness; targeted follow-up acquisition is triggered only by unresolved uncertainty; a sufficiency certificate determines when cheap pre-coding localization has reached its frontier; and Context Planning then materializes the smallest obligation-complete information units that the coding agent actually needs.**

That model is more ambitious than improved ranking but substantially less speculative than a general repository-reasoning agent. It also makes the new obligation hypothesis falsifiable: if explicit obligations, evidence resolution, and sequential closure do not reduce complete-coverage cost on prospective tasks, `devtools` can retreat to stronger ranking without having entangled deterministic repository truth, Context Planning, or evaluation with the experiment.

The central architectural change is consequently **not a new retrieval algorithm**. It is changing the question from:

> “Which files are most relevant?”

to:

> **“What must be known for this task, which repository information can establish each requirement, what evidence distinguishes competing explanations, what remains unresolved, what is genuinely unknowable yet, and what is the least costly evidence-backed Context that lets implementation begin safely?”**

That formulation preserves the strongest parts of the existing `devtools` design—snapshot-bound deterministic RI, evidence provenance, high-recall lexical retrieval, structural semantics, and a separate Context-planning layer—while supplying the missing layer that the reported dogfood results most directly expose.