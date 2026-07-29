from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from core.logger import get_logger
from core.module_manager import BaseModule
from .formatter import SpeechFormatter
from .greetings import Greetings

if TYPE_CHECKING:
    from core.engine import CoreEngine


class SpeechModule(BaseModule):
    """Natural speech module implementation for THIF CORE."""

    def __init__(self) -> None:
        super().__init__(name="speech", description="Natural speech module")
        self.logger = get_logger(name="thif_core.speech")
        self.formatter = SpeechFormatter(logger=self.logger)
        self.greetings = Greetings(logger=self.logger)

    def start(self, engine: CoreEngine | None = None) -> None:
        self.logger.info("Starting speech module...")
        now = datetime.now()
        greeting = self.greetings.get_greeting(now)
        time_text = self.formatter.format_time(now)
        date_text = self.formatter.format_date(now)
        temp_comment = self.formatter.format_temperature_comment(22.0)

        self.logger.info("Speech module loaded.")
        self.logger.info("Greeting: %s", greeting)
        self.logger.info("Time: %s", time_text)
        self.logger.info("Date: %s", date_text)
        self.logger.info("Temperature comment: %s", temp_comment)

    def stop(self) -> None:
        self.logger.info("Stopping speech module")
