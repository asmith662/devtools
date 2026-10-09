# U2 exact-hint extraction and deterministic routing

Non-installable experimental composition. Native RI and native grounding retain
repository truth. U2 owns task syntax observations, task-only caller reference,
frozen associations, exact invocation and presentation. It supplies candidate
evidence, never relevance, witness acceptance, obligation satisfaction or readiness.
U2 cannot repair missing or incomplete InformationNeeds.

The [capability inventory](CAPABILITIES.md) records admission and deferred routes.
`models.py`, `extraction.py`, `routing.py`, `presentation.py`, and `serialization.py`
are the single experiment contracts. No production domain depends on them.
The first prospective consumer is [Case 0012](../codex_dogfood/case_0012/README.md),
whose Stage A freezes the policy without invoking its hints against the repository.

## Frozen syntax policy u2-task-syntax-v1

Inspect single-backtick, single-line code spans and unquoted slash paths directly
introduced by `path`, `file` or `resource`. Character offsets are half-open Unicode
code-point spans in the exact task string, excluding surrounding backticks.
Reject code fences/multibacktick runs. Preserve every scanned span's accept/reject
decision. Ordinary prose outside these supported forms is deliberately unscanned;
caller review may identify missed explicit hints without repository lookup.

- Code slash paths must be native canonical repository-relative addresses, with
  conservative ASCII path characters, no traversal/absolute/drive/backslash/space.
  Without explicit path/file/resource wording, require a recognized filename
  suffix (`py`, `md`, `toml`, `yaml`, `yml`, `json`, `txt`); do not guess that
  division-like code such as `x/y` denotes a resource. Fenced or unclosed code
  blocks are excluded conservatively.
- Single filenames such as `pyproject.toml` require explicit file/path/resource wording.
- Dotted Python modules require explicit module/package wording, even inside code.
- Class/type, function and method introductions allow exact code identifiers or
  qualified dotted names. This is tentative syntax typing, not repository identity.
- Bare class/function/method identifiers are retained but unsupported in routing;
  qualification is never recovered from resource contents or prior answers.
- Operational lines marked `Operational:` are excluded, including any handoff path.

Do not extract arbitrary CamelCase, capitals, filenames without introduction,
generic dotted prose, code-formatted English, CLI commands, runtime expressions,
wildcards or generic type expressions. A code-formatted dotted name without a
module/API cue is a recorded rejection. Bare inline identifiers with explicit
API cues are observations, not fabricated globally resolvable locators.

## Routing and presentation

Only frozen RESOURCE_ADDRESS, PYTHON_MODULE, PYTHON_DIRECT_CLASS,
PYTHON_DIRECT_FUNCTION and qualified PYTHON_DIRECT_METHOD requests are admitted.
Module names are split only according to explicit task syntax; imported facade
bindings are never traversed speculatively. Method requests explicitly name
module, class and method. A unique native class is required before containment.

Only RESOLVED outcomes promote a whole native resource occurrence. Every native
grounding account survives, including all ambiguous referents and unsupported or
unresolved reasons. Repeated declarations in one resource still remain ambiguous.
Deduplicate resources, order by hint source span, route identity then native
candidate identity, and append the complete positive lexical lane excluding
already presented resources. Preserve every match object, rank, score and term
contribution. This is reproducible presentation order, not a relevance score.
The original global full-task lexical lane remains separately unchanged.

Tests use controlled native fixtures and synthetic task identities, never Case
0011 gold defaults. No Case 0012 execution entry point or Stage B outputs are
provided in this checkpoint. U3, R1.7, semantic-resolution experiments and BM25F
remain outside its scope.
