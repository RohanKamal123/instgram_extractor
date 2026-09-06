"""Entry-point for ``reel-archivist`` CLI (currently boots the status UI)."""
from __future__ import annotations

import argparse
import sys

import uvicorn

from .config import Settings


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="reel-archivist",
        description="Personal AI archivist for Instagram Reels (Phase 0 skeleton)",
    )
    parser.add_argument(
        "--ui-only",
        action="store_true",
        help="Start the interactive status UI without processing workers.",
    )
    parser.add_argument(
        "--create-db",
        action="store_true",
        help="Create or migrate the local SQLite database schema, then exit.",
    )
    args = parser.parse_args()

    settings = Settings()
    settings.ensure_directories()

    from .db.connection import init_database

    init_database(settings)

    if args.create_db:
        print(f"[ok] Database initialized at {settings.database_path_abs}")
        return 0

    print(
        f"[reel-archivist] Starting status UI on http://{settings.UI_HOST}:{settings.UI_PORT}"
    )
    print(
        "[reel-archivist] Press Ctrl+C to stop. Phase 0: infrastructure skeleton only."
    )

    from .ui.app import create_app

    app = create_app(settings)
    uvicorn.run(
        app,
        host=settings.UI_HOST,
        port=settings.UI_PORT,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=False,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
