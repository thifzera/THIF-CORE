from __future__ import annotations

import logging


class WeatherTranslator:
    """Translate raw weather condition codes into human-friendly text."""

    TRANSLATIONS: dict[str, str] = {
        "clear": "limpo",
        "rain": "chuva",
        "cloudy": "nublado",
        "snow": "neve",
    }

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("thif_core.weather.translator")

    def translate(self, condition_code: str) -> str:
        """Translate a weather condition code into a localized phrase."""
        translation = self.TRANSLATIONS.get(condition_code, condition_code)
        self.logger.info("Translating weather condition '%s' -> '%s'", condition_code, translation)
        return translation
