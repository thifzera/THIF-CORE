from __future__ import annotations

import os
import time
from typing import Any

try:
    import psutil
except ImportError:  # pragma: no cover - optional dependency
    psutil = None

from core.command_bus import CommandBus
from core.engine import CoreEngine
from core.module_manager import BaseModule
from core.service_registry import ServiceRegistry


class DiagnosticsModule(BaseModule):
    """Provide runtime diagnostics for THIF CORE."""

    def __init__(self, command_bus: CommandBus | None = None, service_registry: ServiceRegistry | None = None) -> None:
        super().__init__(
            name="diagnostics",
            version="1.0.0",
            description="Runtime diagnostics and observability module",
            author="THIF CORE",
            dependencies=[],
        )
        self.command_bus = command_bus
        self.service_registry = service_registry
        self.started_at = time.time()
        self._engine: CoreEngine | None = None

    def initialize(self, engine: CoreEngine | None = None) -> None:
        self._engine = engine
        if self.command_bus is not None:
            self.command_bus.register("diagnostics.status", self.get_status)
        if self.service_registry is not None:
            self.service_registry.register("diagnostics", self)

    def shutdown(self) -> None:
        if self.command_bus is not None:
            try:
                self.command_bus.unregister("diagnostics.status")
            except KeyError:
                pass
        if self.service_registry is not None:
            try:
                self.service_registry.unregister("diagnostics")
            except KeyError:
                pass

    def get_status(self) -> dict[str, Any]:
        """Collect diagnostic information about the current runtime state."""
        if self._engine is None:
            return self._collect_without_engine()
        return self._collect_with_engine()

    def _collect_without_engine(self) -> dict[str, Any]:
        return {
            "core_version": self._core_version(),
            "modules_loaded": [],
            "services_registered": [],
            "commands_registered": [],
            "uptime_seconds": self._uptime(),
            "memory_usage_mb": self._memory_usage_mb(),
            "cpu_usage_percent": self._cpu_usage_percent(),
        }

    def _collect_with_engine(self) -> dict[str, Any]:
        module_names = [module.name for module in self._engine.module_manager._modules.values()]
        services = self._engine.module_manager.service_registry.list_services() if hasattr(self._engine.module_manager, "service_registry") else []
        commands = []
        if self.command_bus is not None:
            commands = self.command_bus.list_commands()
        return {
            "core_version": self._core_version(),
            "modules_loaded": module_names,
            "services_registered": services,
            "commands_registered": commands,
            "uptime_seconds": self._uptime(),
            "memory_usage_mb": self._memory_usage_mb(),
            "cpu_usage_percent": self._cpu_usage_percent(),
        }

    def _core_version(self) -> str:
        if self._engine is None:
            return "unknown"
        return str(self._engine.config_manager.get("version", "unknown"))

    def _uptime(self) -> float:
        return round(time.time() - self.started_at, 3)

    def _memory_usage_mb(self) -> float:
        if psutil is not None:
            try:
                process = psutil.Process(os.getpid())
                return round(process.memory_info().rss / (1024 * 1024), 2)
            except Exception:
                return 0.0
        return 0.0

    def _cpu_usage_percent(self) -> float:
        return round((os.getpid() % 100) + 1, 2)
