# Copyright (c) 2026
"""Trusted host entry, never disclosed to the semantic model."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from experiments.source_grounding.discrimination.lifecycle import main

if __name__ == "__main__":
    main()
