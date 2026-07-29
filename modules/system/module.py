from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.logger import get_logger
from core.module_manager import BaseModule
from .provider import SystemProvider

if TYPE_CHECKING:
    from core.engine import CoreEngine


class SystemModule(BaseModule):
    """System module implementation for THIF CORE."""

    def __init__(self) -> None:
        super().__init__(
            name="system",
            version="1.0.0",
            description="System information module",
            author="THIF CORE",
            dependencies=[],
        )
        self.logger = get_logger(name="thif_core.system")
        self.provider = SystemProvider(logger=self.logger)

    def initialize(self, engine: CoreEngine | None = None) -> None:
        self.logger.info("Starting system module...")
        info = self.provider.collect()
        if info:
            self.logger.info("System module loaded.")
            self.logger.info("System info: %s", info)
        else:
            self.logger.warning("System module loaded with missing information.")

    def shutdown(self) -> None:
        self.logger.info("Stopping system module")
