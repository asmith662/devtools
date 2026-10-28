# B-0035: first-request repository discoverability

Maintain the existing neutral repository coding host so a newly invoked coding
model can discover the complete host-authorized source surface without a separate
listing-only inference round. This is the concrete follow-up recorded in canonical
B-0035 after local coding Case 0002. Keep all existing public signatures and Tools.

Preserve the original objective as the first message. Include exactly one
JSON-encoded metadata message, with repository_id, snapshot_id, source_acquired
(false), and resources. Each resource has address, content_identity, byte_size and
editable (a boolean from the host's editable subset). Values correspond to the
current authenticated source scope, including UTF-8 sizes. Include every scoped
resource and no others. This is a transient model-facing projection, not a new
durable schema or source identity. Do not disclose resource content or absolute
host paths. Metadata does not acquire source, satisfy readiness or authorize edits.

Repeated preparation and complete-input continuation must not accumulate copies.
Preparation after admitted source refresh must describe the current snapshot.
Charge the complete metadata and existing Tools/continuation to the existing
Prompt byte bound; refuse over-budget requests rather than silently truncate or
omit resources. Preserve stale-source refusal, native call correlation, actual
source disclosure before edits, host admission, fixed checks, restoration,
candidate/terminal outcomes and all existing limits. No new registry, executor,
provider, file-search engine, generic type or Qwen-specific dependency is needed.

Inspect source with the authorized Tools, then submit grounded exact edits.
Tests, docs, configuration and experiment evidence are read-only. Only existing
Agents coding Python modules are editable. Do not change tests or checks, expand
scope, choose commands, publish, or implement other backlog work. Failed checks
will produce real bounded feedback; you may repair within the frozen limits.
