from __future__ import annotations

import logging


class SoundLibrary:
    """Manage sound playback resources for the voice module."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("thif_core.voice.sounds")

    def play(self, sound_name: str) -> None:
        """Log a sound playback request."""
        self.logger.info("Playing sound: %s", sound_name)
