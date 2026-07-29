from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.engine import CoreEngine


class VoiceManager:
    """Manage voice system resources and playback orchestration."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("thif_core.voice")
        self.active = False

    def initialize(self, engine: CoreEngine | None = None) -> None:
        self.logger.info("Initializing voice manager")
        self.active = True

    def shutdown(self) -> None:
        self.logger.info("Shutting down voice manager")
        self.active = False
