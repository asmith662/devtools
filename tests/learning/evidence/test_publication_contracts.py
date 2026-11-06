# Copyright (c) 2026
"""Publication identities are independent of authored file or execution claims."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, cast
from uuid import UUID, uuid4, uuid5

import pytest

from devtools.core.time import Timestamp
from devtools.learning.evidence.publication import (
    ArtifactRecord,
    PublicationManifest,
    generation_name,
)


@pytest.mark.parametrize("time", [None, "UTC"])
def test_generation_requires_actual_utc_timestamp(time: object) -> None:
    """A display claim is not a timestamp."""
    with pytest.raises(ValueError, match="timezone-aware UTC"):
        generation_name(cast("Any", time), uuid4())


def test_generation_and_artifact_require_uuid_identities() -> None:
    """Strings cannot silently become nominal artifact or generation identities."""
    with pytest.raises(TypeError, match="publication identity"):
        generation_name(Timestamp.now().value, cast("UUID", "id"))
    with pytest.raises(TypeError, match="artifact identity"):
        ArtifactRecord(cast("UUID", "id"), "a.json", "a.json", 0, "0" * 64)


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("publication_id", "foreign", TypeError),
        ("producing_execution_id", "foreign", TypeError),
        ("publication_execution_id", "foreign", TypeError),
        ("artifacts", ("invented",), TypeError),
    ],
)
def test_manifest_refuses_wrong_identity_and_member_types(
    field: str,
    value: object,
    error: type[Exception],
) -> None:
    """Pure constructor controls do not claim actual scientific publication."""
    manifest = _manifest()
    with pytest.raises(error):
        replace(manifest, **{field: cast("Any", value)})


@pytest.mark.parametrize("field", ["publication_id", "publication_execution_id"])
def test_manifest_separates_publication_from_producing_occurrence(field: str) -> None:
    """The same nominal occurrence cannot supply distinct custody roles."""
    manifest = _manifest()
    with pytest.raises(ValueError, match="distinct"):
        replace(manifest, **{field: cast("Any", manifest.producing_execution_id)})


def _manifest() -> PublicationManifest:
    identity, producer = uuid4(), uuid4()
    time = Timestamp.now().value
    return PublicationManifest(
        identity,
        producer,
        generation_name(time, identity),
        time,
        ("a.json",),
        (ArtifactRecord(uuid5(identity, "a.json"), "a.json", "a.json", 0, "0" * 64),),
    )
