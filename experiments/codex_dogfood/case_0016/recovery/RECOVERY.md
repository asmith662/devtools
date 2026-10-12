# Case 0016 capture-only recovery

Attempt 1 = FAILED_AUDIT_ONLY. Attempt 2 has not started. No successful Stage B, packet, gold or effectiveness claim.

The established cause is permission denial replacing derived raw_checkpoint.json after durable RETURNED at operation 166. A contemporaneous PowerShell reader is a plausible contributor only. No sleeps, write retries, process termination or scientific changes are introduced.

The sealed Case 0012 immutable journal/event/native-memo schema is reused unchanged. A capture-only subclass disables its mutable save hook. No raw checkpoint or equivalent mutable latest file is written during active execution. Final checkpoint bytes are derived from immutable records once at publication. Unique append-only timestamped progress is non-authoritative; publication warnings cannot veto a durable scientific RETURNED and cannot rerun it.

Durable ENTERED -> invoke once -> durable RETURNED completes the operation. Native exceptions retain FAILED_NO_RETURN and stop. Failure to durably publish authoritative RETURNED stops without retry. Final success requires the complete journal, completion seal and deterministic scientific validation.

Attempt 2 starts at operation 1 with independent native returns. No attempt-1 object enters treatment inputs. The 464 operation identities and scientific invocation AST are identical, as are all 193 Stage-A-sealed files. No production source, owner boundary, query/edge/seed/PPR/flow/RRF/map/gold/gate semantics change.

Unexecuted Stage C code is allowlisted, deterministic and tested; it projects only Stage A task/obligations/resource bytes after a successful committed/pushed attempt 2. No packet or sterile workspace exists at this checkpoint.
