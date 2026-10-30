# B-0035 Stage B: initial complete inventory and lifecycle

Implement the remaining host integration in the existing repository/navigation
composition. Stage A's model-authored complete_inventory representation has passed
independent acceptance and is installed as the current candidate, not yet production.
This is a fresh worker Context. No prior model session or source acquisition is
being replayed. Current exact source follows under new snapshot identities.

Required behavior:
- The first RepositoryCodingHost model request contains exactly one complete
  authorized resource inventory, as distinct metadata. Keep the exact objective
  first and present; no inventory-only inference step is necessary.
- Use the accepted representation contract. All resources in the current scope,
  including empty text, must have correct addresses, UTF-8 sizes, content identities
  and editable flags. Repository and snapshot IDs must match current observed scope.
- The complete inventory is not the ranked/incomplete task-candidate view. Both
  must coexist when task navigation is enabled. Existing native Tool definitions,
  calls and correlated feedback must stay valid.
- Repeated prepare calls do not accumulate duplicate inventory. After an admitted
  source change has been installed and verified, the next request's inventory
  describes that current scope, not cached old metadata.
- Inventory does not disclose source text, unauthorized paths or absolute roots;
  it creates no source acquisition or edit-witness credit. Keep exact source
  bindings, currentness, retained native history and custody intact. Inserting
  metadata must not misalign source-message or check-feedback indices.
- Count complete inventory in full serialized ModelRequest capacity, including
  Tools and other Context. If mandatory metadata cannot fit, refuse explicitly
  with a budget/capacity outcome before model entry; projection must not silently
  discard it. Preserve objective, native boundaries and existing compaction.
- Keep initial metadata and installed-source refresh behavior available without
  requiring optional task navigation to be enabled.

Editable files: src/devtools/agents/coding/repository.py and navigation.py only.
repository.py has only 737 bytes of resulting-source headroom. navigation.py has
substantial space and already owns metadata presentation. Choose a coherent
implementation through these existing owners; no new files or size-limit increases.
Do not change tests, lint rules, authorization or the accepted Stage A behavior.
No reference patch is supplied. The public focused tests are authorized for reading;
hidden acceptance is not in scope.

There are at most ten acting requests, six native acquisition actions, four edit
proposals and three applications (two natural check-feedback repairs). Budget
investigation so that actual validation feedback can still be consumed. You may
read necessary missing source, propose a grounded edit, or report a real blocker.
The host does not require a predetermined patch or force an edit. Source metadata
or historical notes are not current exact edit witnesses.
