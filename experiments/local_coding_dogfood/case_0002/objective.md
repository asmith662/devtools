Repair the release catalog's semantic-version ordering. Users report that a final
release can lose to its release candidate, numeric prerelease components are
ordered incorrectly, and build metadata changes which otherwise equal release
is chosen. The same supported version precedence must be used by catalog
selection and the public ascending version display.

Follow the repository's documented strict SemVer 2 contract: numeric core fields;
stable above prerelease at the same core; numeric prerelease identifiers below
nonnumeric identifiers and compared numerically; other prerelease identifiers
compared lexically; matching shorter identifier sequences before longer ones;
build metadata ignored. First eligible publication wins equal precedence.

Preserve exact project/platform eligibility, default preview exclusion, disabled
and malformed-record handling, immutable record identity, input order, manifest
round trips, strict accepted version syntax and public signatures. Runtime must
remain standard-library only. Do not solve this by editing tests, configuration
or docs, duplicating a second ordering policy, or bypassing the catalog facade.

The host authorizes reads within this small repository and edits to all runtime
Python files under releasevault/. No specific edit target or mandatory source
witness list is prescribed. Discover relevant owners and interacting contracts
using list_repository/search_source, then acquire actual source with read_source.
Search metadata is not source acquisition or edit authority. All exact edit
anchors must be covered by current source actually read. Tests/docs/config are
read-only; a separate frozen held-out oracle is not exposed.

Use native Tools. Search operates over the authorized snapshot's existing
file/symbol/window index and returns metadata. read_source uses zero-based
character offsets with exclusive end; listing/search returns complete lengths.
Read/search and edit batches must be separate. Fixed validation runs after each
admitted edit; consume real failure feedback if repair is needed. You may also
request validate_candidate or inspect_and_validate_change. Neither accepts shell
commands. A model completion narrative is not candidate acceptance.
