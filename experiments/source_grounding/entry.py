# Copyright (c) 2026

"""Load pinned experiment code without adding the checkout to worker environment."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from experiments.source_grounding.workers import main

if __name__ == "__main__":
    main()
