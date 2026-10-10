# Case 0012 Stage B capture and recovery

Stage A is immutable at 4ff6d3950e6c0be834f136a649c1a127f91fdba3.
This experimental package owns execution/capture and separate Stage B traces.
Parent Stage A artifacts remain byte-identical. No gold or effectiveness is owned here.

Read RECOVERY_PROTOCOL.md first. Attempt 1 under attempts/case-0012-stage-b-1 is
permanently aborted, audit-only and not evaluable. Original bytes, source, inventory,
operation boundary and exposure are sealed. It cannot be resumed or labeled.

The maintainer-authorized attempt 2 starts from operation zero after the hardened
recovery checkpoint is committed and pushed. Each frozen operation may execute at
most once within that attempt. Immutable entered/returned JSON records use exclusive
creation, flush/fsync/close and digest chains. Complete native return fields and
aliases have canonical graph descriptions plus trusted incremental pickle segments.
Raw checkpoint is derived metadata; summary replacement failure does not lose a
return or require a native rerun. Native filesystem atomic writing still owns
summary publication. Direct exclusive creation is a documented experiment boundary
because native writing supplies replacement, not O_EXCL claims. Parent-directory
crash durability remains filesystem-dependent.

CLI:

    uv run python -B -m experiments.codex_dogfood.case_0012.stage_b.execute execute
    uv run python -B -m experiments.codex_dogfood.case_0012.stage_b.execute finalize
    uv run python -B -m experiments.codex_dogfood.case_0012.stage_b.execute verify

Only execute invokes native production operations. Finalize and verify replay
immutable native records and never retrieve/resolve/present. Existing entries block
new execution. A separate immutable completion record distinguishes a full schedule
from a returned prefix. Missing values are never inferred. Canonical publications
accept only matching bytes during interrupted finalization.

Full native B/C task-extraction provenance remains distinct. The frozen behavioral
projection supplies equivalence. A fixture-tested byte-identical streaming identity
adapter avoids materializing repeated native JSON graphs; no treatment source or
semantics change. Complete exact evidence is also in exact_resolutions.json.gz;
lexical.json retains every positive row and complete term contributions. Native
objects are in the authenticated journal, never an adjudicator-supplied pickle.

Packet building consumes only frozen Stage A task/obligation/resource inputs. The
standalone validator has stdlib imports and strict structural allowlists. Packet
publication requires validated capture and independently identical double builds.
No adjudication is performed here. U3 future; R1.7 retained; true R2 BM25F mandatory.
