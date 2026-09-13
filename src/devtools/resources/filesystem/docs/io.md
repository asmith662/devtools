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
`file_format` passed to `read()` bypasses suffix inference. Binary has no
codec-backed suffix support.

## Reading

```python
read(path, *, file_format=None, max_bytes=16 * 1024 * 1024)
```

`read()` requires a `ResolvedPath` to an existing regular file. It checks the
reported size before a complete `read_bytes()`, checks the loaded size again,
resolves the codec, and returns the rich concrete model. `max_bytes=None`
disables the limit; negative values raise `ValueError`. Permission failures
normalize to `FilesystemPermissionError`.

The default is 16 MiB. Its bound is intentionally not race-free:

```text
stat → pre-read check → read_bytes() → post-read check
```

A growing file is rejected after the second check and no oversized model is
returned, but its grown contents can be allocated before rejection. Streaming
bounded reads are not implemented.

## Writing

```python
write(file, *, overwrite=True)
```

The model's `format`, not the target suffix, selects its codec. Explicit model
and codec matching prevents JSON, Markdown, and CSV TextFile subclasses from
being encoded by TextCodec. Missing parent directories are not created.
`overwrite=False` raises built-in `FileExistsError` when the destination exists.

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
