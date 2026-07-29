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
        super().__init__(
            name="voice",
            version="1.0.0",
            description="Voice output module",
            author="THIF CORE",
            dependencies=[],
        )
        self.logger = get_logger(name="thif_core.voice")
        self.manager = VoiceManager(logger=self.logger)
        self.tts = TTS(logger=self.logger)
        self.sounds = SoundLibrary(logger=self.logger)

    def initialize(self, engine: CoreEngine | None = None) -> None:
        self.logger.info("Starting voice module")
        self.manager.initialize(engine=engine)
        self.sounds.play("startup")
        if engine is not None and hasattr(engine, "module_manager"):
            speech_module = engine.module_manager.get_module("speech")
            if speech_module is not None and hasattr(speech_module, "build_sequence"):
                self.tts.speak(speech_module.build_sequence(engine))

    def shutdown(self) -> None:
        self.logger.info("Stopping voice module")
        self.manager.shutdown()
