# Prospective Localization Case 0005

**FROZEN BEFORE RETRIEVAL AND ROUTING — Stage A only.**

This case uses a real upcoming production evidence-to-witness association task.
The exact complete task/global query, purpose, anchors, nine mandatory
obligations and their named criteria, nine ordered lexical queries and nine
explicit role preferences are retained in [treatment.json](treatment.json) and
[pre_retrieval.json](pre_retrieval.json). Initial witness alternatives are empty.
The package-integration obligation has a bounded conditional applicability
condition; Stage C determines applicability independently. No resource has been
judged required, helpful or unnecessary here.

The new hypothesis is whether caller-selected positive role support reduces the
candidate review surface relative to the SAME native obligation-specific BM25
lanes. Global native lexical control, own-obligation native baseline and routed
own-obligation presentation are three distinct surfaces. There is no numeric
success threshold and no general superiority claim from one case.

## Caller treatment

The first five semantic/provenance/integration obligations select `PYTHON_CODE`.
Package integration selects `PACKAGE_SURFACE OR PACKAGE_MEMBER`; tests select
`TEST`; documentation selects `DOCUMENTATION`. Validation deliberately selects
no preferred roles: no supported validation role covers the command,
documentation and configuration contract. Its lane remains native/escape-only.
These decisions precede static role derivation and come from task meaning, not
repository filenames or observed role assignments. Every exact query and
preference rationale is retained in the machine-readable treatment.

The production router has exactly preferred-positive-support and escape tiers.
ANY selected role qualifies; additional roles/supports add no priority. Native
order survives inside each tier, every candidate survives, native rank survives,
and routed position is one-based presentation position. The global lane is
unchanged and unrouted. No negative evidence, confidence, satisfaction,
elimination, score modification or lane fusion is introduced.

## Snapshot and static inputs

The starting commit is `1bd2c7a5676ba78edd46879f2c06625c13c12d17`.
The logical RepositoryId continues the existing dogfood repository identity.
Only eligible tracked blobs from this commit are exported: Python, Markdown,
TOML and YAML under source, docs and ordinary tests, plus root README, AGENTS,
pyproject and the protected development validation script. Historical ledger,
experimental/confirmation tests, caches, other experiments/scripts, binary and
untracked/local files are excluded. Prior experimental capture exceptions are
omitted because they are not governing this production association task.
Selection is frozen before outcomes and defines bounded corpus completeness.

[freeze.py](freeze.py) uses canonical managed Git commands, path resolution,
bounded filesystem reads/atomic text writes, discovery, observation, corpus,
representation, lexical analysis/statistics and static inverted-index primitives.
It never imports an acquisition/routing execution function. Exported temporary
paths are incidental locators retained on discovery, not semantic repository
identity. Native pickle/gzip serialization is an explicit experimental binary
boundary: production filesystem reading/writing has no binary codec, so bounded
archive reads and exclusive creation are used without inventing a framework
codec. Pickle is trusted only
after frozen digest verification, never as untrusted interchange.

[inputs.pkl.gz](inputs.pkl.gz) retains the complete native acquisition REQUEST
(not a result), exact resource content and index, native role-evidence view and
caller `ObligationRolePreference` values. Role evidence is production-derived,
not hand assigned. Its recipe uses every eligible Python resource below explicit
`src` and `tests` module roots, native immediate package membership, native
mirrored paths, root pyproject declarations and selectors, a module universe
from both roots, and explicit root working-directory/pytest frames. All analyses
and scope/unsupported/absence semantics are retained on the role view.

The manifest binds repository/snapshot/corpus/frame and resource content
identities, committed blob hashes, production implementation hashes, derivation
identity/version, Python version and archive digest. The static role view is
reproduced during validation; no routing executes. Implementation binding covers
every eligible production Python module including transitive dependencies.
BM25 defaults are `k1=1.2`, `b=0.75`, filename weight `0.25`, native
content-plus-filename behavior, positive matches only, with a bound equal to
eligible resource count. Native ties retain lexical corpus address order.
Discovery bounds are 10,000 resources/20,000 traversal entries; observation is
bounded at 1 MiB per resource.

[integrity.json](integrity.json) seals normalized LF text bytes of treatment,
manifest, support/tests/protocol and exact binary archive bytes. It is itself
sealed by the Stage A Git commit. All artifacts refuse silent replacement.
The freeze can be checked with:

```text
uv run python experiments/codex_dogfood/case_0005/freeze.py --validate
uv run pytest --no-cov experiments/codex_dogfood/case_0005/test_freeze.py
```

## Frozen measurements

For each independently judged REQUIRED information unit and unique resource,
record global native rank, own native rank, own routed position, tier and reach.
For every conjunctive acceptable alternative, completion is the maximum member
position if ALL members are reachable; otherwise no finite completion exists.
ANY complete alternative suffices. Report all alternatives, then best finite
completion per obligation independently on all three surfaces. Raw required
judgments remain separate from alternative completion.

Report global complete required-resource depth, obligation-wise maximum best
native completion and obligation-wise maximum best routed completion separately;
the latter are not merged rankings. Report applicable mandatory acquisition
coverage on each surface, not production satisfaction.

For each obligation, compare candidate counts in native/routed prefixes through
their respective best complete acceptable alternative. Report summed prefix
occurrences and unique resource unions separately. An obligation with no finite
completion makes the whole-case review surface incomplete; do not silently drop
it. Keep obligation-relative units and unique resources distinct.

Report preferred/escape counts, required/helpful/unnecessary witnesses by tier,
and unresolved judgments. A required escape witness survives acquisition but
exposes a role-routing limitation. Compare worse/better/equal positions, global
safety reach, deep escape, native worse than global and empty preference
invariance descriptively without post-hoc thresholds. Retain candidate union,
duplicate/overlap/zero-lane diagnostics and cross-obligation reach. Helpful-only
diagnostics never enter mandatory completion. Native lexical contributions may
be inspected AFTER primary measurements, without cross-lane score comparison,
tuning or causal claims. Exact measurement definitions are in the manifest.

## Blind adjudication and firewall

Stage C must be a fresh independent session with a verified treatment-free
packet containing only task, purpose, anchors, obligations, criteria/provenance
and eligible resource identities/content/governing architecture. Hide lexical
queries, preferred-role mappings, the role view/assignments, routing results,
tiers, ranks, positions, scores, Retrieval provenance, retrieved flags and
runtime. Treatment mappings themselves are blind, not just results.

Freeze applicability, narrow REQUIRED/helpful/unnecessary/unresolved judgments,
minimal acceptable alternatives, complete identity coverage, task-start
inferability, inherent-discovery prerequisites and obvious interpretation gaps.
Opened/modified files and future implementation behavior are not gold. Do not
silently repair the obligation frame during adjudication.

Case 0004 supplies only the aggregate motivation that lexical decomposition
improved discrimination but left a substantial review surface. No gold
identities, witness memberships, resource-level rankings or hypothetical routing
outcomes were used. No Case 0005 acquisition, routing, adjudication or task
implementation has occurred. Confirmation remains sealed.

Task/frame/query/preference/settings/role recipe/implementation/metrics changes
must preserve this treatment and introduce an explicitly distinct version.

## Exact next stage: Stage B (not executed here)

1. Verify Stage A committed artifact hashes from `integrity.json`; run the static
   validator before loading native pickle. Verify the manifest implementation
   hashes against starting-commit Git blobs and current normalized source bytes.
   Refuse any drift or existing Stage B outputs. Use the frozen Python/environment
   and production implementation; do not rebuild from a newer checkout.
2. Load ONLY the retained native archive into `native`.
3. Execute once:

```python
from devtools.context.localization.lexical import acquire_localization_lexical_evidence
from devtools.context.localization.routing import route_localization_lexical_evidence

acquisition = acquire_localization_lexical_evidence(native["request"])
routed = route_localization_lexical_evidence(
    acquisition, native["role_evidence"], native["preferences"]
)
```

4. Retain both native objects together with unchanged input/protocol digests and
   runtime in a new exclusive `capture.pkl.gz`; serialize exact global/native
   lane ranks, native lexical contributions and separate routed positions/tiers
   into new `retrieval.json` and `routing.json`. Verify candidate preservation,
   tier ordering and unchanged global identity, then commit Stage B. Do not tune
   treatment or adjudicate during capture. Stage B support can be authored then;
   no executable acquisition command is part of this Stage A helper.
5. Build a treatment-free blind packet, freeze independent Stage C judgments,
   then join only in Stage D. No effectiveness result exists at Stage A.
