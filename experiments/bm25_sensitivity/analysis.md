# R1.6 canonical BM25 sensitivity development

Development evidence only; prospective Case 0010 effectiveness remains UNKNOWN. Production parameters unchanged.

Protocol frozen at `0fec2dc79f625f0e17fa8369311b583ac1765489`; 180 configurations x six frozen cases, five selection-eligible and Case 0008 supplementary. Required-reach-safe configurations: 180/180. Pareto configurations: 98.

Selected roles: `{"burden": [2.4, 0.5, 1.0], "completion": [2.4, 0.0, 2.0], "robust": [2.4, 0.75, 0.25]}`. Deduplicated challengers: `[[2.4, 0.0, 2.0], [2.4, 0.5, 1.0], [2.4, 0.75, 0.25]]`.

## Per-case primary metrics

| Config (k1,b,filename) | Case | Global | Max own | Prefix union | Occurrences | Required resources/cells/units |
|---|---:|---:|---:|---:|---:|---|
| (1.2, 0.75, 0.25) | 4 | 325 | 193 | 256 | 602 | 17/17; 25/25; 25/25 |
| (1.2, 0.75, 0.25) | 5 | 342 | 110 | 151 | 295 | 24/24; 27/27; 27/27 |
| (1.2, 0.75, 0.25) | 6 | 155 | 58 | 81 | 205 | 18/18; 28/28; 33/33 |
| (1.2, 0.75, 0.25) | 7 | 346 | 192 | 249 | 661 | 27/27; 55/55; 56/56 |
| (1.2, 0.75, 0.25) | 8 | 361 | None | None | None | 22/22; 48/50; 69/71 |
| (1.2, 0.75, 0.25) | 9 | 342 | 185 | 257 | 454 | 23/23; 37/37; 42/42 |
| (2.4, 0.0, 2.0) | 4 | 332 | 191 | 257 | 676 | 17/17; 25/25; 25/25 |
| (2.4, 0.0, 2.0) | 5 | 342 | 85 | 120 | 344 | 24/24; 27/27; 27/27 |
| (2.4, 0.0, 2.0) | 6 | 212 | 54 | 83 | 274 | 18/18; 28/28; 33/33 |
| (2.4, 0.0, 2.0) | 7 | 292 | 180 | 234 | 701 | 27/27; 55/55; 56/56 |
| (2.4, 0.0, 2.0) | 8 | 325 | None | None | None | 22/22; 48/50; 69/71 |
| (2.4, 0.0, 2.0) | 9 | 363 | 194 | 263 | 533 | 23/23; 37/37; 42/42 |
| (2.4, 0.5, 1.0) | 4 | 326 | 187 | 251 | 599 | 17/17; 25/25; 25/25 |
| (2.4, 0.5, 1.0) | 5 | 341 | 75 | 106 | 241 | 24/24; 27/27; 27/27 |
| (2.4, 0.5, 1.0) | 6 | 172 | 44 | 75 | 189 | 18/18; 28/28; 33/33 |
| (2.4, 0.5, 1.0) | 7 | 285 | 187 | 235 | 636 | 27/27; 55/55; 56/56 |
| (2.4, 0.5, 1.0) | 8 | 333 | None | None | None | 22/22; 48/50; 69/71 |
| (2.4, 0.5, 1.0) | 9 | 357 | 185 | 246 | 460 | 23/23; 37/37; 42/42 |
| (2.4, 0.75, 0.25) | 4 | 322 | 185 | 253 | 578 | 17/17; 25/25; 25/25 |
| (2.4, 0.75, 0.25) | 5 | 339 | 106 | 135 | 243 | 24/24; 27/27; 27/27 |
| (2.4, 0.75, 0.25) | 6 | 144 | 54 | 77 | 186 | 18/18; 28/28; 33/33 |
| (2.4, 0.75, 0.25) | 7 | 338 | 185 | 241 | 628 | 27/27; 55/55; 56/56 |
| (2.4, 0.75, 0.25) | 8 | 354 | None | None | None | 22/22; 48/50; 69/71 |
| (2.4, 0.75, 0.25) | 9 | 352 | 177 | 247 | 436 | 23/23; 37/37; 42/42 |

## Baseline k1 slice

| Parameters | Median max-own ratio | Worst max-own ratio | Median union ratio | Worst union ratio |
|---|---:|---:|---:|---:|
| [0.6, 0.75, 0.25] | 1.0454545454545454 | 1.0702702702702702 | 1.0397350993377483 | 1.0493827160493827 |
| [0.9, 0.75, 0.25] | 1.0172413793103448 | 1.0324324324324323 | 1.01171875 | 1.0246913580246915 |
| [1.2, 0.75, 0.25] | 1.0 | 1.0 | 1.0 | 1.0 |
| [1.5, 0.75, 0.25] | 0.9827586206896551 | 0.9948186528497409 | 0.9844357976653697 | 1.0 |
| [1.8, 0.75, 0.25] | 0.9567567567567568 | 0.9844559585492227 | 0.9727626459143969 | 0.99609375 |
| [2.4, 0.75, 0.25] | 0.9585492227979274 | 0.9636363636363636 | 0.9610894941634242 | 0.98828125 |

## Baseline b slice

| Parameters | Median max-own ratio | Worst max-own ratio | Median union ratio | Worst union ratio |
|---|---:|---:|---:|---:|
| [1.2, 0.0, 0.25] | 1.0486486486486486 | 1.2758620689655173 | 1.0350194552529184 | 1.1728395061728396 |
| [1.2, 0.25, 0.25] | 1.0216216216216216 | 1.1379310344827587 | 1.0132450331125828 | 1.0864197530864197 |
| [1.2, 0.5, 0.25] | 0.9948186528497409 | 1.0862068965517242 | 1.0066225165562914 | 1.0740740740740742 |
| [1.2, 0.75, 0.25] | 1.0 | 1.0 | 1.0 | 1.0 |
| [1.2, 1.0, 0.25] | 1.0162162162162163 | 1.0208333333333333 | 0.9883268482490273 | 1.0602409638554218 |

## Baseline filename_weight slice

| Parameters | Median max-own ratio | Worst max-own ratio | Median union ratio | Worst union ratio |
|---|---:|---:|---:|---:|
| [1.2, 0.75, 0.0] | 1.0 | 1.309090909090909 | 1.01171875 | 1.185430463576159 |
| [1.2, 0.75, 0.1] | 1.0 | 1.209090909090909 | 1.0078125 | 1.119205298013245 |
| [1.2, 0.75, 0.25] | 1.0 | 1.0 | 1.0 | 1.0 |
| [1.2, 0.75, 0.5] | 1.0 | 1.0 | 1.0 | 1.0038910505836576 |
| [1.2, 0.75, 1.0] | 1.0 | 1.0 | 1.0 | 1.0040160642570282 |
| [1.2, 0.75, 2.0] | 1.0 | 1.0 | 1.0 | 1.0080321285140563 |

Full absolute/per-obligation/top-K/partition data, exact normalized ratios and pair surfaces are in development.json.gz. Per-case tradeoffs and losing configurations are retained. Diagnostics retain query/term/source/overtaker mechanics in diagnostics.json.gz.

Limitations: related in-repository development tasks, gold-version differences, one captured repository environment, no held-out outcomes. Development selection is not production adoption. Parameter interactions are not causally allocated. No query weighting, identifier treatment, BM25F or semantic-resolution work.

BM25+/BM25L audit: VARIANTS.md. No R1.6b prerequisite justified on retained evidence; open variant questions remain recorded. R1.7 follows completed prospective R1.6; R2 remains mandatory.
