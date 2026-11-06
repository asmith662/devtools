# Learning engineering fixtures

These are exposed development inputs, not a blind scientific evaluation.
Numeric values, row order, original target meanings and population roles are
retained from B-0096 `tasks.json`, SHA-256
`12469106162e432f881c9551fcd1cd47d462737b0c483752327b651cf4540289`;
the frozen manifest SHA-256 is
`7fa60833378c1bdcbd04c21907f8ccc810483820285d620f2e01fc902ea21a93`.
The donor implementation baseline is
`e069092e9b83c349ddb4efee09a3b1891ea0ad63`. No historical coefficients,
quality tables, costs or scientific ledgers are runtime inputs.

- Iris: Fisher (1936), [UCI Iris](https://archive.ics.uci.edu/dataset/53/iris),
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as recorded by the
  retained rights review. Original classes 1/2 map to binary 0/1. The first
  supplied outer/inner split retains 49 fitting, 17 online and 34 final rows.
  Original row membership is preserved; biological subject independence is
  unknown and is not asserted.
- Auto MPG: Quinlan (1993), [UCI Auto MPG](https://archive.ics.uci.edu/dataset/9/auto+mpg),
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as recorded in the
  authenticated source/metadata acquisition receipts. The retained ZIP SHA-256
  is `5fc1507522b73b8050d3aa45df51eefe1b666ae5f428a5f1347b6483339f1003`.
  Its 398 original records contain six rows with missing numeric fields; the
  fixture records their original zero-based indices and excludes them without
  imputation. Complete raw feature/target tuples match the 392 selected rows as
  a multiset. The 274/59/59 memberships, four original numeric features, unknown
  feature units, and target unit `publisher mpg` remain unchanged. Original
  training group identities include duplicates. Held-group independence is not
  asserted. Source ordering is not treated as chronology.

Changes by this migration are selection and JSON packaging into destination-owned
test resources. No publisher endorsement, new acquisition, current publisher-byte
equality or independent-subject claim is implied. Historical source-role and
failed-preflight evidence remains in the donor; it is not new execution authority.

Destination fixture framing uses LF. Newline normalization preserves the parsed source, memberships, units and acquisition receipts exactly; original donor files are unchanged.
