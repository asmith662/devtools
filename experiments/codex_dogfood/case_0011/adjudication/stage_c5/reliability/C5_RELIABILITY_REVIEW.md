# Case 0011 C.5 reliability review

SEVERE_ARCHITECTURE_RELEVANT_DISAGREEMENT. Neither adjudication alone is safe for Stage D. Reconciliation is required. Both fail the strict every-required-unit direct rule, but the exact failed units and causes are disputed. U1 effectiveness is UNKNOWN; no final U1 outcome is selected.

This is a fully inspectable comparison of frozen claims, not reconciliation. The independent granularity and collective audits are diagnostics awaiting confirmation. No treatment or confirmation data was accessed.

## Executive comparison

| Measure | Primary C.5 | Independent C.5-R | Agreement / implication |
| --- | --- | --- | --- |
| Pair labels | 13 direct; 59 partial; 504 noncoverage | 21 direct; 41 partial; 514 noncoverage | 544/576 = 94.4444%; 32 disagreements |
| Direct mappings | 13 | 21 | 12 shared / 22 union; Jaccard 54.5455% |
| Strict covered units | 13/32 | 20/32 | 21/32 statuses agree; 11 disagree |
| Need classifications | 9 necessary; 9 partial-only | 13 necessary; 1 redundant; 4 partial-only | 11/18 agree; 7 disagree |
| Direct-complete alternatives | 0/12 | 6/12 | 6/12 direct-completeness agree |
| Secondary granularity-aware coverage | not independently audited | 26/32 | 8/12 alternatives diagnostic complete; never replaces strict U1 |

## Exact pair-label confusion matrix

Rows = primary; columns = independent. Cohen's kappa is descriptive only; these fixed semantic judgments are not a random sample.

### Pair labels

| Primary / independent | DIRECTLY_COVERS | PARTIALLY_COVERS | DOES_NOT_COVER | AMBIGUOUS |
| --- | --- | --- | --- | --- |
| DIRECTLY_COVERS | 12 | 1 | 0 | 0 |
| PARTIALLY_COVERS | 9 | 34 | 16 | 0 |
| DOES_NOT_COVER | 0 | 6 | 498 | 0 |
| AMBIGUOUS | 0 | 0 | 0 | 0 |

Exact agreement 544/576 (94.444444%); disagreements 32; descriptive kappa 0.7367909978865596.

### Unit statuses

| Primary / independent | COVERED | PARTIAL_ONLY | UNCOVERED | AMBIGUOUS_ONLY |
| --- | --- | --- | --- | --- |
| COVERED | 12 | 1 | 0 | 0 |
| PARTIAL_ONLY | 8 | 9 | 0 | 0 |
| UNCOVERED | 0 | 2 | 0 | 0 |
| AMBIGUOUS_ONLY | 0 | 0 | 0 | 0 |

Exact agreement 21/32 (65.625000%); disagreements 11; descriptive kappa 0.37142857142857144.

### Need classifications

| Primary / independent | NECESSARY | USEFUL_REDUNDANT | PARTIAL_ONLY | UNNECESSARY | MISFORMULATED | AMBIGUOUS |
| --- | --- | --- | --- | --- | --- | --- |
| NECESSARY | 8 | 0 | 1 | 0 | 0 | 0 |
| USEFUL_REDUNDANT | 0 | 0 | 0 | 0 | 0 | 0 |
| PARTIAL_ONLY | 5 | 1 | 3 | 0 | 0 | 0 |
| UNNECESSARY | 0 | 0 | 0 | 0 | 0 | 0 |
| MISFORMULATED | 0 | 0 | 0 | 0 | 0 | 0 |
| AMBIGUOUS | 0 | 0 | 0 | 0 | 0 | 0 |

Exact agreement 11/18 (61.111111%); disagreements 7; descriptive kappa 0.2631578947368422.

### Alternative strict completeness

| Primary / independent | COMPLETE | INCOMPLETE |
| --- | --- | --- |
| COMPLETE | 0 | 0 |
| INCOMPLETE | 6 | 6 |

Exact agreement 6/12 (50.000000%); disagreements 6; descriptive kappa 0.0.

## Direct and partial mapping reliability

| Label | Primary | Independent | Intersection | Union | Jaccard | Primary retained | Independent retained |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DIRECTLY_COVERS | 13 | 21 | 12 | 22 | 0.5454545454545454 | 0.9230769230769231 | 0.5714285714285714 |
| PARTIALLY_COVERS | 59 | 41 | 34 | 66 | 0.5151515151515151 | 0.576271186440678 | 0.8292682926829268 |
| DOES_NOT_COVER | 504 | 514 | 498 | 520 | 0.9576923076923077 | 0.9880952380952381 | 0.9688715953307393 |
| AMBIGUOUS | 0 | 0 | 0 | 0 | None | None | None |

DIRECT: primary-only = 1; review-only = 9. PARTIAL: primary-only = 25; review-only = 7. Partial→direct = 9; partial→noncoverage = 16; noncoverage→direct = 0; noncoverage→partial = 6; direct→partial = 1. The independent reviewer became more direct through nine promotions and more decisive through sixteen removals of weak partial relationships. No agreed noncoverage pool should hide direct instability.

### Direct reliability by need

Unit-obligation and alternative totals overlap when membership overlaps; need-obligation is reported separately.

| Owner | Primary | Independent | Shared | Union | Jaccard | Primary retained | Independent retained |
| --- | --- | --- | --- | --- | --- | --- | --- |
| case-0011-context-utf8-ceiling/ownership/assembly-owner | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| case-0011-context-utf8-ceiling/ownership/dependencies | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| case-0011-context-utf8-ceiling/bytes/rendered-boundary | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| case-0011-context-utf8-ceiling/bytes/encoding | 0 | 0 | 0 | 0 | None | None | None |
| case-0011-context-utf8-ceiling/ceiling/validation | 2 | 2 | 2 | 2 | 1.0 | 1.0 | 1.0 |
| case-0011-context-utf8-ceiling/ceiling/rejection | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| case-0011-context-utf8-ceiling/request/copy | 1 | 2 | 1 | 2 | 0.5 | 1.0 | 0.5 |
| case-0011-context-utf8-ceiling/request/prompt | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| case-0011-context-utf8-ceiling/frame/binding | 2 | 3 | 2 | 3 | 0.6666666666666666 | 1.0 | 0.6666666666666666 |
| case-0011-context-utf8-ceiling/frame/items | 1 | 0 | 0 | 1 | 0.0 | 0.0 | None |
| case-0011-context-utf8-ceiling/exports/public-boundary | 0 | 2 | 0 | 2 | 0.0 | None | 0.0 |
| case-0011-context-utf8-ceiling/tests/text-boundaries | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| case-0011-context-utf8-ceiling/tests/frame-rejection | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| case-0011-context-utf8-ceiling/tests/request-preservation | 2 | 2 | 2 | 2 | 1.0 | 1.0 | 1.0 |
| case-0011-context-utf8-ceiling/documentation/architecture | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| case-0011-context-utf8-ceiling/documentation/package | 0 | 0 | 0 | 0 | None | None | None |
| case-0011-context-utf8-ceiling/validation/protected-entry | 0 | 0 | 0 | 0 | None | None | None |
| case-0011-context-utf8-ceiling/validation/configuration | 2 | 2 | 2 | 2 | 1.0 | 1.0 | 1.0 |

### Direct reliability by unit

Unit-obligation and alternative totals overlap when membership overlaps; need-obligation is reported separately.

| Owner | Primary | Independent | Shared | Union | Jaccard | Primary retained | Independent retained |
| --- | --- | --- | --- | --- | --- | --- | --- |
| unit-0057f1c75647a0b3e2d678bb704888665ee7ffbfeec0e56f27c501027a03c027 | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2 | 0 | 0 | 0 | 0 | None | None | None |
| unit-1466ea6b2b7b8cdc077c41ad15c6baf8087b6e7a230723f83b9911815a09a10c | 0 | 0 | 0 | 0 | None | None | None |
| unit-183296beacda118e38a058b6d2588e582fd74639627706768ea3eb9396cc4580 | 0 | 0 | 0 | 0 | None | None | None |
| unit-1979aa6106ebf66bce887d463ebbcb9d0745566f1875c359373e6e5afb72a394 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-1bb673f66452efaf4d344988ed48b3011927a477ec8a2c9b4f5e77b2fd81aa42 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-1bb99811c2a45a9ce6d5dc32206e23d64f9fffa2d10fa642ca5f4ea6ce518c69 | 0 | 0 | 0 | 0 | None | None | None |
| unit-21e7319918686d72a7f9e79f31bc68ed4922858fa7bfa299d351ea43ef3b0b87 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-33a494497198cadf88145cc45dc05ca55e09e6405588ce5cdd12c4f2c65e8371 | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| unit-4b3c320635122396ffe052357de8b5f96f074e35017c0331a650de95844eaccd | 0 | 0 | 0 | 0 | None | None | None |
| unit-50dcfb5fd4a867c57ed46736f5e8858a763c0a2f62aecc6e809ad822716dbb30 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-5991a5afbd7d664372fc5b2357e8fbcacfa5d73d5560dcd97f853aa279e36b1c | 0 | 0 | 0 | 0 | None | None | None |
| unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7 | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| unit-5e58e7852d6acb8027c97bf0d6ccc3deede219f1c229e52225d0b31b7ed29af6 | 0 | 0 | 0 | 0 | None | None | None |
| unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7 | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605 | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c | 0 | 0 | 0 | 0 | None | None | None |
| unit-7ec311946c51700e892b24d725de3a5b89904e240505c5e5e79e4d1736e56bb9 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-87f78f68bcbaca8cbda3d9fc4b8f1daee88e66a1ed350ec6441d5861cbb400fc | 0 | 0 | 0 | 0 | None | None | None |
| unit-8ad51eaf88aadfa2dd3d6fff7c23390b4bec7f204bc74d276ba759e0e6b3aa14 | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| unit-a090f45af360240ad7ce7630ffd09098a6a1b7887839d5266196a6f645880702 | 1 | 2 | 1 | 2 | 0.5 | 1.0 | 0.5 |
| unit-a2c6080b9a63cdbb8cb2057c41ba2c618614bc672246ada53ce1f470cf4d7fca | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-a3e3b3430e6bfb7351af007e1cfff42c912e499682a4d3e332c4ac6b7e043580 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-ab36d70f1deecd237ce4358ffb3258f71b19a55589c1815c3a99545581e8cbdf | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2 | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| unit-d553be405368fb0607f76e8e953d24dcecf462b0308474311add157d55b57fc7 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-e3c24d637a4dca9783a7b6b86dbe1abcda4ad0117b8933cc798af53004501e08 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-eac315eb2a9f6a5634e094a5d4ef2960559030b62385b832a57f0f8d893b72de | 0 | 0 | 0 | 0 | None | None | None |
| unit-f0a8cdef8232323f591cb10fdee77345e0352146b082c5bea0fb239ac9602965 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-f2f60cee7a81549ef3634c65a08ec026019e35505a0b7457ff348af70571ace3 | 1 | 0 | 0 | 1 | 0.0 | 0.0 | None |
| unit-f7ba939e852e8f0f8e89d99664675a3cd8f8c1d48ac0acdc0bc9b4ebb7d22c50 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| unit-fddd6c59fb1d485b6e4a6a749f66062c76ddd58df987a692ae75827e2f9b8329 | 0 | 0 | 0 | 0 | None | None | None |

### Direct reliability by obligation

Unit-obligation and alternative totals overlap when membership overlaps; need-obligation is reported separately.

| Owner | Primary | Independent | Shared | Union | Jaccard | Primary retained | Independent retained |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ownership | 0 | 2 | 0 | 2 | 0.0 | None | 0.0 |
| bytes | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| ceiling | 3 | 4 | 3 | 4 | 0.75 | 1.0 | 0.75 |
| request | 1 | 3 | 1 | 3 | 0.3333333333333333 | 1.0 | 0.3333333333333333 |
| frame | 3 | 3 | 2 | 4 | 0.5 | 0.6666666666666666 | 0.6666666666666666 |
| exports | 0 | 2 | 0 | 2 | 0.0 | None | 0.0 |
| tests | 4 | 4 | 4 | 4 | 1.0 | 1.0 | 1.0 |
| documentation | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| validation | 2 | 2 | 2 | 2 | 1.0 | 1.0 | 1.0 |

### Direct reliability by need_obligation

Unit-obligation and alternative totals overlap when membership overlaps; need-obligation is reported separately.

| Owner | Primary | Independent | Shared | Union | Jaccard | Primary retained | Independent retained |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ownership | 0 | 2 | 0 | 2 | 0.0 | None | 0.0 |
| bytes | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| ceiling | 2 | 3 | 2 | 3 | 0.6666666666666666 | 1.0 | 0.6666666666666666 |
| request | 1 | 3 | 1 | 3 | 0.3333333333333333 | 1.0 | 0.3333333333333333 |
| frame | 3 | 3 | 2 | 4 | 0.5 | 0.6666666666666666 | 0.6666666666666666 |
| exports | 0 | 2 | 0 | 2 | 0.0 | None | 0.0 |
| tests | 4 | 4 | 4 | 4 | 1.0 | 1.0 | 1.0 |
| documentation | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| validation | 2 | 2 | 2 | 2 | 1.0 | 1.0 | 1.0 |

### Direct reliability by alternative

Unit-obligation and alternative totals overlap when membership overlaps; need-obligation is reported separately.

| Owner | Primary | Independent | Shared | Union | Jaccard | Primary retained | Independent retained |
| --- | --- | --- | --- | --- | --- | --- | --- |
| alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1 | 1 | 1 | 1 | 1 | 1.0 | 1.0 | 1.0 |
| alternative-5823cd216c59ce3b109a4657e44e0050b4fbc485a58d5da984d3e7da3ebed7c5 | 1 | 2 | 1 | 2 | 0.5 | 1.0 | 0.5 |
| alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc | 1 | 2 | 1 | 2 | 0.5 | 1.0 | 0.5 |
| alternative-d1599c2ce73551e58d4eeb482661a9e62312f3766c7a77dd9bb95a8a7c1a3638 | 1 | 2 | 1 | 2 | 0.5 | 1.0 | 0.5 |
| alternative-15d7c3ffc813581557be5c4e0732549f4686d0fe3999af4783abbbbb7c9db6eb | 0 | 1 | 0 | 1 | 0.0 | None | 0.0 |
| alternative-fa2c4638c8d6ffb4c5cab8f91fcc0e562d8256c72a831797541622b2bf8531c6 | 0 | 2 | 0 | 2 | 0.0 | None | 0.0 |
| alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063 | 3 | 3 | 2 | 4 | 0.5 | 0.6666666666666666 | 0.6666666666666666 |
| alternative-f8cc13a78a696e2cf395ea58f422d4eb26c24a17ba9eacbb7f3645755872877c | 0 | 2 | 0 | 2 | 0.0 | None | 0.0 |
| alternative-cf445deec2b6d543ca84fbd68a8dc1c97d0e7ce2f0ae19fc3b3e04f45231545f | 0 | 2 | 0 | 2 | 0.0 | None | 0.0 |
| alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1 | 1 | 3 | 1 | 3 | 0.3333333333333333 | 1.0 | 0.3333333333333333 |
| alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed | 4 | 4 | 4 | 4 | 1.0 | 1.0 | 1.0 |
| alternative-112ca6b6a76691a25e2cf528a62311634ca38c88086c4464abdc1d3588733158 | 2 | 2 | 2 | 2 | 1.0 | 1.0 | 1.0 |

## Every pair-label disagreement, including every disputed direct mapping

### case-0011-context-utf8-ceiling/ownership/assembly-owner × unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605

Need: Which common Context Planning contract owns copied ModelRequest assembly?

Unit: The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

Owning need obligation: ownership; unit obligations: ['ceiling']; alternatives: ['alternative-5823cd216c59ce3b109a4657e44e0050b4fbc485a58d5da984d3e7da3ebed7c5', 'alternative-d1599c2ce73551e58d4eeb482661a9e62312f3766c7a77dd9bb95a8a7c1a3638', 'alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc'].

**primary: DOES_NOT_COVER**

Fact sought: Which common Context Planning contract owns copied ModelRequest assembly?

Fact established: The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

The need asks for ownership of copied ModelRequest assembly. This unit establishes the complete existing assembly signature, rendered input, unlimited entire-text behavior and final copy step. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

**review: PARTIALLY_COVERS**

Fact sought: the common contract owning copied assembly and its caller-directed planning role

Fact established: The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

The need seeks the common contract owning copied assembly and its caller-directed planning role. It covers identification of the common assembly entry point as the assembly contract; it does not require keyword-only rendered input, absent limit argument, full context handling and final replace timing. Therefore its complete answer does not establish the whole unit.

covered_part: identification of the common assembly entry point as the assembly contract

missing_part: keyword-only rendered input, absent limit argument, full context handling and final replace timing

### case-0011-context-utf8-ceiling/ownership/assembly-owner × unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2

Need: Which common Context Planning contract owns copied ModelRequest assembly?

Unit: Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection.

Owning need obligation: ownership; unit obligations: ['ownership']; alternatives: ['alternative-cf445deec2b6d543ca84fbd68a8dc1c97d0e7ce2f0ae19fc3b3e04f45231545f', 'alternative-f8cc13a78a696e2cf395ea58f422d4eb26c24a17ba9eacbb7f3645755872877c'].

**primary: PARTIALLY_COVERS**

Fact sought: Which common Context Planning contract owns copied ModelRequest assembly?

Fact established: Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection.

The need seeks common ownership of copied request assembly. The complete unit additionally requires ownership of ordered caller-directed plans, faithful realization before rendering, and independence from automatic selection and Retrieval; answering this need need not establish that remainder.

covered_part: common ownership of copied request assembly

missing_part: ownership of ordered caller-directed plans, faithful realization before rendering, and independence from automatic selection and Retrieval

**review: DIRECTLY_COVERS**

Fact sought: the common contract owning copied assembly and its caller-directed planning role

Fact established: Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection.

Identifying the common assembly owner as a contract requires its pipeline responsibility: caller-directed ordered plans, faithful realization, rendering and copied assembly, with automatic selection/Retrieval outside that ownership. This is a single architectural responsibility statement.

### case-0011-context-utf8-ceiling/ownership/dependencies × unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7

Need: What dependency constraints separate common Context Planning from language-specific adapters and Retrieval?

Unit: Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency.

Owning need obligation: ownership; unit obligations: ['ownership']; alternatives: ['alternative-cf445deec2b6d543ca84fbd68a8dc1c97d0e7ce2f0ae19fc3b3e04f45231545f', 'alternative-f8cc13a78a696e2cf395ea58f422d4eb26c24a17ba9eacbb7f3645755872877c'].

**primary: PARTIALLY_COVERS**

Fact sought: What dependency constraints separate common Context Planning from language-specific adapters and Retrieval?

Fact established: Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency.

The need seeks absence of language-adapter and Retrieval dependencies. The complete unit additionally requires the actual ModelRequest/Prompt imports and type-only ContextDisclosure dependency; answering this need need not establish that remainder.

covered_part: absence of language-adapter and Retrieval dependencies

missing_part: the actual ModelRequest/Prompt imports and type-only ContextDisclosure dependency

**review: DIRECTLY_COVERS**

Fact sought: allowed dependency directions and the separation of common planning from adapters and Retrieval

Fact established: Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency.

A complete dependency-boundary answer identifies the allowed ModelRequest/Prompt imports, the type-only ContextDisclosure dependency and absence of adapter/Retrieval dependencies in rendering and assembly. This establishes the complete import-boundary unit.

### case-0011-context-utf8-ceiling/ceiling/rejection × unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7

Need: What assembly contract permits rejection before modifying a request, without truncating or omitting items?

Unit: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

Owning need obligation: ceiling; unit obligations: ['request']; alternatives: ['alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1'].

**primary: DOES_NOT_COVER**

Fact sought: What assembly contract permits rejection before modifying a request, without truncating or omitting items?

Fact established: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

The need asks for the assembly rejection seam before request modification without item loss. This unit establishes the frozen ModelRequest dataclass and complete declared fields. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

**review: PARTIALLY_COVERS**

Fact sought: the assembly input and construction boundary at which full-context rejection can precede request copying

Fact established: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

The need seeks the assembly input and construction boundary at which full-context rejection can precede request copying. It covers immutability supporting rejection without modifying the caller request; it does not require the complete prompt/settings/conversation/provider_settings/tools field inventory. Therefore its complete answer does not establish the whole unit.

covered_part: immutability supporting rejection without modifying the caller request

missing_part: the complete prompt/settings/conversation/provider_settings/tools field inventory

### case-0011-context-utf8-ceiling/ceiling/rejection × unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605

Need: What assembly contract permits rejection before modifying a request, without truncating or omitting items?

Unit: The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

Owning need obligation: ceiling; unit obligations: ['ceiling']; alternatives: ['alternative-5823cd216c59ce3b109a4657e44e0050b4fbc485a58d5da984d3e7da3ebed7c5', 'alternative-d1599c2ce73551e58d4eeb482661a9e62312f3766c7a77dd9bb95a8a7c1a3638', 'alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc'].

**primary: PARTIALLY_COVERS**

Fact sought: What assembly contract permits rejection before modifying a request, without truncating or omitting items?

Fact established: The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

The need seeks whole-context assembly and a copied request created only at the final replacement, providing a rejection seam. The complete unit additionally requires the keyword-only signature, rendered input type and absence of an existing limit argument; answering this need need not establish that remainder.

covered_part: whole-context assembly and a copied request created only at the final replacement, providing a rejection seam

missing_part: the keyword-only signature, rendered input type and absence of an existing limit argument

**review: DIRECTLY_COVERS**

Fact sought: the assembly input and construction boundary at which full-context rejection can precede request copying

Fact established: The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

Locating the safe rejection boundary requires describing the current keyword-only rendered-disclosure input, lack of a ceiling, whole-context handling and final replace construction. Together these establish where rejection precedes the copied request without dropping items.

### case-0011-context-utf8-ceiling/request/copy × unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7

Need: How does copied ModelRequest assembly preserve all fields other than the appended Context?

Unit: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

Owning need obligation: request; unit obligations: ['request']; alternatives: ['alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1'].

**primary: PARTIALLY_COVERS**

Fact sought: How does copied ModelRequest assembly preserve all fields other than the appended Context?

Fact established: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

The need seeks retention of the request fields other than the changed prompt. The complete unit additionally requires the complete declared field inventory and the frozen-dataclass declaration; answering this need need not establish that remainder.

covered_part: retention of the request fields other than the changed prompt

missing_part: the complete declared field inventory and the frozen-dataclass declaration

**review: DIRECTLY_COVERS**

Fact sought: the immutable request field inventory and copying mechanism preserving unrelated fields

Fact established: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

An account of preserving every request field needs the full immutable request shape: prompt, settings, conversation, provider_settings and tools. That inventory and frozen-dataclass status establish the whole unit.

### case-0011-context-utf8-ceiling/request/prompt × unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7

Need: How are the original task text and Prompt role preserved when Context is appended?

Unit: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

Owning need obligation: request; unit obligations: ['request']; alternatives: ['alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1'].

**primary: DOES_NOT_COVER**

Fact sought: How are the original task text and Prompt role preserved when Context is appended?

Fact established: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

The need asks for original task text and Prompt role preservation. This unit establishes the frozen ModelRequest dataclass and complete declared fields. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

**review: PARTIALLY_COVERS**

Fact sought: preservation of the original task text and Prompt role during appending

Fact established: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

The need seeks preservation of the original task text and Prompt role during appending. It covers the prompt-bearing request whose Prompt is preserved; it does not require frozen-dataclass status and the complete inventory of other fields. Therefore its complete answer does not establish the whole unit.

covered_part: the prompt-bearing request whose Prompt is preserved

missing_part: frozen-dataclass status and the complete inventory of other fields

### case-0011-context-utf8-ceiling/request/prompt × unit-a090f45af360240ad7ce7630ffd09098a6a1b7887839d5266196a6f645880702

Need: How are the original task text and Prompt role preserved when Context is appended?

Unit: Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role.

Owning need obligation: request; unit obligations: ['request']; alternatives: ['alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1'].

**primary: PARTIALLY_COVERS**

Fact sought: How are the original task text and Prompt role preserved when Context is appended?

Fact established: Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role.

The need seeks Prompt role preservation and original task embedded in new prompt content. The complete unit additionally requires the dataclasses.replace operation replacing only Prompt and thereby retaining every other field; answering this need need not establish that remainder.

covered_part: Prompt role preservation and original task embedded in new prompt content

missing_part: the dataclasses.replace operation replacing only Prompt and thereby retaining every other field

**review: DIRECTLY_COVERS**

Fact sought: preservation of the original task text and Prompt role during appending

Fact established: Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role.

Explaining how appending preserves the Prompt role requires the new Prompt construction with the original role and its installation in a copied request. The single replace/Prompt operation establishes this whole unit.

### case-0011-context-utf8-ceiling/frame/binding × unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2

Need: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Unit: Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values.

Owning need obligation: frame; unit obligations: ['frame']; alternatives: ['alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063'].

**primary: DOES_NOT_COVER**

Fact sought: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Fact established: Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values.

The need asks for repository/snapshot/content checks binding disclosure to plan. This unit establishes qualified-reference purpose, derivation, analysis, target-type and resolution admission plus materializer re-admission. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

**review: PARTIALLY_COVERS**

Fact sought: repository, snapshot, content and plan/item identity checks binding a disclosure to its plan

Fact established: Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values.

The need seeks repository, snapshot, content and plan/item identity checks binding a disclosure to its plan. It covers derivation/coverage and analysis-membership consistency relevant to evidence binding; it does not require blank-purpose admission, supported target/route restrictions and rechecking directly constructed immutable values. Therefore its complete answer does not establish the whole unit.

covered_part: derivation/coverage and analysis-membership consistency relevant to evidence binding

missing_part: blank-purpose admission, supported target/route restrictions and rechecking directly constructed immutable values

### case-0011-context-utf8-ceiling/frame/binding × unit-ab36d70f1deecd237ce4358ffb3258f71b19a55589c1815c3a99545581e8cbdf

Need: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Unit: Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained.

Owning need obligation: frame; unit obligations: ['frame']; alternatives: ['alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063'].

**primary: PARTIALLY_COVERS**

Fact sought: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Fact established: Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained.

The need seeks target resource and repository/snapshot frame consistency of resolution support and retained analysis. The complete unit additionally requires target declaration membership when analysis is retained; answering this need need not establish that remainder.

covered_part: target resource and repository/snapshot frame consistency of resolution support and retained analysis

missing_part: target declaration membership when analysis is retained

**review: DIRECTLY_COVERS**

Fact sought: repository, snapshot, content and plan/item identity checks binding a disclosure to its plan

Fact established: Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained.

Retained target resolution and declaration evidence are content/frame bindings. A complete answer includes matching resource/repository/snapshot identities and declaration membership when analysis exists, exhausting the unit.

### case-0011-context-utf8-ceiling/frame/items × unit-f2f60cee7a81549ef3634c65a08ec026019e35505a0b7457ff348af70571ace3

Need: What contracts retain item order, exact item text and native disclosure provenance?

Unit: Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation.

Owning need obligation: frame; unit obligations: ['frame']; alternatives: ['alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063'].

**primary: DIRECTLY_COVERS**

Fact sought: What contracts retain item order, exact item text and native disclosure provenance?

Fact established: Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation.

The item-order/exact-text/native-provenance contract question seeks the common retained item structure and its correspondence to the ordered plan. A complete answer gives immutable identity, representation, addresses, content identities, text and native provenance plus one matching item per ordered choice, establishing the entire unit.

**review: PARTIALLY_COVERS**

Fact sought: ordered item realization and retention of exact text and native provenance

Fact established: Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation.

The need seeks ordered item realization and retention of exact text and native provenance. It covers immutable exact-text/native-provenance retention and one item per ordered choice; it does not require the complete address/content/option/representation identity schema and matching requirements. Therefore its complete answer does not establish the whole unit.

covered_part: immutable exact-text/native-provenance retention and one item per ordered choice

missing_part: the complete address/content/option/representation identity schema and matching requirements

### case-0011-context-utf8-ceiling/exports/public-boundary × unit-0057f1c75647a0b3e2d678bb704888665ee7ffbfeec0e56f27c501027a03c027

Need: What public Context Planning package exports expose copied assembly to callers?

Unit: The planning public package explicitly imports and lists its common renderer, rendered value and assembler in __all__.

Owning need obligation: exports; unit obligations: ['exports']; alternatives: ['alternative-fa2c4638c8d6ffb4c5cab8f91fcc0e562d8256c72a831797541622b2bf8531c6'].

**primary: PARTIALLY_COVERS**

Fact sought: What public Context Planning package exports expose copied assembly to callers?

Fact established: The planning public package explicitly imports and lists its common renderer, rendered value and assembler in __all__.

The need seeks the planning package assembler import/export exposing copied assembly. The complete unit additionally requires explicit common renderer and rendered-value companion imports and their __all__ entries; answering this need need not establish that remainder.

covered_part: the planning package assembler import/export exposing copied assembly

missing_part: explicit common renderer and rendered-value companion imports and their __all__ entries

**review: DIRECTLY_COVERS**

Fact sought: the public import and __all__ boundaries exposing assembly and its companion values

Fact established: The planning public package explicitly imports and lists its common renderer, rendered value and assembler in __all__.

A complete public-boundary answer identifies the planning imports and __all__ entries for the assembler and the renderer/value through which callers supply it. These are exactly this unit's export facts.

### case-0011-context-utf8-ceiling/exports/public-boundary × unit-8ad51eaf88aadfa2dd3d6fff7c23390b4bec7f204bc74d276ba759e0e6b3aa14

Need: What public Context Planning package exports expose copied assembly to callers?

Unit: The outer Context public facade explicitly imports the common planning assembler and companion plan/materialization/rendering symbols and lists them in __all__.

Owning need obligation: exports; unit obligations: ['exports']; alternatives: ['alternative-fa2c4638c8d6ffb4c5cab8f91fcc0e562d8256c72a831797541622b2bf8531c6'].

**primary: PARTIALLY_COVERS**

Fact sought: What public Context Planning package exports expose copied assembly to callers?

Fact established: The outer Context public facade explicitly imports the common planning assembler and companion plan/materialization/rendering symbols and lists them in __all__.

The need seeks public exposure of the common planning assembler. The complete unit additionally requires the distinct outer Context facade and its complete companion plan/materialization/rendering imports and __all__ entries; answering this need need not establish that remainder.

covered_part: public exposure of the common planning assembler

missing_part: the distinct outer Context facade and its complete companion plan/materialization/rendering imports and __all__ entries

**review: DIRECTLY_COVERS**

Fact sought: the public import and __all__ boundaries exposing assembly and its companion values

Fact established: The outer Context public facade explicitly imports the common planning assembler and companion plan/materialization/rendering symbols and lists them in __all__.

Exposing common assembly to callers includes the outer Context facade, its explicit imports and __all__ entries for the assembler and companion planning values. Explaining that public boundary establishes the entire unit.

### case-0011-context-utf8-ceiling/tests/text-boundaries × unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c

Need: Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Unit: Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes.

Owning need obligation: tests; unit obligations: ['bytes', 'request']; alternatives: ['alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1', 'alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1'].

**primary: PARTIALLY_COVERS**

Fact sought: Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Fact established: Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes.

The need seeks preserved exact rendered strings, UTF-8 and newline boundaries. The complete unit additionally requires the full assembly envelopes and independent reported Context byte length excluding the task; answering this need need not establish that remainder.

covered_part: preserved exact rendered strings, UTF-8 and newline boundaries

missing_part: the full assembly envelopes and independent reported Context byte length excluding the task

**review: DOES_NOT_COVER**

Fact sought: existing exact-text, non-ASCII and newline tests and their text fixtures

Fact established: Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes.

The need seeks existing exact-text, non-ASCII and newline tests and their text fixtures. This unit instead establishes task/Context envelopes combined with independent UTF-8 counting and byte fidelity. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/text-boundaries × unit-87f78f68bcbaca8cbda3d9fc4b8f1daee88e66a1ed350ec6441d5861cbb400fc

Need: Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Unit: Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference.

Owning need obligation: tests; unit obligations: ['tests']; alternatives: ['alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed'].

**primary: DOES_NOT_COVER**

Fact sought: Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Fact established: Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference.

The need asks for exact-text/non-ASCII/newline tests and fixtures. This unit establishes qualified test-option construction via interpretation, production analysis and retained-reference choice. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

**review: PARTIALLY_COVERS**

Fact sought: existing exact-text, non-ASCII and newline tests and their text fixtures

Fact established: Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference.

The need seeks existing exact-text, non-ASCII and newline tests and their text fixtures. It covers identification of a retained qualified option used as a text-test fixture; it does not require construction through module interpretation and production reference analysis before choosing the reference. Therefore its complete answer does not establish the whole unit.

covered_part: identification of a retained qualified option used as a text-test fixture

missing_part: construction through module interpretation and production reference analysis before choosing the reference

### case-0011-context-utf8-ceiling/tests/text-boundaries × unit-e3c24d637a4dca9783a7b6b86dbe1abcda4ad0117b8933cc798af53004501e08

Need: Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Unit: Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization.

Owning need obligation: tests; unit obligations: ['bytes']; alternatives: ['alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1'].

**primary: PARTIALLY_COVERS**

Fact sought: Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Fact established: Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization.

The need seeks exact-text and newline preservation behavior. The complete unit additionally requires the full canonical renderer header, identity, count and ordered-heading construction; answering this need need not establish that remainder.

covered_part: exact-text and newline preservation behavior

missing_part: the full canonical renderer header, identity, count and ordered-heading construction

**review: DOES_NOT_COVER**

Fact sought: existing exact-text, non-ASCII and newline tests and their text fixtures

Fact established: Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization.

The need seeks existing exact-text, non-ASCII and newline tests and their text fixtures. This unit instead establishes the complete canonical rendered-disclosure text layout. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/frame-rejection × unit-21e7319918686d72a7f9e79f31bc68ed4922858fa7bfa299d351ea43ef3b0b87

Need: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Unit: Qualified-reference materialization checks the source dependency repository/snapshot, source occurrence snapshot/address, resource presence and equality with retained source content.

Owning need obligation: tests; unit obligations: ['frame']; alternatives: ['alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Fact established: Qualified-reference materialization checks the source dependency repository/snapshot, source occurrence snapshot/address, resource presence and equality with retained source content.

The need seeks tested source frame/content mismatch and missing-resource rejection. The complete unit additionally requires the complete source dependency and occurrence snapshot/address checking contract; answering this need need not establish that remainder.

covered_part: tested source frame/content mismatch and missing-resource rejection

missing_part: the complete source dependency and occurrence snapshot/address checking contract

**review: DOES_NOT_COVER**

Fact sought: existing tests distinguishing foreign/stale frames and retained-content mismatches

Fact established: Qualified-reference materialization checks the source dependency repository/snapshot, source occurrence snapshot/address, resource presence and equality with retained source content.

The need seeks existing tests distinguishing foreign/stale frames and retained-content mismatches. This unit instead establishes source-side qualified materialization frame/content checks. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/frame-rejection × unit-4b3c320635122396ffe052357de8b5f96f074e35017c0331a650de95844eaccd

Need: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Unit: Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed.

Owning need obligation: tests; unit obligations: ['frame']; alternatives: ['alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Fact established: Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed.

The need seeks tested common repository/snapshot mismatch rejection. The complete unit additionally requires ordered realization, returned identity/representation checks and all-success publication; answering this need need not establish that remainder.

covered_part: tested common repository/snapshot mismatch rejection

missing_part: ordered realization, returned identity/representation checks and all-success publication

**review: DOES_NOT_COVER**

Fact sought: existing tests distinguishing foreign/stale frames and retained-content mismatches

Fact established: Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed.

The need seeks existing tests distinguishing foreign/stale frames and retained-content mismatches. This unit instead establishes common materialization ordering, admission and atomic publication. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/frame-rejection × unit-5e58e7852d6acb8027c97bf0d6ccc3deede219f1c229e52225d0b31b7ed29af6

Need: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Unit: Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices.

Owning need obligation: tests; unit obligations: ['frame']; alternatives: ['alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Fact established: Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices.

The need seeks tested mixed repository/snapshot frame rejection. The complete unit additionally requires the immutable ordered-plan contract and its other purpose, emptiness and duplicate checks; answering this need need not establish that remainder.

covered_part: tested mixed repository/snapshot frame rejection

missing_part: the immutable ordered-plan contract and its other purpose, emptiness and duplicate checks

**review: DOES_NOT_COVER**

Fact sought: existing tests distinguishing foreign/stale frames and retained-content mismatches

Fact established: Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices.

The need seeks existing tests distinguishing foreign/stale frames and retained-content mismatches. This unit instead establishes the immutable plan's structure and all choice/purpose/frame admission restrictions. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/frame-rejection × unit-a2c6080b9a63cdbb8cb2057c41ba2c618614bc672246ada53ce1f470cf4d7fca

Need: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Unit: Qualified-reference materialization checks target support/subject snapshots, target resource presence, subject resource-dependency identity and equality with retained target support.

Owning need obligation: tests; unit obligations: ['frame']; alternatives: ['alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Fact established: Qualified-reference materialization checks target support/subject snapshots, target resource presence, subject resource-dependency identity and equality with retained target support.

The need seeks tested target frame/content mismatch and missing-resource rejection. The complete unit additionally requires the complete target support/subject snapshot and subject resource-dependency checks; answering this need need not establish that remainder.

covered_part: tested target frame/content mismatch and missing-resource rejection

missing_part: the complete target support/subject snapshot and subject resource-dependency checks

**review: DOES_NOT_COVER**

Fact sought: existing tests distinguishing foreign/stale frames and retained-content mismatches

Fact established: Qualified-reference materialization checks target support/subject snapshots, target resource presence, subject resource-dependency identity and equality with retained target support.

The need seeks existing tests distinguishing foreign/stale frames and retained-content mismatches. This unit instead establishes target-side materialization frame/content checks. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/frame-rejection × unit-ab36d70f1deecd237ce4358ffb3258f71b19a55589c1815c3a99545581e8cbdf

Need: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Unit: Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained.

Owning need obligation: tests; unit obligations: ['frame']; alternatives: ['alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Fact established: Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained.

The need seeks tested target resource and repository/snapshot frame consistency. The complete unit additionally requires retained analysis target declaration-membership checks; answering this need need not establish that remainder.

covered_part: tested target resource and repository/snapshot frame consistency

missing_part: retained analysis target declaration-membership checks

**review: DOES_NOT_COVER**

Fact sought: existing tests distinguishing foreign/stale frames and retained-content mismatches

Fact established: Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained.

The need seeks existing tests distinguishing foreign/stale frames and retained-content mismatches. This unit instead establishes qualified target support/declaration frame and membership checks. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/frame-rejection × unit-eac315eb2a9f6a5634e094a5d4ef2960559030b62385b832a57f0f8d893b72de

Need: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Unit: Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance.

Owning need obligation: tests; unit obligations: ['frame']; alternatives: ['alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Fact established: Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance.

The need seeks tested foreign/stale/missing/unequal-occurrence rejection. The complete unit additionally requires exact item text, retained identities and original native provenance; answering this need need not establish that remainder.

covered_part: tested foreign/stale/missing/unequal-occurrence rejection

missing_part: exact item text, retained identities and original native provenance

**review: DOES_NOT_COVER**

Fact sought: existing tests distinguishing foreign/stale frames and retained-content mismatches

Fact established: Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance.

The need seeks existing tests distinguishing foreign/stale frames and retained-content mismatches. This unit instead establishes whole-resource admission coupled with retained text/identity/native provenance. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/request-preservation × unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7

Need: Which tests establish copied-request preservation and invalid argument validation?

Unit: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

Owning need obligation: tests; unit obligations: ['request']; alternatives: ['alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish copied-request preservation and invalid argument validation?

Fact established: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

The need seeks preservation of tested non-prompt request fields. The complete unit additionally requires the frozen dataclass declaration and complete field inventory including tools; answering this need need not establish that remainder.

covered_part: preservation of tested non-prompt request fields

missing_part: the frozen dataclass declaration and complete field inventory including tools

**review: DOES_NOT_COVER**

Fact sought: existing copied-request preservation tests and invalid-argument test conventions

Fact established: ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

The need seeks existing copied-request preservation tests and invalid-argument test conventions. This unit instead establishes the immutable ModelRequest schema and complete field inventory. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/request-preservation × unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605

Need: Which tests establish copied-request preservation and invalid argument validation?

Unit: The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

Owning need obligation: tests; unit obligations: ['ceiling']; alternatives: ['alternative-5823cd216c59ce3b109a4657e44e0050b4fbc485a58d5da984d3e7da3ebed7c5', 'alternative-d1599c2ce73551e58d4eeb482661a9e62312f3766c7a77dd9bb95a8a7c1a3638', 'alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish copied-request preservation and invalid argument validation?

Fact established: The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

The need seeks copied-request preservation and argument-admission behavior under assembly. The complete unit additionally requires the keyword-only signature, rendered type, lack of a limit and full-text/final-replace implementation contract; answering this need need not establish that remainder.

covered_part: copied-request preservation and argument-admission behavior under assembly

missing_part: the keyword-only signature, rendered type, lack of a limit and full-text/final-replace implementation contract

**review: DOES_NOT_COVER**

Fact sought: existing copied-request preservation tests and invalid-argument test conventions

Fact established: The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

The need seeks existing copied-request preservation tests and invalid-argument test conventions. This unit instead establishes the existing assembly signature and final copied-request construction boundary. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/request-preservation × unit-a090f45af360240ad7ce7630ffd09098a6a1b7887839d5266196a6f645880702

Need: Which tests establish copied-request preservation and invalid argument validation?

Unit: Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role.

Owning need obligation: tests; unit obligations: ['request']; alternatives: ['alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish copied-request preservation and invalid argument validation?

Fact established: Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role.

The need seeks tested role and non-prompt field preservation. The complete unit additionally requires the actual dataclasses.replace implementation replacing only Prompt; answering this need need not establish that remainder.

covered_part: tested role and non-prompt field preservation

missing_part: the actual dataclasses.replace implementation replacing only Prompt

**review: DOES_NOT_COVER**

Fact sought: existing copied-request preservation tests and invalid-argument test conventions

Fact established: Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role.

The need seeks existing copied-request preservation tests and invalid-argument test conventions. This unit instead establishes the exact replace and role-preserving Prompt construction operation. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/tests/request-preservation × unit-f7ba939e852e8f0f8e89d99664675a3cd8f8c1d48ac0acdc0bc9b4ebb7d22c50

Need: Which tests establish copied-request preservation and invalid argument validation?

Unit: Immutable ModelUsage optional integer admission accepts None, rejects bool and non-int with descriptive TypeError, and rejects negative counts with descriptive ValueError.

Owning need obligation: tests; unit obligations: ['ceiling']; alternatives: ['alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc'].

**primary: PARTIALLY_COVERS**

Fact sought: Which tests establish copied-request preservation and invalid argument validation?

Fact established: Immutable ModelUsage optional integer admission accepts None, rejects bool and non-int with descriptive TypeError, and rejects negative counts with descriptive ValueError.

The need seeks optional integer/type/negative-count testable admission behavior. The complete unit additionally requires the complete ModelUsage admission contract and its separate TypeError versus ValueError convention; answering this need need not establish that remainder.

covered_part: optional integer/type/negative-count testable admission behavior

missing_part: the complete ModelUsage admission contract and its separate TypeError versus ValueError convention

**review: DOES_NOT_COVER**

Fact sought: existing copied-request preservation tests and invalid-argument test conventions

Fact established: Immutable ModelUsage optional integer admission accepts None, rejects bool and non-int with descriptive TypeError, and rejects negative counts with descriptive ValueError.

The need seeks existing copied-request preservation tests and invalid-argument test conventions. This unit instead establishes the ModelUsage optional integer admission precedent. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/documentation/architecture × unit-183296beacda118e38a058b6d2588e582fd74639627706768ea3eb9396cc4580

Need: What governing architecture documentation distinguishes Context capacity from automatic selection?

Unit: The planning overview describes exact materialization, native provenance, appended copied-request Context and both supported choices, and distinguishes future token budgets/universal costs from current behavior.

Owning need obligation: documentation; unit obligations: ['documentation']; alternatives: ['alternative-15d7c3ffc813581557be5c4e0732549f4686d0fe3999af4783abbbbb7c9db6eb'].

**primary: PARTIALLY_COVERS**

Fact sought: What governing architecture documentation distinguishes Context capacity from automatic selection?

Fact established: The planning overview describes exact materialization, native provenance, appended copied-request Context and both supported choices, and distinguishes future token budgets/universal costs from current behavior.

The need seeks distinction of capacity/selection and future budgets from current behavior. The complete unit additionally requires the package overview facts about exact materialization, native provenance, copied Context and both supported choices; answering this need need not establish that remainder.

covered_part: distinction of capacity/selection and future budgets from current behavior

missing_part: the package overview facts about exact materialization, native provenance, copied Context and both supported choices

**review: DOES_NOT_COVER**

Fact sought: the governing architecture document and its current capacity versus selection contract

Fact established: The planning overview describes exact materialization, native provenance, appended copied-request Context and both supported choices, and distinguishes future token budgets/universal costs from current behavior.

The need seeks the governing architecture document and its current capacity versus selection contract. This unit instead establishes the planning overview's current and future capability claims. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/documentation/architecture × unit-33a494497198cadf88145cc45dc05ca55e09e6405588ce5cdd12c4f2c65e8371

Need: What governing architecture documentation distinguishes Context capacity from automatic selection?

Unit: The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature.

Owning need obligation: documentation; unit obligations: ['documentation']; alternatives: ['alternative-15d7c3ffc813581557be5c4e0732549f4686d0fe3999af4783abbbbb7c9db6eb'].

**primary: PARTIALLY_COVERS**

Fact sought: What governing architecture documentation distinguishes Context capacity from automatic selection?

Fact established: The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature.

The need seeks identification of governing architecture documentation relevant to bounded capacity. The complete unit additionally requires its canonical current cross-package status and full current planning/materialization/rendering/assembly description; answering this need need not establish that remainder.

covered_part: identification of governing architecture documentation relevant to bounded capacity

missing_part: its canonical current cross-package status and full current planning/materialization/rendering/assembly description

**review: DIRECTLY_COVERS**

Fact sought: the governing architecture document and its current capacity versus selection contract

Fact established: The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature.

Identifying governing architecture for the capacity change requires identifying its canonical authority and the current planning-to-assembly account being extended. The unit establishes precisely that authority and existing architectural scope.

### case-0011-context-utf8-ceiling/documentation/package × unit-33a494497198cadf88145cc45dc05ca55e09e6405588ce5cdd12c4f2c65e8371

Need: What package documentation describes rendered Context and copied assembly contracts?

Unit: The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature.

Owning need obligation: documentation; unit obligations: ['documentation']; alternatives: ['alternative-15d7c3ffc813581557be5c4e0732549f4686d0fe3999af4783abbbbb7c9db6eb'].

**primary: PARTIALLY_COVERS**

Fact sought: What package documentation describes rendered Context and copied assembly contracts?

Fact established: The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature.

The need seeks documented current planning/rendering/assembly behavior. The complete unit additionally requires identification and canonical current status of the governing cross-package architecture overview; answering this need need not establish that remainder.

covered_part: documented current planning/rendering/assembly behavior

missing_part: identification and canonical current status of the governing cross-package architecture overview

**review: DOES_NOT_COVER**

Fact sought: package documentation of rendered Context and copied assembly contracts

Fact established: The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature.

The need seeks package documentation of rendered Context and copied assembly contracts. This unit instead establishes the governing architecture document's canonical authority and existing pipeline scope. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/documentation/package × unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c

Need: What package documentation describes rendered Context and copied assembly contracts?

Unit: Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes.

Owning need obligation: documentation; unit obligations: ['bytes', 'request']; alternatives: ['alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1', 'alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1'].

**primary: PARTIALLY_COVERS**

Fact sought: What package documentation describes rendered Context and copied assembly contracts?

Fact established: Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes.

The need seeks documented task preservation with appended Context. The complete unit additionally requires the complete envelopes, independently reported UTF-8 length and embedded newline-byte semantics; answering this need need not establish that remainder.

covered_part: documented task preservation with appended Context

missing_part: the complete envelopes, independently reported UTF-8 length and embedded newline-byte semantics

**review: DOES_NOT_COVER**

Fact sought: package documentation of rendered Context and copied assembly contracts

Fact established: Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes.

The need seeks package documentation of rendered Context and copied assembly contracts. This unit instead establishes task/Context envelopes combined with independent UTF-8 counting and byte fidelity. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/documentation/package × unit-e3c24d637a4dca9783a7b6b86dbe1abcda4ad0117b8933cc798af53004501e08

Need: What package documentation describes rendered Context and copied assembly contracts?

Unit: Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization.

Owning need obligation: documentation; unit obligations: ['bytes']; alternatives: ['alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1'].

**primary: PARTIALLY_COVERS**

Fact sought: What package documentation describes rendered Context and copied assembly contracts?

Fact established: Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization.

The need seeks documented unchanged rendered item text and ordered Context construction. The complete unit additionally requires the complete canonical header, identity, count, heading and explicit LF/no-normalization construction; answering this need need not establish that remainder.

covered_part: documented unchanged rendered item text and ordered Context construction

missing_part: the complete canonical header, identity, count, heading and explicit LF/no-normalization construction

**review: DOES_NOT_COVER**

Fact sought: package documentation of rendered Context and copied assembly contracts

Fact established: Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization.

The need seeks package documentation of rendered Context and copied assembly contracts. This unit instead establishes the complete canonical rendered-disclosure text layout. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

### case-0011-context-utf8-ceiling/validation/protected-entry × unit-7ec311946c51700e892b24d725de3a5b89904e240505c5e5e79e4d1736e56bb9

Need: What established entry point runs protected development validation?

Unit: Project configuration enforces strict pytest configuration/markers and production devtools branch coverage at a 100 percent threshold.

Owning need obligation: validation; unit obligations: ['validation']; alternatives: ['alternative-112ca6b6a76691a25e2cf528a62311634ca38c88086c4464abdc1d3588733158'].

**primary: DOES_NOT_COVER**

Fact sought: What established entry point runs protected development validation?

Fact established: Project configuration enforces strict pytest configuration/markers and production devtools branch coverage at a 100 percent threshold.

The need asks for identification of the protected validation entry point. This unit establishes strict pytest configuration/markers and production branch coverage threshold. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

**review: PARTIALLY_COVERS**

Fact sought: the established protected development validation entry point and its scope

Fact established: Project configuration enforces strict pytest configuration/markers and production devtools branch coverage at a 100 percent threshold.

The need seeks the established protected development validation entry point and its scope. It covers use of established project coverage settings through the protected entry point; it does not require strict pytest configuration/markers and the precise production branch-coverage threshold as configuration facts. Therefore its complete answer does not establish the whole unit.

covered_part: use of established project coverage settings through the protected entry point

missing_part: strict pytest configuration/markers and the precise production branch-coverage threshold as configuration facts

## Shared direct mappings: both semantic rationales

These agreed labels still receive a rationale review proposition; no agreed DOES_NOT_COVER mappings are added to inflate the packet.

### case-0011-context-utf8-ceiling/bytes/rendered-boundary × unit-e3c24d637a4dca9783a7b6b86dbe1abcda4ad0117b8933cc798af53004501e08

Need: What exact rendered Context text, headings and separators are appended during assembly?

Unit: Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization.

Primary rationale: A complete account of the exact appended rendered Context necessarily identifies the disclosure header, purpose, plan/snapshot identities, item count, ordered headings and option identities, unchanged item text, and explicit LF separators without normalization.

Independent rationale: An exact appended-payload answer must enumerate the header metadata, ordered headings/identities, unchanged item bodies and precise LF separators without normalization. Omitting any of these would leave the requested exact text unspecified.

### case-0011-context-utf8-ceiling/ceiling/validation × unit-50dcfb5fd4a867c57ed46736f5e8858a763c0a2f62aecc6e809ad822716dbb30

Need: What existing validation and error conventions apply to optional nonnegative integer limits and invalid booleans?

Unit: The existing request-side optional integer validator accepts None, explicitly rejects bool and non-int, and raises a descriptive ValueError; its positive token domain must not override the task's nonnegative byte domain.

Primary rationale: The optional integer/error-convention question seeks None admission, bool/non-int exclusion and descriptive exceptions. Answering the existing request validator convention establishes those rules and its positive token domain; the frozen nonnegative byte-domain question expressly requires recognizing that positive-token validation cannot be copied unchanged.

Independent rationale: Explaining applicable optional integer conventions includes the request-side None/type/ValueError precedent and distinguishing its positive token domain from the required nonnegative byte domain. Without that distinction the requested applicability question would be incompletely answered.

### case-0011-context-utf8-ceiling/ceiling/validation × unit-f7ba939e852e8f0f8e89d99664675a3cd8f8c1d48ac0acdc0bc9b4ebb7d22c50

Need: What existing validation and error conventions apply to optional nonnegative integer limits and invalid booleans?

Unit: Immutable ModelUsage optional integer admission accepts None, rejects bool and non-int with descriptive TypeError, and rejects negative counts with descriptive ValueError.

Primary rationale: The question seeks existing optional nonnegative integer admission and error conventions, including invalid booleans. The ModelUsage contract is exactly that convention: None is accepted, bool/non-int raise descriptive TypeError and negative counts raise descriptive ValueError.

Independent rationale: ModelUsage supplies the matching optional nonnegative integer admission precedent. A complete account of applicable type/domain error conventions establishes None acceptance, bool/non-int TypeError and negative ValueError for this immutable value.

### case-0011-context-utf8-ceiling/request/copy × unit-a090f45af360240ad7ce7630ffd09098a6a1b7887839d5266196a6f645880702

Need: How does copied ModelRequest assembly preserve all fields other than the appended Context?

Unit: Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role.

Primary rationale: How copied assembly preserves all other request fields asks for the actual copying operation and its Prompt preservation rule. The unit supplies dataclasses.replace with only prompt replaced and the original Prompt role retained; that operation completely answers the preservation mechanism.

Independent rationale: The field-preservation mechanism is replacing only prompt through dataclasses.replace and constructing the new Prompt with the original role. A complete copying answer establishes the exact operation and its role retention.

### case-0011-context-utf8-ceiling/frame/binding × unit-21e7319918686d72a7f9e79f31bc68ed4922858fa7bfa299d351ea43ef3b0b87

Need: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Unit: Qualified-reference materialization checks the source dependency repository/snapshot, source occurrence snapshot/address, resource presence and equality with retained source content.

Primary rationale: A complete answer to repository/snapshot/content binding checks must explain qualified-source dependency and occurrence frame/address checks, resource existence and equality with retained source content. Those are precisely the complete source-side frame contract established by the unit.

Independent rationale: The source-side repository/snapshot/content binding is part of the requested frame checks. A complete answer must identify the dependency and occurrence frames, address/presence checks and retained-content equality, which exhaust this unit.

### case-0011-context-utf8-ceiling/frame/binding × unit-a2c6080b9a63cdbb8cb2057c41ba2c618614bc672246ada53ce1f470cf4d7fca

Need: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Unit: Qualified-reference materialization checks target support/subject snapshots, target resource presence, subject resource-dependency identity and equality with retained target support.

Primary rationale: The content/frame binding question includes qualified-target support and subject snapshots, resource existence, subject resource-dependency identity and retained-support equality. Answering all target binding checks establishes the complete unit rather than merely sharing the word snapshot.

Independent rationale: The target-side binding question includes support/subject frames, presence, dependency identity and retained support equality. Each is part of the requested complete target frame check, with no independent non-frame clause in this unit.

### case-0011-context-utf8-ceiling/tests/text-boundaries × unit-1bb673f66452efaf4d344988ed48b3011927a477ec8a2c9b4f5e77b2fd81aa42

Need: Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Unit: Common planning tests build retained snapshots by writing exact UTF-8 bytes and observing explicitly addressed resources.

Primary rationale: Seeking existing exact-text, non-ASCII and newline fixtures requires the retained-resource fixture construction that preserves exact bytes. This unit establishes writing exact UTF-8 bytes and explicitly observing addressed resources to build retained snapshots; that setup is the complete relevant fixture fact sought.

Independent rationale: The exact-text fixture question requires how retained test text is made exact. Writing UTF-8 bytes and observing the addressed resources is the complete fixture mechanism stated here, so explaining that fixture establishes the unit.

### case-0011-context-utf8-ceiling/tests/frame-rejection × unit-a3e3b3430e6bfb7351af007e1cfff42c912e499682a4d3e332c4ac6b7e043580

Need: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Unit: Common planning tests distinguish changed snapshot from changed retained content under the same snapshot identity and exercise missing-resource rejection with replace and pytest.raises.

Primary rationale: The need expressly asks for tests of foreign/stale repository, snapshot and content rejection. A full answer identifies the changed-snapshot, same-snapshot changed-content and missing-resource cases, and how replace/pytest.raises exercise them, establishing the complete regression-test unit.

Independent rationale: A complete frame-rejection test answer distinguishes changed snapshots, changed content within a retained snapshot identity and missing resources, including the replacement/raises test idiom. These are exactly the test distinctions in the unit.

### case-0011-context-utf8-ceiling/tests/request-preservation × unit-1979aa6106ebf66bce887d463ebbcb9d0745566f1875c359373e6e5afb72a394

Need: Which tests establish copied-request preservation and invalid argument validation?

Unit: The common assembly test checks unchanged original task, Prompt role, shared settings/conversation/provider values, task-before-Context placement and replace(assembled, prompt=task.prompt) == task.

Primary rationale: The copied-request preservation test question seeks the complete common assembly regression: original task and role, shared non-prompt values, append placement and inverse replacement showing equality to the caller request. These assertions together establish the full reviewed test fact.

Independent rationale: The preservation-test question calls for the existing checks of original text, role, other fields and copy equivalence. Explaining the common assembly test completely includes its task-before-Context assertion and replacement-back equality, establishing every listed check.

### case-0011-context-utf8-ceiling/tests/request-preservation × unit-d553be405368fb0607f76e8e953d24dcecf462b0308474311add157d55b57fc7

Need: Which tests establish copied-request preservation and invalid argument validation?

Unit: Existing request numeric tests use pytest parametrization and descriptive ValueError matching for bool, string, float and out-of-domain integers, test None separately, and test valid integers; the new byte tests must accept zero as the task directs.

Primary rationale: The invalid-argument test question seeks existing numeric test conventions, including parametrization, descriptive ValueError matching, None and valid cases. The frozen task basis supplies the nonnegative byte domain, so a complete answer also distinguishes the new accepted zero from existing out-of-domain token integers.

Independent rationale: The requested invalid-argument tests include parametrized wrong-type/domain cases, descriptive matching, separate None and valid-integer cases. Interpreting those conventions for this task also requires the explicit zero exception, establishing the whole unit.

### case-0011-context-utf8-ceiling/validation/configuration × unit-7ec311946c51700e892b24d725de3a5b89904e240505c5e5e79e4d1736e56bb9

Need: What established tooling configuration constrains test, type and style validation?

Unit: Project configuration enforces strict pytest configuration/markers and production devtools branch coverage at a 100 percent threshold.

Primary rationale: The tooling-configuration question expressly seeks constraints on testing. Answering it establishes strict pytest configuration and markers, production branch coverage and the 100 percent threshold, which is the complete unit.

Independent rationale: The test-configuration question directly seeks strict pytest/marker settings and the production branch-coverage threshold. A complete configuration answer includes all of these enforcement settings.

### case-0011-context-utf8-ceiling/validation/configuration × unit-f0a8cdef8232323f591cb10fdee77345e0352146b082c5bea0fb239ac9602965

Need: What established tooling configuration constrains test, type and style validation?

Unit: Project configuration selects Python 3.12, Ruff ALL with documented exceptions and 88-column formatting, and strict mypy over source, test and experiment trees with explicit package bases and src import base.

Primary rationale: The test/type/style configuration question seeks the project interpreter, lint/format rules and typing settings. A complete answer establishes Python 3.12, Ruff ALL and exceptions, 88 columns, and strict mypy scopes/package/import-base settings, exactly the complete unit.

Independent rationale: The type/style configuration answer requires the Python version, Ruff selection/exceptions/line length, and strict mypy scope and import/package settings. These settings exhaust the complete unit.

## All 32 unit statuses

| Unit | Primary | Independent | Statement |
| --- | --- | --- | --- |
| unit-0057f1c75647a0b3e2d678bb704888665ee7ffbfeec0e56f27c501027a03c027 | PARTIAL_ONLY | COVERED | The planning public package explicitly imports and lists its common renderer, rendered value and assembler in __all__. |
| unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2 | UNCOVERED | PARTIAL_ONLY | Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values. |
| unit-1466ea6b2b7b8cdc077c41ad15c6baf8087b6e7a230723f83b9911815a09a10c | PARTIAL_ONLY | PARTIAL_ONLY | The protected command is the documented protected development entry point; it excludes the experiment test tree before collection, retains project pytest configuration and branch coverage with the 100 percent gate, returns pytest's exit code, and does not authorize excluded confirmation validation. |
| unit-183296beacda118e38a058b6d2588e582fd74639627706768ea3eb9396cc4580 | PARTIAL_ONLY | PARTIAL_ONLY | The planning overview describes exact materialization, native provenance, appended copied-request Context and both supported choices, and distinguishes future token budgets/universal costs from current behavior. |
| unit-1979aa6106ebf66bce887d463ebbcb9d0745566f1875c359373e6e5afb72a394 | COVERED | COVERED | The common assembly test checks unchanged original task, Prompt role, shared settings/conversation/provider values, task-before-Context placement and replace(assembled, prompt=task.prompt) == task. |
| unit-1bb673f66452efaf4d344988ed48b3011927a477ec8a2c9b4f5e77b2fd81aa42 | COVERED | COVERED | Common planning tests build retained snapshots by writing exact UTF-8 bytes and observing explicitly addressed resources. |
| unit-1bb99811c2a45a9ce6d5dc32206e23d64f9fffa2d10fa642ca5f4ea6ce518c69 | PARTIAL_ONLY | PARTIAL_ONLY | The qualified-reference plan adapter delegates to its validated materializer and renderer and retains both source/target addresses and content identities, the rendered text and native materialized value in the common item. |
| unit-21e7319918686d72a7f9e79f31bc68ed4922858fa7bfa299d351ea43ef3b0b87 | COVERED | COVERED | Qualified-reference materialization checks the source dependency repository/snapshot, source occurrence snapshot/address, resource presence and equality with retained source content. |
| unit-33a494497198cadf88145cc45dc05ca55e09e6405588ce5cdd12c4f2c65e8371 | PARTIAL_ONLY | COVERED | The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature. |
| unit-4b3c320635122396ffe052357de8b5f96f074e35017c0331a650de95844eaccd | PARTIAL_ONLY | PARTIAL_ONLY | Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed. |
| unit-50dcfb5fd4a867c57ed46736f5e8858a763c0a2f62aecc6e809ad822716dbb30 | COVERED | COVERED | The existing request-side optional integer validator accepts None, explicitly rejects bool and non-int, and raises a descriptive ValueError; its positive token domain must not override the task's nonnegative byte domain. |
| unit-5991a5afbd7d664372fc5b2357e8fbcacfa5d73d5560dcd97f853aa279e36b1c | PARTIAL_ONLY | PARTIAL_ONLY | The protected command runs tests only; the validation guide separately specifies uv Ruff lint/format, mypy and diff whitespace checks, including staged diff checking where applicable. |
| unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7 | PARTIAL_ONLY | COVERED | ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools. |
| unit-5e58e7852d6acb8027c97bf0d6ccc3deede219f1c229e52225d0b31b7ed29af6 | PARTIAL_ONLY | PARTIAL_ONLY | Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices. |
| unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7 | PARTIAL_ONLY | COVERED | Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency. |
| unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605 | PARTIAL_ONLY | COVERED | The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call. |
| unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c | PARTIAL_ONLY | PARTIAL_ONLY | Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes. |
| unit-7ec311946c51700e892b24d725de3a5b89904e240505c5e5e79e4d1736e56bb9 | COVERED | COVERED | Project configuration enforces strict pytest configuration/markers and production devtools branch coverage at a 100 percent threshold. |
| unit-87f78f68bcbaca8cbda3d9fc4b8f1daee88e66a1ed350ec6441d5861cbb400fc | UNCOVERED | PARTIAL_ONLY | Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference. |
| unit-8ad51eaf88aadfa2dd3d6fff7c23390b4bec7f204bc74d276ba759e0e6b3aa14 | PARTIAL_ONLY | COVERED | The outer Context public facade explicitly imports the common planning assembler and companion plan/materialization/rendering symbols and lists them in __all__. |
| unit-a090f45af360240ad7ce7630ffd09098a6a1b7887839d5266196a6f645880702 | COVERED | COVERED | Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role. |
| unit-a2c6080b9a63cdbb8cb2057c41ba2c618614bc672246ada53ce1f470cf4d7fca | COVERED | COVERED | Qualified-reference materialization checks target support/subject snapshots, target resource presence, subject resource-dependency identity and equality with retained target support. |
| unit-a3e3b3430e6bfb7351af007e1cfff42c912e499682a4d3e332c4ac6b7e043580 | COVERED | COVERED | Common planning tests distinguish changed snapshot from changed retained content under the same snapshot identity and exercise missing-resource rejection with replace and pytest.raises. |
| unit-ab36d70f1deecd237ce4358ffb3258f71b19a55589c1815c3a99545581e8cbdf | PARTIAL_ONLY | COVERED | Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained. |
| unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2 | PARTIAL_ONLY | COVERED | Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection. |
| unit-d553be405368fb0607f76e8e953d24dcecf462b0308474311add157d55b57fc7 | COVERED | COVERED | Existing request numeric tests use pytest parametrization and descriptive ValueError matching for bool, string, float and out-of-domain integers, test None separately, and test valid integers; the new byte tests must accept zero as the task directs. |
| unit-e3c24d637a4dca9783a7b6b86dbe1abcda4ad0117b8933cc798af53004501e08 | COVERED | COVERED | Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization. |
| unit-eac315eb2a9f6a5634e094a5d4ef2960559030b62385b832a57f0f8d893b72de | PARTIAL_ONLY | PARTIAL_ONLY | Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance. |
| unit-f0a8cdef8232323f591cb10fdee77345e0352146b082c5bea0fb239ac9602965 | COVERED | COVERED | Project configuration selects Python 3.12, Ruff ALL with documented exceptions and 88-column formatting, and strict mypy over source, test and experiment trees with explicit package bases and src import base. |
| unit-f2f60cee7a81549ef3634c65a08ec026019e35505a0b7457ff348af70571ace3 | COVERED | PARTIAL_ONLY | Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation. |
| unit-f7ba939e852e8f0f8e89d99664675a3cd8f8c1d48ac0acdc0bc9b4ebb7d22c50 | COVERED | COVERED | Immutable ModelUsage optional integer admission accepts None, rejects bool and non-int with descriptive TypeError, and rejects negative counts with descriptive ValueError. |
| unit-fddd6c59fb1d485b6e4a6a749f66062c76ddd58df987a692ae75827e2f9b8329 | PARTIAL_ONLY | PARTIAL_ONLY | The common mixed-plan test uses CRLF and non-ASCII qualified/whole-resource fixtures and checks unchanged retained source, native whole-resource provenance and rendered item order. |

Eight units upgrade from PARTIAL_ONLY to COVERED; one downgrades from COVERED to PARTIAL_ONLY. Twelve are covered in both; nine are partial-only in both. Both primary UNCOVERED units become independent PARTIAL_ONLY, not directly covered.

### Every unit-status disagreement and both rationales

#### unit-0057f1c75647a0b3e2d678bb704888665ee7ffbfeec0e56f27c501027a03c027

The planning public package explicitly imports and lists its common renderer, rendered value and assembler in __all__.

Primary: PARTIAL_ONLY; independent: COVERED.

Need case-0011-context-utf8-ceiling/exports/public-boundary: What public Context Planning package exports expose copied assembly to callers?

Primary PARTIALLY_COVERS: The need seeks the planning package assembler import/export exposing copied assembly. The complete unit additionally requires explicit common renderer and rendered-value companion imports and their __all__ entries; answering this need need not establish that remainder.

Independent DIRECTLY_COVERS: A complete public-boundary answer identifies the planning imports and __all__ entries for the assembler and the renderer/value through which callers supply it. These are exactly this unit's export facts.

#### unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2

Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values.

Primary: UNCOVERED; independent: PARTIAL_ONLY.

Need case-0011-context-utf8-ceiling/frame/binding: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Primary DOES_NOT_COVER: The need asks for repository/snapshot/content checks binding disclosure to plan. This unit establishes qualified-reference purpose, derivation, analysis, target-type and resolution admission plus materializer re-admission. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

Independent PARTIALLY_COVERS: The need seeks repository, snapshot, content and plan/item identity checks binding a disclosure to its plan. It covers derivation/coverage and analysis-membership consistency relevant to evidence binding; it does not require blank-purpose admission, supported target/route restrictions and rechecking directly constructed immutable values. Therefore its complete answer does not establish the whole unit.

#### unit-33a494497198cadf88145cc45dc05ca55e09e6405588ce5cdd12c4f2c65e8371

The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature.

Primary: PARTIAL_ONLY; independent: COVERED.

Need case-0011-context-utf8-ceiling/documentation/architecture: What governing architecture documentation distinguishes Context capacity from automatic selection?

Primary PARTIALLY_COVERS: The need seeks identification of governing architecture documentation relevant to bounded capacity. The complete unit additionally requires its canonical current cross-package status and full current planning/materialization/rendering/assembly description; answering this need need not establish that remainder.

Independent DIRECTLY_COVERS: Identifying governing architecture for the capacity change requires identifying its canonical authority and the current planning-to-assembly account being extended. The unit establishes precisely that authority and existing architectural scope.

Need case-0011-context-utf8-ceiling/documentation/package: What package documentation describes rendered Context and copied assembly contracts?

Primary PARTIALLY_COVERS: The need seeks documented current planning/rendering/assembly behavior. The complete unit additionally requires identification and canonical current status of the governing cross-package architecture overview; answering this need need not establish that remainder.

Independent DOES_NOT_COVER: The need seeks package documentation of rendered Context and copied assembly contracts. This unit instead establishes the governing architecture document's canonical authority and existing pipeline scope. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

#### unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7

ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

Primary: PARTIAL_ONLY; independent: COVERED.

Need case-0011-context-utf8-ceiling/ceiling/rejection: What assembly contract permits rejection before modifying a request, without truncating or omitting items?

Primary DOES_NOT_COVER: The need asks for the assembly rejection seam before request modification without item loss. This unit establishes the frozen ModelRequest dataclass and complete declared fields. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

Independent PARTIALLY_COVERS: The need seeks the assembly input and construction boundary at which full-context rejection can precede request copying. It covers immutability supporting rejection without modifying the caller request; it does not require the complete prompt/settings/conversation/provider_settings/tools field inventory. Therefore its complete answer does not establish the whole unit.

Need case-0011-context-utf8-ceiling/request/copy: How does copied ModelRequest assembly preserve all fields other than the appended Context?

Primary PARTIALLY_COVERS: The need seeks retention of the request fields other than the changed prompt. The complete unit additionally requires the complete declared field inventory and the frozen-dataclass declaration; answering this need need not establish that remainder.

Independent DIRECTLY_COVERS: An account of preserving every request field needs the full immutable request shape: prompt, settings, conversation, provider_settings and tools. That inventory and frozen-dataclass status establish the whole unit.

Need case-0011-context-utf8-ceiling/request/prompt: How are the original task text and Prompt role preserved when Context is appended?

Primary DOES_NOT_COVER: The need asks for original task text and Prompt role preservation. This unit establishes the frozen ModelRequest dataclass and complete declared fields. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

Independent PARTIALLY_COVERS: The need seeks preservation of the original task text and Prompt role during appending. It covers the prompt-bearing request whose Prompt is preserved; it does not require frozen-dataclass status and the complete inventory of other fields. Therefore its complete answer does not establish the whole unit.

Need case-0011-context-utf8-ceiling/tests/request-preservation: Which tests establish copied-request preservation and invalid argument validation?

Primary PARTIALLY_COVERS: The need seeks preservation of tested non-prompt request fields. The complete unit additionally requires the frozen dataclass declaration and complete field inventory including tools; answering this need need not establish that remainder.

Independent DOES_NOT_COVER: The need seeks existing copied-request preservation tests and invalid-argument test conventions. This unit instead establishes the immutable ModelRequest schema and complete field inventory. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

#### unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7

Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency.

Primary: PARTIAL_ONLY; independent: COVERED.

Need case-0011-context-utf8-ceiling/ownership/dependencies: What dependency constraints separate common Context Planning from language-specific adapters and Retrieval?

Primary PARTIALLY_COVERS: The need seeks absence of language-adapter and Retrieval dependencies. The complete unit additionally requires the actual ModelRequest/Prompt imports and type-only ContextDisclosure dependency; answering this need need not establish that remainder.

Independent DIRECTLY_COVERS: A complete dependency-boundary answer identifies the allowed ModelRequest/Prompt imports, the type-only ContextDisclosure dependency and absence of adapter/Retrieval dependencies in rendering and assembly. This establishes the complete import-boundary unit.

#### unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605

The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

Primary: PARTIAL_ONLY; independent: COVERED.

Need case-0011-context-utf8-ceiling/ownership/assembly-owner: Which common Context Planning contract owns copied ModelRequest assembly?

Primary DOES_NOT_COVER: The need asks for ownership of copied ModelRequest assembly. This unit establishes the complete existing assembly signature, rendered input, unlimited entire-text behavior and final copy step. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

Independent PARTIALLY_COVERS: The need seeks the common contract owning copied assembly and its caller-directed planning role. It covers identification of the common assembly entry point as the assembly contract; it does not require keyword-only rendered input, absent limit argument, full context handling and final replace timing. Therefore its complete answer does not establish the whole unit.

Need case-0011-context-utf8-ceiling/bytes/rendered-boundary: What exact rendered Context text, headings and separators are appended during assembly?

Primary PARTIALLY_COVERS: The need seeks assembly of the entire context.text. The complete unit additionally requires the keyword-only signature, rendered input type, absence of a limit argument and final replace staging; answering this need need not establish that remainder.

Independent PARTIALLY_COVERS: The need seeks the complete appended rendered payload, its headings, boundaries and separators. It covers assembly of the entire context.text payload; it does not require keyword-only rendered input, absent limit argument and final copied-request construction timing. Therefore its complete answer does not establish the whole unit.

Need case-0011-context-utf8-ceiling/ceiling/rejection: What assembly contract permits rejection before modifying a request, without truncating or omitting items?

Primary PARTIALLY_COVERS: The need seeks whole-context assembly and a copied request created only at the final replacement, providing a rejection seam. The complete unit additionally requires the keyword-only signature, rendered input type and absence of an existing limit argument; answering this need need not establish that remainder.

Independent DIRECTLY_COVERS: Locating the safe rejection boundary requires describing the current keyword-only rendered-disclosure input, lack of a ceiling, whole-context handling and final replace construction. Together these establish where rejection precedes the copied request without dropping items.

Need case-0011-context-utf8-ceiling/request/copy: How does copied ModelRequest assembly preserve all fields other than the appended Context?

Primary PARTIALLY_COVERS: The need seeks creation of the copied request by replacement. The complete unit additionally requires the complete entry-point signature, rendered input, no-limit signature and entire-text assembly contract; answering this need need not establish that remainder.

Independent PARTIALLY_COVERS: The need seeks the immutable request field inventory and copying mechanism preserving unrelated fields. It covers creation of the copied request at the final replace call; it does not require keyword-only RenderedContextDisclosure input, no existing limit argument and full-context assembly. Therefore its complete answer does not establish the whole unit.

Need case-0011-context-utf8-ceiling/tests/request-preservation: Which tests establish copied-request preservation and invalid argument validation?

Primary PARTIALLY_COVERS: The need seeks copied-request preservation and argument-admission behavior under assembly. The complete unit additionally requires the keyword-only signature, rendered type, lack of a limit and full-text/final-replace implementation contract; answering this need need not establish that remainder.

Independent DOES_NOT_COVER: The need seeks existing copied-request preservation tests and invalid-argument test conventions. This unit instead establishes the existing assembly signature and final copied-request construction boundary. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

#### unit-87f78f68bcbaca8cbda3d9fc4b8f1daee88e66a1ed350ec6441d5861cbb400fc

Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference.

Primary: UNCOVERED; independent: PARTIAL_ONLY.

Need case-0011-context-utf8-ceiling/tests/text-boundaries: Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Primary DOES_NOT_COVER: The need asks for exact-text/non-ASCII/newline tests and fixtures. This unit establishes qualified test-option construction via interpretation, production analysis and retained-reference choice. That unit fact is a different acquisition target: a complete answer to the need can leave it unknown, and no component of it is sought by this need. Subsystem proximity or possible incidental discovery is insufficient.

Independent PARTIALLY_COVERS: The need seeks existing exact-text, non-ASCII and newline tests and their text fixtures. It covers identification of a retained qualified option used as a text-test fixture; it does not require construction through module interpretation and production reference analysis before choosing the reference. Therefore its complete answer does not establish the whole unit.

#### unit-8ad51eaf88aadfa2dd3d6fff7c23390b4bec7f204bc74d276ba759e0e6b3aa14

The outer Context public facade explicitly imports the common planning assembler and companion plan/materialization/rendering symbols and lists them in __all__.

Primary: PARTIAL_ONLY; independent: COVERED.

Need case-0011-context-utf8-ceiling/exports/public-boundary: What public Context Planning package exports expose copied assembly to callers?

Primary PARTIALLY_COVERS: The need seeks public exposure of the common planning assembler. The complete unit additionally requires the distinct outer Context facade and its complete companion plan/materialization/rendering imports and __all__ entries; answering this need need not establish that remainder.

Independent DIRECTLY_COVERS: Exposing common assembly to callers includes the outer Context facade, its explicit imports and __all__ entries for the assembler and companion planning values. Explaining that public boundary establishes the entire unit.

#### unit-ab36d70f1deecd237ce4358ffb3258f71b19a55589c1815c3a99545581e8cbdf

Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained.

Primary: PARTIAL_ONLY; independent: COVERED.

Need case-0011-context-utf8-ceiling/frame/binding: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Primary PARTIALLY_COVERS: The need seeks target resource and repository/snapshot frame consistency of resolution support and retained analysis. The complete unit additionally requires target declaration membership when analysis is retained; answering this need need not establish that remainder.

Independent DIRECTLY_COVERS: Retained target resolution and declaration evidence are content/frame bindings. A complete answer includes matching resource/repository/snapshot identities and declaration membership when analysis exists, exhausting the unit.

Need case-0011-context-utf8-ceiling/tests/frame-rejection: Which tests establish foreign or stale repository/snapshot/content frame rejection?

Primary PARTIALLY_COVERS: The need seeks tested target resource and repository/snapshot frame consistency. The complete unit additionally requires retained analysis target declaration-membership checks; answering this need need not establish that remainder.

Independent DOES_NOT_COVER: The need seeks existing tests distinguishing foreign/stale frames and retained-content mismatches. This unit instead establishes qualified target support/declaration frame and membership checks. The requested answer can be complete without establishing that fact: identifying a related owner, behavior, document, test or tool does not establish a different contract or its particular implementation/assertions. No specific constituent of this unit is requested by this need in its frozen task context.

#### unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2

Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection.

Primary: PARTIAL_ONLY; independent: COVERED.

Need case-0011-context-utf8-ceiling/ownership/assembly-owner: Which common Context Planning contract owns copied ModelRequest assembly?

Primary PARTIALLY_COVERS: The need seeks common ownership of copied request assembly. The complete unit additionally requires ownership of ordered caller-directed plans, faithful realization before rendering, and independence from automatic selection and Retrieval; answering this need need not establish that remainder.

Independent DIRECTLY_COVERS: Identifying the common assembly owner as a contract requires its pipeline responsibility: caller-directed ordered plans, faithful realization, rendering and copied assembly, with automatic selection/Retrieval outside that ownership. This is a single architectural responsibility statement.

Need case-0011-context-utf8-ceiling/ownership/dependencies: What dependency constraints separate common Context Planning from language-specific adapters and Retrieval?

Primary PARTIALLY_COVERS: The need seeks common planning independence from Retrieval. The complete unit additionally requires ownership of ordered caller-directed plans and faithful realization through rendering and assembly; answering this need need not establish that remainder.

Independent PARTIALLY_COVERS: The need seeks allowed dependency directions and the separation of common planning from adapters and Retrieval. It covers independence from Retrieval and adapter-side ownership; it does not require the common owner's ordered caller-directed planning and faithful realization/rendering/assembly pipeline. Therefore its complete answer does not establish the whole unit.

Need case-0011-context-utf8-ceiling/frame/items: What contracts retain item order, exact item text and native disclosure provenance?

Primary PARTIALLY_COVERS: The need seeks ordered faithful realization. The complete unit additionally requires the complete common ownership/lifecycle boundary and independence from Retrieval and automatic selection; answering this need need not establish that remainder.

Independent PARTIALLY_COVERS: The need seeks ordered item realization and retention of exact text and native provenance. It covers ordered plans and faithful realization of selected items; it does not require common pipeline ownership and separation from Retrieval/automatic selection. Therefore its complete answer does not establish the whole unit.

Need case-0011-context-utf8-ceiling/documentation/architecture: What governing architecture documentation distinguishes Context capacity from automatic selection?

Primary PARTIALLY_COVERS: The need seeks separation from automatic selection. The complete unit additionally requires ownership of ordered caller-directed plans and faithful realization through rendering and copied assembly independently of Retrieval; answering this need need not establish that remainder.

Independent PARTIALLY_COVERS: The need seeks the governing architecture document and its current capacity versus selection contract. It covers the architectural distinction between common Context capacity and automatic selection; it does not require the complete ordered plan/realization/rendering/copied-assembly responsibility. Therefore its complete answer does not establish the whole unit.

#### unit-f2f60cee7a81549ef3634c65a08ec026019e35505a0b7457ff348af70571ace3

Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation.

Primary: COVERED; independent: PARTIAL_ONLY.

Need case-0011-context-utf8-ceiling/frame/binding: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Primary PARTIALLY_COVERS: The need seeks retained content identities and correspondence between disclosure and plan choices. The complete unit additionally requires the full immutable item field inventory, exact text/native provenance and ordered identity/representation correspondence; answering this need need not establish that remainder.

Independent PARTIALLY_COVERS: The need seeks repository, snapshot, content and plan/item identity checks binding a disclosure to its plan. It covers address/content/option/representation binding and one matching item per ordered plan choice; it does not require the immutable item's exact text and native_provenance retention. Therefore its complete answer does not establish the whole unit.

Need case-0011-context-utf8-ceiling/frame/items: What contracts retain item order, exact item text and native disclosure provenance?

Primary DIRECTLY_COVERS: The item-order/exact-text/native-provenance contract question seeks the common retained item structure and its correspondence to the ordered plan. A complete answer gives immutable identity, representation, addresses, content identities, text and native provenance plus one matching item per ordered choice, establishing the entire unit.

Independent PARTIALLY_COVERS: The need seeks ordered item realization and retention of exact text and native provenance. It covers immutable exact-text/native-provenance retention and one item per ordered choice; it does not require the complete address/content/option/representation identity schema and matching requirements. Therefore its complete answer does not establish the whole unit.

## All 18 need classifications

| Need | Primary | Independent | Statement |
| --- | --- | --- | --- |
| case-0011-context-utf8-ceiling/ownership/assembly-owner | PARTIAL_ONLY | NECESSARY | Which common Context Planning contract owns copied ModelRequest assembly? |
| case-0011-context-utf8-ceiling/ownership/dependencies | PARTIAL_ONLY | NECESSARY | What dependency constraints separate common Context Planning from language-specific adapters and Retrieval? |
| case-0011-context-utf8-ceiling/bytes/rendered-boundary | NECESSARY | NECESSARY | What exact rendered Context text, headings and separators are appended during assembly? |
| case-0011-context-utf8-ceiling/bytes/encoding | PARTIAL_ONLY | PARTIAL_ONLY | What existing UTF-8 and newline handling contracts preserve exact rendered text? |
| case-0011-context-utf8-ceiling/ceiling/validation | NECESSARY | NECESSARY | What existing validation and error conventions apply to optional nonnegative integer limits and invalid booleans? |
| case-0011-context-utf8-ceiling/ceiling/rejection | PARTIAL_ONLY | NECESSARY | What assembly contract permits rejection before modifying a request, without truncating or omitting items? |
| case-0011-context-utf8-ceiling/request/copy | NECESSARY | NECESSARY | How does copied ModelRequest assembly preserve all fields other than the appended Context? |
| case-0011-context-utf8-ceiling/request/prompt | PARTIAL_ONLY | USEFUL_REDUNDANT | How are the original task text and Prompt role preserved when Context is appended? |
| case-0011-context-utf8-ceiling/frame/binding | NECESSARY | NECESSARY | What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan? |
| case-0011-context-utf8-ceiling/frame/items | NECESSARY | PARTIAL_ONLY | What contracts retain item order, exact item text and native disclosure provenance? |
| case-0011-context-utf8-ceiling/exports/public-boundary | PARTIAL_ONLY | NECESSARY | What public Context Planning package exports expose copied assembly to callers? |
| case-0011-context-utf8-ceiling/tests/text-boundaries | NECESSARY | NECESSARY | Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior? |
| case-0011-context-utf8-ceiling/tests/frame-rejection | NECESSARY | NECESSARY | Which tests establish foreign or stale repository/snapshot/content frame rejection? |
| case-0011-context-utf8-ceiling/tests/request-preservation | NECESSARY | NECESSARY | Which tests establish copied-request preservation and invalid argument validation? |
| case-0011-context-utf8-ceiling/documentation/architecture | PARTIAL_ONLY | NECESSARY | What governing architecture documentation distinguishes Context capacity from automatic selection? |
| case-0011-context-utf8-ceiling/documentation/package | PARTIAL_ONLY | PARTIAL_ONLY | What package documentation describes rendered Context and copied assembly contracts? |
| case-0011-context-utf8-ceiling/validation/protected-entry | PARTIAL_ONLY | PARTIAL_ONLY | What established entry point runs protected development validation? |
| case-0011-context-utf8-ceiling/validation/configuration | NECESSARY | NECESSARY | What established tooling configuration constrains test, type and style validation? |

Primary-only NECESSARY: frame/items. Review-only NECESSARY: ownership/assembly-owner, ownership/dependencies, ceiling/rejection, exports/public-boundary, documentation/architecture. request/prompt changes PARTIAL_ONLY→USEFUL_REDUNDANT. frame/items changes NECESSARY→PARTIAL_ONLY. No MISFORMULATED or AMBIGUOUS classification or formulation disagreement is established.

### Every need-classification disagreement

#### case-0011-context-utf8-ceiling/ownership/assembly-owner

Which common Context Planning contract owns copied ModelRequest assembly?

Primary PARTIAL_ONLY: This need seeks an identifiable component of 1 units but no complete reviewed unit; no statement defect warrants MISFORMULATED.

Primary formulation: The frozen statement has a recognizable, answerable acquisition target. Partial mappings reflect its limited scope relative to compound gold facts, rather than an incoherent question or an unsupported premise. No meaning is genuinely under-specified.

Independent NECESSARY: The common ownership contract is uniquely established by this focused ownership question.

Independent formulation: Actionable repository information question in the frozen task context; neither misformulation nor unresolvable ambiguity is established. Narrow scope or lack of a whole-unit match is not misformulation.

#### case-0011-context-utf8-ceiling/ownership/dependencies

What dependency constraints separate common Context Planning from language-specific adapters and Retrieval?

Primary PARTIAL_ONLY: This need seeks an identifiable component of 2 units but no complete reviewed unit; no statement defect warrants MISFORMULATED.

Primary formulation: The frozen statement has a recognizable, answerable acquisition target. Partial mappings reflect its limited scope relative to compound gold facts, rather than an incoherent question or an unsupported premise. No meaning is genuinely under-specified.

Independent NECESSARY: Dependency boundaries are a distinct task constraint, uniquely sought completely here.

Independent formulation: Actionable repository information question in the frozen task context; neither misformulation nor unresolvable ambiguity is established. Narrow scope or lack of a whole-unit match is not misformulation.

#### case-0011-context-utf8-ceiling/ceiling/rejection

What assembly contract permits rejection before modifying a request, without truncating or omitting items?

Primary PARTIAL_ONLY: This need seeks an identifiable component of 2 units but no complete reviewed unit; no statement defect warrants MISFORMULATED.

Primary formulation: The frozen statement has a recognizable, answerable acquisition target. Partial mappings reflect its limited scope relative to compound gold facts, rather than an incoherent question or an unsupported premise. No meaning is genuinely under-specified.

Independent NECESSARY: The safe rejection boundary uniquely seeks the complete existing assembly input/construction contract.

Independent formulation: Actionable repository information question in the frozen task context; neither misformulation nor unresolvable ambiguity is established. Narrow scope or lack of a whole-unit match is not misformulation.

#### case-0011-context-utf8-ceiling/request/prompt

How are the original task text and Prompt role preserved when Context is appended?

Primary PARTIAL_ONLY: This need seeks an identifiable component of 3 units but no complete reviewed unit; no statement defect warrants MISFORMULATED.

Primary formulation: The frozen statement has a recognizable, answerable acquisition target. Partial mappings reflect its limited scope relative to compound gold facts, rather than an incoherent question or an unsupported premise. No meaning is genuinely under-specified.

Independent USEFUL_REDUNDANT: This is a usable, focused original-task/role question. Its directly covered Prompt-copy operation is also directly covered by N07. Its extra partial contribution to envelope accounting does not change the frozen redundant label.

Independent formulation: Actionable repository information question in the frozen task context; neither misformulation nor unresolvable ambiguity is established. Narrow scope or lack of a whole-unit match is not misformulation.

#### case-0011-context-utf8-ceiling/frame/items

What contracts retain item order, exact item text and native disclosure provenance?

Primary NECESSARY: This need directly seeks the complete facts of 1 units, including 1 uniquely directly covered units.

Primary formulation: The frozen statement has a recognizable, answerable acquisition target. Partial mappings reflect its limited scope relative to compound gold facts, rather than an incoherent question or an unsupported premise. No meaning is genuinely under-specified.

Independent PARTIAL_ONLY: The item-order/text/provenance concern is legitimate and collectively useful. The reviewed units add identity/admission, rendering metadata or test-specific facts, so no complete unit is directly established.

Independent formulation: Actionable repository information question in the frozen task context; neither misformulation nor unresolvable ambiguity is established. Narrow scope or lack of a whole-unit match is not misformulation.

#### case-0011-context-utf8-ceiling/exports/public-boundary

What public Context Planning package exports expose copied assembly to callers?

Primary PARTIAL_ONLY: This need seeks an identifiable component of 2 units but no complete reviewed unit; no statement defect warrants MISFORMULATED.

Primary formulation: The frozen statement has a recognizable, answerable acquisition target. Partial mappings reflect its limited scope relative to compound gold facts, rather than an incoherent question or an unsupported premise. No meaning is genuinely under-specified.

Independent NECESSARY: The public-boundary question uniquely seeks the planning and outer-facade export declarations.

Independent formulation: Actionable repository information question in the frozen task context; neither misformulation nor unresolvable ambiguity is established. Narrow scope or lack of a whole-unit match is not misformulation.

#### case-0011-context-utf8-ceiling/documentation/architecture

What governing architecture documentation distinguishes Context capacity from automatic selection?

Primary PARTIAL_ONLY: This need seeks an identifiable component of 3 units but no complete reviewed unit; no statement defect warrants MISFORMULATED.

Primary formulation: The frozen statement has a recognizable, answerable acquisition target. Partial mappings reflect its limited scope relative to compound gold facts, rather than an incoherent question or an unsupported premise. No meaning is genuinely under-specified.

Independent NECESSARY: The governing-document question uniquely establishes canonical architecture authority and the current pipeline scope to extend.

Independent formulation: Actionable repository information question in the frozen task context; neither misformulation nor unresolvable ambiguity is established. Narrow scope or lack of a whole-unit match is not misformulation.

## Every witness alternative and member-level causes

Members remain ALL complementary within an alternative; alternatives remain ANY per obligation. Members are never pooled across alternatives. Primary states are derived under the strict direct rule; collective completeness is a secondary independent diagnostic.

### alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1 (bytes)

Primary direct complete: False; independent direct complete: False; independent diagnostic: FULLY_COVERED_ONLY_COLLECTIVELY.

Every member is required within this alternative. Every member is established, but at least one requires a listed diagnostic collective set.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c | PARTIAL_ONLY | PARTIAL_ONLY | COLLECTIVELY_COVERABLE | Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes. |
| unit-e3c24d637a4dca9783a7b6b86dbe1abcda4ad0117b8933cc798af53004501e08 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization. |

### alternative-5823cd216c59ce3b109a4657e44e0050b4fbc485a58d5da984d3e7da3ebed7c5 (ceiling)

Primary direct complete: False; independent direct complete: True; independent diagnostic: FULLY_DIRECTLY_COVERED.

Every member is required within this alternative. Every member has a direct need.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-50dcfb5fd4a867c57ed46736f5e8858a763c0a2f62aecc6e809ad822716dbb30 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | The existing request-side optional integer validator accepts None, explicitly rejects bool and non-int, and raises a descriptive ValueError; its positive token domain must not override the task's nonnegative byte domain. |
| unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call. |

### alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc (ceiling)

Primary direct complete: False; independent direct complete: True; independent diagnostic: FULLY_DIRECTLY_COVERED.

Every member is required within this alternative. Every member has a direct need.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call. |
| unit-f7ba939e852e8f0f8e89d99664675a3cd8f8c1d48ac0acdc0bc9b4ebb7d22c50 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Immutable ModelUsage optional integer admission accepts None, rejects bool and non-int with descriptive TypeError, and rejects negative counts with descriptive ValueError. |

### alternative-d1599c2ce73551e58d4eeb482661a9e62312f3766c7a77dd9bb95a8a7c1a3638 (ceiling)

Primary direct complete: False; independent direct complete: True; independent diagnostic: FULLY_DIRECTLY_COVERED.

Every member is required within this alternative. Every member has a direct need.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call. |
| unit-d553be405368fb0607f76e8e953d24dcecf462b0308474311add157d55b57fc7 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Existing request numeric tests use pytest parametrization and descriptive ValueError matching for bool, string, float and out-of-domain integers, test None separately, and test valid integers; the new byte tests must accept zero as the task directs. |

### alternative-15d7c3ffc813581557be5c4e0732549f4686d0fe3999af4783abbbbb7c9db6eb (documentation)

Primary direct complete: False; independent direct complete: False; independent diagnostic: INCOMPLETE.

Every member is required within this alternative. The listed incomplete members lack both a direct need and a defensible complete collective set. Other alternatives cannot fill these gaps inside this alternative.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-183296beacda118e38a058b6d2588e582fd74639627706768ea3eb9396cc4580 | PARTIAL_ONLY | PARTIAL_ONLY | ATOMIC_FOR_NEED_MAPPING | The planning overview describes exact materialization, native provenance, appended copied-request Context and both supported choices, and distinguishes future token budgets/universal costs from current behavior. |
| unit-33a494497198cadf88145cc45dc05ca55e09e6405588ce5cdd12c4f2c65e8371 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature. |

### alternative-fa2c4638c8d6ffb4c5cab8f91fcc0e562d8256c72a831797541622b2bf8531c6 (exports)

Primary direct complete: False; independent direct complete: True; independent diagnostic: FULLY_DIRECTLY_COVERED.

Every member is required within this alternative. Every member has a direct need.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-0057f1c75647a0b3e2d678bb704888665ee7ffbfeec0e56f27c501027a03c027 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | The planning public package explicitly imports and lists its common renderer, rendered value and assembler in __all__. |
| unit-8ad51eaf88aadfa2dd3d6fff7c23390b4bec7f204bc74d276ba759e0e6b3aa14 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | The outer Context public facade explicitly imports the common planning assembler and companion plan/materialization/rendering symbols and lists them in __all__. |

### alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063 (frame)

Primary direct complete: False; independent direct complete: False; independent diagnostic: INCOMPLETE.

Every member is required within this alternative. The listed incomplete members lack both a direct need and a defensible complete collective set. Other alternatives cannot fill these gaps inside this alternative.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2 | UNCOVERED | PARTIAL_ONLY | OVERCOMPOUND_FOR_PAIRWISE_MAPPING | Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values. |
| unit-1bb99811c2a45a9ce6d5dc32206e23d64f9fffa2d10fa642ca5f4ea6ce518c69 | PARTIAL_ONLY | PARTIAL_ONLY | COLLECTIVELY_COVERABLE | The qualified-reference plan adapter delegates to its validated materializer and renderer and retains both source/target addresses and content identities, the rendered text and native materialized value in the common item. |
| unit-21e7319918686d72a7f9e79f31bc68ed4922858fa7bfa299d351ea43ef3b0b87 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Qualified-reference materialization checks the source dependency repository/snapshot, source occurrence snapshot/address, resource presence and equality with retained source content. |
| unit-4b3c320635122396ffe052357de8b5f96f074e35017c0331a650de95844eaccd | PARTIAL_ONLY | PARTIAL_ONLY | COLLECTIVELY_COVERABLE | Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed. |
| unit-5e58e7852d6acb8027c97bf0d6ccc3deede219f1c229e52225d0b31b7ed29af6 | PARTIAL_ONLY | PARTIAL_ONLY | OVERCOMPOUND_FOR_PAIRWISE_MAPPING | Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices. |
| unit-a2c6080b9a63cdbb8cb2057c41ba2c618614bc672246ada53ce1f470cf4d7fca | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Qualified-reference materialization checks target support/subject snapshots, target resource presence, subject resource-dependency identity and equality with retained target support. |
| unit-ab36d70f1deecd237ce4358ffb3258f71b19a55589c1815c3a99545581e8cbdf | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained. |
| unit-eac315eb2a9f6a5634e094a5d4ef2960559030b62385b832a57f0f8d893b72de | PARTIAL_ONLY | PARTIAL_ONLY | COLLECTIVELY_COVERABLE | Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance. |
| unit-f2f60cee7a81549ef3634c65a08ec026019e35505a0b7457ff348af70571ace3 | COVERED | PARTIAL_ONLY | COLLECTIVELY_COVERABLE | Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation. |

### alternative-f8cc13a78a696e2cf395ea58f422d4eb26c24a17ba9eacbb7f3645755872877c (ownership)

Primary direct complete: False; independent direct complete: True; independent diagnostic: FULLY_DIRECTLY_COVERED.

Every member is required within this alternative. Every member has a direct need.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency. |
| unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection. |

### alternative-cf445deec2b6d543ca84fbd68a8dc1c97d0e7ce2f0ae19fc3b3e04f45231545f (ownership)

Primary direct complete: False; independent direct complete: True; independent diagnostic: FULLY_DIRECTLY_COVERED.

Every member is required within this alternative. Every member has a direct need.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency. |
| unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection. |

### alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1 (request)

Primary direct complete: False; independent direct complete: False; independent diagnostic: FULLY_COVERED_ONLY_COLLECTIVELY.

Every member is required within this alternative. Every member is established, but at least one requires a listed diagnostic collective set.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7 | PARTIAL_ONLY | COVERED | ATOMIC_FOR_NEED_MAPPING | ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools. |
| unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c | PARTIAL_ONLY | PARTIAL_ONLY | COLLECTIVELY_COVERABLE | Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes. |
| unit-a090f45af360240ad7ce7630ffd09098a6a1b7887839d5266196a6f645880702 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role. |

### alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed (tests)

Primary direct complete: False; independent direct complete: False; independent diagnostic: INCOMPLETE.

Every member is required within this alternative. The listed incomplete members lack both a direct need and a defensible complete collective set. Other alternatives cannot fill these gaps inside this alternative.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-1979aa6106ebf66bce887d463ebbcb9d0745566f1875c359373e6e5afb72a394 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | The common assembly test checks unchanged original task, Prompt role, shared settings/conversation/provider values, task-before-Context placement and replace(assembled, prompt=task.prompt) == task. |
| unit-1bb673f66452efaf4d344988ed48b3011927a477ec8a2c9b4f5e77b2fd81aa42 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Common planning tests build retained snapshots by writing exact UTF-8 bytes and observing explicitly addressed resources. |
| unit-87f78f68bcbaca8cbda3d9fc4b8f1daee88e66a1ed350ec6441d5861cbb400fc | UNCOVERED | PARTIAL_ONLY | ATOMIC_FOR_NEED_MAPPING | Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference. |
| unit-a3e3b3430e6bfb7351af007e1cfff42c912e499682a4d3e332c4ac6b7e043580 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Common planning tests distinguish changed snapshot from changed retained content under the same snapshot identity and exercise missing-resource rejection with replace and pytest.raises. |
| unit-d553be405368fb0607f76e8e953d24dcecf462b0308474311add157d55b57fc7 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Existing request numeric tests use pytest parametrization and descriptive ValueError matching for bool, string, float and out-of-domain integers, test None separately, and test valid integers; the new byte tests must accept zero as the task directs. |
| unit-fddd6c59fb1d485b6e4a6a749f66062c76ddd58df987a692ae75827e2f9b8329 | PARTIAL_ONLY | PARTIAL_ONLY | ATOMIC_FOR_NEED_MAPPING | The common mixed-plan test uses CRLF and non-ASCII qualified/whole-resource fixtures and checks unchanged retained source, native whole-resource provenance and rendered item order. |

### alternative-112ca6b6a76691a25e2cf528a62311634ca38c88086c4464abdc1d3588733158 (validation)

Primary direct complete: False; independent direct complete: False; independent diagnostic: INCOMPLETE.

Every member is required within this alternative. The listed incomplete members lack both a direct need and a defensible complete collective set. Other alternatives cannot fill these gaps inside this alternative.

| Member | Primary | Independent | Granularity | Statement |
| --- | --- | --- | --- | --- |
| unit-1466ea6b2b7b8cdc077c41ad15c6baf8087b6e7a230723f83b9911815a09a10c | PARTIAL_ONLY | PARTIAL_ONLY | OVERCOMPOUND_FOR_PAIRWISE_MAPPING | The protected command is the documented protected development entry point; it excludes the experiment test tree before collection, retains project pytest configuration and branch coverage with the 100 percent gate, returns pytest's exit code, and does not authorize excluded confirmation validation. |
| unit-5991a5afbd7d664372fc5b2357e8fbcacfa5d73d5560dcd97f853aa279e36b1c | PARTIAL_ONLY | PARTIAL_ONLY | COLLECTIVELY_COVERABLE | The protected command runs tests only; the validation guide separately specifies uv Ruff lint/format, mypy and diff whitespace checks, including staged diff checking where applicable. |
| unit-7ec311946c51700e892b24d725de3a5b89904e240505c5e5e79e4d1736e56bb9 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Project configuration enforces strict pytest configuration/markers and production devtools branch coverage at a 100 percent threshold. |
| unit-f0a8cdef8232323f591cb10fdee77345e0352146b082c5bea0fb239ac9602965 | COVERED | COVERED | ATOMIC_FOR_NEED_MAPPING | Project configuration selects Python 3.12, Ruff ALL with documented exceptions and 88-column formatting, and strict mypy over source, test and experiment trees with explicit package bases and src import base. |

## Independent unit-granularity audit

Primary C.5 did not independently supply this audit. These are independent propositions awaiting confirmation; reviewed gold is unchanged.

| Category | Count |
| --- | --- |
| ATOMIC_FOR_NEED_MAPPING | 23 |
| COLLECTIVELY_COVERABLE | 6 |
| OVERCOMPOUND_FOR_PAIRWISE_MAPPING | 3 |
| AMBIGUOUS_GRANULARITY | 0 |

### unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2 — OVERCOMPOUND_FOR_PAIRWISE_MAPPING

Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values.

The unit joins purpose validity, derivation/analysis membership, target-type/route support, and defensive re-admission of directly constructed values. These are independently searchable admission predicates plus a separate materializer enforcement fact. A single frame-binding need cannot reasonably be required to establish this entire bundle; the frozen needs do not ask for all of its purpose/type/route/re-admission dimensions.

Primary: UNCOVERED; independent: PARTIAL_ONLY.

Proposed minimal sets: []

### unit-1466ea6b2b7b8cdc077c41ad15c6baf8087b6e7a230723f83b9911815a09a10c — OVERCOMPOUND_FOR_PAIRWISE_MAPPING

The protected command is the documented protected development entry point; it excludes the experiment test tree before collection, retains project pytest configuration and branch coverage with the 100 percent gate, returns pytest's exit code, and does not authorize excluded confirmation validation.

The unit bundles documentation authority, pre-collection exclusion, retained configuration/coverage, exit-code propagation and an authorization boundary. Entry-point discovery and tooling configuration are legitimate distinct needs, but neither nor their union requires all implementation mechanics, especially exit-code propagation. Demanding one direct need for that bundle imposes an invalid pairwise contract.

Primary: PARTIAL_ONLY; independent: PARTIAL_ONLY.

Proposed minimal sets: []

### unit-1bb99811c2a45a9ce6d5dc32206e23d64f9fffa2d10fa642ca5f4ea6ce518c69 — COLLECTIVELY_COVERABLE

The qualified-reference plan adapter delegates to its validated materializer and renderer and retains both source/target addresses and content identities, the rendered text and native materialized value in the common item.

Validated source/target identity handoff and the renderer/text/native-value handoff are distinct dimensions of the same adapter bridge. N09 supplies the former and N10 the latter; either alone omits the other.

Primary: PARTIAL_ONLY; independent: PARTIAL_ONLY.

Proposed minimal sets: [['case-0011-context-utf8-ceiling/frame/binding', 'case-0011-context-utf8-ceiling/frame/items']]

### unit-4b3c320635122396ffe052357de8b5f96f074e35017c0331a650de95844eaccd — COLLECTIVELY_COVERABLE

Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed.

Frame/identity validation including publication only after all items validate is distinct from realization order. N09 supplies admission and all-success integrity; N10 supplies selected-choice order. Neither alone establishes both.

Primary: PARTIAL_ONLY; independent: PARTIAL_ONLY.

Proposed minimal sets: [['case-0011-context-utf8-ceiling/frame/binding', 'case-0011-context-utf8-ceiling/frame/items']]

### unit-5991a5afbd7d664372fc5b2357e8fbcacfa5d73d5560dcd97f853aa279e36b1c — COLLECTIVELY_COVERABLE

The protected command runs tests only; the validation guide separately specifies uv Ruff lint/format, mypy and diff whitespace checks, including staged diff checking where applicable.

The protected entry point's tests-only scope and the separately configured lint/format/type/whitespace workflow answer different validation questions. N17 supplies the scope and N18 the required separate tooling checks, including applicable staged checking.

Primary: PARTIAL_ONLY; independent: PARTIAL_ONLY.

Proposed minimal sets: [['case-0011-context-utf8-ceiling/validation/protected-entry', 'case-0011-context-utf8-ceiling/validation/configuration']]

### unit-5e58e7852d6acb8027c97bf0d6ccc3deede219f1c229e52225d0b31b7ed29af6 — OVERCOMPOUND_FOR_PAIRWISE_MAPPING

Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices.

The unit combines the immutable plan schema and ordering/frame identities with independently searchable purpose validity, nonempty selection, homogeneous purpose/frame and duplicate-choice rules. Frame binding and item retention do not ask for all choice-admission predicates. A single direct frame/item need is an invalid requirement for this bundled schema-and-admission unit.

Primary: PARTIAL_ONLY; independent: PARTIAL_ONLY.

Proposed minimal sets: []

### unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c — COLLECTIVELY_COVERABLE

Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes.

Envelope placement and context-only UTF-8/newline fidelity are distinct parts of the assembly accounting contract. N03 or N08 supplies the separate unchanged-task/Context envelope boundary; N04 supplies encoding, context-only byte reporting and exact newline fidelity. N07 alone supplies task preservation without the envelope structure. Thus the two listed pairs are the inclusion-minimal sufficient sets.

Primary: PARTIAL_ONLY; independent: PARTIAL_ONLY.

Proposed minimal sets: [['case-0011-context-utf8-ceiling/bytes/rendered-boundary', 'case-0011-context-utf8-ceiling/bytes/encoding'], ['case-0011-context-utf8-ceiling/bytes/encoding', 'case-0011-context-utf8-ceiling/request/prompt']]

### unit-eac315eb2a9f6a5634e094a5d4ef2960559030b62385b832a57f0f8d893b72de — COLLECTIVELY_COVERABLE

Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance.

Whole-resource frame/content rejection and the retained item's text/native provenance are separate integrity and representation facts. N09 supplies all admission and identity checks; N10 supplies unchanged content and native occurrence retention.

Primary: PARTIAL_ONLY; independent: PARTIAL_ONLY.

Proposed minimal sets: [['case-0011-context-utf8-ceiling/frame/binding', 'case-0011-context-utf8-ceiling/frame/items']]

### unit-f2f60cee7a81549ef3634c65a08ec026019e35505a0b7457ff348af70571ace3 — COLLECTIVELY_COVERABLE

Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation.

The item's immutable text/native provenance schema and the plan-to-item cardinality/identity binding are distinct representation and binding contracts. N10 supplies immutable ordered text/provenance retention; N09 supplies the complete identity fields and matching requirements.

Primary: COVERED; independent: PARTIAL_ONLY.

Proposed minimal sets: [['case-0011-context-utf8-ceiling/frame/binding', 'case-0011-context-utf8-ceiling/frame/items']]

## Collective need sets and minimality

Every proposed set has unique frozen members, partial facets, nonempty sufficiency and singleton-removal rationales, and no subset redundancy. This validates the semantic proof structure, not semantic truth; fresh reconciliation must confirm sufficiency and minimality.

### unit-1bb99811c2a45a9ce6d5dc32206e23d64f9fffa2d10fa642ca5f4ea6ce518c69

The qualified-reference plan adapter delegates to its validated materializer and renderer and retains both source/target addresses and content identities, the rendered text and native materialized value in the common item.

1 proposed minimal set(s); remains PARTIAL_ONLY under the strict direct rule.

Validated source/target identity handoff and the renderer/text/native-value handoff are distinct dimensions of the same adapter bridge. N09 supplies the former and N10 the latter; either alone omits the other.

Each listed set has two needs. The covered_part/missing_part records show that either singleton omits a distinct necessary facet. No other frozen need supplies the missing facet completely; supersets add no necessary evidence. These are all identified inclusion-minimal sufficient sets.

Set: ['case-0011-context-utf8-ceiling/frame/binding', 'case-0011-context-utf8-ceiling/frame/items']

case-0011-context-utf8-ceiling/frame/binding: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Necessary contribution: delegation to validated materialization and retention of source/target addresses and content identities

Missing from this member alone: the renderer-to-item text handoff and retention of the native materialized value

case-0011-context-utf8-ceiling/frame/items: What contracts retain item order, exact item text and native disclosure provenance?

Necessary contribution: renderer-to-item exact text and native materialized-value retention

Missing from this member alone: delegation through frame-validated materialization and both source/target address/content identity bindings

### unit-4b3c320635122396ffe052357de8b5f96f074e35017c0331a650de95844eaccd

Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed.

1 proposed minimal set(s); remains PARTIAL_ONLY under the strict direct rule.

Frame/identity validation including publication only after all items validate is distinct from realization order. N09 supplies admission and all-success integrity; N10 supplies selected-choice order. Neither alone establishes both.

Each listed set has two needs. The covered_part/missing_part records show that either singleton omits a distinct necessary facet. No other frozen need supplies the missing facet completely; supersets add no necessary evidence. These are all identified inclusion-minimal sufficient sets.

Set: ['case-0011-context-utf8-ceiling/frame/binding', 'case-0011-context-utf8-ceiling/frame/items']

case-0011-context-utf8-ceiling/frame/binding: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Necessary contribution: repository/snapshot rejection, returned identity/representation verification and withholding a disclosure until all items validate

Missing from this member alone: ordered realization of the selected choices

case-0011-context-utf8-ceiling/frame/items: What contracts retain item order, exact item text and native disclosure provenance?

Necessary contribution: realization of each selected option in order

Missing from this member alone: repository/snapshot rejection, returned identity/representation verification and all-success publication

### unit-5991a5afbd7d664372fc5b2357e8fbcacfa5d73d5560dcd97f853aa279e36b1c

The protected command runs tests only; the validation guide separately specifies uv Ruff lint/format, mypy and diff whitespace checks, including staged diff checking where applicable.

1 proposed minimal set(s); remains PARTIAL_ONLY under the strict direct rule.

The protected entry point's tests-only scope and the separately configured lint/format/type/whitespace workflow answer different validation questions. N17 supplies the scope and N18 the required separate tooling checks, including applicable staged checking.

Each listed set has two needs. The covered_part/missing_part records show that either singleton omits a distinct necessary facet. No other frozen need supplies the missing facet completely; supersets add no necessary evidence. These are all identified inclusion-minimal sufficient sets.

Set: ['case-0011-context-utf8-ceiling/validation/protected-entry', 'case-0011-context-utf8-ceiling/validation/configuration']

case-0011-context-utf8-ceiling/validation/protected-entry: What established entry point runs protected development validation?

Necessary contribution: the protected entry point running tests only

Missing from this member alone: separate uv Ruff lint/format, mypy and working/staged diff checks prescribed by the guide

case-0011-context-utf8-ceiling/validation/configuration: What established tooling configuration constrains test, type and style validation?

Necessary contribution: the separate lint/format/type and working/staged whitespace-check validation requirements

Missing from this member alone: the protected command's tests-only scope

### unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c

Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes.

2 proposed minimal set(s); remains PARTIAL_ONLY under the strict direct rule.

Envelope placement and context-only UTF-8/newline fidelity are distinct parts of the assembly accounting contract. N03 or N08 supplies the separate unchanged-task/Context envelope boundary; N04 supplies encoding, context-only byte reporting and exact newline fidelity. N07 alone supplies task preservation without the envelope structure. Thus the two listed pairs are the inclusion-minimal sufficient sets.

Each listed set has two needs. The covered_part/missing_part records show that either singleton omits a distinct necessary facet. No other frozen need supplies the missing facet completely; supersets add no necessary evidence. These are all identified inclusion-minimal sufficient sets.

Set: ['case-0011-context-utf8-ceiling/bytes/rendered-boundary', 'case-0011-context-utf8-ceiling/bytes/encoding']

case-0011-context-utf8-ceiling/bytes/rendered-boundary: What exact rendered Context text, headings and separators are appended during assembly?

Necessary contribution: separate task/Context envelope boundaries and unchanged appended payload text

Missing from this member alone: the context-only UTF-8 length report and preservation of each embedded string's newline bytes

case-0011-context-utf8-ceiling/bytes/encoding: What existing UTF-8 and newline handling contracts preserve exact rendered text?

Necessary contribution: context-only UTF-8 length accounting and unchanged embedded strings/newline bytes

Missing from this member alone: the separate outer task and Context envelope structure

Set: ['case-0011-context-utf8-ceiling/bytes/encoding', 'case-0011-context-utf8-ceiling/request/prompt']

case-0011-context-utf8-ceiling/bytes/encoding: What existing UTF-8 and newline handling contracts preserve exact rendered text?

Necessary contribution: context-only UTF-8 length accounting and unchanged embedded strings/newline bytes

Missing from this member alone: the separate outer task and Context envelope structure

case-0011-context-utf8-ceiling/request/prompt: How are the original task text and Prompt role preserved when Context is appended?

Necessary contribution: unchanged original task in its separate envelope alongside the Context envelope

Missing from this member alone: context-only UTF-8 length reporting and exact preservation of context.text and its newlines

### unit-eac315eb2a9f6a5634e094a5d4ef2960559030b62385b832a57f0f8d893b72de

Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance.

1 proposed minimal set(s); remains PARTIAL_ONLY under the strict direct rule.

Whole-resource frame/content rejection and the retained item's text/native provenance are separate integrity and representation facts. N09 supplies all admission and identity checks; N10 supplies unchanged content and native occurrence retention.

Each listed set has two needs. The covered_part/missing_part records show that either singleton omits a distinct necessary facet. No other frozen need supplies the missing facet completely; supersets add no necessary evidence. These are all identified inclusion-minimal sufficient sets.

Set: ['case-0011-context-utf8-ceiling/frame/binding', 'case-0011-context-utf8-ceiling/frame/items']

case-0011-context-utf8-ceiling/frame/binding: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Necessary contribution: foreign/stale frame, missing-resource and retained-occurrence rejection plus resource/content identity bindings

Missing from this member alone: unchanged item content and original-occurrence native provenance retention

case-0011-context-utf8-ceiling/frame/items: What contracts retain item order, exact item text and native disclosure provenance?

Necessary contribution: unchanged retained text and original-occurrence native provenance

Missing from this member alone: foreign/stale frame, missing-resource and unequal-occurrence rejection and resource/content identity bindings

### unit-f2f60cee7a81549ef3634c65a08ec026019e35505a0b7457ff348af70571ace3

Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation.

1 proposed minimal set(s); remains PARTIAL_ONLY under the strict direct rule.

The item's immutable text/native provenance schema and the plan-to-item cardinality/identity binding are distinct representation and binding contracts. N10 supplies immutable ordered text/provenance retention; N09 supplies the complete identity fields and matching requirements.

Each listed set has two needs. The covered_part/missing_part records show that either singleton omits a distinct necessary facet. No other frozen need supplies the missing facet completely; supersets add no necessary evidence. These are all identified inclusion-minimal sufficient sets.

Set: ['case-0011-context-utf8-ceiling/frame/binding', 'case-0011-context-utf8-ceiling/frame/items']

case-0011-context-utf8-ceiling/frame/binding: What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Necessary contribution: address/content/option/representation binding and one matching item per ordered plan choice

Missing from this member alone: the immutable item's exact text and native_provenance retention

case-0011-context-utf8-ceiling/frame/items: What contracts retain item order, exact item text and native disclosure provenance?

Necessary contribution: immutable exact-text/native-provenance retention and one item per ordered choice

Missing from this member alone: the complete address/content/option/representation identity schema and matching requirements

## Strict and granularity-aware coverage

Strict primary: 13/32; strict independent: 20/32. Secondary independent GRANULARITY_AWARE_COVERED: 26/32 (20 direct plus six collective). Six still lack complete coverage: three overcompound propositions and three atomic partial-only units. The strict every-unit failure holds in both reviews; neither identifies the same exact failed set. Alternatives: six fully direct, two complete only collectively, four incomplete, zero ambiguous. Four alternatives are strictly incomplete in both but also remain incomplete in the independent diagnostic; two further alternatives are strictly incomplete in both and become diagnostic complete only collectively.

Remaining diagnostic units:

- unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2: Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values.
- unit-1466ea6b2b7b8cdc077c41ad15c6baf8087b6e7a230723f83b9911815a09a10c: The protected command is the documented protected development entry point; it excludes the experiment test tree before collection, retains project pytest configuration and branch coverage with the 100 percent gate, returns pytest's exit code, and does not authorize excluded confirmation validation.
- unit-183296beacda118e38a058b6d2588e582fd74639627706768ea3eb9396cc4580: The planning overview describes exact materialization, native provenance, appended copied-request Context and both supported choices, and distinguishes future token budgets/universal costs from current behavior.
- unit-5e58e7852d6acb8027c97bf0d6ccc3deede219f1c229e52225d0b31b7ed29af6: Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices.
- unit-87f78f68bcbaca8cbda3d9fc4b8f1daee88e66a1ed350ec6441d5861cbb400fc: Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference.
- unit-fddd6c59fb1d485b6e4a6a749f66062c76ddd58df987a692ae75827e2f9b8329: The common mixed-plan test uses CRLF and non-ASCII qualified/whole-resource fixtures and checks unchanged retained source, native whole-resource provenance and rendered item order.

## Exact current failure-cause assessment

### INFORMATION_NEED_COVERAGE_FAILURE: ESTABLISHED

Both reviewers fail the frozen every-unit direct rule; exact failed membership is disputed. This is not a retrieval or effectiveness result.

Exact supporting metrics: {"primary_missing_direct": 19, "review_missing_direct": 12}

### UNDER_SPECIFIED_INFORMATION_NEEDS: POSSIBLE

The three overcompound propositions identify purpose, admission and execution facets absent from the questions, but neither reviewer classifies a need MISFORMULATED or AMBIGUOUS. Broader intent versus unit bundling remains unresolved.

Exact supporting metrics: {"primary_misformulated_or_ambiguous": 0, "review_misformulated_or_ambiguous": 0}

### UNDER_DECOMPOSED_NEED_SET: SUPPORTED

Three units have unrequested admission/execution facets and three other atomic units remain partial-only. Missing focused questions are plausible, but no need-set repair or attribution is selected.

Exact supporting metrics: {"review_atomic_partial_only": 3, "review_overcompound": 3}

### NEED_TO_UNIT_GRANULARITY_MISMATCH: SUPPORTED

Independent diagnostic proposes six collectively coverable and three overcompound units. Collective proofs are structurally validated semantic claims awaiting confirmation, not reviewed truth.

Exact supporting metrics: {"collective_units": 6, "diagnostic_review_covered": 26, "minimal_sets": 7, "strict_review_covered": 20}

### C5_SEMANTIC_ADJUDICATION_INSTABILITY: ESTABLISHED

Observed disagreements affect direct facts, required-unit coverage, need necessity and whole alternatives; class imbalance cannot make this architecture-safe.

Exact supporting metrics: {"direct_intersection": 12, "direct_union": 22, "need_disagreements": 7, "pair_disagreements": 32, "unit_disagreements": 11}

## Reliability conclusion and Stage D boundary

Only 12 of 22 distinct direct mappings are shared; 11 unit statuses and 7 need classifications change, and six alternatives change strict completeness. Several changes affect ownership, dependencies, exports, frame integrity and necessity. This joint pattern, not one arbitrary cutoff, requires reconciliation.

Neither primary C.5 alone nor independent C.5-R alone is safe for Stage D. Reconciliation is required. Strict direct-rule failure is robust as a Boolean, not as an exact missing-unit attribution. The exact cause remains disputed. Stage D has not occurred and remains BLOCKED. This checkpoint cannot conclude retrieval success, treatment effects, acquisition effectiveness, information-need authoring defect, a final frozen U1 outcome, or confirmation. The prepared packet authorizes only a future fresh semantic reconciliation session; this task performs none.
