# Case 0009 blind packet integrity recovery

The independent Stage C attempt stopped before decompressing the resource
archive. It accessed the packet instruction and manifest, then compared the
manifest's `resources_sha256` value with compressed archive bytes.

The old manifest SHA-256 was
`4542a655fd7be22363a06ac877eee3ec71868d268b0de7663b1e7b5dae1c1de2`. Its
`resources_sha256` value was
`29e09439ad7812b96f7a10ccb40e34548e842a56ab9e90306fcac8a299349c99`. The
committed archive SHA-256 was
`c23e0908d664e9c81149dec54a81aeeff3ef25fa9624c342cfac9bda44be5b37`.

The mismatch came from comparing different byte layers. `resources_sha256`
sealed the canonical uncompressed JSON payload, not the gzip file. The old
archive was deterministic already: its gzip modification time is zero, its
payload digest equals the manifest value, and a rebuild from hash-verified
Stage A inputs reproduces the old archive byte for byte. No archive content or
frozen task semantics were wrong.

Recovery adds an isolated adjudication packet builder with explicit
`resources_payload_sha256` and `resources_archive_sha256` fields, resource,
obligation, and cell counts, and the deterministic builder identity. It keeps
the archive bytes unchanged and updates the manifest, packet instruction, and
integrity seal. The new archive digest remains
`c23e0908d664e9c81149dec54a81aeeff3ef25fa9624c342cfac9bda44be5b37`; the
canonical payload digest remains
`29e09439ad7812b96f7a10ccb40e34548e842a56ab9e90306fcac8a299349c99`.
The repaired manifest SHA-256 is
`a68bf46bec7e7875e9321986864bbe3cb12cec80ecc167992d770610f48ae932`; the
repaired packet integrity record SHA-256 is
`edce2e60cea2e5dee279ad60aa9d97b9ac3fd95514167f242a8f87d78e8e9849`.

The packet was reconstructed from the hash-pinned `inputs.pkl.gz` Stage A
snapshot and checked against Stage A task and obligation objects. All 531
resource identities, content identities, and content strings match; all nine
obligations and 4,779 expected cells match. No treatment result, ranking,
score, cost, comparison, confirmation, or reserve outcome was accessed. No
judgments were created, and no treatment was rerun.
