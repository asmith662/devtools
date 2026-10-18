# Copyright (c) 2026
"""Host-owned independent checks for the second coding task, not model Context."""

ACCEPTANCE = r"""import ast
from devtools.context import PythonSourceRange
from devtools.context.python.function.materialization import _extract_source_segment

checks = 0
for separator in ("\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"):
    for newline in ("\n", "\r\n", "\r"):
        for prefix in ("", "async "):
            source = ("# prefix " + separator + " text" + newline + prefix
                      + "def sample():" + newline + '    return "caf\u00e9'
                      + separator + 'tail"' + newline)
            node = ast.parse(source).body[0]
            span = PythonSourceRange(node.lineno, node.col_offset,
                                     node.end_lineno, node.end_col_offset)
            expected = ast.get_source_segment(source, node)
            try:
                actual = _extract_source_segment(source, span)
            except Exception as error:
                raise AssertionError("Valid AST source could not be materialized: "
                                     + repr((separator, newline, prefix))) from error
            assert actual == expected, (separator, newline, prefix, actual, expected)
            checks += 1
assert checks == 48
print("PASS: 48 exact AST segment checks, Unicode separators, LF/CRLF/CR, sync/async")
"""
