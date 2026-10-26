# Filesystem I/O

## Format resolution

`resolve_file_format(path)` resolves the final suffix case-insensitively:

| Suffix | Format |
|---|---|
| `.csv` | CSV |
| `.json` | JSON |
| `.md`, `.markdown` | Markdown |
| `.txt` | Text |

Unsupported or unimplemented formats raise `FileFormatError`. An explicit
`file_format` passed to `read()` bypasses suffix inference. Binary is explicit
only: `read(path, file_format=FileFormat.BINARY)` preserves arbitrary bytes under
the same byte limits. Neither `.bin` nor an unknown suffix implies binary.

## Reading

```python
read(path, *, file_format=None, max_bytes=16 * 1024 * 1024)
```

`read()` requires a `ResolvedPath` to an existing regular file. It checks the
reported size before reading, checks the retained size again,
resolves the codec, and returns the rich concrete model. `max_bytes=None`
disables the limit; negative values raise `ValueError`. Permission failures
normalize to `FilesystemPermissionError`.

The default is 16 MiB. Finite reads consume at most `max_bytes + 1` bytes,
including when a source grows after stat. Short reads are accumulated until EOF
or that sentinel bound; an oversized prefix is rejected before codec decoding.
Streams close on success or failure. Retained buffers and copies are bounded in
proportion to the limit; this is not an exact total-process memory allocation cap.

```text
stat -> pre-read check -> bounded stream read -> post-read check -> decode
```

`max_bytes=None` still permits complete unbounded content. Permission failures
at open/read retain domain normalization. The Qwen-authored bounded reader and
independent stream/Repository-observation regressions, originally feature-published
in `61637ff8`, are integrated on main. The original engineering evidence retains
its historical execution and acceptance qualifications.

## Writing

```python
write(file, *, overwrite=True)
```

The model's `format`, not the target suffix, selects its codec. `BinaryFile`
uses `BinaryCodec` and the same overwrite/atomic-replacement policy. Explicit model
and codec matching prevents JSON, Markdown, and CSV TextFile subclasses from
being encoded by TextCodec. Missing parent directories are not created.
`overwrite=False` raises built-in `FileExistsError` when a destination directory
entry exists, including a dangling symbolic link. Inspection uses `lstat`, so
refusal preserves the original link independently of referent existence. Permission
failures normalize to `FilesystemPermissionError`; other inspection errors
propagate rather than being interpreted as safe absence. A genuinely missing
entry remains writable. `overwrite=True` retains atomic replacement semantics.
This admission check is not atomic concurrent create-if-absent: external writers
can still race it, and higher-level ownership remains necessary.

The normal write lifecycle is:

```text
encode current model state
    ↓
create sibling temporary file
    ↓
record its path for cleanup
    ↓
write, flush, fsync
    ↓
os.replace(destination)
    ↓
remove temporary file on failure
```

Under normal local atomic-replace filesystem semantics, observers should see
either the previous destination or the complete replacement, rather than a
partially written destination. The temporary file is in the target directory,
so replacement stays on that filesystem.

This is not a full crash transaction: the parent directory is not fsynced,
directory-entry durability after sudden power loss is filesystem-dependent, and
there is no locking or concurrent-writer coordination.

## Security boundaries

I/O does not guarantee allowed-root containment, symlink-escape prevention,
path authorization, TOCTOU elimination, ownership/permission policy, locking,
or secure deletion. Those concerns are outside this package.
