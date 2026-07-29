from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.logger import get_logger
from core.module_manager import BaseModule
from .manager import VoiceManager
from .sounds import SoundLibrary
from .tts import TTS

if TYPE_CHECKING:
    from core.engine import CoreEngine


class VoiceModule(BaseModule):
    """Voice module implementation for THIF CORE."""

    def __init__(self) -> None:
        super().__init__(name="voice", description="Voice output module")
        self.logger = get_logger(name="thif_core.voice")
        self.manager = VoiceManager(logger=self.logger)
        self.tts = TTS(logger=self.logger)
        self.sounds = SoundLibrary(logger=self.logger)

    def start(self, engine: CoreEngine | None = None) -> None:
        self.logger.info("Starting voice module")
        self.manager.initialize(engine=engine)

    def stop(self) -> None:
        self.logger.info("Stopping voice module")
        self.manager.shutdown()
