"""Create database tables.

Usage:
    python -m scripts.init_db
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps/api/src"))

from idxwitcher_api.db.base import Base
from idxwitcher_api.db.session import engine
import idxwitcher_api.db.models  # noqa: F401


def main():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    main()
