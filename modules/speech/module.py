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
        super().__init__(
            name="speech",
            version="1.0.0",
            description="Natural speech module",
            author="THIF CORE",
            dependencies=[],
        )
        self.logger = get_logger(name="thif_core.speech")
        self.formatter = SpeechFormatter(logger=self.logger)
        self.greetings = Greetings(logger=self.logger)

    def build_sequence(self, engine: CoreEngine | None = None) -> str:
        """Build one natural spoken sequence for the startup flow."""
        now = datetime.now()
        greeting = self.greetings.get_greeting(now)
        time_text = self.formatter.format_time(now)
        date_text = self.formatter.format_date(now)
        temp_comment = self.formatter.format_temperature_comment(22.0)

        config = engine.config_manager if engine is not None else None
        name = config.get("name", "THIF") if config is not None else "THIF"
        city = config.get("city", "São Paulo") if config is not None else "São Paulo"
        voice = config.get("voice", "teste") if config is not None else "teste"
        speed = config.get("speed", "normal") if config is not None else "normal"

        parts = [
            f"{greeting}, eu sou {name}.",
            f"Hoje é {date_text}.",
            f"Agora são {time_text}.",
            f"A cidade configurada é {city}.",
            f"A voz selecionada é {voice} e a velocidade é {speed}.",
            f"{temp_comment}",
            "Estou pronto para iniciar o núcleo.",
            "Até logo.",
        ]
        return " ".join(parts)

    def initialize(self, engine: CoreEngine | None = None) -> None:
        self.logger.info("Starting speech module...")
        sequence = self.build_sequence(engine)
        self.logger.info("Speech module loaded.")
        self.logger.info("Speech sequence: %s", sequence)

    def shutdown(self) -> None:
        self.logger.info("Stopping speech module")
