# Case 0005 Stage B.5 blind packet

**BLIND PACKET PREPARED — NOT ADJUDICATED.**

The Stage A checkpoint and its committed input/integrity bindings were verified.
This packet was projected from the retained Stage A native request and snapshot
contents. Its allowlist contains the task text and purpose, task provenance,
shared anchors, frozen obligation predicates/criteria/status/applicability and
empty pre-Retrieval witness alternatives, repository/snapshot/frame identity,
and eligible resource address/content identities and exact text.

| Blind artifact | SHA-256 |
| --- | --- |
| [blind_manifest.json](adjudication/blind_manifest.json) | `c3d6455d09bcd53beec75c7d325489096f3b4a44c8b2aa6c4266233d93ca1177` |
| [blind_resources.json.gz](adjudication/blind_resources.json.gz) | `01c786e7c74ae72ffd93e6d861fb080fb613d941788d0c6ea987c2dcb67889b7` |

The archive contains exactly 515 resources bound to RepositoryId
`d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8`, RepositorySnapshotId
`0705f0e5ef729d28ed044f36b929a2c9436ad38c821c154bd11430f5fb58989a`, and
eligible-frame identity `12fe8c45e9b90ad9142a2700e6a4c258e222ceb64d719df4e7cb06bc8e2b4d7b`.
All addresses, content identities and UTF-8 contents match the retained frozen
snapshot in its original order. The package-integration applicability condition
is preserved without a determination.

The manifest and resource records use strict allowlisted schemas. They contain
no lexical treatment, caller role preferences, derived role assignments, or
Stage B output. The builder did not open or deserialize Stage B artifacts. It
does not run retrieval, routing or any resource judgment.

Builder: [build_adjudication_packet.py](build_adjudication_packet.py). Check the
saved packet and deterministically reconstruct it from verified Stage A inputs
with:

```text
uv run python experiments/codex_dogfood/case_0005/build_adjudication_packet.py --verify
```

The initial build succeeded, reconstruction/schema/frame checks passed, and a
repeated build was refused before writing. The two packet artifact hashes
remained unchanged. Scoped tests cover schema allowlisting, source boundaries,
conditionality and overwrite protection.

Next, a fresh independent Stage C session must use only the blind manifest and
resource archive. It must adjudicate applicability, required/helpful/unnecessary
information, acceptable witness alternatives, task-start inferability and
interpretation gaps. It must not inspect treatment or result artifacts. No
adjudication has occurred; confirmation remains sealed.
