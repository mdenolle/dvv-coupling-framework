"""Shared pytest configuration.

Ensures the repository root is importable so ``import analysis`` works, and
forces a non-interactive matplotlib backend for headless test runs.
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
