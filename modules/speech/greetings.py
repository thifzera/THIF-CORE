from __future__ import annotations

import logging
from datetime import datetime


class Greetings:
    """Generate greeting phrases based on the current time."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("thif_core.speech.greetings")

    def get_greeting(self, timestamp: datetime) -> str:
        """Return an appropriate greeting for the provided time."""
        hour = timestamp.hour
        if hour < 12:
            greeting = "Bom dia"
        elif hour < 18:
            greeting = "Boa tarde"
        else:
            greeting = "Boa noite"

        self.logger.info("Generated greeting: %s", greeting)
        return greeting
