from __future__ import annotations

import logging


class TTS:
    """Text-to-speech helper for voice output."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("thif_core.voice.tts")

    def speak(self, text: str) -> None:
        """Log the requested text-to-speech output."""
        self.logger.info("TTS speak called with text: %s", text)
