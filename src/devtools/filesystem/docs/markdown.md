# Markdown models and codec

`MarkdownFile` is an immutable TextFile with derived `headings` and `sections`.
`MarkdownHeading` and `MarkdownSection` are frozen structural values. Markdown
is a narrow structural helper, not a CommonMark AST.

## Headings and fences

Only ATX headings are recognized. Levels are 1 through 6, opening markers
require whitespace before heading text, and empty heading text is accepted.
Heading lines are one-based. Closing hash markers are normalized by the current
ATX pattern. Setext headings are unsupported.

Headings within recognized fenced code are ignored. Fences use backticks or
tildes, permit up to three leading spaces, and close only with the same
character at least as long as the opening fence. The current parser accepts
trailing text after a closing fence prefix and does not claim complete
CommonMark fence compliance.

## Sections and lookup

A section starts at its owning heading and ends immediately before the next
heading of the same or higher level. Lower-level headings remain in the parent
section. Boundaries use one-based inclusive lines.

`MarkdownSection.content` excludes the heading line and is normalized logical
source: `splitlines()` plus `"\n"` joining means CRLF becomes logical newline
text and final-newline/exact source-slice fidelity is not retained.
`find_heading()` and `find_section()` return the first matching structure and
are case-insensitive by default.

## Codec and inherited text behavior

`MarkdownCodec` only decodes and encodes `.content`. Headings and sections are
always derived and are never serialized independently. Markdown inherits
literal contains, logical lines, and source regex operations from TextFile.
There is no structural Markdown rewriting, Setext support, or full CommonMark
parsing.
