# Package contracts

Catalog is the public facade. Manifest decoding and cache snapshots retain source
order. Selection combines eligibility with shared version ordering. Presentation
uses the same version semantics. Paths and CLI presentation have no network or
filesystem effects. Parsing accepts the catalog's strict language and rejects
unsupported version forms. Sorting keys are process-local, not persisted schema.

Tests are fixed requirements. Do not change test, configuration or documentation
files to make a candidate pass.
