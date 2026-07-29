from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.logger import get_logger
from core.module_manager import BaseModule
from .provider import WeatherProvider
from .translator import WeatherTranslator

if TYPE_CHECKING:
    from core.engine import CoreEngine


class WeatherModule(BaseModule):
    """Weather module implementation for THIF CORE."""

    def __init__(self) -> None:
        super().__init__(
            name="weather",
            version="1.0.0",
            description="Weather information module",
            author="THIF CORE",
            dependencies=[],
        )
        self.logger = get_logger(name="thif_core.weather")
        self.provider = WeatherProvider(logger=self.logger)
        self.translator = WeatherTranslator(logger=self.logger)

    def initialize(self, engine: CoreEngine | None = None) -> None:
        self.logger.info("Starting weather module")
        try:
            weather = self.provider.fetch("default")
            translated_condition = self.translator.translate(str(weather.get("condition", "unknown")))
            temperature = weather.get("temperature", 0.0)
            self.logger.info("Weather: %s, temperature: %s°C", translated_condition, temperature)
        except Exception as error:
            self.logger.error("Weather module failed to start: %s", error)

    def shutdown(self) -> None:
        self.logger.info("Stopping weather module")
