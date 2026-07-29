from __future__ import annotations

from pathlib import Path

from .engine import CoreEngine


def initialize(config_path: str | Path | None = None) -> CoreEngine:
    """Initialize a CoreEngine instance with optional configuration."""
    return CoreEngine(config_path=config_path)


def start_engine(config_path: str | Path | None = None) -> CoreEngine:
    """Initialize and start a CoreEngine instance."""
    engine = initialize(config_path=config_path)
    engine.start()
    return engine


run = start_engine
