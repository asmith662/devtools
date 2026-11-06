# Copyright (c) 2026
"""Closed retained-state codecs reject added or silently coerced scientific meaning."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.learning.classification.linear import FittedBinaryLinearClassifier
from devtools.learning.classification.margin import FittedMarginClassifier
from devtools.learning.integrations.local.linear_classification import (
    decode_model,
    model_document,
)
from devtools.learning.integrations.local.margin_classification import (
    decode_margin,
    margin_document,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.learning.classification.test_states import Witness


@pytest.mark.parametrize("method", ["square-logistic", "square-margin"])
@pytest.mark.parametrize(
    "fault",
    ["schema", "real", "pair", "categories", "digest"],
)
def test_retained_native_state_rejects_type_and_correspondence_faults(
    fitted: Callable[[str], Witness],
    method: str,
    fault: str,
) -> None:
    """Modify copies of genuine native fitted states; no native retry is involved."""
    state, _ = fitted(method)
    decode: Callable[[bytes], FittedBinaryLinearClassifier | FittedMarginClassifier]
    if isinstance(state, FittedBinaryLinearClassifier):
        data = model_document(state)
        decode = decode_model
    else:
        assert isinstance(state, FittedMarginClassifier)
        data = margin_document(state)
        decode = decode_margin
    values = cast("dict[str, Any]", data["state"])
    if fault == "schema":
        data["schema"] = "unknown"
    elif fault == "real":
        values["intercept"] = 0
    elif fault == "pair":
        values["configuration"] = [["missing-value"]]
    elif fault == "categories":
        values["categories"] = [0.0, 1.0]
    else:
        data["content_sha256"] = "0" * 64
    with pytest.raises(ValueError, match=r"codec|binary64|key/value|category|content"):
        decode(json.dumps(data).encode())
