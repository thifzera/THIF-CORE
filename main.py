from __future__ import annotations

import argparse
from pathlib import Path

from core.startup import initialize


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(description="THIF CORE")
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parent / "config" / "config.json")
    return parser


def main() -> int:
    """Initialize and run the THIF CORE application."""
    parser = build_parser()
    args = parser.parse_args()

    engine = initialize(config_path=args.config)
    engine.start()
    engine.logger.info("%s started", engine.config_manager.get("application"))
    engine.logger.info("Pressione Ctrl+C para parar.")

    try:
        engine.run()
    except KeyboardInterrupt:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

