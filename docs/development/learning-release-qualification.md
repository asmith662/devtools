# Learning release qualification

**Current status: combined-main review candidate, protected-qualified; not merged into main.**
See [final main reconciliation](learning-main-reconciliation.md) for the current
combined gate, package and Python 3.14 host interoperability receipts.
The following feature-only result and repair chronology remain historical evidence.
Protected candidate `009cca843ea5bef675e8f7fdf2e9b223e8fcc59e` passes 5,235 tests,
two existing opt-in skips and exactly 100% of 19,308 statements and 5,242 branches.
Ruff, formatting, strict typing, layout, base/extra wheel and source-independence
checks pass. Production and wheel bytes remain those of `c6688cce`.
The chronology below preserves earlier failures and bounded corrections.

Qualification resumes from `623b6b38b8800767e14c57673b150b8634ea4149`.
The original protected denominator is 20,077 statements plus 5,604 branches;
the full terminal result is 4,526 passes, two opt-in skips and 84.55% coverage.
The retained data is inspected read-only. The two subsequently removed unselected
classifier wrappers remain part of that historical denominator, but not current
production source. Module-level diagnostics are retained under
`.local/learning-release/coverage-diagnostic.json` during repair.

The first measured correction passes 153 learning tests. Test-only tracing runs
inside the actual one-process, suspended-start worker after its explicit site
initialization. It imports coverage instrumentation, not application/test source.
Data stays outside scientific publication members in the owned operation root.
Combination verifies a fresh nonce, exact plan and request bytes, interpreter,
measured-source hashes and coverage-data hash. Missing captures after refusal or
forced termination are not invented. The protected denominator/threshold and
scientific worker custody are unchanged. Subset coverage is diagnostic only.

The subsequent measured learning/Commands run passes all 421 selected tests in
115.23 seconds. Its current learning denominator is 6,160 statements/branches;
1,371 remain unexecuted (77.7435%). This subset's overall repository coverage is
25.84% and correctly exits 1 under the unchanged 100% policy. It is not a
replacement protected-gate receipt. Fresh unmeasured verification follows
cohesion-only validator extractions. Strict mypy passes all 732 maintained
modules. The maintained Ruff cleanup remains in progress.

The completed style checkpoint resolves the original 147 diagnostics. Ruff
passes over maintained framework source, learning tests and the qualification
entry point; the seven explicit call-contract exceptions below are the only new
argument-count exceptions. All changed maintained Python paths are formatted,
strict mypy passes 734 modules, and the post-refactor learning/Commands run
passes 450 tests in 61.33 seconds with `inputs_unchanged: true`
(`learning-release-style-16.json`). The protected coverage gate is still pending.

The private `_Investigation` class holds only this bounded agent's existing
per-invocation state and Tool callbacks. Public admission and result APIs,
ModelInteraction/ToolRunner use, grants, consumed slots, original wire fields,
ACK order and protected final sequencing remain unchanged. It adds no reusable
runtime, workflow engine, registry, Context bag or persistence schema.

Recorder and reader checks, independent family arithmetic, native fitting,
publication members and atomic visibility now have responsibility-focused
helpers. The deferred batching API's private range/callback parameters are
removed from the only remaining full-population prediction path; all original
math, distance ordering, tolerance and operation/storage ceilings remain.
Malformed UUID/state or publication JSON types now use explicit TypeError at
three typed boundaries, retaining refusal and error evidence. Parent prediction
checking is extracted from the qualifier's failure-retention handler; it still
compares actual label-free results with independently inspected publication.

Two 421-test targeted runs finish successfully (55.79/55.77 seconds), but their
in-process receipt marks input drift. Read-only comparison finds identical
source/index/HEAD inputs; a bounded reproduction identifies scikit-learn import
initialization of `KMP_DUPLICATE_LIB_OK` and `KMP_INIT_AT_FORK`. These are test
environment observations, not accepted stable-input receipts. Subsequent targeted
invocations initialize that dependency before authenticating inputs. The official
protected runner uses a separate pytest process. No environment-fingerprint rule
is removed or relaxed.

## Dependency closure review

The source mapping retains every original donor identity, plus a symbol-level
`release_scope_review`. Deferred generic metric/bundle/requirement machinery,
heterogeneous raw-table preparation, recipe catalog generation/interactions and
regression batching have no selected first-capability consumer. Their removal
does not remove a needed refusal or alter the supported native methods. The
original reference validator is extracted unchanged beside `EvidenceReference`;
only the population-role enum is needed from raw observations. SQUARE transforms,
F1/MAE typed values, exact grants, source/role binding, immutable fitted state,
publication and independent inspection remain maintained and measured.

The unused Gaussian classifier switches are removed from the private shared
training inspector; selected kNN feature/category/row checks remain. Common
classifier native observations, fitted-state shape and scientific ACK validators
are extracted without changing validation order. An invalid regression target or
specification is now refused with its intended TypeError before accessing its
version. The negative tests exercise genuine retained Mean/Ridge/kNN states;
no new Iris/MPG investigation was performed.

New publication controls include missing/mismatched journals, immutable pointer
integrity, inconsistent membership, hardlinks, primary/secondary recording
failures and failed visibility publication. New SQLite controls exercise real
writer contention, atomic terminal rollback, duplicate/conflicting ACKs,
stage/progress order, corrupt stored projections, source-bound read-only
snapshots and exact child/event membership. Their authored failures are
engineering controls, not original scientific measurements.

## Narrow exception review

The following two imported exception boundaries require catching arbitrary
`Exception` from caller-owned collaborators. Enumerating built-in exceptions
would weaken the established scientific contract. Only rule BLE001 at these
specific handlers is excepted; no global exemption is introduced.

| Source boundary | Reason | Existing qualification |
| --- | --- | --- |
| `evidence/context.py`, `_emit`, observer handler (original line 223) | An optional observer failure must become a scientific diagnostic without changing computation. Arbitrary user callbacks have no closed exception set. | Managed standardization observer-failure and publication observer-failure tests; 153-test measured pass. |
| `evidence/context.py`, `__exit__`, secondary recorder handler (original line 331) | A recorder failure while reporting an existing primary failure adds an explicit incomplete-recording note, preserving the original error. | Publication primary/secondary recording-failure tests in the same pass. |

The required-recorder handler still raises on missing acknowledgment. These
exceptions do not authorize swallowing computation failures, accepting incomplete
evidence or retrying effects.

The following argument-count exceptions are limited to existing concrete call
contracts. Their independent provenance and recorder/observer/parent controls
remain explicit. Combining them into a new general configuration or execution
object solely for a five-argument style limit would obscure those distinctions
and change the demonstrated call contracts. No complexity, branch, type or
security check is excepted. Original line locations below identify the review
input; later helper extraction and formatting can move them.

| Source and symbol | Exact rule | Reason and existing qualification |
| --- | --- | --- |
| `agents/learning/process.py:171`, `investigate` | PLR0913 | Five independently admitted model/task/worker/budget/root inputs plus mandatory explicit profile. Real scripted native Tool and parent-consumption tests pass. |
| `learning/evidence/publication.py:123`, `_validate_publication_request` | PLR0913 | Seven independent version-one manifest intent fields must be cross-checked before observed artifacts exist. Publication corruption and membership tests pass. Private callers will name the metadata arguments explicitly. |
| `learning/integrations/local/publication.py:592`, `publish_artifacts` | PLR0913 | Retains the existing public writer/validator, exact identities, dependencies, optional observations and ownership controls. All 57 filesystem/publication controls pass. |
| `learning/integrations/local/publication.py:680`, `_publish` | PLR0913 | Same explicit validated intent plus the active scientific occurrence; keeps unobserved intent distinct from the final immutable manifest. Private metadata arguments become keyword-only. |
| `learning/integrations/sklearn/regression/__init__.py:244`, `fit_regression` | PLR0913 | Separate specification, training population, preparation and required recorder plus optional parent/observer. Actual Mean/Ridge/kNN fits and retained-state checks pass. |
| `learning/representation/standardization.py:278`, `transform` | PLR0913 | Distinct source/population/role/representation identities and optional scientific observation controls. Exact arithmetic, held-role and observer controls pass. |
| `learning/representation/standardization.py:403`, `fit_feature_standardization` | PLR0913 | Same explicit provenance, fitting-only role and recording controls at the preparation boundary. The 31 independent standardization controls pass. |

These exceptions preserve the demonstrated APIs. They do not except new helpers,
accept unsupported source types or remove the 100% coverage requirement. The
post-refactor source requires fresh focused regression and coverage receipts.

## Additional scientific refusal controls

The next test checkpoint passes 272 newly maintained controls in 8.42 seconds,
with `inputs_unchanged: true` (`learning-release-plans-29.json`). Ruff remains
clear and strict mypy checks 746 modules. These tests add actual authored logistic
and margin fits, retained-state corruption, category/coordinate validation,
source/role/unit mismatches, packet/state/work bounds, finite host reservations,
reference-profile decisions and typed numerical overflow outcomes.

Real SQLite commits followed by missing, foreign or stale returned ACKs establish
that a completed effect does not imply caller acceptance. Interrupted contexts
retain their original interruption and incomplete/failed observations. Closed
wire contracts reject invented causes, malformed types and extra fields.
Event and scalar-measurement modules reach 100% in the combined diagnostic data;
this is not a protected-gate pass. The authenticated `coverage-04` combination
checks unchanged production inputs and retains its seed and combined data hashes.
Overall learning diagnostic coverage at that point is 81.5387%; later controls
still require measured combination.

Runtime refusal tests explicitly simulate Python 3.14 and incompatible package
metadata, thread reports and wrong file kinds. A separate positive test observes
actual installed native libraries under one thread without fitting. The larger
future storage profile and elapsed clock are simulated negative controls, with
no grant or numerical effects; the reviewed 9/10/8/3/8/8 study limits are unchanged.
These controls do not claim actual Python 3.14 numerical qualification.

Retained failed receipts include an assertion using a valid capacity version,
an incorrect authored population-ID expectation and a recovery invocation which
omitted the required exclusive temporary root. Corrections change the tests or
the invocation environment, preserving the valid production refusals and all
independent-host guards. A fresh owned external root resolves the permission
failure; no shared temporary tree is removed or reconfigured.

## Runtime scope

The initial numerical profile intentionally remains Windows CPython 3.12.13 and
the four pinned learning-extra distributions. The package contract explicitly
refuses other numerical runtimes until qualified. Ordinary Devtools's broader
Python support does not establish learning portability; Python 3.14.3 is not
silently added to numerical acceptance. Installed base checks remain separate.

## Combined scientific and contained-command checkpoint

The `coverage-09` measured group passes all 722 selected learning and contained
Commands tests in 194.48 seconds, with authenticated unchanged inputs. Learning
coverage is 97.2602739726%: 172 of 6,278 statements/branches remain missed. The
whole repository subset correctly exits 1 at 31.08% under the unchanged 100%
policy; no new full protected release pass is claimed. Strict mypy checks 762
modules and maintained Ruff is clear. Production bytes remain those of
`638a6a48ccee9cc3af8d85aa5168f1ee5921128e`.

A second genuine control-worker path now collects authenticated coverage using
the direct interpreter, `-S`, explicit site initialization, empty `PYTHONPATH`,
one native thread and the existing one-process Job. Successful workers must
retain their capture; refused or killed workers cannot invent one. CPython does
not trace audit callbacks while dispatching audit events. A separate test captures
the actual callback registration and invokes its exact guards directly, covering
network/child-process/foreign-write refusals without installing a global pytest
audit hook. Real contained execution and source guards remain separately tested.

Additional controls cover retained-state arithmetic and codec corruption, source
roles/units, scientific event and publication contracts, actual SQLite rollback,
read-only snapshots, ACK and lifecycle errors, independent preparation and metric
replay, and host packet/response bounds. Lazy fixture acquisition keeps genuine
authored Mean/Ridge/kNN/logistic/margin witnesses inside active measurement.
Explicitly authored backend reports test refusal and diagnostic custody; they are
not native measurements. Alternate-platform lock reports are unit simulations,
not POSIX runtime qualification. No original Iris/MPG study is rerun or rewritten.

Retained failed receipts include a schema-driver injection which initially missed
leading DDL whitespace, a missing simulated `os.path`, a non-existent role enum,
a mismatched population version and an incorrect expected corruption exception.
Their corrections change test controls, not scientific or isolation semantics.
The complete selected group now passes. Native capture and focused combinations
retain nonce/request/interpreter/source/data identities; each append verifies
that its seed's production hashes still match. Raw receipts remain task-owned
under `.local/learning-release/`.

## Scientific release-candidate coverage

Fresh `coverage-11` data, without reused arcs, passes 776 learning/Commands
tests in 215.93 seconds. All 6,279 learning statement/branch terms and the
Windows Job implementation are covered at 100%. Every worker capture is bound
to its exact operation, packet, interpreter and current source. The repository
subset still correctly exits 1 at 31.27%: this is readiness for the full gate,
not a protected-gate pass. The preceding fresh run passed 774 tests and left
only the staged-manifest refusal; an actual validator adding an unexpected file
after the initial membership check now establishes that refusal.

Production refinements keep feature-only checks separate from deferred target
checks; narrow the private ledger stage helper to the three stage payloads
(`_record` handles admission separately before `_advance`); and group the
quantitative fit-required dispatch alongside binary prediction dispatch. No
SQL schema, source rule, ACK, grant, method parameter or tolerance changes.
A narrow internal cast records the already-established payload partition rather
than adding a silently ignored non-stage branch. Independent corruption tests
still reject malformed past history even after a later writer ACK.

A fresh base-import diagnostic caught eager optional-adapter imports introduced
during style cleanup. Explicit per-method lazy loading restores the original
optional-dependency contract. A real contained `-S` interpreter rejects all
NumPy/SciPy/sklearn/threadpoolctl imports while importing coding, the learning
agent and independent inspector successfully. The actual native investigator
and parent-consumption cases still pass (34-case focused receipt
`learning-release-optional-44.json`). Earlier installed-wheel results are not
reused to qualify this changed source; the final wheel is rebuilt below.

Maintained static scope is `src tests apps scripts`, with the established
retained `tests/experiments` role omitted explicitly on the command line. Ruff
reports zero diagnostics, all 922 maintained Python files are formatted, strict
mypy passes 767 modules, and linked-worktree layout/diff checks pass. No global
exclusion, rule or coverage configuration is changed. The retained Ruff
COM812/formatter advisory and ignored inherited VIRTUAL_ENV warning are not
suppressed. Read-only Git inspection sees concurrent main at
`9f404adccea4a19765bb886c94fe592c555a39ac`; no merge is performed.

## First full release-candidate gate and bounded correction

The exact committed `c6688cce` protected run completed all 5,236 tests: 5,234
passed and the original two opt-in tests skipped. Pytest took 5,060.56 seconds;
managed wall time was 5,080.405603 seconds. Inputs remained unchanged and neither
output stream was truncated. The run failed honestly at 99.9877800407332%:
19,305/19,308 statements and all 5,242 branches were covered. Only
`resources/commands/execution.py:190-192`, the suspended-process admission
exception cleanup, was missed. This is a statement/exception-handler gap, not
uncollected numerical execution or a remaining scientific branch deficit.

The new focused case creates a genuine suspended direct-interpreter child and
explicitly injects refusal before Job admission/resume. It verifies the original
OSError is preserved, the exact created PID is the refused PID, the actual child
is terminated/reaped with a nonzero return code, and its entry marker never
appears. It signals only this invocation's own child. All four real containment
controls pass. This is an injected admission refusal against a real process,
not a claim that Windows naturally failed admission.

An authenticated diagnostic combination of the retained failed full data and
this four-test group reaches exactly 100%: 19,308 statements and 5,242 branches,
zero missed terms. Production hashes match the failed full run; its source and
wheel are unchanged. The combination is not a replacement protected gate. A
fresh full run on the committed correction remains mandatory. Original failed
full receipts are retained under `learning-qualification/release-repair-c6688cce`.

## Narrow external-boundary style exceptions

In addition to the seven reviewed argument-count declarations, two BLE001
exceptions retain the original scientific callback/error semantics: evidence
`context.py:214` catches arbitrary optional observer errors, records a warning
and preserves computation; `context.py:343` catches secondary recording errors
while retaining the primary failure and incomplete-recording note. Genuine
SQLite ACK faults and interruption controls qualify these paths. BaseException
interruptions are not silently swallowed as ordinary observer errors.

Commands `execution.py:188-189` has two scoped SLF001 exceptions, plus the
existing stub-gap `attr-defined` annotation at line 188. CPython 3.12's asyncio
Process has no public original Windows-handle accessor. This resource boundary
reads the owned transport's Popen and its original handle, then independently
checks that handle's PID before Job assignment and resume. The profile records
the exact CPython executable/ABI; real suspended-start, descendant refusal,
timeout, cancellation and now admission-refusal cleanup are qualified. This is
not a portable private-API claim. No blanket rule exemption is introduced.

## Passing final protected gate

The exact committed `009cca84` command `uv run python
scripts/validate_development.py` completes with exit 0: 5,235 passed and the two
existing opt-in skips in 4,946.82 pytest seconds. Managed wall time is
4,964.833935 seconds. Every one of 19,308 statements and 5,242 branches is
covered; there are zero missed lines or branches. Inputs remain unchanged and
output is not truncated. Coverage-data SHA-256 is
`8cd13658e3726e33ec6ddbe6fe1a471c4120c9be22758ada8d20231c32003502`.
Raw terminal/input receipts and per-module counts are retained under
`learning-qualification/release-009cca84/`. This is a fresh protected pass,
separate from the diagnostic data combination.

No product source changes follow `c6688cce`; `009cca84` adds the missing
suspended-admission cleanup test and retained failure documentation. Final
report-only publication preserves the qualified executable tree and wheel
member hashes. Original test selection, branch instrumentation, threshold and
assertions remain unchanged.

## Installed package and retained scientific correspondence

Hatchling 1.33.0 builds the 699,901-byte wheel from committed product source,
SHA-256 `c0e437e0123c82aee256beab02bdfc32ae536bf063084560dc15e4d0e520874f`.
All 409 product members match physical source bytes, with only normal dist-info
metadata outside `devtools/`. No tests, apps, scripts, archives, cache or donor
source is packaged. Requires-Dist keeps all four numerical libraries behind the
learning extra. The initial network-sandbox build fails; the owned warm-cache
offline build and complete extra/base resolver installations succeed (25 and
18 resolved packages). PowerShell reports redirected native stderr as errors in
those retained logs; independent installed controls and both `uv pip check`
invocations have genuine zero exits. The cache-inside-source advisory is
addressed by exact wheel-membership inspection, not suppression.

Six standalone scripted ModelInteraction/Tool control cases pass in 49.382999
seconds, including genuine classification, regression, margin, null, unsupported
and tied-boundary paths. They preserve STOP/CONTINUE/ABSTAIN, exact host grants,
inspection before subsequent decisions, protected final selection and actual
parent predictions. Invalid role requests cause zero native effects. Base coding
read/edit/check/archive/restore passes in 1.653998 seconds with no numerical
distributions. Every loaded Devtools module originates in the selected installed
site; 13 active read/import denial probes per environment pass with no unexpected
forbidden access. Selected interpreter, package/ABI and actual native DLL/thread
identities are retained in package runtime/scientific records.

Independent inspection from the installed base wheel takes 1.416947 seconds,
reproduces all seven original accepted v2 publications and predictions without
fitting, and leaves all 80 evidence files unchanged. A separate 1.032736-second
inspection refuses all seven original v1 publications and leaves their 80 files
unchanged. These inspections explicitly read only the admitted original result
data; they import no archived producing program or numerical library. No new
Iris/MPG study, fitted-state reuse for training or confirmation disclosure occurs.
Final source outcomes and exact publication identities are retained in
`package/retained-source-outcomes.json` and `package/independent-inspection.json`.

## Costs, limits and main review

The two complete release gates cost 5,080.405603 and 4,964.833935 managed seconds
(10,045.239538 total). The fresh focused learning/Job group costs 215.93 seconds;
subset/diagnostic costs are separate and never stand in for a full gate. Original
accepted two-task execution remains 21.994368 outer seconds, six native fits,
seven procedure states, six preparations, one SQUARE materialization and seven
numerical invocations/actions, within the unchanged 9/10/8/3/8/8 envelope. Nine
scripted model calls include the separate terminal choices. Original rejected
and accepted executions are not combined into one supposedly under-budget run.
No paid/live inference, shared model service or source download is used. Total
CPU, peak RSS, energy and all-session aggregate cost remain unmeasured.

Read-only committed-tree review sees `origin/main` at
`825bc23b98e366e97d56e3146a1d752285f383bd`, six commits after the shared base
`26c07ef1b26436dd10dc50c752cd63a6619c7bba` on main's side. Only the documentation
map overlaps, and its frozen three-way text preview is clean. Main's provider
policy v4 enrollment and bounded/validated llama.cpp HTTP responses introduce no
change to the native ModelInteraction/Tool contracts used here. No merge, rebase,
main push, canonical source write or shared service mutation occurs. The combined
main/feature tree is not qualified by this feature-only pass: deliberate main
reconciliation, policy/docs review, affected checks and a fresh combined protected
gate remain prerequisites to human integration. The live local-model hypothesis
milestone is identified, not implemented.

Final separate static receipts record zero Ruff diagnostics over maintained
`src tests apps scripts` (retained `tests/experiments` omitted by role), 922
formatted files, strict mypy across 767 modules, layout and diff passes, and
strict UTF-8 decoding of all 69 learning/consumer/changed-Commands Python sources.
They are retained under the final receipt directory's `static/`. No source
exclusion, threshold, warning filter or security-relevant assertion changes.

Release-repair checkpoints after `623b6b38` are:

- `f84e160b20ad29fbf3b09a39bd09ffa6f9580509`: authenticated process coverage, closure review and initial scientific refusals.
- `638a6a48ccee9cc3af8d85aa5168f1ee5921128e`: maintained lint/cohesion and preserved scientific boundaries.
- `3b3623f301146948112482ca71c55b5816bf2638`: source, state, authority and ACK controls.
- `ef2460339cd1b6fd92643c790f45c5e307968f73`: retained arithmetic, independent-reader and second-worker coverage controls.
- `c6688cce532164d11a2125ae7d8baee248a849c3`: complete scientific/Job coverage and restored optional base imports; final product/wheel source.
- `009cca843ea5bef675e8f7fdf2e9b223e8fcc59e`: genuine suspended-admission cleanup refusal test, preserved 99.99% failure, and final fresh passing protected candidate.

All checkpoints are preserved and published on the feature branch. The final
report/receipt commit adds no executable changes and is identified by the branch
ref and ignored Codex completion handoff. Main remains unmodified and unmerged
by this assignment. Original donor/history byte custody remains intact.
