import sys
from pathlib import Path

# Add repo root (kitchen/) to Python's import path so tests can import: backend.app...
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
