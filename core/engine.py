from __future__ import annotations

from pathlib import Path

from .config import ConfigManager
from .events import EventBus
from .logger import get_logger
from .module_manager import ModuleManager
from modules.voice.module import VoiceModule


class CoreEngine:
    """Main runtime orchestrator for THIF CORE."""

    def __init__(self, config_path: str | Path | None = None) -> None:
        self.config_manager = ConfigManager(config_path=config_path)
        self.logger = get_logger(
            name="thif_core",
            log_file=self.config_manager.get("logging.file"),
            level=self.config_manager.get("logging.level", "INFO"),
        )
        self.event_bus = EventBus()
        self.module_manager = ModuleManager()
        self._register_default_modules()
        self.is_running = False

    def _register_default_modules(self) -> None:
        """Register built-in modules for the engine."""
        voice_module = VoiceModule()
        self.module_manager.register_module(voice_module)
        self.module_manager.enable_module(voice_module.name)

    def start(self) -> None:
        """Start the engine and all enabled modules."""
        if self.is_running:
            return

        self.logger.info("Starting THIF CORE engine")
        self.is_running = True
        self.event_bus.publish("engine.started", {"engine": self})
        self.module_manager.start_all(engine=self)

    def stop(self) -> None:
        """Stop the engine and all started modules."""
        if not self.is_running:
            return

        self.logger.info("Stopping THIF CORE engine")
        self.module_manager.stop_all()
        self.event_bus.publish("engine.stopped", {"engine": self})
        self.is_running = False

    def run(self) -> None:
        """Run the engine loop until a shutdown condition occurs."""
        self.start()
        try:
            while self.is_running:
                import time

                time.sleep(0.1)
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
        finally:
            self.stop()
