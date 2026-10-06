# Case 0009 independent blind adjudication

Read `manifest.json`, `resources.json.gz`, this instruction, and
`integrity.json` solely to verify packet integrity. Do not read parent
treatment, results, costs, protocol, implementation, or earlier case outcomes.
Use the obligation-relative methodology in the manifest. Freeze
complete identity-qualified judgments, applicability, required information
units, acceptable alternatives, and inferability before any treatment join.
This packet contains the entire eligible frame; no ranking or treatment
membership. No judgments have been made. A separate independent stage is
required.

Integrity fields distinguish `resources_payload_sha256` (canonical
uncompressed JSON bytes) from `resources_archive_sha256` (exact gzip bytes).
The archive uses deterministic gzip with `mtime=0`; `integrity.json` also seals
the manifest, archive, and this instruction.
