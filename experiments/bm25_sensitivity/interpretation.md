# Development interpretation and limits

The complete grid and all losing configurations are retained in
`development.json.gz`; `analysis.md` gives absolute values and baseline slices.
Selection was frozen before grid outcomes, using five fully completable cases.
All six cases participate in REQUIRED-reach safety. Case 0008's two own-lane
misses remain misses under every configuration: changing saturation, length
normalization or filename score weight cannot create absent lexical overlap.
This is development evidence, not prospective confirmation or production adoption.

At baseline filename weight and b, increasing k1 reduces median maximum-own
completion from 1.0455x baseline at 0.6 to 0.9585x at 2.4. All five selection
cases improve maximum-own completion at 2.4; prefix union also improves in all
five. The median is slightly nonmonotonic between 1.8 and 2.4, and Case 0009's
global completion worsens from 342 to 352 at 2.4. Thus 1.2 is not an invariant
plateau, but this bounded grid does not establish an optimum beyond its boundary.
Higher k1 increases sensitivity to repeated terms; R1.5 records exact TF,
saturation denominators, field contributions and added/removed overtakers.
DF/IDF, tokenization and query terms remain unchanged.

Length normalization is case-dependent. Disabling it at baseline other settings
worsens the worst maximum-own ratio to 1.2759 and union to 1.1728. Full
normalization has a median union improvement (0.9883) but a worst union regression
(1.0602). These ranks reflect different resource lengths and competing term TF,
not a universal preference for short or long source files. Diagnostics retain
document/average lengths and exact normalization factors for both witnesses and
overtakers. The selected completion arm combines no normalization with strong
filename evidence: its Case 0006 global depth worsens 155 to 212 even though
maximum-own improves 58 to 54. This interaction must not be hidden by its median.

Filename weight 0.25 is useful support but not privileged. Removing it causes a
worst maximum-own ratio of 1.3091 and union ratio of 1.1854. At baseline k1/b,
weights 0.5, 1 and 2 tie baseline median maximum-own and union, with small union
regressions in individual cases. Yet the burden-selected joint configuration
(2.4, 0.5, 1) cuts Case 0005 union 151 to 106 and Case 0006 union 81 to 75.
Filename-only gains and collisions are explicit independent-field contributions,
not BM25F field weights. No query weights are altered.

The robust challenger (2.4, 0.75, 0.25) improves maximum-own and prefix union on
all five complete cases, with modest rather than decisive gains. The burden arm
has larger task-dependent gains and global regressions in Cases 0006/0009. The
completion arm has both improvements and severe global regressions. All three
are retained exactly as selected; none replaces production. Ninety-eight
configurations are Pareto nondominated across every eligible case's four primary
metrics. The full k1-by-b, k1-by-filename and b-by-filename surfaces preserve all
remaining-parameter slices; they do not assign additive causal credit.

Representative diagnostics select the largest REQUIRED rank gain/regression per
case for each one-factor baseline slice and selected arm, with deterministic
obligation/address ties. They retain source spans, query DF/IDF and judged yields,
score reconstruction, field effects, exact overtaker changes and conservative
failure attribution. These are inspectable mechanics; a term's yield is not
authorization to remove/downweight it. R1.7 will address that separate question.

Concrete Case 0005 examples: raising only k1 to 2.4 moves the REQUIRED
Localization facade from 66 to 42 in package-integration, increasing content
score by 2.2573. Its `localization` term has TF 6, DF 45, IDF 2.4284 and document
length 102 versus average 803.1709; no filename contribution explains that gain.
Removing only length normalization moves REQUIRED `docs/architecture.md` from
16 to 5 in semantic-ownership, increasing content score by 20.1438. Neither
observation licenses a new default: other obligations regress. Removing filename
weight moves REQUIRED `retrieval/composition.py` 72 to 70 in snapshot-frame with
zero target-score change, illustrating changes to competitors rather than new
target evidence. In that lane `repository` matches 210 judged cells: six REQUIRED,
three HELPFUL_ONLY and 201 UNNECESSARY (required yield 2.857%, useful 4.286%).
The package lane's `localization` footprint is 45 cells: one REQUIRED, three
HELPFUL_ONLY and 41 UNNECESSARY. Those exact profiles are obligation-relative.

Cases are related tasks in one repository, with different historical gold
schemas and alternative conventions. We verify their exact frozen native
baseline scores/orders rather than substitute current files. Case 0008 remains
supplementary; earlier top-K-only evidence is not silently upgraded into complete
obligation gold. No confirmation/reserve judgments were accessed. BM25+/BM25L
audit is in `VARIANTS.md`: no additional variant prerequisite is justified before
BM25F on audited evidence; their untested questions remain open. R2 is mandatory
after prospective R1.6 and R1.7. Localization continuation is unchanged.
