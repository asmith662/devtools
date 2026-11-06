# Copyright (c) 2026
from devtools.learning.integrations.local._codec import array as _array
from devtools.learning.integrations.local._codec import nonempty_text as _text
from devtools.learning.integrations.local._codec import retained_object as _object
from devtools.learning.representation.features import FeatureTable, FeatureValueKind


def _real(value: object) -> float:
    """Retain the original binary64 decoding boundary without ANOVA fitting."""
    if type(value) is not float:
        msg = "original binary64 selector values required"
        raise ValueError(msg)
    return value


def _table(value: object) -> FeatureTable:
    d = _object(value)
    return FeatureTable(
        tuple(_text(v) for v in _array(d["feature_names"])),
        tuple(tuple(_real(v) for v in _array(row)) for row in _array(d["rows"])),
        tuple(FeatureValueKind(_text(v)) for v in _array(d["feature_value_kinds"])),
    )
