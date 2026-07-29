from __future__ import annotations

import logging
from datetime import datetime


class SpeechFormatter:
    """Format dates, times and temperature comments into spoken text."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("thif_core.speech.formatter")

    def format_time(self, timestamp: datetime) -> str:
        """Return the time expressed in natural language."""
        formatted = timestamp.strftime("%H:%M")
        self.logger.info("Formatting time for speech: %s", formatted)
        return formatted

    def format_date(self, timestamp: datetime) -> str:
        """Return the date expressed in natural language."""
        formatted = timestamp.strftime("%d/%m/%Y")
        self.logger.info("Formatting date for speech: %s", formatted)
        return formatted

    def format_temperature_comment(self, temperature: float) -> str:
        """Return a temperature commentary for speech."""
        if temperature <= 0:
            comment = "Está muito frio." 
        elif temperature < 15:
            comment = "Está fresco." 
        elif temperature < 25:
            comment = "Está agradável." 
        else:
            comment = "Está quente." 
        self.logger.info("Formatting temperature comment: %s", comment)
        return comment
