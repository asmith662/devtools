# Copyright (c) 2026
"""Trusted host entry; scientific model CWD never imports the checkout."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from experiments.source_grounding.chunked.lifecycle import main

if __name__ == "__main__":
    main()
