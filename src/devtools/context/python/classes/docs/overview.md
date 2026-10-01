# Python class and direct method Repository Intelligence

`devtools.context.python.classes` analyzes one caller-selected resource from a
retained `RepositorySnapshot`, or a caller-ordered distinct resource selection.
It parses the observed UTF-8 content with an identified Python 3.12 Abstract
Syntax Tree (AST) grammar and establishes only these positive declaration forms:

```text
observed resource
  ├── direct Module.body FunctionDef / AsyncFunctionDef   [existing function RI]
  └── direct Module.body ClassDef
        ├── direct ClassDef.body FunctionDef
        └── direct ClassDef.body AsyncFunctionDef
```

The class/method analysis does not republish existing module-body function
facts. It reuses their `PythonSourceRange`, `PythonSourceOccurrence`,
`PythonModuleResourceDependency`, and syntactic function-kind values, while
keeping the established direct module-body function API and identity unchanged.
Class and method declarations have separate derivation, subject, and knowledge
identities. This Python-specific package owns their facts and the bounded
direct-base derivation described below.

## Identity, provenance, and containment

The class subject identity depends on parser/derivation definition, snapshot,
the exact observed resource/content dependency, and class ordinal among direct
module-body classes. A method subject also depends on its containing class
subject and ordinal among that class's direct methods. Names are retained for
display and exact syntax knowledge, never used alone as subject identity. These
are structural repository subjects, not runtime Python `__qualname__` values.

Every class and method retains an exact source occurrence with one-based lines
and zero-based UTF-8 byte columns. The per-resource derivation retains its
repository and snapshot identities, content-bearing observed resource, parser
version, and bounded traversal semantics. A class retains the exact occurrence
and source text of each direct base expression as **syntax**. A separate
derivation assesses possible repository class targets without changing the
original declaration.
AST declaration spans begin at `class`/`def`/`async def`, excluding preceding
decorator lines. Decorators do not classify descriptor or runtime behavior.

```text
method occurrence resource ──→ observed module resource
method direct lexical parent ──→ class declaration
class occurrence resource  ──→ observed module resource
class direct lexical parent ──→ Module.body scope (bounded analysis claim)
```

`PythonMethodDeclarationKnowledge.containing_class` is the one canonical direct
lexical-parent link. Both directions navigate it; no reverse fact is derived.
`build_python_class_method_containment_view(snapshot, aggregate=...)` validates
native analyses against the retained snapshot without reparsing or file reads.
It exposes `module_body_classes_in(address)`, `direct_methods_of(class)`,
`containing_class_of(method)`, and `occurrence_resource_of(class_or_method)`.
An analyzed resource or class can return an empty tuple. An unselected resource
or declaration raises an error rather than implying absence.

Successful coverage counts supported classes/methods, separately counted
module-body functions handled by existing function RI, and encountered class
or function syntax outside this analysis's positive scope. Excluded occurrences
retain exact source locations. Syntax failure publishes no successful coverage.
Local classes, nested classes, nested functions, methods of excluded classes,
and indirect declarations under control-flow statements are not positive facts.
Absence in this bounded result says nothing about runtime classes or methods.

Repository Intelligence records this structure. Retrieval may later decide
whether it is relevant to an InformationNeed. Context Planning may later choose
a class or method representation for disclosure. Neither decision is made here.
The current qualified Reference/direct Call analyzer still resolves only its
existing imported-function forms. Future method References/Calls need separate
qualified attribute and receiver/type resolution. The current resource-level
Personalized PageRank graph does not consume these new facts. A future graph
view may project class, method, base, and Reference relationships prospectively.

## Bounded direct-base resolution

```text
Child class -> exact direct base-expression syntax and UTF-8 span
               | bounded static module/import/member resolution
               v
          one assessment per expression
               | RESOLVED only
               v
          supported Base class declaration
```

`derive_python_direct_bases(snapshot, aggregate=..., module_universe=...)`
assesses every retained base expression. `PythonDirectBaseAssessment` is the
canonical result. Only `RESOLVED` establishes a direct repository class-to-class
relation; every other outcome preserves the syntax and reason. Identity binds
the child declaration, base ordinal/span/text, module universe, outcome, source
and target derivations, and supporting import facts where present. Both endpoints
are structural class subjects, never names alone. Source and target analyses
retain exact observed resource/content and snapshot dependencies. Derivation
uses retained snapshot state and never reopens files.

`PythonDirectBaseAnalysis.direct_bases_of(child)` preserves base syntax order;
`direct_subclasses_of(base)` projects the *same* positive assessments backward
in selected resource/class/base order. There is no independent reverse fact.

Supported positive routes are:

- A simple name bound by exactly one earlier undecorated direct module-body
  class in the same resource, with no competing observed binding.
- A simple name from a direct `from module import Class [as Alias]`, where
  production import resolution identifies one observed module and that module
  has exactly one direct undecorated class binding for the imported member.
- An attribute chain `module.Class` or `alias.Class` matching a direct
  `import module [as alias]` and one supported direct class in that resolved
  module. `import pkg.module` supports `pkg.module.Class`.

The bounded static binding check inspects direct module-body bindings before
the child class. Competing/rebound names, conditional bindings, wildcard
imports, decorated target classes, and ambiguous module or class targets
prevent a positive result. For imported members, the target module's whole
direct binding surface is checked. Relative imports use existing module
interpretation facts. Facade re-exports and arbitrary attribute evaluation
are outside this contract. `obj.Base`, calls, subscriptions such as `Base[T]`,
builtins, and unobserved/external classes remain assessed without fabricated
repository class subjects. One base may resolve while another does not.

This is a bounded **static repository relation**, not complete Python runtime
inheritance. It does not evaluate decorators, metaclasses, dynamic globals,
module execution, `__getattr__`, C3 Method Resolution Order (MRO), inherited
methods, overrides, or transitive subclass closure. Absence of a positive
relation does not mean a class has no runtime base. Repository Intelligence
owns the relationship; Retrieval decides whether to project it into a graph,
and Context Planning decides what to disclose. The current Personalized
PageRank (PPR) graph is unchanged.
