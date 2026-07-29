from __future__ import annotations

import logging
from random import choice


class WeatherProvider:
    """Provide weather condition data from a simulated source."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("thif_core.weather.provider")

    def fetch(self, location: str) -> dict[str, str | float]:
        """Fetch weather data for the requested location."""
        self.logger.info("Fetching weather for location: %s", location)
        conditions = [
            {"condition": "clear", "temperature": 26.0},
            {"condition": "rain", "temperature": 18.5},
            {"condition": "cloudy", "temperature": 22.0},
            {"condition": "snow", "temperature": -2.0},
        ]
        return choice(conditions)
