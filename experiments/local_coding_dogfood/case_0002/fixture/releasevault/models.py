"""Repository-independent catalog data."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Artifact:
    project: str
    platform: str
    version: str
    uri: str
    enabled: bool = True

    def __post_init__(self):
        if not self.project or not self.platform or not self.uri:
            raise ValueError("artifact identity fields must be present")
