# Filesystem codecs

Codecs convert representations and models; they do not access disk. Generic
disk I/O is owned by [`read()` and `write()`](io.md).

## Current codecs

`TextCodec`, `JsonCodec`, `MarkdownCodec`, and `CsvCodec` support bytes/text
conversion for their corresponding models. There is no BinaryCodec.

- TextCodec performs `bytes <-> decoded text` without structural parsing.
- JsonCodec provides `decode`, `parse`, `serialize`, and `encode`.
- MarkdownCodec encodes and decodes authoritative Markdown `.content`.
- CsvCodec provides `decode`, `parse`, `serialize`, and `encode` for headers,
  rows, and dialects.

Decode failures and unknown encodings normalize to `TextDecodingError`; output
encoding failures normalize to `TextEncodingError`. Format parsing and
serialization failures use `FileFormatError` where appropriate.

## Architecture

Codec resolution is a static internal format-to-codec-class map. No common
codec base class or Protocol exists because the four concrete codecs remain
small and their signatures differ meaningfully. There is no registry or plugin
discovery.

JSON and CSV serialization uses current structured state, not source
provenance. Markdown and text encoding preserve their `.content` source.

See [json.md](json.md), [markdown.md](markdown.md), and [csv.md](csv.md) for
the format details.
