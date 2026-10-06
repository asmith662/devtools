# Case 0009 Stage C publication

Stage C was independently adjudicated in a sterile external workspace. The
eight Stage C artifacts in this directory were imported byte-for-byte, and
their exact SHA-256 hashes are authoritative provenance for this publication.

The isolated Stage C test suite passed all 16 tests, and deterministic replay
reproduced the sealed judgments, statistics, and digest exactly. Direct test
execution in the broader repository adjudication directory fails the sterile
workspace whitelist by design because that directory also contains packet
recovery files. Publication validation therefore reconstructs the sterile
workspace outside the repository.

Ruff and formatting findings on the frozen Python artifacts are diagnostic
only. These artifacts remain unchanged to preserve their adjudication bytes.
Any future change requires a new adjudication artifact/version rather than
modification of these files.
