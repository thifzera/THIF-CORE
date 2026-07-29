from __future__ import annotations

from enum import Enum
from pathlib import Path

from .config import ConfigManager
from .events import EventBus
from .logger import get_logger
from .module_manager import ModuleManager
from .scheduler import Scheduler


class EngineState(Enum):
    NOT_INITIALIZED = "not_initialized"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    SHUTDOWN = "shutdown"
    ERROR = "error"


class CoreEngine:
    """Main runtime orchestrator for THIF CORE."""

    def __init__(self, config_path: str | Path | None = None, module_manager: ModuleManager | None = None) -> None:
        self.config_manager = ConfigManager(config_path=config_path)
        self.logger = get_logger(
            name="thif_core",
            log_file=self.config_manager.get("logging.file"),
            level=self.config_manager.get("logging.level", "INFO"),
        )
        self.event_bus = EventBus()
        self.module_manager = module_manager or ModuleManager()
        self.scheduler = Scheduler()
        self.is_running = False
        self.state = EngineState.NOT_INITIALIZED

    def initialize(self) -> None:
        """Initialize engine resources and prepare for startup."""
        if self.state != EngineState.NOT_INITIALIZED:
            return

        self.logger.info("Initializing THIF CORE engine")
        self.state = EngineState.INITIALIZED

    def _log_boot_banner(self) -> None:
        """Log the THIF boot banner using the application logger."""
        self.logger.info("=== NÚCLEO THIF ===")

    def start(self) -> None:
        """Start the engine and all enabled modules."""
        if self.is_running:
            return

        if self.state == EngineState.NOT_INITIALIZED:
            self.initialize()

        self.logger.info("Starting THIF CORE engine")
        self._log_boot_banner()
        self.scheduler.start()
        self.is_running = True
        self.state = EngineState.RUNNING
        self.module_manager.boot(engine=self)

    def stop(self) -> None:
        """Stop the engine and all started modules."""
        if not self.is_running:
            return

        self.logger.info("Stopping THIF CORE engine")
        self.module_manager.stop_all()
        self.scheduler.stop()
        self.event_bus.publish("engine.stopped", {"engine": self})
        self.is_running = False
        self.state = EngineState.STOPPED

    def shutdown(self) -> None:
        """Shutdown the engine and release all resources."""
        if self.state == EngineState.SHUTDOWN:
            return

        self.stop()
        self.state = EngineState.SHUTDOWN

    def status(self) -> EngineState:
        """Return the current engine lifecycle state."""
        return self.state

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
