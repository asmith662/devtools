# CSV models and codec

CSV is header-based and string-valued. It consists of `CsvQuoting`,
`CsvDialect`, `CsvRow`, `CsvFile`, and `CsvCodec`.

## Dialect and quoting

`CsvQuoting` exposes stable policies: `MINIMAL`, `ALL`, `NONNUMERIC`, and
`NONE`. `NONNUMERIC` is a CSV quoting policy; it does not coerce cells into
numeric Python values.

`CsvDialect` is immutable and defaults to comma delimiter, double quote marker,
no escape character, doubled-quote escaping, no initial-space skipping, `"\n"`
line termination, and minimal quoting. Delimiter and quote characters must be
one character; escape character is optional but one character when supplied;
the line terminator cannot be empty. Standard-library CSV behavior governs
additional invalid combinations. Dialect sniffing is not implemented.

## Rows and files

`CsvRow` stores immutable header and cell tuples. It supports positional,
negative, slice, and header-name indexing; iteration yields cell values.
Importantly, `"name" in row` tests header membership, not whether a cell has
that value. `get`, `keys`, `values`, `items`, `as_dict`, and `convert` are
available.

`CsvFile` stores immutable `headers`, `rows`, and `dialect`; it supports row
sequence access, `column()`, `find()`, `find_all()`, `find_by()`, immutable
row transformations, and `convert_rows()`. Inserted or replaced rows must have
exactly matching headers.

## Parsing and provenance

An empty source is invalid. A nonempty unique, nonblank header is required;
header-only CSV is valid. Empty cells are valid strings, but blank records and
malformed row widths are invalid. No numeric or date coercion occurs.

`.content` is original decoded source provenance. `.headers` and `.rows` are
current state. Transformations preserve `.content`; CsvCodec serializes current
headers and rows.

## Codec

`CsvCodec` uses standard-library `csv.reader` and `csv.writer` with
`StringIO(newline="")`, applies the file dialect, supports quoted delimiters and
embedded newlines, and performs encoding normalization. It does not read or
write disk directly and does not provide typed cell conversion.
