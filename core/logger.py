from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class AppLogger:
    """Centralized application logger with console and optional file output."""

    def __init__(self, name: str = "thif_core", log_file: str | Path | None = None, level: int | str = logging.INFO) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self._resolve_level(level))
        self.logger.propagate = False

        if self.logger.handlers:
            return

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        if log_file is not None:
            path = Path(log_file)
            path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = RotatingFileHandler(path, maxBytes=2 * 1024 * 1024, backupCount=5)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    @staticmethod
    def _resolve_level(level: int | str) -> int:
        if isinstance(level, int):
            return level
        return logging.getLevelName(level)

    def get_logger(self) -> logging.Logger:
        """Return the constructed logger instance."""
        return self.logger


def get_logger(name: str = "thif_core", log_file: str | Path | None = None, level: int | str = logging.INFO) -> logging.Logger:
    """Create or return a named logger configured for the application."""
    return AppLogger(name=name, log_file=log_file, level=level).get_logger()
