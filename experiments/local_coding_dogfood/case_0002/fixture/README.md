# Releasevault

Catalogs preserve publication order and immutable Artifact identities. Catalog.choose
selects the newest eligible artifact for an exact project and normalized platform.
Preview inclusion is caller policy; disabled/invalid records are not eligible.
Catalog.versions displays accepted version strings in ascending precedence.

Versions use strict SemVer 2 syntax, not Python package-version syntax. Major,
minor and patch compare numerically. Stable versions outrank prereleases at the
same core version. Prerelease identifiers compare left to right: numeric values
numerically, numeric identifiers below nonnumeric identifiers, other identifiers
by ASCII lexical order; a matching shorter sequence precedes a longer one.
Build metadata is ignored for precedence. Equal-precedence records retain input
order, and choose returns the first eligible original object among ties.

Runtime is standard-library only. The catalog's strict syntax, public signatures,
eligibility, interchange and snapshot ownership remain supported contracts.
